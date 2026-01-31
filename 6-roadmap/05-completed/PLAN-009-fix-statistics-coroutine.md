# PLAN-009: Fix Statistics Coroutine Warnings

**Priority:** 🟡 MEDIUM (Display Issue)
**Status:** Planned
**Estimated Effort:** 1 hour
**Dependencies:** None
**Discovered By:** First Principles Analysis

---

## Problem Statement

`get_statistics()` methods in main.py are **async coroutines** but are called as **sync functions**.

**Impact:** Statistics display shows coroutine objects instead of actual data

---

## The Issue

**Location:** `main.py:688-708`

**Code:**
```python
def get_statistics(self) -> Dict[str, Any]:
    """
    Get system statistics.

    Returns:
        Dictionary with system statistics
    """
    stats = {
        "initialized": self._initialized,
        "project_path": str(self.project_path),
        "agent_count": len(self._agents),
        "agents": list(self._agents.keys()),
    }

    if self._task_router:
        stats["routing"] = self._task_router.get_statistics()  # ❌ ASYNC NOT AWAITED

    if self._orchestrator:
        stats["orchestrator"] = self._orchestrator.get_statistics()  # ❌ ASYNC NOT AWAITED

    return stats
```

**Problem:**
- `TaskRouter.get_statistics()` is `async def`
- `AgentOrchestrator.get_statistics()` is `async def`
- Called from sync `get_statistics()` without `await`

**Result:**
```python
{
    "routing": <coroutine object TaskRouter.get_statistics at 0x...>,
    "orchestrator": <coroutine object AgentOrchestrator.get_statistics at 0x...>
}
```

**Warning:**
```
RuntimeWarning: coroutine 'TaskRouter.get_statistics' was never awaited
RuntimeWarning: coroutine 'AgentOrchestrator.get_statistics' was never awaited
```

---

## Solution Design

### Option A: Make get_statistics() Async (Recommended)

**Pros:**
- Clean solution
- Consistent with other methods
- Properly awaits coroutines

**Cons:**
- Requires updating all callers

**Implementation:**
```python
async def get_statistics(self) -> Dict[str, Any]:
    """
    Get system statistics.

    Returns:
        Dictionary with system statistics
    """
    stats = {
        "initialized": self._initialized,
        "project_path": str(self.project_path),
        "agent_count": len(self._agents),
        "agents": list(self._agents.keys()),
    }

    if self._task_router:
        stats["routing"] = await self._task_router.get_statistics()  # ✅ AWAITED

    if self._orchestrator:
        stats["orchestrator"] = await self._orchestrator.get_statistics()  # ✅ AWAITED

    return stats
```

---

### Option B: Create Sync Wrapper

**Pros:**
- Doesn't break existing callers
- Backward compatible

**Cons:**
- More complex
- May run event loop

**Implementation:**
```python
def get_statistics(self) -> Dict[str, Any]:
    """Get system statistics (sync wrapper)."""
    stats = {
        "initialized": self._initialized,
        "project_path": str(self.project_path),
        "agent_count": len(self._agents),
        "agents": list(self._agents.keys()),
    }

    # Get sync stats or create task
    if self._task_router:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Event loop running, can't await
                stats["routing"] = {"status": "unavailable (async)"}
            else:
                stats["routing"] = loop.run_until_complete(
                    self._task_router.get_statistics()
                )
        except Exception:
            stats["routing"] = {"status": "unavailable"}

    if self._orchestrator:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                stats["orchestrator"] = {"status": "unavailable (async)"}
            else:
                stats["orchestrator"] = loop.run_until_complete(
                    self._orchestrator.get_statistics()
                )
        except Exception:
            stats["orchestrator"] = {"status": "unavailable"}

    return stats

async def get_statistics_async(self) -> Dict[str, Any]:
    """Get system statistics (async version)."""
    stats = {
        "initialized": self._initialized,
        "project_path": str(self.project_path),
        "agent_count": len(self._agents),
        "agents": list(self._agents.keys()),
    }

    if self._task_router:
        stats["routing"] = await self._task_router.get_statistics()

    if self._orchestrator:
        stats["orchestrator"] = await self._orchestrator.get_statistics()

    return stats
```

---

### Option C: Add Sync Methods to Components

**Pros:**
- Clean separation
- Both sync and async available

