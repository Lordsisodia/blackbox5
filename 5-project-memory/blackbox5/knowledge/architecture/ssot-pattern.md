# Single Source of Truth (SSOT) Pattern

**Version:** 1.0.0
**Created:** 2026-02-04
**Applies To:** BlackBox5 Project Structure

---

## Overview

The Single Source of Truth (SSOT) pattern ensures that every piece of information in BlackBox5 has exactly one canonical location. This prevents drift, contradictions, and confusion when multiple files claim to be authoritative.

**Core Principle:** Reference, don't duplicate.

---

## The Pattern

### 1. One Canonical Source Per Concern

Each type of information lives in exactly one place:

| Concern | Canonical Location | Purpose |
|---------|-------------------|---------|
| **Project Identity** | `project/context.yaml` | Name, version, vision, goals |
| **Active Goals** | `goals/active/*/goal.yaml` | Goal definitions, sub-goals, acceptance criteria |
| **Active Tasks** | `tasks/active/*/task.md` | Task definitions, success criteria, context |
| **Decisions** | `decisions/*/*.md` | Architecture, scope, technical decisions |
| **Structure** | `STATE.yaml` | Index/aggregator of project structure |
| **Templates** | `.templates/` | Reusable templates for tasks, docs, etc. |
| **Knowledge** | `knowledge/` | Patterns, conventions, learnings |

### 2. STATE.yaml as Aggregator

STATE.yaml is an **index**, not a database. It references canonical sources rather than duplicating them.

**Correct:**
```yaml
project:
  reference: "project/context.yaml"
  cached_version: "5.1.0"
  last_sync: "2026-02-04"
```

**Incorrect:**
```yaml
project:
  name: "BlackBox5"  # Duplicate of context.yaml
  version: "5.1.0"   # Duplicate of context.yaml
  description: "..." # Duplicate of context.yaml
```

### 3. Reference Chain

When information is needed, follow the reference chain:

```
RALF Context → STATE.yaml → Canonical Source → Actual Data
     ↑              ↑              ↑
  derived      aggregator    single source of truth
```

---

## Canonical Sources Reference

### Project Identity

**Location:** `project/context.yaml`

**Contains:**
- Project name and version
- Vision and purpose
- Primary goals
- Constraints and assumptions

**Update When:**
- Project vision changes
- Version is released
- Goals are updated

**Reference From:**
- STATE.yaml (reference only)
- Ralf-context.md (derived)

---

### Active Goals

**Location:** `goals/active/IG-*/goal.yaml`

**Contains:**
- Goal ID and name
- Description and purpose
- Sub-goals with acceptance criteria
- Linked tasks
- Progress tracking

**Update When:**
- New goal created
- Goal completed
- Sub-goal status changes
- Task links added/removed

**Reference From:**
- STATE.yaml (in decisions/goals sections)
- Plans that implement the goal

---

### Active Tasks

**Location:** `tasks/active/TASK-*/task.md`

**Contains:**
- Task ID and title
- Objective and success criteria
- Context and background
- Approach and steps

**Update When:**
- Task created
- Status changes (pending → in_progress → completed)
- Success criteria met

**Reference From:**
- Goals (linked_tasks)
- Plans (task lists)
- STATE.yaml (if indexed)

---

### Decisions

**Location:** `decisions/architectural/*.md`, `decisions/scope/*.md`, `decisions/technical/*.md`

**Contains:**
- Decision ID and title
- Context and problem
- Decision made
- Consequences (positive and negative)

**Update When:**
- New decision made
- Decision status changes (proposed → accepted → deprecated)

**Reference From:**
- STATE.yaml (decisions section)
- Goals (links.decisions)
- Tasks (context)

---

### Structure (STATE.yaml)

**Location:** `STATE.yaml`

**Contains:**
- Root file index
- Folder structure
- References to goals, tasks, decisions
- Metadata about last update

**Update When:**
- Files added/removed from root
- Folder structure changes
- References need refreshing

**Important:** STATE.yaml should contain only references and metadata, not duplicated content.

---

## Anti-Patterns to Avoid

### ❌ Copying Data Between Files

**Don't:** Copy project version from context.yaml to STATE.yaml

**Do:** Reference context.yaml from STATE.yaml

