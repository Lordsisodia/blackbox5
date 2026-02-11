# mikeyobrien/ralph-orchestrator Analysis

## Overview

Ralph Orchestrator is a sophisticated **hat-based agent orchestration framework** written in Rust that implements the "Ralph Wiggum technique" — autonomous task completion through continuous iteration. It coordinates multiple AI agents (called "hats") through an event-driven pub/sub system, with each hat specializing in specific tasks like planning, building, reviewing, or researching.

The framework is production-ready with:
- Multi-backend support (Claude Code, Kiro, Gemini CLI, Codex, Amp, Copilot CLI, OpenCode)
- Web dashboard for monitoring and management
- 31 built-in presets for different workflows (TDD, spec-driven, debugging)
- Human-in-the-loop via Telegram integration (RObot)
- Parallel loop execution via git worktrees
- Comprehensive diagnostics and observability

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RALPH ORCHESTRATOR                                   │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                      👑 HATLESS RALPH (Constant)                       │ │
│  │  • Always present, cannot be configured away                           │ │
│  │  • Owns scratchpad (.ralph/agent/scratchpad.md)                       │ │
│  │  • Owns completion detection (LOOP_COMPLETE)                          │ │
│  │  • Universal fallback for orphaned events                             │ │
│  │  • Delegates to hats or executes directly                             │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                         │
│                    ┌───────────────┼───────────────┐                         │
│                    │ delegates     │ delegates     │ delegates               │
│                    ▼               ▼               ▼                         │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐             │
│  │   🔨 Builder     │ │   👀 Reviewer    │ │   🔍 Researcher  │             │
│  │   backend:claude │ │   backend:gemini │ │   backend:kiro   │             │
│  └────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘             │
│           │                    │                    │                        │
│           └────────event───────┴────────event───────┘                        │
│                    (hat-to-hat direct, bypasses Ralph)                       │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                     📁 DISK STATE (Git-based)                          │ │
│  │  • .ralph/agent/memories.md    — Persistent learning                  │ │
│  │  • .ralph/agent/tasks.jsonl    — Runtime work tracking                │ │
│  │  • .ralph/events.jsonl         — Event log (JSONL format)             │ │
│  │  • .ralph/loop.lock            — PID + prompt of primary loop         │ │
│  │  • .ralph/loops.json           — Registry of all tracked loops        │ │
│  │  • .ralph/merge-queue.jsonl    — Event-sourced merge queue            │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Core Philosophy

The framework follows **"The Ralph Tenets":**

1. **Fresh Context Is Reliability** — Each iteration clears context. Re-read specs, plan, code every cycle.
2. **Backpressure Over Prescription** — Don't prescribe how; create gates that reject bad work (tests, typechecks, builds, lints).
3. **The Plan Is Disposable** — Regeneration costs one planning loop. Cheap. Never fight to save a plan.
4. **Disk Is State, Git Is Memory** — Memories and Tasks are the handoff mechanisms. No sophisticated coordination needed.
5. **Steer With Signals, Not Scripts** — The codebase is the instruction manual.
6. **Let Ralph Ralph** — Sit *on* the loop, not *in* it. Tune like a guitar, don't conduct like an orchestra.

---

## Core Components

### 1. **HatlessRalph** (`crates/ralph-core/src/hatless_ralph.rs`)

The constant coordinator that cannot be replaced or configured away:
- Builds prompts for Ralph's own execution
- Determines if Ralph should handle an event (when no hat subscribes)
- Manages hat topology for multi-hat mode prompt generation
- Owns the completion promise detection

```rust
pub struct HatlessRalph {
    completion_promise: String,
    core: CoreConfig,
    hat_topology: Option<HatTopology>,
    starting_event: Option<String>,
    memories_enabled: bool,
    objective: Option<String>,
    skill_index: String,
    robot_guidance: Vec<String>,
}
```

### 2. **EventLoop** (`crates/ralph-core/src/event_loop/mod.rs`)

The main orchestration engine:
- Runs iterations until completion promise detected or termination condition met
- Routes events to appropriate hats based on subscriptions
- Falls back to Ralph for orphaned events
- Handles safeguards (max iterations, max runtime, cost limits, stall detection)

