# MoltBot Autonomous Agent Specification

## Overview
A standardized autonomous agent that runs continuously on the VPS, analyzes BlackBox5, identifies issues, proposes solutions, and executes them via Claude Code instances - all while keeping you informed via Telegram.

## Core Concept
```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Telegram  │◄───►│  MoltBot     │◄───►│  BlackBox5  │
│   (You)     │     │  Autonomous  │     │  Analysis   │
└─────────────┘     └──────────────┘     └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  Claude Code │
                     │  Instances   │
                     │  (Execution) │
                     └──────────────┘
```

## Operating Modes

### Mode 1: Safe Observation (Default)
- Analyzes BB5 continuously
- Reports findings via Telegram
- **Waits for your approval** before any action
- No automatic code changes

### Mode 2: Semi-Autonomous
- Analyzes and proposes solutions
- Creates GitHub branches for changes
- **Shows you diffs** via Telegram
- Executes only after your "yes" reply

### Mode 3: Full Autonomous (Future)
- Handles low-risk improvements automatically
- Still reports everything via Telegram
- Escalates risky changes to you

## Branch Strategy

```
main (production)
├── vps/moltbot-analysis-20260209-001 (analysis findings)
├── vps/moltbot-fix-20260209-001 (proposed fixes)
├── vps/moltbot-improvement-20260209-001 (improvements)
└── vps/moltbot-emergency-20260209-001 (critical fixes)
```

All MoltBot work happens in `vps/*` branches. Never touches `main` directly.

## Communication Protocol (Telegram)

### Message Types FROM MoltBot

**1. Analysis Report (Daily)**
```
🔍 BB5 Daily Analysis

Issues Found: 3
━━━━━━━━━━━━━━━

1. [MEDIUM] Orphaned tasks in 5-project-memory
   12 tasks have no linked plan
   → Propose: Auto-link or archive

2. [LOW] Documentation drift detected
   3 ADRs reference non-existent files
   → Propose: Update or remove references

3. [HIGH] Skill registry out of sync
   5 skills declared but not implemented
   → Propose: Implement or remove

Reply:
• "1" - Fix issue #1
• "2" - Fix issue #2
• "3" - Fix issue #3
• "all" - Fix all issues
• "status" - Get detailed status
• "pause" - Stop autonomous mode
```

**2. Action Proposal**
```
⚡ Proposed Action

Issue: Orphaned tasks in 5-project-memory
Solution: Auto-link 12 tasks to nearest plan
Branch: vps/moltbot-fix-20260209-001

Estimated time: 15 minutes
Risk level: LOW

Reply:
• "yes" - Execute this action
• "no" - Skip this issue
• "details" - Show full analysis
• "modify" - Suggest changes
```

**3. Execution Report**
```
✅ Action Complete

Branch: vps/moltbot-fix-20260209-001
Commits: 3
Files changed: 12

Summary:
• Linked 8 tasks to Plan-A
• Linked 4 tasks to Plan-B
• Created ADR-047 documenting decision

Review: https://github.com/Lordsisodia/blackbox5/pull/xxx

Reply:
• "merge" - Merge to main
• "review" - Show full diff
• "revert" - Undo changes
• "next" - Continue to next issue
```

**4. Emergency Alert**
```
🚨 EMERGENCY

Critical issue detected:
STATE.yaml corruption - 47 tasks in invalid state

Immediate action required.
Safe recovery mode activated.

Reply:
• "fix" - Attempt automatic recovery
• "hold" - Wait for manual review
• "backup" - Create backup first
```

### Commands TO MoltBot

| Command | Action |
|---------|--------|
| `status` | Current analysis status |
| `analyze` | Run full analysis now |
| `issues` | List all open issues |
| `fix [n]` | Fix issue number n |
| `mode safe` | Switch to safe mode |
| `mode semi` | Switch to semi-autonomous |
| `pause` | Stop all activity |
| `resume` | Resume activity |
| `branches` | List active branches |
| `merge [branch]` | Merge branch to main |
| `learn` | Show what MoltBot has learned |

## Implementation Architecture

### Components

```
moltbot-autonomous/
├── moltbot-agent.py          # Main agent loop
├── analyzers/
│   ├── task_analyzer.py      # Find orphaned tasks
│   ├── doc_analyzer.py       # Find doc drift
│   ├── skill_analyzer.py     # Check skill registry
│   └── git_analyzer.py       # Check git health
├── executors/
│   ├── claude_executor.py    # Spawn Claude Code
│   ├── git_executor.py       # Git operations
│   └── telegram_notifier.py  # Send notifications
├── config/
│   ├── moltbot.yaml          # Agent configuration
│   └── rules.yaml            # Safety rules
└── state/
    ├── current_analysis.json # Last analysis
    ├── pending_actions.json  # Actions awaiting approval
    └── executed_actions.json # History
```

### Safety Rules (Hardcoded)

