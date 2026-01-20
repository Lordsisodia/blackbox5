"""
Statistics Collection - Agent performance and usage metrics
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)


class StatisticsCollector:
    """
    Collects and aggregates statistics about agent performance.

    Tracks:
    - Agent performance metrics
    - Task completion rates
    - Error frequencies
    - Token usage
    """

    def __init__(self):
        self._metrics: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self._aggregates: Dict[str, Dict[str, Any]] = {}

    def record_metric(self, agent: str, metric_name: str, value: Any):
        """Record a metric for an agent."""
        metric = {
            "agent": agent,
            "metric": metric_name,
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        self._metrics[f"{agent}.{metric_name}"].append(metric)

    def get_agent_stats(self, agent: str, hours: int = 24) -> Dict[str, Any]:
        """Get statistics for a specific agent."""
        cutoff = datetime.now() - timedelta(hours=hours)

        stats = {
            "agent": agent,
            "period_hours": hours,
            "metrics": {}
        }

        for key, metrics in self._metrics.items():
            if key.startswith(f"{agent}."):
                metric_name = key.split(".", 1)[1]
                recent = [m for m in metrics if datetime.fromisoformat(m["timestamp"]) > cutoff]

                if recent:
                    values = [m["value"] for m in recent if isinstance(m["value"], (int, float))]
                    if values:
                        stats["metrics"][metric_name] = {
                            "count": len(values),
                            "avg": sum(values) / len(values),
                            "min": min(values),
                            "max": max(values)
                        }

        return stats

    def get_task_completion_rate(self, hours: int = 24) -> Dict[str, float]:
        """Get task completion rates by agent."""
        # TODO: Implement actual task tracking
        return {}

    def get_error_frequency(self, hours: int = 24) -> Dict[str, int]:
        """Get error frequencies by agent."""
        cutoff = datetime.now() - timedelta(hours=hours)
        errors = defaultdict(int)

        for metrics in self._metrics.values():
            for metric in metrics:
                if metric["metric"].startswith("error") and datetime.fromisoformat(metric["timestamp"]) > cutoff:
                    errors[metric["agent"]] += 1

        return dict(errors)

    def get_token_usage(self, agent: str, hours: int = 24) -> Dict[str, int]:
        """Get token usage for an agent."""
        # TODO: Implement actual token tracking
        return {"input": 0, "output": 0, "total": 0}
