# TASK-RALF-002: Create RALF Configuration System

**Status:** pending
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
- [ ] Create `2-engine/.autonomous/lib/config.py` configuration loader
- [ ] Support all 5 configuration sources with proper precedence
- [ ] Create `2-engine/.autonomous/config/default.yaml` with defaults
- [ ] Update all 6 agent scripts to use config system
- [ ] Add configuration validation
- [ ] Create `.ralf/config.yaml` template for projects

## Rollback Strategy
Keep hardcoded fallbacks in all scripts.
