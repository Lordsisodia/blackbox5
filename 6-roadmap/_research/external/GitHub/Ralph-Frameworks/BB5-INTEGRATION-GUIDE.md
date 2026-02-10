# BB5 Ralph Integration Guide

**Date:** 2026-02-10
**Status:** Draft
**Purpose:** Practical guide for integrating Ralph framework patterns into BB5

---

## Executive Summary

This guide provides step-by-step instructions for integrating proven patterns from 4 Ralph frameworks into BB5's RALF executor. Focus is on reusing working code with minimal modifications.

**Integration Priority:**
1. Safety mechanisms (circuit breaker) - Week 1
2. Structured memory system - Week 2
3. Agent specialization (hats) - Week 3-4
4. Event pub/sub - Week 5-6

---

## Part 1: Circuit Breaker Pattern

### Source: frankbria/ralph-claude-code

**What it does:** Prevents runaway loops by tracking failures and halting execution when thresholds are exceeded.

**Why BB5 needs it:** Current retry logic is basic (fixed count). No protection against infinite loops or API quota exhaustion.

### Implementation

#### File: `bin/ralf-executor/circuit_breaker.py`

```python
#!/usr/bin/env python3
"""Circuit breaker pattern for BB5 RALF executor.

Adapted from frankbria/ralph-claude-code/lib/circuit_breaker.sh
"""

import time
import json
import os
from enum import Enum
from dataclasses import dataclass, asdict
from typing import Optional, Callable, Any


class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    HALF_OPEN = "half_open"  # Testing if service recovered
    OPEN = "open"          # Halted, rejecting calls


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker."""
    no_progress_threshold: int = 3      # Open after N loops with no progress
    same_error_threshold: int = 5       # Open after N loops with same error
    permission_denial_threshold: int = 2  # Open after N permission denials
    cooldown_minutes: int = 30          # Time before HALF_OPEN
    auto_reset: bool = False            # Reset to CLOSED on startup


@dataclass
class CircuitBreakerState:
    """Persistent state for circuit breaker."""
    state: str = "closed"
    failure_count: int = 0
    consecutive_no_progress: int = 0
    consecutive_same_error: int = 0
    consecutive_permission_denials: int = 0
    last_error: str = ""
    opened_at: Optional[float] = None
    last_change: Optional[float] = None


class CircuitBreaker:
    """Prevents runaway loops by tracking failures.

    Three states:
    - CLOSED: Normal operation, calls pass through
    - OPEN: Halted due to failures, calls rejected
    - HALF_OPEN: Testing if service recovered

    Usage:
        cb = CircuitBreaker(state_file=".ralf/circuit_state.json")

        try:
            result = cb.call(execute_task, task_file)
        except CircuitBreakerOpen:
            logger.error("Circuit breaker is open - halting execution")
            return
    """

    def __init__(self, state_file: str, config: Optional[CircuitBreakerConfig] = None):
        self.config = config or CircuitBreakerConfig()
        self.state_file = state_file
        self.state = self._load_state()

        # Auto-reset if configured
        if self.config.auto_reset and self.state.state == "open":
            self.reset()

    def _load_state(self) -> CircuitBreakerState:
        """Load state from disk or create new."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    return CircuitBreakerState(**data)
            except Exception:
                pass
        return CircuitBreakerState()

    def _save_state(self):
        """Persist state to disk."""
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(asdict(self.state), f, indent=2)

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection.

        Args:
            func: Function to call
            *args, **kwargs: Arguments to pass to function

        Returns:
            Result from func

        Raises:
            CircuitBreakerOpen: If circuit is OPEN and cooldown hasn't passed
        """
        # Check if we should transition from OPEN to HALF_OPEN
        if self.state.state == "open":
            if self._should_attempt_reset():
                self.state.state = "half_open"
                self.state.last_change = time.time()
                self._save_state()
            else:
                raise CircuitBreakerOpen(
                    f"Circuit breaker is OPEN. "
                    f"Cooldown: {self._get_remaining_cooldown():.0f} minutes remaining"
                )

        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure(e)
            raise

    def on_success(self):
        """Record successful execution."""
        self.state.consecutive_no_progress = 0
        self.state.consecutive_same_error = 0
        self.state.consecutive_permission_denials = 0

        # If HALF_OPEN and success, close the circuit
        if self.state.state == "half_open":
            self.state.state = "closed"
            self.state.failure_count = 0
            self.state.opened_at = None
            self.state.last_change = time.time()

        self._save_state()

    def on_failure(self, error: Exception):
        """Record failed execution.

        Args:
            error: The exception that occurred
        """
        error_str = str(error)
        self.state.failure_count += 1

        # Track same error
        if error_str == self.state.last_error:
            self.state.consecutive_same_error += 1
        else:
            self.state.consecutive_same_error = 1
            self.state.last_error = error_str

        # Check if we should open the circuit
        should_open = (
            self.state.consecutive_no_progress >= self.config.no_progress_threshold or
            self.state.consecutive_same_error >= self.config.same_error_threshold
        )

        if should_open and self.state.state != "open":
            self.state.state = "open"
            self.state.opened_at = time.time()
            self.state.last_change = time.time()

        self._save_state()

    def on_no_progress(self):
        """Record iteration with no file changes."""
        self.state.consecutive_no_progress += 1

        if self.state.consecutive_no_progress >= self.config.no_progress_threshold:
            if self.state.state != "open":
                self.state.state = "open"
                self.state.opened_at = time.time()
                self.state.last_change = time.time()

        self._save_state()

    def on_permission_denial(self):
        """Record permission denial."""
        self.state.consecutive_permission_denials += 1

        if self.state.consecutive_permission_denials >= self.config.permission_denial_threshold:
            if self.state.state != "open":
                self.state.state = "open"
                self.state.opened_at = time.time()
                self.state.last_change = time.time()

        self._save_state()

    def _should_attempt_reset(self) -> bool:
        """Check if cooldown has passed."""
        if self.state.opened_at is None:
            return True

        elapsed_minutes = (time.time() - self.state.opened_at) / 60
        return elapsed_minutes >= self.config.cooldown_minutes

    def _get_remaining_cooldown(self) -> float:
        """Get remaining cooldown time in minutes."""
        if self.state.opened_at is None:
            return 0

        elapsed_minutes = (time.time() - self.state.opened_at) / 60
        return max(0, self.config.cooldown_minutes - elapsed_minutes)

    def reset(self):
        """Manually reset circuit to CLOSED."""
        self.state = CircuitBreakerState()
        self.state.last_change = time.time()
        self._save_state()

    def get_status(self) -> dict:
        """Get current status for monitoring."""
        return {
            "state": self.state.state,
            "failure_count": self.state.failure_count,
            "consecutive_no_progress": self.state.consecutive_no_progress,
            "consecutive_same_error": self.state.consecutive_same_error,
            "consecutive_permission_denials": self.state.consecutive_permission_denials,
            "remaining_cooldown": self._get_remaining_cooldown() if self.state.state == "open" else 0
        }


class CircuitBreakerOpen(Exception):
    """Raised when circuit breaker is OPEN."""
    pass


# Integration with existing executor
class CircuitBreakerMixin:
    """Mixin to add circuit breaker to existing executor."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.circuit_breaker = CircuitBreaker(
            state_file=".autonomous/circuit_state.json",
            config=CircuitBreakerConfig(
                no_progress_threshold=3,
                same_error_threshold=5,
                cooldown_minutes=30
            )
        )

    def execute_with_protection(self, task_func, *args, **kwargs):
        """Execute task with circuit breaker protection."""
        try:
            return self.circuit_breaker.call(task_func, *args, **kwargs)
        except CircuitBreakerOpen as e:
            self.logger.error(f"Circuit breaker halted execution: {e}")
            # Create alert/notification
            self._create_circuit_breaker_alert(str(e))
            raise

    def _create_circuit_breaker_alert(self, message: str):
        """Create alert when circuit breaker opens."""
        alert_file = ".autonomous/alerts/circuit_breaker_open.md"
        os.makedirs(os.path.dirname(alert_file), exist_ok=True)

        with open(alert_file, 'w') as f:
            f.write(f"""# Circuit Breaker Alert

**Status:** OPEN
**Time:** {datetime.now().isoformat()}
**Message:** {message}

## Actions Required

1. Review recent execution logs
2. Check for recurring errors
3. Fix underlying issue
4. Reset circuit breaker when ready:
   ```python
   from circuit_breaker import CircuitBreaker
   cb = CircuitBreaker(".autonomous/circuit_state.json")
   cb.reset()
   ```

## Recent State

```json
{json.dumps(self.circuit_breaker.get_status(), indent=2)}
```
""")
```

