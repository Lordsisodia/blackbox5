# PLAN.md: CLI Interface & Tooling Suite (Feature F-016)

**Task:** TASK-1738375000 - CLI Interface & Tooling Suite
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 2-3 days
**Estimated Lines:** 2330
**Importance:** 85 (High)

---

## 1. First Principles Analysis

### Why Does RALF Need a CLI?

1. **Operational Efficiency**: Currently operators must manually edit YAML files to manage tasks, queues, and configuration. This is error-prone and slow.
2. **Reduced Cognitive Load**: A CLI provides discoverable commands instead of requiring knowledge of file structures and formats.
3. **Automation Enablement**: CLI enables scripting and integration with other tools.
4. **User Experience**: Rich terminal output with colors and formatting improves situational awareness.

### What Happens Without a CLI?

- **Barrier to Entry**: New users struggle to interact with RALF
- **Manual Errors**: Direct file editing leads to YAML syntax errors and invalid states
- **Slow Operations**: Checking task status requires opening and reading multiple files
- **No Standardization**: Each user develops their own ad-hoc scripts

### How Should the CLI Work?

1. **Unified Entry Point**: Single `ralf` command with subcommands
2. **Consistent Interface**: All commands follow same patterns (flags, output formats)
3. **Rich Output**: Use Rich library for tables, colors, and formatting
4. **Integration**: Read/write existing communication files (queue.yaml, heartbeat.yaml)
5. **Extensibility**: Easy to add new commands and features

---

## 2. Current State Assessment

### Existing Infrastructure

| Component | Location | Status |
|-----------|----------|--------|
| Communication Files | `.autonomous/communications/` | YAML-based, no CLI access |
| ConfigManagerV2 | `lib/config_manager_v2.py` | Available for config operations |
| Task System | `tasks/active/`, `tasks/completed/` | File-based, manual access only |
| Queue System | `communications/queue.yaml` | YAML-based, no CLI |
| Agent Heartbeat | `communications/heartbeat.yaml` | YAML-based, no CLI |

### Current Pain Points

1. **No unified interface** - Users must know file locations and formats
2. **No colorized output** - Raw YAML is hard to scan quickly
3. **No command discovery** - Users must read documentation to know what's possible
4. **No automation support** - Cannot easily script RALF operations

---

## 3. Proposed Solution

### CLI Architecture

```
ralf
├── task          # Task management commands
│   ├── list      # List active tasks
│   ├── show      # Show task details
│   └── claim     # Claim a task manually
├── queue         # Queue management
│   ├── show      # Display queue with priorities
│   └── add       # Create task from backlog
├── agent         # Agent management
│   ├── status    # Show planner/executor health
│   └── logs      # Display recent logs
├── system        # System operations
│   ├── health    # Overall system status
│   └── metrics   # Performance metrics
└── config        # Configuration
    ├── get       # Retrieve config value
    └── set       # Update config value
```

### Command Specifications

**Core Commands (P0 - Must Have):**

| Command | Description | Output |
|---------|-------------|--------|
| `ralf task list` | List active tasks | Table with ID, title, priority, status |
| `ralf queue show` | Display queue | Priority-ordered list with scores |
| `ralf agent status` | Agent health | Status indicators (green/yellow/red) |
| `ralf system health` | System status | Overall health with component status |

**Extended Commands (P1 - Should Have):**

| Command | Description | Output |
|---------|-------------|--------|
| `ralf task show <id>` | Task details | Full task information |
| `ralf task claim <id>` | Claim task | Confirmation with task assigned |
| `ralf queue add <feature>` | Add to queue | Confirmation with queue position |
| `ralf config get <key>` | Get config | Value or "not set" |
| `ralf config set <key> <val>` | Set config | Confirmation |

**Advanced Commands (P2 - Nice to Have):**

| Command | Description |
|---------|-------------|
| `ralf agent start/stop/restart` | Control agent lifecycle |
| `ralf logs tail` | Stream recent logs |
| `ralf metrics show` | Display performance metrics |

### Output Formatting

