# PLAN.md: Create RALF Configuration System

**Task ID:** TASK-RALF-002
**Status:** Planning
**Priority:** CRITICAL
**Parent:** Issue #4 - RALF Knows Project Structure
**Estimated Effort:** 6 hours

---

## 1. First Principles Analysis

### Why is a Unified Configuration System Critical?

1. **Single Source of Truth**: One place to configure all RALF behavior
2. **Project Agnosticism**: RALF can adapt to any project structure
3. **User Customization**: Users can override defaults without code changes
4. **Environment Flexibility**: Different configs for dev, test, production
5. **Feature Toggles**: Enable/disable features without deployment

### What Happens Without a Configuration System?

| Problem | Impact | Severity |
|---------|--------|----------|
| Hardcoded paths | Cannot use with other projects | Critical |
| Scattered settings | Inconsistent behavior | High |
| No feature toggles | Cannot disable broken features | High |
| Environment-specific hacks | Code pollution | Medium |
| Difficult onboarding | New users confused | Medium |

### How Does a Configuration Hierarchy Help?

By supporting multiple configuration sources with clear precedence, we enable:
- **CLI arguments** for one-off overrides
- **Environment variables** for deployment-specific settings
- **Project config** for team-shared defaults
- **User config** for personal preferences
- **Engine defaults** for out-of-box functionality

---

## 2. Current State Assessment

### Existing Configuration

| Source | Location | Status |
|--------|----------|--------|
| Hardcoded paths | 6 agent scripts | Critical issue |
| Environment variables | Not used | Missing |
| Config files | None | Missing |
| CLI arguments | Minimal | Partial |

### Configuration Needs

| Component | Needs Configuration |
|-----------|---------------------|
| Scout agent | Output directory, enabled/disabled |
| Planner agent | Priority weights, enabled/disabled |
| Executor agent | Timeout settings, enabled/disabled |
| Verifier agent | Validation rules, enabled/disabled |
| Skills system | Config path, enabled/disabled |
| Improvement loop | Max iterations, enabled/disabled |
| Timeline | Enabled/disabled |
| Storage | Backend, format |

---

## 3. Proposed Solution

### Configuration Hierarchy (Highest to Lowest Priority)

```
1. CLI Arguments
   ↓
2. Environment Variables
   ↓
3. Project Config (.ralf/config.yaml)
   ↓
4. User Config (~/.config/ralf/config.yaml)
   ↓
5. Engine Defaults (2-engine/.autonomous/config/default.yaml)
```

### Configuration Schema

```yaml
ralf:
  version: "3.0.0"

paths:
  project_root: "${RALF_PROJECT_DIR}"
  engine_dir: "${RALF_ENGINE_DIR}"
  autonomous_dir: "${RALF_PROJECT_DIR}/.autonomous"
  tasks_dir: "${RALF_PROJECT_DIR}/tasks"
  runs_dir: "${RALF_PROJECT_DIR}/.autonomous/runs"
  analysis_dir: "${RALF_PROJECT_DIR}/.autonomous/analysis"

agents:
  scout:
    enabled: true
    script: "scout-intelligent.py"
    output_dir: "analysis/scout-reports"
  planner:
    enabled: true
    script: "planner-prioritize.py"
  executor:
    enabled: true
    script: "executor-implement.py"
    timeout_minutes: 30
  verifier:
    enabled: true
    script: "verifier-validate.py"

features:
  skills:
    enabled: true
    config_path: "operations/skill-selection.yaml"
  improvement_loop:
    enabled: true
    max_iterations: 10
  timeline:
    enabled: true

storage:
  backend: "filesystem"  # or "database", "git"
  format: "yaml"         # or "json", "sqlite"
```

---

## 4. Implementation Plan

### Phase 1: Create Default Configuration (30 min)

**1.1 Create `2-engine/.autonomous/config/default.yaml`**
- Define complete default configuration
- Include all agent settings
- Include all feature toggles
- Include storage configuration

**1.2 Create configuration schema validator**
- Define required fields
- Define type constraints
- Define valid values for enums

### Phase 2: Create Configuration Loader (90 min)

**2.1 Create `2-engine/.autonomous/lib/config.py`**

