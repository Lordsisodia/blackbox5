# Test Case Registry

This directory contains the test case registry for the BB5/SISO-Internal project.

## Structure

Each test case is stored as a separate YAML file with the naming convention:
```
{TC-CATEGORY-NNN}.yaml
```

Examples:
- `TC-UNIT-001.yaml` - Unit test case
- `TC-INT-001.yaml` - Integration test case
- `TC-E2E-001.yaml` - End-to-end test case
- `TC-SAFETY-001.yaml` - Safety system test case
- `TC-QUALITY-001.yaml` - Quality gate validation

## Categories

| Category | Code | Description | Target Count |
|----------|------|-------------|--------------|
| Unit | UNIT | Individual function/class tests | 100 |
| Integration | INT | Component interaction tests | 30 |
| End-to-End | E2E | Full workflow tests | 15 |
| Safety | SAFETY | Safety system tests | 10 |
| Quality | QUALITY | Quality gate validations | 20 |

## Test Case Schema

```yaml
test_case:
  id: "TC-UNIT-001"
  name: "Descriptive test name"
  category: "unit"
  priority: "critical|high|medium|low"
  status: "active|draft|deprecated|skipped"
  automation_status: "automated|manual|partial"
  description: "Detailed test description"
  preconditions: "Setup required"
  steps:
    - "Step 1"
    - "Step 2"
  expected_result: "Expected outcome"
  related_requirements: ["REQ-001"]
  related_tasks: ["TASK-001"]
  automated_test_file: "path/to/test.py"
  automated_test_function: "test_function_name"
  last_executed: "2026-02-09T00:00:00Z"
  last_result: "passed|failed|error|skipped"
```

## Adding a New Test Case

1. Copy the template from `../.templates/tests/test-case-template.yaml`
2. Fill in all required fields
3. Name the file according to the convention
4. Update the test tracking system

## Current Status

See [Test Tracking System](../test-tracking-system.yaml) for current metrics and gaps.