```yaml
# GOOD
project:
  reference: "project/context.yaml"
  cached_version: "5.1.0"  # Cache for quick access only

# BAD
project:
  name: "BlackBox5"        # Duplicated from context.yaml
  version: "5.1.0"         # Duplicated from context.yaml
  description: "..."       # Duplicated from context.yaml
```

---

### ❌ Assuming STATE.yaml is Always Right

**Don't:** Trust STATE.yaml as the authoritative source

**Do:** Follow references to canonical sources

```yaml
# When checking project version:
# DON'T: Read STATE.yaml project.version
# DO: Read project/context.yaml project.version
```

---

### ❌ Not Updating References When Moving Files

**Don't:** Move a file without updating references

**Do:** Update all references when moving canonical sources

```bash
# When moving a decision:
# 1. Move the file
mv decisions/architectural/old-name.md decisions/architectural/new-name.md

# 2. Update STATE.yaml decisions section
# 3. Update any goals linking to it
# 4. Update any tasks referencing it
```

---

### ❌ Creating Multiple Sources for Same Info

**Don't:** Create new files that duplicate existing canonical sources

**Do:** Reference existing sources or update the canonical source

```yaml
# DON'T create project/identity.yaml when project/context.yaml exists
# DO update project/context.yaml if you need to add information
```

---

## Ralf-context.md

### What It Is

Ralf-context.md is a **derived document** that aggregates information from canonical sources for the RALF loop. It is NOT a source of truth.

### How It's Generated

1. Read canonical sources (context.yaml, STATE.yaml, active goals/tasks)
2. Extract relevant information
3. Format for RALF consumption
4. Write to Ralf-context.md

### When to Update

- At the start of each RALF run
- When canonical sources change significantly
- When RALF loop reports context issues

### Important

Never edit Ralf-context.md directly. Always update the canonical source and regenerate.

---

## Validation Process

### Automated Validation

Run the validation script to check for SSOT violations:

```bash
python3 bin/validate-ssot.py
```

**Checks:**
- STATE.yaml syntax is valid
- All referenced files exist
- No duplicate information detected
- Goals link to existing tasks
- Decisions have corresponding files

### Manual Review

Periodically review for SSOT violations:

1. **Check for duplicates:** Search for the same information in multiple files
2. **Verify references:** Ensure STATE.yaml references are up to date
3. **Review changes:** Check recent edits for accidental duplication
4. **Update Ralf-context:** Regenerate if canonical sources changed

---

## Examples

### Example 1: Adding a New Goal

**Correct Flow:**
1. Create `goals/active/IG-010/goal.yaml` (canonical source)
2. Update `STATE.yaml` goals section to reference it
3. Regenerate `Ralf-context.md`

**Incorrect Flow:**
1. Add goal details directly to `STATE.yaml`
2. Create goal file separately
3. Information drifts between files

---

### Example 2: Updating Project Version

**Correct Flow:**
1. Update `project/context.yaml` version field
2. Update `STATE.yaml` cached_version reference
3. Regenerate `Ralf-context.md`

**Incorrect Flow:**
1. Update version in `STATE.yaml` only
2. `project/context.yaml` now has old version
3. Confusion about which is correct

---

### Example 3: Moving a Task

**Correct Flow:**
1. Move task file to new location
2. Update all goals linking to it
3. Update `STATE.yaml` if indexed
4. Regenerate `Ralf-context.md`

**Incorrect Flow:**
1. Move task file
2. Don't update references
3. Broken links everywhere

---

## Quick Reference

| If you need to... | Go to... | Then update... |
|-------------------|----------|----------------|
| Change project vision | `project/context.yaml` | `Ralf-context.md` |
| Add a goal | `goals/active/IG-*/goal.yaml` | `STATE.yaml` |
| Create a task | `tasks/active/TASK-*/task.md` | Linking goals |
| Make a decision | `decisions/*/*.md` | `STATE.yaml`, goals |
| Update structure | `STATE.yaml` | `Ralf-context.md` |
| Fix a template | `.templates/` | Generated files |

---

## Related Documents

- `project/context.yaml` - Project identity (canonical)
- `STATE.yaml` - Structure index (aggregator)
- `Ralf-context.md` - RALF context (derived)
- `bin/validate-ssot.py` - Validation script

---

**Remember:** Reference, don't duplicate. One canonical source per concern.
