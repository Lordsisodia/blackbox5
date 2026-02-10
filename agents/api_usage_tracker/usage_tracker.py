"""
API Usage Tracker - Monitor and track API usage across all providers
Provides usage statistics, cost estimation, and rate limit monitoring.
"""

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class ProviderUsage:
    """Usage statistics for a single provider"""
    provider_id: str
    requests: int
    total_tokens: int
    avg_duration_ms: float
    success_rate: float
    error_rate: float
    estimated_cost: float = 0.0
    last_used: Optional[datetime] = None


@dataclass
class UsageAlert:
    """Alert generated based on usage patterns"""
    level: str  # info, warning, critical
    message: str
    provider: str
    metric: str
    value: float
    threshold: float
    timestamp: datetime = field(default_factory=datetime.utcnow)


class APIUsageTracker:
    """
    Tracks API usage across all providers for cost optimization and monitoring.
    """

    def __init__(self, db_path: str = None, config_path: str = None):
        """Initialize usage tracker"""
        self.db_path = db_path or "/opt/blackbox5/data/api-usage.db"
        self.config_path = config_path or "/opt/blackbox5/config/api-keys.yaml"
        self.provider_costs: Dict[str, Dict] = {}

        self.init_db()
        self.load_costs()

    def init_db(self):
        """Initialize database schema"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Main usage table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                provider TEXT NOT NULL,
                api_key_id TEXT,
                agent TEXT,
                task_type TEXT,
                tokens_used INTEGER DEFAULT 0,
                request_duration_ms INTEGER,
                success BOOLEAN DEFAULT 1,
                error_message TEXT
            )
        ''')

        # Rate limit tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rate_limits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                provider TEXT NOT NULL,
                api_key_id TEXT,
                requests_count INTEGER DEFAULT 0,
                tokens_count INTEGER DEFAULT 0,
                window_start DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Indexes for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_usage_provider ON api_usage(provider)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_usage_timestamp ON api_usage(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_usage_agent ON api_usage(agent)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_rate_provider ON rate_limits(provider, window_start)')

        conn.commit()
        conn.close()

        logger.info(f"Initialized usage tracker database: {self.db_path}")

    def load_costs(self):
        """Load cost configuration from API keys config"""
        import yaml

        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)

            providers = config.get('providers', {})
            for provider_id, provider_config in providers.items():
                if 'costs' in provider_config:
                    self.provider_costs[provider_id] = {
                        'input_per_million': provider_config['costs'].get('input_per_million', 0),
                        'output_per_million': provider_config['costs'].get('output_per_million', 0),
                        'currency': provider_config['costs'].get('currency', 'USD')
                    }

            logger.info(f"Loaded cost configuration for {len(self.provider_costs)} providers")

        except Exception as e:
            logger.warning(f"Could not load cost configuration: {e}")

    def track_usage(
        self,
        provider: str,
        agent: str = None,
        task_type: str = None,
        tokens_used: int = 0,
        duration_ms: int = 0,
        success: bool = True,
        error_message: str = None,
        api_key_id: str = None
    ) -> int:
        """
        Track API usage.

        Returns:
            Row ID of inserted record
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO api_usage
                (provider, api_key_id, agent, task_type, tokens_used, request_duration_ms, success, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (provider, api_key_id, agent, task_type, tokens_used, duration_ms, success, error_message))

            row_id = cursor.lastrowid
            conn.commit()
            conn.close()

            logger.debug(f"Tracked usage: {provider} {tokens_used} tokens")

            return row_id

        except Exception as e:
            logger.error(f"Error tracking usage: {e}")
            return 0

    def update_rate_limit(
        self,
        provider: str,
        api_key_id: str = None,
        requests_delta: int = 1,
        tokens_delta: int = 0
    ):
        """Update rate limit tracking for a provider"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get current minute window
            window_start = datetime.utcnow().replace(second=0, microsecond=0)

            # Check if entry exists for this window
            cursor.execute('''
                SELECT id, requests_count, tokens_count
                FROM rate_limits
                WHERE provider = ? AND api_key_id = ? AND window_start = ?
            ''', (provider, api_key_id or 'default', window_start.isoformat()))

            row = cursor.fetchone()

            if row:
                # Update existing entry
                cursor.execute('''
                    UPDATE rate_limits
                    SET requests_count = requests_count + ?,
                        tokens_count = tokens_count + ?
                    WHERE id = ?
                ''', (requests_delta, tokens_delta, row[0]))
            else:
                # Create new entry
                cursor.execute('''
                    INSERT INTO rate_limits
                    (provider, api_key_id, requests_count, tokens_delta, window_start)
                    VALUES (?, ?, ?, ?, ?)
                ''', (provider, api_key_id or 'default', requests_delta, tokens_delta, window_start.isoformat()))

            conn.commit()
            conn.close()

        except Exception as e:
            logger.error(f"Error updating rate limit: {e}")

    def get_rate_limits(self, provider: str, api_key_id: str = None) -> Dict[str, int]:
        """Get current rate limit status for a provider"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get current minute's usage
            window_start = datetime.utcnow().replace(second=0, microsecond=0)
            window_end = window_start + timedelta(minutes=1)

            cursor.execute('''
                SELECT COALESCE(SUM(requests_count), 0), COALESCE(SUM(tokens_count), 0)
                FROM rate_limits
                WHERE provider = ?
                AND api_key_id = ?
                AND window_start >= ?
            ''', (provider, api_key_id or 'default', window_start.isoformat()))

            requests, tokens = cursor.fetchone()

            conn.close()

            return {
                "requests_this_minute": requests or 0,
                "tokens_this_minute": tokens or 0
            }

        except Exception as e:
            logger.error(f"Error getting rate limits: {e}")
            return {"requests_this_minute": 0, "tokens_this_minute": 0}

    def get_stats(
        self,
        provider: str = None,
        agent: str = None,
        task_type: str = None,
        days: int = 7,
        group_by: str = None  # provider, agent, task_type, hour, day
    ) -> Dict[str, Any]:
        """
        Get usage statistics.

        Args:
            provider: Filter by provider
            agent: Filter by agent
            task_type: Filter by task type
            days: Number of days to look back
            group_by: Group results by field

        Returns:
            Dictionary with usage statistics
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Build query
            query = '''
                SELECT
                    COUNT(*) as requests,
                    SUM(tokens_used) as total_tokens,
                    AVG(request_duration_ms) as avg_duration,
                    SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful,
                    SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failed,
                    MIN(timestamp) as first_seen,
                    MAX(timestamp) as last_seen
                FROM api_usage
                WHERE timestamp >= datetime('now', ?)
            '''

            params = [f'-{days} days']

            conditions = []
            if provider:
                conditions.append("provider = ?")
                params.append(provider)
            if agent:
                conditions.append("agent = ?")
                params.append(agent)
            if task_type:
                conditions.append("task_type = ?")
                params.append(task_type)

            if conditions:
                query += ' AND ' + ' AND '.join(conditions)

            # Add grouping
            if group_by:
                query = query.replace(
                    "SELECT",
                    f"SELECT {group_by},"
                )
                query += f" GROUP BY {group_by}"

            cursor.execute(query, params)
            rows = cursor.fetchall()

            conn.close()

            # Process results
            stats = {}

            if group_by:
                for row in rows:
                    key = row[0]
                    requests, total_tokens, avg_duration, successful, failed, first_seen, last_seen = row[1:]

                    stats[key] = {
                        "requests": requests or 0,
                        "total_tokens": total_tokens or 0,
                        "avg_duration_ms": round(avg_duration or 0, 2),
                        "success_rate": round((successful / requests * 100) if requests > 0 else 0, 2),
                        "error_rate": round((failed / requests * 100) if requests > 0 else 0, 2),
                        "estimated_cost": self._estimate_cost(group_by.replace("'", ""), total_tokens or 0),
                        "first_seen": first_seen,
                        "last_seen": last_seen
                    }
            else:
                if rows:
                    row = rows[0]
                    requests, total_tokens, avg_duration, successful, failed, first_seen, last_seen = row

                    stats = {
                        "requests": requests or 0,
                        "total_tokens": total_tokens or 0,
                        "avg_duration_ms": round(avg_duration or 0, 2),
                        "success_rate": round((successful / requests * 100) if requests > 0 else 0, 2),
                        "error_rate": round((failed / requests * 100) if requests > 0 else 0, 2),
                        "estimated_cost": self._estimate_cost(provider, total_tokens or 0),
                        "first_seen": first_seen,
                        "last_seen": last_seen
                    }

            return stats

        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {}

    def _estimate_cost(self, provider: str, tokens: int) -> float:
        """Estimate cost for tokens used by provider"""
        if not provider or provider not in self.provider_costs:
            return 0.0

        costs = self.provider_costs[provider]
        input_cost = (tokens * 0.5 * costs['input_per_million']) / 1_000_000  # Assume 50% input
        output_cost = (tokens * 0.5 * costs['output_per_million']) / 1_000_000  # Assume 50% output

        return round(input_cost + output_cost, 4)

    def get_provider_stats(self, days: int = 7) -> Dict[str, ProviderUsage]:
        """Get statistics grouped by provider"""
        stats = self.get_stats(days=days, group_by='provider')

        provider_stats = {}
        for provider_id, data in stats.items():
            provider_stats[provider_id] = ProviderUsage(
                provider_id=provider_id,
                requests=data.get('requests', 0),
                total_tokens=data.get('total_tokens', 0),
                avg_duration_ms=data.get('avg_duration_ms', 0),
                success_rate=data.get('success_rate', 0),
                error_rate=data.get('error_rate', 0),
                estimated_cost=data.get('estimated_cost', 0.0),
                last_seen=datetime.fromisoformat(data['last_seen']) if data.get('last_seen') else None
            )

        return provider_stats

    def check_alerts(self) -> List[UsageAlert]:
        """Check for usage alerts based on configured thresholds"""
        alerts = []

        # Load configuration
        import yaml
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)

            global_alerts = config.get('global_settings', {}).get('alerts', {})

            # Check error rates
            provider_stats = self.get_provider_stats(days=1)
            for provider_id, stats in provider_stats.items():
                if stats.requests > 10:  # Only alert if enough data
                    error_rate = stats.error_rate
                    threshold = global_alerts.get('error_rate_threshold', 0.10) * 100

                    if error_rate >= threshold:
                        alerts.append(UsageAlert(
                            level="critical" if error_rate > threshold * 2 else "warning",
                            message=f"High error rate: {error_rate:.1f}%",
                            provider=provider_id,
                            metric="error_rate",
                            value=error_rate,
                            threshold=threshold
                        ))

                    # Check latency
                    if stats.avg_duration_ms > 5000:
                        alerts.append(UsageAlert(
                            level="warning",
                            message=f"High latency: {stats.avg_duration_ms:.0f}ms",
                            provider=provider_id,
                            metric="avg_latency_ms",
                            value=stats.avg_duration_ms,
                            threshold=5000
                        ))

        except Exception as e:
            logger.warning(f"Could not check alerts: {e}")

        return alerts

    def generate_report(self, days: int = 7) -> Dict[str, Any]:
        """Generate comprehensive usage report"""
        provider_stats = self.get_provider_stats(days=days)
        alerts = self.check_alerts()

        # Calculate totals
        total_requests = sum(p.requests for p in provider_stats.values())
        total_tokens = sum(p.total_tokens for p in provider_stats.values())
        total_cost = sum(p.estimated_cost for p in provider_stats.values())
        avg_success_rate = sum(p.success_rate * p.requests for p in provider_stats.values()) / total_requests if total_requests > 0 else 0

        return {
            "period_days": days,
            "summary": {
                "total_requests": total_requests,
                "total_tokens": total_tokens,
                "total_cost": round(total_cost, 4),
                "avg_success_rate": round(avg_success_rate, 2)
            },
            "by_provider": {
                pid: {
                    "requests": p.requests,
                    "total_tokens": p.total_tokens,
                    "avg_duration_ms": p.avg_duration_ms,
                    "success_rate": p.success_rate,
                    "error_rate": p.error_rate,
                    "estimated_cost": p.estimated_cost,
                    "last_used": p.last_used.isoformat() if p.last_used else None
                }
                for pid, p in provider_stats.items()
            },
            "alerts": [
                {
                    "level": a.level,
                    "message": a.message,
                    "provider": a.provider,
                    "metric": a.metric,
                    "value": a.value,
                    "threshold": a.threshold,
                    "timestamp": a.timestamp.isoformat()
                }
                for a in alerts
            ],
            "generated_at": datetime.utcnow().isoformat()
        }

    def cleanup_old_data(self, retention_days: int = 90):
        """Remove old usage data beyond retention period"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Clean usage records
            cursor.execute('''
                DELETE FROM api_usage
                WHERE timestamp < datetime('now', ?)
            ''', (f'-{retention_days} days',))

            usage_deleted = cursor.rowcount

            # Clean rate limit records (keep only last 24 hours)
            cursor.execute('''
                DELETE FROM rate_limits
                WHERE window_start < datetime('now', '-1 day')
            ''')

            rate_deleted = cursor.rowcount

            conn.commit()
            conn.close()

            logger.info(f"Cleaned up {usage_deleted} usage records and {rate_deleted} rate limit records")

        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")


