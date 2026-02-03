# Blackbox5 Run Structure Map v2 - COMPREHENSIVE

**Generated:** 2026-02-04
**Status:** Complete analysis of ALL run locations

---

## 📊 TRUE RUN STATISTICS

**Total Runs Found: 236**

### By Location

| Location | Count | Type |
|----------|-------|------|
| `planner/runs/` | 87 | Planner agent runs |
| `executor/runs/` | 61 | Executor agent runs |
| `architect/runs/archived/` | 47 | Architect agent runs |
| `runs/unknown/completed/` | 38 | Legacy/unspecified runs |
| `.autonomous/runs/` | 2 | Root autonomous runs |
| `2-engine/` (orphaned) | 1 | Misplaced run |

---

## 🗂️ Complete Directory Structure

```
~/.blackbox5/5-project-memory/blackbox5/
│
├── .autonomous/
│   ├── agents/
│   │   ├── planner/
│   │   │   └── runs/              # 87 runs
│   │   │       ├── run-0001
│   │   │       ├── run-0002
│   │   │       ├── ...
│   │   │       ├── run-0080
│   │   │       └── run-test
│   │   │
│   │   ├── executor/
│   │   │   └── runs/              # 61 runs
│   │   │       ├── run-0001
│   │   │       ├── run-0002
│   │   │       └── ...
│   │   │
│   │   └── architect/
│   │       └── runs/
│   │           └── archived/      # 47 runs
│   │
│   └── runs/                      # 2 runs (root level)
│
└── runs/                          # Legacy structure
    ├── unknown/
    │   └── completed/             # 38 runs
    ├── planner/                   # Empty
    ├── executor/                  # Empty
    └── completed/                 # Empty
```

---

## 🏗️ TWO DIFFERENT RUN STRUCTURES

### Structure A: Agent-Specific Runs (Primary)
**Location:** `.autonomous/agents/{agent}/runs/`

Used by: Planner (87 runs), Executor (61 runs), Architect (47 runs)

**Files per run:**
```
run-XXXX/
├── metadata.yaml          # Loop metadata
├── THOUGHTS.md           # Agent analysis
├── DECISIONS.md          # Decisions made
└── RESULTS.md            # Outcomes
```

**Metadata format (planner):**
```yaml
loop:
  number: 30
  agent: planner
  timestamp_start: "2026-02-01T16:00:00Z"
  timestamp_end: "2026-02-01T16:15:00Z"
  duration_seconds: 900

state:
  active_tasks_count: 3
  completed_tasks_count: 13
  executor_status: healthy
  queue_depth: 3
  lpm_baseline: 500

actions_taken:
  - type: analyze
    description: "Deep data analysis..."
    impact: "Discovered LPM acceleration"

discoveries:
  - type: pattern
    description: "LPM acceleration sustained"
    impact: high
    confidence: 85
```

**Metadata format (executor):**
```yaml
run:
  id: "run-0065"
  agent: "executor"
  timestamp_start: "..."
  timestamp_end: "..."
  duration_seconds: 280

task:
  task_id: "TASK-1769958230"
  feature_id: "F-013"
  title: "Code Review & Quality Assurance"
  status: completed

execution:
  lines_added: 2750
  lines_removed: 0
  files_modified: 12
  lpm: 497
  commits: 3

results:
  status: success
  summary: "Feature F-013 completed successfully"
```

### Structure B: Session-Based Runs (Legacy/New)
**Location:** `runs/{agent}/` and `runs/unknown/`

Used by: Session hooks (38 runs)

**Files per run:**
```
run-YYYYMMDD-HHMMSS/
├── .hook_initialized      # Marker file
├── .ralf-metadata         # Run metadata
├── metadata.yaml          # Extended metadata
├── THOUGHTS.md           # Template
├── DECISIONS.md          # Template
└── RESULTS.md            # Template
```

---

## 📈 RUN ANALYSIS

### Planner Runs (87 total)
- **Naming:** run-0001 to run-0080 + run-test + dated runs
- **Loop numbers:** 1-80
- **Average duration:** ~15 minutes (900 seconds)
- **Content:** Rich metadata with discoveries, actions, insights

### Executor Runs (61 total)
- **Naming:** run-0001 to run-0065 (some gaps)
- **Average duration:** ~4-5 minutes (240-300 seconds)
- **Content:** Task execution metrics (LPM, lines changed, commits)

### Architect Runs (47 total)
- **Location:** `architect/runs/archived/`
- **Naming:** run-0001 to run-0047
- **Status:** All archived

### Legacy Runs (38 total)
- **Location:** `runs/unknown/completed/`
- **Naming:** run-YYYYMMDD-HHMMSS format
- **Status:** All completed, mostly empty templates

---

## 🔍 KEY FINDINGS

### 1. DUAL STRUCTURE PROBLEM
**Issue:** Two different run folder structures exist
- Agent runs: `.autonomous/agents/{agent}/runs/` (rich data)
- Session runs: `runs/unknown/` (minimal data)

**Impact:** Fragmented history, inconsistent analysis

### 2. AGENT RUNS ARE THE REAL DATA
- 195 agent runs (planner + executor + architect)
- Rich metadata, decisions, insights
- Actual work tracking happens here

### 3. SESSION RUNS ARE MINIMAL
- 38 session runs
- Mostly empty templates
- Created by hooks but not populated

### 4. NAMING INCONSISTENCY
- Planner: run-0001, run-0002, ... run-0080
- Executor: run-0001, run-0002, ... run-0065
- Legacy: run-20260204-035541

### 5. MISSING LINKS
- No clear connection between session runs and agent runs
- No unified run ID system
- No cross-reference between structures

---

## 💡 RECOMMENDATIONS

### Immediate (Critical)
1. **Unify run structures** - Choose one format
2. **Link session runs to agent runs** - Cross-reference
3. **Standardize naming** - Use consistent format

### Short-term (High Impact)
1. **Migrate legacy runs** - Consolidate into agent structure
2. **Add run relationships** - parent_run, child_runs
3. **Create run index** - Searchable catalog

### Long-term (Strategic)
1. **Run analytics** - Query across all runs
2. **Pattern detection** - Find insights from 236 runs
3. **Run visualization** - Timeline of activity

---

## 📋 QUERY EXAMPLES

### Find All Runs
```bash
find ~/.blackbox5/5-project-memory/blackbox5 -type d -name "run-*" | wc -l
```

### Find Planner Runs
```bash
ls ~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/planner/runs/ | wc -l
```

### Find Latest Runs
```bash
ls -lt ~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/planner/runs/ | head -10
```

### Find Longest Planner Loop
```bash
for dir in ~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/planner/runs/run-*/; do
  duration=$(grep "duration_seconds:" "$dir/metadata.yaml" 2>/dev/null | awk '{print $2}')
  echo "$duration: $(basename $dir)"
done | sort -rn | head -10
```

### Find High-LPM Executor Runs
```bash
for dir in ~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/executor/runs/run-*/; do
  lpm=$(grep "lpm:" "$dir/metadata.yaml" 2>/dev/null | awk '{print $2}')
  [[ -n "$lpm" ]] && echo "$lpm: $(basename $dir)"
done | sort -rn | head -10
```

---

## 🎯 SUMMARY

**The Real Story:**
- **236 total runs** (not 40!)
- **195 agent runs** with rich data
- **Dual structures** causing fragmentation
- **Agent runs are the source of truth**

**Next Steps:**
1. Unify the two run structures
2. Link session runs to agent runs
3. Build analytics on the 195 agent runs

---

*Map v2 - Complete analysis of all 236 run folders*
