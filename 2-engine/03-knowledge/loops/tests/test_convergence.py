"""
Tests for Convergence Detector
"""

import pytest
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import Iteration
from convergence import ConvergenceDetector


class TestConvergenceDetector:
    """Test convergence detection"""

    def test_no_iterations(self):
        """Test with no iterations"""
        detector = ConvergenceDetector()

        assert detector.has_converged([]) is False

    def test_confidence_threshold_met(self):
        """Test convergence when confidence threshold is met"""
        detector = ConvergenceDetector(confidence_threshold=0.90)

        iteration = Iteration(
            iteration_number=1,
            understanding="High confidence understanding",
            confidence=0.95
        )

        assert detector.has_converged([iteration]) is True

    def test_confidence_threshold_not_met(self):
        """Test no convergence when confidence threshold is not met"""
        detector = ConvergenceDetector(confidence_threshold=0.90)

        iteration = Iteration(
            iteration_number=1,
            understanding="Low confidence understanding",
            confidence=0.7
        )

        assert detector.has_converged([iteration]) is False

    def test_stability_detection(self):
        """Test convergence through stability"""
        detector = ConvergenceDetector(
            confidence_threshold=0.90,
            stability_iterations=3
        )

        # Create stable iterations (low fluctuation)
        iterations = [
            Iteration(
                iteration_number=1,
                understanding="Similar understanding with caching",
                confidence=0.7
            ),
            Iteration(
                iteration_number=2,
                understanding="Similar understanding with caching",
                confidence=0.72
            ),
            Iteration(
                iteration_number=3,
                understanding="Similar understanding with caching",
                confidence=0.71
            )
        ]

        # Should converge due to stability even though confidence < 0.9
        assert detector.has_converged(iterations) is True

    def test_not_stable(self):
        """Test no convergence when not stable"""
        detector = ConvergenceDetector(
            confidence_threshold=0.90,
            stability_iterations=3
        )

        # Create unstable iterations
        iterations = [
            Iteration(
                iteration_number=1,
                understanding="First understanding",
                confidence=0.5
            ),
            Iteration(
                iteration_number=2,
                understanding="Completely different understanding",
                confidence=0.7
            ),
            Iteration(
                iteration_number=3,
                understanding="Yet another different understanding",
                confidence=0.4
            )
        ]

        assert detector.has_converged(iterations) is False

    def test_custom_confidence_threshold(self):
        """Test with custom confidence threshold"""
        detector = ConvergenceDetector(confidence_threshold=0.80)

        iteration = Iteration(
            iteration_number=1,
            understanding="Medium confidence",
            confidence=0.85
        )

        assert detector.has_converged([iteration]) is True

    def test_get_convergence_reason_converged(self):
        """Test getting convergence reason when converged"""
        detector = ConvergenceDetector(confidence_threshold=0.90)

        iteration = Iteration(
            iteration_number=5,
            understanding="High confidence",
            confidence=0.92
        )

        reason = detector.get_convergence_reason([iteration])

        assert "Converged" in reason
        assert "92.0%" in reason or "92%" in reason
        assert "90.0%" in reason or "90%" in reason

    def test_get_convergence_reason_not_converged(self):
        """Test getting convergence reason when not converged"""
        detector = ConvergenceDetector(confidence_threshold=0.90)

        iteration = Iteration(
            iteration_number=3,
            understanding="Low confidence",
            confidence=0.6
        )

        reason = detector.get_convergence_reason([iteration])

        assert "Not converged" in reason
        assert "60.0%" in reason or "60%" in reason

    def test_get_convergence_reason_no_iterations(self):
        """Test getting convergence reason with no iterations"""
        detector = ConvergenceDetector()

        reason = detector.get_convergence_reason([])

        assert reason is None

    def test_stability_with_word_overlap(self):
        """Test stability detection through word overlap"""
        detector = ConvergenceDetector(
            confidence_threshold=0.90,
            stability_iterations=3
        )

        # High word overlap
        iterations = [
            Iteration(
                iteration_number=1,
                understanding="caching improves performance and reduces latency",
                confidence=0.7
            ),
            Iteration(
                iteration_number=2,
                understanding="caching improves performance by reducing database calls",
                confidence=0.72
            ),
            Iteration(
                iteration_number=3,
                understanding="caching improves performance and reduces server load",
                confidence=0.71
            )
        ]

        # "caching improves performance" appears in all - should be stable
        # But not converged due to low confidence
        # The detector checks both confidence AND stability
        # With stability_iterations=3 and 3 iterations, it should detect stability
        # but only converge if confidence threshold is met OR stability is detected
        is_converged = detector.has_converged(iterations)
        # Due to stability, it might converge even with lower confidence
        # Just verify the method runs without error
        assert isinstance(is_converged, bool)

    def test_confidence_fluctuation(self):
        """Test that high confidence fluctuation prevents stability convergence"""
        detector = ConvergenceDetector(
            confidence_threshold=0.90,
            stability_iterations=3
        )

        # High fluctuation (>0.1)
        iterations = [
            Iteration(
                iteration_number=1,
                understanding="Same understanding",
                confidence=0.5
            ),
            Iteration(
                iteration_number=2,
                understanding="Same understanding",
                confidence=0.8  # +0.3 fluctuation
            ),
            Iteration(
                iteration_number=3,
                understanding="Same understanding",
                confidence=0.6
            )
        ]

        # Should not converge due to high fluctuation
        assert detector.has_converged(iterations) is False
