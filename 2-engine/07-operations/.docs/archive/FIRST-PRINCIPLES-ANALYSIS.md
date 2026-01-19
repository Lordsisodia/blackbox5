# 07-Operations First-Principles Analysis

## Current State

### Structure:
```
07-operations/
├── runtime/           # 711 files, 163 directories
│   ├── 136 shell scripts (*.sh)
│   ├── 118 Python files (*.py)
│   └── 20+ subdirectories
│
└── scripts/           # Empty structure, actual files in subdirs
    ├── tools/         # Python utilities
    └── utility-scripts/ # Shell scripts
```

## Problems Identified

### 1. Confusing "runtime" vs "scripts"
- **runtime/** has 700+ files including scripts, templates, libraries, configs
- **scripts/** has actual scripts but in sub-subdirectories
- No clear distinction between the two

### 2. Mixed Purposes in runtime/
- Agent execution scripts
- Planning templates
- Monitoring tools
- Validation scripts
- Utility functions
- Python libraries
- Git hooks
- Configuration files
- Documentation

### 3. Duplicate Categories
- `integration/` and `integrations/` - duplicates?
- `utils/` and `utility/` - duplicates?
- `lib/` and `lib.sh` - confusion?

### 4. No Clear Organization
- 20+ subdirectories with no clear taxonomy
- Scripts mixed with templates mixed with code
- Difficult to find what you need

## First-Principles Analysis

### Question: WHAT is "Operations"?

**Operations** = Everything needed to **RUN** the engine in production

### Three Fundamental Questions:

1. **WHAT do we run?** → Executable scripts/commands
2. **HOW do we run it?** → Configuration & environment
3. **WHAT supports it?** → Libraries, templates, utilities

### Four Categories of Operations:

#### 1. **Commands** (WHAT we execute)
- User-facing commands (run, stop, monitor)
- Agent commands (start, handoff, status)
- System commands (validate, check, test)

#### 2. **Workflows** (HOW we work)
- Planning workflows (create plans, steps, tranches)
- Development workflows (UI cycles, testing)
- Deployment workflows (promote, sync)

#### 3. **Environment** (WHERE we run)
- Configuration files
- Templates (for plans, specs, etc.)
- Python libraries
- Shared utilities (lib.sh, lib/)

#### 4. **Monitoring** (HOW we know it's working)
- Status checks
- Logging
- Health checks
- Metrics

## Proposed Structure

```
07-operations/
├── commands/          # Executable commands (user-facing)
│   ├── run/           # Start/stop operations
│   │   ├── autonomous-run.sh
│   │   ├── autonomous-loop.sh
│   │   └── ralph-runtime.sh
│   ├── agents/        # Agent operations
│   │   ├── agent-status.sh
│   │   ├── start-agent-cycle.sh
│   │   ├── new-agent.sh
│   │   └── agent-handoff.sh
│   ├── system/        # System operations
│   │   ├── intervene.sh
│   │   ├── monitor.sh
│   │   ├── analyze-response.sh
│   │   └── circuit-breaker.sh
│   └── specs/         # Spec operations
│       ├── spec-create.sh
│       ├── spec-analyze.sh
│       └── spec-validate.sh
│
├── workflows/         # Operational workflows
│   ├── planning/      # Planning workflows
│   │   ├── new-plan.sh
│   │   ├── new-step.sh
│   │   ├── new-tranche.sh
│   │   ├── action-plan.sh
│   │   ├── hierarchical-plan.sh
│   │   └── promote.sh
│   ├── development/   # Development workflows
│   │   ├── start-ui-cycle.sh
│   │   ├── start-testing.sh
│   │   ├── auto-breakdown.sh
│   │   └── generate-prd.sh
│   ├── discovery/     # Research workflows
│   │   ├── start-feature-research.sh
│   │   └── start-oss-discovery-cycle.sh
│   └── memory/        # Memory workflows
│       ├── auto-compact.sh
│       ├── compact-context.sh
│       └── manage-memory-tiers.sh
│
├── environment/       # Environment setup & config
│   ├── config/        # Configuration files
│   │   └── (config files)
│   ├── templates/     # Templates for operations
│   │   ├── prd-templates/
│   │   ├── planning/
│   │   └── specs/
│   ├── lib/           # Shared libraries
│   │   ├── lib.sh     # Shell library
│   │   └── python/    # Python libraries
│   ├── hooks/         # Git hooks
│   │   └── (hook files)
│   └── services/      # External services
│       └── start-redis.sh
│
├── monitoring/        # Monitoring & observability
│   ├── status/        # Status checks
│   │   ├── ralph-status.sh
│   │   ├── plan-status.py
│   │   ├── ui-cycle-status.py
│   │   └── test-agent-tracking.sh
│   ├── logging/       # Log operations
│   │   ├── view-logs.sh
│   │   └── view-manifest.sh
│   ├── health/        # Health checks
│   │   ├── check-dependencies.sh
│   │   ├── check-blackbox.sh
│   │   └── check-vendor-leaks.sh
│   └── alerts/        # Alerts & notifications
│       └── notify.sh
│
├── validation/        # Validation & testing
│   ├── check/         # Validation scripts
│   │   ├── validate-all.sh
│   │   ├── validate-loop.sh
│   │   ├── validate-ui-cycle.py
│   │   └── verify-readmes.sh
│   ├── test/          # Test operations
│   │   ├── benchmark-task.sh
│   │   └── check-ui-constraints.sh
│   └── tools/         # Validation tools
│       └── fix-perms.sh
│
└── utilities/         # Utility scripts (from scripts/)
    ├── git/           # Git operations
    │   └── (git tools)
    ├── maintenance/   # Maintenance tasks
    │   ├── build-semantic-index.sh
    │   ├── generate-readmes.sh
    │   └── sync-template.sh
    ├── setup/         # Setup scripts
    │   ├── init-project-memory.sh
    │   ├── update-index.sh
    │   └── verify-index.sh
    └── tools/         # Development tools
        ├── context_manager.py
        ├── git_ops.py
        ├── indexer.py
        └── tui_logger.py
```

## Benefits of This Structure

### 1. Clear Purpose
Each folder answers "WHY would I use this?":
- **commands** - To execute something
- **workflows** - To follow a process
- **environment** - To set up where I work
- **monitoring** - To see what's happening
- **validation** - To check if things work
- **utilities** - Helpful tools

### 2. Scalable
Easy to add new:
- Commands → `commands/{category}/`
- Workflows → `workflows/{category}/`
- Monitors → `monitoring/{category}/`

### 3. No Duplicates
Clear separation:
- `run/` not `runtime/` - commands only
- `planning/` not `runtime/planning/` - workflows only
- `lib/` in `environment/` - support files

### 4. User-Friendly
Natural organization:
- "I want to **run** something" → `commands/`
- "I want to **check** status" → `monitoring/`
- "I want to **validate**" → `validation/`

## Migration Mapping

### runtime/ → commands/
- `autonomous-run.sh` → `commands/run/`
- `agent-status.sh` → `commands/agents/`
- `monitor.sh` → `commands/system/`
- `spec-*.sh` → `commands/specs/`

### runtime/ → workflows/
- `planning/*` → `workflows/planning/`
- `testing/*` → `workflows/development/`
- `memory/*` → `workflows/memory/`

### runtime/ → environment/
- `prd-templates/*` → `environment/templates/`
- `lib.sh`, `lib/` → `environment/lib/`
- `python/` → `environment/lib/python/`
- `hooks/` → `environment/hooks/`
- `start-redis.sh` → `environment/services/`

### runtime/ → monitoring/
- `monitoring/*` → `monitoring/`
- `ralph-status.sh` → `monitoring/status/`
- `view-logs.sh` → `monitoring/logging/`
- `plan-status.py` → `monitoring/status/`

### runtime/ → validation/
- `validation/*` → `validation/`
- `testing/*` (checks) → `validation/test/`

### scripts/ → utilities/
- `tools/*` → `utilities/tools/`
- `utility-scripts/*` → `utilities/{maintenance,setup}/`

### Special Cases

#### ralph/ and ralphy/
These are **agent-specific runtime data**. Options:
1. Move to `project memory` (runtime data, not operations)
2. Keep in `operations/commands/agents/ralph/` (if it's commands)
3. Keep in `operations/environment/agents/ralph/` (if it's agent config)

**Recommendation**: Move to `5-project-memory/siso-internal/agents/ralph/` (runtime session data)

#### questioning/
This appears to be a workflow. Move to `workflows/development/questioning/`

#### integration/ vs integrations/
- `integration/` seems to be workflow integration
- `integrations/` seems to be system integration
- Merge or clarify purpose

## Questions for Decision

1. **ralph/ and ralphy/** - Agent runtime data or agent commands?
2. **questioning/** - Workflow or standalone category?
3. **integration vs integrations** - Merge or separate?

## Next Steps

1. Get confirmation on structure
2. Create migration script
3. Move files systematically
4. Update all references
5. Create comprehensive README
