# TASK-ARCH-067: Decouple Agents from Project Structure

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-06
**Type:** Structural Architecture

## Objective
Decouple the 6-agent pipeline from BlackBox5-specific structure so it can work with any project.

## Background
Scout analysis found tight coupling:
- All agent scripts hardcode BlackBox5 paths
- Agent scripts reference specific task IDs (TASK-SKIL-005, etc.)
- Communication protocols are BlackBox5-specific
- Cannot reuse agents for other projects

## Coupling Issues to Fix

### 1. Hardcoded Paths (CRITICAL)
```python
# Current (in all 6 agent scripts)
PROJECT_DIR = Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"

# Should be
PROJECT_DIR = get_project_path()  # From config or parameter
```

### 2. Hardcoded Task Handlers (HIGH)
```python
# Current (in executor-implement.py)
if task_id == "TASK-SKIL-005":
    # Specific handler for this task

# Should be
# Generic handler based on task type/category
```

### 3. Hardcoded File References (HIGH)
```python
# Current
skill_metrics = load("skill-metrics.yaml")  # Assumes specific structure

# Should be
skill_metrics = load(config.skill_metrics_path)  # Configurable
```

### 4. Communication Coupling (MEDIUM)
```python
# Current
events_file = "~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml"

# Should be
events_file = config.communication.events_path
```

## Decoupling Strategy

### Phase 1: Configuration-Driven
- Create agent-config.yaml
- Move all hardcoded values to config
- Update agents to read from config

### Phase 2: Interface Standardization
- Create base Agent class
- Define standard inputs/outputs
- Make agents project-agnostic

### Phase 3: Project Initialization
- Create project init tool
- Generates config from template
- Sets up required directories

## Success Criteria
- [ ] All hardcoded paths removed from agents
- [ ] Agent-config.yaml created and used
- [ ] Agents work with any project directory
- [ ] Base Agent class created
- [ ] Project initialization tool created
- [ ] Tests verify agents work with different projects

## Context
- Scout report: `.autonomous/analysis/scout-agent-architecture.md`
- Agent scripts: `2-engine/.autonomous/bin/`

## Approach
1. Create agent-config.yaml schema
2. Create base Agent class
3. Update scout-intelligent.py
4. Update planner-prioritize.py
5. Update executor-implement.py
6. Update verifier-validate.py
7. Create project init tool
8. Test with mock project

## Dependencies
- TASK-ARCH-065 (path library)
- TASK-ARCH-066 (unify communication)

## Rollback Strategy
- Keep hardcoded versions as backup
- Feature flag for new config-driven mode

## Estimated Effort
8-10 hours

## Related Tasks
- TASK-ARCH-061: Migrate engine scripts to project
- TASK-ARCH-063: Standardize project content to engine
