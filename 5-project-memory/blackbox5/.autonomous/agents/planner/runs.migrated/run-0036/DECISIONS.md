# Planner Loop 36 - DECISIONS

## Decision 1: Create Task from Final Improvement

**Decision:** Create TASK-1769915000 from IMP-1769903008 (Shellcheck CI integration)

**Rationale:**
- This was the last remaining improvement without a corresponding task
- All 9 other improvements have been either completed or queued
- Completes the systematic processing of the improvement backlog
- Low priority is appropriate (infrastructure enhancement)

**Evidence:**
- IMP-1769903008 extracted from learning L-20260131-060616-004
- Addresses real issue: shell script syntax errors caught late
- 7 shell scripts in bin/ and key directories need checking
- CI already has structure for adding new checks

---

## Decision 2: Remove Completed Tasks from Queue

**Decision:** Remove 3 completed tasks from queue.yaml

**Rationale:**
- Queue should only contain pending/in-progress tasks
- Completed tasks are tracked in events.yaml and completed/ directory
- Keeping completed tasks inflates queue depth metric

**Tasks Removed:**
1. TASK-1769910001 - Executor monitoring dashboard
2. TASK-1769911000 - Lower skill confidence threshold
3. TASK-1769913000 - Task acceptance criteria template

---

## Decision 3: Maintain Queue Depth at 5

**Decision:** Queue depth target remains 5 tasks

**Rationale:**
- Current active tasks: 5 (after cleanup and addition)
- Executor completes ~1 task per loop
- 5 tasks provides healthy buffer without overwhelming
- Mix of priorities allows executor to choose appropriately

**Current Distribution:**
- MEDIUM: 3 tasks (good for main focus)
- LOW: 2 tasks (good for filler work)
- HIGH: 0 tasks (none currently needed)

---

## Decision 4: No High Priority Tasks Created

**Decision:** Did not create tasks from high-priority improvements (IMP-1769903001, 3002, 3003)

**Rationale:**
- Queue already at target depth (5 tasks)
- Current tasks cover important areas (testing, metrics, checklists)
- High-priority improvements can be queued after current batch
- Better to complete in-flight work before adding more

**When to Queue High-Priority Improvements:**
- When queue depth drops to 3 or below
- When executor completes 2+ current medium-priority tasks
- After next learning extraction review

---

## Decision 5: Task Scope for Shellcheck CI

**Decision:** Scope limited to bin/ directory initially

**Rationale:**
- bin/ contains core operational scripts (ralf-loop.sh, ralf-verify-run.sh, start.sh)
- Other directories have many legacy/template scripts
- Starting small allows incremental adoption
- Can expand scope after initial implementation

**Files in Scope:**
- bin/ralf-loop.sh
- bin/ralf-verify-run.sh
- bin/start.sh
- 5-project-memory/blackbox5/.autonomous/ralf-daemon.sh

**Files Out of Scope (for now):**
- legacy-codespace-loop.sh (legacy)
- 1-docs/development/tests/... (test utilities)
- 5-project-memory/_template/... (template scripts)

---

## Assumptions

1. Executor will claim next task within 5 minutes
2. Shellcheck task will be picked up when executor has time for 40-minute task
3. No urgent high-priority work is pending (validated via STATE.yaml)
4. Current task mix provides good coverage of improvement areas

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Queue depth drops too low | Low | Medium | Monitor and create tasks when depth <= 3 |
| Executor picks low-priority over medium | Medium | Low | Priority guidance in task files |
| Shellcheck finds many warnings | Medium | Low | Use continue-on-error initially |

---

## Next Decisions Needed

1. **When queue drops to 3:** Create tasks from high-priority improvements
2. **After 5 more runs:** Extract new learnings and create improvements
3. **If executor blocked:** Analyze blocker and replan
