# TASK-SSOT-038: Standardize Template System - Run Archival Policy

**Status:** completed
**Priority:** LOW
**Created:** 2026-02-06
**Completed:** 2026-02-07
**Parent:** SSOT Violations - Run Folder Accumulation

## Objective
Implement an archival policy and automated cleanup system for old run folders to reduce storage waste and improve operational performance.

## Success Criteria
- [x] Archival policy defined in `archive-policy.yaml`
- [x] Archival script created to compress old runs into monthly archives
- [x] Archive index created for searchable run lookup
- [x] Cleanup schedule configured (weekly cron job)
- [x] Restore function implemented for retrieving archived runs
- [x] Policy keeps last 50 runs and all active task runs
- [x] Runs archived after 30 days, deleted after 365 days
- [x] Special tags (milestone, important, reference) preserved

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

## Implementation Results

### Files Created

1. **Archive Policy** (`~/.blackbox5/5-project-memory/blackbox5/.autonomous/archive-policy.yaml`)
   - Retention rules: keep last 50 runs, archive after 30 days, delete after 365 days
   - Special tag preservation (milestone, important, reference, audit, compliance)
   - Active task run protection
   - Compression settings (tar.gz, level 6)
   - Monthly archive grouping

2. **Archival Script** (`~/.blackbox5/bin/archive-runs.sh`)
   - Commands: `archive`, `restore <project> <run-id>`, `list <project>`, `status`
   - Automatically creates archive directories and index files
   - Respects preserve tags and active task associations
   - Generates archival logs and reports
   - Cross-platform compatible (macOS/Linux)

3. **Cron Setup Script** (`~/.blackbox5/bin/setup-archive-cron.sh`)
   - Installs weekly cron job (Sundays at 2:00 AM)
   - Configurable schedule
   - Logs to `~/.blackbox5/5-project-memory/.archive-cron.log`

### Test Results

Tested on blackbox5 project:
- Found 199 run directories across all agent types
- Correctly identified runs within keep_last limit (50 per agent)
- Verified preserve tag detection (milestone, important, etc.)
- Confirmed active task protection
- Archive directory structure created: `~/.blackbox5/5-project-memory/blackbox5/.autonomous/archive/`

### Usage

```bash
# Check archive status across all projects
~/.blackbox5/bin/archive-runs.sh status

# Run archival manually
~/.blackbox5/bin/archive-runs.sh archive

# List archived runs for a project
~/.blackbox5/bin/archive-runs.sh list blackbox5

# Restore a specific run
~/.blackbox5/bin/archive-runs.sh restore blackbox5 run-0001

# Setup automated weekly archival
~/.blackbox5/bin/setup-archive-cron.sh
```

## Rollback Strategy
If archival causes issues, restore runs from archives using the restore function and adjust archival policy to be more conservative with retention periods.
