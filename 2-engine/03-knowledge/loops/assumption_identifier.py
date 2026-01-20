"""
Assumption Identifier
======================

Extracts and classifies assumptions from reasoning text.

Uses natural language patterns to identify:
- Explicit assumptions ("I assume that...", "Assuming...")
- Implicit assumptions (statements presented as facts without evidence)
- Conditional statements (if/then statements)
"""

from typing import List
import re

# Handle both relative and absolute imports
try:
    from .models import Assumption, AssumptionType
except ImportError:
    from models import Assumption, AssumptionType


class AssumptionIdentifier:
    """
    Identifies assumptions in reasoning text.

    Assumption classification:
    - CRITICAL: Core to the problem - if wrong, everything fails
    - IMPORTANT: Significant but not core
    - MINOR: Nice to have, low impact
    """

    # Patterns that indicate assumptions
    ASSUMPTION_PATTERNS = [
        r"i\s+(?:assume|assumed|assuming)\s+(that\s+)?(.+?)[.,;]",
        r"assumption:\s*(.+?)[.,;]",
        r"assuming\s+(.+?)[.,;]",
        r"presumably\s+(.+?)[.,;]",
        r"presumably\s+(.+?)[.,;]",
        r"likely\s+(.+?)[.,;]",
        r"probably\s+(.+?)[.,;]",
    ]

    # Patterns that indicate critical assumptions
    CRITICAL_KEYWORDS = [
        "must", "require", "need", "critical", "essential", "fundamental",
        "core", "key", "primary", "necessary", "depends on"
    ]

    # Patterns that indicate minor assumptions
    MINOR_KEYWORDS = [
        "might", "could", "maybe", "possibly", "potentially",
        "perhaps", "conceivably", "theoretically"
    ]

    def __init__(self):
        """Initialize assumption identifier."""
        # Compile regex patterns for performance
        self.patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.ASSUMPTION_PATTERNS]

    async def identify(self, understanding: str, context: str = "") -> List[Assumption]:
        """
        Identify assumptions in current understanding.

        Args:
            understanding: Current reasoning/understanding text
            context: Additional context for classification

        Returns:
            List of assumptions found
        """
        assumptions = []

        # Extract explicit assumptions using patterns
        for pattern in self.patterns:
            matches = pattern.finditer(understanding)
            for match in matches:
                statement = match.group(2) if match.lastindex >= 2 else match.group(1)
                statement = statement.strip()

                if statement and len(statement) > 5:  # Filter out short matches
                    assumption_type = self._classify_assumption(statement, understanding)
                    assumptions.append(Assumption(
                        statement=statement,
                        type=assumption_type,
                        context=context
                    ))

        # Extract implicit assumptions (statements without evidence)
        implicit = self._identify_implicit_assumptions(understanding, context)
        assumptions.extend(implicit)

        # Remove duplicates while preserving order
        seen = set()
        unique_assumptions = []
        for assumption in assumptions:
            normalized = assumption.statement.lower().strip()
            if normalized not in seen:
                seen.add(normalized)
                unique_assumptions.append(assumption)

        return unique_assumptions

    def _classify_assumption(self, statement: str, context: str) -> AssumptionType:
        """
        Classify an assumption by importance.

        Args:
            statement: The assumption statement
            context: Full context for classification

        Returns:
            AssumptionType (CRITICAL, IMPORTANT, or MINOR)
        """
        statement_lower = statement.lower()
        context_lower = context.lower()

        # Check for critical keywords
        for keyword in self.CRITICAL_KEYWORDS:
            if keyword in statement_lower or keyword in context_lower:
                return AssumptionType.CRITICAL

        # Check for minor keywords
        for keyword in self.MINOR_KEYWORDS:
            if keyword in statement_lower:
                return AssumptionType.MINOR

        # Default to IMPORTANT
        return AssumptionType.IMPORTANT

    def _identify_implicit_assumptions(self, understanding: str, context: str) -> List[Assumption]:
        """
        Identify implicit assumptions (statements presented as facts without evidence).

        This is a simplified implementation. In production, this would use
        more sophisticated NLP to detect assertions without evidence.

        Args:
            understanding: Current reasoning text
            context: Additional context

        Returns:
            List of implicit assumptions
        """
        assumptions = []

        # Look for statements that assert facts without evidence
        # Pattern: "[Noun phrase] is [adjective/noun]" without qualifiers
        sentences = understanding.split(".")

        for sentence in sentences:
            sentence = sentence.strip()

            # Skip very short or very long sentences
            if len(sentence) < 10 or len(sentence) > 200:
                continue

            # Skip if already has qualifier (not an implicit assumption)
            qualifiers = ["might", "could", "may", "possibly", "probably",
                         "likely", "perhaps", "seems", "appears"]
            if any(qualifier in sentence.lower() for qualifier in qualifiers):
                continue

            # Look for assertion patterns
            if " is " in sentence or " are " in sentence:
                # This might be an implicit assumption
                assumption_type = self._classify_assumption(sentence, context)

                # Only add if it seems important enough
                if assumption_type != AssumptionType.MINOR:
                    assumptions.append(Assumption(
                        statement=sentence,
                        type=assumption_type,
                        context=f"Implicit assumption from: {context[:100]}"
                    ))

        return assumptions

    def prioritize(self, assumptions: List[Assumption]) -> List[Assumption]:
        """
        Prioritize assumptions by importance.

        Args:
            assumptions: List of assumptions

        Returns:
            Sorted list (CRITICAL first, then IMPORTANT, then MINOR)
        """
        priority_order = {
            AssumptionType.CRITICAL: 0,
            AssumptionType.IMPORTANT: 1,
            AssumptionType.MINOR: 2
        }

        return sorted(assumptions, key=lambda a: priority_order.get(a.type, 99))
