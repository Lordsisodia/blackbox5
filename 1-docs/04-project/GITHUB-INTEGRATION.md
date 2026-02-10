# GitHub Integration for BlackBox5

This document describes the GitHub integration setup for BlackBox5 autonomous development.

## Overview

BlackBox5 integrates with GitHub to provide:

1. **Automated PR Creation** - Agents can automatically create PRs for their changes
2. **Task Synchronization** - BlackBox5 tasks sync to GitHub Issues
3. **Project Board** - Issues automatically organized on GitHub Projects board
4. **Documentation Generation** - Auto-generated API docs and module indexes
5. **CI/CD Pipelines** - Automated testing, linting, and deployment

## Setup Guide

### 1. Repository Verification

The repository is already initialized: `git@github.com:Lordsisodia/blackbox5.git`

### 2. GitHub Personal Access Token

To enable agent actions on GitHub, you need a Personal Access Token (PAT):

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Select the following scopes:
   - `repo` (Full control of private repositories)
   - `workflow` (Update GitHub Action workflows)
   - `project` (Read and write organization and user projects)
4. Save the token securely (e.g., in `~/.secrets/github_token`)
5. Add to your environment:
   ```bash
   export GITHUB_TOKEN=$(cat ~/.secrets/github_token)
   ```

### 3. Add Token to GitHub Secrets

For GitHub Actions to work, add the token as a repository secret:

1. Go to repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `GITHUB_TOKEN` (or create a fine-grained token `AGENT_TOKEN`)
4. Value: Your PAT
5. Click "Add secret"

For project board sync, you can also add `PROJECT_TOKEN`.

### 4. Project Board Setup

Create a GitHub Project board:

1. Go to repository → Projects
2. Click "New Project"
3. Name: "BlackBox5 Development"
4. Select "Board" template
5. Create columns: "Backlog", "To Do", "In Progress", "Review", "Done"

Update the `PROJECT_NUMBER` in `bin/sync_to_project_board.py` if needed.

## Workflows

### Automated PR Creation (`agent-pr.yml`)

Agents can create PRs automatically:

```bash
gh workflow run agent-pr.yml \
  -f agent_name="claude-mac" \
  -f branch_name="feature/new-feature" \
  -f pr_title="Add new feature" \
  -f pr_description="Description of changes" \
  -f labels="enhancement,needs-review" \
  -f target_branch="main"
```

### Task Sync (`sync-tasks.yml`)

Tasks from `5-project-memory/*/tasks/` automatically sync to GitHub Issues:

- Runs every hour
- Creates new issues for tasks
- Updates existing issues with latest state
- Labels tasks by status and priority
- Can be triggered manually for specific tasks

### Documentation Generation (`documentation-generator.yml`)

Auto-generates documentation from code:

- API documentation from Python files
- Module index
- Table of contents in README files
- Triggers on push to main or PRs

### Project Board Sync (`project-board-sync.yml`)

Organizes issues on the project board:

- Automatically adds new issues to "To Do"
- Moves issues based on labels:
  - `🔄 In Progress` → "In Progress"
  - `✅ Done` → "Done"
  - `🔥 High Priority` → "To Do"
  - `🌱 Low Priority` → "Backlog"

## Issue Labels

### Status Labels
- `🔄 In Progress` - Task is currently being worked on
- `✅ Done` - Task completed
- `❌ Failed` - Task failed
- `📝 Planning` - Task in planning phase

### Priority Labels
- `🔥 High Priority` - Urgent tasks
- `⚡ Medium Priority` - Normal priority
- `🌱 Low Priority` - Nice to have

### Type Labels
- `blackbox5-task` - Standard task
- `enhancement` - Feature request
- `bug` - Bug report
- `documentation` - Documentation update

## Development Workflow

### 1. Agent Creates Task

Agent creates a task in `5-project-memory/<project>/tasks/<task-id>/state.json`

### 2. Task Syncs to GitHub

The hourly sync workflow creates/updates a GitHub Issue:
- Title: `[Task <ID>] <Objective>`
- Body: Full task details including subtasks
- Labels: Status + Priority labels

### 3. Agent Works on Task

Agent makes changes and commits to a feature branch.

### 4. Automated PR Creation

When ready, agent creates a PR:
```bash
gh workflow run agent-pr.yml \
  -f agent_name="agent-name" \
  -f branch_name="feature/branch-name" \
  -f pr_title="Task #<id>: Implement feature"
```

### 5. CI/CD Runs

- PR checks run automatically
- Tests execute
- Linting and security scans

### 6. Documentation Updates

- Documentation generator runs on PR
- Auto-updates API docs and module index
- Comments on PR with changes

### 7. Project Board Updates

- Issue automatically moves to "In Progress" when PR is created
- Moves to "Review" when PR is ready
- Moves to "Done" when PR is merged

## Manual Operations

### Create Issue from Task

```bash
cd /opt/blackbox5
export GITHUB_TOKEN=$(cat ~/.secrets/github_token)
python bin/sync_tasks_to_github.py
```

### Generate Documentation

```bash
cd /opt/blackbox5
python bin/generate_api_docs.py
python bin/generate_module_index.py
python bin/update_readme_toc.py
```

### Sync Issue to Project Board

```bash
cd /opt/blackbox5
export ISSUE_NUMBER=123
python bin/sync_to_project_board.py
```

## Monitoring

### View All Workflows

```bash
gh workflow list
gh run list --workflow=sync-tasks.yml
```

### Check Sync Status

```bash
gh run view --workflow=sync-tasks.yml
```

### View Recent Issues

```bash
gh issue list --label "blackbox5-task" --limit 20
```

## Troubleshooting

### Token Issues

If workflows fail with authentication errors:
1. Verify `GITHUB_TOKEN` secret is set
2. Check token has correct scopes
3. Regenerate token if expired

### Sync Not Running

If task sync isn't working:
1. Check workflow status: `gh workflow view sync-tasks.yml`
2. View recent runs: `gh run list --workflow=sync-tasks.yml`
3. Check logs: `gh run view <run-id> --log`

### Project Board Issues

If issues aren't appearing on project board:
1. Verify `PROJECT_NUMBER` in script matches project
2. Check project permissions
3. Verify token has `project` scope

## Best Practices

1. **Use Descriptive Issue Titles**: Include task ID in PR/issue titles
2. **Label Consistently**: Use standard label format for automatic project board sync
3. **Branch Naming**: Use feature/task-based branch names
4. **Commit Messages**: Follow conventional commit format
5. **Documentation**: Update docs alongside code changes

## Security

- Store tokens in environment variables or secret managers
- Use fine-grained tokens when possible
- Rotate tokens regularly
- Don't commit tokens to repository
- Use branch protection rules

## Future Enhancements

- [ ] Automatic PR merging for CI-passing changes
- [ ] Automated changelog generation
- [ ] Integration with project management tools (Linear, Notion)
- [ ] Custom workflow triggers based on task states
- [ ] Automated release notes generation
