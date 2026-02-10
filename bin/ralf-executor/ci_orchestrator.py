#!/usr/bin/env python3
"""CI Orchestrator for BB5 - Coordinates the continuous improvement pipeline.

Event-driven using inotify (Linux) or watchdog (cross-platform).
Inspired by snarktank/ralph and mikeyobrien/ralph-orchestrator.
"""
import os
import sys
import time
import json
import subprocess
import threading
from datetime import datetime
from pathlib import Path

# Try to use inotify on Linux, fallback to polling watchdog
try:
    import inotify.adapters  # type: ignore
    HAS_INOTIFY = True
except ImportError:
    HAS_INOTIFY = False
    try:
        from watchdog.observers import Observer  # type: ignore
        from watchdog.events import FileSystemEventHandler  # type: ignore
        HAS_WATCHDOG = True
    except ImportError:
        HAS_WATCHDOG = False

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from event_bus import event_bus
from state_manager import state_manager

# BB5 paths
BB5_ROOT = "/Users/shaansisodia/.blackbox5"
PROJECT_ROOT = f"{BB5_ROOT}/5-project-memory/blackbox5"
AGENTS_DIR = f"{PROJECT_ROOT}/.claude/agents"

# Agent definitions
AGENTS = {
    "error-detector": {
        "name": "bb5-error-detector",
        "description": "Error detection specialist",
        "trigger": "manual",  # Run manually or on schedule
        "input": "scan target",
        "output": "issue.detected event"
    },
    "issue-validator": {
        "name": "bb5-issue-validator",
        "description": "Issue validation specialist",
        "trigger": "issue.detected",
        "input": "issue_id",
        "output": "issue.validated or issue.rejected"
    },
    "ci-planner": {
        "name": "bb5-ci-planner",
        "description": "CI planning specialist",
        "trigger": "issue.validated",
        "input": "issue_id",
        "output": "plan.created"
    },
    "ci-executor": {
        "name": "bb5-ci-executor",
        "description": "CI execution specialist",
        "trigger": "plan.created",
        "input": "plan_id",
        "output": "execution.completed or execution.failed"
    },
    "ci-validator": {
        "name": "bb5-ci-validator",
        "description": "CI validation specialist",
        "trigger": "execution.completed",
        "input": "execution_id",
        "output": "issue.resolved or execution.failed"
    }
}


class EventHandler:
    """Handles filesystem events."""

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.last_position = 0

    def on_event(self, event_path=None):
        """Called when events file changes."""
        # Read new events from file
        events = self._read_new_events()
        for event in events:
            self.orchestrator._handle_event(event)

    def _read_new_events(self):
        """Read events added since last check."""
        events = []
        if not os.path.exists(event_bus.events_file):
            return events

        with open(event_bus.events_file, 'r') as f:
            # Seek to last position
            f.seek(self.last_position)
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
            # Update position
            self.last_position = f.tell()

        return events


