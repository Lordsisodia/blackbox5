# RALF Testing Guide

**Version:** 1.0.0
**Last Updated:** 2026-02-01
**Framework:** pytest

---

## Overview

RALF uses pytest for automated testing. The testing framework provides quality assurance, enables faster development, and serves as executable documentation.

### Test Structure

```
tests/
├── unit/              # Unit tests (fast, isolated)
├── integration/       # Integration tests (component interactions)
├── fixtures/          # Test fixtures and test data
├── lib/               # Test utilities and helpers
├── config/            # Test configuration files
├── conftest.py        # Shared pytest fixtures
└── pytest.ini         # Pytest configuration
```

### Test Categories

1. **Unit Tests:** Test individual components in isolation
   - Fast execution (< 1 second per test)
   - No external dependencies
   - Mock file I/O, network calls

2. **Integration Tests:** Test component interactions
   - Slower than unit tests
   - Test real dependencies
   - Focus on critical workflows

---

## Quick Start

### Installing Dependencies

```bash
# Install pytest
pip install pytest

# Optional: Install coverage.py
pip install coverage

# Optional: Install pytest-xdist for parallel execution
pip install pytest-xdist
```

### Running Tests

```bash
# Run all tests
./bin/run_tests.sh

# Run unit tests only
./bin/run_tests.sh --unit

# Run integration tests only
./bin/run_tests.sh --integration

# Run with verbose output
./bin/run_tests.sh --verbose

# Run with coverage reporting
./bin/run_tests.sh --coverage
```

### Using pytest Directly

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/unit/test_config_manager.py

# Run specific test
pytest tests/unit/test_config_manager.py::TestConfigManager::test_load_default_config

# Run with verbose output
pytest -v tests/

# Run with coverage
pytest --cov=2-engine/.autonomous/lib --cov-report=html
```

---

## Writing Tests

### Basic Test Structure

```python
import pytest

class TestMyComponent:
    """Test MyComponent functionality."""

    def test_something(self):
        """Test description."""
        # Arrange
        expected = "value"

        # Act
        actual = get_value()

        # Assert
        assert actual == expected
```

### Using Fixtures

```python
def test_with_fixture(temp_dir, sample_config):
    """Test using fixtures."""
    # temp_dir: Temporary directory (auto-cleaned)
    # sample_config: Sample configuration dict

    config_path = temp_dir / "config.yaml"
    # Use fixtures...
```

### Using Test Utilities

```python
from tests.lib.test_utils import (
    mock_config,
    mock_task,
    assert_file_exists,
    assert_yaml_valid
)

def test_with_utilities():
    """Test using utilities."""
    config = mock_config(skill_invocation_confidence=80)
    assert config['thresholds']['skill_invocation_confidence'] == 80
```

---

## Test Patterns

### Pattern 1: Testing File Operations

```python
def test_file_operation(temp_dir):
    """Test file creation and validation."""
    # Create file
    file_path = temp_dir / "test.txt"
    file_path.write_text("content")

    # Assert file exists
    assert_file_exists(str(file_path))
```

### Pattern 2: Testing YAML Config

```python
def test_yaml_config(mock_yaml_file):
    """Test YAML configuration loading."""
    # mock_yaml_file: Fixture that creates valid YAML

    # Assert YAML is valid
    assert_yaml_valid(mock_yaml_file)

    # Assert YAML has key
    assert_yaml_has_key(mock_yaml_file, 'thresholds.skill_invocation_confidence')
```

### Pattern 3: Testing with Mocks

```python
def test_with_mock_config():
    """Test using mock configuration."""
    # Create mock config
    config = mock_config(
        skill_invocation_confidence=85,
        queue_depth_min=2
    )

    # Use mock config in test
    assert config['thresholds']['skill_invocation_confidence'] == 85
```

### Pattern 4: Testing Error Handling

```python
def test_error_handling():
    """Test error handling."""
    # Expect exception
    with pytest.raises(ValueError):
        raise ValueError("Invalid value")
