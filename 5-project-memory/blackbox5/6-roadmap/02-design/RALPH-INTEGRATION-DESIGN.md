# Ralph Integration Design

**Status:** Design Phase  
**Created:** 2026-01-30  
**Purpose:** Define how Ralph fits into Blackbox5's existing project memory infrastructure

---

## Current State Analysis

### Blackbox5 Project Memory Structure (Existing)

```
5-project-memory/
├── _template/                    # Framework templates
│   └── blackbox/
│       └── _template/
│           ├── agents/_template/ # Agent templates
│           ├── context.md        # Project context
│           └── ...
│
└── {project-id}/                 # Project-specific memory
    ├── decisions/                # Why we're doing it this way
    ├── knowledge/                # How it works + learnings
    ├── operations/               # How the AI system runs
    │   └── agents/
    │       ├── active/           # Currently running agents
    │       └── history/          # Past agent sessions
    │           └── sessions/
    │               └── {agent-name}/
    ├── plans/                    # What we're building
    │   ├── active/               # Active epics
    │   ├── prds/                 # Product requirements
    │   │   ├── active/
    │   │   ├── backlog/
    │   │   └── completed/
    │   └── features/             # Feature management
    ├── project/                  # What is this project
    │   └── _meta/
    │       ├── context.yaml      # Project context
    │       └── ...
    └── tasks/                    # What we're working on
        ├── active/               # Active task files
        ├── working/              # Working task folders
        └── completed/            # Completed tasks
```

### Key Insight: Agent Memory Location

Per the AI Agent Guide, agent sessions are stored in:
```
{project-memory}/{project-id}/operations/agents/history/sessions/{agent-name}/
```

This means Ralph's session data should live in the **project-specific memory**, not the framework/engine folder.

---

## Ralph Integration Strategy

### Core Principle: Ralph is a Project-Level Agent

Ralph operates on **projects**, not on Blackbox5 itself. Therefore:

1. **Ralph's runtime** lives in Blackbox5 engine (`2-engine/07-operations/runtime/ralph/`)
2. **Ralph's sessions** live in project memory (`5-project-memory/{project}/operations/agents/history/sessions/ralph/`)
3. **Ralph's prompts** are project-specific, not global

### Where Things Live

| Component | Location | Rationale |
|-----------|----------|-----------|
| Ralph Runtime | `2-engine/07-operations/runtime/ralph/` | Shared infrastructure |
| Ralph Binary | `2-engine/07-operations/commands/run/ralph-cli.sh` | Global command |
| Ralph Prompt (template) | `5-project-memory/_template/blackbox/_template/agents/ralph/` | Project template |
| Ralph Prompt (project) | `{project}/operations/agents/ralph/prompt.md` | Project-specific |
| Ralph Sessions | `{project}/operations/agents/history/sessions/ralph/` | Per-project history |
| Ralph Progress | `{project}/operations/agents/ralph/progress.md` | Project progress |
| Ralph PRD | `{project}/plans/prds/active/ralph-{feature}.md` | Standard PRD location |

---

## Ralph Prompt Architecture

### The Problem with the Current Approach

The current `PROMPT.md` I created is **too long and complex**. Research shows:

> "The Curse of Instructions: Model adherence drops with 10+ bullet points."

The optimal Ralph prompt is **minimal but complete**.

### Universal Ralph Prompt Structure (Distilled)

Based on all sources (Huntley, snarktank, iannuttall, Ralph TUI):

```markdown
# Ralph Loop Prompt

## Context
@AGENT.md @progress.txt @plan.md

## Your Task
1. Read plan.md — find highest priority unchecked item
2. Read progress.txt — understand what's been learned
3. Implement that ONE item completely
4. Run: [quality gates]
5. If passing: commit, mark complete, log learnings
6. If failing: debug, fix, retry (max 3x)

## Rules
- ONE task per loop. Never batch.
- Use subagents for all searches
- Update progress.txt after every iteration
- Never modify multiple unrelated files

## Exit
If all items complete: output <promise>COMPLETE</promise>
```

### Blackbox5-Specific Additions

For Blackbox5 integration, we need minimal additions:

```markdown
## Blackbox5 Context
- Read: {project}/project/_meta/context.yaml
- Read: {project}/STATE.yaml
- Update: {project}/operations/agents/ralph/progress.md
- PRD Location: {project}/plans/prds/active/
```

---

## Ralph Session Data Flow

### Initialization

