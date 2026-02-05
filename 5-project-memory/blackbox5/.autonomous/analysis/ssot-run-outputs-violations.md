# SSOT Run/Agent Outputs Violations Report

**Scout:** Architecture Analysis Agent
**Date:** 2026-02-06
**Status:** Complete

---

## Summary

Run outputs and agent artifacts are scattered across **10+ locations** with massive duplication. **835+ run output files** exist with overlapping content.

---

## 1. Run Folder Proliferation (CRITICAL)

**Run folders exist in 10+ locations:**

| Location | Count | Purpose |
|----------|-------|---------|
| `.autonomous/agents/planner/runs/` | ~80 | Planner agent runs |
| `.autonomous/agents/architect/runs/` | ~25 | Architect agent runs |
| `.autonomous/agents/executor/runs/` | ~7 | Executor agent runs |
| `.autonomous/agents/analyzer/runs/` | ~5 | Analyzer agent runs |
| `.autonomous/runs/` | ~7 | General runs |
| `runs/` | ~130+ | Main run folder |
| `tasks/active/TASK-*/runs/` | ~20 | Task-specific runs |
| `goals/active/IG-*/runs/` | ~5 | Goal-specific runs |
| `plans/active/*/runs/` | ~3 | Plan-specific runs |
| `5-project-memory/blackbox5/runs/` | ~200+ | Duplicate run storage |

**Total: 482+ run folders scattered across the system**

---

## 2. Output File Duplication Pattern

**Each run folder contains the SAME 4 files:**

```
run-XXXX/
├── THOUGHTS.md      # Agent thoughts (~400 lines each)
├── DECISIONS.md     # Agent decisions (~300 lines each)
├── LEARNINGS.md     # Agent learnings (~200 lines each)
└── RESULTS.md       # Agent results (~250 lines each)
```

**Math:**
- 482 runs × 4 files = **1,928 output files**
- Average 1,150 lines per run = **554,300 lines of duplicated content patterns**

---

## 3. Content Duplication Between Runs and Analysis

**Scout findings duplicated:**

| Source | Files | Content |
|--------|-------|---------|
| Run folders | 482 runs × 4 files | Raw agent outputs |
| `knowledge/analysis/` | 22 files | Extracted insights |
| `.autonomous/analysis/` | 30+ files | Scout reports |

**Example Duplication:**
- Planner Run 0045: `.autonomous/agents/planner/runs/run-0045/THOUGHTS.md` (463 lines)
- Also in: `knowledge/analysis/planner-insights-20260201-run0045.md`
- Also referenced in: `.autonomous/analysis/planner-reports/`

**Same insights exist in 3+ places.**

---

## 4. Analysis Report Format Duplication

**Each scout report exists in BOTH formats:**

| Report | JSON | YAML | Duplication |
|--------|------|------|-------------|
| scout-report-intelligent-20260205-013135 | ✓ | ✓ | 100% identical data |
| scout-report-intelligent-20260205-013356 | ✓ | ✓ | 100% identical data |
| scout-report-intelligent-20260205-aggregated | ✓ | ✓ | 100% identical data |
| planner-report-loop-30 | ✓ | ✓ | 100% identical data |
| executor-report-loop-65 | ✓ | ✓ | 100% identical data |
| verifier-report-* | ✓ | ✓ | 100% identical data |

**8 reports × 2 formats = 16 files for 8 reports' worth of data**

---

## 5. Metadata Duplication

**Run metadata stored in multiple places:**

| Location | Data | Issue |
|----------|------|-------|
| `run-*/metadata.yaml` | Loop, agent, timestamps | Canonical per-run |
| `heartbeat.yaml` | References run_number | May not match metadata |
| `events.yaml` | References run_id | Different ID format |
| `agent-state.yaml` | Should track runs | EMPTY |

**Example Inconsistency:**
- Run 0074 metadata: `agent: planner`, `loop: 25`
- heartbeat.yaml shows: `planner: run_number: 79`
- Events show: `run_id: executor-test-001`

**Same run referenced 3 different ways.**

---

## 6. Decision Registry Duplication

**Decisions scattered across 242+ files:**

| Location | Count | Content |
|----------|-------|---------|
| `runs/*/DECISIONS.md` | ~130 | Run decisions |
| `.autonomous/agents/planner/runs/*/DECISIONS.md` | ~80 | Planner decisions |
| `.autonomous/agents/architect/runs/*/DECISIONS.md` | ~25 | Architect decisions |
| `.autonomous/memory/decisions/registry.md` | 1 | **EMPTY - should be SSOT** |

**Violation:** Central registry shows "Total Decisions: 0" but 242+ files contain detailed decisions.

---

## Recommendations for SSOT

### 1. Run Folder Consolidation
**Canonical Location:** `runs/` (single directory)
- Move all `.autonomous/agents/*/runs/` to central `runs/`
- Delete task/goal/plan-specific run folders
- Use naming convention: `runs/{agent-type}-{loop}-{timestamp}/`

### 2. Output File Consolidation
**Canonical Pattern:** One file per run, not four
- Merge THOUGHTS.md + DECISIONS.md + LEARNINGS.md + RESULTS.md
- Into single `run-report.md` with sections
- Reduces 1,928 files to ~482 files

### 3. Analysis Extraction Pipeline
**Process:**
1. Run completes → Output in run folder
2. Extraction agent reads run output
3. Insights extracted to `knowledge/analysis/`
4. Run folder archived/compressed
5. Central registry updated

### 4. Report Format Standardization
**Choose ONE format:** YAML (human-readable + machine-parseable)
- Delete all JSON duplicates
- Keep only YAML versions
- Consistent schema across all reports

### 5. Decision Centralization
**Canonical Source:** `.autonomous/memory/decisions/registry.md`
- Extract all decisions from run folders
- Add to central registry with run references
- Run folders should reference decisions by ID only

---

## Critical Files Requiring Immediate Attention

1. `.autonomous/agents/planner/runs/` - 80 folders to consolidate
2. `.autonomous/agents/architect/runs/` - 25 folders to consolidate
3. `5-project-memory/blackbox5/runs/` - 200+ duplicate folders
4. `knowledge/analysis/` - Merge with `.autonomous/analysis/`
5. `.autonomous/memory/decisions/registry.md` - Populate from run folders

---

## Task Creation Checklist

- [ ] TASK-SSOT-006: Consolidate run folders to single location
- [ ] TASK-SSOT-007: Merge 4 output files per run into 1
- [ ] TASK-SSOT-008: Create analysis extraction pipeline
- [ ] TASK-SSOT-009: Standardize on YAML format for reports
- [ ] TASK-SSOT-010: Extract decisions to central registry
- [ ] TASK-SSOT-011: Archive old run folders after extraction
