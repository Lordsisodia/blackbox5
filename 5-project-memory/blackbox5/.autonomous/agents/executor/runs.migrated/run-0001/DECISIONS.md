# Decisions - TASK-1738366802

## Which Runs to Keep vs Archive

**Context:** Need to decide how many runs to keep in completed/ vs move to archived/

**Selected:** Keep last 5 runs in completed/, archive the remaining 42

**Rationale:**
- Task specification explicitly stated: "Keep recent completed runs (last 5) in completed/ for quick reference"
- 5 runs provides sufficient recent history for quick access
- 42 runs archived maintains the analysis history without cluttering completed/

**Reversibility:** HIGH - Runs can be moved back from archived/ to completed/ if needed

## Run Selection Method

**Context:** Need to determine which runs are "oldest" vs "newest"

**Selected:** Alphabetical sort of run directory names

**Rationale:**
- Run names follow patterns: run-0001, run-1769*, run-20260131_*
- Alphabetical sort correctly orders: run-0001 (earliest) → run-20260131_* (latest)
- This matches the chronological order of run creation

**Reversibility:** MEDIUM - If naming convention changes, sort order may need adjustment
