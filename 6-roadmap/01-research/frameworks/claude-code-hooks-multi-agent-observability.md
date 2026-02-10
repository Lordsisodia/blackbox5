# Claude Code Hooks Multi-Agent Observability

**Source:** https://github.com/disler/claude-code-hooks-multi-agent-observability
**Added:** 2026-02-10
**Research Status:** Pending Analysis

## Overview

Real-time monitoring and visualization system for Claude Code agents through comprehensive hook event tracking. Enables monitoring of multiple concurrent agents with session tracking, event filtering, and live updates.

## Key Features

### 1. Hook Event Types (12 Total)
- **PreToolUse** - Before tool execution
- **PostToolUse** - After successful tool execution
- **PostToolUseFailure** - After failed tool execution
- **PermissionRequest** - When permissions are requested
- **Notification** - General notifications
- **Stop** - Session stop events
- **SubagentStart** - Sub-agent initialization
- **SubagentStop** - Sub-agent completion
- **PreCompact** - Before context compaction
- **UserPromptSubmit** - User input submission
- **SessionStart** - New session begins
- **SessionEnd** - Session terminates

### 2. Architecture

```
Claude Agents → Hook Scripts → HTTP POST → Bun Server → SQLite → WebSocket → Vue Client
```

**Components:**
- **Server** (`apps/server/`): Bun-powered TypeScript server with SQLite (WAL mode)
- **Client** (`apps/client/`): Vue 3 TypeScript app with real-time visualization
- **Hooks** (`.claude/hooks/`): Python scripts using `uv` for event interception

### 3. Multi-Agent Support
- Tracks agent teams working in parallel
- Supports `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`
- Builder and Validator agent definitions
- Session-based color coding for visual distinction

### 4. Unique Capabilities

- **MCP Tool Detection**: Identifies `mcp_server` and `mcp_tool_name` in events
- **Stop Hook Validators**: Prevent infinite loops and validate file creation/content
- **Planning Commands**: `/plan_w_team` slash command generates spec documents
- **Real-time Dashboard**: Live pulse charts, event timelines, chat transcript viewer

## Setup Requirements

- Claude Code (Anthropic's CLI)
- Astral `uv` (Python package manager)
- Bun/npm/yarn
- Optional: `just` command runner, API keys

**Quick start:** `just start` (server on port 4000, client on port 5173)

## Potential BB5 Integration Points

### 1. RALF Executor Monitoring
- Hook into RALF autonomous execution loop
- Real-time visibility into task execution
- Track agent decisions and tool usage

### 2. Agent Team Coordination
- Monitor multiple BB5 agents working in parallel
- Visual dashboard for agent status
- Event tracking for debugging

### 3. Task Execution Analytics
- Track task completion rates
- Monitor tool usage patterns
- Identify bottlenecks in execution

### 4. Integration with Existing Hooks
- BB5 already has hook infrastructure
- Can extend with observability hooks
- SQLite storage aligns with BB5 data architecture

## Research Questions

1. How can we adapt this for BB5's autonomous RALF loop?
2. Can we integrate with existing Redis-based status system?
3. What's the performance impact of hook overhead?
4. How to handle multi-VPS agent deployment?
5. Can we use this for the MoltBot integration?

## Next Steps

- [ ] Clone and test the repository
- [ ] Analyze hook implementation details
- [ ] Design BB5 integration architecture
- [ ] Prototype with RALF executor
- [ ] Evaluate performance impact
