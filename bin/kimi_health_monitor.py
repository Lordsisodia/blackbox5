#!/usr/bin/env python3
"""
Kimi API Health Monitor
Periodic health checks and usage monitoring for all Kimi API keys
"""

import os
import sys
import time
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List
import requests
from pathlib import Path

# Add bin directory to path
sys.path.insert(0, '/opt/blackbox5/bin')

from kimi_load_balancer import KimiLoadBalancer

class KimiHealthMonitor:
    """Health monitoring for Kimi API keys"""

    def __init__(self, config_path: str = '/opt/blackbox5/config/kimi-keys.yaml'):
        self.lb = KimiLoadBalancer(config_path)
        self.db_path = '/opt/blackbox5/data/kimi_usage.db'
        self.log_file = Path('/opt/blackbox5/logs/kimi-health-check.log')
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def log(self, message: str):
        """Write to log file"""
        timestamp = datetime.now().isoformat()
        log_line = f"[{timestamp}] {message}\n"
        with open(self.log_file, 'a') as f:
            f.write(log_line)
        print(message)

    def check_key(self, key_id: str, key_name: str, api_key: str) -> Dict:
        """Perform health check on a single key"""
        start_time = time.time()
        result = {
            'key_id': key_id,
            'key_name': key_name,
            'timestamp': datetime.now().isoformat(),
            'status': 'unknown',
            'latency_ms': None,
            'error': None
        }

        try:
            # Make a minimal API request
            response = requests.post(
                f"{self.lb.config['kimi_api']['base_url']}/chat/completions",
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': self.lb.config['kimi_api']['model'],
                    'messages': [{'role': 'user', 'content': 'ping'}],
                    'max_tokens': 1
                },
                timeout=10
            )

            latency_ms = (time.time() - start_time) * 1000
            result['latency_ms'] = round(latency_ms, 2)

            if response.status_code == 200:
                result['status'] = 'healthy'
                self.log(f"✓ {key_name} ({key_id}) - healthy ({latency_ms:.0f}ms)")
            else:
                result['status'] = 'unhealthy'
                result['error'] = f"HTTP {response.status_code}"
                self.log(f"✗ {key_name} ({key_id}) - HTTP {response.status_code}")

        except requests.exceptions.Timeout:
            result['status'] = 'unhealthy'
            result['error'] = 'timeout'
            result['latency_ms'] = 10000
            self.log(f"✗ {key_name} ({key_id}) - timeout")

        except Exception as e:
            result['status'] = 'unhealthy'
            result['error'] = str(e)
            self.log(f"✗ {key_name} ({key_id}) - {str(e)}")

        return result

    def check_all_keys(self) -> List[Dict]:
        """Check all keys"""
        self.log("=" * 60)
        self.log(f"Starting health checks at {datetime.now().isoformat()}")
        self.log("=" * 60)

        results = []
        for key in self.lb.keys:
            result = self.check_key(key['key_id'], key['name'], key['api_key'])
            results.append(result)

            # Update load balancer stats
            if result['status'] == 'healthy':
                self.lb.stats[key['key_id']].consecutive_failures = 0
                if self.lb.stats[key['key_id']].status == 'disabled':
                    self.lb.stats[key['key_id']].status = 'active'
                    self.log(f"  → Re-enabled {key['name']}")
            else:
                stats = self.lb.stats[key['key_id']]
                stats.consecutive_failures += 1
                stats.last_error = result['error']
                stats.last_error_time = datetime.now().isoformat()

                if stats.consecutive_failures >= self.lb.config['failover']['max_failures_before_disable']:
                    stats.status = 'disabled'
                    self.log(f"  → Disabled {key['name']} after {stats.consecutive_failures} failures")

        # Write results to database
        self._write_health_results(results)

        # Print summary
        self._print_summary(results)

        return results

    def _write_health_results(self, results: List[Dict]):
        """Write health check results to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS health_checks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    key_id TEXT,
                    key_name TEXT,
                    status TEXT,
                    latency_ms REAL,
                    error_message TEXT
                )
            ''')

            # Insert results
            for result in results:
                cursor.execute('''
                    INSERT INTO health_checks (key_id, key_name, status, latency_ms, error_message)
                    VALUES (?, ?, ?, ?, ?)
                ''', (result['key_id'], result['key_name'], result['status'],
                      result['latency_ms'], result['error']))

            conn.commit()
            conn.close()

        except Exception as e:
            self.log(f"Failed to write health results: {e}")

    def _print_summary(self, results: List[Dict]):
        """Print health check summary"""
        healthy = sum(1 for r in results if r['status'] == 'healthy')
        unhealthy = len(results) - healthy
        avg_latency = sum(r['latency_ms'] or 0 for r in results) / len(results) if results else 0

        self.log(f"\nSummary: {healthy} healthy, {unhealthy} unhealthy")
        self.log(f"Average latency: {avg_latency:.0f}ms")
        self.log("=" * 60)

    def check_trial_expiration(self):
        """Check for upcoming trial key expirations"""
        self.log("\nChecking trial key expirations...")

        now = datetime.now()
        warning_days = self.lb.config['alerts']['trial_expiry_warning_days']
        warning_date = now + timedelta(days=warning_days)

        expiring_soon = []

        for key in self.lb.keys:
            if key.get('expires') and key['priority'] > 1:  # Trial keys only
                expire_date = datetime.strptime(key['expires'], '%Y-%m-%d')

                if now >= expire_date:
                    self.log(f"⚠ {key['name']} ({key['key_id']}) - EXPIRED on {key['expires']}")
                    self.lb.stats[key['key_id']].status = 'disabled'
                elif expire_date <= warning_date:
                    days_left = (expire_date - now).days
                    self.log(f"⚠ {key['name']} ({key['key_id']}) - expires in {days_left} days ({key['expires']})")
                    expiring_soon.append(key)

        if expiring_soon:
            self.log(f"\n⚠ {len(expiring_soon)} trial key(s) expiring within {warning_days} days")
        else:
            self.log("✓ No trial keys expiring soon")

    def check_usage_alerts(self):
        """Check for usage alerts"""
        self.log("\nChecking usage alerts...")

        alerts_triggered = []

        for key in self.lb.keys:
            key_id = key['key_id']
            stats = self.lb.stats[key_id]

            # Check error rate
            if stats.requests_total > 10:  # Only check if enough requests
                error_rate = stats.requests_failed / stats.requests_total
                threshold = self.lb.config['alerts']['key_error_rate_threshold']
                if error_rate > threshold:
                    alert = f"High error rate: {key['name']} ({error_rate:.1%} > {threshold:.1%})"
                    self.log(f"⚠ {alert}")
                    alerts_triggered.append(alert)

            # Check usage threshold
            if key.get('max_tokens') and stats.tokens_input > 0:
                usage_ratio = stats.tokens_input / key['max_tokens']
                threshold = self.lb.config['alerts']['key_usage_threshold']
                if usage_ratio > threshold:
                    alert = f"High usage: {key['name']} ({usage_ratio:.1%} > {threshold:.1%})"
                    self.log(f"⚠ {alert}")
                    alerts_triggered.append(alert)

        # Check global usage
        summary = self.lb.get_summary()
        for key in self.lb.keys:
            if key.get('max_tokens'):
                global_ratio = summary['total_tokens_input'] / (key['max_tokens'] * 9)  # 9 keys
                threshold = self.lb.config['alerts']['global_usage_threshold']
                if global_ratio > threshold:
                    alert = f"High global usage ({global_ratio:.1%} > {threshold:.1%})"
                    self.log(f"⚠ {alert}")
                    alerts_triggered.append(alert)

        if alerts_triggered:
            self.log(f"\n⚠ {len(alerts_triggered)} alert(s) triggered")
        else:
            self.log("✓ No usage alerts")

    def generate_report(self, hours: int = 24) -> Dict:
        """Generate health and usage report for the last N hours"""
        cutoff = datetime.now() - timedelta(hours=hours)

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get health check results
            cursor.execute('''
                SELECT key_id, key_name, status, AVG(latency_ms) as avg_latency, COUNT(*) as checks
                FROM health_checks
                WHERE timestamp > ?
                GROUP BY key_id
            ''', (cutoff.isoformat(),))
            health_results = cursor.fetchall()

            # Get usage data
            cursor.execute('''
                SELECT key_id, key_name,
                       SUM(tokens_input) as total_tokens_in,
                       SUM(tokens_output) as total_tokens_out,
                       SUM(cost) as total_cost,
                       COUNT(*) as requests,
                       SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful
                FROM usage
                WHERE timestamp > ?
                GROUP BY key_id
            ''', (cutoff.isoformat(),))
            usage_results = cursor.fetchall()

            conn.close()

            report = {
                'period_hours': hours,
                'generated_at': datetime.now().isoformat(),
                'health': {},
                'usage': {},
                'summary': {}
            }

            # Format health data
            for row in health_results:
                key_id, key_name, status, avg_latency, checks = row
                report['health'][key_id] = {
                    'key_name': key_name,
                    'status': status,
                    'avg_latency_ms': round(avg_latency, 2) if avg_latency else None,
                    'total_checks': checks
                }

            # Format usage data
            for row in usage_results:
                key_id, key_name, tokens_in, tokens_out, cost, requests, successful = row
                report['usage'][key_id] = {
                    'key_name': key_name,
                    'tokens_input': tokens_in or 0,
                    'tokens_output': tokens_out or 0,
                    'cost': round(cost or 0, 4),
                    'requests': requests,
                    'success_rate': round(successful / requests, 4) if requests else 0
                }

            # Calculate summary
            total_requests = sum(u['requests'] for u in report['usage'].values())
            total_cost = sum(u['cost'] for u in report['usage'].values())
            healthy_keys = sum(1 for h in report['health'].values() if h['status'] == 'healthy')

            report['summary'] = {
                'total_requests': total_requests,
                'total_cost': round(total_cost, 4),
                'healthy_keys': healthy_keys,
                'total_keys': len(report['health'])
            }

            return report

        except Exception as e:
            self.log(f"Failed to generate report: {e}")
            return {'error': str(e)}

    def run_once(self):
        """Run a single health check cycle"""
        self.check_all_keys()
        self.check_trial_expiration()
        self.check_usage_alerts()

    def run_continuous(self, interval_minutes: int = 60):
        """Run continuous health checks"""
        self.log(f"\nStarting continuous health monitoring (interval: {interval_minutes} minutes)")
        self.log("Press Ctrl+C to stop\n")

        try:
            while True:
                self.run_once()
                self.log(f"\nWaiting {interval_minutes} minutes until next check...\n")
                time.sleep(interval_minutes * 60)
        except KeyboardInterrupt:
            self.log("\nStopping health monitor...")
            self.log(f"Final report:")
            report = self.generate_report()
            print(json.dumps(report, indent=2))

def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description='Kimi API Health Monitor')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    parser.add_argument('--interval', type=int, default=60, help='Check interval in minutes')
    parser.add_argument('--report', type=int, metavar='HOURS', help='Generate report for last N hours')
    args = parser.parse_args()

    monitor = KimiHealthMonitor()

    if args.report:
        report = monitor.generate_report(args.report)
        print(json.dumps(report, indent=2))
    elif args.once:
        monitor.run_once()
    else:
        monitor.run_continuous(args.interval)

if __name__ == '__main__':
    main()
