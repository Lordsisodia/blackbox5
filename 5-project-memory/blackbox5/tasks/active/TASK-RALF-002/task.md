# TASK-RALF-002: Create RALF Configuration System

**Status:** completed
**Priority:** CRITICAL
**Parent:** Issue #4 - RALF Knows Project Structure

## Objective
Create a unified configuration system for RALF that supports project-agnostic operation.

## Configuration Hierarchy (Highest to Lowest Priority)
1. CLI Arguments
2. Environment Variables
3. Project Config (`.ralf/config.yaml`)
4. User Config (`~/.config/ralf/config.yaml`)
5. Engine Defaults (`2-engine/.autonomous/config/default.yaml`)

## Configuration Schema
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

## Success Criteria
- [x] Create `2-engine/.autonomous/lib/config.py` configuration loader
- [x] Support all 5 configuration sources with proper precedence
- [x] Create `2-engine/.autonomous/config/default.yaml` with defaults
- [x] Update all 6 agent scripts to use config system
- [x] Add configuration validation
- [x] Create `.ralf/config.yaml` template for projects

## Files Created

### Core Configuration Files
1. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/config/default.yaml` - Engine defaults
2. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/config/project-template.yaml` - Project template
3. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/lib/config.py` - Configuration loader library
4. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/lib/test_config.py` - Test suite

### User and Project Configs
5. `/Users/shaansisodia/.blackbox5/.ralf/config.yaml` - User-level config
6. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.ralf/config.yaml` - BlackBox5 project config

### Updated Agent Scripts
7. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/bin/scout-intelligent.py`
8. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/bin/planner-prioritize.py`
9. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/bin/executor-implement.py`
10. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/bin/verifier-validate.py`
11. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/bin/improvement-loop.py`

## Configuration Features

### Environment Variables Supported
- `RALF_PROJECT_DIR` - Override project directory
- `RALF_ENGINE_DIR` - Override engine directory
- `RALF_LOG_LEVEL` - Set logging level
- `RALF_STORAGE_BACKEND` - Storage backend type
- `RALF_SCOUT_ENABLED` - Enable/disable scout
- `RALF_PLANNER_ENABLED` - Enable/disable planner
- `RALF_EXECUTOR_ENABLED` - Enable/disable executor
- `RALF_VERIFIER_ENABLED` - Enable/disable verifier
- `RALF_MAX_ITERATIONS` - Max improvement loop iterations
- `RALF_AUTO_EXECUTE` - Auto-execute improvements

### API Usage
```python
from config import get_config

config = get_config()

# Get values with type coercion
project_root = config.get_path('paths.project_root')
scout_enabled = config.get_bool('agents.scout.enabled')
timeout = config.get_int('agents.scout.timeout_seconds', 300)
log_level = config.get_str('logging.level', 'INFO')

# Get agent config
scout_config = config.get_agent_config('scout')

# Validate
if config.is_valid():
    print("Configuration is valid")
```

## Test Results
All 8 configuration tests passed:
- Basic Configuration Loading
- Environment Variable Substitution
- Type Coercion
- Configuration Validation
- Configuration Source Status
- Agent Configuration
- Hook Timeouts
- Print Status

## Rollback Strategy
Keep hardcoded fallbacks in all scripts. The config system is additive - if config fails, scripts fall back to existing path resolution.

## Notes
- Configuration system is backward compatible
- Existing hardcoded paths remain as fallbacks
- Environment variables take precedence over file configs
- Project configs override user configs
