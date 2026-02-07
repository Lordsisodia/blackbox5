# Multi-Agent Management Patterns: OpenClaw vs Claude Code

**Research Date:** 2026-02-07
**Purpose:** Identify best practices for managerial agent architecture in BlackBox5 + OpenClaw integration

---

## Executive Summary

This analysis compares multi-agent management patterns between OpenClaw and Claude Code to inform the design of a managerial agent architecture for BlackBox5. Both systems offer distinct approaches to agent coordination, workspace isolation, routing, and security. The recommended architecture synthesizes the strengths of both systems while addressing the specific needs of the BlackBox5 ecosystem.

---

## 1. Comparison: OpenClaw vs Claude Code Agent Management

### 1.1 Architecture Philosophy

| Aspect | OpenClaw | Claude Code |
|--------|----------|-------------|
| **Core Model** | Gateway-based multi-agent runtime with channel routing | Single-session subagent delegation model |
| **Agent Identity** | Multiple fully-isolated agents (separate workspaces, auth, sessions) | Subagents within a parent conversation context |
| **Communication** | Channel-based (WhatsApp, Telegram, Slack, etc.) | File-based configuration + interactive commands |
| **Scoping** | Agent-per-channel/per-peer routing | Task-based delegation with description matching |
| **Persistence** | Per-agent session stores (`~/.openclaw/agents/<agentId>/sessions`) | Subagent transcripts in `~/.claude/projects/{project}/{sessionId}/subagents/` |

### 1.2 Agent Lifecycle

**OpenClaw:**
- Agents are long-running entities with persistent workspaces
- Each agent has dedicated: workspace, `agentDir`, session store, auth profiles
- Agents defined in `openclaw.json` configuration
- Spawned via `sessions_spawn` tool for sub-agent tasks
- Sub-agents run in isolated sessions (`agent:<agentId>:subagent:<uuid>`)

**Claude Code:**
- Subagents are ephemeral, task-scoped instances
- Created via `/agents` command or markdown files with YAML frontmatter
- Four scope levels: CLI flag (session) > Project > User > Plugin
- Automatic delegation based on task description matching
- Subagents cannot spawn other subagents (prevents infinite nesting)

### 1.3 Configuration Approach

**OpenClaw (JSON5 Configuration):**
```json5
{
  agents: {
    list: [
      {
        id: "support",
        name: "Support Agent",
        workspace: "~/.openclaw/workspace-support",
        agentDir: "~/.openclaw/agents/support/agent",
        model: "anthropic/claude-sonnet-4-5",
        sandbox: { mode: "all", scope: "agent" },
        tools: { allow: ["read", "exec"], deny: ["write"] }
      }
    ]
  },
  bindings: [
    { agentId: "support", match: { channel: "slack", teamId: "T123" } }
  ]
}
```

**Claude Code (Markdown with YAML Frontmatter):**
```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
permissionMode: default
skills:
  - api-conventions
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

---

## 2. Best Practices for Managerial Agent Architecture

### 2.1 Task Routing Strategies

#### Intent-Based Routing
- **Description:** Route tasks based on natural language intent analysis
- **Implementation:** Use detailed agent descriptions that Claude matches against task descriptions
- **Best For:** Dynamic task assignment where the manager doesn't know the exact agent needed
- **Example:** "Use proactively" in descriptions triggers automatic delegation

#### Capability-Based Routing
- **Description:** Route based on explicit capability matching (tools, permissions, model)
- **Implementation:** Define agent capabilities in configuration; match against task requirements
- **Best For:** Security-sensitive environments requiring strict tool restrictions
- **Example:** OpenClaw's `tools.allow`/`tools.deny` with capability tags

#### Channel/Context-Based Routing
- **Description:** Route based on message source (channel, peer, account)
- **Implementation:** OpenClaw bindings with `match` criteria (channel, accountId, peer, guildId, teamId)
- **Best For:** Multi-tenant or multi-user environments
- **Example:** WhatsApp DMs to personal agent, Slack work channels to work agent

#### Hybrid Routing (Recommended)
```yaml
routing_strategy:
  primary: channel_context    # First match by channel/peer
  secondary: capability       # Then filter by required tools
  tertiary: intent            # Finally use description matching for ambiguous cases
  fallback: default_agent     # Route to default if no match
