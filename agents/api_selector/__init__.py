"""
API Selector Agent for BlackBox5
Automatically selects the optimal API provider based on task requirements.
"""

from .api_selector import APISelector, TaskType, ProviderConfig

__all__ = ['APISelector', 'TaskType', 'ProviderConfig']
__version__ = '1.0.0'
