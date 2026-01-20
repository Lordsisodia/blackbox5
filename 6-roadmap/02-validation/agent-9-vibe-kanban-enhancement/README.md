# Agent 9 - Vibe Kanban MCP Enhancements for Managerial Agents

## Overview

This document outlines enhancements to the Vibe Kanban MCP server to enable better agent-to-agent communication, code visibility, conversation history access, and mid-conversation intervention capabilities for managerial agents.

## Current State Analysis

### Existing Vibe Kanban MCP Tools (from `task_server.rs`)
1. **get_context** - Get project/task/workspace metadata
2. **create_task** - Create new tasks
3. **list_projects** - List all projects
4. **list_tasks** - List tasks with filters
5. **get_task** - Get task details
6. **update_task** - Update task status/description
7. **delete_task** - Delete tasks
8. **list_repos** - List repositories in a project
9. **get_repo** - Get repository details including scripts
10. **update_setup_script** - Update repository setup script
11. **update_cleanup_script** - Update repository cleanup script
12. **update_dev_server_script** - Update dev server script
13. **start_workspace_session** - Start an agent working on a task

### Current Managerial Agent Capabilities
From `vibe_kanban_manager.py` and `team_dashboard.py`:
- Task CRUD operations
- Agent spawning and monitoring
- Workspace change tracking
- Merge and review coordination
- Dependency management
- Performance metrics and reporting

### Limitations
1. **No direct agent-to-agent messaging** - Agents cannot send messages to each other
2. **Limited code visibility** - Managers cannot see what code agents have accessed/modified
3. **No conversation history** - Managers cannot see agent conversation logs
4. **No intervention mechanism** - Cannot interrupt or guide active agents
5. **No real-time agent state** - Limited visibility into agent thinking process

---

## Proposed MCP Tool Enhancements

### 1. Agent-to-Agent Communication Tools

#### 1.1 `send_agent_message`
Send a message to a specific agent's workspace session.

```rust
#[derive(Debug, Deserialize, schemars::JsonSchema)]
pub struct SendAgentMessageRequest {
    #[schemars(description = "The workspace ID of the target agent")]
    pub workspace_id: Uuid,
    #[schemars(description = "Message content (markdown supported)")]
    pub message: String,
    #[schemars(description = "Optional message priority")]
    pub priority: Option<String>, // "info", "warning", "critical"
}

#[derive(Debug, Serialize, schemars::JsonSchema)]
pub struct SendAgentMessageResponse {
    pub success: bool,
    pub message_id: String,
    pub delivered_at: String,
}
```

**Use Cases:**
- Manager asks agent for status update
- Agent asks peer agent for coordination
- Emergency broadcast to all active agents

#### 1.2 `list_active_agents`
List all currently active agent sessions with their states.

```rust
#[derive(Debug, Deserialize, schemars::JsonSchema)]
pub struct ListActiveAgentsRequest {
    #[schemars(description = "Optional project filter")]
    pub project_id: Option<Uuid>,
}

#[derive(Debug, Serialize, schemars::JsonSchema)]
pub struct AgentSessionInfo {
    pub workspace_id: Uuid,
    pub task_id: Uuid,
    pub task_title: String,
    pub agent_type: String,
    pub status: String,
    pub started_at: String,
    pub last_activity: String,
    pub branch: String,
    pub workspace_path: String,
}

#[derive(Debug, Serialize, schemars::JsonSchema)]
pub struct ListActiveAgentsResponse {
    pub agents: Vec<AgentSessionInfo>,
    pub count: usize,
}
```

#### 1.3 `broadcast_message`
Send a message to all active agents.

```rust
#[derive(Debug, Deserialize, schemars::JsonSchema)]
pub struct BroadcastMessageRequest {
    #[schemars(description = "Message content")]
    pub message: String,
    #[schemars(description = "Optional project filter")]
    pub project_id: Option<Uuid>,
    #[schemars(description = "Message priority")]
    pub priority: Option<String>,
}
```

---

### 2. Code Visibility Tools

#### 2.1 `get_agent_code_context`
Get code files accessed/modified by an agent.

