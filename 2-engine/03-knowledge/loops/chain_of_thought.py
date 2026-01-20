"""
Chain-of-Thought Verifier for Thought Loop Framework
===================================================

Makes reasoning explicit and verifiable through step-by-step breakdown.
Addresses the "knowing decisions are correct" requirement.
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
import re

try:
    from .models import Assumption, AssumptionType
except ImportError:
    from models import Assumption, AssumptionType


@dataclass
class ReasoningStep:
    """A single step in a reasoning chain"""
    step_number: int
    premise: str
    reasoning: str
    conclusion: str
    assumptions: List[str] = field(default_factory=list)
    is_valid: Optional[bool] = None
    confidence: float = 0.5
    evidence: List[str] = field(default_factory=list)


@dataclass
class ReasoningChain:
    """A complete chain of reasoning"""
    steps: List[ReasoningStep]
    final_conclusion: str
    overall_validity: Optional[bool] = None
    overall_confidence: float = 0.0
    identified_assumptions: List[str] = field(default_factory=list)
    verification_report: Dict = field(default_factory=dict)


@dataclass
class VerificationResult:
    """Result of verifying a reasoning chain"""
    is_valid: bool
    is_complete: bool
    is_sound: bool
    weak_links: List[int]  # Step numbers with weak reasoning
    missing_assumptions: List[str]
    suggestions: List[str]
    confidence_score: float


class ChainOfThoughtVerifier:
    """
    Verifies reasoning by making it explicit and step-by-step.

    Addresses the "knowing decisions are correct" requirement by:
    1. Breaking reasoning into explicit, verifiable steps
    2. Identifying assumptions at each step
    3. Validating each inference step
    4. Detecting weak links in the reasoning chain
    5. Generating improvement suggestions
    """

    def __init__(self):
        self.step_indicators = [
            'first', 'second', 'third', 'fourth', 'fifth',
            'next', 'then', 'after that', 'finally',
            'step', 'therefore', 'thus', 'so', 'consequently'
        ]

    def parse_reasoning_chain(self, reasoning: str) -> ReasoningChain:
        """
        Parse reasoning text into explicit reasoning steps.

        Args:
            reasoning: The reasoning text to parse

        Returns:
            ReasoningChain with parsed steps
        """
        # Try to detect explicit steps
        steps = self._extract_steps(reasoning)

        # If no explicit steps found, treat as single step
        if not steps:
            steps = [ReasoningStep(
                step_number=1,
                premise="Given the problem",
                reasoning=reasoning,
                conclusion=self._extract_conclusion(reasoning),
                assumptions=[],
                confidence=0.5
            )]

        # Extract final conclusion
        final_conclusion = steps[-1].conclusion if steps else ""

        # Identify all assumptions
        all_assumptions = []
        for step in steps:
            all_assumptions.extend(step.assumptions)

        return ReasoningChain(
            steps=steps,
            final_conclusion=final_conclusion,
            identified_assumptions=list(set(all_assumptions))
        )

    def verify_chain(self, chain: ReasoningChain) -> VerificationResult:
        """
        Verify a reasoning chain for validity and soundness.

        Args:
            chain: The reasoning chain to verify

        Returns:
            VerificationResult with detailed analysis
        """
        # Verify each step
        weak_links = []
        missing_assumptions = []
        suggestions = []

        for step in chain.steps:
            step_result = self._verify_step(step)

            if not step_result['is_valid']:
                weak_links.append(step.step_number)

            missing_assumptions.extend(step_result['missing_assumptions'])
            suggestions.extend(step_result['suggestions'])

        # Check overall validity
        is_valid = len(weak_links) == 0

        # Check completeness
        is_complete = self._check_completeness(chain)

        # Check soundness (are premises reasonable?)
        is_sound = self._check_soundness(chain)

        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(
            is_valid, is_complete, is_sound, len(weak_links), len(chain.steps)
        )

        return VerificationResult(
            is_valid=is_valid,
            is_complete=is_complete,
            is_sound=is_sound,
            weak_links=weak_links,
            missing_assumptions=list(set(missing_assumptions)),
            suggestions=list(set(suggestions)),
            confidence_score=confidence_score
        )

    def create_chain_from_understanding(self, understanding: str) -> ReasoningChain:
        """
        Create a structured reasoning chain from freeform understanding.

        Args:
            understanding: The understanding text

        Returns:
            ReasoningChain with structured steps
        """
        # Break understanding into logical steps
        sentences = [s.strip() for s in understanding.split('.') if s.strip()]

        steps = []
        for i, sentence in enumerate(sentences):
            # Try to classify sentence type
            if i == 0:
                # First sentence is likely premise
                step = ReasoningStep(
                    step_number=i + 1,
                    premise=sentence,
                    reasoning="Initial understanding",
                    conclusion=sentence,
                    confidence=0.5
                )
            elif i == len(sentences) - 1:
                # Last sentence is likely conclusion
                step = ReasoningStep(
                    step_number=i + 1,
                    premise=sentences[i - 1] if i > 0 else "",
                    reasoning="Final reasoning",
                    conclusion=sentence,
                    confidence=0.6
                )
            else:
                # Middle sentences are reasoning steps
                step = ReasoningStep(
                    step_number=i + 1,
                    premise=sentences[i - 1] if i > 0 else "",
                    reasoning=sentence,
                    conclusion=sentence,
                    confidence=0.5
                )

            steps.append(step)

        return ReasoningChain(
            steps=steps,
            final_conclusion=sentences[-1] if sentences else "",
            overall_confidence=0.5
        )

    def improve_chain(self, chain: ReasoningChain,
                      verification: VerificationResult) -> ReasoningChain:
        """
        Improve a reasoning chain based on verification results.

        Args:
            chain: The original reasoning chain
            verification: Verification results

        Returns:
            Improved ReasoningChain
        """
        improved_steps = []

        for step in chain.steps:
            # Check if this is a weak link
            if step.step_number in verification.weak_links:
                # Add explicit assumptions
                step.assumptions = [
                    f"Assumption needed for step {step.step_number}",
                    "Need to verify this inference"
                ]

                # Lower confidence for weak steps
                step.confidence = max(0.3, step.confidence - 0.2)

                # Add evidence placeholder
                step.evidence.append(f"Evidence needed to verify step {step.step_number}")

            # Mark validity
            step.is_valid = step.step_number not in verification.weak_links

            improved_steps.append(step)

        # Update overall properties
        improved_chain = ReasoningChain(
            steps=improved_steps,
            final_conclusion=chain.final_conclusion,
            overall_validity=verification.is_valid,
            overall_confidence=verification.confidence_score,
            verification_report={
                'weak_links': verification.weak_links,
                'suggestions': verification.suggestions
            }
        )

        return improved_chain

    def validate_explicitness(self, reasoning: str) -> Dict[str, any]:
        """
        Check if reasoning is explicit and verifiable.

        Args:
            reasoning: The reasoning text to check

        Returns:
            Dict with explicitness assessment
        """
        assessment = {
            'is_explicit': False,
            'has_clear_steps': False,
            'has_explicit_conclusions': False,
            'has_explanatory_connectors': False,
            'verdict': '',
            'suggestions': []
        }

        reasoning_lower = reasoning.lower()

        # Check for step indicators
        has_steps = any(indicator in reasoning_lower for indicator in self.step_indicators)
        assessment['has_clear_steps'] = has_steps

        # Check for explicit conclusions
        conclusion_indicators = ['therefore', 'thus', 'so', 'consequently', 'hence']
        has_conclusions = any(ind in reasoning_lower for ind in conclusion_indicators)
        assessment['has_explicit_conclusions'] = has_conclusions

        # Check for explanatory connectors
        explanatory_indicators = ['because', 'since', 'given that', 'as a result', 'leads to']
        has_explanatory = any(ind in reasoning_lower for ind in explanatory_indicators)
        assessment['has_explanatory_connectors'] = has_explanatory

        # Overall explicitness
        explicitness_score = sum([
            assessment['has_clear_steps'],
            assessment['has_explicit_conclusions'],
            assessment['has_explanatory_connectors']
        ]) / 3.0

        assessment['is_explicit'] = explicitness_score >= 0.5

        if explicitness_score >= 0.7:
            assessment['verdict'] = "Highly explicit - reasoning is clear and verifiable"
        elif explicitness_score >= 0.5:
            assessment['verdict'] = "Moderately explicit - some steps could be clearer"
        else:
            assessment['verdict'] = "Not explicit enough - reasoning needs more structure"

        # Generate suggestions
        if not assessment['has_clear_steps']:
            assessment['suggestions'].append(
                "Break reasoning into explicit steps (first, then, next, finally)"
            )

        if not assessment['has_explicit_conclusions']:
            assessment['suggestions'].append(
                "Use conclusion indicators (therefore, thus, consequently)"
            )

        if not assessment['has_explanatory_connectors']:
            assessment['suggestions'].append(
                "Add explanatory connectors (because, since, leads to)"
            )

        return assessment

    def _extract_steps(self, reasoning: str) -> List[ReasoningStep]:
        """Extract reasoning steps from text."""
        steps = []
        sentences = [s.strip() for s in reasoning.split('.') if s.strip()]

        current_step = 1
        for i, sentence in enumerate(sentences):
            # Check if this sentence starts a new step
            if any(indicator in sentence.lower() for indicator in self.step_indicators):
                step = ReasoningStep(
                    step_number=current_step,
                    premise=sentences[i - 1] if i > 0 else "Given context",
                    reasoning=sentence,
                    conclusion=sentences[i + 1] if i + 1 < len(sentences) else sentence,
                    confidence=0.5
                )
                steps.append(step)
                current_step += 1

        return steps

    def _extract_conclusion(self, text: str) -> str:
        """Extract the conclusion from reasoning text."""
        # Look for conclusion indicators
        conclusion_indicators = ['therefore', 'thus', 'so', 'consequently', 'hence']

        sentences = [s.strip() for s in text.split('.') if s.strip()]

        for sentence in reversed(sentences):  # Check from end
            for indicator in conclusion_indicators:
                if indicator in sentence.lower():
                    return sentence

        # If no explicit conclusion, return last sentence
        return sentences[-1] if sentences else ""

    def _verify_step(self, step: ReasoningStep) -> Dict:
        """Verify a single reasoning step."""
        result = {
            'is_valid': True,
            'missing_assumptions': [],
            'suggestions': []
        }

        # Check if premise is empty
        if not step.premise or step.premise == "Given context":
            result['missing_assumptions'].append(
                f"Step {step.step_number} lacks clear premise"
            )
            result['suggestions'].append(
                f"State the starting assumption for step {step.step_number}"
            )
            # Don't mark as invalid, but note the issue

        # Check if reasoning is too brief
        if len(step.reasoning) < 20:
            result['suggestions'].append(
                f"Expand reasoning in step {step.step_number} - too brief"
            )

        # Check if conclusion follows
        if not step.conclusion or step.conclusion == step.premise:
            result['is_valid'] = False
            result['suggestions'].append(
                f"Step {step.step_number} conclusion doesn't advance the reasoning"
            )

        # Check for logical connectors
        if 'because' not in step.reasoning.lower() and 'therefore' not in step.reasoning.lower():
            if len(step.reasoning) > 30:  # Only for longer reasoning
                result['suggestions'].append(
                    f"Add logical connectors (because, therefore) to step {step.step_number}"
                )

        return result

    def _check_completeness(self, chain: ReasoningChain) -> bool:
        """Check if reasoning chain is complete."""
        if not chain.steps:
            return False

        # Has at least 2 steps (premise → conclusion)
        if len(chain.steps) < 2:
            return False

        # Has explicit final conclusion
        if not chain.final_conclusion:
            return False

        return True

    def _check_soundness(self, chain: ReasoningChain) -> bool:
        """Check if premises are reasonable (soundness)."""
        # This is a simplified check
        # In practice, would need knowledge base to verify premises

        for step in chain.steps:
            # Check for obviously problematic premises
            if 'obviously' in step.premise.lower() and not step.evidence:
                return False

            if 'clearly' in step.premise.lower() and not step.evidence:
                return False

        return True

    def _calculate_confidence_score(self, is_valid: bool, is_complete: bool,
                                    is_sound: bool, weak_links: int,
                                    total_steps: int) -> float:
        """Calculate overall confidence score."""
        score = 0.5  # Base score

        if is_valid:
            score += 0.2

        if is_complete:
            score += 0.15

        if is_sound:
            score += 0.15

        # Penalize for weak links
        weak_ratio = weak_links / total_steps if total_steps > 0 else 0
        score -= weak_ratio * 0.3

        return max(0.0, min(1.0, score))
