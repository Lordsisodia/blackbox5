# PLAN.md: Decouple RALF from Skill System

**Task:** TASK-RALF-003 - Decouple RALF from Skill System
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 3-4 days
**Parent:** Issue #4 - RALF Knows Project Structure
**Importance:** 90 (Critical)

---

## 1. First Principles Analysis

### Why Decouple RALF from the Skill System?

1. **Reusability**: RALF should work with any project structure, not just BlackBox5
2. **Modularity**: Skills should be an optional feature, not a hard dependency
3. **Testing**: Decoupled components can be tested independently
4. **Flexibility**: Projects can use RALF without adopting the full BB5 skill framework
5. **Maintainability**: Changes to skills don't require changes to core RALF

### What Happens Without Decoupling?

- **BB5 Lock-in**: RALF cannot be used in non-BB5 projects
- **Broken Assumptions**: Agents fail when `operations/skill-*.yaml` files don't exist
- **Hardcoded Logic**: Skill-related task IDs (TASK-SKIL-*) break in other contexts
- **Validation Failures**: Verifier expects BB5-specific YAML structure
- **Path Issues**: Absolute hardcoded paths break on different systems

### How Should Decoupling Work?

1. **Abstract Interface**: Define `SkillProvider` interface that RALF uses
2. **Multiple Implementations**: BB5-specific provider and null provider
3. **Capability-Based Routing**: Route tasks by capability, not hardcoded IDs
4. **Graceful Degradation**: Continue operating when skills are unavailable
5. **Configuration-Driven**: Enable/disable skills via configuration

---

## 2. Current State Assessment

### Current Hardcoded Dependencies

| Component | Location | Issue |
|-----------|----------|-------|
| Scout Agents | `2-engine/.autonomous/bin/scout*.py` | Assume `operations/skill-*.yaml` exists |
| Executor | `2-engine/.autonomous/bin/executor*.py` | Hardcoded skill task IDs |
| Verifier | `2-engine/.autonomous/bin/verifier*.py` | Validates BB5-specific YAML structure |
| Metrics Collector | `bin/collect-skill-metrics.py` | Absolute hardcoded path |

### Skill Files Assumed to Exist

```
operations/
├── skill-selection.yaml      # Skill selection rules
├── skill-metrics.yaml        # Skill effectiveness metrics
├── skill-usage.yaml          # Skill usage history
└── ...
```

### Current Problems by Component

**1. Scout Agents:**
```python
# Problem: No check if skill files exist
skill_selection = yaml.safe_load(
    open("operations/skill-selection.yaml")  # Crashes if missing
)
```

**2. Executor:**
```python
# Problem: Hardcoded task IDs
if task_id.startswith("TASK-SKIL-"):
    # Skill-specific logic
```

**3. Verifier:**
```python
# Problem: BB5-specific validation
if 'threshold: 60' in content:  # Assumes BB5 format
    checks_passed += 1
```

**4. Metrics Collector:**
```python
# Problem: Absolute path
metrics_path = Path('/Users/shaansisodia/.blackbox5/.../skill-metrics.yaml')
```

---

## 3. Proposed Solution

### Skill Provider Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    RALF Core System                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              SkillProvider (Interface)               │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  get_skill_metrics() -> Dict                        │   │
│  │  get_skill_usage() -> Dict                          │   │
│  │  select_skill(task_description: str) -> Optional[str]│  │
│  │  is_enabled() -> bool                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                           ▲                                 │
│           ┌───────────────┴───────────────┐                 │
│           │                               │                 │
│  ┌────────┴────────┐          ┌──────────┴────────┐       │
│  │ BlackBox5Skill  │          │   NullSkill       │       │
│  │    Provider     │          │    Provider       │       │
│  ├─────────────────┤          ├───────────────────┤       │
│  │ BB5-specific    │          │ No-op implementation│      │
│  │ implementation  │          │ for non-BB5 projects│      │
│  └─────────────────┘          └───────────────────┘       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### SkillProvider Interface

