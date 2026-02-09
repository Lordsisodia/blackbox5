# Activate BB5 Core Agent Team

## Purpose
This document activates the BB5 core agent team: Context Collector, Superintelligence, and Scribe.

## When to Use
Run this when:
- Starting a new complex task
- Need deep analysis of BB5 state
- Making architecture/design decisions
- Beginning improvement work

## Activation Sequence

### Step 1: Spawn Context Collector
```
Spawn a sub-agent named "bb5-context-collector" with the prompt from /Users/shaansisodia/.blackbox5/.claude/agents/bb5-context-collector.md
```

### Step 2: Spawn Scribe
```
Spawn a sub-agent named "bb5-scribe" with the prompt from /Users/shaansisodia/.blackbox5/.claude/agents/bb5-scribe.md
```

### Step 3: Spawn Superintelligence (if complex task)
```
Spawn a sub-agent named "bb5-superintelligence" with the prompt from /Users/shaansisodia/.blackbox5/.claude/agents/bb5-superintelligence.md
```

## Agent Team Coordination

The three agents work together:
1. **Context Collector** → Gathers BB5 state, produces CONTEXT_REPORT.md
2. **Superintelligence** → Uses context report for 7-dimension analysis
3. **Scribe** → Documents all thinking, decisions, and learnings

## Output

After activation, check:
- `runs/current/CONTEXT_REPORT.md` - BB5 state
- `runs/current/SUPERINTELLIGENCE_ANALYSIS.md` - Analysis (if activated)
- `runs/current/THOUGHTS.md` - Thinking process
- `runs/current/DECISIONS.md` - Decision log
- `runs/current/LEARNINGS.md` - Learnings

## Auto-Activation

This team auto-activates via hooks:
- `session-start-agent-teams.sh` - Prepares run directory
- `post-message-agent-teams.sh` - Triggers on complex keywords
