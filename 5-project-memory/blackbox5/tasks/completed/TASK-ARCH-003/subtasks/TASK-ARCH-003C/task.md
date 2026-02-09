# TASK-ARCH-003C: Execute SSOT Fixes

**Status:** pending
**Priority:** CRITICAL
**Parent Task:** TASK-ARCH-003
**Created:** 2026-02-04
**Estimated:** 45 minutes
**Depends On:** TASK-ARCH-003B

---

## Objective

Execute the planned fixes based on audit findings. Make STATE.yaml an aggregator, not a duplicator.

---

## Success Criteria

- [ ] All changes from audit implemented
- [ ] YAML syntax valid
- [ ] No broken references
- [ ] Version numbers synced
- [ ] Validation script passes
- [ ] Git commit created

---

## Execution Steps

### Step 1: Backup (2 min)
```bash
cp STATE.yaml STATE.yaml.backup.$(date +%Y%m%d-%H%M%S)
git add STATE.yaml.backup.*
```

### Step 2: Fix YAML Parse Error (5 min)

**Location:** Lines 360-361
**Issue:** Malformed YAML in docs section

**Fix:**
```yaml
# BEFORE (broken):
docs:
  root:
    path: ".docs/"
    files:
      - "siso-internal-patterns.md"
        purpose: "10 key patterns"  # <- Wrong indentation

# AFTER (fixed):
docs:
  root:
    path: ".docs/"
    files:
      - file: "siso-internal-patterns.md"
        purpose: "10 key patterns"
```

### Step 3: Remove Deleted File References (5 min)

Remove from `root_files` section:
- ACTIVE.md
- WORK-LOG.md
- _NAMING.md (or update path)
- QUERIES.md
- UNIFIED-STRUCTURE.md

### Step 4: Update Project Section (10 min)

**BEFORE:**
```yaml
project:
  name: blackbox5
  version: "5.1.0"
  description: "Global AI Infrastructure for multi-agent orchestration"
  status: "active"
  last_updated: "2026-02-04T06:00:00Z"
  updated_by: "Claude"
  structure_version: "unified-1.0"
```

**AFTER:**
```yaml
project:
  reference: "project/context.yaml"
  cached_version: "5.1.0"
  last_sync: "2026-02-04T06:00:00Z"
  # NOTE: Canonical project identity is in project/context.yaml
  # This section provides quick reference only
```

### Step 5: Sync Version Numbers (3 min)

Update `project/context.yaml`:
```yaml
project:
  version: "5.1.0"  # Was "5.0.0", now synced with STATE.yaml
```

### Step 6: Fix IG-006 Goal (5 min)

Edit `goals/active/IG-006/goal.yaml`:

**Remove:**
```yaml
linked_tasks:
  - TASK-001
  - TASK-002
  - TASK-003
```

**Replace with:**
```yaml
linked_tasks: []
# NOTE: Tasks were placeholder references, removed during SSOT cleanup
```

### Step 7: Validate (10 min)

```bash
# Test YAML syntax
python3 -c "import yaml; yaml.safe_load(open('STATE.yaml'))"

# Run full validation
python3 bin/validate-ssot.py

# Check RALF context still loads
head -50 Ralf-context.md
```

### Step 8: Commit (5 min)

```bash
git add STATE.yaml project/context.yaml goals/active/IG-006/goal.yaml
git commit -m "fix: resolve SSOT violations

- STATE.yaml now references (not duplicates) project/context.yaml
- Removed references to deleted files (ACTIVE.md, WORK-LOG.md, etc.)
- Fixed YAML parse error in docs section
- Synced version numbers (5.1.0)
- Fixed broken goal-task links in IG-006
- Added validation script for future checks

Validation: python3 bin/validate-ssot.py passes
Task: TASK-ARCH-003"
```

---

## Rollback Procedure

If anything breaks:

```bash
# Restore backup
cp STATE.yaml.backup.* STATE.yaml

# Or git revert
git revert HEAD

# Verify
python3 bin/validate-ssot.py
```

---

## Verification Checklist

- [ ] `python3 -c "import yaml; yaml.safe_load(open('STATE.yaml'))"` passes
- [ ] `python3 bin/validate-ssot.py` shows 0 errors
- [ ] `cat project/context.yaml | grep version` shows "5.1.0"
- [ ] `cat goals/active/IG-006/goal.yaml` has no linked_tasks
- [ ] Git commit created with descriptive message
- [ ] Ralf-context.md still readable

---

## Deliverable

Committed changes + validation passing.
