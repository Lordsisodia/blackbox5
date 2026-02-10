"""
Security Patterns Utility for BlackBox5

Shared security pattern detection functions for use across multiple hooks.
"""

import re


# Dangerous rm command patterns (comprehensive detection)
DANGEROUS_RM_PATTERNS = [
    r'\brm\s+.*-[a-z]*r[a-z]*f',  # rm -rf, rm -fr, rm -Rf
    r'\brm\s+.*-[a-z]*f[a-z]*r',  # rm -fr variations
    r'\brm\s+--recursive\s+--force',  # rm --recursive --force
    r'\brm\s+--force\s+--recursive',  # rm --force --recursive
    r'\brm\s+-r\s+.*-f',  # rm -r ... -f
    r'\brm\s+-f\s+.*-r',  # rm -f ... -r
]

# Dangerous paths that should block rm -rf
DANGEROUS_RM_PATHS = [
    r'/',           # Root directory
    r'/\*',         # Root with wildcard
    r'~',           # Home directory
    r'~/',          # Home directory path
    r'\$HOME',      # Home environment variable
    r'\.\.',        # Parent directory references
    r'\*',          # Wildcards in general rm -rf context
    r'\.',          # Current directory
    r'\.\s*$',      # Current directory at end of command
]

# .env file access patterns (block .env, allow .env.sample)
ENV_ACCESS_PATTERNS = [
    r'\b\.env\b(?!\.sample)',  # .env but not .env.sample
    r'cat\s+.*\.env\b(?!\.sample)',  # cat .env
    r'echo\s+.*>\s*\.env\b(?!\.sample)',  # echo > .env
    r'touch\s+.*\.env\b(?!\.sample)',  # touch .env
    r'cp\s+.*\.env\b(?!\.sample)',  # cp .env
    r'mv\s+.*\.env\b(?!\.sample)',  # mv .env
]


def is_dangerous_rm_command(command):
    """
    Check if a command contains dangerous rm patterns.

    Args:
        command: String containing the bash command to check

    Returns:
        True if command contains dangerous rm patterns, False otherwise
    """
    # Normalize command
    normalized = ' '.join(command.lower().split())

    # Check against all dangerous patterns
    for pattern in DANGEROUS_RM_PATTERNS:
        if re.search(pattern, normalized):
            return True

    # If rm has recursive flag, also check for dangerous paths
    if re.search(r'\brm\s+.*-[a-z]*r', normalized):
        for path in DANGEROUS_RM_PATHS:
            if re.search(path, normalized):
                return True

    return False


def is_env_file_access(command):
    """
    Check if a command attempts to access .env files (excluding .env.sample).

    Args:
        command: String containing the bash command to check

    Returns:
        True if command accesses .env files, False otherwise
    """
    for pattern in ENV_ACCESS_PATTERNS:
        if re.search(pattern, command):
            return True
    return False


def normalize_command(command):
    """
    Normalize a command by removing extra spaces and converting to lowercase.

    Args:
        command: Original command string

    Returns:
        Normalized command string
    """
    return ' '.join(command.lower().split())
