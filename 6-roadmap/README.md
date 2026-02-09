# BlackBox5 Roadmap

**Purpose**: Single source of truth for all planned, active, and completed work  
**Status**: Active  
**Last Updated**: 2026-01-30

---

## Quick Start

### For AI Agents
1. Check `STATE.yaml` for the next action
2. Use `QUERIES.md` for query patterns
3. Read item metadata from `{stage}/{ID}-{name}/metadata.yaml`

### For Humans
1. Read `roadmap.md` for the dashboard view
2. Browse folders by stage (00-proposed through 05-completed)
3. Check `STRUCTURE.md` for how the roadmap works

---

## Directory Structure

```
6-roadmap/
├── STATE.yaml              # Single source of truth (MACHINE-READABLE)
├── INDEX.yaml              # Master index with paths
├── QUERIES.md              # Query patterns for AI agents
├── roadmap.md              # Human dashboard
├── STRUCTURE.md            # How the roadmap system works
│
├── 00-proposed/            # Initial ideas (19 proposals)
├── 01-research/            # Investigation phase
├── 02-design/              # Technical design phase
├── 02-validation/          # Design validation
├── 03-planned/             # Ready to implement
├── 04-active/              # Currently in progress
├── 05-completed/           # Shipped items (by year)
│
├── research/               # Research documentation
├── first-principles/       # First principles analysis
├── frameworks/             # Framework research
├── (see ../../1-docs/guides/)  # How-to guides (moved to 1-docs)
├── archives/               # Historical summaries
└── templates/              # Document templates
```

---

## Stage Folders

| Stage | Folder | Purpose | Count |
|-------|--------|---------|-------|
| Proposed | `00-proposed/` | Initial ideas awaiting evaluation | 19 |
| Research | `01-research/` | Active investigation | Multiple |
| Design | `02-design/` | Technical design phase | Active |
| Validation | `02-validation/` | Design validation | Active |
| Planned | `03-planned/` | Ready to implement | Multiple |
| Active | `04-active/` | Currently in progress | 1 (PLAN-008) |
| Completed | `05-completed/` | Shipped items | By year |

---

## Key Documents

### System Files
| File | Purpose |
|------|---------|
| `STATE.yaml` | **Single source of truth** - Current state, next actions, blockers |
| `INDEX.yaml` | Master index of all items with paths |
| `QUERIES.md` | Query patterns for AI agents |
| `STRUCTURE.md` | How the roadmap system works |

### Human-Facing
| File | Purpose |
|------|---------|
| `roadmap.md` | Dashboard view of all work |
| `CRITICAL-GAPS-FINAL-REPORT.md` | Critical gaps analysis |
| `CRITICAL-GAPS-RESOLUTION-PLAN.md` | Plan to resolve gaps |

### Guides
| Location | Contents |
|----------|----------|
| `../../1-docs/guides/design/` | Design system documentation (moved) |
| `../../1-docs/guides/implementation/` | Implementation guides (moved) |
| `../../1-docs/guides/strategy/` | Testing and strategy guides (moved) |

---

## How to Use the Roadmap

### Finding What to Work On

```bash
# Check next action
grep "next_action:" STATE.yaml

# Check ready plans
grep -A 20 "ready_to_start:" STATE.yaml

# Check blocked items
grep -A 20 "blocked:" STATE.yaml
```

### Reading a Plan

```bash
# 1. Read metadata for overview
cat 03-planned/PLAN-XXX-name/metadata.yaml

# 2. Read README for summary
cat 03-planned/PLAN-XXX-name/README.md

# 3. Read plan.md for full details
cat 03-planned/PLAN-XXX-name/plan.md
```

### Moving Items Between Stages

```bash
# Planned → Active
mv 03-planned/PLAN-XXX-name 04-active/PLAN-XXX-name

# Update metadata.yaml status: active
# Update STATE.yaml

# Active → Completed
mv 04-active/PLAN-XXX-name 05-completed/2026/PLAN-XXX-name

# Update metadata.yaml status: completed
# Update STATE.yaml
```

---

## Active Work

### Currently In Progress
- **PLAN-008**: Fix Critical API Mismatches
  - Location: `04-active/PLAN-008-fix-critical-api-mismatches/`
  - Status: Active
  - Contents: CHANGELOG.md, COMPLETION-REPORT.md, SUMMARY.md

### Ready to Start
See `STATE.yaml` → `plans.ready_to_start`

### Blocked
See `STATE.yaml` → `plans.blocked`

---

## Templates

Create new items using templates in `templates/`:

- `plan-template.md` - For new plans
- `proposal-template.md` - For new proposals
- `research-template.md` - For research items
- `active-template.md` - For active work
- `completed-template.md` - For completed items

---

## Design Principles

1. **Single Source of Truth**: `STATE.yaml` is authoritative
2. **File System IS Documentation**: Structure conveys meaning
3. **Metadata Separation**: `metadata.yaml` for machines, `README.md` for humans
4. **Flat Structure**: Avoid deep nesting
5. **Predictable Paths**: `{stage}/{ID}-{name}/` pattern

---

## Related Documentation

- [STRUCTURE.md](./STRUCTURE.md) - Complete structure guide
- [QUERIES.md](./QUERIES.md) - AI agent query patterns
- [STATE.yaml](./STATE.yaml) - Current state
- [roadmap.md](./roadmap.md) - Human dashboard

---

*This roadmap follows the BlackBox5 memory system pattern. See `5-project-memory/` for more.*
