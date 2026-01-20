"""
Bayesian Confidence Updater for Thought Loop Framework
======================================================

Updates confidence using Bayes' theorem to properly weigh evidence.
Addresses the "breaking down logic" requirement by making belief updates explicit.
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import math

try:
    from .models import Evidence, Assumption, AssumptionType, AssumptionValidation, Validity
except ImportError:
    from models import Evidence, Assumption, AssumptionType, AssumptionValidation, Validity


@dataclass
class BayesianUpdate:
    """A single Bayesian belief update"""
    prior: float  # Prior probability P(H)
    likelihood: float  # P(E|H)
    marginal_likelihood: float  # P(E)
    posterior: float  # P(H|E)
    evidence_strength: float  # How strong the evidence is
    confidence_interval: Tuple[float, float]  # Uncertainty bounds


@dataclass
class BeliefState:
    """Current belief state with uncertainty quantification"""
    mean: float  # Mean belief (probability)
    variance: float  # Variance (uncertainty)
    samples: int  # Number of evidence samples
    update_history: List[BayesianUpdate]


class BayesianUpdater:
    """
    Updates beliefs systematically using Bayesian reasoning.

    Addresses the "breaking down logic" requirement by:
    1. Making confidence updates explicit and mathematical
    2. Properly weighing supporting vs contradicting evidence
    3. Quantifying uncertainty in beliefs
    4. Avoiding overconfidence through proper Bayesian updating
    5. Tracking the full belief update history
    """

    def __init__(self, min_confidence: float = 0.01, max_confidence: float = 0.99):
        """
        Initialize Bayesian updater.

        Args:
            min_confidence: Minimum confidence floor (avoid 0 for updateability)
            max_confidence: Maximum confidence ceiling (avoid 1 for updateability)
        """
        self.min_confidence = min_confidence
        self.max_confidence = max_confidence

    def update_with_evidence(self, prior: float, evidence: List[Evidence],
                             hypothesis: str) -> BayesianUpdate:
        """
        Update belief using Bayes' theorem with multiple evidence pieces.

        Args:
            prior: Prior probability P(H)
            evidence: List of evidence items
            hypothesis: The hypothesis being tested

        Returns:
            BayesianUpdate with all values and confidence interval
        """
        # Calculate likelihood P(E|H) - probability of evidence if hypothesis is true
        likelihood = self._calculate_likelihood(evidence)

        # Calculate marginal likelihood P(E) - total probability of evidence
        marginal_likelihood = self._calculate_marginal_likelihood(evidence, prior, likelihood)

        # Calculate posterior using Bayes' theorem
        # P(H|E) = [P(E|H) × P(H)] / P(E)
        posterior_raw = (likelihood * prior) / marginal_likelihood if marginal_likelihood > 0 else prior

        # Clamp to reasonable bounds
        posterior = max(self.min_confidence, min(self.max_confidence, posterior_raw))

        # Calculate evidence strength
        evidence_strength = self._calculate_evidence_strength(evidence, likelihood, marginal_likelihood)

        # Calculate confidence interval (uncertainty quantification)
        confidence_interval = self._calculate_confidence_interval(
            posterior, evidence_strength, len(evidence)
        )

        return BayesianUpdate(
            prior=prior,
            likelihood=likelihood,
            marginal_likelihood=marginal_likelihood,
            posterior=posterior,
            evidence_strength=evidence_strength,
            confidence_interval=confidence_interval
        )

    def update_from_validation(self, prior: float,
                                validation: AssumptionValidation) -> BayesianUpdate:
        """
        Update belief from an AssumptionValidation result.

        Args:
            prior: Prior probability
            validation: Assumption validation result

        Returns:
            BayesianUpdate with updated belief
        """
        # Convert validation to evidence representation
        evidence = self._validation_to_evidence(validation)

        return self.update_with_evidence(prior, evidence, validation.assumption)

    def sequential_update(self, initial_prior: float,
                          evidence_list: List[List[Evidence]]) -> BeliefState:
        """
        Perform sequential Bayesian updates as evidence comes in.

        Args:
            initial_prior: Starting prior probability
            evidence_list: List of evidence batches, processed sequentially

        Returns:
            BeliefState with final belief and full history
        """
        current_prior = initial_prior
        history = []
        variance = 0.25  # Start with high uncertainty (max variance for 0-1 range)

        for evidence_batch in evidence_list:
            update = self.update_with_evidence(current_prior, evidence_batch, "hypothesis")
            history.append(update)

            # Update prior to posterior for next iteration
            current_prior = update.posterior

            # Reduce uncertainty as we gather evidence
            # Variance decreases with more samples
            variance = self._update_variance(variance, len(evidence_batch))

        return BeliefState(
            mean=current_prior,
            variance=variance,
            samples=sum(len(batch) for batch in evidence_list),
            update_history=history
        )

    def detect_overconfidence(self, belief: float, evidence_count: int,
                               confidence_interval: Tuple[float, float]) -> Dict[str, any]:
        """
        Detect if belief is overconfident given limited evidence.

        Args:
            belief: Current belief (probability)
            evidence_count: Number of evidence samples
            confidence_interval: Current confidence interval

        Returns:
            Dict with overconfidence assessment
        """
        assessment = {
            'is_overconfident': False,
            'reason': '',
            'suggested_adjustment': 0.0
        }

        # Calculate expected uncertainty given evidence count
        expected_uncertainty = self._expected_uncertainty(evidence_count)

        # Actual uncertainty from confidence interval
        actual_uncertainty = confidence_interval[1] - confidence_interval[0]

        # Check if actual uncertainty is too small given evidence
        if actual_uncertainty < expected_uncertainty * 0.5:
            assessment['is_overconfident'] = True
            assessment['reason'] = (
                f"Confidence interval ({actual_uncertainty:.3f}) is too narrow "
                f"for {evidence_count} evidence samples (expected ~{expected_uncertainty:.3f})"
            )

            # Suggest adjustment - widen the interval
            adjustment_factor = expected_uncertainty / actual_uncertainty
            assessment['suggested_adjustment'] = adjustment_factor

        # Check for extreme beliefs with insufficient evidence
        if evidence_count < 5:
            if belief > 0.9:
                assessment['is_overconfident'] = True
                assessment['reason'] = (
                    f"Very high confidence ({belief:.2f}) with only {evidence_count} "
                    "evidence samples is likely overconfident"
                )
                assessment['suggested_adjustment'] = 0.7  # Regress toward 0.5

            elif belief < 0.1:
                assessment['is_overconfident'] = True
                assessment['reason'] = (
                    f"Very low confidence ({belief:.2f}) with only {evidence_count} "
                    "evidence samples is likely overconfident"
                )
                assessment['suggested_adjustment'] = 0.7  # Regress toward 0.5

        return assessment

    def compare_priors(self, prior1: float, prior2: float,
                       evidence: List[Evidence]) -> Dict[str, BayesianUpdate]:
        """
        Compare how different priors affect posterior beliefs.

        Args:
            prior1: First prior probability
            prior2: Second prior probability
            evidence: Evidence to update both priors

        Returns:
            Dict mapping prior names to BayesianUpdate results
        """
        update1 = self.update_with_evidence(prior1, evidence, "hypothesis1")
        update2 = self.update_with_evidence(prior2, evidence, "hypothesis2")

        return {
            'prior1': update1,
            'prior2': update2,
            'convergence': abs(update1.posterior - update2.posterior),
            'converged': abs(update1.posterior - update2.posterior) < 0.1
        }

    def _calculate_likelihood(self, evidence: List[Evidence]) -> float:
        """
        Calculate P(E|H) - probability of evidence if hypothesis is true.

        Higher if evidence supports, lower if evidence contradicts.
        """
        if not evidence:
            return 0.5  # Neutral likelihood with no evidence

        supporting_count = len([e for e in evidence if e.supports])
        contradicting_count = len([e for e in evidence if not e.supports])
        total_count = len(evidence)

        # Base likelihood from supporting vs contradicting ratio
        if contradicting_count == 0:
            # All supporting - high likelihood
            return 0.95
        elif supporting_count == 0:
            # All contradicting - low likelihood
            return 0.05
        else:
            # Mixed evidence - calculate ratio
            support_ratio = supporting_count / total_count
            # Map to [0.05, 0.95] range
            return 0.05 + (support_ratio * 0.90)

    def _calculate_marginal_likelihood(self, evidence: List[Evidence],
                                        prior: float, likelihood: float) -> float:
        """
        Calculate P(E) - total probability of evidence.

        P(E) = P(E|H) × P(H) + P(E|¬H) × P(¬H)
        """
        # P(¬H) = 1 - P(H)
        prior_complement = 1.0 - prior

        # For P(E|¬H), we invert the likelihood
        # If evidence is likely given H, it's unlikely given not H
        likelihood_complement = 1.0 - likelihood

        # Calculate marginal
        marginal = (likelihood * prior) + (likelihood_complement * prior_complement)

        # Avoid division by zero
        return max(marginal, 0.01)

    def _calculate_evidence_strength(self, evidence: List[Evidence],
                                     likelihood: float,
                                     marginal_likelihood: float) -> float:
        """
        Calculate how strong the evidence is.

        Strong evidence moves belief significantly, weak evidence has little effect.
        """
        if not evidence:
            return 0.0

        # Evidence strength is related to how much likelihood differs from marginal
        # When P(E|H) is very different from P(E), evidence is strong
        strength = abs(likelihood - marginal_likelihood)

        # Normalize to [0, 1]
        return min(1.0, strength * 2)

    def _calculate_confidence_interval(self, posterior: float,
                                         evidence_strength: float,
                                         evidence_count: int) -> Tuple[float, float]:
        """
        Calculate confidence interval around posterior belief.

        More evidence and stronger evidence = narrower interval.
        """
        # Base uncertainty decreases with more evidence
        base_uncertainty = 1.0 / (1.0 + evidence_count * 0.5)

        # Adjust by evidence strength
        uncertainty = base_uncertainty * (1.0 - evidence_strength * 0.5)

        # Ensure bounds are in [0, 1]
        lower = max(0.0, posterior - uncertainty)
        upper = min(1.0, posterior + uncertainty)

        return (lower, upper)

    def _update_variance(self, current_variance: float, new_samples: int) -> float:
        """
        Update variance as new evidence arrives.

        More samples = less variance (more certainty).
        """
        # Simple variance reduction formula
        reduction_factor = 1.0 / (1.0 + new_samples * 0.1)
        return current_variance * reduction_factor

    def _expected_uncertainty(self, evidence_count: int) -> float:
        """Calculate expected uncertainty range given evidence count."""
        if evidence_count == 0:
            return 1.0  # Maximum uncertainty
        # Uncertainty decreases with more evidence
        return 1.0 / (1.0 + math.sqrt(evidence_count) * 0.5)

    def _validation_to_evidence(self, validation: AssumptionValidation) -> List[Evidence]:
        """Convert AssumptionValidation to list of Evidence objects."""
        evidence_list = []

        # Add supporting evidence
        for supporting in validation.supporting_evidence:
            evidence_list.append(Evidence(
                text=supporting.get('text', supporting.get('content', '')),
                source=supporting.get('source', 'validation'),
                supports=True
            ))

        # Add contradicting evidence
        for contradicting in validation.contradicting_evidence:
            evidence_list.append(Evidence(
                text=contradicting.get('text', contradicting.get('content', '')),
                source=contradicting.get('source', 'validation'),
                supports=False
            ))

        # If no explicit evidence, create from validity assessment
        if not evidence_list:
            supports = validation.validity in [Validity.VALID, Validity.UNCERTAIN]
            evidence_list.append(Evidence(
                text=validation.reasoning,
                source='validation_assessment',
                supports=supports
            ))

        return evidence_list
