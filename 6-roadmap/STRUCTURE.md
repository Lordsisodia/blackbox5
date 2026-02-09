# BlackBox5 Roadmap - Structure Guide

> **Purpose**: Help AI agents and humans understand the roadmap structure
> **Principle**: File system IS the documentation (mirrors memory system pattern)

**Last Updated:** 2026-01-20

---

## Quick Start for AI Agents

### Finding Information

| Question | Query | Files to Check |
|----------|-------|----------------|
| What should I work on? | `next action` | `STATE.yaml` → `next_action` |
| What's ready to start? | `ready plans` | `STATE.yaml` → `plans.ready_to_start` |
| What's blocking X? | `blocking {PLAN}` | `STATE.yaml` → `dependencies.blocking` |
| Plan details? | `{PLAN-ID} details` | `03-planned/{PLAN-ID}/metadata.yaml` |
| Full plan? | `{PLAN-ID} plan` | `03-planned/{PLAN-ID}/plan.md` |

### First Steps

```bash
# 1. Check next action
grep "next_action" STATE.yaml

# 2. Get quick details
cat 03-planned/PLAN-*/metadata.yaml

# 3. Read summary
cat 03-planned/PLAN-*/README.md

# 4. Read full plan
cat 03-planned/PLAN-*/plan.md
```

---

## Directory Structure

```
6-roadmap/
├── STATE.yaml              # Single source of truth (machine-readable)
├── QUERIES.md              # Agent query guide (how to find things)
├── INDEX.yaml              # Master index (with paths)
├── roadmap.md              # Human dashboard
├── STRUCTURE.md            # This file
│
├── research/               # Research documentation & analysis
│   ├── BLACKBOX5-RESEARCH-CATEGORIES.md
│   ├── BLACKBOX5-VISION-AND-FLOW.md
│   ├── FIRST-PRINCIPLES-ANALYSIS.md
│   ├── VALIDATION-PLAN.md
│   ├── RESEARCH-AGENTS-STATUS.md
│   └── research-agents-setup.md
│
├── (moved to ../../1-docs/guides/)  # How-to guides and execution plans now in 1-docs
│
├── archives/               # Historical summaries & completed reports
│   ├── ROADMAP-SUMMARY.md
│   ├── COMPLETE-SUMMARY.md
│   ├── QUICK-WINS-SUMMARY.md
│   ├── SESSION-SUMMARY.md
│   └── RESUMPTION-POINT.md
│
├── templates/              # Document templates for creating items
│   ├── active-template.md
│   ├── completed-template.md
│   ├── design-template.md
│   ├── plan-template.md
│   ├── proposal-template.md
│   └── research-template.md
│
├── frameworks/             # Framework research & analysis
├── first-principles/       # First principles deep analysis & validations
│
├── 00-proposed/            # Initial ideas (19 proposals)
│   └── {PROPOSAL-ID}/
│       ├── metadata.yaml   # Machine-readable metadata
│       ├── README.md       # Human summary (optional)
│       └── proposal.md    # Full proposal
│
├── 01-research/            # Investigation phase
│   └── {RESEARCH-ID}/
│       ├── metadata.yaml
│       ├── README.md
│       └── research.md
│
├── 02-design/              # Technical design phase
│   └── {DESIGN-ID}/
│       ├── metadata.yaml
│       └── design.md
│
├── 03-planned/             # Ready to implement
│   └── {PLAN-ID}/
│       ├── metadata.yaml   # {id, priority, effort, dependencies}
│       ├── README.md       # Executive summary
│       ├── plan.md         # Full plan
│       ├── tasks/          # Sub-tasks (if needed)
│       └── context/        # Related docs (if needed)
│
├── 04-active/              # Currently in progress
│   └── {ACTIVE-ID}/
│       ├── metadata.yaml
│       ├── progress.md     # Daily progress
│       └── outputs/
│
├── 05-completed/           # Shipped items
│   └── YYYY/
│       └── {COMPLETED-ID}/
│           ├── metadata.yaml
│           └── report.md
│
├── 06-cancelled/           # Cancelled items
└── 07-backlog/             # Not prioritized
```

---

## Item Folder Structure

Every item (proposal/research/design/plan/active/completed) follows this pattern:

