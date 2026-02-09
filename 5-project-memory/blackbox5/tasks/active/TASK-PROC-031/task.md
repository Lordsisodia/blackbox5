# TASK-PROC-031: Task Selection Randomization

**Status:** completed
**Priority:** MEDIUM
**Category:** process
**Estimated Effort:** 45 minutes
**Created:** 2026-02-09
**Completed:** 2026-02-09
**Source:** Process improvement initiative

---

## Objective

Add randomization to task selection to prevent always picking the same tasks from the highest priority group, ensuring fairness and preventing task starvation.

---

## Success Criteria

- [x] Random selection among highest priority tasks implemented
- [x] Configurable randomization factor added to config
- [x] Fairness mechanism to prevent task starvation
- [x] Randomization can be enabled/disabled via config
- [x] Test selection behavior works correctly
- [x] Documentation updated

---

## Context

**Current Behavior:**
The task selection in `storage_backend.py` always picked the first task from the sorted list (highest priority_score). This led to:
- Same tasks being picked repeatedly
- Task starvation for equally important tasks
- Lack of diversity in task execution

**Solution Implemented:**
- Among tasks with the same highest priority, randomly select one based on weighted probability
- Configurable randomization factor (0-1) controls randomness vs determinism
- Track selection count to ensure fairness (prevent starvation)

---

## Implementation

### Files Modified

1. **`/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.ralf/config.yaml`**
   - Added `task_selection` configuration section
   - Config options:
     - `randomization_enabled`: true/false
     - `randomization_factor`: 0.0-1.0 (0=deterministic, 1=fully random)
     - `fairness_window`: Number of selections to track
     - `fairness_boost_factor`: How much to boost unselected tasks

2. **`/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/lib/storage_backend.py`**
   - Added `random` import
   - Added `_load_task_selection_config()` method
   - Added `_apply_randomization()` method with weighted random selection
   - Added `_update_selection_tracking()` for fairness tracking
   - Added `select_next_task()` method as primary selection API
   - Added CLI commands: `select` and `test-selection`

### Selection Algorithm

1. Get all ready tasks (pending, no dependencies, not claimed)
2. Group tasks by priority level (CRITICAL > HIGH > MEDIUM > LOW)
3. Within highest priority group with ready tasks:
   - Calculate weight for each task: `(1 - rf) * priority_score + rf * fairness_boost`
   - `rf` = randomization_factor
   - `fairness_boost` decreases with recent selections
4. Perform weighted random selection
5. Return selected task first in list

### Test Results

**With randomization disabled:**
```
ACTION-PLAN-youtube-pipeline: 10/10 (100%) - Always picks same task
```

**With randomization_factor = 0.3 (default):**
```
TASK-AUTO-015:                12/20 (60.0%)
ACTION-PLAN-youtube-pipeline:  8/20 (40.0%)
Fairness CV: 28.3%
```

**With randomization_factor = 0.8:**
```
TASK-AUTO-015:                10/20 (50.0%)
ACTION-PLAN-youtube-pipeline: 10/20 (50.0%)
Fairness CV: 0.0% (perfect distribution)
```

---

## Usage

### Test Selection Behavior
```bash
python3 /Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/lib/storage_backend.py --project blackbox5 test-selection --iterations 20
```

### Select Next Task
```bash
python3 /Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/lib/storage_backend.py --project blackbox5 select
```

### Configuration
Edit `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.ralf/config.yaml`:
```yaml
task_selection:
  randomization_enabled: true
  randomization_factor: 0.3
  fairness_window: 5
  fairness_boost_factor: 1.5
```

---

## Rollback Strategy

If changes cause issues:
1. Set `randomization_enabled: false` in config.yaml
2. Or revert to previous version of storage_backend.py

---

## Notes

The implementation ensures:
- **Backward compatibility**: Randomization is opt-in via config
- **Fairness**: Tasks not recently selected get preference
- **Configurability**: Fine-tune randomness vs determinism
- **Transparency**: Test command shows selection distribution
