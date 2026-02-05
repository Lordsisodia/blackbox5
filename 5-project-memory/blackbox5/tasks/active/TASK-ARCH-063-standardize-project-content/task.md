# TASK-ARCH-063: Standardize Generic Project Content to Engine

**Status:** pending
**Priority:** MEDIUM
**Created:** 2026-02-06
**Type:** Structural Architecture

## Objective
Move 45 generic items from project to engine to standardize across all projects.

## Background
Project contains generic frameworks (queue management, metrics, skill selection) that should be in engine for reuse.

## Items to Standardize

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

### operations/ (8)
- skill-selection.yaml
- skill-metrics.yaml
- skill-usage.yaml
- improvement-metrics.yaml
- improvement-pipeline.yaml
- estimation-guidelines.yaml
- context-gathering.yaml
- testing-guidelines.yaml

### .autonomous/agents/ (9)
- analyzer/ pattern
- architect/ pattern
- executor/ pattern
- planner/ pattern
- scout/ pattern
- github-analysis-pipeline.sh

### .docs/ (5)
- template-system-guide.md
- ai-template-usage-guide.md
- task-system-design.md
- dot-docs-system.md
- goals-system-guide.md

## Success Criteria
- [ ] All 33 items moved to appropriate engine locations
- [ ] Project uses engine versions via imports/references
- [ ] Thin wrappers created where needed
- [ ] Documentation updated

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
