# Skills System Architecture - Current State

**Visualization of the duplicate skills systems problem**

---

## Current Architecture (BROKEN)

```
┌─────────────────────────────────────────────────────────────┐
│                   BLACKBOX5 ENGINE                          │
│                  /2-engine/02-agents/                       │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  skills-cap/ │    │ .skills-new/ │    │ legacy-skills│
│              │    │              │    │     ❌       │
│  59 skills   │    │  33 skills   │    │              │
│              │    │              │    │  9 skills    │
│  ─────────   │    │  ─────────   │    │              │
│  26 unique   │    │  CANONICAL   │    │  GHOST DIR   │
│  33 dupes    │    │  (TARGET)    │    │              │
│              │    │              │    │  Wrong name  │
│  INACTIVE    │    │  XML FORMAT  │    │  in refs     │
└──────────────┘    └──────────────┘    └──────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                    ┌──────────────┐
                    │   AGENTS     │
                    │              │
                    │  Try to load │
                    │  ../../.skills/│
                    │              │
                    │  ❌ FAILS    │
                    │  (doesn't    │
                    │   exist)     │
                    └──────────────┘
```

---

## Agent Skill References (BROKEN)

```yaml
# In agent manifest.yaml files:
skills:
  - "../../.skills/repo-codebase-navigation.md"  # ❌ BROKEN
  - "../../.skills/testing-playbook.md"          # ❌ BROKEN
  - "../../.skills/supabase-ddl-rls.md"          # ❌ BROKEN

# Actual location: "../../legacy-skills/..."
# Should be: "../../.skills-legacy/..." or migrate to .skills-new
```

---

## Skill Overlap Analysis

```
TOTAL SKILLS: 59 + 33 + 9 = 101 (with duplicates)

Unique Distribution:
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  skills-cap/      59  ████████████████████  (26 unique) │
│  .skills-new/     33  ██████████  (0 unique - all dupes) │
│  legacy-skills/    9  ███  (9 unique - old format)      │
│                                                          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Duplicates:       33  ██████████  (shared skills)      │
│  Unique Total:     68  █████████████████                │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Category Comparison

```
CATEGORY                  skills-cap    .skills-new    Status
───────────────────────── ────────────  ─────────────  ──────
Collaboration                   13            10        3 unique in cap
Core Infra                       2             2        All dupes
Dev Workflow                    15             5        10 unique in cap
Integration                     22            13        9 unique in cap
Knowledge                        7             3        4 unique in cap
Planning                         4             0        4 unique in cap
Research                         8             0        8 unique in cap
Kanban                           7             0        7 unique in cap
Other                           11             0        11 unique in cap
Legacy                          -             -        9 unique legacy
```

---

## Proposed Architecture (FIXED)

```
┌─────────────────────────────────────────────────────────────┐
│                   BLACKBOX5 ENGINE                          │
│                  /2-engine/02-agents/                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────┐
                    │ .skills-new/ │
                    │              │
                    │  68 skills   │
                    │  (migrated)  │
                    │              │
                    │  SINGLE      │
                    │  CANONICAL   │
                    │  SYSTEM      │
                    │              │
                    │  XML FORMAT  │
                    └──────────────┘
                              │
                              ▼
                    ┌──────────────┐
                    │   AGENTS     │
                    │              │
                    │  Load from   │
                    │  capabilities│
                    │  /.skills-new│
                    │              │
                    │  ✅ WORKS    │
                    └──────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  ARCHIVED SYSTEMS                           │
│  .skills-cap-20260120/    (backup, 30 day retention)       │
│  .skills-legacy-20260120/  (backup, 30 day retention)      │
└─────────────────────────────────────────────────────────────┘
```

---

## Migration Flow

```
STEP 1: Fix Paths (Immediate)
┌─────────────┐     rename     ┌──────────────┐
│legacy-skills│  ───────────►  │.skills-legacy│
└─────────────┘                └──────────────┘

STEP 2: Migrate Unique Skills (This Week)
┌─────────────┐     migrate     ┌──────────────┐
│ skills-cap  │  ────────────►  │ .skills-new  │
│ (26 unique) │                 │ (+26 skills) │
└─────────────┘                 └──────────────┘

STEP 3: Archive (After Verification)
┌─────────────┐     archive     ┌──────────────────┐
│ skills-cap  │  ────────────►  │ .skills-cap-old  │
└─────────────┘                 └──────────────────┘
```

---

## MCP Integration Status

```
MCP Servers with Skill Definitions: 13

