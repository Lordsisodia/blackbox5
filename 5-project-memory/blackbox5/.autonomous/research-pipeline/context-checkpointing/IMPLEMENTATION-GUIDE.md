# Context Checkpointing - Implementation Guide

**Status:** Ready for Implementation
**Estimated Effort:** 2 weeks (1 dev)
**MVP:** 1 day

---

## Quick Start (MVP)

### Step 1: Create Core Module (30 min)

```python
# 2-engine/helpers/legacy/context_checkpoint.py

#!/usr/bin/env python3
"""Context Checkpointing System for RALF."""

import yaml
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class CheckpointConfig:
    route_name: str
    agent_type: str
    project: str = "blackbox5"
    checkpoint_interval: int = 50000

    @property
    def context_dir(self) -> Path:
        return Path.home() / f".blackbox5/5-project-memory/{self.project}/.autonomous/context/routes"

    @property
    def context_file(self) -> Path:
        return self.context_dir / f"{self.route_name}.md"


@dataclass
class CheckpointData:
    checkpoint_id: str
    timestamp: str
    tokens_consumed: int
    summary: str
    key_events: List[str]
    decisions_made: List[Dict]
    files_modified: List[str]


class ContextCheckpoint:
    """Manages context checkpointing for long-running tasks."""

    def __init__(self, config: CheckpointConfig):
        self.config = config
        self.context_file = config.context_file

    def should_checkpoint(self, current_tokens: int) -> bool:
        """Check if checkpoint should be created."""
        context = self._load_context()
        if not context:
            return True

        last_tokens = context.get('context_checkpoint', {}).get('tokens_at_checkpoint', 0)
        return (current_tokens - last_tokens) >= self.config.checkpoint_interval

    def create_checkpoint(
        self,
        current_tokens: int,
        thoughts_file: Optional[Path] = None,
        session_data: Optional[Dict] = None
    ) -> Path:
        """Create a new checkpoint."""
        existing = self._load_context()

        checkpoint_data = CheckpointData(
            checkpoint_id=self._generate_id(),
            timestamp=datetime.now(timezone.utc).isoformat(),
            tokens_consumed=current_tokens,
            summary=self._summarize(thoughts_file),
            key_events=self._extract_events(session_data),
            decisions_made=[],
            files_modified=session_data.get('files_modified', []) if session_data else []
        )

        if existing:
            context = self._update_existing(existing, checkpoint_data, current_tokens)
        else:
            context = self._create_initial(checkpoint_data, current_tokens)

        self._write_context(context)
        return self.context_file

    def _generate_id(self) -> str:
        return f"cp-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"

    def _summarize(self, thoughts_file: Optional[Path]) -> str:
        if not thoughts_file or not thoughts_file.exists():
            return "No thoughts available"
        # MVP: Simple truncation
        content = thoughts_file.read_text()
        return content[-5000:] if len(content) > 5000 else content

    def _extract_events(self, session_data: Optional[Dict]) -> List[str]:
        if not session_data:
            return []
        files = session_data.get('files_modified', [])
        return [f"Modified {len(files)} files"] if files else []

    def _load_context(self) -> Optional[Dict]:
        if not self.context_file.exists():
            return None
        content = self.context_file.read_text()
        if not content.startswith('---'):
            return None
        parts = content.split('---', 2)
        return yaml.safe_load(parts[1]) if len(parts) >= 3 else None

    def _create_initial(self, cp: CheckpointData, tokens: int) -> Dict:
        return {
            'context_checkpoint': {
                'version': '1.0.0',
                'route': self.config.route_name,
                'agent_type': self.config.agent_type,
                'created': cp.timestamp,
                'last_checkpoint': cp.timestamp,
                'checkpoint_count': 1,
                'tokens_at_checkpoint': tokens,
                'total_tokens_consumed': tokens,
            },
            'decisions': cp.decisions_made,
            'active_work': {
                'current_task': None,
                'current_phase': None,
                'work_status': 'in_progress',
            },
            'checkpoint_history': [{
                'checkpoint_id': cp.checkpoint_id,
                'timestamp': cp.timestamp,
                'tokens': cp.tokens_consumed,
                'summary_ref': cp.summary[:200],
                'key_events': cp.key_events
            }]
        }

    def _update_existing(self, existing: Dict, cp: CheckpointData, tokens: int) -> Dict:
        existing['context_checkpoint']['last_checkpoint'] = cp.timestamp
        existing['context_checkpoint']['checkpoint_count'] += 1
        existing['context_checkpoint']['tokens_at_checkpoint'] = tokens
        existing['context_checkpoint']['total_tokens_consumed'] = tokens

        existing['checkpoint_history'].append({
            'checkpoint_id': cp.checkpoint_id,
            'timestamp': cp.timestamp,
            'tokens': cp.tokens_consumed,
            'summary_ref': cp.summary[:200],
            'key_events': cp.key_events
        })

        return existing

    def _write_context(self, context: Dict):
        self.config.context_dir.mkdir(parents=True, exist_ok=True)

        yaml_content = yaml.dump(context, default_flow_style=False, sort_keys=False)

        full_content = f"""---
{yaml_content}---

## Checkpoint History

{self._build_history(context)}

---
*Auto-generated context checkpoint*
"""

        temp_file = self.context_file.with_suffix('.tmp')
        temp_file.write_text(full_content)
        temp_file.rename(self.context_file)

    def _build_history(self, context: Dict) -> str:
        lines = []
        for cp in reversed(context.get('checkpoint_history', [])):
            lines.append(f"### {cp.get('checkpoint_id', 'unknown')}")
            lines.append(f"- Tokens: {cp.get('tokens', 0)}")
            lines.append(f"- Summary: {cp.get('summary_ref', 'N/A')}")
            lines.append("")
        return "\n".join(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["init", "check", "create"])
    parser.add_argument("--route", required=True)
    parser.add_argument("--agent-type", default="executor")
    parser.add_argument("--tokens", type=int)
    parser.add_argument("--thoughts", type=Path)

    args = parser.parse_args()

    config = CheckpointConfig(route_name=args.route, agent_type=args.agent_type)
    checkpoint = ContextCheckpoint(config)

    if args.command == "init":
        checkpoint.create_checkpoint(0)
        print(f"Initialized context for: {args.route}")

    elif args.command == "check":
        should = checkpoint.should_checkpoint(args.tokens)
        print(f"Should checkpoint: {should}")

    elif args.command == "create":
        path = checkpoint.create_checkpoint(args.tokens, args.thoughts)
        print(f"Created checkpoint: {path}")
```

