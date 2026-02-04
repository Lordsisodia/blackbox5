# Auditor Validator Timeline Memory

**Agent:** Auditor Validator
**Task:** TASK-ARCH-003B Validation
**Phase:** Audit
**Created:** 2026-02-04

---

## Work History

No previous runs.

---

## Work Queue

### Validation Tasks
1. [ ] Monitor Auditor Worker run
2. [ ] Read THOUGHTS.md, RESULTS.md
3. [ ] Check audit coverage completeness
4. [ ] Identify missed violations
5. [ ] Write feedback to chat-log.yaml

---

## Current Assignment

```yaml
monitoring: null
last_validation: null
feedback_given: []
```

---

## Validation Checklist

### Coverage Check
- [ ] Did auditor check all root_files in STATE.yaml?
- [ ] Did auditor verify YAML syntax error location?
- [ ] Did auditor compare both version files?
- [ ] Did auditor check ALL goals for task links?
- [ ] Did auditor run validate-ssot.py?

### Quality Check
- [ ] Are findings specific (file:line)?
- [ ] Are actions clear and actionable?
- [ ] Is the audit report well-structured?
- [ ] Are edge cases considered?

### Missed Patterns (Watch For)
- Hidden file references (dotfiles)
- Symlink targets
- Folder contents mismatches
- Cross-reference errors

---

## Feedback Template

```yaml
# Write to communications/ssot-chat-log.yaml
messages:
  - from: auditor-validator
    to: auditor-worker
    timestamp: "2026-02-04THH:MM:SSZ"
    type: feedback|block|approve
    content: |
      Specific observation or instruction
      Based on: [evidence]
      Suggest: [action]
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
│ Find latest auditor-worker run      │
│ in auditor-worker/runs/             │
└─────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│ Read THOUGHTS.md, RESULTS.md        │
│ Check coverage against checklist    │
└─────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│ Write feedback to chat-log.yaml     │
│ Update timeline-memory.md           │
└─────────────────────────────────────┘
  │
  ▼
EXIT (Status: COMPLETE)
```

---

## Success Criteria

- [ ] All auditor work reviewed
- [ ] Coverage gaps identified (if any)
- [ ] Feedback provided via chat-log.yaml
- [ ] Validation results logged

---

## Communication

### Write To
- `auditor-validator/runs/*/THOUGHTS.md` (observations)
- `auditor-validator/runs/*/RESULTS.md` (coverage metrics)
- `communications/ssot-chat-log.yaml` (feedback to worker)
- `communications/ssot-audit-state.yaml` (validation state)

### Read From
- `auditor-worker/runs/*/` (all worker output)
- `communications/ssot-events.yaml` (pipeline events)
