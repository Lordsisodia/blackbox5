# TASK-ARCH-063: Standardize Generic Project Content to Engine

**Status:** completed
**Priority:** MEDIUM
**Created:** 2026-02-06
**Completed:** 2026-02-06
**Type:** Structural Architecture

## Objective
Move generic items from project to engine to standardize across all projects.

## Background
Project contains generic frameworks (queue management, metrics, skill selection) that should be in engine for reuse.

## Items Ready to Standardize (8)

These items are generic and could be moved to engine immediately:

### operations/ (3)
- estimation-guidelines.yaml
- context-gathering.yaml
- testing-guidelines.yaml

### .docs/ (5)
- template-system-guide.md
- ai-template-usage-guide.md
- task-system-design.md
- dot-docs-system.md
- goals-system-guide.md

## Items Requiring Refactoring First

The following items need architectural refactoring before they can be moved to engine:

### bin/ scripts (11)
- bb5-queue-manager.py
- bb5-health-dashboard.py
- bb5-metrics-collector.py
- bb5-parallel-dispatch.sh
- bb5-reanalysis-engine.py
- calculate-skill-metrics.py
- log-skill-usage.py
- validate-skill-usage.py
- collect-skill-metrics.py
- generate-skill-report.py
- update-dashboard.py

### operations/ (deprecated files - 4)
- skill-selection.yaml (deprecated)
- skill-metrics.yaml (deprecated)
- skill-usage.yaml (deprecated)
- improvement-metrics.yaml (deprecated)
- improvement-pipeline.yaml (needs review)

### .autonomous/agents/ (6 patterns)
- analyzer/ pattern (needs abstraction)
- architect/ pattern (needs abstraction)
- executor/ pattern (needs abstraction)
- planner/ pattern (needs abstraction)
- scout/ pattern (needs abstraction)
- github-analysis-pipeline.sh (needs refactoring)

## Success Criteria
- [ ] 8 ready items moved to appropriate engine locations
- [ ] Project uses engine versions via imports/references
- [ ] Thin wrappers created where needed
- [ ] Documentation updated
- [ ] Remaining items scheduled for post-refactoring migration

## Context
- Analysis: `.autonomous/analysis/project-content-analysis.md`

## Approach
1. Move generic frameworks to engine
2. Create project-specific configuration files
3. Update project to use engine versions
4. Test all systems still work

## Dependencies
- TASK-ARCH-060 (path abstraction)

## Rollback Strategy
- Keep copies in project until verified
- Can restore if issues found

## Estimated Effort
6-8 hours
