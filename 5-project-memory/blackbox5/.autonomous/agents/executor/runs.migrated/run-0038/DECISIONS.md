# Decisions - TASK-1769911101

## Decision 1: Library-Based vs. Inline Implementation

**Context:** Need to implement roadmap sync functionality that can be called from Executor and potentially other agents.

**Selected:** Library-based approach (`roadmap_sync.py`)

**Rationale:**
- **Reusability:** Can be called from Executor, Planner, or manual CLI
- **Testability:** Easy to test independently with `--dry-run` flag
- **Maintainability:** Single source of truth for sync logic
- **Modularity:** Clean separation of concerns (sync logic vs. execution logic)
- **Extensibility:** Easy to add new features (webhooks, dashboards, etc.)

**Alternatives Considered:**
1. Inline bash scripts in Executor prompt
   - Rejected: Hard to test, hard to reuse, harder to maintain
2. Built-in to Executor code (if Executor was Python)
   - Rejected: Executor is currently prompt-based, not code-based
3. External service/microservice
   - Rejected: Overkill for this use case, adds complexity

**Reversibility:** HIGH - Can replace library with different implementation without breaking Executor (just change the call)

---

## Decision 2: Non-Blocking Sync Behavior

**Context:** Roadmap sync is a side effect of task completion, not part of the core work.

**Selected:** Non-blocking (sync failures do not prevent task completion)

**Rationale:**
- **Resilience:** Task completion should succeed even if STATE.yaml is temporarily unavailable
- **No single point of failure:** Sync issues do not block all work
- **Graceful degradation:** Manual STATE.yaml updates are always possible
- **User experience:** Executor does not stall on sync issues

**Behavior:**
- Sync failures logged but do not return error code
- Task completion proceeds normally after sync failure
- Executor continues with git commit and push
- No manual intervention required

**Alternatives Considered:**
1. Blocking sync (fail task if sync fails)
   - Rejected: Would block all work on STATE.yaml issues
2. Optional sync (only run if flag set)
   - Rejected: Would be forgotten, defeats purpose

**Reversibility:** MEDIUM - Would require Executor prompt change to make blocking

---

## Decision 3: Multi-Method Plan Detection

**Context:** STATE.yaml structure does not store task_id in plans. Need to find which plan a task belongs to.

**Selected:** Multi-method detection approach (3 methods, tried in sequence)

**Methods:**
1. **Content search:** Parse task file content for "PLAN-XXX" patterns
2. **Task ID pattern:** Extract from task ID (e.g., `TASK-XXX-plan-003`)
3. **Filename pattern:** Extract from filename with regex

**Rationale:**
- **High success rate:** Multiple methods increase likelihood of finding plan
- **Flexible:** Works with various task naming conventions
- **Graceful failure:** If no plan found, treats as success (task may not be associated with a plan)
- **No data migration:** Does not require changes to STATE.yaml structure

**Alternatives Considered:**
1. Add task_id field to STATE.yaml plans
   - Rejected: Requires STATE.yaml schema change, migration effort
2. Manual mapping file (task_id → plan_id)
   - Rejected: Additional maintenance burden, sync issues
3. Require task files to always specify plan_id in metadata
   - Rejected: Breaking change for existing task format

**Reversibility:** HIGH - Can add more detection methods or change priority without breaking existing functionality

---

## Decision 4: Automatic Backups Before Modification

**Context:** STATE.yaml is critical file. Corruption would be disastrous.

**Selected:** Automatic timestamped backups before every modification

**Implementation:**
```python
backup_path = f"{state_yaml_path}.backup.{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
shutil.copy2(state_yaml_path, backup_path)
```

**Rationale:**
- **Safety:** Can always recover from corruption or error
- **Audit trail:** Backups show history of changes
- **Rollback:** Easy to undo incorrect syncs
- **Zero cost:** Disk space is cheap, backups are small (KB range)

**Alternatives Considered:**
1. Git-based rollback
   - Rejected: Requires git operations, adds complexity, not always available
2. No backups (validation only)
   - Rejected: Too risky, single error could corrupt STATE.yaml
