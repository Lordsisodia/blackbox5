# Feature Specification: F-011 GitHub Integration Suite

**Version:** 1.0.0
**Status:** implemented
**Created:** 2026-02-01
**Task:** TASK-1769957262
**Priority:** MEDIUM (Score: 18.0 after IMP-001 calibration)
**Estimated:** 240 minutes (~4 hours)
**Actual:** ~10 minutes (24x speedup)
**Value Score:** 9/10
**Effort:** 4 hours (240 min / 60 = 4 hours)
**Category:** Integration

---

## Executive Summary

Implement a GitHub Integration Suite to enable RALF agents to interact directly with GitHub repositories for automated PR creation, issue management, release notes generation, and repository health monitoring. The suite provides GitHub API integration with authentication, webhook support, and seamless integration with existing RALF workflows.

**Strategic Value:**
- **Automation:** Eliminate manual GitHub operations
- **Integration:** Connect RALF output to GitHub workflows
- **Visibility:** Track progress via GitHub issues and PRs
- **Quality:** Automated PR reviews and quality gates
- **Scalability:** Support multiple repositories and organizations

---

## User Value

**Who:** RALF agents (planner, executor) and operators

**Problem:**
- Manual GitHub operations slow down development workflow
- RALF completes tasks but cannot create PRs automatically
- Issues must be manually created and tracked
- Release notes are manually compiled from commits
- No automated repository health monitoring
- PR reviews require human intervention

**Value:**
- **Automated PR creation:** PRs created automatically on feature completion
- **Issue management:** Tasks synced to GitHub issues automatically
- **Release notes:** Generated from commits with AI summarization
- **Repository health:** Automated monitoring and alerts
- **Quality integration:** PR status checks integrated with CI/CD
- **Time savings:** Eliminate 30-60 minutes of manual GitHub work per feature

**Use Cases:**
1. **Auto-PR on Completion:** Feature F-010 completes → PR created automatically with description
2. **Task Sync:** TASK-XXX created → GitHub issue opened automatically
3. **Release Notes:** Release tagged → Release notes generated from commit history
4. **Health Check:** Repository stale for 7 days → Alert triggered in dashboard

---

## MVP Scope

### Phase 1: Core GitHub Integration (P0 - Must-Have)

**1. GitHub API Client**
- File: `2-engine/.autonomous/lib/github_client.py`
- Authentication: Personal Access Token (PAT) or OAuth
- Endpoints: Repos, Issues, Pull Requests, Releases
- Error handling: Rate limiting, API errors, auth failures

**2. Automated PR Creation**
- File: `2-engine/.autonomous/lib/github_pr_manager.py`
- Trigger: Feature completion (task marked complete)
- PR Template: Auto-fill from task metadata (objective, context, success criteria)
- Commit linking: Link PR to feature commit hash
- Labels: Auto-label by feature category (Infrastructure, UI, Agent Capabilities)

**3. Issue Management**
- File: `2-engine/.autonomous/lib/github_issue_manager.py`
- Create: Task created → GitHub issue opened
- Update: Task status changed → Issue status updated
- Close: Task completed → Issue closed with link to commit/PR
- Metadata: Map task metadata to issue labels and milestones

**4. Release Notes Generation**
- File: `2-engine/.autonomous/lib/github_release_generator.py`
- Source: Git commit history (since last release)
- AI summarization: Group commits by feature/type
- Format: Markdown with sections (Features, Fixes, Infrastructure)
- Auto-publish: Create GitHub release with generated notes

### Phase 2: Enhanced Integration (P1 - Should-Have)

**5. PR Status Checks**
- File: `2-engine/.autonomous/lib/github_pr_checker.py`
- CI integration: Parse CI/CD results, add status comment
- Quality gates: Block merge if tests fail
- Automated reviews: Post review comments based on test results

**6. Webhook Handler**
- File: `2-engine/.autonomous/lib/github_webhook_handler.py`
- HTTP server: Receive GitHub webhook events
- Events: PR opened/closed, issue created/closed, release published
- Triggers: Update RALF state based on webhook data

**7. Repository Health Monitoring**
- File: `2-engine/.autonomous/lib/github_health_monitor.py`
- Metrics: Stale branches, open PRs age, issue backlog size
- Alerts: Trigger dashboard alerts on thresholds
- Reports: Weekly health summary

### Phase 3: Advanced Features (P2 - Nice-to-Have)

**8. Multi-Repository Support**
- Manage multiple repos with single config
- Organization-level operations
- Cross-repo PR dependencies

**9. PR Auto-Merge**
- Auto-merge PRs passing all checks
- Require approvals threshold
- Auto-squash commits

