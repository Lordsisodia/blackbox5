# PLAN.md: Fix routes.yaml Incorrect Paths

**Task:** TASK-ARCH-064
**Status:** pending
**Created:** 2026-02-06

## Objective
Fix 17 incorrect paths in project routes.yaml.

## Issues Found

### Engine Paths (10 paths - WRONG)
All engine paths incorrectly nest `2-engine` inside project:
- engine: `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine`
- Should be: `/Users/shaansisodia/.blackbox5/2-engine`

### Memory Paths (6 paths - WRONG)
Duplicated segments: `5-project-memory/blackbox5/5-project-memory/blackbox5/...`
- Should be: `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/...`

### Feedback Paths (3 paths - WRONG)
Same duplication issue as memory paths.

## Implementation Steps
1. Backup routes.yaml (5 min)
2. Fix 10 engine paths (remove nested project prefix) (5 min)
3. Fix 6 memory paths (remove duplication) (5 min)
4. Fix 3 feedback paths (remove duplication) (5 min)
5. Verify all paths exist (5 min)
6. Test with validation script (5 min)

## Timeline
- Total: ~50 minutes (1 hour)

## Success Criteria
- [ ] All 10 engine paths corrected to sibling location
- [ ] All 6 memory paths deduplicated
- [ ] All 3 feedback paths deduplicated
- [ ] All paths verified to exist
- [ ] YAML syntax validated