### Integration Steps

1. **Copy file** to `bin/ralf-executor/circuit_breaker.py`
2. **Modify** `executor.py` to import and use `CircuitBreakerMixin`
3. **Wrap** task execution with `execute_with_protection()`
4. **Add** circuit breaker status check to dashboard

### Testing

```python
# test_circuit_breaker.py
import unittest
from circuit_breaker import CircuitBreaker, CircuitBreakerOpen

class TestCircuitBreaker(unittest.TestCase):
    def test_opens_after_failures(self):
        cb = CircuitBreaker("/tmp/test_cb.json")

        # Simulate failures
        for _ in range(3):
            try:
                cb.call(lambda: (_ for _ in ()).throw(Exception("Test error")))
            except Exception:
                pass

        # Circuit should be open
        with self.assertRaises(CircuitBreakerOpen):
            cb.call(lambda: "success")
```

---

## Part 2: Structured Memory System

### Source: mikeyobrien/ralph-orchestrator

**What it does:** Categorizes learnings into types (Pattern, Decision, Fix, Context) with token budget management.

**Why BB5 needs it:** We write LEARNINGS.md but don't structure or retrieve them effectively.

### Implementation

#### File: `bin/ralf-executor/memory_manager.py`

```python
#!/usr/bin/env python3
"""Structured memory system for BB5.

Adapted from mikeyobrien/ralph-orchestrator memory system.
"""

import os
import json
import time
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict
from enum import Enum


class MemoryType(Enum):
    PATTERN = "pattern"      # Reusable code patterns
    DECISION = "decision"    # Architecture decisions
    FIX = "fix"             # Bug fixes and solutions
    CONTEXT = "context"     # Project-specific context


@dataclass
class Memory:
    """Single memory entry."""
    id: str
    memory_type: str
    content: str
    tags: List[str]
    source_task: str
    created: str

    def to_markdown(self) -> str:
        """Convert to markdown format."""
        return f"""### {self.id}

**Type:** {self.memory_type}
**Tags:** {', '.join(self.tags)}
**Source:** {self.source_task}
**Created:** {self.created}

{self.content}

---
"""


class MemoryManager:
    """Manages persistent learning across sessions.

    Usage:
        mm = MemoryManager(".autonomous/memories/")

        # Add memory from task execution
        mm.add_memory(
            memory_type=MemoryType.PATTERN,
            content="Use sqlx for database migrations",
            tags=["database", "migration"],
            source_task="TASK-001"
        )

        # Retrieve for prompt
        memories = mm.get_memories_for_prompt(
            query="database",
            max_tokens=2000
        )
    """

    def __init__(self, memories_dir: str, max_total_tokens: int = 10000):
        self.memories_dir = memories_dir
        self.max_total_tokens = max_total_tokens
        self.index_file = os.path.join(memories_dir, "index.json")

        os.makedirs(memories_dir, exist_ok=True)
        self.index = self._load_index()

    def _load_index(self) -> Dict:
        """Load memory index."""
        if os.path.exists(self.index_file):
            with open(self.index_file, 'r') as f:
                return json.load(f)
        return {"memories": [], "last_updated": None}

    def _save_index(self):
        """Save memory index."""
        self.index["last_updated"] = datetime.now().isoformat()
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2)

    def add_memory(self, memory_type: MemoryType, content: str,
                   tags: List[str], source_task: str) -> Memory:
        """Add a new memory.

        Args:
            memory_type: Type of memory (Pattern, Decision, Fix, Context)
            content: The learning/pattern/decision
            tags: Categories for retrieval
            source_task: Which task created this memory

        Returns:
            Created Memory object
        """
        memory = Memory(
            id=f"mem-{int(time.time())}-{hash(content) % 10000:04d}",
            memory_type=memory_type.value,
            content=content,
            tags=tags,
            source_task=source_task,
            created=datetime.now().isoformat()
        )

        # Save to file
        memory_file = os.path.join(self.memories_dir, f"{memory.id}.md")
        with open(memory_file, 'w') as f:
            f.write(memory.to_markdown())

        # Update index
        self.index["memories"].append({
            "id": memory.id,
            "type": memory.memory_type,
            "tags": tags,
            "source": source_task,
            "created": memory.created,
            "file": memory_file
        })
        self._save_index()

        return memory

    def get_memories(self, memory_type: Optional[MemoryType] = None,
                     tags: Optional[List[str]] = None) -> List[Memory]:
        """Retrieve memories by type and/or tags.

        Args:
            memory_type: Filter by type
            tags: Filter by tags (ANY match)

        Returns:
            List of matching memories
        """
        memories = []

        for entry in self.index["memories"]:
            # Filter by type
            if memory_type and entry["type"] != memory_type.value:
                continue

            # Filter by tags
            if tags and not any(t in entry["tags"] for t in tags):
                continue

            # Load memory file
            memory_file = entry.get("file") or os.path.join(
                self.memories_dir, f"{entry['id']}.md"
            )

            if os.path.exists(memory_file):
                with open(memory_file, 'r') as f:
                    content = f.read()

                # Parse memory from markdown
                memory = self._parse_memory_markdown(content, entry)
                memories.append(memory)

        # Sort by recency
        memories.sort(key=lambda m: m.created, reverse=True)
        return memories

    def get_memories_for_prompt(self, query: Optional[str] = None,
                                max_tokens: int = 2000) -> str:
        """Get formatted memories for agent prompt.

        Args:
            query: Search query (matches tags and content)
            max_tokens: Token budget for memories

        Returns:
            Formatted markdown string for prompt injection
        """
        memories = self.get_memories()

        # Filter by query if provided
        if query:
            query_lower = query.lower()
            memories = [
                m for m in memories
                if query_lower in m.content.lower()
                or any(query_lower in t.lower() for t in m.tags)
            ]

        # Build prompt section within token budget
        # Rough estimate: 4 chars ≈ 1 token
        max_chars = max_tokens * 4

        sections = []
        current_chars = 0

        # Group by type
        by_type = {}
        for m in memories:
            by_type.setdefault(m.memory_type, []).append(m)

        for memory_type in ["pattern", "decision", "fix", "context"]:
            type_memories = by_type.get(memory_type, [])
            if not type_memories:
                continue

            section = f"\n## {memory_type.upper()}S\n\n"
            for m in type_memories[:3]:  # Top 3 per type
                entry = f"- **{m.id}**: {m.content[:200]}\n"
                if current_chars + len(section) + len(entry) > max_chars:
                    break
                section += entry

            sections.append(section)
            current_chars += len(section)

        if not sections:
            return ""

        return "## MEMORIES FROM PREVIOUS RUNS\n" + "".join(sections)

    def _parse_memory_markdown(self, content: str, entry: Dict) -> Memory:
        """Parse memory from markdown file."""
        lines = content.split('\n')

        # Extract content after frontmatter
        content_start = 0
        for i, line in enumerate(lines):
            if line.startswith('**Type:**'):
                content_start = i + 1
                break

        memory_content = '\n'.join(lines[content_start:]).strip()
        # Remove separator
        memory_content = memory_content.rstrip('-').strip()

        return Memory(
            id=entry["id"],
            memory_type=entry["type"],
            content=memory_content,
            tags=entry.get("tags", []),
            source_task=entry.get("source", ""),
            created=entry.get("created", "")
        )

    def consolidate_memories(self):
        """Consolidate old memories into summary."""
        # TODO: Use LLM to summarize old memories
        pass


# Integration with executor
class MemoryMixin:
    """Mixin to add memory management to executor."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.memory_manager = MemoryManager(".autonomous/memories/")

    def build_prompt_with_memories(self, base_prompt: str,
                                   task_context: str) -> str:
        """Build prompt with relevant memories."""
        memories = self.memory_manager.get_memories_for_prompt(
            query=task_context,
            max_tokens=2000
        )

        if memories:
            return f"{base_prompt}\n\n{memories}\n\n---\n\n"
        return base_prompt

    def extract_and_store_memories(self, run_folder: str, task_id: str):
        """Extract memories from completed run."""
        learnings_file = os.path.join(run_folder, "LEARNINGS.md")

        if not os.path.exists(learnings_file):
            return

        with open(learnings_file, 'r') as f:
            content = f.read()

        # Parse learnings and convert to structured memories
        # This could be enhanced with LLM-based extraction

        # For now, store the whole learnings as context
        self.memory_manager.add_memory(
            memory_type=MemoryType.CONTEXT,
            content=content,
            tags=["learnings", task_id],
            source_task=task_id
        )
```