┌──────────────────────────────────────────────────────┐
│ ✅ supabase          ✅ chrome-devtools               │
│ ✅ shopify           ✅ playwright                    │
│ ✅ github            ✅ filesystem                    │
│ ✅ serena            ✅ sequential-thinking            │
│ ✅ docx              ✅ siso-internal                 │
│ ✅ pdf               ✅ artifacts-builder              │
│ ✅ mcp-builder       ✅ (mcp-builder itself)          │
└──────────────────────────────────────────────────────┘

Status: All defined in .skills-new with XML structure
Tools: Callable through MCP system (no skill loading needed)
```

---

## File Paths Reference

```
CURRENT STATE:
blackbox5/2-engine/02-agents/
├── capabilities/
│   ├── skills-cap/          # 59 skills (INACTIVE)
│   │   ├── collaboration-communication/
│   │   ├── development-workflow/
│   │   ├── integration-connectivity/
│   │   └── [12 more categories]
│   │
│   └── .skills-new/         # 33 skills (CANONICAL)
│       ├── collaboration-communication/
│       ├── development-workflow/
│       ├── integration-connectivity/
│       ├── core-infrastructure/
│       └── knowledge-documentation/
│
├── legacy-skills/           # 9 skills (GHOST)
│   ├── feedback-triage.md
│   ├── testing-playbook.md
│   └── [7 more]
│
└── implementations/
    └── [agents reference ../../.skills/ which doesn't exist]
```

```
PROPOSED STATE:
blackbox5/2-engine/02-agents/
├── capabilities/
│   └── .skills/             # 68 skills (SINGLE CANONICAL)
│       ├── collaboration-communication/
│       ├── development-workflow/
│       ├── integration-connectivity/
│       ├── core-infrastructure/
│       ├── knowledge-documentation/
│       ├── planning/        # migrated from skills-cap
│       ├── research/        # migrated from skills-cap
│       └── [other categories]
│
└── implementations/
    └── [agents reference ../capabilities/.skills/]

Archive:
├── .skills-cap-20260120/    # backup, delete after 30 days
└── .skills-legacy-20260120/  # backup, delete after 30 days
```

---

## Decision Tree: Which Skill System to Use?

```
┌─────────────────────────────────────────────────────────┐
│  Do you need to add/update a skill TODAY?              │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │ Is it in .skills-new? │
              └───────────────────────┘
                    │            │
                   YES          NO
                    │            │
                    ▼            ▼
          ┌─────────────┐  ┌──────────────────┐
          │ Use .skills-│  │ Check skills-cap │
          │    new      │  │    for it        │
          └─────────────┘  └──────────────────┘
                                 │
                          ┌──────┴──────┐
                         YES          NO
                          │            │
                          ▼            ▼
                    ┌──────────┐  ┌────────────┐
                    │ Migrate │  │ Create new │
                    │ to .skills│  │ in .skills- │
                    │   -new   │  │    new      │
                    └──────────┘  └────────────┘

FUTURE STATE (after consolidation):
┌─────────────────────────────────────────────────────────┐
│  All skills in .skills/ (renamed from .skills-new)     │
│  Single source of truth                                 │
│  No decision tree needed                                │
└─────────────────────────────────────────────────────────┘
```

---

## Risk Timeline

```
IMMEDIATE (Day 1):          Broken agent skill loading
                           ━━━━━━━━━━━━━━━━ ◀ High Risk

THIS WEEK:                 Potential skill loss during migration
                           ━━━━━━━━━━━ ◀ Medium Risk

THIS MONTH:                Documentation drift and confusion
                           ━━━━━━━ ◀ Low Risk

AFTER CONSOLIDATION:       ✅ Single system, clear architecture
                           ━━━━━━━━━━━━━━━━━━ ✅ Resolved
```

---

## Key Takeaways

1. **Three Systems Exist** - Not two as initially suspected
2. **Agents Are Broken** - Path references don't match actual directories
3. **Consolidation Incomplete** - 26 skills at risk of being lost
4. **Solution Clear** - Migrate to .skills-new and fix paths
5. **7-9 Hours** - Estimated time to fully resolve

---

**Diagram Created**: 2026-01-20
**Purpose**: Visual aid for understanding the duplicate systems problem
**Status**: Current state documented, proposed state ready for implementation
