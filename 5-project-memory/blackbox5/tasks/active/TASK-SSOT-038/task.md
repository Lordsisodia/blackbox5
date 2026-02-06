# TASK-SSOT-038: Standardize Template System

**Status:** pending
**Priority:** LOW
**Created:** 2026-02-06
**Parent:** SSOT Violations - Run Folder Accumulation

## Objective
Implement an archival policy and automated cleanup system for old run folders to reduce storage waste and improve operational performance.

## Success Criteria
- [ ] Archival policy defined in `archive-policy.yaml`
- [ ] Archival script created to compress old runs into monthly archives
- [ ] Archive index created for searchable run lookup
- [ ] Cleanup schedule configured (weekly cron job)
- [ ] Restore function implemented for retrieving archived runs
- [ ] Policy keeps last 50 runs and all active task runs
- [ ] Runs archived after 30 days, deleted after 365 days
- [ ] Special tags (milestone, important, reference) preserved

## Context
Run folders accumulate over time, consuming disk space and slowing down directory operations. There is currently no archival policy, leading to storage waste, performance issues with directory listings, clutter making it hard to find relevant runs, and unclear retention guidelines.

## Approach
1. Define archival policy with retention rules and compression settings
2. Create archival script using tarfile and gzip for monthly compression
3. Build archive index with run metadata for searchability
4. Schedule weekly cleanup via cron
5. Implement restore function to extract specific runs from archives

## Estimated Effort
2-3 hours

## Rollback Strategy
If archival causes issues, restore runs from archives using the restore function and adjust archival policy to be more conservative with retention periods.
