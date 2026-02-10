#!/usr/bin/env python3
"""
Flask API server for Kimi Load Balancer Dashboard
Provides REST endpoints for the dashboard UI
"""

import os
import sys
import json
from datetime import datetime, timedelta
from flask import Flask, jsonify, send_from_directory
from pathlib import Path
import sqlite3

# Add bin directory to path
sys.path.insert(0, '/opt/blackbox5/bin')

from kimi_load_balancer import KimiLoadBalancer

app = Flask(__name__)

# Initialize load balancer
lb = KimiLoadBalancer()
db_path = '/opt/blackbox5/data/kimi_usage.db'

@app.route('/')
def index():
    """Serve dashboard HTML"""
    return send_from_directory('/opt/blackbox5/dashboard-ui', 'kimi-dashboard.html')

@app.route('/api/kimi/summary')
def get_summary():
    """Get usage summary"""
    return jsonify(lb.get_summary())

@app.route('/api/kimi/stats')
def get_stats():
    """Get detailed stats for all keys"""
    return jsonify(lb.get_stats())

@app.route('/api/kimi/health')
def get_health():
    """Get recent health check results"""
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Get last 10 health checks per key
        cursor.execute('''
            SELECT key_id, key_name, status, latency_ms, timestamp
            FROM health_checks
            WHERE timestamp > datetime('now', '-1 hour')
            ORDER BY timestamp DESC
            LIMIT 50
        ''')

        results = []
        for row in cursor.fetchall():
            results.append({
                'key_id': row['key_id'],
                'key_name': row['key_name'],
                'status': row['status'],
                'latency_ms': row['latency_ms'],
                'timestamp': row['timestamp']
            })

        conn.close()
        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/kimi/usage/<int:hours>')
def get_usage(hours=24):
    """Get usage data for last N hours"""
    try:
        cutoff = datetime.now() - timedelta(hours=hours)

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                key_id,
                key_name,
                SUM(tokens_input) as tokens_input,
                SUM(tokens_output) as tokens_output,
                SUM(cost) as cost,
                COUNT(*) as requests,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful
            FROM usage
            WHERE timestamp > ?
            GROUP BY key_id
            ORDER BY tokens_input DESC
        ''', (cutoff.isoformat(),))

        results = []
        for row in cursor.fetchall():
            results.append({
                'key_id': row['key_id'],
                'key_name': row['key_name'],
                'tokens_input': row['tokens_input'] or 0,
                'tokens_output': row['tokens_output'] or 0,
                'cost': row['cost'] or 0,
                'requests': row['requests'],
                'successful': row['successful']
            })

        conn.close()
        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/kimi/alerts')
def get_alerts():
    """Get current alerts"""
    alerts = []

    # Check for disabled keys
    for key_id, stats in lb.get_stats().items():
        if stats['status'] == 'disabled':
            alerts.append({
                'type': 'error',
                'message': f"Key {stats['name']} is disabled"
            })

    # Check for high error rates
    for key_id, stats in lb.get_stats().items():
        if stats['requests_total'] > 10:
            error_rate = stats['requests_failed'] / stats['requests_total']
            if error_rate > 0.10:  # 10% threshold
                alerts.append({
                    'type': 'warning',
                    'message': f"Key {stats['name']} has high error rate: {error_rate:.1%}"
                })

    # Check for expiring trial keys
    now = datetime.now()
    warning_date = now + timedelta(days=7)

    for key in lb.keys:
        if key.get('expires') and key['priority'] > 1:
            expire_date = datetime.strptime(key['expires'], '%Y-%m-%d')
            if expire_date <= warning_date:
                days_left = (expire_date - now).days
                alerts.append({
                    'type': 'warning',
                    'message': f"Trial key {key['name']} expires in {days_left} days"
                })

    return jsonify(alerts)

@app.route('/api/kimi/trigger-health-check', methods=['POST'])
def trigger_health_check():
    """Trigger immediate health check"""
    try:
        from kimi_health_monitor import KimiHealthMonitor
        monitor = KimiHealthMonitor()
        results = monitor.check_all_keys()
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def main():
    """Main function"""
    print("=" * 60)
    print("Kimi Load Balancer Dashboard API Server")
    print("=" * 60)
    print()
    print("Dashboard: http://localhost:5000")
    print("API endpoints:")
    print("  GET  /api/kimi/summary")
    print("  GET  /api/kimi/stats")
    print("  GET  /api/kimi/health")
    print("  GET  /api/kimi/usage/<hours>")
    print("  GET  /api/kimi/alerts")
    print("  POST /api/kimi/trigger-health-check")
    print()

    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()