**Cons:**
- More code to maintain
- Duplicates functionality

**Implementation:**

```python
# In TaskRouter
def get_statistics_sync(self) -> Dict[str, Any]:
    """Get statistics (sync version)."""
    return {
        "registered_agents": len(self._agents),
        "last_routing": None,
        # ... sync-only stats
    }

async def get_statistics(self) -> Dict[str, Any]:
    """Get statistics (async version)."""
    return {
        "registered_agents": len(self._agents),
        "last_routing": await self._get_last_routing_async(),
        # ... full stats
    }
```

---

## Recommendation: Option A

Make `get_statistics()` async for consistency and correctness.

---

## Implementation Plan

### Step 1: Update main.py (30 min)

**Change:**
```python
# BEFORE:
def get_statistics(self) -> Dict[str, Any]:
    ...

# AFTER:
async def get_statistics(self) -> Dict[str, Any]:
    ...
```

**Add await:**
```python
if self._task_router:
    stats["routing"] = await self._task_router.get_statistics()

if self._orchestrator:
    stats["orchestrator"] = await self._orchestrator.get_statistics()
```

---

### Step 2: Update Callers (30 min)

**Find all callers:**
```bash
grep -r "get_statistics()" blackbox5 --include="*.py"
```

**Update each:**
```python
# BEFORE:
stats = bb5.get_statistics()

# AFTER:
stats = await bb5.get_statistics()
```

**Known callers:**
- `main.py:789` - Test code in `if __name__ == "__main__"`

---

### Step 3: Test (15 min)

```python
# test_statistics.py

import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path("blackbox5/2-engine/01-core/infrastructure")))

from main import Blackbox5

async def test_statistics():
    """Test get_statistics works correctly"""
    bb5 = Blackbox5()
    await bb5.initialize()

    # Get statistics
    stats = await bb5.get_statistics()

    print(f"Initialized: {stats['initialized']}")
    print(f"Agents: {stats['agent_count']}")
    print(f"Routing stats type: {type(stats.get('routing'))}")
    print(f"Orchestrator stats type: {type(stats.get('orchestrator'))}")

    # Verify not coroutine objects
    assert not isinstance(stats.get('routing'), asyncio.coroutines.Coroutine), \
        "Routing stats is coroutine, not awaited!"
    assert not isinstance(stats.get('orchestrator'), asyncio.coroutines.Coroutine), \
        "Orchestrator stats is coroutine, not awaited!"

    print("✅ Statistics work correctly")

    await bb5.shutdown()

asyncio.run(test_statistics())
```

---

## Success Criteria

- ✅ `get_statistics()` is async
- ✅ All async methods properly awaited
- ✅ No coroutine objects in output
- ✅ No RuntimeWarning about unawaited coroutines
- ✅ Statistics display actual data
- ✅ All callers updated to await

---

## Rollout Plan

### Pre-conditions
- [ ] PLAN-008 complete (main.py working)
- [ ] All callers identified

### Execution
1. Make get_statistics() async
2. Add await to async calls
3. Update all callers
4. Test statistics display

### Post-conditions
- [ ] No coroutine warnings
- [ ] Statistics display correctly
- [ ] All code using stats updated

---

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Breaking existing callers | Medium | Medium | Find all callers with grep |
| Event loop issues | Low | Low | Only in async context |
| Test code fails | Low | Low | Update test code too |

---

## Dependencies

**Blocks:**
- Statistics display
- Monitoring functionality

**Blocked By:**
- PLAN-008 (should fix main.py first)

**Can Parallel With:**
- Most other plans (different methods)

---

## Files to Modify

| File | Changes | Description |
|------|---------|-------------|
| `main.py:688` | 1 | Change def to async def |
| `main.py:702` | 1 | Add await to task_router.get_statistics() |
| `main.py:705` | 1 | Add await to orchestrator.get_statistics() |
| `main.py:789` | 1 | Update test code to await |

**Total:** 4 line changes

---

## Next Steps

1. Update main.py get_statistics() (30 min)
2. Update all callers (30 min)
3. Test statistics (15 min)

**Total Estimated Time:** 1 hour

---

**Status:** Planned
**Ready to Execute:** After PLAN-008
**Assigned To:** Unassigned
**Priority:** 🟡 MEDIUM (display issue, doesn't break functionality)
