# RALF Run 0002 - DECISIONS

**Task:** RALF-2026-01-30-002: Add Dry-Run Mode to Shell Scripts

---

## Decision 1: Shared Library Approach

**Decision:** Create a shared `dry_run.sh` library instead of inline code in each script

**Rationale:**
- DRY principle - don't repeat the same logic 6 times
- Consistent behavior across all scripts
- Easier to update dry-run behavior in one place
- Can add utilities like dry_run_log() for consistent formatting

**Trade-offs:**
- Adds a dependency (scripts must source the library)
- Slightly more complex initial setup
- Library must exist for scripts to work

---

## Decision 2: Argument Parsing Pattern

**Decision:** Use standard bash case statement for --dry-run flag

**Rationale:**
- Compatible with existing argument parsing in scripts
- Can coexist with other flags
- Standard pattern familiar to bash developers

**Pattern:**
```bash
DRY_RUN=false
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run) DRY_RUN=true; shift ;;
        *) shift ;;
    esac
done
```

---

## Decision 3: Output Format

**Decision:** Use `[DRY-RUN] Would: <action>` format

**Rationale:**
- Clear visual distinction from actual execution
- Easy to grep/filter in logs
- Consistent with common CLI conventions
- Task specification requested this format

---

## Decision 4: Exit Code Behavior

**Decision:** Return 0 in dry-run mode if validation passes

**Rationale:**
- Allows test scripts to validate without side effects
- Non-zero only if there's an actual error (missing files, etc.)
- Consistent with tools like `terraform plan`

---

## Decision 5: Execution Order

**Decision:** Start with ralf-loop.sh (most critical), then proceed by priority

**Rationale:**
- Highest impact first
- If interrupted, most important script has dry-run
- ralf-loop.sh likely has patterns that can be reused

---
