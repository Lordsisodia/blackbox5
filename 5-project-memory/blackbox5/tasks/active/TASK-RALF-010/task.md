# TASK-RALF-010: Implement Graceful Error Handling and Degradation

**Status:** pending
**Priority:** HIGH
**Parent:** Issue #4 - RALF Knows Project Structure

## Objective
Implement graceful error handling that doesn't assume BB5-specific file structures.

## Current Problems

### 1. No Fallback When Files Missing
**planner-prioritize.py lines 77-108:**
```python
def load_scout_report(self) -> bool:
    if not self.scout_report_path.exists():
        print(f"❌ Scout report not found: {self.scout_report_path}")
        return False  # No fallback, just fails
```

### 2. Error Reports Save to BB5-Only Locations
**improvement-loop.py lines 183-219:**
```python
def save_loop_report(self) -> Path:
    report_dir = REPORTS_DIR / "loop-reports"  # BB5-specific path
    report_dir.mkdir(parents=True, exist_ok=True)
```

### 3. Hard Failures on Missing BB5 Files
**roadmap_sync.py lines 336-353:**
```python
if not os.path.exists(state_yaml_path):
    result["error"] = f"STATE.yaml not found at {state_yaml_path}"
    return result  # Hard failure, no fallback
```

### 4. BB5-Specific Validation
**verifier-validate.py lines 82-96:**
```python
# Check 1: Threshold is 60
if 'threshold: 60' in content:
    checks_passed += 1
```

## Solution Approach

### Phase 1: Create Error Handler Interface
```python
# 2-engine/.autonomous/lib/error_handler.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from pathlib import Path
from enum import Enum

class RecoveryAction(Enum):
    CONTINUE = "continue"
    RETRY = "retry"
    SKIP = "skip"
    ABORT = "abort"
    DEGRADED = "degraded"

class ErrorHandler(ABC):
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

    def handle_file_not_found(
        self,
        path: Path,
        context: str,
        alternatives: List[Path] = None
    ) -> Optional[Path]:
        # Log the missing file
        print(f"⚠️  File not found: {path} (context: {context})")

        # Try alternatives
        alternatives = alternatives or []
        for alt in alternatives + self.fallback_paths:
            alt_path = alt / path.name if alt.is_dir() else alt
            if alt_path.exists():
                print(f"✓ Using alternative: {alt_path}")
                return alt_path

        # If graceful degradation enabled, return None instead of failing
        if self.graceful_degradation:
            print(f"⚠️  Continuing without {path.name}")
            return None

        raise FileNotFoundError(f"Required file not found: {path}")

    def handle_validation_failure(
        self,
        result: Dict[str, Any],
        severity: str = "error"
    ) -> RecoveryAction:
        if severity == "critical":
            return RecoveryAction.ABORT
        elif severity == "error" and not self.graceful_degradation:
            return RecoveryAction.ABORT
        else:
            return RecoveryAction.DEGRADED

    def handle_missing_feature(
        self,
        feature_name: str,
        fallback_behavior: str = "skip"
    ) -> RecoveryAction:
        print(f"⚠️  Optional feature not available: {feature_name}")
        if fallback_behavior == "skip":
            return RecoveryAction.SKIP
        elif fallback_behavior == "degraded":
            return RecoveryAction.DEGRADED
        else:
            return RecoveryAction.CONTINUE
```

### Phase 2: Create Report Directory Resolver
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

    def get_report_dir(self, report_type: str = "general") -> Path:
        """Get report directory with fallback chain."""

        # Try primary configured paths
        for path_str in self.primary_paths:
            path = Path(path_str).expanduser()
            path = path / report_type
            if path.exists() or self._can_create(path):
                return path

        # Try project directory
        project_dir = Path(os.environ.get("RALF_PROJECT_DIR", "."))
        for subdir in [".ralf/reports", ".autonomous/analysis", "reports"]:
            path = project_dir / subdir / report_type
            if path.exists() or self._can_create(path):
                return path

        # Try temp directory as last resort
        if self.temp_fallback:
            temp_dir = Path(tempfile.gettempdir()) / "ralf-reports" / report_type
            temp_dir.mkdir(parents=True, exist_ok=True)
            print(f"⚠️  Using temp directory for reports: {temp_dir}")
            return temp_dir

        raise RuntimeError(f"Cannot find or create report directory for {report_type}")

    def _can_create(self, path: Path) -> bool:
        """Check if we can create the directory."""
        try:
            path.mkdir(parents=True, exist_ok=True)
            return True
        except (PermissionError, OSError):
            return False
```

### Phase 3: Update Components to Use Error Handler

**Update improvement-loop.py:**
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
        except Exception as e:
            action = self.error_handler.handle_validation_failure(
                {"error": str(e)},
                severity="warning"
            )
            if action == RecoveryAction.ABORT:
                raise
            return None
```

**Update planner-prioritize.py:**
```python
def load_scout_report(self) -> bool:
    # Try primary path
    if self.scout_report_path.exists():
        # ... load report
        return True

    # Try alternatives
    alternative = self.error_handler.handle_file_not_found(
        self.scout_report_path,
        context="scout report loading",
        alternatives=self._get_alternative_report_paths()
    )

    if alternative:
        self.scout_report_path = alternative
        return self._load_report_from_path(alternative)

    # Gracefully continue without scout report
    print("⚠️  Continuing without scout report - will use default prioritization")
    self.opportunities = []
    return True
```

## Success Criteria
- [ ] Create `ErrorHandler` abstract interface
- [ ] Create `GracefulErrorHandler` implementation
- [ ] Create `ReportDirectoryResolver` for fallback report paths
- [ ] Update improvement-loop.py to use error handler
- [ ] Update planner-prioritize.py to handle missing reports gracefully
- [ ] Update executor-implement.py to handle task loading failures
- [ ] Update verifier-validate.py to use structured validation
- [ ] Add configuration for graceful degradation mode
- [ ] RALF continues operation when BB5-specific files are missing

## Rollback Strategy
Can disable graceful degradation via configuration if issues arise.
