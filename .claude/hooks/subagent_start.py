#!/usr/bin/env python3
"""
SubagentStart Hook - Track agent spawn events

Logs when Executor, Planner, or Architect subagents are spawned.
Writes to logs/subagent_start.json

Usage:
    subagent_start.py
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def main() -> None:
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Extract fields for logging
        agent_id = input_data.get("agent_id", "unknown")
        agent_type = input_data.get("agent_type", "unknown")

        # Add timestamp to input data for logging
        input_data["logged_at"] = datetime.now().isoformat()

        # Ensure log directory exists
        log_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "subagent_start.json")

        # Read existing log data or initialize empty list
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []

        # Append new data
        log_data.append(input_data)

        # Write back to file with formatting
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)

        sys.exit(0)

    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Handle any other errors gracefully
        sys.exit(0)


if __name__ == "__main__":
    main()
