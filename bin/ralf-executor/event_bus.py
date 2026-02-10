#!/usr/bin/env python3
"""Simple event bus for BB5 agent communication."""
import json
import os
import time
from datetime import datetime
from pathlib import Path

# BB5 paths
BB5_ROOT = "/Users/shaansisodia/.blackbox5"
PROJECT_ROOT = f"{BB5_ROOT}/5-project-memory/blackbox5"
CI_ROOT = f"{PROJECT_ROOT}/.autonomous/ci"
EVENTS_FILE = f"{CI_ROOT}/events/events.jsonl"

class EventBus:
    """Simple event bus for CI system."""

    def __init__(self):
        self.events_file = EVENTS_FILE
        os.makedirs(os.path.dirname(self.events_file), exist_ok=True)

    def publish(self, event_type, payload, source="ci-orchestrator"):
        """Publish an event."""
        event = {
            "id": f"evt-{int(time.time())}",
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "payload": payload,
            "source": source
        }
        with open(self.events_file, 'a') as f:
            f.write(json.dumps(event) + '\n')
        return event["id"]

    def get_events(self, event_type=None, since=None):
        """Get events from log."""
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
        return events

# Singleton for easy import
event_bus = EventBus()
