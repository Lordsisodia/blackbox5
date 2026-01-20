"""
Thought Loop Core
=================

Main orchestration engine for iterative first-principles reasoning.

Runs up to 10 iterations of:
1. State understanding
2. Identify assumptions
3. Validate assumptions through research
4. Update understanding based on findings
5. First-principles check ("Do you even need to do this?")
6. Check for convergence
"""

import asyncio
from typing import List, Optional, Dict, Any, Callable
from pathlib import Path
import json
from datetime import datetime

# Handle both relative and absolute imports
try:
    from .models import (
        Iteration,
        ThoughtLoopResult,
        Assumption,
        AssumptionValidation,
        FirstPrinciplesCheck,
    )
    from .assumption_identifier import AssumptionIdentifier
    from .validation import ValidationModule
    from .first_principles_checker import FirstPrinciplesChecker
    from .convergence import ConvergenceDetector
except ImportError:
    from models import (
        Iteration,
        ThoughtLoopResult,
        Assumption,
        AssumptionValidation,
        FirstPrinciplesCheck,
    )
    from assumption_identifier import AssumptionIdentifier
    from validation import ValidationModule
    from first_principles_checker import FirstPrinciplesChecker
    from convergence import ConvergenceDetector


class ThoughtLoop:
    """
    Main thought loop engine.

    Coordinates iterative reasoning with assumption validation,
    first-principles checks, and convergence detection.

    Example:
        .. code-block:: python

            loop = ThoughtLoop()
            result = await loop.run("Should we add caching to this system?")

            if result.converged:
                print(f"Answer: {result.answer} (confidence: {result.confidence:.1%})")
            else:
                print(f"Best effort: {result.answer}")
    """

    def __init__(
        self,
        max_iterations: int = 10,
        confidence_threshold: float = 0.90,
        project_root: Optional[Path] = None,
        llm_client: Optional[Any] = None,
        project_id: str = "siso-internal",
        project_memory_path: Optional[Path] = None,
        auto_save: bool = True
    ):
        """
        Initialize thought loop.

        Args:
            max_iterations: Maximum iterations to run (default: 10)
            confidence_threshold: Target confidence for convergence (default: 0.90)
            project_root: Project root for internal research
            llm_client: Optional LLM client for reasoning (if not provided, uses simple heuristics)
            project_id: Project ID for memory integration (default: "siso-internal")
            project_memory_path: Path to project memory (auto-detected if not provided)
            auto_save: Automatically save sessions to project memory (default: True)
        """
        self.max_iterations = max_iterations
        self.confidence_threshold = confidence_threshold
        self.project_root = project_root or Path.cwd()
        self.llm_client = llm_client
        self.project_id = project_id
        self.auto_save = auto_save

        # Initialize components
        self.assumption_identifier = AssumptionIdentifier()
        self.validator = ValidationModule(project_root=self.project_root)
        self.first_principles_checker = FirstPrinciplesChecker()
        self.convergence_detector = ConvergenceDetector(
            confidence_threshold=confidence_threshold
        )

        # Initialize project memory integration
        self.memory_integration = None
        if self.auto_save:
            try:
                from .project_memory import ProjectMemoryIntegration
                self.memory_integration = ProjectMemoryIntegration(
                    project_id=project_id,
                    project_memory_path=project_memory_path,
                    auto_save=True
                )
            except ImportError:
                from project_memory import ProjectMemoryIntegration
                self.memory_integration = ProjectMemoryIntegration(
                    project_id=project_id,
                    project_memory_path=project_memory_path,
                    auto_save=True
                )

        # Tracking
        self.iterations: List[Iteration] = []
        self.reasoning_trace: List[str] = []
        self.session_start_time = None

    async def run(
        self,
        problem: str,
        context: str = "",
        initial_understanding: str = "",
        progress_callback: Optional[Callable[[Iteration], None]] = None
    ) -> ThoughtLoopResult:
        """
        Run thought loop until convergence or max iterations.

        Args:
            problem: The problem to analyze
            context: Additional context
            initial_understanding: Starting understanding (optional)
            progress_callback: Optional callback for each iteration

        Returns:
            ThoughtLoopResult with final answer and confidence
        """
        # Initialize
        self.iterations = []
        self.reasoning_trace = []
        self.session_start_time = datetime.now()

        # Initial understanding
        if not initial_understanding:
            initial_understanding = await self._generate_initial_understanding(problem, context)

        self.reasoning_trace.append(f"Initial understanding: {initial_understanding}")

        # Main iteration loop
        for iteration_num in range(1, self.max_iterations + 1):
            self.reasoning_trace.append(f"\n--- Iteration {iteration_num} ---")

            # Get previous understanding (or initial for first iteration)
            if self.iterations:
                previous_understanding = self.iterations[-1].understanding
            else:
                previous_understanding = initial_understanding

            # Run single iteration
            iteration = await self._run_iteration(
                iteration_num=iteration_num,
                problem=problem,
                context=context,
                current_understanding=previous_understanding
            )

            self.iterations.append(iteration)

            # Progress callback
            if progress_callback:
                if asyncio.iscoroutinefunction(progress_callback):
                    await progress_callback(iteration)
                else:
                    progress_callback(iteration)

            # Check for convergence
            if self.convergence_detector.has_converged(self.iterations):
                self.reasoning_trace.append(
                    f"Converged after {iteration_num} iterations with {iteration.confidence:.1%} confidence"
                )
                break

            # Update understanding for next iteration
            if iteration.assumptions_validated:
                # Update understanding based on validations
                updated_understanding = await self._update_understanding(
                    previous_understanding,
                    iteration.assumptions_validated,
                    iteration.first_principles_check
                )
                # Store updated understanding (will be used in next iteration)
                # Note: We don't modify iteration.understanding as it's a record

        # Generate final result
        result = await self._generate_result(problem)

        # Calculate duration
        duration_seconds = (datetime.now() - self.session_start_time).total_seconds()

        # Auto-save to project memory if enabled
        if self.memory_integration and self.auto_save:
            try:
                session_id = await self.memory_integration.save_session(result, duration_seconds)
                self.reasoning_trace.append(f"\nSession saved to project memory: {session_id}")
            except Exception as e:
                self.reasoning_trace.append(f"\nFailed to save to project memory: {e}")

        return result

    async def _run_iteration(
        self,
        iteration_num: int,
        problem: str,
        context: str,
        current_understanding: str
    ) -> Iteration:
        """
        Run a single iteration.

        Args:
            iteration_num: Current iteration number
            problem: Original problem
            context: Additional context
            current_understanding: Understanding from previous iteration

        Returns:
            Iteration with results
        """
        # Step 1: Identify assumptions
        self.reasoning_trace.append("Identifying assumptions...")
        assumptions = await self.assumption_identifier.identify(
            current_understanding,
            context=context
        )

        self.reasoning_trace.append(f"Found {len(assumptions)} assumptions")

        # Step 2: Validate assumptions (in parallel for efficiency)
        self.reasoning_trace.append("Validating assumptions...")
        validations = []

        # Prioritize critical and important assumptions
        try:
            from .models import AssumptionType
        except ImportError:
            from models import AssumptionType
        priority_assumptions = [a for a in assumptions if a.type in [AssumptionType.CRITICAL, AssumptionType.IMPORTANT]]

        if priority_assumptions:
            validations = await self.validator.validate_batch(
                priority_assumptions[:5],  # Limit to 5 per iteration
                parallel=True
            )

        self.reasoning_trace.append(f"Validated {len(validations)} assumptions")

        # Step 3: First-principles check
        self.reasoning_trace.append("Running first-principles check...")
        fp_check = await self.first_principles_checker.check(
            current_understanding,
            problem
        )

        self.reasoning_trace.append(
            f"First-principles check: {'necessary' if fp_check.necessary else 'not necessary'} "
            f"(confidence: {fp_check.confidence:.1%})"
        )

        # Step 4: Calculate confidence
        confidence = await self._calculate_confidence(
            current_understanding,
            validations,
            fp_check
        )

        self.reasoning_trace.append(f"Iteration confidence: {confidence:.1%}")

        # Create iteration object
        return Iteration(
            iteration_number=iteration_num,
            understanding=current_understanding,
            assumptions_identified=assumptions,
            assumptions_validated=validations,
            first_principles_check=fp_check,
            confidence=confidence
        )

    async def _calculate_confidence(
        self,
        understanding: str,
        validations: List[AssumptionValidation],
        fp_check: FirstPrinciplesCheck
    ) -> float:
        """
        Calculate confidence for current understanding.

        Args:
            understanding: Current understanding
            validations: Assumption validations
            fp_check: First-principles check result

        Returns:
            Confidence score (0-1)
        """
        # Start with base confidence
        confidence = 0.5

        # Factor in assumption validations
        if validations:
            valid_count = sum(1 for v in validations if v.validity.value in ["valid", "VALID"])
            invalid_count = sum(1 for v in validations if v.validity.value in ["invalid", "INVALID"])

            # Increase confidence for valid assumptions
            confidence += (valid_count * 0.05)

            # Decrease confidence for invalid assumptions
            confidence -= (invalid_count * 0.1)

            # Add average validation confidence
            avg_validation_conf = sum(v.confidence for v in validations) / len(validations)
            confidence += (avg_validation_conf * 0.1)

        # Factor in first-principles check
        if fp_check:
            # If action is necessary, increase confidence
            # If not necessary, this might indicate we should reconsider
            if fp_check.necessary:
                confidence += (fp_check.confidence * 0.1)
            else:
                # Not necessary - this is actually good (we're avoiding unnecessary work)
                confidence += (fp_check.confidence * 0.15)

        # Clamp to [0, 1]
        return max(0.0, min(1.0, confidence))

    async def _update_understanding(
        self,
        previous_understanding: str,
        validations: List[AssumptionValidation],
        fp_check: Optional[FirstPrinciplesCheck]
    ) -> str:
        """
        Update understanding based on validation results.

        Args:
            previous_understanding: Previous understanding
            validations: Validation results
            fp_check: First-principles check

        Returns:
            Updated understanding
        """
        # Start with previous understanding
        updates = [previous_understanding]

        # Add validation insights
        if validations:
            valid_count = sum(1 for v in validations if v.validity.value in ["valid", "VALID"])
            invalid_count = sum(1 for v in validations if v.validity.value in ["invalid", "INVALID"])

            if valid_count > 0:
                updates.append(f"Validated {valid_count} assumptions through research")
            if invalid_count > 0:
                updates.append(f"Found {invalid_count} invalid assumptions that need reconsideration")

        # Add first-principles insights
        if fp_check and not fp_check.necessary:
            updates.append(f"First-principles check suggests: {fp_check.reasoning}")
            if fp_check.alternatives:
                updates.append(f"Alternative approaches: {', '.join(fp_check.alternatives[:2])}")

        # Combine updates
        if len(updates) == 1:
            return previous_understanding
        else:
            return ". ".join(updates)

    async def _generate_initial_understanding(self, problem: str, context: str) -> str:
        """
        Generate initial understanding of the problem.

        Args:
            problem: The problem statement
            context: Additional context

        Returns:
            Initial understanding
        """
        # If we have an LLM client, use it
        if self.llm_client:
            try:
                prompt = f"""Analyze this problem and provide initial understanding:

Problem: {problem}

Context: {context}

Provide:
1. What is the core problem?
2. What are we trying to achieve?
3. What assumptions might we be making?

Keep it concise (2-3 sentences)."""

                response = await self._call_llm(prompt)
                return response.strip()
            except Exception as e:
                # Fall through to heuristic approach
                pass

        # Heuristic approach: extract key elements
        understanding = f"Addressing: {problem}"

        if context:
            understanding += f". Context: {context[:200]}"

        return understanding

    async def _generate_result(self, problem: str) -> ThoughtLoopResult:
        """
        Generate final result from iterations.

        Args:
            problem: Original problem

        Returns:
            ThoughtLoopResult with final answer
        """
        if not self.iterations:
            return ThoughtLoopResult(
                converged=False,
                final_iteration=0,
                confidence=0.0,
                understanding="No iterations run",
                answer="Unable to determine - no iterations completed",
                iterations=[],
                reasoning_trace=self.reasoning_trace
            )

        latest_iteration = self.iterations[-1]
        converged = self.convergence_detector.has_converged(self.iterations)

        # Generate final answer
        answer = await self._generate_answer(
            problem,
            latest_iteration,
            converged
        )

        return ThoughtLoopResult(
            converged=converged,
            final_iteration=len(self.iterations),
            confidence=latest_iteration.confidence,
            understanding=latest_iteration.understanding,
            answer=answer,
            iterations=self.iterations,
            reasoning_trace=self.reasoning_trace,
            metadata={
                "problem": problem,
                "max_iterations": self.max_iterations,
                "confidence_threshold": self.confidence_threshold,
                "completed_at": datetime.now().isoformat()
            }
        )

    async def _generate_answer(
        self,
        problem: str,
        latest_iteration: Iteration,
        converged: bool
    ) -> str:
        """
        Generate final answer based on iterations.

        Args:
            problem: Original problem
            latest_iteration: Most recent iteration
            converged: Whether converged

        Returns:
            Final answer (YES/NO/MAYBE with reasoning)
        """
        # Check first-principles result
        if latest_iteration.first_principles_check:
            fp_check = latest_iteration.first_principles_check

            # If first-principles says not necessary, answer is NO
            if not fp_check.necessary and fp_check.confidence >= 0.7:
                return f"NO - {fp_check.reasoning}. Alternatives: {', '.join(fp_check.alternatives[:2])}"

        # Check assumption validations
        invalid_count = sum(
            1 for v in latest_iteration.assumptions_validated
            if v.validity.value in ["invalid", "INVALID"]
        )

        if invalid_count > 0 and latest_iteration.confidence < 0.5:
            return f"NO - Found {invalid_count} invalid assumptions. Reconsider the approach."

        # If converged with high confidence, answer YES
        if converged and latest_iteration.confidence >= 0.9:
            return f"YES - {latest_iteration.understanding[:200]}"

        # If not converged but reasonable confidence, MAYBE
        if latest_iteration.confidence >= 0.7:
            return f"LIKELY - {latest_iteration.understanding[:200]}"

        # Low confidence - more research needed
        return f"UNCERTAIN - Need more research. Current understanding: {latest_iteration.understanding[:200]}"

    async def _call_llm(self, prompt: str) -> str:
        """
        Call LLM for reasoning.

        Args:
            prompt: The prompt

        Returns:
            LLM response
        """
        if not self.llm_client:
            raise ValueError("LLM client not configured")

        # This is a placeholder - actual implementation depends on LLM client type
        # Could be Anthropic, OpenAI, etc.

        # For Anthropic Claude:
        # response = await self.llm_client.messages.create(
        #     model="claude-3-5-sonnet-20241022",
        #     max_tokens=1000,
        #     messages=[{"role": "user", "content": prompt}]
        # )
        # return response.content[0].text

        raise NotImplementedError("LLM client integration not implemented")

    def save_state(self, file_path: Path) -> None:
        """
        Save current state to file.

        Args:
            file_path: Path to save state
        """
        state = {
            "iterations": [it.to_dict() for it in self.iterations],
            "reasoning_trace": self.reasoning_trace,
            "max_iterations": self.max_iterations,
            "confidence_threshold": self.confidence_threshold
        }

        with open(file_path, 'w') as f:
            json.dump(state, f, indent=2, default=str)

    def load_state(self, file_path: Path) -> None:
        """
        Load state from file.

        Args:
            file_path: Path to load state from
        """
        with open(file_path) as f:
            state = json.load(f)

        # Restore iterations (simplified - would need proper deserialization)
        self.reasoning_trace = state.get("reasoning_trace", [])
        self.max_iterations = state.get("max_iterations", 10)
        self.confidence_threshold = state.get("confidence_threshold", 0.90)
