# SSOT Metrics/Monitoring Violations Report

**Scout:** Architecture Analysis Agent
**Date:** 2026-02-06
**Status:** Complete

---

## Summary

Metrics and monitoring data is duplicated across **4+ locations**, causing inconsistent reporting and maintenance burden.

---

## 1. Skill Metrics Duplication (CRITICAL)

**Same skill data exists in FOUR files:**

| File | Lines | Purpose |
|------|-------|---------|
| `operations/skill-metrics.yaml` | 620 | Effectiveness scores, ROI calculations |
| `operations/skill-usage.yaml` | 303 | Usage tracking, success rates |
| `.autonomous/operations/skill-usage.yaml` | 484 | Different schema, different data |
| `CLAUDE.md` | ~50 | Domain-to-skill mapping table |

**Specific Duplications:**
- `bmad-pm`, `bmad-architect`, `bmad-analyst`, `bmad-sm`, `bmad-ux`, `bmad-dev`, `bmad-qa`, `bmad-tea`, `bmad-quick-flow` - ALL defined in multiple files
- Confidence threshold of 70% defined in:
  - `default.yaml` (line 45)
  - `skill-selection.yaml` (line 12)
  - `CLAUDE.md` (domain-to-skill mapping table)

**Inconsistency Example:**
- `skill-metrics.yaml` tracks `effectiveness_score`, `roi_calculation`
- `skill-usage.yaml` tracks `usage_count`, `success_count`, `trigger_accuracy`
- `.autonomous/operations/skill-usage.yaml` has entirely different skill categories

---

## 2. Task Count Duplication

**Task counts stored in 3+ places:**

| Location | Count | Status |
|----------|-------|--------|
| `queue.yaml` | 90 total, 25 completed, 5 in_progress, 60 pending | May be stale |
| `STATE.yaml` | Lists active/completed separately | Derived from queue? |
| Actual task files | ~104 tasks in directories | Ground truth |

**Discrepancy Found:**
- queue.yaml shows 25 completed
- Actual task files show 30+ completed
- queue.yaml shows 90 total tasks
- Actual count is 104 tasks

---

## 3. Security Checks Log Duplication

**security_checks.json exists in 6 locations:**

1. `tasks/active/.logs/security_checks.json`
2. `runs/.logs/security_checks.json`
3. `.logs/security_checks.json`
4. `6-roadmap/research/external/YouTube/AI-Improvement-Research/.logs/security_checks.json`
5. `2-engine/.logs/security_checks.json`
6. `.logs/security_checks.json` (root)

**Violation:** Same log data scattered across multiple directories with no clear ownership.

---

## 4. Events Log Duplication

**Events stored in 5+ locations:**

| File | Purpose | Entries |
|------|---------|---------|
| `.autonomous/agents/communications/events.yaml` | Agent lifecycle events | 530+ events |
| `.autonomous/agents/communications/queue.yaml` | Task queue events | Mixed with queue data |
| `timeline.yaml` | Project timeline events | 1500+ lines |
| `goals/active/*/timeline.yaml` | Goal-specific events | 8+ files |
| `runs/*/events.yaml` | Run-specific events | 200+ run folders |

**Issue:** Same event types logged in multiple places with different formats.

---

## 5. Dashboard/Health Metrics Duplication

**Health/monitoring data calculated independently:**

| Source | Data | Issue |
|--------|------|-------|
| `bin/bb5-health-dashboard.py` | Calculates health from multiple sources | May not match actual state |
| `bin/bb5-metrics-collector.py` | Collects metrics independently | Different calculation method |
| `STATE.yaml` | Claims to have metrics section | Empty or outdated |

**No single source for:**
- System health status
- Task completion rates
- Agent performance metrics
- Queue depth/status

---

## Recommendations for SSOT

### 1. Skill Metrics SSOT
**Canonical Source:** `operations/skill-registry.yaml` (to be created)
- Merge skill-metrics.yaml + skill-usage.yaml into ONE file
- Delete `.autonomous/operations/skill-usage.yaml`
- CLAUDE.md should reference, not duplicate

### 2. Task Counts SSOT
**Canonical Source:** Count from actual task files
- queue.yaml should be DERIVED, not source
- Create `bb5 task:count` command that counts actual files
- Remove hardcoded counts from queue.yaml metadata

### 3. Security Logs SSOT
**Canonical Source:** Single `.logs/security_checks.json` at project root
- Delete all other instances
- Update scripts to write to single location
- Use symlinks if cross-project sharing needed

### 4. Events SSOT
**Canonical Source:** `.autonomous/agents/communications/events.yaml`
- timeline.yaml should be DERIVED view
- Goal-specific timelines should query central events
- Run folders should reference central events, not duplicate

### 5. Metrics Collection SSOT
**Canonical Source:** New `metrics/` directory with single collector
- One script collects all metrics
- Dashboard reads from single metrics store
- All calculations in one place

---

## Critical Files Requiring Immediate Attention

1. `operations/skill-metrics.yaml` - Merge with skill-usage.yaml
2. `.autonomous/operations/skill-usage.yaml` - Delete (different schema)
3. `queue.yaml` - Remove hardcoded counts, derive from files
4. Multiple `security_checks.json` - Consolidate to one
5. `bin/bb5-health-dashboard.py` + `bin/bb5-metrics-collector.py` - Merge into one

---

## Task Creation Checklist

- [ ] TASK-SSOT-001: Consolidate skill metrics files
- [ ] TASK-SSOT-002: Create single security_checks.json location
- [ ] TASK-SSOT-003: Derive task counts from files instead of hardcoding
- [ ] TASK-SSOT-004: Merge health dashboard and metrics collector
- [ ] TASK-SSOT-005: Create central events store