```

### 2.2 Workspace Isolation Patterns

#### Pattern 1: Full Isolation (OpenClaw Style)
- Each agent has completely separate workspace directory
- Separate auth profiles, session stores, skills
- No shared state between agents
- **Use When:** Multi-user scenarios, strict security boundaries, different personas

#### Pattern 2: Project-Scoped Isolation (Claude Code Style)
- Agents share project context but have isolated execution contexts
- Subagents inherit parent permissions but can be restricted
- Skills can be preloaded or shared
- **Use When:** Single-user, collaborative coding, task-specific specialization

#### Pattern 3: Hierarchical Isolation (Recommended for BlackBox5)
```
~/.blackbox5/
├── 5-project-memory/
│   └── <project>/
│       └── .autonomous/
│           ├── workspace/           # Shared project context
│           ├── agents/
│           │   ├── <agent-id>/      # Agent-specific state
│           │   │   ├── sessions/
│           │   │   ├── skills/
│           │   │   └── auth/
│           │   └── ...
│           └── shared/              # Cross-agent shared resources
```

### 2.3 Context Management Best Practices

1. **Bootstrap File Injection**
   - OpenClaw: Injects `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `USER.md` at session start
   - Sub-agents get `AGENTS.md` + `TOOLS.md` only (no persona files)
   - Keep bootstrap files under 20,000 chars to avoid token burn

2. **Memory Segmentation**
   - Daily memory logs: `memory/YYYY-MM-DD.md`
   - Curated long-term: `MEMORY.md` (main session only)
   - Sub-agent results via "announce" pattern with status + summary

3. **Context Compaction**
   - Both systems support auto-compaction at ~95% capacity
   - Subagents have independent compaction from main conversation
   - Set `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` for earlier compaction

---

## 3. Routing Strategies Deep Dive

### 3.1 OpenClaw Routing Hierarchy

Routing rules are evaluated in order (most-specific wins):

1. **Exact peer match** (`bindings` with `peer.kind` + `peer.id`)
2. **Guild match** (Discord) via `guildId`
3. **Team match** (Slack) via `teamId`
4. **Account match** (`accountId` on the channel)
5. **Channel match** (any account on that channel)
6. **Default agent** (`agents.list[].default`, else first list entry, fallback to `main`)

### 3.2 Claude Code Delegation Logic

Claude automatically delegates when:
- Task description matches subagent's `description` field
- User explicitly requests a subagent ("Use the code-reviewer agent")
- Task requires specialized capabilities (built-in Explore, Plan agents)

**Trigger phrases:** "use proactively" in descriptions encourages automatic delegation

### 3.3 Recommended Routing for BlackBox5

```yaml
# BlackBox5 Routing Configuration
routing:
  layers:
    # Layer 1: Explicit task routing (highest priority)
    - type: explicit
      match: task.metadata.assigned_agent

    # Layer 2: Goal/Plan-based routing
    - type: goal
      match: task.goal_id
      agent_mapping:
        "GOAL-001": "architect-agent"
        "GOAL-002": "dev-agent"

    # Layer 3: Capability-based routing
    - type: capability
      match:
        - pattern: "architecture|design|refactor"
          agent: "architect"
        - pattern: "implement|code|test"
          agent: "developer"
        - pattern: "research|analyze|investigate"
          agent: "researcher"

    # Layer 4: Tool requirement routing
    - type: tools_required
      match:
        - tools: ["database", "sql"]
          agent: "db-specialist"
        - tools: ["git", "github"]
          agent: "devops-agent"

    # Layer 5: Default fallback
    - type: default
      agent: "general-purpose"
```

---

## 4. Security and Isolation Patterns

### 4.1 Sandboxing Models

**OpenClaw Sandboxing:**
- Docker-based containerization
- Three modes: `"off"`, `"non-main"`, `"all"`
- Two scopes: `"session"` (per-session container), `"agent"` (per-agent container)
- Per-agent sandbox configuration overrides global defaults

**Claude Code Sandboxing:**
- OS-level primitives (Seatbelt on macOS, bubblewrap on Linux)
- Filesystem isolation: Read/write to working directory only
- Network isolation: Domain restrictions via proxy
- Sandboxed bash tool with `dangerouslyDisableSandbox` escape hatch

### 4.2 Tool Restriction Hierarchy

