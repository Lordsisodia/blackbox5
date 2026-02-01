# QUERIES.md - Roadmap Query Guide

> **Purpose**: Help AI agents find roadmap information quickly without browsing file systems
> **Principle**: Query layer > browse layer for AI agents
> **Pattern**: Mirrors the memory system's QUERIES.md

**Last Updated**: 2026-01-20
**Maintainer**: Update when adding new query patterns

---

## Quick Reference

| Question | Query | Files to Check |
|----------|-------|----------------|
| What should I work on? | `next action` | `STATE.yaml` → `next_action` |
| What's ready to start? | `ready plans` | `STATE.yaml` → `plans.ready_to_start` |
| What's blocking X? | `blocking` | `STATE.yaml` → `dependencies.blocking` |
| Plan details? | `{PLAN-ID} details` | `03-planned/{PLAN-ID}/metadata.yaml` |
| Full plan? | `{PLAN-ID} plan` | `03-planned/{PLAN-ID}/plan.md` |
| Proposal summary? | `{PROPOSAL-ID}` | `00-proposed/{PROPOSAL-ID}/README.md` |
| Research findings? | `{RESEARCH-ID}` | `01-research/{RESEARCH-ID}/findings/` |
| Overall status? | `roadmap status` | `roadmap.md` or `STATE.yaml` → `stats` |

---

## Query Patterns

### Pattern 1: "What should I work on?"

**Agent Types**: All agents starting work

**Query**: `next action` or `what should i work on`

**What to Check**:
1. **First**: `STATE.yaml` → `next_action` (single best answer)
2. **Then**: `03-planned/{next_action}/metadata.yaml` (quick details)
3. **Finally**: `03-planned/{next_action}/README.md` (human summary)

**Example Response Structure**:
```
Next Action: PLAN-001
- Name: Fix Skills System Critical Issues
- Priority: critical
- Effort: 1-2 days
- Dependencies: None
- Path: 03-planned/PLAN-001-fix-skills-system/

Quick Summary:
[from README.md - 3-5 lines]

Next Steps:
[from plan.md or README.md]
```

**When to Use**:
- Agent session starts
- Looking for next task
- "What should I do?" questions

---

### Pattern 2: "What's ready to start?"

**Agent Types**: PMs looking for assignable work

**Query**: `ready plans` or `what can i start`

**What to Check**:
1. **First**: `STATE.yaml` → `plans.ready_to_start` (all unblocked plans)
2. **Filter**: By priority, domain, or effort
3. **Then**: Read individual `metadata.yaml` files

**Example Response Structure**:
```
Ready to Start (5 plans):

Critical Priority:
- PLAN-001: Fix Skills System (1-2 days)
- PLAN-004: Fix Import Paths (1-2 days)

Immediate Priority (Quick Wins):
- PLAN-005: Initialize Vibe Kanban (1-2 hours)
- PLAN-007: Enable 90% Compression (15 min)

High Priority:
- PLAN-006: Remove Duplicates (3-5 days)

Details:
For full details, check each plan's metadata.yaml
```

**When to Use**:
- Planning work allocation
- Finding quick wins
- Parallelization opportunities

---

### Pattern 3: "What's blocking X?"

**Agent Types**: PMs, developers blocked by dependencies

**Query**: `blocking {PLAN-ID}` or `why is {PLAN-ID} blocked`

**What to Check**:
1. **First**: `STATE.yaml` → `dependencies.blocked`
2. **Then**: `STATE.yaml` → `plans.blocked`
3. **Context**: Check blocking plans' status

**Example Response Structure**:
```
PLAN-003 is blocked by:
- PLAN-001: Fix Skills System (status: planned)
- PLAN-002: Fix YAML Loading (status: planned, blocked by PLAN-001)
- PLAN-005: Initialize Vibe Kanban (status: planned)

Critical Path:
1. Complete PLAN-001 (1-2 days)
2. Complete PLAN-002 (1 day)
3. Complete PLAN-005 (1-2 hours)
4. Then PLAN-003 can start (3-5 days)

Minimum time to unblock: 2-3 days
```

