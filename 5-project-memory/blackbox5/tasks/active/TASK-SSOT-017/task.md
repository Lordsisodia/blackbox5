# TASK-SSOT-017: Create Analysis Extraction Pipeline

**Status:** pending
**Priority:** MEDIUM
**Created:** 2026-02-06
**Parent:** Issue #17 - SSOT Run/Agent Outputs Violations

## Objective
Create pipeline to extract insights from run folders to knowledge/analysis/. Archive run folders after extraction.

## Success Criteria
- [ ] Design extraction pipeline workflow
- [ ] Create extraction agent/script
- [ ] Extract insights from 482+ run folders
- [ ] Add to knowledge/analysis/ with cross-references
- [ ] Create archival process for old runs
- [ ] Document extraction pipeline

## Context
Run outputs contain valuable insights but are scattered:
- 482+ run folders with THOUGHTS.md, DECISIONS.md, LEARNINGS.md
- Knowledge exists in runs but not extracted to central store
- Run folders never cleaned up (unbounded growth)

## Approach
1. Design extraction workflow
2. Create extraction script
3. Process run folders in batches
4. Extract to knowledge/analysis/
5. Archive/compress old runs
6. Set up retention policy

## Related Files
- */runs/*/
- knowledge/analysis/
- .autonomous/analysis/

## Rollback Strategy
Archive (don't delete) run folders until extraction verified.
