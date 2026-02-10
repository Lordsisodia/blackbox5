#!/usr/bin/env python3
"""
Kimi API Load Balancer for BlackBox5
Implements intelligent load balancing across 9 Kimi API keys with health monitoring and usage tracking
"""

import os
import yaml
import json
import sqlite3
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
from dataclasses import dataclass, asdict
import threading
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/opt/blackbox5/logs/kimi-load-balancer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('kimi_load_balancer')

@dataclass
class KeyStats:
    """Statistics for an API key"""
    name: str
    key_id: str
    requests_total: int = 0
    requests_success: int = 0
    requests_failed: int = 0
    tokens_input: int = 0
    tokens_output: int = 0
    last_used: Optional[str] = None
    last_error: Optional[str] = None
    last_error_time: Optional[str] = None
    consecutive_failures: int = 0
    cost_total: float = 0.0
    status: str = "active"  # active, degraded, disabled

class KimiLoadBalancer:
    """Main load balancer class"""

    def __init__(self, config_path: str = '/opt/blackbox5/config/kimi-keys.yaml'):
        self.config_path = config_path
        self.config = self._load_config()
        self.keys = self._parse_keys()
        self.stats: Dict[str, KeyStats] = self._init_stats()
        self.current_rotation_index = 0
        self.db_path = '/opt/blackbox5/data/kimi_usage.db'
        self._init_database()
        self._lock = threading.Lock()

    def _load_config(self) -> dict:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            raise

    def _parse_keys(self) -> List[dict]:
        """Parse and expand environment variables in keys"""
        parsed_keys = []
        for key in self.config['keys']:
            key_copy = key.copy()
            # Expand environment variables in api_key
            api_key = key_copy['api_key']
            if api_key.startswith('${') and api_key.endswith('}'):
                env_var = api_key[2:-1]
                key_copy['api_key'] = os.getenv(env_var, '')
            parsed_keys.append(key_copy)
        return parsed_keys

    def _init_stats(self) -> Dict[str, KeyStats]:
        """Initialize statistics for all keys"""
        stats = {}
        for key in self.keys:
            stats[key['key_id']] = KeyStats(
                name=key['name'],
                key_id=key['key_id'],
                status=key.get('status', 'active')
            )
        return stats

    def _init_database(self):
        """Initialize SQLite database for usage tracking"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create usage table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                key_id TEXT,
                key_name TEXT,
                agent TEXT,
                task_type TEXT,
                tokens_input INTEGER,
                tokens_output INTEGER,
                success INTEGER,
                error_message TEXT,
                cost REAL
            )
        ''')

        # Create key_health table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS key_health (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                key_id TEXT,
                status TEXT,
                error_rate REAL,
                avg_latency REAL,
                consecutive_failures INTEGER
            )
        ''')

        conn.commit()
        conn.close()

    def _get_healthy_keys(self, agent: Optional[str] = None) -> List[dict]:
        """Get list of healthy, active keys"""
        healthy_keys = []
        now = datetime.now()

        for key in self.keys:
            key_id = key['key_id']
            stats = self.stats.get(key_id)

            # Skip disabled keys
            if not stats or stats.status == 'disabled':
                continue

            # Check expiration
            if key.get('expires'):
                expire_date = datetime.strptime(key['expires'], '%Y-%m-%d')
                if now >= expire_date:
                    logger.warning(f"Key {key['name']} has expired")
                    stats.status = 'disabled'
                    continue

            # Check if key has too many consecutive failures
            if stats.consecutive_failures >= self.config['failover']['max_failures_before_disable']:
                stats.status = 'disabled'
                logger.warning(f"Key {key['name']} disabled due to {stats.consecutive_failures} consecutive failures")
                continue

            # Check if key is assigned to this agent (if specified)
            if agent and 'assigned_agents' in key:
                if agent not in key['assigned_agents']:
                    # Check if it's a CISO key (fallback for any agent)
                    if key['priority'] != 1:
                        continue

            healthy_keys.append(key)

        return healthy_keys

    def get_key(self, agent: Optional[str] = None, task_type: Optional[str] = None) -> Optional[Tuple[str, str]]:
        """
        Get an API key based on load balancing strategy
        Returns: (key_id, api_key) or None
        """
        with self._lock:
            strategy = self.config['load_balancing']['strategy']
            healthy_keys = self._get_healthy_keys(agent)

            if not healthy_keys:
                logger.error("No healthy keys available!")
                return None

            selected_key = None

            if strategy == 'round-robin':
                selected_key = self._round_robin_select(healthy_keys)
            elif strategy == 'least-used':
                selected_key = self._least_used_select(healthy_keys)
            elif strategy == 'priority':
                selected_key = self._priority_select(healthy_keys)
            elif strategy == 'health-first':
                # Try priority first, then round-robin
                selected_key = self._priority_select(healthy_keys)
                if not selected_key:
                    selected_key = self._round_robin_select(healthy_keys)
            else:
                # Default to round-robin
                selected_key = self._round_robin_select(healthy_keys)

            if selected_key:
                return selected_key['key_id'], selected_key['api_key']
            return None

    def _round_robin_select(self, keys: List[dict]) -> Optional[dict]:
        """Round-robin key selection"""
        if not keys:
            return None

        key = keys[self.current_rotation_index % len(keys)]
        self.current_rotation_index += 1
        return key

    def _least_used_select(self, keys: List[dict]) -> Optional[dict]:
        """Select key with lowest usage"""
        if not keys:
            return None

        # Sort by total requests
        sorted_keys = sorted(keys, key=lambda k: self.stats[k['key_id']].requests_total)
        return sorted_keys[0]

    def _priority_select(self, keys: List[dict]) -> Optional[dict]:
        """Select key by priority (lowest number = highest priority)"""
        if not keys:
            return None

        # Sort by priority
        sorted_keys = sorted(keys, key=lambda k: k['priority'])

        # Check if primary key is healthy
        for key in sorted_keys:
            if key['priority'] == 1:  # CISO key
                stats = self.stats[key['key_id']]
                if stats.status == 'active' and stats.consecutive_failures == 0:
                    return key

        # Return highest priority healthy key
        for key in sorted_keys:
            stats = self.stats[key['key_id']]
            if stats.status == 'active':
                return key

        return None

    def record_usage(self, key_id: str, agent: str, task_type: str,
                     tokens_input: int, tokens_output: int,
                     success: bool, error_message: Optional[str] = None,
                     latency_ms: Optional[int] = None):
        """Record API usage for a key"""
        with self._lock:
            if key_id not in self.stats:
                logger.warning(f"Unknown key_id: {key_id}")
                return

            stats = self.stats[key_id]
            now = datetime.now().isoformat()

            # Update stats
            stats.requests_total += 1
            if success:
                stats.requests_success += 1
                stats.tokens_input += tokens_input
                stats.tokens_output += tokens_output
                stats.consecutive_failures = 0
                stats.last_error = None
                stats.last_error_time = None
            else:
                stats.requests_failed += 1
                stats.consecutive_failures += 1
                stats.last_error = error_message
                stats.last_error_time = now

                # Check if key should be disabled
                if stats.consecutive_failures >= self.config['failover']['max_failures_before_disable']:
                    stats.status = 'disabled'
                    logger.error(f"Key {key_id} disabled after {stats.consecutive_failures} failures")

            stats.last_used = now

            # Calculate cost
            cost = self._calculate_cost(tokens_input, tokens_output)
            stats.cost_total += cost

            # Write to database
            self._write_usage_db(key_id, stats.name, agent, task_type,
                                 tokens_input, tokens_output, success,
                                 error_message, cost)

            # Update health database
            self._write_health_db(key_id, stats, latency_ms)

    def _calculate_cost(self, tokens_input: int, tokens_output: int) -> float:
        """Calculate cost based on token usage"""
        costs = self.config['costs']
        input_cost = (tokens_input / 1_000_000) * costs['input_tokens_per_million']
        output_cost = (tokens_output / 1_000_000) * costs['output_tokens_per_million']
        return input_cost + output_cost

    def _write_usage_db(self, key_id: str, key_name: str, agent: str, task_type: str,
                        tokens_input: int, tokens_output: int, success: bool,
                        error_message: Optional[str], cost: float):
        """Write usage to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usage (key_id, key_name, agent, task_type, tokens_input,
                                   tokens_output, success, error_message, cost)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (key_id, key_name, agent, task_type, tokens_input,
                  tokens_output, 1 if success else 0, error_message, cost))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to write to usage DB: {e}")

    def _write_health_db(self, key_id: str, stats: KeyStats, latency_ms: Optional[int]):
        """Write health stats to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Calculate error rate
            error_rate = 0.0
            if stats.requests_total > 0:
                error_rate = stats.requests_failed / stats.requests_total

            cursor.execute('''
                INSERT INTO key_health (key_id, status, error_rate,
                                         avg_latency, consecutive_failures)
                VALUES (?, ?, ?, ?, ?)
            ''', (key_id, stats.status, error_rate, latency_ms, stats.consecutive_failures))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to write to health DB: {e}")

    def health_check(self, key_id: str) -> bool:
        """Perform health check on a key"""
        key = next((k for k in self.keys if k['key_id'] == key_id), None)
        if not key:
            return False

        try:
            # Simple health check - make a minimal API request
            response = requests.post(
                f"{self.config['kimi_api']['base_url']}/chat/completions",
                headers={
                    'Authorization': f'Bearer {key["api_key"]}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': self.config['kimi_api']['model'],
                    'messages': [{'role': 'user', 'content': 'ping'}],
                    'max_tokens': 1
                },
                timeout=10
            )

            success = response.status_code == 200
            if not success:
                logger.warning(f"Health check failed for {key_id}: {response.status_code}")

            return success

        except Exception as e:
            logger.error(f"Health check error for {key_id}: {e}")
            return False

    def check_all_keys(self):
        """Perform health check on all keys"""
        for key in self.keys:
            key_id = key['key_id']
            stats = self.stats.get(key_id)

            if not stats:
                continue

            # Skip keys that are currently disabled (but recheck periodically)
            if stats.status == 'disabled':
                # Recheck every 5 minutes
                if stats.last_error_time:
                    last_error = datetime.fromisoformat(stats.last_error_time)
                    if (datetime.now() - last_error).seconds < 300:
                        continue

            # Perform health check
            is_healthy = self.health_check(key_id)

            if is_healthy:
                if stats.status == 'disabled':
                    stats.status = 'active'
                    stats.consecutive_failures = 0
                    logger.info(f"Key {key_id} re-enabled after health check")
            else:
                stats.consecutive_failures += 1
                if stats.consecutive_failures >= self.config['failover']['max_failures_before_disable']:
                    stats.status = 'disabled'
                    logger.error(f"Key {key_id} disabled after health check failure")

    def get_stats(self) -> Dict:
        """Get current statistics for all keys"""
        with self._lock:
            stats_dict = {}
            for key_id, stats in self.stats.items():
                stats_dict[key_id] = asdict(stats)
            return stats_dict

    def get_summary(self) -> Dict:
        """Get usage summary across all keys"""
        with self._lock:
            total_requests = sum(s.requests_total for s in self.stats.values())
            total_success = sum(s.requests_success for s in self.stats.values())
            total_tokens_in = sum(s.tokens_input for s in self.stats.values())
            total_tokens_out = sum(s.tokens_output for s in self.stats.values())
            total_cost = sum(s.cost_total for s in self.stats.values())

            active_keys = sum(1 for s in self.stats.values() if s.status == 'active')
            disabled_keys = sum(1 for s in self.stats.values() if s.status == 'disabled')

            return {
                'total_requests': total_requests,
                'total_success': total_success,
                'total_failed': total_requests - total_success,
                'success_rate': total_success / total_requests if total_requests > 0 else 0,
                'total_tokens_input': total_tokens_in,
                'total_tokens_output': total_tokens_out,
                'total_cost': total_cost,
                'active_keys': active_keys,
                'disabled_keys': disabled_keys,
                'currency': self.config['costs']['currency']
            }

def main():
    """Main function for testing"""
    lb = KimiLoadBalancer()

    # Test key selection
    print("Testing key selection:")
    for i in range(5):
        key = lb.get_key(agent='main', task_type='planning')
        print(f"  Request {i+1}: {key}")

    # Print summary
    print("\nSummary:")
    print(json.dumps(lb.get_summary(), indent=2))

if __name__ == '__main__':
    main()