### Step 2: Test MVP (15 min)

```bash
# Create test route
cd ~/.blackbox5/5-project-memory/blackbox5

# Initialize context
python3 2-engine/helpers/legacy/context_checkpoint.py init \
    --route test-route \
    --agent-type executor

# Verify file created
cat .autonomous/context/routes/test-route.md

# Simulate checkpoint at 50k tokens
python3 2-engine/helpers/legacy/context_checkpoint.py create \
    --route test-route \
    --tokens 50000 \
    --thoughts .autonomous/runs/run-*/THOUGHTS.md

# Check if another checkpoint needed (should be False)
python3 2-engine/helpers/legacy/context_checkpoint.py check \
    --route test-route \
    --tokens 52000
```

### Step 3: Manual Integration Test (15 min)

1. Start a RALF task
2. Run for ~50k tokens
3. Verify checkpoint created automatically
4. Start new RALF instance
5. Load context via reader
6. Verify decisions preserved

---

## Full Implementation Tasks

### Task 1: Core Data Model ✅ (MVP Complete)

**Files:**
- `2-engine/helpers/legacy/context_checkpoint.py`

**Requirements:**
- [x] Checkpoint dataclass
- [x] File I/O with YAML frontmatter
- [x] Basic summarization
- [x] CLI interface

### Task 2: Context Reader

**File:** `2-engine/helpers/legacy/context_reader.py`