3. Manual backups before sync
   - Rejected: Would be forgotten, defeats purpose

**Reversibility:** LOW - Removing backups would reduce safety, but would not break functionality

---

## Decision 5: STATE.yaml Location (6-roadmap vs. Others)

**Context:** Found 3 different STATE.yaml files in the repository. Need to choose which one to sync.

**Options Found:**
1. `/workspaces/blackbox5/5-project-memory/blackbox5/STATE.yaml` (project state)
2. `/workspaces/blackbox5/.autonomous/STATE.yaml` (minimal, initialization)
3. `/workspaces/blackbox5/6-roadmap/STATE.yaml` (roadmap state)

**Selected:** `/workspaces/blackbox5/6-roadmap/STATE.yaml`

**Rationale:**
- **Correct structure:** Has `plans.ready_to_start`, `plans.blocked`, `plans.completed` sections
- **Active usage:** Recently updated (2026-02-01), contains current roadmap data
- **Plan references:** Contains actual PLAN-XXX entries with dependencies
- **Purpose-built:** Directory name (6-roadmap) indicates it's the roadmap file

**Evidence:**
- File contains 29 plans with proper structure
- Has `next_action` field pointing to PLAN-003
- Plans have dependencies, priorities, status
- Matches task description (references "plan completion tracking")

**Reversibility:** HIGH - Can change path in Executor prompt and documentation without breaking library

---

## Decision 6: Dry-Run Mode for Testing

**Context:** Need to test sync functionality without risking STATE.yaml corruption.

**Selected:** Implement `--dry-run` CLI flag that skips writing changes

**Rationale:**
- **Safe testing:** Can validate logic without touching STATE.yaml
- **Debugging:** Can see what would happen before running
- **Manual validation:** User can review changes before applying
- **CLI standard:** Common pattern for destructive operations

**Implementation:**
```bash
python3 roadmap_sync.py TASK-XXX /path/to/STATE.yaml --dry-run
```

**Behavior:**
- All logic runs normally
- Backup is NOT created
- STATE.yaml is NOT modified
- Results show what would have happened

**Alternatives Considered:**
1. Separate test STATE.yaml file
   - Rejected: Would not catch real-world issues
2. Git-based testing (test on branch)
   - Rejected: Too slow for quick validation
3. No dry-run mode (testing on production)
   - Rejected: Too risky

**Reversibility:** LOW - Removing dry-run would reduce testability but would not affect production behavior

---

## Decision 7: Idempotent Operations

**Context:** Sync might run multiple times for same task (e.g., retry, manual run).

**Selected:** Make all operations idempotent (safe to run multiple times)

**Implementation:**
- Check if plan already completed before moving
- Return success if already completed (with warning)
- No duplicate entries in completed section
- Dependencies list properly handles duplicate removals

**Rationale:**
- **Safety:** Running sync twice does not corrupt STATE.yaml
- **Retry-friendly:** Can retry failed syncs without side effects
- **Manual use:** Users can run manually without worrying about duplicates
- **Testing:** Easy to test same scenario multiple times

**Alternatives Considered:**
1. Fail if plan already completed
   - Rejected: Would block retries and manual runs
2. Always append to completed (create duplicates)
   - Rejected: Corrupts STATE.yaml with duplicates

**Reversibility:** LOW - Removing idempotency would make system less safe and harder to use

---

## Summary of Key Decisions

| Decision | Selection | Reversibility | Impact |
|----------|-----------|---------------|---------|
| Implementation | Library-based | HIGH | Modular, reusable, testable |
| Blocking behavior | Non-blocking | MEDIUM | Resilient, no single point of failure |
| Plan detection | Multi-method | HIGH | High success rate, flexible |
| Backups | Automatic | LOW | Safe, auditable, rollback-capable |
| STATE.yaml location | 6-roadmap | HIGH | Correct file for roadmap sync |
| Testing | Dry-run mode | LOW | Safe validation, debugging |
| Idempotency | Yes | LOW | Safe to retry, manual-friendly |

**Overall Philosophy:** Safety and resilience over optimization. Sync is a side effect, not a critical path. Failures should be graceful, not catastrophic.
