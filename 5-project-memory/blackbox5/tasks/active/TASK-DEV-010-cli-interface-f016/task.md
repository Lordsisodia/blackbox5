# TASK-1738375000: Implement Feature F-016 (CLI Interface & Tooling Suite)

**Type:** implement
**Priority:** high
**Status:** in_progress
**Created:** 2026-02-01T16:01:00Z
**Estimated Lines:** 2330

## Lines-Per-Minute Estimation Formula

**Based on executor throughput analysis (runs 58-63):**
- Mean throughput: 346 lines/min (updated 2026-02-01, Loop 29)
- Standard deviation: 172 lines/min
- Coefficient of variation: 55% (varies by feature complexity)

**Formula:**
```
Estimated Minutes = Estimated Lines / 346
Estimated Minutes = 2330 / 346 = 6.7 minutes
```

**Accuracy:** 9% error vs 95% error (time-based) - 23x improvement

## Objective

Implement a unified command-line interface for RALF operations, enabling operators to interact with the autonomous system through intuitive commands instead of direct file manipulation.

## Context

This feature provides the primary operator interface for RALF. Currently, operators must manually edit YAML files to manage tasks, queues, and configuration. A CLI will significantly improve operational efficiency and reduce errors.

Feature spec: `plans/features/FEATURE-016-cli-tooling.md`

## Success Criteria

### Must-Have (P0)
- [x] `ralf task list` displays current active tasks ✅ IMPLEMENTED
- [x] `ralf queue show` displays queue with priority scores ✅ IMPLEMENTED
- [x] `ralf agent status` shows planner/executor health ✅ IMPLEMENTED
- [x] `ralf system health` displays overall system status ✅ IMPLEMENTED
- [x] Color output for severity (red=error, yellow=warning, green=healthy) ✅ IMPLEMENTED
- [x] Help text for all commands (`--help` flag) ✅ IMPLEMENTED

### Should-Have (P1)
- [x] `ralf task show <task-id>` displays full task details ✅ IMPLEMENTED
- [ ] `ralf task claim <task-id>` claims a task manually
- [ ] `ralf queue add <feature-id>` creates new task from backlog
- [ ] `ralf config get <key>` retrieves configuration value
- [ ] `ralf config set <key> <value>` updates configuration
- [ ] Auto-completion for bash/zsh
- [x] JSON output mode for automation (`--output json`) ✅ IMPLEMENTED
- [ ] JSON output mode for automation (`--output json`)

### Nice-to-Have (P2)
- [ ] `ralf agent start/stop/restart` controls agent lifecycle
- [ ] `ralf logs tail` displays recent logs
- [ ] `ralf metrics show` displays performance metrics
- [ ] Interactive mode with menu system
- [ ] Configuration file for CLI settings (`~/.ralf-cli.yaml`)

## Approach

1. Create CLI framework structure in `2-engine/.autonomous/cli/`
2. Implement main entry point (`ralf.py`) with Click
3. Build core command groups (task, queue, agent, system, config)
4. Implement output formatting library with Rich
5. Add context management for RALF environment
6. Integrate with existing communication files (queue.yaml, heartbeat.yaml, events.yaml)
7. Add auto-completion support
8. Create comprehensive documentation

**Dependencies:**
- Click (Python CLI framework)
- Rich (terminal formatting)
- PyYAML (already used)

## Files to Create

- `2-engine/.autonomous/cli/ralf.py`: Main entry point (~80 lines)
- `2-engine/.autonomous/cli/commands/__init__.py`: Command initialization (~20 lines)
- `2-engine/.autonomous/cli/commands/task.py`: Task commands (~280 lines)
- `2-engine/.autonomous/cli/commands/queue.py`: Queue commands (~260 lines)
- `2-engine/.autonomous/cli/commands/agent.py`: Agent commands (~240 lines)
- `2-engine/.autonomous/cli/commands/config.py`: Config commands (~320 lines)
- `2-engine/.autonomous/cli/commands/system.py`: System commands (~220 lines)
- `2-engine/.autonomous/cli/lib/__init__.py`: Library initialization (~20 lines)
- `2-engine/.autonomous/cli/lib/output.py`: Output formatting (~280 lines)
- `2-engine/.autonomous/cli/lib/completion.py`: Auto-completion (~180 lines)
- `2-engine/.autonomous/cli/lib/context.py`: Context management (~140 lines)
- `2-engine/.autonomous/config/cli-config.yaml`: CLI settings (~80 lines)
- `operations/.docs/cli-guide.md`: User guide (~650 lines)

