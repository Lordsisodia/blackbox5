"""
Gap Analyzer - Requirement validation and coverage analysis
"""

import logging
from typing import List, Dict, Any, Set

logger = logging.getLogger(__name__)


class GapAnalyzer:
    """
    Analyzes requirements to identify gaps and missing information.

    Provides coverage analysis and validation checking.
    """

    def __init__(self):
        self._requirements: List[Dict[str, Any]] = []
        self._gaps: List[Dict[str, Any]] = []

    def add_requirement(self, req_id: str, text: str, category: str):
        """Add a requirement to analyze."""
        self._requirements.append({
            "id": req_id,
            "text": text,
            "category": category,
            "covered": False
        })

    def analyze_gaps(self) -> List[Dict[str, Any]]:
        """Analyze requirements for gaps."""
        gaps = []

        for req in self._requirements:
            # Check if requirement has enough detail
            if len(req["text"]) < 50:
                gaps.append({
                    "requirement": req["id"],
                    "issue": "insufficient_detail",
                    "severity": "medium"
                })

            # Check if category is specified
            if not req.get("category"):
                gaps.append({
                    "requirement": req["id"],
                    "issue": "missing_category",
                    "severity": "low"
                })

        self._gaps = gaps
        return gaps

    def get_coverage(self) -> Dict[str, Any]:
        """Get coverage statistics."""
        total = len(self._requirements)
        covered = sum(1 for r in self._requirements if r.get("covered", False))

        return {
            "total": total,
            "covered": covered,
            "uncovered": total - covered,
            "coverage_percent": (covered / total * 100) if total > 0 else 0
        }

    def validate(self) -> bool:
        """Validate all requirements."""
        return len(self.analyze_gaps()) == 0
