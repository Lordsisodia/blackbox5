#!/usr/bin/env python3
"""
pre-tool-security.py - Smart security hook for BB5
Blocks dangerous commands while allowing legitimate agent operations
"""

import json
import sys
import re
from pathlib import Path

def detect_agent_type():
    """Detect which agent is running based on context."""
    import os

    cwd = os.getcwd()
    run_dir = os.environ.get('RALF_RUN_DIR', cwd)

    # Check path patterns
    if '/planner/' in run_dir or '/planner/' in cwd:
        return 'planner'
    elif '/executor/' in run_dir or '/executor/' in cwd:
        return 'executor'
    elif '/architect/' in run_dir or '/architect/' in cwd:
        return 'architect'

    # Check for agent-specific files
    if Path('queue.yaml').exists() or Path('loop-metadata-template.yaml').exists():
        return 'planner'
    elif any(Path('.').glob('task-*-spec.md')):
        return 'executor'

    return 'unknown'

def is_dangerous_command(tool_name, tool_input, agent_type):
    """Check if tool use is dangerous based on agent context."""

    # Only check Bash commands
    if tool_name != 'Bash':
        return False, None

    command = tool_input.get('command', '')

    # Pattern 1: Dangerous rm -rf (block for all agents)
    dangerous_rm_patterns = [
        r'\brm\s+.*-[a-z]*r[a-z]*f',  # rm -rf, rm -fr
        r'\brm\s+--recursive\s+--force',
        r'\brm\s+-r\s+.*-f',
        r'\brm\s+-f\s+.*-r',
    ]

    dangerous_paths = [r'/', r'/\*', r'~', r'\$HOME', r'\*', r'\.']

    for pattern in dangerous_rm_patterns:
        if re.search(pattern, command):
            # Check if targeting dangerous paths
            for path in dangerous_paths:
                if re.search(rf'\s+{path}(\s|$)', command):
                    return True, f"Blocked dangerous rm command targeting {path}"

    # Pattern 2: .env file access (allow for all agents - removed restriction)
    # Note: Original blocked non-executor agents, but this was too restrictive
    # Users need .env access for legitimate configuration tasks
    pass  # .env access now allowed for all agents

    # Pattern 3: git push --force (block for planner/executor, allow architect)
    if re.search(r'git\s+push\s+.*--force', command):
        if agent_type in ['planner', 'executor']:
            return True, "Blocked force push (use architect agent for destructive git ops)"

    # Pattern 4: Direct database modifications without architect
    if re.search(r'(psql|mysql|mongo).*\b(DROP|DELETE|TRUNCATE)\b', command, re.IGNORECASE):
        if agent_type != 'architect':
            return True, "Blocked destructive DB operation (requires architect agent)"

    return False, None

def log_security_event(tool_name, tool_input, blocked, reason, agent_type):
    """Log security check to JSON file."""
    import os
    from datetime import datetime

    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'agent_type': agent_type,
        'tool_name': tool_name,
        'command': tool_input.get('command', ''),
        'blocked': blocked,
        'reason': reason
    }

    # Determine log path based on agent type
    base_dir = Path(os.environ.get('RALF_RUN_DIR', os.getcwd()))
    log_dir = base_dir / '.logs'
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / 'security_checks.json'

    # Read existing or create new
    if log_file.exists():
        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)
        except:
            logs = []
    else:
        logs = []

    logs.append(log_entry)

    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)

def main():
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())

        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})

        # Detect agent type
        agent_type = detect_agent_type()

        # Check if dangerous
        is_blocked, reason = is_dangerous_command(tool_name, tool_input, agent_type)

        # Log the check
        log_security_event(tool_name, tool_input, is_blocked, reason, agent_type)

        if is_blocked:
            print(f"SECURITY BLOCK: {reason}", file=sys.stderr)
            print(f"Agent: {agent_type}", file=sys.stderr)
            print("If this is intentional, use architect agent or modify hook.", file=sys.stderr)
            sys.exit(2)  # Block the tool

        # Allow the tool
        sys.exit(0)

    except json.JSONDecodeError:
        # Invalid JSON, allow anyway
        sys.exit(0)
    except Exception as e:
        # Hook error, log but don't block
        print(f"Security hook error: {e}", file=sys.stderr)
        sys.exit(0)

if __name__ == '__main__':
    main()