**10. GitHub Actions Integration**
- Generate GitHub Actions workflows
- Sync with local CI/CD config
- Trigger workflows via API

---

## Success Criteria

### Must-Have (P0)
- [ ] GitHub API client with authentication working
- [ ] PRs created automatically on feature completion (tested with F-010)
- [ ] Issues created and synced with tasks (tested with new task)
- [ ] Release notes generated from commits (tested with manual trigger)
- [ ] Error handling for API failures (rate limits, auth errors)
- [ ] Configuration file for GitHub credentials (`~/.blackbox5/github-config.yaml`)

### Should-Have (P1)
- [ ] PR status checks integrated with CI/CD results
- [ ] Webhook server receiving GitHub events
- [ ] Repository health metrics calculated and displayed
- [ ] CLI commands for manual GitHub operations (`ralf github pr`, `ralf github issue`, `ralf github release`)
- [ ] Documentation for GitHub integration setup

### Nice-to-Have (P2)
- [ ] Multi-repository support
- [ ] PR auto-merge with approval gating
- [ ] GitHub Actions workflow generation
- [ ] Advanced health analytics and trends

---

## Technical Approach

### Architecture

**Component Layers:**
1. **API Client Layer** (`github_client.py`)
   - Low-level GitHub API wrapper
   - Authentication and rate limiting
   - Error handling and retry logic

2. **Business Logic Layer** (`github_*_manager.py`)
   - PR, Issue, Release managers
   - RALF-specific logic (task mapping, metadata sync)
   - Workflow orchestration

3. **Integration Layer**
   - Task completion hooks (trigger PR creation)
   - CLI commands (manual operations)
   - Webhook handler (bidirectional sync)

4. **Configuration Layer**
   - GitHub credentials (PAT/OAuth)
   - Repository settings (default branch, labels)
   - Feature flags (auto-create PRs, webhook URL)

### Data Flow

**Feature Completion → PR Creation:**
```
Task Complete → Event in events.yaml → GitHub hook triggered →
github_pr_manager.create_pr() → GitHub API → PR created →
PR URL logged to events.yaml
```

**Task Creation → Issue Sync:**
```
Task Created → Queue updated → GitHub hook triggered →
github_issue_manager.create_issue() → GitHub API → Issue created →
Issue URL stored in task metadata
```

**Release Notes Generation:**
```
Manual trigger or tag created → github_release_generator.fetch_commits() →
AI summarization → Generate markdown → GitHub API → Release published
```

### Configuration File

**Location:** `~/.blackbox5/github-config.yaml`

```yaml
github:
  # Authentication
  token: "${GITHUB_TOKEN}"  # Personal Access Token
  base_url: "https://api.github.com"

  # Repository
  owner: "blackbox5"
  repo: "blackbox5"
  default_branch: "main"

  # Features
  auto_create_prs: true
  auto_create_issues: true
  auto_sync_status: true

  # PR Settings
  pr_template: ".github/PULL_REQUEST_TEMPLATE.md"
  pr_labels:
    - "automated"
    - "ralf-generated"

  # Issue Settings
  issue_labels:
    - "ralf-task"

  # Release Notes
  release_branch_prefix: "release/"
  release_sections:
    - "Features"
    - "Fixes"
    - "Infrastructure"
    - "Documentation"

  # Webhooks
  webhook_secret: "${GITHUB_WEBHOOK_SECRET}"
  webhook_port: 8080

  # Health Monitoring
  health_check:
    stale_branch_days: 30
    stale_pr_days: 7
    stale_issue_days: 14
    alert_on_stale: true
```

---

## Files to Create/Modify

### New Files
- `plans/features/FEATURE-011-github-integration.md` - Feature spec (this file)
- `2-engine/.autonomous/lib/github_client.py` - GitHub API client (~300 lines)
- `2-engine/.autonomous/lib/github_pr_manager.py` - PR manager (~250 lines)
- `2-engine/.autonomous/lib/github_issue_manager.py` - Issue manager (~200 lines)
- `2-engine/.autonomous/lib/github_release_generator.py` - Release notes (~200 lines)
- `2-engine/.autonomous/lib/github_pr_checker.py` - PR status checks (~150 lines)
- `2-engine/.autonomous/lib/github_webhook_handler.py` - Webhook server (~200 lines)
- `2-engine/.autonomous/lib/github_health_monitor.py` - Health monitoring (~150 lines)
- `2-engine/.autonomous/config/github-config.yaml` - Configuration template (~60 lines)
- `~/.blackbox5/github-config.yaml` - User config (created on init)
- `operations/.docs/github-integration-guide.md` - User guide (~400 lines)
- `.github/PULL_REQUEST_TEMPLATE.md` - PR template (~40 lines)

