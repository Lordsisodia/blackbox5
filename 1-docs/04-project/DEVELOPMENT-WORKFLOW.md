# BlackBox5 Development Workflow

This guide describes the complete development workflow for BlackBox5, including task management, GitHub integration, and autonomous agent operations.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Task Lifecycle](#task-lifecycle)
- [Branching Strategy](#branching-strategy)
- [Commit Convention](#commit-convention)
- [PR Workflow](#pr-workflow)
- [Testing Requirements](#testing-requirements)
- [Documentation Standards](#documentation-standards)
- [Autonomous Operations](#autonomous-operations)

## Overview

BlackBox5 uses a fully integrated development workflow where:

1. **Tasks** are managed in the local task system (`5-project-memory/`)
2. **GitHub Issues** automatically sync with tasks
3. **Agents** work autonomously on feature branches
4. **PRs** are created automatically by agents
5. **CI/CD** runs tests and checks automatically
6. **Documentation** is auto-generated from code

## Quick Start

### For Human Developers

```bash
# 1. Create a task (or let an agent create one)
bb5 task:create "Implement new feature"

# 2. Task automatically appears as GitHub Issue

# 3. Create feature branch
git checkout -b feature/feature-name

# 4. Make changes and commit
git add .
git commit -m "feat: implement new feature"

# 5. Push and create PR
git push origin feature/feature-name
gh pr create --title "Task #123: Implement new feature" --body "Closes #123"

# 6. Wait for CI checks, then merge
```

### For Autonomous Agents

Agents can run autonomously:

```bash
# Agent creates task automatically
# Agent works on task
# Agent commits changes
# Agent triggers automated PR creation
gh workflow run agent-pr.yml \
  -f agent_name="agent-name" \
  -f branch_name="feature/feature-name" \
  -f pr_title="Task #123: Implement feature"
```

## Task Lifecycle

```
┌─────────────┐
│   Created   │ Task created in 5-project-memory/
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Planned   │ Task synced to GitHub Issue
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ In Progress │ Issue moves to "In Progress" column
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Review    │ PR created, issue moves to "Review"
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Done      │ PR merged, issue closed, moves to "Done"
└─────────────┘
```

### Task States

| State | Label | Project Column | Description |
|-------|-------|----------------|-------------|
| created | 📝 Planning | Planning | Task created, not started |
| in_progress | 🔄 In Progress | In Progress | Agent/human working on task |
| review | 🔍 Review | Review | PR created, awaiting review |
| complete | ✅ Done | Done | Task completed and merged |
| failed | ❌ Failed | Backlog | Task failed to complete |

## Branching Strategy

### Branch Types

| Branch Type | Format | Purpose | Example |
|-------------|--------|---------|---------|
| Feature | `feature/short-desc` | New feature | `feature/user-auth` |
| Bugfix | `bugfix/description` | Bug fix | `bugfix/login-error` |
| Hotfix | `hotfix/critical-fix` | Urgent fix | `hotfix/security-patch` |
| Task | `task/ID-description` | Specific task | `task/123-add-endpoint` |
| Refactor | `refactor/component` | Code cleanup | `refactor/api-client` |

### Rules

1. **Main Branch Protection**
   - `main` is protected
   - PRs required for all changes
   - CI checks must pass
   - At least 1 approval required

2. **Branch Cleanup**
   - Delete merged branches
   - Archive stale feature branches

3. **Branch Naming**
   - Use kebab-case
   - Keep names concise
   - Include task ID when relevant

## Commit Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>[optional scope]: <subject>

[optional body]

[optional footer(s)]
```

### Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat: add user authentication` |
| `fix` | Bug fix | `fix: resolve login timeout` |
| `docs` | Documentation | `docs: update API reference` |
| `style` | Code style | `style: format code with black` |
| `refactor` | Refactoring | `refactor: simplify auth flow` |
| `test` | Tests | `test: add unit tests for auth` |
| `chore` | Maintenance | `chore: update dependencies` |
| `perf` | Performance | `perf: optimize database queries` |
| `ci` | CI/CD | `ci: add automated tests` |

### Examples

```
feat(auth): add OAuth2 login support

Implement OAuth2 authentication flow with Google and GitHub providers.

- Add OAuth2 configuration
- Implement token exchange
- Update user model

Closes #123
```

```
fix(api): resolve timeout on large requests

Increase timeout to handle large payloads and add retry logic.

Fixes #456
```

## PR Workflow

### PR Title Format

```
Task #<id>: <short description>
<type>: <description>
```

Examples:
- `Task #123: Add user authentication`
- `fix: Resolve login timeout error`
- `feat: Implement OAuth2 flow`

### PR Template

PRs should include:

```markdown
## Description
<Describe changes>

## Related Issue
Closes #123

## Changes
- <Change 1>
- <Change 2>

## Testing
- <Tests added>
- <Manual testing steps>

## Checklist
- [ ] Tests pass
- [ ] Code formatted
- [ ] Documentation updated
- [ ] No new warnings
```

### PR Review Process

1. **Automated Checks**
   - CI tests pass
   - Linting passes
   - Security scan passes

2. **Code Review**
   - At least 1 approval required
   - Reviewer comments addressed
   - No unresolved conversations

3. **Merge**
   - Squash merge preferred
   - Commit message auto-generated
   - Branch deleted after merge

## Testing Requirements

### Test Coverage

- Unit tests: >80% coverage for critical paths
- Integration tests: Key workflows
- Smoke tests: Core functionality

### Test Structure

```
2-engine/tests/
├── unit/           # Fast, isolated tests
├── integration/    # Service integration tests
├── functional/     # End-to-end tests
└── fixtures/       # Test data
```

### Running Tests

```bash
# Run all tests
pytest

# Run unit tests only
pytest 2-engine/tests/unit/ -m unit

# Run specific test
pytest 2-engine/tests/unit/test_agent.py::test_create

# Run with coverage
pytest --cov=2-engine --cov-report=html
```

### Test Labels

```python
@pytest.mark.unit
def test_unit_test():
    pass

@pytest.mark.integration
def test_integration_test():
    pass

@pytest.mark.slow
def test_slow_test():
    pass
```

## Documentation Standards

### Code Documentation

```python
def process_user(user_id: int, action: str) -> dict:
    """
    Process a user action.

    Args:
        user_id: The user's unique identifier
        action: The action to perform

    Returns:
        A dictionary with result and status

    Raises:
        ValueError: If user_id is invalid
        PermissionError: If user lacks permissions

    Example:
        >>> process_user(123, "activate")
        {'result': 'success', 'status': 'active'}
    """
    pass
```

### Module Documentation

Each module should have:

```python
"""
Module: user_management

Description:
    This module provides user management functionality including
    user creation, authentication, and authorization.

Classes:
    UserManager: Main user management interface
    User: User data model

Functions:
    create_user: Create a new user
    authenticate_user: Authenticate a user

Dependencies:
    - database.py: Database connection
    - auth.py: Authentication utilities
"""
```

### README Structure

Each module/package should have a README:

```markdown
# Module Name

## Purpose
<Brief description>

## Installation
pip install -e .

## Usage
```python
from module import function
function()
```

## API Reference
### function_name()
Description...

## Tests
pytest tests/test_module.py

## Contributing
How to contribute...
```

## Autonomous Operations

### Agent Task Execution

Agents can work autonomously:

1. **Create Task**
   - Agent generates task definition
   - Saves to `5-project-memory/<project>/tasks/<id>/state.json`

2. **Work on Task**
   - Agent creates feature branch
   - Makes code changes
   - Runs tests locally
   - Commits changes

3. **Create PR**
   - Agent triggers `agent-pr.yml` workflow
   - PR automatically created with labels
   - CI checks run

4. **Monitor**
   - Agent monitors PR status
   - Addresses review comments
   - Merges if approved

### Agent Permissions

Configure agent permissions in GitHub:
- Give agents write access to branches
- Allow automated PR creation
- Grant permission to close issues
- Enable workflow dispatch

### Automation Safety

To prevent runaway autonomous changes:

1. **Require Review**
   - All agent PRs require human approval
   - Use branch protection rules

2. **Rate Limiting**
   - Limit PR creation frequency
   - Set maximum concurrent branches

3. **Staging**
   - Deploy to staging first
   - Require staging approval for production

4. **Rollback**
   - Keep previous commits
   - Fast rollback procedures

## Continuous Integration

### Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci.yml` | Push, PR | Run tests, linting, security |
| `test.yml` | Schedule | Full test suite |
| `docs.yml` | Push to docs | Build and deploy docs |
| `agent-pr.yml` | Manual | Create agent PRs |
| `sync-tasks.yml` | Schedule | Sync tasks to issues |
| `documentation-generator.yml` | Push | Auto-generate docs |

### CI Checks

Required checks for merge:
- ✅ Unit tests pass
- ✅ Code formatted (black)
- ✅ Linting passes (flake8)
- ✅ Type checking passes (mypy)
- ✅ Security scan passes (bandit)

Optional checks:
- ⚠️ Integration tests
- ⚠️ Performance tests

## Continuous Deployment

### Deployment Pipeline

```
┌─────────────┐
│  Push to    │ Feature branch
│  Feature    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  PR Merge   │ To main
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  CI Checks  │ Tests, linting
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Deploy to   │ Staging
│  Staging    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Staging     │ Tests, verification
│   Tests     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Deploy to   │ Production
│ Production  │
└─────────────┘
```

### Deployment Environments

| Environment | Purpose | Auto-deploy |
|-------------|---------|-------------|
| Staging | Testing, verification | Yes (on main) |
| Production | Live system | Manual approval |

### Rollback Procedure

```bash
# Identify last good deployment
gh release list

# Rollback to specific commit
git checkout <commit-hash>
git push origin main --force

# Or use GitHub rollback
gh release rollback <version>
```

## Monitoring and Observability

### Metrics

Track:
- PR merge rate
- PR lead time
- Test coverage
- CI/CD success rate
- Deployment frequency
- Failed deployments

### Dashboards

GitHub Actions provides:
- Workflow run history
- Failure rates
- Performance metrics

## Best Practices

### Do

✅ Write tests for new features
✅ Update documentation with code changes
✅ Use conventional commit messages
✅ Keep PRs small and focused
✅ Review code before merging
✅ Delete merged branches
✅ Label issues and PRs appropriately

### Don't

❌ Commit directly to main
❌ Merge failing PRs
❌ Skip tests
❌ Ignore security warnings
❌ Create massive PRs
❌ Leave comments unresolved

## Troubleshooting

### Common Issues

**CI failures:**
- Check logs: `gh run view <run-id> --log`
- Run tests locally: `pytest`
- Check formatting: `black --check .`

**Sync failures:**
- Verify GITHUB_TOKEN is set
- Check workflow logs
- Test script manually

**Merge conflicts:**
- Rebase feature branch: `git rebase main`
- Resolve conflicts
- Force push: `git push --force`

## Resources

- [GitHub Integration Guide](GITHUB-INTEGRATION.md)
- [Contributing Guidelines](../../CONTRIBUTING.md)
- [Code of Conduct](../../CODE_OF_CONDUCT.md)
- [Documentation](../README.md)

---

*Last updated: 2026-02-10*
