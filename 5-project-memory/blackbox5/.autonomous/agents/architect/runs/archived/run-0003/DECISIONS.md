# RALF Run 0003 - DECISIONS

**Date:** 2026-01-30
**Task:** RALF-2026-01-30-002

---

## Decision 1: Library Design Pattern

**Context:** Need to share dry-run utilities across multiple shell scripts

**Options:**
1. Inline the code in each script (duplication)
2. Source a common library (single source of truth)

**Decision:** Use a sourced library at `lib/dry_run.sh`

**Rationale:**
- DRY principle - single source of truth
- Easier to maintain and update
- Consistent behavior across all scripts
- Existing lib/ directory already used for Python modules

---

## Decision 2: Output Format

**Context:** Need consistent, parseable output for dry-run mode

**Options:**
1. `DRY-RUN: command`
2. `[DRY-RUN] Would: command`
3. `[SIMULATION] command`

**Decision:** Use `[DRY-RUN] Would: <action>`

**Rationale:**
- Clear bracketed prefix for grepping
- "Would" clearly indicates intent without action
- Colon separates metadata from command
- Easy to visually scan

---

## Decision 3: Exit Code Behavior

**Context:** What should dry-run return?

**Options:**
1. Always return 0
2. Return 0 if validation passes, non-zero if errors
3. Return the same code as real execution would

**Decision:** Return 0 if validation passes, non-zero if errors detected

**Rationale:**
- Dry-run should validate prerequisites
- Useful for CI/CD pipelines
- Distinguishes between "would work" and "would fail"

---

## Decision 4: Modification Scope

**Context:** Which operations need dry-run protection?

**Decision:** Protect all operations that:
- Modify files (write, delete, move)
- Execute external commands with side effects
- Modify git state (commit, push, branch)
- Create or delete directories
- Send data to external services

**Rationale:**
- Safety first - better to over-protect than under-protect
- Can always relax restrictions later
- Clear audit trail of what would change