**Code:**
```python
#!/usr/bin/env python3
"""Context Reader for accessing checkpointed context."""

import yaml
from pathlib import Path
from typing import Dict, Optional, List


class ContextReader:
    """Reads context checkpoint files on demand."""

    def __init__(self, project: str = "blackbox5"):
        self.context_dir = (
            Path.home() / ".blackbox5/5-project-memory"
            / project / ".autonomous/context/routes"
        )

    def list_routes(self) -> List[str]:
        """List all available route contexts."""
        if not self.context_dir.exists():
            return []
        return [f.stem for f in self.context_dir.glob("*.md")]

    def get_context(self, route: str, max_history: int = 3) -> Optional[Dict]:
        """Get context for a specific route."""
        context_file = self.context_dir / f"{route}.md"
        if not context_file.exists():
            return None

        content = context_file.read_text()
        if not content.startswith('---'):
            return None

        parts = content.split('---', 2)
        return yaml.safe_load(parts[1]) if len(parts) >= 3 else None

    def get_summary(self, route: str) -> str:
        """Get human-readable summary."""
        context = self.get_context(route)
        if not context:
            return f"No context found for route: {route}"

        cp = context.get('context_checkpoint', {})
        lines = [
            f"Route: {cp.get('route', 'unknown')}",
            f"Agent: {cp.get('agent_type', 'unknown')}",
            f"Checkpoints: {cp.get('checkpoint_count', 0)}",
            f"Total Tokens: {cp.get('total_tokens_consumed', 0):,}",
        ]

        active = context.get('active_work', {})
        lines.extend([
            "",
            "## Active Work",
            f"Task: {active.get('current_task', 'None')}",
            f"Phase: {active.get('current_phase', 'unknown')}",
            f"Status: {active.get('work_status', 'unknown')}",
        ])

        decisions = context.get('decisions', [])
        if decisions:
            lines.extend(["", "## Recent Decisions"])
            for d in decisions[-3:]:
                lines.append(f"- {d.get('id', 'DEC-?')}: {d.get('decision', 'Untitled')}")

        return "\n".join(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["list", "read"])
    parser.add_argument("--route")

    args = parser.parse_args()

    reader = ContextReader()

    if args.command == "list":
        routes = reader.list_routes()
        print("Available contexts:")
        for r in routes:
            print(f"  - {r}")

    elif args.command == "read":
        if not args.route:
            print("Error: --route required")
        else:
            print(reader.get_summary(args.route))
```

### Task 3: Integrate with context_budget.py

**Modify:** `2-engine/helpers/legacy/context_budget.py`

**Add to ThresholdAction:**
```python
# Add checkpoint action
def _trigger_checkpoint(self):
    """Trigger context checkpoint creation."""
    import subprocess
    import os

    route = os.environ.get("BB5_ROUTE", "default")
    run_dir = self.run_dir or Path.cwd()

    result = subprocess.run([
        sys.executable,
        "-m", "context_checkpoint",
        "create",
        "--route", route,
        "--tokens", str(self.current_tokens),
        "--thoughts", str(run_dir / "THOUGHTS.md")
    ], capture_output=True, text=True)

    if result.returncode == 0:
        self.logger.info(f"Context checkpoint created: {result.stdout.strip()}")
    else:
        self.logger.error(f"Checkpoint failed: {result.stderr}")
```

**Add to thresholds:**
```python
# In __init__, add checkpoint threshold
self.thresholds.append(Threshold(
    name="checkpoint",
    percentage=0.35,  # 35% = ~70k tokens for 200k context
    action=self.actions["checkpoint"]
))
```

### Task 4: RALF Integration

**Modify:** `2-engine/instructions/ralf.md`

**Add section:**
```markdown
## Context Checkpointing

When working on long-running tasks, context checkpoints preserve key decisions and work state.

### Checking for Context

At session start, check if a context checkpoint exists:

```bash
# List available contexts
python3 2-engine/helpers/legacy/context_reader.py list

# Read specific context
python3 2-engine/helpers/legacy/context_reader.py read --route {route-name}
```

### When to Load Context

Load context checkpoint when:
- Resuming work on a task after interruption
- Need to understand previous decisions
- Context window is filling up and you need historical reference

### Access Pattern

**DO NOT auto-inject context.** Instead:

1. Check if checkpoint exists: `context_reader.py list`
2. If relevant, load summary: `context_reader.py read --route {name}`
3. Reference specific decisions or work state as needed
4. Only load full context if necessary

### Creating Checkpoints

Checkpoints are created automatically at ~50k token intervals.

To create manually:
```bash
python3 2-engine/helpers/legacy/context_checkpoint.py create \
    --route {route-name} \
    --tokens {current-count} \
    --thoughts THOUGHTS.md
```
```

### Task 5: Session Tracker Integration

**Modify:** `2-engine/helpers/legacy/session_tracker.py`

**Add method:**
```python
def record_checkpoint(self, checkpoint_id: str, checkpoint_path: str):
    """Record checkpoint in run tracking."""
    self.run_data['checkpoint'] = {
        'id': checkpoint_id,
        'path': checkpoint_path,
        'timestamp': datetime.now(timezone.utc).isoformat()
    }
    self._save_tracking()
    self.logger.info(f"Recorded checkpoint: {checkpoint_id}")
```

### Task 6: CLI Commands

**Create:** `2-engine/interface/cli/commands/context.py`