**Color Scheme:**
- Green (#00FF00): Healthy, success, completed
- Yellow (#FFFF00): Warning, pending, in-progress
- Red (#FF0000): Error, critical, failed
- Blue (#0000FF): Info, neutral status

**Output Modes:**
- Default: Rich formatted tables/panels
- `--output json`: Machine-readable JSON
- `--output yaml`: YAML format
- `--no-color`: Plain text without colors

---

## 4. Implementation Plan

### Phase 1: CLI Framework (Day 1)

**Files to Create:**
1. `2-engine/.autonomous/cli/ralf.py` - Main entry point (~80 lines)
2. `2-engine/.autonomous/cli/__init__.py` - Package initialization
3. `2-engine/.autonomous/cli/commands/__init__.py` - Command registration

**Key Features:**
- Click framework setup
- Command group structure
- Global options (--output, --no-color, --config)
- Help text generation

### Phase 2: Core Commands (Day 1-2)

**Files to Create:**
1. `2-engine/.autonomous/cli/commands/task.py` - Task commands (~280 lines)
2. `2-engine/.autonomous/cli/commands/queue.py` - Queue commands (~260 lines)
3. `2-engine/.autonomous/cli/commands/agent.py` - Agent commands (~240 lines)
4. `2-engine/.autonomous/cli/commands/system.py` - System commands (~220 lines)

**Implementation Details:**
- Read from `.autonomous/communications/` files
- Format output with Rich tables/panels
- Handle errors gracefully
- Backup files before modifications

### Phase 3: Output Library (Day 2)

**Files to Create:**
1. `2-engine/.autonomous/cli/lib/__init__.py` - Library initialization
2. `2-engine/.autonomous/cli/lib/output.py` - Output formatting (~280 lines)
3. `2-engine/.autonomous/cli/lib/context.py` - Context management (~140 lines)

**Features:**
- Table formatting with Rich
- Color application based on severity
- JSON/YAML output modes
- Progress indicators

### Phase 4: Extended Features (Day 2-3)

**Files to Create:**
1. `2-engine/.autonomous/cli/commands/config.py` - Config commands (~320 lines)
2. `2-engine/.autonomous/cli/lib/completion.py` - Auto-completion (~180 lines)
3. `2-engine/.autonomous/config/cli-config.yaml` - CLI settings (~80 lines)

**Features:**
- Config get/set using ConfigManagerV2
- Bash/zsh auto-completion
- CLI configuration file

### Phase 5: Documentation (Day 3)

**Files to Create:**
1. `operations/.docs/cli-guide.md` - User guide (~650 lines)

**Documentation Includes:**
- Installation instructions
- Command reference
- Usage examples
- Configuration options
- Troubleshooting

---

## 5. Files to Create/Modify

### New Files

| File | Lines | Purpose |
|------|-------|---------|
| `2-engine/.autonomous/cli/ralf.py` | 80 | Main CLI entry point |
| `2-engine/.autonomous/cli/__init__.py` | 10 | Package init |
| `2-engine/.autonomous/cli/commands/__init__.py` | 20 | Command registration |
| `2-engine/.autonomous/cli/commands/task.py` | 280 | Task management commands |
| `2-engine/.autonomous/cli/commands/queue.py` | 260 | Queue management commands |
| `2-engine/.autonomous/cli/commands/agent.py` | 240 | Agent status commands |
| `2-engine/.autonomous/cli/commands/system.py` | 220 | System health commands |
| `2-engine/.autonomous/cli/commands/config.py` | 320 | Configuration commands |
| `2-engine/.autonomous/cli/lib/__init__.py` | 10 | Library init |
| `2-engine/.autonomous/cli/lib/output.py` | 280 | Output formatting library |
| `2-engine/.autonomous/cli/lib/completion.py` | 180 | Auto-completion support |
| `2-engine/.autonomous/cli/lib/context.py` | 140 | Context management |
| `2-engine/.autonomous/config/cli-config.yaml` | 80 | CLI configuration |
| `operations/.docs/cli-guide.md` | 650 | User documentation |

**Total Estimated Lines:** 2330

### Dependencies

- `click` - Python CLI framework
- `rich` - Terminal formatting
- `pyyaml` - Already used in project

---

## 6. Success Criteria

### P0 (Must Have)
- [ ] `ralf task list` displays current active tasks
- [ ] `ralf queue show` displays queue with priority scores
- [ ] `ralf agent status` shows planner/executor health
- [ ] `ralf system health` displays overall system status
- [ ] Color output for severity (red=error, yellow=warning, green=healthy)
- [ ] Help text for all commands (`--help` flag)

### P1 (Should Have)
- [ ] `ralf task show <task-id>` displays full task details
- [ ] `ralf task claim <task-id>` claims a task manually
- [ ] `ralf queue add <feature-id>` creates new task from backlog
- [ ] `ralf config get <key>` retrieves configuration value
- [ ] `ralf config set <key> <value>` updates configuration
- [ ] Auto-completion for bash/zsh
- [ ] JSON output mode for automation (`--output json`)

### P2 (Nice to Have)
- [ ] `ralf agent start/stop/restart` controls agent lifecycle
- [ ] `ralf logs tail` displays recent logs
- [ ] `ralf metrics show` displays performance metrics
- [ ] Interactive mode with menu system
- [ ] Configuration file for CLI settings (`~/.ralf-cli.yaml`)

---

## 7. Rollback Strategy

If CLI causes issues:

1. **Immediate**: CLI is additive - doesn't modify existing files
2. **Short-term**: Remove CLI directory to disable
3. **Full**: No changes to existing system, safe to delete

**Rollback Commands:**
```bash
rm -rf 2-engine/.autonomous/cli/
rm -f 2-engine/.autonomous/config/cli-config.yaml
```

---

## 8. Estimated Timeline

| Phase | Duration | Lines |
|-------|----------|-------|
| Phase 1: CLI Framework | 4 hours | 110 |
| Phase 2: Core Commands | 8 hours | 1000 |
| Phase 3: Output Library | 4 hours | 430 |
| Phase 4: Extended Features | 6 hours | 580 |
| Phase 5: Documentation | 4 hours | 650 |
| Testing & Polish | 4 hours | - |
| **Total** | **30 hours (2-3 days)** | **2770** |

---

## 9. Key Design Decisions

### Decision 1: Click vs Argparse
**Choice:** Click framework
**Rationale:** Better help generation, command groups, type validation, industry standard

### Decision 2: Rich vs Plain Output
**Choice:** Rich library with fallback
**Rationale:** Superior formatting, tables, panels, but `--no-color` for compatibility

### Decision 3: File Structure
**Choice:** Separate commands/ and lib/ directories
**Rationale:** Clean separation of concerns, easy to extend

### Decision 4: Integration Pattern
**Choice:** Read/write existing YAML files directly
**Rationale:** No database needed, works with existing infrastructure, backup before modify

---

*Plan created based on Feature F-016 specification and task requirements*
