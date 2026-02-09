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
import requests
from datetime import datetime
from pathlib import Path

BB5_DIR = Path("/opt/blackbox5")
SPAWN_QUEUE = BB5_DIR / "5-project-memory/blackbox5/.autonomous/agents/communications/spawn-queue.yaml"
SIGNALS_DIR = BB5_DIR / "5-project-memory/blackbox5/.autonomous/signals"
RUNS_DIR = BB5_DIR / "5-project-memory/blackbox5/.autonomous/runs"
LOG_FILE = BB5_DIR / ".autonomous/logs/vps-agent-loop.log"
MESSAGES_FILE = BB5_DIR / "agents" / "moltbot-autonomous" / "saved-messages.jsonl"
LAST_UPDATE_ID_FILE = BB5_DIR / "agents" / "moltbot-autonomous" / ".last_update_id"

# Telegram configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8581639813:AAFA13wDTKEX2x6J-lVfpq9QHnsGRnB1EZo")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7643203581")
TELEGRAM_TOPIC_ID = os.getenv("TELEGRAM_TOPIC_ID", "")  # Set for topic-specific updates

def log(message):
    timestamp = datetime.now().isoformat()
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(log_line + "\n")

def send_telegram_update(run_id, status, agent_type, duration, git_info=None):
    """Send run completion update to Telegram"""
    try:
        # Determine emoji based on status
        emoji = "📊"
        if status == "COMPLETED":
            emoji = "✅"
        elif status == "FAILED":
            emoji = "❌"
        elif status == "IN_PROGRESS":
            emoji = "⚠️"

        # Build message
        message = f"{emoji} <b>BB5 Run Complete</b>\n"
        message += f"<code>{run_id}</code>\n"
        message += "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        message += f"<b>Status:</b> {status}\n"
        message += f"<b>Agent:</b> {agent_type}\n"
        message += f"<b>Duration:</b> {duration}s\n\n"

        # Add git info if available
        if git_info:
            if git_info.get('committed'):
                message += f"<b>🔄 Git</b>\n"
                message += f"• Committed: yes\n"
                if git_info.get('pushed'):
                    message += f"• Pushed: yes\n"
                else:
                    message += f"• Pushed: no\n"
                message += "\n"

        # Add next action hint
        if status == "COMPLETED":
            message += "<i>✓ Run completed. Starting next cycle...</i>"
        elif status == "FAILED":
            message += "<i>⚠ Run failed. Will retry...</i>"
        else:
            message += "<i>⏳ Run in progress...</i>"

        # Send to Telegram
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        if TELEGRAM_TOPIC_ID:
            payload["message_thread_id"] = TELEGRAM_TOPIC_ID

        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json=payload,
            timeout=10
        )
    except Exception as e:
        log(f"Failed to send Telegram update: {e}")

def send_startup_notification():
    """Send startup notification to Telegram"""
    try:
        message = "🤖 <b>VPS Agent Loop Started</b>\n"
        message += "━━━━━━━━━━━━━━━━━━━━━━━\n"
        message += "<i>Will report after each run completes</i>"

        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        if TELEGRAM_TOPIC_ID:
            payload["message_thread_id"] = TELEGRAM_TOPIC_ID

        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json=payload,
            timeout=10
        )
    except Exception as e:
        log(f"Failed to send startup notification: {e}")

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

    # Record start time
    start_time = time.time()

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

    # Calculate duration
    duration = int(time.time() - start_time)

    log(f"Completed agent: {agent_type} (run: {run_id}, duration: {duration}s)")

    # Send Telegram update
    send_telegram_update(run_id, "COMPLETED", agent_type, duration)

    return entry

def check_git_changes():
    """Check for git changes and commit if needed"""
    git_info = {'committed': False, 'pushed': False}
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
            commit_result = subprocess.run(
                ["git", "commit", "-m", f"vps-agent: auto-commit {timestamp}"],
                capture_output=True,
                text=True
            )

            if commit_result.returncode == 0:
                git_info['committed'] = True
                log("Changes committed")

                # Try to push
                push_result = subprocess.run(
                    ["git", "push", "origin", "autonomous-improvement"],
                    capture_output=True,
                    text=True
                )

                if push_result.returncode == 0:
                    git_info['pushed'] = True
                    log("Changes pushed to GitHub")
                else:
                    log(f"Push failed: {push_result.stderr[:200]}")
            else:
                log(f"Commit failed: {commit_result.stderr[:200]}")

            return git_info
        else:
            return git_info

    except Exception as e:
        log(f"Error checking git: {e}")
        return git_info

