# snarktank/ralph Analysis

## Overview

Ralph is a lightweight, bash-based autonomous AI agent loop designed to repeatedly run AI coding tools (Amp or Claude Code) until all PRD items are complete. It implements the "Ralph pattern" popularized by Geoffrey Huntley, emphasizing **fresh context per iteration** with memory persistence through git history, `progress.txt`, and `prd.json`.

The framework is designed for simplicity and portability - the core loop is a single bash script (~114 lines) with supporting skill definitions and prompt templates.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        ralph.sh                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  FOR i = 1 to MAX_ITERATIONS                        │   │
│  │    ┌──────────────────────────────────────────┐    │   │
│  │    │  Spawn fresh AI instance (Amp/Claude)    │    │   │
│  │    │  Feed prompt.md or CLAUDE.md            │    │   │
│  │    │  Capture output                         │    │   │
│  │    └──────────────────────────────────────────┘    │   │
│  │    IF output contains <promise>COMPLETE: EXIT      │   │
│  │  END FOR                                           │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
   ┌──────────┐        ┌──────────┐          ┌──────────┐
   │prd.json  │        │progress. │          │git repo  │
   │(tasks)   │        │txt       │          │(commits) │
   └──────────┘        └──────────┘          └──────────┘
```

### Key Architectural Decisions

1. **Single-threaded sequential execution** - No parallel agent execution
2. **Fresh context per iteration** - Each AI spawn is stateless
3. **File-based state management** - JSON + text files for persistence
4. **Git as memory** - Commit history serves as long-term memory
5. **External tool dependency** - Relies on Amp CLI or Claude Code being installed

## Core Components

### 1. ralph.sh (Main Loop)
**Location:** `/ralph.sh`
**Lines:** 114

The bash script that orchestrates the autonomous loop:
- Parses arguments (`--tool amp|claude`, `max_iterations`)
- Archives previous runs when branch changes
- Iterates up to MAX_ITERATIONS (default: 10)
- Spawns AI tool with appropriate prompt file
- Checks for `<promise>COMPLETE</promise>` completion signal
- Handles errors gracefully (continues on failure)

Key code pattern:
```bash
for i in $(seq 1 $MAX_ITERATIONS); do
  if [[ "$TOOL" == "amp" ]]; then
    OUTPUT=$(cat "$SCRIPT_DIR/prompt.md" | amp --dangerously-allow-all 2>&1 | tee /dev/stderr) || true
  else
    OUTPUT=$(claude --dangerously-skip-permissions --print < "$SCRIPT_DIR/CLAUDE.md" 2>&1 | tee /dev/stderr) || true
  fi

  if echo "$OUTPUT" | grep -q "<promise>COMPLETE</promise>"; then
    exit 0
  fi
done
```

### 2. CLAUDE.md / prompt.md (Agent Instructions)
**Location:** `/CLAUDE.md`, `/prompt.md`

The prompt template given to each AI instance. Contains:
- Task instructions (read PRD, pick story, implement, commit)
- Progress report format (append-only to progress.txt)
- Codebase patterns consolidation rules
- AGENTS.md update guidelines
- Quality requirements (typecheck, tests)
- Browser testing requirements for UI stories
- Stop condition (`<promise>COMPLETE</promise>`)

### 3. prd.json (Task State)
**Location:** `/prd.json` (user-created)
**Example:** `/prd.json.example`

JSON structure defining:
- `project`: Project name
- `branchName`: Git branch for this feature
- `description`: Feature description
- `userStories`: Array of stories with:
  - `id`: US-001, US-002, etc.
  - `title`: Short description
  - `description`: Full user story format
  - `acceptanceCriteria`: Verifiable checklist
  - `priority`: Execution order
  - `passes`: Boolean completion status
  - `notes`: Implementation notes

### 4. progress.txt (Memory/Learnings)
**Location:** `/progress.txt` (auto-generated)

Append-only log of:
- Codebase Patterns section (at top)
- Per-iteration learnings
- Files changed
- Gotchas discovered

### 5. Skills (PRD Generation)
**Location:** `/skills/prd/SKILL.md`, `/skills/ralph/SKILL.md`

Claude Code skill definitions for:
- **prd skill**: Generate Product Requirements Documents from feature descriptions
- **ralph skill**: Convert PRD markdown to prd.json format

Skills include:
- Clarifying question patterns
- Story sizing guidelines (must fit in one iteration)
- Dependency ordering rules
- Acceptance criteria best practices

### 6. Flowchart Visualization
**Location:** `/flowchart/`

React + React Flow interactive visualization of the Ralph workflow. Deployed to GitHub Pages at https://snarktank.github.io/ralph/

### 7. Claude Code Plugin
**Location:** `/.claude-plugin/`

Plugin manifest for Claude Code marketplace integration, enabling:
```bash
/plugin marketplace add snarktank/ralph
/plugin install ralph-skills@ralph-marketplace
```

## Autonomous Loop Mechanism

### Loop Flow

```
┌─────────────┐
│   START     │
└──────┬──────┘
       ▼
