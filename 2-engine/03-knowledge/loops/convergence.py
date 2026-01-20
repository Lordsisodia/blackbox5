"""
Convergence Detector
====================

Detects when a thought loop has converged to a stable, high-confidence answer.

Convergence criteria:
1. Confidence threshold met (≥0.90)
2. Understanding has stabilized (minimal changes between iterations)
3. Maximum iterations reached (circuit breaker)
"""

from typing import List, Optional

# Handle both relative and absolute imports
try:
    from .models import Iteration
except ImportError:
    from models import Iteration


class ConvergenceDetector:
    """
    Detects when thought loop iterations have converged.

    Convergence is determined by:
    - Confidence ≥ 0.90 (primary criterion)
    - Understanding stability (secondary criterion)
    """

    def __init__(self, confidence_threshold: float = 0.90, stability_iterations: int = 3):
        """
        Initialize convergence detector.

        Args:
            confidence_threshold: Minimum confidence for convergence (default: 0.90)
            stability_iterations: How many consecutive stable iterations needed (default: 3)
        """
        self.confidence_threshold = confidence_threshold
        self.stability_iterations = stability_iterations

    def has_converged(self, iterations: List[Iteration]) -> bool:
        """
        Check if thought loop has converged.

        Args:
            iterations: All iterations so far

        Returns:
            True if converged (confidence ≥ threshold), False otherwise
        """
        if not iterations:
            return False

        latest = iterations[-1]

        # Primary criterion: confidence threshold
        if latest.confidence >= self.confidence_threshold:
            return True

        # Secondary criterion: understanding stability
        # Check if understanding has stabilized over recent iterations
        if len(iterations) >= self.stability_iterations:
            recent = iterations[-self.stability_iterations:]
            if self._is_stable(recent):
                # If stable but not confident, still return True
                # This prevents infinite loops on uncertain problems
                return True

        return False

    def _is_stable(self, iterations: List[Iteration]) -> bool:
        """
        Check if understanding has stabilized across iterations.

        Stability means:
        - Confidence is not fluctuating wildly
        - Understanding text is similar across iterations

        Args:
            iterations: Iterations to check for stability

        Returns:
            True if stable, False otherwise
        """
        if len(iterations) < 2:
            return False

        # Check confidence stability (not fluctuating more than 0.1)
        confidences = [it.confidence for it in iterations]
        max_conf = max(confidences)
        min_conf = min(confidences)

        if max_conf - min_conf > 0.1:
            return False

        # Check understanding similarity (simple word overlap)
        # In production, this would use semantic similarity
        understandings = [it.understanding.lower() for it in iterations]

        # Get unique words across all understandings
        all_words = set()
        for understanding in understandings:
            all_words.update(understanding.split())

        # If most words are shared, understanding is stable
        if len(all_words) == 0:
            return True

        shared_words = 0
        for word in all_words:
            if all(word in understanding for understanding in understandings):
                shared_words += 1

        stability_ratio = shared_words / len(all_words)
        return stability_ratio >= 0.5  # 50% word overlap threshold

    def get_convergence_reason(self, iterations: List[Iteration]) -> Optional[str]:
        """
        Get a human-readable explanation of why convergence was or wasn't reached.

        Args:
            iterations: All iterations

        Returns:
            Explanation string or None if no iterations
        """
        if not iterations:
            return None

        latest = iterations[-1]

        if latest.confidence >= self.confidence_threshold:
            return f"Converged with {latest.confidence:.1%} confidence (threshold: {self.confidence_threshold:.1%})"

        if len(iterations) >= self.stability_iterations:
            recent = iterations[-self.stability_iterations:]
            if self._is_stable(recent):
                return f"Stabilized after {len(iterations)} iterations (confidence: {latest.confidence:.1%})"

        return f"Not converged (confidence: {latest.confidence:.1%}, threshold: {self.confidence_threshold:.1%})"