**When to Use**:
- Understanding dependencies
- Planning critical path
- Resolving blockers

---

### Pattern 4: "Tell me about {PLAN-ID}"

**Agent Types**: All agents

**Query**: `{PLAN-ID} details` or `{PLAN-ID} plan`

**What to Check**:
1. **First**: `03-planned/{PLAN-ID}/metadata.yaml` (machine-readable)
2. **Then**: `03-planned/{PLAN-ID}/README.md` (human summary)
3. **Full details**: `03-planned/{PLAN-ID}/plan.md`

**Example Response Structure**:
```
PLAN-001: Fix Skills System Critical Issues

Status:
- Priority: critical
- Effort: 1-2 days
- Status: planned
- Dependencies: None
- Blocks: PLAN-002, PLAN-003

Problem:
[from README.md - what's broken]

Solution:
[from README.md - what we're doing]

Files to Change:
[from metadata.yaml or plan.md]

Risk Level: High (core system)
Confidence: High (clear fix)
```

**When to Use**:
- Understanding a specific plan
- Estimating work
- Checking if plan is relevant

---

### Pattern 5: "What proposals exist?"

**Agent Types**: PMs, researchers

**Query**: `proposals` or `proposals {domain}`

**What to Check**:
1. **First**: `STATE.yaml` → `proposals` (indexed by tier)
2. **Filter**: By domain, priority, or weight
3. **Then**: Read individual `README.md` files

**Example Response Structure**:
```
Proposals by Tier:

Critical (Tier 1) - 66% weight:
- PROPOSAL-001: Memory & Context (18%)
- PROPOSAL-002: Reasoning & Planning (17%)
- PROPOSAL-003: Skills & Capabilities (16%)
- PROPOSAL-004: Execution & Safety (15%)

High (Tier 2) - 39% weight:
- PROPOSAL-005: Agent Types (12%)
...

For Skills Domain:
- PROPOSAL-003: Skills & Capabilities Research
  Path: 00-proposed/PROPOSAL-003-skills-capabilities/
```

**When to Use**:
- Planning research phase
- Understanding domain coverage
- Prioritizing research

---

### Pattern 6: "What did we learn from {RESEARCH-ID}?"

**Agent Types**: Architects, researchers

**Query**: `{RESEARCH-ID} findings` or `{RESEARCH-ID} research`

**What to Check**:
1. **First**: `01-research/{RESEARCH-ID}/metadata.yaml` (summary)
2. **Then**: `01-research/{RESEARCH-ID}/findings/` (flat structure)
3. **Full**: `01-research/{RESEARCH-ID}/research.md`

**Example Response Structure**:
```
VALIDATION-001: Comprehensive Validation Report

Status: Complete
Date: 2026-01-19
Domain: validation

Key Findings:
[from findings/ - each file is a finding]

Summary:
[from metadata.yaml or research.md]

Recommendations:
[from research.md]

Related Plans:
[linked from metadata.yaml]
```

**When to Use**:
- Understanding research results
- Applying findings to plans
- Making decisions

---

### Pattern 7: "What's the overall roadmap status?"

**Agent Types**: PMs, stakeholders

**Query**: `roadmap status` or `overall status`

**What to Check**:
1. **First**: `roadmap.md` (human dashboard)
2. **Then**: `STATE.yaml` → `stats` (machine-readable)

**Example Response Structure**:
```
BlackBox5 Roadmap Status:

Summary:
- Total Items: 27
- Proposed: 19
- Planned: 7
- Active: 0
- Completed: 1

Current Focus: Planning Phase
Next Action: PLAN-001

By Priority:
- Critical: 6
- High: 5
- Medium: 7
- Low: 5

By Domain:
- Infrastructure: 12
- Agents: 6
- Skills: 2
- Memory: 2
- ...
```

**When to Use**:
- Status checks
- Reporting
- Understanding overall progress

