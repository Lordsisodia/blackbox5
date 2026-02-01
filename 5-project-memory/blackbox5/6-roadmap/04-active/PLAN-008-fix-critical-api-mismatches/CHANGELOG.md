# PLAN-008: API Mismatch Fixes - Detailed Change Log

## Overview
Fixed 4 critical API parameter mismatches in `main.py` that prevented the Blackbox5 system from processing any requests.

## File Modified
`2-engine/01-core/infrastructure/main.py`

---

## Change 1: Task Object Initialization (Lines 449-459)

### Issue
Task class was being instantiated with incorrect parameter names:
- Used `task_id` instead of `id`
- Used `task_type` instead of `type`
- Used `domain` which doesn't exist in Task class
- Used `context` which doesn't exist in Task class

### Fix
```python
# BEFORE (Incorrect):
task = Task(
    task_id=f"task_{session_id}",
    description=request,
    task_type=task_type,
    domain=domain,
    priority=priority,  # String instead of int
    context=context,     # Doesn't exist
    metadata={"session_id": session_id}
)

# AFTER (Correct):
task = Task(
    id=f"task_{session_id}",
    description=request,
    type=task_type,
    priority=self._map_priority_to_int(priority),  # Now int
    required_capabilities=set(),  # Required field
    metadata={"session_id": session_id, "domain": domain, "context": context}
)
```

### API Reference
Task class definition (`routing/task_router.py:96-103`):
```python
@dataclass
class Task:
    id: str
    description: str
    type: str = "general"
    priority: int = 5
    required_capabilities: Set[str] = field(default_factory=set)
    complexity: Optional[ComplexityLevel] = None
    estimated_duration: float = 10.0
    metadata: Dict[str, Any] = field(default_factory=dict)
```

---

## Change 2: Added Priority Mapping Helper (Lines 510-518)

### Issue
Task class expects `priority` as integer (1-10), but code was using string values.

### Fix
Added helper method to convert string priority to integer:
```python
def _map_priority_to_int(self, priority: str) -> int:
    """Map string priority to integer (1-10)."""
    priority_map = {
        "critical": 10,
        "high": 8,
        "normal": 5,
        "low": 2
    }
    return priority_map.get(priority.lower(), 5)
```

---

## Change 3: Fixed Task Field References (Line 392)

### Issue
Code referenced non-existent Task fields `task_id` and `domain`.

### Fix
```python
# BEFORE (Incorrect):
logger.info(f"Parsed task: {task.task_id} (type: {task.task_type}, domain: {task.domain})")

# AFTER (Correct):
logger.info(f"Parsed task: {task.id} (type: {task.type}, priority: {task.priority})")
```

---

## Change 4: Fixed AgentTask Creation (Lines 567-573)

### Issue
AgentTask was referencing non-existent `task.task_type` field and using `task.context` directly.

### Fix
```python
# BEFORE (Incorrect):
agent_task = AgentTask(
    id=task.id,
    description=task.description,
    type=task.task_type,  # Field doesn't exist
    complexity="medium",
    context=task.context or {}  # Field doesn't exist
)

# AFTER (Correct):
agent_task = AgentTask(
    id=task.id,
    description=task.description,
    type=task.type,  # Correct field
    complexity="medium",
    context=task.metadata.get("context", {})  # Correct access
)
```

### API Reference
AgentTask class definition (`agents/core/base_agent.py`):
```python
@dataclass
class AgentTask:
    id: str
    description: str
    type: str = "general"
    complexity: str = "medium"
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
```

---

## Change 5: Replaced execute_wave_based with execute_workflow (Lines 596-653)

### Issue
Code called non-existent `execute_wave_based()` method and used incorrect WorkflowStep parameters.

