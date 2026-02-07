# BlackBox5 Architecture Analysis: RALF Management Gaps & OpenClaw Integration

**Analysis Date:** 2026-02-07
**Analyst:** Claude Code
**Scope:** RALF autonomous system, agent architecture, MCP integrations, and OpenClaw management layer potential

---

## Executive Summary

BlackBox5's RALF (Recursive Autonomous Loop Framework) is a sophisticated file-based multi-agent system with 10 registered agents organized in a Scout → Analyzer → Planner → Executor pipeline. While architecturally sound for local autonomous operation, it lacks centralized management capabilities that would enable external orchestration via OpenClaw or similar managerial layers.

**Key Finding:** RALF is designed for *local* autonomy, not *distributed* management. Integration with OpenClaw requires bridging this architectural gap.

---

## 1. Current RALF Architecture

### 1.1 Agent Registry Structure

Located at `~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/agent-registry.yaml`:

| Agent | Type | Status | Role |
|-------|------|--------|------|
| scout | bash | active | GitHub repo discovery & extraction |
| analyzer | hybrid | active | Pattern recognition & summarization |
| planner | bash | active | Integration planning & task generation |
| executor | bash | active | Task execution & git operations |
| architect | hybrid | active | System design & decisions |
| communications | yaml | active | Event/queue/heartbeat management |
| execution | yaml | active | 5-slot parallel execution framework |
| metrics | yaml | active | Performance tracking & ROI |
| reanalysis | yaml | active | Task relevance & priority maintenance |
| github-analysis-pipeline | bash | active | 3-agent orchestration (Scout→Analyzer→Planner) |

### 1.2 Communication Protocol

**File-Based Dual-RALF Protocol** (`communications/protocol.yaml`):

```
Planner Agent                    Executor Agent
     |                                |
  Writes →  queue.yaml  ←--------- Reads
  Reads  ←  events.yaml  ←-------- Writes
  Both   ↔  chat-log.yaml  ←→     Both
  Both   ↔  heartbeat.yaml  ←→    Both
```

**Key Characteristics:**
- Loop interval: 30 seconds for both agents
- Queue depth target: 3-5 tasks (max 10)
- Heartbeat timeout: 120 seconds
- Event retention: 100 events
- Chat retention: 50 messages

### 1.3 Task Queue System

**Location:** `communications/queue.yaml`

Current State (90 tasks total):
- Completed: 25
- In Progress: 5
- Pending: 60
- Blocked: 52 (waiting on dependencies)

**Priority Formula:** `(impact / effort) * confidence`
- Impact = `(business_value * 0.4) + (technical_debt * 0.35) + (unblock_factor * 0.25)`
- Resource types: cpu_bound, io_bound, memory_bound, network_bound
- Parallel groups: wave_1 through wave_4 + sequential

### 1.4 Execution Framework

**5-Slot Parallel Execution** (`execution/execution-state.yaml`):

| Slot | Profile | Purpose | Max Duration |
|------|---------|---------|--------------|
| slot_1 | cpu_bound | High-computation tasks | 30m |
| slot_2 | io_bound | File/documentation ops | 20m |
| slot_3 | memory_bound | Data-intensive tasks | 45m |
| slot_4 | network_bound | External communication | 60m |
| slot_5 | reserve | Overflow & critical tasks | unlimited |

---

## 2. Current MCP Server Capabilities

### 2.1 RALF MCP Server (`mcp-server-ralf.py`)

**Tools Available:**
| Tool | Purpose |
|------|---------|
| ralf_get_queue | Read task queue |
| ralf_get_events | Read event log |
| ralf_get_verify | Read verification status |
| ralf_list_tasks | List all tasks |
| ralf_get_task_status | Get specific task status |
| ralf_run_command | Execute arbitrary command |

**Limitations:**
- Read-only for queue/events (no write capability)
- No agent control (start/stop/pause)
- No task injection capability
- No real-time event streaming
- Runs on VPS (`/opt/ralf` base path)

### 2.2 Moltbot MCP Server (`mcp-server-moltbot.py`)

**Tools Available:**
| Tool | Purpose |
|------|---------|
| moltbot_get_status | Gateway process status |
| moltbot_send_message | Telegram messaging |
| moltbot_get_ralf_status | Queue status via SSH |
| moltbot_get_user_context | User context retrieval |
| moltbot_run_command | VPS command execution |

**Connection:** SSH to VPS (77.42.66.40) as root

### 2.3 OpenClaw WebSocket Bridge (`mcp-openclaw-websocket.py`)

