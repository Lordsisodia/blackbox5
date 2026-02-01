# FEATURE-007: CI/CD Pipeline Integration

**Status:** active
**Priority:** high
**Type:** feature
**Estimated:** 150 minutes (~2.5 hours)

---

## User Value

**Who benefits:** RALF system (quality assurance and automated operations)

**What problem does it solve:** No automated testing or deployment pipeline exists. Quality assurance is manual and sporadic. Code commits proceed without validation, allowing bugs and regressions to reach production. Test execution is ad-hoc rather than systematic.

**What value does it create:** Automated testing, deployment triggers, and quality gates integrated with RALF task completion workflow. Ensures code quality before commits, prevents bad code from reaching main branch, and provides continuous feedback on system health.

**Example:**
- Who: BlackBox5 RALF system (automated quality assurance)
- Problem: Executor completes tasks and commits code, but no validation runs before merge. Bugs introduced by feature F-005 only discovered during F-006 execution.
- Value: Pre-commit hooks catch syntax errors immediately. GitHub Actions runs full test suite on every push. Quality gates block merging if tests fail. Task completion triggers automated validation.

---

## Feature Scope

**MVP (Minimum Viable Product):**
- [ ] Pre-commit hooks enhanced with test execution (pytest, linting, YAML validation)
- [ ] Test runner script created (bin/run-tests.sh) with unit, integration, and linting commands
- [ ] GitHub Actions CI workflow created (.github/workflows/ci.yml)
- [ ] Quality gates implemented (block commits on test failure, block merges on CI failure)
- [ ] Quality gate report tracking (operations/quality-gate-report.yaml)
- [ ] Integration with task completion (tests triggered after commits, results reported to events.yaml)
- [ ] CI/CD documentation (operations/.docs/cicd-guide.md)

**Future Enhancements (out of scope for this feature):**
- [ ] GitHub Actions CD workflow (automated deployment)
- [ ] Code coverage tracking (coverage.py, Codecov)
- [ ] Performance testing integration
- [ ] Security scanning (Snyk, Dependabot)
- [ ] Multi-environment deployments (staging, production)

**Scope Boundaries:**
- **IN SCOPE:** Pre-commit hooks, GitHub Actions CI workflow, test runner script, quality gate tracking, documentation
- **OUT OF SCOPE:** Automated deployment (CD), code coverage tools, security scanning, performance testing

---

## Context & Background

**Why this feature matters:**
- As RALF ships more features, manual QA doesn't scale
- Automated testing ensures code quality before commits reach main
- Quality gates prevent bad code from breaking the system
- Continuous feedback enables rapid iteration and confidence in changes
- CI/CD is foundational infrastructure for sustainable feature delivery

**Related Features:**
- Previous: TASK-1769916004 (Feature Framework) - Provides task completion workflow
- Previous: TASK-1769952151 (F-005 Automated Documentation) - Feature delivery validated
- Previous: TASK-1769952152 (F-006 User Preferences) - Feature delivery validated
- Current: F-007 enables automated quality assurance for all future features

**Current State:**
- No automated testing before commits
- No CI/CD pipeline (no GitHub Actions workflows)
- Manual quality assurance (ad-hoc, inconsistent)
- No quality gate tracking or reporting
- Test execution must be triggered manually (if tests exist at all)

**Desired State:**
- Pre-commit hooks catch errors before commit
- GitHub Actions runs full test suite on every push
- Quality gates block bad commits from reaching main
- Quality gate status tracked and reported
- CI/CD pipeline documented and operational

---

## Success Criteria

### Must-Have (Required for completion)
- [ ] Pre-commit hooks enhanced - test execution, linting, YAML validation added to .pre-commit-config.yaml
- [ ] Test runner script created - bin/run-tests.sh with run_unit_tests(), run_integration_tests(), run_linting(), validate_yaml()
- [ ] GitHub Actions CI workflow created - .github/workflows/ci.yml with lint, test, validate jobs
- [ ] Quality gates implemented - pre-commit blocks bad commits, GitHub Actions blocks failed merges
- [ ] Quality gate tracking - operations/quality-gate-report.yaml tracks pass rates and failures
- [ ] Task completion integration - roadmap_sync.py triggers tests after commit, reports to events.yaml
- [ ] CI/CD documentation - operations/.docs/cicd-guide.md covers setup, usage, troubleshooting

### Should-Have (Important but not blocking)
- [ ] Existing tests discovered and cataloged - test inventory created
- [ ] Test execution is fast - unit tests < 5 seconds, full suite < 30 seconds
- [ ] Quality gate dashboard - readable report format for tracking trends
- [ ] Error handling - graceful failure when tests don't exist or infrastructure unavailable

