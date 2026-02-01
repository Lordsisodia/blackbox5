# PLAN-002: Fix YAML Agent Loading

**Priority:** 🔴 CRITICAL
**Status:** Planned (Blocked by PLAN-001)
**Estimated Effort:** 1 day
**Dependencies:** PLAN-001

---

## Executive Summary

YAML-based specialist agents are **not loading at all**. Only 3 of 21 agents work.

**Current State:**
- Core Agents: 3/3 (100%) ✅
- Specialist Agents: 0/18 (0%) ❌

---

## The Problem

**AgentLoader only scans one directory:**
```
blackbox5/2-engine/01-core/agents/
```

But YAML agents are at:
```
blackbox5/2-engine/02-agents/specialists/
```

AgentLoader also doesn't parse YAML files.

---

## The Solution

**2-Phase Fix:**

1. **Extend AgentLoader** (4 hours) - Support multiple paths
2. **Add YAML Parsing** (3 hours) - Load .yaml agent definitions

---

## Files to Change

- `agent_loader.py` - Add multi-path and YAML support

---

## Success Criteria

✅ YAML agents load successfully
✅ 18/18 specialist agents loaded
✅ 21/21 total agents loaded

---

## Next Steps

1. Wait for PLAN-001 to complete
2. Extend AgentLoader for multiple paths
3. Add YAML parsing
4. Test all 21 agents load

**Blocked by:** PLAN-001

---

**Ready to Execute:** No (waiting for PLAN-001)
