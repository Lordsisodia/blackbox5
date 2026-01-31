# TASK: Increase Test Coverage to 70%

**Type:** Quality / Testing
**Priority:** HIGH (P1)
**Status:** pending
**Estimated Effort:** 4-6 weeks
**Assigned To:** TBD (QA Lead + Development Team)

---

## Objective

Increase test coverage from current ~24% (by file count) to 70%+ with focus on critical paths, error handling, and integration scenarios.

---

## Success Criteria

- [ ] Test coverage reaches 70%+ (measured by pytest-cov)
- [ ] All critical paths have integration tests
- [ ] All error paths are tested
- [ ] Test suite runs in < 10 minutes
- [ ] Coverage report generated in CI/CD
- [ ] Quality gates enforce coverage threshold

---

## Current State

**Test Files:** 91 files
**Total Python Files:** 381 files
**Current Coverage:** ~24% (by file count)
**Gap:** Need to add tests for ~290 files to reach 70%

**Coverage by Area:**
- Memory systems: Good coverage
- Safety systems: Good coverage
- Core orchestration: Moderate coverage
- Tools/integrations: Poor coverage
- Interface layer: Poor coverage

---

## Priority Areas for Testing

### 1. Critical Paths (Must Have)
**Priority:** P0
**Files:** ~50 files
**Effort:** 2 weeks

These are the core execution paths that must work:

- `core/orchestration/Orchestrator.py`
- `core/orchestration/task_router.py`
- `core/agents/definitions/core/base_agent.py`
- `runtime/memory/systems/EnhancedProductionMemorySystem.py`
- `core/interface/cli/task_commands.py`
- All agent implementations

**Test Types:**
- Unit tests for each method
- Integration tests for workflows
- End-to-end tests for critical paths

---

### 2. Error Handling (Must Have)
**Priority:** P0
**Files:** ~30 files
**Effort:** 1 week

Test all error paths and exception handling:

- All exception handling blocks
- Validation logic
- Failure recovery
- Error logging

**Test Types:**
- Negative tests (invalid inputs)
- Exception tests
- Error recovery tests

---

### 3. Integration Layer (Should Have)
**Priority:** P1
**Files:** ~40 files
**Effort:** 1.5 weeks

Test external integrations with mocking:

- `tools/integrations/github/`
- `tools/integrations/mcp/`
- `tools/integrations/supabase/`
- `tools/integrations/vibe/`

**Test Types:**
- Integration tests with mocking
- Contract tests
- Error handling tests

---

### 4. Interface Layer (Should Have)
**Priority:** P1
**Files:** ~30 files
**Effort:** 1 week

Test user-facing interfaces:

- CLI commands
- REST API endpoints
- Client library

**Test Types:**
- API tests
- CLI tests
- Client tests

---

### 5. Utility Functions (Nice to Have)
**Priority:** P2
**Files:** ~140 files
**Effort:** 1.5 weeks

Test helper functions and utilities:

- Core tools
- Utility functions
- Helper classes

**Test Types:**
- Unit tests

---

## Implementation Approach

### Phase 1: Setup and Baseline (Week 1)

**1.1 Setup Coverage Tools:**
```bash
# Install coverage tools
pip install pytest pytest-cov pytest-mock coverage[toml]

# Create pytest configuration
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["2-engine", "tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--cov=2-engine",
    "--cov-report=html",
    "--cov-report=term-missing",
    "--cov-fail-under=70"
]

# .coveragerc
[run]
source = 2-engine
omit = [
    "*/tests/*",
    "*/test_*.py",
    "*/__pycache__/*",
    "*/site-packages/*"
]

[report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "@abstractmethod"
]
```

**1.2 Generate Baseline Report:**
```bash
# Generate baseline coverage
pytest --cov=2-engine --cov-report=html --cov-report=term

# Open HTML report
open htmlcov/index.html
```

**1.3 Identify Untested Files:**
```bash
# Find files with no tests
coverage report --show-missing | grep "0%"
```

**1.4 Create Test Plan Spreadsheet:**
Track progress with columns:
- File path
- Priority (P0/P1/P2)
- Current coverage %
- Target coverage %
- Assigned to
- Status

---

### Phase 2: Critical Path Testing (Weeks 2-3)

**2.1 Orchestrator Tests:**
```python
# tests/core/orchestration/test_orchestrator.py

import pytest
from core.orchestration.Orchestrator import Orchestrator
from core.orchestration.state.Workflow import Workflow

class TestOrchestrator:
    """Test Orchestrator critical functionality."""

    def test_execute_workflow_success(self):
        """Test successful workflow execution."""
        orchestrator = Orchestrator()
        workflow = Workflow(name="test", steps=[...])
        result = orchestrator.execute_workflow(workflow, {})
        assert result["status"] == "completed"

    def test_execute_workflow_with_invalid_input(self):
        """Test workflow with invalid input raises error."""
        orchestrator = Orchestrator()
        with pytest.raises(ValueError):
            orchestrator.execute_workflow(None, {})

    def test_execute_workflow_with_step_failure(self):
        """Test workflow handles step failures correctly."""
        # Test implementation

    # Add 20+ more tests
```

**2.2 Agent Tests:**
```python
# tests/core/agents/test_base_agent.py

class TestBaseAgent:
    """Test BaseAgent core functionality."""

    def test_agent_initialization(self):
        """Test agent initializes correctly."""
        agent = BaseAgent(name="test", role="developer")
        assert agent.name == "test"
        assert agent.role == "developer"

    def test_agent_execute_task(self):
        """Test agent can execute a task."""
        # Test implementation

    # Add 15+ more tests
```