### Nice-to-Have (If time permits)
- [ ] GitHub Actions CD workflow skeleton - .github/workflows/cd.yml (manual trigger)
- [ ] Test result artifacts - GitHub Actions uploads test reports
- [ ] Quality gate notifications - status posted to chat-log.yaml on failure

### Verification Method
- [ ] Manual testing: Intentionally fail a test, verify pre-commit blocks commit
- [ ] Integration testing: Complete a task, verify tests run and results reported
- [ ] CI testing: Push to branch, verify GitHub Actions workflow triggers
- [ ] Documentation review: cicd-guide.md covers all setup and usage scenarios

---

## Technical Approach

### Architecture Overview

```
┌─────────────────┐
│  Task Complete  │
│  (Executor)     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│  1. Pre-Commit Hooks             │
│     - Lint Python files          │
│     - Validate YAML              │
│     - Run pytest (modified)      │
│     - Block commit on failure    │
└────────┬────────────────────────┘
         │ (commit allowed)
         ▼
┌─────────────────────────────────┐
│  2. Git Commit                   │
│     - Code committed to branch   │
│     - roadmap_sync.py triggered  │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  3. Task Completion Integration  │
│     - roadmap_sync.py calls      │
│       run_tests.sh               │
│     - Results written to         │
│       events.yaml                │
│     - Quality gate report        │
│       updated                    │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  4. Git Push                     │
│     - Push to remote branch      │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  5. GitHub Actions CI            │
│     - Lint job runs              │
│     - Test job runs              │
│     - Validate job runs          │
│     - Quality gate: Block merge  │
│       if any job fails           │
└─────────────────────────────────┘
```

### Phase 1: Feature Specification (15 min)
- Create FEATURE-007-cicd-integration.md (this file)
- Document MVP scope, success criteria, technical approach
- Define rollout plan (pre-commit → GitHub Actions)

### Phase 2: Existing Test Analysis (15 min)
- Search for test files (test_*.py, *_test.py, tests/)
- Check for existing GitHub Actions workflows (.github/workflows/)
- Review pre-commit config (.pre-commit-config.yaml)
- Identify test frameworks (pytest, unittest, bash)
- Catalog test coverage gaps

### Phase 3: Pre-Commit Hook Integration (30 min)
- **Enhance .pre-commit-config.yaml:**
  - Add flake8 hook (Python linting)
  - Add black hook (Python formatting)
  - Add yamllint hook (YAML validation)
  - Add pytest hook (run tests for modified files)
- **Create bin/run-tests.sh:**
  - run_unit_tests() - Execute pytest
  - run_integration_tests() - Run integration tests
  - run_linting() - Run flake8, black --check
  - validate_yaml() - Validate YAML files
  - run_all() - Execute all checks

### Phase 4: GitHub Actions Workflow (40 min)
- **Create .github/workflows/ci.yml:**
  - Triggers: push to main, pull requests, manual
  - Jobs:
    - lint: flake8, black, markdownlint
    - test: pytest, integration tests
    - validate: yamllint, schema validation
  - Quality gate: Require all jobs pass for merge
- **Create .github/workflows/cd.yml (optional skeleton):**
  - Triggers: manual workflow_dispatch
  - Jobs: build, deploy (placeholder)

### Phase 5: Quality Gates (30 min)
- **Implement pre-commit quality gate:**
  - Pre-commit blocks commit if tests fail
  - Skip option available (--no-verify)
- **Implement GitHub Actions quality gate:**
  - Branch protection rule (require CI checks)
  - Block merge if CI fails
- **Create quality gate report:**
  - File: operations/quality-gate-report.yaml
  - Track: test pass rate, linting errors, validation failures
  - Report last 10 runs, trends

### Phase 6: Integration with Task Completion (15 min)
- **Modify 2-engine/.autonomous/lib/roadmap_sync.py:**
  - After commit, call bin/run-tests.sh
  - Capture test results
  - Write results to events.yaml
  - Update quality-gate-report.yaml

### Phase 7: Documentation (5 min)
- **Create operations/.docs/cicd-guide.md:**
  - Overview (CI/CD pipeline, benefits)
  - Pre-commit hooks (setup, usage, bypass)
  - GitHub Actions (workflows, triggers, jobs)
  - Quality gates (rules, enforcement, monitoring)
  - Troubleshooting (test failures, pipeline issues)
  - Best practices (fast tests, fix failures promptly)

---

## Implementation Details

### File 1: .pre-commit-config.yaml (Enhance)

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.9

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=100]

  - repo: https://github.com/adrienverge/yamllint
    rev: v1.33.0
    hooks:
      - id: yamllint
        args: [-d, {extends: default, rules: {line-length: {max: 120}}}]

  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: bin/run-tests.sh unit
        language: script
        pass_filenames: false
        always_run: true
