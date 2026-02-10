# BlackBox5 Autonomous Improvement System

## Overview

The BlackBox5 Autonomous Improvement System is a self-improving workflow that runs every 20 minutes to analyze, prioritize, and improve the BlackBox5 codebase using a coordinated team of specialized AI agents.

## Architecture

```
Cron Job (every 20 min)
    ↓
Improvement Script
    ↓
┌─────────────────────────────────────┐
│ 1. Task Analyzer                   │
│    - Reads active tasks            │
│    - Analyzes metadata             │
│    - Sorts by priority             │
│    - Generates prioritized list    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. Improvement Plan Generator      │
│    - Creates improvement plans      │
│    - Defines acceptance criteria    │
│    - Estimates complexity & time    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. Agent Protocol Coordinator       │
│    - Spawns specialized agents      │
│    - Routes tasks to agents         │
│    - Coordinates execution          │
│    - Collects results               │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. Agent Team Execution             │
│    - Architect: Analysis & design   │
│    - Engineering: Implementation    │
│    - Testing: Quality assurance     │
│    - Verification: Validation        │
│    - Scribe: Documentation          │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 5. Reporting & GitHub Push           │
│    - Generates comprehensive report │
│    - Updates metrics                │
│    - Pushes changes to GitHub       │
└─────────────────────────────────────┘
```

## Components

### 1. Core Scripts

| Script | Purpose |
|--------|---------|
| `autonomous/improve-blackbox5.sh` | Main cron job entry point |
| `autonomous/task-analyzer.py` | Analyzes and prioritizes tasks |
| `autonomous/improvement-plan-generator.py` | Generates improvement plans |
| `autonomous/agent-protocol.py` | Coordinates agent team |
| `agents/moltbot-autonomous/mob-bot-spawner.py` | Spawns Claude Code CLI agents |

### 2. Configuration

| File | Purpose |
|------|---------|
| `config/claude-agent-team.yaml` | Agent team configuration |
| `dashboard-ui/autonomous-improvement.js` | Dashboard widget |

### 3. Data & Logs

| Directory | Contents |
|-----------|----------|
| `.autonomous/logs/` | Improvement cycle logs |
| `.autonomous/metrics/` | Performance metrics |
| `.autonomous/reports/` | Detailed improvement reports |
| `.autonomous/improvement-log.md` | Main activity log |

## Agent Team

### Architect Agent
- **Role:** Analyzes codebase, identifies improvements
- **Focus:** Architecture patterns, system design, best practices
- **Tools:** read, write, edit, exec, web_search

### Engineering Agent
- **Role:** Implements improvements, refactors code
- **Focus:** Code implementation, refactoring, tests
- **Tools:** read, write, edit, exec

### Senior Engineering Agent
- **Role:** Handles complex, high-priority implementations
- **Focus:** Performance, security, multi-component integration
- **Tools:** read, write, edit, exec

### Testing Agent
- **Role:** Writes tests, validates quality
- **Focus:** Unit, integration, e2e tests, coverage
- **Tools:** read, write, edit, exec

### Verification Agent
- **Role:** Checks results, confirms fixes work
- **Focus:** Acceptance criteria, smoke tests, validation
- **Tools:** read, exec, web_search

### Scribe Agent
- **Role:** Documents everything done
- **Focus:** Documentation, reports, knowledge base
- **Tools:** read, write, edit

## Task Prioritization

Tasks are prioritized based on:

1. **Priority Level** (high=30, medium=20, low=10)
2. **Age** (older tasks get bonus points)
3. **Blocking Status** (blocking tasks get +15)
4. **Complexity** (easy tasks get +10 for quick wins)
5. **Status** (in-progress gets +10, blocked gets -20)

### Priority Levels

- **High Priority:**
  - Tasks marked as "high" in metadata
  - Tasks older than 72 hours
  - Tasks blocking other work

- **Medium Priority:**
  - Tasks marked as "medium"
  - Tasks 24-72 hours old

- **Quick Wins:**
  - Tasks that can be done < 30 minutes
  - Tasks with clear, simple requirements

- **Low Priority:**
  - Newer tasks
  - Tasks with unclear requirements
  - Tasks marked as "low" priority

## Metrics Tracking

The system tracks the following metrics:

| Metric | Description |
|--------|-------------|
| Tasks Analyzed | Count of tasks analyzed in each cycle |
| Tasks Completed | Number of tasks completed |
| Agents Used | Number of agents deployed |
| Success Rate | Percentage of successful task completions |
| Agent Reports | Detailed reports from each agent |

## Dashboard Integration

The autonomous improvement system includes a dashboard widget that displays:

