# TASK-SSOT-040: Create Unified Operations Dashboard

**Status:** pending
**Priority:** MEDIUM
**Created:** 2026-02-06
**Parent:** SSOT Violations - Skill Documentation Scattering

## Objective
Consolidate skill documentation from multiple locations into a unified directory structure with standardized format and searchable index.

## Success Criteria
- [ ] Unified skill directory created at `.autonomous/skills/`
- [ ] Skill index created at `skills/index.yaml` with all available skills
- [ ] Standard skill documentation template defined
- [ ] Engine skill docs migrated from `2-engine/.autonomous/skills/`
- [ ] Project skill docs migrated to unified location
- [ ] Operations skill data integrated into skill directories
- [ ] Skill discovery updated to use centralized index
- [ ] Categories defined (git, database, testing, etc.)

## Context
Skill documentation is currently scattered across engine skills, project skills, and operations data files. This creates discovery difficulty, inconsistent formats, maintenance overhead from multiple update locations, and no unified index of available skills. The solution requires a single location with standard format and cross-referencing to skill data.

## Approach
1. Create unified `skills/` directory structure with subdirectories per skill
2. Define standard documentation format (README.md, USAGE.md, SKILL.yaml)
3. Migrate existing skill documentation from all locations
4. Generate skill index with categories and trigger keywords
5. Update skill selection to use centralized index for discovery

## Estimated Effort
2-3 hours

## Rollback Strategy
If unified structure causes issues, maintain symlinks from old locations to new unified location while transitioning, or revert to separate locations with synchronization script.
