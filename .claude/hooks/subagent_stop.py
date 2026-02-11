#!/usr/bin/env python3
"""
SubagentStop Hook - Track agent completion events

Logs when Executor, Planner, or Architect subagents complete.
Writes to logs/subagent_stop.json

Usage:
    subagent_stop.py
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def extract_task_context(input_data: dict) -> str:
    """
    Extract task context from the subagent input data.

    Looks for the agent transcript path and reads the initial task/prompt
    from the JSONL transcript file.

    Args:
        input_data: The input data dictionary from stdin

    Returns:
        A brief description of what the subagent was doing
    """
    # Try to get agent transcript path
    transcript_path = input_data.get("agent_transcript_path")
    if not transcript_path:
        # Fallback to regular transcript_path
        transcript_path = input_data.get("transcript_path")

    if not transcript_path or not os.path.exists(transcript_path):
        return "completed a task"

    try:
        # Read the JSONL transcript file
        with open(transcript_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)

                    # Look for user messages or initial prompts
                    entry_type = entry.get("type", "")

                    if entry_type == "user":
                        # The content is nested in message.content
                        message = entry.get("message", {})
                        content = message.get("content", "") if isinstance(message, dict) else ""

                        # Fallback to direct content field
                        if not content:
                            content = entry.get("content", "")

                        if isinstance(content, str) and content:
                            # Truncate if too long
                            if len(content) > 200:
                                return content[:200] + "..."
                            return content
                        elif isinstance(content, list):
                            # Handle content blocks
                            for block in content:
                                if isinstance(block, dict) and block.get("type") == "text":
                                    text = block.get("text", "")
                                    if text:
                                        if len(text) > 200:
                                            return text[:200] + "..."
                                        return text

                    # Also check for prompt field
                    prompt = entry.get("prompt", "")
                    if prompt:
                        if len(prompt) > 200:
                            return prompt[:200] + "..."
                        return prompt

                except json.JSONDecodeError:
                    continue

    except (OSError, IOError):
        pass

    return "completed a task"


def summarize_task(task_context: str, agent_id: str = "unknown") -> str:
    """
    Summarize task completion.

    For BB5, uses a simple heuristic that extracts the first few words
    of the task description. In production, this could be extended to use
    a local LLM (Ollama) for better summarization.

    Args:
        task_context: The task description
        agent_id: The agent ID

    Returns:
        A summary message
    """
    if not task_context or task_context == "completed a task":
        return f"Agent {agent_id} completed task"

    # Simple heuristic: take first sentence and truncate
    if "." in task_context:
        summary = task_context.split(".")[0] + "."
    elif "," in task_context:
        summary = task_context.split(",")[0] + ","
    else:
        summary = task_context[:100] + "..." if len(task_context) > 100 else task_context

    return f"Agent {agent_id}: {summary}"


def main() -> None:
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Extract fields for logging
        agent_id = input_data.get("agent_id", "unknown")
        agent_type = input_data.get("agent_type", "unknown")

        # Extract and summarize task context
        task_context = extract_task_context(input_data)
        summary = summarize_task(task_context, agent_id)

        # Add summary to input data
        input_data["summary"] = summary
        input_data["logged_at"] = datetime.now().isoformat()

        # Ensure log directory exists
        log_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "subagent_stop.json")

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