```
{ID}-{name}/
├── metadata.yaml           # REQUIRED - Machine-readable
├── README.md               # OPTIONAL - Human summary
├── {content}.md            # REQUIRED - Full content
├── tasks/                  # OPTIONAL - Sub-tasks
├── context/                # OPTIONAL - Related docs
└── artifacts/              # OPTIONAL - Generated artifacts
```

### metadata.yaml Format

```yaml
id: "PLAN-001"
name: "Fix Skills System"
slug: "fix-skills-system"
status: "planned"           # proposed|research|design|planned|active|completed|cancelled
priority: "critical"        # critical|high|medium|low|immediate
effort: "1-2 days"
domain: "skills"
category: "bugfix"

created: "2026-01-20"
updated: "2026-01-20"

dependencies:
  requires: ["PLAN-002"]
  blocks: ["PLAN-003"]
  blocked_by: ["PLAN-001"]

problem:
  summary: "What's broken"
  impact: "Why it matters"

solution:
  approach: "How we'll fix it"

success_criteria:
  - criterion_1: true
  - criterion_2: true

confidence: "high"
ready_to_execute: true
```

---

## File Purposes

| File | Purpose | Who Uses It |
|------|---------|-------------|
| `STATE.yaml` | Single source of truth | AI agents (primary), humans |
| `QUERIES.md` | Query patterns | AI agents |
| `roadmap.md` | Human dashboard | Humans |
| `INDEX.yaml` | Master index | Both |
| `{item}/metadata.yaml` | Item metadata | AI agents |
| `{item}/README.md` | Human summary | Humans |
| `{item}/plan.md` | Full content | Both |

---

## Workflows

### Starting Work (AI Agent)

```bash
# 1. Check next action
next_action=$(grep "next_action" STATE.yaml | cut -d: -f2 | tr -d ' ')

# 2. Get details
cat 03-planned/$next_action/metadata.yaml

# 3. Read summary
cat 03-planned/$next_action/README.md

# 4. Read full plan
cat 03-planned/$next_action/plan.md
```

### Creating a New Plan

```bash
# 1. Create folder
mkdir 03-planned/PLAN-XXX-name

# 2. Create metadata.yaml
# Use template from templates/plan-metadata.yaml

# 3. Create README.md
# Use template from templates/plan-readme.md

# 4. Create plan.md
# Use template from templates/plan-template.md

# 5. Update STATE.yaml
# Add to plans.ready_to_start or plans.blocked

# 6. Update INDEX.yaml
# Add to improvements.planned
```

### Moving Items Between Stages

```bash
# Planned → Active
mv 03-planned/PLAN-XXX-name 04-active/ACTIVE-XXX-name

# Update metadata.yaml: status: "active"
# Update STATE.yaml: move from planned to active

# Active → Completed
mv 04-active/ACTIVE-XXX-name 05-completed/$(date +%Y)/COMPLETED-XXX-name

# Update metadata.yaml: status: "completed"
# Update STATE.yaml: move from active to completed
```

---

## Key Design Principles

1. **Single Source of Truth** - `STATE.yaml` is authoritative
2. **File System IS Documentation** - Structure conveys meaning
3. **Metadata Separation** - `metadata.yaml` for machines, `README.md` for humans
4. **Flat Structure** - Avoid deep nesting
5. **Predictable Paths** - `{stage}/{ID}-{name}/` pattern

---

## Comparison with Memory System

This structure mirrors the proven memory system pattern:

| Roadmap | Memory | Purpose |
|---------|--------|---------|
| `STATE.yaml` | `STATE.yaml` | Single source of truth |
| `QUERIES.md` | `QUERIES.md` | Agent query guide |
| `roadmap.md` | `ACTIVE.md` | Human dashboard |
| `03-planned/{PLAN-ID}/` | `plans/active/{feature}/` | Item folders |
| `metadata.yaml` | `metadata.yaml` | Item metadata |

---

## Related Documents

- **QUERIES.md**: Detailed query patterns for AI agents
- **STATE.yaml**: Single source of truth
- **roadmap.md**: Human dashboard
- **INDEX.yaml**: Master index

---

**Maintenance**: When adding new item types or changing structure, update this file first.

**Principle**: Make it easy for agents to understand and navigate the roadmap without meta-documentation.
