# Architecture Folder Template

**Purpose:** Standard architecture documentation structure for any project
**Location:** `{project}/architecture/`

---

## Folder Structure

```
architecture/
├── README.md              # Overview and navigation
├── ADR.md                 # Architecture Decision Records
├── decisions/             # Individual architecture decisions
├── knowledge/             # Architectural patterns and knowledge
├── context/               # Current system state
│   ├── ROOT_LAYOUT.yaml   # Machine-readable current structure
│   └── DEPENDENCIES.md    # System dependencies
└── plans/                 # Future improvement plans
    └── TARGET_STRUCTURE.md # Clean target architecture
```

---

## File Templates

### README.md
```markdown
# {Project} Architecture

**Location:** `{project}/architecture/`
**Purpose:** Single source of truth for {Project} system architecture
**Last Updated:** {date}

---

## Overview

This folder contains all architecture documentation for {Project}:
- Current state of the system
- Architecture decisions (ADRs)
- Future improvement plans
- Knowledge about architectural patterns

---

## Quick Navigation

| What you want | Where to look |
|---------------|---------------|
| Current structure | `context/ROOT_LAYOUT.yaml` |
| Why a decision was made | `decisions/` or `ADR.md` |
| Future improvements | `plans/TARGET_STRUCTURE.md` |
| Architectural patterns | `knowledge/` |

---

## Current State Summary

**Status:** {status}

**Key Issues:**
- {Issue 1}
- {Issue 2}

---

## Architecture Principles

1. **Clear Separation** - Concerns clearly separated
2. **Single Source of Truth** - Each piece of data lives in one place
3. **Intuitive Layout** - New developers understand structure quickly
4. **AI-Friendly** - Structure is machine-readable and navigable
```

### context/ROOT_LAYOUT.yaml
```yaml
meta:
  project: {project_name}
  version: "1.0.0"
  last_updated: "{date}"
  total_root_items: {count}
  status: "{active|needs_cleanup|deprecated}"

root_items:
  - name: "{folder_name}"
    type: folder
    purpose: "{description}"
    status: {active|deprecated|migrating}
    notes: "{optional}"

issues:
  - id: ARCH-001
    description: "{issue_description}"
    severity: {high|medium|low}
    status: {open|in_progress|resolved}
```

### plans/TARGET_STRUCTURE.md
```markdown
# Target Architecture Structure

## Principles

1. **Clear Separation**
2. **Intuitive Names**
3. **No Duplicates**
4. **AI-Friendly**

## Target Structure

```
{project}/
├── README.md
├── {core_files}
├── architecture/
└── {other_folders}
```

## What Changed

### Deleted
- {item} - {reason}

### Renamed
- {old} → {new}

### Created
- {item} - {purpose}

## Migration Path

See migration plan for detailed steps.

## Success Criteria

- [ ] {criterion 1}
- [ ] {criterion 2}
```

---

## How to Use This Template

1. Copy this folder structure to your project
2. Fill in project-specific details
3. Document current state in ROOT_LAYOUT.yaml
4. Define target state in TARGET_STRUCTURE.md
5. Track decisions in ADR.md and decisions/

---

## Example Projects Using This Template

- BlackBox5: `5-project-memory/blackbox5/architecture/`
