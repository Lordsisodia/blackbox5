# Skills Integration Visual Guide

**Date**: 2026-01-28
**Purpose**: Visual representation of the skills integration plan

---

## Before Integration (Current State)

```
┌─────────────────────────────────────────────────────────────┐
│                    Black Box 5 Agent                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Current Skill Access                                │  │
│  │  ─────────────────────────────────────────────────  │  │
│  │  • Engine skills: Via SkillManager (Python API)     │  │
│  │  • Agent skills: Manual filesystem reads             │  │
│  │  • MCP skills: Via MCP server integration            │  │
│  │  • No unified discovery                               │  │
│  │  • No on-demand loading                               │  │
│  │  • Manual process                                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Problems**:
- ❌ No unified skill discovery
- ❌ No on-demand loading (token inefficient)
- ❌ No Agent Skills Standard compatibility
- ❌ Manual skill loading process

---

## After Integration (Target State)

```
┌─────────────────────────────────────────────────────────────────┐
│                        Black Box 5 Agent                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Skill Orchestration Layer (NEW)                       │    │
│  │  ────────────────────────────────────────────────────  │    │
│  │  ✓ Unified skill discovery                           │    │
│  │  ✓ On-demand loading (token efficient)               │    │
│  │  ✓ Skill routing (Tier 1 vs Tier 2)                  │    │
│  │  ✓ Caching and context management                    │    │
│  │  ✓ Analytics and monitoring                          │    │
│  └────────────────────────────────────────────────────────┘    │
│                          ↕                                     │
│           ┌─────────────┴─────────────┐                       │
│           ↓                           ↓                       │
│  ┌─────────────────────┐   ┌─────────────────────────┐    │
│  │  Tier 1: Engine     │   │  Tier 2: Agent Skills   │    │
│  │  Skills            │   │  (Agent Skills Standard)│    │
│  ├─────────────────────┤   ├─────────────────────────┤    │
│  │ • SkillManager     │   │ • ~/.claude/skills/     │    │
│  │ • Python classes   │   │ • SKILL.md files       │    │
│  │ • JSON metadata    │   │ • YAML frontmatter     │    │
│  │ • Runtime import   │   │ • On-demand load       │    │
│  │ • Engine-internal  │   │ • Cross-platform       │    │
│  │                     │   │ • Token-efficient      │    │
│  │ Used for:          │   │                         │    │
│  │ • Memory ops       │   │ Used for:               │    │
│  │ • Task orchestrate  │   │ • Database operations  │    │
│  │ • Hook management  │   │ • Git workflows        │    │
│  │ • Agent lifecycle   │   │ • Testing patterns     │    │
│  └─────────────────────┘   │ • Process workflows    │    │
│                             │ • Integration          │    │
│                             └─────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Skill Loading Flow

```
User Request
     │
     ↓
┌─────────────────┐
│ Agent Receives  │
│ Request         │
└────────┬────────┘
         │
         ↓
┌─────────────────────────┐
│ Agent Identifies Need    │
│ for Specific Skill       │
└────────┬──────────────────┘
         │
         ↓
┌─────────────────────────┐
│ agent.load_skill()       │
│                         │
│ ┌─────────────────────┐ │
│ │ SkillOrchestrator    │ │
│ ├─────────────────────┤ │
│ │ 1. Check Cache      │ │
│ │    (hit?) → Return   │ │
│ │                     │ │
│ │ 2. Discover Skill   │ │
│ │    (which tier?)    │ │
│ │                     │ │
│ │ 3. Load Content    │ │
│ │    (Tier 1 or 2)   │ │
│ │                     │ │
│ │ 4. Cache Result    │ │
│ └─────────────────────┘ │
└────────┬──────────────────┘
         │
         ↓
┌─────────────────────────┐
│ Skill Content Injected   │
│ into Agent Context        │
└────────┬──────────────────┘
         │
         ↓
┌─────────────────────────┐
│ Agent Uses Skill to      │
│ Complete Task            │
└────────┬──────────────────┘
         │
         ↓
┌─────────────────────────┐
│ Analytics Tracked:       │
│ • Skill discovery        │
│ • Skill load             │
│ • Skill usage            │
│ • Token usage            │
└─────────────────────────┘
```