```

---

## Fixtures Reference

### Built-in Fixtures (conftest.py)

- **temp_dir:** Temporary directory (auto-cleaned after test)
- **sample_config:** Sample configuration dict
- **sample_task:** Sample task dict
- **sample_event:** Sample event dict
- **mock_yaml_file:** Mock YAML file with sample config
- **engine_lib_path:** Path to engine lib directory
- **reset_environment:** Reset environment variables (auto-applied)

### Using Fixtures

```python
def test_example(temp_dir, sample_config):
    """Test using fixtures."""
    # Use temp_dir for file operations
    config_file = temp_dir / "config.yaml"

    # Use sample_config as test data
    assert 'thresholds' in sample_config
```

---

## Test Utilities Reference

### File Assertions

```python
from tests.lib.test_utils import (
    assert_file_exists,
    assert_file_not_exists,
    assert_dir_exists
)

# Assert file exists
assert_file_exists("/path/to/file")

# Assert file doesn't exist
assert_file_not_exists("/path/to/nonexistent")

# Assert directory exists
assert_dir_exists("/path/to/dir")
```

### YAML Assertions

```python
from tests.lib.test_utils import (
    assert_yaml_valid,
    assert_yaml_has_key
)

# Assert YAML is valid
assert_yaml_valid("/path/to/config.yaml")

# Assert YAML has key (supports dot notation)
assert_yaml_has_key("/path/to/config.yaml", "thresholds.skill_invocation_confidence")
```

### Mock Generators

```python
from tests.lib.test_utils import (
    mock_config,
    mock_task,
    mock_event
)

# Generate mock config
config = mock_config(
    skill_invocation_confidence=80,
    queue_depth_min=2,
    queue_depth_max=8
)

# Generate mock task
task = mock_task(
    task_id="TASK-001",
    task_type="implement",
    priority="high"
)

# Generate mock event
event = mock_event(
    task_id="TASK-001",
    event_type="completed",
    result="success"
)
```

### Test Data Helpers

```python
from tests.lib.test_utils import (
    create_temp_yaml_file,
    create_temp_file,
    cleanup_test_files
)

# Create temp YAML file
yaml_path = create_temp_yaml_file({"key": "value"})

# Create temp text file
txt_path = create_temp_file("content", suffix=".txt")

# Clean up test files
cleanup_test_files(yaml_path, txt_path)
```

---

## Best Practices

### 1. Keep Tests Simple

```python
# Good: Simple, focused test
def test_confidence_default():
    """Test default confidence is 70."""
    config = ConfigManager()
    assert config.get('thresholds.skill_invocation_confidence') == 70

# Bad: Complex test with multiple assertions
def test_config_too_many_things():
    """Test too many things at once."""
    config = ConfigManager()
    assert config.get('thresholds.skill_invocation_confidence') == 70
    assert config.get('thresholds.queue_depth_min') == 3
    assert config.get('routing.default_agent') == 'executor'
    # ... too many assertions
```

### 2. Use Descriptive Names

```python
# Good: Descriptive name
def test_load_user_config_overrides_defaults()

# Bad: Vague name
def test_config()
```

### 3. Arrange, Act, Assert

```python
def test_user_config_override():
    # Arrange: Set up test data
    default_config = mock_config()
    user_config = mock_config(skill_invocation_confidence=80)

    # Act: Execute code under test
    config = ConfigManager(user_config, default_config)

    # Assert: Verify expected outcome
    assert config.get('thresholds.skill_invocation_confidence') == 80
```

### 4. Use Fixtures for Shared Setup

```python
# Good: Use fixture
@pytest.fixture
def config_file(temp_dir):
    """Create config file for testing."""
    config_path = temp_dir / "config.yaml"
    # ... create config
    return config_path

def test_with_config(config_file):
    """Test using shared fixture."""
    # Use config_file

