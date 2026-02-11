# Run 20260209_130541 - DECISIONS

**Started:** 2026-02-09T13:05:41Z

## Decisions Made

### 2026-02-09T13:07:00Z - Agent Definition Format Standard

**Context:** Current agent definitions lack proper YAML frontmatter and consistent structure needed for Claude Code plugin compatibility.

**Options Considered:**
1. Keep current format - simple markdown with headers
2. Add YAML frontmatter - standard Claude Code plugin format
3. Create separate agent registry - JSON/YAML index file

**Decision:** Adopt YAML frontmatter format for all agents (Option 2).

**Rationale:**
- Aligns with Claude Code plugin conventions
- Enables automatic agent discovery and activation
- Provides metadata for tool selection and model choice
- Used by the reference implementation in claude-workflow-v2

**Confidence:** High

**Reversibility:** Easy - can remove frontmatter if needed

**Related:** Agent auto-activation via hooks

---

### 2026-02-09T13:08:00Z - Path Reference Strategy

**Context:** `activate-core-team.md` contains hardcoded absolute paths that won't work across different environments.

**Options Considered:**
1. Use environment variables - `${BB5_DIR}/.claude/agents/...`
2. Use relative paths - `.claude/agents/...`
3. Use plugin root variable - `${CLAUDE_PLUGIN_ROOT}/.claude/agents/...`

**Decision:** Use relative paths from BB5 root (Option 2).

**Rationale:**
- Simple and portable across environments
- Works regardless of where BB5 is cloned
- Consistent with how hooks reference paths
- No dependency on environment variables being set

**Confidence:** High

**Reversibility:** Easy

---

### 2026-02-09T13:09:00Z - Orchestrator Agent Addition

**Context:** The core team has context collector, scribe, and superintelligence but lacks coordination for multi-file tasks.

**Options Considered:**
1. Add orchestration to existing agents - each agent self-coordinates
2. Create dedicated orchestrator agent - single coordination point
3. Use superintelligence for orchestration - overload existing agent

**Decision:** Create dedicated orchestrator agent (Option 2).

**Rationale:**
- Clear separation of concerns
- Orchestrator can spawn and manage other agents
- Follows pattern from claude-workflow-v2 reference
- Enables complex multi-phase task execution

**Confidence:** High

**Reversibility:** Medium - would need to redistribute orchestration logic

---

### 2026-02-09T13:10:00Z - Agent Output Standardization

**Context:** Agents document outputs in different ways, some don't specify output locations.

**Decision:** All agents must specify output locations in `runs/current/` directory.

**Standard Outputs:**
- `runs/current/THOUGHTS.md` - Thinking process
- `runs/current/DECISIONS.md` - Decision log
- `runs/current/LEARNINGS.md` - Learnings and patterns
- `runs/current/RESULTS.md` - Final outcomes
- `runs/current/CONTEXT_REPORT.md` - BB5 state (context collector)
- `runs/current/SUPERINTELLIGENCE_ANALYSIS.md` - Analysis (superintelligence)
- `runs/current/ORCHESTRATION_REPORT.md` - Coordination (orchestrator)

**Confidence:** High

**Reversibility:** Easy
