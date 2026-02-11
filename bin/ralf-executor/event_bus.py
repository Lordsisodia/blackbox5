#!/usr/bin/env python3
"""Event bus with WAL persistence for BB5 agent communication."""
import json
import os
import time
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# BB5 paths
BB5_ROOT = "/Users/shaansisodia/blackbox5"
PROJECT_ROOT = f"{BB5_ROOT}/5-project-memory/blackbox5"
CI_ROOT = f"{PROJECT_ROOT}/.autonomous/ci"
EVENTS_FILE = f"{CI_ROOT}/events/events.jsonl"
WAL_FILE = f"{CI_ROOT}/events/events.wal"
CHECKPOINT_FILE = f"{CI_ROOT}/events/checkpoint.json"

class EventBus:
    """Event bus with write-ahead logging for durability."""

    def __init__(self):
        self.events_file = EVENTS_FILE
        self.wal_file = WAL_FILE
        self.checkpoint_file = CHECKPOINT_FILE
        os.makedirs(os.path.dirname(self.events_file), exist_ok=True)
        self._lock_file = f"{CI_ROOT}/events/.lock"
        self._ensure_lock_dir()

    def _ensure_lock_dir(self):
        """Ensure events directory exists."""
        os.makedirs(os.path.dirname(self.events_file), exist_ok=True)

    def _acquire_lock(self):
        """Simple file-based lock."""
        while os.path.exists(self._lock_file):
            time.sleep(0.01)
        Path(self._lock_file).touch()

    def _release_lock(self):
        """Release file-based lock."""
        if os.path.exists(self._lock_file):
            os.remove(self._lock_file)

    def _write_wal(self, event: Dict[str, Any]):
        """Write event to write-ahead log."""
        with open(self.wal_file, 'a') as f:
            f.write(json.dumps(event) + '\n')
            f.flush()
            os.fsync(f.fileno())  # Ensure durability

    def _commit_wal(self, event: Dict[str, Any]):
        """Commit WAL entry to main log."""
        with open(self.events_file, 'a') as f:
            f.write(json.dumps(event) + '\n')
            f.flush()
            os.fsync(f.fileno())

    def _checkpoint(self):
        """Create checkpoint for recovery."""
        checkpoint = {
            "timestamp": datetime.now().isoformat(),
            "events_file_size": os.path.getsize(self.events_file) if os.path.exists(self.events_file) else 0,
            "wal_file_size": os.path.getsize(self.wal_file) if os.path.exists(self.wal_file) else 0
        }
        with open(self.checkpoint_file, 'w') as f:
            json.dump(checkpoint, f)

    def recover(self) -> List[Dict[str, Any]]:
        """Recover events from WAL after crash."""
        recovered = []

        # Check if WAL has uncommitted events
        if os.path.exists(self.wal_file):
            with open(self.wal_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        event = json.loads(line)
                        recovered.append(event)
                    except json.JSONDecodeError:
                        continue

            # Re-commit recovered events
            for event in recovered:
                with open(self.events_file, 'a') as f:
                    f.write(json.dumps(event) + '\n')

            # Clear WAL after recovery
            os.remove(self.wal_file)
            print(f"[EventBus] Recovered {len(recovered)} events from WAL")

        return recovered

    def publish(self, event_type: str, payload: Dict[str, Any], source: str = "ci-orchestrator") -> str:
        """Publish an event with WAL durability."""
        self._acquire_lock()
        try:
            event = {
                "id": f"evt-{int(time.time() * 1000)}",  # Higher precision ID
                "timestamp": datetime.now().isoformat(),
                "type": event_type,
                "payload": payload,
                "source": source
            }

            # Write to WAL first (durability)
            self._write_wal(event)

            # Commit to main log
            self._commit_wal(event)

            # Clear WAL entry (optimistic)
            # In production, we'd truncate the WAL, but for simplicity we keep it

            # Periodic checkpoint
            if int(time.time()) % 60 == 0:  # Every minute
                self._checkpoint()

            return event["id"]
        finally:
            self._release_lock()

    def get_events(self, event_type: Optional[str] = None, since: Optional[str] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get events from log with optional filtering."""
        events = []
        if not os.path.exists(self.events_file):
            return events

        with open(self.events_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                    if event_type and event.get('type') != event_type:
                        continue
                    if since and event.get('timestamp', '') < since:
                        continue
                    events.append(event)
                except json.JSONDecodeError:
                    continue

        if limit:
            events = events[-limit:]

        return events

    def get_event_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific event by ID."""
        events = self.get_events()
        for event in events:
            if event.get('id') == event_id:
                return event
        return None

# Singleton for easy import
event_bus = EventBus()

# Auto-recover on module load
recovered = event_bus.recover()
if recovered:
    print(f"[EventBus] Automatically recovered {len(recovered)} events from WAL")