```rust
#[derive(Debug, Deserialize, schemars::JsonSchema)]
pub struct GetAgentCodeContextRequest {
    #[schemars(description = "Workspace ID")]
    pub workspace_id: Uuid,
    #[schemars(description = "Include file contents")]
    pub include_contents: Option<bool>,
}

#[derive(Debug, Serialize, schemars::JsonSchema)]
pub struct FileAccessInfo {
    pub path: String,
    pub action: String, // "read", "modified", "created", "deleted"
    pub timestamp: String,
    pub content_preview: Option<String>, // First N chars
}

#[derive(Debug, Serialize, schemars::JsonSchema)]
pub struct GetAgentCodeContextResponse {
    pub workspace_id: Uuid,
    pub task_id: Uuid,
    pub files: Vec<FileAccessInfo>,
    pub git_status: Option<String>,
    pub diff_summary: Option<String>,
}
```

#### 2.2 `get_codebase_snapshot`
Get a snapshot of the codebase state in a workspace.

```rust
#[derive(Debug, Deserialize, schemars::JsonSchema)]
pub struct GetCodebaseSnapshotRequest {
    #[schemars(description = "Workspace ID")]
    pub workspace_id: Uuid,
}

#[derive(Debug, Serialize, schemars::JsonSchema)]
pub struct CodebaseSnapshotResponse {
    pub workspace_id: Uuid,
    pub branch: String,
    pub commit_hash: String,
    pub file_tree: Vec<FileTreeNode>,
    pub modified_files: Vec<String>,
    pub summary: String,
}

#[derive(Debug, Serialize, schemars::JsonSchema)]
pub struct FileTreeNode {
    pub path: String,
    pub file_type: String, // "file", "directory"
    pub size: Option<u64>,
    pub children: Option<Vec<FileTreeNode>>,
}
```

#### 2.3 `search_agent_code`
Search across all agent workspaces for code patterns.

```rust
#[derive(Debug, Deserialize, schemars::JsonSchema)]
pub struct SearchAgentCodeRequest {
    #[schemars(description = "Search query (regex supported)")]
    pub query: String,
    #[schemars(description = "File pattern filter")]
    pub file_pattern: Option<String>,
    #[schemars(description = "Search type: 'content', 'filename', 'both'")]
    pub search_type: Option<String>,
}

#[derive(Debug, Serialize, schemars::JsonSchema)]
pub struct CodeMatch {
    pub workspace_id: Uuid,
    pub task_title: String,
    pub file_path: String,
    pub line_number: Option<u32>,
    pub match_content: String,
    pub context: Option<String>,
}

#[derive(Debug, Serialize, schemars::JsonSchema)]
pub struct SearchAgentCodeResponse {
    pub matches: Vec<CodeMatch>,
    pub count: usize,
}
```

---

### 3. Conversation History Tools

#### 3.1 `get_agent_conversation`
Get conversation logs for an agent session.

```rust
#[derive(Debug, Deserialize, schemars::JsonSchema)]
pub struct GetAgentConversationRequest {
    #[schemars(description = "Workspace ID")]
    pub workspace_id: Uuid,
    #[schemars(description = "Limit number of messages")]
    pub limit: Option<u32>,
    #[schemars(description = "Filter by role: 'user', 'assistant', 'all'")]
    pub role_filter: Option<String>,
}

#[derive(Debug, Serialize, schemars::JsonSchema)]
pub struct ConversationMessage {
    pub role: String,
    pub content: String,
    pub timestamp: String,
    pub tool_calls: Option<Vec<ToolCallInfo>>,
    pub metadata: Option<serde_json::Value>,
}

#[derive(Debug, Serialize, schemars::JsonSchema)]
pub struct ToolCallInfo {
    pub tool_name: String,
    pub arguments: serde_json::Value,
    pub result: Option<String>,
    pub error: Option<String>,
}

#[derive(Debug, Serialize, schemars::JsonSchema)]
pub struct GetAgentConversationResponse {
    pub workspace_id: Uuid,
    pub task_id: Uuid,
    pub messages: Vec<ConversationMessage>,
    pub summary: Option<String>,
    pub total_turns: usize,
}
```

#### 3.2 `get_conversation_summary`
Get a summarized view of agent conversations.

```rust
#[derive(Debug, Deserialize, schemars::JsonSchema)]
pub struct GetConversationSummaryRequest {
    #[schemars(description = "Project ID")]
    pub project_id: Uuid,
}

#[derive(Debug, Serialize, schemars::JsonSchema)]
pub struct AgentConversationSummary {
    pub workspace_id: Uuid,
    pub task_title: String,
    pub agent_type: String,
    pub started_at: String,
    pub status: String,
    pub message_count: usize,
    pub tool_call_count: usize,
    pub topics: Vec<String>,
    pub summary: String,
}

#[derive(Debug, Serialize, schemars::JsonSchema)]
pub struct GetConversationSummaryResponse {
    pub agents: Vec<AgentConversationSummary>,
    pub total_messages: usize,
}
```