---

### Phase 3: Error Path Testing (Week 4)

**3.1 Test All Exception Handling:**
```python
def test_orchestrator_handles_keyboard_interrupt():
    """Test that KeyboardInterrupt is not caught."""
    orchestrator = Orchestrator()
    with pytest.raises(KeyboardInterrupt):
        orchestrator.execute_workflow(interrupting_workflow, {})

def test_memory_handles_database_errors():
    """Test memory system handles database errors."""
    memory = EnhancedProductionMemorySystem()
    with pytest.raises(DatabaseError):
        memory.store(None)  # Invalid input
```

---

### Phase 4: Integration Testing (Weeks 5-6)

**4.1 Integration Tests with Mocking:**
```python
# tests/integrations/test_github_integration.py

import pytest
from unittest.mock import Mock, patch
from tools.integrations.github.manager import GitHubManager

class TestGitHubIntegration:
    """Test GitHub integration."""

    @patch('tools.integrations.github.provider.GitHubProvider')
    def test_create_issue(self, mock_provider):
        """Test creating a GitHub issue."""
        mock_provider.create_issue.return_value = {"id": 123}
        manager = GitHubManager(token="test", repo="owner/repo")
        result = manager.create_issue("Test issue", "Body")
        assert result["id"] == 123

    # Add 10+ more tests
```

---

### Phase 5: Coverage Enforcement (Week 6)

**5.1 Add CI/CD Quality Gate:**
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements-dev.txt
      - run: pytest --cov=2-engine --cov-report=xml
      - uses: codecov/codecov-action@v2
      - name: Check coverage threshold
        run: |
          coverage report --fail-under=70
```

**5.2 Add Pre-Commit Hook:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: Run tests
        entry: pytest --cov=2-engine --cov-fail-under=70
        language: system
        pass_filenames: false
```

---

## Testing Best Practices

### 1. Test Structure
```python
# Arrange-Act-Assert pattern
def test_something():
    # Arrange: Set up test data
    input_data = create_test_data()

    # Act: Execute the code
    result = function_under_test(input_data)

    # Assert: Verify the result
    assert result == expected_output
```

### 2. Test Naming
```python
# Good: Descriptive
def test_orchestrator_returns_error_when_workflow_is_empty()

# Bad: Vague
def test_orchestrator()
```

### 3. Use Fixtures
```python
# conftest.py
@pytest.fixture
def sample_workflow():
    """Provide a sample workflow for testing."""
    return Workflow(name="test", steps=[...])

# Use in tests
def test_with_fixture(sample_workflow):
    result = orchestrator.execute_workflow(sample_workflow, {})
```

### 4. Mock External Dependencies
```python
from unittest.mock import patch

@patch('requests.get')
def test_external_api(mock_get):
    mock_get.return_value = Mock(status_code=200, json={"data": "test"})
    result = call_external_api()
    assert result == {"data": "test"}
```

---

## Coverage Targets by Area

| Area | Current | Target | Priority |
|------|---------|--------|----------|
| Core orchestration | 40% | 80% | P0 |
| Agent system | 30% | 75% | P0 |
| Memory systems | 60% | 85% | P0 |
| Safety systems | 50% | 80% | P0 |
| Integration layer | 10% | 70% | P1 |
| Interface layer | 15% | 70% | P1 |
| Tools | 5% | 60% | P2 |
| Utilities | 0% | 50% | P2 |

**Overall Target:** 70%

---

## Deliverables

1. Test coverage increased to 70%+
2. Coverage report in CI/CD
3. Quality gates enforcing threshold
4. Integration test suite
5. Test documentation
6. Pre-commit hooks for testing

---

## Metrics and Reporting

### Weekly Report
```markdown
# Test Coverage Progress - Week X

## Progress
- Files covered: 267/381 (70%)
- Lines covered: 35,000/50,000 (70%)
- Tests added: 50 new tests
- Tests passing: 450/450 (100%)

## This Week
- Completed: Core orchestration tests
- In Progress: Integration tests
- Next Week: Interface layer tests

## Blockers
- None

## Coverage by Area
| Area | Coverage | Target | Status |
|------|----------|--------|--------|
| Core | 85% | 80% | ✅ |
| Agents | 75% | 75% | ✅ |
| Memory | 82% | 85% | 🟡 |
```

---

## Risk Mitigation

### Risk 1: Test maintenance burden
**Mitigation:**
- Focus on stable APIs
- Use fixtures for test data
- Document test patterns

### Risk 2: Slow test suite
**Mitigation:**
- Use pytest-xdist for parallel execution
- Separate unit and integration tests
- Use mocking for slow operations

### Risk 3: Brittle tests
**Mitigation:**
- Avoid testing implementation details
- Test behavior, not implementation
- Use contract testing for integrations

---

## References

- **Gap ID:** TEST-001
- **Related Documentation:** `gaps.md`, `roadmap.md`
- **Tools:**
  - pytest: https://docs.pytest.org/
  - pytest-cov: https://pytest-cov.readthedocs.io/
  - coverage.py: https://coverage.readthedocs.io/

---

## Notes

- **Why this matters:** Low test coverage leads to regression risk and fear of refactoring
- **70% is achievable:** Focus on critical paths first
- **Quality over quantity:** Better to have good tests than just many tests
- **Make it fast:** Tests should run quickly or developers won't run them
- **Automated enforcement:** CI/CD gate prevents coverage regression