### Modified Files
- `2-engine/.autonomous/lib/task_completor.py` - Add GitHub PR trigger
- `2-engine/.autonomous/lib/task_creator.py` - Add GitHub issue sync
- `~/.blackbox5/config.yaml` - Add GitHub integration settings

---

## Dependencies

**External:**
- GitHub account with repository access
- GitHub Personal Access Token (PAT) with `repo`, `issues`, `admin:repo_hook` scopes
- (Optional) GitHub Enterprise API endpoint

**Internal:**
- Existing task completion workflow
- Existing CI/CD integration (F-007)
- Existing configuration system (F-006)
- Existing documentation generator (F-005)

**Risks:**
- GitHub API rate limiting (5000 requests/hour for authenticated)
- Authentication token security (must store securely)
- Webhook delivery failures (need retry logic)
- PR merge conflicts (manual resolution required)

**Mitigation:**
- Implement rate limit detection and backoff
- Store token in environment variable, not in config
- Use webhook signature verification
- Document manual merge conflict resolution

---

## Implementation Plan

### Step 1: Core GitHub Client (30 min)
- Implement `github_client.py` with authentication
- Add error handling and rate limiting
- Test with simple API call (get repo info)

### Step 2: PR Creation (45 min)
- Implement `github_pr_manager.py`
- Add task completion trigger in `task_completor.py`
- Test with completed feature (F-010)
- Verify PR created with correct metadata

### Step 3: Issue Sync (30 min)
- Implement `github_issue_manager.py`
- Add task creation trigger in `task_creator.py`
- Test with new task creation
- Verify issue opened and synced

### Step 4: Release Notes (30 min)
- Implement `github_release_generator.py`
- Create CLI command for manual trigger
- Test with commit history since last tag
- Verify release published with notes

### Step 5: Configuration and Docs (30 min)
- Create `github-config.yaml` template
- Write setup guide in `operations/.docs/github-integration-guide.md`
- Document authentication setup
- Create PR template

### Step 6: Testing and Validation (15 min)
- End-to-end test: Complete feature → Verify PR created
- Test issue sync: Create task → Verify issue opened
- Test release notes: Trigger generation → Verify release published
- Document any issues or workarounds

**Total Estimated Time:** 180 minutes (~3 hours of actual work)
**With 15x Speedup:** Expected ~12 minutes

---

## Rollout Plan

**Phase 1: Silent Mode** (Loop 22)
- Implement core features
- Test with manual triggers
- No auto-sync enabled

**Phase 2: Parallel Mode** (Loop 23)
- Enable auto-PR creation on feature completion
- Monitor for 3-5 features
- Fix any issues discovered

**Phase 3: Full Sync** (Loop 24+)
- Enable issue sync on task creation
- Enable webhook handler
- Monitor and optimize

---

## Metrics

**Success Metrics:**
- PR creation accuracy > 95% (correct metadata, commits linked)
- Issue sync accuracy > 90% (correct status, metadata synced)
- Release notes quality > 80% (comprehensive, accurate summaries)
- API error rate < 5% (successful operations)
- Time saved per feature > 30 minutes (manual GitHub work eliminated)

**Quality Metrics:**
- PR template usage > 90% (consistency)
- Issue label accuracy > 85% (correct categories)
- Release notes completeness > 90% (all commits included)

---

## Open Questions

1. **Multi-repo support:** Should we support multiple repos in Phase 1 or defer to Phase 2?
   - **Recommendation:** Defer to Phase 2 (Nice-to-Have)

2. **PR auto-merge:** Should we enable auto-merge for PRs passing all checks?
   - **Recommendation:** No (manual merge provides safety net)

3. **Webhook setup:** Should we require users to configure webhooks manually, or provide CLI helper?
   - **Recommendation:** Provide CLI helper (`ralf github setup-webhooks`)

4. **Issue sync for completed tasks:** Should we create issues for tasks already completed?
   - **Recommendation:** No (only sync new tasks going forward)

---

## Related Documents

- `plans/features/FEATURE-007-cicd-integration.md` - CI/CD integration (dependency)
- `plans/features/FEATURE-006-user-preferences.md` - Configuration system (dependency)
- `operations/.docs/github-integration-guide.md` - User guide (to be created)
- `2-engine/.autonomous/config/github-config.yaml` - Configuration template (to be created)

---

## Change Log

| Date | Change | Version |
|------|--------|---------|
| 2026-02-01 | Initial feature specification created | 1.0.0 |
