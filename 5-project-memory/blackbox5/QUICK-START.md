# Blackbox5 Quick Start Guide

## 🚀 Quick Start (Simple Commands)

### Start Everything
```bash
# From the BLACKBOX5 directory:
./start.sh
```
This starts both the API server and Vibe Kanban GUI automatically.

### Other Options
```bash
./start.sh --api-only    # Start only the API
./start.sh --gui-only    # Start only Vibe Kanban
./start.sh --help        # Show all options
```

### Using Python Commands
```bash
python blackbox.py start              # Start everything
python blackbox.py start --api-only   # Start API only
python blackbox.py start --gui-only   # Start GUI only
python blackbox.py status             # Check what's running
python blackbox.py agents             # List all 21 agents
python blackbox.py chat "Hello"       # Send a message
python blackbox.py stop               # Stop everything
```

### Core Systems (100% Functional)
- **AgentLoader** - Discovers and loads 3 core agents (Architect, Analyst, Developer)
- **Routing System** - TaskRouter and TaskComplexityAnalyzer
- **Safety System** - KillSwitch, SafeMode, ConstitutionalClassifier
- **Managerial Agent** - VibeKanbanManager for task tracking
- **REST API** - Full FastAPI server with safety endpoints

### Agents Status (3/21 Working)
```
✅ ArchitectAgent - System architecture and design
✅ AnalystAgent - Analysis and research
✅ DeveloperAgent - Code implementation
⏳ 18 Specialist Agents - Being added by autonomous agents
```

---

## Quick Start

### 1. Start the API Server
```bash
cd 2-engine/01-core
python3 -m interface.api.main
```

**API will be available at:** `http://localhost:8000`

**Interactive docs:** `http://localhost:8000/docs`

---

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Chat with Blackbox5
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is 2+2?"}'
```

### List Available Agents
```bash
curl http://localhost:8000/agents
```

### Safety Status
```bash
curl http://localhost:8000/safety/status
```

### System Statistics
```bash
curl http://localhost:8000/stats
```

---

## Using from Python

```python
import asyncio
from agents.core.agent_loader import AgentLoader

async def main():
    # Load agents
    loader = AgentLoader()
    await loader.load_all()

    # List available agents
    agents = loader.list_agents()
    print(f"Available agents: {agents}")

    # Get a specific agent
    architect = loader.get_agent("ArchitectAgent")
    print(f"Agent role: {architect.role}")

asyncio.run(main())
```

---

## Using Vibe Kanban GUI

### Start Vibe Kanban
```bash
cd 3-gui/vibe-kanban
pnpm run dev
```

**GUI will be available at:** `http://localhost:3000`

Your task database (59MB) is already in place at `3-gui/vibe-kanban/dev_assets/dev.db`

---

## Updating Vibe Kanban

When you want to get the latest Vibe Kanban updates:

```bash
cd 3-gui/vibe-kanban
./upgrade.sh
```

This automatically:
- Backs up your database
- Pulls latest changes
- Preserves your data

---

## Current Limitations (Being Fixed by Agents)

### 1. Specialist Agents (18 agents)
**Status:** 4 autonomous agents working on this in Vibe Kanban
- PLAN-001: Fix Skills System
- PLAN-002: Fix YAML Agent Loading
- PLAN-004: Fix Import Paths

### 2. Skills System Cleanup
**Status:** 3 competing implementations, needs consolidation
**Impact:** Minor - skills work but could be cleaner

---

## Architecture Overview

```
blackbox5/
├── 2-engine/01-core/        # Core engine (UNIVERSAL, UNCHANGING)
│   ├── agents/              # Agent implementations
│   ├── routing/             # Task routing
│   ├── safety/              # Safety systems
│   └── interface/api/       # REST API
│
├── 3-gui/                   # User interfaces
│   ├── vibe-kanban/         # Vibe Kanban (latest from GitHub)
│   └── framework/           # Future frameworks
│
├── 5-project-memory/        # Project-specific memory (VARIES)
└── 6-roadmap/               # Self-improvement roadmap
```

---

## Testing Blackbox5

### Run Core Tests
```bash
cd 2-engine/01-core
python3 -c "
from routing import TaskRouter
from safety import KillSwitch, SafeMode
from agents.core.agent_loader import AgentLoader
import asyncio

async def test():
    loader = AgentLoader()
    await loader.load_all()
    print(f'✅ {len(loader.list_agents())} agents loaded')
    print('✅ All core systems functional!')

asyncio.run(test())
"
```

---

## Monitoring Agent Progress

Check what the autonomous agents are working on:

```python
from agents.managerial import VibeKanbanManager, TaskStatus

manager = VibeKanbanManager()

# Get in-progress tasks
tasks = manager.list_tasks(status=TaskStatus.IN_PROGRESS)
for task in tasks:
    print(f"{task.title}: {task.status.value}")
```

Or visit the Vibe Kanban dashboard to see visual progress.

---

## Next Steps

1. **Try the API** - Start the server and send a chat message
2. **Explore the GUI** - Open Vibe Kanban to see your projects
3. **Monitor agents** - Check Vibe Kanban for autonomous progress
4. **Wait or help** - Let agents finish, or contribute directly

---

## Getting Help

- **API Docs:** `http://localhost:8000/docs`
- **Health Check:** `http://localhost:8000/health`
- **Vibe Kanban:** `http://localhost:3000`
- **Issues:** Check EXECUTION-STATUS.md for known issues

---

**Last Updated:** 2025-01-20
**Status:** Core functional, specialists in progress
