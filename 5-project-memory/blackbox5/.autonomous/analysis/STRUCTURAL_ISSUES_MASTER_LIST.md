# BlackBox5 Structural Issues Master List

## Overview
This document captures all architectural/structural issues identified by the 5 architect scouts.
These are NOT tactical bugs (like hardcoded values) but fundamental structural problems affecting how the system fits together.

---

## Issue #1: 2-engine/ vs 5-project-memory/blackbox5/ Split (CRITICAL)
**Status**: Analysis Complete → Implementation Ready
**Owner**: TBD
**Confidence**: 85%

### Problem
The boundary between engine (shared across projects) and project-specific memory is unclear.
18 duplications exist between the two locations. 47+ hardcoded cross-boundary paths.
269 files contain hardcoded references.

### Guiding Principle (from user)
- **Engine (2-engine/)**: Anything standardized across ALL projects
- **Project Memory (5-project-memory/blackbox5/)**: Anything specific to BlackBox5 project

### Analysis Complete

**Scout Reports:**
- `scout-content-misplacement.md` - 8 engine items → project, 11 project items → engine
- `scout-duplications-deep-dive.md` - 18 categories analyzed
- `scout-routes-structure.md` - routes.yaml issues documented
- `scout-agent-architecture.md` - agent coupling analysis
- `verification-engine-project-issues.md` - Verification of all issues found
- `scout-hidden-dependencies.md` - Hidden dependencies discovered

**Key Findings:**
1. **47 hardcoded paths** crossing boundaries (in 8 Python scripts)
2. **269 files** contain hardcoded `.blackbox5` path references
3. **routes.yaml has incorrect paths** (10+ paths with wrong nesting)
4. **8 engine scripts** are BlackBox5-specific (should move to project)
5. **11 project items** are generic (should move to engine)
6. **6-agent pipeline** is tightly coupled to BlackBox5 structure
7. **12 bb5-* commands** depend on engine library (dry_run.sh)
8. **Hidden dependencies** in hooks, environment variables, runtime checks

### Additional Issues Discovered
1. Engine routes.yaml has outdated run path (references non-existent `ralf-core`)
2. Shell scripts also have hardcoded paths (bb5-scout-improve, ralf-improve)
3. bin/blackbox.py uses relative paths assuming specific structure
4. All 12 bb5-* commands source dry_run.sh from engine (will fail if moved)

### Tasks Created
- TASK-ARCH-060: Path abstraction layer
- TASK-ARCH-061: Migrate engine scripts to project
- TASK-ARCH-062: Consolidate duplicate prompts
- TASK-ARCH-063: Standardize project content to engine
- TASK-ARCH-064: Fix routes.yaml incorrect paths
- TASK-ARCH-065: Create path resolution library
- TASK-ARCH-066: Unify agent communication
- TASK-ARCH-067: Decouple agents from project structure

---

## Issue #2: SSOT Violations - Task Status in Multiple Places (HIGH)
**Status**: Analysis Complete
**Owner**: TBD

### Problem
Task status exists in multiple locations with no single source of truth:
- `queue.yaml` - queue status (90 tasks tracked)
- `STATE.yaml` - system state
- `events.yaml` - event log (2830+ events)
- Individual task files - task status
- Timeline.yaml - milestone tracking

### Impact
- Data inconsistency (queue shows 25 completed, task files may differ)
- Race conditions (multiple agents modify queue.yaml)
- Unclear which status is authoritative
- Manual sync required (0% success rate)

### Scout Analysis
**Report:** `scout-data-flow.md`

**Key Findings:**
1. **No clear state ownership**: Queue owns priority/ordering, task files own details, events own history
2. **Race condition risk**: Multiple agents can modify queue.yaml simultaneously (no file locking)
3. **Inconsistent formats**: queue.yaml uses YAML list, task.md uses markdown frontmatter
4. **Status propagation broken**: Manual sync between systems doesn't work

### Recommendations
1. Make task.md files the canonical source of truth
2. Generate queue.yaml from scanning task files (read-only)
3. Remove manual queue updates
4. Add file locking for any shared state modifications

---