#### 3.3 `get_thinking_process`
Get the thinking/reasoning process of an agent.

```rust
#[derive(Debug, Deserialize, schemars::JsonSchema)]
pub struct GetThinkingProcessRequest {
    #[schemars(description = "Workspace ID")]
    pub workspace_id: Uuid,
}

#[derive(Debug, Serialize, schemars::JsonSchema)]
pub struct ThinkingStep {
    pub step_number: u32,
    pub thought: String,
    pub next_action: Option<String>,
    pub timestamp: String,
    pub confidence: Option<f32>,
}

#[derive(Debug, Serialize, schemars::JsonSchema)]
pub struct GetThinkingProcessResponse {
    pub workspace_id: Uuid,
    pub current_step: Option<ThinkingStep>,
    pub completed_steps: Vec<ThinkingStep>,
    pub total_steps: usize,
    pub estimated_completion: Option<String>,
}
```

---

### 4. Mid-Conversation Intervention Tools

#### 4.1 `interrupt_agent`
Send an interrupt signal to an active agent.

```rust
#[derive(Debug, Deserialize, schemars::JsonSchema)]
pub struct InterruptAgentRequest {
    #[schemars(description = "Workspace ID")]
    pub workspace_id: Uuid,
    #[schemars(description = "Reason for interruption")]
    pub reason: String,
    #[schemars(description = "Wait for agent to acknowledge")]
    pub wait_for_ack: Option<bool>,
}

#[derive(Debug, Serialize, schemars::JsonSchema)]
pub struct InterruptAgentResponse {
    pub success: bool,
    pub agent_status: String,
    pub interrupt_id: String,
}
```

#### 4.2 `inject_instruction`
Inject a new instruction into an agent's context.

```rust
#[derive(Debug, Deserialize, schemars::JsonSchema)]
pub struct InjectInstructionRequest {
    #[schemars(description = "Workspace ID")]
    pub workspace_id: Uuid,
    #[schemars(description = "Instruction to inject")]
    pub instruction: String,
    #[schemars(description = "Priority level")]
    pub priority: Option<String>, // "context", "override", "critical"
}

#[derive(Debug, Serialize, schemars::JsonSchema)]
pub struct InjectInstructionResponse {
    pub success: bool,
    pub instruction_id: String,
    pub agent_acknowledged: bool,
}
```

#### 4.3 `pause_resume_agent`
Pause or resume an agent session.

```rust
#[derive(Debug, Deserialize, schemars::JsonSchema)]
pub struct PauseResumeAgentRequest {
    #[schemars(description = "Workspace ID")]
    pub workspace_id: Uuid,
    #[schemars(description = "Action: 'pause' or 'resume'")]
    pub action: String,
    #[schemars(description = "Reason for state change")]
    pub reason: Option<String>,
}

#[derive(Debug, Serialize, schemars::JsonSchema)]
pub struct PauseResumeAgentResponse {
    pub success: bool,
    pub previous_state: String,
    pub new_state: String,
}
```

#### 4.4 `redirect_agent`
Redirect an agent to a different task or approach.

```rust
#[derive(Debug, Deserialize, schemars::JsonSchema)]
pub struct RedirectAgentRequest {
    #[schemars(description = "Workspace ID")]
    pub workspace_id: Uuid,
    #[schemars(description = "New task ID (optional)")]
    pub new_task_id: Option<Uuid>,
    #[schemars(description = "New approach instructions")]
    pub new_approach: String,
    #[schemars(description = "Preserve current context")]
    pub preserve_context: Option<bool>,
}

#[derive(Debug, Serialize, schemars::JsonSchema)]
pub struct RedirectAgentResponse {
    pub success: bool,
    pub redirect_id: String,
    pub context_preserved: bool,
}
```

---

### 5. Enhanced Monitoring Tools

#### 5.1 `get_agent_metrics`
Get detailed metrics for an agent session.