**OpenClaw Tool Filtering Order:**
1. Tool profile (`tools.profile`)
2. Provider tool profile (`tools.byProvider[provider].profile`)
3. Global tool policy (`tools.allow` / `tools.deny`)
4. Provider tool policy (`tools.byProvider[provider].allow/deny`)
5. Agent-specific tool policy (`agents.list[].tools.allow/deny`)
6. Agent provider policy (`agents.list[].tools.byProvider[provider].allow/deny`)
7. Sandbox tool policy (`tools.sandbox.tools`)
8. Subagent tool policy (`tools.subagents.tools`)

**Claude Code Tool Control:**
- `tools` field: Allowlist
- `disallowedTools` field: Denylist
- `permissionMode`: `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan`
- `PreToolUse` hooks for conditional validation

### 4.3 Permission Models

| Feature | OpenClaw | Claude Code |
|---------|----------|-------------|
| **Tool Allow/Deny** | Yes (hierarchical) | Yes (inheritance-based) |
| **Sandboxing** | Docker containers | OS-level (Seatbelt/bubblewrap) |
| **Elevated Mode** | Sender-based allowlist | Permission modes + hooks |
| **Auth Isolation** | Per-agent auth profiles | Inherited from parent |
| **Session Isolation** | Separate session stores | Isolated subagent contexts |

### 4.4 Recommended Security Architecture

```yaml
security_layers:
  # Layer 1: Network/Container (OpenClaw-style)
  sandbox:
    mode: "all"  # or "non-main" for flexibility
    scope: "agent"  # One container per agent
    docker:
      workspaceAccess: "ro"  # Read-only by default

  # Layer 2: Tool Policy (Both)
  tools:
    profile: "restricted"
    allow: ["read", "sessions_list", "sessions_send"]
    deny: ["exec", "write", "edit", "apply_patch"]

  # Layer 3: Permission Mode (Claude Code-style)
  permission_mode: "default"  # Require approval for sensitive operations

  # Layer 4: Runtime Validation (Claude Code-style)
  hooks:
    PreToolUse:
      - matcher: "Bash"
        command: "./scripts/validate-command.sh"
      - matcher: "Write|Edit"
        command: "./scripts/validate-file-write.sh"
```

---

## 5. MCP as a Management Bus

### 5.1 MCP Integration Patterns

**Claude Code MCP:**
- MCP servers provide external tools to agents
- Three scopes: local, project, user
- Dynamic tool updates via `list_changed` notifications
- Tool search for large MCP server collections
- Can act as MCP server itself (`claude mcp serve`)

**OpenClaw Integration Potential:**
- MCP servers could extend OpenClaw's built-in tools
- Gateway could expose agent management via MCP
- Sub-agents could be spawned through MCP tools

### 5.2 Recommended MCP Architecture for BlackBox5

```yaml
mcp_servers:
  # Agent Management Server
  agent_manager:
    type: stdio
    command: "bb5"
    args: ["agent", "mcp-serve"]
    provides:
      - agent_list
      - agent_spawn
      - agent_status
      - agent_stop

  # Task Queue Server
  task_queue:
    type: http
    url: "http://localhost:8080/mcp"
    provides:
      - task_enqueue
      - task_dequeue
      - task_status

  # Project Memory Server
  project_memory:
    type: stdio
    command: "bb5"
    args: ["memory", "mcp-serve"]
    provides:
      - memory_search
      - memory_store
      - memory_get
```

### 5.3 MCP as Agent Discovery Mechanism

```yaml
agent_discovery:
  mechanism: mcp_tool_search
  workflow:
    1: Manager receives task
    2: Manager queries MCP for available agent capabilities
    3: Manager matches task requirements to agent capabilities
    4: Manager spawns appropriate agent via MCP
    5: Agent reports results back through MCP
```

---

## 6. Agent Discovery Mechanisms

### 6.1 Static Configuration

**OpenClaw:** Agents defined in `openclaw.json` with explicit bindings
**Claude Code:** Subagents in `~/.claude/agents/` or `.claude/agents/`

### 6.2 Dynamic Discovery

**OpenClaw:**
- `agents_list` tool to discover available agents
- `agents.list[].subagents.allowAgents` for cross-agent spawning

**Claude Code:**
- `/agents` command lists all available agents
- Automatic delegation based on description matching
- Plugin-provided agents

### 6.3 Capability-Based Discovery (Recommended)

