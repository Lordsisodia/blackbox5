# Blackbox5 Core Components

**Version:** 5.0.0
**Last Updated:** 2026-01-20
**Status:** Production Ready

---

## Overview

Blackbox5 is a multi-agent AI orchestration system with 12+ specialized agents, a 4-layer memory system, event-driven architecture, and intelligent task routing. This document catalogs the most important core components of the Blackbox.

---

## Architecture Principle: Engine vs. Memory Separation

**Critical Design Decision:** The engine and project memory are **separate and interchangeable**.

### Why This Separation Exists:

1. **Engine = Universal Framework** - The engine (`2-engine/`) works across ALL projects. It contains the fundamental orchestration logic, agent definitions, skills, and integrations. This code never changes based on which project it's running.

2. **Memory = Backend Integration** - Project memory (`5-project-memory/`) is a backend data store that connects TO the engine. Each project has its own memory with project-specific context, code understanding, and historical data. The information varies project-by-project, but the structure follows the same template.

### Analogy:

Think of it like a database application:
- **Engine** = The application code (SQL client, ORM, business logic)
- **Memory** = The database itself (PostgreSQL, MySQL - same schema, different data)

Just as you can swap database connections while keeping the same application code, you can swap project memories while keeping the same engine.

### Benefits:

- **Engine Reusability:** One engine serves any number of projects
- **Memory Isolation:** Each project's knowledge stays separate
- **Scalability:** Add new projects without modifying the engine
- **Testing:** Test engine against different memory states
- **Version Control:** Engine and memory evolve independently

---

## Top-Level Directory Structure

```
blackbox5/
├── 01-core/           # Core interface and API definitions
├── 2-engine/          # The autonomous engine (Ralphie) ← UNIVERSAL, UNCHANGING
├── 3-gui/             # Graphical User Interface (web-based)
├── 5-project-memory/  # Project-specific memory storage ← PER-PROJECT, VARIES
├── 6-roadmap/         # Self-improvement roadmap
├── vibe-kanban/       # Vibe Kanban integration
└── 1-docs/            # Comprehensive documentation
```

---

## 1. Autonomous Engine (2-engine/)

**Purpose:** The brain of Blackbox5 - handles all autonomous execution, task routing, and agent coordination.

**Current Implementation:** Ralphie (Rust-based autonomous agent runtime)

### Sub-Components:

