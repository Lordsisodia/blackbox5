# PLAN.md: Implement Graceful Error Handling and Degradation

**Task:** TASK-RALF-010 - Graceful Error Handling and Degradation
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 3-4 days
**Parent:** Issue #4 - RALF Knows Project Structure
**Importance:** 90 (Critical)

---

## 1. First Principles Analysis

### Why Does RALF Need Graceful Error Handling?

1. **Resilience**: RALF should continue operating when non-critical files are missing
2. **Portability**: Should work across different project structures without hard failures
3. **User Experience**: Clear error messages guide users to solutions
4. **Debugging**: Structured error handling makes issues easier to diagnose
5. **Degradation**: Partial functionality is better than complete failure

### What Happens Without Graceful Handling?

- **Hard Failures**: Single missing file stops entire pipeline
- **Poor UX**: Cryptic Python tracebacks instead of helpful messages
- **BB5 Lock-in**: Cannot run in projects without BB5-specific files
- **Data Loss**: Partial results lost due to report save failures
- **Silent Errors**: Issues go unnoticed until they cause bigger problems

### How Should Error Handling Work?

1. **Recovery Actions**: CONTINUE, RETRY, SKIP, ABORT, DEGRADED
2. **Fallback Chains**: Try alternatives before failing
3. **Graceful Degradation**: Reduce functionality instead of stopping
4. **Structured Logging**: Consistent error format across components
5. **Configuration**: Enable/disable graceful mode per environment

---

## 2. Current State Assessment

### Current Error Handling Problems

| Component | Location | Issue |
|-----------|----------|-------|
| Planner | `planner-prioritize.py:77-108` | No fallback when scout report missing |
| Improvement Loop | `improvement-loop.py:183-219` | Reports save to BB5-only locations |
| Roadmap Sync | `roadmap_sync.py:336-353` | Hard failure on missing STATE.yaml |
| Verifier | `verifier-validate.py:82-96` | BB5-specific validation only |

### Problem Examples

**1. No Fallback When Files Missing:**
```python
# planner-prioritize.py
def load_scout_report(self) -> bool:
    if not self.scout_report_path.exists():
        print(f"❌ Scout report not found: {self.scout_report_path}")
        return False  # No fallback, just fails
```

**2. BB5-Only Report Locations:**
```python
# improvement-loop.py
def save_loop_report(self) -> Path:
    report_dir = REPORTS_DIR / "loop-reports"  # BB5-specific path
    report_dir.mkdir(parents=True, exist_ok=True)
```

**3. Hard Failures on Missing Files:**
```python
# roadmap_sync.py
if not os.path.exists(state_yaml_path):
    result["error"] = f"STATE.yaml not found at {state_yaml_path}"
    return result  # Hard failure, no fallback
```

**4. BB5-Specific Validation:**
```python
# verifier-validate.py
if 'threshold: 60' in content:
    checks_passed += 1  # Assumes BB5 format
```

---

## 3. Proposed Solution

### Error Handler Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Error Handling System                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              ErrorHandler (Interface)                │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  handle_file_not_found() -> Optional[Path]          │   │
│  │  handle_validation_failure() -> RecoveryAction      │   │
│  │  handle_missing_feature() -> RecoveryAction         │   │
│  └─────────────────────────────────────────────────────┘   │
│                           ▲                                 │
│                           │                                 │
│              ┌────────────┴────────────┐                    │
│              │                         │                    │
│     ┌────────┴────────┐       ┌────────┴────────┐          │
│     │  GracefulError  │       │   StrictError   │          │
│     │     Handler     │       │     Handler     │          │
│     ├─────────────────┤       ├─────────────────┤          │
│     │ Try alternatives│       │ Fail fast on    │          │
│     │ Degrade service │       │ any error       │          │
│     └─────────────────┘       └─────────────────┘          │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              ReportDirectoryResolver                 │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  get_report_dir(report_type) -> Path                │   │
│  │  Try: primary paths -> project dir -> temp          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### ErrorHandler Interface