### Integration Steps

1. **Copy file** to `bin/ralf-executor/memory_manager.py`
2. **Modify** prompt building to include `get_memories_for_prompt()`
3. **After** task completion, call `extract_and_store_memories()`
4. **Update** agent prompts to reference memories

---

## Part 3: Agent Specialization (Hats)

### Source: mikeyobrien/ralph-orchestrator

**What it does:** Defines specialized agent personas with triggers and instructions.

**Why BB5 needs it:** Your agents have roles but no formal trigger system or standardized instructions.

### Implementation

#### File: `.claude/agents/hat-definitions.yaml`

```yaml
# BB5 Agent Hat Definitions
# Adapted from mikeyobrien/ralph-orchestrator

hats:
  context-collector:
    name: "Context Collector"
    description: "Gathers comprehensive BB5 state before task execution"
    triggers: ["task.started", "context.needed"]
    backend: "claude-opus-4-6"
    timeout_minutes: 10
    instructions: |
      ## Context Collector Role

      Your job is to gather all relevant context for the task.

      ### Actions
      1. Read task definition
      2. Examine relevant codebase files
      3. Check recent commits and changes
      4. Review related tasks and their outcomes
      5. Identify potential risks or blockers

      ### Output
      Write comprehensive context summary to:
      - `CONTEXT.md` in the run folder

      ### Trigger Next
      Emit event: `context.collected`

  planner:
    name: "Planner"
    description: "Creates implementation plans from context"
    triggers: ["context.collected"]
    backend: "claude-opus-4-6"
    timeout_minutes: 15
    instructions: |
      ## Planner Role

      Create a detailed implementation plan.

      ### Actions
      1. Read context from Context Collector
      2. Break task into subtasks
      3. Identify dependencies
      4. Estimate effort
      5. Define acceptance criteria

      ### Output
      Write plan to:
      - `PLAN.md` in the run folder

      ### Trigger Next
      Emit event: `plan.created`

  executor:
    name: "Executor"
    description: "Implements the solution"
    triggers: ["plan.approved", "task.direct"]
    backend: "claude-opus-4-6"
    timeout_minutes: 30
    instructions: |
      ## Executor Role

      Implement the solution according to the plan.

      ### Actions
      1. Read the plan
      2. Implement changes
      3. Run tests
      4. Update documentation

      ### Output
      Write results to:
      - `RESULTS.md`
      - `CHANGES.md`

      ### Trigger Next
      Emit event: `execution.completed`

  verifier:
    name: "Verifier"
    description: "Validates implementation against requirements"
    triggers: ["execution.completed"]
    backend: "claude-opus-4-6"
    timeout_minutes: 10
    instructions: |
      ## Verifier Role

      Validate that the implementation meets requirements.

      ### Actions
      1. Review changes
      2. Run tests
      3. Check acceptance criteria
      4. Identify any issues

      ### Output
      Write verification to:
      - `VERIFICATION.md`

      ### Trigger Next
      Emit event: `verification.passed` or `verification.failed`

  scribe:
    name: "Scribe"
    description: "Documents thinking, decisions, and learnings"
    triggers: ["*"]  # All events
    backend: "claude-opus-4-6"
    timeout_minutes: 5
    instructions: |
      ## Scribe Role

      Document the process for future reference.

      ### Actions
      1. Monitor all events
      2. Extract key decisions
      3. Document learnings
      4. Update memories

      ### Output
      Write to:
      - `THOUGHTS.md`
      - `DECISIONS.md`
      - `LEARNINGS.md`

# Event routing configuration
event_routing:
  default_handler: "executor"  # If no hat matches, use executor
  fallback_to_ralph: true      # If hat fails, try executor
```

