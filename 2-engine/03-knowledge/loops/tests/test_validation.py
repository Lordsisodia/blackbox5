"""
Tests for Validation Module
"""

import pytest
from pathlib import Path
import sys
from pathlib import Path as PathLib

# Add parent directory to path
sys.path.insert(0, str(PathLib(__file__).parent.parent))

from models import Assumption, AssumptionType, Validity
from validation import ValidationModule


class TestValidationModule:
    """Test assumption validation"""

    def test_init(self):
        """Test initialization"""
        validator = ValidationModule()

        assert validator.enable_web_search is False
        assert validator.enable_semantic_search is True

    @pytest.mark.asyncio
    async def test_validate_simple_assumption(self):
        """Test validating a simple assumption"""
        validator = ValidationModule()

        assumption = Assumption(
            statement="Caching improves performance",
            type=AssumptionType.IMPORTANT
        )

        validation = await validator.validate(assumption)

        assert validation.assumption == assumption
        assert validation.validity in [Validity.VALID, Validity.INVALID, Validity.UNCERTAIN]
        assert 0.0 <= validation.confidence <= 1.0
        assert len(validation.reasoning) > 0

    @pytest.mark.asyncio
    async def test_validate_batch(self):
        """Test validating multiple assumptions"""
        validator = ValidationModule()

        assumptions = [
            Assumption("Database is bottleneck", AssumptionType.CRITICAL),
            Assumption("Caching will help", AssumptionType.IMPORTANT),
            Assumption("API is fast enough", AssumptionType.MINOR),
        ]

        validations = await validator.validate_batch(assumptions, parallel=True)

        assert len(validations) == 3
        for validation in validations:
            assert validation.validity in [Validity.VALID, Validity.INVALID, Validity.UNCERTAIN]

    @pytest.mark.asyncio
    async def test_validate_batch_sequential(self):
        """Test validating assumptions sequentially"""
        validator = ValidationModule()

        assumptions = [
            Assumption(f"Assumption {i}", AssumptionType.IMPORTANT)
            for i in range(3)
        ]

        validations = await validator.validate_batch(assumptions, parallel=False)

        assert len(validations) == 3

    @pytest.mark.asyncio
    async def test_no_evidence_found(self):
        """Test validation when no evidence is found"""
        validator = ValidationModule(enable_semantic_search=False, enable_web_search=False)

        assumption = Assumption(
            statement="Completely fictional assumption that won't be found",
            type=AssumptionType.IMPORTANT
        )

        validation = await validator.validate(assumption)

        # Should return UNCERTAIN with low confidence when no evidence
        if len(validation.supporting_evidence) == 0 and len(validation.contradicting_evidence) == 0:
            assert validation.validity == Validity.UNCERTAIN
            assert validation.confidence < 0.5

    @pytest.mark.asyncio
    async def test_evidence_structure(self):
        """Test that evidence has proper structure"""
        validator = ValidationModule()

        assumption = Assumption("Test assumption", AssumptionType.IMPORTANT)
        validation = await validator.validate(assumption)

        # Check evidence objects
        all_evidence = validation.supporting_evidence + validation.contradicting_evidence

        for evidence in all_evidence:
            assert hasattr(evidence, 'text')
            assert hasattr(evidence, 'source')
            assert hasattr(evidence, 'supports')
            assert hasattr(evidence, 'confidence')
            assert 0.0 <= evidence.confidence <= 1.0

    def test_assess_support_positive(self):
        """Test assessing support for positive content"""
        validator = ValidationModule()

        query = "caching improves performance"
        content = "Caching works effectively and improves system performance significantly"

        supports = validator._assess_support(query, content)

        # Content has "works", "effectively", "improves" - should support
        assert supports is True

    def test_assess_support_negative(self):
        """Test assessing support for negative content"""
        validator = ValidationModule()

        query = "caching improves performance"
        content = "Caching does not work and creates problems"

        supports = validator._assess_support(query, content)

        # Content has "not work", "problems" - should not support
        assert supports is False

    def test_assess_validity_strong_support(self):
        """Test validity assessment with strong supporting evidence"""
        validator = ValidationModule()

        from models import Evidence

        assumption = Assumption("Test", AssumptionType.IMPORTANT)

        supporting = [
            Evidence("Evidence 1", "source1", supports=True, confidence=0.8),
            Evidence("Evidence 2", "source2", supports=True, confidence=0.9),
            Evidence("Evidence 3", "source3", supports=True, confidence=0.7),
        ]

        contradicting = [
            Evidence("Counter 1", "source4", supports=False, confidence=0.3),
        ]

        validity, confidence, reasoning = validator._assess_validity(
            assumption,
            supporting,
            contradicting
        )

        # Strong support should result in VALID
        assert validity == Validity.VALID
        assert confidence >= 0.7
        assert "support" in reasoning.lower()

    def test_assess_validity_strong_contradiction(self):
        """Test validity assessment with strong contradicting evidence"""
        validator = ValidationModule()

        from models import Evidence

        assumption = Assumption("Test", AssumptionType.IMPORTANT)

        supporting = [
            Evidence("Evidence 1", "source1", supports=True, confidence=0.3),
        ]

        contradicting = [
            Evidence("Counter 1", "source4", supports=False, confidence=0.9),
            Evidence("Counter 2", "source5", supports=False, confidence=0.8),
            Evidence("Counter 3", "source6", supports=False, confidence=0.9),
        ]

        validity, confidence, reasoning = validator._assess_validity(
            assumption,
            supporting,
            contradicting
        )

        # Strong contradiction should result in INVALID
        assert validity == Validity.INVALID
        assert confidence >= 0.7
        assert "contradict" in reasoning.lower()

    def test_assess_validity_mixed(self):
        """Test validity assessment with mixed evidence"""
        validator = ValidationModule()

        from models import Evidence

        assumption = Assumption("Test", AssumptionType.IMPORTANT)

        supporting = [
            Evidence("Evidence 1", "source1", supports=True, confidence=0.7),
            Evidence("Evidence 2", "source2", supports=True, confidence=0.6),
        ]

        contradicting = [
            Evidence("Counter 1", "source4", supports=False, confidence=0.6),
            Evidence("Counter 2", "source5", supports=False, confidence=0.7),
        ]

        validity, confidence, reasoning = validator._assess_validity(
            assumption,
            supporting,
            contradicting
        )

        # Mixed evidence should result in UNCERTAIN
        assert validity == Validity.UNCERTAIN
        assert "mixed" in reasoning.lower()

    @pytest.mark.asyncio
    async def test_git_history_analysis(self):
        """Test git history analysis"""
        validator = ValidationModule()

        # This will work if we're in a git repo
        results = await validator._analyze_git_history("caching")

        # Results should be a list
        assert isinstance(results, list)

        # If results exist, check structure
        for result in results:
            assert "message" in result
            assert "supports" in result
            assert "confidence" in result
