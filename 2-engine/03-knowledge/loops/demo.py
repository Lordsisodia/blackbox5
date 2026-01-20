#!/usr/bin/env python3
"""
Demo Script for Thought Loop Framework
======================================

Run this script to see the thought loop in action.

Example:
    python demo.py

The demo will show a thought loop analyzing whether to add caching
to a system where only 11% of time is spent on data fetching.
"""

import asyncio
from pathlib import Path
import sys

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))


async def demo_basic_usage():
    """Demonstrate basic usage of ThoughtLoop"""
    print("=" * 80)
    print("THOUGHT LOOP FRAMEWORK - BASIC DEMO")
    print("=" * 80)
    print()

    from thought_loop import ThoughtLoop

    # Create a thought loop
    loop = ThoughtLoop()

    # Define the problem
    problem = "Should we add caching when only 11% of time is spent on data fetching?"

    print(f"Problem: {problem}")
    print()
    print("Running thought loop...")
    print("-" * 80)

    # Run the thought loop
    result = await loop.run(problem)

    # Display results
    print()
    print("=" * 80)
    print("RESULTS")
    print("=" * 80)
    print()
    print(f"Converged: {result.converged}")
    print(f"Final Iteration: {result.final_iteration}")
    print(f"Confidence: {result.confidence:.1%}")
    print()
    print(f"Answer: {result.answer}")
    print()
    print("=" * 80)
    print("REASONING TRACE")
    print("=" * 80)
    print()
    for trace in result.reasoning_trace:
        print(trace)
    print()
    print("=" * 80)
    print("ITERATION SUMMARY")
    print("=" * 80)
    print()
    print(result.get_iteration_summary())


async def demo_with_progress():
    """Demonstrate thought loop with progress callback"""
    print()
    print("=" * 80)
    print("THOUGHT LOOP WITH PROGRESS CALLBACK")
    print("=" * 80)
    print()

    from thought_loop import ThoughtLoop

    loop = ThoughtLoop(max_iterations=5)

    problem = "Should we optimize the database queries?"

    print(f"Problem: {problem}")
    print()

    # Progress callback to show iteration progress
    def progress_callback(iteration):
        print(f"  [Iteration {iteration.iteration_number}] Confidence: {iteration.confidence:.1%} - {iteration.understanding[:80]}...")

    print("Iterations:")
    result = await loop.run(problem, progress_callback=progress_callback)

    print()
    print(f"Final: {result.answer}")
    print(f"Converged: {result.converged} (confidence: {result.confidence:.1%})")


async def demo_first_principles():
    """Demonstrate first-principles validation"""
    print()
    print("=" * 80)
    print("FIRST-PRINCIPLES VALIDATION DEMO")
    print("=" * 80)
    print()

    from first_principles_checker import FirstPrinciplesChecker

    checker = FirstPrinciplesChecker()

    # Test 1: Necessary action
    print("Test 1: Critical security fix")
    print("-" * 40)
    result1 = await checker.check(
        "We must fix the SQL injection vulnerability immediately",
        problem="Security breach detected"
    )
    print(f"  Necessary: {result1.necessary}")
    print(f"  Confidence: {result1.confidence:.1%}")
    print(f"  Reasoning: {result1.reasoning}")
    print()

    # Test 2: Possibly unnecessary optimization
    print("Test 2: Optimization without measurement")
    print("-" * 40)
    result2 = await checker.check(
        "We should add caching to improve performance"
    )
    print(f"  Necessary: {result2.necessary}")
    print(f"  Confidence: {result2.confidence:.1%}")
    print(f"  Reasoning: {result2.reasoning}")
    if result2.alternatives:
        print(f"  Alternatives:")
        for alt in result2.alternatives:
            print(f"    - {alt}")


async def demo_assumption_identification():
    """Demonstrate assumption identification"""
    print()
    print("=" * 80)
    print("ASSUMPTION IDENTIFICATION DEMO")
    print("=" * 80)
    print()

    from assumption_identifier import AssumptionIdentifier

    identifier = AssumptionIdentifier()

    understanding = """
    I assume that caching will significantly improve performance.
    I also assume that the database is the bottleneck.
    Presumably, adding Redis will reduce load times.
    We might need to invalidate the cache properly.
    """

    print("Understanding:")
    print(understanding.strip())
    print()
    print("Identified Assumptions:")
    print("-" * 40)

    assumptions = await identifier.identify(understanding)

    for i, assumption in enumerate(assumptions, 1):
        print(f"  {i}. [{assumption.type.value.upper()}] {assumption.statement}")

    print()
    print("Prioritized:")
    print("-" * 40)

    prioritized = identifier.prioritize(assumptions)
    for i, assumption in enumerate(prioritized, 1):
        print(f"  {i}. [{assumption.type.value.upper()}] {assumption.statement}")


async def demo_validation():
    """Demonstrate assumption validation"""
    print()
    print("=" * 80)
    print("ASSUMPTION VALIDATION DEMO")
    print("=" * 80)
    print()

    from models import Assumption, AssumptionType
    from validation import ValidationModule

    validator = ValidationModule()

    # Test assumptions
    assumptions = [
        Assumption("Caching improves performance", AssumptionType.IMPORTANT),
        Assumption("Database is the bottleneck", AssumptionType.CRITICAL),
    ]

    print("Validating assumptions...")
    print()

    for assumption in assumptions:
        print(f"Assumption: {assumption.statement}")
        print("-" * 40)

        validation = await validator.validate(assumption)

        print(f"  Validity: {validation.validity.value}")
        print(f"  Confidence: {validation.confidence:.1%}")
        print(f"  Reasoning: {validation.reasoning}")
        print(f"  Evidence: {len(validation.supporting_evidence)} supporting, "
              f"{len(validation.contradicting_evidence)} contradicting")
        print()


async def demo_save_load():
    """Demonstrate saving and loading state"""
    print()
    print("=" * 80)
    print("SAVE/LOAD STATE DEMO")
    print("=" * 80)
    print()

    from thought_loop import ThoughtLoop
    import tempfile
    from pathlib import Path

    # Run a loop
    loop = ThoughtLoop(max_iterations=3)
    result = await loop.run("Should we add tests?")

    # Save state
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        state_file = Path(f.name)

    loop.save_state(state_file)
    print(f"Saved state to: {state_file}")

    # Load into new loop
    new_loop = ThoughtLoop()
    new_loop.load_state(state_file)
    print(f"Loaded state into new loop")
    print(f"  Max iterations: {new_loop.max_iterations}")
    print(f"  Confidence threshold: {new_loop.confidence_threshold}")

    # Clean up
    state_file.unlink()


async def main():
    """Run all demos"""
    await demo_basic_usage()
    await demo_with_progress()
    await demo_first_principles()
    await demo_assumption_identification()
    await demo_validation()
    await demo_save_load()

    print()
    print("=" * 80)
    print("DEMO COMPLETE")
    print("=" * 80)
    print()
    print("The Thought Loop Framework is ready to use!")
    print()
    print("Key features:")
    print("  - Iterative first-principles reasoning (up to 10 iterations)")
    print("  - Automatic assumption identification and validation")
    print("  - Research-backed validation (git history, codebase search)")
    print("  - First-principles necessity checking")
    print("  - Convergence detection (90% confidence threshold)")
    print()
    print("Import and use:")
    print()
    print("  from thought_loop import ThoughtLoop")
    print()
    print("  loop = ThoughtLoop()")
    print("  result = await loop.run('Your problem here')")
    print("  print(result.answer)")


if __name__ == "__main__":
    asyncio.run(main())