```python
# 2-engine/.autonomous/lib/skill_provider.py

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from pathlib import Path

class SkillProvider(ABC):
    """Abstract interface for skill system integration."""

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

    @abstractmethod
    def get_skill_config(self) -> Dict:
        """Get skill system configuration."""
        pass


class BlackBox5SkillProvider(SkillProvider):
    """BB5-specific skill provider implementation."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.ops_dir = project_dir / "operations"

    def is_enabled(self) -> bool:
        """Check if BB5 skill system is present."""
        return (
            (self.ops_dir / "skill-selection.yaml").exists() or
            (self.ops_dir / "skill-metrics.yaml").exists()
        )

    def get_skill_metrics(self) -> Dict:
        """Load skill metrics from BB5 location."""
        metrics_path = self.ops_dir / "skill-metrics.yaml"
        if not metrics_path.exists():
            return {}

        with open(metrics_path) as f:
            return yaml.safe_load(f) or {}

    def get_skill_usage(self) -> Dict:
        """Load skill usage from BB5 location."""
        usage_path = self.ops_dir / "skill-usage.yaml"
        if not usage_path.exists():
            return {}

        with open(usage_path) as f:
            return yaml.safe_load(f) or {}

    def select_skill(self, task_description: str) -> Optional[str]:
        """Select skill using BB5 selection rules."""
        selection_path = self.ops_dir / "skill-selection.yaml"
        if not selection_path.exists():
            return None

        # Load selection rules
        with open(selection_path) as f:
            rules = yaml.safe_load(f) or {}

        # Apply selection logic
        # ... (existing logic moved here)

        return selected_skill

    def get_skill_config(self) -> Dict:
        """Get BB5 skill configuration."""
        return {
            "provider": "blackbox5",
            "operations_dir": str(self.ops_dir),
            "files": {
                "selection": "skill-selection.yaml",
                "metrics": "skill-metrics.yaml",
                "usage": "skill-usage.yaml"
            }
        }


class NullSkillProvider(SkillProvider):
    """No-op provider when skills are disabled or unavailable."""

    def is_enabled(self) -> bool:
        return False

    def get_skill_metrics(self) -> Dict:
        return {}

    def get_skill_usage(self) -> Dict:
        return {}

    def select_skill(self, task_description: str) -> Optional[str]:
        return None

    def get_skill_config(self) -> Dict:
        return {"provider": "null", "enabled": False}


class SkillProviderFactory:
    """Factory for creating appropriate skill provider."""

    @staticmethod
    def create(project_dir: Path) -> SkillProvider:
        """Create the appropriate skill provider for the project."""
        # Try BB5 provider first
        bb5_provider = BlackBox5SkillProvider(project_dir)
        if bb5_provider.is_enabled():
            return bb5_provider

        # Fall back to null provider
        return NullSkillProvider()
```

### Capability-Based Task Routing

Replace hardcoded task ID checks with capability detection:

```python
# BEFORE (hardcoded)
if task_id.startswith("TASK-SKIL-"):
    return SkillExecutor()

# AFTER (capability-based)
if self.skill_provider.is_enabled():
    task_capabilities = self.detect_capabilities(task)
    if "skill-management" in task_capabilities:
        return SkillExecutor()
```

### Updated Agent Pattern

```python
# 2-engine/.autonomous/bin/scout-improve.py (updated)

class ScoutImprove:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.skill_provider = SkillProviderFactory.create(config.project_dir)

    def analyze(self) -> ScoutReport:
        """Analyze project for improvement opportunities."""
        report = ScoutReport()

        # Only analyze skills if skill system is enabled
        if self.skill_provider.is_enabled():
            report.skill_metrics = self.skill_provider.get_skill_metrics()
            report.skill_opportunities = self._analyze_skill_usage()
        else:
            report.skill_metrics = None
            report.skill_opportunities = []

        # Continue with other analysis (not skill-dependent)
        report.code_issues = self._analyze_code()
        report.process_issues = self._analyze_process()

        return report
```

---

## 4. Implementation Plan

### Phase 1: Create Skill Provider Interface (Day 1)

**Files to Create:**
1. `2-engine/.autonomous/lib/skill_provider.py` - Abstract interface and implementations

**Features:**
- `SkillProvider` abstract base class
- `BlackBox5SkillProvider` implementation
- `NullSkillProvider` implementation
- `SkillProviderFactory` for auto-detection

### Phase 2: Update Scout Agents (Day 1-2)

**Files to Modify:**
1. `2-engine/.autonomous/bin/scout-improve.py`
2. `2-engine/.autonomous/bin/scout-intelligent.py`
3. `2-engine/.autonomous/bin/scout-task-based.py`

