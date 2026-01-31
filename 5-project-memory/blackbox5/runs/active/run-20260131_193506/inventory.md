# Blackbox5 Codebase Inventory

**Generated:** 2026-01-31 19:40:00
**Run ID:** run-20260131_193506
**Task:** TASK-PLANNING-001-strategic-analysis

---

## Executive Summary

Blackbox5 is a **global AI infrastructure platform** for autonomous software development and multi-agent orchestration. It serves as a meta-system that manages AI agents and coordinates complex development workflows.

### Scale Metrics
- **Python Files:** 381 files
- **Test Files:** 91 files (~24% coverage by file count)
- **Documentation:** 288 README files
- **Core Components:** 6 major directories
- **Agent Types:** 3 core + 18 specialist + managerial

---

## Directory Structure

### Root Organization
```
/workspaces/blackbox5/
├── 1-docs/              # Documentation (decision records, guides)
├── 2-engine/            # Core orchestration engine (consolidated from 8 folders)
│   ├── core/            # Agents, orchestration, interface, safety systems
│   ├── runtime/         # Memory systems, hooks, monitoring
│   └── tools/           # Integrations, utilities (106+ tools)
├── 3-gui/               # GUI layer (Vibe Kanban, integrations)
├── 5-project-memory/    # Project state, tasks, decisions, knowledge
├── 6-roadmap/           # Self-improvement roadmap
└── bin/                 # Executable scripts and CLI tools
```

### 2-Engine Structure (Consolidated)
```
2-engine/
├── core/
│   ├── agents/definitions/
│   │   ├── core/           # Base classes, Architect, Analyst, Developer
│   │   ├── managerial/     # Task lifecycle, coordination
│   │   └── specialists/    # 18 domain-specific agents (YAML-defined)
│   ├── orchestration/      # Pipeline, routing, state management
│   ├── interface/          # CLI, API, client interfaces
│   └── safety/             # Kill switch, classifiers, governance
├── runtime/
│   ├── memory/             # Multi-tier memory system
│   ├── hooks/              # Event-driven hooks
│   └── monitoring/         # Status tracking, validation
└── tools/
    ├── core/               # Core utilities (106+ tools)
    └── integrations/       # External service adapters
```

---

## Core Components

### 1. Agent System
**Purpose:** Hierarchical multi-agent coordination

**Components:**
- **3 Core Agents:**
  - Architect (CA): System design and architecture
  - Analyst (BP, RS, CB, DP): Research and analysis
  - Developer (DS, CR): Implementation and coding

- **18 Specialist Agents:** (YAML-defined)
  - Security-specialist, ML-specialist, Testing-specialist
  - Frontend-specialist, Backend-specialist, DevOps-specialist
  - Database-specialist, API-specialist, Performance-specialist
  - And 10 more domain specialists

- **Managerial Agents:**
  - Task Lifecycle Manager
  - Claude Coordinator
  - Skills Management

**Architecture:** Hierarchical with skill-based specialization
**Entry Point:** `2-engine/core/agents/definitions/core/`

---

### 2. Orchestration Engine
**Purpose:** Task processing and agent coordination

**Components:**
- **Unified Pipeline:** Task processing with anti-pattern detection
- **Task Router:** Intelligent agent assignment based on task type
- **State Manager:** Distributed state with race condition fixes
- **Circuit Breakers:** Failure isolation and resilience patterns
- **Atomic Commits:** Transaction safety for workflow operations

**Key Files:**
- `Orchestrator.py` (639 lines) - Main orchestration logic
- `task_router.py` - Agent selection
- `state_manager.py` - State management

**Entry Point:** `2-engine/core/orchestration/`

---

### 3. Memory Architecture
**Purpose:** Multi-tier knowledge management and storage

**Components:**
- **Working Memory:** Short-term task memory (in-memory)
- **Agent Memory:** Per-agent persistent JSON storage
- **Episodic Memory:** Long-term learning storage
- **Brain System:** Neo4j knowledge graph with vector embeddings
- **Consolidation:** Memory importance scoring and pruning

**Storage Backends:**
- PostgreSQL (structured data + vectors)
- Neo4j (knowledge graph)
- JSON (agent-specific storage)
- Embeddings (OpenAI text-embedding-3-small)

**Entry Point:** `2-engine/runtime/memory/`

---

### 4. Integration Layer
**Purpose:** External service adapters

**Integrations:**
- **GitHub:** Issue/PR management with CCPM patterns (710 lines of docs)
- **MCP:** Model Context Protocol integration
- **Supabase:** Database and real-time features
- **Vibe:** Kanban board integration
- **Obsidian:** Knowledge base integration
- **Vercel:** Deployment integration
- **OpenAI:** Embeddings and AI services

**Entry Point:** `2-engine/tools/integrations/`

---

### 5. Safety Systems
**Purpose:** Multi-layer protection and governance

**Components:**
- **Kill Switch:** Emergency shutdown
- **Intent Classifier:** Command safety validation
- **Safe Mode:** Restricted operation mode
- **Input Validation:** Sanitization layers
- **Audit Logging:** Complete operation trace

