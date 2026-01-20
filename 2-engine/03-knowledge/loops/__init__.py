"""
Thought Loop Framework
======================

A framework for iterative first-principles reasoning with assumption validation
and convergence detection. Enables AI agents to think deeply about problems and
converge on high-confidence answers through research and self-questioning.

Example:
    .. code-block:: python

        from blackbox5.engine.knowledge.loops import ThoughtLoop

        loop = ThoughtLoop()
        result = await loop.run("Should we add caching to this system?")

        if result.converged:
            print(f"Answer: {result.answer} (confidence: {result.confidence:.1%})")
        else:
            print(f"Best effort after {result.final_iteration} iterations")

Core Components:
    - ThoughtLoop: Main orchestration engine
    - AssumptionIdentifier: Extract assumptions from reasoning
    - ValidationModule: Research-backed assumption validation
    - FirstPrinciplesChecker: "Do you even need to do this?" validation
    - ConvergenceDetector: Detect when reasoning has stabilized

Enhanced Components (for deeper analysis):
    - LogicalValidator: Detect fallacies and validate reasoning structure
    - SocraticQuestioner: Systematic questioning for deeper analysis
    - BayesianUpdater: Proper confidence updating using Bayes' theorem
    - ChainOfThoughtVerifier: Make reasoning explicit and verifiable
    - FiveWhysAnalyzer: Root cause analysis through systematic questioning

Project Memory Integration:
    - ProjectMemoryIntegration: Automatic saving to Blackbox5 project memory
"""

from .models import (
    Assumption,
    AssumptionType,
    AssumptionValidation,
    Iteration,
    ThoughtLoopResult,
    FirstPrinciplesCheck,
    Evidence,
)

# Core components
from .thought_loop import ThoughtLoop
from .assumption_identifier import AssumptionIdentifier
from .validation import ValidationModule
from .first_principles_checker import FirstPrinciplesChecker
from .convergence import ConvergenceDetector

# Enhanced components
from .logical_validator import LogicalValidator, ValidationResult, FallacyDetection
from .socratic_questioner import (
    SocraticQuestioner,
    SocraticQuestion,
    DialogueRound,
    QuestioningSession,
)
from .bayesian_updater import BayesianUpdater, BayesianUpdate, BeliefState
from .chain_of_thought import (
    ChainOfThoughtVerifier,
    ReasoningStep,
    ReasoningChain,
    VerificationResult,
)
from .five_whys import FiveWhysAnalyzer, WhyLevel, FiveWhysResult

# Project memory integration
from .project_memory import ProjectMemoryIntegration

__all__ = [
    # Models
    "Assumption",
    "AssumptionType",
    "AssumptionValidation",
    "Iteration",
    "ThoughtLoopResult",
    "FirstPrinciplesCheck",
    "Evidence",
    # Core Components
    "ThoughtLoop",
    "AssumptionIdentifier",
    "ValidationModule",
    "FirstPrinciplesChecker",
    "ConvergenceDetector",
    # Enhanced Components - Logical Validation
    "LogicalValidator",
    "ValidationResult",
    "FallacyDetection",
    # Enhanced Components - Socratic Questioning
    "SocraticQuestioner",
    "SocraticQuestion",
    "DialogueRound",
    "QuestioningSession",
    # Enhanced Components - Bayesian Updating
    "BayesianUpdater",
    "BayesianUpdate",
    "BeliefState",
    # Enhanced Components - Chain of Thought
    "ChainOfThoughtVerifier",
    "ReasoningStep",
    "ReasoningChain",
    "VerificationResult",
    # Enhanced Components - Five Whys
    "FiveWhysAnalyzer",
    "WhyLevel",
    "FiveWhysResult",
    # Project Memory Integration
    "ProjectMemoryIntegration",
]