---

## Agent Skill Usage Example

### Example: Amelia (Developer) Needs to Run Database Migration

**Before** (Current):
```python
# Amelia has to:
1. Remember to look for database migration skill
2. Find the skill file manually
3. Read and understand the skill
4. Execute the migration
5. Hope she didn't miss anything
```

**After** (With Integration):
```python
# Amelia's workflow:

# 1. Request skill (automatic)
amelia: "Load the supabase-operations skill"

# 2. Skill orchestrator handles it
SkillOrchestrator:
  - Checks cache (miss)
  - Discovers skill (Tier 2)
  - Loads SKILL.md
  - Caches content
  - Returns to agent

# 3. Amelia uses skill
amelia: "Use the supabase-operations skill to execute migration"

# 4. Skill content provides:
- Step-by-step instructions
- Command examples
- Troubleshooting guide
- Best practices

# 5. Migration completes successfully
# 6. Analytics tracked automatically
```

---

## Token Efficiency Comparison

### Before (Manual Loading)

```
Agent Context:
├─ System prompt:           5,000 tokens
├─ Task description:        1,000 tokens
├─ ALL skill files:         20,000 tokens  ← Always loaded!
│   └─ Even if not needed
├─ Code context:            10,000 tokens
└─ Total:                   36,000 tokens
```

### After (On-Demand Loading)

```
Agent Context:
├─ System prompt:           5,000 tokens
├─ Task description:        1,000 tokens
├─ Requested skill ONLY:    1,000 tokens  ← Loaded on-demand!
│   └─ Just what's needed
├─ Code context:            10,000 tokens
└─ Total:                   17,000 tokens

Token Savings: 19,000 tokens (53% reduction)
```

---

## Agent-Skill Mappings

### Amelia 💻 (Developer)

```
Required Skills:
├─ git-workflows           (Version control, branching)
├─ testing-patterns         (Unit, integration, E2E)
└─ supabase-operations     (Migrations, DDL, RLS)

Optional Skills:
├─ debugging-systematic    (Debug workflows)
└─ code-generation         (AI-assisted coding)
```

### Mary 📊 (Analyst)

```
Required Skills:
├─ data-analysis            (Statistics, insights)
├─ reporting                (Visualization, dashboards)
└─ siso-tasks-cli          (Task queries, analytics)

Optional Skills:
├─ research-methods         (Deep research techniques)
└─ documentation-generation  (Report creation)
```

### Alex 🏗️ (Architect)

```
Required Skills:
├─ system-design            (Architecture patterns)
├─ architecture-patterns    (Design patterns)
└─ documentation            (Design docs, specs)

Optional Skills:
├─ tech-stack-evaluation    (Technology decisions)
└─ api-design               (REST, GraphQL design)
```

### John 📋 (Product Manager)

```
Required Skills:
├─ feedback-triage          (Process feedback)
├─ feature-planning         (Backlog management)
└─ prd-creation            (Requirements docs)

Optional Skills:
├─ stakeholder-management   (Communication)
└─ roadmap-planning        (Release planning)
```

---

## Directory Structure

### Before (Current)

```
blackbox5/
├── 2-engine/
│   ├── 01-core/agents/
│   │   └── core/skill_manager.py      # Tier 1 only
│   └── 04-work/modules/skills/        # Mixed formats
│       ├── feedback-triage.md
│       ├── supabase-ddl-rls.md
│       ├── siso-tasks/
│       │   ├── prompt.md
│       │   └── skill.json
│       └── ...
└── ~/.claude/skills/                           # Doesn't exist!
```

### After (Target)

