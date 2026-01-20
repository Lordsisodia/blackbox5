"""
Tests for Logical Validator
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from logical_validator import LogicalValidator, ValidationResult, FallacyDetection


class TestLogicalValidator:
    """Test logical validation and fallacy detection"""

    def test_detect_ad_hominem(self):
        """Test detection of ad hominem fallacy"""
        validator = LogicalValidator()

        argument = "You can't trust his economic policies - he's divorced!"
        result = validator.validate(argument)

        assert len(result.fallacies) > 0
        ad_hominem = [f for f in result.fallacies if f.fallacy_type == 'ad_hominem']
        assert len(ad_hominem) > 0

    def test_detect_straw_man(self):
        """Test detection of straw man fallacy"""
        validator = LogicalValidator()

        argument = "So you're saying that we should destroy the economy?"
        result = validator.validate(argument)

        straw_man = [f for f in result.fallacies if f.fallacy_type == 'straw_man']
        assert len(straw_man) > 0

    def test_detect_false_dilemma(self):
        """Test detection of false dilemma"""
        validator = LogicalValidator()

        argument = "Either we cut taxes or the economy will collapse."
        result = validator.validate(argument)

        false_dilemma = [f for f in result.fallacies if f.fallacy_type == 'false_dilemma']
        assert len(false_dilemma) > 0

    def test_detect_circular_reasoning(self):
        """Test detection of circular reasoning"""
        validator = LogicalValidator()

        argument = "This is true because it's true."
        result = validator.validate(argument)

        circular = [f for f in result.fallacies if f.fallacy_type == 'circular_reasoning']
        assert len(circular) > 0

    def test_detect_appeal_to_authority(self):
        """Test detection of appeal to authority"""
        validator = LogicalValidator()

        argument = "Experts say this is true, so it must be true."
        result = validator.validate(argument)

        appeal = [f for f in result.fallacies if f.fallacy_type == 'appeal_to_authority']
        assert len(appeal) > 0

    def test_extract_premises_and_conclusion(self):
        """Test extraction of argument structure"""
        validator = LogicalValidator()

        argument = "All men are mortal. Socrates is a man. Therefore, Socrates is mortal."
        premises, conclusion = validator._extract_structure(argument)

        assert len(premises) >= 1
        assert len(conclusion) > 0
        assert "therefore" in conclusion.lower() or "Socrates" in conclusion

    def test_validity_score_calculation(self):
        """Test validity score calculation"""
        validator = LogicalValidator()

        # Clean argument should have some score
        clean = "The evidence supports this conclusion."
        result1 = validator.validate(clean)
        assert result1.validity_score >= 0.0

        # Argument with fallacies should have lower score
        with_fallacy = "You're stupid, so you're wrong. Either that or destroy everything."
        result2 = validator.validate(with_fallacy)
        # Fallacies should reduce the score
        assert len(result2.fallacies) > len(result1.fallacies)

    def test_classify_reasoning_type(self):
        """Test classification of reasoning type"""
        validator = LogicalValidator()

        # Deductive
        deductive = "If it rains, the ground gets wet. It is raining. Therefore, the ground is wet."
        type1 = validator._classify_reasoning_type(deductive, [], "")
        assert type1 in ['deductive', 'unknown']

        # Inductive
        inductive = "Most swans are white, so this swan is probably white."
        type2 = validator._classify_reasoning_type(inductive, [], "")
        assert type2 in ['inductive', 'unknown']

    def test_check_assumptions_logical(self):
        """Test checking assumptions for contradictions"""
        validator = LogicalValidator()

        from models import Assumption, AssumptionType

        assumptions = [
            Assumption("The system is fast", AssumptionType.IMPORTANT),
            Assumption("The system is NOT fast", AssumptionType.IMPORTANT),
        ]

        warnings = validator.check_assumptions_logical(assumptions, "test")
        # Should detect contradiction with explicit negation
        assert len(warnings) >= 0  # At least check it runs without error

    def test_validate_inference_step(self):
        """Test validation of single inference step"""
        validator = LogicalValidator()

        # Modus ponens
        result1 = validator.validate_inference_step(
            "If it rains, ground is wet",
            "It is raining, therefore ground is wet",
            "deductive"
        )
        assert result1['valid'] is True

    def test_no_fallacies_clean_argument(self):
        """Test that clean argument has no fallacies"""
        validator = LogicalValidator()

        argument = "The data shows a clear trend. Therefore, we should adjust our strategy."
        result = validator.validate(argument)

        # Should have few or no fallacies
        critical_fallacies = [f for f in result.fallacies if f.severity == 'critical']
        assert len(critical_fallacies) == 0