#### File: `bin/ralf-executor/hat_manager.py`

```python
#!/usr/bin/env python3
"""Hat-based agent specialization for BB5.

Adapted from mikeyobrien/ralph-orchestrator hat system.
"""

import yaml
import os
from typing import List, Dict, Optional


class Hat:
    """Single hat definition."""

    def __init__(self, name: str, config: Dict):
        self.name = name
        self.config = config
        self.triggers = config.get('triggers', [])
        self.instructions = config.get('instructions', '')
        self.backend = config.get('backend', 'claude-opus-4-6')
        self.timeout = config.get('timeout_minutes', 15)

    def matches_trigger(self, event_type: str) -> bool:
        """Check if this hat handles the event type."""
        return event_type in self.triggers or '*' in self.triggers

    def build_prompt(self, base_prompt: str, context: Dict) -> str:
        """Build specialized prompt for this hat."""
        return f"""{self.instructions}

## Context

{context.get('description', '')}

## Task

{base_prompt}

## Instructions

Focus ONLY on your specific role. Do not perform other hats' responsibilities.
When complete, document your work and emit the appropriate event.
"""


class HatManager:
    """Manages hat definitions and routing.

    Usage:
        hm = HatManager(".claude/agents/hat-definitions.yaml")

        # Find hat for event
        hat = hm.get_hat_for_event("task.started")
        if hat:
            prompt = hat.build_prompt(base_prompt, context)
    """

    def __init__(self, config_file: str):
        self.config_file = config_file
        self.hats: Dict[str, Hat] = {}
        self.routing_config = {}
        self._load_config()

    def _load_config(self):
        """Load hat definitions from YAML."""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Hat config not found: {self.config_file}")

        with open(self.config_file, 'r') as f:
            config = yaml.safe_load(f)

        for name, hat_config in config.get('hats', {}).items():
            self.hats[name] = Hat(name, hat_config)

        self.routing_config = config.get('event_routing', {})

    def get_hat_for_event(self, event_type: str) -> Optional[Hat]:
        """Find hat that handles this event type."""
        for hat in self.hats.values():
            if hat.matches_trigger(event_type):
                return hat
        return None

    def get_all_hats(self) -> List[Hat]:
        """Get all hat definitions."""
        return list(self.hats.values())

    def get_hat(self, name: str) -> Optional[Hat]:
        """Get specific hat by name."""
        return self.hats.get(name)
```

