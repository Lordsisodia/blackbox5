# PLAN.md: Consolidate Security Checks - Single Source of Truth

**Task:** TASK-SSOT-005 - Security checks in multiple locations
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 2-3 hours
**Importance:** 65 (Medium-High)

---

## 1. First Principles Analysis

### The Core Problem
Security check configurations and results are scattered across:
- `5-project-memory/blackbox5/.logs/security_checks.json`
- `2-engine/.logs/security_checks.json`
- Potentially other `.logs/security_checks.*` files

This creates:
1. **Fragmented View**: No single place to see all security issues
2. **Inconsistent Standards**: Different checks in different locations
3. **Maintenance Overhead**: Multiple files to update when checks change
4. **Reporting Complexity**: Aggregating results requires multiple reads

### Guiding Principle
- **Project-Owned Security**: Security checks are project-specific
- **Centralized Reporting**: Single location for all security data
- **Engine Provides Framework**: Engine has check tools, project has results

---

## 2. Current State Analysis

### Files Involved

| File | Purpose | Last Updated |
|------|---------|--------------|
| `5-project-memory/blackbox5/.logs/security_checks.json` | Project security results | 2026-02-05 |
| `2-engine/.logs/security_checks.json` | Engine security results | 2026-02-05 |

### Content Analysis

Both files likely contain:
- Check timestamps
- Check types (credentials, permissions, etc.)
- Results (pass/fail)
- Issues found
- Remediation status

---

## 3. Proposed Solution

### Decision: Project-Owned Security Data

**Canonical Location:** `5-project-memory/blackbox5/.logs/security_checks.json`

**Rationale:**
- Security issues are project-specific
- Engine provides the checking tools/framework
- Project defines what checks to run and stores results

### Implementation Plan

#### Phase 1: Audit (30 min)

1. Read both security check files
2. Identify:
   - Unique checks in engine file (need migration)
   - Unique checks in project file (keep)
   - Overlapping checks (merge, keep most recent)

#### Phase 2: Merge (1 hour)

1. Merge all checks into project file
2. Deduplicate overlapping checks
3. Preserve history/timestamps
4. Update schema if needed

#### Phase 3: Update Scripts (1 hour)

**Update:** Security check scripts to write to project location

```python
# Before
SECURITY_LOG = "2-engine/.logs/security_checks.json"

# After
SECURITY_LOG = get_project_path() + "/.logs/security_checks.json"
```

#### Phase 4: Cleanup (30 min)

1. Remove `2-engine/.logs/security_checks.json`
2. Update any scripts reading from engine location
3. Update documentation

---

## 4. Files to Modify

### Modified Files
1. `5-project-memory/blackbox5/.logs/security_checks.json` - Merge engine data
2. `2-engine/.logs/security_checks.json` - Remove after migration

### Scripts to Update
1. Security check scripts in `2-engine/.autonomous/bin/`
2. Any monitoring/dashboard scripts
3. Hook scripts that log security issues

---

## 5. Success Criteria

- [ ] All security checks consolidated to project file
- [ ] Engine security file removed
- [ ] All scripts write to project location
- [ ] No duplicate checks
- [ ] Security dashboard shows all issues
- [ ] Historical data preserved

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Restore engine security file
2. **Fix**: Debug script updates
3. **Re-migrate**: Once fixed

---

## 7. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Audit | 30 min | 30 min |
| Phase 2: Merge | 1 hour | 1.5 hours |
| Phase 3: Script Updates | 1 hour | 2.5 hours |
| Phase 4: Cleanup | 30 min | 3 hours |
| **Total** | | **2-3 hours** |

---

*Plan created based on SSOT violation analysis - Security checks in multiple locations*
