#!/usr/bin/env python3
"""
VPS Agent Loop - Lightweight autonomous agent for VPS
Runs continuously, processes spawn queue, and executes simple agent tasks
Designed for VPS deployment without requiring GLM or Claude API
"""

import os
import sys
import time
import json
import yaml
import subprocess
from datetime import datetime
from pathlib import Path

BB5_DIR = Path("/opt/blackbox5")
SPAWN_QUEUE = BB5_DIR / "5-project-memory/blackbox5/.autonomous/agents/communications/spawn-queue.yaml"
SIGNALS_DIR = BB5_DIR / "5-project-memory/blackbox5/.autonomous/signals"
RUNS_DIR = BB5_DIR / "5-project-memory/blackbox5/.autonomous/runs"
LOG_FILE = BB5_DIR / ".autonomous/logs/vps-agent-loop.log"

def log(message):
    timestamp = datetime.now().isoformat()
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
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
        SPAWN_QUEUE.parent.mkdir(parents=True, exist_ok=True)
        with open(SPAWN_QUEUE, "w") as f:
            yaml.dump(entries, f, default_flow_style=False)
    except Exception as e:
        log(f"Error writing spawn queue: {e}")

def create_run_folder():
    """Create a new run folder"""
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_folder = RUNS_DIR / f"run-{run_id}"
    run_folder.mkdir(parents=True, exist_ok=True)

    # Create standard files
    (run_folder / "THOUGHTS.md").write_text(f"""# VPS Agent Run {run_id}

**Started:** {datetime.now().isoformat()}

## Execution Log

""")

    (run_folder / "DECISIONS.md").write_text(f"""# VPS Agent Run {run_id} - DECISIONS

**Started:** {datetime.now().isoformat()}

""")

    (run_folder / "LEARNINGS.md").write_text(f"""# VPS Agent Run {run_id} - LEARNINGS

**Started:** {datetime.now().isoformat()}

""")

    (run_folder / "RESULTS.md").write_text(f"""# VPS Agent Run {run_id} - RESULTS

**Started:** {datetime.now().isoformat()}
**Status:** IN_PROGRESS

""")

    (run_folder / "status.txt").write_text("IN_PROGRESS")

    return run_folder, run_id

def process_spawn_entry(entry):
    """Process a single spawn queue entry"""
    agent_type = entry.get('agent_type', 'unknown')
    prompt = entry.get('prompt', '')

    log(f"Processing agent: {agent_type}")

    # Create run folder
    run_folder, run_id = create_run_folder()

    # Create signal file
    signal_file = SIGNALS_DIR / f"{agent_type}-active"
    SIGNALS_DIR.mkdir(parents=True, exist_ok=True)

    signal_data = {
        "timestamp": datetime.now().isoformat(),
        "agent_type": agent_type,
        "prompt": prompt[:200] if prompt else "",
        "run_id": run_id,
        "run_folder": str(run_folder),
        "status": "processing"
    }

    with open(signal_file, "w") as f:
        json.dump(signal_data, f, indent=2)

    # Append to THOUGHTS.md
    thoughts_file = run_folder / "THOUGHTS.md"
    with open(thoughts_file, "a") as f:
        f.write(f"\n## {datetime.now().isoformat()} - Processing {agent_type}\n\n")
        f.write(f"Prompt: {prompt[:200]}...\n\n")

    # Update entry status
    entry['status'] = 'completed'
    entry['completed_at'] = datetime.now().isoformat()
    entry['run_id'] = run_id

    # Update status file
    (run_folder / "status.txt").write_text("COMPLETED")

    # Update RESULTS.md
    with open(run_folder / "RESULTS.md", "a") as f:
        f.write(f"\n## Completed: {agent_type}\n")
        f.write(f"Status: COMPLETED\n")

    log(f"Completed agent: {agent_type} (run: {run_id})")

    return entry

def check_git_changes():
    """Check for git changes and commit if needed"""
    try:
        os.chdir(BB5_DIR)

        # Check for changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True
        )

        if result.stdout.strip():
            # There are changes
            log("Git changes detected, committing...")

            # Add all changes
            subprocess.run(["git", "add", "-A"], check=False)

            # Commit
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            subprocess.run(
                ["git", "commit", "-m", f"vps-agent: auto-commit {timestamp}"],
                check=False
            )

            # Try to push
            push_result = subprocess.run(
                ["git", "push", "origin", "autonomous-improvement"],
                capture_output=True,
                text=True
            )

            if push_result.returncode == 0:
                log("Changes pushed to GitHub")
            else:
                log(f"Push failed: {push_result.stderr[:200]}")

            return True
        else:
            return False

    except Exception as e:
        log(f"Error checking git: {e}")
        return False

def run_cycle():
    """Run one cycle of the agent loop"""
    log("=" * 50)
    log("Starting VPS Agent Cycle")

    # 1. Read spawn queue
    entries = read_spawn_queue()
    pending = [e for e in entries if isinstance(e, dict) and e.get('status') == 'pending']

    log(f"Found {len(pending)} pending entries in spawn queue")

    # 2. Process pending entries
    updated_entries = []
    for entry in entries:
        if isinstance(entry, dict) and entry.get('status') == 'pending':
            try:
                updated_entry = process_spawn_entry(entry)
                updated_entries.append(updated_entry)
            except Exception as e:
                log(f"Error processing entry: {e}")
                entry['status'] = 'failed'
                entry['error'] = str(e)
                updated_entries.append(entry)
        else:
            updated_entries.append(entry)

    # 3. Write updated queue
    write_spawn_queue(updated_entries)

    # 4. Check for git changes
    check_git_changes()

    log("Cycle complete")

def main():
    log("=" * 50)
    log("VPS Agent Loop Starting")
    log(f"BB5_DIR: {BB5_DIR}")
    log(f"Spawn Queue: {SPAWN_QUEUE}")
    log(f"Signals Dir: {SIGNALS_DIR}")
    log("=" * 50)

    # Ensure directories exist
    SPAWN_QUEUE.parent.mkdir(parents=True, exist_ok=True)
    SIGNALS_DIR.mkdir(parents=True, exist_ok=True)
    RUNS_DIR.mkdir(parents=True, exist_ok=True)

    # Initialize empty queue if needed
    if not SPAWN_QUEUE.exists():
        write_spawn_queue([])

    # Main loop
    cycle_count = 0
    while True:
        try:
            run_cycle()
            cycle_count += 1

            # Sleep between cycles
            log("Sleeping for 30 seconds...")
            time.sleep(30)

        except KeyboardInterrupt:
            log("Shutting down (KeyboardInterrupt)")
            break
        except Exception as e:
            log(f"Error in main loop: {e}")
            time.sleep(60)  # Longer sleep on error

if __name__ == "__main__":
    main()