---

## Part 4: Event Pub/Sub System

### Source: mikeyobrien/ralph-orchestrator

**What it does:** Decoupled communication via events instead of direct file manipulation.

**Why BB5 needs it:** Current queue.yaml manipulation is fragile. Events enable better orchestration.

### Implementation

#### File: `bin/ralf-executor/event_bus.py`

```python
#!/usr/bin/env python3
"""Event pub/sub system for BB5 agent communication.

Adapted from mikeyobrien/ralph-orchestrator event system.
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Callable, Optional
from dataclasses import dataclass, asdict
from threading import Lock


@dataclass
class Event:
    """Single event."""
    type: str
    payload: Dict
    timestamp: str
    source: str
    id: str


class EventBus:
    """Pub/sub event bus for agent communication.

    Usage:
        bus = EventBus(".autonomous/events/")

        # Subscribe to events
        bus.subscribe("task.started", on_task_started)
        bus.subscribe("execution.completed", on_execution_completed)

        # Publish events
        bus.publish("task.started", {"task_id": "TASK-001"})
    """

    def __init__(self, events_dir: str):
        self.events_dir = events_dir
        self.subscribers: Dict[str, List[Callable]] = {}
        self.events_file = os.path.join(events_dir, "events.jsonl")
        self.lock = Lock()

        os.makedirs(events_dir, exist_ok=True)

    def subscribe(self, event_type: str, handler: Callable):
        """Subscribe to an event type.

        Args:
            event_type: Type of event to subscribe to
            handler: Function to call when event occurs
        """
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)

    def publish(self, event_type: str, payload: Dict, source: str = "system"):
        """Publish an event.

        Args:
            event_type: Type of event
            payload: Event data
            source: Component that generated the event
        """
        event = Event(
            id=f"evt-{int(time.time())}-{hash(str(payload)) % 10000:04d}",
            type=event_type,
            payload=payload,
            timestamp=datetime.now().isoformat(),
            source=source
        )

        # Persist to JSONL
        with self.lock:
            with open(self.events_file, 'a') as f:
                f.write(json.dumps(asdict(event)) + '\n')

        # Notify subscribers
        for handler in self.subscribers.get(event_type, []):
            try:
                handler(event)
            except Exception as e:
                print(f"Error in event handler: {e}")

        # Notify wildcard subscribers
        for handler in self.subscribers.get('*', []):
            try:
                handler(event)
            except Exception as e:
                print(f"Error in wildcard handler: {e}")

    def get_events(self, event_type: Optional[str] = None,
                   since: Optional[str] = None) -> List[Event]:
        """Retrieve events from log.

        Args:
            event_type: Filter by type
            since: ISO timestamp to filter from

        Returns:
            List of events
        """
        events = []

        if not os.path.exists(self.events_file):
            return events

        with open(self.events_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    data = json.loads(line)

                    # Filter by type
                    if event_type and data.get('type') != event_type:
                        continue

                    # Filter by time
                    if since and data.get('timestamp', '') < since:
                        continue

                    events.append(Event(**data))
                except json.JSONDecodeError:
                    continue

        return events


# Integration with existing queue system
class QueueEventAdapter:
    """Adapts existing queue.yaml to event system."""

    def __init__(self, event_bus: EventBus, queue_file: str):
        self.event_bus = event_bus
        self.queue_file = queue_file

    def on_task_added(self, task_id: str):
        """Called when task is added to queue."""
        self.event_bus.publish("task.added", {
            "task_id": task_id,
            "queue_file": self.queue_file
        })

    def on_task_started(self, task_id: str):
        """Called when task execution starts."""
        self.event_bus.publish("task.started", {
            "task_id": task_id
        })

    def on_task_completed(self, task_id: str, status: str):
        """Called when task completes."""
        self.event_bus.publish("task.completed", {
            "task_id": task_id,
            "status": status
        })
```

