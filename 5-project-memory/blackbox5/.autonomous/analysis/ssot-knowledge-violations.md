# SSOT Knowledge Violations Report

**Scout:** Architecture Analysis Agent
**Date:** 2026-02-06
**Status:** Complete

---

## Critical Finding: Massive Knowledge Duplication

The BlackBox5 system has **severe SSOT violations** with knowledge scattered across 800+ locations. Knowledge that should exist in ONE place is instead duplicated across many files.

---

## 1. Decision Duplication

**Primary Location (SSOT):**
- `.autonomous/memory/decisions/registry.md` - The intended global decision registry

**Duplicated Across:**
- **242 DECISIONS.md files** in run folders:
  - `.autonomous/agents/planner/runs/*/DECISIONS.md` (~80 files)
  - `.autonomous/agents/architect/runs/*/DECISIONS.md` (~25 files)
  - `runs/*/DECISIONS.md` (~130+ files)
  - `.autonomous/runs/*/DECISIONS.md` (~7 files)

**Violation Example:**
The global registry at `registry.md` shows "Total Decisions: 0" but individual run folders contain 8+ detailed decisions with full rationale. These decisions are NOT extracted to the central registry.

---

## 2. Learning/Insights Duplication

**Scattered Across:**
- **43 LEARNINGS.md files** in run folders
- **250 THOUGHTS.md files** in run folders
- **42 ASSUMPTIONS.md files** in run folders
- **258 RESULTS.md files** in run folders
- **22 analysis documents** in `knowledge/analysis/`
- `knowledge/analysis/master-inefficiency-list.md` (aggregated but not linked to sources)

**Violation Example:**
Planner Run 0045 has comprehensive insights in:
- `.autonomous/agents/planner/runs/run-0045/THOUGHTS.md` (463 lines)
- `.autonomous/agents/planner/runs/run-0045/DECISIONS.md` (487 lines)
- `knowledge/analysis/planner-insights-20260201-run0045.md` (analysis document)

These contain overlapping insights but are not cross-referenced.

---

## 3. Skill Effectiveness Duplication

**Duplicated Across THREE Locations:**

1. `operations/skill-metrics.yaml` (620 lines)
   - Contains skill definitions, metrics schema, task outcomes, recovery metrics

2. `operations/skill-usage.yaml` (303 lines)
   - Contains skill usage tracking, usage_log, metadata

3. `.autonomous/operations/skill-usage.yaml` (484 lines)
   - **Different file** with different skill definitions

**Violation:**
- Same skill information exists in multiple places with different schemas
- `skill-metrics.yaml` tracks effectiveness_score, roi_calculation
- `skill-usage.yaml` tracks usage_count, success_count, trigger_accuracy
- The `.autonomous/operations/skill-usage.yaml` has entirely different skill categories

---

## 4. Analysis Reports Duplication

**Scout Reports Duplicated:**
- `.autonomous/analysis/scout-reports/`
  - 3 JSON files + 5 YAML files = **8 files for same reports**
  - Example: `scout-report-intelligent-20260205-013135.json` and `scout-report-intelligent-20260205-013135.yaml` contain identical data

**Agent Reports:**
- `.autonomous/analysis/planner-reports/` (2 YAML + 2 JSON)
- `.autonomous/analysis/executor-reports/` (2 YAML + 2 JSON)
- `.autonomous/analysis/verifier-reports/` (2 YAML + 2 JSON)
- `.autonomous/analysis/loop-reports/` (1 JSON)

Each report exists in BOTH JSON and YAML formats - clear duplication.

---

## 5. Security/Metrics Logs Duplication

**security_checks.json exists in 6 locations:**
- `tasks/active/.logs/security_checks.json`
- `runs/.logs/security_checks.json`
- `.logs/security_checks.json`
- `6-roadmap/research/external/YouTube/AI-Improvement-Research/.logs/security_checks.json`
- `2-engine/.logs/security_checks.json`
- `.logs/security_checks.json` (root)

---

## Summary of SSOT Violations

| Category | SSOT Location | Duplicate Locations | Count |
|----------|---------------|---------------------|-------|
| **Decisions** | `registry.md` | Run folders (DECISIONS.md) | 242 files |
| **Learnings** | `knowledge/analysis/` | Run folders (LEARNINGS.md) | 43 files |
| **Thoughts** | Should be extracted | Run folders (THOUGHTS.md) | 250 files |
| **Skill Metrics** | `operations/skill-metrics.yaml` | `operations/skill-usage.yaml`, `.autonomous/operations/skill-usage.yaml` | 3 files |
| **Analysis Reports** | YAML or JSON (not both) | Both formats in scout-reports/ | 8 files |
| **Security Logs** | Single `.logs/` | 6 different `.logs/` directories | 6 files |

---

## Recommendations for SSOT

1. **Decision Centralization:**
   - Extract all decisions from run folders to `registry.md`
   - Run folders should only reference decisions by ID, not duplicate content

2. **Learning Extraction:**
   - Create a process to extract insights from run folders to `knowledge/analysis/`
   - Run folders should contain only run-specific context, not general insights

3. **Skill Metrics Consolidation:**
   - Merge `skill-metrics.yaml` and `skill-usage.yaml` into ONE file
   - Delete `.autonomous/operations/skill-usage.yaml` (different schema)
   - Establish ONE schema for skill tracking

4. **Report Format Standardization:**
   - Choose ONE format (YAML or JSON) for scout reports
   - Delete duplicate format files

5. **Log Consolidation:**
   - Consolidate all `security_checks.json` into single location
   - Use symlinks or single source with proper paths

6. **Automated Extraction:**
   - Create a script to periodically extract insights from run folders
   - Update central knowledge stores automatically
   - Archive run folders after extraction