**Entry Point:** `2-engine/core/safety/`

---

### 6. Interface Layer
**Purpose:** User and system interfaces

**Components:**
- **CLI:** Command-line interface (`bin/blackbox`, `bin/verify-task`)
- **REST API:** HTTP endpoints for external access
- **Client Libraries:** Python client for programmatic access
- **Web Hooks:** Event-driven notifications

**Entry Point:** `2-engine/core/interface/`

---

## Tool Catalog

**Total Tools:** 106+ documented tools

**Categories:**
- File operations (read, write, edit, search)
- Git operations (commit, push, status)
- Testing utilities (runner, coverage, reporting)
- Code quality (linters, formatters, analyzers)
- Memory operations (store, retrieve, search)
- Integration utilities (GitHub, MCP, etc.)

**Documentation:** `CATALOG.md` contains complete tool index

---

## Configuration Files

### Build & Dependencies
- `requirements.txt` - Production dependencies
- `requirements-dev.txt` - Development dependencies
- `pyproject.toml` - (if present) Project configuration

### Git Configuration
- `.gitignore` - Git ignore patterns (newly created)
- `.git/` - Version control metadata

### Documentation
- `README.md` - Project overview
- `AGENT-GUIDE.md` - AI agent quick reference
- `SYSTEM-MAP.yaml` - Machine-readable structure
- `CATALOG.md` - Feature catalog (200+ items)

---

## Testing Infrastructure

### Test Organization
```
2-engine/
├── core/
│   ├── agents/definitions/*/tests/
│   ├── orchestration/*/*test*.py
│   ├── interface/client/test_*.py
│   └── safety/tests/
├── runtime/
│   ├── memory/systems/test_*.py
│   └── monitoring/*/test*.py
└── tools/
    └── integrations/_template/tests/
```

### Test Types
- Unit tests (per-module)
- Integration tests (memory systems)
- Anti-pattern detection tests
- Safety system tests
- End-to-end workflow tests

### Coverage
- **By File Count:** ~24% (91 test files / 381 total)
- **Key Areas Covered:** Memory, safety, core orchestration
- **Gaps:** Edge cases, performance, API contracts

---

## Key Metrics Summary

| Metric | Value | Notes |
|--------|-------|-------|
| Python Files | 381 | Core codebase |
| Test Files | 91 | ~24% coverage |
| Documentation Files | 288+ | README files |
| Tools | 106+ | Documented in CATALOG.md |
| Core Agents | 3 | Architect, Analyst, Developer |
| Specialist Agents | 18 | YAML-defined |
| Lines of Code (estimate) | ~50,000 | Based on file counts |
| Main Languages | Python, Bash, YAML | Multi-language system |

---

## Architecture Patterns

### Design Patterns Used
1. **Hierarchical Agent System:** Multi-layer coordination
2. **Plugin Architecture:** Dynamic skill loading
3. **Adapter Pattern:** Integration layer
4. **Dependency Injection:** Memory and tool systems
5. **Circuit Breaker Pattern:** Resilience layer
6. **Repository Pattern:** Data access abstraction
7. **Observer Pattern:** Hook system
8. **Strategy Pattern:** Agent selection

### Key Architectural Decisions
- **6-Folder Consolidation:** Merged 8 folders into 5 for better organization
- **Multi-Tier Memory:** Balance performance and persistence
- **Safety-First:** Multiple protection layers
- **Progressive Disclosure:** Skills loaded on-demand
- **Bash-based RALF:** Legacy autonomous system (being replaced)

---

## Entry Points

### For Development
- **CLI:** `bin/blackbox` - Main command-line interface
- **RALF Loop:** `2-engine/.autonomous/shell/ralf-loop.sh` - Autonomous execution
- **Verify Task:** `bin/verify-task` - Pre-execution validation

### For Integration
- **REST API:** `2-engine/core/interface/api/server.py`
- **Client Library:** `2-engine/core/interface/client/`
- **MCP Integration:** `2-engine/tools/integrations/mcp/`

### For Documentation
- **Quick Reference:** `AGENT-GUIDE.md`
- **Feature Catalog:** `CATALOG.md`
- **System Map:** `SYSTEM-MAP.yaml`
- **Project State:** `5-project-memory/blackbox5/STATE.yaml`

---

## Legacy Components

### Being Deprecated
- **2-engine/.autonomous/** - Bash-based RALF system
  - Replaced by Python-based autonomous system
  - Contains legacy scripts and prompts

### Migration Status
- **Project Memory:** Reorganized to 6-folder structure (completed)
- **RALF-Core:** Consolidated into blackbox5 (completed)
- **Documentation:** Centralized in 1-docs/ (completed)

---

## Next Steps

This inventory provides the foundation for:
1. **Gap Analysis:** Identify missing components
2. **Security Audit:** Review credential handling
3. **Performance Analysis:** Identify bottlenecks
4. **Technical Debt Assessment:** Prioritize refactoring
5. **Strategic Roadmap:** Plan improvements

**See also:** `gaps.md`, `roadmap.md`, `recommendations/`