## Issue #3: Missing Storage Abstraction Layer (HIGH)
**Status**: Analysis Complete
**Owner**: TBD

### Problem
Direct YAML/JSON manipulation throughout codebase. 38+ files use raw file I/O. No unified storage interface.

### Impact
- Code duplication (38+ instances of yaml.safe_load())
- Hard to change storage backends
- No transaction support
- Testing difficulty
- Race conditions (no file locking)

### Scout Analysis
**Report:** `scout-abstraction-layers.md`

**Key Findings:**
1. **38 files use direct file I/O**: yaml.safe_load(), json.load(), open() scattered throughout
2. **No StorageBackend abstraction**: Every script implements its own loading/saving
3. **Pattern repeated in**: queue-manager, reanalysis-engine, metrics-collector, sync-state, validate-ssot, etc.
4. **No transaction support**: Partial writes possible if interrupted

### Missing Abstractions
| Layer | Status | Issue |
|-------|--------|-------|
| Storage | MISSING | No unified storage interface |
| Queue | MISSING | Direct YAML manipulation |
| Task | PARTIAL | Multiple incompatible Task classes |
| Agent | MISSING | No base Agent class |
| Event | PARTIAL | No Event interface |
| Configuration | MISSING | No Config service |

### Recommendations
1. Create `StorageBackend` abstract class with load(), save(), query() methods
2. Implementations: YAMLStorage, JSONStorage, VectorStorage
3. Add transaction support (temp files + atomic move)
4. Add file locking for concurrent access

---

## Issue #4: RALF Knows Project Structure (MEDIUM)
**Status**: Analysis Complete
**Owner**: TBD

### Problem
RALF components have hardcoded knowledge of BlackBox5 directory structure.
All 6 agent scripts hardcode paths to `~/.blackbox5/5-project-memory/blackbox5`.

### Impact
- Violates separation of concerns
- RALF can't be reused for other projects
- Changes to structure require RALF changes
- Tight coupling to BlackBox5 (score: 10/10)

### Scout Analysis
**Report:** `scout-component-boundaries.md`, `scout-agent-architecture.md`

**Key Findings:**
1. **All 6 agent scripts hardcoded**:
   - scout-intelligent.py
   - planner-prioritize.py
   - executor-implement.py
   - verifier-validate.py
   - improvement-loop.py
   - scout-task-based.py

2. **Direct manipulation of**:
   - Task files
   - queue.yaml
   - skill metrics
   - Events/heartbeat

3. **Cannot be reused** for other projects due to tight coupling

### Recommendations
1. Extract all paths to configuration
2. Create agent-config.yaml with project paths
3. Make RALF project-agnostic via CLI args or env vars
4. Move BlackBox5-specific agents to project directory

---

## Issue #5: File-Based Coordination - Race Conditions (MEDIUM)
**Status**: Analysis Complete
**Owner**: TBD

### Problem
12 hooks across 8 lifecycle events use file-based coordination without locking.
Multiple race conditions identified.

### Impact
- Data corruption (queue.yaml, events.yaml)
- Lost events
- Duplicate task execution
- Fragile integrations
- Hard to debug

### Scout Analysis
**Report:** `scout-integration-points.md`

**Race Conditions Found:**

| File | Risk Level | Issue |
|------|------------|-------|
| `queue.yaml` | **CRITICAL** | Task claims use read-modify-write without locks |
| `events.yaml` | **CRITICAL** | Append-only writes from multiple sources |
| `execution-state.yaml` | **MEDIUM** | Slot updates via yq eval -i (not atomic) |
| `agent-state.yaml` | **MEDIUM** | sed-based updates with backup files |

**Specific Issues:**
1. **Task Claim Race** - `bb5-parallel-dispatch.sh` claims tasks by reading queue.yaml, then writing back with yq - no file locking
2. **Slot Status Updates** - Multiple slots updating execution-state.yaml concurrently
3. **Event Logging** - Hook-triggered events append to events.yaml without coordination
4. **Synchronous blocking writes** - Each event appends directly to YAML file

### Recommendations
1. Implement file locking using `flock` for all coordination files
2. Create event queue with proper buffering
3. Use atomic operations (temp file + move)
4. Add health monitoring for stuck coordination