### Fix
```python
# BEFORE (Incorrect):
workflow_step = WorkflowStep(
    agent_type="developer",  # Wrong parameter
    task=task.description,    # Should be AgentTask
    agent_id=None,            # Doesn't exist
    timeout=300               # Should be float
)

result = await self._orchestrator.execute_wave_based(  # Method doesn't exist
    tasks=[workflow_step],
    workflow_id=task.id
)

# AFTER (Correct):
agent_task = AgentTask(
    id=task.id,
    description=task.description,
    type=task.type,
    complexity="medium",
    context=task.metadata.get("context", {})
)

workflow_step = WorkflowStep(
    name=f"Step: {task.description[:50]}",
    agent_name=routing_decision.recommended_agent or "developer",
    task=agent_task,
    timeout=300.0
)

workflow = Workflow(
    id=task.id,
    name=f"Workflow: {task.description[:50]}",
    description=task.description,
    steps=[workflow_step],
    metadata={"task_id": task.id}
)

result = await self._orchestrator.execute_workflow(workflow)
```

### API Reference
WorkflowStep class definition (`orchestration/Orchestrator.py:32-79`):
```python
@dataclass
class WorkflowStep:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    agent_name: str = ""
    task: Optional[AgentTask] = None
    depends_on: List[str] = field(default_factory=list)
    timeout: float = 300.0
    # ... other fields
```

Workflow class definition (`orchestration/Orchestrator.py:83-115`):
```python
@dataclass
class Workflow:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    steps: List[WorkflowStep] = field(default_factory=list)
    status: WorkflowStatus = WorkflowStatus.PENDING
    # ... other fields
```

AgentOrchestrator method signature:
```python
async def execute_workflow(self, workflow: Workflow) -> Workflow:
    """Execute a workflow."""
```

---

## Change 6: Added Workflow Import (Line 47)

### Issue
Workflow class wasn't imported but was needed.

### Fix
```python
# BEFORE:
from orchestration.Orchestrator import AgentOrchestrator, WorkflowStep

# AFTER:
from orchestration.Orchestrator import AgentOrchestrator, WorkflowStep, Workflow
```

---

## Change 7: Fixed All task.task_id References (Multiple Lines)

### Issue
Code used `task.task_id` but Task class uses `id` field.

### Fix
Replaced all instances of `task.task_id` with `task.id` using find-replace.

Affected lines:
- Line 392: Task logging
- Line 457: Task metadata
- Line 586: Multi-agent workflow
- Line 614: Multi-agent workflow ID
- Line 632: Multi-agent metadata

---

## Testing Summary

### Test 1: Import Test
```bash
cd 2-engine/01-core
python3 -c "from infrastructure.main import Blackbox5"
```
**Result:** ✅ PASSED - No import errors

### Test 2: Compilation Test
```bash
python3 -m py_compile infrastructure/main.py
```
**Result:** ✅ PASSED - No syntax errors

### Test 3: API Validation
Manually verified all class instantiations against their definitions.
**Result:** ✅ PASSED - All APIs match

---

## Files Referenced (Not Modified)

1. `2-engine/01-core/routing/task_router.py` - Task, AgentCapabilities, TaskRouter classes
2. `2-engine/01-core/agents/core/base_agent.py` - AgentTask, AgentResult classes
3. `2-engine/01-core/orchestration/Orchestrator.py` - Workflow, WorkflowStep, AgentOrchestrator classes

---

## Commit Message Suggestion

```
fix: Resolve critical API parameter mismatches in main.py

Fixed 4 critical issues preventing system from processing requests:

1. Task initialization: Changed task_id→id, task_type→type, removed domain
2. AgentTask creation: Fixed field references (type, context)
3. Orchestrator method: execute_wave_based→execute_workflow with proper Workflow object
4. Task field references: All task.task_id→task.id

Added _map_priority_to_int() helper to convert string priority to int.
Added Workflow to imports.

All changes align with actual class definitions in:
- routing/task_router.py (Task class)
- agents/core/base_agent.py (AgentTask class)
- orchestration/Orchestrator.py (Workflow, AgentOrchestrator)

Testing: Import and compilation tests pass.

Fixes: PLAN-008
```
