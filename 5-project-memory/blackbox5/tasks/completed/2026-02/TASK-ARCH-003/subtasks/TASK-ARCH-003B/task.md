# TASK-ARCH-003B: Audit Current State

**Status:** pending
**Priority:** CRITICAL
**Parent Task:** TASK-ARCH-003
**Created:** 2026-02-04
**Estimated:** 20 minutes
**Depends On:** TASK-ARCH-003A

---

## Objective

Audit the current state of all files referenced in STATE.yaml. Document what exists, what's missing, and what needs updating.

---

## Success Criteria

- [ ] Complete inventory of root files vs. STATE.yaml references
- [ ] List of all broken references found
- [ ] Version number audit (STATE.yaml vs. context.yaml)
- [ ] Goal-task link audit
- [ ] Audit report documented

---

## Audit Checklist

### 1. Root Files Audit

Check each file listed in STATE.yaml `root_files`:

| File | Listed in STATE.yaml | Actually Exists | Status |
|------|---------------------|-----------------|--------|
| MAP.yaml | ✅ | ? | Check |
| STATE.yaml | ✅ | ✅ | OK |
| ACTIVE.md | ✅ | ❌ | **REMOVE** |
| WORK-LOG.md | ✅ | ❌ | **REMOVE** |
| timeline.yaml | ✅ | ? | Check |
| feature_backlog.yaml | ✅ | ? | Check |
| test_results.yaml | ✅ | ? | Check |
| _NAMING.md | ✅ | ❌ (moved) | **UPDATE PATH** |
| QUERIES.md | ✅ | ❌ | **REMOVE** |
| README.md | ✅ | ✅ | OK |
| goals.yaml | ✅ | ? | Check |
| UNIFIED-STRUCTURE.md | ✅ | ❌ | **REMOVE** |

### 2. YAML Syntax Audit

**Check STATE.yaml lines 360-361:**
- Open file in editor
- Go to line 360
- Identify the indentation/mapping error
- Document exact fix needed

### 3. Version Audit

**Compare versions:**
```bash
# Get STATE.yaml version
grep "version:" STATE.yaml | head -1

# Get context.yaml version
grep "version:" project/context.yaml
```

**Document:**
- STATE.yaml version: ___
- context.yaml version: ___
- Decision: Which is canonical? ___

### 4. Goal-Task Link Audit

**Check IG-006:**
```bash
cat goals/active/IG-006/goal.yaml | grep -A5 "linked_tasks"
```

**Verify each task exists:**
- TASK-001: exists? ___
- TASK-002: exists? ___
- TASK-003: exists? ___

**Check IG-007:**
- TASK-ARCH-003: exists? ___
- TASK-ARCH-004: exists? ___

### 5. Folder Contents Audit

**Check if folders match STATE.yaml:**
- `folders.project.contents` matches `project/`? ___
- `folders.plans.subfolders.active.contents` matches `plans/active/`? ___
- `folders.decisions.subfolders.architectural.contents` matches `decisions/architectural/`? ___

---

## Audit Report Template

```markdown
# SSOT Audit Report

**Date:** 2026-02-04
**Auditor:** Claude

## Findings

### Broken References (N found)
1. [file] - [reason] - [action needed]

### Version Mismatch
- Expected: X.X.X
- Found: Y.Y.Y
- Action: [update STATE.yaml | update context.yaml]

### Missing Tasks
- [goal] references [task] which [doesn't exist | exists]

### Recommendations
1. [priority]: [action]
```

---

## Deliverable

Audit report saved to: `tasks/active/TASK-ARCH-003/subtasks/TASK-ARCH-003B/audit-report.md`