Key termination reasons:
```rust
pub enum TerminationReason {
    CompletionPromise,      // Normal completion
    MaxIterations,          // Hit iteration limit
    MaxRuntime,             // Exceeded time limit
    MaxCost,                // Exceeded cost budget
    ConsecutiveFailures,    // Too many failures in a row
    LoopThrashing,          // Repeated blocked events
    ValidationFailure,      // Too many malformed JSONL lines
    Stopped,                // Manual stop
    Interrupted,            // SIGINT/SIGTERM
    RestartRequested,       // Via Telegram /restart
}
```

### 3. **HatRegistry** (`crates/ralph-core/src/hat_registry.rs`)

Manages agent personas (hats):
- Creates hats from configuration (NO default hats — empty config = empty registry)
- Prefix-indexed O(1) subscriber lookup for performance
- Supports glob patterns in triggers (e.g., `task.*`, `build.*`)

```rust
pub struct HatRegistry {
    hats: HashMap<HatId, Hat>,
    configs: HashMap<HatId, HatConfig>,
    prefix_index: HashSet<String>,  // O(1) early-exit optimization
}
```

### 4. **Task System** (`crates/ralph-core/src/task.rs`, `task_store.rs`)

Lightweight task tracking inspired by Steve Yegge's Beads:
- JSONL persistence
- Dependency tracking (`blocked_by`)
- Priority levels (1-5)
- Loop ID ownership for parallel execution

```rust
pub struct Task {
    pub id: String,              // task-{timestamp}-{hex}
    pub title: String,
    pub description: Option<String>,
    pub status: TaskStatus,      // Open, InProgress, Closed, Failed
    pub priority: u8,            // 1-5
    pub blocked_by: Vec<String>, // Task IDs that must complete first
    pub loop_id: Option<String>, // For parallel loop filtering
    pub created: String,
    pub closed: Option<String>,
}
```

### 5. **Memory System** (`crates/ralph-core/src/memory.rs`, `memory_store.rs`)

Persistent learning across sessions:
- Markdown-based storage (human-readable)
- Four memory types: Pattern, Decision, Fix, Context
- Token budget management for prompt injection
- Tag-based categorization and search

```rust
pub struct Memory {
    pub id: String,              // mem-{timestamp}-{hex}
    pub memory_type: MemoryType, // Pattern, Decision, Fix, Context
    pub content: String,
    pub tags: Vec<String>,
    pub created: String,
}
```

### 6. **Event System** (`crates/ralph-core/src/event_reader.rs`, `event_parser.rs`)

JSONL-based event handling (replaced fragile XML parsing):
```jsonl
{"topic": "build.task", "payload": "Implement auth", "ts": "2024-01-15T10:00:00Z"}
{"topic": "build.done", "payload": "Tests pass", "ts": "2024-01-15T10:30:00Z"}
```

- Events written to `.ralph/events.jsonl`
- Incremental reading with position tracking
- Default publishes fallback when hats forget to emit events

### 7. **Web Dashboard** (`backend/ralph-web-server/`, `frontend/ralph-web/`)

Full-stack monitoring interface:
- **Backend**: Fastify + tRPC + SQLite
  - `Dispatcher`: Task execution engine with polling loop
  - `LoopsManager`: Parallel loop management and merge queue processing
  - `TaskQueueService`: Persistent task queue with state machine
- **Frontend**: React + Vite + TailwindCSS
  - Real-time log streaming via WebSocket
  - Loop monitoring and control
  - Task management UI

---

## Autonomous Loop Mechanism