```python
# 2-engine/.autonomous/lib/error_handler.py

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from pathlib import Path
from enum import Enum

class RecoveryAction(Enum):
    """Possible recovery actions for errors."""
    CONTINUE = "continue"    # Continue with default/empty values
    RETRY = "retry"          # Retry the operation
    SKIP = "skip"            # Skip this step
    ABORT = "abort"          # Stop execution
    DEGRADED = "degraded"    # Continue with reduced functionality

class ErrorHandler(ABC):
    """Abstract interface for error handling."""

    @abstractmethod
    def handle_file_not_found(
        self,
        path: Path,
        context: str,
        alternatives: List[Path] = None
    ) -> Optional[Path]:
        """Handle missing file, return alternative path or None."""
        pass

    @abstractmethod
    def handle_validation_failure(
        self,
        result: Dict[str, Any],
        severity: str = "error"
    ) -> RecoveryAction:
        """Determine recovery strategy for validation failure."""
        pass

    @abstractmethod
    def handle_missing_feature(
        self,
        feature_name: str,
        fallback_behavior: str = "skip"
    ) -> RecoveryAction:
        """Handle missing optional feature."""
        pass


class GracefulErrorHandler(ErrorHandler):
    """Error handler with graceful degradation."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.graceful_degradation = config.get("graceful_degradation", True)
        self.fallback_paths = config.get("fallback_paths", [])
        self.logger = logging.getLogger(__name__)

    def handle_file_not_found(
        self,
        path: Path,
        context: str,
        alternatives: List[Path] = None
    ) -> Optional[Path]:
        """Handle missing file with fallback chain."""
        self.logger.warning(f"File not found: {path} (context: {context})")

        # Try provided alternatives
        alternatives = alternatives or []
        for alt in alternatives:
            alt_path = alt / path.name if alt.is_dir() else alt
            if alt_path.exists():
                self.logger.info(f"Using alternative: {alt_path}")
                return alt_path

        # Try configured fallback paths
        for fallback in self.fallback_paths:
            fallback_path = Path(fallback) / path.name
            if fallback_path.exists():
                self.logger.info(f"Using fallback: {fallback_path}")
                return fallback_path

        # If graceful degradation enabled, return None
        if self.graceful_degradation:
            self.logger.info(f"Continuing without {path.name}")
            return None

        # Otherwise, raise error
        raise FileNotFoundError(f"Required file not found: {path}")

    def handle_validation_failure(
        self,
        result: Dict[str, Any],
        severity: str = "error"
    ) -> RecoveryAction:
        """Handle validation failure."""
        self.logger.warning(f"Validation failure ({severity}): {result}")

        if severity == "critical":
            return RecoveryAction.ABORT
        elif severity == "error" and not self.graceful_degradation:
            return RecoveryAction.ABORT
        elif severity == "warning":
            return RecoveryAction.CONTINUE
        else:
            return RecoveryAction.DEGRADED

    def handle_missing_feature(
        self,
        feature_name: str,
        fallback_behavior: str = "skip"
    ) -> RecoveryAction:
        """Handle missing optional feature."""
        self.logger.warning(f"Optional feature not available: {feature_name}")

        if fallback_behavior == "skip":
            return RecoveryAction.SKIP
        elif fallback_behavior == "degraded":
            return RecoveryAction.DEGRADED
        else:
            return RecoveryAction.CONTINUE


class StrictErrorHandler(ErrorHandler):
    """Error handler that fails fast on any error."""

    def handle_file_not_found(
        self,
        path: Path,
        context: str,
        alternatives: List[Path] = None
    ) -> Optional[Path]:
        """Always raise on missing file."""
        raise FileNotFoundError(f"Required file not found: {path} (context: {context})")

    def handle_validation_failure(
        self,
        result: Dict[str, Any],
        severity: str = "error"
    ) -> RecoveryAction:
        """Always abort on validation failure."""
        if severity in ("critical", "error"):
            return RecoveryAction.ABORT
        return RecoveryAction.CONTINUE

    def handle_missing_feature(
        self,
        feature_name: str,
        fallback_behavior: str = "skip"
    ) -> RecoveryAction:
        """Treat missing features as errors."""
        raise RuntimeError(f"Required feature not available: {feature_name}")
```

