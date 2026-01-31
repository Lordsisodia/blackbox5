# TASK: Refactor Orchestrator.execute_workflow Method

**Type:** Code Quality / Refactoring
**Priority:** HIGH (P0)
**Status:** pending
**Estimated Effort:** 1 week
**Assigned To:** TBD (Senior Developer)

---

## Objective

Refactor the 138-line `execute_workflow` method in `Orchestrator.py` into smaller, focused methods to improve testability, maintainability, and readability.

---

## Success Criteria

- [ ] No method in Orchestrator exceeds 30 lines
- [ ] `execute_workflow` delegates to focused helper methods
- [ ] All extracted methods have unit tests
- [ ] Integration test verifies behavior unchanged
- [ ] Logging maintained or improved
- [ ] Code review approved
- [ ] No performance regression

---

## Current State

**File:** `2-engine/core/orchestration/Orchestrator.py`
**Method:** `execute_workflow` (lines 190-328)
**Size:** 138 lines
**Responsibilities:**
- Input validation
- Context preparation
- Step execution
- Error handling
- State management
- Completion handling
- Logging

---

## Proposed Structure

### Main Method (Orchestrator.py)

```python
def execute_workflow(self, workflow, context):
    """
    Execute a workflow with proper error handling and state management.

    Args:
        workflow: The workflow to execute
        context: Execution context with configuration

    Returns:
        dict: Execution results with status and data

    Raises:
        WorkflowError: If workflow execution fails
    """
    # Validate inputs
    self._validate_workflow_inputs(workflow, context)

    # Prepare execution context
    exec_context = self._prepare_execution_context(workflow, context)

    # Execute workflow steps
    try:
        results = self._execute_workflow_steps(workflow, exec_context)
    except WorkflowError as e:
        return self._handle_workflow_error(e, exec_context)

    # Handle completion
    return self._handle_workflow_completion(results, exec_context)
```

### Extracted Methods

#### 1. Input Validation
```python
def _validate_workflow_inputs(self, workflow, context):
    """
    Validate workflow and context before execution.

    Args:
        workflow: The workflow to validate
        context: The context to validate

    Raises:
        ValueError: If inputs are invalid
        TypeError: If inputs have wrong type
    """
    if not workflow:
        raise ValueError("Workflow cannot be empty")

    if not context:
        raise ValueError("Context cannot be empty")

    if not hasattr(workflow, 'steps'):
        raise TypeError("Workflow must have 'steps' attribute")

    if not workflow.steps:
        raise ValueError("Workflow must have at least one step")

    # Add more validation as needed
```

#### 2. Context Preparation
```python
def _prepare_execution_context(self, workflow, context):
    """
    Prepare the execution context with all required state.

    Args:
        workflow: The workflow to execute
        context: Base execution context

    Returns:
        dict: Enhanced execution context
    """
    exec_context = {
        "workflow": workflow,
        "base_context": context,
        "state": "initialized",
        "start_time": time.time(),
        "step_results": [],
        "metadata": {
            "workflow_id": getattr(workflow, 'id', 'unknown'),
            "workflow_name": getattr(workflow, 'name', 'unnamed'),
        }
    }

    # Add any additional preparation
    self._log_workflow_start(exec_context)

    return exec_context
```

#### 3. Step Execution
```python
def _execute_workflow_steps(self, workflow, exec_context):
    """
    Execute all workflow steps in order.

    Args:
        workflow: The workflow with steps to execute
        exec_context: Current execution context

    Returns:
        list: Results from each step

    Raises:
        WorkflowError: If any step fails
    """
    results = []

    for idx, step in enumerate(workflow.steps):
        self._log_step_start(idx, step, exec_context)

        try:
            step_result = self._execute_step(step, exec_context)
            results.append(step_result)

            # Update context with step result
            exec_context["step_results"].append(step_result)

            self._log_step_complete(idx, step, step_result)

        except Exception as e:
            error = WorkflowError(
                f"Step {idx} failed: {str(e)}",
                step_index=idx,
                step=step,
                context=exec_context
            )
            self._log_step_error(idx, step, e)
            raise error

    return results
```

#### 4. Error Handling
```python
def _handle_workflow_error(self, error, exec_context):
    """
    Handle workflow execution errors.

    Args:
        error: The WorkflowError that occurred
        exec_context: Current execution context

    Returns:
        dict: Error result with details
    """
    duration = time.time() - exec_context["start_time"]

    logger.error(
        f"Workflow {exec_context['metadata']['workflow_name']} "
        f"failed after {duration:.2f}s: {error}"
    )

    # Update state
    exec_context["state"] = "failed"
    exec_context["error"] = str(error)
    exec_context["duration"] = duration

    # Save error to state manager if available
    if self.state_manager:
        self.state_manager.save_error_state(exec_context)

    return {
        "status": "error",
        "error": str(error),
        "step_index": getattr(error, 'step_index', None),
        "duration": duration,
        "context": exec_context
    }
```

#### 5. Completion Handling
```python
def _handle_workflow_completion(self, results, exec_context):
    """
    Handle successful workflow completion.

    Args:
        results: Results from all steps
        exec_context: Current execution context

    Returns:
        dict: Success result with data
    """
    duration = time.time() - exec_context["start_time"]

    logger.info(
        f"Workflow {exec_context['metadata']['workflow_name']} "
        f"completed in {duration:.2f}s with {len(results)} steps"
    )

    # Update state
    exec_context["state"] = "completed"
    exec_context["results"] = results
    exec_context["duration"] = duration

    # Save completion state if available
    if self.state_manager:
        self.state_manager.save_completion_state(exec_context)

    return {
        "status": "completed",
        "results": results,
        "duration": duration,
        "step_count": len(results),
        "context": exec_context
    }
```

