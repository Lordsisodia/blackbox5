# BlackBox5 Agent System Architecture

## Visual Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BLACKBOX5 AGENT SYSTEM                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        CORE INFRASTRUCTURE                           │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                     │   │
│  │  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐            │   │
│  │  │ BaseAgent    │   │ AgentLoader  │   │ SkillManager │            │   │
│  │  │ (Abstract)   │   │ (Discovery)  │   │ (Skills)     │            │   │
│  │  │              │   │              │   │              │            │   │
│  │  │ ✅ WORKING   │   │ ✅ WORKING   │   │ ⚠️ 0 SKILLS  │            │   │
│  │  └──────────────┘   └──────────────┘   └──────────────┘            │   │
│  │         │                   │                   │                  │   │
│  └─────────┼───────────────────┼───────────────────┼──────────────────┘   │
│            │                   │                   │                      │
│            ▼                   ▼                   ▼                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                          CORE AGENTS (3)                            │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                     │   │
│  │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │   │
│  │   │              │  │              │  │              │             │   │
│  │   │  Developer   │  │   Analyst    │  │  Architect   │             │   │
│  │   │   Agent      │  │    Agent     │  │    Agent     │             │   │
│  │   │              │  │              │  │              │             │   │
│  │   │  (Amelia 💻) │  │  (Mary 📊)   │  │  (Alex 🏗️)   │             │   │
│  │   │              │  │              │  │              │             │   │
│  │   │  ✅ WORKING  │  │  ✅ WORKING  │  │  ✅ WORKING  │             │   │
│  │   └──────────────┘  └──────────────┘  └──────────────┘             │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    ORCHESTRATION LAYER                              │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                     │   │
│  │  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐            │   │
│  │  │ Orchestrator │   │  BMAD Orch.  │   │ EventBus     │            │   │
│  │  │              │   │              │   │              │            │   │
│  │  │ ✅ IMPLEMENTED│   │ ✅ IMPLEMENTED│  │ ✅ WORKING   │            │   │
│  │  │ ⚠️ UNTESTED  │   │ ⚠️ UNTESTED  │   │              │            │   │
│  │  └──────────────┘   └──────────────┘   └──────────────┘            │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                 SPECIALIST AGENTS (Not Discovered)                   │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                     │   │
│  │  🔄 YAML Agents (18) - NOT LOADED BY AGENTLOADER                     │   │
│  │     ├── BMAD Agents (10) - pm, dev, architect, analyst, etc.        │   │
│  │     ├── Specialist Agents (8) - orchestrator, custom, etc.          │   │
│  │     └── Location: /02-agents/implementations/                       │   │
│  │                                                                     │   │
│  │  🔄 Ralph Agent - Autonomous execution specialist                   │   │
│  │  🔄 Lumelle - Architect specialist                                  │   │
│  │  🔄 Custom Agents - Various specialized roles                       │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    SKILLS & CAPABILITIES                            │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                     │   │
│  │  ⚠️ SKILL MANAGER ISSUE: 0 SKILLS DISCOVERED                        │   │
│  │                                                                     │   │
│  │  Skills exist but not discovered:                                   │   │
│  │  ├── planning/      (story, epic, prd, architecture)               │   │
│  │  ├── kanban/        (board, setup)                                  │   │
│  │  ├── context/       (storage, manager, snapshot)                    │   │
│  │  └── research/      (semantic_search)                               │   │
│  │                                                                     │   │
│  │  🔄 PLANNING AGENT: Not implemented (exists as skills)               │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component Status Summary

| Component | Status | Notes |
|-----------|--------|-------|
| **BaseAgent** | ✅ Working | All agents inherit properly |
| **AgentLoader** | ✅ Working | Discovers 3/21 agents (only core) |
| **SkillManager** | ⚠️ Issue | 0 skills discovered (fixable) |
| **DeveloperAgent** | ✅ Working | Executes tasks successfully |
| **AnalystAgent** | ✅ Working | Executes tasks successfully |
| **ArchitectAgent** | ✅ Working | Executes tasks successfully |
| **Orchestrator** | ⚠️ Untested | Implemented but not validated |
| **BMAD Orchestrator** | ⚠️ Untested | Implemented but not validated |
| **YAML Agents (18)** | 🔄 Not Loaded | Not in AgentLoader search path |
| **Skills (planning, etc.)** | ❌ Not Found | Discovery pattern mismatch |
| **Planning Agent** | ⚠️ Missing | Exists as skills, not agent |

## Data Flow