```python
"""Context checkpoint CLI commands."""

import click
from pathlib import Path

from ...helpers.legacy.context_reader import ContextReader
from ...helpers.legacy.context_checkpoint import ContextCheckpoint, CheckpointConfig


@click.group()
def context():
    """Manage context checkpoints."""
    pass


@context.command()
@click.option('--project', default='blackbox5')
def list(project):
    """List available context checkpoints."""
    reader = ContextReader(project)
    routes = reader.list_routes()

    if not routes:
        click.echo("No context checkpoints found.")
        return

    click.echo("Available context checkpoints:")
    for route in routes:
        click.echo(f"  - {route}")


@context.command()
@click.option('--route', required=True)
@click.option('--project', default='blackbox5')
def show(route, project):
    """Show context checkpoint details."""
    reader = ContextReader(project)
    summary = reader.get_summary(route)
    click.echo(summary)


@context.command()
@click.option('--route', required=True)
@click.option('--agent-type', default='executor')
@click.option('--project', default='blackbox5')
def init(route, agent_type, project):
    """Initialize context checkpoint for a route."""
    config = CheckpointConfig(
        route_name=route,
        agent_type=agent_type,
        project=project
    )
    checkpoint = ContextCheckpoint(config)
    path = checkpoint.create_checkpoint(0)
    click.echo(f"Initialized context checkpoint: {path}")


@context.command()
@click.option('--route', required=True)
@click.option('--tokens', type=int, required=True)
@click.option('--thoughts', type=click.Path(exists=True))
@click.option('--agent-type', default='executor')
@click.option('--project', default='blackbox5')
def create(route, tokens, thoughts, agent_type, project):
    """Create a context checkpoint."""
    config = CheckpointConfig(
        route_name=route,
        agent_type=agent_type,
        project=project
    )
    checkpoint = ContextCheckpoint(config)

    thoughts_path = Path(thoughts) if thoughts else None
    path = checkpoint.create_checkpoint(tokens, thoughts_path)
    click.echo(f"Created checkpoint: {path}")
```

---

## Testing Strategy

### Unit Tests

```python
# tests/test_context_checkpoint.py

import pytest
from pathlib import Path
from datetime import datetime, timezone

from context_checkpoint import ContextCheckpoint, CheckpointConfig, CheckpointData


class TestContextCheckpoint:
    def test_create_initial_checkpoint(self, tmp_path):
        config = CheckpointConfig(
            route_name="test-route",
            agent_type="executor"
        )
        config.context_dir = tmp_path

        checkpoint = ContextCheckpoint(config)
        path = checkpoint.create_checkpoint(0)

        assert path.exists()
        assert "test-route" in path.name

    def test_should_checkpoint_first_time(self, tmp_path):
        config = CheckpointConfig(route_name="test", agent_type="executor")
        config.context_dir = tmp_path

        checkpoint = ContextCheckpoint(config)
        assert checkpoint.should_checkpoint(0) is True

    def test_should_checkpoint_after_interval(self, tmp_path):
        config = CheckpointConfig(route_name="test", agent_type="executor")
        config.context_dir = tmp_path

        checkpoint = ContextCheckpoint(config)
        checkpoint.create_checkpoint(0)  # Initial

        # Should not checkpoint at 40k
        assert checkpoint.should_checkpoint(40000) is False

        # Should checkpoint at 50k
        assert checkpoint.should_checkpoint(50000) is True
```

### Integration Tests

1. **End-to-end flow:**
   - Start RALF task
   - Verify checkpoint created at 50k
   - Start new RALF instance
   - Load context
   - Verify decisions preserved

2. **Concurrent access:**
   - Two RALF instances on same route
   - Verify no corruption

3. **Recovery:**
   - Simulate crash mid-checkpoint
   - Verify atomic write prevents corruption

---

## Deployment Checklist

- [ ] Core module implemented
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Documentation updated
- [ ] RALF instructions updated
- [ ] CLI commands working
- [ ] Hook scripts installed
- [ ] Migration script tested (if applicable)
- [ ] Rollback plan documented

---

## Rollback Plan

If issues arise:

1. **Disable checkpointing:**
   ```bash
   export BB5_DISABLE_CHECKPOINTS=1
   ```

2. **Revert to timeline-memory:**
   ```bash
   # Use existing timeline-memory.md files
   cp .autonomous/research-pipeline/agents/{agent}/timeline-memory.md \
      .autonomous/context/routes/{route}.md
   ```

3. **Remove checkpoint files:**
   ```bash
   rm -rf .autonomous/context/routes/
   ```

---

## Success Criteria

| Criteria | Target | Test |
|----------|--------|------|
| Checkpoint creation | 100% at 50k | Automated test |
| Context retrieval | <100ms | Benchmark |
| File size | <100KB per checkpoint | Monitor |
| Decision preservation | 100% | Unit test |
| Token overhead | <5% | Profiling |

---

*Implementation guide generated from analysis*
*Ready for development*
