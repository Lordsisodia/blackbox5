# Completed Goals

This directory contains goals that have been achieved and archived.

## Structure

```
completed/
└── IG-XXX/              # Completed goal directory
    ├── goal.yaml        # Original goal definition
    ├── timeline.yaml    # Timeline of all events
    ├── outcome.yaml     # What actually happened (new)
    └── journal/         # Narrative updates
        └── YYYY-MM-DD.md
```

## When to Move a Goal Here

A goal is moved from `active/` to `completed/` when:
- All acceptance criteria are met
- All linked tasks are completed
- Outcome is documented in `outcome.yaml`
- Goal status is set to `completed`

## Outcome.yaml Format

```yaml
outcome:
  completion_date: "2026-02-12T21:51:00Z"
  final_status: "completed"
  success_percentage: 100
  lessons_learned:
    - "Lesson 1"
    - "Lesson 2"
  unexpected_results:
    - "Result 1"
    - "Result 2"
  next_steps:
    - "Follow-up task 1"
    - "Follow-up task 2"
```

## See Also

- `../README.md` - Goals system overview
- `../INDEX.yaml` - Index of all goals (active and completed)
