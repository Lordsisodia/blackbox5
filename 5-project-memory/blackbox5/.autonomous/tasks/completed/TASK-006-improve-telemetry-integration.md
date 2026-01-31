# TASK-006: Improve Telemetry Integration

**Status:** completed
**Priority:** HIGH
**Created:** 2026-01-30
**Agent:** RALF

## Problem Statement

The RALF autonomous loop is not properly integrating with the telemetry system. While the `c` script now initializes telemetry at the start of each loop, the RALF agent itself should:

1. Record events during task execution
2. Track metrics (files read/written, commands executed, errors)
3. Report phase transitions
4. Capture decision points

## Current State

- Telemetry file is created at loop start via `telemetry.sh init`
- Telemetry file is marked complete at loop end via `telemetry.sh complete`
- BUT: No events or metrics are being recorded during execution

## Desired State

RALF should use the telemetry system throughout execution:

```bash
# During task execution
./telemetry.sh event "$TELEMETRY_FILE" "task_started" "TASK-001"
./telemetry.sh metric "$TELEMETRY_FILE" "files_read" 5
./telemetry.sh phase "$TELEMETRY_FILE" "task_selection" "complete"
```

## Acceptance Criteria

- [x] RALF records at least 3 events per loop
- [x] RALF tracks files_read, files_written, commands_executed metrics
- [x] RALF reports phase transitions (initialization → task_selection → execution → completion)
- [x] Telemetry data is viewable via `./telemetry.sh status`
- [x] Documentation updated in ralf.md

## Technical Notes

The telemetry script supports these commands:
- `init` - Create new telemetry file
- `event <file> <type> <data>` - Record an event
- `metric <file> <name> <value>` - Update a metric
- `phase <file> <phase> <status>` - Update phase status
- `complete <file>` - Mark run complete
- `status [file]` - View telemetry status

Location: `~/.blackbox5/2-engine/.autonomous/shell/telemetry.sh`

## Related

- Run logs: `5-project-memory/ralf-core/.autonomous/LOGS/`
- Telemetry data: `2-engine/.autonomous/.Autonomous/telemetry/`
- Previous tasks: TASK-001, TASK-002, TASK-003

## Completion

**Completed:** 2026-01-30T21:19:00Z
**Run Folder:** N/A - Documentation update
**Agent:** Agent-2.3
**Path Used:** Quick Flow
**Phase Gates:** N/A
**Decisions Recorded:** 0
