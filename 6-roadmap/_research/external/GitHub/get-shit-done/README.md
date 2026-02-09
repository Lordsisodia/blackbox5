# Get-Shit-Done (GSD) Framework Research

**Repository:** https://github.com/glittercowboy/get-shit-done
**Author:** @glittercowboy
**Type:** Spec-Driven Development Framework
**Status:** Analysis Complete
**Priority:** ⭐⭐⭐⭐⭐ (High - Adopt patterns for BB5)

---

## Mission

Extract GSD's simplicity patterns to combine with BlackBox5's power. GSD achieves remarkable effectiveness with minimal ceremony - this research identifies specific patterns to port.

---

## What is GSD?

Get-Shit-Done is a "light-weight and powerful meta-prompting, context engineering and spec-driven development system for Claude Code."

### Core Philosophy

> "The complexity is in the system, not in your workflow"

> "No enterprise roleplay bullshit. I'm not a 50-person software company with sprint ceremonies and Jira workflows. I'm just a creative person trying to build great things that work."

> "I trust the workflow. It just does a good job."

---

## Key Innovations

### 1. Context Engineering

**Problem Solved:** Context rot — quality degradation as Claude fills its context window

**Solution:**
- Fresh 200k context per agent
- Atomic plans that fit in clean windows
- Thin orchestrator that stays at 30-40% context

### 2. XML Prompt Formatting

**Why XML over Markdown:**
- Explicit element boundaries
- Machine-parseable definitions
- Built-in verification (`<verify>`, `<done>`)
- Type safety (`type="auto"` vs `type="checkpoint:*"`)

**Example:**
```xml
<task type="auto">
  <name>Create login endpoint</name>
  <files>src/app/api/auth/login/route.ts</files>
  <action>Use jose for JWT (not jsonwebtoken - CommonJS issues)</action>
  <verify>curl -X POST localhost:3000/api/auth/login returns 200</verify>
  <done>Valid credentials return cookie, invalid return 401</done>
</task>
```

### 3. Thin Orchestrator Pattern

> "The orchestrator never does heavy lifting. It spawns agents, waits, integrates results."

**Benefits:**
- Main context window stays healthy
- Parallel execution possible
- Quality doesn't degrade over long sessions

### 4. Human-in-the-Loop Checkpoints

**Types:**
- `checkpoint:human-verify` - Visual/functional checks
- `checkpoint:decision` - Implementation choices
- `checkpoint:human-action` - Manual steps

**Pattern:**
```xml
<task type="checkpoint:human-verify" gate="blocking">
  <what-built>What Claude automated</what-built>
  <how-to-verify>Exact test steps</how-to-verify>
  <resume-signal>Type "approved" or describe issues</resume-signal>
</task>
```

### 5. Session Continuity

**`.continue-here.md`** - Captures mental state for resumption:
- Current state
- Completed work
- Remaining work
- Decisions made
- Blockers
- Next action

**Commands:**
- `/gsd:pause-work` - Creates handoff file
- `/gsd:resume-work` - Restores session

---

## Command Structure

### 26 Total Commands

**Core Workflow (7):**
- `/gsd:new-project` - Full initialization
- `/gsd:discuss-phase [N]` - Pre-planning decisions
- `/gsd:plan-phase [N]` - Research + plan + verify
- `/gsd:execute-phase <N>` - Parallel execution
- `/gsd:verify-work [N]` - User acceptance
- `/gsd:complete-milestone` - Archive and tag
- `/gsd:new-milestone [name]` - Start next version

**Navigation & Status (4):**
- `/gsd:progress` - "Where am I? What's next?"
- `/gsd:help` - Command reference
- `/gsd:update` - Framework updates
- `/gsd:join-discord` - Community

**Phase Management (5):**
- `/gsd:add-phase` - Append to roadmap
- `/gsd:insert-phase [N]` - Urgent insertion
- `/gsd:remove-phase [N]` - Delete and renumber
- `/gsd:list-phase-assumptions [N]` - Preview approach
- `/gsd:plan-milestone-gaps` - Gap closure

**Session Management (2):**
- `/gsd:pause-work` - Create handoff state
- `/gsd:resume-work` - Restore session