class CIOrchestrator:
    """Orchestrates the CI pipeline using event-driven architecture."""

    def __init__(self):
        self.running = False
        self.cycle_count = 0
        self.event_handler = EventHandler(self)
        self._processed_events = set()  # Track processed event IDs

    def start(self):
        """Start the event-driven orchestrator."""
        self.running = True
        print(f"[{datetime.now().isoformat()}] CI Orchestrator starting...")
        print(f"Monitoring events at: {event_bus.events_file}")

        # Ensure events file exists
        os.makedirs(os.path.dirname(event_bus.events_file), exist_ok=True)

        # Get initial file position
        if os.path.exists(event_bus.events_file):
            self.event_handler.last_position = os.path.getsize(event_bus.events_file)

        # Start event-driven monitoring
        if HAS_INOTIFY:
            self._start_inotify()
        elif HAS_WATCHDOG:
            self._start_watchdog()
        else:
            print("Warning: No inotify/watchdog available, falling back to polling")
            self._start_polling()

    def _start_inotify(self):
        """Start Linux inotify-based monitoring (event-driven)."""
        print("Using inotify for event-driven monitoring")
        events_dir = os.path.dirname(event_bus.events_file)

        i = inotify.adapters.Inotify()
        i.add_watch(events_dir.encode())

        try:
            for event in i.event_gen(yield_nones=False):
                if not self.running:
                    break

                (_, type_names, path, filename) = event

                # Check if our events file was modified
                if filename == os.path.basename(event_bus.events_file):
                    if 'IN_MODIFY' in type_names or 'IN_CLOSE_WRITE' in type_names:
                        self.cycle_count += 1
                        self.event_handler.on_event()
        except KeyboardInterrupt:
            pass
        finally:
            i.remove_watch(events_dir.encode())

    def _start_watchdog(self):
        """Start watchdog-based monitoring (event-driven)."""
        print("Using watchdog for event-driven monitoring")
        events_dir = os.path.dirname(event_bus.events_file)

        class WatchdogHandler(FileSystemEventHandler):
            def __init__(self, handler):
                self.handler = handler

            def on_modified(self, event):
                if not event.is_directory:
                    if os.path.basename(event.src_path) == os.path.basename(event_bus.events_file):
                        self.handler.on_event()

        observer = Observer()
        observer.schedule(WatchdogHandler(self.event_handler), events_dir, recursive=False)
        observer.start()

        try:
            while self.running:
                time.sleep(0.1)  # Small sleep to prevent CPU spin
        except KeyboardInterrupt:
            pass
        finally:
            observer.stop()
            observer.join()

    def _start_polling(self):
        """Fallback polling mode (not event-driven)."""
        print("Using polling fallback (5 second interval)")
        while self.running:
            self.cycle_count += 1
            try:
                self.event_handler.on_event()
            except Exception as e:
                print(f"Error in cycle {self.cycle_count}: {e}")
            time.sleep(5)

    def stop(self):
        """Stop the orchestrator."""
        self.running = False
        print(f"[{datetime.now().isoformat()}] CI Orchestrator stopping...")

    def _handle_event(self, event):
        """Handle a single event (idempotent)."""
        event_id = event.get("id")

        # Skip already processed events
        if event_id in self._processed_events:
            return
        self._processed_events.add(event_id)

        # Limit memory usage
        if len(self._processed_events) > 10000:
            self._processed_events = set(list(self._processed_events)[-5000:])

        event_type = event.get("type")
        payload = event.get("payload", {})

        if event_type == "issue.detected":
            self._spawn_agent("issue-validator", payload)
        elif event_type == "issue.validated":
            self._spawn_agent("ci-planner", payload)
        elif event_type == "plan.created":
            self._spawn_agent("ci-executor", payload)
        elif event_type == "execution.completed":
            self._spawn_agent("ci-validator", payload)

    def _check_pending_work(self):
        """Check for pending work that needs agents."""
        # Check for validated issues without plans
        issues = state_manager.list_issues(status="validated")
        for issue in issues:
            if not issue.get("plan_id"):
                self._spawn_agent("ci-planner", {"issue_id": issue["issue_id"]})

        # Check for created plans without executions
        # (This would require listing plans, skipping for now)

    def _spawn_agent(self, agent_key, payload):
        """Spawn an agent to handle work."""
        agent = AGENTS.get(agent_key)
        if not agent:
            return

        agent_name = agent["name"]
        agent_file = f"{AGENTS_DIR}/{agent_name}.md"

        if not os.path.exists(agent_file):
            print(f"Agent file not found: {agent_file}")
            return

        # Create spawn event
        event_bus.publish(
            "agent.spawned",
            {
                "agent": agent_name,
                "trigger": agent["trigger"],
                "input": payload
            },
            source="ci-orchestrator"
        )

        print(f"[{datetime.now().isoformat()}] Spawning {agent_name} with payload: {payload}")

        # Spawn the agent using Claude Code
        # This uses the Task tool equivalent via CLI
        self._spawn_claude_agent(agent_name, payload)

    def _spawn_claude_agent(self, agent_name, payload):
        """Spawn a Claude Code agent."""
        # Build the prompt for the agent
        prompt = self._build_agent_prompt(agent_name, payload)

        # Write prompt to temp file
        prompt_file = f"/tmp/bb5-agent-{agent_name}-{int(time.time())}.txt"
        with open(prompt_file, 'w') as f:
            f.write(prompt)

        # Spawn using claude command
        cmd = [
            "claude",
            "--no-stream",
            "--output-format", "json",
            "-p", prompt
        ]

        try:
            # Run in background (non-blocking)
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            print(f"  -> Agent {agent_name} spawned (PID detached)")
        except Exception as e:
            print(f"  -> Failed to spawn {agent_name}: {e}")

    def _build_agent_prompt(self, agent_name, payload):
        """Build the prompt for an agent."""
        base_prompt = f"""You are the {agent_name} agent for BlackBox5 Continuous Improvement.

Your task is to process the following input and complete your assigned work.

INPUT:
```json
{json.dumps(payload, indent=2)}
```

INSTRUCTIONS:
1. Read your agent definition at: {AGENTS_DIR}/{agent_name}.md
2. Follow the process defined in your agent file
3. Use the event_bus and state_manager for communication
4. Publish appropriate events when complete
5. Document your work in the CI directories

Complete your task and exit.
"""
        return base_prompt

    def trigger_error_detection(self, scan_target="logs"):
        """Manually trigger error detection."""
        issue_id = state_manager.create_issue(
            title=f"Error scan: {scan_target}",
            description=f"Automated error detection scan of {scan_target}",
            source="manual_trigger",
            severity="medium"
        )

        event_bus.publish(
            "issue.detected",
            {"issue_id": issue_id, "scan_target": scan_target},
            source="manual"
        )

        print(f"Triggered error detection for {scan_target}")
        print(f"Issue created: {issue_id}")
        return issue_id

    def status(self):
        """Show current CI status."""
        print("\n=== BB5 CI Status ===\n")

        print("Issues:")
        for status in ["detected", "validated", "planned", "in_progress", "resolved", "rejected"]:
            issues = state_manager.list_issues(status=status)
            print(f"  {status}: {len(issues)}")

        print("\nRecent Events:")
        events = event_bus.get_events()
        for event in events[-10:]:
            print(f"  [{event.get('timestamp', 'N/A')}] {event.get('type')} from {event.get('source')}")

        print(f"\nOrchestrator cycles: {self.cycle_count}")
        print(f"Running: {self.running}")


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="BB5 CI Orchestrator")
    parser.add_argument("command", choices=["start", "stop", "status", "trigger"])
    parser.add_argument("--target", default="logs", help="Scan target for trigger")
    parser.add_argument("--daemon", action="store_true", help="Run as daemon")

    args = parser.parse_args()

    orchestrator = CIOrchestrator()

    if args.command == "start":
        if args.daemon:
            # Fork to background
            pid = os.fork()
            if pid > 0:
                print(f"Orchestrator started as daemon (PID: {pid})")
                sys.exit(0)
        orchestrator.start()
    elif args.command == "stop":
        # Write stop file
        with open("/tmp/bb5-ci-stop", 'w') as f:
            f.write("stop")
        print("Stop signal sent")
    elif args.command == "status":
        orchestrator.status()
    elif args.command == "trigger":
        orchestrator.trigger_error_detection(args.target)