┌─────────────┐     ┌──────────────────────────────────────────┐
│ Read prd.   │────▶│ Find highest priority story with         │
│ json        │     │ passes: false                            │
└─────────────┘     └──────────────────┬───────────────────────┘
                                       │
       ┌───────────────────────────────┘
       ▼
┌─────────────┐     ┌──────────────────────────────────────────┐
│ Implement   │────▶│ - Write code                             │
│ story       │     │ - Run typecheck/lint/tests               │
└─────────────┘     │ - Update AGENTS.md with patterns         │
                    └──────────────────┬───────────────────────┘
                                       │
       ┌───────────────────────────────┘
       ▼
┌─────────────┐     ┌──────────────────────────────────────────┐
│ Commit if   │────▶│ git commit -m "feat: [ID] - [Title]"     │
│ checks pass │     └──────────────────────────────────────────┘
└─────────────┘
       │
       ▼
┌─────────────┐     ┌──────────────────────────────────────────┐
│ Update      │────▶│ Set passes: true in prd.json             │
│ prd.json    │     └──────────────────────────────────────────┘
└─────────────┘
       │
       ▼
┌─────────────┐     ┌──────────────────────────────────────────┐
│ Append to   │────▶│ Add learnings to progress.txt            │
│ progress.txt│     └──────────────────────────────────────────┘
└─────────────┘
       │
       ▼
┌─────────────┐
│ ALL stories │──NO──▶ Spawn new AI instance (fresh context)
│ complete?   │         (loop continues)
└─────────────┘
       │YES
       ▼
┌─────────────┐
│ Output      │
│ <promise>   │
│ COMPLETE    │
└─────────────┘
```

### Key Loop Characteristics

1. **Stateless Iterations**: Each AI spawn has NO memory of previous iterations
2. **Deterministic Story Selection**: Always picks highest priority incomplete story
3. **Mandatory Quality Gates**: Must pass typecheck/tests before commit
4. **Progressive Learning**: progress.txt accumulates patterns for future iterations
5. **Git-based Recovery**: Each commit is a checkpoint

## Agent Orchestration

### Single-Agent Pattern

Ralph uses a **single-agent sequential pattern**, NOT multi-agent orchestration:
- One AI instance runs at a time
- No agent specialization (same prompt for all iterations)
- No agent communication (stateless)
- No task delegation

### Agent Lifecycle

```
Spawn (fresh context)
    │
    ▼
Read prd.json + progress.txt
    │
    ▼
Execute ONE user story
    │
    ▼
Commit + Update state files
    │
    ▼
