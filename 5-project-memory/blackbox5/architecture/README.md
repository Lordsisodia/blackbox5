# BlackBox5 Architecture

**Location:** `5-project-memory/blackbox5/architecture/`
**Purpose:** Single source of truth for BlackBox5 system architecture
**Last Updated:** 2026-02-02

---

## Overview

This folder contains all architecture documentation for BlackBox5:
- Current state of the system
- Architecture decisions (ADRs)
- Future improvement plans
- Knowledge about architectural patterns

---

## Folder Structure

```
architecture/
├── README.md              # This file - overview and navigation
├── ADR.md                 # Architecture Decision Records
├── decisions/             # Individual architecture decisions
├── knowledge/             # Architectural knowledge and patterns
├── context/               # Current system state
└── plans/                 # Future improvement plans
```

---

## Quick Navigation

| What you want | Where to look |
|---------------|---------------|
| Current folder structure | `context/ROOT_LAYOUT.yaml` |
| Why a decision was made | `decisions/` or `ADR.md` |
| Future improvements | `plans/TARGET_STRUCTURE.md` |
| Architectural patterns | `knowledge/` |

---

## Current State Summary

**Status:** Architecture needs cleanup

**Key Issues:**
1. 7 `.autonomous` folders scattered throughout
2. Unclear separation between engine and project data
3. Legacy task system coexists with new task system
4. Root `.autonomous` purpose unclear

**Active Goal:** IG-006 (Restructure BlackBox5 Architecture)

---

## Architecture Principles

1. **Clear Separation** - Engine (shared) vs Project (specific)
2. **Single Source of Truth** - Each piece of data lives in one place
3. **Intuitive Layout** - New developers understand structure in 5 minutes
4. **AI-Friendly** - Structure is machine-readable and navigable

---

## How to Use This Folder

### For Humans:
- Review `context/` to understand current state
- Check `plans/` to see proposed improvements
- Read `decisions/` to understand why things are the way they are

### For Agents:
- Read `context/ROOT_LAYOUT.yaml` to navigate the system
- Check `ADR.md` for architecture constraints
- Follow `plans/` for improvement tasks

---

## Related Files

- `../goals.yaml` - Goal IG-006 tracks architecture improvement
- `../autonomous/MIGRATION-PLAN.md` - Detailed migration steps
- `../MAP.yaml` - Complete file-level project map