```yaml
agent_registry:
  discovery_methods:
    - type: capability_broadcast
      agents_announce:
        - agent_id
        - capabilities
        - tools_available
        - model
        - cost_estimate

    - type: skill_registry
      location: "~/.blackbox5/skills/"
      agents_register_skills_they_support

    - type: mcp_introspection
      query_mcp_servers_for_agent_capabilities
```

---

## 7. Recommended Architecture for BlackBox5 + OpenClaw Integration

### 7.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    BlackBox5 Manager Agent                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │   Router    │  │  Scheduler  │  │    Context Manager      │  │
│  │  (Routing)  │  │  (Queue)    │  │  (Workspace/Memory)     │  │
│  └──────┬──────┘  └──────┬──────┘  └───────────┬─────────────┘  │
│         └─────────────────┴─────────────────────┘                │
│                           │                                      │
│                    ┌──────┴──────┐                              │
│                    │  MCP Bus    │                              │
│                    └──────┬──────┘                              │
└───────────────────────────┼─────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────┴────┐        ┌────┴────┐        ┌────┴────┐
   │ Agent 1 │        │ Agent 2 │        │ Agent N │
   │(OpenClaw│        │(OpenClaw│        │(OpenClaw│
   │ Runtime)│        │ Runtime)│        │ Runtime)│
   └────┬────┘        └────┬────┘        └────┬────┘
        │                   │                   │
   ┌────┴────┐        ┌────┴────┐        ┌────┴────┐
   │Workspace│        │Workspace│        │Workspace│
   │  + Auth │        │  + Auth │        │  + Auth │
   └─────────┘        └─────────┘        └─────────┘
```

### 7.2 Agent Types

```yaml
agent_types:
  manager:
    description: "Central coordination agent for BlackBox5"
    tools: ["route_task", "spawn_agent", "monitor_agents", "synthesize_results"]
    model: "claude-opus-4-6"

  architect:
    description: "System design, patterns, scalability decisions"
    tools: ["read", "write", "research", "analyze"]
    model: "claude-opus-4-6"
    skills: ["bmad-architect"]

  developer:
    description: "Code implementation, testing, debugging"
    tools: ["read", "write", "edit", "bash", "test"]
    model: "claude-sonnet-4-5"
    skills: ["bmad-dev", "git-commit"]

  researcher:
    description: "Information gathering, best practices, analysis"
    tools: ["read", "grep", "glob", "web_search", "web_fetch"]
    model: "claude-haiku"
    permission_mode: "plan"

  qa:
    description: "Testing strategy, quality validation"
    tools: ["read", "test", "analyze"]
    model: "claude-sonnet-4-5"
    skills: ["bmad-qa"]
```

### 7.3 Configuration Structure

```json5
// ~/.blackbox5/config.json
{
  bb5: {
    version: "2.0",

    // Manager Agent Configuration
    manager: {
      agentId: "bb5-manager",
      workspace: "~/.blackbox5/5-project-memory",
      model: "anthropic/claude-opus-4-6",
      routing_strategy: "hybrid"
    },

    // Agent Definitions
    agents: {
      defaults: {
        model: "anthropic/claude-sonnet-4-5",
        sandbox: { mode: "non-main", scope: "agent" },
        subagents: {
          maxConcurrent: 4,
          model: "anthropic/claude-haiku",
          archiveAfterMinutes: 60
        }
      },
      list: [
        {
          id: "architect",
          name: "BMAD Architect",
          workspace: "~/.blackbox5/agents/architect",
          skills: ["bmad-architect", "superintelligence-protocol"],
          tools: { allow: ["read", "write", "research"], deny: ["exec"] }
        },
        {
          id: "developer",
          name: "BMAD Developer",
          workspace: "~/.blackbox5/agents/developer",
          skills: ["bmad-dev", "git-commit", "codebase-navigation"],
          tools: { profile: "coding" }
        },
        {
          id: "researcher",
          name: "BMAD Researcher",
          workspace: "~/.blackbox5/agents/researcher",
          model: "anthropic/claude-haiku",
          tools: { allow: ["read", "web_search", "web_fetch"], deny: ["write", "edit"] }
        }
      ]
    },

    // Routing Configuration
    routing: {
      rules: [
        { agentId: "architect", match: { taskType: "architecture" } },
        { agentId: "developer", match: { taskType: "implementation" } },
        { agentId: "researcher", match: { taskType: "research" } }
      ],
      fallback: "developer"
    },

    // MCP Integration
    mcp: {
      servers: {
        bb5_manager: {
          type: "stdio",
          command: "bb5",
          args: ["mcp-serve"]
        }
      }
    }
  }
}
```

### 7.4 Task Lifecycle

```
1. Task Creation
   └─ User or system creates task in BlackBox5

