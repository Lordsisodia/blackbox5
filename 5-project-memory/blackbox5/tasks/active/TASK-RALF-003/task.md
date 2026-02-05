# TASK-RALF-003: Decouple RALF from Skill System

**Status:** pending
**Priority:** HIGH
**Parent:** Issue #4 - RALF Knows Project Structure

## Objective
Make RALF's skill system optional and decoupled from BlackBox5-specific implementation.

## Current Problems
1. All scout agents assume `operations/skill-*.yaml` files exist
2. Executor has hardcoded skill-related task IDs (TASK-SKIL-005, TASK-SKIL-008)
3. Verifier validates BB5-specific skill YAML structure
4. `collect-skill-metrics.py` has absolute hardcoded path

## Solution Approach

### Phase 1: Extract Skill Interface
Create `2-engine/.autonomous/lib/skill_provider.py`:
```python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class SkillProvider(ABC):
    @abstractmethod
    def get_skill_metrics(self) -> Dict:
        """Return skill effectiveness metrics."""
        pass

    @abstractmethod
    def get_skill_usage(self) -> Dict:
        """Return skill usage history."""
        pass

    @abstractmethod
    def select_skill(self, task_description: str) -> Optional[str]:
        """Select appropriate skill for task."""
        pass

    @abstractmethod
    def is_enabled(self) -> bool:
        """Check if skill system is available."""
        pass

class BlackBox5SkillProvider(SkillProvider):
    """BB5-specific skill provider implementation."""
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir

    def is_enabled(self) -> bool:
        return (self.project_dir / "operations" / "skill-selection.yaml").exists()
    # ... implementations

class NullSkillProvider(SkillProvider):
    """No-op provider when skills disabled."""
    def is_enabled(self) -> bool:
        return False
    # ... no-op implementations
```

### Phase 2: Update Agents
- Modify scout agents to check `skill_provider.is_enabled()` before reading skill files
- Modify executor to use capability-based routing instead of hardcoded task IDs
- Modify verifier to validate against interface, not specific YAML structure

### Phase 3: Fix Absolute Path Bug
Fix `collect-skill-metrics.py` line 11:
```python
# BEFORE (BROKEN)
metrics_path = Path('/Users/shaansisodia/.blackbox5/.../skill-metrics.yaml')

# AFTER
metrics_path = PROJECT_DIR / "operations" / "skill-metrics.yaml"
```

## Success Criteria
- [ ] Create `SkillProvider` abstract interface
- [ ] Create `BlackBox5SkillProvider` implementation
- [ ] Create `NullSkillProvider` for projects without skills
- [ ] Update all scout agents to use skill provider
- [ ] Update executor to use capability routing
- [ ] Update verifier to use generic validation
- [ ] Fix absolute path in `collect-skill-metrics.py`
- [ ] RALF works gracefully when skill system disabled

## Rollback Strategy
Keep BB5-specific code paths as fallback.
