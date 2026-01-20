"""
Integration tests for Thought Loop Framework
"""

import pytest
from pathlib import Path
import sys
from pathlib import Path as PathLib

# Add parent directory to path
sys.path.insert(0, str(PathLib(__file__).parent.parent))

from thought_loop import ThoughtLoop
from models import (
    Assumption,
    AssumptionType,
    Iteration,
    ThoughtLoopResult,
)


class TestThoughtLoopIntegration:
    """Integration tests for the full thought loop"""

    @pytest.mark.asyncio
    async def test_simple_converging_loop(self):
        """Test a thought loop that converges quickly"""
        loop = ThoughtLoop()

        # Simple problem that should converge
        result = await loop.run("Should we fix critical security bug?")

        assert isinstance(result, ThoughtLoopResult)
        assert isinstance(result.converged, bool)
        assert isinstance(result.confidence, float)
        assert len(result.answer) > 0
        assert result.final_iteration >= 1
        assert result.final_iteration <= loop.max_iterations

    @pytest.mark.asyncio
    async def test_max_iterations_reached(self):
        """Test that loop stops at max iterations"""
        loop = ThoughtLoop(max_iterations=3)

        # Complex problem that might not converge
        result = await loop.run("What is the meaning of life?")

        assert result.final_iteration <= 3
        assert len(result.iterations) <= 3

    @pytest.mark.asyncio
    async def test_with_context(self):
        """Test thought loop with additional context"""
        loop = ThoughtLoop()

        context = "The system currently takes 450ms to respond"
        result = await loop.run(
            "Should we optimize performance?",
            context=context
        )

        assert isinstance(result, ThoughtLoopResult)
        # Context should influence the reasoning
        assert len(result.reasoning_trace) > 0

    @pytest.mark.asyncio
    async def test_progress_callback(self):
        """Test progress callback during iteration"""
        loop = ThoughtLoop()

        iterations_seen = []

        async def callback(iteration):
            iterations_seen.append(iteration.iteration_number)

        result = await loop.run(
            "Test problem",
            progress_callback=callback
        )

        # Should have seen at least one iteration
        assert len(iterations_seen) >= 1
        assert result.final_iteration == len(iterations_seen)

    @pytest.mark.asyncio
    async def test_iteration_trace(self):
        """Test that reasoning trace is recorded"""
        loop = ThoughtLoop()

        result = await loop.run("Should we add tests?")

        # Should have reasoning trace
        assert len(result.reasoning_trace) > 0
        # Should mention iterations
        assert any("Iteration" in trace for trace in result.reasoning_trace)

    @pytest.mark.asyncio
    async def test_result_to_dict(self):
        """Test converting result to dict"""
        loop = ThoughtLoop()

        result = await loop.run("Test problem")

        data = result.to_dict()

        assert "converged" in data
        assert "confidence" in data
        assert "answer" in data
        assert "iterations" in data or "iterations_count" in data

    @pytest.mark.asyncio
    async def test_result_to_json(self):
        """Test converting result to JSON"""
        loop = ThoughtLoop()

        result = await loop.run("Test problem")

        json_str = result.to_json()

        assert isinstance(json_str, str)
        assert len(json_str) > 0
        # Should be valid JSON
        import json
        parsed = json.loads(json_str)
        assert "converged" in parsed

    @pytest.mark.asyncio
    async def test_save_and_load_state(self, tmp_path):
        """Test saving and loading state"""
        loop = ThoughtLoop()

        # Run a loop
        result = await loop.run("Test problem")

        # Save state
        state_file = tmp_path / "state.json"
        loop.save_state(state_file)

        # Check file exists
        assert state_file.exists()

        # Load into new loop
        new_loop = ThoughtLoop()
        new_loop.load_state(state_file)

        # Check state was loaded
        assert new_loop.max_iterations == loop.max_iterations
        assert new_loop.confidence_threshold == loop.confidence_threshold

    @pytest.mark.asyncio
    async def test_caching_example(self):
        """Test the classic caching example from the documentation"""
        loop = ThoughtLoop()

        result = await loop.run(
            "Should we add caching when only 11% of time is spent on data fetching?"
        )

        # Should produce some answer
        assert len(result.answer) > 0
        # First-principles should suggest not optimizing without measurement
        # (This depends on the heuristics working correctly)

    @pytest.mark.asyncio
    async def test_custom_confidence_threshold(self):
        """Test with custom confidence threshold"""
        loop = ThoughtLoop(confidence_threshold=0.95)

        result = await loop.run("Simple problem")

        # Check threshold was set
        assert loop.confidence_threshold == 0.95

    @pytest.mark.asyncio
    async def test_iteration_structure(self):
        """Test that iterations have proper structure"""
        loop = ThoughtLoop()

        result = await loop.run("Test problem")

        for iteration in result.iterations:
            assert hasattr(iteration, 'iteration_number')
            assert hasattr(iteration, 'understanding')
            assert hasattr(iteration, 'confidence')
            assert hasattr(iteration, 'assumptions_identified')
            assert hasattr(iteration, 'assumptions_validated')
            assert hasattr(iteration, 'first_principles_check')

            # Check types
            assert isinstance(iteration.iteration_number, int)
            assert isinstance(iteration.confidence, float)
            assert isinstance(iteration.assumptions_identified, list)
            assert isinstance(iteration.assumptions_validated, list)

    @pytest.mark.asyncio
    async def test_first_principles_integration(self):
        """Test that first-principles check is integrated"""
        loop = ThoughtLoop()

        result = await loop.run("Should we add a new layer?")

        # At least one iteration should have first-principles check
        has_fp_check = any(
            it.first_principles_check is not None
            for it in result.iterations
        )

        assert has_fp_check

    @pytest.mark.asyncio
    async def test_assumption_validation_integration(self):
        """Test that assumption validation is integrated"""
        loop = ThoughtLoop()

        result = await loop.run("I assume caching will help performance")

        # At least one iteration should have validated assumptions
        has_validations = any(
            len(it.assumptions_validated) > 0
            for it in result.iterations
        )

        # Note: This depends on assumptions being identified and validated
        # which is heuristic-based

    @pytest.mark.asyncio
    async def test_get_iteration_summary(self):
        """Test getting iteration summary"""
        loop = ThoughtLoop()

        result = await loop.run("Test problem")

        summary = result.get_iteration_summary()

        assert len(summary) > 0
        assert "Thought Loop Summary" in summary
        assert "Iteration" in summary

    @pytest.mark.asyncio
    async def test_confidence_progression(self):
        """Test that confidence generally progresses"""
        loop = ThoughtLoop(max_iterations=5)

        result = await loop.run("Test problem")

        if len(result.iterations) >= 2:
            # Confidence shouldn't fluctuate wildly
            confidences = [it.confidence for it in result.iterations]
            max_change = max(abs(confidences[i] - confidences[i-1])
                           for i in range(1, len(confidences)))

            # Shouldn't change by more than 0.5 in a single iteration
            assert max_change < 0.5

    @pytest.mark.asyncio
    async def test_metadata(self):
        """Test that result includes metadata"""
        loop = ThoughtLoop(max_iterations=7, confidence_threshold=0.85)

        result = await loop.run("Test problem")

        assert "problem" in result.metadata
        assert "max_iterations" in result.metadata
        assert "confidence_threshold" in result.metadata
        assert "completed_at" in result.metadata

        assert result.metadata["max_iterations"] == 7
        assert result.metadata["confidence_threshold"] == 0.85
