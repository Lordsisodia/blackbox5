# Complete File Categorization - 07-Operations

## Critical Discoveries

### 1. blackbox-template/ - MISPLACED
**Location**: `runtime/python/core/blackbox-template/_template/`
**What it is**: Complete project template for scaffolding new BlackBox projects
**Where it should be**: `5-project-memory/_template/blackbox/`
**Reason**: This is project scaffolding, not operations

### 2. Scripts/ - Duplicate Structure
**Location**: `scripts/tools/tools/` (nested!)
**Issue**: Tools inside tools inside tools
**Fix**: Flatten structure

---

## Complete Categorization by First Principles

### Principle: WHAT is this file FOR?

#### Category 1: PROJECT SCAFFOLDING (Not Operations!)
These are **templates** for creating new projects.

**Move to**: `5-project-memory/_template/`

```
runtime/python/core/blackbox-template/_template/
├── .gitignore
├── .plans/
├── .prompts/
├── .skills/
├── agents/
├── context.md
├── deepresearch/
├── docs-ledger.md
├── experiments/
├── information-routing.md
├── journal.md
├── manifest.yaml
├── README.md
├── schemas/
├── scripts/           # 41 scripts!
├── snippets/
└── tasks.md
```

#### Category 2: AGENT RUNTIME DATA (Not Operations!)
These are **session data** for running agents.

**Move to**: `5-project-memory/siso-internal/agents/`

```
runtime/ralph/          # Ralph agent session data
runtime/ralphy/         # Ralphy agent session data
```

#### Category 3: OPERATIONAL COMMANDS
Executable scripts that **DO** something.

**Keep in**: `07-operations/commands/`

##### Run Commands (commands/run/)
```
runtime/autonomous-run.sh
runtime/autonomous-loop.sh
runtime/ralph-runtime.sh
runtime/ralph-cli.sh
runtime/ralph-loop.sh
```

##### Agent Commands (commands/agents/)
```
runtime/agent-status.sh
runtime/agents/agent-handoff.sh
runtime/agents/new-agent.sh
runtime/agents/start-agent-cycle.sh
```

##### System Commands (commands/system/)
```
runtime/intervene.sh
runtime/monitor.sh
runtime/analyze-response.sh
runtime/circuit-breaker.sh
```

##### Spec Commands (commands/specs/)
```
runtime/spec-create.sh
runtime/spec-analyze.sh
runtime/spec-validate.sh
```

##### Service Commands (commands/services/)
```
runtime/start-redis.sh
```

#### Category 4: WORKFLOWS
Multi-step processes that **guide** work.

**Keep in**: `07-operations/workflows/`

##### Planning Workflows (workflows/planning/)
```
runtime/planning/action-plan.sh
runtime/planning/new-plan.sh
runtime/planning/new-run.sh
runtime/planning/new-step.sh
runtime/planning/new-step-hierarchical.sh
runtime/planning/new-tranche.sh
runtime/planning/promote.sh
runtime/planning/spec-create.sh
runtime/new-step.sh
runtime/hierarchical-plan.sh
```

##### Development Workflows (workflows/development/)
```
runtime/auto-breakdown.sh
runtime/generate-prd.sh
runtime/questioning-workflow.sh
runtime/questioning/        # (questioning workflow content)
runtime/testing/start-ui-cycle.sh
runtime/testing/start-testing.sh
```

##### Discovery Workflows (workflows/discovery/)
```
runtime/testing/start-feature-research.sh
runtime/testing/start-oss-discovery-cycle.sh
```

##### Memory Workflows (workflows/memory/)
```
runtime/memory/auto-compact.sh
runtime/memory/compact-context.sh
runtime/memory/compact-ui-context.sh
runtime/memory/manage-memory-tiers.sh
```

#### Category 5: ENVIRONMENT & CONFIGURATION
Files that **DEFINE** where/how things run.

**Keep in**: `07-operations/environment/`

##### Templates (environment/templates/)
```
runtime/prd-templates/     # PRD templates
```

##### Libraries (environment/lib/)
```
runtime/lib.sh             # Main shell library
runtime/lib/               # Shell library modules
runtime/lib/auto-compact.sh
runtime/lib/background-manager.sh
runtime/lib/bmad-tracker.sh
runtime/lib/circuit-breaker/circuit-breaker.sh
runtime/lib/exit_decision_engine.sh
runtime/lib/hooks-manager.sh
runtime/lib/keyword-detector.sh
runtime/lib/mcp-manager.sh
runtime/lib/notify.sh
runtime/lib/response_analyzer.sh
runtime/lib/spec-creation/validation.sh
runtime/lib/vendor-validator.sh

runtime/python/           # Python libraries (not template!)
```

##### Git Hooks (environment/hooks/)
```
runtime/hooks/inject-context.sh
runtime/hooks/validate-changes.sh
```

#### Category 6: MONITORING
Files that **OBSERVE** system state.

**Keep in**: `07-operations/monitoring/`

##### Status Monitoring (monitoring/status/)
```
runtime/monitoring/ralph-status.sh
runtime/monitoring/start-10h-monitor.sh
runtime/test-agent-tracking.sh
runtime/plan-status.py
runtime/ui-cycle-status.py
runtime/ralph/monitor-autonomous.sh
```

##### Logging (monitoring/logging/)
```
runtime/view-logs.sh
runtime/view-manifest.sh
```