#### 01-core/ - Core Behaviors (84 files)
- **client/** - Agent client implementation
- **communication/** - Communication protocols
- **infrastructure/** - Infrastructure components
- **interface/** - User/agent interfaces
  - **api/** - REST API (server.py, main.py)
  - **cli/** - CLI commands (bb5.py, prd_commands.py, epic_commands.py, task_commands.py, github_commands.py)
  - **integrations/** - Integration interfaces
  - **spec_driven/** - Spec-driven agents (prd_agent.py, epic_agent.py, task_agent.py)
- **middleware/** - Token compression, context extraction, guide middleware
- **orchestration/** - Orchestrator logic
- **pipeline/** - Various pipelines (bb5, unified, feature, testing)
- **resilience/** - Circuit breakers, atomic commits, anti-pattern detection
- **routing/** - Task routing
- **state/** - State management
- **tracking/** - Todo management, manifests, deviation handling

#### 02-agents/ - Agent Implementations (460 files - LARGEST)
- **capabilities/** - What agents CAN do (skills)
  - **.skills-new/** - New skills system
  - **skills-cap/** - Skills capabilities
  - **workflows-cap/** - Workflow capabilities
- **implementations/** - Agent implementations
  - **01-core/** - Core agents (manager, orchestrator)
  - **02-bmad/** - BMAD methodology agents
  - **03-research/** - Research agents
  - **04-specialists/** - Specialist agents
  - **05-enhanced/** - Enhanced agents
  - **custom/** - Custom agents
- **legacy-skills/** - Legacy skills (may be deprecated)

#### 03-knowledge/ - Knowledge Systems (160 files)
- **guides/** - Step-by-step instructions
- **memory/** - Short-term memory
- **schemas/** - Data structures
- **semantic/** - Semantic search (placeholder for future use)
- **storage/** - Long-term storage
  - **brain/** - Knowledge storage infrastructure (Docker configs, SQL schemas)
  - **consolidation/** - Memory consolidation
  - **episodic/** - Episodic memory
  - **importance/** - Importance scoring

#### 04-work/ - Work Definitions (161 files)
- **frameworks/** - Framework definitions (BMAD, GSD, etc.)
- **modules/** - Work modules
- **planning/** - Planning system
- **tasks/** - Task management
- **workflows/** - Workflow definitions

#### 05-tools/ - Tool Primitives (25 files)
- **data_tools/** - Data manipulation tools
- **maintenance/** - Maintenance tools
- **migration/** - Migration tools
- **validation/** - Validation tools

#### 06-integrations/ - External Integrations (76 files)
- **github/** - GitHub integration
- **github-actions/** - GitHub Actions integration
- **mcp/** - MCP (Model Context Protocol) integration
- **notion/** - Notion integration
- **obsidian/** - Obsidian integration
- **supabase/** - Supabase integration
- **vercel/** - Vercel integration
- **vibe/** - Vibe Kanban integration
- **cloudflare/** - Cloudflare integration

#### 07-operations/ - Runtime & Scripts (668 files - LARGEST)
- **runtime/** - Runtime scripts and data (141 shell scripts, 122 Python files)
  - **agents/** - Agent management scripts
  - **hooks/** - Git hooks
  - **integration/** - Integration scripts
  - **integrations/** - More integration scripts
- **scripts/** - Utility scripts

#### 08-development/ - Tests & Development (110 files)
- **api/** - API documentation/examples
- **development-tools/** - Development tools, templates, examples, tests
- **examples/** - More examples
- **tests/** - Test suite

---

## 2. Roadmap Module (6-roadmap/)

**Purpose:** Self-improvement area where research and improvements are tracked and executed.

### Structure:

```
6-roadmap/
├── 00-proposed/       # Proposed improvements
├── 01-research/       # Active research
├── 02-design/         # Design phase
├── 02-validation/     # Validation phase
├── 03-planned/        # Planned improvements
├── 04-active/         # Currently active work
├── 05-completed/      # Completed improvements
├── 06-cancelled/      # Cancelled items
├── 07-backlog/        # Backlog items
├── first-principles/  # First principles research
├── frameworks/        # Framework research
├── framework-research/ # Additional framework research
└── templates/         # Templates for new roadmap items
```

### Key Files:
- **EXECUTION-PLAN.md** - Current execution plan
- **INDEX.yaml** - Roadmap index
- **ROADMAP-SUMMARY.md** - Summary of roadmap status
- **VALIDATION-PLAN.md** - Validation procedures
- **RESEARCH-AGENTS-STATUS.md** - Status of research agents

---

## 3. Tasks Module (04-work/ in engine)

**Purpose:** Handles how Blackbox5 plans out tasks and manages the entire pipeline of them being completed and checked.

### Key Components:

#### Planning System
- Task decomposition
- Dependency graph creation
- Wave-based parallelization
- Execution plan generation

#### Task Management
- Task creation and tracking
- Status updates
- Result integration
- Deviation handling

#### Workflow Definitions
- **BMAD** - Business Model Agent Development methodology
- **GSD** - Get Stuff Done methodology
- **Spec-driven** - Specification-driven development
- **Feature pipeline** - Feature development pipeline
- **Testing pipeline** - Testing workflow

---

## 4. Skills Bank (02-agents/capabilities/ in engine)

**Purpose:** A collection of interchangeable skills that agents can use.

### Structure:

```
02-agents/capabilities/
├── .skills-new/        # New skills system
├── skills-cap/         # Skills capabilities
└── workflows-cap/      # Workflow capabilities
```

### Skill Categories:
- **Action skills** - Specific actions (write-tests, deploy, etc.)
- **Workflow skills** - Multi-step workflows
- **Integration skills** - Integration with external systems
- **Testing skills** - Testing and verification
- **Documentation skills** - Documentation generation

**Note:** The integration bank and skills are effectively the same thing - both provide capabilities that agents can use. Integrations are essentially skills that connect to external systems.

---

## 5. Integration Bank (06-integrations/ in engine)

**Purpose:** Different integrations with external systems that Blackbox5 can connect to.

### Available Integrations:

- **GitHub** - Issue/PR management, repository operations
- **GitHub Actions** - CI/CD pipeline integration
- **MCP** - Model Context Protocol (external tools)
- **Notion** - Documentation and knowledge base
- **Obsidian** - Note-taking system
- **Supabase** - Backend as a service
- **Vercel** - Deployment platform
- **Cloudflare** - CDN and DNS services
- **Vibe Kanban** - Project management (also has own folder)

**Note:** As mentioned in #4, integrations and skills are closely related. Integrations are essentially skills with external system connections.

---

## 6. Graphical User Interface (3-gui/)

**Purpose:** Web-based GUI for interacting with Blackbox5.

### Technology Stack:
- **Framework:** Vite + TypeScript
- **Styling:** Tailwind CSS
- **Package Manager:** npm

### Structure:

```
3-gui/
├── public/             # Static assets
├── src/                # Source code
├── research/           # Research and design
├── node_modules/       # Dependencies
├── index.html          # Entry point
├── package.json        # Dependencies and scripts
├── vite.config.ts      # Vite configuration
├── tailwind.config.js  # Tailwind configuration
└── tsconfig.json       # TypeScript configuration
```

---

## 7. Memory Systems (03-knowledge/ + 5-project-memory/)

**Purpose:** 4-layer memory system for storing and retrieving information.

### Memory Layers:

1. **Working Memory** (03-knowledge/memory/)
   - Session context
   - Short-term storage
   - Limited to ~100K tokens

2. **Episodic Memory** (03-knowledge/storage/episodic/)
   - ChromaDB vector storage
   - Similarity-based retrieval
   - Episode storage

3. **Semantic Memory** (03-knowledge/storage/brain/)
   - Neo4j knowledge graph
   - Concept relationships
   - Graph-based queries

4. **Procedural Memory** (03-knowledge/storage/)
   - Redis-based pattern storage
   - Skill patterns
   - Best practices

### Project Memory (5-project-memory/) ← PER-PROJECT BACKEND

**IMPORTANT:** This is separate from the engine's memory systems and follows a different architecture principle.

```
5-project-memory/
├── siso-internal/    # SISO Internal project memory (project-specific data)
├── _template/        # Template for new project memories
├── INDEX.yaml        # Memory index
└── code_index.md     # Code index
```

#### Key Distinction:

| Aspect | Engine Memory (03-knowledge/) | Project Memory (5-project-memory/) |
|--------|-------------------------------|------------------------------------|
| **Location** | `2-engine/03-knowledge/` | `5-project-memory/` |
| **Scope** | Universal - works for any project | Project-specific - unique per project |
| **Purpose** | Memory STORAGE INFRASTRUCTURE | Memory CONTENT/DATA |
| **Changes** | Never changes per project | Varies project-by-project |
| **Analogy** | Database client library | Database instance with data |

#### What This Means:

The engine's `03-knowledge/` folder contains the **code and infrastructure** for storing and retrieving memories (ChromaDB setup, Neo4j schemas, consolidation algorithms, etc.). This code is universal.

The `5-project-memory/` folder contains the **actual data** for a specific project (code indexes, project context, historical decisions, etc.). This data is project-specific.

When you create a new project, you:
1. Copy the `_template/` folder structure
2. Populate it with project-specific information
3. Connect the same engine to this new memory

---

## 8. Event Bus (01-core/communication/ in engine)

**Purpose:** Redis-based event communication system for component coordination.

### Features:
- Pub/sub messaging
- Event validation
- JSON serialization
- Multiple subscribers
- External integration sync

---

## 9. Core Infrastructure Components

### Task Router (01-core/routing/)
**Purpose:** Intelligent complexity-based task routing

- Analyzes task complexity
- Routes to single or multi-agent
- Estimates duration and confidence

### Orchestrator (01-core/orchestration/)
**Purpose:** Wave-based parallelization for multi-agent coordination

- Task decomposition
- Wave execution
- Result integration
- Progress monitoring

### Circuit Breaker (01-core/resilience/)
**Purpose:** Fault tolerance and error recovery

- Failure threshold detection
- Automatic recovery
- Timeout handling
- Anti-pattern detection

### State Manager (01-core/state/)
**Purpose:** System state management

- State persistence
- State transitions
- Checkpoint management
- Atomic commits

### Manifest System (01-core/tracking/)
**Purpose:** Operation tracking and manifests

- Operation logging
- Step tracking
- Result storage
- Historical records

---

## 10. Agent Types

### Core Agents
- **Manager** - Coordinates multi-agent workflows
- **Orchestrator** - Wave-based execution
- **Task Router** - Intelligent routing

### BMAD Agents
- **Mary** - Product Manager
- **Winston** - Architect
- **Arthur** - Developer
- **John** - Tech Writer/Reviewer
- **TEA** - Test Engineer Agent

### Specialist Agents
- Research agents
- Code agents
- Writing agents
- Testing agents
- Enhanced agents

---

## 11. CLI Tools (01-core/interface/cli/)

**Purpose:** Command-line interface for interacting with Blackbox5.

### Commands:
- `bb5 ask` - Ask questions or give tasks
- `bb5 agents` - List available agents
- `bb5 inspect` - Inspect agent capabilities
- `bb5 skills` - List available skills
- `bb5 guide` - Find guides for tasks
- `bb5 prd` - PRD commands
- `bb5 epic` - Epic commands
- `bb5 task` - Task commands
- `bb5 github` - GitHub commands

---

## 12. REST API (01-core/interface/api/)

**Purpose:** RESTful API for programmatic access to Blackbox5.

### Endpoints:
- `POST /chat` - Process chat messages
- `GET /agents` - List all agents
- `GET /agents/{agent_name}` - Get agent details
- `GET /skills` - List all skills
- `GET /guides/search` - Search for guides
- `GET /guides/intent` - Find guides by intent
- `GET /health` - Health check

---

## Summary of Core Components

### Universal Components (Engine - Never Change Per Project)

| # | Component | Location | Purpose |
|---|-----------|----------|---------|
| 1 | Autonomous Engine | 2-engine/ | The brain (Ralphie) - UNIVERSAL framework |
| 2 | Roadmap | 6-roadmap/ | Self-improvement |
| 3 | Tasks | 2-engine/04-work/ | Task planning and execution |
| 4 | Skills Bank | 2-engine/02-agents/capabilities/ | Reusable skills |
| 5 | Integration Bank | 2-engine/06-integrations/ | External integrations |
| 6 | GUI | 3-gui/ | Web interface |
| 7 | Memory Infrastructure | 2-engine/03-knowledge/ | Memory STORAGE CODE (ChromaDB, Neo4j, etc.) |
| 8 | Event Bus | 2-engine/01-core/communication/ | Event communication |
| 9 | Task Router | 2-engine/01-core/routing/ | Intelligent routing |
| 10 | Orchestrator | 2-engine/01-core/orchestration/ | Multi-agent coordination |
| 11 | Circuit Breaker | 2-engine/01-core/resilience/ | Fault tolerance |
| 12 | State Manager | 2-engine/01-core/state/ | State management |
| 13 | Manifest System | 2-engine/01-core/tracking/ | Operation tracking |
| 14 | CLI Tools | 2-engine/01-core/interface/cli/ | Command-line interface |
| 15 | REST API | 2-engine/01-core/interface/api/ | Programmatic access |

### Per-Project Components (Memory - Varies Per Project)

| # | Component | Location | Purpose |
|---|-----------|----------|---------|
| 16 | Project Memory | 5-project-memory/ | Memory CONTENT/DATA (project-specific) |

### Key Architectural Split:

```
┌─────────────────────────────────────────────────────────────────┐
│                    UNIVERSAL ENGINE                             │
│                    (2-engine/)                                  │
│                                                                 │
│  • Agents, Skills, Integrations                                 │
│  • Task Routing, Orchestration                                  │
│  • Memory STORAGE CODE (03-knowledge/)                          │
│  • CLI, API, GUI                                                │
│                                                                 │
│  ← This code works for ANY project, never changes               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ connects to
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  PROJECT MEMORY                                 │
│                  (5-project-memory/)                            │
│                                                                 │
│  • Project-specific context                                     │
│  • Code indexes                                                 │
│  • Historical data                                              │
│  • Project knowledge                                            │
│                                                                 │
│  ← Unique per project, varies based on project                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Notes on Your Original List

1. **Autonomous engine (Ralphie)** ✅ - `2-engine/` - Correct
   - **Universal framework** that works across all projects
   - Contains agents, skills, integrations, orchestration, and memory infrastructure

2. **Roadmap** ✅ - `6-roadmap/` - Correct
   - Self-improvement system for Blackbox5 itself

3. **Tasks module** ✅ - `2-engine/04-work/` - Correct
   - Task planning, execution, and workflow definitions

4. **Skills bank** ✅ - `2-engine/02-agents/capabilities/` - Correct
   - Reusable skills that agents can use

5. **Integration bank** ✅ - `2-engine/06-integrations/` - Correct
   - **Note:** You're right that integration bank and skills are closely related. Both provide capabilities that agents can use. Integrations are essentially skills with external system connections.

6. **GUI module** ✅ - `3-gui/` - Correct
   - Web-based interface

7. **Memory Systems** ✅ - Two locations, different purposes:
   - **`2-engine/03-knowledge/`** - Memory STORAGE INFRASTRUCTURE (code)
   - **`5-project-memory/`** - Memory CONTENT/DATA (project-specific)
   - **Critical distinction:** Engine provides universal memory code, project memory provides project-specific data

---

**Status:** Production Ready
**Version:** 5.0.0
**Last Updated:** 2026-01-20
**Maintainer:** Blackbox5 Core Team
