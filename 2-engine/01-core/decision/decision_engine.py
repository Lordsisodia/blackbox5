"""
Decision Engine - Core decision-making system
"""

import logging
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class DecisionType(Enum):
    """Types of decisions."""
    RULE_BASED = "rule_based"
    ML_BASED = "ml_based"
    HYBRID = "hybrid"


class DecisionEngine:
    """
    Makes decisions based on rules and/or ML models.

    Provides confidence scoring and decision logging.
    """

    def __init__(self):
        self._rules: List[Callable] = []
        self._models: Dict[str, Any] = {}
        self._history: List[Dict[str, Any]] = []

    def add_rule(self, rule: Callable):
        """Add a rule-based decision function."""
        self._rules.append(rule)

    def decide(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a decision based on context.

        Args:
            context: Current context

        Returns:
            Decision with confidence score
        """
        decisions = []

        # Try rules first
        for rule in self._rules:
            try:
                result = rule(context)
                if result:
                    decisions.append({
                        "type": DecisionType.RULE_BASED,
                        "result": result,
                        "confidence": result.get("confidence", 0.5)
                    })
            except Exception as e:
                logger.error(f"Rule error: {e}")

        # Select best decision
        if decisions:
            best = max(decisions, key=lambda d: d["confidence"])
            decision = {
                "result": best["result"],
                "confidence": best["confidence"],
                "type": best["type"],
                "timestamp": datetime.now().isoformat()
            }
        else:
            decision = {
                "result": None,
                "confidence": 0.0,
                "type": DecisionType.RULE_BASED,
                "timestamp": datetime.now().isoformat()
            }

        self._history.append(decision)
        return decision

    def get_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get decision history."""
        return self._history[-limit:]
