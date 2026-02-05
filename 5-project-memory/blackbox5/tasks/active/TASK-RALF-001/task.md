# TASK-RALF-001: Extract Hardcoded Paths from RALF Agent Scripts

**Status:** pending
**Priority:** CRITICAL
**Parent:** Issue #4 - RALF Knows Project Structure

## Objective
Remove all hardcoded paths from the 6 RALF agent scripts and replace with configuration.

## Files to Modify
1. `2-engine/.autonomous/bin/scout-intelligent.py` (lines 30-32)
2. `2-engine/.autonomous/bin/scout-task-based.py` (lines 23-25)
3. `2-engine/.autonomous/bin/planner-prioritize.py` (lines 23-26)
4. `2-engine/.autonomous/bin/executor-implement.py` (lines 25-29)
5. `2-engine/.autonomous/bin/verifier-validate.py` (lines 24-26)
6. `2-engine/.autonomous/bin/improvement-loop.py` (lines 24-27)

## Current Hardcoded Pattern
```python
PROJECT_DIR = Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"
ENGINE_DIR = Path.home() / ".blackbox5" / "2-engine"
```

## Target Pattern
```python
PROJECT_DIR = Path(os.environ.get("RALF_PROJECT_DIR", Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"))
ENGINE_DIR = Path(os.environ.get("RALF_ENGINE_DIR", Path.home() / ".blackbox5" / "2-engine"))
```

## Success Criteria
- [ ] All 6 scripts use environment variables for paths
- [ ] Scripts fall back to current hardcoded paths (backward compatibility)
- [ ] Scripts validate paths exist on startup
- [ ] Scripts provide helpful error messages if paths invalid
- [ ] Create `.env.example` documenting required variables

## Rollback Strategy
Revert to hardcoded paths if issues arise.
