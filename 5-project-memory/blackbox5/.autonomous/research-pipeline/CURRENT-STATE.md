# Research Pipeline - Current State

**Date:** 2026-02-04
**Status:** Ready for deployment (3 minor fixes applied)
**Architecture:** Dual-RALF with Swarm Memory

---

## File Structure (Current)

```
research-pipeline/
├── AGENT-SWARM-MEMORY-ARCHITECTURE.md    # Swarm architecture spec
├── ARCHITECTURE-ALIGNMENT.md             # BB5 alignment analysis
├── DUAL-RALF-RESEARCH-ARCHITECTURE.md    # Main architecture doc
├── INDEX.md                              # Quick reference
├── README.md                             # Project readme
├── STATE.yaml                            # Pipeline state
├── SWARM-MEMORY-INTEGRATION.md           # Integration guide
├── WORKER-VALIDATOR-COORDINATION.md      # Coordination protocol
├── XREF.md                               # Cross-references
│
├── launch-all.sh                         # Launch all 6 agents
├── launch-analyst.sh                     # Launch analyst pair
├── launch-planner.sh                     # Launch planner pair
├── launch-scout.sh                       # Launch scout pair
│
├── .claude/
│   └── hooks/
│       ├── README.md                     # Hook documentation
│       ├── session-start-swarm.sh        # Three-layer injection ✅
│       └── session-start-timeline-memory.sh
│
├── .templates/
│   ├── communications/                   # 8 templates
│   ├── prompts/                          # 6 agent prompts ✅
│   └── runs/                             # 7 run templates
│
├── agents/                               # 6 agents ✅
│   ├── analyst-validator/
│   │   ├── memory/
│   │   ├── metrics/
│   │   ├── runs/
│   │   ├── state/
│   │   ├── running-memory.md            # Session state ✅
│   │   └── timeline-memory.md           # Long-term memory ✅
│   ├── analyst-worker/                   # Same structure
│   ├── planner-validator/                # Same structure
│   ├── planner-worker/                   # Same structure
│   ├── scout-validator/                  # Same structure
│   └── scout-worker/                     # Same structure
│
├── communications/                       # Initialized ✅
│   ├── analyst-state.yaml               # From template
│   ├── events.yaml                      # From template
│   ├── heartbeat.yaml                   # From template
│   ├── planner-state.yaml               # From template
│   ├── protocol.yaml                    # From template
│   ├── queue.yaml                       # From template
│   └── scout-state.yaml                 # From template
│
├── context/
│   ├── patterns-index.yaml
│   ├── routes.yaml                      # Updated with swarm paths ✅
│   └── sources.yaml
│
├── data/
│   ├── analysis/                        # Empty (for analyst output)
│   ├── patterns/                        # Empty (for scout output)
│   └── tasks/                           # Empty (for planner output)
│
├── logs/
│   ├── analyst/
│   ├── pipeline/
│   ├── planner/
│   └── scout/
│
├── operations/
│   ├── skill-usage.yaml
│   └── token-usage.yaml
│
├── reviews/
│
└── swarm/                               # Global coordination ✅
    ├── events.yaml                      # Swarm event bus
    ├── heartbeat.yaml                   # 6-agent health
    ├── ledger.md                        # Chronological history
    └── state.yaml                       # Pipeline state machine
```

---

## Statistics

| Category | Count | Status |
|----------|-------|--------|
| **Documentation** | 9 files | ✅ Complete |
| **Launch Scripts** | 4 scripts | ✅ Executable |
| **Hook Scripts** | 2 scripts | ✅ Executable |
| **Agent Prompts** | 6 prompts | ✅ Complete with work assignment |
| **Agent Memory** | 12 files (2 per agent) | ✅ Initialized |
| **Swarm Files** | 4 files | ✅ Complete |
| **Communication Templates** | 8 templates | ✅ Complete |
| **Communication Instances** | 7 files | ✅ Initialized from templates |
| **Run Templates** | 7 templates | ✅ Complete |
| **Context Files** | 3 files | ✅ Routes updated |
| **Empty Directories** | 30+ | Ready for runtime data |

**Total Files:** ~70 files
**Total Directories:** 52 directories

---

## What's Complete

### ✅ Architecture
- [x] Dual-RALF architecture documented
- [x] Worker-validator coordination protocol defined
- [x] Swarm memory architecture specified
- [x] BB5 alignment verified

### ✅ Agents
- [x] 6 agent directories created
- [x] Agent prompts written (with work assignment logic)
- [x] Timeline memory files created (with swarm_context)
- [x] Running memory files created
- [x] Memory/metrics/runs/state subdirectories created

### ✅ Swarm Coordination
- [x] swarm/heartbeat.yaml - Global health monitoring
- [x] swarm/events.yaml - Event bus with routing
- [x] swarm/state.yaml - Pipeline state machine
- [x] swarm/ledger.md - Chronological history

### ✅ Communication
- [x] Communication templates created
- [x] Communication instances initialized
- [x] Routes.yaml updated with swarm paths

### ✅ Hooks
- [x] session-start-swarm.sh - Three-layer injection
- [x] session-start-timeline-memory.sh - Basic injection
- [x] Hook README documentation

