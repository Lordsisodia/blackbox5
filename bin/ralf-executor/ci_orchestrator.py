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
BB5_ROOT = "/Users/shaansisodia/blackbox5"
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


class CircuitBreaker:
    """Circuit breaker pattern to prevent cascade failures."""

    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open

    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        if self.state == "open":
            if self._should_attempt_reset():
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is open")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _should_attempt_reset(self):
        """Check if enough time has passed to try again."""
        if not self.last_failure_time:
            return True
        return (time.time() - self.last_failure_time) > self.recovery_timeout

    def _on_success(self):
        """Handle successful call."""
        if self.state == "half-open":
            self.state = "closed"
        self.failures = 0

    def _on_failure(self):
        """Handle failed call."""
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "open"


class RateLimiter:
    """Rate limiter for agent spawning."""

    def __init__(self, max_per_minute=10):
        self.max_per_minute = max_per_minute
        self.spawn_times = []

    def can_spawn(self):
        """Check if spawn is allowed under rate limit."""
        now = time.time()
        # Remove spawns older than 1 minute
        self.spawn_times = [t for t in self.spawn_times if now - t < 60]
        return len(self.spawn_times) < self.max_per_minute

    def record_spawn(self):
        """Record a spawn attempt."""
        self.spawn_times.append(time.time())

    def get_wait_time(self):
        """Get seconds until next spawn allowed."""
        if self.can_spawn():
            return 0
        now = time.time()
        oldest = min(self.spawn_times)
        return max(0, 60 - (now - oldest))


class AgentMonitor:
    """Monitors health of spawned agents."""

    def __init__(self, timeout_seconds=300):
        self.timeout_seconds = timeout_seconds
        self.active_agents = {}  # agent_id -> {started_at, issue_id, pid}
        self.completed_agents = []
        self._lock = threading.Lock()

    def record_start(self, agent_id, issue_id, pid=None):
        """Record agent start."""
        with self._lock:
            self.active_agents[agent_id] = {
                "started_at": time.time(),
                "issue_id": issue_id,
                "pid": pid,
                "last_heartbeat": time.time()
            }

    def record_heartbeat(self, agent_id):
        """Update agent heartbeat."""
        with self._lock:
            if agent_id in self.active_agents:
                self.active_agents[agent_id]["last_heartbeat"] = time.time()

    def record_complete(self, agent_id, success=True):
        """Record agent completion."""
        with self._lock:
            if agent_id in self.active_agents:
                info = self.active_agents.pop(agent_id)
                info["completed_at"] = time.time()
                info["success"] = success
                self.completed_agents.append(info)
                # Keep only last 100 completed
                if len(self.completed_agents) > 100:
                    self.completed_agents = self.completed_agents[-100:]

    def get_stuck_agents(self):
        """Get agents that have timed out."""
        now = time.time()
        stuck = []
        with self._lock:
            for agent_id, info in list(self.active_agents.items()):
                if now - info["last_heartbeat"] > self.timeout_seconds:
                    stuck.append((agent_id, info))
        return stuck

    def get_stats(self):
        """Get monitoring stats."""
        with self._lock:
            return {
                "active": len(self.active_agents),
                "completed": len(self.completed_agents),
                "stuck": len(self.get_stuck_agents())
            }


class CIOrchestrator:
    """Orchestrates the CI pipeline using event-driven architecture."""

    def __init__(self, max_agents_per_minute=10, circuit_threshold=5, agent_timeout=300):
        self.running = False
        self.cycle_count = 0
        self.event_handler = EventHandler(self)
        self._processed_events = set()  # Track processed event IDs
        self.rate_limiter = RateLimiter(max_agents_per_minute)
        self.circuit_breaker = CircuitBreaker(failure_threshold=circuit_threshold)
        self.agent_monitor = AgentMonitor(timeout_seconds=agent_timeout)
        self._spawn_stats = {"success": 0, "failed": 0, "rate_limited": 0}
        self._health_check_interval = 30
        self._last_health_check = 0

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
        i.add_watch(events_dir)

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
                        self._check_health()
        except KeyboardInterrupt:
            pass
        finally:
            i.remove_watch(events_dir)

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

    def _check_health(self):
        """Check health of active agents."""
        now = time.time()
        if now - self._last_health_check < self._health_check_interval:
            return
        self._last_health_check = now

        stuck = self.agent_monitor.get_stuck_agents()
        for agent_id, info in stuck:
            print(f"[{datetime.now().isoformat()}] Agent {agent_id} stuck, marking failed")
            self.agent_monitor.record_complete(agent_id, success=False)
            # Publish failure event
            event_bus.publish(
                "agent.failed",
                {"agent_id": agent_id, "issue_id": info.get("issue_id"), "reason": "timeout"},
                source="ci-orchestrator"
            )

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
        """Spawn an agent to handle work with rate limiting and circuit breaker."""
        agent = AGENTS.get(agent_key)
        if not agent:
            return

        agent_name = agent["name"]
        agent_file = f"{AGENTS_DIR}/{agent_name}.md"

        if not os.path.exists(agent_file):
            print(f"Agent file not found: {agent_file}")
            return

        # Check rate limiter
        if not self.rate_limiter.can_spawn():
            wait_time = self.rate_limiter.get_wait_time()
            print(f"[{datetime.now().isoformat()}] Rate limit hit for {agent_name}, waiting {wait_time:.1f}s")
            self._spawn_stats["rate_limited"] += 1
            # Re-queue the event by publishing it again
            time.sleep(wait_time)
            # Re-check after wait
            if not self.rate_limiter.can_spawn():
                print(f"[{datetime.now().isoformat()}] Still rate limited, skipping {agent_name}")
                return

        # Check circuit breaker
        if self.circuit_breaker.state == "open":
            print(f"[{datetime.now().isoformat()}] Circuit breaker open, skipping {agent_name}")
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

        # Spawn with circuit breaker protection
        try:
            self.circuit_breaker.call(self._spawn_claude_agent, agent_name, payload)
            self.rate_limiter.record_spawn()
            self._spawn_stats["success"] += 1
        except Exception as e:
            print(f"[{datetime.now().isoformat()}] Failed to spawn {agent_name}: {e}")
            self._spawn_stats["failed"] += 1

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
        print(f"\nSpawn Statistics:")
        print(f"  Success: {self._spawn_stats['success']}")
        print(f"  Failed: {self._spawn_stats['failed']}")
        print(f"  Rate Limited: {self._spawn_stats['rate_limited']}")
        print(f"\nCircuit Breaker: {self.circuit_breaker.state}")
        print(f"Rate Limit: {len(self.rate_limiter.spawn_times)}/{self.rate_limiter.max_per_minute} agents/min")
        stats = self.agent_monitor.get_stats()
        print(f"\nAgent Monitor:")
        print(f"  Active: {stats['active']}")
        print(f"  Completed: {stats['completed']}")
        print(f"  Stuck: {stats['stuck']}")


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
