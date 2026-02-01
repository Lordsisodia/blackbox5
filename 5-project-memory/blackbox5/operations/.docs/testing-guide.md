# Testing Guide

**Purpose:** Practical guide for implementing tests in RALF executor runs

**Audience:** RALF executors implementing tasks

**Last Updated:** 2026-02-01

---

## Quick Start

### 1. Before You Write Code

Always write the test first:

```python
# test_calculator.py
import unittest

class TestCalculator(unittest.TestCase):
    def test_add_two_positive_numbers(self):
        """Test adding two positive numbers."""
        result = add(2, 3)
        self.assertEqual(result, 5)

    def test_add_negative_numbers(self):
        """Test adding negative numbers."""
        result = add(-2, -3)
        self.assertEqual(result, -5)
```

Run the test to confirm it fails:

```bash
python3 -m unittest test_calculator -v
# Expected: FAIL (function doesn't exist yet)
```

### 2. Write Minimal Code

```python
# calculator.py
def add(a, b):
    """Add two numbers."""
    return a + b
```

Run the test again:

```bash
python3 -m unittest test_calculator -v
# Expected: OK
```

### 3. Refactor

Improve the code while keeping tests green:

```python
def add(a: int, b: int) -> int:
    """
    Add two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    return a + b
```

---

## Test Structure

### Arrange-Act-Assert Pattern

Every test should follow this structure:

```python
def test_feature_description(self):
    # Arrange: Set up test data and conditions
    input_data = {"key": "value"}
    expected_result = "expected"

    # Act: Execute the code being tested
    result = function_under_test(input_data)

    # Assert: Verify the result
    self.assertEqual(result, expected_result)
```

### Given-When-Then Pattern (BDD Style)

```python
def test_given_valid_input_when_processing_then_returns_success(self):
    # Given
    context = setup_valid_context()

    # When
    result = process(context)

    # Then
    self.assertTrue(result.is_success)
```

---

## Testing Different Components

### Unit Tests

Test individual functions in isolation:

```python
class TestTaskParser(unittest.TestCase):
    def test_parse_valid_task_file(self):
        """Test parsing a well-formed task file."""
        content = """
# TASK-001: Test Task

**Status:** pending
**Priority:** high
"""
        task = parse_task(content)
        self.assertEqual(task["id"], "TASK-001")
        self.assertEqual(task["title"], "Test Task")
        self.assertEqual(task["status"], "pending")

    def test_parse_invalid_task_file(self):
        """Test parsing malformed task file."""
        with self.assertRaises(ParseError):
            parse_task("invalid content")
```

### Integration Tests

Test component interactions:

```python
class TestTaskExecution(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.run_dir = create_temp_run_dir()
        initialize_systems(self.run_dir)

    def test_full_task_lifecycle(self):
        """Test complete task execution flow."""
        # Create task
        task = create_task("TASK-001", "Test Task")

        # Execute task
        result = execute_task(task, self.run_dir)

        # Verify results
        self.assertTrue(result.success)
        self.assert_file_exists(self.run_dir / "RESULTS.md")
```

### Shell Script Tests

For CLI tools and workflows:

```bash
#!/bin/bash
# test-workflow.sh

set -e  # Exit on error

# Setup
TEST_DIR=$(mktemp -d)
trap "rm -rf $TEST_DIR" EXIT

# Test: Initialize run directory
echo "Testing: Initialize run directory"
./ralf.sh init --run-dir "$TEST_DIR"
assert_file_exists "$TEST_DIR/metadata.yaml"

# Test: Execute task
echo "Testing: Execute task"
./ralf.sh execute --task TASK-001 --run-dir "$TEST_DIR"
assert_file_exists "$TEST_DIR/RESULTS.md"

# Test: Verify results
echo "Testing: Verify results"
if grep -q "COMPLETE" "$TEST_DIR/RESULTS.md"; then
    echo "✓ Test passed"
else
    echo "✗ Test failed"
    exit 1
fi

echo "All tests passed!"
```

---

## Async Testing

### Basic Async Test

