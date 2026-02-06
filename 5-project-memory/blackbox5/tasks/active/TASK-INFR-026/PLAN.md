# PLAN.md: Test Results Template Not Populated

**Task ID:** TASK-INFR-026  
**Status:** Planning  
**Priority:** MEDIUM  
**Category:** Infrastructure  
**Estimated Effort:** 80 minutes  
**Importance Rating:** 75/100

---

## 1. First Principles Analysis

### Why is Test Result Aggregation Important?

1. **Visibility Without Noise**: Know test status without CI logs
2. **Trend Analysis**: Historical data reveals patterns
3. **Quality Gates**: Automated decisions based on results
4. **Debugging Efficiency**: Centralized failure info

### What Happens Without Tracking?

- **Template empty**: `test_results.yaml` has `FILL_ME` placeholders
- **No historical visibility**: Cannot track health over time
- **Manual investigation**: Dig through GitHub Actions
- **Missed regressions**: No automated detection

### How Can We Aggregate from CI/CD?

Current CI/CD already:
1. Runs pytest with coverage
2. Uploads to Codecov
3. Generates XML reports

**Missing:**
- JUnit XML output
- Artifact upload
- Script to populate `test_results.yaml`
- Aggregation across runs

---

## 2. Current State Assessment

### Existing Infrastructure

| Component | Location | Status |
|-----------|----------|--------|
| CI Workflow | `.github/workflows/ci.yml` | Active |
| Test Results Template | `test_results.yaml` | **Empty** |
| Template Definition | `.templates/root/test_results.yaml.template` | **Empty** |
| Existing Results | `2-engine/tests/blackbox5-test-results.txt` | 48 tests, 89.6% pass |

### Current CI Test Execution

```yaml
- name: Run unit tests
  run: |
    pytest 2-engine/tests/unit/ -v --tb=short \
      --cov=2-engine --cov-report=xml
  continue-on-error: true
```

**Issues:**
- No JUnit XML output
- No artifact upload
- `continue-on-error: true` masks failures

---

## 3. Proposed Solution

### Aggregation Pipeline

```
CI/CD Pipeline
    ↓
Pytest with JUnit XML
    ↓
Artifact Upload
    ↓
Aggregation Script
    ↓
Populated test_results.yaml
    ↓
Dashboard
```

### Aggregation Schema

```yaml
test_run:
  id: "TR-{timestamp}"
  timestamp: "2026-02-06T12:00:00Z"
  branch: "main"
  commit_sha: "abc123"

summary:
  total_tests: 48
  passed: 43
  failed: 5
  coverage_percent: 89.6
  duration_seconds: 45.2

suites:
  - name: "unit"
    total: 24
    passed: 22
    failed: 2

test_cases:
  - id: "TC-001"
    name: "test_agent_coordination"
    status: "passed"
    duration_seconds: 0.45

history:
  - date: "2026-02-05"
    passed: 45
    failed: 3
    coverage: 90.2
```

---

## 4. Implementation Plan

### Phase 1: Design Schema (15 min)

1. Define complete YAML schema
2. Design history retention (30 runs)
3. Define status calculation
4. Create schema validation

### Phase 2: Create CI/CD Integration (20 min)

1. Modify `.github/workflows/ci.yml`:
   - Add `--junitxml=test-results.xml`
   - Add artifact upload step
   - Add aggregation step

### Phase 3: Implement Storage Script (20 min)

Create `bb5-test-results-aggregator.py`:
- Parse JUnit XML
- Extract coverage from coverage.xml
- Update test_results.yaml
- Maintain history

### Phase 4: Create Dashboard (10 min)

Create `bb5-test-dashboard.py`:
- Generate markdown dashboard
- Test trend graph
- Flaky test warnings

### Phase 5: Test and Document (15 min)

1. Test aggregator locally
2. Trigger CI on test branch
3. Verify file populated
4. Document usage

---

## 5. Success Criteria

| Criterion | Metric | Verification |
|-----------|--------|--------------|
| Schema defined | 100% documented | Template updated |
| CI integration | Artifacts uploaded | Check Actions |
| Storage implemented | test_results.yaml populated | File has data |
| Dashboard created | Markdown exists | test-dashboard.md |
| History maintained | 30 days | History array |

---

## 6. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Schema | 15 min | 15 min |
| Phase 2: CI/CD | 20 min | 35 min |
| Phase 3: Script | 20 min | 55 min |
| Phase 4: Dashboard | 10 min | 65 min |
| Phase 5: Test | 15 min | 80 min |
| **Total** | **80 min** | **~1.5 hours** |

---

*Plan created based on test infrastructure analysis*
