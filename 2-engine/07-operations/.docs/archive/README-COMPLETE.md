# 07-Operations - Complete Guide

## Purpose

**Operations** = Everything needed to **RUN** the BlackBox5 Engine in production

This folder contains operational scripts, workflows, monitoring, validation, and utilities. It does NOT contain:
- Project templates (those are in `5-project-memory/_template/`)
- Agent runtime data (that's in `5-project-memory/siso-internal/agents/`)
- Development tools (those are in `05-tools/`)
- Research reference (that's in `08-development/reference/`)

## First-Principles Organization

The folder is organized by **WHAT YOU WANT TO DO**:

```
07-operations/
├── commands/       # Execute something
├── workflows/      # Follow a process
├── environment/    # Set up where you work
├── monitoring/     # Check system health
├── validation/     # Verify things work
└── utilities/      # Helpful tools
```

---

## Commands (`commands/`)

**User-facing executable scripts.**

### Run Operations (`commands/run/`)
Start and manage running systems:

| Script | Purpose |
|--------|---------|
| `autonomous-run.sh` | Start autonomous agent execution |
| `autonomous-loop.sh` | Run autonomous loop continuously |
| `ralph-runtime.sh` | Run Ralph agent runtime |
| `ralph-cli.sh` | Ralph CLI interface |
| `ralph-loop.sh` | Ralph execution loop |

### Agent Operations (`commands/agents/`)
Manage agent lifecycle:

| Script | Purpose |
|--------|---------|
| `agent-status.sh` | Check agent status |
| `start-agent-cycle.sh` | Start agent execution cycle |
| `new-agent.sh` | Create new agent |
| `agent-handoff.sh` | Hand off between agents |

### System Operations (`commands/system/`)
System-level commands:

| Script | Purpose |
|--------|---------|
| `intervene.sh` | Intervene in running system |
| `monitor.sh` | Monitor system activity |
| `analyze-response.sh` | Analyze system responses |
| `circuit-breaker.sh` | Trigger circuit breaker |

### Spec Operations (`commands/specs/`)
Work with specifications:

| Script | Purpose |
|--------|---------|
| `spec-create.sh` | Create new specification |
| `spec-analyze.sh` | Analyze specification |
| `spec-validate.sh` | Validate specification |

### Service Operations (`commands/services/`)
External services:

| Script | Purpose |
|--------|---------|
| `start-redis.sh` | Start Redis service |

---

## Workflows (`workflows/`)

**Multi-step operational processes.**

### Planning Workflows (`workflows/planning/`)
Create and manage plans:

| Script | Purpose |
|--------|---------|
| `new-plan.sh` | Create new project plan |
| `new-step.sh` | Create new plan step |
| `new-step-hierarchical.sh` | Create hierarchical step |
| `new-tranche.sh` | Create new tranche |
| `new-run.sh` | Create new run |
| `action-plan.sh` | Create action plan |
| `hierarchical-plan.sh` | Create hierarchical plan |
| `promote.sh` | Promote plan artifacts |
| `spec-create.sh` | Create spec from plan |

### Development Workflows (`workflows/development/`)
Development processes:

| Script | Purpose |
|--------|---------|
| `start-ui-cycle.sh` | Start UI development cycle |
| `start-testing.sh` | Start testing workflow |
| `auto-breakdown.sh` | Auto-breakdown tasks |
| `generate-prd.sh` | Generate PRD from analysis |
| `questioning-workflow.sh` | Questioning workflow |

### Discovery Workflows (`workflows/discovery/`)
Research and discovery:

| Script | Purpose |
|--------|---------|
| `start-feature-research.sh` | Start feature research |
| `start-oss-discovery-cycle.sh` | Start OSS discovery |

### Memory Workflows (`workflows/memory/`)
Memory management:

| Script | Purpose |
|--------|---------|
| `auto-compact.sh` | Auto-compact working memory |
| `compact-context.sh` | Compact context |
| `compact-ui-context.sh` | Compact UI context |
| `manage-memory-tiers.sh` | Manage memory tiers |

---

## Environment (`environment/`)

**Configuration, templates, and support files.**

### Templates (`environment/templates/`)
Operational templates:
- `prd-templates/` - PRD templates for various use cases

### Libraries (`environment/lib/`)
Shared libraries and utilities:

**Shell Library**:
- `lib.sh` - Main shell utility library
- `lib/auto-compact.sh` - Memory compaction
- `lib/background-manager.sh` - Background process management
- `lib/bmad-tracker.sh` - BMAD tracking
- `lib/circuit-breaker/` - Circuit breaker implementation
- `lib/exit_decision_engine.sh` - Exit decisions
- `lib/hooks-manager.sh` - Git hooks management
- `lib/keyword-detector.sh` - Keyword detection
- `lib/mcp-manager.sh` - MCP integration
- `lib/notify.sh` - Notifications
- `lib/response_analyzer.sh` - Response analysis
- `lib/spec-creation/validation.sh` - Spec validation
- `lib/vendor-validator.sh` - Vendor validation

**Python Libraries**:
- `python/` - Python utility modules

### Git Hooks (`environment/hooks/`)
Git hooks for operations:
- `inject-context.sh` - Inject context into commits
- `validate-changes.sh` - Validate changes before commit

---

## Monitoring (`monitoring/`)

**Observe system health and status.**

### Status Checks (`monitoring/status/`)
Check system status:

| Script | Purpose |
|--------|---------|
| `ralph-status.sh` | Ralph agent status |
| `monitor-autonomous.sh` | Monitor autonomous execution |
| `test-agent-tracking.sh` | Test agent tracking |
| `plan-status.py` | Plan status check |
| `ui-cycle-status.py` | UI cycle status |
| `start-10h-monitor.sh` | Start 10-hour monitoring |

### Logging (`monitoring/logging/`)
Log operations:
- `view-logs.sh` - View system logs
- `view-manifest.sh` - View manifest file

---

## Validation (`validation/`)

**Verify system integrity and functionality.**

### Validation Scripts (`validation/check/`)
Run validations:

| Script | Purpose |
|--------|---------|
| `validate-all.sh` | Run all validations |
| `validate-loop.sh` | Validate in a loop |
| `validate_spec.sh` | Validate specification |
| `verify-readmes.sh` | Verify README coverage |
| `validate-ui-cycle.py` | Validate UI cycle |

### Test Operations (`validation/test/`)
Test operations:

| Script | Purpose |
|--------|---------|
| `benchmark-task.sh` | Benchmark task performance |
| `check-ui-constraints.sh` | Check UI constraints |
| `check-vendor-leaks.sh` | Check for vendor leaks |
| `test-context-variables.sh` | Test context variables |
| `test-hierarchical-tasks.sh` | Test hierarchical tasks |

### Phase Tests (`validation/test/phases/`)
Organized by testing phases:
- `phase2/` - Phase 2 validation
- `phase3/` - Phase 3 tests (integration, questioning, spec creation, validation)
- `phase4/` - Phase 4 tests (circuit breaker, integration, ralph runtime, response analyzer)

---

## Utilities (`utilities/`)

**Helpful utility scripts.**

### Git Utilities (`utilities/git/`)
Git-related operations:
- `install-hooks.sh` - Install git hooks
- `sync-template.sh` - Sync templates

### Maintenance (`utilities/maintenance/`)
Maintenance tasks:
- `build-semantic-index.sh` - Build semantic search index
- `fix-perms.sh` - Fix file permissions
- `generate-readmes.sh` - Generate README files
- `review-compactions.sh` - Review memory compactions

### Notification (`utilities/notifications/`)
- `notify.sh` - Send notifications

---

## Quick Reference

### I want to...

| Action | Location |
|--------|----------|
| **Run the engine** | `commands/run/autonomous-run.sh` |
| **Check status** | `monitoring/status/` |
| **Create a plan** | `workflows/planning/new-plan.sh` |
| **View logs** | `monitoring/logging/view-logs.sh` |
| **Validate system** | `validation/check/validate-all.sh` |
| **Start agent** | `commands/agents/start-agent-cycle.sh` |
| **Monitor system** | `monitoring/` |
| **Generate PRD** | `workflows/development/generate-prd.sh` |
| **Compact memory** | `workflows/memory/auto-compact.sh` |

---

## What's NOT Here (And Where It Is)

### Project Templates → `5-project-memory/_template/`
- `blackbox-template/_template/` - Complete project scaffolding template

### Agent Runtime Data → `5-project-memory/siso-internal/agents/`
- `ralph/` - Ralph agent session data
- `ralphy/` - Ralphy agent session data

### Development Tools → `05-tools/tools/`
- Python development utilities (context_manager, git_ops, indexer, tui_logger)

### Research Reference → `08-development/reference/research/`
- Research query templates and rubrics

---

## Principles

1. **Action-oriented**: Organized by what you want to DO
2. **Clear naming**: Folder names describe purpose
3. **No duplication**: Each thing has one place
4. **Scalable**: Easy to add new commands/workflows
5. **User-friendly**: Natural language organization

---

## Statistics

- **Total files**: ~617 (after removing non-operations)
- **Shell scripts**: ~136
- **Python files**: ~118 (utilities and libraries)
- **Categories**: 6 main areas

---

## Related

- Engine code: `../01-core/`, `../02-agents/`
- Development: `../08-development/`
- Project memory: `../../5-project-memory/`
- Tools: `../05-tools/`
- Integrations: `../06-integrations/`
