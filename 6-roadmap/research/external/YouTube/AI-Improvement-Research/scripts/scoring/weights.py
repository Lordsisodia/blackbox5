"""
Scoring Weights Configuration for YouTube Channel Ranking System.

These weights determine how much each dimension contributes to the overall score.
All weights should sum to 1.0 (100%).
"""

# Default scoring weights
DEFAULT_WEIGHTS = {
    'knowledge': 0.25,      # Knowledge density and educational value
    'engagement': 0.20,     # Audience engagement quality
    'consistency': 0.20,    # Upload regularity and sustained quality
    'quality': 0.15,        # Production quality (audio/video)
    'impact': 0.15,         # Long-term value and influence
    'novelty': 0.05,        # Content uniqueness and originality
}

# Tier thresholds
TIER_THRESHOLDS = {
    'S': (90, 100),         # Exceptional
    'A': (80, 89),          # Excellent
    'B': (70, 79),          # Good
    'C': (60, 69),          # Average
    'D': (0, 59),           # Below Average
}

# Scoring bounds for normalization
SCORE_BOUNDS = {
    'knowledge': {'min': 0, 'max': 100},
    'engagement': {'min': 0, 'max': 100},
    'consistency': {'min': 0, 'max': 100},
    'quality': {'min': 0, 'max': 100},
    'impact': {'min': 0, 'max': 100},
    'novelty': {'min': 0, 'max': 100},
}

# Default scores for missing data (conservative estimates)
DEFAULT_SCORES = {
    'knowledge': 50,
    'engagement': 50,
    'consistency': 50,
    'quality': 50,
    'impact': 50,
    'novelty': 50,
}


def get_weights():
    """Get current scoring weights."""
    return DEFAULT_WEIGHTS.copy()


def get_tier(score):
    """
    Determine tier based on overall score.

    Args:
        score: Overall composite score (0-100)

    Returns:
        str: Tier letter (S, A, B, C, D)
    """
    for tier, (min_score, max_score) in TIER_THRESHOLDS.items():
        if min_score <= score <= max_score:
            return tier
    return 'D'  # Default to lowest tier if out of bounds


def validate_weights(weights):
    """
    Validate that weights sum to 1.0.

    Args:
        weights: Dictionary of dimension weights

    Returns:
        bool: True if valid

    Raises:
        ValueError: If weights don't sum to 1.0
    """
    total = sum(weights.values())
    if abs(total - 1.0) > 0.001:  # Allow small floating point error
        raise ValueError(f"Weights must sum to 1.0, got {total}")
    return True
