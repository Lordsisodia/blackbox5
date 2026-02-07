# MCP and Plugin Architecture for BlackBox5 Agent Mesh

**Research Date:** 2026-02-07
**Status:** Architecture Recommendation
**Priority:** CRITICAL

---

## Executive Summary

This document provides a comprehensive analysis of Claude Code's MCP (Model Context Protocol) and plugin architecture, with specific recommendations for BlackBox5's agent communication system and Agent Mesh implementation.

**Key Findings:**
1. MCP is the emerging industry standard for AI-tool integration (Anthropic-backed, 21.2k+ stars)
2. Claude Code plugins provide a powerful distribution mechanism for skills, agents, and MCP servers
3. BlackBox5 can leverage MCP as both client (consuming external tools) and server (exposing RALF capabilities)
4. Tool naming convention `mcp__<server>__<tool>` enables seamless integration

---

## 1. MCP Server Integration

### 1.1 What is MCP?

The **Model Context Protocol (MCP)** is an open standard protocol developed by Anthropic for building secure, two-way connections between AI-powered tools and external data sources or systems.

**Key Characteristics:**
- **Open Standard:** Public specification with community involvement
- **JSON-RPC 2.0:** Standard protocol for requests/responses
- **Transport Agnostic:** Supports stdio, HTTP, SSE, WebSocket
- **Security First:** Explicit consent, user control, tool validation
- **Three Core Features:** Resources (read), Tools (actions), Prompts (templates)

### 1.2 MCP Server Types

Claude Code supports four transport types for MCP servers:

#### HTTP (Recommended for Remote)
```bash
# Basic syntax
claude mcp add --transport http <name> <url>

# Example: Connect to Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# With Bearer token
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

**Characteristics:**
- Most widely supported for cloud-based services
- REST-like interface
- Supports load balancing and CDN caching
- Ideal for production deployments

#### SSE (Server-Sent Events) - Deprecated
```bash
# Basic syntax (deprecated, use HTTP instead)
claude mcp add --transport sse <name> <url>

# Example
claude mcp add --transport sse asana https://mcp.asana.com/sse
```

**Note:** SSE is deprecated in favor of HTTP transports.

#### stdio (Local Processes)
```bash
# Basic syntax
claude mcp add [options] <name> -- <command> [args...]

# Example: Add Airtable server
claude mcp add --transport stdio --env AIRTABLE_API_KEY=YOUR_KEY airtable \
  -- npx -y airtable-mcp-server

# Important: Options must come BEFORE the server name
# The -- (double dash) separates Claude's flags from server command
```

**Characteristics:**
- Runs as local processes on the machine
- Ideal for tools needing direct system access
- Custom scripts and development tools
- Lower latency for local operations

#### WebSocket (Real-time)
```python
# Python MCP SDK example
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("BlackBox5")
mcp.run(transport="websocket", port=8080)
```

**Characteristics:**
- Bidirectional streaming
- Real-time updates
- Low latency
- Ideal for collaborative features

### 1.3 Tool Naming Convention

MCP tools are automatically namespaced using the pattern:
```
mcp__<server_name>__<tool_name>
```

**Examples:**
- `mcp__github__list_prs` - List PRs from GitHub MCP server
- `mcp__sentry__get_errors` - Get errors from Sentry MCP server
- `mcp__postgres__query` - Query PostgreSQL via MCP server

**Benefits:**
- Prevents naming conflicts between servers
- Clear identification of tool source
- Easy to discover available tools

### 1.4 MCP Prompts as Slash Commands

MCP servers can expose prompts that become slash commands in Claude Code:

```bash
# Discover available prompts
/

# Execute a prompt without arguments
/mcp__github__list_prs

# Execute with arguments
/mcp__github__pr_review 456
/mcp__jira__create_issue "Bug in login flow" high
```

**Format:** `/mcp__<server>__<prompt>`

### 1.5 OAuth Authentication

Remote MCP servers can use OAuth 2.0 for secure authentication:

```bash
# 1. Add the server
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# 2. Authenticate within Claude Code
> /mcp

# 3. Follow browser flow to login
```

**Features:**
- Tokens stored securely
- Automatic refresh
- Clear authentication UI
- Works with HTTP servers

---

## 2. MCP for Agent Communication

### 2.1 MCP as Agent Message Bus

MCP can serve as a standardized message bus for agent-to-agent communication:

```
┌─────────────────────────────────────────────────────────┐
│                 MCP Message Bus Layer                    │
│         (Standardized agent communication)               │
└──────────────┬──────────────────────────┬───────────────┘
               │                          │
       ┌───────┴────────┐        ┌───────┴────────┐
       ▼                ▼        ▼                ▼
