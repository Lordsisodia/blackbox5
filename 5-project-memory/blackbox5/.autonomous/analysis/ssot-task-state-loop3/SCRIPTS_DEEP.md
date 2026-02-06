# SSOT Task State: Loop 3 Deep Dive - Script Dependencies

**Scout:** Architecture Analysis Agent (Loop 3)
**Date:** 2026-02-06
**Previous Scouts:** 10 agents

---

## Critical Finding: No Unified State Management Layer

Each script independently reads/writes YAML files with:
- Different parsing methods (yq, awk, Python yaml)
- Different error handling (some fail, some silently continue)
- **No synchronization** between related state changes
- **No validation** that cross-file references are consistent

---

## 1. STATE.yaml Dependencies

**Scripts that READ STATE.yaml:**
| Script | Line | Breaks When Stale |
|--------|------|-------------------|
| `bin/ralf-planner` | 157 | Plans wrong tasks |
| `bin/verify-task` | 121-147 | Reports stale as fresh |
| `validate-ssot.py` | 42-77 | Validates structure not content |

**Scripts that WRITE STATE.yaml:**
| Script | Status | Issue |
|--------|--------|-------|
| `sync-state.py` | EXISTS but NOT RUN | Has TODO for STATE.yaml update |
| `ralf-executor:mark_task_complete()` | PLACEHOLDER | Line 220-223: Just logs "placeholder" |

---

## 2. queue.yaml Has DUAL LOCATIONS

**Location 1**: `.autonomous/agents/communications/queue.yaml` (90 tasks)
**Location 2**: Referenced as `.autonomous/communications/queue.yaml` in some scripts

**Scripts Reading queue.yaml:**
| Script | Lines | Purpose |
|--------|-------|---------|
| `bb5-queue-manager.py` | 241-282 | Loads queue for prioritization |
| `ralf-task-select.sh` | 72, 93-104 | Claims tasks - uses awk parsing |
| `ralf-planner-v2` | 138-143 | Reads queue depth |
| `ralf-executor` | 136-138 | Gets next task |
| `ralf-architect` | 134-139 | Reads for context |
| `ralf-stop-hook.sh` | 274-289 | Updates task status |
| `subagent-tracking.sh` | 55-57, 133-137 | Queries parent_task |

---

## 3. CRITICAL RACE CONDITIONS

**Multiple scripts write to queue.yaml simultaneously:**
- `ralf-planner` adds tasks (line 141)
- `ralf-executor` removes completed tasks (lines 179-211)
- `ralf-task-select.sh` updates status with `awk` (lines 134-145)
- `bb5-queue-manager.py` saves prioritized queue (lines 318-334)

**No file locking mechanism found.**

---

## 4. timeline.yaml Corruption

**Scripts Writing timeline.yaml:**
| Script | Trigger | Issue |
|--------|---------|-------|
| `bb5-timeline` | Manual CLI | Uses awk to insert - no validation |
| `timeline-maintenance.sh` | PostToolUse | Auto-injects phantom tasks with numeric IDs |
| `stop-hierarchy-update.sh` | Stop hook | Updates goal timelines |

**Issue:** timeline-maintenance.sh injects events with broken `related_items`:
- `related_items: ["11"]` - numeric IDs without TASK- prefix
- `related_items: ["TASK-INFR-010"]` - correct format
- Mixed formats cause confusion

---

## 5. events.yaml - Append-Only Corruption Risk

**Scripts Writing events.yaml:**
| Script | Method | Risk |
|--------|--------|------|
| `ralf-executor:add_event()` | Python YAML dump | Safe, truncates to last 100 |
| `ralf-task-select.sh` | `cat >>` append | **DANGEROUS** - Raw text append |
| `ralf-stop-hook.sh` | Python inline | Updates queue and events |
| `subagent-tracking.sh` | Python inline | Event injection |

**CRITICAL ISSUE** - `ralf-task-select.sh` (lines 119-127):
```bash
cat >> "$EVENTS_FILE" << EOF
- timestamp: "$TIMESTAMP"
  task_id: "$NEXT_TASK"
  type: started
EOF
```

This assumes events.yaml is a simple list. If file has YAML structure, this **breaks the format**.

---

## 6. Missing Sync Mechanisms - "Ghost State" Problem

**No Atomic Updates:** When task completes:
1. `ralf-executor` removes from queue.yaml
2. `stop-hierarchy-update.sh` updates task.md status
3. `timeline-maintenance.sh` adds timeline event
4. **STATE.yaml is NEVER updated** (sync-state.py exists but isn't called)

**Orphaned Task Directories:** 97 tasks exist in filesystem but not in queue.yaml
- Scripts scan `tasks/active/` for filesystem state
- queue.yaml is "source of truth" for execution
- **Result:** Tasks exist but are invisible to RALF

---

## 7. Error Handling - "Silent Failures"

**Scripts with NO error handling:**
| Script | Line | Behavior |
|--------|------|----------|
| `ralf-planner` | 77 | yq returns "0" if queue.yaml missing - silently continues |
| `ralf-executor` | 137 | yq returns empty if queue.yaml missing - idle loop |

**Only script that fails properly:** `bb5-timeline` (line 48) exits with error

---

## 8. Hook Scripts - Hidden State Dependencies

**Session Start Hooks** (read state):
| Hook | Files Read | Purpose |
|------|-----------|---------|
| `session-start-blackbox5.sh` | queue.yaml, events.yaml | Build agent context |
| `session-start-navigation.sh` | timeline.yaml | Validate structure |
| `subagent-tracking.sh` | queue.yaml | Find parent_task |

**Post-Tool Hooks** (write state):
| Hook | Writes To | Trigger |
|------|-----------|---------|
| `timeline-maintenance.sh` | timeline.yaml | TaskUpdate, Write, Edit |
| `subagent-tracking.sh` | events.yaml | Tool use tracking |

**Stop Hooks** (write state):
| Hook | Writes To | Issue |
|------|-----------|-------|
| `stop-hierarchy-update.sh` | task.md, timeline.yaml | Updates status but not queue.yaml |
| `ralf-stop-hook.sh` | queue.yaml, events.yaml | Only runs on RALF stop |

---

## 9. What Breaks When State is Wrong

| Scenario | Impact |
|----------|--------|
| queue.yaml corrupted | RALF executor idle loops - no work |
| STATE.yaml stale | Planner plans wrong tasks |
| timeline.yaml phantom tasks | False progress reporting |
| events.yaml format broken | Event tracking fails |
| Missing sync | "Ghost tasks" - exist but invisible |

---

## What Previous Scouts Missed

| Finding | Severity |
|---------|----------|
| Race conditions in queue.yaml writes | CRITICAL |
| Raw text append to events.yaml | CRITICAL |
| No file locking mechanism | CRITICAL |
| Silent failures on missing files | HIGH |
| Hook script state dependencies | HIGH |
| Missing atomic updates | HIGH |

---

## Conclusion

**The Real Problem:** There is no unified state management layer. Scripts maintain state independently with no coordination, creating a system that appears to work but produces increasingly divergent "truths" about project state.

**The state files aren't just corrupted - they're maintained by a web of uncoordinated scripts.**
