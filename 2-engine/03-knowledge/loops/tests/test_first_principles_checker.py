"""
Tests for First-Principles Checker
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import FirstPrinciplesCheck
from first_principles_checker import FirstPrinciplesChecker


class TestFirstPrinciplesChecker:
    """Test first-principles validation"""

    @pytest.mark.asyncio
    async def test_check_necessary_action(self):
        """Test checking a necessary action"""
        checker = FirstPrinciplesChecker()

        understanding = "We must fix the critical security bug that allows SQL injection"

        result = await checker.check(understanding)

        assert result.necessary is True
        assert len(result.reasoning) > 0
        assert 0.0 <= result.confidence <= 1.0

    @pytest.mark.asyncio
    async def test_check_unnecessary_optimization(self):
        """Test checking an unnecessary optimization"""
        checker = FirstPrinciplesChecker()

        understanding = "We should add optimization for caching before measuring performance"

        result = await checker.check(understanding)

        # Should detect optimization without measurement as potentially unnecessary
        assert isinstance(result.necessary, bool)
        # If unnecessary, should provide alternatives
        if not result.necessary:
            assert len(result.alternatives) > 0

    @pytest.mark.asyncio
    async def test_check_with_problem_statement(self):
        """Test checking with explicit problem statement"""
        checker = FirstPrinciplesChecker()

        problem = "Users are experiencing slow load times"
        understanding = "We should add a caching layer to improve performance"

        result = await checker.check(understanding, problem)

        assert isinstance(result.necessary, bool)
        # Should mention the problem in reasoning
        assert len(result.reasoning) > 0

    @pytest.mark.asyncio
    async def test_extract_problem(self):
        """Test extracting problem from understanding"""
        checker = FirstPrinciplesChecker()

        understanding = "The problem is slow API response times. We need to optimize."

        problem = checker._extract_problem(understanding, "")

        assert "slow" in problem.lower()
        assert "api" in problem.lower()

    @pytest.mark.asyncio
    async def test_extract_problem_explicit(self):
        """Test extracting explicit problem"""
        checker = FirstPrinciplesChecker()

        problem = "Database is too slow"
        understanding = "We should add caching"

        extracted = checker._extract_problem(understanding, problem)

        # Should use the provided problem
        assert "database" in extracted.lower()
        assert "slow" in extracted.lower()

    @pytest.mark.asyncio
    async def test_check_first_principles_violations(self):
        """Test detecting first-principles violations"""
        checker = FirstPrinciplesChecker()

        # Optimizing without measurement
        understanding1 = "We should optimize the database queries"
        violations1 = checker._check_first_principles(understanding1)
        assert len(violations1) >= 1

        # Adding complexity without need
        understanding2 = "We should add an abstraction layer"
        violations2 = checker._check_first_principles(understanding2)
        # Might detect as unnecessary complexity
        assert isinstance(violations2, list)

    @pytest.mark.asyncio
    async def test_generate_alternatives(self):
        """Test generating alternative approaches"""
        checker = FirstPrinciplesChecker()

        understanding = "We should optimize the database"
        problem = "Performance is slow"

        alternatives = checker._generate_alternatives(understanding, problem)

        # Should generate at least one alternative
        assert len(alternatives) >= 1
        assert len(alternatives) <= 3  # Max 3 alternatives

        # Alternatives should be strings
        for alt in alternatives:
            assert isinstance(alt, str)
            assert len(alt) > 0

    @pytest.mark.asyncio
    async def test_generate_alternatives_refactor(self):
        """Test generating alternatives for refactoring"""
        checker = FirstPrinciplesChecker()

        understanding = "We should refactor the user module"

        alternatives = checker._generate_alternatives(understanding, "")

        # Should suggest testing first
        assert any("test" in alt.lower() for alt in alternatives)

    @pytest.mark.asyncio
    async def test_generate_alternatives_optimization(self):
        """Test generating alternatives for optimization"""
        checker = FirstPrinciplesChecker()

        understanding = "We should optimize the code"

        alternatives = checker._generate_alternatives(understanding, "")

        # Should suggest measuring first
        assert any("measure" in alt.lower() or "benchmark" in alt.lower() for alt in alternatives)

    @pytest.mark.asyncio
    async def test_check_assumption_necessity_critical(self):
        """Test checking assumption necessity for critical assumptions"""
        checker = FirstPrinciplesChecker()

        result = checker.check_assumption_necessity(
            "Security validation must pass",
            context="User authentication"
        )

        # Should be necessary (has "must", "security")
        assert result.necessary is True
        assert result.confidence >= 0.7

    @pytest.mark.asyncio
    async def test_check_assumption_necessity_minor(self):
        """Test checking assumption necessity for minor assumptions"""
        checker = FirstPrinciplesChecker()

        result = checker.check_assumption_necessity(
            "This might possibly help",
            context="Optimization"
        )

        # Should not be necessary (has "might", "possibly")
        assert result.necessary is False
        assert result.confidence >= 0.6
        # Should provide alternatives
        assert len(result.alternatives) >= 1

    @pytest.mark.asyncio
    async def test_assess_necessity_high_confidence(self):
        """Test necessity assessment with high confidence"""
        checker = FirstPrinciplesChecker()

        understanding = "We must fix this critical bug immediately"

        necessary, confidence = checker._assess_necessity(understanding, "")

        # Should be necessary with high confidence
        assert necessary is True
        assert confidence >= 0.7

    @pytest.mark.asyncio
    async def test_assess_necessity_low_confidence(self):
        """Test necessity assessment with low confidence"""
        checker = FirstPrinciplesChecker()

        understanding = "We might consider adding a feature"

        necessary, confidence = checker._assess_necessity(understanding, "")

        # Might not be necessary (has "might")
        # Or might be necessary with low confidence
        assert isinstance(necessary, bool)
        assert isinstance(confidence, float)
        assert 0.0 <= confidence <= 1.0