## Dependencies

None - This is a standalone feature that integrates with existing communication files.

## Notes

- Use ConfigManagerV2 from F-015 for configuration operations
- Read from `.autonomous/communications/` files for data
- Write updates to same files (with backup before modifications)
- Ensure all commands have proper error handling
- Test with real queue.yaml and heartbeat.yaml files
- Use colors consistently: red=error, yellow=warning, green=healthy

---

## Progress Update (2026-02-12)

### Completed ✅

**Core CLI Framework:**
- [x] Main entry point: `/opt/blackbox5/2-engine/.autonomous/cli/ralf.py` (~450 lines)
- [x] Installed as `/usr/local/bin/ralf` - available from any directory
- [x] Version 1.0.0 with Click framework
- [x] Auto-detection of BlackBox5 root directory
- [x] Color output with colorama

**Implemented Commands (P0 + Partial P1):**
- [x] `ralf task list` - List active tasks with status/priority
- [x] `ralf task show <task-id>` - Show full task details
- [x] `ralf queue show` - Display queue sorted by priority
- [x] `ralf agent status` - Show planner/executor health
- [x] `ralf system health` - Overall system status with health score
- [x] All commands support `--output json` for machine-readable output
- [x] All commands have `--help` documentation

**Documentation:**
- [x] Comprehensive README.md at `/opt/blackbox5/2-engine/.autonomous/cli/README.md`
- [x] Usage examples for all commands
- [x] Troubleshooting guide
- [x] Color scheme reference

**Testing:**
- [x] All P0 commands tested and working
- [x] Works from any directory (auto-detects BlackBox5 root)
- [x] Tested with real queue.yaml and heartbeat.yaml files
- [x] JSON output mode verified

### Remaining (P1 & P2)

**Missing P1 Features:**
- [ ] `ralf task claim <task-id>` - Claim a task manually
- [ ] `ralf task complete <task-id>` - Mark task complete
- [ ] `ralf queue add <feature-id>` - Add task from backlog
- [ ] `ralf queue remove <task-id>` - Remove task from queue
- [ ] `ralf queue reorder` - Reorder by priority
- [ ] `ralf config get <key>` - Retrieve configuration
- [ ] `ralf config set <key> <value>` - Update configuration
- [ ] `ralf config validate` - Validate configuration
- [ ] `ralf config diff [env]` - Compare environments
- [ ] Bash/zsh auto-completion

**Missing P2 Features:**
- [ ] `ralf agent start/stop/restart` - Agent lifecycle control
- [ ] `ralf logs tail` - Display recent logs
- [ ] `ralf metrics show` - Performance metrics
- [ ] `ralf system version` - Version info
- [ ] Interactive mode with menu system
- [ ] Configuration file for CLI settings (`~/.ralf-cli.yaml`)

### Implementation Notes

**Architecture Decisions:**
- Used Click framework for CLI (standard choice)
- Used colorama for cross-platform color support (instead of Rich)
- Single-file implementation (~450 lines) instead of multi-file structure
- Auto-detection of BlackBox5 root from current directory
- Fallback to `~/.blackbox5` when not in BlackBox5 tree

**File Locations:**
- CLI script: `/opt/blackbox5/2-engine/.autonomous/cli/ralf.py`
- Installed as: `/usr/local/bin/ralf`
- Documentation: `/opt/blackbox5/2-engine/.autonomous/cli/README.md`
- Data files (auto-detected):
  - Queue: `.autonomous/agents/communications/queue.yaml`
  - Heartbeat: `.autonomous/agents/communications/heartbeat.yaml`

**Current Status:**
- P0 (Must-Have): 100% complete ✅
- P1 (Should-Have): ~30% complete (task show + JSON output)
- P2 (Nice-to-Have): 0% complete

**Production Readiness:**
The CLI is ready for use for core operations (viewing tasks, queue, agents, system health). Additional P1/P2 features can be added incrementally as needed.
