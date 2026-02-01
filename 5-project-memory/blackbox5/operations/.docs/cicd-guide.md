# CI/CD Pipeline Guide

**Version:** 1.0.0
**Last Updated:** 2026-02-01
**Purpose:** Comprehensive guide for BlackBox5 CI/CD pipeline

---

## Table of Contents

1. [Overview](#overview)
2. [Pre-Commit Hooks](#pre-commit-hooks)
3. [GitHub Actions Workflows](#github-actions-workflows)
4. [Test Runner Script](#test-runner-script)
5. [Quality Gates](#quality-gates)
6. [Quality Gate Report](#quality-gate-report)
7. [Integration with Task Completion](#integration-with-task-completion)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)

---

## Overview

The BlackBox5 CI/CD pipeline provides automated testing, quality assurance, and deployment triggers integrated with the RALF task completion workflow. It ensures code quality before commits and prevents bad code from reaching the main branch.

### Pipeline Components

```
┌─────────────────┐
│  Code Change    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│  1. Pre-Commit Hooks             │
│     - Lint (black, isort, flake8)│
│     - YAML validation            │
│     - Secret detection           │
│     - Fast tests (pytest)        │
│     - Block commit on failure    │
└────────┬────────────────────────┘
         │ (commit allowed)
         ▼
┌─────────────────────────────────┐
│  2. Git Commit                   │
│     - Code committed to branch   │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  3. Git Push                     │
│     - Push to remote branch      │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  4. GitHub Actions CI            │
│     - Shell script linting       │
│     - Code quality (black, etc)  │
│     - Security scanning          │
│     - Unit tests (pytest)        │
│     - Smoke tests                │
│     - Quality gate: Block merge  │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  5. Quality Gate Report          │
│     - Results tracked            │
│     - Trends monitored           │
│     - Health status updated      │
└─────────────────────────────────┘
```

### Benefits

- **Catch errors early:** Pre-commit hooks catch issues before commit
- **Automated quality:** GitHub Actions runs comprehensive tests on every push
- **Quality gates:** Block merges if tests fail
- **Trend tracking:** Monitor quality metrics over time
- **Non-blocking:** Failures logged but don't halt development (except quality gates)

---

## Pre-Commit Hooks

### What Are Pre-Commit Hooks?

Pre-commit hooks are scripts that run automatically before a git commit is created. They catch issues early in the development cycle.

### Available Hooks

BlackBox5 includes the following pre-commit hooks:

| Hook | Purpose | Config |
|------|---------|--------|
| **trailing-whitespace** | Remove trailing whitespace | .pre-commit-config.yaml |
| **end-of-file-fixer** | Ensure newline at EOF | .pre-commit-config.yaml |
| **check-yaml** | Validate YAML syntax | .pre-commit-config.yaml |
| **check-json** | Validate JSON syntax | .pre-commit-config.yaml |
| **check-added-large-files** | Prevent large files > 1MB | .pre-commit-config.yaml |
| **detect-secrets** | Detect secrets in code | .pre-commit-config.yaml |
| **gitleaks** | Comprehensive secret scanning | .pre-commit-config.yaml |
| **bandit** | Python security linting | .pre-commit-config.yaml |
| **black** | Python code formatting | .pre-commit-config.yaml |
| **isort** | Python import sorting | .pre-commit-config.yaml |
| **flake8** | Python linting | .pre-commit-config.yaml |
| **pytest** | Run tests on changed files | .pre-commit-config.yaml |

### Installation

```bash
# Install pre-commit framework
pip install pre-commit

# Install hooks
pre-commit install

# Verify installation
pre-commit run --all-files
```

### Usage

Hooks run automatically on `git commit`. To manually run all hooks:

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run specific hooks
pre-commit run black --all-files
pre-commit run flake8 --all-files
```

### Bypassing Pre-Commit Hooks

**WARNING:** Bypassing pre-commit hooks is discouraged. Use only in emergencies.

```bash
# Bypass all hooks (NOT RECOMMENDED)
git commit --no-verify -m "Commit message"

# Bypass specific hook (edit .pre-commit-config.yaml, comment out hook, commit, restore)
```

### Updating Hooks

```bash
# Update hook versions
pre-commit autoupdate

# Reinstall with updated versions
pre-commit install --force
```

---

## GitHub Actions Workflows

### Available Workflows

BlackBox5 includes the following GitHub Actions workflows:

| Workflow | Purpose | Triggers |
|----------|---------|----------|
| **ci.yml** | Main CI pipeline | Push to main, pull requests |
| **test.yml** | Test suite (unit + integration) | Manual, scheduled, PR labels |
| **docs.yml** | Documentation builds | Push to main, PR |
| **scheduled.yml** | Scheduled tasks | Cron schedule |
| **pr-checks.yml** | PR-specific checks | Pull requests |
| **keepalive.yml** | Keep workflow active | Schedule |

### CI Workflow (.github/workflows/ci.yml)

The main CI workflow runs on every push to `main` and on all pull requests.

**Jobs:**

1. **shellcheck** - Lint shell scripts
2. **lint** - Code quality checks (black, isort, flake8, mypy)
3. **security** - Security scanning (bandit, safety)
4. **test** - Unit tests (Python 3.11, 3.12)
5. **smoke** - Smoke tests (core imports)

**Quality Gate:** All jobs must pass for merge to be allowed.

### Viewing Workflow Results

1. Navigate to the **Actions** tab in GitHub
2. Select the workflow run
3. View job logs and results

### Troubleshooting Failed Workflows

1. **Check logs:** Click on the failed job for detailed logs
2. **Reproduce locally:** Run `bin/run-tests.sh` to reproduce failures
3. **Fix issues:** Address errors locally
4. **Push fix:** Commit and push fixes to trigger new run

---

## Test Runner Script

### Overview

The `bin/run-tests.sh` script provides a unified interface for running tests, linting, and validation locally.

### Usage

```bash
# Run unit tests
bin/run-tests.sh unit

# Run integration tests
bin/run-tests.sh integration

# Run all tests
bin/run-tests.sh all

# Run linting only
bin/run-tests.sh lint

# Validate YAML files
bin/run-tests.sh yaml

# Run full quality gate
bin/run-tests.sh quality-gate

# Show help
bin/run-tests.sh help
```

### Options

| Option | Description |
|--------|-------------|
| `--fast-only` | Run only fast tests (skip slow/integration tests) |
| `--cov` | Run with coverage report |
| `--verbose` | Enable verbose output |

### Examples

```bash
# Run fast unit tests only
bin/run-tests.sh unit --fast-only

# Run all tests with coverage
bin/run-tests.sh all --cov

# Run quality gate
bin/run-tests.sh quality-gate
```

### Test Structure

```
2-engine/tests/
├── unit/                    # Unit tests (fast, no external deps)
│   ├── test_agent_coordination.py
│   ├── test_agent_output_bus.py
│   ├── test_error_handling.py
│   └── test_managerial_agent.py
└── integration/             # Integration tests (slower, external deps)
```

### Running Tests Manually (pytest)

```bash
# Run unit tests directly
pytest 2-engine/tests/unit/ -v

# Run with coverage
pytest 2-engine/tests/unit/ -v --cov=2-engine --cov-report=term

# Run specific test file
pytest 2-engine/tests/unit/test_agent_coordination.py -v

# Run specific test
pytest 2-engine/tests/unit/test_agent_coordination.py::test_function_name -v
```

---

## Quality Gates

### What Are Quality Gates?

Quality gates are automated checks that **block** certain actions if criteria are not met. BlackBox5 has two levels of quality gates:

1. **Pre-commit quality gate:** Blocks commits if fast checks fail
2. **GitHub Actions quality gate:** Blocks merges if CI fails

### Quality Gate Rules

| Gate | Rule | Enforcement |
|------|------|-------------|
| **Pre-commit** | All hooks must pass | Blocks `git commit` |
| **CI** | All jobs must pass | Blocks merge to main |
| **Tests** | 100% pass rate required | Blocks commit/merge |
| **Linting** | No critical errors | Blocks commit/merge |
| **YAML** | No validation errors | Blocks commit/merge |

### Bypassing Quality Gates

**Pre-commit bypass** (NOT RECOMMENDED):
```bash
git commit --no-verify -m "Commit message"
```

**CI bypass** (NOT RECOMMENDED):
- Disable branch protection rules in GitHub repository settings
- **WARNING:** This disables quality gate enforcement for all contributors

### Quality Gate Status

Check quality gate status:

```bash
# Run quality gate locally
bin/run-tests.sh quality-gate

# Check quality gate report
cat operations/quality-gate-report.yaml

# Check events.yaml for recent quality gate runs
cat .autonomous/communications/events.yaml | grep -A 10 "type: quality_gate"
```

---

## Quality Gate Report

### Overview

The `operations/quality-gate-report.yaml` file tracks quality metrics over time, including:

- Test pass rates (last 10 runs)
- Linting error trends
- YAML validation failures
- Average test duration
- Overall system health

### Report Structure

```yaml
quality_gate_report:
  last_updated: "2026-02-01T12:00:00Z"
  summary:
    total_runs: 50
    passed_runs: 48
    failed_runs: 2
    pass_rate: 96.0
  recent_runs: [...]  # Last 10 runs
  trends:
    test_pass_rate_last_10: 98.5
    linting_errors_last_10: 1
    validation_failures_last_10: 0
    avg_test_duration_last_10: 45.2
  status:
    overall_health: "excellent"  # excellent | good | warning | critical
    last_quality_gate: "passed"
    blocked_commits: 5
    blocked_merges: 2
  components:
    unit_tests:
      status: "passed"
      pass_rate: 100.0
      last_run: "2026-02-01T12:00:00Z"
    linting:
      status: "passed"
      errors_last_run: 0
      last_run: "2026-02-01T12:00:00Z"
    yaml_validation:
      status: "passed"
      errors_last_run: 0
      last_run: "2026-02-01T12:00:00Z"
```

### Updating the Report

The report is automatically updated by:

1. **Task completion:** `quality_gate.py` called from task workflow
2. **Manual run:** `python 2-engine/.autonomous/lib/quality_gate.py run <task_id> <agent> <run_number> <project_dir>`

### Health Status Levels

| Level | Pass Rate | Description |
|-------|-----------|-------------|
| **excellent** | ≥ 95% | All systems healthy |
| **good** | ≥ 80% | Minor issues, acceptable |
| **warning** | ≥ 50% | Degraded quality, investigate |
| **critical** | < 50% | Serious issues, immediate action |

---

## Integration with Task Completion

### Overview

Quality gates are integrated with the RALF task completion workflow. When a task completes, tests are automatically run and results are tracked.

### Integration Points

1. **roadmap_sync.py:** Calls `quality_gate.py` after task completion
2. **quality_gate.py:** Runs tests, updates report, writes to events.yaml
3. **events.yaml:** Records quality gate results
4. **quality-gate-report.yaml:** Tracks metrics over time

### Manual Quality Gate Run

```bash
# From project root
python 2-engine/.autonomous/lib/quality_gate.py \
    run TASK-001 executor 56 \
    /workspaces/blackbox5/5-project-memory/blackbox5 \
    abc123
```

### Programmatic Usage

```python
from quality_gate import record_quality_gate_result

result = record_quality_gate_result(
    task_id="TASK-001",
    agent="executor",
    run_number=56,
    project_dir="/path/to/blackbox5",
    commit_hash="abc123",
    run_tests=True
)

if result["success"]:
    print("Quality gate passed")
else:
    print("Quality gate failed")
```

---

## Troubleshooting

### Pre-Commit Hooks Fail

**Problem:** Pre-commit hooks fail on commit

**Solutions:**

1. **Check what failed:**
   ```bash
   pre-commit run --all-files
   ```

2. **Fix formatting issues:**
   ```bash
   black .
   isort .
   ```

3. **Fix linting issues:**
   ```bash
   flake8 . --fix
   ```

4. **Fix YAML issues:**
   ```bash
   yamllint -c .yamllint .
   ```

5. **Re-run hooks:**
   ```bash
   pre-commit run --all-files
   ```

### Tests Fail Locally

**Problem:** `bin/run-tests.sh` fails

**Solutions:**

1. **Run with verbose output:**
   ```bash
   bin/run-tests.sh unit --verbose
   ```

2. **Run specific test:**
   ```bash
   pytest 2-engine/tests/unit/test_file.py::test_function -v
   ```

3. **Check Python version:**
   ```bash
   python --version  # Should be 3.11 or 3.12
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```

### CI Workflow Fails on GitHub

**Problem:** GitHub Actions CI workflow fails

**Solutions:**

1. **Check workflow logs:**
   - Go to Actions tab in GitHub
   - Click on failed workflow run
   - Click on failed job
   - Read logs

2. **Reproduce locally:**
   ```bash
   bin/run-tests.sh quality-gate
   ```

3. **Check for environment differences:**
   - Python version
   - Dependency versions
   - Environment variables

4. **Fix and push:**
   ```bash
   git add .
   git commit -m "Fix CI failure"
   git push origin main
   ```

### Quality Gate Blocks Merge

**Problem:** Quality gate failing, blocking merge

**Solutions:**

1. **Check quality gate status:**
   ```bash
   cat operations/quality-gate-report.yaml
   ```

2. **Check recent events:**
   ```bash
   cat .autonomous/communications/events.yaml | grep -A 10 "type: quality_gate"
   ```

3. **Fix failing components:**
   - Run `bin/run-tests.sh quality-gate`
   - Fix failures
   - Commit and push fixes

4. **Verify fix:**
   - Wait for CI to run on push
   - Check CI status in Actions tab
   - Merge when CI passes

### Flaky Tests

**Problem:** Tests pass sometimes, fail other times

**Solutions:**

1. **Identify flaky test:**
   ```bash
   # Run test multiple times
   for i in {1..10}; do pytest test_file.py::test_function; done
   ```

2. **Add retry logic (temporary workaround):**
   ```python
   @pytest.mark.flaky(reruns=3)
   def test_flaky_function():
       # test code
   ```

3. **Fix root cause:**
   - Add proper cleanup/teardown
   - Remove dependency on external state
   - Add proper mocks/stubs

4. **Disable test if unfixable:**
   ```python
   @pytest.mark.skip(reason="Flaky test, TODO: fix")
   def test_flaky_function():
       # test code
   ```

---

## Best Practices

### Writing Tests

1. **Keep tests fast:** Unit tests should run in < 5 seconds
2. **Test behavior, not implementation:** Focus on what code does, not how
3. **Use descriptive names:** `test_user_login_fails_with_invalid_credentials`
4. **One assertion per test:** Tests should fail for one reason only
5. **Use fixtures:** Share test setup code with pytest fixtures

### Test Structure

```python
# Good test
def test_user_login_success(client, valid_user):
    """Test that user can login with valid credentials"""
    response = client.post("/login", json={
        "username": valid_user.username,
        "password": valid_user.password
    })

    assert response.status_code == 200
    assert "token" in response.json

# Bad test (too many assertions)
def test_user_login_and_profile_and_settings(client, valid_user):
    """Tests too many things"""
    # ... 50 lines of assertions
```

### Keeping Tests Fast

1. **Mock external dependencies:** Don't make real API calls in tests
2. **Use fixtures:** Share setup code, don't repeat
3. **Parallelize:** Use `pytest-xdist` to run tests in parallel
4. **Skip slow tests:** Mark integration tests as `@pytest.mark.slow`

### Code Quality

1. **Run black before committing:** `black .`
2. **Run isort before committing:** `isort .`
3. **Fix flake8 errors:** `flake8 . --fix`
4. **Run pre-commit:** `pre-commit run --all-files`

### CI/CD Workflow

1. **Keep workflows fast:** Optimize job execution time
2. **Use caching:** Cache dependencies in GitHub Actions
3. **Parallelize jobs:** Run independent jobs concurrently
4. **Fail fast:** Exit early on critical failures

### Quality Gates

1. **Don't bypass:** Avoid `git commit --no-verify`
2. **Fix failures promptly:** Don't let broken code sit
3. **Monitor trends:** Watch quality-gate-report.yaml for degradation
4. **Investigate failures:** Understand root cause, don't just patch

---

## Appendix

### Files Reference

| File | Purpose |
|------|---------|
| `.pre-commit-config.yaml` | Pre-commit hooks configuration |
| `.github/workflows/ci.yml` | Main CI workflow |
| `.github/workflows/test.yml` | Test suite workflow |
| `bin/run-tests.sh` | Unified test runner |
| `2-engine/.autonomous/lib/quality_gate.py` | Quality gate library |
| `operations/quality-gate-report.yaml` | Quality metrics tracking |
| `.autonomous/communications/events.yaml` | Event log |

### Commands Reference

```bash
# Pre-commit
pre-commit install                          # Install hooks
pre-commit run --all-files                  # Run all hooks
pre-commit autoupdate                       # Update hooks

# Tests
bin/run-tests.sh unit                       # Run unit tests
bin/run-tests.sh quality-gate               # Run quality gate
pytest 2-engine/tests/unit/ -v              # Run pytest directly

# Quality gate
python 2-engine/.autonomous/lib/quality_gate.py run TASK-001 executor 56 /path/to/project

# Reports
cat operations/quality-gate-report.yaml     # View quality report
cat .autonomous/communications/events.yaml  # View events
```

### Further Reading

- [pytest Documentation](https://docs.pytest.org/)
- [pre-commit Documentation](https://pre-commit.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Black Code Formatter](https://black.readthedocs.io/)

---

**End of CI/CD Pipeline Guide**

For questions or issues, refer to the troubleshooting section or check the events.yaml for recent quality gate runs.
