# PLAN.md: Standardize Project Content to Engine

**Task:** TASK-ARCH-063
**Status:** pending
**Created:** 2026-02-06

## Objective
Move 15 generic patterns from project to engine for standardization.

## Items to Migrate

### bin/ Scripts (11 items)
- bb5-queue-manager.py → queue-manager.py
- bb5-health-dashboard.py → health-dashboard.py
- bb5-metrics-collector.py → metrics-collector.py
- bb5-parallel-dispatch.sh → parallel-dispatch.sh
- bb5-reanalysis-engine.py → reanalysis-engine.py
- calculate-skill-metrics.py → skill-metrics-calculator.py
- log-skill-usage.py → skill-usage-logger.py
- validate-skill-usage.py → skill-usage-validator.py
- collect-skill-metrics.py → (merge into calculator)
- generate-skill-report.py → (merge into calculator)
- update-dashboard.py → (keep in project, BB5-specific)

### operations/ Files (3 items)
- skill-selection.yaml → engine/config/skill-framework/
- skill-metrics.yaml → engine/config/skill-framework/
- skill-usage.yaml → engine/config/skill-framework/

### .docs/ Files (1 item)
- template-system-guide.md → engine/.docs/

## Abstraction Required
- Path abstraction via environment variables
- Project name configuration
- Operations directory location

## Timeline
- Engine Preparation: 2 hours
- Script Migration: 4 hours
- Project Wrappers: 1 hour
- Testing: 2 hours
- Documentation: 1 hour
- Total: 10-12 hours

## Success Criteria
- [ ] All 11 scripts migrated to engine
- [ ] All 3 operations schemas in engine
- [ ] Project wrappers created and tested
- [ ] Backward compatibility maintained