2. Manager Analysis
   └─ Manager agent analyzes task requirements
   └─ Determines required capabilities

3. Agent Selection
   └─ Match task to agent via routing rules
   └─ Fallback to capability-based selection

4. Agent Spawning
   └─ Spawn selected agent via sessions_spawn
   └─ Or delegate to subagent (Claude Code style)

5. Execution
   └─ Agent executes task in isolated workspace
   └─ Reports progress via session tools

6. Completion
   └─ Agent announces results
   └─ Manager synthesizes and stores learnings

7. Context Update
   └─ Update project memory
   └─ Store task outcomes
```

### 7.5 Integration with Existing BlackBox5 Components

```yaml
integration_points:
  # BB5 CLI Integration
  cli:
    command: "bb5 agent:spawn <agent-type> <task>"
    spawns_subagent_via_manager

  # Task System Integration
  tasks:
    location: "~/.blackbox5/5-project-memory/<project>/.autonomous/tasks/"
    manager_polls_for_pending_tasks
    auto_assigns_to_appropriate_agent

  # Memory System Integration
  memory:
    daily_logs: "memory/YYYY-MM-DD.md"
    curated: "MEMORY.md"
    agent_learnings: "~/.blackbox5/5-project-memory/<project>/.autonomous/memory/"

  # RALF Integration
  ralf:
    manager_can_delegate_to_ralf_worker_agents
    ralf_reports_back_via_mcp_or_sessions
```

---

## 8. Implementation Recommendations

### 8.1 Phase 1: Foundation
1. Implement manager agent with basic routing
2. Define 3-4 core agent types (architect, developer, researcher, qa)
3. Set up per-agent workspaces with isolation
4. Implement task queue integration

### 8.2 Phase 2: MCP Integration
1. Create MCP server for agent management
2. Expose agent discovery via MCP tools
3. Enable dynamic tool loading
4. Integrate with existing BB5 CLI

### 8.3 Phase 3: Advanced Features
1. Implement capability-based routing
2. Add agent-to-agent messaging
3. Create agent performance metrics
4. Build auto-scaling for agent pools

### 8.4 Key Design Principles

1. **Isolation by Default:** Each agent gets its own workspace and auth
2. **Explicit Routing:** Clear rules for task-to-agent matching
3. **Fail-Safe:** Unknown tasks route to general-purpose agent
4. **Observable:** All agent actions logged and auditable
5. **Recoverable:** Sub-agents can be resumed after interruption
6. **Cost-Aware:** Route to cheaper models for simple tasks

---

## 9. References

### OpenClaw Documentation
- `/Users/shaansisodia/.blackbox5/6-roadmap/research/external/documentation/openclaw/raw/pages/concepts-agent-workspace.md`
- `/Users/shaansisodia/.blackbox5/6-roadmap/research/external/documentation/openclaw/raw/pages/concepts-channel-routing.md`
- `/Users/shaansisodia/.blackbox5/6-roadmap/research/external/documentation/openclaw/raw/pages/concepts-multi-agent.md`
- `/Users/shaansisodia/.blackbox5/6-roadmap/research/external/documentation/openclaw/raw/pages/tools-subagents.md`
- `/Users/shaansisodia/.blackbox5/6-roadmap/research/external/documentation/openclaw/raw/pages/multi-agent-sandbox-tools.md`

### Claude Code Documentation
- `/Users/shaansisodia/.blackbox5/6-roadmap/research/external/documentation/claude-code/raw/pages/docs-en-sub-agents.md`
- `/Users/shaansisodia/.blackbox5/6-roadmap/research/external/documentation/claude-code/raw/pages/docs-en-mcp.md`
- `/Users/shaansisodia/.blackbox5/6-roadmap/research/external/documentation/claude-code/raw/pages/docs-en-sandboxing.md`

---

*Document generated for BlackBox5 multi-agent architecture planning.*
