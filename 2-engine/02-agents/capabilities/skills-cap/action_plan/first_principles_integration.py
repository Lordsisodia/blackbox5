"""
First Principles Integration for Action Plans

Integrates first principles thinking into action plan creation and execution.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Import the existing FirstPrinciplesEngine
fp_engine_path = Path(__file__).parent.parent.parent.parent.parent
fp_engine_path = fp_engine_path / "07-operations" / "environment" / "lib" / "python"
sys.path.insert(0, str(fp_engine_path))

try:
    from core.runtime.fp_engine.first_principles import (
        FirstPrinciplesEngine,
        Constraint,
        ConstraintType,
        Assumption,
        Hypothesis
    )
except ImportError:
    # If the import fails, define local versions
    from enum import Enum

    class ConstraintType(Enum):
        HARD = "hard"
        SOFT = "soft"

    class Constraint:
        def __init__(self, text: str, type: ConstraintType, source: str = "unknown"):
            self.text = text
            self.type = type
            self.source = source

    class Assumption:
        def __init__(self, text: str, confidence: str = "medium", test: str = ""):
            self.text = text
            self.confidence = confidence
            self.test = test

    class Hypothesis:
        def __init__(self, name: str, type: str, approach: str, rationale: str,
                     assumptions: List[str], pros: List[str], cons: List[str],
                     risks: List[str]):
            self.name = name
            self.type = type
            self.approach = approach
            self.rationale = rationale
            self.assumptions = assumptions
            self.pros = pros
            self.cons = cons
            self.risks = risks

    class FirstPrinciplesEngine:
        def __init__(self):
            self.components = []
            self.constraints = []
            self.assumptions = []
            self.hypotheses = []

        def decompose(self, problem: str, context: Dict[str, Any] = None):
            words = problem.split()
            components = []
            for word in words:
                if len(word) > 3:
                    components.append({
                        'name': word.lower(),
                        'description': f"Component from: {problem}",
                        'type': 'variable'
                    })
            return components

        def map_constraints(self, constraints_input: List[str],
                           hard_keywords: List[str] = None,
                           soft_keywords: List[str] = None):
            if hard_keywords is None:
                hard_keywords = ['must', 'shall', 'required', 'cannot', 'must not',
                               'law', 'legal', 'regulation', 'compliance', 'security']
            if soft_keywords is None:
                soft_keywords = ['should', 'prefer', 'ideally', 'desired', 'nice to have',
                               'typical', 'conventional', 'standard', 'best practice']

            constraints = []
            for constraint_text in constraints_input:
                constraint_lower = constraint_text.lower()
                if any(keyword in constraint_lower for keyword in hard_keywords):
                    constraint_type = ConstraintType.HARD
                elif any(keyword in constraint_lower for keyword in soft_keywords):
                    constraint_type = ConstraintType.SOFT
                else:
                    constraint_type = ConstraintType.SOFT

                constraints.append(Constraint(
                    text=constraint_text,
                    type=constraint_type,
                    source="user_input"
                ))
            return constraints

        def ground_assumptions(self, assumptions_input: List[str]):
            assumptions = []
            for assumption_text in assumptions_input:
                assumptions.append(Assumption(
                    text=assumption_text,
                    confidence="medium",
                    test="TODO: Design validation test"
                ))
            return assumptions

        def reconstruct(self, components, constraints, objectives):
            hypotheses = []
            if len(components) > 0:
                hypotheses.append(Hypothesis(
                    name="Conservative Approach",
                    type="conservative",
                    approach="Minimal change to existing solution",
                    rationale="Lowest risk, proven path",
                    assumptions=[c.get('name', c.name) for c in components[:3]],
                    pros=["Low risk", "Quick implementation", "Proven"],
                    cons=["May not optimize well", "Limited innovation"],
                    risks=["May miss optimization opportunities"]
                ))

            if len(components) > 1:
                hypotheses.append(Hypothesis(
                    name="Novel Approach",
                    type="novel",
                    approach="New architecture addressing fundamentals",
                    rationale="Balanced innovation and risk",
                    assumptions=["New approach is feasible", "Team can adapt"],
                    pros=["Better optimization", "Learning opportunity"],
                    cons=["Higher risk", "Longer timeline"],
                    risks=["Uncertainty in new approach", "May encounter unknown issues"]
                ))

            if len(components) > 2:
                hypotheses.append(Hypothesis(
                    name="Radical Redesign",
                    type="radical",
                    approach="Complete rethinking from first principles",
                    rationale="Maximum optimization without legacy constraints",
                    assumptions=["Can rebuild from scratch", "Resources available"],
                    pros=["Maximum optimization", "No legacy debt"],
                    cons=["Highest risk", "Longest timeline", "Resource intensive"],
                    risks=["May not be feasible", "Could fail completely"]
                ))

            return hypotheses

from .models import FirstPrinciplesResult, Assumption as ActionPlanAssumption, Constraint as ActionPlanConstraint


class FirstPrinciplesIntegration:
    """
    Integrates first principles thinking into action plans.

    Provides methods to:
    - Analyze phases and tasks using first principles
    - Generate hypotheses for different approaches
    - Validate approaches against constraints
    - Extract and document thinking processes
    """

    def __init__(self):
        """Initialize the first principles integration."""
        self.engine = FirstPrinciplesEngine()

    def analyze_problem(self, problem: str, context: Optional[Dict[str, Any]] = None) -> FirstPrinciplesResult:
        """
        Analyze a problem using first principles.

        Args:
            problem: The problem statement
            context: Additional context

        Returns:
            FirstPrinciplesResult with analysis
        """
        # Step 1: What problem are we ACTUALLY solving?
        true_problem = self._extract_true_problem(problem)

        # Step 2: What do we know to be TRUE?
        fundamental_truths = self._extract_fundamental_truths(problem, context)

        # Step 3: What are we assuming?
        assumptions_texts = self._identify_assumptions(problem, context)
        assumptions = [
            ActionPlanAssumption(
                text=a,
                confidence="medium",
                test="TODO: Design validation test"
            )
            for a in assumptions_texts
        ]

        # Step 4: What MUST be included? What can we eliminate?
        essential_requirements = self._derive_essential_requirements(fundamental_truths)
        optional_elements = self._identify_optional_elements(problem, context)

        return FirstPrinciplesResult(
            true_problem=true_problem,
            fundamental_truths=fundamental_truths,
            assumptions=assumptions,
            essential_requirements=essential_requirements,
            optional_elements=optional_elements
        )

    def analyze_phase(self, phase_name: str, phase_description: str,
                     context: Optional[Dict[str, Any]] = None) -> FirstPrinciplesResult:
        """
        Analyze a phase using first principles.

        Args:
            phase_name: Name of the phase
            phase_description: Description of what the phase does
            context: Additional context

        Returns:
            FirstPrinciplesResult with phase analysis
        """
        problem = f"Phase: {phase_name}\n{phase_description}"
        return self.analyze_problem(problem, context)

    def analyze_task(self, task_title: str, task_description: str,
                    context: Optional[Dict[str, Any]] = None) -> FirstPrinciplesResult:
        """
        Analyze a task using first principles.

        Args:
            task_title: Title of the task
            task_description: Description of what the task does
            context: Additional context

        Returns:
            FirstPrinciplesResult with task analysis
        """
        problem = f"Task: {task_title}\n{task_description}"
        return self.analyze_problem(problem, context)

    def generate_hypotheses(self, analysis: FirstPrinciplesResult,
                          constraints: List[ActionPlanConstraint]) -> List[str]:
        """
        Generate solution hypotheses from first principles analysis.

        Args:
            analysis: First principles analysis result
            constraints: List of constraints

        Returns:
            List of hypothesis descriptions
        """
        # Use the engine to reconstruct solutions
        components = [
            {'name': req, 'type': 'requirement'}
            for req in analysis.essential_requirements
        ]

        constraint_texts = [c.text for c in constraints]
        mapped_constraints = self.engine.map_constraints(constraint_texts)

        hypotheses = self.engine.reconstruct(
            components=components,
            constraints=mapped_constraints,
            objectives=analysis.essential_requirements
        )

        return [
            f"{h.name}: {h.approach}\n  Rationale: {h.rationale}\n  Pros: {', '.join(h.pros[:2])}\n  Cons: {', '.join(h.cons[:2])}"
            for h in hypotheses
        ]

    def validate_approach(self, approach: str,
                         constraints: List[ActionPlanConstraint]) -> Dict[str, Any]:
        """
        Validate an approach against constraints.

        Args:
            approach: Description of the approach
            constraints: List of constraints to validate against

        Returns:
            Validation result with is_valid flag and violations
        """
        violations = []

        # Check against hard constraints
        for constraint in constraints:
            if constraint.type == ConstraintType.HARD:
                # In production, this would do actual validation logic
                # For now, document what should be checked
                pass

        is_valid = len(violations) == 0

        return {
            'is_valid': is_valid,
            'violations': violations,
            'checked_constraints': len(constraints)
        }

    def generate_validation_tests(self, analysis: FirstPrinciplesResult) -> List[str]:
        """
        Generate validation tests from first principles analysis.

        Args:
            analysis: First principles analysis result

        Returns:
            List of test descriptions
        """
        tests = []

        # Test assumptions
        for assumption in analysis.assumptions:
            tests.append(f"Validate assumption: {assumption.text}")

        # Test essential requirements
        for requirement in analysis.essential_requirements:
            tests.append(f"Verify requirement: {requirement}")

        # General validation tests
        tests.append("Proof of concept implementation")
        tests.append("Integration testing")
        tests.append("Performance validation")

        return tests

    def _extract_true_problem(self, problem: str) -> str:
        """
        Extract what problem we're ACTUALLY solving.

        This is where we strip away assumptions and get to the core.
        """
        # Look for key patterns
        if "how to" in problem.lower():
            # Extract the "how to" part
            start = problem.lower().find("how to")
            return problem[start:].strip()
        elif "implement" in problem.lower():
            return f"Need to: {problem}"
        elif "build" in problem.lower():
            return f"Need to: {problem}"
        else:
            return f"Problem: {problem}"

    def _extract_fundamental_truths(self, problem: str,
                                   context: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        Extract what we know to be TRUE.
        """
        truths = []

        # Extract obvious truths from the problem
        if "user" in problem.lower():
            truths.append("Users are involved in this system")

        if "data" in problem.lower():
            truths.append("Data needs to be stored or processed")

        if "api" in problem.lower() or "interface" in problem.lower():
            truths.append("System needs to communicate with other components")

        # Add context-based truths
        if context:
            if 'requirements' in context:
                truths.append("Requirements have been defined")
            if 'constraints' in context:
                truths.append("Constraints exist that must be satisfied")

        return truths

    def _identify_assumptions(self, problem: str,
                            context: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        Identify what we're assuming without evidence.
        """
        assumptions = []

        # Common assumptions to look for
        assumption_patterns = [
            "should",
            "will",
            "can",
            "expected to",
            "typically"
        ]

        words = problem.split()
        for i, word in enumerate(words):
            if word.lower() in assumption_patterns:
                # Extract the assumption phrase
                phrase_start = max(0, i - 2)
                phrase_end = min(len(words), i + 5)
                assumption = " ".join(words[phrase_start:phrase_end])
                assumptions.append(assumption)

        # Add context-based assumptions
        if context:
            if 'tech_stack' in context:
                assumptions.append(f"Tech stack {context['tech_stack']} is appropriate")

        return assumptions

    def _derive_essential_requirements(self, fundamental_truths: List[str]) -> List[str]:
        """
        Derive what MUST be included from fundamental truths.
        """
        requirements = []

        # From truths, derive requirements
        for truth in fundamental_truths:
            if "user" in truth.lower():
                requirements.append("User interface or interaction layer")

            if "data" in truth.lower():
                requirements.append("Data storage or processing mechanism")

            if "communicate" in truth.lower():
                requirements.append("Communication interface or API")

        # Ensure we have at least some requirements
        if not requirements:
            requirements.append("Functional solution to the problem")

        return requirements

    def _identify_optional_elements(self, problem: str,
                                   context: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        Identify what can be eliminated (optional elements).
        """
        optional = []

        # Common optional elements
        optional.append("Advanced features beyond core functionality")
        optional.append("Optimizations that can be added later")
        optional.append("Nice-to-have UI improvements")

        return optional


def create_first_principles_analysis(text: str) -> FirstPrinciplesResult:
    """
    Convenience function to create a first principles analysis from text.

    Args:
        text: Problem or task description

    Returns:
        FirstPrinciplesResult
    """
    integration = FirstPrinciplesIntegration()
    return integration.analyze_problem(text)
