# BlackBox5 - Global AI Infrastructure

**Location:** `/opt/blackbox5/`

This is the BlackBox5 autonomous agent system installation.

## Quick Start

```bash
# Run RALF autonomous loop
cd /opt/blackbox5 && ./bin/ralf blackbox5

# Run with specific model (if configured)
glm    # GLM-4.7
kimi   # Kimi-k2.5
loop   # RALF with GLM
```

## Directory Structure

```
/opt/blackbox5/
├── 1-docs/                    # Documentation (383 files)
│   ├── 01-theory/             # Theoretical foundations
│   ├── 02-implementation/     # Code architecture
│   ├── 03-guides/             # How-to guides
│   ├── 04-project/            # Project management
│   ├── 05-examples/           # Reference implementations
│   ├── decisions/             # Architecture Decision Records
│   ├── development/           # Development resources
│   └── engine-guides/         # Engine-specific guides
├── 2-engine/                  # Core engine (15 subsystems)
│   ├── agents/                # Agent definitions
│   ├── core/                  # Core orchestration
│   ├── executables/           # Executable scripts
│   ├── helpers/               # Helper functions
│   ├── infrastructure/        # Infrastructure components
│   ├── interface/             # CLI and API interfaces
│   ├── modules/               # Modular components
│   ├── runtime/               # Runtime systems
│   ├── safety/                # Safety systems
│   └── tests/                 # Test suites
├── 5-project-memory/          # Project data and state
│   ├── blackbox5/             # Main project memory
│   │   ├── tasks/             # Active/completed tasks
│   │   ├── goals/             # Project goals
│   │   ├── plans/             # Implementation plans
│   │   ├── .autonomous/       # RALF autonomous system
│   │   └── knowledge/         # Knowledge base
├── 6-roadmap/                 # Roadmap & plans
├── agents/                    # Agent definitions and configs
├── bin/                       # Executable scripts (70+ tools)
│   ├── bb5                    # Main navigation CLI
│   ├── ralf                   # RALF autonomous system
│   └── bb5-*                  # Various BB5 utilities
├── .autonomous/               # Autonomous system files
├── autonomous/                # Autonomous configurations
├── .claude/                   # Claude Code configurations
├── config/                    # System configurations
├── dashboard-ui/              # Web dashboard interface
├── docs/                      # Additional documentation
├── engine/                    # Engine code
├── gateway/                   # Gateway services
├── logs/                      # System logs
├── observability/             # Monitoring and observability
├── openclaw/                  # OpenClaw integration
├── scripts/                   # Utility scripts
├── services/                  # Background services
├── skills/                    # Skill definitions
├── tasks/                     # Task management
├── tests/                     # Test files
└── workspace/                 # Working directory
```

## Environment Variable

```bash
export BLACKBOX5_HOME="/opt/blackbox5"
```

## Project-Specific Data

Project data is stored in `5-project-memory/blackbox5/`:
- `tasks/` - Active, completed, and archived tasks
- `goals/` - Project goals and milestones
- `plans/` - Implementation plans linked to goals
- `.autonomous/` - RALF autonomous system state and runs
- `knowledge/` - Knowledge base and learnings
- `STATE.yaml` - Single source of truth for project state

## Key Documentation

- **Getting Started**: See [1-docs/README.md](1-docs/README.md) for comprehensive documentation
- **Architecture**: [1-docs/01-theory/](1-docs/01-theory/) - Theoretical foundations
- **Implementation**: [1-docs/02-implementation/](1-docs/02-implementation/) - Code architecture
- **Guides**: [1-docs/03-guides/](1-docs/03-guides/) - How-to guides and tutorials
- **Project Status**: [1-docs/04-project/](1-docs/04-project/) - Project planning and status

## Core Systems

### RALF Autonomous System
- **Location**: `/opt/blackbox5/bin/ralf`
- **Purpose**: Continuous autonomous improvement
- **Documentation**: See [1-docs/01-theory/05-autonomous-systems/](1-docs/01-theory/05-autonomous-systems/)

### Agent Memory
- **Location**: Runtime memory system
- **Purpose**: Multi-tier memory (working, episodic, long-term)
- **Documentation**: See [1-docs/01-theory/02-memory/](1-docs/01-theory/02-memory/)

### Multi-Agent Orchestration
- **Location**: `/opt/blackbox5/2-engine/core/orchestration/`
- **Purpose**: Agent coordination and task routing
- **Documentation**: See [1-docs/02-implementation/01-core/orchestration/](1-docs/02-implementation/01-core/orchestration/)
