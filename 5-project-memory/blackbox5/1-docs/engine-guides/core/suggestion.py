"""
Suggestion - Proactive suggestions for agents
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class Suggestion:
    """A proactive suggestion for an agent."""

    def __init__(self, content: str, confidence: float, context: Dict[str, Any]):
        self.content = content
        self.confidence = confidence
        self.context = context
        self.created_at = datetime.now()
        self.id = f"suggestion_{id(self)}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "content": self.content,
            "confidence": self.confidence,
            "context": self.context,
            "created_at": self.created_at.isoformat()
        }