### Iteration Lifecycle

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ITERATION LIFECYCLE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. READ STATE                                                               │
│     ├─► Read .ralph/agent/scratchpad.md (if memories disabled)            │
│     ├─► Read .ralph/agent/tasks.jsonl (task queue)                        │
│     ├─► Read .ralph/events.jsonl (pending events)                         │
│     └─► Determine which hat/Ralph should run                                │
│                                                                              │
│  2. SELECT EXECUTOR                                                          │
│     ├─► If event has subscriber → Select that hat's backend                 │
│     └─► If no subscriber → Select Ralph's backend (cli.backend)             │
│                                                                              │
│  3. BUILD PROMPT                                                             │
│     ├─► If Ralph: build_hatless_ralph() + hat topology (if hats exist)      │
│     └─► If hat: build_hat_prompt() with hat instructions                    │
│                                                                              │
│  4. EXECUTE                                                                  │
│     ├─► Invoke backend (claude/kiro/gemini/codex/amp/custom)                │
│     └─► Agent reads state, does work, writes events                         │
│                                                                              │
│  5. PROCESS RESULTS                                                          │
│     ├─► Read new events from .ralph/events.jsonl                            │
│     ├─► If no events + hat has default_publishes → Use default              │
│     ├─► If no events + no default → Event falls to Ralph                    │
│     └─► Route next event or check completion                                  │
│                                                                              │
│  6. CHECK COMPLETION                                                         │
│     ├─► Only Ralph can output LOOP_COMPLETE                                 │
│     ├─► All tasks terminal? → Complete                                      │
│     └─► Otherwise → Next iteration                                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Safeguards

| Safeguard | Default | Exit Code |
|-----------|---------|-----------|
| Max Iterations | 50-100 | 2 |
| Max Runtime | 3600s (1 hour) | 2 |
| Max Cost | Configurable | 2 |
| Consecutive Failures | 3 | 1 |
| Loop Thrashing | 3 consecutive blocked | 1 |
| Validation Failure | 5 malformed JSONL lines | 1 |

---

## Agent Orchestration (Focus Area)

### Hat-Based Architecture

Ralph uses a **pub/sub event system** where hats subscribe to topics and publish events:

```yaml
# ralph.yml - Hat configuration example
hats:
  builder:
    name: "Builder"
    triggers: ["build.task"]           # Subscribes to these events
    publishes: ["build.done", "build.blocked"]
    default_publishes: "build.done"    # Fallback if no event written
    backend: "claude"                  # Per-hat backend
    instructions: |
      ## BUILDER PHASE
      Implement the task. Record your thinking as memories...

  confessor:
    name: "Confessor"
    triggers: ["build.done"]
    publishes: ["confession.clean", "confession.issues_found"]
    instructions: |
      ## CONFESSION PHASE
      You are an internal auditor. Your ONLY job is to find issues...
```

### Event Routing

1. **Explicit routing**: Event topic matches hat's `triggers`
2. **Default publishes**: If hat completes without writing event, use `default_publishes`
3. **Ralph fallback**: If no subscriber for event, Ralph handles it

### Per-Hat Backends

Hats can use different AI backends:
```yaml
hats:
  coder:
    backend: "claude"           # Claude Code
  reviewer:
    backend: "gemini"           # Gemini CLI (different perspective)
  researcher:
    backend:
      type: "kiro"
      agent: "researcher"       # Kiro with custom agent
  custom:
    backend:
      command: "./my-agent"
      args: ["--mode", "build"]
```

### Parallel Loop Execution

Ralph supports multiple orchestration loops in parallel using git worktrees:

```
Primary Loop (holds .ralph/loop.lock)
├── Runs in main workspace
├── Processes merge queue on completion
└── Spawns merge-ralph for queued loops

Worktree Loops (.worktrees/<loop-id>/)
├── Isolated filesystem via git worktree
├── Symlinked memories, specs, tasks → main repo
├── Queue for merge on completion
└── Exit cleanly (no spawn)
```

**Use case**: Run multiple independent tasks simultaneously without conflicts.

---

## Task Management

### Task Lifecycle

```
┌─────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────┐
│  Open   │───►│ InProgress  │───►│   Closed    │    │ Failed  │
│  [ ]    │    │    [~]      │    │    [x]      │    │   [!]   │
└─────────┘    └─────────────┘    └─────────────┘    └─────────┘
```

### Task Store Operations

