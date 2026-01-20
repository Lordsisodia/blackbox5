# BLACKBOX5 🚀

> **Universal Multi-Agent Orchestration System**

## 🔍 **START HERE:** [CATALOG.md](CATALOG.md) - The master index of everything in BLACKBOX5

---

### Quick Start

```bash
# Start everything
./start.sh

# Or use Python
python3 blackbox.py start
python3 blackbox.py status
python3 blackbox.py agents
```

### 📚 Essential Reading

| Document | What It Is |
|----------|-------------|
| **[CATALOG.md](CATALOG.md)** | **🔍 UNIVERSAL INDEX - Every agent, tool, integration** |
| [QUICK-START.md](QUICK-START.md) | Quick start guide with examples |
| [CORE-COMPONENTS.md](CORE-COMPONENTS.md) | Detailed documentation |

---

## What BLACKBOX5 Is

BLACKBOX5 is **not an AI agent itself**. It's the **infrastructure** that AI agents use to:
- Access tools and capabilities
- Manage tasks through Vibe Kanban
- Use MCP integrations
- Run autonomous operations

Think of it as: **AI agents are the brain, BLACKBOX5 is the hands and tools.**

---

## Core Components (All Functional)

### ✅ Agent Core System
| Component | Purpose | Status |
|-----------|---------|--------|
| **AgentLoader** | Discovers and loads agents dynamically | ✅ Working |
| **TaskRouter** | Routes tasks to appropriate agents | ✅ Working |
| **Orchestrator** | Multi-agent workflow coordination | ✅ Working |
| **EventBus** | In-memory event system | ✅ Working |
| **Safety Systems** | KillSwitch, SafeMode, Constitutional AI | ✅ Working |
| **REST API** | FastAPI server at `localhost:8000` | ✅ Working |

### ✅ Three Core Agents (Template-Based)
| Agent | Role | Output |
|-------|------|--------|
| **ArchitectAgent** (Alex) | System architecture, design patterns | Architecture templates |
| **AnalystAgent** (Mary) | Research, analysis, documentation | Report templates |
| **DeveloperAgent** (Amelia) | Coding, debugging, testing | Code templates |

> **Note:** These return pre-written templates. The real AI comes from external agents (Claude Code, etc.) using this infrastructure.

---

## MCP Integrations (Configured & Ready)

BLACKBOX5 provides these MCP servers for AI agents to use:

| MCP Server | Purpose | Tools Available |
|------------|---------|-----------------|
| **vibe_kanban** | Project & task management | `list_projects`, `create_task`, `update_task`, `start_workspace_session`, `list_repos` |
| **supabase** | Database operations | DB queries, migrations, edge functions, auth, storage |
| **filesystem** | File operations | Read, write, search, watch files |
| **playwright** | Browser automation | Navigate, click, screenshot, test |
| **sequential-thinking** | Chain-of-thought reasoning | Structured reasoning steps |
| **fetch** | HTTP requests | Web fetching, API calls |

**Configuration:** `2-engine/.config/mcp-servers.json`

---

## How AI Agents Use BLACKBOX5

### Workflow Example (Claude Code working through BLACKBOX5):

```
1. Claude Code receives a task
         ↓
2. Uses Vibe Kanban MCP to create/task track work
         ↓
3. Uses Filesystem MCP to read/write code
         ↓
4. Uses Supabase MCP for database operations
         ↓
5. Uses Playwright MCP for browser testing
         ↓
6. Updates Vibe Kanban task status
         ↓
7. Task complete
```

### Available to AI Agents Right Now:

**Via MCP Tools:**
- Create and manage tasks in Vibe Kanban
- Start workspace sessions with different executors (claude-code, amp, gemini, codex, etc.)
- Read/write files anywhere in the project
- Run Supabase migrations and queries
- Automate browser interactions
- Perform structured reasoning
- Make HTTP requests and fetch web content

**Via BLACKBOX5 API:**
```bash
# Start the API server
cd 2-engine/01-core
python3 -m interface.api.main

# Available at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

---

## Quick Start

### 1. Start the API Server
```bash
cd 2-engine/01-core
python3 -m interface.api.main
```

### 2. Test Core Functionality
```bash
# Health check
curl http://localhost:8000/health

# Chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What can you do?"}'

# List agents
curl http://localhost:8000/agents

# System stats
curl http://localhost:8000/stats
```

### 3. Access Vibe Kanban
```bash
cd 3-gui/vibe-kanban
pnpm run dev
# GUI at http://localhost:3000
```

---

## Vibe Kanban Integration

**Vibe Kanban is the task outsourcing system** - AI agents use it to:

1. **Create tasks** for themselves or other agents
2. **Track progress** across autonomous operations
3. **Start workspace sessions** with specific executors
4. **Manage repositories** and their setup/cleanup/dev scripts

### MCP Tools Available:

```python
# List all projects
mcp__vibe_kanban__list_projects()

# Create a new task (requires project_id)
mcp__vibe_kanban__create_task(
    project_id="uuid",
    title="Task name",
    description="Optional description"
)