def save_incoming_messages():
    """Check for and save incoming Telegram messages"""
    try:
        last_id = 0
        if LAST_UPDATE_ID_FILE.exists():
            try:
                last_id = int(LAST_UPDATE_ID_FILE.read_text().strip())
            except:
                pass

        response = requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates",
            params={"offset": last_id + 1, "limit": 100},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        if not data.get("ok"):
            return

        updates = data.get("result", [])
        if not updates:
            return

        saved_count = 0
        for update in updates:
            update_id = update["update_id"]

            if "message" not in update:
                LAST_UPDATE_ID_FILE.parent.mkdir(parents=True, exist_ok=True)
                LAST_UPDATE_ID_FILE.write_text(str(update_id))
                continue

            message = update["message"]
            chat_id = message.get("chat", {}).get("id")

            # Only save messages from authorized chat
            if str(chat_id) != TELEGRAM_CHAT_ID:
                LAST_UPDATE_ID_FILE.parent.mkdir(parents=True, exist_ok=True)
                LAST_UPDATE_ID_FILE.write_text(str(update_id))
                continue

            # Skip bot commands (messages starting with /)
            text = message.get("text", "")
            if text.startswith("/"):
                LAST_UPDATE_ID_FILE.parent.mkdir(parents=True, exist_ok=True)
                LAST_UPDATE_ID_FILE.write_text(str(update_id))
                continue

            # Build message record
            msg_data = {
                "saved_at": datetime.now().isoformat(),
                "update_id": update_id,
                "message_id": message.get("message_id"),
                "date": message.get("date"),
                "text": text,
                "from": {
                    "id": message.get("from", {}).get("id"),
                    "username": message.get("from", {}).get("username"),
                    "first_name": message.get("from", {}).get("first_name")
                },
                "chat": {
                    "id": chat_id,
                    "type": message.get("chat", {}).get("type"),
                    "title": message.get("chat", {}).get("title")
                }
            }

            # Add topic info if present
            if "message_thread_id" in message:
                msg_data["topic_id"] = message["message_thread_id"]

            # Save the message
            MESSAGES_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(MESSAGES_FILE, "a") as f:
                f.write(json.dumps(msg_data, default=str) + "\n")

            saved_count += 1
            LAST_UPDATE_ID_FILE.parent.mkdir(parents=True, exist_ok=True)
            LAST_UPDATE_ID_FILE.write_text(str(update_id))

        if saved_count > 0:
            log(f"Saved {saved_count} incoming message(s)")

    except Exception as e:
        log(f"Error saving messages: {e}")

def send_cycle_summary(entries_processed, git_info, duration):
    """Send summary of the cycle to Telegram"""
    try:
        message = f"📊 <b>Cycle Summary</b>\n"
        message += "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        message += f"<b>Entries Processed:</b> {entries_processed}\n"
        message += f"<b>Duration:</b> {duration}s\n\n"

        if git_info.get('committed'):
            message += f"<b>🔄 Git</b>\n"
            message += f"• Committed: yes\n"
            message += f"• Pushed: {'yes' if git_info.get('pushed') else 'no'}\n"

        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        if TELEGRAM_TOPIC_ID:
            payload["message_thread_id"] = TELEGRAM_TOPIC_ID

        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json=payload,
            timeout=10
        )
    except Exception as e:
        log(f"Failed to send cycle summary: {e}")

def run_cycle():
    """Run one cycle of the agent loop"""
    log("=" * 50)
    log("Starting VPS Agent Cycle")

    # Record cycle start time
    cycle_start_time = time.time()

    # 0. Save any incoming Telegram messages
    save_incoming_messages()

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
    git_info = check_git_changes()

    log("Cycle complete")

    # Send summary update about the whole cycle
    cycle_duration = int(time.time() - cycle_start_time)
    send_cycle_summary(len(pending), git_info, cycle_duration)

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

    # Send startup notification
    send_startup_notification()

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