# CLI for testing
if __name__ == "__main__":
    tracker = APIUsageTracker()

    print("=== API Usage Tracker Test ===\n")

    # Track some test data
    tracker.track_usage("kimi", "main", "coding", 5000, 1234, True)
    tracker.track_usage("glm", "main", "general", 3000, 800, True)
    tracker.track_usage("claude_code", "planner", "reasoning", 10000, 2000, True)

    # Get stats
    stats = tracker.get_stats(days=7)
    print(f"Overall stats (last 7 days): {json.dumps(stats, indent=2, default=str)}\n")

    # Get provider stats
    provider_stats = tracker.get_provider_stats(days=7)
    for provider_id, usage in provider_stats.items():
        print(f"{provider_id}:")
        print(f"  Requests: {usage.requests}")
        print(f"  Tokens: {usage.total_tokens:,}")
        print(f"  Success rate: {usage.success_rate}%")
        print(f"  Estimated cost: ${usage.estimated_cost:.4f}")
        print()

    # Check alerts
    alerts = tracker.check_alerts()
    if alerts:
        print("Alerts:")
        for alert in alerts:
            print(f"  [{alert.level.upper()}] {alert.provider}: {alert.message}")
    else:
        print("No alerts")

    # Generate report
    report = tracker.generate_report()
    print(f"\n=== Report ===")
    print(json.dumps(report, indent=2, default=str))
