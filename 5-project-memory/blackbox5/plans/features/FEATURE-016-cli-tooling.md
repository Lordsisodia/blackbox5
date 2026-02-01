# Feature F-016: CLI Interface & Tooling Suite

**Status:** Planned
**Priority:** High
**Estimated Effort:** 150 minutes (human) / ~7 minutes (AI)
**Estimated Lines:** ~2,300 lines
**Type:** Operational Maturity

---

## Executive Summary

Provide a unified command-line interface for RALF operations, enabling operators to interact with the autonomous system without direct file manipulation. The CLI will provide commands for task management, queue inspection, system status, agent control, and configuration management.

**User Value:** Operators can manage RALF through intuitive commands instead of editing YAML files manually.

**MVP Scope:** Core commands for task/queue/agent operations, auto-completion, color output, help system.

---

## User Stories

### As a RALF Operator...
1. I want to view the current task queue so I can see what work is pending
2. I want to view system status so I can check if agents are healthy
3. I want to claim a task manually so I can intervene when needed
4. I want to view task details so I can understand what's being worked on
5. I want to restart an agent so I can recover from failures
6. I want to manage configuration so I can tune system behavior

---

## Technical Approach

### Architecture

```
ralf-cli/
├── ralf.py                 # Main CLI entry point
├── commands/
│   ├── __init__.py
│   ├── task.py            # Task commands (list, show, claim, complete)
│   ├── queue.py           # Queue commands (list, add, remove, reorder)
│   ├── agent.py           # Agent commands (status, start, stop, restart)
│   ├── config.py          # Config commands (get, set, validate, diff)
│   └── system.py          # System commands (health, metrics, logs)
├── lib/
│   ├── __init__.py
│   ├── output.py          # Output formatting (tables, colors, JSON)
│   ├── completion.py      # Shell auto-completion
│   └── context.py         # Context management (RALF_PROJECT_DIR, etc.)
└── tests/
    └── test_cli.py
```

### Technology Stack
- **Framework:** Click (Python CLI framework, already widely used)
- **Output:** Rich (terminal formatting, tables, progress bars)
- **Completion:** argcomplete or Click built-in completion
- **Config:** PyYAML (already used)

---

## Success Criteria

### Must-Have (P0)
- [ ] `ralf task list` displays current active tasks
- [ ] `ralf queue show` displays queue with priority scores
- [ ] `ralf agent status` shows planner/executor health
- [ ] `ralf system health` displays overall system status
- [ ] Color output for severity (red=error, yellow=warning, green=healthy)
- [ ] Help text for all commands (`--help` flag)

### Should-Have (P1)
- [ ] `ralf task show <task-id>` displays full task details
- [ ] `ralf task claim <task-id>` claims a task manually
- [ ] `ralf queue add <feature-id>` creates new task from backlog
- [ ] `ralf config get <key>` retrieves configuration value
- [ ] `ralf config set <key> <value>` updates configuration
- [ ] Auto-completion for bash/zsh
- [ ] JSON output mode for automation (`--output json`)

### Nice-to-Have (P2)
- [ ] `ralf agent start/stop/restart` controls agent lifecycle
- [ ] `ralf logs tail` displays recent logs
- [ ] `ralf metrics show` displays performance metrics
- [ ] Interactive mode with menu system
- [ ] Configuration file for CLI settings (`~/.ralf-cli.yaml`)

---

## Command Reference

### Task Commands
```bash
ralf task list                    # List active tasks
ralf task show <task-id>          # Show task details
ralf task claim <task-id>         # Claim a task
ralf task complete <task-id>      # Mark task complete
```

### Queue Commands
```bash
ralf queue show                   # Show queue with priorities
ralf queue add <feature-id>       # Add task from backlog
ralf queue remove <task-id>       # Remove task from queue
ralf queue reorder                # Reorder by priority
```

### Agent Commands
```bash
ralf agent status                 # Show agent status
ralf agent start [planner|executor]  # Start agent
ralf agent stop [planner|executor]   # Stop agent
ralf agent restart [planner|executor] # Restart agent
```

### Config Commands
```bash
ralf config get <key>             # Get config value
ralf config set <key> <value>     # Set config value
ralf config validate              # Validate configuration
ralf config diff [env]            # Compare environments
```

### System Commands
```bash
ralf system health                # Show system health
ralf system metrics               # Show performance metrics
ralf system logs [--tail]         # View system logs
ralf system version               # Show version info
```

---

## Integration Points

### Data Sources (Read)
- `.autonomous/communications/queue.yaml` - Task queue
- `.autonomous/communications/events.yaml` - Event log
- `.autonomous/communications/heartbeat.yaml` - Agent health
- `.autonomous/tasks/active/` - Active task files
- `2-engine/.autonomous/config/` - Configuration files