---

## Issue #6: Component Boundary Violations (MEDIUM)
**Status**: Analysis Complete
**Owner**: TBD

### Problem
6 major components with unclear boundaries and tight coupling:
- RALF System
- Task System
- Agent System
- Skill System
- Memory System
- Queue System

### Impact
- Tight coupling (score 8-10/10)
- Hard to test
- Changes ripple through system
- CLI commands bypass orchestrator
- Circular dependencies

### Scout Analysis
**Report:** `scout-component-boundaries.md`

**Boundary Violations Found:**

| Violation | Components | Severity |
|-----------|------------|----------|
| Hardcoded paths | RALF, Agent, Task | CRITICAL |
| SSOT violations | Task, Queue, Events | HIGH |
| Missing storage abstraction | All components | HIGH |
| RALF knows project structure | RALF, all others | MEDIUM |
| File-based coordination | Agent, Queue, Events | MEDIUM |
| Circular dependencies | Skill, Task, Agent | MEDIUM |
| Dual implementations | Agent, Memory | MEDIUM |

**Tight Coupling Areas:**
1. **Directory Structure** (10/10) - 47+ hardcoded path references
2. **File Formats** (9/10) - YAML schemas hardcoded across components
3. **Task ID Conventions** (8/10) - Specific task ID patterns assumed
4. **Configuration Files** (8/10) - Direct references to specific YAML files

### Recommendations
1. Create configuration-driven architecture
2. Standardize agent interface contract
3. Implement storage abstraction layer
4. Create unified queue interface
5. Make RALF project-agnostic

---

## Issue #7: Missing Unified Queue Interface (MEDIUM)
**Status**: Analysis Complete
**Owner**: TBD

### Problem
6-agent pipeline uses raw YAML files with inline Python parsing.
No Queue abstraction. Direct file manipulation in bb5-queue-manager.py.

### Impact
- Can't swap queue implementations
- Hard to test
- No queue-level features (priorities, retries, etc.)
- Queue operations mixed with file I/O logic
- Race conditions (no locking)

### Scout Analysis
**Report:** `scout-abstraction-layers.md`

**Key Findings:**
1. **Direct YAML manipulation** in bb5-queue-manager.py lines 241-332
2. **No Queue class** - just raw file read/write
3. **No abstraction layer** - YAML structure exposed to callers
4. **Mixed concerns** - Queue operations + file I/O + business logic

### Recommendations
1. Create `Queue` class with methods: enqueue(), dequeue(), peek(), list()
2. Hide YAML structure from callers
3. Add file locking for thread safety
4. Enable queue backend changes without code changes

---

## Issue #8: Missing Task State Service (MEDIUM)
**Status**: Analysis Complete
**Owner**: TBD

### Problem
No centralized service for task state management.
Each component manages state independently.
No lifecycle management for resources.

### Impact
- State inconsistency
- No state change auditing
- Hard to track task lifecycle
- Orphaned resources (tasks, runs, events)
- Unbounded growth (2830+ events, run folders never cleaned)

### Scout Analysis
**Reports:** `scout-data-flow.md`, `scout-lifecycle-management.md`

**Lifecycle Issues Found:**

| Resource | Issue | Impact |
|----------|-------|--------|
| Tasks | Orphaned, inconsistent state | Confusion about what's real |
| Runs | No cleanup, unbounded growth | Disk space, clutter |
| Agents | No state tracking | Can't monitor agent health |
| Goals/Plans | No auto-progression | Stale goals |
| Events | Unbounded growth (2830+), no retention | Performance, noise |

**Missing Lifecycle Management:**
1. **No automated archival** - Old tasks/runs accumulate forever
2. **No retention policy** - All history kept indefinitely
3. **No cleanup on failure** - Failed agents don't clean up state
4. **No lifecycle hooks** - on_create, on_complete, on_archive

### Recommendations
1. Implement TaskStateService with clear ownership
2. Add automated lifecycle management
3. Create retention policies (e.g., archive after 30 days)
4. Add lifecycle hooks for cleanup actions
5. Implement event aggregation and retention

---

## Issue #9: Broken Configuration System (HIGH)
**Status**: Analysis Complete
**Owner**: TBD

