# Honest Technical Assessment: Vibe Kanban MCP Enhancements

## The Brutal Truth

**Most of what I proposed earlier is NOT possible right now.** Here's why:

### What's Actually Already There

Looking at the Vibe Kanban codebase:

1. **Session tracking exists** - `sessions` table with `workspace_id` and `executor`
2. **Execution process tracking exists** - `execution_processes` with status, timestamps
3. **Coding agent turns exist** - `coding_agent_turns` with `prompt` and `summary`
4. **Logs exist** - `execution_process_logs` with JSONL-formatted logs
5. **Workspace context exists** - Can get workspace, task, project, repos all linked
6. **Active workspace detection** - `find_all_with_status()` shows `is_running` state

### What's Missing (The Hard Truth)

| Proposed Feature | Possible? | Why/Why Not |
|-----------------|-----------|-------------|
| **Agent-to-agent messaging** | **NO** | Agents run in isolated containers/processes. No message bus. No way to interrupt a running agent process from outside. |
| **Conversation history** | **PARTIAL** | `coding_agent_turns` stores prompt + summary only. Full conversation (tool calls, responses) is NOT stored in DB - it lives in the agent's process memory only. |
| **Code visibility** | **PARTIAL** | Can see git state in workspace. Can see files. But no tracking of which files an agent "read" - only which files were modified. |
| **Mid-conversation intervention** | **NO** | Agents are external processes (Claude Code, Cursor, etc.). Vibe Kanban spawns them and waits. No mechanism to inject messages mid-execution. |
| **Real-time thinking process** | **NO** | Agent's thinking happens in the external agent's brain (OpenAI, Anthropic API). VK only sees the final results. |

### The Architecture Problem