**Tools Available:**
| Tool | Purpose |
|------|---------|
| openclaw_send | Send message to Telegram/WhatsApp |
| openclaw_receive | Poll for responses |
| openclaw_conversation | Send and wait for response |
| openclaw_status | Connection status check |

**Connection:** WebSocket to VPS gateway (port 18789)

---

## 3. Management Functions Missing

### 3.1 Agent Lifecycle Management

**Current State:** Agents are bash scripts started manually or via cron
**Missing:**
- [ ] Agent start/stop/restart commands
- [ ] Agent health monitoring with auto-restart
- [ ] Agent resource usage tracking
- [ ] Agent log aggregation
- [ ] Agent version management
- [ ] Agent scaling (beyond 2-agent limit)

### 3.2 Task Orchestration

**Current State:** File-based queue with Planner/Executor coordination
**Missing:**
- [ ] External task injection API
- [ ] Task priority override capability
- [ ] Task cancellation mid-execution
- [ ] Task reassignment between executors
- [ ] Bulk task operations
- [ ] Task dependency visualization

### 3.3 Event System

**Current State:** YAML append-only event log
**Missing:**
- [ ] Real-time event streaming (WebSocket/SSE)
- [ ] Event filtering and routing
- [ ] Event persistence beyond 100 entries
- [ ] Event-driven webhooks
- [ ] Event aggregation and analytics

### 3.4 State Management

**Current State:** STATE.yaml with section-based ownership
**Missing:**
- [ ] Centralized state API
- [ ] State snapshots and rollback
- [ ] State conflict resolution automation
- [ ] Cross-project state aggregation
- [ ] State-based alerting

### 3.5 Monitoring & Observability

**Current State:** Heartbeat YAML with 120s timeout
**Missing:**
- [ ] Real-time metrics dashboard
- [ ] Agent performance metrics
- [ ] Queue depth alerting
- [ ] Execution slot utilization tracking
- [ ] Error rate monitoring
- [ ] Resource consumption tracking

### 3.6 Communication Hub

**Current State:** File-based chat-log.yaml
**Missing:**
- [ ] Real-time messaging (WebSocket)
- [ ] Multi-channel support (beyond Telegram)
- [ ] Message threading and context
- [ ] Human-in-the-loop approval flows
- [ ] Broadcast messaging to all agents

---

## 4. Integration Points for OpenClaw

### 4.1 MCP as Primary Interface

**Current MCP Tools:** Read-heavy, limited write capabilities

**Recommended Additions:**
```yaml
# Agent Managementalf_agent_start(agent_id, config)alf_agent_stop(agent_id, graceful=True)alf_agent_restart(agent_id)alf_agent_status(agent_id)

# Task Managementalf_task_create(task_spec)alf_task_update(task_id, updates)alf_task_cancel(task_id)alf_task_reassign(task_id, target_executor)

# Queue Managementalf_queue_pause()alf_queue_resume()alf_queue_clear()alf_queue_reorder(priority_rules)

# Event Streamingalf_events_stream(since=timestamp, filter=types)alf_events_subscribe(webhook_url, event_types)
```

### 4.2 Webhook Integration Points

**RALF → OpenClaw Webhooks:**
| Event | Payload | Destination |
|-------|---------|-------------|
| task_started | task_id, agent, timestamp | OpenClaw gateway |
| task_completed | task_id, result, commit_hash | OpenClaw gateway |
| task_failed | task_id, error, logs | OpenClaw gateway |
| agent_stopped | agent_id, reason | OpenClaw gateway |
| queue_empty | queue_depth, timestamp | OpenClaw gateway |
| heartbeat_timeout | agent_id, last_seen | OpenClaw gateway |

**OpenClaw → RALF Webhooks:**
| Command | Action | Auth |
|---------|--------|------|
| inject_task | Add task to queue | Token |
| pause_agent | Stop agent gracefully | Token |
| resume_agent | Start agent | Token |
| update_priority | Reorder queue | Token |
| request_status | Full system status | Token |

### 4.3 API Layer Requirements

**REST API Endpoints Needed:**
```
GET  /api/v1/agents              # List all agents
GET  /api/v1/agents/{id}         # Agent details
POST /api/v1/agents/{id}/start   # Start agent
POST /api/v1/agents/{id}/stop    # Stop agent

GET  /api/v1/tasks               # List tasks
POST /api/v1/tasks               # Create task
GET  /api/v1/tasks/{id}          # Task details
PUT  /api/v1/tasks/{id}          # Update task
DELETE /api/v1/tasks/{id}        # Cancel task

GET  /api/v1/queue               # Queue status
POST /api/v1/queue/pause         # Pause processing
POST /api/v1/queue/resume        # Resume processing

GET  /api/v1/events              # Event log
GET  /api/v1/events/stream       # SSE stream

GET  /api/v1/metrics             # System metrics
GET  /api/v1/health              # Health check
```

