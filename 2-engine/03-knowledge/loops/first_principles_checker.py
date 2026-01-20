"""
First-Principles Checker
========================

Asks the fundamental question: "Do you even need to do this?"

Applies first-principles reasoning to determine whether a proposed action
is actually necessary or if there's a simpler/more effective approach.
"""

from typing import List, Optional
import re

# Handle both relative and absolute imports
try:
    from .models import FirstPrinciplesCheck
except ImportError:
    from models import FirstPrinciplesCheck


class FirstPrinciplesChecker:
    """
    Validates necessity using first-principles reasoning.

    Key questions:
    1. What problem are we actually solving?
    2. Is this the simplest solution?
    3. What are we assuming?
    4. What happens if we do nothing?
    5. Is there a different approach?
    """

    # Patterns that indicate unnecessary complexity
    UNNECESSARY_PATTERNS = [
        r"optimization\s+(?:without|before)\s+(?:benchmark|measure|test)",
        r"(?:add|implement|create)\s+(?:layer|abstraction|wrapper)\s+(?:for|to)",
        r"refactor\s+(?:without|before)\s+(?:test|spec)",
        r"(?:new|additional|extra)\s+(?:feature|functionality)",
    ]

    # Patterns that indicate necessity
    NECESSARY_PATTERNS = [
        r"(?:critical|security|bug|fix|error)",
        r"(?:must|require|need)\s+(?:to|fix|resolve)",
        r"(?:fail|broken|crash|issue)",
        r"(?:user|customer)\s+(?:need|want|request)",
    ]

    def __init__(self):
        """Initialize first-principles checker."""
        self.unnecessary_patterns = [re.compile(p, re.IGNORECASE) for p in self.UNNECESSARY_PATTERNS]
        self.necessary_patterns = [re.compile(p, re.IGNORECASE) for p in self.NECESSARY_PATTERNS]

    async def check(self, understanding: str, problem: str = "") -> FirstPrinciplesCheck:
        """
        Apply first-principles validation.

        Args:
            understanding: Current understanding/reasoning
            problem: Original problem statement

        Returns:
            FirstPrinciplesCheck with necessity determination
        """
        # Extract what problem we're solving
        actual_problem = self._extract_problem(understanding, problem)

        # Check if action is necessary
        necessary, confidence = self._assess_necessity(understanding, actual_problem)

        # Generate reasoning
        reasoning = self._generate_reasoning(
            understanding,
            actual_problem,
            necessary,
            confidence
        )

        # Generate alternatives
        alternatives = self._generate_alternatives(understanding, actual_problem)

        return FirstPrinciplesCheck(
            necessary=necessary,
            reasoning=reasoning,
            confidence=confidence,
            alternatives=alternatives
        )

    def _extract_problem(self, understanding: str, problem: str) -> str:
        """
        Extract the actual problem being solved.

        Args:
            understanding: Current reasoning
            problem: Original problem statement

        Returns:
            The actual problem statement
        """
        # If problem is provided, use it
        if problem and len(problem) > 10:
            return problem

        # Try to extract problem from understanding
        # Look for patterns like "The problem is...", "We need to fix..."
        problem_patterns = [
            r"(?:problem|issue|challenge)\s+(?:is|:)\s*([^.]+)",
            r"(?:need|want)\s+to\s+(?:fix|solve|resolve)\s+([^.]+)",
            r"(?:goal|objective)\s+(?:is|:)\s*([^.]+)",
        ]

        for pattern in problem_patterns:
            match = re.search(pattern, understanding, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        # Fallback: use first sentence
        first_sentence = understanding.split(".")[0].strip()
        return first_sentence if first_sentence else understanding[:100]

    def _assess_necessity(self, understanding: str, problem: str) -> tuple[bool, float]:
        """
        Assess whether the action is necessary.

        Args:
            understanding: Current reasoning
            problem: Problem statement

        Returns:
            Tuple of (is_necessary, confidence)
        """
        understanding_lower = understanding.lower()

        # Check for necessary patterns (high confidence)
        for pattern in self.necessary_patterns:
            if pattern.search(understanding_lower):
                return True, 0.8

        # Check for unnecessary patterns (high confidence)
        for pattern in self.unnecessary_patterns:
            if pattern.search(understanding_lower):
                return False, 0.7

        # Check for first-principles violations
        violations = self._check_first_principles(understanding)

        if violations:
            # If there are violations, likely unnecessary
            return False, 0.6 + (len(violations) * 0.1)

        # Default to necessary with low confidence
        return True, 0.5

    def _check_first_principles(self, understanding: str) -> List[str]:
        """
        Check for first-principles violations.

        Args:
            understanding: Current reasoning

        Returns:
            List of violation descriptions
        """
        violations = []
        understanding_lower = understanding.lower()

        # Violation 1: Optimizing without measuring
        if re.search(r"(?:optimize|improve|speed up)\s+", understanding_lower):
            if not re.search(r"(?:benchmark|measure|profile|metric)", understanding_lower):
                violations.append("Optimizing without baseline measurement")

        # Violation 2: Adding complexity without clear need
        if re.search(r"(?:layer|abstraction|indirection)", understanding_lower):
            if not re.search(r"(?:simplify|reduce|remove)", understanding_lower):
                violations.append("Adding complexity without clear justification")

        # Violation 3: Following trends/best practices blindly
        if re.search(r"(?:best practice|standard|pattern)\s+should", understanding_lower):
            if not re.search(r"(?:why|because|reason)", understanding_lower):
                violations.append("Following practice without understanding why")

        # Violation 4: Solving wrong problem
        if re.search(r"(?:implement|build|create)\s+", understanding_lower):
            if not re.search(r"(?:problem|need|requirement)", understanding_lower):
                violations.append("Building without clear problem statement")

        return violations

    def _generate_reasoning(
        self,
        understanding: str,
        problem: str,
        necessary: bool,
        confidence: float
    ) -> str:
        """
        Generate human-readable reasoning.

        Args:
            understanding: Current reasoning
            problem: Problem statement
            necessary: Whether action is necessary
            confidence: Confidence in assessment

        Returns:
            Reasoning explanation
        """
        if necessary:
            reasoning = f"This action appears necessary to solve: '{problem[:100]}...'"
            if confidence >= 0.7:
                reasoning += " The problem is clearly defined and the action addresses it directly."
            else:
                reasoning += " However, consider if there's a simpler approach."
        else:
            reasoning = f"This action may not be necessary"
            violations = self._check_first_principles(understanding)
            if violations:
                reasoning += f" due to: {', '.join(violations[:2])}"
            else:
                reasoning += ". Consider if the problem is clearly defined and if this is the simplest solution."

        return reasoning

    def _generate_alternatives(self, understanding: str, problem: str) -> List[str]:
        """
        Generate alternative approaches.

        Args:
            understanding: Current reasoning
            problem: Problem statement

        Returns:
            List of alternative approaches
        """
        alternatives = []

        understanding_lower = understanding.lower()

        # Common alternatives based on patterns

        # If optimizing: suggest measuring first
        if re.search(r"(?:optimize|improve|speed up)", understanding_lower):
            if not re.search(r"(?:benchmark|measure|profile)", understanding_lower):
                alternatives.append("Measure first to establish baseline and identify actual bottleneck")

        # If adding abstraction: suggest simplification
        if re.search(r"(?:layer|abstraction|wrapper|indirection)", understanding_lower):
            alternatives.append("Consider if direct implementation would be simpler")

        # If building new: suggest reusing existing
        if re.search(r"(?:build|create|implement)", understanding_lower):
            alternatives.append("Check if existing solutions/libraries can solve this")

        # If refactoring: suggest tests first
        if re.search(r"refactor", understanding_lower):
            if not re.search(r"test", understanding_lower):
                alternatives.append("Add tests before refactoring to ensure behavior is preserved")

        # Default alternative
        if not alternatives:
            alternatives.append("Consider if doing nothing is an option - what happens if we don't act?")

        return alternatives[:3]  # Return top 3 alternatives

    def check_assumption_necessity(
        self,
        assumption_statement: str,
        context: str = ""
    ) -> FirstPrinciplesCheck:
        """
        Check if an assumption is necessary to validate.

        Some assumptions are critical and must be validated.
        Others are minor and can be deferred.

        Args:
            assumption_statement: The assumption statement
            context: Additional context

        Returns:
            FirstPrinciplesCheck with necessity assessment
        """
        # Critical assumptions are always necessary to validate
        critical_indicators = [
            "must", "require", "critical", "essential", "fundamental",
            "security", "safety", "correctness", "data"
        ]

        assumption_lower = assumption_statement.lower()

        for indicator in critical_indicators:
            if indicator in assumption_lower:
                return FirstPrinciplesCheck(
                    necessary=True,
                    reasoning=f"Assumption contains critical indicator '{indicator}'",
                    confidence=0.8,
                    alternatives=[]
                )

        # Minor assumptions can be deferred
        minor_indicators = [
            "might", "could", "maybe", "possibly", "nice to have"
        ]

        for indicator in minor_indicators:
            if indicator in assumption_lower:
                return FirstPrinciplesCheck(
                    necessary=False,
                    reasoning=f"Assumption contains minor indicator '{indicator}'",
                    confidence=0.7,
                    alternatives=["Defer validation to later iteration", "Accept as working assumption"]
                )

        # Default: necessary with moderate confidence
        return FirstPrinciplesCheck(
            necessary=True,
            reasoning="Assumption appears relevant to the problem",
            confidence=0.5,
            alternatives=[]
        )