**Changes:**
- Check `skill_provider.is_enabled()` before reading skill files
- Use provider methods instead of direct file access
- Handle null provider gracefully

### Phase 3: Update Executor (Day 2)

**Files to Modify:**
1. `2-engine/.autonomous/bin/executor-implement.py`

**Changes:**
- Replace hardcoded task ID checks with capability detection
- Use skill provider for skill-related routing
- Continue execution when skills unavailable

### Phase 4: Update Verifier (Day 2-3)

**Files to Modify:**
1. `2-engine/.autonomous/bin/verifier-validate.py`

**Changes:**
- Validate against `SkillProvider` interface, not specific YAML structure
- Skip skill validation when provider is null
- Generic validation that works for any skill system

### Phase 5: Fix Absolute Path Bug (Day 3)

**Files to Modify:**
1. `bin/collect-skill-metrics.py`

**Changes:**
```python
# BEFORE (BROKEN)
metrics_path = Path('/Users/shaansisodia/.blackbox5/.../skill-metrics.yaml')

# AFTER
metrics_path = PROJECT_DIR / "operations" / "skill-metrics.yaml"
```

### Phase 6: Testing (Day 3-4)

**Files to Create:**
1. `2-engine/.autonomous/tests/test_skill_provider.py`

**Test Cases:**
- Null provider returns empty data
- BB5 provider loads from correct paths
- Factory selects correct provider
- Agents work with null provider
- Agents work with BB5 provider

---

## 5. Files to Create/Modify

### New Files

| File | Purpose |
|------|---------|
| `2-engine/.autonomous/lib/skill_provider.py` | Skill provider interface and implementations |
| `2-engine/.autonomous/tests/test_skill_provider.py` | Unit tests |

### Modified Files

| File | Changes |
|------|---------|
| `2-engine/.autonomous/bin/scout-improve.py` | Use skill provider |
| `2-engine/.autonomous/bin/scout-intelligent.py` | Use skill provider |
| `2-engine/.autonomous/bin/scout-task-based.py` | Use skill provider |
| `2-engine/.autonomous/bin/executor-implement.py` | Capability-based routing |
| `2-engine/.autonomous/bin/verifier-validate.py` | Interface-based validation |
| `bin/collect-skill-metrics.py` | Fix absolute path |

---

## 6. Success Criteria

- [ ] Create `SkillProvider` abstract interface
- [ ] Create `BlackBox5SkillProvider` implementation
- [ ] Create `NullSkillProvider` for projects without skills
- [ ] Update all scout agents to use skill provider
- [ ] Update executor to use capability routing
- [ ] Update verifier to use generic validation
- [ ] Fix absolute path in `collect-skill-metrics.py`
- [ ] RALF works gracefully when skill system disabled

---

## 7. Rollback Strategy

If decoupling causes issues:

1. **Immediate**: Keep BB5-specific code paths as fallback
2. **Short-term**: Revert to direct file access for BB5 projects
3. **Full**: Complete rollback using git history

**Fallback Pattern:**
```python
# In each agent, keep fallback
try:
    # Use skill provider
    metrics = self.skill_provider.get_skill_metrics()
except Exception:
    # Fallback to BB5 direct access
    metrics = self._legacy_load_metrics()
```

---

## 8. Estimated Timeline

| Phase | Duration |
|-------|----------|
| Phase 1: Skill Provider Interface | 4 hours |
| Phase 2: Update Scout Agents | 6 hours |
| Phase 3: Update Executor | 4 hours |
| Phase 4: Update Verifier | 4 hours |
| Phase 5: Fix Path Bug | 2 hours |
| Phase 6: Testing | 6 hours |
| **Total** | **26 hours (3-4 days)** |

---

## 9. Key Design Decisions

### Decision 1: Interface vs Direct Access
**Choice:** Abstract interface with multiple implementations
**Rationale:** Clean separation, testability, flexibility

### Decision 2: Auto-Detection vs Configuration
**Choice:** Factory auto-detects provider type
**Rationale:** Zero configuration for common cases

### Decision 3: Null Object Pattern
**Choice:** Null provider instead of optional/None
**Rationale:** Eliminates null checks throughout code

### Decision 4: Capability vs ID Routing
**Choice:** Route by capability, not hardcoded IDs
**Rationale:** Works with any task naming convention

---

*Plan created based on Issue #4 requirements and decoupling best practices*
