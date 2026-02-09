# TASK-RALF-003: Decouple RALF from Skill System

**Status:** completed
**Priority:** HIGH
**Parent:** Issue #4 - RALF Knows Project Structure
**Completed:** 2026-02-08

## Objective
Make RALF's skill system optional and decoupled from BlackBox5-specific implementation.

## Changes Made

### Phase 1: Extract Skill Interface
Created `2-engine/.autonomous/lib/skill_provider.py` with:
- `SkillProvider` abstract interface with 7 methods
- `NullSkillProvider` no-op implementation for projects without skills
- `BlackBox5SkillProvider` BB5-specific implementation
- `ConfigDrivenSkillProvider` generic config-based implementation
- `get_skill_provider()` factory function for auto-detection
- `check_skills_enabled()` convenience function

### Phase 2: Create RALF Configuration System
Created `2-engine/.autonomous/lib/ralf_config.py` with:
- `RalfConfig` dataclass with all configuration options
- Environment variable support (RALF_*)
- YAML config file support (ralf-config.yaml)
- Feature flags for gradual rollout

### Phase 3: Update RALF Components

#### ralf-planner
- Added config loading from ralf-config.yaml
- Added environment variable overrides
- Added `select_skill_for_task()` function using skill provider
- Skill selection is now optional based on `SKILLS_ENABLED` flag

#### ralf-executor
- Added config loading from ralf-config.yaml
- Added `get_skill_guidance()` function using skill provider
- Added `AUTO_COMMIT` support
- Skill guidance is now optional

#### collect-skill-metrics.py
- Fixed hardcoded absolute path on line 11
- Now uses `PROJECT_DIR` environment variable with fallback
- Path is now: `PROJECT_DIR / 'operations' / 'skill-metrics.yaml'`

### Phase 4: Configuration File
Created `5-project-memory/blackbox5/ralf-config.yaml` with default settings:
```yaml
skills_enabled: true
skill_provider_type: auto
auto_commit: false
idle_timeout: 300
loop_interval: 30
queue_target: 5
queue_min: 2
```

### Phase 5: Testing
Created `2-engine/.autonomous/lib/test_skill_provider.py` with comprehensive tests:
- NullSkillProvider returns safe defaults
- ConfigDrivenSkillProvider works with generic config
- Factory function correctly selects provider type
- check_skills_enabled works correctly
- BlackBox5SkillProvider handles missing registry gracefully

**All tests pass.**

## Success Criteria
- [x] Create `SkillProvider` abstract interface
- [x] Create `BlackBox5SkillProvider` implementation
- [x] Create `NullSkillProvider` for projects without skills
- [x] Update ralf-planner to use skill provider
- [x] Update ralf-executor to use skill provider
- [x] Fix absolute path in `collect-skill-metrics.py`
- [x] RALF works gracefully when skill system disabled

## Files Created
1. `2-engine/.autonomous/lib/skill_provider.py` - Skill provider interface
2. `2-engine/.autonomous/lib/ralf_config.py` - RALF configuration system
3. `2-engine/.autonomous/lib/test_skill_provider.py` - Test suite
4. `5-project-memory/blackbox5/ralf-config.yaml` - Default config

## Files Modified
1. `bin/ralf-tools/ralf-planner` - Added skill provider integration
2. `bin/ralf-tools/ralf-executor` - Added skill provider integration
3. `5-project-memory/blackbox5/bin/collect-skill-metrics.py` - Fixed hardcoded path

## Usage

### Disable Skills
```bash
export RALF_SKILLS_ENABLED=false
# or set in ralf-config.yaml:
# skills_enabled: false
```

### Use Generic Skills (Non-BB5)
Create `ralf-skills.yaml` in project root:
```yaml
skills:
  my-skill:
    name: "My Skill"
    keywords:
      - keyword1
      - keyword2
```

### Use BB5 Skills
Keep `operations/skill-registry.yaml` - auto-detected.

## Rollback Strategy
All changes are backward compatible:
- Default behavior unchanged (skills enabled)
- BB5 skill registry still auto-detected
- Environment variables can override any setting
- Null provider provides safe fallbacks
