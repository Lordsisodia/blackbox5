#!/usr/bin/env python3
"""
Enhanced SessionStart hook for BB5.

Provides:
- Git status (branch, uncommitted changes)
- Context file loading (.claude/CONTEXT.md, .claude/TODO.md, TODO.md)
- JSON logging to logs/session_start.json
- Returns additionalContext to Claude
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def log_session_start(input_data):
    """Log session start event to logs directory."""
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / 'session_start.json'

    # Read existing log data or initialize empty list
    if log_file.exists():
        with open(log_file, 'r') as f:
            try:
                log_data = json.load(f)
            except (json.JSONDecodeError, ValueError):
                log_data = []
    else:
        log_data = []

    # Append the entire input data with timestamp
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "data": input_data
    }
    log_data.append(log_entry)

    # Write back to file
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=2)


def get_git_status():
    """Get current git status information."""
    try:
        # Get current branch
        branch_result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True,
            text=True,
            timeout=5
        )
        current_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "unknown"

        # Get uncommitted changes count
        status_result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if status_result.returncode == 0:
            changes = status_result.stdout.strip().split('\n') if status_result.stdout.strip() else []
            uncommitted_count = len(changes)
        else:
            uncommitted_count = 0

        return current_branch, uncommitted_count
    except Exception:
        return None, None


def load_context_files():
    """Load relevant context files from the project."""
    context_parts = []

    # Context files to load in priority order
    context_files = [
        ".claude/CONTEXT.md",
        ".claude/TODO.md",
        "TODO.md"
    ]

    for file_path in context_files:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r') as f:
                    content = f.read().strip()
                    if content:
                        context_parts.append(f"\n--- Content from {file_path} ---")
                        context_parts.append(content[:1000])  # Limit to 1000 chars
            except Exception:
                pass

    return "\n".join(context_parts)


def main():
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--load-context', action='store_true',
                          help='Load development context at session start')
        args = parser.parse_args()

        # Read JSON input from stdin
        input_data = json.loads(sys.stdin.read())

        # Extract fields
        session_id = input_data.get('session_id', 'unknown')
        source = input_data.get('source', 'unknown')  # "startup", "resume", or "clear"

        # Log the session start event
        log_session_start(input_data)

        # If load-context is requested, build additional context
        if args.load_context:
            context_parts = []

            # Add timestamp and session info
            context_parts.append(f"Session started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            context_parts.append(f"Session source: {source}")
            context_parts.append(f"Session ID: {session_id}")

            # Add git information
            branch, changes = get_git_status()
            if branch:
                context_parts.append(f"Git branch: {branch}")
                if changes > 0:
                    context_parts.append(f"Uncommitted changes: {changes} files")

            # Load context files
            context_parts.append(load_context_files())

            context = "\n".join(context_parts)

            # Return additional context to Claude via JSON output
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": context
                }
            }
            print(json.dumps(output))
            sys.exit(0)

        # Success
        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:
        # Handle errors gracefully, exit with success code
        sys.exit(0)


if __name__ == '__main__':
    main()
