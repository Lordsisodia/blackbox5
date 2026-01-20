"""
Tests for Five Whys Analyzer
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from five_whys import FiveWhysAnalyzer, WhyLevel, FiveWhysResult


class TestFiveWhysAnalyzer:
    """Test Five Whys root cause analysis"""

    def test_analyze_generates_levels(self):
        """Test that analysis generates Why levels"""
        analyzer = FiveWhysAnalyzer()

        problem = "The website is slow"
        result = analyzer.analyze(problem)

        assert len(result.levels) > 0
        assert result.problem == problem

    def test_analyze_identifies_root_cause(self):
        """Test that analysis identifies root cause"""
        analyzer = FiveWhysAnalyzer()

        problem = "The website crashes"
        result = analyzer.analyze(problem)

        assert len(result.root_cause) > 0
        assert result.root_cause_type in ['systemic', 'process', 'human_error', 'technical']

    def test_analyze_with_provided_answers(self):
        """Test analysis with provided answers"""
        analyzer = FiveWhysAnalyzer()

        problem = "Server is down"
        answers = [
            "Because the database connection failed",
            "Because the database server was restarted",
            "Because there was a configuration change",
            "Because the deployment process doesn't validate configs",
            "Because there's no pre-deployment validation process"
        ]

        result = analyzer.analyze_with_answers(problem, answers)

        assert len(result.levels) == 5
        assert result.root_cause == answers[-1]

    def test_root_cause_classification(self):
        """Test root cause type classification"""
        analyzer = FiveWhysAnalyzer()

        # Process issue
        answer1 = "There's no validation process in place"
        root_type1 = analyzer._classify_root_cause(answer1)
        assert root_type1 == 'process'

        # Systemic issue
        answer2 = "The system architecture has a single point of failure"
        root_type2 = analyzer._classify_root_cause(answer2)
        assert root_type2 == 'systemic'

        # Technical issue
        answer3 = "There's a bug in the code"
        root_type3 = analyzer._classify_root_cause(answer3)
        assert root_type3 == 'technical'

    def test_generates_solutions(self):
        """Test that analysis generates solutions"""
        analyzer = FiveWhysAnalyzer()

        problem = "Data is inconsistent"
        result = analyzer.analyze(problem)

        assert len(result.suggested_solutions) > 0
        assert any(len(s) > 0 for s in result.suggested_solutions)

    def test_validate_depth_continues_until_root(self):
        """Test depth validation continues until root cause found"""
        analyzer = FiveWhysAnalyzer()

        problem = "Users are unhappy"

        # At shallow depth, should continue
        validation1 = analyzer.validate_depth(problem, 1, "Because the UI is slow")
        assert validation1['should_continue'] is True

        # At depth 5, should stop
        validation2 = analyzer.validate_depth(problem, 5, "There's no process for validating requirements")
        assert validation2['should_continue'] is False

    def test_max_depth_limit(self):
        """Test that analysis respects max depth"""
        analyzer = FiveWhysAnalyzer(max_depth=3)

        problem = "Test problem"
        result = analyzer.analyze(problem)

        assert len(result.levels) <= 3

    def test_check_for_blame(self):
        """Test blame detection in analysis"""
        analyzer = FiveWhysAnalyzer()

        # Create levels with blame
        levels = [
            WhyLevel(1, "Why?", "Because John made a mistake", 0.7, [], False),
            WhyLevel(2, "Why?", "Because she didn't follow process", 0.7, [], False),
        ]

        warnings = analyzer.check_for_blame(levels)

        assert len(warnings) > 0
        assert any('blame' in w.lower() or 'individual' in w.lower() for w in warnings)

    def test_no_blame_for_systemic_issues(self):
        """Test that systemic issues don't trigger blame warnings"""
        analyzer = FiveWhysAnalyzer()

        # Create levels with systemic focus
        levels = [
            WhyLevel(1, "Why?", "Because the process is broken", 0.7, [], False),
            WhyLevel(2, "Why?", "Because there's no validation", 0.7, [], False),
        ]

        warnings = analyzer.check_for_blame(levels)

        # Should have fewer or no warnings
        assert len(warnings) == 0

    def test_confidence_calculation(self):
        """Test overall confidence calculation"""
        analyzer = FiveWhysAnalyzer()

        problem = "Test problem"
        result = analyzer.analyze(problem)

        assert 0.0 <= result.confidence <= 1.0

    def test_root_cause_at_systemic_level(self):
        """Test that systemic issues are identified as root causes"""
        analyzer = FiveWhysAnalyzer()

        answer = "There's no governance process for changes"
        is_root = analyzer._is_potential_root_cause(answer, 5)  # At depth 5

        assert is_root is True
        # Also test at shallow depth - should not be root cause yet
        is_root_shallow = analyzer._is_potential_root_cause(answer, 2)
        assert is_root_shallow is False

    def test_human_error_not_root_cause(self):
        """Test that human error alone is not accepted as root cause"""
        analyzer = FiveWhysAnalyzer()

        answer = "Because the operator made a mistake"
        is_root = analyzer._is_potential_root_cause(answer, 2)

        # Should not accept human error as root cause at shallow depth
        assert is_root is False

    def test_solutions_for_each_root_cause_type(self):
        """Test that solutions match root cause type"""
        analyzer = FiveWhysAnalyzer()

        # Process root cause
        solutions1 = analyzer._generate_solutions("No validation process", 'process', [])
        assert any('process' in s.lower() or 'validation' in s.lower() for s in solutions1)

        # Systemic root cause
        solutions2 = analyzer._generate_solutions("Single point of failure", 'systemic', [])
        assert any('system' in s.lower() or 'architecture' in s.lower() for s in solutions2)

    def test_question_generation(self):
        """Test why question generation"""
        analyzer = FiveWhysAnalyzer()

        q1 = analyzer._generate_why_question("Database is slow", 2)
        assert "why" in q1.lower()
        assert "database is slow" in q1.lower()

        q2 = analyzer._generate_why_question("No monitoring", 3)
        assert "and why" in q2.lower()
