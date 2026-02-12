"""
Constitutional Classifier Module

Input/output content filtering for BlackBox 5 safety system.
"""

from .constitutional_classifier import (
    ConstitutionalClassifier,
    CheckResult,
    ContentType,
    ViolationType,
    Severity,
    get_classifier,
    check_user_input,
    check_agent_output,
)

__all__ = [
    'ConstitutionalClassifier',
    'CheckResult',
    'ContentType',
    'ViolationType',
    'Severity',
    'get_classifier',
    'check_user_input',
    'check_agent_output',
]