1. **Never push to main** - Always use `vps/*` branches
2. **Never delete files** - Only archive/rename
3. **Never modify secrets** - Skip `.env`, `.secrets` files
4. **Max 3 actions per hour** - Rate limiting
5. **Auto-pause on error** - Stop if 3 consecutive failures
6. **Require approval for HIGH risk** - Never auto-execute high risk

### Analysis Schedule

```yaml
schedule:
  full_analysis: "0 */6 * * *"      # Every 6 hours
  quick_scan: "*/15 * * * *"        # Every 15 minutes
  health_check: "*/5 * * * *"       # Every 5 minutes
  daily_report: "0 9 * * *"         # Daily at 9 AM
  weekly_review: "0 9 * * 1"        # Monday 9 AM
```

## Claude Code Integration

### How MoltBot Spawns Claude

```python
# Example: Fix orphaned tasks
subprocess.run([
    "claude", "--mcp-config", "/opt/blackbox5/.mcp-moltbot.json",
    "--prompt", """
    You are fixing orphaned tasks in BlackBox5.

    Context: 12 tasks in 5-project-memory/blackbox5/.autonomous/tasks/active/
    have no linked plan in 6-roadmap/

    Task: Link each orphaned task to the most appropriate plan,
    or create a new plan if needed.

    Rules:
    - Work in branch: vps/moltbot-fix-{timestamp}
    - Create ADR documenting decisions
    - Update STATE.yaml
    - Never delete tasks, only link them

    Report back via Telegram when complete.
    """
])
```

### Execution Flow

```
1. MoltBot detects issue
2. Creates branch vps/moltbot-fix-xxx
3. Spawns Claude Code instance
4. Claude works on branch
5. Claude reports completion
6. MoltBot notifies you via Telegram
7. You approve/reject
8. If approved, MoltBot merges PR
```

## State Management

### What MoltBot Tracks

```yaml
# current_analysis.json
{
  "timestamp": "2026-02-09T10:00:00Z",
  "issues": [
    {
      "id": "ISS-001",
      "severity": "medium",
      "type": "orphaned_task",
      "description": "12 tasks have no linked plan",
      "proposed_action": "auto_link_tasks",
      "status": "pending_approval"
    }
  ],
  "metrics": {
    "total_tasks": 156,
    "orphaned_tasks": 12,
    "completed_tasks": 89,
    "documentation_drift": 3
  }
}

# pending_actions.json
{
  "actions": [
    {
      "id": "ACT-001",
      "issue_id": "ISS-001",
      "branch": "vps/moltbot-fix-20260209-001",
      "proposed_at": "2026-02-09T10:05:00Z",
      "status": "awaiting_approval",
      "risk_level": "low"
    }
  ]
}
```

## Deployment on VPS

### Installation

```bash
# On VPS (77.42.66.40)
cd /opt/blackbox5

# Create agent directory
mkdir -p agents/moltbot-autonomous

# Install systemd service
sudo tee /etc/systemd/system/moltbot-autonomous.service << 'EOF'
[Unit]
Description=MoltBot Autonomous Agent
After=network.target moltbot.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/blackbox5
Environment="HOME=/root"
Environment="TELEGRAM_BOT_TOKEN=8581639813:AAFA13wDTKEX2x6J-lVfpq9QHnsGRnB1EZo"
Environment="TELEGRAM_CHAT_ID=7643203581"
Environment="GITHUB_TOKEN=xxx"
Environment="RALF_ENGINE_DIR=/opt/blackbox5/2-engine/.autonomous"
Environment="RALF_PROJECT_DIR=/opt/blackbox5/5-project-memory/blackbox5"
ExecStart=/usr/bin/python3 /opt/blackbox5/agents/moltbot-autonomous/moltbot-agent.py
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable moltbot-autonomous
sudo systemctl start moltbot-autonomous
```

### Monitoring

```bash
# Check status
sudo systemctl status moltbot-autonomous

# View logs
sudo journalctl -u moltbot-autonomous -f

# Telegram test
python3 -c "
import requests
requests.post('https://api.telegram.org/bot8581639813:AAFA13wDTKEX2x6J-lVfpq9QHnsGRnB1EZo/sendMessage',
    json={'chat_id': '7643203581', 'text': '🤖 MoltBot Autonomous is online'})
"
```

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Issues detected/day | 5-10 | Analysis reports |
| False positive rate | <20% | User "no" responses |
| Time to fix (low risk) | <30 min | Execution logs |
| User approval rate | >70% | Action history |
| System uptime | >95% | Service status |

## Next Steps

1. **Build MVP** (Today)
   - Basic analyzer framework
   - Telegram integration
   - Single issue type (orphaned tasks)
   - Safe mode only

2. **Add Executors** (This week)
   - Claude Code spawning
   - Git branch management
   - PR creation

3. **Enhance Intelligence** (Next week)
   - Multiple analyzers
   - Risk assessment
   - Learning from feedback

4. **Full Autonomy** (Future)
   - Semi-autonomous mode
   - Predictive fixes
   - Workflow optimization