Terminate (context discarded)
```

### Memory Model

| Memory Type | Location | Persistence | Use Case |
|-------------|----------|-------------|----------|
| Short-term | AI context window | Single iteration | Current story implementation |
| Medium-term | progress.txt | Across iterations | Learnings, patterns, gotchas |
| Long-term | Git commits | Permanent | Code history, rollback points |
| State | prd.json | Across iterations | Task completion tracking |

## Task Management

### Task Structure (prd.json)

```json
{
  "userStories": [
    {
      "id": "US-001",
      "title": "Add priority field to database",
      "description": "As a developer...",
      "acceptanceCriteria": [
        "Add priority column...",
        "Typecheck passes"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```

### Task Selection Algorithm

1. Filter: `passes: false`
2. Sort: By `priority` ascending
3. Select: First item (highest priority incomplete)

### Task Sizing Rules

**Right-sized (one iteration):**
- Add database column + migration
- Add UI component to existing page
- Update server action with new logic
- Add filter dropdown

**Too big (must split):**
- "Build entire dashboard"
- "Add authentication"
- "Refactor the API"

### Dependency Management

Stories must be ordered by dependency in prd.json:
1. Schema/database changes first
2. Server actions/backend logic second
3. UI components third
4. Dashboard/summary views last

## Integration with Claude Code

### Direct Integration

```bash
# Run with Claude Code
./ralph.sh --tool claude [max_iterations]
```

The script invokes Claude Code via stdin redirection:
```bash
OUTPUT=$(claude --dangerously-skip-permissions --print < "$SCRIPT_DIR/CLAUDE.md" 2>&1 | tee /dev/stderr) || true
```

### Flags Used

- `--dangerously-skip-permissions`: Allows autonomous operation without user confirmation
- `--print`: Outputs to stdout for capture

### Skill Integration

Skills can be installed globally:
```bash
cp -r skills/prd ~/.claude/skills/
cp -r skills/ralph ~/.claude/skills/
```

Or via marketplace:
```bash
/plugin marketplace add snarktank/ralph
```

### AGENTS.md Pattern

Ralph introduces the AGENTS.md convention for preserving learnings:
- Located in directories with implementation
- Updated with patterns discovered during implementation
- Automatically read by Claude Code on future iterations
- Serves as documentation for human developers too

## Strengths

1. **Simplicity**: Single bash script, minimal dependencies (jq + AI tool)
2. **Fresh Context**: Each iteration starts clean, avoiding context pollution
3. **Git-Native**: Leverages git for history, branching, and rollback
4. **Tool Agnostic**: Works with both Amp and Claude Code
5. **Deterministic**: Clear task selection and completion criteria
6. **Self-Documenting**: progress.txt becomes project documentation
7. **Skill Ecosystem**: PRD generation and conversion skills
8. **Visualization**: Interactive flowchart for understanding the pattern
9. **Marketplace Ready**: Packaged as Claude Code plugin
10. **Battle-Tested**: Based on Geoffrey Huntley's proven pattern

## Weaknesses/Limitations

1. **No Parallel Execution**: Single-threaded, slow for large projects
2. **No Agent Specialization**: Same prompt for all tasks
3. **No Dynamic Planning**: Static prd.json, no runtime adaptation
4. **No Error Recovery**: Failed iterations don't trigger special handling
5. **Manual PRD Creation**: Requires human to create initial PRD (though skills help)
6. **No Inter-Agent Communication**: Stateless design prevents collaboration
7. **Limited Observability**: No dashboard or real-time monitoring
8. **File-Based State**: No database for complex state management
9. **No Retry Logic**: Failed stories must be manually reset
10. **Assumes Greenfield**: No explicit handling of merge conflicts or existing branches
11. **Context Window Limits**: Stories must fit in single iteration
12. **No Priority Reordering**: Static priorities, no runtime adjustment

## Integration Potential for BB5

### High-Value Elements to Adopt

1. **Fresh Context Pattern**: BB5 RALF could benefit from periodic context resets
2. **AGENTS.md Convention**: Excellent for preserving learnings across sessions
3. **Progress.txt Logging**: Structured append-only logging is valuable
4. **Skill Packaging**: Claude Code marketplace integration approach
5. **Story Sizing Guidelines**: Clear rules for task granularity
6. **Flowchart Visualization**: Good for documentation and onboarding

### Integration Approaches

#### Option 1: Direct Fork/Extension
- Fork snarktank/ralph as base
- Add BB5-specific features (multi-agent, dynamic planning)
- Keep simplicity while adding capabilities

#### Option 2: Component Extraction
- Extract skills system for PRD generation
- Adopt AGENTS.md pattern for memory
- Use ralph.sh as fallback/simple mode

#### Option 3: Reference Implementation
- Study patterns but build BB5-specific solution
- Use as benchmark for simplicity vs capability tradeoffs

### Specific BB5 Enhancements

| Ralph Feature | BB5 Enhancement |
|---------------|-----------------|
| Single-agent | Multi-agent teams with specialization |
| Static prd.json | Dynamic task queue with runtime prioritization |
| File-based state | Database + event stream for observability |
| Sequential execution | Parallel execution with dependency resolution |
| Bash script | Python/TypeScript with proper error handling |
| No monitoring | Real-time dashboard and alerting |
| Manual PRD | AI-assisted PRD generation and refinement |

## Recommendation

**Priority: HIGH - Study and Adopt Patterns**

### Should BB5 Integrate?

**Yes, but as a reference and fallback, not as the primary architecture.**

### Rationale

1. **Proven Pattern**: snarktank/ralph demonstrates a working minimal viable autonomous loop
2. **Simplicity Wins**: The bash-based approach shows how little infrastructure is actually required
3. **Fresh Context**: The stateless iteration pattern is valuable for preventing context pollution
4. **AGENTS.md**: This convention should be adopted by BB5 immediately

### Integration Strategy

1. **Immediate**: Adopt AGENTS.md and progress.txt patterns in BB5
2. **Short-term**: Use ralph.sh as a fallback/simple mode for BB5
3. **Medium-term**: Extract PRD skills for BB5's planning module
4. **Long-term**: Build BB5 RALF as superset - keep ralph compatibility mode

### Risk Assessment

| Risk | Mitigation |
|------|------------|
| Over-engineering BB5 | Use ralph as simplicity benchmark |
| Reinventing patterns | Adopt proven patterns from ralph |
| Feature creep | Maintain ralph-compatible minimal mode |

### Final Verdict

snarktank/ralph is an excellent **reference implementation** of a minimal autonomous agent loop. BB5 should:

1. **Study it deeply** - Understand why each design decision was made
2. **Adopt patterns** - AGENTS.md, progress.txt, story sizing
3. **Extend carefully** - Add capabilities (multi-agent, monitoring) without losing simplicity
4. **Maintain compatibility** - Keep a "ralph mode" for simple use cases

The framework demonstrates that autonomous coding agents don't require complex infrastructure - a bash loop and good prompts can go a long way. BB5 should aim to preserve this simplicity while adding enterprise-grade features.

---

## Files Analyzed

- `/ralph.sh` - Main orchestration loop
- `/CLAUDE.md` - Claude Code agent instructions
- `/prompt.md` - Amp agent instructions
- `/AGENTS.md` - Project documentation
- `/README.md` - User documentation
- `/prd.json.example` - Task format example
- `/skills/prd/SKILL.md` - PRD generation skill
- `/skills/ralph/SKILL.md` - PRD conversion skill
- `/.claude-plugin/plugin.json` - Plugin manifest
- `/.claude-plugin/marketplace.json` - Marketplace definition
- `/.github/workflows/deploy.yml` - CI/CD for flowchart
- `/flowchart/src/App.tsx` - Interactive visualization
