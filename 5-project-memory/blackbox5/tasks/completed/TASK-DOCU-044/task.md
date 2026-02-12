# TASK-DOCU-044: Task System Design References Non-Existent Files

**Status:** completed
**Priority:** LOW
**Category:** documentation
**Estimated Effort:** 30 minutes
**Created:** 2026-02-05T01:57:10.950095
**Source:** Scout opportunity docs-006 (Score: 7.0)

---

## Objective
Verify if tasks.yaml and queue.yaml exist in the communications folder as referenced in documentation.



---

## Success Criteria

- [x] Understand the issue completely
- [x] Implement the suggested action
- [x] Validate the fix works
- [x] Document changes in LEARNINGS.md

---

## Context

**Suggested Action:** Verify if tasks.yaml and queue.yaml exist in communications folder

**Files to Check/Modify:**

---

## Rollback Strategy

If changes cause issues:
1. Revert to previous state using git
2. Document what went wrong
3. Update this task with learnings

---

## Notes

**Completed:** 2026-02-12

### Investigation Findings

After investigating the communications folder structure, here's what was found:

#### 1. Communications Locations
There are TWO communications folders in the BlackBox5 structure:

**Top-level communications folder:**
```
/opt/blackbox5/5-project-memory/blackbox5/.autonomous/communications/
└── queue-core.yaml  (10 bytes, contains: `tasks: []`)
```

**Agent-level communications folder:**
```
/opt/blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/
├── agent-state.yaml
├── chat-log.yaml
├── events.yaml
├── heartbeat.yaml
├── protocol.yaml
└── queue.yaml         ✅ (26KB, active queue file)
```

#### 2. File Existence Verification

| File Referenced | Expected Location | Actual Location | Status |
|----------------|-------------------|-----------------|---------|
| `queue.yaml` | `.autonomous/communications/` | `.autonomous/agents/communications/` | ✅ Exists (different location) |
| `tasks.yaml` | `.autonomous/communications/` | Not found | ❌ Does not exist |

#### 3. Documentation Issues

Multiple documentation files incorrectly reference `communications/queue.yaml` at the top level:

- `DUAL-RALF-ARCHITECTURE.md` - References `communications/queue.yaml` (should be `agents/communications/queue.yaml`)
- `research-pipeline/context/routes.yaml` - Has `queue: "communications/queue.yaml"`
- `research-pipeline/.templates/prompts/planner-worker.md` - Multiple incorrect references

#### 4. Root Cause

The documentation was written assuming a flat structure where communications/ is at the top level of .autonomous/. However, the actual implementation uses a nested structure where communications/ is under agents/. This is the correct structure according to `README.md` which shows:

```
.autonomous/
└── agents/
    └── communications/        # Agent coordination
        ├── agent-state.yaml
        ├── queue.yaml
        └── ...
```

### Resolution

**No code changes required** - The files exist in the correct location per the actual architecture. The documentation needs to be updated to reflect the correct path structure.

### Recommendations

1. Update documentation to reference `agents/communications/queue.yaml` instead of `communications/queue.yaml`
2. Verify if `queue-core.yaml` in top-level communications/ is still needed or if it's legacy
3. Standardize path references across all documentation files

### Files Reviewed
- `/opt/blackbox5/5-project-memory/blackbox5/.autonomous/communications/queue-core.yaml`
- `/opt/blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/queue.yaml`
- `/opt/blackbox5/5-project-memory/blackbox5/.autonomous/README.md`
- `/opt/blackbox5/5-project-memory/blackbox5/.autonomous/DUAL-RALF-ARCHITECTURE.md`
- Multiple research-pipeline prompt files
