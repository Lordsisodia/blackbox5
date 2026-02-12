"""
Kill Switch Module

Emergency shutdown capability for BlackBox 5 multi-agent system.
"""

from .kill_switch import (
    KillSwitch,
    KillSwitchState,
    KillSwitchReason,
    get_kill_switch,
    activate_emergency_shutdown,
    require_operational,
)

__all__ = [
    'KillSwitch',
    'KillSwitchState',
    'KillSwitchReason',
    'get_kill_switch',
    'activate_emergency_shutdown',
    'require_operational',
]
