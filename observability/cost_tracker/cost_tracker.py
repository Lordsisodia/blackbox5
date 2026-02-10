#!/usr/bin/env python3
"""
Cost Tracker for BlackBox5 Observability System.

Tracks token usage and costs across all APIs and agents.
Supports OpenAI, Claude, Kimi, Google, and other providers.
"""

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Parent imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "bin" / "lib"))

from health_monitor.database import _get_connection

logger = logging.getLogger(__name__)


class APIProvider(Enum):
    """Supported API providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"  # Claude
    KIMI = "kimi"
    GOOGLE = "google"
    COHERE = "cohere"
    MISTRAL = "mistral"
    AZURE = "azure"
    UNKNOWN = "unknown"


class ModelType(Enum):
    """Model types for cost calculation."""
    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    CLAUDE_3_OPUS = "claude-3-opus"
    CLAUDE_3_SONNET = "claude-3-sonnet"
    CLAUDE_3_HAIKU = "claude-3-haiku"
    CLAUDE_3_5_SONNET = "claude-3-5-sonnet"
    KIMI_MOONSHOT = "kimi-moonshot"
    GEMINI_PRO = "gemini-pro"
    GEMINI_ULTRA = "gemini-ultra"
    UNKNOWN = "unknown"


# Pricing per 1M tokens (input/output)
PRICING = {
    # OpenAI pricing (as of 2025)
    ModelType.GPT_4: (30.0, 60.0),
    ModelType.GPT_4_TURBO: (10.0, 30.0),
    ModelType.GPT_3_5_TURBO: (0.5, 1.5),
    ModelType.GPT_4O: (5.0, 15.0),
    ModelType.GPT_4O_MINI: (0.15, 0.6),
    ModelType.GPT_4: (30.0, 60.0),

    # Claude pricing
    ModelType.CLAUDE_3_OPUS: (15.0, 75.0),
    ModelType.CLAUDE_3_SONNET: (3.0, 15.0),
    ModelType.CLAUDE_3_HAIKU: (0.25, 1.25),
    ModelType.CLAUDE_3_5_SONNET: (3.0, 15.0),

    # Kimi pricing (approximate)
    ModelType.KIMI_MOONSHOT: (2.0, 6.0),

    # Google pricing (approximate)
    ModelType.GEMINI_PRO: (0.5, 1.5),
    ModelType.GEMINI_ULTRA: (7.0, 21.0),

    # Defaults
    ModelType.UNKNOWN: (1.0, 3.0),
}


@dataclass
class APICall:
    """Represents a single API call."""
    timestamp: datetime
    agent: str
    provider: APIProvider
    model: ModelType
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost_usd: float
    request_id: Optional[str] = None
    success: bool = True
    error: Optional[str] = None
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "agent": self.agent,
            "provider": self.provider.value,
            "model": self.model.value,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "cost_usd": self.cost_usd,
            "request_id": self.request_id,
            "success": self.success,
            "error": self.error,
            "metadata": self.metadata,
        }


@dataclass
class CostSummary:
    """Summary of costs for a period."""
    start_date: datetime
    end_date: datetime
    total_cost: float
    total_tokens: int
    total_calls: int
    successful_calls: int
    failed_calls: int
    by_provider: Dict[str, float]
    by_model: Dict[str, float]
    by_agent: Dict[str, float]


class CostTracker:
    """Main cost tracking class."""

    def __init__(self, db_path: Optional[Path] = None):
        """Initialize cost tracker."""
        if db_path is None:
            from health_monitor.config import get_config
            config = get_config()
            self.db_path = config.db_path
        else:
            self.db_path = db_path

        self._init_database()

    def _init_database(self):
        """Initialize cost tracking tables."""
        with _get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS api_costs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp INTEGER NOT NULL,
                    agent TEXT NOT NULL,
                    provider TEXT NOT NULL,
                    model TEXT NOT NULL,
                    input_tokens INTEGER NOT NULL,
                    output_tokens INTEGER NOT NULL,
                    total_tokens INTEGER NOT NULL,
                    cost_usd REAL NOT NULL,
                    request_id TEXT,
                    success INTEGER DEFAULT 1,
                    error TEXT,
                    metadata TEXT,
                    INDEX idx_timestamp (timestamp),
                    INDEX idx_agent (agent),
                    INDEX idx_provider (provider),
                    INDEX idx_model (model)
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS budget_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    triggered_at INTEGER NOT NULL,
                    budget_type TEXT NOT NULL,
                    threshold_percent REAL NOT NULL,
                    current_cost REAL NOT NULL,
                    budget_limit REAL NOT NULL,
                    acknowledged INTEGER DEFAULT 0,
                    INDEX idx_triggered_at (triggered_at)
                )
            """)

            conn.commit()

        logger.info("Cost tracker database initialized")

    def record_call(
        self,
        agent: str,
        provider: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        request_id: Optional[str] = None,
        success: bool = True,
        error: Optional[str] = None,
        metadata: Optional[Dict] = None,
    ) -> APICall:
        """Record an API call and calculate cost."""
        try:
            provider_enum = APIProvider(provider.lower())
        except ValueError:
            provider_enum = APIProvider.UNKNOWN
            logger.warning(f"Unknown provider: {provider}")

        try:
            model_enum = ModelType(model.lower())
        except ValueError:
            model_enum = ModelType.UNKNOWN
            logger.warning(f"Unknown model: {model}")

        # Calculate cost
        input_price, output_price = PRICING.get(model_enum, PRICING[ModelType.UNKNOWN])
        cost_usd = (input_tokens * input_price / 1_000_000) + (output_tokens * output_price / 1_000_000)

        api_call = APICall(
            timestamp=datetime.now(),
            agent=agent,
            provider=provider_enum,
            model=model_enum,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            cost_usd=cost_usd,
            request_id=request_id,
            success=success,
            error=error,
            metadata=metadata or {},
        )

        # Save to database
        with _get_connection() as conn:
            conn.execute("""
                INSERT INTO api_costs
                (timestamp, agent, provider, model, input_tokens, output_tokens,
                 total_tokens, cost_usd, request_id, success, error, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                int(api_call.timestamp.timestamp()),
                api_call.agent,
                api_call.provider.value,
                api_call.model.value,
                api_call.input_tokens,
                api_call.output_tokens,
                api_call.total_tokens,
                api_call.cost_usd,
                api_call.request_id,
                1 if api_call.success else 0,
                api_call.error,
                json.dumps(api_call.metadata),
            ))
            conn.commit()

        logger.debug(f"Recorded API call: {agent} {model} ${cost_usd:.4f}")
        return api_call

    def get_cost_summary(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> CostSummary:
        """Get cost summary for a date range."""
        start_ts = int(start_date.timestamp())
        end_ts = int(end_date.timestamp())

        with _get_connection() as conn:
            # Total stats
            row = conn.execute("""
                SELECT
                    SUM(cost_usd) as total_cost,
                    SUM(total_tokens) as total_tokens,
                    COUNT(*) as total_calls,
                    SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_calls,
                    SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failed_calls
                FROM api_costs
                WHERE timestamp >= ? AND timestamp <= ?
            """, (start_ts, end_ts)).fetchone()

            # By provider
            by_provider = {}
            for row in conn.execute("""
                SELECT provider, SUM(cost_usd) as cost
                FROM api_costs
                WHERE timestamp >= ? AND timestamp <= ?
                GROUP BY provider
            """, (start_ts, end_ts)).fetchall():
                by_provider[row[0]] = row[1]

            # By model
            by_model = {}
            for row in conn.execute("""
                SELECT model, SUM(cost_usd) as cost
                FROM api_costs
                WHERE timestamp >= ? AND timestamp <= ?
                GROUP BY model
            """, (start_ts, end_ts)).fetchall():
                by_model[row[0]] = row[1]

            # By agent
            by_agent = {}
            for row in conn.execute("""
                SELECT agent, SUM(cost_usd) as cost
                FROM api_costs
                WHERE timestamp >= ? AND timestamp <= ?
                GROUP BY agent
            """, (start_ts, end_ts)).fetchall():
                by_agent[row[0]] = row[1]

        return CostSummary(
            start_date=start_date,
            end_date=end_date,
            total_cost=row[0] or 0.0,
            total_tokens=row[1] or 0,
            total_calls=row[2] or 0,
            successful_calls=row[3] or 0,
            failed_calls=row[4] or 0,
            by_provider=by_provider,
            by_model=by_model,
            by_agent=by_agent,
        )

    def get_costs_by_provider(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> Dict[str, Dict]:
        """Get detailed breakdown by provider."""
        start_ts = int(start_date.timestamp())
        end_ts = int(end_date.timestamp())

        result = {}
        with _get_connection() as conn:
            for row in conn.execute("""
                SELECT
                    provider,
                    SUM(cost_usd) as cost,
                    SUM(total_tokens) as tokens,
                    COUNT(*) as calls,
                    SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as errors
                FROM api_costs
                WHERE timestamp >= ? AND timestamp <= ?
                GROUP BY provider
            """, (start_ts, end_ts)).fetchall():
                result[row[0]] = {
                    "cost": row[1],
                    "tokens": row[2],
                    "calls": row[3],
                    "errors": row[4],
                }

        return result

    def get_costs_by_agent(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> Dict[str, Dict]:
        """Get detailed breakdown by agent."""
        start_ts = int(start_date.timestamp())
        end_ts = int(end_date.timestamp())

        result = {}
        with _get_connection() as conn:
            for row in conn.execute("""
                SELECT
                    agent,
                    SUM(cost_usd) as cost,
                    SUM(total_tokens) as tokens,
                    COUNT(*) as calls,
                    SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as errors
                FROM api_costs
                WHERE timestamp >= ? AND timestamp <= ?
                GROUP BY agent
            """, (start_ts, end_ts)).fetchall():
                result[row[0]] = {
                    "cost": row[1],
                    "tokens": row[2],
                    "calls": row[3],
                    "errors": row[4],
                }

        return result

    def get_cost_trends(
        self,
        days: int = 30,
        group_by: str = "day",
    ) -> List[Dict]:
        """Get cost trends over time."""
        cutoff = int((datetime.now() - timedelta(days=days)).timestamp())

        result = []
        with _get_connection() as conn:
            if group_by == "day":
                for row in conn.execute("""
                    SELECT
                        DATE(timestamp, 'unixepoch') as date,
                        SUM(cost_usd) as cost,
                        SUM(total_tokens) as tokens,
                        COUNT(*) as calls
                    FROM api_costs
                    WHERE timestamp >= ?
                    GROUP BY date
                    ORDER BY date
                """, (cutoff,)).fetchall():
                    result.append({
                        "date": row[0],
                        "cost": row[1],
                        "tokens": row[2],
                        "calls": row[3],
                    })

        return result

    def check_budget_alerts(
        self,
        monthly_budget: float,
        alert_threshold: float = 0.9,
    ) -> List[Dict]:
        """Check if budget thresholds have been exceeded."""
        now = datetime.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start_ts = int(month_start.timestamp())

        alerts = []

        # Get current month's costs
        with _get_connection() as conn:
            row = conn.execute("""
                SELECT SUM(cost_usd) as total_cost
                FROM api_costs
                WHERE timestamp >= ?
            """, (start_ts,)).fetchone()

            current_cost = row[0] or 0.0
            budget_percent = current_cost / monthly_budget if monthly_budget > 0 else 0

        # Check thresholds
        thresholds = [0.5, 0.75, 0.9, 1.0]
        for threshold in thresholds:
            if budget_percent >= threshold and budget_percent < threshold + 0.25:
                severity = "critical" if threshold >= 0.9 else "warning"

                # Check if we've already alerted for this threshold
                already_alerted = False
                with _get_connection() as conn:
                    row = conn.execute("""
                        SELECT COUNT(*) as count
                        FROM budget_alerts
                        WHERE triggered_at >= ?
                        AND budget_type = 'monthly'
                        AND threshold_percent >= ?
                    """, (start_ts, threshold)).fetchone()
                    already_alerted = row[0] > 0

                if not already_alerted:
                    # Create alert
                    alert = {
                        "severity": severity,
                        "budget_type": "monthly",
                        "threshold_percent": threshold,
                        "current_cost": current_cost,
                        "budget_limit": monthly_budget,
                        "budget_percent": budget_percent,
                        "triggered_at": now.isoformat(),
                    }
                    alerts.append(alert)

                    # Record in database
                    with _get_connection() as conn:
                        conn.execute("""
                            INSERT INTO budget_alerts
                            (triggered_at, budget_type, threshold_percent, current_cost, budget_limit)
                            VALUES (?, ?, ?, ?, ?)
                        """, (
                            int(now.timestamp()),
                            "monthly",
                            threshold,
                            current_cost,
                            monthly_budget,
                        ))
                        conn.commit()

        return alerts

    def get_recent_calls(
        self,
        limit: int = 100,
        agent: Optional[str] = None,
    ) -> List[APICall]:
        """Get recent API calls."""
        with _get_connection() as conn:
            if agent:
                rows = conn.execute("""
                    SELECT * FROM api_costs
                    WHERE agent = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (agent, limit)).fetchall()
            else:
                rows = conn.execute("""
                    SELECT * FROM api_costs
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (limit,)).fetchall()

        calls = []
        for row in rows:
            calls.append(APICall(
                timestamp=datetime.fromtimestamp(row[1]),
                agent=row[2],
                provider=APIProvider(row[3]),
                model=ModelType(row[4]),
                input_tokens=row[5],
                output_tokens=row[6],
                total_tokens=row[7],
                cost_usd=row[8],
                request_id=row[9],
                success=bool(row[10]),
                error=row[11],
                metadata=json.loads(row[12]) if row[12] else {},
            ))

        return calls


def main():
    """CLI for cost tracker."""
    import argparse

    parser = argparse.ArgumentParser(description="BlackBox5 Cost Tracker")
    parser.add_argument("--since", type=int, default=7, help="Days to look back")
    parser.add_argument("--agent", type=str, help="Filter by agent")
    parser.add_argument("--budget", type=float, help="Monthly budget for alerts")
    parser.add_argument("--format", choices=["table", "json"], default="table")

    args = parser.parse_args()

    tracker = CostTracker()
    start_date = datetime.now() - timedelta(days=args.since)
    end_date = datetime.now()

    if args.budget:
        alerts = tracker.check_budget_alerts(args.budget)
        if alerts:
            print("🚨 Budget Alerts:")
            for alert in alerts:
                print(f"  {alert['severity'].upper()}: ${alert['current_cost']:.2f} of ${alert['budget_limit']:.2f} ({alert['budget_percent']:.1%})")
        else:
            print("✅ No budget alerts")
        print()

    summary = tracker.get_cost_summary(start_date, end_date)

    if args.format == "json":
        print(json.dumps(summary.to_dict(), indent=2, default=str))
    else:
        print(f"📊 Cost Summary ({args.since} days)")
        print("=" * 50)
        print(f"  Total Cost: ${summary.total_cost:.2f}")
        print(f"  Total Tokens: {summary.total_tokens:,}")
        print(f"  Total Calls: {summary.total_calls:,}")
        print(f"  Success Rate: {summary.successful_calls / summary.total_calls * 100:.1f}%")
        print()
        print("  By Provider:")
        for provider, cost in sorted(summary.by_provider.items(), key=lambda x: x[1], reverse=True):
            print(f"    {provider}: ${cost:.2f}")
        print()
        print("  By Agent:")
        for agent, cost in sorted(summary.by_agent.items(), key=lambda x: x[1], reverse=True):
            print(f"    {agent}: ${cost:.2f}")


if __name__ == "__main__":
    main()