**Utilities (6):**
- `/gsd:settings` - Configuration
- `/gsd:set-profile <profile>` - Model switching
- `/gsd:add-todo [desc]` - Capture ideas
- `/gsd:check-todos` - List pending
- `/gsd:debug [desc]` - Systematic debugging
- `/gsd:quick` - Ad-hoc task execution
- `/gsd:map-codebase` - Brownfield analysis

---

## File Structure

```
.planning/
├── PROJECT.md          # Vision, always loaded
├── REQUIREMENTS.md     # Scoped v1/v2 requirements
├── ROADMAP.md          # Where you're going
├── STATE.md            # Decisions, blockers, position
├── PLAN.md             # Atomic task with XML structure
├── SUMMARY.md          # What happened, committed to history
├── CONTEXT.md          # Phase-specific context
├── .continue-here.md   # Session handoff (temporary)
├── config.json         # Project settings
├── research/           # Ecosystem knowledge
├── todos/              # Captured ideas
└── quick/              # Quick mode tracking
```

---

## Comparison to BlackBox5

| Aspect | GSD | BlackBox5 |
|--------|-----|-----------|
| **Philosophy** | Solo developer, minimal ceremony | Multi-agent infrastructure, structured |
| **Complexity** | Hidden in system | Visible in hierarchy |
| **Commands** | 26 flat commands | Hierarchical subcommands |
| **Prompts** | XML structured | Markdown mostly |
| **Context** | Fresh 200k per agent | Shared, accumulates |
| **Orchestrator** | Thin, coordinates only | Heavier, does work |
| **Research** | 4 parallel researchers | Sequential scout |
| **Planning** | Planner + Checker loop | Single planner |
| **Execution** | Wave-based parallel | Sequential/limited parallel |
| **Verification** | Explicit verifier + debugger | Limited verification |
| **State** | STATE.md (<100 lines) | STATE.yaml (unbounded) |
| **Session** | Pause/resume with handoff | No standard mechanism |
| **Commits** | Atomic per task | Batch commits |
| **Skills** | None | 23+ specialized skills |
| **Memory** | File-based | ChromaDB, Redis, files |
| **RALF** | No equivalent | Autonomous improvement loop |

---

## What to Adopt for BlackBox5

### Immediate Wins

1. **XML Task Schema** - Structured, verifiable tasks
2. **Simplified CLI** - Flat command namespace
3. **STATE.md Digest** - Human-readable, bounded state
4. **Session Handoff** - Pause/resume with `.continue-here.md`

### Medium-term

5. **Thin Orchestrator** - RALF coordinates only
6. **Parallel Research** - 4 specialized researchers
7. **Wave Execution** - Dependency-based parallelism
8. **Fresh Context** - 200k per agent

### Long-term

9. **Planner + Checker Loop** - Iterative planning
10. **Verifier + Debugger Loop** - Automated verification
11. **Atomic Commits** - One commit per task
12. **Checkpoint System** - Human-in-the-loop gates

---

## Anti-Patterns to Avoid

GSD explicitly rejects:
- Sprint ceremonies
- Story points
- Stakeholder syncs
- Retrospectives
- Jira workflows
- Approval gates
- Enterprise roleplay

**BlackBox5 should:**
- Keep automation, remove ceremony
- Default to action, not approval
- Trust the workflow
- Hide complexity behind simple commands

---

## Directory Structure

```
get-shit-done/
├── README.md              # This file
├── data/
│   └── repos/             # Cloned GSD repository
│       └── get-shit-done/ # (to be cloned)
├── extracted/             # Deep analysis
│   ├── commands.md        # Command analysis
│   ├── xml-patterns.md    # XML schema analysis
│   ├── state-management.md # STATE.md analysis
│   └── orchestration.md   # Agent orchestration analysis
└── synthesized/           # BB5 integration plan
    └── adoption-roadmap.md # Implementation plan
```

---

## References

- **Repository:** https://github.com/glittercowboy/get-shit-done
- **Framework Research:** `/Users/shaansisodia/.blackbox5/6-roadmap/frameworks/`
- **BB5 Integration:** See `synthesized/adoption-roadmap.md`
