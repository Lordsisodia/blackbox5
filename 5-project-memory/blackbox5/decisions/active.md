# Active Architectural Decisions

**Last Updated:** 2026-02-02

This document tracks active architectural decisions. Move to `decisions/archived/` when superseded.

---

## D-001: 4-File Run Structure

**Date:** 2026-02-02
**Status:** Active
**Deciders:** Claude + User

### Context
Analyzed 146 runs to determine actual file usage.

### Decision
Reduce from 6 files to 4 files per run:
- THOUGHTS.md (100% usage) - Keep separate
- RESULTS.md (99% usage) - Keep separate
- DECISIONS.md (97% usage) - Keep separate
- metadata.yaml (76% usage) - Keep
- LEARNINGS.md (13% usage) - Merge into metadata
- ASSUMPTIONS.md (12% usage) - Merge into metadata

### Consequences
- Simpler structure
- Easier to parse
- Less cognitive load

---

## D-002: Hook-Based Enforcement

**Date:** 2026-02-02
**Status:** Active
**Deciders:** Claude + User

### Context
0% queue sync success with prompt-based enforcement.

### Decision
Use COMMAND hooks (bash) instead of prompt instructions:
- SessionStart hook: Creates run folder
- Stop hook: Handles completion

### Consequences
- 100% reliable (code, not LLM)
- Zero tokens
- <100ms execution

---

## D-003: Dynamic Prompt Context

**Date:** 2026-02-02
**Status:** Active
**Deciders:** Claude + User

### Context
Need self-updating context for multi-agent system.

### Decision
Build prompts by concatenating context files:
- project-structure.md
- architecture/map.md
- decisions/active.md
- goals.yaml
- learnings/recent.md

### Consequences
- Agents always have current context
- No manual prompt updates needed
- Architecture changes propagate automatically

---

## Template for New Decisions

```markdown
## D-XXX: [Title]

**Date:** YYYY-MM-DD
**Status:** Active/Superseded
**Deciders:** [Who decided]

### Context
[What was the problem]

### Decision
[What was decided]

### Consequences
[What happens as a result]
```
