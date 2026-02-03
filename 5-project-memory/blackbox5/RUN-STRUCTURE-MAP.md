# Blackbox5 Run Structure Map

**Generated:** 2026-02-04
**Purpose:** Complete reference for RALF run organization and lifecycle

---

## 📁 Run Directory Hierarchy

```
~/.blackbox5/5-project-memory/blackbox5/runs/
│
├── .docs/                          # Documentation for run system
│
├── planner/                        # Planner agent runs (active)
│   └── (empty - planner uses unknown/)
│
├── executor/                       # Executor agent runs (active)
│   └── completed/
│       └── executor-test-001/      # Test run
│
├── unknown/                        # Default/unspecified agent runs
│   ├── completed/                  # Archived runs (38 runs)
│   │   ├── run-20260204-035541/    # Example completed run
│   │   ├── run-20260204-035528/
│   │   └── ... (36 more)
│   └── (active runs go here)
│
└── completed/                      # Generic completed runs

```

---

## 📊 Run Statistics

| Category | Count | Location |
|----------|-------|----------|
| Unknown (completed) | 38 | `runs/unknown/completed/` |
| Executor (completed) | 2 | `runs/executor/completed/` |
| Planner | 0 | `runs/planner/` |
| Active (current) | 0 | All archived |

**Total Runs:** 40

---

## 🏗️ Run Folder Structure

Each run folder contains:

```
run-YYYYMMDD-HHMMSS/
├── .hook_initialized          # Marker file (timestamp)
├── .ralf-metadata             # Run metadata (YAML)
├── metadata.yaml              # Extended run metadata
├── THOUGHTS.md               # Agent reasoning & analysis
├── DECISIONS.md              # Decisions made during run
└── RESULTS.md                # Run outcomes & metrics
```

### File Details

#### `.hook_initialized`
- **Purpose:** Marker that session-start hook ran
- **Content:** ISO timestamp
- **Size:** ~26 bytes

#### `.ralf-metadata`
```yaml
run:
  id: "run-20260204-035541"
  timestamp: "2026-02-04T03:55:41+07:00"
  project: "blackbox5"
  agent_type: "unknown"
  status: initialized

git:
  branch: "main"
  commit: "bbd6c0e"

paths:
  project_root: "/Users/shaansisodia/.blackbox5"
  project_memory: ".../5-project-memory/blackbox5"
  run_dir: ".../runs/unknown/run-20260204-035541"

completion:
  timestamp: "2026-02-04T03:56:52+07:00"
  status: archived
```

#### `metadata.yaml`
```yaml
run:
  id: "run-20260204-035541"
  project: "blackbox5"
  agent: "unknown"
  timestamp_start: "2026-02-04T03:55:41+07:00"
  timestamp_end: "2026-02-04T03:56:52+07:00"
  duration_seconds: 71

state:
  task_claimed: null
  task_status: null
  files_modified: []
  commit_hash: "f7e61d4"

results:
  status: "in_progress"
  summary: ""
  tasks_completed: []
  tasks_created: []
  blockers: []
```

#### `THOUGHTS.md`
Template with sections:
- State Assessment
- Context (Git branch/commit)
- Analysis
- Next Steps

#### `DECISIONS.md`
Template for tracking decisions:
- Decision ID (D-001, D-002, etc.)
- Context
- Decision
- Rationale
- Consequences

#### `RESULTS.md`
Template with:
- Summary
- Tasks Completed
- Tasks Created
- Blockers

---

## 🔄 Run Lifecycle

### Phase 1: Initialization
**Trigger:** Claude Code session starts
**Hook:** `bin/ralf-session-start-hook.sh`

1. Hook detects project (blackbox5)
2. Creates run folder: `runs/unknown/run-YYYYMMDD-HHMMSS/`
3. Generates all template files
4. Sets environment variables:
   - `RALF_RUN_DIR`
   - `RALF_RUN_ID`
   - `RALF_PROJECT_ROOT`

### Phase 2: Execution
- Agent works on task
- Post-tool hook logs file changes to events.yaml
- Agent can update THOUGHTS.md, DECISIONS.md

