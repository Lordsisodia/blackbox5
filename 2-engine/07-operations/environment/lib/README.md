# Blackbox5 Environment Library

Component in Blackbox5.

## Location

```
2-engine/07-operations/environment/lib/
```

## Purpose

This directory contains library systems and utility scripts for the Blackbox5 autonomous agent environment. Each library system follows the AgentMD metadata specification for AI discoverability and cross-project knowledge reuse.

## Metadata System

All artifacts in this directory have associated `metadata.yaml` files following the **AgentMD schema** defined in:
```
2-engine/03-knowledge/storage/brain/metadata/schema.yaml
```

### Metadata Directory

See `.metadata/` for:
- **INDEX.yaml**: Master catalog of all artifacts
- **generate-metadata.sh**: Template generator for new metadata
- **validate-metadata.sh**: Validation script for metadata consistency
- **README.md**: Complete metadata documentation

### Quick Metadata Stats

| Category | Count |
|----------|-------|
| Library Systems | 8 |
| Root Scripts | 11 |
| Total Artifacts | 19 |

## Library Systems

Each library system is in its own subdirectory with `metadata.yaml`:

| ID | Name | Phase | Purpose |
|----|------|-------|---------|
| `context-variables-lib` | Context Variables | 1 | Shared state and context management |
| `hierarchical-tasks-lib` | Hierarchical Tasks | 2 | Parent-child task relationships (CrewAI) |
| `task-breakdown` | Task Breakdown | 2 | MetaGPT-inspired task extraction |
| `spec-creation` | Spec Creation | 2 | Structured specifications and validation |
| `circuit-breaker` | Circuit Breaker | 3 | Loop protection and stagnation detection |
| `hooks-lib` | Hooks | 3 | Pre-tool execution hooks |
| `response-analyzer` | Response Analyzer | 4 | Response quality analysis |
| `ralph-runtime` | Ralph Runtime | 4 | Autonomous execution engine |

## Root-Level Scripts

Utility scripts in the root `lib/` directory have metadata in `.metadata/`:

| Script | Phase | Category | Purpose |
|--------|-------|----------|---------|
| `auto-compact.sh` | 3 | memory-management | Automatic context compression |
| `background-manager.sh` | 4 | task-management | Parallel background tasks |
| `bmad-tracker.sh` | 2 | methodology | BMAD 4-phase tracking |
| `exit_decision_engine.sh` | 3 | circuit-breaker | Intelligent exit decisions |
| `hooks-manager.sh` | 3 | hooks | Hook management |
| `keyword-detector.sh` | 4 | modes | Keyword-based mode switching |
| `lib.sh` | 1 | utilities | Shared utility functions |
| `mcp-manager.sh` | 3 | integrations | MCP server management |
| `notify.sh` | 4 | notifications | Multi-channel notifications |
| `response-analyzer.sh` | 4 | analysis | Response analysis |
| `vendor-validator.sh` | 3 | validation | Vendor lock-in detection |

## Phases

1. **Phase 1**: Foundation - Context, utilities, shared libraries
2. **Phase 2**: Planning - Task breakdown, spec creation, hierarchical tasks
3. **Phase 3**: Execution - Circuit breaker, validation, integration
4. **Phase 4**: Autonomous - Runtime, analysis, monitoring

## Discovery by Intent

| I want to... | Use... | Phase |
|--------------|--------|-------|
| Manage shared state | `context-variables/` | 1 |
| Create task hierarchies | `hierarchical-tasks/` | 2 |
| Break down requirements | `task-breakdown/` | 2 |
| Create specifications | `spec-creation/` | 2 |
| Prevent infinite loops | `circuit-breaker/` | 3 |
| Validate file changes | `hooks/` | 3 |
| Analyze responses | `response-analyzer/` | 4 |
| Run autonomous execution | `ralph-runtime/` | 4 |

## Usage

### Using Library Systems

Each library system can be imported and used independently:

```python
# Example: Using hierarchical-tasks
from lib.hierarchical_tasks import HierarchicalTask, TaskDependency

task = HierarchicalTask(id="task-1", description="Build feature")
subtask = HierarchicalTask(id="task-1-1", description="Write code", parent_id="task-1")
```

### Using Scripts

Scripts can be sourced or executed directly:

```bash
# Source shared library
source lib/lib.sh

# Run background task manager
lib/background-manager.sh add "My task" --agent developer --priority high
```

### Finding Metadata

```bash
# List all metadata
find lib -name "metadata.yaml"

# Validate all metadata
lib/.metadata/validate-metadata.sh -r

# Generate new metadata
lib/.metadata/generate-metadata.sh -t library -n "My Lib" my-lib
```

## Integration

These libraries integrate with:
- **Blackbox5 Core**: Agent framework and orchestration
- **Brain Storage**: Metadata and knowledge management
- **Ralph Runtime**: Autonomous execution engine
- **Circuit Breaker**: Safety and loop protection

## Documentation

See individual library directories for detailed documentation:
- Each library has a `README.md`
- Each library has `metadata.yaml` with relationships
- Each library may have `examples/` with usage examples

## Metadata Schema Reference

The AgentMD schema defines:
- **Required fields**: id, type, name, category, version
- **Relationships**: depends_on, used_by, relates_to
- **Classification**: phase, layer, status, stability
- **Documentation**: docs, examples
- **Metrics**: usage_count, last_used, success_rate

Full schema: `2-engine/03-knowledge/storage/brain/metadata/schema.yaml`

## Parent Directory

Part of: [`2-engine/07-operations/environment/`](../)