---

## Agent-Specific Queries

### For PM Agents (John)
**Common Queries**:
- `next action` - What should we work on?
- `ready plans` - What's assignable?
- `blocking {PLAN}` - What's blocked?
- `roadmap status` - Overall status

**Primary Files**:
- `STATE.yaml`
- `roadmap.md`
- Individual `README.md` files

---

### For Architect Agents (Winston)
**Common Queries**:
- `{PLAN-ID} details` - Technical details
- `{PROPOSAL-ID}` - Research proposals
- `blocking {PLAN}` - Dependencies
- `{domain} proposals` - Domain-specific research

**Primary Files**:
- `STATE.yaml` → proposals
- Individual `plan.md` files
- `01-research/*/findings/`

---

### For Developer Agents (Arthur)
**Common Queries**:
- `next action` - What to work on
- `{PLAN-ID} plan` - Full implementation plan
- `ready plans` - Pick something to do
- `{PLAN-ID} details` - Quick specs

**Primary Files**:
- `STATE.yaml` → next_action
- `03-planned/*/plan.md`
- `03-planned/*/metadata.yaml`

---

## Search Strategies

### When You Don't Know the ID

1. **Use STATE.yaml first**:
   - Check `plans.ready_to_start` for assignable work
   - Check `plans.blocked` for blocked items
   - Check `proposals` for research

2. **Use domain filters**:
   - `STATE.yaml` → `proposals.critical` for high-priority research
   - `STATE.yaml` → `status_by_domain` for domain-specific items

3. **Use priority filters**:
   - `STATE.yaml` → `status_by_priority` for priority breakdown

### Finding Related Information

**From a Plan**:
1. Read `metadata.yaml` for links
2. Check `dependencies` in `STATE.yaml`
3. Check `blocks` in `STATE.yaml` for what this enables

**From a Proposal**:
1. Read `README.md` for summary
2. Read `proposal.md` for details
3. Check `linked_plans` in `metadata.yaml`

**From Research**:
1. Read `findings/` folder (flat structure)
2. Check `linked_plans` in `metadata.yaml`
3. Check `recommendations` in `research.md`

---

## Quick Start

### New Agent Session

```bash
# 1. Check next action
grep "next_action" STATE.yaml

# 2. Get quick details
cat 03-planned/PLAN-*/metadata.yaml

# 3. Read summary
cat 03-planned/PLAN-*/README.md
```

### Before Starting Work

```bash
# 1. Check if blocked
grep -A 10 "blocked:" STATE.yaml

# 2. Check dependencies
grep -A 20 "dependencies:" STATE.yaml

# 3. Read full plan
cat 03-planned/PLAN-XXX/plan.md
```

### After Completing Work

```bash
# 1. Update plan status
# Edit 03-planned/PLAN-XXX/metadata.yaml

# 2. Move to next stage
# mv 03-planned/PLAN-XXX 04-active/ACTIVE-XXX

# 3. Update STATE.yaml
# Edit STATE.yaml stats and plans
```

---

## Best Practices

### For Agents

1. **Start with STATE.yaml** - It's the single source of truth
2. **Use metadata.yaml** - Machine-readable, quick to parse
3. **Check README.md** - Human-readable summaries
4. **Read plan.md** - Only when you need full details
5. **Follow dependencies** - Check `blocked` and `blocking` in STATE.yaml

### For Humans

1. **Use roadmap.md** - Human dashboard
2. **Use STATE.yaml** - For detailed status
3. **Update metadata.yaml** - When plan status changes
4. **Keep structure clean** - One folder per item
5. **Update STATE.yaml** - When moving items between stages

---

## Related Documents

- **STATE.yaml**: Single source of truth
- **roadmap.md**: Human dashboard
- **INDEX.yaml**: Master index (legacy, may deprecate)

---

**Maintenance**: Update this file when:
- Adding new query patterns
- Changing file structure
- Discovering better search strategies

**Principle**: Make it easy for agents to find information without browsing file systems.