```
blackbox5/
├── 2-engine/
│   ├── 01-core/agents/
│   │   ├── core/skill_manager.py        # Tier 1 (unchanged)
│   │   └── base/agent.py              # Updated with skill methods
│   └── 02-orchestration/skills/        # NEW orchestration layer
│       ├── orchestrator.py
│       ├── scanner.py
│       ├── cache.py
│       ├── analytics.py
│       └── mappings.py
│
├── ~/.claude/skills/                        # NEW: Agent Skills Standard
│   ├── supabase-operations/
│   │   └── SKILL.md
│   ├── siso-tasks-cli/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── examples/
│   ├── feedback-triage/
│   │   └── SKILL.md
│   ├── git-workflows/
│   │   └── SKILL.md
│   ├── testing-patterns/
│   │   ├── unit-testing/
│   │   │   └── SKILL.md
│   │   └── integration-testing/
│   │       └── SKILL.md
│   └── notifications-local/
│       └── SKILL.md
│
└── blackbox5/.claude/skills/            # Project-specific skills
    └── project-specific-skill/
        └── SKILL.md
```

---

## Implementation Timeline

```
Week 1: Foundation              Week 2: Conversion
┌──────────────────┐          ┌──────────────────┐
│ • SkillOrchestrator │          │ • Convert 6      │
│ • SkillScanner     │          │   skills        │
│ • Directory setup  │          │ • Multi-project  │
│ • Agent updates   │          │   Supabase      │
│ • Unit tests       │          │ • Templates      │
└──────────────────┘          └──────────────────┘

Week 3: Integration           Week 4: Testing
┌──────────────────┐          ┌──────────────────┐
│ • Agent prompts   │          │ • Test framework │
│ • Skill loading   │          │ • Token metrics  │
│ • Skill mappings  │          │ • Analytics      │
│ • Context mgmt     │          │ • Documentation  │
│ • Integration     │          │ • Training       │
└──────────────────┘          └──────────────────┘
```

---

## Success Metrics Dashboard

### Real-time Metrics

```
┌─────────────────────────────────────┐
│  Skills Dashboard                     │
├─────────────────────────────────────┤
│                                         │
│  Total Skills:        13              │
│  ├─ Tier 1:          4               │
│  └─ Tier 2:          9               │
│                                         │
│  Active Agents:       4               │
│  ├─ Amelia 💻                        │
│  ├─ Mary 📊                          │
│  ├─ Alex 🏗️                          │
│  └─ John 📋                          │
│                                         │
│  Skill Usage Today:                   │
│  ├─ supabase-operations:  12         │
│  ├─ git-workflows:          8         │
│  ├─ feedback-triage:        3         │
│  └─ testing-patterns:       5         │
│                                         │
│  Token Efficiency:                    │
│  ├─ Cache hit rate:       85%        │
│  ├─ Avg load time:       0.3s       │
│  └─ Token savings:        53%        │
│                                         │
└─────────────────────────────────────┘
```

---

## Quick Start Guide

### For Agents

**How to Use Skills**:

1. **List Available Skills**
   ```
   "What skills are available?"
   ```

2. **Load a Skill**
   ```
   "Load the supabase-operations skill"
   ```

3. **Use a Skill**
   ```
   "Use the supabase-operations skill to execute migration"
   ```

### For Developers

**How to Create Skills**:

1. **Create Skill Directory**
   ```bash
   mkdir -p ~/.claude/skills/my-skill
   ```

2. **Create SKILL.md**
   ```yaml
   ---
   name: my-skill
   description: What this skill does
   tags: [category, keywords]
   ---

   # My Skill

   ## Purpose
   ...

   ## Commands
   ...
   ```

3. **Test with Agent**
   ```
   claude-code "Load the my-skill skill"
   ```

---

## Summary

This integration plan provides:

✅ **Unified skill system** - Single interface for all skills
✅ **Token efficiency** - On-demand loading saves 50%+ tokens
✅ **Agent compatibility** - Works with Claude Code and agents
✅ **Scalability** - Easy to add new skills
✅ **Analytics** - Track usage and optimize

**4-week implementation** to full production
**Low risk** with gradual rollout and rollback options

---

**Visual Guide Version**: 1.0.0
**Last Updated**: 2026-01-28
**Companion**: [SKILLS-INTEGRATION-PLAN.md](./SKILLS-INTEGRATION-PLAN.md)