```python
"""RALF configuration loader with hierarchy support."""
import os
import yaml
from pathlib import Path
from typing import Any, Optional

class RalfConfig:
    """RALF configuration manager."""

    def __init__(self):
        self._config = {}
        self._load()

    def _load(self):
        """Load configuration from all sources."""
        # 5. Engine defaults (lowest priority)
        self._load_defaults()

        # 4. User config
        self._load_user_config()

        # 3. Project config
        self._load_project_config()

        # 2. Environment variables
        self._load_env_vars()

        # 1. CLI arguments (highest priority)
        # Applied after initialization via override()

    def _load_defaults(self):
        """Load engine defaults."""
        defaults_path = Path(__file__).parent.parent / "config" / "default.yaml"
        if defaults_path.exists():
            with open(defaults_path) as f:
                self._config = yaml.safe_load(f)

    def _load_user_config(self):
        """Load user configuration."""
        user_config_path = Path.home() / ".config" / "ralf" / "config.yaml"
        self._merge_config(user_config_path)

    def _load_project_config(self):
        """Load project configuration."""
        project_config_path = Path(".ralf") / "config.yaml"
        self._merge_config(project_config_path)

    def _load_env_vars(self):
        """Load environment variable overrides."""
        env_mappings = {
            "RALF_PROJECT_DIR": ["paths", "project_root"],
            "RALF_ENGINE_DIR": ["paths", "engine_dir"],
            "RALF_SCOUT_ENABLED": ["agents", "scout", "enabled"],
            "RALF_PLANNER_ENABLED": ["agents", "planner", "enabled"],
            "RALF_EXECUTOR_ENABLED": ["agents", "executor", "enabled"],
            "RALF_VERIFIER_ENABLED": ["agents", "verifier", "enabled"],
        }

        for env_var, path in env_mappings.items():
            value = os.environ.get(env_var)
            if value:
                self._set_nested(path, self._convert_type(value))

    def _merge_config(self, path: Path):
        """Merge configuration from file."""
        if path.exists():
            with open(path) as f:
                override = yaml.safe_load(f)
                self._deep_merge(self._config, override)

    def _deep_merge(self, base: dict, override: dict):
        """Deep merge two dictionaries."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def get(self, path: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation path."""
        keys = path.split(".")
        value = self._config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def override(self, path: str, value: Any):
        """Override configuration value (for CLI args)."""
        self._set_nested(path.split("."), value)

    def validate(self) -> list[str]:
        """Validate configuration and return list of errors."""
        errors = []

        # Validate paths exist
        project_root = self.get("paths.project_root")
        if project_root and not Path(project_root).exists():
            errors.append(f"paths.project_root does not exist: {project_root}")

        # Validate agent scripts exist
        for agent in ["scout", "planner", "executor", "verifier"]:
            script = self.get(f"agents.{agent}.script")
            if script:
                engine_dir = self.get("paths.engine_dir")
                script_path = Path(engine_dir) / ".autonomous" / "bin" / script
                if not script_path.exists():
                    errors.append(f"agents.{agent}.script not found: {script_path}")

        return errors
```

### Phase 3: Create Project Config Template (15 min)

**3.1 Create `.ralf/config.yaml` template**
```yaml
# RALF Project Configuration
# Place this file in your project root as .ralf/config.yaml

ralf:
  version: "3.0.0"

# Project-specific paths (relative to project root)
paths:
  # Override if your project structure differs
  autonomous_dir: ".autonomous"
  tasks_dir: "tasks"
  runs_dir: ".autonomous/runs"

# Agent configuration
agents:
  scout:
    enabled: true
    output_dir: "analysis/scout-reports"
  planner:
    enabled: true
  executor:
    enabled: true
    timeout_minutes: 30
  verifier:
    enabled: true

# Feature toggles
features:
  skills:
    enabled: true
  improvement_loop:
    enabled: true
    max_iterations: 10
  timeline:
    enabled: true
```

### Phase 4: Update Agent Scripts (90 min)

**4.1 Update all 6 agent scripts**
- Replace direct path imports with config usage
- Add configuration validation on startup
- Use config values for agent-specific settings

Example update:
```python
from lib.config import RalfConfig

config = RalfConfig()
errors = config.validate()
if errors:
    for error in errors:
        print(f"Config error: {error}")
    sys.exit(1)

PROJECT_DIR = Path(config.get("paths.project_root"))
SCOUT_ENABLED = config.get("agents.scout.enabled", True)
```

### Phase 5: Testing (75 min)

**5.1 Configuration Loading Test**
- Test hierarchy precedence
- Verify CLI args override env vars
- Verify env vars override config files
- Verify config files override defaults

**5.2 Validation Test**
- Test with invalid paths
- Test with missing agent scripts
- Test with invalid feature toggles
- Verify helpful error messages

**5.3 Integration Test**
- Run each agent with custom config
- Verify settings applied correctly
- Test feature toggles (enable/disable)

**5.4 Backward Compatibility Test**
- Run without any config files
- Verify defaults work
- Verify env vars still work

---

## 5. Success Criteria

| Criterion | Verification Method |
|-----------|---------------------|
| Config loader created | `lib/config.py` exists and loads |
| All 5 sources supported | Test hierarchy precedence |
| Default config created | `config/default.yaml` exists |
| All 6 agent scripts updated | Code review |
| Configuration validation works | Test with invalid config |
| Project config template created | `.ralf/config.yaml` template exists |
| Backward compatibility maintained | Run without config files |

---

## 6. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Default Configuration | 30 min | 30 min |
| Phase 2: Configuration Loader | 90 min | 120 min |
| Phase 3: Project Config Template | 15 min | 135 min |
| Phase 4: Update Agent Scripts | 90 min | 225 min |
| Phase 5: Testing | 75 min | 300 min |
| **Total** | **5 hours** | |

---

## 7. Rollback Strategy

If issues arise:
1. Keep hardcoded fallbacks in all scripts
2. Revert to TASK-RALF-001 implementation (env vars only)
3. Remove config loader
4. Remove default config

---

## 8. Dependencies

- **TASK-RALF-001** (Extract Hardcoded Paths) - Must be completed first
- Path module from TASK-RALF-001 will be extended

---

## 9. Future Extensions

This configuration system enables future features:
- **Database backend** - Change storage.backend to "database"
- **Git storage** - Track all changes in git
- **Remote configuration** - Load config from URL
- **Configuration UI** - Web interface for settings

---

*A unified configuration system is the foundation for RALF's flexibility and adoption.*
