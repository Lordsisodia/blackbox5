# PLAN.md: Architecture Dashboard Stale Status

**Task ID:** TASK-DOCU-049
**Status:** Planning
**Priority:** LOW
**Created:** 2026-02-05
**Estimated Effort:** 15 minutes
**Source:** Scout opportunity docs-008 (Score: 6.5)

---

## 1. First Principles Analysis

### Why Refresh Dashboard Status?

1. **Accuracy**: Dashboard shows outdated task statuses
2. **Trust**: Stale data reduces confidence in system
3. **Decision Making**: Current status needed for prioritization
4. **Visibility**: Stakeholders need accurate project health view

### What Happens Without Refresh?

| Problem | Impact | Severity |
|---------|--------|----------|
| Wrong priorities | Decisions based on old data | Medium |
| Missed completions | Don't know what's done | Medium |
| False alarms | Shows blocked tasks as active | Low |
| Poor planning | Can't see actual progress | Medium |

### How Should Dashboard Stay Current?

**Automated Refresh:**
- Run update-dashboard.py on schedule
- Trigger on task status changes
- CI/CD integration for auto-update

---

## 2. Current State Assessment

### Dashboard System

**Generator:** `bin/update-dashboard.py`

**Output:** `.docs/architecture-dashboard.md`

**Current Metrics:**
- Empty directories count
- Active/completed tasks count
- Active goals count
- Knowledge files count
- Validation status
- ARCH task statuses
- Recent changes

### Stale Data Indicators

The dashboard shows:
- Task statuses from last manual run
- "Last Updated" timestamp in the past
- ARCH tasks may show wrong status
- Recent changes section outdated

---

## 3. Proposed Solution

### Immediate Fix

Run update-dashboard.py to refresh all metrics:

```bash
python3 bin/update-dashboard.py
```

### Automation Options

**Option 1: GitHub Actions**
```yaml
# .github/workflows/update-dashboard.yml
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  push:
    paths:
      - 'tasks/**'
      - 'goals/**'
```

**Option 2: Task Completion Hook**
- Trigger update when task status changes
- Integrated with bb5-task command

**Option 3: RALF Integration**
- Add dashboard update to RALF workflow
- Run after each agent cycle

---

## 4. Implementation Plan

### Phase 1: Immediate Refresh (2 min)

1. **Run update script**
   ```bash
   cd /Users/shaansisodia/.blackbox5/5-project-memory/blackbox5
   python3 bin/update-dashboard.py
   ```

2. **Verify output**
   - Check `.docs/architecture-dashboard.md`
   - Confirm timestamp updated
   - Review task statuses

### Phase 2: Validate Accuracy (5 min)

1. **Cross-check task statuses**
   - Compare dashboard to actual task files
   - Verify ARCH task statuses
   - Check completed vs pending counts

2. **Verify metrics**
   - Empty directory count
   - Active goals count
   - Knowledge file count

### Phase 3: Document Automation (8 min)

1. **Create GitHub Actions workflow**
   - Schedule-based trigger
   - Path-based trigger
   - Auto-commit updated dashboard

2. **Add to documentation**
   - Document update process
   - Add to operations guide

---

## 5. Success Criteria

- [ ] Dashboard refreshed with current data
- [ ] Timestamp shows recent update
- [ ] Task statuses verified accurate
- [ ] Automation implemented (optional)
- [ ] Documentation updated

---

## 6. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Refresh | 2 min | 2 min |
| Phase 2: Validate | 5 min | 7 min |
| Phase 3: Automation | 8 min | 15 min |
| **Total** | **15 min** | **~15 min** |

---

## 7. Rollback Strategy

If refresh causes issues:

1. **Immediate:** Restore previous dashboard from git
   ```bash
   git checkout HEAD~1 -- .docs/architecture-dashboard.md
   ```

2. **Fix:** Debug update-dashboard.py script
3. **Re-run:** After fixing issues

---

## 8. Files to Modify

| File | Changes | Lines |
|------|---------|-------|
| `.docs/architecture-dashboard.md` | Auto-generated refresh | ~150 |
| `.github/workflows/update-dashboard.yml` | New automation (optional) | ~30 |

---

*Plan created: 2026-02-06*
*Ready for implementation*