```bash
# User starts Ralph on a project
ralph-cli.sh start --project siso-internal --plan plans/prds/active/feature-x.md

# Ralph runtime:
1. Checks project exists in 5-project-memory/
2. Creates operations/agents/ralph/ structure if missing
3. Loads project context
4. Starts the loop
```

### Per-Loop Execution

```
┌─────────────────────────────────────────────────────────────┐
│ RALPH LOOP ITERATION                                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ 1. READ CONTEXT                                             │
│    - {project}/project/_meta/context.yaml                   │
│    - {project}/STATE.yaml                                   │
│    - {project}/operations/agents/ralph/progress.md          │
│    - {project}/plans/prds/active/{plan}.md                  │
│                                                             │
│ 2. SELECT TASK                                              │
│    - Find highest priority unchecked item in plan           │
│    - Verify dependencies met                                │
│                                                             │
│ 3. IMPLEMENT                                                │
│    - Use subagents for exploration                          │
│    - Write code following project patterns                  │
│    - Run quality gates                                      │
│                                                             │
│ 4. VALIDATE                                                 │
│    - Tests pass                                             │
│    - No regressions                                         │
│    - Documentation updated                                  │
│                                                             │
│ 5. DOCUMENT                                                 │
│    - Update progress.md                                     │
│    - Commit with descriptive message                        │
│    - Log learnings                                          │
│                                                             │
│ 6. EXIT                                                     │
│    - Output status                                          │
│    - If all complete: <promise>COMPLETE</promise>           │
│    - Bash loop restarts Ralph                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Session Storage

```
{project}/operations/agents/history/sessions/ralph/
├── sessions.json              # All sessions index
├── session-{id}/              # Individual session
│   ├── session.json           # Session metadata
│   ├── progress.md            # Progress log
│   ├── decisions.json         # Decisions made
│   └── artifacts/             # Generated files
```

---

## Project-Specific Ralph Configuration

### File: `{project}/operations/agents/ralph/config.yaml`

```yaml
ralph_config:
  version: "2.0.0"
  
  # Context files to read each loop
  context_files:
    - "project/_meta/context.yaml"
    - "STATE.yaml"
    - "operations/agents/ralph/progress.md"
  
  # Plan source
  plan_source: "plans/prds/active/"
  
  # Quality gates
  quality_gates:
    - "npm run typecheck"
    - "npm run test"
    - "npm run lint"
  
  # Sub-agent prompts
  sub_agents:
    validation: "operations/agents/ralph/prompts/validation.md"
    test: "operations/agents/ralph/prompts/test.md"
    research: "operations/agents/ralph/prompts/research.md"
  
  # Exit conditions
  exit_conditions:
    - all_tasks_complete
    - error_threshold_exceeded
    - human_intervention_required
```

### File: `{project}/operations/agents/ralph/prompt.md`

```markdown
# Ralph Loop Prompt — {Project Name}

## Context
@project/_meta/context.yaml
@STATE.yaml
@operations/agents/ralph/progress.md
@plans/prds/active/{current-plan}.md

## Your Task
1. Read the PRD — find highest priority unchecked item
2. Read progress.md — understand what's been learned
3. Implement that ONE item completely
4. Run: npm run typecheck && npm test && npm run lint
5. If passing: commit, mark complete, log learnings to progress.md
6. If failing: debug, fix, retry (max 3x)

## Project-Specific Rules
- Follow the coding patterns in src/
- Use TypeScript for all new files
- Tests must have >80% coverage
- Update AGENT.md if you learn something new

## Exit
If all items complete: output <promise>COMPLETE</promise>
```

### File: `{project}/operations/agents/ralph/progress.md`

```markdown
# Ralph Progress — {Project Name}

**Last Updated:** {timestamp}
**Current Plan:** {plan-name}
**Status:** {active/complete/blocked}

## Completed Tasks

### {timestamp} — {task-name}
- **Status:** ✅ Complete
- **Commit:** {hash}
- **Learnings:** {what was learned}

## Current Task

**Task:** {task-name}
**Started:** {timestamp}
**Progress:** {X%}

## Blockers

- {None / blocker description}

## Next Up

1. {Next task}
```

---

## Integration with Blackbox5 Systems

### First Principles Engine

Ralph should use FP decision-making for:
- Task selection (when multiple high-priority tasks)
- Implementation approach (when multiple options)
- Error recovery (when stuck)

**Integration:**
```yaml
# In config.yaml
first_principles:
  enabled: true
  decision_log: "decisions/ralph/"
  principles:
    - PR-0001  # Cost Decomposition
    - PR-0002  # ADI Cycle
