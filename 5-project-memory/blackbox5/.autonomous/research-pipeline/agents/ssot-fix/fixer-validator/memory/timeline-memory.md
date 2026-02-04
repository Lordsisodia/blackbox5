# Fixer Validator Timeline Memory

**Agent:** Fixer Validator
**Task:** TASK-ARCH-003C Validation
**Phase:** Execute
**Created:** 2026-02-04

---

## Work History

No previous runs.

---

## Work Queue

### Validation Tasks
1. [ ] Monitor Fixer Worker runs
2. [ ] Review each fix against SSOT principles
3. [ ] Check for new violations introduced
4. [ ] Validate architecture decisions
5. [ ] Approve or block via chat-log.yaml

---

## Current Assignment

```yaml
monitoring: null
approvals_given: []
blocks_given: []
last_validation: null
```

---

## SSOT Principles Checklist

### Single Source of Truth
- [ ] STATE.yaml references (not duplicates) context.yaml
- [ ] No duplicate project identity information
- [ ] File references point to canonical locations

### Convention over Configuration
- [ ] Changes follow existing naming conventions
- [ ] Structure matches established patterns

### Minimal Viable Documentation
- [ ] Comments explain WHY, not WHAT
- [ ] No redundant documentation

### Hierarchy of Information
- [ ] Project identity in context.yaml (correct)
- [ ] STATE.yaml as aggregator (correct)
- [ ] Goals in goals/ folder (correct)

---

## Validation Rules

### BLOCK If:
- Duplicate information introduced
- Canonical source changed instead of reference
- New SSOT violation created
- RALF context broken

### APPROVE If:
- Fix follows SSOT principles
- No new violations
- Validation script passes
- Architecture improved

---

## Feedback Template

```yaml
# Write to communications/ssot-chat-log.yaml
messages:
  - from: fixer-validator
    to: fixer-worker
    timestamp: "2026-02-04THH:MM:SSZ"
    type: block|approve|suggest
    content: |
      [Specific feedback]

      Principle: [which SSOT principle]
      Evidence: [what was observed]
      Required: [action needed]
```

---

## Work Assignment Logic

```
START
  │
  ▼
┌─────────────────────────────┐
│ Read this timeline-memory   │
│ (injected via SessionStart) │
└─────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│ Find latest fixer-worker run        │
│ in fixer-worker/runs/               │
└─────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│ Read THOUGHTS.md, RESULTS.md        │
│ Check changes against principles    │
└─────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│ Decision:                           │
│ - Block if violation introduced     │
│ - Approve if principles followed    │
│ - Suggest if improvement possible   │
└─────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│ Write to chat-log.yaml              │
│ Update timeline-memory.md           │
└─────────────────────────────────────┘
  │
  ▼
EXIT (Status: COMPLETE)
```

---

## Success Criteria

- [ ] All fixes reviewed
- [ ] SSOT principles verified
- [ ] No new violations introduced
- [ ] Feedback provided for each fix

---

## Communication

### Write To
- `fixer-validator/runs/*/THOUGHTS.md` (observations)
- `fixer-validator/runs/*/RESULTS.md` (validation results)
- `communications/ssot-chat-log.yaml` (feedback)
- `communications/ssot-fixer-state.yaml` (validation state)

### Read From
- `fixer-worker/runs/*/` (all worker output)
- `communications/ssot-events.yaml` (pipeline events)
- `STATE.yaml` (to verify changes)
