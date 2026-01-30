# BlackBox5 - Global AI Infrastructure

**Location:** `~/.blackbox5/`

This is the global BlackBox5 installation, accessible from any project.

## Quick Start

```bash
# Run RALF autonomous loop
c

# Run with specific model
glm    # GLM-4.7
kimi   # Kimi-k2.5
loop   # RALF with GLM
```

## Directory Structure

```
~/.blackbox5/
├── bin/              # Executable scripts
├── 1-docs/           # Documentation
├── 2-engine/         # Core engine
│   ├── 01-core/      # Agents, state, safety
│   └── 03-knowledge/ # Memory systems
├── 3-gui/            # GUI applications
├── 5-project-memory/ # Project data
└── 6-roadmap/        # Roadmap & plans
```

## Environment Variable

```bash
export BLACKBOX5_HOME="$HOME/.blackbox5"
```

## Project-Specific Data

Each project gets a subdirectory in `5-project-memory/`:
- `5-project-memory/<project-name>/tasks/`
- `5-project-memory/<project-name>/runs/`
- `5-project-memory/<project-name>/state.json`
