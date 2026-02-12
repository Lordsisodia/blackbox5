#!/usr/bin/env python3
"""
Agent Runner - Processes spawn queue and executes agents
Reads ~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/spawn-queue.yaml
and spawns the appropriate agents
"""

import yaml
import json
import os
import sys
from datetime import datetime
from pathlib import Path

BB5_DIR = Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"
SPAWN_QUEUE = BB5_DIR / ".autonomous" / "agents" / "communications" / "spawn-queue.yaml"
SIGNALS_DIR = BB5_DIR / ".autonomous" / "signals"
LOG_FILE = BB5_DIR / ".autonomous" / "logs" / "agent-runner.log"

def log(message):
    timestamp = datetime.now().isoformat()
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    with open(LOG_FILE, "a") as f:
        f.write(log_line + "\n")

def read_spawn_queue():
    """Read the spawn queue YAML file"""
    if not SPAWN_QUEUE.exists():
        return []

    try:
        with open(SPAWN_QUEUE, "r") as f:
            content = f.read()
        if not content.strip():
            return []
        return yaml.safe_load(content) or []
    except Exception as e:
        log(f"Error reading spawn queue: {e}")
        return []

def write_spawn_queue(entries):
    """Write updated spawn queue"""
    try:
        with open(SPAWN_QUEUE, "w") as f:
            yaml.dump(entries, f, default_flow_style=False)
    except Exception as e:
        log(f"Error writing spawn queue: {e}")

def spawn_scribe_agent(entry):
    """Spawn scribe agent to update documentation"""
    log("Spawning scribe agent...")

    # Get current run directory
    run_dir = BB5_DIR / ".autonomous" / "runs" / "current"
    if not run_dir.exists():
        log("No current run directory found")
        return False

    # Read chat logs
    chat_logs_dir = BB5_DIR / ".autonomous" / "memory" / "chat-logs"
    thoughts_file = run_dir / "THOUGHTS.md"

    # Simple implementation: append to THOUGHTS.md
    if thoughts_file.exists():
        with open(thoughts_file, "a") as f:
            f.write(f"\n## {datetime.now().isoformat()} - Auto-Logged\n\n")
            f.write(f"Prompt: {entry.get('prompt', 'N/A')[:100]}...\n")
            f.write(f"Agent: {entry.get('agent_type', 'N/A')}\n")
            f.write(f"Reason: {entry.get('reason', 'N/A')}\n\n")

    log("Scribe agent completed")
    return True

def spawn_context_gatherer(entry):
    """Spawn context gatherer to scan projects"""
    log("Spawning context gatherer...")

    # Simple implementation: scan project structure
    projects_dir = Path.home() / ".blackbox5" / "5-project-memory"

    context = {
        "timestamp": datetime.now().isoformat(),
        "projects_scanned": [],
        "prompt": entry.get('prompt', '')
    }

    if projects_dir.exists():
        for project in projects_dir.iterdir():
            if project.is_dir():
                context["projects_scanned"].append({
                    "name": project.name,
                    "path": str(project)
                })

    # Write context to file
    context_file = BB5_DIR / ".autonomous" / "context-latest.json"
    with open(context_file, "w") as f:
        json.dump(context, f, indent=2)

    log(f"Context gatherer completed - scanned {len(context['projects_scanned'])} projects")
    return True

# Mapping of agent types to signal file names and display names
AGENT_SIGNAL_MAP = {
    'superintelligence': ('superintelligence-active', 'superintelligence protocol'),
    'research-suite': ('research-suite-active', 'research suite'),
    'executor': ('executor-active', 'executor'),
    'planner': ('planner-active', 'planner'),
    'debug-workflow': ('debug-workflow-active', 'debug workflow'),
    'validator': ('validator-active', 'validator'),
    'git-commit': ('git-commit-active', 'git commit'),
    'dependency-analysis': ('dependency-analysis-active', 'dependency analysis'),
    'performance-analysis': ('performance-analysis-active', 'performance analysis'),
    'security-audit': ('security-audit-active', 'security audit'),
}

def spawn_agent(agent_type, entry):
    """
    Generic agent spawner that creates signal files.

    Args:
        agent_type: Type of agent to spawn
        entry: Queue entry containing prompt and metadata

    Returns:
        bool: True if successful, False otherwise
    """
    if agent_type not in AGENT_SIGNAL_MAP:
        log(f"Unknown agent type for signal spawning: {agent_type}")
        return False

    signal_file, display_name = AGENT_SIGNAL_MAP[agent_type]
    log(f"Spawning {display_name}...")

    try:
        signal = SIGNALS_DIR / signal_file
        with open(signal, "w") as f:
            f.write(json.dumps({
                "timestamp": datetime.now().isoformat(),
                "prompt": entry.get('prompt', ''),
                "status": "activating"
            }))

        log(f"{display_name.title()} activation signal created")
        return True
    except Exception as e:
        log(f"Error creating signal for {agent_type}: {e}")
        return False

def process_entry(entry):
    """
    Process a single spawn queue entry.

    Routes to appropriate spawn handler based on agent type.
    Agents with custom logic have dedicated handlers,
    while signal-based agents use the generic spawn_agent function.

    Args:
        entry: Queue entry with agent_type, status, prompt, etc.

    Returns:
        Updated entry with status and completion info
    """
    agent_type = entry.get('agent_type')
    status = entry.get('status')

    if status != 'pending':
        return entry

    log(f"Processing agent: {agent_type}")

    # Update status to running
    entry['status'] = 'running'
    entry['started_at'] = datetime.now().isoformat()

    # Spawn based on agent type
    success = False
    try:
        # Agents with custom logic
        if agent_type == 'scribe':
            success = spawn_scribe_agent(entry)
        elif agent_type == 'context-gatherer':
            success = spawn_context_gatherer(entry)
        # Signal-based agents use generic handler
        elif agent_type in AGENT_SIGNAL_MAP:
            success = spawn_agent(agent_type, entry)
        else:
            log(f"Unknown agent type: {agent_type}")
            entry['status'] = 'failed'
            entry['error'] = f"Unknown agent type: {agent_type}"
            return entry
    except Exception as e:
        log(f"Error spawning {agent_type}: {e}")
        entry['status'] = 'failed'
        entry['error'] = str(e)
        return entry

    # Update status based on result
    if success:
        entry['status'] = 'completed'
        entry['completed_at'] = datetime.now().isoformat()
    else:
        entry['status'] = 'failed'

    return entry

def main():
    log("Agent Runner starting...")

    # Ensure directories exist
    SIGNALS_DIR.mkdir(parents=True, exist_ok=True)
    (BB5_DIR / ".autonomous" / "logs").mkdir(parents=True, exist_ok=True)

    # Read spawn queue
    entries = read_spawn_queue()
    if not entries:
        log("No entries in spawn queue")
        return

    log(f"Found {len(entries)} entries in spawn queue")

    # Process each entry
    updated_entries = []
    for entry in entries:
        if isinstance(entry, dict) and entry.get('status') == 'pending':
            updated_entry = process_entry(entry)
            updated_entries.append(updated_entry)
        else:
            updated_entries.append(entry)

    # Write updated queue
    write_spawn_queue(updated_entries)

    log("Agent Runner completed")

if __name__ == "__main__":
    main()