- Current cycle status (running/idle/error)
- Improvement metrics (tasks, agents, success rate)
- Agent utilization (which agents are active)
- Recent improvement cycles
- Top priority tasks

To access the dashboard:
1. Ensure the dashboard is running
2. The autonomous improvement widget auto-initializes
3. Data refreshes every 30 seconds

## Setup Instructions

### Initial Setup

1. **Run the setup script:**
   ```bash
   bash /opt/blackbox5/scripts/setup-autonomous-loops.sh
   ```

2. **Verify the setup:**
   ```bash
   bash /opt/blackbox5/scripts/test-autonomous-loops.sh
   ```

3. **Monitor the first cycle:**
   ```bash
   tail -f /opt/blackbox5/.autonomous/improvement-log.md
   ```

### Manual Testing

To test individual components:

```bash
# Test task analyzer
python3 /opt/blackbox5/autonomous/task-analyzer.py

# Test improvement plan generator
python3 /opt/blackbox5/autonomous/improvement-plan-generator.py

# Test agent protocol
python3 /opt/blackbox5/autonomous/agent-protocol.py

# Test mob bot spawner
python3 /opt/blackbox5/agents/moltbot-autonomous/mob-bot-spawner.py

# Run full cycle
bash /opt/blackbox5/autonomous/improve-blackbox5.sh
```

## File Structure

```
/opt/blackbox5/
├── autonomous/
│   ├── improve-blackbox5.sh          # Main cron job script
│   ├── task-analyzer.py              # Task analysis
│   ├── improvement-plan-generator.py # Plan generation
│   └── agent-protocol.py             # Agent coordination
├── agents/
│   └── moltbot-autonomous/
│       └── mob-bot-spawner.py        # Agent spawner
├── config/
│   └── claude-agent-team.yaml        # Agent team config
├── dashboard-ui/
│   └── autonomous-improvement.js     # Dashboard widget
├── scripts/
│   ├── setup-autonomous-loops.sh     # Setup script
│   └── test-autonomous-loops.sh      # Testing script
└── .autonomous/
    ├── logs/                         # Cycle logs
    ├── metrics/                      # Performance metrics
    ├── reports/                      # Detailed reports
    ├── improvement-log.md            # Main activity log
    └── README.md                     # This file
```

## Troubleshooting

### Cron Job Not Running

Check if cron is installed and configured:
```bash
# Check cron service
sudo systemctl status cron

# Check crontab
crontab -l

# Check cron logs
sudo grep CRON /var/log/syslog
```

### Task Analyzer Fails

Check the tasks directory:
```bash
ls -la /opt/blackbox5/5-project-memory/blackbox5/tasks/active/
```

### Agent Protocol Fails

Check for priorized tasks:
```bash
cat /opt/blackbox5/.autonomous/prioritized-tasks.json
```

### GitHub Push Fails

Check git configuration:
```bash
cd /opt/blackbox5
git remote -v
git status
```

## Monitoring

### View Logs

```bash
# Main improvement log
tail -f /opt/blackbox5/.autonomous/improvement-log.md

# Individual cycle logs
ls /opt/blackbox5/.autonomous/logs/
```

### View Metrics

```bash
# Latest cycle metrics
cat /opt/blackbox5/.autonomous/metrics/latest-cycle.json

# All metrics
ls /opt/blackbox5/.autonomous/metrics/
```

### View Reports

```bash
# Latest report
ls -t /opt/blackbox5/.autonomous/reports/ | head -1
cat /opt/blackbox5/.autonomous/reports/$(ls -t /opt/blackbox5/.autonomous/reports/ | head -1)
```

## Best Practices

1. **Review Improvement Plans:** Always review the improvement plan before execution
2. **Monitor Early:** Closely monitor the first few cycles
3. **Adjust Prioritization:** Tune task prioritization based on results
4. **Check Metrics:** Regularly review metrics to identify trends
5. **Update Documentation:** Keep the system documentation up to date

## Safety Features

- **Duplicate Prevention:** PID file prevents multiple concurrent cycles
- **Error Handling:** Errors are logged and don't crash the system
- **Rollback:** Git makes it easy to revert changes
- **Manual Override:** Can disable cron job anytime

## Future Enhancements

- [ ] Add more sophisticated task dependency resolution
- [ ] Implement agent collaboration protocols
- [ ] Add performance benchmarking
- [ ] Create task templates for common improvements
- [ ] Add real-time agent status updates
- [ ] Implement automatic rollback on failures

## Contributing

To contribute improvements to the autonomous system:

1. Create a feature branch
2. Make your changes
3. Test with `test-autonomous-loops.sh`
4. Submit a pull request

## License

Part of the BlackBox5 project. See main project license for details.

---

**Generated by BlackBox5 Autonomous Improvement System**
