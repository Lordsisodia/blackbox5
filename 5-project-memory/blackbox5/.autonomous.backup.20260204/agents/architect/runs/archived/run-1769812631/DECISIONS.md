# DECISIONS - TASK-1769812506

**Task:** Fix AgentLoader Import Paths (Unblocks Agent Loading)
**Run Date:** 2026-01-30T22:37:11Z

---

## Decision 1: Fix Path Calculation in agent_loader.py

**Context:** agent_loader.py:20 had `parent.parent.parent` which only goes up 3 levels from `core/agent_loader.py` to `agents/`, not enough to reach `2-engine/` for importing `core/interface/client/`.

**Options:**
| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| A | Add 4th parent to path | Correct fix, minimal change | None |
| B | Move agent_loader.py | Different structure | Breaks other imports |
| C | Use absolute path | Works | Not portable |

**Selected:** Option A - Add 4th parent (`parent.parent.parent.parent`)

**Rationale:** Minimal change, maintains existing structure, portable.

**Reversibility:** LOW - Single line change, easily reverted

---

## Decision 2: Fix Import Path in ClaudeCodeAgentMixin.py

**Context:** ClaudeCodeAgentMixin.py:20 had `from client.ClaudeCodeClient` which assumes `client/` is in the Python path, but it's actually at `core/interface/client/`.

**Options:**
| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| A | Use absolute import path | Clear, explicit | Longer |
| B | Use relative import | Shorter | Can be confusing |
| C | Add to sys.path in callers | Works everywhere | Spreads complexity |

**Selected:** Option A - Use `from core.interface.client.ClaudeCodeClient`

**Rationale:** Explicit is better than implicit, makes dependency clear.

**Reversibility:** LOW - Single line change

---

## Decision 3: Fix Import Paths in All 3 Python Agents

**Context:** DeveloperAgent.py, AnalystAgent.py, and ArchitectAgent.py all had the same incorrect import pattern.

**Options:**
| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| A | Fix all 3 agents now | Consistent, complete | More changes |
| B | Fix only 1, others later | Minimal change | Inconsistent |
| C | Create shared import module | DRY | Adds indirection |

**Selected:** Option A - Fix all 3 agents

**Rationale:** Consistent fix, prevents future confusion, all agents were broken anyway.

**Reversibility:** LOW - Each file independent, easily reverted

---

## Summary

| Decision | Impact | Risk | Reversibility |
|----------|--------|------|---------------|
| Path calculation fix | Enables all imports | LOW | LOW |
| ClaudeCodeAgentMixin import | Enables mixin usage | LOW | LOW |
| Fix all 3 agents | Enables Python agents | LOW | LOW |

**Overall Risk:** LOW - All changes are localized, well-tested, easily reversible.
