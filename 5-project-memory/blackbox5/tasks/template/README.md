# {TASK_ID}: {TASK_TITLE}

**Created:** {TIMESTAMP}
**Type:** {TASK_TYPE}
**Priority:** {PRIORITY}
**Assigned To:** {AGENT}

---

## Goal

{CLEAR_STATEMENT_OF_OBJECTIVE}

---

## Reasoning

{WHY_THIS_TASK_IS_IMPORTANT}

{LINK_TO_PLANNING_OR_ANALYSIS_DOCUMENTATION}

---

## Task Plan

See `PLAN.md` for detailed implementation steps.

---

## Quick Links

- **Task Context:** `TASK-CONTEXT.md` (filled by planning agent)
- **Active Context:** `ACTIVE-CONTEXT.md` (filled by execution agent)
- **Implementation Plan:** `PLAN.md`
- **Timeline:** `TIMELINE.md`
- **Changelog:** `CHANGELOG.md`

---

## Status

- **Created:** {TIMESTAMP}
- **Started:** {START_TIME}
- **Completed:** {COMPLETION_TIME}
- **Duration:** {ESTIMATED_DURATION}

---

## Execution Notes

This task folder contains all context, planning, and execution artifacts for tracking the complete lifecycle of this task.

### Folder Structure

```
{TASK_ID}/
├── README.md           # This file - task overview and links
├── TASK-CONTEXT.md     # Filled by planner - relevant files, routes, info
├── ACTIVE-CONTEXT.md   # Filled by executor - learnings and discoveries
├── PLAN.md             # Step-by-step implementation plan
├── TIMELINE.md         # Chronological log of all steps taken
├── CHANGELOG.md        # Detailed list of all modifications made
└── run-{TIMESTAMP}/    # Execution run folders (one per attempt)
    ├── THOUGHTS.md     # Narrative reasoning (process)
    ├── RESULTS.md      # Outcomes (what happened)
    ├── DECISIONS.md    # Key choices (why)
    └── metadata.yaml   # State + learnings + assumptions
```

### Context Files

**TASK-CONTEXT.md** (filled by planning agent):
- Links to all relevant files and routes
- Required background information
- Dependencies and prerequisites
- Architectural considerations

**ACTIVE-CONTEXT.md** (filled by execution agent):
- Lessons learned during execution
- Unexpected discoveries
- New patterns or approaches found
- Things to document for future tasks

### Execution Artifacts

Each execution attempt creates a `run-{TIMESTAMP}` folder containing:
- **THOUGHTS.md:** Step-by-step reasoning and decisions
- **RESULTS.md:** What actually happened (success/failure, outputs)
- **DECISIONS.md:** Key choices and their rationale
- **metadata.yaml:** Structured state (duration, exit status, learnings)

---

## Related Documentation

- **7-Phase Execution Flow:** See agent prompts for complete flow
- **Task Selection:** Run `bb5 task:select` or `python3 bin/ralf-task-select.py`
- **Completion:** Run `bb5 task:complete {TASK_ID}` or update STATE.yaml