### Report Directory Resolver

```python
# 2-engine/.autonomous/lib/report_resolver.py

from pathlib import Path
from typing import List, Optional
import tempfile
import os

class ReportDirectoryResolver:
    """Resolve report directory with multiple fallbacks."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.primary_paths = config.get("report_paths", [])
        self.temp_fallback = config.get("temp_fallback", True)
        self.project_dir = Path(config.get("project_dir", "."))

    def get_report_dir(self, report_type: str = "general") -> Path:
        """Get report directory with fallback chain."""

        # Try primary configured paths
        for path_str in self.primary_paths:
            path = Path(path_str).expanduser()
            path = path / report_type
            if self._ensure_dir(path):
                return path

        # Try project directory standard locations
        for subdir in [".ralf/reports", ".autonomous/analysis", "reports", ".logs"]:
            path = self.project_dir / subdir / report_type
            if self._ensure_dir(path):
                return path

        # Try temp directory as last resort
        if self.temp_fallback:
            temp_dir = Path(tempfile.gettempdir()) / "ralf-reports" / report_type
            temp_dir.mkdir(parents=True, exist_ok=True)
            print(f"⚠️  Using temp directory for reports: {temp_dir}")
            return temp_dir

        raise RuntimeError(f"Cannot find or create report directory for {report_type}")

    def _ensure_dir(self, path: Path) -> bool:
        """Ensure directory exists or can be created."""
        try:
            path.mkdir(parents=True, exist_ok=True)
            # Test write access
            test_file = path / ".write_test"
            test_file.touch()
            test_file.unlink()
            return True
        except (PermissionError, OSError):
            return False
```

### Updated Component Patterns

**improvement-loop.py:**
```python
class ImprovementLoop:
    def __init__(self, config: ConfigManager, error_handler: ErrorHandler):
        self.config = config
        self.error_handler = error_handler
        self.report_resolver = ReportDirectoryResolver(config)

    def save_loop_report(self) -> Optional[Path]:
        try:
            report_dir = self.report_resolver.get_report_dir("loop-reports")
            # ... save report
            return report_path
        except Exception as e:
            action = self.error_handler.handle_validation_failure(
                {"error": str(e), "component": "improvement-loop"},
                severity="warning"
            )
            if action == RecoveryAction.ABORT:
                raise
            return None
```

**planner-prioritize.py:**
```python
def load_scout_report(self) -> bool:
    # Try primary path
    if self.scout_report_path.exists():
        return self._load_report_from_path(self.scout_report_path)

    # Try alternatives via error handler
    alternative = self.error_handler.handle_file_not_found(
        self.scout_report_path,
        context="scout report loading",
        alternatives=self._get_alternative_report_paths()
    )

    if alternative:
        return self._load_report_from_path(alternative)

    # Gracefully continue without scout report
    print("⚠️  Continuing without scout report - using default prioritization")
    self.opportunities = []
    return True
```

---

## 4. Implementation Plan

### Phase 1: Create Error Handler Interface (Day 1)

**Files to Create:**
1. `2-engine/.autonomous/lib/error_handler.py` - Error handler interface and implementations

**Features:**
- `RecoveryAction` enum
- `ErrorHandler` abstract base class
- `GracefulErrorHandler` implementation
- `StrictErrorHandler` implementation

### Phase 2: Create Report Resolver (Day 1)

**Files to Create:**
1. `2-engine/.autonomous/lib/report_resolver.py` - Report directory resolution

**Features:**
- Primary path resolution
- Project directory fallback
- Temp directory fallback
- Write access testing

### Phase 3: Update improvement-loop.py (Day 1-2)

**Changes:**
- Accept `ErrorHandler` in constructor
- Use `ReportDirectoryResolver` for report paths
- Handle save failures gracefully
- Return `Optional[Path]` instead of `Path`

### Phase 4: Update planner-prioritize.py (Day 2)

**Changes:**
- Use error handler for missing scout reports
- Provide alternative report paths
- Continue with defaults when report missing
- Log warnings instead of errors

### Phase 5: Update executor-implement.py (Day 2-3)