┌──────────┐    ┌──────────┐  ┌──────────┐  ┌──────────┐
│ Agent A  │    │ Agent B  │  │ Agent C  │  │ Agent D  │
│(Planner) │    │(Executor)│  │(Reviewer)│  │(Debugger)│
└──────────┘    └──────────┘  └──────────┘  └──────────┘
```

**Benefits:**
- Standardized protocol across all agents
- Language-agnostic (agents can be in different languages)
- Built-in security and access control
- Observable and debuggable

### 2.2 Tool-Based Agent RPC

Agents can expose capabilities as MCP tools:

```python
# Agent A exposes planning capability
@mcp.tool()
def create_plan(task_description: str) -> dict:
    """Create an execution plan for a task."""
    plan = planner.create(task_description)
    return {"plan_id": plan.id, "steps": plan.steps}

# Agent B calls Agent A's capability
result = await mcp_client.call_tool(
    "mcp__planner__create_plan",
    {"task_description": "Implement OAuth2"}
)
```

**Pattern:** Tool-based RPC between agents

### 2.3 MCP Resource Subscriptions

Agents can subscribe to resources for real-time updates:

```python
# Agent subscribes to task queue changes
@mcp.resource("bb5://tasks/{agent_id}")
def get_agent_tasks(agent_id: str) -> str:
    """Get tasks assigned to specific agent."""
    tasks = task_queue.get_for_agent(agent_id)
    return json.dumps(tasks)

# Reference in prompts
> Check my tasks at @bb5:tasks://agent-123
```

**Benefits:**
- Real-time updates
- Efficient polling
- Standardized access patterns

---

## 3. Plugin Architecture

### 3.1 Plugin Directory Structure

Claude Code plugins follow a standardized structure:

```
my-plugin/
├── .claude-plugin/           # Metadata directory (REQUIRED)
│   └── plugin.json          # Plugin manifest
├── commands/                 # Default command location
│   ├── status.md
│   └── logs.md
├── agents/                   # Default agent location
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── skills/                   # Agent Skills
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── hooks/                    # Hook configurations
│   ├── hooks.json
│   └── security-hooks.json
├── .mcp.json                # MCP server definitions
├── .lsp.json                # LSP server configurations
├── scripts/                 # Hook and utility scripts
│   ├── security-scan.sh
│   ├── format-code.py
│   └── deploy.js
├── LICENSE
└── CHANGELOG.md
```

**Important:** Only `plugin.json` goes inside `.claude-plugin/`. All other directories must be at the plugin root.

### 3.2 plugin.json Manifest Format

```json
{
  "name": "blackbox5-agent-mesh",
  "version": "1.2.0",
  "description": "BlackBox5 Agent Mesh integration plugin",
  "author": {
    "name": "BlackBox5 Team",
    "email": "team@blackbox5.ai",
    "url": "https://github.com/blackbox5"
  },
  "homepage": "https://docs.blackbox5.ai",
  "repository": "https://github.com/blackbox5/agent-mesh-plugin",
  "license": "MIT",
  "keywords": ["agents", "mcp", "mesh", "orchestration"],

  "commands": "./custom/commands/",
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json"
}
```

**Required Fields:**
- `name`: Unique identifier (kebab-case, no spaces)

**Metadata Fields:**
- `version`: Semantic version (e.g., "1.2.0")
- `description`: Brief explanation
- `author`: Author information
- `homepage`: Documentation URL
- `repository`: Source code URL
- `license`: License identifier
- `keywords`: Discovery tags

**Component Path Fields:**
- `commands`: Additional command files/directories
- `agents`: Agent definition files
- `skills`: Skill directories
- `hooks`: Hook configuration
- `mcpServers`: MCP server config
- `outputStyles`: Output style files
- `lspServers`: LSP configuration

### 3.3 Plugin Components

#### Skills (Model-Invoked)
```markdown
---
name: code-review
description: Reviews code for best practices and potential issues.
             Use when reviewing code, checking PRs, or analyzing code quality.
---

When reviewing code, check for:
1. Code organization and structure
2. Error handling
3. Security concerns
4. Test coverage
```

**Location:** `skills/` directory with `SKILL.md` files

#### Agents (Subagents)
```markdown
---
description: What this agent specializes in
capabilities: ["task1", "task2", "task3"]
---

