# Incoming Feedback

**Purpose:** Raw feedback from RALF runs before processing

---

## How to Add Feedback

Create a new file following the naming convention:
```
FEEDBACK-{run-id}-{timestamp}.md
```

Example: `FEEDBACK-run-0001-20260130.md`

## File Format

```markdown
---
run_id: "run-0001"
timestamp: "2026-01-30T08:30:00Z"
type: "improvement"
category: "shell"
severity: "low"
---

# Brief Title

## Observation
What was noticed.

## Context
When/where it occurred.

## Suggestion
What could improve.

## Impact
Expected benefit.
```

## Types

- `improvement` - Make something better
- `bug` - Fix something broken
- `observation` - Notable pattern
- `question` - Needs investigation

## Categories

- `shell` - Shell scripts
- `prompt` - LLM prompts
- `lib` - Library code
- `workflow` - Workflows
- `skill` - BMAD skills
- `docs` - Documentation
- `other` - Everything else

## Severity

- `low` - Nice to have
- `medium` - Should fix
- `high` - Important
- `critical` - Blocking

---

*Files in this directory are reviewed and moved to `../processed/`*
