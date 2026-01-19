# 07-Operations

Operational scripts, workflows, and tools for running the BlackBox5 Engine in production.

## Purpose

This folder contains everything needed to **operate** the engine:
- Execute commands (run agents, start workflows)
- Monitor system health and status
- Validate system integrity
- Manage environment and configuration

## Structure

The folder is organized by **WHAT YOU WANT TO DO**:

```
07-operations/
├── commands/          # Execute something
├── workflows/         # Follow a process
├── environment/       # Set up where you work
├── monitoring/        # Check system status
├── validation/        # Verify things work
└── utilities/         # Helpful tools
```

## Commands (`commands/`)

**User-facing executable scripts.**

### Run Operations (`commands/run/`)
Start, stop, and manage running systems:
- `autonomous-run.sh` - Start autonomous agent execution
- `autonomous-loop.sh` - Run autonomous loop continuously
- `ralph-runtime.sh` - Run Ralph agent runtime

### Agent Operations (`commands/agents/`)
Manage agent lifecycle:
- `agent-status.sh` - Check agent status
- `start-agent-cycle.sh` - Start agent execution cycle
- `new-agent.sh` - Create new agent
- `agent-handoff.sh` - Hand off between agents

### System Operations (`commands/system/`)
System-level commands:
- `intervene.sh` - Intervene in running system
- `monitor.sh` - Monitor system activity
- `analyze-response.sh` - Analyze system responses
- `circuit-breaker.sh` - Trigger circuit breaker

### Spec Operations (`commands/specs/`)
Work with specifications:
- `spec-create.sh` - Create new specification
- `spec-analyze.sh` - Analyze specification
- `spec-validate.sh` - Validate specification

## Workflows (`workflows/`)

**Multi-step operational processes.**

### Planning Workflows (`workflows/planning/`)
Create and manage plans:
- `new-plan.sh` - Create new project plan
- `new-step.sh` - Create new plan step
- `new-tranche.sh` - Create new tranche
- `action-plan.sh` - Create action plan
- `hierarchical-plan.sh` - Create hierarchical plan
- `promote.sh` - Promote plan artifacts

### Development Workflows (`workflows/development/`)
Development processes:
- `start-ui-cycle.sh` - Start UI development cycle
- `start-testing.sh` - Start testing workflow
- `auto-breakdown.sh` - Auto-breakdown tasks
- `generate-prd.sh` - Generate PRD from analysis
- `questioning/` - Questioning workflow

### Discovery Workflows (`workflows/discovery/`)
Research and discovery:
- `start-feature-research.sh` - Start feature research
- `start-oss-discovery-cycle.sh` - Start OSS discovery

### Memory Workflows (`workflows/memory/`)
Memory management:
- `auto-compact.sh` - Auto-compact working memory
- `compact-context.sh` - Compact context
- `manage-memory-tiers.sh` - Manage memory tiers

## Environment (`environment/`)

**Configuration, templates, and support files.**

### Configuration (`environment/config/`)
System configuration files.

### Templates (`environment/templates/`)
Operational templates:
- `prd-templates/` - PRD templates
- `planning/` - Planning templates
- `specs/` - Specification templates

### Libraries (`environment/lib/`)
Shared libraries and utilities:
- `lib.sh` - Shell utility library
- `python/` - Python utility modules
- `lib/` - Legacy library directory

### Hooks (`environment/hooks/`)
Git hooks for operations.

### Services (`environment/services/`)
External service management:
- `start-redis.sh` - Start Redis service

## Monitoring (`monitoring/`)

**Observe system health and status.**

### Status Checks (`monitoring/status/`)
Check system status:
- `ralph-status.sh` - Ralph agent status
- `plan-status.py` - Plan status check
- `ui-cycle-status.py` - UI cycle status
- `test-agent-tracking.sh` - Test agent tracking

### Logging (`monitoring/logging/`)
Log operations:
- `view-logs.sh` - View system logs
- `view-manifest.sh` - View manifest file

### Health Checks (`monitoring/health/`)
System health:
- `check-dependencies.sh` - Check dependencies
- `check-blackbox.sh` - Validate Blackbox structure
- `check-vendor-leaks.sh` - Check for vendor leaks

### Alerts (`monitoring/alerts/`)
Notifications and alerts:
- `notify.sh` - Send notifications

## Validation (`validation/`)

**Verify system integrity and functionality.**

### Validation Scripts (`validation/check/`)
Run validations:
- `validate-all.sh` - Run all validations
- `validate-loop.sh` - Validate in a loop
- `validate-ui-cycle.py` - Validate UI cycle
- `verify-readmes.sh` - Verify README coverage

### Test Operations (`validation/test/`)
Test operations:
- `benchmark-task.sh` - Benchmark task performance
- `check-ui-constraints.sh` - Check UI constraints

### Tools (`validation/tools/`)
Validation utilities:
- `fix-perms.sh` - Fix file permissions

## Utilities (`utilities/`)

**Helpful utility scripts.**

### Git Operations (`utilities/git/`)
Git-related utilities.

### Maintenance (`utilities/maintenance/`)
Maintenance tasks:
- `build-semantic-index.sh` - Build semantic search index
- `generate-readmes.sh` - Generate README files
- `sync-template.sh` - Sync templates

### Setup (`utilities/setup/`)
Setup operations:
- `init-project-memory.sh` - Initialize project memory
- `update-index.sh` - Update search index
- `verify-index.sh` - Verify search index

### Development Tools (`utilities/tools/`)
Developer tools:
- `context_manager.py` - Context management
- `git_ops.py` - Git operations
- `indexer.py` - File indexing
- `tui_logger.py` - TUI logging

## Quick Reference

### I want to...

| Action | Location |
|--------|----------|
| Run the engine | `commands/run/autonomous-run.sh` |
| Check status | `monitoring/status/ralph-status.sh` |
| Create a plan | `workflows/planning/new-plan.sh` |
| View logs | `monitoring/logging/view-logs.sh` |
| Validate system | `validation/check/validate-all.sh` |
| Start agent | `commands/agents/start-agent-cycle.sh` |
| Monitor system | `monitoring/` |

## Principles

1. **Action-oriented**: Organized by what you want to DO
2. **Clear naming**: Folder names describe purpose
3. **No duplication**: Each thing has one place
4. **Scalable**: Easy to add new commands/workflows
5. **User-friendly**: Natural language organization

## File Statistics

- **Total files**: ~711
- **Shell scripts**: ~136
- **Python files**: ~118
- **Categories**: 6 main areas

## Related

- Engine code: `../01-core/`, `../02-agents/`
- Development: `../08-development/`
- Project memory: `../../5-project-memory/`
