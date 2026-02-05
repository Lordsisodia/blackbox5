# PLAN.md: Fix Goal Status Mismatches

**Task:** TASK-SSOT-008 - Goal status in goals/active vs timeline.yaml mismatch
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 2-3 hours
**Importance:** 60 (Medium)

---

## 1. First Principles Analysis

### The Core Problem
Goal status is tracked in multiple places:
- `5-project-memory/blackbox5/goals/active/[ID]/goal.yaml` - Goal file
- `5-project-memory/blackbox5/timeline.yaml` - Timeline tracking
- `5-project-memory/blackbox5/STATE.yaml` - State summary

This creates:
1. **Status Mismatches**: Same goal shows different status in different files
2. **Manual Updates**: Must update multiple files when status changes
3. **Inconsistency**: Timeline may show completed while goal shows active
4. **Reporting Errors**: Dashboards show incorrect goal status

### First Principles Solution
- **Source of Truth**: Goal file is canonical
- **Derived Data**: Timeline/STATE derive from goal files
- **Single Update**: Change status in one place only
- **Validation**: Automated checks for consistency

---

## 2. Current State Analysis

### Files Involved

| File | Status Field | Purpose |
|------|--------------|---------|
| goals/active/IG-001/goal.yaml | `status` | Goal definition |
| timeline.yaml | `goals[ig-001].status` | Timeline tracking |
| STATE.yaml | `active_goals` | State summary |

### Example Mismatch

```yaml
# goals/active/IG-001/goal.yaml
status: completed

# timeline.yaml
goals:
  ig-001:
    status: in_progress  # MISMATCH!

# STATE.yaml
active_goals:
  - IG-001  # Should not be in active if completed
```

---

## 3. Proposed Solution

### Step 1: Audit Mismatches (30 min)

1. Read all goal files
2. Read timeline.yaml
3. Read STATE.yaml
4. Identify all mismatches

### Step 2: Fix Current Mismatches (30 min)

1. Update timeline.yaml to match goal files
2. Update STATE.yaml to match goal files
3. Document any discrepancies found

### Step 3: Create Derivation Script (1 hour)

**File:** `2-engine/.autonomous/lib/goal_utils.py`

```python
def get_goal_status(goal_id: str) -> str:
    """Get goal status from canonical source (goal.yaml)."""
    goal_path = get_project_path() / "goals" / "active" / goal_id / "goal.yaml"
    if goal_path.exists():
        goal = yaml.safe_load(goal_path.read_text())
        return goal.get("status", "unknown")
    return "not_found"

def get_all_goal_statuses() -> Dict[str, str]:
    """Get all goal statuses from goal files."""
    goals_dir = get_project_path() / "goals" / "active"
    statuses = {}
    for goal_dir in goals_dir.iterdir():
        if goal_dir.is_dir():
            goal_id = goal_dir.name
            statuses[goal_id] = get_goal_status(goal_id)
    return statuses

def sync_timeline_goals():
    """Sync timeline.yaml with actual goal statuses."""
    statuses = get_all_goal_statuses()
    # Update timeline.yaml with correct statuses
```

### Step 4: Update Scripts (1 hour)

Update all scripts that read goal status:

```python
# Before
with open("timeline.yaml") as f:
    timeline = yaml.safe_load(f)
status = timeline["goals"][goal_id]["status"]

# After
from goal_utils import get_goal_status
status = get_goal_status(goal_id)
```

---

## 4. Files to Modify

### New Files
1. `2-engine/.autonomous/lib/goal_utils.py` - Goal utilities

### Modified Files
1. `5-project-memory/blackbox5/timeline.yaml` - Fix mismatches
2. `5-project-memory/blackbox5/STATE.yaml` - Fix mismatches
3. Scripts reading goal status

---

## 5. Success Criteria

- [ ] All goal status mismatches identified and fixed
- [ ] goal_utils.py created with get_goal_status()
- [ ] All scripts updated to use canonical source
- [ ] Validation script created to prevent future mismatches
- [ ] Documentation updated

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Restore original timeline.yaml and STATE.yaml
2. **Fix**: Debug derivation logic
3. **Re-apply**: Once fixed

---

## 7. Estimated Timeline

| Step | Duration | Cumulative |
|------|----------|------------|
| Step 1: Audit | 30 min | 30 min |
| Step 2: Fix Mismatches | 30 min | 1 hour |
| Step 3: Derivation Script | 1 hour | 2 hours |
| Step 4: Update Scripts | 1 hour | 3 hours |
| **Total** | | **2-3 hours** |

---

*Plan created based on SSOT violation analysis - Goal status mismatches*