### 4.4 Database Migration Path

**Current:** YAML files
**Future for OpenClaw Integration:**

```
Phase 1: SQLite (3-5 agents)
- Move queue, events, heartbeat to SQLite
- Add API layer with FastAPI
- Maintain file-based fallback

Phase 2: PostgreSQL (5-10 agents)
- Full relational model
- Real-time subscriptions via LISTEN/NOTIFY
- Historical analytics

Phase 3: Redis + PostgreSQL (10+ agents)
- Redis for real-time pub/sub
- PostgreSQL for persistence
- Horizontal scaling support
```

---

## 5. Event Flow: OpenClaw ↔ RALF

### 5.1 Current Event Flow (File-Based)

```
┌─────────────┐     queue.yaml     ┌─────────────┐
│   Planner   │ ─────────────────→ │   Executor  │
│  (writes)   │                    │   (reads)   │
└─────────────┘                    └─────────────┘
       ↑                                  │
       │         events.yaml              │
       └──────────────────────────────────┘
              (executor writes)
```

### 5.2 Proposed Event Flow (With OpenClaw)

```
┌─────────────────────────────────────────────────────────────┐
│                        OpenClaw Gateway                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Telegram   │  │   WebSocket │  │    Webhook Router   │  │
│  │   Bot       │  │   Server    │  │                     │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
└─────────┼────────────────┼────────────────────┼─────────────┘
          │                │                    │
          ▼                ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                    RALF API Layer                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  REST API   │  │  MCP Server │  │  Event Streaming    │  │
│  │  (FastAPI)  │  │  (stdio)    │  │  (SSE/WebSocket)    │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
└─────────┼────────────────┼────────────────────┼─────────────┘
          │                │                    │
          ▼                ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                    RALF Core System                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Agent     │  │    Task     │  │      Event          │  │
│  │   Manager   │  │    Queue    │  │      Bus            │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 5.3 Event Routing Matrix

| Source Event | OpenClaw Action | RALF Response |
|--------------|-----------------|---------------|
| task_completed | Send Telegram notification | Archive task |
| task_failed | Alert user, ask for guidance | Pause queue |
| queue_empty | Ask user for new tasks | Enter idle mode |
| agent_crashed | Alert user, attempt restart | Log failure |
| heartbeat_timeout | Alert user | Mark agent offline |
| user_command (Telegram) | Parse & route to API | Execute command |
| user_approval_request | Send approval buttons | Wait for response |

---

## 6. Recommended Integration Architecture

### 6.1 Layered Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Layer 4: User Interfaces                                │
│  - Telegram Bot (OpenClaw)                               │
│  - Web Dashboard (future)                                │
│  - Mobile App (future)                                   │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 3: OpenClaw Gateway                               │
│  - Message routing                                       │
│  - User context management                               │
│  - Command parsing                                       │
│  - Response formatting                                   │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 2: RALF API Gateway                               │
│  - REST API (FastAPI)                                    │
│  - MCP Server (stdio)                                    │
│  - Webhook handlers                                      │
│  - Event streaming (SSE)                                 │
│  - Authentication/Authorization                          │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 1: RALF Core                                      │
│  - Agent lifecycle manager                               │
│  - Task queue (SQLite/PostgreSQL)                        │
│  - Event bus (Redis/pub-sub)                             │
│  - Execution engine (5 slots)                            │
│  - State management                                      │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 0: Agents                                         │
│  - Scout, Analyzer, Planner, Executor                    │
│  - Architect, Communications, Execution                  │
│  - Metrics, Reanalysis                                   │
└─────────────────────────────────────────────────────────┘
```

### 6.2 Implementation Phases

**Phase 1: Foundation (Week 1-2)**
- [ ] Create FastAPI-based RALF API server
- [ ] Migrate queue/events from YAML to SQLite
- [ ] Implement agent start/stop endpoints
- [ ] Add basic authentication

**Phase 2: MCP Enhancement (Week 3)**
- [ ] Extend MCP server with write capabilities
- [ ] Add task injection tool
- [ ] Add agent control tools
- [ ] Implement event streaming