```rust
#[derive(Debug, Deserialize, schemars::JsonSchema)]
pub struct GetAgentMetricsRequest {
    #[schemars(description = "Workspace ID")]
    pub workspace_id: Uuid,
}

#[derive(Debug, Serialize, schemars::JsonSchema)]
pub struct AgentMetrics {
    pub workspace_id: Uuid,
    pub task_id: Uuid,

    // Time metrics
    pub started_at: String,
    pub duration_seconds: u64,
    pub active_time_seconds: u64,
    pub idle_time_seconds: u64,

    // Activity metrics
    pub messages_exchanged: u32,
    pub tools_called: u32,
    pub files_read: u32,
    pub files_modified: u32,
    pub files_created: u32,

    // Performance metrics
    pub average_response_time_ms: Option<f64>,
    pub token_usage: TokenUsage,
    pub error_count: u32,

    // Progress metrics
    pub completion_percentage: u8,
    pub current_step: Option<String>,
    pub estimated_remaining_seconds: Option<u64>,
}

#[derive(Debug, Serialize, schemars::JsonSchema)]
pub struct TokenUsage {
    pub input_tokens: u32,
    pub output_tokens: u32,
    pub total_tokens: u32,
}
```

#### 5.2 `stream_agent_events`
Subscribe to real-time events from an agent session.

```rust
#[derive(Debug, Deserialize, schemars::JsonSchema)]
pub struct StreamAgentEventsRequest {
    #[schemars(description = "Workspace ID")]
    pub workspace_id: Uuid,
    #[schemars(description = "Event types to stream")]
    pub event_types: Option<Vec<String>>, // "message", "tool_call", "file_change", "error"
}

// This would be a streaming/SSE endpoint rather than a simple RPC
```

---

## Implementation Architecture

### Backend Components Required

1. **Message Broker/Queue**
   - For agent-to-agent messaging
   - Could use Redis, RabbitMQ, or in-memory channels
   - Handles message delivery and persistence

2. **Session Manager**
   - Tracks all active agent sessions
   - Maintains agent state and metadata
   - Handles session lifecycle events

3. **Event Store**
   - Stores conversation history
   - Tracks tool calls and file operations
   - Enables querying and analysis

4. **Intervention Handler**
   - Processes interrupt/inject requests
   - Manages instruction injection
   - Handles pause/resume state transitions

5. **Code Context Service**
   - Tracks file access patterns
   - Maintains workspace snapshots
   - Provides search capabilities

### Data Model Extensions

New database tables/collections needed:

```sql
-- Agent sessions table (extends existing workspaces)
CREATE TABLE agent_sessions (
    id UUID PRIMARY KEY,
    workspace_id UUID REFERENCES workspaces(id),
    task_id UUID REFERENCES tasks(id),
    agent_type VARCHAR(100),
    status VARCHAR(50), -- active, paused, completed, failed, interrupted
    started_at TIMESTAMPTZ,
    last_activity TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    metadata JSONB
);

-- Agent messages table
CREATE TABLE agent_messages (
    id UUID PRIMARY KEY,
    from_session_id UUID REFERENCES agent_sessions(id),
    to_session_id UUID REFERENCES agent_sessions(id),
    message TEXT,
    priority VARCHAR(20), -- info, warning, critical
    status VARCHAR(50), -- pending, delivered, read
    created_at TIMESTAMPTZ,
    delivered_at TIMESTAMPTZ
);

-- Conversation events table
CREATE TABLE conversation_events (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES agent_sessions(id),
    event_type VARCHAR(50), -- message, tool_call, file_change, error, thinking
    event_data JSONB,
    timestamp TIMESTAMPTZ
);

-- File access tracking
CREATE TABLE agent_file_access (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES agent_sessions(id),
    file_path TEXT,
    action VARCHAR(50), -- read, write, create, delete
    timestamp TIMESTAMPTZ,
    content_preview TEXT
);

-- Interventions table
CREATE TABLE agent_interventions (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES agent_sessions(id),
    intervention_type VARCHAR(50), -- interrupt, inject, pause, redirect
    reason TEXT,
    instruction TEXT,
    status VARCHAR(50), -- pending, acknowledged, completed, failed
    created_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ
);
```

---

## Integration Points

### 1. Vibe Kanban Server
- Add new API endpoints under `/api/agent-sessions/`
- Extend existing task attempts API
- WebSocket/SSE support for real-time updates

### 2. Managerial Agent Skills
- New `AgentCommunicator` class in `vibe_kanban_manager.py`
- Enhanced `TeamDashboard` with intervention controls
- New `AgentIntervention` skill module

### 3. Executor Integrations
- Hook into agent session lifecycle
- Capture conversation events
- Support for message reception and display
- Implement interrupt handling

---

## Usage Examples

### Example 1: Manager Checking Agent Progress
```python
# Manager agent wants to check on a specialist agent
manager = VibeKanbanManager()

# List active agents
agents = manager.list_active_agents()
for agent in agents:
    print(f"Agent {agent['task_title']}: {agent['status']}")

# Get conversation summary
summary = mcp.get_conversation_summary(project_id)
for agent in summary['agents']:
    print(f"{agent['task_title']}: {agent['message_count']} messages")
    print(f"  Topics: {', '.join(agent['topics'])}")
```