# Bad: Duplicate setup
def test_a():
    config_path = Path("/tmp/test_a.yaml")
    # ... create config

def test_b():
    config_path = Path("/tmp/test_b.yaml")
    # ... duplicate setup code
```

### 5. Mock External Dependencies

```python
# Good: Mock file I/O
def test_with_mock(temp_dir):
    """Test using mock file system."""
    mock_file = temp_dir / "mock.yaml"
    mock_file.write_text("key: value")
    # Test with mock file

# Bad: Real file I/O
def test_with_real_file():
    """Test using real file system."""
    # Tests real file system (slower, side effects)
```

---

## CI/CD Integration

### Pre-commit Hook (Optional)

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Run tests before commit

./bin/run_tests.sh --unit

if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

### GitHub Actions (Future)

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install pytest
      - run: ./bin/run_tests.sh --coverage
```

---

## Troubleshooting

### Issue: Tests Fail with Import Errors

**Problem:** `ModuleNotFoundError: No module named 'config_manager'`

**Solution:** Ensure engine lib is in Python path:

```python
import sys
from pathlib import Path

ENGINE_LIB = Path("/workspaces/blackbox5/2-engine/.autonomous/lib")
if str(ENGINE_LIB) not in sys.path:
    sys.path.insert(0, str(ENGINE_LIB))
```

### Issue: Tests Are Slow

**Problem:** Tests take too long to run

**Solutions:**
- Use unit tests instead of integration tests
- Mock file I/O and network calls
- Run tests in parallel (pytest-xdist)
- Use `--unit` flag to run only fast tests

### Issue: Fixtures Don't Work

**Problem:** `fixture 'temp_dir' not found`

**Solution:** Ensure `conftest.py` is in `tests/` directory and pytest is run from project root.

### Issue: Coverage Report Missing

**Problem:** `--coverage` flag doesn't work

**Solution:** Install coverage.py:

```bash
pip install coverage
```

---

## Test Coverage

### Current Coverage

- **ConfigManager:** 8 tests covering load, validate, get, set, save
- **Queue Sync:** 1 test covering sync on task completion
- **Roadmap Sync:** 1 test covering metrics update
- **Task Distribution:** 1 test covering task routing
- **State Sync:** 1 test covering state synchronization

**Total:** 12 tests

### Target Coverage

- Unit tests: 80% coverage of core libraries
- Integration tests: Critical workflows covered
- Test execution time: < 10 seconds for all tests

---

## Adding New Tests

### Step 1: Create Test File

```bash
# Unit test
touch tests/unit/test_my_component.py

# Integration test
touch tests/integration/test_workflow.py
```

### Step 2: Write Test

```python
import pytest

class TestMyComponent:
    """Test MyComponent functionality."""

    def test_feature_x(self):
        """Test Feature X."""
        # Arrange, Act, Assert
        assert True
```

### Step 3: Run Test

```bash
# Run new test
pytest tests/unit/test_my_component.py -v
```

### Step 4: Add to Suite

Test is automatically discovered by pytest. No additional configuration needed.

---

## Resources

- **pytest Documentation:** https://docs.pytest.org/
- **Python Testing Best Practices:** https://docs.python-guide.org/writing/tests/
- **Coverage.py Documentation:** https://coverage.readthedocs.io/

---

## Summary

The RALF testing framework provides:

✅ **Fast Feedback:** Unit tests run in < 1 second each
✅ **Quality Assurance:** Catch bugs early, prevent regressions
✅ **Documentation:** Tests serve as executable documentation
✅ **CI/CD Foundation:** Ready for F-007 (CI/CD Pipeline Integration)
✅ **Developer Experience:** Simple, well-documented, easy to extend

**Next Steps:**
1. Run `./bin/run_tests.sh` to verify all tests pass
2. Add new tests when implementing features
3. Aim for 80% coverage of core libraries
4. Keep tests fast and focused

---

**End of Guide**