```

### BMAD Agent Spawning

Ralph can spawn BMAD agents for specialized tasks:

```yaml
# In config.yaml
bmad_integration:
  enabled: true
  agents:
    analyst: "2-engine/02-agents/implementations/03-research/3-research/deep-research/"
    architect: "2-engine/02-agents/implementations/02-agents/modules/architect/"
    dev: "2-engine/02-agents/implementations/02-agents/modules/dev/"
```

### AgentMemory Integration

Ralph sessions are automatically tracked in AgentMemory:

```yaml
# In config.yaml
memory:
  agent_memory: true
  project_memory: true
  semantic_index: true
```

---

## Ralph CLI Commands

```bash
# Start Ralph on a project
ralph-cli.sh start --project siso-internal --plan feature-x

# Check status
ralph-cli.sh status --project siso-internal

# Pause/resume
ralph-cli.sh pause --project siso-internal
ralph-cli.sh resume --project siso-internal

# Stop
ralph-cli.sh stop --project siso-internal

# View logs
ralph-cli.sh logs --project siso-internal --tail 100

# List sessions
ralph-cli.sh sessions --project siso-internal
```

---

## Implementation Plan

### Phase 1: Core Infrastructure

1. **Create Ralph Runtime** (`2-engine/07-operations/runtime/ralph/`)
   - RalphRuntime class
   - Session management
   - Loop orchestration

2. **Create Ralph CLI** (`2-engine/07-operations/commands/run/ralph-cli.sh`)
   - Command parsing
   - Project selection
   - Loop management

### Phase 2: Project Memory Integration

1. **Create Project Templates** (`5-project-memory/_template/blackbox/_template/agents/ralph/`)
   - `prompt.md` template
   - `config.yaml` template
   - `progress.md` template

2. **Create Ralph Session Structure**
   - `operations/agents/history/sessions/ralph/` structure
   - Session indexing
   - Progress tracking

### Phase 3: Blackbox5 Integration

1. **First Principles Integration**
   - Decision logging
   - ADI cycle support

2. **BMAD Integration**
   - Agent spawning
   - Context passing

3. **Memory Integration**
   - AgentMemory sync
   - Semantic indexing

---

## Key Design Decisions

### 1. Project-Centric, Not Global

Ralph is configured per-project, not globally. Each project has its own:
- Prompt
- Config
- Progress tracking
- Session history

### 2. Minimal Prompts

The prompt should be <50 lines. Key principles:
- ONE task per loop
- Use subagents for searches
- Update progress after each iteration
- Exit with <promise>COMPLETE</promise>

### 3. Leverage Existing Infrastructure

Don't reinvent:
- Use existing project memory structure
- Use existing BMAD agents
- Use existing First Principles engine
- Use existing AgentMemory

### 4. Configurable Quality Gates

Each project defines its own quality gates:
```yaml
quality_gates:
  - "npm run typecheck"
  - "npm run test"
  - "npm run lint"
```

---

## Open Questions

1. **How does Ralph discover which plan to work on?**
   - Option A: User specifies `--plan`
   - Option B: Ralph reads `STATE.yaml` for active plan
   - Option C: Ralph picks highest priority from `plans/prds/active/`

2. **How does Ralph handle multiple PRDs?**
   - Option A: Work on one PRD at a time
   - Option B: Merge PRDs into unified task list
   - Option C: Priority across all PRDs

3. **How does Ralph update PRD progress?**
   - Option A: Update checkboxes in PRD file
   - Option B: Update separate progress.md
   - Option C: Both

4. **Should Ralph spawn sub-agents as separate processes or inline?**
   - Option A: Separate processes (clean context)
   - Option B: Inline (faster, shared context)
   - Option C: Configurable

---

## Next Steps

1. **Finalize open questions** (this document)
2. **Create Ralph Runtime** (Phase 1)
3. **Create project templates** (Phase 2)
4. **Test with real project** (siso-internal or blackbox5)
5. **Iterate based on learnings**

---

## References

- **Ralph Technique:** Jeffrey Huntley (July 2025)
- **snarktank/ralph:** https://github.com/snarktank/ralph
- **iannuttall/ralph:** https://github.com/iannuttall/ralph
- **Ralph TUI:** https://ralph-tui.com/
- **Blackbox5 AI Agent Guide:** `5-project-memory/AI-AGENT-GUIDE.md`
