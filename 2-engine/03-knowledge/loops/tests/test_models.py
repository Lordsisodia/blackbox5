"""
Tests for data models
"""

import pytest
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import (
    Assumption,
    AssumptionType,
    AssumptionValidation,
    Validity,
    Evidence,
    FirstPrinciplesCheck,
    Iteration,
    ThoughtLoopResult,
)


class TestAssumption:
    """Test Assumption model"""

    def test_create_assumption(self):
        """Test creating an assumption"""
        assumption = Assumption(
            statement="Caching will improve performance",
            type=AssumptionType.CRITICAL,
            context="Discussion about performance optimization"
        )

        assert assumption.statement == "Caching will improve performance"
        assert assumption.type == AssumptionType.CRITICAL
        assert assumption.context == "Discussion about performance optimization"

    def test_assumption_to_dict(self):
        """Test converting assumption to dict"""
        assumption = Assumption(
            statement="Test assumption",
            type=AssumptionType.IMPORTANT
        )

        data = assumption.to_dict()

        assert data["statement"] == "Test assumption"
        assert data["type"] == "important"


class TestEvidence:
    """Test Evidence model"""

    def test_create_evidence(self):
        """Test creating evidence"""
        evidence = Evidence(
            text="Research shows caching helps",
            source="https://example.com",
            url="https://example.com",
            supports=True,
            confidence=0.8
        )

        assert evidence.text == "Research shows caching helps"
        assert evidence.source == "https://example.com"
        assert evidence.supports is True
        assert evidence.confidence == 0.8


class TestAssumptionValidation:
    """Test AssumptionValidation model"""

    def test_create_validation(self):
        """Test creating a validation"""
        assumption = Assumption(
            statement="Test",
            type=AssumptionType.IMPORTANT
        )

        supporting = [
            Evidence(text="Supports this", source="test", supports=True)
        ]

        validation = AssumptionValidation(
            assumption=assumption,
            validity=Validity.VALID,
            supporting_evidence=supporting,
            confidence=0.8,
            reasoning="Strong evidence supports this"
        )

        assert validation.validity == Validity.VALID
        assert len(validation.supporting_evidence) == 1
        assert validation.confidence == 0.8

    def test_validation_to_dict(self):
        """Test converting validation to dict"""
        assumption = Assumption(
            statement="Test",
            type=AssumptionType.IMPORTANT
        )

        validation = AssumptionValidation(
            assumption=assumption,
            validity=Validity.UNCERTAIN,
            confidence=0.5
        )

        data = validation.to_dict()

        assert data["validity"] == "uncertain"
        assert data["confidence"] == 0.5


class TestFirstPrinciplesCheck:
    """Test FirstPrinciplesCheck model"""

    def test_create_check(self):
        """Test creating a first-principles check"""
        check = FirstPrinciplesCheck(
            necessary=True,
            reasoning="This solves a real problem",
            confidence=0.8,
            alternatives=["Alternative approach", "Another alternative"]
        )

        assert check.necessary is True
        assert check.confidence == 0.8
        assert len(check.alternatives) == 2

    def test_check_to_dict(self):
        """Test converting check to dict"""
        check = FirstPrinciplesCheck(
            necessary=False,
            reasoning="Not necessary",
            confidence=0.7
        )

        data = check.to_dict()

        assert data["necessary"] is False
        assert data["confidence"] == 0.7


class TestIteration:
    """Test Iteration model"""

    def test_create_iteration(self):
        """Test creating an iteration"""
        iteration = Iteration(
            iteration_number=1,
            understanding="Current understanding",
            confidence=0.7
        )

        assert iteration.iteration_number == 1
        assert iteration.understanding == "Current understanding"
        assert iteration.confidence == 0.7
        assert len(iteration.assumptions_identified) == 0
        assert len(iteration.assumptions_validated) == 0

    def test_iteration_to_dict(self):
        """Test converting iteration to dict"""
        iteration = Iteration(
            iteration_number=1,
            understanding="Test",
            confidence=0.8
        )

        data = iteration.to_dict()

        assert data["iteration_number"] == 1
        assert data["confidence"] == 0.8
        assert "timestamp" in data


class TestThoughtLoopResult:
    """Test ThoughtLoopResult model"""

    def test_create_result(self):
        """Test creating a result"""
        result = ThoughtLoopResult(
            converged=True,
            final_iteration=5,
            confidence=0.92,
            understanding="Final understanding",
            answer="YES - This is the right approach"
        )

        assert result.converged is True
        assert result.final_iteration == 5
        assert result.confidence == 0.92
        assert result.answer == "YES - This is the right approach"

    def test_result_to_dict(self):
        """Test converting result to dict"""
        result = ThoughtLoopResult(
            converged=False,
            final_iteration=10,
            confidence=0.6,
            understanding="Partial understanding",
            answer="UNCERTAIN"
        )

        data = result.to_dict()

        assert data["converged"] is False
        assert data["final_iteration"] == 10
        assert data["confidence"] == 0.6

    def test_result_to_json(self):
        """Test converting result to JSON"""
        result = ThoughtLoopResult(
            converged=True,
            final_iteration=3,
            confidence=0.95,
            understanding="Clear understanding",
            answer="YES"
        )

        json_str = result.to_json()

        assert '"conversed": true' in json_str or '"converged": true' in json_str
        assert '"confidence": 0.95' in json_str

    def test_get_iteration_summary(self):
        """Test getting iteration summary"""
        iterations = [
            Iteration(
                iteration_number=1,
                understanding="Understanding 1",
                confidence=0.6
            ),
            Iteration(
                iteration_number=2,
                understanding="Understanding 2",
                confidence=0.8
            ),
            Iteration(
                iteration_number=3,
                understanding="Understanding 3",
                confidence=0.95
            )
        ]

        result = ThoughtLoopResult(
            converged=True,
            final_iteration=3,
            confidence=0.95,
            understanding="Final",
            answer="YES",
            iterations=iterations
        )

        summary = result.get_iteration_summary()

        assert "Iteration 1:" in summary
        assert "Iteration 2:" in summary
        assert "Iteration 3:" in summary
        assert "60.0%" in summary or "60%" in summary
        assert "95.0%" in summary or "95%" in summary
