# RALF Global Decision Registry

**Purpose:** Track all significant decisions made across RALF runs for reversibility and learning.

**Location:** `~/.blackbox5/5-project-memory/ralf-core/.autonomous/decision_registry.md`

---

## Decision Log

<!-- Decisions will be appended here by RALF agent -->

---

## Format Template

```yaml
- id: "DEC-[LOOP]-[NUMBER]"
  timestamp: "ISO8601"
  phase: "[INIT/PLAN/EXECUTE/VALIDATE/WRAP]"
  context: "[What was the decision about]"
  options_considered:
    - id: "OPT-001"
      description: "[Option description]"
      pros: ["[pro1]", "[pro2]"]
      cons: ["[con1]", "[con2]"]
    - id: "OPT-002"
      description: "[Option description]"
      pros: ["[pro1]"]
      cons: ["[con1]", "[con2]"]
  selected_option: "OPT-[N]"
  rationale: "[Why this option was selected]"
  assumptions:
    - id: "ASM-001"
      statement: "[Assumption]"
      risk_level: "[LOW/MEDIUM/HIGH]"
      verification_method: "[How to verify]"
      status: "[PENDING/VERIFIED/INVALIDATED]"
  reversibility: "[LOW/MEDIUM/HIGH]"
  rollback_complexity: "[Description]"
  rollback_steps:
    - "[Step 1]"
    - "[Step 2]"
  verification:
    required: true/false
    criteria:
      - "[Criterion 1]"
  status: "[DECIDED/IMPLEMENTED/VERIFIED/ROLLED_BACK]"
```

---

## Statistics

- Total Decisions: 0
- Pending Verification: 0
- Verified: 0
- Rolled Back: 0