```bash
ralph tools task list                    # List all tasks
ralph tools task ready                   # Show ready-to-work tasks
ralph tools task add "Fix bug" -p 1      # Add high-priority task
ralph tools task close <id>              # Mark task complete
ralph tools task fail <id>               # Mark task failed
```

### Integration with Event Loop

- Tasks replace scratchpad for completion verification (when memories enabled)
- Loop terminates when no open tasks + consecutive LOOP_COMPLETE
- Each task tracks its creating loop ID for parallel execution isolation

---

## Integration with Claude Code

### Primary Backend

Claude Code is the default and most supported backend:
```yaml
cli:
  backend: claude
  prompt_mode: arg  # or "file" for large prompts
```

### Skill System

Ralph integrates with Claude Code's skill system:
```yaml
skills:
  enabled: true
  dirs:
  - .claude/skills
  overrides:
    ralph-operations:
      auto_inject: true
```

Skills are automatically discovered and injected into prompts.

### Agent Definitions

Claude Code agents defined in `.claude/agents/`:
- `code-assist.md` — Implementation guidance
- `ralph-e2e-verifier.md` — E2E testing
- `ralph-loop-runner.md` — Loop execution

### RObot (Human-in-the-Loop)

Telegram integration for human interaction:
```yaml
RObot:
  enabled: true
  timeout_seconds: 120
  telegram:
    bot_token: "${RALPH_TELEGRAM_BOT_TOKEN}"
```

Event types:
- `human.interact` — Agent asks question, blocks until response
- `human.response` — Reply to agent question
- `human.guidance` — Proactive human guidance injected into prompt

---

## Strengths

1. **Sophisticated Event Architecture**: The pub/sub system with hatless Ralph as universal fallback is elegant and resilient. No single point of failure.

2. **Multi-Backend Flexibility**: Per-hat backend configuration allows leveraging each tool's strengths (Claude for coding, Gemini for review, Kiro for MCP tools).

3. **Production-Grade Observability**: Comprehensive diagnostics, structured logging, web dashboard, and telemetry make debugging and monitoring straightforward.

4. **Git-Native State Management**: Using git worktrees for parallel execution and disk-based state (JSONL, markdown) eliminates complex distributed state coordination.

5. **Robust Safeguards**: Multiple termination conditions prevent runaway loops and excessive costs.

6. **Memory System**: Persistent learning across sessions with token budget management and semantic search.

7. **Preset Ecosystem**: 31 built-in presets for common workflows (TDD, spec-driven, debugging, etc.).

8. **Human-in-the-Loop**: Telegram integration allows agents to ask questions and receive guidance without breaking the loop.

9. **Skill Integration**: Native support for Claude Code's skill system enables modular, reusable capabilities.

10. **Fresh Context Philosophy**: Each iteration starts fresh, avoiding context rot and ensuring reliable execution.

---

## Weaknesses/Limitations

1. **Rust Complexity**: The codebase is substantial (~15K+ lines of Rust) with a steep learning curve for contributors.

2. **Backend Dependency**: Requires external CLI tools (Claude Code, etc.) installed and configured.

3. **Git-Centric**: Tightly coupled to git workflows; less suitable for non-git projects or monorepos with complex branching.

4. **No Native Parallelism Within Loops**: Hats execute sequentially; parallel execution only via worktrees (separate processes).

5. **YAML Configuration**: While flexible, complex hat configurations can become verbose and error-prone.

6. **Limited Dynamic Hat Lifecycle**: Hats are fixed at startup; no dynamic spawning/killing of hats mid-loop.

7. **Disk I/O Overhead**: Heavy reliance on file system for state (events.jsonl, tasks.jsonl) could be a bottleneck for very high-frequency operations.

8. **No Built-in Vector Search**: Memory search is keyword/tag-based; no semantic/embedding search for memories.

9. **Web Dashboard Maturity**: Marked as "Alpha" with expected breaking changes.

10. **Resource Intensive**: Running multiple parallel loops with worktrees can consume significant disk space and memory.

---

## Integration Potential for BB5

### High-Value Integration Points

1. **Event Loop Architecture**: The pub/sub event system with hatless coordinator is directly applicable to BB5's RALF executor. Could replace or augment the current task-based approach.