### Problem
Configuration is scattered across 20+ YAML files with no centralized system.
Documented hierarchy (User > Project > Engine > Environment > Base > Default) is NOT implemented.

### Impact
- No single source of truth for configuration
- Hardcoded paths instead of config values
- Duplicate configuration files
- No config validation in practice
- Inconsistent config loading across scripts

### Scout Analysis
**Report:** `scout-configuration-system.md`

**Key Findings:**
1. **20+ config files** scattered across engine and project
2. **Duplicate configs**: Two skill-usage.yaml files
3. **Hardcoded paths** in bin/ralf-report, bin/ralf-branch, bin/ralf-analyze, bin/blackbox
4. **Config schema exists** (config.schema.yaml) but NOT used
5. **User config** (~/.blackbox5/config.yaml) documented but doesn't exist
6. **Routes.yaml not used** - scripts hardcode paths instead
7. **Environment variables inconsistent** - RALF_PROJECT_ROOT, BB5_PROJECT_ROOT, BLACKBOX5_HOME all used

**Configuration Files:**
- Engine: 13 config files (routes.yaml, base.yaml, default.yaml, dev/prod/staging.yaml, skill-registry.yaml, etc.)
- Project: 5 config files (routes.yaml, skill-selection.yaml, skill-metrics.yaml, skill-usage.yaml x2)

### Recommendations
1. Create central config loader implementing documented hierarchy
2. Eliminate hardcoded paths - use config values
3. Merge duplicate configs
4. Add config validation against schema
5. Standardize environment variables
6. Make routes.yaml functional (scripts should use it)

---

## Issue #10: Untestable Architecture (HIGH)
**Status**: Analysis Complete
**Owner**: TBD

### Problem
Architecture lacks testability due to tight coupling, hardcoded paths, and no dependency injection.
Core business logic has zero test coverage.

### Impact
- Cannot unit test components in isolation
- Changes break things unexpectedly
- No confidence in refactoring
- Manual testing only

### Scout Analysis
**Report:** `scout-testing-infrastructure.md`

**Key Findings:**
1. **7+ Python agent scripts** in 2-engine/.autonomous/bin/ have ZERO tests
2. **10+ Python scripts** in 5-project-memory/blackbox5/bin/ have ZERO tests
3. **Hardcoded paths** prevent testing with mock directories
4. **No dependency injection** - components instantiate dependencies directly
5. **Tight coupling to file system** - raw open()/read()/write() calls
6. **No test fixtures** - each test creates own mock data

**Components Lacking Tests (HIGH RISK):**
- scout-intelligent.py
- planner-prioritize.py
- executor-implement.py
- verifier-validate.py
- improvement-loop.py
- bb5-queue-manager.py

**Components WITH Tests:**
- Decision Registry, Memory System, Session Tracker, State Machine, Workspace
- (All infrastructure, no business logic)

### Recommendations
1. Add configuration injection (pass paths as parameters)
2. Create FileSystem abstraction for test mocking
3. Create centralized test fixtures
4. Add pytest configuration
5. Priority: Test queue manager, then agents

---

---

## Priority Order (Recommended)

1. **Issue #1** - Engine/Project split (foundational)
2. **Issue #9** - Configuration system (enables other fixes)
3. **Issue #3** - Storage abstraction (enables other fixes)
4. **Issue #2** - SSOT violations (data integrity)
5. **Issue #4** - RALF decoupling (reusability)
6. **Issue #6** - Component boundaries (maintainability)
7. **Issue #7** - Queue interface (scalability)
8. **Issue #5** - File coordination (reliability)
9. **Issue #8** - Task state service (observability)
10. **Issue #10** - Testable architecture (quality)

---

## Notes

- Created: 2026-02-06
- Updated: 2026-02-06
- Source: 5 Architect Scout Analysis + 13 Deep Dive Scouts
- Status: **10 structural issues identified and analyzed**
- Confidence: **85%** that all major engine/project issues found

## Summary Statistics