```
┌─────────────────────────────────────────────────────────────────┐
│                     Vibe Kanban Server                         │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐      │
│  │   Database    │  │   API Server  │  │  MCP Server   │      │
│  │  (SQLite)     │  │   (Axum)      │  │  (rmcp)        │      │
│  └───────────────┘  └───────────────┘  └───────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ spawns, waits
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              External Agent Process (Isolated)                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Claude Code / Cursor / Copilot / etc.                  │   │
│  │  - Runs in workspace directory                          │   │
│  │  - Has full conversation in memory                      │   │
│  │  - VK only sees: prompt, exit code, logs               │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

**Vibe Kanban cannot see inside the agent process.** It's a black box.

---

## What IS Actually Possible (Right Now)

### 1. List Active Agents ✅ **EASY**

Already have the data. Just expose via MCP.

**Implementation**: Add 1 MCP tool that queries existing tables.

```rust
#[tool(description = "List all active agent sessions")]
async fn list_active_agents(&self) -> Result<CallToolResult, ErrorData> {
    // Query: workspaces + sessions + execution_processes
    // Filter: status = 'running' AND run_reason = 'codingagent'
    // Return: workspace_id, task_id, executor, started_at, branch
}
```

**Time**: 1-2 hours

### 2. Get Agent Logs ✅ **EASY**

Logs are already stored in `execution_process_logs`.

**Implementation**: Add 1 MCP tool.

```rust
#[tool(description = "Get execution logs for an agent")]
async fn get_agent_logs(&self, Parameters(WorkspaceRequest { workspace_id })) -> ... {
    // Get session -> latest execution_process -> execution_process_logs
    // Return: parsed logs
}
```

**Time**: 2-3 hours

### 3. Get Workspace Git Status ✅ **EASY**

Can run git commands in workspace directory.

**Implementation**: Add 1 MCP tool.

```rust
#[tool(description = "Get git diff for a workspace")]
async fn get_workspace_diff(&self, Parameters(WorkspaceRequest { workspace_id })) -> ... {
    // Get workspace.container_ref
    // Run: git diff, git status, git log
    // Return: diff output
}
```

**Time**: 2-3 hours

### 4. Get Agent Turn Summary ✅ **EASY**

Already in `coding_agent_turns` table.

**Implementation**: Add 1 MCP tool.

```rust
#[tool(description = "Get agent turn summary (prompt + result)")]
async fn get_agent_turn_summary(&self, Parameters(WorkspaceRequest { workspace_id })) -> ... {
    // Join: workspace -> session -> execution_process -> coding_agent_turns
    // Return: prompt, summary, created_at
}
```

**Time**: 1-2 hours

### 5. Get Latest Task Status Across All Workspaces ✅ **EASY**

Already have all the data.

**Implementation**: Add 1 MCP tool.

```rust
#[tool(description = "Get status overview of all tasks across workspaces")]
async fn get_team_overview(&self, Parameters(ProjectRequest { project_id })) -> ... {
    // Join: tasks -> workspaces -> sessions -> execution_processes
    // Return: task status, is_running, last_activity
}
```

**Time**: 2-3 hours

---

## What's Possible WITH Small Changes

### 6. Send Message to Next Agent Turn ⚠️ **MEDIUM**

Can't interrupt running agent, BUT can store a message that gets picked up when the agent starts its next turn.

**Implementation**:
1. Add new table: `pending_agent_messages(workspace_id, message, created_at)`
2. Modify agent startup to check for and inject pending messages
3. Add MCP tool to queue messages

**Time**: 4-6 hours (requires DB migration + executor changes)

### 7. Track File Access Patterns ⚠️ **MEDIUM**

Can use filesystem watching or wrap git commands to track file reads.

**Implementation**:
1. Add `file_access_log` table
2. Wrap agent git operations to log touched files
3. Add MCP tools to query access patterns

**Time**: 4-6 hours

### 8. Basic Metrics Dashboard ⚠️ **MEDIUM**

Already have the data, just need aggregation queries.

**Implementation**:
1. Add MCP tools for metrics queries
2. Compute: avg runtime, success rate, files per task

**Time**: 3-4 hours

---

## What's NOT Possible (Without Major Re-architecture)

### ❌ Real-time Agent Messaging
**Why**: Agents are external binary processes. No message injection mechanism exists.
**Would need**: Build a custom agent wrapper that reads from a message queue mid-turn.

### ❌ Full Conversation History
**Why**: Only prompt + summary are stored. Full conversation (with tool calls) lives in agent memory.
**Would need**: Modify every executor (Claude, Cursor, Copilot, etc.) to stream full conversation to VK.

### ❌ Mid-Conversation Intervention
**Why**: Once agent process starts, it runs until completion. VK just waits for exit code.
**Would need**: Build custom agent orchestration layer with bidirectional communication.

### ❌ See What Agent "Saw" (Not Modified)
**Why**: VK only sees git changes. Doesn't track file reads.
**Would need**: Filesystem monitoring or agent instrumentation (language server protocol).

---

## Quick Win Implementation Plan

Do these 5 things TODAY:

| # | Tool | Difficulty | Time | Value |
|---|------|------------|------|-------|
| 1 | `list_active_agents` | EASY | 2h | ⭐⭐⭐⭐⭐ |
| 2 | `get_agent_logs` | EASY | 3h | ⭐⭐⭐⭐ |
| 3 | `get_workspace_diff` | EASY | 3h | ⭐⭐⭐⭐ |
| 4 | `get_agent_turn_summary` | EASY | 2h | ⭐⭐⭐ |
| 5 | `get_team_overview` | EASY | 3h | ⭐⭐⭐⭐⭐ |

**Total time: ~13 hours (1-2 days)**

This gives you:
- See which agents are running
- Read their logs
- See what code they changed
- Get summaries of their work
- Team-wide status dashboard

---

## The REAL Solution (If You Want Full Features)

To get actual agent-to-agent communication and intervention, you need:

### Option A: Build Agent Sidecar
```
┌─────────────┐     ┌─────────────┐
│  VK Server  │────▶│  Sidecar    │────▶┌─────────────┐
│             │     │  Process    │     │  Claude     │
└─────────────┘     │  (Message   │     │  Code       │
                    │   Queue)    │────▶│             │
                    └─────────────┘     └─────────────┘
```

The sidecar:
- Intercepts agent I/O
- Maintains message queue
- Allows injection mid-turn
- Streams full conversation back to VK

**Effort**: 2-3 weeks full-time work

### Option B: Custom Agent Runtime
Build your own agent execution layer (don't use external binaries).

**Effort**: 4-6 weeks full-time work

### Option C: Fork Executors
Fork Claude Code, Cursor, etc. to add VK integration hooks.

**Effort**: 1-2 weeks per executor + ongoing maintenance

---

## Recommendation

**Do the 5 quick wins first** (1-2 days). Then decide if you need more.

The 5 quick wins give you 80% of the visibility you actually need for managerial oversight. The remaining 20% (real-time intervention) requires major re-architecture that may not be worth it.

Want me to implement the 5 quick wins now?