### Phase 3: Completion
**Trigger:** Claude Code session ends
**Hook:** `bin/ralf-stop-hook.sh`

1. Updates metadata.yaml with end timestamp
2. Calculates duration
3. Records files modified
4. Updates .ralf-metadata with completion info
5. Moves run to `completed/` folder

---

## 🔧 Hook System

### Session Start Hook
**File:** `bin/ralf-session-start-hook.sh`
**Trigger:** `.claude/settings.json` - `SessionStart` event
**Purpose:** Create run folder and templates

### Stop Hook
**File:** `bin/ralf-stop-hook.sh`
**Trigger:** `.claude/settings.json` - `Stop` event
**Purpose:** Finalize run metadata and archive

### Post-Tool Hook
**File:** `bin/ralf-post-tool-hook.sh`
**Trigger:** `.claude/settings.json` - `PostToolUse` event
**Purpose:** Detect file changes and log to events.yaml

---

## 📈 Observations & Issues

### Current State
1. **All runs in "unknown"** - Agent type not being detected
2. **No active runs** - All 38 runs archived
3. **Empty templates** - Most THOUGHTS.md files have placeholder content
4. **Short durations** - Most runs < 2 minutes

### Potential Optimizations

#### 1. Agent Type Detection
**Issue:** All runs marked as "unknown"
**Solution:** Improve agent detection in session-start hook
- Check prompt content
- Use working directory patterns
- Allow agent to self-identify

#### 2. Run Folder Organization
**Issue:** All runs in `unknown/` regardless of agent
**Solution:** Auto-sort into `planner/` or `executor/` based on detected type

#### 3. Template Quality
**Issue:** Templates are mostly empty
**Solution:**
- Add more structured prompts
- Include recent context from events.yaml
- Pre-populate with relevant task info

#### 4. Archive Strategy
**Issue:** Runs moved immediately to completed/
**Solution:**
- Keep recent runs (last 24h) in active folder
- Only archive after verification
- Add "in_review" status

#### 5. Metadata Enrichment
**Issue:** Limited metadata captured
**Suggestions:**
- Add lines added/removed
- Track tool usage counts
- Record model used (Claude, Kimi, etc.)
- Capture cost/time metrics

---

## 🗂️ File Sizes (Typical)

| File | Size Range | Purpose |
|------|------------|---------|
| .hook_initialized | 20-30 bytes | Marker |
| .ralf-metadata | 600-700 bytes | Core metadata |
| metadata.yaml | 350-450 bytes | Extended metadata |
| THOUGHTS.md | 400-1000 bytes | Analysis |
| DECISIONS.md | 300-800 bytes | Decisions |
| RESULTS.md | 400-1000 bytes | Outcomes |

**Typical Run Folder:** 2-4 KB total

---

## 🔍 Query Examples

### Find Recent Runs
```bash
ls -lt ~/.blackbox5/5-project-memory/blackbox5/runs/unknown/completed/ | head -10
```

### Find Longest Runs
```bash
for dir in ~/.blackbox5/5-project-memory/blackbox5/runs/unknown/completed/run-*/; do
  duration=$(grep "duration_seconds:" "$dir/metadata.yaml" 2>/dev/null | awk '{print $2}')
  echo "$duration: $(basename $dir)"
done | sort -rn | head -10
```

### Find Runs with Blockers
```bash
grep -l "blockers:" ~/.blackbox5/5-project-memory/blackbox5/runs/unknown/completed/run-*/RESULTS.md
```

---

## 📋 Recommendations

### Immediate (High Impact)
1. **Fix agent type detection** - Sort runs into planner/executor folders
2. **Add run duration tracking** - Better visibility into work patterns
3. **Enrich templates** - Pre-populate with task context

### Short-term (Medium Impact)
1. **Add metrics collection** - Lines changed, tools used, cost
2. **Create run dashboard** - Quick overview of recent activity
3. **Implement run search** - Find runs by task, date, or outcome

### Long-term (Strategic)
1. **Run analytics** - Pattern detection across runs
2. **Auto-categorization** - Tag runs by type (bugfix, feature, refactor)
3. **Run comparison** - Diff between similar runs

---

*Map generated by analyzing 40 run folders and hook scripts*
