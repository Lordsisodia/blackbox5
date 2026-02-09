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

def spawn_superintelligence(entry):
    """Activate superintelligence protocol"""
    log("Activating superintelligence protocol...")

    # Create team activation signal
    team_signal = SIGNALS_DIR / "superintelligence-active"
    with open(team_signal, "w") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "prompt": entry.get('prompt', ''),
            "status": "activating"
        }))

    log("Superintelligence team activation signal created")
    return True

def spawn_research_suite(entry):
    """Spawn research suite agents"""
    log("Spawning research suite...")
    signal = SIGNALS_DIR / "research-suite-active"
    with open(signal, "w") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "prompt": entry.get('prompt', ''),
            "status": "activating"
        }))
    log("Research suite activation signal created")
    return True

def spawn_executor(entry):
    """Spawn executor agent"""
    log("Spawning executor...")
    signal = SIGNALS_DIR / "executor-active"
    with open(signal, "w") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "prompt": entry.get('prompt', ''),
            "status": "activating"
        }))
    log("Executor activation signal created")
    return True

def spawn_planner(entry):
    """Spawn planner agent"""
    log("Spawning planner...")
    signal = SIGNALS_DIR / "planner-active"
    with open(signal, "w") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "prompt": entry.get('prompt', ''),
            "status": "activating"
        }))
    log("Planner activation signal created")
    return True

def spawn_debug_workflow(entry):
    """Spawn debug workflow"""
    log("Spawning debug workflow...")
    signal = SIGNALS_DIR / "debug-workflow-active"
    with open(signal, "w") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "prompt": entry.get('prompt', ''),
            "status": "activating"
        }))
    log("Debug workflow activation signal created")
    return True

def spawn_validator(entry):
    """Spawn validator agent"""
    log("Spawning validator...")
    signal = SIGNALS_DIR / "validator-active"
    with open(signal, "w") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "prompt": entry.get('prompt', ''),
            "status": "activating"
        }))
    log("Validator activation signal created")
    return True

def spawn_git_commit(entry):
    """Spawn git commit agent"""
    log("Spawning git commit agent...")
    signal = SIGNALS_DIR / "git-commit-active"
    with open(signal, "w") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "prompt": entry.get('prompt', ''),
            "status": "activating"
        }))
    log("Git commit activation signal created")
    return True

def spawn_dependency_analysis(entry):
    """Spawn dependency analysis"""
    log("Spawning dependency analysis...")
    signal = SIGNALS_DIR / "dependency-analysis-active"
    with open(signal, "w") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "prompt": entry.get('prompt', ''),
            "status": "activating"
        }))
    log("Dependency analysis activation signal created")
    return True

def spawn_performance_analysis(entry):
    """Spawn performance analysis"""
    log("Spawning performance analysis...")
    signal = SIGNALS_DIR / "performance-analysis-active"
    with open(signal, "w") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "prompt": entry.get('prompt', ''),
            "status": "activating"
        }))
    log("Performance analysis activation signal created")
    return True

def spawn_security_audit(entry):
    """Spawn security audit"""
    log("Spawning security audit...")
    signal = SIGNALS_DIR / "security-audit-active"
    with open(signal, "w") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "prompt": entry.get('prompt', ''),
            "status": "activating"
        }))
    log("Security audit activation signal created")
    return True

def process_entry(entry):
    """Process a single spawn queue entry"""
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
        if agent_type == 'scribe':
            success = spawn_scribe_agent(entry)
        elif agent_type == 'context-gatherer':
            success = spawn_context_gatherer(entry)
        elif agent_type == 'superintelligence':
            success = spawn_superintelligence(entry)
        elif agent_type == 'research-suite':
            success = spawn_research_suite(entry)
        elif agent_type == 'executor':
            success = spawn_executor(entry)
        elif agent_type == 'planner':
            success = spawn_planner(entry)
        elif agent_type == 'debug-workflow':
            success = spawn_debug_workflow(entry)
        elif agent_type == 'validator':
            success = spawn_validator(entry)
        elif agent_type == 'git-commit':
            success = spawn_git_commit(entry)
        elif agent_type == 'dependency-analysis':
            success = spawn_dependency_analysis(entry)
        elif agent_type == 'performance-analysis':
            success = spawn_performance_analysis(entry)
        elif agent_type == 'security-audit':
            success = spawn_security_audit(entry)
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