```

### File 2: bin/run-tests.sh (Create)

```bash
#!/bin/bash
# Test runner script for RALF CI/CD pipeline

run_unit_tests() {
    echo "Running unit tests..."
    pytest tests/unit/ -v --tb=short
}

run_integration_tests() {
    echo "Running integration tests..."
    pytest tests/integration/ -v --tb=short
}

run_linting() {
    echo "Running linting..."
    flake8 2-engine/ --max-line-length=100
    black --check 2-engine/
}

validate_yaml() {
    echo "Validating YAML files..."
    yamllint -c .yamllint .
}

run_all() {
    run_unit_tests && run_integration_tests && run_linting && validate_yaml
}

case "$1" in
    unit) run_unit_tests ;;
    integration) run_integration_tests ;;
    lint) run_linting ;;
    yaml) validate_yaml ;;
    *) run_all ;;
esac
```

### File 3: .github/workflows/ci.yml (Create)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install flake8 black yamllint
      - name: Run linting
        run: |
          flake8 2-engine/ --max-line-length=100
          black --check 2-engine/
          yamllint -c .yamllint .

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install pytest
      - name: Run tests
        run: |
          bin/run-tests.sh

  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate YAML
        run: |
          pip install yamllint
          yamllint -c .yamllint .
```

### File 4: operations/quality-gate-report.yaml (Create)

```yaml
quality_gate_report:
  last_updated: "2026-02-01T00:00:00Z"

  summary:
    total_runs: 0
    passed_runs: 0
    failed_runs: 0
    pass_rate: 0.0

  recent_runs: []

  trends:
    test_pass_rate_last_10: 0.0
    linting_errors_last_10: 0
    validation_failures_last_10: 0
```

### File 5: operations/.docs/cicd-guide.md (Create)

Comprehensive guide covering:
- Overview of CI/CD pipeline
- Pre-commit hook setup and usage
- GitHub Actions workflows
- Quality gate enforcement
- Troubleshooting common issues
- Best practices for test development

---

## Rollout Plan

### Phase 1: Pre-Commit Hooks (Day 1)
- Enhance .pre-commit-config.yaml
- Create bin/run-tests.sh
- Document pre-commit setup
- Validate pre-commit hooks work

### Phase 2: GitHub Actions (Day 1)
- Create .github/workflows/ci.yml
- Push to test CI workflow
- Validate CI runs on push
- Test quality gate (attempt merge with failed tests)

### Phase 3: Integration (Day 1)
- Modify roadmap_sync.py
- Test task completion integration
- Validate quality gate report updates
- Update documentation

### Phase 4: Documentation (Day 1)
- Create cicd-guide.md
- Review and validate documentation
- Final testing of complete pipeline

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Slow tests block development | Medium | High | Keep unit tests fast (<5 sec), integration tests separate |
| Flaky tests erode confidence | Medium | High | Fix or disable flaky tests immediately |
| Pipeline breaks halt progress | Low | High | Monitor pipeline health, quick fix turnaround |
| Pre-commit hooks bypassed | High | Low | Document bypass (--no-verify), educate on risks |
| GitHub Actions quota exceeded | Low | Medium | Monitor usage, optimize workflow execution time |

---

## Dependencies

**Required (blocking):**
- None (all prerequisites are infrastructure already in place)

**Optional (nice-to-have):**
- Existing test files (tests/unit/, tests/integration/)
- Existing GitHub Actions workflows
- Existing pre-commit config

---

## Success Metrics

- [ ] Pre-commit hooks execute on every commit attempt
- [ ] GitHub Actions CI runs on every push to main
- [ ] Quality gates block merges when tests fail
- [ ] Quality gate report tracks test results over time
- [ ] Task completion triggers automated tests
- [ ] Documentation enables operators to troubleshoot CI/CD issues

---

## Notes

**Testing Strategy:**
- Intentionally write bad code (syntax error) - verify pre-commit blocks commit
- Push to feature branch - verify GitHub Actions triggers
- Fail a test - verify quality gate blocks merge
- Complete a task - verify tests run automatically

**Best Practices:**
- Keep unit tests fast (<5 seconds)
- Fix flaky tests immediately
- Monitor pipeline health
- Document test requirements
- Use test fixtures and mocks

**Troubleshooting:**
- Pre-commit hook bypass: git commit --no-verify (use sparingly)
- GitHub Actions failure: Check Actions tab for logs
- Test failures: Run bin/run-tests.sh locally to debug
- YAML validation errors: Check yamllint config

---

**Feature Status:** Active (Implementation in progress)
**Last Updated:** 2026-02-01
**Next Milestone:** Complete Phase 2 (Existing Test Analysis)