##### Health Checks (monitoring/health/)
```
runtime/validation/check-dependencies.sh  # Move here
runtime/validation/check-blackbox.sh       # Move here
```

#### Category 7: VALIDATION
Files that **VERIFY** correctness.

**Keep in**: `07-operations/validation/)

##### Validation Scripts (validation/check/)
```
runtime/validation/validate-all.sh
runtime/validation/validate-loop.sh
runtime/validation/validate_spec.sh
runtime/validation/verify-readmes.sh
runtime/validate-ui-cycle.py
```

##### Test Scripts (validation/test/)
```
runtime/testing/benchmark-task.sh
runtime/testing/check-ui-constraints.sh
runtime/testing/check-vendor-leaks.sh
runtime/testing/test-context-variables.sh
runtime/testing/test-hierarchical-tasks.sh
```

##### Phase Tests (validation/test/phases/)
```
runtime/testing/phase2/validate-phase2.sh
runtime/testing/phase3/*.sh
runtime/testing/phase4/*.sh
```

#### Category 8: UTILITIES
Helpful tools that **ASSIST** operations.

**Keep in**: `07-operations/utilities/`

##### Git Utilities (utilities/git/)
```
runtime/utility/install-hooks.sh
runtime/utility/sync-template.sh
```

##### Maintenance (utilities/maintenance/)
```
runtime/utility/build-semantic-index.sh
runtime/utility/fix-perms.sh
runtime/utility/generate-readmes.sh
runtime/utility/review-compactions.sh
```

##### Notification (utilities/notifications/)
```
runtime/utility/notify.sh
runtime/lib/notify.sh      # Duplicate, decide
```

#### Category 9: DEVELOPMENT TOOLS
Tools for **development** (not operations).

**Move to**: `05-tools/tools/`

```
scripts/tools/context_manager.py
scripts/tools/git_ops.py
scripts/tools/indexer.py
scripts/tools/tui_logger.py
scripts/tools/maintenance/*.sh
scripts/tools/validation/*.sh
```

#### Category 10: PROJECT SETUP SCRIPTS
Scripts for **setting up** projects.

**Move to**: `5-project-memory/_template/scripts/` or keep in `operations/utilities/setup/`

```
scripts/utility-scripts/init-project-memory.sh
scripts/utility-scripts/update-index.sh
scripts/utility-scripts/verify-index.sh
```

---

## Integration Workflows (Special Category)

**Location**: `runtime/integration/`
**Files**: `integrate_spec.sh`

**Question**: Is this:
1. An operational workflow? → `workflows/integration/`
2. Part of 06-integrations/? → Move there

**Recommendation**: Keep as workflow if it's about USING integrations, move to 06-integrations if it's about CREATING them

---

## RESEARCH SNIPPETS (Special Category)

**Location**: `runtime/python/core/snippets/research/`
**What it is**: Research query templates and rubrics

**Question**: Should this be:
1. In `08-development/reference/research/`? (Reference material)
2. In `5-project-memory/_template/research/`? (Research templates)
3. Deleted? (Outdated)

**Recommendation**: Move to `08-development/reference/research/snippets/`

---

## Summary of Moves

### Move OUT of 07-operations:

1. **Project Template** → `5-project-memory/_template/blackbox/`
   - `runtime/python/core/blackbox-template/_template/`

2. **Agent Runtime Data** → `5-project-memory/siso-internal/agents/`
   - `runtime/ralph/`
   - `runtime/ralphy/`

3. **Development Tools** → `05-tools/tools/`
   - `scripts/tools/*.py`

4. **Research Snippets** → `08-development/reference/research/`
   - `runtime/python/core/snippets/research/`

### Keep IN 07-operations:

1. **Commands** (all executable scripts)
2. **Workflows** (all multi-step processes)
3. **Environment** (config, templates, lib, hooks)
4. **Monitoring** (status, logging, health)
5. **Validation** (all checks and tests)
6. **Utilities** (helpful tools)

---

## File Count Summary

### Total Files: 711

### Moves Required:
- To project memory: ~50 files (template + ralph + ralphy)
- To development: ~40 files (research snippets)
- To tools: ~4 files (Python tools)
- **Keep in operations**: ~617 files

### Final Structure:
```
07-operations/           # ~617 files (clean, focused)
├── commands/            # ~30 executable commands
├── workflows/           # ~40 workflow scripts
├── environment/         # ~200 config/lib files
├── monitoring/          # ~20 monitoring scripts
├── validation/          # ~300 validation/test scripts
└── utilities/           # ~27 utility scripts
```

---

## Implementation Order

### Phase 1: Move OUT (Things that don't belong)
1. Move blackbox-template to project memory
2. Move ralph/ralphy to project memory
3. Move research snippets to development
4. Move development tools to tools

### Phase 2: Create NEW Structure
1. Create commands/, workflows/, environment/, monitoring/, validation/, utilities/
2. Create subdirectories

### Phase 3: Move IN (Organize remaining files)
1. Move command scripts
2. Move workflow scripts
3. Move environment files
4. Move monitoring scripts
5. Move validation scripts
6. Move utility scripts

### Phase 4: Clean Up
1. Remove empty directories
2. Remove duplicates
3. Update references

### Phase 5: Verify
1. Count files (should be ~617)
2. Test critical operations
3. Update README
