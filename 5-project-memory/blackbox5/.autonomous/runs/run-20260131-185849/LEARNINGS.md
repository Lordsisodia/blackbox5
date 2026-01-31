# RALF Run Learnings

**Run ID:** run-20260131-185849

---

## Learning 1: Documentation Drift

**Discovery:** RALF prompt documentation (ralf.md) contains outdated information that contradicts the actual implementation.

**Details:**
- Documentation says: "Never main/master" — Only run on dev, feature/*, or other non-production branches
- Implementation (ralf-loop.sh line 178-179): "Branch check removed - RALF can run on main"

**Implication:** When conflicts exist between documentation and implementation code, trust the implementation. Documentation may not have been updated when features changed.

**Recommendation:** Update ralf.md to remove or clarify the branch safety restriction.

---

## Learning 2: Environment Variable Initialization

**Discovery:** RALF environment variables are not automatically set when invoked. They must be set by the ralf-loop.sh script.

**Details:**
- Variables needed: RALF_PROJECT_DIR, RALF_ENGINE_DIR, RALF_BLACKBOX5_DIR, RALF_RUN_DIR
- These are exported by ralf-loop.sh (lines 411-414) before running the prompt
- When RALF is invoked directly (not through the loop), these variables don't exist

**Implication:** Always verify environment variables are set. If not, derive them from:
- RALF_PROJECT_DIR: From routes.yaml or .autonomous location
- RALF_ENGINE_DIR: From 2-engine/.autonomous location
- RALF_BLACKBOX5_DIR: Root of blackbox5 project
- RALF_RUN_DIR: Create new run directory with timestamp

---

## Learning 3: Task Queue Structure

**Discovery:** Task directories reflect workflow state. Absence of `active/` directory means no work to do.

**Details:**
- Expected structure: `tasks/active/`, `tasks/completed/`, `tasks/pending/`
- Current state: Only `tasks/completed/` exists with 38+ tasks
- This indicates healthy project with all work completed

**Implication:** No active tasks = RALF should report COMPLETE and exit successfully.

---

## Learning 4: Run Directory Template

**Discovery:** RALF runs create documentation files but no explicit template exists.

**Details:**
- Expected files in run directory: THOUGHTS.md, RESULTS.md, DECISIONS.md, ASSUMPTIONS.md, LEARNINGS.md
- RALF prompt says these are "Pre-created" with "FILL_ME" markers
- In practice, these may need to be created manually if ralf-loop.sh doesn't create them

**Implication:** When invoked outside the loop, create these files explicitly with proper content.

---

## Learning 5: Project Health Indicators

**Discovery:** Multiple indicators show blackbox5 is healthy and actively maintained.

**Evidence:**
1. **Recent Commits**: Quality improvements (fixing bare except clauses)
2. **Test Coverage**: PLAN-003 shows 9/9 tests passing (100%)
3. **Feature Completion**: Planning Agent fully integrated with Vibe Kanban
4. **Documentation**: Comprehensive skill documentation created
5. **Tooling**: CLI tools implemented for workflows

**Implication:** RALF system is functioning as intended. The autonomous framework is shipping features while humans sleep (as stated in RALF purpose).

---

## Learning 6: routes.yaml is Central

**Discovery:** The routes.yaml file contains canonical path definitions for the entire blackbox5 project.

**Details:**
- Location: `/workspaces/blackbox5/5-project-memory/blackbox5/.autonomous/routes.yaml`
- Contains paths to: engine, memory, knowledge, docs, tools, integrations
- Used by RALF to understand project structure

**Implication:** Always read routes.yaml first to understand project layout before taking action.
