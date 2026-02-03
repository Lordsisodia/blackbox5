# TASK-1769908019: Credential Handling Audit and Remediation

**Type:** security
**Priority:** CRITICAL
**Status:** pending
**Created:** 2026-02-01T08:03:19Z
**Source:** Migrated from legacy/autonomous-improvement branch (TASK-003)

---

## Objective

Audit and fix credential handling across the codebase to prevent credential leaks and establish secure credential management practices.

---

## Context

Security is foundational to the Blackbox5 system. This task ensures no credentials are leaked in git history, code, or documentation. It establishes patterns for secure credential management going forward.

This task was identified on the legacy/autonomous-improvement branch as a critical security requirement.

---

## Success Criteria

- [ ] Git history audited for leaked credentials
- [ ] All leaked credentials rotated (if found)
- [ ] All placeholder credentials removed from code
- [ ] Pre-commit hooks installed to prevent future leaks
- [ ] Environment variable pattern standardized
- [ ] Credential management documentation created
- [ ] All contributors notified of changes

---

## Approach

### Phase 1: Git History Audit (Day 1)

**1.1 Search for leaked credentials:**
```bash
# Search for GitHub tokens
git log -p -S "ghp_" --all
git log -p --all -- "token="

# Search for OpenAI API keys
git log -p -S "sk-" --all

# Search for database passwords
git log -p -S "blackbox4brain" --all

# Search for API keys in general
git log -p -S "api_key" --all
git log -p -S "apikey" --all
git log -p -S "api-key" --all

# Search for common secret patterns
git log -p --all -- "**/key.pem" "**/.env" "**/secrets.yaml"
```

**1.2 If credentials found:**
1. **Immediate rotation:**
   - Rotate GitHub tokens (if any found)
   - Rotate database passwords (if any found)
   - Rotate API keys (if any found)
   - Notify all users of rotation

2. **Clean git history:**
   ```bash
   # Option 1: BFG Repo-Cleaner (faster, safer)
   java -jar bfg.jar --replace-text passwords.txt

   # Option 2: git filter-branch (slower, more control)
   git filter-branch --force --index-filter \
     'git rm --cached --ignore-unmatch file-with-secrets' \
     --prune-empty --tag-name-filter cat -- --all

   # Force push to all remotes
   git push origin --force --all
   git push origin --force --tags
   ```

3. **Notify team:**
   - Document what leaked, what was rotated, actions taken

**1.3 Document findings:**
- Create incident report if credentials were leaked
- Document root cause
- Update procedures to prevent recurrence

---

### Phase 2: Replace Placeholder Credentials (Days 2-3)

**2.1 Find all placeholder credentials:**
```bash
# Search for common placeholder patterns
grep -rn "ghp_xxx\|ghp_xxxxxxxxxxxx" 2-engine/ --include="*.py" --include="*.md"
grep -rn "token=\"your" 2-engine/ --include="*.py"
grep -rn "password=\"your" 2-engine/ --include="*.py"
grep -rn "\"your_token\"" 2-engine/ --include="*.py"
```

**2.2 Replace in code:**

**Before:**
```python
# Bad - placeholder in code
client = GitHubClient(token="ghp_xxxxxxxxxxxx")
```

**After:**
```python
# Good - environment variable
import os
client = GitHubClient(token=os.environ.get("GITHUB_TOKEN"))
```

**2.3 Update documentation:**
- Add `.env.example` file with placeholder values
- Document required environment variables
- Update setup instructions

---

### Phase 3: Pre-commit Hooks (Day 4)

**3.1 Install pre-commit:**
```bash
pip install pre-commit
pre-commit install
```

**3.2 Create `.pre-commit-config.yaml`:**
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: detect-private-key
      - id: detect-aws-credentials

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

**3.3 Create baseline:**
```bash
detect-secrets scan > .secrets.baseline
```

---

### Phase 4: Documentation (Day 5)

**4.1 Create credential management guide:**
- Document: `1-docs/development/security/credential-management.md`
- Include: Environment setup, rotation procedures, incident response

**4.2 Update contributor docs:**
- Add security section to CONTRIBUTING.md
- Document pre-commit hook requirements

---

## Files to Modify

- `.pre-commit-config.yaml` (create)
- `.secrets.baseline` (create)
- `.env.example` (create)
- `1-docs/development/security/credential-management.md` (create)
- Various files with placeholder credentials (to be identified during audit)

## Files to Read

- `2-engine/.autonomous/prompts/system/executor-identity.md` (check for any embedded credentials)
- All Python files in `2-engine/` (search for credential patterns)
- Git history (audit for leaked secrets)

## Dependencies

- None (self-contained security task)

## Rollback Strategy

- If credential rotation causes issues, have backup credentials ready
- Document all changes for easy reversal
- Test all integrations after rotation

## Notes

- **CRITICAL:** If credentials are found leaked, rotate them IMMEDIATELY before continuing
- This audit may reveal need for immediate action - be prepared to interrupt other work
- Consider using GitHub's secret scanning alerts if available
- Document everything for compliance/audit trail

## Related

- Source: legacy/autonomous-improvement branch TASK-003
- Security best practices: https://docs.github.com/en/code-security/secret-scanning