# Agent Name

Detailed description of the agent's role, expertise, and when Claude should invoke it.

## Capabilities

- Specific task the agent excels at
- Another specialized capability
- When to use this agent vs others
```

**Location:** `agents/` directory

#### Hooks (Event Handlers)
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

**Available Events:**
- `PreToolUse`: Before Claude uses any tool
- `PostToolUse`: After Claude successfully uses any tool
- `PostToolUseFailure`: After tool execution fails
- `PermissionRequest`: When permission dialog shown
- `UserPromptSubmit`: When user submits prompt
- `Notification`: When Claude sends notifications
- `Stop`: When Claude attempts to stop
- `SubagentStart`: When subagent started
- `SubagentStop`: When subagent stops
- `SessionStart`: At session beginning
- `SessionEnd`: At session end
- `PreCompact`: Before conversation compaction

**Hook Types:**
- `command`: Execute shell commands/scripts
- `prompt`: Evaluate prompt with LLM
- `agent`: Run agentic verifier

#### MCP Servers (in Plugins)
```json
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    },
    "plugin-api-client": {
      "command": "npx",
      "args": ["@company/mcp-server", "--plugin-mode"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

**Features:**
- Automatic lifecycle (start when plugin enables)
- Use `${CLAUDE_PLUGIN_ROOT}` for plugin-relative paths
- Multiple transport types supported
- Appear alongside manually configured MCP tools

### 3.4 Auto-Discovery Mechanisms

Plugins are automatically discovered when:
1. Installed via `/plugin install`
2. Loaded with `--plugin-dir` flag
3. Found in `.claude/plugins/` directory

**Discovery Process:**
1. Scan for `.claude-plugin/plugin.json` files
2. Validate manifest schema
3. Load components (skills, agents, hooks, MCP servers)
4. Register commands and slash commands
5. Start MCP servers

---

## 4. BlackBox5 as MCP Server

### 4.1 RALF MCP Server Architecture

Current implementation (`mcp-server-ralf.py`) provides basic tools:

```python
# Current RALF MCP Server Tools
tools = [
    {
        "name": "ralf_get_queue",
        "description": "Get the current RALF task queue",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "ralf_get_events",
        "description": "Get recent RALF events",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "ralf_get_task_status",
        "description": "Get status of a specific task",
        "inputSchema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "string"}
            },
            "required": ["task_id"]
        }
    },
    {
        "name": "ralf_run_command",
        "description": "Run a command in the RALF directory",
        "inputSchema": {
            "type": "object",
            "properties": {
                "command": {"type": "string"}
            },
            "required": ["command"]
        }
    }
]
```

### 4.2 Recommended Enhanced RALF MCP Server

```python
from mcp.server.fastmcp import FastMCP
import json

mcp = FastMCP("blackbox5-ralf")

# Agent Registry Tools
@mcp.tool()
def list_agents() -> dict:
    """List all registered agents in the BlackBox5 mesh."""
    return {
        "agents": [
            {"id": "planner", "status": "active", "capabilities": ["planning"]},
            {"id": "executor", "status": "active", "capabilities": ["execution"]},
            {"id": "reviewer", "status": "idle", "capabilities": ["review"]}
        ]
    }

@mcp.tool()
def get_agent_status(agent_id: str) -> dict:
    """Get detailed status of a specific agent."""
    return {
        "agent_id": agent_id,
        "status": "active",
        "current_task": "TASK-123",
        "queue_depth": 3,
        "last_heartbeat": "2026-02-07T10:30:00Z"
    }

# Task Management Tools
@mcp.tool()
def create_task(
    title: str,
    description: str,
    priority: str = "medium",
    assignee: str = None
) -> dict:
    """Create a new task in the RALF queue."""
    task_id = generate_task_id()
    return {
        "task_id": task_id,
        "status": "created",
        "title": title,
        "assignee": assignee
    }

@mcp.tool()
def delegate_task(task_id: str, agent_id: str) -> dict:
    """Delegate a task to a specific agent."""
    return {
        "task_id": task_id,
        "delegated_to": agent_id,
        "status": "delegated"
    }

# Event System Tools
@mcp.tool()
def subscribe_to_events(event_types: list[str]) -> dict:
    """Subscribe to RALF event notifications."""
    return {
        "subscription_id": "sub-123",
        "events": event_types,
        "status": "active"
    }

@mcp.resource("bb5://tasks/{status}")
def get_tasks_by_status(status: str) -> str:
    """Get tasks filtered by status."""
    tasks = task_queue.get_by_status(status)
    return json.dumps(tasks)

@mcp.resource("bb5://agents/{agent_id}/metrics")
def get_agent_metrics(agent_id: str) -> str:
    """Get performance metrics for an agent."""
    metrics = metrics_collector.get_for_agent(agent_id)
    return json.dumps(metrics)

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8000)
```

### 4.3 Agent Registry as MCP Resource

```python
@mcp.resource("bb5://registry/agents")
def list_all_agents() -> str:
    """List all agents in the registry."""
    agents = agent_registry.get_all()
    return json.dumps([{
        "id": a.id,
        "name": a.name,
        "capabilities": a.capabilities,
        "status": a.status,
        "endpoint": a.endpoint
    } for a in agents])

@mcp.resource("bb5://registry/agents/{agent_id}/card")
def get_agent_card(agent_id: str) -> str:
    """Get agent card (capability descriptor)."""
    agent = agent_registry.get(agent_id)
    return json.dumps({
        "id": agent.id,
        "name": agent.name,
        "description": agent.description,
        "capabilities": agent.capabilities,
        "tools": agent.tools,
        "resources": agent.resources
    })
```

### 4.4 Event System as MCP Notifications

```python
@mcp.tool()
def emit_event(
    event_type: str,
    payload: dict,
    source: str
) -> dict:
    """Emit an event to the BlackBox5 event bus."""
    event = {
        "type": event_type,
        "payload": payload,
        "source": source,
        "timestamp": datetime.utcnow().isoformat()
    }
    event_bus.emit(event)
    return {"event_id": event["id"], "status": "emitted"}

# MCP notifications for real-time updates
@mcp.notification()
def on_task_completed(task_id: str, result: dict):
    """Notify when a task is completed."""
    pass
```

---

## 5. Plugin Distribution

### 5.1 Plugin Marketplaces

Plugins can be distributed through marketplaces:

```json
// marketplace.json
{
  "name": "BlackBox5 Official",
  "plugins": [
    {
      "name": "bb5-agent-mesh",
      "source": "./plugins/bb5-agent-mesh",
      "description": "Agent mesh integration for BlackBox5",
      "version": "1.0.0"
    },
    {
      "name": "bb5-ralf-mcp",
      "source": "./plugins/bb5-ralf-mcp",
      "description": "RALF MCP server integration",
      "version": "1.0.0"
    }
  ]
}
```

**Installation:**
```bash
# Install from marketplace
claude plugin install bb5-agent-mesh@blackbox5

# Install to specific scope
claude plugin install bb5-agent-mesh --scope project
```

### 5.2 GitHub-Based Installation

```bash
# Install directly from GitHub
claude plugin install github.com/blackbox5/bb5-agent-mesh-plugin

# With specific version
claude plugin install github.com/blackbox5/bb5-agent-mesh-plugin@v1.2.0
```

### 5.3 Version Management

Follow semantic versioning:
```
MAJOR.MINOR.PATCH
```

**Version Format in plugin.json:**
```json
{
  "name": "bb5-agent-mesh",
  "version": "2.1.0"
}
```

**Best Practices:**
- Start at `1.0.0` for first stable release
- Update version before distributing changes
- Document changes in CHANGELOG.md
- Use pre-release versions for testing (`2.0.0-beta.1`)

---

## 6. Integration Patterns

### 6.1 MCP vs Direct Task Tool Usage

| Aspect | MCP | Direct Task Tool |
|--------|-----|------------------|
| **Standardization** | Industry standard | Claude Code specific |
| **Portability** | Works across clients | Claude Code only |
| **Discovery** | Automatic tool discovery | Manual registration |
| **Security** | Built-in consent model | Permission-based |
| **Flexibility** | External process | In-process |
| **Overhead** | Higher (IPC/network) | Lower (direct) |
| **Use Case** | External tools/services | Internal subagents |

### 6.2 When to Use Each Approach

**Use MCP When:**
- Integrating external services (GitHub, Sentry, databases)
- Building reusable tools across projects
- Need standardized protocol for multiple clients
- Tools run in separate processes/containers
- Security isolation is important

**Use Direct Task Tool When:**
- Spawning subagents for parallel work
- Internal task delegation within BlackBox5
- Need tight integration with Claude Code
- Lower latency is critical
- Working within a single codebase

### 6.3 Hybrid MCP + Task Architectures

```
┌─────────────────────────────────────────────────────────┐
│                    Claude Code Host                      │
└──────────────┬──────────────────────────┬───────────────┘
               │                          │
    ┌──────────▼──────────┐    ┌──────────▼──────────┐
    │   MCP Client        │    │   Task Tool         │
    │   (External Tools)  │    │   (Internal Agents) │
    └──────────┬──────────┘    └──────────┬──────────┘
               │                          │
    ┌──────────▼──────────┐    ┌──────────▼──────────┐
    │  External Services  │    │  BlackBox5 Agents   │
    │  - GitHub           │    │  - Planner          │
    │  - Sentry           │    │  - Executor         │
    │  - PostgreSQL       │    │  - Reviewer         │
    └─────────────────────┘    └─────────────────────┘
```

**Pattern:** Use MCP for external integrations, Task tool for internal orchestration.

---

## 7. Recommendations for BlackBox5

### 7.1 Immediate Actions (This Week)

1. **Implement Enhanced RALF MCP Server**
   - Add agent registry tools
   - Add task management tools
   - Add event subscription support
   - Use FastMCP for rapid development

2. **Create BlackBox5 Plugin**
   - Package RALF MCP server as plugin
   - Add custom skills for agent management
   - Add hooks for automatic task tracking

3. **Configure MCP Scopes**
   ```bash
   # Add RALF MCP server to project scope
   claude mcp add --transport stdio ralf -- \
     python /opt/ralf/mcp-server-ralf.py
   ```

### 7.2 Short-Term (Next 2 Weeks)

1. **Agent Mesh via MCP**
   - Implement agent discovery service as MCP resource
   - Create agent cards for all RALF agents
   - Enable tool-based agent RPC

2. **Plugin Distribution**
   - Create GitHub repository for BB5 plugins
   - Set up marketplace structure
   - Document installation process

3. **Event System Integration**
   - Expose RALF events as MCP notifications
   - Enable real-time agent status updates
   - Add subscription management

### 7.3 Medium-Term (Next Month)

1. **Hybrid Architecture**
   - MCP for external tool integration
   - Task tool for internal agent orchestration
   - Clear separation of concerns

2. **Advanced Features**
   - Intent-based routing via MCP
   - Multi-factor agent selection
   - Routing feedback and learning

3. **Production Hardening**
   - OAuth for remote MCP servers
   - Managed MCP configuration
   - Security policies and allowlists

### 7.4 Configuration Example

```json
// .mcp.json for BlackBox5 project
{
  "mcpServers": {
    "bb5-ralf": {
      "type": "stdio",
      "command": "python",
      "args": ["/opt/ralf/mcp-server-ralf.py"],
      "env": {
        "RALF_BASE": "/opt/ralf"
      }
    },
    "bb5-agent-registry": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    },
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```

---

## 8. Key Takeaways

1. **MCP is Strategic:** Industry-standard protocol for AI-tool integration, backed by Anthropic
2. **Plugin Distribution:** Enables sharing BB5 capabilities across projects and teams
3. **Tool Naming:** `mcp__<server>__<tool>` convention prevents conflicts
4. **Hybrid Approach:** Use MCP for external tools, Task tool for internal agents
5. **RALF as MCP Server:** Expose agent registry, tasks, and events via MCP
6. **OAuth Support:** Secure authentication for remote MCP servers
7. **Auto-Discovery:** Plugins automatically register skills, agents, hooks, and MCP servers

---

## References

1. [Claude Code MCP Documentation](https://code.claude.com/docs/en/mcp)
2. [Claude Code Plugins Documentation](https://code.claude.com/docs/en/plugins)
3. [Plugins Reference](https://code.claude.com/docs/en/plugins-reference)
4. [MCP Specification](https://modelcontextprotocol.io/specification/2025-11-25)
5. [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
6. [BlackBox5 MCP Architecture Recommendation](/Users/shaansisodia/.blackbox5/6-roadmap/01-research/skills-capabilities/findings/mcp-architecture-recommendation.md)
7. [Agent Discovery & Routing Research](/Users/shaansisodia/.blackbox5/6-roadmap/01-research/agent-types/findings/02-agent-discovery-routing.md)

---

**Document Version:** 1.0
**Last Updated:** 2026-02-07
**Status:** Ready for Implementation
