"""
YouTube Channel Scoring Package

Provides tools for calculating educational value scores for YouTube channels.
"""

from .engine import ChannelScorer, score_all_channels
from .weights import get_weights, get_tier, DEFAULT_WEIGHTS

__all__ = [
    'ChannelScorer',
    'score_all_channels',
    'get_weights',
    'get_tier',
    'DEFAULT_WEIGHTS',
]
