# Testing Agent Workflow

**Purpose**: Test functionality, ensure Supabase connections work
**Trigger**: After feature implementation or on-demand
**Mode**: `testing`

---

## Workflow Steps

### 1. Test Discovery

```yaml
step: discover_tests
actions:
  - Find all test files:
      - Unit tests: *.test.ts, *.test.js
      - Integration tests: *.integration.test.ts
      - E2E tests: *.e2e.test.ts

  - Identify tests for recent changes:
      - Tests in modified files
      - Tests for affected features
      - New tests added

  - Check for missing tests:
      - Files without corresponding tests
      - Features without test coverage
```

### 2. Test Environment Setup

```yaml
step: setup_environment
actions:
  - Verify test database (if needed)
  - Reset test data
  - Verify Supabase test project
  - Check environment variables
  - Install dependencies if needed
```

### 3. Unit Tests

```yaml
step: run_unit_tests
actions:
  - Run unit test suite
  - Capture results:
      - Total tests
      - Passed
      - Failed
      - Skipped
      - Duration

  - For failures:
      - Capture error messages
      - Identify failing files
      - Categorize errors

  - Generate unit test report
```

### 4. Integration Tests

```yaml
step: run_integration_tests
actions:
  - Run integration test suite
  - Focus on Supabase connections:
      - Database operations
      - RLS policies
      - Auth flows
      - API endpoints

  - Test data flow:
      - Create → Read → Update → Delete
      - Error handling
      - Edge cases

  - Capture results
  - Generate integration test report
```

### 5. Supabase Verification

```yaml
step: verify_supabase
critical: true
actions:
  - Test connection:
      - Can connect to project
      - Auth is working
      - Database is accessible

  - Test RLS policies:
      - Policies are in place
      - Policies work as expected
      - No unauthorized access

  - Test migrations:
      - Migrations run successfully
      - Schema matches code
      - No drift

  - Document any issues
```

### 6. Test Results Analysis

```yaml
step: analyze_results
actions:
  - Aggregate all test results
  - Calculate metrics:
      - Pass rate
      - Coverage (if available)
      - Average duration

  - Identify patterns:
      - Common failure types
      - Flaky tests
      - Slow tests

  - Compare to baseline:
      - Previous run results
      - Trend analysis
```

### 7. Issue Documentation

```yaml
step: document_issues
actions:
  - For each failure:
      - Document error
      - Identify root cause
      - Suggest fix
      - Create task if needed

  - Categorize issues:
      - Critical: Block deployment
      - High: Should fix soon
      - Medium: Fix when convenient
      - Low: Nice to have
```

### 8. Report Generation

```yaml
step: generate_report
output: STATE/test-report-{timestamp}.yaml
content:
  - timestamp
  - summary:
      - total_tests: N
      - passed: N
      - failed: N
      - skipped: N
      - pass_rate: N%
      - duration: N seconds

  - unit_tests:
      - total: N
      - passed: N
      - failed: N

  - integration_tests:
      - total: N
      - passed: N
      - failed: N

  - supabase:
      - connection: pass/fail
      - rls: pass/fail
      - migrations: pass/fail

  - failures:
      - test_name
      - error_message
      - severity
      - suggested_fix

  - recommendations: []
```

### 9. State Update

```yaml
step: update_state
actions:
  - Update TEST-RESULTS.yaml
  - Update feature status if tests pass
  - Mark tasks as "tested" or "needs_fix"
  - Log to WORK-LOG.md
```

---

## Decision Points

### If Critical Tests Fail
```
Action: Block deployment
- Mark feature as "blocked"
- Alert user immediately
- Create high-priority fix task
- Do not proceed with deployment
```

### If Supabase Connection Fails
```
Action: Investigate
- Check network
- Verify credentials
- Check Supabase status
- Retry with backoff
- If still failing, alert user
```

### If Coverage Too Low
```
Action: Suggest tests
- Identify untested code
- Create tasks for test creation
- Do not block (warning only)
```

---

## Output

### All Tests Pass
```yaml
status: success
timestamp: "2026-01-30T10:00:00Z"
results:
  unit_tests:
    total: 50
    passed: 50
    failed: 0
    duration: 30s

  integration_tests:
    total: 20
    passed: 20
    failed: 0
    duration: 60s

  supabase:
    connection: pass
    rls: pass
    migrations: pass

  overall:
    pass_rate: 100%
    status: "ready_for_deployment"
```

### Some Tests Fail
```yaml
status: partial
timestamp: "2026-01-30T10:00:00Z"
results:
  unit_tests:
    total: 50
    passed: 48
    failed: 2

  failures:
    - test: "user-profile.test.ts"
      error: "Cannot read property 'name' of undefined"
      severity: high
      fix_task: "TASK-2026-01-30-003"

    - test: "auth.integration.test.ts"
      error: "RLS policy blocking valid request"
      severity: critical
      fix_task: "TASK-2026-01-30-004"

  status: "blocked"
  action_required: "Fix critical RLS issue"
```

---

## Integration with Other Agents

After testing:
1. Signal feature-dev agent if fixes needed
2. Update STATE.yaml with test results
3. Update TEST-RESULTS.yaml
4. Log to WORK-LOG.md
5. If all pass, signal deployment (if configured)