| Metric | Count |
|--------|-------|
| **Structural Issues** | 10 |
| **Critical Issues** | 2 (Issues #1, #9) |
| **High Priority** | 4 (Issues #2, #3, #10) |
| **Medium Priority** | 4 (Issues #4, #5, #6, #7, #8) |
| **Scout Reports** | 19 documents |
| **Tasks Created** | 8 (for Issue #1 only) |
| **Hardcoded Paths** | 47+ confirmed, 269 suspected |
| **Files with Path References** | 269 |

## Documents Created (19 Total)

### Initial Analysis (6 files)
1. `engine-project-split-analysis.md` - Consolidated analysis
2. `cross-boundary-paths.md` - 47 hardcoded paths
3. `engine-content-analysis.md` - Engine content review
4. `project-content-analysis.md` - Project content review
5. `engine-project-duplications.md` - 18 duplications
6. `migration-strategy.md` - Migration plan

### Scout Reports (12 files)
7. `scout-content-misplacement.md` - Content misplacement
8. `scout-duplications-deep-dive.md` - Duplications deep dive
9. `scout-routes-structure.md` - Routes.yaml structure
10. `scout-agent-architecture.md` - Agent architecture
11. `scout-data-flow.md` - Data flow and state ownership
12. `scout-component-boundaries.md` - Component boundaries
13. `scout-abstraction-layers.md` - Abstraction layers
14. `scout-integration-points.md` - Integration points
15. `scout-lifecycle-management.md` - Lifecycle management
16. `verification-engine-project-issues.md` - Verification report
17. `scout-hidden-dependencies.md` - Hidden dependencies
18. `scout-configuration-system.md` - Configuration system
19. `scout-testing-infrastructure.md` - Testing infrastructure

### Plan
- `plans/active/engine-project-boundary-plan/epic.md`

### Tasks (8 total for Issue #1)
- TASK-ARCH-060 through TASK-ARCH-067

---

## Issue #11: SSOT - Task State Violations (HIGH)
**Status**: Analysis Complete
**Owner**: TBD
**Report**: `ssot-task-state-violations.md`

### Problem
Task state exists in **5 different places** with no single source of truth:
- `tasks/active/*/task.md` - Individual task files (canonical)
- `queue.yaml` - Task queue with duplicated status
- `STATE.yaml` - Project state with task lists
- `timeline.yaml` - Task events
- `events.yaml` - Execution events

### Key Findings
- Task status duplicated in 4+ places
- 13 duplicate task entries in queue.yaml
- TASK-ARCH-016 appears twice with conflicting statuses
- Timeline shows hundreds of completions, STATE.yaml shows only 4

### Tasks to Create
- TASK-SSOT-001 through TASK-SSOT-005

---

## Issue #12: SSOT - Configuration Violations (HIGH)
**Status**: Analysis Complete
**Owner**: TBD
**Report**: `ssot-configuration-violations.md`

### Problem
Configuration duplicated across **4 skill files** with **32+ hardcoded paths** in scripts.

### Key Findings
- Skills defined in FOUR places (skill-registry.yaml, skill-selection.yaml, skill-metrics.yaml, skill-usage.yaml)
- 32+ bin scripts hardcode `5-project-memory/blackbox5` pattern
- Agent prompts exist in BOTH engine and project
- CLAUDE.md duplicates skill-selection.yaml content

### Tasks to Create
- TASK-SSOT-006 through TASK-SSOT-011

---

## Issue #13: SSOT - Agent State Violations (MEDIUM)
**Status**: Analysis Complete
**Owner**: TBD
**Report**: `ssot-agent-state-violations.md`

### Problem
Agent state stored in **4+ places** with **529 "unknown" agent entries**.

### Key Findings
- `agent-state.yaml` is EMPTY (should be registry)
- `events.yaml` has 529 `agent_type: unknown`
- Status tracked in heartbeat.yaml, execution-state.yaml, events.yaml (inconsistent)
- Run data duplicated across metadata.yaml, heartbeat.yaml, events.yaml

### Tasks to Create
- TASK-SSOT-012 through TASK-SSOT-016

---

## Issue #14: SSOT - Knowledge/Decisions Violations (HIGH)
**Status**: Analysis Complete
**Owner**: TBD
**Report**: `ssot-knowledge-violations.md`

### Problem
Knowledge scattered across **800+ locations**. Decisions in **242 files** not in central registry.

### Key Findings
- 242 DECISIONS.md files in run folders
- 43 LEARNINGS.md, 250 THOUGHTS.md, 42 ASSUMPTIONS.md scattered
- Skill metrics in 3 files with different schemas
- Scout reports exist in BOTH JSON and YAML (100% duplication)
- security_checks.json in 6 locations

### Tasks to Create
- TASK-SSOT-017 through TASK-SSOT-022

---

## Issue #15: SSOT - Goals/Plans Violations (MEDIUM)
**Status**: Analysis Complete
**Owner**: TBD
**Report**: `ssot-goals-plans-violations.md`

### Problem
Goal/plan data duplicated across **6+ locations** with status mismatches.

### Key Findings
- IG-008: goal.yaml shows `draft`, INDEX.yaml shows `in_progress`
- IG-009: goal.yaml shows `completed`, INDEX.yaml shows `in_progress`
- Goals tracked in goal.yaml, INDEX.yaml, goals.yaml, STATE.yaml
- Progress tracked in goal.yaml, INDEX.yaml, timeline.yaml, epic.md
- 8 goal-specific timeline.yaml files + root timeline.yaml

### Tasks to Create
- TASK-SSOT-023 through TASK-SSOT-027

---

## Issue #16: SSOT - Metrics/Monitoring Violations (MEDIUM)
**Status**: Analysis Complete
**Owner**: TBD
**Report**: `ssot-metrics-monitoring-violations.md`

### Problem
Metrics duplicated across **4+ locations** with inconsistent reporting.

### Key Findings
- Skill metrics in 4 files (skill-metrics.yaml, 2x skill-usage.yaml, CLAUDE.md)
- Task counts in 3 places (queue.yaml shows 25 completed, actual is 30+)
- security_checks.json in 6 locations
- Events in 5+ files
- Dashboards calculate independently (may not match)

### Tasks to Create
- TASK-SSOT-028 through TASK-SSOT-032

---

## Issue #17: SSOT - Run/Agent Outputs Violations (HIGH)
**Status**: Analysis Complete
**Owner**: TBD
**Report**: `ssot-run-outputs-violations.md`

### Problem
Run outputs scattered across **10+ locations** with **835+ files**.

### Key Findings
- 482+ run folders in 10+ locations
- Each run has 4 files (THOUGHTS.md, DECISIONS.md, LEARNINGS.md, RESULTS.md)
- 1,928 output files with duplicated content patterns
- Analysis reports in BOTH JSON and YAML (8 reports = 16 files)
- Decision registry EMPTY but 242+ files have decisions

### Tasks to Create
- TASK-SSOT-033 through TASK-SSOT-038

---

## Issue #18: SSOT - Documentation Violations (MEDIUM)
**Status**: Analysis Complete
**Owner**: TBD
**Report**: `ssot-documentation-violations.md`

### Problem
Documentation duplicated across **150+ files** with **11 major duplications**.

### Key Findings
- Skill system documented in 5+ places
- Template system in 4 places
- First principles in 3+ places
- RALF/improvement loop in 4+ places
- CLAUDE.md is 2,000+ lines (needs splitting)

### Tasks to Create
- TASK-SSOT-039 through TASK-SSOT-045

---

## Issue #19: SSOT - Hooks/Triggers Violations (MEDIUM)
**Status**: Analysis Complete
**Owner**: TBD
**Report**: `ssot-hooks-triggers-violations.md`

### Problem
Hooks scattered across **3 directories** with **6 different agent detection implementations**.

### Key Findings
- 33+ hook scripts in 3 locations
- 6 different agent detection methods
- 5+ events.yaml files with no synchronization
- Trigger rules in 3 places (CLAUDE.md, skill-selection.yaml, scripts)
- 529 `agent_type: unknown` in events.yaml

### Tasks to Create
- TASK-SSOT-046 through TASK-SSOT-052

---

## Issue #20: SSOT - External Integrations Violations (CRITICAL)
**Status**: Analysis Complete
**Owner**: TBD
**Report**: `ssot-external-integrations-violations.md`

### Problem
**CRITICAL SECURITY ISSUE**: Hardcoded credentials. MCP configs in 3+ places.

### Key Findings (SECURITY)
- **HARDCODED TELEGRAM BOT TOKEN** in 2 files
- **HARDCODED ZAI API KEY** in secrets.yaml
- MCP server config in 3+ places
- GitHub config in 4+ files
- No centralized secret management

### Immediate Actions Required
1. Remove hardcoded credentials
2. Rotate exposed API keys
3. Implement environment variables

### Tasks to Create
- TASK-SSOT-053 through TASK-SSOT-060 (includes URGENT security tasks)

---

## Summary: All 20 Structural Issues

| Issue | Name | Priority | Status |
|-------|------|----------|--------|
| #1 | Engine/Project Split | CRITICAL | 8 tasks created |
| #2 | SSOT - Task State | HIGH | Analysis complete |
| #3 | Missing Storage Abstraction | HIGH | Analysis complete |
| #4 | RALF Knows Project Structure | MEDIUM | Analysis complete |
| #5 | File-Based Coordination | MEDIUM | Analysis complete |
| #6 | Component Boundary Violations | MEDIUM | Analysis complete |
| #7 | Missing Queue Interface | MEDIUM | Analysis complete |
| #8 | Missing Task State Service | MEDIUM | Analysis complete |
| #9 | Broken Configuration System | HIGH | Analysis complete |
| #10 | Untestable Architecture | HIGH | Analysis complete |
| #11 | SSOT - Task State | HIGH | Analysis complete |
| #12 | SSOT - Configuration | HIGH | Analysis complete |
| #13 | SSOT - Agent State | MEDIUM | Analysis complete |
| #14 | SSOT - Knowledge/Decisions | HIGH | Analysis complete |
| #15 | SSOT - Goals/Plans | MEDIUM | Analysis complete |
| #16 | SSOT - Metrics/Monitoring | MEDIUM | Analysis complete |
| #17 | SSOT - Run/Agent Outputs | HIGH | Analysis complete |
| #18 | SSOT - Documentation | MEDIUM | Analysis complete |
| #19 | SSOT - Hooks/Triggers | MEDIUM | Analysis complete |
| #20 | SSOT - External Integrations | **CRITICAL** | URGENT security issues |

---

## SSOT Scout Reports (10 files)

20. `ssot-task-state-violations.md` - Task state analysis
21. `ssot-configuration-violations.md` - Configuration analysis
22. `ssot-agent-state-violations.md` - Agent state analysis
23. `ssot-knowledge-violations.md` - Knowledge/decisions analysis
24. `ssot-goals-plans-violations.md` - Goals/plans analysis
25. `ssot-metrics-monitoring-violations.md` - Metrics analysis
26. `ssot-run-outputs-violations.md` - Run outputs analysis
27. `ssot-documentation-violations.md` - Documentation analysis
28. `ssot-hooks-triggers-violations.md` - Hooks/triggers analysis
29. `ssot-external-integrations-violations.md` - External integrations analysis

---

## Updated Statistics

| Metric | Count |
|--------|-------|
| **Structural Issues** | 20 |
| **Critical Issues** | 2 (Issues #1, #20) |
| **High Priority** | 9 |
| **Medium Priority** | 9 |
| **Scout Reports** | 29 documents |
| **Tasks Created** | 8 (for Issue #1) |
| **Tasks to Create** | ~60 (for SSOT issues) |
| **Hardcoded Paths** | 47+ confirmed |
| **Security Issues** | 3 (hardcoded credentials) |

---

## Confidence Assessment: 85%

**Why not 100%?**
- Dynamic path references (runtime-constructed) may not be caught
- Some paths in documentation/comments not fully scanned
- Template variables may resolve to hardcoded paths
- 2-engine/core/ directory not fully analyzed
- Runtime dependency analysis not performed

**Gaps for 100% confidence:**
1. Full scan of 2-engine/core/ for project references
2. Audit of ALL shell scripts (not just bb5-*)
3. Analysis of skill files in 2-engine/.autonomous/skills/
4. Runtime testing to catch dynamic path constructions
5. Verification of template files are truly generic