**Phase 3: OpenClaw Integration (Week 4)**
- [ ] Create OpenClaw webhook handlers
- [ ] Implement Telegram command parser
- [ ] Add user approval flows
- [ ] Configure event routing

**Phase 4: Monitoring (Week 5)**
- [ ] Real-time metrics dashboard
- [ ] Health check automation
- [ ] Alerting system
- [ ] Performance analytics

### 6.3 Security Considerations

| Layer | Threat | Mitigation |
|-------|--------|------------|
| API | Unauthorized access | Token-based auth, IP whitelist |
| Webhook | Replay attacks | HMAC signatures, timestamps |
| MCP | Command injection | Input validation, sandboxing |
| Agents | Privilege escalation | Run as non-root, capability limits |
| Database | Data corruption | Transactions, backups, validation |

---

## 7. Key Files and Locations

### 7.1 Configuration Files
| File | Purpose |
|------|---------|
| `~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/agent-registry.yaml` | Agent definitions |
| `~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/protocol.yaml` | Communication rules |
| `~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/queue.yaml` | Task queue |
| `~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml` | Event log |
| `~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/communications/heartbeat.yaml` | Agent health |
| `~/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/execution/execution-state.yaml` | Parallel execution state |

### 7.2 MCP Servers
| File | Purpose |
|------|---------|
| `~/.blackbox5/mcp-server-ralf.py` | RALF read-only MCP |
| `~/.blackbox5/mcp-server-moltbot.py` | VPS SSH bridge |
| `~/.blackbox5/mcp-openclaw-websocket.py` | OpenClaw WebSocket |
| `~/.blackbox5/mcp-openclaw-ssh-bridge.py` | OpenClaw SSH bridge |
| `~/.blackbox5/mcp-redis-bridge.py` | Redis pub/sub bridge |

### 7.3 CLI Tools
| File | Purpose |
|------|---------|
| `~/.blackbox5/bin/bb5` | Main navigation CLI |
| `~/.blackbox5/bin/ralf` | RALF launcher |
| `~/.blackbox5/bin/ralf-executor` | Executor agent script |
| `~/.blackbox5/bin/bb5-queue` | Queue management |
| `~/.blackbox5/bin/bb5-status` | Status reporting |

---

## 8. Conclusion

### 8.1 Current Strengths
1. **Well-structured agent registry** with clear capabilities and dependencies
2. **Mature file-based communication protocol** with conflict resolution
3. **Sophisticated execution framework** with 5-slot parallel processing
4. **Comprehensive task queue** with priority scoring and dependency tracking
5. **Existing MCP infrastructure** ready for extension

### 8.2 Critical Gaps for OpenClaw Integration
1. **No external task injection** - Must be able to add tasks from OpenClaw
2. **No real-time event streaming** - OpenClaw needs live updates
3. **No agent control API** - Cannot start/stop agents remotely
4. **File-based limitations** - YAML files don't scale to real-time management
5. **No webhook support** - Cannot receive commands from OpenClaw

### 8.3 Recommended Priority

**Immediate (Week 1):**
- Implement task injection MCP tool
- Add webhook receiver for OpenClaw commands
- Create SQLite-based queue backend

**Short-term (Week 2-3):**
- Build FastAPI REST API layer
- Implement agent lifecycle management
- Add real-time event streaming

**Medium-term (Month 2):**
- Full OpenClaw integration with approval flows
- Monitoring dashboard
- Multi-project support

---

## Appendix A: Agent Capability Matrix

| Capability | Scout | Analyzer | Planner | Executor | Architect | Comm | Exec | Metrics | Reanalysis |
|------------|-------|----------|---------|----------|-----------|------|------|---------|------------|
| GitHub Ops | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Pattern Recognition | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Task Planning | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Code Execution | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| System Design | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Event Management | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ |
| Parallel Execution | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |
| ROI Tracking | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ |
| Task Reanalysis | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |

## Appendix B: Event Type Reference

From `communications/protocol.yaml`:
- `started` - Task execution began
- `progress` - Task progress update
- `completed` - Task finished successfully
- `failed` - Task execution failed
- `blocked` - Task cannot proceed
- `discovery` - New information found
- `idle` - No tasks available

## Appendix C: Scaling Roadmap

From `communications/protocol.yaml`:

| Phase | Agents | Method | Queue | Changes |
|-------|--------|--------|-------|---------|
| Current | 2 | File-based | Single shared | YAML files |
| Future (3-5) | 3-5 | SQLite | Partitioned by type | Move to SQLite, add agent_id |
| Future (10+) | 10+ | Redis | Pub/sub channels | Redis, separate processes, load balancer |
