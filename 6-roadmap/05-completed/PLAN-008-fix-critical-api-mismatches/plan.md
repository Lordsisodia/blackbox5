# PLAN-008: Fix Critical API Mismatches in main.py

**Priority:** 🔴 CRITICAL (System Won't Boot)
**Status:** Planned
**Estimated Effort:** 2-3 hours
**Dependencies:** None
**Discovered By:** First Principles Analysis

---

## Problem Statement

**main.py cannot process a single request** due to API mismatches. The system boots but **completely fails** when trying to execute.

**Impact:** BlackBox5 is 100% non-functional for request processing

---

## Critical Issues Found

### Issue 1: Task Constructor Parameter Mismatch 🚨

**Location:** `main.py:450`

**Code:**
```python
# main.py tries to create Task like this:
task = Task(
    task_id=f"task_{session_id}",  # ❌ WRONG PARAMETER NAME
    description=request,
    task_type=task_type,
    domain=domain,
    priority=priority,
    context=context,
    metadata={"session_id": session_id}
)
```

**Actual Task class expects:**
```python
# routing/task_router.py Task class:
class Task:
    def __init__(
        self,
        id: str,              # ✅ CORRECT PARAMETER NAME
        description: str,
        task_type: str = "general",
        domain: str = "general",
        priority: str = "normal",
        context: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
```

**Error:**
```python
TypeError: __init__() got an unexpected keyword argument 'task_id'
```

**Fix:**
```python
# Change task_id to id
task = Task(
    id=f"task_{session_id}",  # ✅ FIXED
    description=request,
    task_type=task_type,
    domain=domain,
    priority=priority,
    context=context,
    metadata={"session_id": session_id}
)
```

---

### Issue 2: Orchestrator Method Doesn't Exist 🚨

**Location:** `main.py:612`

**Code:**
```python
# main.py calls:
result = await self._orchestrator.execute_wave_based(
    tasks=[workflow_step],
    workflow_id=task.task_id
)  # ❌ METHOD DOESN'T EXIST
```

**Actual Orchestrator methods:**
```python
# orchestration/Orchestrator.py has:
- execute_workflow()          # ✅ EXISTS
- create_sequential_workflow() # ✅ EXISTS
- create_parallel_workflow()   # ✅ EXISTS
- execute_wave_based()         # ❌ DOESN'T EXIST
```

**Error:**
```python
AttributeError: 'AgentOrchestrator' object has no attribute 'execute_wave_based'
```

**Fix Options:**

**Option A: Use execute_workflow() (Recommended)**
```python
result = await self._orchestrator.execute_workflow(
    workflow_id=task.task_id,
    steps=[workflow_step]
)
```

**Option B: Use create_sequential_workflow()**
```python
workflow = self._orchestrator.create_sequential_workflow(
    workflow_id=task.task_id,
    steps=[workflow_step]
)
result = await workflow.execute()
```

---

### Issue 3: Task/AgentTask Type Mismatch 🚨

**Location:** `main.py:558`

**Code:**
```python
# main.py tries to convert Task to AgentTask:
agent_task = AgentTask(
    id=task.task_id,        # ❌ Wrong parameter names
    description=task.description,
    type=task.task_type,    # ❌ Wrong parameter names
    complexity="medium",
    context=task.context or {}
)
```

**Actual AgentTask class:**
```python
# agents/core/base_agent.py:
@dataclass
class AgentTask:
    task_id: str            # ✅ CORRECT PARAMETER NAME
    description: str
    type: str = "general"
    complexity: str = "medium"
    context: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    deadline: Optional[datetime] = None
```

**Error:**
```python
TypeError: AgentTask.__init__() got an unexpected keyword argument 'id'
```

**Fix:**
```python
# Use correct parameter names:
agent_task = AgentTask(
    task_id=task.id,        # ✅ FIXED (was task.task_id)
    description=task.description,
    type=task.task_type,
    complexity="medium",
    context=task.context or {}
)
```

---

## Solution Design

### Phase 1: Fix Task Constructor (30 min)

**File:** `main.py:450`

**Change:**
```python
# BEFORE:
task = Task(
    task_id=f"task_{session_id}",
    ...
)

# AFTER:
task = Task(
    id=f"task_{session_id}",
    ...
)
```

**Also update all references:**
```python
# Find all uses of task.task_id and change to task.id
# main.py:392, 401, 450, 457, 586, 614
```

---

### Phase 2: Fix Orchestrator Call (1 hour)

**File:** `main.py:612`

**Change:**
```python
# BEFORE:
result = await self._orchestrator.execute_wave_based(
    tasks=[workflow_step],
    workflow_id=task.task_id
)

# AFTER:
result = await self._orchestrator.execute_workflow(
    workflow_id=task.id,
    steps=[workflow_step]
)
```

**Also update result handling:**
```python
# Check what execute_workflow() returns and update accordingly
# Current code expects result.state, result.results, etc.
# Verify execute_workflow() returns compatible structure
```

---

### Phase 3: Fix AgentTask Creation (30 min)

**File:** `main.py:558`

**Change:**
```python
# BEFORE:
agent_task = AgentTask(
    id=task.task_id,
    description=task.description,
    type=task.task_type,
    complexity="medium",
    context=task.context or {}
)

# AFTER:
agent_task = AgentTask(
    task_id=task.id,
    description=task.description,
    type=task.task_type,
    complexity="medium",
    context=task.context or {}
)
```

---

### Phase 4: Fix All task.task_id References (30 min)

**Find and replace:**
```bash
# Find all occurrences
grep -n "task\.task_id" main.py

# Replace with task.id
# Also check for task.task_type → task.task_type (OK)
# task.domain → task.domain (OK)
# task.description → task.description (OK)
```

**Locations to update:**
- main.py:392 - `logger.info(f"Parsed task: {task.task_id}...")`
- main.py:401 - routing decision logging
- main.py:450 - Task constructor (already fixed)
- main.py:457 - metadata
- main.py:558 - AgentTask conversion (already fixed)
- main.py:586 - workflow_id
- main.py:614 - orchestrator call

---

## Implementation Plan

### Step 1: Create Test Script (30 min)

```python
# test_main_py_fixes.py

import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path("blackbox5/2-engine/01-core")))

async def test_task_creation():
    """Test Task can be created with correct parameters"""
    from routing.task_router import Task

    try:
        task = Task(
            id="test_123",
            description="Test task",
            task_type="testing"
        )
        print("✅ Task creation works")
        return True
    except Exception as e:
        print(f"❌ Task creation failed: {e}")
        return False

async def test_agent_task_creation():
    """Test AgentTask can be created"""
    from agents.core.base_agent import AgentTask

    try:
        agent_task = AgentTask(
            task_id="test_123",
            description="Test task",
            type="testing"
        )
        print("✅ AgentTask creation works")
        return True
    except Exception as e:
        print(f"❌ AgentTask creation failed: {e}")
        return False

async def test_orchestrator_method():
    """Test Orchestrator has correct method"""
    from orchestration.Orchestrator import AgentOrchestrator

    try:
        orchestrator = AgentOrchestrator(event_bus=None, task_router=None, memory_base_path="./memory")
        # Check if method exists
        if hasattr(orchestrator, 'execute_workflow'):
            print("✅ Orchestrator.execute_workflow exists")
            return True
        else:
            print(f"❌ Available methods: {[m for m in dir(orchestrator) if not m.startswith('_')]}")
            return False
    except Exception as e:
        print(f"❌ Orchestrator test failed: {e}")
        return False

async def main():
    print("Testing main.py fixes...")
    print("="*60)

    results = []
    results.append(await test_task_creation())
    results.append(await test_agent_task_creation())
    results.append(await test_orchestrator_method())

    print("="*60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")

if __name__ == "__main__":
    asyncio.run(main())
```

### Step 2: Apply Fixes (1 hour)

1. Fix Task constructor (30 min)
2. Fix Orchestrator call (30 min)
3. Fix AgentTask conversion (30 min)
4. Fix all task.task_id references (30 min)

### Step 3: Test End-to-End (30 min)

```python
# test_main_bootstrap.py

import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path("blackbox5/2-engine/01-core/infrastructure")))

async def test_full_bootstrap():
    """Test main.py can boot and process a request"""
    from main import Blackbox5

    bb5 = Blackbox5()
    await bb5.initialize()

    # Try processing a request
    result = await bb5.process_request(
        request="Write a hello world function in Python"
    )

    print(f"Success: {result['result']['success']}")
    print(f"Agent: {result['routing']['agent']}")
    print(f"Strategy: {result['routing']['strategy']}")

    await bb5.shutdown()

asyncio.run(test_full_bootstrap())
```

---

## Success Criteria

- ✅ Task constructor works with `id` parameter
- ✅ AgentTask constructor works with `task_id` parameter
- ✅ Orchestrator.execute_workflow() called correctly
- ✅ All task.task_id references changed to task.id
- ✅ main.py boots successfully
- ✅ main.py can process a simple request
- ✅ No TypeError or AttributeError

---

## Rollout Plan

### Pre-conditions
- [ ] Test script created
- [ ] All fixes identified
- [ ] Backup created

### Execution
1. Run test script to confirm issues
2. Apply all fixes
3. Run test script again
4. Test full bootstrap
5. Verify request processing works

### Post-conditions
- [ ] main.py boots without errors
- [ ] Can process simple requests
- [ ] Single-agent execution works
- [ ] Multi-agent execution works

---

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Breaking other code using Task.task_id | Medium | High | Search entire codebase |
| Orchestrator API different than expected | Medium | Medium | Check Orchestrator source |
| Type mismatches in result handling | Low | Medium | Add error handling |

---

## Dependencies

**Blocks:**
- main.py request processing
- All BlackBox5 functionality

**Blocked By:**
- None

**Can Parallel With:**
- All other plans (different file)

---

## Files to Modify

| File | Lines Changed | Description |
|------|---------------|-------------|
| `main.py:450` | 1 | Task constructor: task_id → id |
| `main.py:392` | 1 | Logging: task.task_id → task.id |
| `main.py:558` | 1 | AgentTask: id → task_id |
| `main.py:586` | 1 | workflow_id: task.task_id → task.id |
| `main.py:612` | 3 | Orchestrator method call |
| `main.py:614` | 1 | workflow_id: task.task_id → task.id |

**Total:** ~8 line changes

---

## Next Steps

1. Create test script (30 min)
2. Apply fixes (1 hour)
3. Test bootstrap (30 min)
4. Test request processing (30 min)

**Total Estimated Time:** 2-3 hours

---

**Status:** Planned
**Ready to Execute:** Yes
**Assigned To:** Unassigned
**Priority:** 🔴 CRITICAL (main.py 100% broken)