```python
import asyncio
import unittest

class TestAsyncOperations(unittest.TestCase):
    def test_async_function(self):
        """Test an async function."""
        async def run_test():
            result = await fetch_data()
            self.assertIsNotNone(result)

        asyncio.run(run_test())
```

### Testing with pytest-asyncio

```python
import pytest

@pytest.mark.asyncio
async def test_async_fetch():
    """Test async data fetching."""
    result = await fetch_data("https://api.example.com")
    assert result["status"] == "success"
```

### Mocking Async Functions

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_with_mocked_client():
    """Test with mocked async client."""
    mock_client = AsyncMock()
    mock_client.get.return_value = {"data": "test"}

    result = await service.get_data(client=mock_client)

    assert result == {"data": "test"}
    mock_client.get.assert_called_once()
```

---

## Test Data Management

### Using Fixtures

```python
# conftest.py
import pytest

@pytest.fixture
def sample_task():
    """Provide a sample task for testing."""
    return {
        "id": "TASK-001",
        "title": "Test Task",
        "status": "pending",
        "priority": "high"
    }

@pytest.fixture
def temp_run_dir(tmp_path):
    """Provide a temporary run directory."""
    run_dir = tmp_path / "run-0001"
    run_dir.mkdir()
    return run_dir
```

Using fixtures in tests:

```python
def test_task_processing(sample_task, temp_run_dir):
    """Test task processing with fixtures."""
    result = process_task(sample_task, temp_run_dir)
    assert result.success
```

### Factory Pattern

```python
class TaskFactory:
    """Factory for creating test tasks."""

    def __init__(self):
        self.counter = 0

    def create(self, **overrides):
        """Create a task with default values."""
        self.counter += 1
        defaults = {
            "id": f"TASK-{self.counter:04d}",
            "title": f"Test Task {self.counter}",
            "status": "pending",
            "priority": "medium"
        }
        defaults.update(overrides)
        return defaults

# Usage
factory = TaskFactory()
task1 = factory.create(priority="high")
task2 = factory.create(status="in_progress")
```

---

## Mocking

### Mocking External Services

```python
from unittest.mock import patch, MagicMock

