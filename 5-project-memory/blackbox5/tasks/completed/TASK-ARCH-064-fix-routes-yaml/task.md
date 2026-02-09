# TASK-ARCH-064: Fix routes.yaml Incorrect Paths

**Status:** pending
**Priority:** CRITICAL
**Created:** 2026-02-06
**Type:** Structural Architecture

## Objective
Fix the incorrect path nesting in project routes.yaml where 2-engine paths are incorrectly nested inside 5-project-memory/blackbox5.

## Background
Scout analysis found 10+ incorrect paths in project routes.yaml suggesting 2-engine is nested inside the project directory. These paths don't exist and will cause failures.

## Incorrect Paths to Fix

Current (WRONG):
```yaml
engine: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine"
engine_shell: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine/.autonomous/shell"
engine_lib: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine/.autonomous/lib"
engine_prompts: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine/.autonomous/prompts"
engine_skills: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine/.autonomous/skills"
engine_schemas: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine/.autonomous/schemas"
engine_routes: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine/.autonomous/routes.yaml"
bmad_skills: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine/.autonomous/skills"
bmad_workflows: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine/.autonomous/workflows"
bmad_wip: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine/.autonomous/wip"
```

Should be (CORRECT):
```yaml
engine: "/Users/shaansisodia/.blackbox5/2-engine"
engine_shell: "/Users/shaansisodia/.blackbox5/2-engine/.autonomous/shell"
# ... etc
```

Also fix duplicated path segments:
```yaml
# WRONG
memory:
  tasks: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/5-project-memory/blackbox5/tasks"

# CORRECT
memory:
  tasks: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/tasks"
```

## Success Criteria
- [ ] All 10+ incorrect engine paths fixed
- [ ] All duplicated path segments fixed
- [ ] All paths verified to exist
- [ ] Validation script created to prevent regression
- [ ] No broken references after fix

## Context
- Scout report: `.autonomous/analysis/scout-routes-structure.md`
- Engine routes: `2-engine/.autonomous/routes.yaml`
- Project routes: `5-project-memory/blackbox5/.autonomous/context/routes.yaml`

## Approach
1. Read both routes.yaml files completely
2. Identify all incorrect paths
3. Fix paths to correct locations
4. Create validation script
5. Test all routes resolve correctly

## Rollback Strategy
- Backup routes.yaml before changes
- One-command restore from backup

## Estimated Effort
1-2 hours

## Related Tasks
- TASK-ARCH-060: Path abstraction layer
- TASK-ARCH-065: Create path resolution library
