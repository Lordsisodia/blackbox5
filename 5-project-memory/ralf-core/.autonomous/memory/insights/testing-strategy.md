# RALF Testing Strategy

**Version:** 1.0
**Created:** 2026-01-30
**Status:** Active

---

## Overview

RALF needs to test changes it makes to the engine. This strategy defines how to test different component types safely.

---

## Component Types & Testing Approaches

### 1. Shell Scripts

**Location:** `engine/shell/`

**Testing Levels:**

#### Level 1: Syntax Validation
```bash
# Check syntax without executing
bash -n script.sh

# Check with shellcheck if available
shellcheck script.sh
```

#### Level 2: Dry-Run Mode
Scripts should support a `--dry-run` flag that:
- Shows what would be executed
- Validates paths and prerequisites
- Reports potential issues
- Returns exit code 0 if validation passes

#### Level 3: Test Environment
- Create isolated test workspace
- Run script against test data
- Verify expected outputs
- Clean up after test

**Current Scripts:**
| Script | Purpose | Test Priority |
|--------|---------|---------------|
| `ralf-loop.sh` | Main daemon loop | Critical |
| `telemetry.sh` | Telemetry collection | High |
| `validate.sh` | Validation utilities | High |
| `task` | Task management | Medium |
| `test-run.sh` | Test execution | Medium |
| `legacy-loop.sh` | Legacy loop (deprecated) | Low |

---

### 2. Library Code

**Location:** `engine/lib/`

**Testing Approach:**

#### Python Libraries
- Co-located unit tests: `test_{module}.py`
- pytest for test runner
- Mock external dependencies
- Test edge cases and error conditions

**Current Libraries:**
| Module | Purpose | Test Status |
|--------|---------|-------------|
| `memory.py` | Memory management | Needs tests |
| `session_tracker.py` | Session tracking | Needs tests |
| `state_machine.py` | State management | Needs tests |
| `workspace.py` | Workspace operations | Needs tests |

---

### 3. Prompts

**Location:** `engine/prompts/`

**Testing Approach:**

#### A/B Testing Framework
1. Version prompts with semantic versioning
2. Track success metrics per version
3. Compare performance across versions
4. Roll back if metrics degrade

**Metrics to Track:**
- Task completion rate
- Error rate
- Time to complete
- Quality of output (subjective assessment)

**Current Prompts:**
| Prompt | Purpose | Version |
|--------|---------|---------|
| `ralf.md` | Main RALF prompt | 1.0 |
| `system/identity.md` | System identity | ? |
| `context/*.md` | Context prompts | ? |
| `exit/*.md` | Exit condition prompts | ? |

---

### 4. Skills

**Location:** `engine/skills/`

**Testing Approach:**

#### Validation Checklist
- [ ] Skill YAML is valid
- [ ] Required fields present
- [ ] Examples work as documented
- [ ] Integration with BMAD works

---

### 5. Workflows

**Location:** `engine/workflows/`

**Testing Approach:**

#### Dry-Run Execution
- Execute workflow steps without side effects
- Validate step transitions
- Check input/output contracts

---

## Automated Testing Infrastructure

### Test Runner Script

Create `engine/shell/test-all.sh`:
```bash
#!/bin/bash
# Run all tests

# 1. Shell script syntax
for script in shell/*.sh; do
    bash -n "$script"
done

# 2. Python tests
cd lib && python -m pytest

# 3. Validate YAML files
# 4. Check prompt formatting
# 5. Integration tests
```

### Pre-Commit Hooks

Before RALF commits changes:
1. Run syntax checks
2. Run unit tests
3. Validate YAML/JSON
4. Check for debug code

### Test Data

Maintain test fixtures in:
- `engine/tests/fixtures/` - Test data files
- `engine/tests/mocks/` - Mock implementations

---

## Testing Workflow for RALF

### Before Making Changes

1. **Identify Component Type**
   - Shell script → Use syntax + dry-run tests
   - Library → Use unit tests
   - Prompt → Use A/B comparison

2. **Create Test Plan**
   - What could break?
   - How to detect breakage?
   - How to roll back?

### After Making Changes

1. **Run Component Tests**
   - Syntax validation
   - Unit tests
   - Dry-run mode

2. **Run Integration Tests**
   - Does it work with other components?
   - Are dependencies satisfied?

3. **Validate in Isolation**
   - Test in workspace/ directory
   - Use test data, not production

4. **Commit with Test Results**
   - Include test output in commit message
   - Reference test plan

---

## Risk Levels

| Change Type | Risk Level | Required Testing |
|-------------|------------|------------------|
| Documentation | Low | Visual review |
| New script | Medium | Syntax + dry-run |
| Modify existing script | High | Full test suite |
| Library change | High | Unit tests + integration |
| Prompt change | Medium | A/B test |
| Config change | Low | Validation |

---

## Success Metrics

- **Test Coverage:** % of components with tests
- **Pass Rate:** % of tests passing
- **Detection Rate:** % of bugs caught before commit
- **Rollback Rate:** % of changes reverted

---

## Future Enhancements

1. **Continuous Integration** - Auto-run tests on changes
2. **Coverage Reporting** - Track test coverage over time
3. **Performance Testing** - Measure script execution time
4. **Fuzzing** - Random input testing for robustness

---