### Data Destinations (Write)
- `.autonomous/communications/queue.yaml` - Queue updates
- `.autonomous/communications/events.yaml` - Event logging
- `.autonomous/tasks/active/` - Task creation/modification
- `2-engine/.autonomous/config/` - Configuration updates

### Existing Components Used
- `ConfigManagerV2` (F-015) for configuration operations
- `heartbeat.yaml` for agent status

---

## Dependencies

**Required:**
- Python 3.8+
- Click (`pip install click`)
- Rich (`pip install rich`)

**Optional:**
- argcomplete (`pip install argcomplete`) for shell completion

---

## File Structure

```
2-engine/.autonomous/
├── cli/
│   ├── ralf.py                 # 80 lines - Main entry point
│   ├── commands/
│   │   ├── __init__.py         # 20 lines
│   │   ├── task.py            # 280 lines - Task commands
│   │   ├── queue.py           # 260 lines - Queue commands
│   │   ├── agent.py           # 240 lines - Agent commands
│   │   ├── config.py          # 320 lines - Config commands
│   │   └── system.py          # 220 lines - System commands
│   └── lib/
│       ├── __init__.py         # 20 lines
│       ├── output.py          # 280 lines - Formatting utilities
│       ├── completion.py      # 180 lines - Auto-completion
│       └── context.py         # 140 lines - Context management
└── config/
    └── cli-config.yaml         # 80 lines - CLI settings

operations/.docs/
└── cli-guide.md                # 650 lines - User guide

plans/features/
└── FEATURE-016-cli-tooling.md  # This file
```

**Total Estimated Lines:** ~2,330 lines

---

## Implementation Plan

### Phase 1: Core CLI Framework (P0)
1. Create main CLI entry point (`ralf.py`)
2. Implement `ralf task list` command
3. Implement `ralf queue show` command
4. Implement `ralf agent status` command
5. Implement `ralf system health` command
6. Add color output and table formatting

### Phase 2: Enhanced Commands (P1)
7. Implement task detail/show command
8. Implement queue management commands (add, remove)
9. Implement config get/set commands
10. Add JSON output mode
11. Implement auto-completion

### Phase 3: Advanced Features (P2)
12. Implement agent control commands (start, stop, restart)
13. Implement logs tail command
14. Implement metrics display
15. Add interactive mode

---

## Testing Strategy

### Unit Tests
- Test each command with mock data
- Test output formatting (table, JSON)
- Test error handling (invalid input, missing files)

### Integration Tests
- Test with real queue.yaml
- Test with real heartbeat.yaml
- Test task creation/modification

### Manual Testing
- Verify all commands work from command line
- Test auto-completion in bash/zsh
- Verify color output in different terminals

---

## Rollout Plan

### Phase 1 (Loop 30): Silent Mode
- Implement CLI framework
- Test internally with manual commands
- Document usage

### Phase 2 (Loop 31): Parallel Mode
- Install CLI in development environment
- Train operators on usage
- Gather feedback

### Phase 3 (Loop 32+): Full Adoption
- Default to CLI for all operations
- Deprecate direct YAML file editing
- Add advanced features (interactive mode)

---

## Risk Assessment

**Risk 1: Breaking Changes to Communication Files**
- **Probability:** Medium
- **Impact:** High
- **Mitigation:** Extensive testing, backup files created before writes

**Risk 2: CLI Dependency Availability**
- **Probability:** Low
- **Impact:** Medium
- **Mitigation:** Click and Rich are mature packages, document installation clearly

**Risk 3: Shell Compatibility**
- **Probability:** Medium
- **Impact:** Low
- **Mitigation:** Support bash and zsh, document known limitations

---

## Effort Estimation

**Component Breakdown:**
- CLI framework (main, context): 200 lines (~5 min)
- Task commands: 280 lines (~6 min)
- Queue commands: 260 lines (~6 min)
- Agent commands: 240 lines (~5 min)
- Config commands: 320 lines (~7 min)
- System commands: 220 lines (~5 min)
- Output library: 280 lines (~6 min)
- Completion: 180 lines (~4 min)
- Documentation: 650 lines (~12 min)
- Feature spec: 250 lines (~5 min)

**Total:** ~2,880 lines → ~8.5 minutes at 337 LPM

**Buffer:** Add 20% for testing and refinement → ~10 minutes

---

## Success Metrics

- **Adoption:** CLI used for 90% of operations (vs direct file editing)
- **Efficiency:** Task inspection time reduced by 50%
- **Satisfaction:** Operators rate CLI 4+ out of 5
- **Reliability:** 99%+ command success rate

---

**Feature Spec Complete** ✅
**Ready for Implementation:** Loop 29-30
