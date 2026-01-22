# AGENTS.md

**Purpose**: Minimal behavioral contract for AI agents in BlackBox5.
**Version**: 3.0.0
**Last Updated**: 2026-01-21

---

## 🎯 BEFORE YOU START

```bash
# 1. Check environment
pwd && git branch && git status
# Never work on main/master for features

# 2. Check recent context
cat 5-project-memory/siso-internal/operations/WORK-LOG.md | tail -20
# Understand what just happened

# 3. Choose your approach
# Simple (1-2 files)?     → Direct execution
# Medium (3-10 files)?   → Ralphy autonomous loop
# Large (10+ files)?     → Planning Agent → Orchestrator
```

---

## 🛡️ NON-NEGOTIABLES

### NEVER
- Work on `main` or `master` branch for features
- Mark work "done" without validation
- Exceed 80% context window (hooks will warn)
- Edit files without reading the impact analysis

### ALWAYS
- Log work (automatic, but verify in WORK-LOG.md)
- Document decisions (ADR format in `5-project-memory/siso-internal/decisions/`)
- Use first principles for complex problems (hooks will trigger)
- Validate completion before saying "done" (hooks will show checklist)

---

## 📋 BEFORE SAYING "DONE"

```
☐ Tests pass
☐ Code follows standards
☐ Documentation updated
☐ Breaking changes documented
☐ Self-review completed
☐ WORK-LOG.md updated
```

---

## 🧠 THINKING FRAMEWORKS (Auto-injected by hooks)

### First Principles
Triggered by: "architecture", "design", "approach"
```
1. What problem are we ACTUALLY solving?
2. What do we know to be TRUE?
3. What are we assuming?
4. What MUST be included? What can we eliminate?
```

### Assumption Detection
Triggered by: "obviously", "clearly", "should be"
```
- What evidence supports this?
- What would change if this were wrong?
- Should we validate first?
```

---

## 🛠️ WORKFLOWS

### MCP TOOLS: Airis Gateway (3 Commands)

You have access to **ONE MCP (Airis)** that provides 60+ tools via 3 simple commands:

| Command | Purpose | Usage |
|---------|---------|-------|
| **airis-find** | Discover tools | `airis-find(query: "read file")` |
| **airis-exec** | Execute tools | `airis-exec(tool: "filesystem:read_file", arguments: {...})` |
| **airis-schema** | Get parameters | `airis-schema(tool: "filesystem:read_file")` |

**Pattern:** Always discover first → check schema → execute

```
Example: Read a file
1. airis-find(query: "read file") → finds filesystem:read_file
2. airis-schema(tool: "filesystem:read_file") → shows {path: string}
3. airis-exec(tool: "filesystem:read_file", arguments: {"path": "config.json"})
```

**Common Tool Categories:**
- `filesystem:*` - Read/write files
- `serena:*` - Search code
- `supabase:*` - Database operations
- `memory:*` - Store/retrieve data
- `fetch:*` - Web requests
- `github:*` - GitHub API

**Full guide:** See `AIRIS-AGENT-GUIDE.md` for complete documentation

---

### Simple Tasks (1-2 files)
```python
# Just execute directly
result = do_the_thing()
```

### Medium Tasks (3-10 files)
```python
from blackbox5.engine.operations.runtime.ralphy import RalphyManager
manager = RalphyManager()
result = manager.execute_task(
    task="Your task here",
    prd_file="specs/prds/current.md",
    engine="claude"
)
# Runs 3-5 autonomous iterations
```

### Large Projects (10+ files)
```python
# Step 1: Plan
from blackbox5.engine.agents.workflows.planning_agent import PlanningAgent
plan = PlanningAgent().plan_and_push("Your requirement")
# Creates: PRD → Epic → Tasks → Vibe Kanban

# Step 2: Execute
from blackbox5.engine.agents.workflows.orchestrator_agent import OrchestratorAgent
results = OrchestratorAgent().orchestrate_parallel_execution()
# 5 parallel agents work on tasks
```

---

## 📁 CRITICAL LOCATIONS

```
5-project-memory/siso-internal/
├── operations/
│   ├── WORK-LOG.md              # YOUR WORK LOG (verify it's updating)
│   ├── reflections/             # Session completion reflections
│   └── agents/                  # Agent sessions
│
├── decisions/                   # ALL decisions go here
│   └── INDEX.md                 # Decision catalog
│
└── knowledge/                   # Learned patterns

2-engine/
├── 02-agents/                   # Agent implementations
├── 06-integrations/             # Vibe Kanban, GitHub
└── 07-operations/              # Ralphy integration
```

---

## 🚨 CONTEXT WARNINGS (Auto-injected by hooks)

### Context > 80%
```
⚠️ Context Usage Warning
Recommendations:
  1. Run /compact to summarize
  2. Start new session with /clear
  3. Use subagents for exploration
```

### Change Impact (Before Edit)
```
📊 Change Impact Analysis for: [file]
This file imports: [...]
This file is used by: [...]
⚠️ Changes here may affect dependent files.
```

### Reversibility Check (Dangerous Ops)
```
⚠️ Reversibility Check
Create backup: git checkout -b backup/$(date +%s)
```

---

## ✅ SUCCESS CRITERIA

You are successful when:
1. **Every Edit** appears in WORK-LOG.md
2. **Every Decision** has an ADR in decisions/
3. **Every Session** creates memories in knowledge/
4. **Every "Done"** passes the validation checklist
5. **No irreversible mistakes** were made
6. **Technical debt** is tracked and visible

---

## 📚 DETAILED REFERENCE

- **AGENT-REFERENCE.md** - Quick reference for all agents
- **AIRIS-AGENT-GUIDE.md** - How to use Airis Gateway MCP tools
- **SKILLS-REGISTRY.md** - All 70+ skills
- **.claude/hooks/README.md** - Complete hooks documentation
- **AGENT-SYSTEM.md** - System architecture and philosophy

---

## 🆘 TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| "Context exceeded" | `/compact` or `/clear` |
| "Hook not running" | `chmod +x .claude/hooks/*.sh` |
| "Can't find agent" | Read AGENT-REFERENCE.md |
| "Lost context" | Read WORK-LOG.md and reflections/ |

---

**This file is auto-loaded at session start. Follow these standards. Maintain excellence.**

**Keep it minimal. Let hooks inject the rest. Preserve context for actual work.**
