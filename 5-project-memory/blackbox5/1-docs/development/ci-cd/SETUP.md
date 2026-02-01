# CI/CD Setup Guide

## Quick Start

The CI/CD pipeline is already configured. Here's how to verify it's working:

### 1. Verify Workflows Exist

```bash
ls -la ~/.blackbox5/.github/workflows/
```

You should see:
- `ci.yml`
- `test.yml`
- `docs.yml`
- `pr-checks.yml`
- `scheduled.yml`

### 2. Push to GitHub

```bash
cd ~/.blackbox5
git add .github/
git commit -m "ci: Add GitHub Actions workflows

- Add CI pipeline for code quality and testing
- Add test suite for comprehensive validation
- Add documentation workflow for MkDocs
- Add PR checks for standards enforcement
- Add scheduled tasks for maintenance
- Add Dependabot configuration

Co-authored-by: Claude <claude@blackbox5.local>"
git push origin main
```

### 3. Verify in GitHub

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. You should see the workflows listed
4. Push a test commit to trigger CI

## What Happens Next

### On Every Push to Main
- CI workflow runs (lint, security, unit tests)
- If docs changed, Documentation workflow runs

### On Every Pull Request
- CI workflow runs
- PR Checks workflow runs
- Results appear in the PR as status checks

### Daily
- Scheduled workflow runs dependency checks
- Stale issues are marked

### Weekly
- Dependabot creates PRs for outdated dependencies

## Customization

### Adding a New Check

1. Edit the appropriate workflow in `.github/workflows/`
2. Add a new job or step
3. Test with `act` locally (see below) or push to a branch

### Skipping CI

Add `[skip ci]` or `[ci skip]` to commit message:
```bash
git commit -m "docs: Update README [skip ci]"
```

### Running Workflows Manually

1. Go to GitHub → Actions
2. Select a workflow
3. Click "Run workflow"
4. Choose branch and options

## Local Testing with Act

Install `act` to test workflows locally:

```bash
# macOS
brew install act

# Run default workflow (CI)
cd ~/.blackbox5
act

# Run specific workflow
act -W .github/workflows/test.yml

# Run with verbose output
act -v
```

Note: Some features (like service containers) may not work locally.

## Required Secrets (Optional)

These workflows work without secrets, but you can add:

| Secret | Purpose | Workflow |
|--------|---------|----------|
| `CODECOV_TOKEN` | Upload coverage reports | ci.yml |
| `GITHUB_TOKEN` | Auto-generated, no setup needed | All |

To add a secret:
1. GitHub → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add name and value

## Branch Protection (Recommended)

To enforce CI passes before merging:

1. GitHub → Settings → Branches
2. Click "Add rule" on `main`
3. Enable:
   - "Require a pull request before merging"
   - "Require status checks to pass"
   - Add checks: `lint`, `test`, `security`
4. Click "Create"

## Monitoring

### View Workflow Status

```bash
# Using GitHub CLI
gh run list
gh run view <run-id>
```

### Notifications

GitHub sends notifications for:
- Failed workflows on your commits
- Workflow runs on your PRs

Configure in GitHub → Settings → Notifications

## Cost Monitoring

Check usage:
1. GitHub → Settings → Billing and plans
2. View "Actions" usage

Free tier: 2,000 minutes/month (private repos)

## Troubleshooting Checklist

- [ ] YAML syntax valid (use online validator or `yamllint`)
- [ ] File in correct location (`.github/workflows/`)
- [ ] Workflow has valid `on:` trigger
- [ ] Job has valid `runs-on:`
- [ ] Steps use correct action versions
- [ ] Repository has Actions enabled (Settings → Actions)

## Next Steps

1. Push the workflows to GitHub
2. Verify they appear in the Actions tab
3. Create a test PR to see checks in action
4. Configure branch protection rules
5. Add status badges to README (optional)