# Start working on a task
mcp__vibe_kanban__start_workspace_session(
    task_id="uuid",
    executor="CLAUDE_CODE",  # or AMP, GEMINI, CODEX, etc.
    repos=[{"repo_id": "uuid", "base_branch": "main"}]
)

# List tasks in a project
mcp__vibe_kanban__list_tasks(
    project_id="uuid",
    status="inprogress",  # or todo, inreview, done, cancelled
    limit=50
)

# Update task status
mcp__vibe_kanban__update_task(
    task_id="uuid",
    status="inprogress",
    title="New title",
    description="New description"
)
```

---

## Skills & Capabilities

**Location:** `2-engine/02-agents/capabilities/`

The infrastructure provides a skills registry system (currently being consolidated):

- **Core Infrastructure** (2 skills): GitHub CLI, Git worktrees
- **Integration & Connectivity** (6 skills): REST API, GraphQL, SQL, ORM
- **Development Workflow** (13 skills): Testing, Docker, CI/CD, refactoring
- **Knowledge & Documentation** (5 skills): API docs, README generation
- **Collaboration & Communication** (10 skills): Automation, research

**Status:** 36/70 skills implemented (51%), 3 competing systems being consolidated.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│              AI Agent (Claude Code, etc.)           │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                    BLACKBOX5                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │ Task Router │─▶│ Orchestrator │─▶│  Agents   │ │
│  └─────────────┘  └──────────────┘  └───────────┘ │
│         │                  │              │         │
│         ▼                  ▼              ▼         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │   Safety    │  │  Event Bus   │  │   Skills  │ │
│  │  Systems    │  │              │  │ Registry  │ │
│  └─────────────┘  └──────────────┘  └───────────┘ │
│                                                     │
├─────────────────────────────────────────────────────┤
│                    MCP Layer                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌─────────┐ │
│  │ Vibe │ │ Supa │ │ File │ │ Play │ │  Fetch  │ │
│  │ Kan  │ │ base │ │ sys  │ │ wright│ │         │ │
│  └──────┘ └──────┘ └──────┘ └──────┘ └─────────┘ │
│                                                     │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   External World    │
              │ (Files, DBs, Web,   │
              │  Projects, etc.)    │
              └─────────────────────┘
```

---

## What Makes BLACKBOX5 Different

### 1. **AI-Agnostic Design**
- Works with any AI agent (Claude Code, AMP, Gemini, Codex, etc.)
- Swappable LLM backend via GLMClient
- No vendor lock-in

### 2. **Self-Improving**
- Autonomous agents continuously improve the system
- Runtime agents work 24/7 on enhancement tasks
- Vibe Kanban tracks all improvement work

### 3. **Safety-First**
- Built-in KillSwitch for emergency stops
- SafeMode for restricted operations
- Constitutional AI for value alignment

### 4. **Modular & Extensible**
- Universal core engine (unchanging)
- Capabilities layer (evolving)
- Skills registry (growing)

---

## Current Status

| Component | Status |
|-----------|--------|
| Core Infrastructure | ✅ 100% Functional |
| 3 Base Agents | ✅ Working (template-based) |
| REST API | ✅ Working at localhost:8000 |
| MCP Integration | ✅ Configured, 5 servers ready |
| Vibe Kanban | ✅ GUI at localhost:3000 |
| Skills System | ⚠️ 51% complete, consolidating |
| Specialist Agents | ⏳ 18 agents being added autonomously |

---

## Getting Started

### For AI Agents Using MCP:
The MCP tools are already available. Just use them:
- `mcp__vibe_kanban__list_projects()`
- `mcp__filesystem__read_text_file()`
- `mcp__supabase__execute_sql()`
- etc.

### For Direct API Access:
```bash
cd 2-engine/01-core
python3 -m interface.api.main
```

### For Vibe Kanban GUI:
```bash
cd 3-gui/vibe-kanban
pnpm run dev
```

---

## File Structure

```
blackbox5/
├── 2-engine/                    # Core engine (UNIVERSAL)
│   ├── 01-core/
│   │   ├── agents/              # Agent implementations
│   │   ├── routing/             # Task routing
│   │   ├── safety/              # Safety systems
│   │   ├── client/              # GLMClient (LLM integration)
│   │   └── interface/api/       # REST API
│   ├── 02-agents/
│   │   └── capabilities/        # Skills & tools
│   ├── .config/
│   │   └── mcp-servers.json     # MCP configuration
│   └── 07-operations/           # Runtime & autonomy
│
├── 3-gui/
│   └── vibe-kanban/             # Vibe Kanban GUI
│
├── 5-project-memory/            # Project-specific data
└── 6-roadmap/                   # Self-improvement plans
```

---

## Summary

**BLACKBOX5 = AI Agent Infrastructure**

- ✅ Not an AI itself - it's the tools AI agents use
- ✅ Provides task management via Vibe Kanban MCP
- ✅ Provides 5+ MCP integrations (filesystem, database, browser, etc.)
- ✅ Self-improving via autonomous agents
- ✅ Safety-first design with kill switches
- ✅ Works with any AI agent (Claude Code, AMP, Gemini, etc.)

**The point:** AI agents (like me) use BLACKBOX5's infrastructure to get work done through tools and task management.
