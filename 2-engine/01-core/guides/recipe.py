"""
Recipe - Reusable guidance patterns
"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class Recipe:
    """A recipe is a reusable guidance pattern."""

    def __init__(self, name: str, pattern: str, confidence: float = 0.8):
        self.name = name
        self.pattern = pattern
        self.confidence = confidence
        self._usage_count = 0

    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply this recipe to the given context."""
        self._usage_count += 1
        return {
            "recipe": self.name,
            "pattern": self.pattern,
            "confidence": self.confidence
        }