```
┌─────────────┐
│   USER      │
│  REQUEST    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│AgentLoader  │ Discovers & loads agents
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ BaseAgent   │ Provides interface
└──────┬──────┘
       │
       ├──▶ ┌──────────────┐
       │    │DeveloperAgent│ Executes coding tasks
       │    └──────────────┘
       │
       ├──▶ ┌──────────────┐
       │    │ AnalystAgent  │ Executes research tasks
       │    └──────────────┘
       │
       ├──▶ ┌──────────────┐
       │    │ArchitectAgent│ Executes design tasks
       │    └──────────────┘
       │
       ▼
┌─────────────┐
│ Orchestrator│ Coordinates multi-agent workflows
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  RESULTS    │
└─────────────┘
```

## Key Findings

### ✅ What Works (3 Critical Items)

1. **Core Agent Infrastructure** - BaseAgent, AgentLoader fully functional
2. **Agent Execution** - All 3 core agents execute tasks successfully
3. **Agent Discovery** - AgentLoader discovers all core Python agents

### ⚠️ What Needs Work (3 Issues)

1. **SkillManager** - Returns 0 skills (discovery pattern mismatch)
2. **YAML Agent Loading** - 18 specialist agents not discovered
3. **Orchestrator Testing** - Implemented but not integration tested

### 🔄 Missing Components

1. **Planning Agent** - Not implemented (exists as skills)
2. **Unified Agent Registry** - No single source of truth for all agents
3. **Skill-to-Agent Mapping** - Skills not attached to agents

## Recommendations Priority

### HIGH (Fix Immediately)

1. **Fix SkillManager Discovery**
   - Add metadata decorators to skill classes
   - OR update SkillManager pattern matching
   - Target: Discover 10+ planning/kanban/context skills

2. **Document Agent Registry**
   - List all 3 core agents
   - Document 18 YAML specialist agents
   - Map capabilities to use cases

### MEDIUM (Next Sprint)

3. **Unify Agent Discovery**
   - Extend AgentLoader search path
   - Load both Python and YAML agents
   - Single agent registry

4. **Test Orchestrator**
   - Integration tests with core agents
   - Workflow execution validation
   - Error handling verification

### LOW (Backlog)

5. **Create Planning Agent** (Optional)
   - If dedicated agent preferred over skills
   - OR document skill-based approach

6. **Consolidate Duplicates**
   - Multiple AgentLoaders
   - Multiple Orchestrators
   - Clarify purpose or consolidate

## File Locations Reference

```
blackbox5/2-engine/
├── 01-core/agents/
│   ├── core/
│   │   ├── base_agent.py           ✅ Main agent class
│   │   ├── agent_loader.py         ✅ Discovery system
│   │   └── skill_manager.py        ⚠️ Needs fix
│   ├── DeveloperAgent.py           ✅ Working
│   ├── AnalystAgent.py             ✅ Working
│   ├── ArchitectAgent.py           ✅ Working
│   └── orchestration/
│       ├── Orchestrator.py         ⚠️ Untested
│       └── orchestrator_deviation_integration.py
│
├── 02-agents/
│   ├── capabilities/skills-cap/    ⚠️ Skills not discovered
│   │   ├── planning/
│   │   ├── kanban/
│   │   ├── context/
│   │   └── research/
│   └── implementations/
│       ├── 02-bmad/                🔄 18 YAML agents (not loaded)
│       └── 04-specialists/         🔄 Ralph, Lumelle, custom
│
└── 07-operations/
    └── environment/lib/python/core/runtime/
        ├── agent_loader.py         🔄 Duplicate?
        └── orchestrator.py         🔄 BMAD version
```

## Test Execution Summary

| Test # | Description | Result | Details |
|--------|-------------|--------|---------|
| 1 | Import BaseAgent | ✅ PASS | All classes imported |
| 2 | Import AgentLoader | ✅ PASS | Class imported |
| 3 | Import SkillManager | ✅ PASS | Class imported |
| 4 | Agent Discovery | ✅ PASS | 3/3 core agents found |
| 5 | BaseAgent Inheritance | ✅ PASS | All agents inherit properly |
| 6 | Agent Execution | ✅ PASS | All agents execute tasks |
| 7 | SkillManager Discovery | ❌ FAIL | 0 skills discovered |

**Overall: 6/7 tests passing (86%)**

---

**Generated:** 2026-01-20
**Validator:** Claude Code Agent System Validator
**Duration:** ~30 minutes
**Files Analyzed:** 50+
**Agents Validated:** 3 core, 18 YAML (not loaded)
**Lines of Code Reviewed:** ~5,000+
