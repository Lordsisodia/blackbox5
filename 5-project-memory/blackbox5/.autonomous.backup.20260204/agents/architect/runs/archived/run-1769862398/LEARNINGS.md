# LEARNINGS: TASK-1769862394 - Continue PLAN-003 PlanningAgent Integration & Tests

## Key Learnings

### 1. Code Structure Evolution
**Learning:** The codebase has migrated from `2-engine/01-core/` to `2-engine/core/`
**Impact:** Existing tests and documentation may reference old paths
**Action:** Always verify actual file structure before assuming paths

### 2. AgentConfig Dataclass Requirements
**Learning:** AgentConfig is a dataclass with specific required fields
**Details:**
- Required: `name`, `full_name`, `role`, `category`, `description`
- Optional: `capabilities`, `tools`, `temperature`, `max_tokens`, `metadata`
**Impact:** Instantiation fails without all required fields
**Best Practice:** Always check dataclass definition before instantiation

### 3. Dynamic Path Resolution
**Learning:** Using `Path(__file__)` to find project root is more robust than hardcoded paths
**Pattern Used:**
```python
root = Path(__file__).resolve()
while root.name != '2-engine' and root.parent != root:
    root = root.parent
sys.path.insert(0, str(root))
```
**Benefit:** Works regardless of where test is run from

### 4. Async Testing Pattern
**Learning:** Python 3.7+ makes async testing simple with `asyncio.run()`
**No Need For:** pytest-asyncio or custom event loops for simple tests

### 5. Integration Test Value
**Learning:** A simple integration test caught two issues:
- Import path configuration problem
- AgentConfig parameter mismatch
**ROI:** High - 30 lines of test code prevented future debugging

## Lessons for Future Tasks

1. **Always read the actual class definition** before writing tests
2. **Check existing test patterns** in the codebase for consistency
3. **Use dynamic path resolution** for test portability
4. **Write tests first** (TDD) or at least alongside code changes
5. **Run tests immediately** after writing them to catch issues early
