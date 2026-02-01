# GitHub Integration Suite - User Guide

**Feature:** F-011 (GitHub Integration Suite)
**Version:** 1.0.0
**Status:** Implemented

---

## Table of Contents

1. [Overview](#overview)
2. [Setup](#setup)
3. [Components](#components)
4. [Usage](#usage)
5. [CLI Commands](#cli-commands)
6. [Configuration](#configuration)
7. [Webhook Setup](#webhook-setup)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)
10. [API Reference](#api-reference)

---

## Overview

The GitHub Integration Suite enables RALF agents to interact directly with GitHub repositories for automated PR creation, issue management, release notes generation, and repository health monitoring.

### Features

- **Automated PR Creation**: Create pull requests automatically on feature completion
- **Issue Management**: Sync RALF tasks with GitHub issues
- **Release Notes**: Generate release notes from commit history
- **PR Status Checks**: Integrate CI/CD results with PR reviews
- **Webhook Handler**: Receive and process GitHub webhook events
- **Health Monitoring**: Track repository health metrics and alerts

### Value

- **Time Savings**: Eliminate 30-60 minutes of manual GitHub work per feature
- **Automation**: Seamless integration between RALF workflows and GitHub
- **Visibility**: Track progress via GitHub issues and PRs
- **Quality**: Automated PR reviews and quality gates

---

## Setup

### Prerequisites

1. **GitHub Account**: Must have access to target repository
2. **Personal Access Token (PAT)**: Generate at https://github.com/settings/tokens
3. **Python Dependencies**: PyGithub library

### Step 1: Install Dependencies

```bash
# Install PyGithub
pip install PyGithub

# Or install with pipenv
pipenv install PyGithub
```

### Step 2: Generate Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Set token scopes:
   - `repo` - Full repository access
   - `issues` - Issue management
   - `admin:repo_hook` - Webhook management
4. Generate and copy the token
5. **IMPORTANT**: Store securely (use environment variable)

### Step 3: Configure Environment Variables

```bash
# Add to ~/.bashrc or ~/.zshrc
export GITHUB_TOKEN="ghp_your_token_here"
export GITHUB_OWNER="your_org_or_user"
export GITHUB_REPO="your_repo_name"

# Optional: Webhook secret
export GITHUB_WEBHOOK_SECRET="your_webhook_secret"

# Reload shell
source ~/.bashrc
```

### Step 4: Create Configuration File

```bash
# Copy template
cp 2-engine/.autonomous/config/github-config.yaml ~/.blackbox5/github-config.yaml

# Edit with your settings
nano ~/.blackbox5/github-config.yaml
```

### Step 5: Test Connection

```bash
# Test GitHub API connection
cd 2-engine/.autonomous/lib
python3 github_client.py

# Expected output:
# Testing GitHub connection...
# GitHub API connection successful. Authenticated as: your_username
```

---

## Components

### 1. GitHub Client (`github_client.py`)

Low-level GitHub API wrapper with authentication, rate limiting, and error handling.

**Key Features:**
- Authentication via Personal Access Token
- Rate limit detection and backoff
- Retry logic for transient failures
- Comprehensive error handling

**Usage:**
```python
from github_client import GitHubClient

client = GitHubClient(
    token="ghp_xxx",
    owner="blackbox5",
    repo="blackbox5"
)

# Get repository info
info = client.get_repo_info()

# List issues
issues = client.list_issues(state="open")

# Get commits
commits = client.get_commits_since(since_date=datetime.now() - timedelta(days=7))
```

### 2. PR Manager (`github_pr_manager.py`)

Automated Pull Request creation on feature completion.

**Key Features:**
- Auto-create PR from task metadata
- Fill PR description from task spec
- Apply labels based on feature category
- Track PR status

**Usage:**
```python
from github_pr_manager import GitHubPRManager

pr_manager = GitHubPRManager(client)

# Create PR from task
pr = pr_manager.create_pr_from_task(
    task_data={
        "task_id": "TASK-1769957262",
        "feature_id": "F-011",
        "title": "GitHub Integration Suite",
        "objective": "Enable RALF to interact with GitHub...",
        "changes": [
            "Created github_client.py",
            "Created github_pr_manager.py"
        ],
        "success_criteria": [
            {"text": "GitHub API working", "status": "[x]"},
            {"text": "PR creation tested", "status": "[x]"}
        ]
    },
    branch="feature/f-011-github-integration",
    labels=["feature", "integration"]
)
```

### 3. Issue Manager (`github_issue_manager.py`)

Automated issue management and sync with RALF tasks.

**Key Features:**
- Auto-create issue from task
- Sync task status to issue status
- Close issue on task completion
- Apply labels automatically

**Usage:**
```python
from github_issue_manager import GitHubIssueManager

issue_manager = GitHubIssueManager(client)

# Create issue from task
issue = issue_manager.create_issue_from_task(
    task_data={
        "task_id": "TASK-1769957262",
        "feature_id": "F-011",
        "title": "Implement GitHub Integration",
        "objective": "Enable RALF to interact with GitHub...",
        "priority": "high"
    },
    labels=["enhancement", "integration"]
)

# Sync task status
issue_manager.sync_task_to_issue(
    task_data={"status": "completed"},
    issue_number=123
)
```

### 4. Release Generator (`github_release_generator.py`)

Automated release notes generation from commit history.

**Key Features:**
- Auto-generate release notes from commits
- Group commits by category (Features, Fixes, Infrastructure)
- Create GitHub releases with notes
- Tag-based release management

**Usage:**
```python
from github_release_generator import GitHubReleaseGenerator

release_gen = GitHubReleaseGenerator(client)

# Generate release notes
notes = release_gen.generate_notes(
    since_date=datetime(2026, 1, 1),
    sections=["Features", "Fixes", "Infrastructure"]
)

# Create release
release = release_gen.create_release(
    tag="v1.0.0",
    name="Version 1.0.0",
    generate_notes=True
)
```

### 5. PR Checker (`github_pr_checker.py`)

PR status checks integration with CI/CD results.

**Key Features:**
- Check PR mergeability status
- Post CI/CD results as comments
- Block merge if tests fail (quality gate)
- Track PR review status

**Usage:**
```python
from github_pr_checker import GitHubPRChecker

pr_checker = GitHubPRChecker(client, quality_gate_enabled=True)

# Check if PR can merge
status = pr_checker.can_merge(pr_number=123)

# Post quality gate report
pr_checker.post_quality_gate_report(
    pr_number=123,
    ci_results=[
        CheckResult(name="tests", status="success", description="All tests passed"),
        CheckResult(name="lint", status="failure", description="Linting errors found")
    ]
)
```

### 6. Webhook Handler (`github_webhook_handler.py`)

HTTP server for receiving and processing GitHub webhook events.

**Key Features:**
- HTTP server for receiving webhooks
- Signature verification
- Event routing to handlers
- Support for all GitHub event types

**Usage:**
```python
from github_webhook_handler import GitHubWebhookHandler

# Create handler
handler = GitHubWebhookHandler(secret="webhook_secret")

# Register custom callback
def pr_callback(event):
    pr = event.payload.get("pull_request", {})
    print(f"PR Event: #{pr.get('number')}")

handler.register_callback("pull_request", pr_callback)

# Start server (blocking)
handler.start_server(port=8080)
```

### 7. Health Monitor (`github_health_monitor.py`)

Repository health monitoring and alerting.

**Key Features:**
- Track stale branches, PRs, and issues
- Calculate health metrics
- Generate health reports
- Alert on threshold violations

**Usage:**
```python
from github_health_monitor import GitHubHealthMonitor

monitor = GitHubHealthMonitor(
    client,
    stale_branch_days=30,
    stale_pr_days=7,
    stale_issue_days=14
)

# Generate health report
report = monitor.generate_health_report()

# Check thresholds and get alerts
alerts = monitor.check_thresholds(report)

# Format report as Markdown
print(monitor.format_health_report(report))
```

---

## Usage

### Basic Workflow

1. **Initialize Client**:
   ```python
   from github_client import GitHubClient

   client = GitHubClient()
   ```

2. **Create PR on Feature Completion**:
   ```python
   from github_pr_manager import GitHubPRManager

   pr_manager = GitHubPRManager(client)
   pr = pr_manager.create_pr_from_task(task_data, branch="feature/xyz")
   ```

3. **Generate Release Notes**:
   ```python
   from github_release_generator import GitHubReleaseGenerator

   release_gen = GitHubReleaseGenerator(client)
   release = release_gen.create_release(tag="v1.0.0", generate_notes=True)
   ```

### Integration with RALF Workflows

#### Task Completion → PR Creation

When a RALF task completes, automatically create a PR:

```python
# In task_completor.py (after task completion)
from github_pr_manager import GitHubPRManager

client = GitHubClient()
pr_manager = GitHubPRManager(client)

# Create PR from completed task
pr = pr_manager.create_pr_from_task(
    task_data=task.metadata,
    branch=task.branch,
    labels=["feature", task.feature_id]
)

# Log PR URL
logger.info(f"PR created: {pr['url']}")
```

#### Task Creation → Issue Sync

When a RALF task is created, automatically create a GitHub issue:

```python
# In task_creator.py (after task creation)
from github_issue_manager import GitHubIssueManager

client = GitHubClient()
issue_manager = GitHubIssueManager(client)

# Create issue from task
issue = issue_manager.create_issue_from_task(
    task_data=task.metadata,
    labels=["ralf-task", f"priority:{task.priority}"]
)

# Store issue URL in task metadata
task.metadata["github_issue_url"] = issue["url"]
```

---

## CLI Commands

Each component includes a CLI interface for manual operations.

### Test GitHub Connection

```bash
cd 2-engine/.autonomous/lib
python3 github_client.py
```

### List Issues

```bash
python3 github_issue_manager.py
```

### List Pull Requests

```bash
python3 github_pr_manager.py
```

### Generate Release Notes

```bash
python3 github_release_generator.py
```

### Generate Health Report

```bash
python3 github_health_monitor.py
```

### Start Webhook Server

```bash
python3 github_webhook_handler.py
```

---

## Configuration

### Configuration File Location

`~/.blackbox5/github-config.yaml`

### Key Settings

```yaml
github:
  token: "${GITHUB_TOKEN}"  # Use environment variable
  base_url: "https://api.github.com"

repository:
  owner: "blackbox5"
  repo: "blackbox5"
  default_branch: "main"

features:
  auto_create_prs: false
  auto_create_issues: false
  auto_sync_status: false
  enable_webhooks: false

pull_requests:
  base_branch: "main"
  create_as_draft: false

issues:
  add_priority_label: true
  add_feature_label: true

webhooks:
  secret: "${GITHUB_WEBHOOK_SECRET}"
  port: 8080
  host: "0.0.0.0"

health_monitoring:
  stale_branch_days: 30
  stale_pr_days: 7
  stale_issue_days: 14

quality_gates:
  enabled: true
  post_status_comments: true
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GITHUB_TOKEN` | Personal Access Token | Yes |
| `GITHUB_OWNER` | Repository owner | No (in config) |
| `GITHUB_REPO` | Repository name | No (in config) |
| `GITHUB_WEBHOOK_SECRET` | Webhook secret | No (only for webhooks) |

---

## Webhook Setup

### Step 1: Generate Webhook Secret

```bash
# Generate secure random secret
openssl rand -hex 32
```

### Step 2: Configure RALF

Add webhook secret to configuration:

```yaml
# ~/.blackbox5/github-config.yaml
webhooks:
  secret: "your_webhook_secret_here"
  port: 8080
```

Or use environment variable:

```bash
export GITHUB_WEBHOOK_SECRET="your_webhook_secret"
```

### Step 3: Start Webhook Server

```bash
# Start webhook server
python3 2-engine/.autonomous/lib/github_webhook_handler.py
```

### Step 4: Configure GitHub Webhook

1. Go to repository Settings → Webhooks → Add webhook
2. Set Payload URL: `http://your-server:8080/webhook`
3. Set Content type: `application/json`
4. Set Secret: (your webhook secret)
5. Select events:
   - Pull requests
   - Issues
   - Pushes
   - Releases
   - Status checks
6. Click "Add webhook"

### Step 5: Test Webhook

Click "Recent Deliveries" in webhook settings to verify events are being received.

---

## Best Practices

### 1. Token Security

- **Always** use environment variables for tokens
- **Never** commit tokens to git
- **Rotate** tokens every 90 days
- **Limit** token scopes to minimum required

### 2. Rate Limiting

GitHub API has rate limits:
- 5000 requests/hour for authenticated requests
- 60 requests/hour for unauthenticated requests

The `github_client.py` automatically:
- Tracks rate limit status
- Warns when limit is low
- Implements backoff on errors

### 3. Error Handling

All components include comprehensive error handling:

```python
try:
    pr = pr_manager.create_pr_from_task(task_data, branch="feature/xyz")
except GitHubAuthError as e:
    logger.error(f"Authentication failed: {e}")
except GitHubRateLimitError as e:
    logger.error(f"Rate limit exceeded: {e}")
except GitHubAPIError as e:
    logger.error(f"API error: {e}")
```

### 4. Quality Gates

Enable quality gates to block merging PRs with failed checks:

```yaml
quality_gates:
  enabled: true
  post_status_comments: true
```

### 5. Webhook Security

- **Always** use signature verification
- **Never** expose webhook endpoint without authentication
- **Use** HTTPS in production
- **Rotate** webhook secrets regularly

### 6. Testing

Test components before enabling automation:

```python
# Test connection
client.test_connection()

# Test PR creation (draft mode)
pr = pr_manager.create_pr_from_task(task_data, branch="feature/test", draft=True)

# Test issue creation
issue = issue_manager.create_issue_from_task(task_data, labels=["test"])

# Verify then clean up
pr_manager.update_pr(pr["number"], state="closed")
issue_manager.close_issue(issue["number"])
```

---

## Troubleshooting

### Issue: Authentication Failed

**Error:** `GitHubAuthError: Authentication failed`

**Solutions:**
1. Verify `GITHUB_TOKEN` is set: `echo $GITHUB_TOKEN`
2. Check token has required scopes (repo, issues, admin:repo_hook)
3. Regenerate token if expired
4. Test token: `curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user`

### Issue: Rate Limit Exceeded

**Error:** `GitHubRateLimitError: Rate limit exceeded`

**Solutions:**
1. Wait for rate limit to reset (check `rate_limit.reset_time`)
2. Reduce request frequency
3. Implement request queuing
4. Consider increasing rate limit (GitHub Enterprise)

### Issue: Webhook Signature Verification Failed

**Error:** `Signature verification failed`

**Solutions:**
1. Verify webhook secret matches in GitHub and config
2. Check secret is set in environment variable
3. Ensure secret is not URL-encoded
4. Regenerate webhook secret if needed

### Issue: PR Merge Conflicts

**Error:** `PR has merge conflicts`

**Solutions:**
1. Pull latest changes: `git pull origin main`
2. Resolve conflicts locally
3. Push resolved branch: `git push origin feature/xyz`
4. PR will auto-update mergeable status

### Issue: Webhook Not Receiving Events

**Solutions:**
1. Check webhook server is running: `curl http://localhost:8080/health`
2. Verify firewall allows inbound traffic on port 8080
3. Check webhook delivery logs in GitHub
4. Test webhook payload: "Redeliver" in GitHub webhook settings

### Issue: Release Notes Empty

**Solutions:**
1. Verify commits exist since last tag
2. Check branch name matches target branch
3. Ensure commit messages match category patterns
4. Manually specify `since_date` if needed

---

## API Reference

### GitHubClient

```python
client = GitHubClient(
    token: Optional[str] = None,
    owner: Optional[str] = None,
    repo: Optional[str] = None,
    base_url: str = "https://api.github.com",
    timeout: int = 30,
    max_retries: int = 3
)

# Methods
client.get_repo() -> Repository
client.get_repo_info() -> Dict[str, Any]
client.list_issues(state: str = "open") -> List[Dict]
client.list_pull_requests(state: str = "open") -> List[Dict]
client.get_commits_since(since: datetime) -> List[Dict]
client.get_latest_release() -> Optional[Dict]
client.test_connection() -> bool
```

### GitHubPRManager

```python
pr_manager = GitHubPRManager(
    client: GitHubClient,
    pr_template_path: Optional[str] = None,
    default_labels: Optional[List[str]] = None
)

# Methods
pr_manager.create_pr(title, body, head, base, labels, reviewers, draft) -> Dict
pr_manager.create_pr_from_task(task_data, branch, base, labels, reviewers, draft) -> Dict
pr_manager.update_pr(pr_number, title, body, state) -> Dict
pr_manager.get_pr_status(pr_number) -> PRStatus
pr_manager.list_prs(state, base) -> List[Dict]
pr_manager.merge_pr(pr_number, commit_message, merge_method) -> Dict
```

### GitHubIssueManager

```python
issue_manager = GitHubIssueManager(
    client: GitHubClient,
    default_labels: Optional[List[str]] = None
)

# Methods
issue_manager.create_issue(title, body, labels, assignees, milestone) -> Dict
issue_manager.create_issue_from_task(task_data, labels, assignees) -> Dict
issue_manager.update_issue(issue_number, title, body, state, labels, assignees) -> Dict
issue_manager.close_issue(issue_number, close_comment, related_pr) -> Dict
issue_manager.add_comment(issue_number, comment) -> Dict
issue_manager.get_issue(issue_number) -> Dict
issue_manager.list_issues(state, labels) -> List[Dict]
issue_manager.sync_task_to_issue(task_data, issue_number) -> Dict
```

### GitHubReleaseGenerator

```python
release_gen = GitHubReleaseGenerator(
    client: GitHubClient,
    default_sections: Optional[List[str]] = None
)

# Methods
release_gen.generate_notes(since_tag, since_date, branch, sections) -> str
release_gen.create_release(tag, name, body, generate_notes, draft, prerelease) -> Dict
release_gen.update_release(release_id, tag_name, name, body, draft, prerelease) -> Dict
release_gen.get_release(tag) -> Optional[Dict]
release_gen.list_releases() -> List[Dict]
```

### GitHubPRChecker

```python
pr_checker = GitHubPRChecker(
    client: GitHubClient,
    quality_gate_enabled: bool = True
)

# Methods
pr_checker.get_pr_status(pr_number) -> PRStatus
pr_checker.get_ci_status(pr_number) -> List[CheckResult]
pr_checker.post_status_comment(pr_number, check_results, summary) -> Dict
pr_checker.post_review_comment(pr_number, review_comments, summary) -> Dict
pr_checker.can_merge(pr_number) -> Dict
pr_checker.get_review_status(pr_number) -> Dict
pr_checker.post_quality_gate_report(pr_number, ci_results) -> Dict
```

### GitHubWebhookHandler

```python
handler = GitHubWebhookHandler(
    secret: Optional[str] = None,
    event_callbacks: Optional[Dict[str, Callable]] = None
)

# Methods
handler.start_server(host: str = "0.0.0.0", port: int = 8080) -> None
handler.stop_server() -> None
handler.register_callback(event_type, callback) -> None
```

### GitHubHealthMonitor

```python
monitor = GitHubHealthMonitor(
    client: GitHubClient,
    stale_branch_days: int = 30,
    stale_pr_days: int = 7,
    stale_issue_days: int = 14
)

# Methods
monitor.get_stale_branches() -> List[Dict]
monitor.get_stale_pull_requests() -> List[Dict]
monitor.get_stale_issues() -> List[Dict]
monitor.get_unreviewed_prs(min_hours: int = 24) -> List[Dict]
monitor.generate_health_report() -> HealthMetrics
monitor.check_thresholds(metrics: HealthMetrics) -> List[HealthAlert]
monitor.format_health_report(metrics: HealthMetrics) -> str
monitor.generate_alert_summary(alerts: List[HealthAlert]) -> str
```

---

## Support

For issues or questions:
1. Check this guide's troubleshooting section
2. Review component docstrings and CLI help
3. Check GitHub API documentation: https://docs.github.com/en/rest
4. Contact RALF maintainers

---

**End of GitHub Integration Suite User Guide**

**Feature F-011 - Version 1.0.0 - Implemented 2026-02-01**
