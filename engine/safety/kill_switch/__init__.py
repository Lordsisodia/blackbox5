# Package marker
from .kill_switch import (
    KillSwitch,
    KillSwitchState,
    KillSwitchReason,
    get_kill_switch,
    KillSwitchGuard,
    activate_emergency_shutdown,
)

__all__ = [
    "KillSwitch",
    "KillSwitchState",
    "KillSwitchReason",
    "get_kill_switch",
    "KillSwitchGuard",
    "activate_emergency_shutdown",
]