### Example 2: Manager Intervening in Agent Work
```python
# Agent is going down wrong path
workspace_id = "..."

# Send a warning message
mcp.send_agent_message(
    workspace_id=workspace_id,
    message="WARNING: Please reconsider your approach to X.",
    priority="warning"
)

# Or inject specific instruction
mcp.inject_instruction(
    workspace_id=workspace_id,
    instruction="Stop. Use the Y pattern instead of X.",
    priority="override"
)
```

### Example 3: Coordinating Multiple Agents
```python
# Broadcast to all agents
mcp.broadcast_message(
    message="Deployment window opens in 30 minutes. Please complete current work.",
    priority="info"
)

# Coordinate between specific agents
agent1_workspace = get_agent_workspace(task_id_1)
agent2_workspace = get_agent_workspace(task_id_2)

mcp.send_agent_message(
    workspace_id=agent2_workspace,
    message=f"Agent 1 has completed X. You can now proceed with Y."
)
```

### Example 4: Reviewing Agent Code Changes
```python
# Manager wants to see what an agent has done
workspace_id = "..."

# Get code context
code_ctx = mcp.get_agent_code_context(
    workspace_id=workspace_id,
    include_contents=False
)

print(f"Files touched: {len(code_ctx['files'])}")
for file in code_ctx['files']:
    print(f"  {file['action']}: {file['path']}")

# Get full diff
if code_ctx['diff_summary']:
    print(code_ctx['diff_summary'])
```

---

## Security & Access Control

1. **Message Authentication**
   - All messages signed by sender
   - Verify sender identity before delivery

2. **Authorization**
   - Managerial agents can send to any agent
   - Specialist agents can only message within their project
   - Audit log for all interventions

3. **Rate Limiting**
   - Prevent message flooding
   - Limit intervention frequency

4. **Privacy**
   - Agents can opt-out of conversation history sharing
   - Sensitive data redaction options

---

## Phased Implementation Plan

### Phase 1: Foundation (Week 1-2)
- Database schema additions
- Session tracking infrastructure
- Basic API endpoints for listing sessions

### Phase 2: Messaging (Week 3-4)
- Message broker setup
- `send_agent_message` implementation
- `broadcast_message` implementation
- Message receipt display in agents

### Phase 3: Visibility (Week 5-6)
- File access tracking
- `get_agent_code_context` implementation
- `search_agent_code` implementation
- Codebase snapshot functionality

### Phase 4: Conversation History (Week 7-8)
- Event capture infrastructure
- `get_agent_conversation` implementation
- `get_conversation_summary` implementation
- `get_thinking_process` implementation

### Phase 5: Intervention (Week 9-10)
- Intervention handler setup
- `interrupt_agent` implementation
- `inject_instruction` implementation
- `pause_resume_agent` implementation
- `redirect_agent` implementation

### Phase 6: Monitoring & Streaming (Week 11-12)
- Metrics collection
- `get_agent_metrics` implementation
- `stream_agent_events` implementation
- Dashboard enhancements

---

## Success Metrics

1. **Adoption**
   - % of agents using new messaging features
   - Message volume per day

2. **Effectiveness**
   - Reduction in agent coordination time
   - Improvement in task completion rates
   - Reduction in failed/blocked tasks

3. **Managerial Efficiency**
   - Time spent monitoring agents
   - Intervention success rate
   - Code review efficiency

4. **System Performance**
   - Message delivery latency
   - Query response times
   - Resource utilization

---

## Open Questions

1. **Message Persistence**
   - How long to store messages?
   - Archive strategy for completed sessions?

2. **Real-time Requirements**
   - WebSocket vs SSE for streaming?
   - Message delivery guarantees?

3. **Cross-Project Communication**
   - Should agents be able to communicate across projects?
   - How to handle access control?

4. **Agent Autonomy**
   - How much should agents be required to respond to managers?
   - Can agents decline interventions?

5. **Scalability**
   - Maximum concurrent agent sessions?
   - Message throughput targets?

---

## References

- Vibe Kanban MCP Server: `3-gui/vibe-kanban/crates/server/src/mcp/task_server.rs`
- Managerial Agent Skills: `2-engine/01-core/agents/managerial/skills/`
- Team Dashboard: `2-engine/01-core/agents/managerial/skills/team_dashboard.py`
- Existing MCP Configuration: `2-engine/.config/mcp-servers.json`
