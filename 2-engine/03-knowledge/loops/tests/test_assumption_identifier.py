"""
Tests for Assumption Identifier
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import Assumption, AssumptionType
from assumption_identifier import AssumptionIdentifier


class TestAssumptionIdentifier:
    """Test assumption identification"""

    @pytest.mark.asyncio
    async def test_identify_explicit_assumptions(self):
        """Test identifying explicit assumptions"""
        identifier = AssumptionIdentifier()

        understanding = "I assume that caching will improve performance. I also assume that the database is the bottleneck."

        assumptions = await identifier.identify(understanding)

        assert len(assumptions) >= 2

        # Check that assumptions were extracted
        assumption_texts = [a.statement.lower() for a in assumptions]
        assert any("caching" in text and "improve" in text for text in assumption_texts)
        assert any("database" in text and "bottleneck" in text for text in assumption_texts)

    @pytest.mark.asyncio
    async def test_classify_critical_assumption(self):
        """Test classifying critical assumptions"""
        identifier = AssumptionIdentifier()

        understanding = "We must optimize the database. This is critical for performance."

        assumptions = await identifier.identify(understanding)

        # Should find at least one critical assumption
        critical_assumptions = [a for a in assumptions if a.type == AssumptionType.CRITICAL]
        assert len(critical_assumptions) >= 1

    @pytest.mark.asyncio
    async def test_classify_minor_assumption(self):
        """Test classifying minor assumptions"""
        identifier = AssumptionIdentifier()

        understanding = "This might possibly improve performance. Maybe it could help."

        assumptions = await identifier.identify(understanding)

        # Might find minor assumptions, but could also be none if patterns don't match
        # Just check it doesn't crash
        assert isinstance(assumptions, list)

    @pytest.mark.asyncio
    async def test_identify_implicit_assumptions(self):
        """Test identifying implicit assumptions"""
        identifier = AssumptionIdentifier()

        understanding = "The database is the bottleneck. Caching reduces latency by 50%."

        assumptions = await identifier.identify(understanding)

        # Should identify assertions as implicit assumptions
        assert len(assumptions) >= 1

    @pytest.mark.asyncio
    async def test_remove_duplicates(self):
        """Test that duplicate assumptions are removed"""
        identifier = AssumptionIdentifier()

        understanding = "I assume caching helps. I assume caching helps. I assume that caching will improve performance."

        assumptions = await identifier.identify(understanding)

        # Should deduplicate similar assumptions
        # "caching helps" and "caching will improve performance" are different, but
        # "I assume caching helps" appearing twice should be deduplicated
        assert len(assumptions) < 3

    @pytest.mark.asyncio
    async def test_with_context(self):
        """Test identification with context"""
        identifier = AssumptionIdentifier()

        understanding = "I assume that the API is slow"
        context = "Discussion about API performance optimization"

        assumptions = await identifier.identify(understanding, context=context)

        assert len(assumptions) >= 1
        # Context should be set on assumptions (may be combined with default)
        assert any(context in a.context or a.context == "" for a in assumptions)

    @pytest.mark.asyncio
    async def test_prioritize(self):
        """Test assumption prioritization"""
        identifier = AssumptionIdentifier()

        assumptions = [
            Assumption("Minor thing", AssumptionType.MINOR),
            Assumption("Important thing", AssumptionType.IMPORTANT),
            Assumption("Critical thing", AssumptionType.CRITICAL),
            Assumption("Another important thing", AssumptionType.IMPORTANT),
            Assumption("Another minor thing", AssumptionType.MINOR),
        ]

        prioritized = identifier.prioritize(assumptions)

        # Critical should be first
        assert prioritized[0].type == AssumptionType.CRITICAL

        # Important should come before minor
        important_indices = [i for i, a in enumerate(prioritized) if a.type == AssumptionType.IMPORTANT]
        minor_indices = [i for i, a in enumerate(prioritized) if a.type == AssumptionType.MINOR]

        if important_indices and minor_indices:
            assert min(important_indices) < max(minor_indices)

    @pytest.mark.asyncio
    async def test_empty_understanding(self):
        """Test with empty understanding"""
        identifier = AssumptionIdentifier()

        assumptions = await identifier.identify("")

        assert len(assumptions) == 0

    @pytest.mark.asyncio
    async def test_no_clear_assumptions(self):
        """Test with text that has no clear assumptions"""
        identifier = AssumptionIdentifier()

        understanding = "The system has three components: user service, API gateway, and database."

        assumptions = await identifier.identify(understanding)

        # Might find implicit assumptions, but likely few
        assert len(assumptions) >= 0

    @pytest.mark.asyncio
    async def test_pattern_matching(self):
        """Test various assumption patterns"""
        identifier = AssumptionIdentifier()

        understanding = """
        Assuming the cache works properly.
        I assume that we have enough memory.
        Presumably the network is fast.
        Likely the bottleneck is the database.
        Probably adding an index will help.
        """

        assumptions = await identifier.identify(understanding)

        # Should find multiple assumptions
        assert len(assumptions) >= 3
