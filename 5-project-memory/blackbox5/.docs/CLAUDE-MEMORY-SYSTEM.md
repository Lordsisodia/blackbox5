# Claude Code Memory System for BlackBox5

**Date:** 2026-02-06
**Status:** Documentation Complete
**Applies To:** BlackBox5 Project Memory System

---

## Overview

Claude Code's memory system offers powerful capabilities that can significantly simplify and enhance BlackBox5. This documentation covers three key features:

1. **`.claude/rules/`** - Auto-triggering skill rules
2. **`CLAUDE.local.md`** - Personal preferences
3. **`@path` imports** - Dynamic context loading

---

## Quick Links

| Feature | Guide | Example | Status |
|---------|-------|---------|--------|
| Rules System | [CLAUDE-RULES-GUIDE.md](./CLAUDE-RULES-GUIDE.md) | 5 example rules | Ready to implement |
| Local Preferences | [CLAUDE-LOCAL-GUIDE.md](./CLAUDE-LOCAL-GUIDE.md) | [CLAUDE.local.md.example](../CLAUDE.local.md.example) | Ready to use |
| Path Imports | [CLAUDE-IMPORTS-GUIDE.md](./CLAUDE-IMPORTS-GUIDE.md) | [CLAUDE.md.example](../CLAUDE.md.example) | Ready to implement |

---

## Why This Matters for BB5

### Current Pain Points

1. **Complex Skill Registry** - 23 skills in 1300-line YAML with manual Phase 1.5 checking
2. **Explicit Context Loading** - Must run `bb5 whereami` to discover location
3. **Scattered Memory** - Context across 10+ files in different directories
4. **No Personalization** - All config is global, no per-user preferences

### How Claude Memory Helps

| BB5 Current | Claude Memory Solution | Benefit |
|-------------|----------------------|---------|
| `skill-registry.yaml` + Phase 1.5 checks | `.claude/rules/` with auto-trigger | Skills apply automatically |
| `bb5 whereami` + AGENT_CONTEXT.md | `CLAUDE.md` with `@path` imports | Context loads automatically |
| Global `~/.claude/CLAUDE.md` | `CLAUDE.local.md` per project | Personal preferences |
| Multiple context files | Unified `CLAUDE.md` with imports | Single source of truth |

---

## Implementation Roadmap

### Phase 1: Path Imports (Week 1)
- [ ] Create project-level `CLAUDE.md` with `@path` imports
- [ ] Test auto-loading of BB5 context
- [ ] Simplify SessionStart hooks

### Phase 2: Rules System (Week 2-3)
- [ ] Create `.claude/rules/` directory
- [ ] Migrate top 5 skills from skill-registry.yaml
- [ ] Test auto-trigger behavior
- [ ] Run parallel (registry + rules) for validation

### Phase 3: Local Preferences (Week 4)
- [ ] Create `CLAUDE.local.md` template
- [ ] Document agent integration for editing
- [ ] Test preference persistence

### Phase 4: Deprecation (Month 2)
- [ ] Deprecate skill-registry.yaml (keep for metrics)
- [ ] Remove AGENT_CONTEXT.md generation
- [ ] Update documentation

---

## Key Concepts

### 1. Rules Auto-Trigger

Rules in `.claude/rules/` automatically apply based on:
- **Path matching** - Rules with `globs: ["**/*.py"]` apply to Python files
- **Keyword matching** - Rules with `trigger: ["git"]` apply to git operations
- **Always-on** - Rules with `alwaysApply: true` load every session

**Example:** A rule with `trigger: ["Should we", "architecture"]` automatically activates when you ask "Should we refactor the auth system?"

### 2. @path Imports Refresh Dynamically

When you use `@goals.yaml` in CLAUDE.md:
- Content is imported at session start
- Refreshes automatically when files change
- No manual update needed

### 3. CLAUDE.local.md is Private

- Automatically added to `.gitignore`
- Perfect for personal preferences
- Not shared with team

---

## Example: Before and After

### Before (Current BB5)

```bash
# User must explicitly discover context
$ bb5 whereami
Current: BlackBox5 project root
Run 'bb5 goal:list' to see goals

# User must manually check skills
$ cat operations/skill-selection.yaml
# Read skill-registry.yaml
# Calculate confidence scores
# Decide which skill to use
```

### After (With Claude Memory)

```markdown
# CLAUDE.md automatically loads:
---
includes:
  - @goals.yaml
  - @STATE.yaml
  - @.autonomous/agents/communications/queue.yaml
---

## Current State
**Active Goal:** {{goals.active.0.name}}
**Current Task:** {{STATE.current_task}}
**Queue Depth:** {{queue.length}}
```

Rules auto-apply based on what you're doing - no manual checking needed.

---

## Documentation Structure

```
.docs/
├── CLAUDE-MEMORY-SYSTEM.md          # This file - overview and roadmap
├── CLAUDE-RULES-GUIDE.md            # Complete rules system guide
├── CLAUDE-LOCAL-GUIDE.md            # Local preferences guide
└── CLAUDE-IMPORTS-GUIDE.md          # @path imports guide

CLAUDE.md.example                    # Example project CLAUDE.md
CLAUDE.local.md.example              # Example local preferences
```

---

## Next Steps

1. **Review the guides** - Start with [CLAUDE-IMPORTS-GUIDE.md](./CLAUDE-IMPORTS-GUIDE.md) for quickest impact
2. **Create your CLAUDE.local.md** - Copy [CLAUDE.local.md.example](../CLAUDE.local.md.example) and customize
3. **Experiment with rules** - Create `.claude/rules/01-test.md` and see how it auto-triggers
4. **Migrate gradually** - Don't replace everything at once; test each feature

---

## Questions?

- For rules: See [CLAUDE-RULES-GUIDE.md](./CLAUDE-RULES-GUIDE.md) FAQ section
- For imports: See [CLAUDE-IMPORTS-GUIDE.md](./CLAUDE-IMPORTS-GUIDE.md) Troubleshooting
- For local prefs: See [CLAUDE-LOCAL-GUIDE.md](./CLAUDE-LOCAL-GUIDE.md) Best Practices

---

**Related:**
- [skill-registry.yaml](../operations/skill-registry.yaml) - Current skills (to be migrated)
- [AGENT_CONTEXT.md](../AGENT_CONTEXT.md) - Current context (to be simplified)
- [goals.yaml](../goals.yaml) - Can be imported via @path
