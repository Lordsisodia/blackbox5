#!/usr/bin/env python3
"""
Task Summarizer Utility

Provides summarization capabilities for subagent tasks.
Currently uses heuristic-based summarization, but can be extended
to use a local LLM (Ollama) for better quality.

Usage:
    from hooks.utils.task_summarizer import summarize_subagent_task

    summary = summarize_subagent_task("Explore codebase", "Executor-123")
"""

import json
import os
import sys
from pathlib import Path

# Add hooks directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def extract_task_context(input_data: dict) -> str:
    """
    Extract task context from the subagent input data.

    Looks for the agent transcript path and reads the initial task/prompt
    from the JSONL transcript file.

    Args:
        input_data: The input data dictionary

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


def summarize_heuristic(task_context: str, agent_name: str = "unknown") -> str:
    """
    Heuristic-based task summarization.

    Simple approach that extracts the first few words of the task description.

    Args:
        task_context: The task description
        agent_name: The agent name

    Returns:
        A summary message
    """
    if not task_context or task_context == "completed a task":
        return f"Agent {agent_name} completed task"

    # Simple heuristic: take first sentence and truncate
    if "." in task_context:
        summary = task_context.split(".")[0] + "."
    elif "," in task_context:
        summary = task_context.split(",")[0] + ","
    else:
        summary = task_context[:100] + "..." if len(task_context) > 100 else task_context

    return f"Agent {agent_name}: {summary}"


def summarize_subagent_task(task_description: str = None, agent_name: str = None) -> str:
    """
    Summarize a subagent task.

    This is the main entry point for task summarization. It can work with
    either a task description string or full input data dictionary.

    Args:
        task_description: Optional task description string
        agent_name: Optional agent name

    Returns:
        A summary message
    """
    if task_description is None:
        return "Task completed"

    # Use heuristic summarization (extendable to LLM later)
    return summarize_heuristic(task_description, agent_name or "unknown")


# For backward compatibility with research repo imports
if __name__ == "__main__":
    # Test the summarizer
    test_cases = [
        "Analyze the codebase structure for the BB5 project",
        "Create a new task plan with 5 steps",
        "Fix the bug in the task tracker",
    ]

    for task in test_cases:
        print(f"Task: {task}")
        print(f"Summary: {summarize_subagent_task(task)}")
        print("-" * 50)