**Changes:**
- Handle task loading failures
- Use error handler for missing task files
- Degrade to basic execution if needed
- Log structured error information

### Phase 6: Update verifier-validate.py (Day 3)

**Changes:**
- Use structured validation results
- Handle missing validation targets
- Support generic validation rules
- Return `RecoveryAction` for failures

### Phase 7: Configuration (Day 3)

**Files to Modify:**
1. `2-engine/.autonomous/config/default.yaml` - Add error handling configuration

**Configuration:**
```yaml
error_handling:
  mode: "graceful"  # graceful | strict
  graceful_degradation: true
  temp_fallback: true
  fallback_paths: []
  log_level: "warning"
```

### Phase 8: Testing (Day 3-4)

**Files to Create:**
1. `2-engine/.autonomous/tests/test_error_handler.py`
2. `2-engine/.autonomous/tests/test_report_resolver.py`

**Test Cases:**
- File not found with alternatives
- File not found without alternatives
- Validation failure handling
- Missing feature handling
- Report directory resolution chain
- Temp directory fallback

---

## 5. Files to Create/Modify

### New Files

| File | Purpose |
|------|---------|
| `2-engine/.autonomous/lib/error_handler.py` | Error handler interface |
| `2-engine/.autonomous/lib/report_resolver.py` | Report directory resolver |
| `2-engine/.autonomous/tests/test_error_handler.py` | Error handler tests |
| `2-engine/.autonomous/tests/test_report_resolver.py` | Resolver tests |

### Modified Files

| File | Changes |
|------|---------|
| `2-engine/.autonomous/bin/improvement-loop.py` | Use error handler and resolver |
| `2-engine/.autonomous/bin/planner-prioritize.py` | Handle missing reports gracefully |
| `2-engine/.autonomous/bin/executor-implement.py` | Handle task loading failures |
| `2-engine/.autonomous/bin/verifier-validate.py` | Structured validation |
| `2-engine/.autonomous/config/default.yaml` | Add error handling config |

---

## 6. Success Criteria

- [ ] Create `ErrorHandler` abstract interface
- [ ] Create `GracefulErrorHandler` implementation
- [ ] Create `ReportDirectoryResolver` for fallback report paths
- [ ] Update improvement-loop.py to use error handler
- [ ] Update planner-prioritize.py to handle missing reports gracefully
- [ ] Update executor-implement.py to handle task loading failures
- [ ] Update verifier-validate.py to use structured validation
- [ ] Add configuration for graceful degradation mode
- [ ] RALF continues operation when BB5-specific files are missing

---

## 7. Rollback Strategy

If error handling causes issues:

1. **Immediate**: Disable graceful degradation via configuration
2. **Short-term**: Revert to strict mode
3. **Full**: Remove error handler usage from components

**Disable Graceful Mode:**
```yaml
# In configuration
error_handling:
  mode: "strict"  # Fail fast on errors
```

---

## 8. Estimated Timeline

| Phase | Duration |
|-------|----------|
| Phase 1: Error Handler Interface | 4 hours |
| Phase 2: Report Resolver | 3 hours |
| Phase 3: Update Improvement Loop | 4 hours |
| Phase 4: Update Planner | 3 hours |
| Phase 5: Update Executor | 4 hours |
| Phase 6: Update Verifier | 3 hours |
| Phase 7: Configuration | 2 hours |
| Phase 8: Testing | 6 hours |
| **Total** | **29 hours (3-4 days)** |

---

## 9. Key Design Decisions

### Decision 1: Interface vs Static Functions
**Choice:** Abstract interface with multiple implementations
**Rationale:** Allows different strategies per environment (dev vs prod)

### Decision 2: Graceful vs Strict Mode
**Choice:** Configurable mode with graceful default
**Rationale:** Development benefits from strict, production from graceful

### Decision 3: Fallback Chain vs Single Fallback
**Choice:** Multiple fallback levels
**Rationale:** Maximizes chance of finding usable location

### Decision 4: RecoveryAction Enum
**Choice:** Explicit action types instead of booleans
**Rationale:** Clear intent, extensible for new actions

---

*Plan created based on Issue #4 requirements and error handling best practices*
