"""
Question Manager - Dependency management and priority-based questioning
"""

import logging
from typing import List, Dict, Any, Optional
from enum import Enum, auto

logger = logging.getLogger(__name__)


class QuestionPriority(Enum):
    """Priority levels for questions."""
    CRITICAL = auto()
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()


class QuestionManager:
    """
    Manages sequential questioning with dependency tracking.

    Ensures questions are asked in the right order based on
    dependencies and priority.
    """

    def __init__(self):
        self._questions: List[Dict[str, Any]] = []
        self._answered: set = set()
        self._dependencies: Dict[str, List[str]] = {}

    def add_question(self, question_id: str, text: str, priority: QuestionPriority,
                    dependencies: Optional[List[str]] = None):
        """Add a question to the queue."""
        self._questions.append({
            "id": question_id,
            "text": text,
            "priority": priority,
            "dependencies": dependencies or []
        })
        if dependencies:
            self._dependencies[question_id] = dependencies

    def get_next_question(self) -> Optional[Dict[str, Any]]:
        """Get the next question to ask."""
        for question in self._questions:
            qid = question["id"]
            if qid in self._answered:
                continue

            # Check dependencies
            if qid in self._dependencies:
                deps = self._dependencies[qid]
                if not all(dep in self._answered for dep in deps):
                    continue

            return question

        return None

    def answer_question(self, question_id: str, answer: str):
        """Record an answer to a question."""
        self._answered.add(question_id)
        logger.info(f"Answered question: {question_id}")

    def get_pending(self) -> List[Dict[str, Any]]:
        """Get all pending questions."""
        return [q for q in self._questions if q["id"] not in self._answered]

    def is_complete(self) -> bool:
        """Check if all questions are answered."""
        return len(self.get_pending()) == 0
