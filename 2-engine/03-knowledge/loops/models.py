"""
Data Models for Thought Loop Framework
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime
import json


class AssumptionType(Enum):
    """Classification of assumptions by importance"""
    CRITICAL = "critical"      # Core to the problem - if wrong, everything fails
    IMPORTANT = "important"    # Significant but not core
    MINOR = "minor"           # Nice to have, low impact


class Validity(Enum):
    """Validation result for an assumption"""
    VALID = "valid"           # Evidence supports the assumption
    INVALID = "invalid"       # Evidence contradicts the assumption
    UNCERTAIN = "uncertain"   # Insufficient or conflicting evidence


@dataclass
class Evidence:
    """A piece of evidence gathered during research"""
    text: str
    source: str              # Where did this evidence come from?
    url: Optional[str] = None
    supports: bool = True     # True = supports assumption, False = contradicts
    confidence: float = 0.5   # 0-1, how reliable is this evidence?


@dataclass
class Assumption:
    """An assumption extracted from reasoning"""
    statement: str           # The assumption text
    type: AssumptionType     # How important is this?
    context: str = ""        # What context led to this assumption?

    def to_dict(self) -> Dict[str, Any]:
        return {
            "statement": self.statement,
            "type": self.type.value,
            "context": self.context
        }


@dataclass
class AssumptionValidation:
    """Result of validating an assumption through research"""
    assumption: Assumption
    validity: Validity
    supporting_evidence: List[Evidence] = field(default_factory=list)
    contradicting_evidence: List[Evidence] = field(default_factory=list)
    confidence: float = 0.5  # 0-1, overall confidence in validity assessment
    reasoning: str = ""      # Explanation of the validation

    def to_dict(self) -> Dict[str, Any]:
        return {
            "assumption": self.assumption.to_dict(),
            "validity": self.validity.value,
            "supporting_evidence_count": len(self.supporting_evidence),
            "contradicting_evidence_count": len(self.contradicting_evidence),
            "confidence": self.confidence,
            "reasoning": self.reasoning
        }


@dataclass
class FirstPrinciplesCheck:
    """Result of first-principles validation"""
    necessary: bool          # Is this actually necessary?
    reasoning: str           # Why or why not?
    confidence: float = 0.5  # 0-1, how confident are we?
    alternatives: List[str] = field(default_factory=list)  # Other approaches

    def to_dict(self) -> Dict[str, Any]:
        return {
            "necessary": self.necessary,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "alternatives": self.alternatives
        }


@dataclass
class Iteration:
    """A single iteration in the thought loop"""
    iteration_number: int
    understanding: str       # Current understanding of the problem
    assumptions_identified: List[Assumption] = field(default_factory=list)
    assumptions_validated: List[AssumptionValidation] = field(default_factory=list)
    first_principles_check: Optional[FirstPrinciplesCheck] = None
    confidence: float = 0.5  # 0-1, how confident in current understanding?
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "iteration_number": self.iteration_number,
            "understanding": self.understanding,
            "assumptions_count": len(self.assumptions_identified),
            "validations_count": len(self.assumptions_validated),
            "first_principles_check": self.first_principles_check.to_dict() if self.first_principles_check else None,
            "confidence": self.confidence,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class ThoughtLoopResult:
    """Final result of a thought loop execution"""
    converged: bool          # Did we converge to high confidence?
    final_iteration: int     # How many iterations did we run?
    confidence: float        # Final confidence level (0-1)
    understanding: str       # Final understanding
    answer: str              # Direct answer to the original problem
    iterations: List[Iteration] = field(default_factory=list)
    reasoning_trace: List[str] = field(default_factory=list)  # Step-by-step reasoning
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "converged": self.converged,
            "final_iteration": self.final_iteration,
            "confidence": self.confidence,
            "understanding": self.understanding,
            "answer": self.answer,
            "iterations_count": len(self.iterations),
            "reasoning_trace": self.reasoning_trace,
            "metadata": self.metadata
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert result to JSON string"""
        return json.dumps(self.to_dict(), indent=indent)

    def get_iteration_summary(self) -> str:
        """Get a human-readable summary of iterations"""
        lines = [
            f"Thought Loop Summary (Converged: {self.converged}, Confidence: {self.confidence:.1%})",
            "=" * 80,
            ""
        ]

        for i, iteration in enumerate(self.iterations, 1):
            lines.append(f"Iteration {i}:")
            lines.append(f"  Confidence: {iteration.confidence:.1%}")
            lines.append(f"  Understanding: {iteration.understanding[:200]}...")
            lines.append(f"  Assumptions: {len(iteration.assumptions_identified)}")
            lines.append("")

        return "\n".join(lines)