2. **Hat System**: BB5 could adopt the hat abstraction for specialized agents:
   - `builder` hat for code implementation
   - `reviewer` hat for PR review
   - `tester` hat for validation
   - `documenter` hat for documentation

3. **Memory System**: BB5's learning layer could leverage Ralph's memory types (Pattern, Decision, Fix, Context) and markdown-based storage.

4. **Parallel Loop Execution**: The git worktree approach for parallel execution could be adapted for BB5's multi-agent scenarios.

5. **Safeguards Framework**: Ralph's termination conditions (max iterations, cost limits, stall detection) should be ported to BB5.

6. **Diagnostics Infrastructure**: The structured logging and diagnostics collection would significantly improve BB5's observability.

7. **Skill Integration**: BB5 could adopt the skill system for modular agent capabilities.

### Adaptation Considerations

| Ralph Feature | BB5 Adaptation | Effort |
|---------------|----------------|--------|
| Hatless Ralph | Core coordinator agent | Medium |
| Event pub/sub | Message bus for agent teams | Medium |
| Per-hat backends | Agent-specific model selection | Low |
| Git worktrees | Container/workspace isolation | Medium |
| Memory system | Learning layer integration | Low |
| Task system | Existing task queue integration | Low |
| Web dashboard | Extend existing BB5 dashboard | High |
| RObot | Human-in-the-loop protocol | Medium |

### Suggested Integration Approach

1. **Phase 1: Core Concepts**
   - Adopt "Hatless Ralph" pattern for BB5's coordinator
   - Implement event pub/sub for agent communication
   - Port safeguard mechanisms

2. **Phase 2: Memory & Learning**
   - Integrate memory types into BB5's learning layer
   - Implement memory injection into agent prompts

3. **Phase 3: Advanced Features**
   - Parallel loop execution via workspace isolation
   - Human-in-the-loop protocol
   - Diagnostics and observability

---

## Recommendation

**Priority: HIGH** — This is the most sophisticated Ralph implementation analyzed.

### Should BB5 Integrate?

**Yes**, with selective adoption:

1. **Adopt the Architecture**: The hatless coordinator + pub/sub event system is a proven, resilient pattern that would strengthen BB5's agent orchestration.

2. **Port Key Components**:
   - Event loop with safeguards
   - Memory system
   - Task management
   - Diagnostics infrastructure

3. **Adapt, Don't Adopt Directly**:
   - BB5 doesn't need the full Rust codebase
   - Extract patterns and reimplement in BB5's tech stack
   - Focus on the event architecture and state management patterns

4. **Leverage for Inspiration**:
   - The "Ralph Tenets" align well with BB5's philosophy
   - Preset system could inspire BB5's workflow templates
   - Skill integration pattern is valuable

### Key Takeaways for BB5

1. **Fresh context per iteration** — Don't carry full conversation history; checkpoint and restart
2. **Disk is state** — Use file-based state for resilience and observability
3. **Backpressure over prescription** — Define quality gates, not step-by-step instructions
4. **Universal fallback** — Always have a coordinator that can handle orphaned work
5. **Structured events** — Use JSONL or similar for event logging, not XML or unstructured text

---

## Files Referenced

- `/ralph.yml` — Main configuration with hat definitions
- `/crates/ralph-core/src/hatless_ralph.rs` — Constant coordinator implementation
- `/crates/ralph-core/src/event_loop/mod.rs` — Main orchestration loop
- `/crates/ralph-core/src/hat_registry.rs` — Hat management
- `/crates/ralph-core/src/task.rs` — Task data structures
- `/crates/ralph-core/src/memory.rs` — Memory data structures
- `/crates/ralph-cli/src/main.rs` — CLI entry point
- `/backend/ralph-web-server/src/queue/Dispatcher.ts` — Web dashboard task dispatcher
- `/backend/ralph-web-server/src/services/LoopsManager.ts` — Parallel loop management
- `/presets/code-assist.yml` — Example preset with 4-hat workflow
- `/.ralph/specs/event-loop/design/detailed-design.md` — Architecture specification
