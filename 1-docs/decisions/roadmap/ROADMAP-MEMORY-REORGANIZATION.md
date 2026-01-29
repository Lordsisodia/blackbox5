# BlackBox5 Roadmap ↔ Project Memory Reorganization

**Status:** Ready to execute
**Created:** 2026-01-20

---

## Executive Summary

The BlackBox5 roadmap contains a mix of:
1. **Active improvement work** (proposals, plans, research in progress)
2. **Reference knowledge** (research findings, architecture docs, frameworks)

These need to be separated:
- **Roadmap** = What we're building next (improvement tracking)
- **Project Memory** = What we know and why (project knowledge)

---

## What Was Created

### 1. Detailed Migration Map
**File:** `blackbox5/ROADMAP-TO-MEMORY-MIGRATION-MAP.md`

Complete mapping of every item in the roadmap to its destination:
- Part 1: Items moving to project memory (with rationale)
- Part 2: Items staying in roadmap (with rationale)
- Part 3: New structure overview (visual tree)
- Part 4: Key principles (decision flow)
- Part 5: Migration checklist (step-by-step)

### 2. Project Memory Structure
**Directory:** `blackbox5/5-project-memory/blackbox5/`

Created 7-folder structure from template:
```
blackbox5/
├── project/          # Project identity & direction (context.yaml created)
├── decisions/        # Architectural, scope, technical decisions
├── plans/           # Active, features, PRDs
├── knowledge/       # Research, frameworks, architecture, first-principles
├── tasks/           # Working, backlog, completed
├── operations/      # Agents, workflows, sessions, logs
└── domains/         # Auth, integrations, supabase, ui
```

### 3. Migration Script
**File:** `blackbox5/5-project-memory/MIGRATION-SCRIPT.sh`

Executable script that:
- Copies reference docs from roadmap to memory
- Preserves active research logs in roadmap
- Organizes content by question type
- Provides summary of changes

---

## Key Distinctions

### Roadmap (Keep)
| Content | Why |
|---------|-----|
| `00-proposed/` | Future improvement ideas |
| `01-research/research-log.md` | Active research tracking |
| `01-research/session-summaries/` | Research progress |
| `03-planned/` | Ready-to-implement plans |
| `04-active/` | Currently implementing |
| System files (STATE, STRUCTURE) | Roadmap infrastructure |

### Project Memory (Move)
| Content | Why |
|---------|-----|
| `research/BLACKBOX5-RESEARCH-CATEGORIES.md` | Reference document |
| `first-principles/` | Project knowledge base |
| `frameworks/` | Framework research findings |
| `01-research/{category}/findings/` | Research outcomes |
| `02-validation/` findings | Validation results |

---

## Migration Decision Flow

```
Is it an improvement to BlackBox5?
├── YES → Is it actively being worked or planned?
│   ├── YES → Roadmap (00-04)
│   └── NO → Roadmap (07-backlog)
└── NO → Is it reference knowledge?
    ├── YES → Project Memory (knowledge/)
    └── NO → Is it a decision?
        ├── YES → Project Memory (decisions/)
        └── NO → Project Memory (project/)
```

---

## Quick Start: Execute Migration

```bash
# Navigate to BlackBox5
cd /Users/shaansisodia/DEV/SISO-ECOSYSTEM/SISO-INTERNAL/blackbox5

# Review the migration map
cat ROADMAP-TO-MEMORY-MIGRATION-MAP.md

# Run the migration script
./5-project-memory/MIGRATION-SCRIPT.sh

# Review results
find 5-project-memory/blackbox5 -type f -name "*.md" | head -20
```

---

## Post-Migration Tasks

### 1. Update Links
```bash
# Find files with old roadmap references
find 5-project-memory/blackbox5 -name "*.md" -exec grep -l "6-roadmap" {} \;
```

### 2. Update Roadmap State
- Update `STATE.yaml` to reflect new structure
- Update `INDEX.yaml` with changed paths
- Update `roadmap.md` dashboard

### 3. Create README in Project Memory
```bash
# 5-project-memory/blackbox5/README.md
# Should explain the 7-folder structure and how to use it
```

### 4. Archive Old Content
- Optionally archive `02-validation/` from roadmap (now in memory)
- Optionally move completed items to `05-completed/YYYY/`

---

## Files to Review

1. **Migration Map:** `ROADMAP-TO-MEMORY-MIGRATION-MAP.md`
   - Complete mapping with rationale
   - Visual structure diagrams
   - Decision flow principles

2. **Project Context:** `5-project-memory/blackbox5/project/context.yaml`
   - Project identity, goals, constraints
   - Current state and gaps
   - Success metrics

3. **Migration Script:** `5-project-memory/MIGRATION-SCRIPT.sh`
   - Executable migration
   - Phase-by-phase execution
   - Summary reporting

---

## Next Actions

1. **Review the migration map** - Understand what moves where
2. **Run the migration script** - Execute the reorganization
3. **Update internal links** - Fix references to moved content
4. **Test the new structure** - Verify agents can find content
5. **Archive old roadmap items** - Clean up completed work

---

## Questions to Resolve

1. Should we delete moved content from roadmap, or keep as redirect?
2. How do we handle cross-references between roadmap and memory?
3. Do we need a bidirectional link system?
4. Should validation be converted to a template for future use?

---

**Status:** Awaiting your review and go-ahead to execute migration.
