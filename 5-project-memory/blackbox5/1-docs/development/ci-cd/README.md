# BlackBox5 CI/CD Pipeline

## Overview

This directory contains GitHub Actions workflows that automate code quality checks, testing, documentation builds, and maintenance tasks for BlackBox5.

## Workflows

### 1. CI (`ci.yml`)
**Trigger:** Every push to main and every pull request

**What it does:**
- **Code Quality**: Runs black, isort, flake8, and mypy
- **Security Scanning**: Runs bandit (code security) and safety (dependency vulnerabilities)
- **Unit Tests**: Runs pytest on unit tests with coverage reporting
- **Smoke Tests**: Verifies core imports work

**Purpose:** Fast feedback on code quality and basic functionality.

### 2. Test Suite (`test.yml`)
**Trigger:** Manual dispatch, daily schedule, or PRs labeled `run-tests` / `run-integration-tests`

**What it does:**
- **Unit Tests**: Comprehensive unit test run
- **Integration Tests**: Tests requiring Redis (and optionally Neo4j/ChromaDB)
- **Safety Tests**: Validates kill switch and constitutional classifier
- **Orchestration Tests**: Tests multi-agent orchestration logic

**Purpose:** Thorough validation before releases or when explicitly requested.

### 3. Documentation (`docs.yml`)
**Trigger:** Push to main affecting docs, or manual dispatch

**What it does:**
- Builds MkDocs documentation
- Regenerates skill catalog (`CATALOG.md`)
- Deploys to GitHub Pages

**Purpose:** Keep documentation and skill catalog up to date.

### 4. PR Checks (`pr-checks.yml`)
**Trigger:** Every pull request

**What it does:**
- Validates PR title follows conventional commits format
- Checks for oversized files (>1MB)
- Quick smoke tests (YAML validation, Python syntax)

**Purpose:** Enforce standards and catch obvious issues early.

### 5. Scheduled Tasks (`scheduled.yml`)
**Trigger:** Daily at 3 AM UTC, or manual dispatch

**What it does:**
- Checks for outdated dependencies
- Validates `STATE.yaml` format
- Marks stale issues/PRs

**Purpose:** Maintenance and housekeeping.

## Configuration Files

### Dependabot (`dependabot.yml`)
Automatically creates PRs to update:
- Python dependencies (weekly)
- GitHub Actions (weekly)

## Usage

### For Developers

1. **Before submitting a PR:**
   ```bash
   # Run the same checks locally
   black --check .
   isort --check-only .
   flake8 .
   mypy .
   pytest 2-engine/tests/unit/
   ```

2. **If CI fails on your PR:**
   - Click "Details" next to the failed check
   - Read the error message
   - Fix locally and push again

3. **To run integration tests on a PR:**
   - Add label `run-integration-tests` to the PR
   - Or go to Actions → Test Suite → Run workflow

### For Maintainers

1. **View all workflows:**
   - Go to GitHub → Actions tab
   - See history of all runs

2. **Manual triggers:**
   - Most workflows support `workflow_dispatch`
   - Go to Actions → Select workflow → Run workflow

3. **Required checks:**
   - Configure in Settings → Branches → Branch protection rules
   - Recommended: Require "Unit Tests" and "Code Quality" to pass

## Cost

All workflows run on **GitHub-hosted runners** (free tier):
- 2,000 minutes/month for private repos
- Unlimited for public repos

Current estimated usage:
- CI workflow: ~3 minutes per run
- Test Suite: ~5-10 minutes per run
- Documentation: ~2 minutes per run

With average 10 PRs/day: ~900 minutes/month (well within free tier)

## Troubleshooting

### Common Issues

**"Module not found" in tests:**
- Check `requirements-dev.txt` includes the dependency
- Workflow uses `pip install -r requirements-dev.txt`

**Black formatting fails:**
- Run `black .` locally to auto-format
- Or configure IDE to format on save

**Integration tests fail:**
- Check if Redis service is running in workflow
- Some tests require actual services (marked with `integration`)

**Workflow not triggering:**
- Check YAML syntax is valid
- Verify file is in `.github/workflows/`
- Check branch name matches (main vs master)

### Getting Help

1. Check workflow logs in GitHub Actions tab
2. Review this documentation
3. See GitHub's [Actions documentation](https://docs.github.com/en/actions)

## Future Improvements

- [ ] Add Neo4j service for graph database tests
- [ ] Add ChromaDB service for vector store tests
- [ ] Add code coverage badges to README
- [ ] Add automated release workflow
- [ ] Add Docker image builds
- [ ] Add performance regression tests
