# RALF Loop 2 Analysis: Testing and Validation Dependencies

## Executive Summary

RALF's testing infrastructure is **deeply coupled to BlackBox5**. The agent scripts all hardcode BB5 paths and assumptions. This means RALF cannot be tested independently and cannot be used on other projects without code changes.

## Critical Findings

### 1. Hardcoded Test Paths (All Agent Scripts)

**All 6 agent scripts hardcode BB5 paths:**

```python
# verifier-validate.py lines 24-26
PROJECT_DIR = Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"

# executor-implement.py lines 25-29
PROJECT_DIR = Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"
ENGINE_DIR = Path.home() / ".blackbox5" / "2-engine"

# planner-prioritize.py lines 23-26
PROJECT_DIR = Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"

# scout-intelligent.py lines 30-32
PROJECT_DIR = Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"

# improvement-loop.py lines 24-27
PROJECT_DIR = Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"
ENGINE_DIR = Path.home() / ".blackbox5" / "2-engine"
```

**Impact:** These agents cannot be tested or run against any other project.

### 2. Validation Logic Tied to BB5-Specific Files

**verifier-validate.py lines 67-132:**
```python
def validate_threshold_fix(self, task: Dict) -> Dict:
    """Validate threshold fix was applied correctly."""
    file_path = PROJECT_DIR / "operations" / "skill-selection.yaml"
    # Validates specific threshold value (60%) for BB5
```

**verifier-validate.py lines 134-190:**
```python
def validate_engine_path_fix(self, task: Dict) -> Dict:
    """Validate engine path fix."""
    file_path = PROJECT_DIR / "bin" / "blackbox.py"
    # Validates specific path change (01-core -> core) for BB5
```

**verifier-validate.py lines 192-214:**
```python
def validate_task(self, task: Dict) -> Dict:
    # Routes validation based on hardcoded task IDs
    if task_id in ["TASK-SKIL-005", "TASK-SKIL-008"]:
        return self.validate_threshold_fix(task)
```

### 3. Test Data Assumes BB5 Structure

**executor-implement.py lines 93-157:**
```python
def execute_threshold_fix(self, task: Dict) -> Dict:
    file_path = PROJECT_DIR / "operations" / "skill-selection.yaml"
    # Hardcodes regex patterns for BB5-specific content
    content = re.sub(r'threshold: 70', 'threshold: 60', content)
```

**executor-implement.py lines 158-203:**
```python
def execute_fix_engine_path(self, task: Dict) -> Dict:
    # Assumes blackbox.py exists at BB5 path
    # Hardcodes path replacement specific to BB5 history
```

### 4. Missing Test Coverage

**Tests that ARE project-agnostic (good):**
- `lib/test_decision_registry.py` - Tests decision registry
- `lib/test_memory.py` - Tests memory system
- `lib/test_state_machine.py` - Tests state machine
- `lib/test_workspace.py` - Tests workspace factory

**Tests that ARE BlackBox5-coupled (problematic):**
- `tests/test_all_features.py` - Tests BB5-specific features
- `tests/unit/test_agent_coordination.py` - Imports from BB5 paths
- `tests/unit/test_agent_output_bus.py` - Uses BB5-specific handlers

**Missing test coverage:**
- No tests for agent loop scripts (scout, planner, executor, verifier)
- No tests for improvement loop orchestration
- No integration tests for Scout→Planner→Executor→Verifier pipeline
- No tests for project-agnostic configuration loading

### 5. Verifier Assumes BB5 Structure for "Valid"

**verifier/verifier-v1.md lines 38-151:**
```bash
# Check 1: File Existence (weight: 0.20)
verify_files_exist() {
    local working_dir="$RALF_PROJECT_DIR/tasks/working/$task_id"
    # ...
}

# 3. Unit Tests (weight: 0.20)
verify_unit_tests() {
    if [ -f "pytest.ini" ] || [ -d "tests" ]; then
        pytest $(get_test_files_for_task "$task_id") --tb=short
        return $?
    fi
    echo "SKIP: No tests found"
    return 0
}
```

**Assumptions:**
- Tasks are in `tasks/working/` directory
- Tests discoverable via `pytest.ini` or `tests/` directory
- Project uses pytest
- Modified files determined from task ID

### 6. validate.sh Requires BB5 Structure

**shell/validate.sh lines 70-88:**
```bash
echo -e "${BLUE}Project Structure:${NC}"
check ".Autonomous directory exists" "[ -d '$PROJECT_DIR/.Autonomous' ]" "required"
check "LEGACY.md exists" "[ -f '$PROJECT_DIR/.Autonomous/LEGACY.md' ]" "required"
check "legacy-loop.sh exists" "[ -f '$PROJECT_DIR/.Autonomous/legacy-loop.sh' ]" "required"
check "tasks/active/ exists" "[ -d '$PROJECT_DIR/.Autonomous/tasks/active' ]" "required"
```

**Lines 82-87:**
```bash
echo -e "${BLUE}Prompt Components:${NC}"
check "prompts/system/identity.md" "[ -f '$PROJECT_DIR/.Autonomous/prompts/system/identity.md' ]" "required"
check "prompts/context/bb5-infrastructure.md" "[ -f '$PROJECT_DIR/.Autonomous/prompts/context/bb5-infrastructure.md' ]" "required"
```

## What Would Be Needed to Test RALF Independently

### A. Configuration Abstraction Layer
- Replace hardcoded `PROJECT_DIR` and `ENGINE_DIR` with configuration
- Support environment variables: `RALF_PROJECT_DIR`, `RALF_ENGINE_DIR`
- Support config file: `.ralfrc` or `ralf.yaml`

### B. Project-Agnostic Validation Framework
- Define generic validation interfaces
- Allow projects to register custom validators
- Remove hardcoded task ID routing

### C. Test Harness for Agent Scripts
- Create mock project structures for testing
- Provide test fixtures for each agent type
- Add integration tests for full pipeline

### D. Separated Test Suites
- **RALF Core Tests:** Test engine without any project
- **RALF Integration Tests:** Test with mock projects
- **BlackBox5 Tests:** Test BB5-specific functionality separately

### E. Example Project Template
- Create minimal example project for testing
- Use for testing and documentation
- Keep separate from BB5

## Decoupling Recommendations

### Immediate (High Priority)
1. **Extract configuration** from all agent scripts into shared config module
2. **Add environment variable support** for `RALF_PROJECT_DIR` and `RALF_ENGINE_DIR`
3. **Create test fixtures** for mock projects

### Short-term (Medium Priority)
4. **Refactor verifier** to use pluggable validators
5. **Refactor executor** to use task handlers from config
6. **Separate BB5-specific tests** from RALF core tests

### Long-term (Lower Priority)
7. **Create RALF test harness** for temporary projects
8. **Add CI/CD pipeline** testing against multiple projects
9. **Document testing patterns** for projects using RALF

## Conclusion

RALF's testing infrastructure is **deeply coupled to BlackBox5**. The agent scripts hardcode BB5 paths and assumptions. This means:

1. **RALF cannot be tested independently** of BB5
2. **RALF cannot be used on other projects** without code changes
3. **Tests for RALF core** are mixed with BB5-specific tests
4. **Validation logic** assumes BB5's structure and conventions

To make RALF portable and testable, these dependencies must be abstracted behind configuration interfaces.