class TestExternalAPI(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_user_data(self, mock_get):
        """Test fetching user data with mocked API."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {"name": "John", "id": 123}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Act
        result = fetch_user(123)

        # Assert
        self.assertEqual(result["name"], "John")
        mock_get.assert_called_with(
            "https://api.example.com/users/123",
            timeout=30
        )
```

### Mocking File System

```python
from unittest.mock import mock_open, patch

def test_file_processing():
    """Test file processing with mocked file system."""
    mock_content = "line1\nline2\nline3"

    with patch('builtins.open', mock_open(read_data=mock_content)):
        result = process_file('test.txt')

    assert len(result) == 3
```

---

## Common Patterns

### Testing Exceptions

```python
def test_raises_error_on_invalid_input():
    """Test that function raises appropriate error."""
    with pytest.raises(ValueError, match="Invalid input"):
        process_data(None)

    with pytest.raises(FileNotFoundError):
        read_file("/nonexistent/path")
```

### Parameterized Tests

```python
import unittest

class TestCalculator(unittest.TestCase):
    def test_addition(self):
        """Test addition with multiple cases."""
        test_cases = [
            (1, 1, 2),
            (0, 0, 0),
            (-1, 1, 0),
            (100, 200, 300),
        ]
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                result = add(a, b)
                self.assertEqual(result, expected)
```

### Testing Side Effects

```python
def test_creates_output_file():
    """Test that function creates expected output."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "output.txt"

        generate_report(output_path)

        assert output_path.exists()
        content = output_path.read_text()
        assert "Report" in content
```

---

## RALF-Specific Testing

### Testing Phase Gates

```python
def test_phase_gate_transitions():
    """Test phase gate enforcement."""
    run_dir = create_test_run()

    # Initial state
    assert get_current_phase(run_dir) == "init"

    # Transition to next phase
    mark_phase_complete(run_dir, "init")
    assert can_enter_phase(run_dir, "planning")

    # Try invalid transition
    assert not can_enter_phase(run_dir, "execution")
```

### Testing Context Budget

```python
def test_context_budget_thresholds():
    """Test context budget threshold enforcement."""
    run_dir = create_test_run()
    budget = initialize_budget(run_dir, max_tokens=100000)

    # Below warning threshold
    assert check_budget(budget, tokens_used=50000).status == "ok"

    # At warning threshold
    assert check_budget(budget, tokens_used=70000).status == "warning"

    # At critical threshold
    assert check_budget(budget, tokens_used=85000).status == "critical"
```

### Testing Decision Registry

```python
def test_decision_registry():
    """Test decision recording and retrieval."""
    run_dir = create_test_run()

    # Record a decision
    record_decision(
        run_dir=run_dir,
        decision_id="DEC-001",
        context="Choosing database",
        selected="PostgreSQL",
        rationale="Better JSON support"
    )

    # Retrieve decision
    decision = get_decision(run_dir, "DEC-001")
    assert decision["selected"] == "PostgreSQL"
```

---

## Running Tests

### Run All Tests

```bash
# Python unittest
python3 -m unittest discover -s tests -v

# pytest
pytest -v
```

### Run Specific Test

```bash
# Run specific test file
python3 -m unittest test_calculator -v

# Run specific test class
python3 -m unittest test_calculator.TestCalculator -v

# Run specific test method
python3 -m unittest test_calculator.TestCalculator.test_add -v
```

### Run with Coverage

```bash
# Install coverage tool
pip install coverage

# Run tests with coverage
coverage run -m unittest discover -s tests
coverage report
coverage html  # Generate HTML report
```

### Run Integration Tests

```bash
# Run RALF integration tests
python3 2-engine/.autonomous/lib/integration_test.py run --run-dir ~/.blackbox5/5-project-memory/ralf-core/.autonomous/runs/run-0001

# Quick verification
python3 2-engine/.autonomous/lib/integration_test.py verify-all
```

---

## Best Practices

### DO

- ✓ Write tests before code (TDD)
- ✓ Keep tests independent and isolated
- ✓ Use descriptive test names
- ✓ Test edge cases and error conditions
- ✓ Use fixtures for common setup
- ✓ Mock external dependencies
- ✓ Keep tests fast
- ✓ Run tests frequently

### DON'T

- ✗ Skip tests because they take too long
- ✗ Test implementation details
- ✗ Share state between tests
- ✗ Ignore failing tests
- ✗ Write tests without assertions
- ✗ Test private methods directly
- ✗ Use sleep() in tests

---

## Troubleshooting

### Test is Flaky

```python
# Bad: Time-dependent test
def test_timeout():
    start = time.time()
    result = slow_operation()
    assert time.time() - start < 1.0  # Flaky!

# Good: Mock time or use deterministic approach
@patch('time.time')
def test_timeout(mock_time):
    mock_time.side_effect = [0, 0.5]  # Controlled time
    result = slow_operation()
    assert result.completed
```

### Test is Slow

```python
# Bad: Hits real database
def test_user_creation():
    user = create_user_in_database()  # Slow!
    assert user.id is not None

# Good: Use in-memory or mock
@patch('database.create_user')
def test_user_creation(mock_create):
    mock_create.return_value = User(id=123)
    user = create_user()
    assert user.id == 123
```

### Test is Brittle

```python
# Bad: Tests internal structure
def test_internal():
    obj = MyClass()
    assert obj._internal_state == "value"  # Brittle!

# Good: Tests public behavior
def test_behavior():
    obj = MyClass()
    result = obj.public_method()
    assert result == "expected"  # Stable
```

---

## Resources

- [Python unittest documentation](https://docs.python.org/3/library/unittest.html)
- [pytest documentation](https://docs.pytest.org/)
- [BATS testing framework](https://github.com/bats-core/bats-core)
- [operations/testing-guidelines.yaml](../testing-guidelines.yaml)
- [operations/quality-gates.yaml](../quality-gates.yaml)
