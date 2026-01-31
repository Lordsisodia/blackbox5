# DECISIONS - Run 1769799687

**Task:** TASK-1769799720 - Create Missing BMAD Workflow YAML Files
**Date:** 2026-01-31T02:02:00Z
**Agent:** Agent-2.3

## Decision Registry

All decisions recorded below with reversibility assessments.

---

### DEC-001: Create Complementary YAML Workflow Definitions

**Context:** The `workflows/` directory was empty, but `routes.yaml` defined 30 workflows.

**Options Considered:**
- **OPT-001:** Assume workflows are only in skill .md files, do nothing
- **OPT-002:** Create standalone YAML workflow definitions that complement skills
- **OPT-003:** Move workflow procedures from skills to YAML files

**Selected Option:** OPT-002

**Rationale:**
- Skills contain narrative procedures (human-readable)
- YAML definitions provide structured metadata (machine-readable)
- Hybrid approach keeps benefits of both
- Minimal disruption to existing system

**Reversibility:** LOW
- Can delete YAML files if not useful
- Skills remain untouched
- No breaking changes

**Rollback Steps:**
1. Delete all `workflows/*.yaml` files
2. Remove generator script `lib/generate_workflows.py`
3. Remove schema `schemas/workflow.schema.yaml`
4. System returns to previous state

---

### DEC-002: Workflow Schema Structure

**Context:** Need a consistent schema for 30 different workflow types.

**Schema Design:**
```yaml
name: string              # Workflow name
command: string           # 2-letter command
description: string       # One-line description
skill: string             # Skill file name
agent: string             # Agent persona name
complexity: string        # simple/medium/complex
steps: [...]              # Step definitions
apc_menu: {...}          # A/P/C configuration
wip_tracking: {...}      # WIP settings
outputs: [...]           # Output artifacts
verification: [...]      # Verification checklist
```

**Rationale:**
- Captures all metadata needed for automation
- Follows existing patterns (routes.yaml, TEMPLATE.md)
- Extensible for future needs

**Reversibility:** LOW
- Schema is documentation
- Easy to modify if structure changes

---

### DEC-003: Use Generator Script Instead of Manual Creation

**Context:** Need to create 30 workflow files consistently.

**Options Considered:**
- **OPT-001:** Manually create each YAML file
- **OPT-002:** Create Python generator script
- **OPT-003:** Use YAML macros/templates

**Selected Option:** OPT-002

**Rationale:**
- Consistent structure across all files
- Faster to iterate and regenerate
- Can be reused when routes.yaml changes
- Easier to maintain

**Reversibility:** LOW
- Generated files can be manually edited
- Generator can be re-run if needed
- No dependency lock-in

---

### DEC-004: Agent Name Extraction from Skill Files

**Context:** Generator needs agent names (John, Amelia, etc.) for workflows.

**Approach:** Parse skill .md files to extract agent names from `**Name:**` pattern in persona section.

**Fallback:** If not found, use "Unknown" as default.

**Rationale:**
- Skills are source of truth for agent info
- Avoids hardcoding agent names
- Automatic if skills are updated

**Reversibility:** MEDIUM
- Parsing logic is in generator
- Can be modified if skill format changes
- Fallback ensures robustness

---

### DEC-005: Complexity Determination

**Context:** Need to assign complexity level (simple/medium/complex) to each workflow.

**Approach:**
- `bmad-pm`, `bmad-architect` → complex
- `bmad-quick-flow` → simple
- Everything else → medium

**Rationale:**
- PM and Architect workflows are most involved
- Quick Flow is for simple tasks
- Consistent with BMAD philosophy

**Reversibility:** LOW
- Complexity is metadata
- Easy to change per-workflow if needed

---

## Verification Summary

| Decision | Status | Verification Method |
|----------|--------|-------------------|
| DEC-001 | Implemented | 30 YAML files generated |
| DEC-002 | Implemented | Schema in `schemas/workflow.schema.yaml` |
| DEC-003 | Implemented | Generator in `lib/generate_workflows.py` |
| DEC-004 | Implemented | Agent names extracted correctly |
| DEC-005 | Implemented | Complexity assigned appropriately |

## Assumptions

| ID | Statement | Risk | Status |
|----|-----------|------|--------|
| ASM-001 | Workflow YAMLs complement, not replace, skills | LOW | Verified |
| ASM-002 | Generator script correctly parses routes.yaml | LOW | Validated |
| ASM-003 | All 30 commands in routes.yaml are valid | LOW | Confirmed |
