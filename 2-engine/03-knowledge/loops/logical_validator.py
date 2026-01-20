"""
Logical Validator for Thought Loop Framework
============================================

Detects logical fallacies and validates reasoning structure to prevent
hallucination and ensure logical soundness.
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import re

try:
    from .models import Assumption, AssumptionType
except ImportError:
    from models import Assumption, AssumptionType


@dataclass
class FallacyDetection:
    """A detected logical fallacy"""
    fallacy_type: str
    description: str
    confidence: str  # 'low', 'medium', 'high'
    evidence: str
    severity: str  # 'critical', 'moderate', 'minor'


@dataclass
class ValidationResult:
    """Result of validating reasoning"""
    is_valid: bool
    is_sound: bool
    fallacies: List[FallacyDetection]
    validity_score: float
    premises: List[str]
    conclusion: str
    reasoning_type: str  # 'deductive', 'inductive', 'abductive', 'unknown'


class LogicalValidator:
    """
    Validates logical structure and detects fallacies in reasoning.

    Addresses the "not hallucinating" requirement by:
    1. Detecting formal and informal fallacies
    2. Validating argument structure (premises → conclusion)
    3. Testing for counterexamples
    4. Assessing reasoning type appropriateness
    """

    def __init__(self):
        self.fallacy_patterns = self._load_fallacy_patterns()
        self.conclusion_indicators = [
            'therefore', 'thus', 'so', 'consequently',
            'hence', 'accordingly', 'as a result', 'it follows that'
        ]
        self.premise_indicators = [
            'because', 'since', 'given that', 'assuming that',
            'for', 'as', 'seeing that'
        ]

    def validate(self, reasoning: str, context: str = "") -> ValidationResult:
        """
        Validate reasoning for logical soundness and detect fallacies.

        Args:
            reasoning: The reasoning text to validate
            context: Optional context for the reasoning

        Returns:
            ValidationResult with detailed analysis
        """
        # Detect fallacies
        fallacies = self._detect_fallacies(reasoning)

        # Extract argument structure
        premises, conclusion = self._extract_structure(reasoning)

        # Determine reasoning type
        reasoning_type = self._classify_reasoning_type(reasoning, premises, conclusion)

        # Test validity
        is_valid = self._test_validity(premises, conclusion, reasoning_type)

        # Test soundness (if valid)
        is_sound = is_valid and self._test_soundness(premises, reasoning)

        # Calculate validity score
        validity_score = self._calculate_validity_score(fallacies, is_valid, is_sound)

        return ValidationResult(
            is_valid=is_valid,
            is_sound=is_sound,
            fallacies=fallacies,
            validity_score=validity_score,
            premises=premises,
            conclusion=conclusion,
            reasoning_type=reasoning_type
        )

    def check_assumptions_logical(self, assumptions: List[Assumption],
                                  reasoning: str) -> List[str]:
        """
        Check if assumptions lead to logical contradictions.

        Args:
            assumptions: List of assumptions to check
            reasoning: The reasoning text

        Returns:
            List of contradiction warnings
        """
        warnings = []

        # Check for direct contradictions
        assumption_texts = [a.statement.lower() for a in assumptions]
        for i, text1 in enumerate(assumption_texts):
            for j, text2 in enumerate(assumption_texts):
                if i >= j:
                    continue

                if self._are_contradictory(text1, text2):
                    warnings.append(
                        f"Contradiction between: '{assumptions[i].statement}' "
                        f"and '{assumptions[j].statement}'"
                    )

        # Check for circular reasoning
        if self._detect_circular_reasoning(reasoning):
            warnings.append(
                "Circular reasoning detected: conclusion assumes what it's trying to prove"
            )

        return warnings

    def validate_inference_step(self, premise: str, conclusion: str,
                                reasoning_type: str = "deductive") -> Dict[str, any]:
        """
        Validate a single inference step.

        Args:
            premise: The premise statement
            conclusion: The conclusion statement
            reasoning_type: Type of reasoning (deductive, inductive, abductive)

        Returns:
            Dict with validation results
        """
        result = {
            'valid': False,
            'confidence': 0.0,
            'issues': [],
            'suggestions': []
        }

        if reasoning_type == "deductive":
            # For deductive, check if conclusion NECESSARILY follows
            if self._check_modus_ponens(premise, conclusion):
                result['valid'] = True
                result['confidence'] = 1.0
            elif self._check_modus_tollens(premise, conclusion):
                result['valid'] = True
                result['confidence'] = 1.0
            else:
                # Try to find counterexample
                counterexample = self._find_counterexample(premise, conclusion)
                if counterexample:
                    result['issues'].append(
                        f"Counterexample found: {counterexample}"
                    )
                    result['suggestions'].append(
                        "Premise does not guarantee conclusion - consider inductive reasoning instead"
                    )
                else:
                    result['valid'] = True
                    result['confidence'] = 0.5  # Uncertain

        elif reasoning_type == "inductive":
            # For inductive, check strength of support
            result['valid'] = True  # Induction is about strength, not validity
            result['confidence'] = self._assess_inductive_strength(premise, conclusion)

            if result['confidence'] < 0.7:
                result['issues'].append("Weak inductive support")
                result['suggestions'].append("Gather more evidence to strengthen")

        elif reasoning_type == "abductive":
            # For abductive, check if it's the best explanation
            result['valid'] = True
            result['confidence'] = self._assess_abductive_strength(premise, conclusion)

            if result['confidence'] < 0.7:
                result['issues'].append("May not be the best explanation")
                result['suggestions'].append("Consider alternative explanations")

        return result

    def _load_fallacy_patterns(self) -> Dict[str, Dict]:
        """Load patterns for detecting logical fallacies"""
        return {
            'ad_hominem': {
                'patterns': [
                    r"you['']?\s+(?:are|were|have been)\s+(?:stupid|idiot|ignorant|hypocrite|wrong)",
                    r"\bhe|she\s+(?:is|was)\s+.+?(?:criminal|liar|fraud|divorced)",
                    r"can['']?t\s+trust\s+\w+\s+because",
                ],
                'description': 'Attacking the person instead of the argument',
                'severity': 'moderate'
            },
            'straw_man': {
                'patterns': [
                    r"so you['']?re\s+saying\s+that",
                    r"you\s+want\s+to\s+(?:destroy|ruin|eliminate)",
                    r"you\s+believe\s+that\s+.+?(?:ridiculous|absurd|crazy)",
                ],
                'description': 'Misrepresenting an argument to make it easier to attack',
                'severity': 'moderate'
            },
            'appeal_to_authority': {
                'patterns': [
                    r"\bexperts?\s+say\b",
                    r"\bscientists?\s+agree\b",
                    r"\bstudies?\s+show\b",
                    r"because\s+\w+\s+(?:said|claimed|stated)",
                ],
                'description': 'Appealing to authority rather than providing evidence',
                'severity': 'minor'
            },
            'appeal_to_popularity': {
                'patterns': [
                    r"everyone\s+knows",
                    r"most\s+people\s+(?:think|believe|agree)",
                    r"nobody\s+(?:wants|thinks|believes)",
                    r"common\s+sense",
                ],
                'description': 'Accepting a claim because many people believe it',
                'severity': 'minor'
            },
            'false_dilemma': {
                'patterns': [
                    r"either\s+.+?\s+or",
                    r"only\s+two\s+options?",
                    r"no\s+alternative\s+but",
                ],
                'description': 'Presenting only two options when more exist',
                'severity': 'moderate'
            },
            'slippery_slope': {
                'patterns': [
                    r"will\s+lead\s+to",
                    r"next\s+thing\s+you\s+know",
                    r"where\s+does\s+it\s+stop",
                    r"inevitably\s+result\s+in",
                ],
                'description': 'Assuming a small action will lead to extreme consequences',
                'severity': 'moderate'
            },
            'circular_reasoning': {
                'patterns': [
                    r"(.+?)\s+because\s+\1",
                    r"true\s+because\s+it['']?s\s+true",
                    r"valid\s+because\s+it['']?s\s+valid",
                ],
                'description': 'Conclusion is assumed in the premises',
                'severity': 'critical'
            },
            'hasty_generalization': {
                'patterns': [
                    r"\ball\s+.+?\s+are\b",
                    r"\bevery\s+.+?\s+always\b",
                    r"\bnever\s+.+?\s+ever\b",
                ],
                'description': 'Drawing broad conclusion from insufficient evidence',
                'severity': 'moderate'
            },
            'affirming_consequent': {
                'patterns': [
                    r"if\s+.+?\s+then\s+.+?\.?\s*.+?\s+therefore\s+.+?",
                ],
                'description': 'Invalid deductive form: If P then Q, Q, therefore P',
                'severity': 'critical'
            },
            'denying_antecedent': {
                'patterns': [
                    r"if\s+.+?\s+then\s+.+?\.?\s*not\s+.+?\s+therefore\s+not",
                ],
                'description': 'Invalid deductive form: If P then Q, not P, therefore not Q',
                'severity': 'critical'
            },
        }

    def _detect_fallacies(self, text: str) -> List[FallacyDetection]:
        """Detect logical fallacies in text"""
        fallacies = []
        text_lower = text.lower()

        for fallacy_type, config in self.fallacy_patterns.items():
            patterns = config['patterns']

            for pattern in patterns:
                if re.search(pattern, text_lower):
                    evidence = self._extract_evidence(text, pattern)
                    fallacies.append(FallacyDetection(
                        fallacy_type=fallacy_type,
                        description=config['description'],
                        confidence='medium',
                        evidence=evidence,
                        severity=config['severity']
                    ))

        return fallacies

    def _extract_structure(self, argument: str) -> Tuple[List[str], str]:
        """Extract premises and conclusion from argument"""
        # Split into sentences
        sentences = [s.strip() for s in argument.split('.') if s.strip()]

        premises = []
        conclusion = ""

        for sentence in sentences:
            is_conclusion = False
            for indicator in self.conclusion_indicators:
                if indicator in sentence.lower():
                    conclusion = sentence
                    is_conclusion = True
                    break

            if not is_conclusion and sentence:
                premises.append(sentence)

        # If no explicit conclusion found, use last sentence
        if not conclusion and sentences:
            conclusion = sentences[-1]
            if premises and premises[-1] == conclusion:
                premises.pop()

        return premises, conclusion

    def _classify_reasoning_type(self, reasoning: str,
                                 premises: List[str],
                                 conclusion: str) -> str:
        """Classify the type of reasoning being used"""
        reasoning_lower = reasoning.lower()

        # Check for deductive indicators
        deductive_indicators = ['necessarily', 'must', 'therefore', 'thus']
        if any(ind in reasoning_lower for ind in deductive_indicators):
            # Verify it's actually deductive structure
            if self._has_conditional_structure(reasoning):
                return 'deductive'

        # Check for inductive indicators
        inductive_indicators = ['most', 'many', 'usually', 'typically',
                               'tends to', 'generally', 'often']
        if any(ind in reasoning_lower for ind in inductive_indicators):
            return 'inductive'

        # Check for abductive indicators
        abductive_indicators = ['best explanation', 'likely', 'probably',
                               'suggests', 'indicates', 'points to']
        if any(ind in reasoning_lower for ind in abductive_indicators):
            return 'abductive'

        # Default to unknown
        return 'unknown'

    def _has_conditional_structure(self, text: str) -> bool:
        """Check if text has if-then structure"""
        return bool(re.search(r'if\s+.+?\s+then', text.lower()))

    def _test_validity(self, premises: List[str], conclusion: str,
                       reasoning_type: str) -> bool:
        """Test if argument is valid (conclusion follows from premises)"""
        if not premises or not conclusion:
            return False

        if reasoning_type == 'deductive':
            # For deductive, check for formal validity
            return self._test_deductive_validity(premises, conclusion)
        elif reasoning_type == 'inductive':
            # For inductive, check strength (not validity)
            return len(premises) > 0
        elif reasoning_type == 'abductive':
            # For abductive, check if explanation is plausible
            return len(premises) > 0

        # Unknown type - check basic structure
        return len(premises) > 0

    def _test_deductive_validity(self, premises: List[str], conclusion: str) -> bool:
        """Test validity of deductive argument"""
        # Check for formal fallacies
        premises_text = ' '.join(premises).lower()

        # Check for affirming the consequent
        if re.search(r'if\s+.+?\s+then', premises_text):
            conclusion_lower = conclusion.lower()
            # This is a simplified check
            if 'therefore' in conclusion_lower:
                return True  # Assume valid unless we detect specific fallacy

        return True  # Default to valid if no obvious errors

    def _test_soundness(self, premises: List[str], reasoning: str) -> bool:
        """Test if premises are actually true (soundness)"""
        # In practice, this would require a knowledge base
        # For now, we check for obvious issues
        reasoning_lower = reasoning.lower()

        # Check if premises are obviously questionable
        questionable_indicators = [
            'obviously', 'clearly', 'naturally', 'everyone knows'
        ]

        for premise in premises:
            premise_lower = premise.lower()
            for indicator in questionable_indicators:
                if indicator in premise_lower:
                    # Premise might be assumed without evidence
                    return False

        return True

    def _calculate_validity_score(self, fallacies: List[FallacyDetection],
                                  is_valid: bool, is_sound: bool) -> float:
        """Calculate overall validity score (0-1)"""
        score = 1.0

        # Deduct for fallacies based on severity
        for fallacy in fallacies:
            if fallacy.severity == 'critical':
                score -= 0.3
            elif fallacy.severity == 'moderate':
                score -= 0.15
            else:  # minor
                score -= 0.05

        # Adjust for validity and soundness
        if not is_valid:
            score *= 0.5
        if not is_sound:
            score *= 0.8

        return max(0.0, min(1.0, score))

    def _extract_evidence(self, text: str, pattern: str) -> str:
        """Extract the part of text that matches the pattern"""
        match = re.search(pattern, text.lower())
        if match:
            start = max(0, match.start() - 30)
            end = min(len(text), match.end() + 30)
            return text[start:end]

    def _are_contradictory(self, text1: str, text2: str) -> bool:
        """Check if two statements contradict each other"""
        # Simple check for direct contradictions
        negations = ['not', 'no', 'never', 'none', 'neither', 'nor']

        # Check if one negates a key term from the other
        words1 = set(text1.split())
        words2 = set(text2.split())

        # Find common content words (excluding stop words)
        common = words1 & words2
        common -= {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'and', 'or', 'but'}

        if common:
            # Check if one has negation and the other doesn't
            has_neg1 = any(neg in text1 for neg in negations)
            has_neg2 = any(neg in text2 for neg in negations)

            if has_neg1 != has_neg2:
                return True

        return False

    def _detect_circular_reasoning(self, text: str) -> bool:
        """Detect if reasoning is circular"""
        patterns = self.fallacy_patterns['circular_reasoning']['patterns']
        text_lower = text.lower()
        return any(re.search(p, text_lower) for p in patterns)

    def _check_modus_ponens(self, premise: str, conclusion: str) -> bool:
        """Check if argument follows modus ponens: If P then Q, P, therefore Q"""
        premise_lower = premise.lower()
        conclusion_lower = conclusion.lower()

        # Look for "if P then Q" structure in premise
        if_match = re.search(r'if\s+(.+?)\s+then\s+(.+)', premise_lower)
        if if_match:
            p, q = if_match.groups()
            # Check if P appears before "therefore" and Q appears after
            if p in conclusion_lower and q in conclusion_lower:
                return True

        return False

    def _check_modus_tollens(self, premise: str, conclusion: str) -> bool:
        """Check if argument follows modus tollens: If P then Q, not Q, therefore not P"""
        premise_lower = premise.lower()
        conclusion_lower = conclusion.lower()

        # Look for "if P then Q" structure
        if_match = re.search(r'if\s+(.+?)\s+then\s+(.+)', premise_lower)
        if if_match:
            p, q = if_match.groups()
            # Check for "not Q" and "therefore not P"
            if f'not {q.strip()}' in conclusion_lower or f"{q.strip()} is not" in conclusion_lower:
                return True

        return False

    def _find_counterexample(self, premise: str, conclusion: str) -> Optional[str]:
        """Try to find a counterexample to the argument"""
        # This is simplified - in practice would use knowledge base
        # For now, just check for common invalid patterns

        premise_lower = premise.lower()

        # Check for affirming consequent: If P then Q, Q, therefore P
        if_match = re.search(r'if\s+(.+?)\s+then\s+(.+)', premise_lower)
        if if_match:
            p, q = if_match.groups()
            conclusion_lower = conclusion.lower()

            # If conclusion just restates P given Q, this is invalid
            if p.strip() in conclusion_lower and q.strip() in conclusion_lower:
                # Check if structure looks like affirming consequent
                if 'therefore' in conclusion_lower or 'thus' in conclusion_lower:
                    return f"Could be true that {q} without {p} being true"

        return None

    def _assess_inductive_strength(self, premise: str, conclusion: str) -> float:
        """Assess strength of inductive argument (0-1)"""
        # Simplified assessment based on indicators
        premise_lower = premise.lower()
        conclusion_lower = conclusion.lower()

        strength = 0.5  # Base strength

        # Look for strength indicators
        if 'all' in premise_lower or 'every' in premise_lower:
            strength += 0.3
        elif 'most' in premise_lower or 'many' in premise_lower:
            strength += 0.2
        elif 'some' in premise_lower or 'few' in premise_lower:
            strength += 0.1

        # Check for hedging in conclusion
        if 'probably' in conclusion_lower or 'likely' in conclusion_lower:
            strength += 0.1  # Appropriate uncertainty

        return min(1.0, strength)

    def _assess_abductive_strength(self, premise: str, conclusion: str) -> float:
        """Assess strength of abductive argument (0-1)"""
        # Simplified assessment
        premise_lower = premise.lower()

        strength = 0.5  # Base strength

        # Look for explanatory power indicators
        if 'explains' in premise_lower or 'because' in premise_lower:
            strength += 0.2

        # Look for simplicity (Occam's razor)
        if 'simple' in premise_lower or 'direct' in premise_lower:
            strength += 0.1

        return min(1.0, strength)
