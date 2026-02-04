# SSOT Fix Pipeline Agents

**Task:** TASK-ARCH-003 - Fix Single Source of Truth Violations
**Architecture:** Dual-RALF Worker-Validator Pattern
**Created:** 2026-02-04

---

## Quick Start

```bash
# 1. Review the delegation plan
cat DELEGATION-PLAN.md

# 2. Check pipeline state
cat communications/ssot-pipeline-state.yaml

# 3. Launch Auditor Worker (TASK-ARCH-003B)
# Use skill: bmad-analyst with timeline-memory injection

# 4. Monitor events
tail -f communications/ssot-events.yaml
```

---

## Agent Structure

```
ssot-fix/
├── DELEGATION-PLAN.md          # Complete delegation strategy
├── README.md                   # This file
│
├── auditor-worker/             # TASK-ARCH-003B: Audit
│   └── memory/
│       └── timeline-memory.md  # Work queue + assignment logic
│
├── auditor-validator/          # Audit validation
│   └── memory/
│       └── timeline-memory.md  # Coverage checklist
│
├── fixer-worker/               # TASK-ARCH-003C: Execute
│   └── memory/
│       └── timeline-memory.md  # Fix specifications
│
├── fixer-validator/            # Fix validation
│   └── memory/
│       └── timeline-memory.md  # SSOT principles
│
├── final-validator/            # TASK-ARCH-003D: Validate
│   └── memory/
│       └── timeline-memory.md  # Validation checklist
│
└── communications/
    ├── ssot-pipeline-state.yaml  # Overall pipeline state
    ├── ssot-events.yaml          # Event bus
    └── ssot-chat-log.yaml        # Agent coordination
```

---

## How to Launch Agents

### Phase 1: Audit (TASK-ARCH-003B)

**Auditor Worker:**
```bash
# Inject timeline-memory.md via SessionStart hook
# Use skill: bmad-analyst
# Task: Inventory all files, document broken references
```

**Auditor Validator:**
```bash
# Run in parallel with worker
# Use skill: bmad-qa
# Task: Validate audit coverage, provide feedback
```

### Phase 2: Execute (TASK-ARCH-003C)

**Fixer Worker:**
```bash
# Wait for audit.complete event
# Use skill: bmad-dev
# Task: Apply fixes per audit report
```

**Fixer Validator:**
```bash
# Run in parallel with worker
# Use skill: bmad-architect
# Task: Validate SSOT principles, approve/block
```

### Phase 3: Validate (TASK-ARCH-003D)

**Final Validator:**
```bash
# Wait for execute.complete event
# Use skill: bmad-qa + bmad-tea
# Task: Run validation, update docs, mark complete
```

---

## Communication Protocol

### Workers Write To:
- `runs/*/THOUGHTS.md` - Reasoning
- `runs/*/RESULTS.md` - Outcomes
- `runs/*/DECISIONS.md` - Decisions
- `communications/ssot-events.yaml` - Events

### Validators Write To:
- `runs/*/THOUGHTS.md` - Observations
- `communications/ssot-chat-log.yaml` - Feedback

### Shared State:
- `communications/ssot-pipeline-state.yaml` - Pipeline status
- `communications/ssot-events.yaml` - Event bus
- `communications/ssot-chat-log.yaml` - Coordination

---

## Success Criteria

- [ ] All 8 SSOT violations fixed
- [ ] YAML syntax valid
- [ ] validate-ssot.py passes
- [ ] RALF context loads correctly
- [ ] Git commit created
- [ ] Documentation updated

---

## Token Budget

| Phase | Agents | Budget |
|-------|--------|--------|
| Audit | 2 | ~11K |
| Execute | 2 | ~21K |
| Validate | 1 | ~2K |
| **Total** | **5** | **~34K** |

---

## Files Modified

1. `STATE.yaml` - Fixed YAML, removed deleted refs, updated project section
2. `project/context.yaml` - Synced version to 5.1.0
3. `goals/active/IG-006/goal.yaml` - Removed bad task references

---

## Rollback

If anything breaks:
```bash
cp STATE.yaml.backup.* STATE.yaml
git checkout -- STATE.yaml project/context.yaml goals/active/IG-006/goal.yaml
```
