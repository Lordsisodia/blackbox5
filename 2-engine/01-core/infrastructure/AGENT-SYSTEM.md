# AGENT-SYSTEM.md

**Blackbox5 Agent Architecture & Hook System Documentation**

**Purpose**: Internal documentation for the Blackbox5 agent system, hook architecture, and behavioral contracts.
**Maintainer**: Core Team
**Version**: 2.0.0
**Last Updated**: 2026-01-21

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Philosophy](#philosophy)
3. [Hook System Architecture](#hook-system-architecture)
4. [Behavioral Contract (AGENTS.md)](#behavioral-contract-agentsmd)
5. [Agent Registry](#agent-registry)
6. [Prompt Injection System](#prompt-injection-system)
7. [Maintenance Guide](#maintenance-guide)

---

## Overview

BlackBox5 uses a **hook-based behavioral system** that creates a disciplined engineering culture around AI-assisted development. The system has two main components:

1. **AGENTS.md** - A behavioral contract that tells agents HOW to work
2. **Hook Scripts** - Automation that enforces behaviors and injects guidance

### Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Code Interface                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              SessionStart Hook: load-agents-context.sh      │
│                  Injects AGENTS.md (Behavioral Contract)     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   .claude/settings.json                     │
│              (Hook Configuration & Permissions)              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   Hook Scripts (21 hooks)                    │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐  │
│  │ UserPromptSubmit│ │  PreToolUse    │ │  PostToolUse   │  │
│  │  (5 hooks)     │ │  (4 hooks)     │ │  (5 hooks)     │  │
│  └────────────────┘ └────────────────┘ └────────────────┘  │
│  ┌────────────────┐ ┌────────────────┐                      │
│  │  SessionStart  │ │   SessionEnd   │                      │
│  │  (3 hooks)     │ │  (2 hooks)     │                      │
│  └────────────────┘ └────────────────┘                      │
│  ┌────────────────┐                                           │
│  │ SubagentStop   │                                           │
│  │  (2 hooks)     │                                           │
│  └────────────────┘                                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│             Enforced Behaviors & Injected Guidance           │
│    (Context, Warnings, Frameworks, Checklists, Reminders)    │
└─────────────────────────────────────────────────────────────┘
```

---

## Philosophy

### What We're Building

A **disciplined engineering culture** where:

1. **Every action is traceable** - Nothing happens without being logged
2. **Every decision is justified** - Rationales must be documented
3. **Every change is understood** - Impact analysis prevents surprises
4. **Every completion is validated** - Quality gates are strict
5. **Every session contributes to learning** - Knowledge is captured

### Core Principles

1. **First Principles Thinking** - Question assumptions, build from fundamentals
2. **Quality Over Speed** - Better to deliver less of higher quality
3. **Documentation as Code** - Capture decisions and reasoning as you work
4. **Continuous Improvement** - Track patterns and improve based on what you learn

### What AGENTS.md Is (and Isn't)

| IS | ISN'T |
|----|--------|
| Behavioral contract | Reference manual |
| Prescriptive (HOW to work) | Descriptive (WHAT exists) |
| Actionable standards | Feature catalog |
| Mandatory reading | Optional lookup |
| Defines culture | Lists tools |

---

## Hook System Architecture

### Event Types

| Event | When It Fires | Purpose | Hook Count |
|-------|---------------|---------|------------|
| **UserPromptSubmit** | After user submits prompt, before AI processes | Inject analysis frameworks | 5 |
| **PreToolUse** | Before any tool execution | Safety checks, impact analysis | 4 |
| **PostToolUse** | After tool execution completes | Learning, logging, quality | 5 |
| **SessionStart** | When Claude Code starts | Environment validation, **AGENT CONTEXT** | 3 |
| **SessionEnd** | When Claude Code session ends | Memory extraction | 2 |
| **SubagentStop** | When subagent finishes | Quality validation | 2 |

### Hook Configuration

**File**: `.claude/settings.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          { "type": "command", "command": ".claude/hooks/load-agents-context.sh" },
          { "type": "command", "command": ".claude/hooks/validate-environment.sh" },
          { "type": "command", "command": ".claude/hooks/manage-session-time.sh" }
        ]
      }
    ]
  }
}
```

---

## Behavioral Contract (AGENTS.md)

### What AGENTS.md Contains

#### 1. Mission Statement
Clear definition of success metrics:
- Quality of code
- Traceability of work
- Learning contributed
- Safety of operations

#### 2. Immediate Actions
Step-by-step session startup:
1. Understand the request (first principles)
2. Check environment (git status, branch)
3. Choose approach (Direct/Ralphy/Orchestration)

#### 3. Mandatory Behaviors (5 ALWAYS Rules)

1. **ALWAYS Log Work**
   - Every Edit/Write → WORK-LOG.md
   - Automatic via hook, but agent should verify

2. **ALWAYS Analyze Impact**
   - Before any Edit
   - Hook shows dependencies automatically
   - Agent MUST READ the analysis

3. **NEVER Mark "Done" Without Validation**
   - Full completion checklist (15 items)
   - Code quality, testing, documentation, review, integration

4. **ALWAYS Document Decisions**
   - ADR format: Context, Decision, Rationale, Alternatives, Consequences
   - Location: `5-project-memory/siso-internal/decisions/[category]/`

5. **ALWAYS Track Technical Debt**
   - TODO/FIXME/HACK comments automatically tracked
   - Agent should proactively address or create issues

#### 4. Thinking Frameworks (3 Mandatory)

**First Principles** (for architecture/design/strategy):
```
1. Question the Question
2. Identify Assumptions
3. Break Down to Fundamentals
4. Build Up from First Principles
```

**Assumption Detection** (continuous):
- Triggered by: "obviously", "clearly", "should be", "everyone knows"
- Action: Stop and question, ask for evidence

**Task Breakdown** (when complex):
- Trigger: >3 ANDs, nested clauses
- Action: Break into 3-7 sub-tasks, prioritize, tackle sequentially

#### 5. Workflows (4 Patterns)

**Workflow 1: Planning Agent** (New features, large projects)
```python
PlanningAgent().plan_and_push("requirement")
# Creates: PRD → Epic → 20+ Tasks → Vibe Kanban
```

**Workflow 2: Orchestrator** (Parallel execution)
```python
OrchestratorAgent().orchestrate_parallel_execution()
# Assigns tasks to 5 parallel agents
```

**Workflow 3: Ralphy** (Single complex task)
```python
RalphyManager().execute_task(task, prd_file, engine="claude")
# 3-5 autonomous iterations
```

**Workflow 4: Direct** (Simple tasks)
```python
# Just execute directly
```

#### 6. Safety Rules (5 NEVER, 5 ALWAYS)

**NEVER**:
1. Work on main/master for features
2. Do irreversible ops without backup
3. Edit without understanding dependencies
4. Mark "done" without validation
5. Exceed 80% context window

**ALWAYS**:
1. Question assumptions
2. Log work (verify WORK-LOG.md)
3. Analyze impact before editing
4. Use first principles for complex problems
5. Validate completion with full checklist

---

## Agent Registry

### Core Agents

| Agent | Location | Purpose | Usage |
|-------|----------|---------|-------|
| **PlanningAgent** | `2-engine/02-agents/workflows/planning_agent.py` | Create PRD, Epic, Tasks | `PlanningAgent().plan_and_push(request)` |
| **OrchestratorAgent** | `2-engine/02-agents/workflows/orchestrator_agent.py` | Coordinate parallel execution | `OrchestratorAgent().orchestrate_parallel_execution()` |
| **PRDAgent** | `2-engine/spec_driven/prd_agent.py` | Parse and validate PRDs | `PRDAgent().load_prd(prd_id)` |
| **EpicAgent** | `2-engine/spec_driven/epic_agent.py` | Create epics from PRDs | `EpicAgent().create_epic(prd_id)` |
| **TaskAgent** | `2-engine/spec_driven/task_agent.py` | Create tasks from epics | `TaskAgent().create_tasks(epic_id)` |

### Specialist Agents

| Agent | Location | Purpose |
|-------|----------|---------|
| **RalphAgent** | `2-engine/02-agents/implementations/04-specialists/4-specialists/ralph-agent/` | Autonomous decision-making |
| **DeepResearchAgent** | `2-engine/02-agents/implementations/03-research/3-research/deep-research/` | In-depth research |
| **OSSDiscoveryAgent** | `2-engine/02-agents/implementations/03-research/3-research/oss-discovery/` | Find OSS components |
| **TestingAgent** | `2-engine/02-agents/implementations/05-enhanced/5-enhanced/testing-agent/` | Generate tests |

### Custom Agents

| Agent | Location | Purpose |
|-------|----------|---------|
| **CodeReviewer** | `2-engine/02-agents/implementations/custom/custom/code_reviewer/agent.md` | Review code |
| **FrontendDeveloper** | `2-engine/02-agents/implementations/custom/custom/frontend_developer/agent.md` | Frontend tasks |
| **BackendDeveloper** | `2-engine/02-agents/implementations/custom/custom/backend_developer/agent.md` | Backend tasks |
| **BugFixer** | `2-engine/02-agents/implementations/custom/custom/bug_fixer/agent.md` | Fix bugs |

---

## Prompt Injection System

### What Gets Injected (and Why)

| Prompt | Event | Trigger | Purpose |
|--------|-------|---------|---------|
| **First Principles Framework** | UserPromptSubmit | Keywords: "architecture", "design", "approach" | Enforce deep thinking over pattern-matching |
| **Assumption Detection** | UserPromptSubmit | Phrases: "obviously", "clearly", "should be" | Challenge implicit assumptions |
| **Task Complexity Warning** | UserPromptSubmit | >3 ANDs or nested clauses | Prevent overwhelmed agents |
| **Dependency Detection** | UserPromptSubmit | "needs X", "requires Y" | Identify blockers before starting |
| **Knowledge Gap Detection** | UserPromptSubmit | Uncertainty phrases | Suggest research before implementation |
| **Context Boundary Warning** | PreToolUse | Context > 80% | Prevent context overflow failures |
| **Change Impact Analysis** | PreToolUse (Edit/Write) | Any file edit | Show blast radius before changes |
| **Reversibility Check** | PreToolUse | Dangerous operations | Prevent irreversible mistakes |
| **Completion Criteria** | PreToolUse | Keywords: "done", "complete" | Ensure quality before stopping |
| **Activity Log** | PostToolUse | Any Edit/Write | Create audit trail |
| **Decision Capture** | PostToolUse | Decision-related files | Record rationale |
| **Technical Debt Detection** | PostToolUse | TODO/FIXME/HACK comments | Make debt visible |
| **Stakeholder Notification** | PostToolUse | API/schema/decision files | Inform affected parties |
| **Test Coverage Reminder** | PostToolUse | Editing .ts/.py without tests | Maintain quality |
| **Reflection on Completion** | SubagentStop/Stop | Any task completion | Maintain momentum, plan next steps |

### Injection Mechanism

1. **Hook Script Executes** → Bash script runs
2. **Condition Check** → Script checks for trigger conditions
3. **Output to STDOUT** → Script outputs markdown/text
4. **Claude Code Captures** → Output injected into context
5. **Agent Processes** → Agent reads and acts on injected content

---

## Maintenance Guide

### Updating AGENTS.md

**When to Update**:
- Adding new mandatory behaviors
- Changing workflows or approaches
- New quality standards or safety rules
- New agent patterns discovered

**Process**:
1. Edit AGENTS.md (root)
2. Update version number (major.minor.patch)
3. Update "Last Updated" date
4. Test with fresh session to verify auto-loading
5. Update this file (AGENT-SYSTEM.md) if architecture changed

**What to Add**:
- New "ALWAYS" or "NEVER" rules
- New thinking frameworks
- New workflows
- Updated success criteria
- New examples

**What NOT to Add**:
- Feature catalogs (that's what CATALOG.md is for)
- API documentation (that's what docs/ are for)
- Tool reference (that's what AGENT-REFERENCE.md is for)

### Adding a New Hook

1. **Create hook script** in `.claude/hooks/`:
```bash
#!/bin/bash
# .claude/hooks/my-new-hook.sh
input=$(cat)
# Your logic here
echo "# 🎯 My Hook Output"
echo "This gets injected into context!"
```

2. **Make executable**:
```bash
chmod +x .claude/hooks/my-new-hook.sh
```

3. **Add to settings.json**:
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          { "type": "command", "command": ".claude/hooks/my-new-hook.sh" }
        ]
      }
    ]
  }
}
```

4. **Document in AGENT-SYSTEM.md**:
- Add to Prompt Injection System table
- Document trigger conditions
- Document output format

5. **Update .claude/hooks/README.md**:
- Add to hook specifications
- Document as critical/high-value

### Adding a New Agent

1. **Create agent implementation**:
```python
# 2-engine/02-agents/implementations/my_agent.py
class MyAgent:
    def execute(self, task: str) -> Dict[str, Any]:
        # Implementation
        return {"success": True, "result": "..."}
```

2. **Create agent metadata**:
```yaml
# 2-engine/02-agents/implementations/my_agent.agent.yaml
id: "my-agent"
type: "agent"
name: "My Agent"
category: "specialist"
description: "What this agent does"
tags: ["tag1", "tag2"]
status: "active"
```

3. **Add to AGENTS.md** (if it's a primary workflow):
- Add to "Workflows You Must Know" section
- Provide usage example
- Specify when to use

4. **Add to AGENT-SYSTEM.md**:
- Add to Agent Registry table
- Document location and purpose

5. **Test integration**:
```python
from blackbox5.engine.agents.implementations.my_agent import MyAgent
agent = MyAgent()
result = agent.execute("test task")
```

### Updating Hooks

1. **Test locally first**:
```bash
echo '{"tool_name":"Edit","tool_input":{"file_path":"test.txt"}}' | \
  .claude/hooks/my-hook.sh
```

2. **Verify output format**:
- Should be markdown or plain text
- Should be concise (< 500 words)
- Should be actionable

3. **Update documentation**:
- Update AGENT-SYSTEM.md
- Update .claude/hooks/README.md
- Test in Claude Code

---

## Environment Variables

```bash
# Configure in .claude/settings.json or system environment
BLACKBOX5_ENGINE_PATH=./2-engine
BLACKBOX5_MEMORY_PATH=./5-project-memory/siso-internal
BLACKBOX5_CONTEXT_THRESHOLD=80  # Context warning percentage
BLACKBOX5_SESSION_TIMEOUT=14400  # Session timeout in seconds (4 hours)
```

---

## File Structure Reference

```
BLACKBOX5/
├── AGENTS.md                          # ⭐ BEHAVIORAL CONTRACT (auto-loaded)
│
├── 2-engine/
│   ├── 01-core/
│   │   └── infrastructure/
│   │       └── AGENT-SYSTEM.md        # ⭐ THIS FILE (system docs)
│   │
│   ├── 02-agents/
│   │   ├── implementations/           # All agent implementations
│   │   │   ├── 01-core/              # Core agents
│   │   │   ├── 02-bmad/              # BMAD framework
│   │   │   ├── 03-research/          # Research agents
│   │   │   ├── 04-specialists/       # Specialist agents
│   │   │   ├── 05-enhanced/          # Enhanced agents
│   │   │   └── custom/               # Custom agents
│   │   │
│   │   └── capabilities/
│   │       └── skills-cap/
│   │           └── SKILLS-REGISTRY.md  # All 70+ skills
│   │
│   ├── 06-integrations/
│   │   ├── vibe/                     # Vibe Kanban manager
│   │   └── github/                   # GitHub sync manager
│   │
│   └── 07-operations/
│       └── runtime/
│           └── ralphy/               # Ralphy integration
│
├── 5-project-memory/
│   └── siso-internal/
│       ├── operations/
│       │   ├── WORK-LOG.md           # Auto-generated work log
│       │   ├── agents/               # Agent sessions
│       │   ├── ralphy/               # Ralphy sessions
│       │   └── reflections/          # Completion reflections
│       │
│       ├── decisions/                 # ALL ADRs go here
│       │   └── INDEX.md
│       │
│       ├── knowledge/                 # Learned patterns
│       └── plans/                     # PRDs, Epics, Tasks
│
├── 1-docs/
│   ├── 01-theory/                    # Architecture
│   ├── 02-implementation/            # Implementation guides
│   └── 03-guides/                    # How-to guides
│
├── .claude/
│   ├── settings.json                 # Hook configuration
│   └── hooks/                        # 21+ hook scripts
│       ├── load-agents-context.sh    # ⭐ Auto-loads AGENTS.md
│       └── README.md                 # Hook documentation
│
└── AGENT-SYSTEM-SUMMARY.md            # Setup summary
```

---

## Success Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| AGENTS.md loaded | 100% | Every session starts with behavioral contract |
| Work logging coverage | 100% | All edits appear in WORK-LOG.md |
| Decision capture rate | 80% | Decisions recorded in decisions/ |
| Completion validation | 100% | "Done" only after full checklist |
| Context overflow failures | 0 | No "context exceeded" errors |
| Technical debt visibility | 100% | All TODO tracked |
| First principles usage | 90% | Complex problems use framework |

---

## Troubleshooting

### AGENTS.md Not Loading

1. **Check hook exists**:
```bash
ls -la .claude/hooks/load-agents-context.sh
```

2. **Check it's executable**:
```bash
chmod +x .claude/hooks/load-agents-context.sh
```

3. **Check settings.json**:
```json
"SessionStart": [
  {
    "hooks": [
      { "command": ".claude/hooks/load-agents-context.sh" },
      ...
    ]
  }
]
```

### Wrong Behavior Enforced

1. **Edit AGENTS.md** (not the hook)
2. **Test with fresh session**
3. **Update AGENT-SYSTEM.md** if architecture changed

### Hook Not Firing

1. **Check matcher pattern** in settings.json
2. **Test manually**: `echo '{}' | .claude/hooks/my-hook.sh`
3. **Check permissions**: `ls -la .claude/hooks/*.sh`

---

## References

- **AGENTS.md** (root): Behavioral contract (auto-loaded)
- **.claude/hooks/README.md**: Complete hooks documentation
- **5-project-memory/siso-internal/operations/AGENT-REFERENCE.md**: Quick reference
- **2-engine/02-agents/capabilities/skills-cap/SKILLS-REGISTRY.md**: All skills

---

**This is internal system documentation. Keep it synchronized with AGENTS.md.**
**When updating behaviors, update AGENTS.md first, then this file.**
**Version 2.0.0 - Refocused on behavioral contract, not just reference.**