### ✅ Launch Scripts
- [x] launch-all.sh - Launch all 6 agents
- [x] launch-scout.sh - Launch scout pair
- [x] launch-analyst.sh - Launch analyst pair
- [x] launch-planner.sh - Launch planner pair
- [x] All scripts made executable

---

## What's Empty (Will Populate at Runtime)

### Empty Directories (Normal)
These will be populated as agents run:

- `agents/*/memory/` - Learning & strategy (populated by agents)
- `agents/*/metrics/` - Performance tracking (populated by agents)
- `agents/*/runs/` - Run directories (created per run)
- `agents/*/state/` - Agent state (populated by agents)
- `communications/` - Now initialized with templates
- `data/analysis/` - Analyst output (populated by analyst-worker)
- `data/patterns/` - Scout output (populated by scout-worker)
- `data/tasks/` - Planner output (populated by planner-worker)
- `logs/*/` - Log files (populated at runtime)
- `reviews/` - Code reviews (populated at runtime)

---

## Recent Fixes Applied

### Fix 1: Routes.yaml Updated
**Added swarm paths:**
```yaml
swarm: "swarm"
swarm_heartbeat: "swarm/heartbeat.yaml"
swarm_events: "swarm/events.yaml"
swarm_state: "swarm/state.yaml"
swarm_ledger: "swarm/ledger.md"
```

### Fix 2: Communications Initialized
**Copied from templates:**
- scout-state.yaml
- analyst-state.yaml
- planner-state.yaml
- events.yaml
- heartbeat.yaml
- queue.yaml
- protocol.yaml

### Fix 3: Hook Scripts Executable
**Made executable:**
- session-start-swarm.sh
- session-start-timeline-memory.sh

---

## How to Start

### Step 1: Install Hook (One-time)
Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/research-pipeline/.claude/hooks/session-start-swarm.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Step 2: Launch Agents

**Option A: Launch all at once**
```bash
cd /Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/research-pipeline
./launch-all.sh
```

**Option B: Launch by phase**
```bash
./launch-scout.sh    # Scout worker + validator
./launch-analyst.sh  # Analyst worker + validator
./launch-planner.sh  # Planner worker + validator
```

### Step 3: Monitor

**Check swarm health:**
```bash
cat swarm/heartbeat.yaml
```

**Check pipeline state:**
```bash
cat swarm/state.yaml
```

**View event log:**
```bash
cat swarm/events.yaml
```

**Read ledger:**
```bash
cat swarm/ledger.md
```

---

## Expected Behavior

### First Run
1. Hook injects 3-layer context (swarm + pipeline + agent)
2. Agent reads timeline-memory.md
3. Agent finds empty work queue
4. Agent checks events.yaml
5. Agent exits with Status: IDLE (no work yet)

### After Sources Added
1. Operator adds sources to `context/sources.yaml`
2. Scout worker finds source in queue
3. Scout extracts patterns → `data/patterns/`
4. Scout publishes `pattern.extracted` event
5. Analyst worker sees event, analyzes pattern
6. Analyst publishes `analysis.complete` event
7. Planner worker sees event, creates BB5 task
8. Validators provide feedback throughout

---

## Key Integration Points

### With BB5
- **Input:** Research pipeline reads from BB5 structure
- **Output:** Research pipeline writes to `communications/queue.yaml`
- **Coordination:** Separate from BB5 agents (planner/executor)
- **No Conflicts:** Isolated in `research-pipeline/` directory

### Within Research Pipeline
- **Scout → Analyst:** via `data/patterns/` + events
- **Analyst → Planner:** via `data/analysis/` + events
- **Planner → BB5:** via `communications/queue.yaml`
- **Validators:** via `communications/chat-log.yaml`

---

## Troubleshooting

### Hook Not Injecting
1. Check file permissions: `ls -la .claude/hooks/`
2. Verify settings.json path is absolute
3. Test hook manually: `echo '{}' | ./.claude/hooks/session-start-swarm.sh`

### Agents Not Finding Work
1. Check timeline-memory.md has work_queue
2. Verify events.yaml has events
3. Check routes.yaml paths are correct

### Communication Failures
1. Verify communications/ files exist
2. Check YAML syntax is valid
3. Ensure agents have write permissions

---

## Next Steps (Post-Launch)

1. **Monitor token usage** - Check `operations/token-usage.yaml`
2. **Tune budgets** - Adjust in `swarm/state.yaml`
3. **Add sources** - Populate `context/sources.yaml`
4. **Review ledger** - Check `swarm/ledger.md` for activity
5. **Optimize** - Based on actual usage patterns

---

## Architecture Verification

✅ **Aligned with BB5:**
- Uses same run isolation pattern
- Uses same metrics/state directories
- Extends heartbeat to 6 agents
- Adds hook-based memory injection

✅ **Swarm Coordination:**
- Global health monitoring
- Event-driven work routing
- Automatic bottleneck detection
- Resource allocation management

✅ **Agent Memory:**
- Timeline memory (long-term)
- Running memory (short-term)
- Work assignment logic
- Swarm context awareness

✅ **Ready for Deployment:**
- All files created
- All scripts executable
- Routes updated
- Communications initialized

---

*System is ready to launch. Start with `./launch-all.sh` after installing the hook.*
