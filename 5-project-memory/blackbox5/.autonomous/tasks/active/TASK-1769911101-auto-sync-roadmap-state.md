# TASK-1769911101: Implement Automatic Roadmap State Synchronization

**Type:** implement
**Priority:** high
**Status:** pending
**Created:** 2026-02-01T14:55:00Z
**Improvement:** IMP-1769903001

## Objective

Implement automatic synchronization between task completion and roadmap STATE.yaml to prevent drift between documented state and actual state.

## Context

**Chronic Issue:** STATE.yaml frequently drifts from reality:
- Plans marked "planned" when work is complete
- next_action pointing to completed work
- Duplicate tasks created due to stale state
- 7+ learnings mention this issue

**Evidence:**
- L-1769861933: "Roadmap State Can Become Outdated"
- L-1769813746: "Plan Completion Tracking Gap"
- L-20260131-060933: "Roadmap State Can Drift from Reality"
- L-1769807450: "Roadmap State Decay"

**Impact:**
- Duplicate tasks created (see TASK-1769914000 double execution)
- Confusion about what work remains
- Wasted time on completed work
- Manual STATE.yaml updates required

## Success Criteria

- [ ] Roadmap sync library created in `2-engine/.autonomous/lib/roadmap_sync.py`
- [ ] Post-task-completion hook updates STATE.yaml automatically
- [ ] Plan status changes "planned" → "completed" when task finishes
- [ ] Dependent plans automatically unblocked when prerequisite completes
- [ ] next_action updated to next unblocked plan
- [ ] No manual STATE.yaml updates required for standard task completion
- [ ] Tested with at least 2 plan completions
- [ ] Documentation created in `operations/.docs/roadmap-sync-guide.md`

## Approach

### Phase 1: Create Sync Library (20 min)
1. Create `2-engine/.autonomous/lib/roadmap_sync.py`
2. Implement core functions:
   - `update_plan_status(plan_id, status)` - Change plan status
   - `unblock_dependents(plan_id)` - Unblock plans that depend on completed plan
   - `update_next_action()` - Set next_action to next unblocked plan
   - `find_plan_by_task_id(task_id)` - Locate plan from completed task
3. Add STATE.yaml parsing and updating logic
4. Include validation to prevent corruption

### Phase 2: Create Completion Hook (10 min)
1. Add hook to Executor task completion workflow
2. After marking task complete: trigger roadmap sync
3. Hook should:
   - Extract task ID from completed task
   - Find associated plan in STATE.yaml
   - Update plan status to "completed"
   - Unblock dependent plans
   - Update next_action
4. Log all STATE.yaml changes

### Phase 3: Integrate into Workflow (10 min)
1. Modify Executor prompt to call sync hook
2. Add to "Task Completion" section
3. Update task completion template to include sync step
4. Add error handling for sync failures

### Phase 4: Test and Validate (5 min)
1. Create test plan in STATE.yaml
2. Create associated task
3. Complete task and verify STATE.yaml updated
4. Check dependent plans unblocked
5. Verify next_action updated correctly

## Files to Modify

- `2-engine/.autonomous/lib/roadmap_sync.py` (create)
  - Core sync logic
  - STATE.yaml parsing/updating
  - Plan finding and status updates

- `2-engine/.autonomous/prompts/system/executor/variations/v2-legacy-based.md`
  - Add sync call to task completion workflow
  - Section: "Final Step: Update Metadata and Signal Completion"

- `.templates/tasks/task-completion.md.template` (if exists)
  - Add roadmap sync step to completion checklist

- `operations/.docs/roadmap-sync-guide.md` (create)
  - How roadmap sync works
  - What gets updated automatically
  - Manual STATE.yaml updates still needed

## Notes

**Sync Strategy:**
1. When task completes, extract task ID
2. Search STATE.yaml for plan with matching task_id
3. Update plan status: "planned" → "completed"
4. Find all plans with dependencies on this plan
5. Remove those dependencies or mark plans as "unblocked"
6. Set next_action to first unblocked "planned" plan

**Example Implementation:**
```python
def sync_roadmap_on_task_completion(task_id, state_yaml_path):
    """Update STATE.yaml when task completes"""
    state = yaml.safe_load(open(state_yaml_path))

    # Find plan associated with this task
    for plan in state['plans']:
        if plan.get('task_id') == task_id:
            plan['status'] = 'completed'

            # Unblock dependent plans
            for other_plan in state['plans']:
                if task_id in other_plan.get('dependencies', []):
                    other_plan['dependencies'].remove(task_id)

            # Update next_action
            completed = [p for p in state['plans'] if p['status'] == 'completed']
            unblocked = [p for p in state['plans']
                        if p['status'] == 'planned'
                        and not p.get('dependencies')]
            if unblocked:
                state['next_action'] = unblocked[0]['id']

            break

    # Write updated state
    with open(state_yaml_path, 'w') as f:
        yaml.dump(state, f)
```

**Handling Edge Cases:**
- Task not associated with any plan → skip sync
- Plan already marked completed → log warning, skip
- STATE.yaml file missing → log error, continue
- Corrupted STATE.yaml → do not update, log error

**Dependencies:**
- Related to improvement IMP-1769903001
- Supports IMP-1769903003 (duplicate detection)
- Reduces need for IMP-1769903002 (pre-execution research)

**Estimated Time:** 45 minutes
**Context Level:** 2 (moderate complexity)
**Risk:** Medium (modifies STATE.yaml which is critical)

**Warnings:**
- Test thoroughly with STATE.yaml backup
- Add validation to prevent corruption
- Log all STATE.yaml changes
- If sync fails, should not block task completion
- Monitor first 10 syncs to ensure accuracy
