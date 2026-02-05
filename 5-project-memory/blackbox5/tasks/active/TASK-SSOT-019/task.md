# TASK-SSOT-019: Make STATE.yaml Derived from Task Files

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-06
**Parent:** Issue #11 - SSOT Task State Violations

## Objective
Make STATE.yaml a derived view that aggregates from task.md files, not a separate source of truth.

## Success Criteria:
- [ ] Create script to generate STATE.yaml from task files
- [ ] Remove manual STATE.yaml updates
- [ ] Add "last_generated" timestamp
- [ ] Ensure STATE.yaml fields match task file data
- [ ] Document STATE.yaml as derived view
- [ ] Auto-regenerate on task changes

## Context
STATE.yaml currently duplicates task data:
- Lists active and completed tasks
- But task files are canonical source
- Manual sync doesn't work (0% success)

## Approach
1. Analyze STATE.yaml schema
2. Create generation script
3. Map task file fields to STATE.yaml fields
4. Remove manual updates
5. Add auto-generation trigger

## Related Files
- STATE.yaml
- tasks/active/*/task.md
- tasks/completed/*/task.md
- bin/bb5-* commands that update STATE.yaml

## Rollback Strategy
Keep manual update capability until generation proven reliable.
