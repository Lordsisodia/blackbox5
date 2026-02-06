# Next Priority: @path Imports Implementation

**Status:** Documented, Ready for Implementation
**Priority:** High (after P0 rules)
**Estimated Effort:** 1-2 days

---

## Overview

After implementing the P0 rules, the next priority is to set up @path imports in the project CLAUDE.md. This will:
- Auto-load BB5 context without `bb5 whereami`
- Unify scattered context files
- Enable dynamic context refresh

---

## Implementation Steps

### Step 1: Create Project CLAUDE.md
Create `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/CLAUDE.md`:

```markdown
---
name: BlackBox5 Project Context
includes:
  - @/goals.yaml
  - @/STATE.yaml
  - @/.autonomous/agents/communications/queue.yaml
  - @/AGENT_CONTEXT.md
---

# BlackBox5 Project

## Current State
**Active Goal:** {{goals.active.0.name}}
**Current Task:** {{STATE.current_task}}
**Queue Depth:** {{queue.length}}

## Navigation
- `bb5 whereami` - Current location
- `bb5 goal:list` - List goals
- `bb5 task:current` - Current task

## Core Instructions
{{include @/.docs/CLAUDE-MEMORY-SYSTEM.md}}
```

### Step 2: Test Auto-Loading
1. Start new Claude session in BB5 directory
2. Verify context auto-loads
3. Check that goals, state, queue are accessible

### Step 3: Simplify SessionStart Hook
Update hook to:
1. Detect agent type
2. Output minimal context (CLAUDE.md handles the rest)
3. Log session start

### Step 4: Document
Update CLAUDE-IMPORTS-GUIDE.md with:
- Lessons learned
- Troubleshooting tips
- Best practices discovered

---

## Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
| `CLAUDE.md` | Create | Project context with imports |
| `SessionStart hook` | Modify | Simplify to use CLAUDE.md |
| `CLAUDE-IMPORTS-GUIDE.md` | Update | Add implementation notes |

---

## Success Criteria

- [ ] CLAUDE.md auto-loads when entering BB5 directory
- [ ] Goals, state, queue accessible without bb5 commands
- [ ] SessionStart hook simplified
- [ ] No regression in context quality

---

## Related Documentation

- [CLAUDE-IMPORTS-GUIDE.md](./CLAUDE-IMPORTS-GUIDE.md) - Complete guide
- [CLAUDE.md.example](../CLAUDE.md.example) - Working example
- [RULES-CONSOLIDATION.md](./RULES-CONSOLIDATION.md) - P0 rules status

---

**Created:** 2026-02-06
**By:** Claude Code