---

## Integration Checklist

### Week 1: Circuit Breaker
- [ ] Copy `circuit_breaker.py` to `bin/ralf-executor/`
- [ ] Modify `executor.py` to use `CircuitBreakerMixin`
- [ ] Add circuit breaker status to dashboard
- [ ] Write tests
- [ ] Document usage

### Week 2: Memory System
- [ ] Copy `memory_manager.py` to `bin/ralf-executor/`
- [ ] Modify prompt building to include memories
- [ ] Add memory extraction after task completion
- [ ] Create memories directory structure
- [ ] Test memory retrieval

### Week 3-4: Agent Hats
- [ ] Create `hat-definitions.yaml`
- [ ] Copy `hat_manager.py` to `bin/ralf-executor/`
- [ ] Modify agent spawner to use hats
- [ ] Update agent prompts with hat instructions
- [ ] Test hat routing

### Week 5-6: Event System
- [ ] Copy `event_bus.py` to `bin/ralf-executor/`
- [ ] Create `QueueEventAdapter`
- [ ] Replace direct queue manipulation with events
- [ ] Test event flow
- [ ] Add event monitoring

---

## Testing Strategy

### Unit Tests
```python
# test_integration.py
import unittest
from circuit_breaker import CircuitBreaker
from memory_manager import MemoryManager, MemoryType
from hat_manager import HatManager
from event_bus import EventBus

class TestIntegration(unittest.TestCase):
    def test_circuit_breaker_opens(self):
        cb = CircuitBreaker("/tmp/test_cb.json")
        # Test failure counting
        # Test state transitions

    def test_memory_storage(self):
        mm = MemoryManager("/tmp/test_memories/")
        # Test add/get
        # Test token budget

    def test_hat_routing(self):
        hm = HatManager("test-hats.yaml")
        # Test trigger matching
        # Test prompt building

    def test_event_pub_sub(self):
        bus = EventBus("/tmp/test_events/")
        # Test subscribe/publish
        # Test persistence
```

### Integration Tests
1. Run full task with circuit breaker
2. Verify memory extraction and retrieval
3. Test hat-based agent routing
4. Verify event flow end-to-end

---

## Migration Path

### Phase 1: Add New Components (Parallel)
- New files don't affect existing code
- Feature flags control usage
- Gradual adoption

### Phase 2: Replace Gradually
- Replace retry logic with circuit breaker
- Enhance existing memory with structured system
- Add hat layer on top of existing agents
- Use events alongside queue.yaml

### Phase 3: Remove Legacy
- Remove old retry logic
- Deprecate unstructured learnings
- Remove direct queue manipulation

---

## Success Metrics

- [ ] Zero runaway loops (circuit breaker catches all)
- [ ] Memories retrieved in 90%+ of tasks
- [ ] Agent specialization reduces context confusion
- [ ] Event system handles 100+ events/day
- [ ] All tests pass
- [ ] Documentation complete

---

*Integration guide version 1.0*
*For questions, see individual framework analysis documents*