---

## Implementation Steps

### Step 1: Create Test Coverage (Days 1-2)
**Before refactoring, ensure we have test coverage for current behavior.**

1. Write integration test for `execute_workflow`:
```python
# tests/core/orchestration/test_orchestrator_execute_workflow.py
import pytest
from core.orchestration.Orchestrator import Orchestrator

def test_execute_workflow_success():
    """Test successful workflow execution."""
    orchestrator = Orchestrator()
    workflow = create_test_workflow(steps=[...])
    context = create_test_context()

    result = orchestrator.execute_workflow(workflow, context)

    assert result["status"] == "completed"
    assert "results" in result
    assert result["step_count"] == len(workflow.steps)

def test_execute_workflow_with_invalid_input():
    """Test workflow with invalid input."""
    orchestrator = Orchestrator()

    with pytest.raises(ValueError):
        orchestrator.execute_workflow(None, {})

def test_execute_workflow_with_step_failure():
    """Test workflow when a step fails."""
    orchestrator = Orchestrator()
    workflow = create_test_workflow_with_failing_step()
    context = create_test_context()

    result = orchestrator.execute_workflow(workflow, context)

    assert result["status"] == "error"
    assert "error" in result

def test_execute_workflow_logging():
    """Test that workflow execution produces appropriate logs."""
    # Capture logs and verify
```

2. Run tests to ensure they pass:
```bash
pytest tests/core/orchestration/test_orchestrator_execute_workflow.py -v
```

3. **Save baseline:** This test suite ensures refactoring doesn't change behavior.

---

### Step 2: Extract Validation Logic (Day 2)
1. Extract input validation to `_validate_workflow_inputs`
2. Update `execute_workflow` to call extracted method
3. Run tests to verify no breakage
4. Add unit tests for validation method

---

### Step 3: Extract Context Preparation (Day 2-3)
1. Extract context preparation to `_prepare_execution_context`
2. Update `execute_workflow`
3. Run tests
4. Add unit tests

---

### Step 4: Extract Step Execution (Day 3-4)
1. Extract step execution to `_execute_workflow_steps`
2. Extract step error handling to `_log_step_error`
3. Update `execute_workflow`
4. Run tests
5. Add unit tests

---

### Step 5: Extract Error Handling (Day 4)
1. Extract error handling to `_handle_workflow_error`
2. Update `execute_workflow`
3. Run tests
4. Add unit tests

---

### Step 6: Extract Completion Handling (Day 4-5)
1. Extract completion handling to `_handle_workflow_completion`
2. Update `execute_workflow`
3. Run tests
4. Add unit tests

---

### Step 7: Clean Up and Optimize (Day 5)
1. Review all extracted methods
2. Check for code duplication
3. Verify logging is consistent
4. Add docstrings if missing
5. Check for performance issues

---

### Step 8: Final Testing (Day 6)
1. Run full test suite:
```bash
pytest tests/core/orchestration/ -v
```

2. Run integration tests:
```bash
pytest tests/integration/ -v
```

3. Performance test (ensure no regression):
```python
def test_execute_workflow_performance():
    """Verify refactoring didn't degrade performance."""
    import time

    orchestrator = Orchestrator()
    workflow = create_large_test_workflow()
    context = create_test_context()

    start = time.time()
    result = orchestrator.execute_workflow(workflow, context)
    duration = time.time() - start

    assert duration < 5.0  # Should complete in < 5 seconds
```

---

### Step 9: Code Review (Day 6-7)
1. Create pull request:
   - Link to issue/task
   - Describe refactoring approach
   - Show before/after comparison
   - Include test results

2. Request review from:
   - Senior developer
   - Architecture team (if major change)

3. Address feedback

---

## Testing Strategy

### Unit Tests
- Test each extracted method independently
- Test edge cases (empty inputs, None values, etc.)
- Test error paths

### Integration Tests
- Test full workflow execution
- Test multi-step workflows
- Test error recovery
- Test state management

### Performance Tests
- Benchmark before and after
- Ensure no regression
- Test with large workflows

---

## Deliverables

1. Refactored `execute_workflow` method
2. Extracted helper methods (5+ methods)
3. Comprehensive test coverage
4. Performance benchmarks
5. Updated docstrings
6. Code review approval

---

## Benefits of This Refactoring

### Before
- 138-line method (hard to understand)
- Multiple responsibilities (violates SRP)
- Difficult to test (requires complex setup)
- Hard to modify (risk of breaking things)

### After
- 15-line main method (easy to understand)
- Single responsibility per method
- Easy to test (each method tested independently)
- Easy to modify (changes isolated to specific method)

---

## References

- **Gap ID:** CQ-003
- **Related Documentation:** `gaps.md`, `phase-0-critical-fixes.md`
- **File:** `2-engine/core/orchestration/Orchestrator.py:190-328`
- **Pattern:** Extract Method refactoring (Martin Fowler)

---

## Notes

- **Why this matters:** Large methods are difficult to understand, test, and modify
- **Refactoring principle:** Each method should do one thing well
- **Testing is critical:** Must have tests before refactoring to ensure behavior doesn't change
- **Keep it small:** Aim for methods under 30 lines
- **Descriptive names:** Method names should clearly describe what they do
