# TASK: Credential Handling Audit and Remediation

**Type:** Security
**Priority:** CRITICAL (P0)
**Status:** pending
**Estimated Effort:** 3-5 days
**Assigned To:** TBD (Security Engineer + Dev)

---

## Objective

Audit and fix credential handling across the codebase to prevent credential leaks and establish secure credential management practices.

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

## Implementation Steps

### Step 1: Git History Audit (Day 1)

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
   - Email: "Credential leak detected and remediated"
   - Include: What leaked, what was rotated, actions taken

**1.3 Document findings:**
- Create incident report if credentials were leaked
- Document root cause
- Update procedures to prevent recurrence

---

### Step 2: Replace Placeholder Credentials (Days 2-3)

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
# 2-engine/tools/integrations/github/manager.py
manager = GitHubManager(
    token="ghp_xxx",
    repo="owner/repo"
)
```

**After:**
```python
# 2-engine/tools/integrations/github/manager.py
import os

manager = GitHubManager(
    token=os.getenv("GITHUB_TOKEN"),
    repo=os.getenv("GITHUB_REPO", "owner/repo")
)
```

**2.3 Replace in documentation:**

**Before:**
```markdown
## Usage

```python
manager = GitHubManager(token="ghp_xxx", repo="owner/repo")
```
```

**After:**
```markdown
## Usage

First, set required environment variables:

```bash
export GITHUB_TOKEN="your_actual_token_here"
export GITHUB_REPO="owner/repo"
```

Then use in code:

```python
manager = GitHubManager(
    token=os.getenv("GITHUB_TOKEN"),
    repo=os.getenv("GITHUB_REPO")
)
```
```

**2.4 Update demo files:**
- Ensure all demos use environment variables
- Add setup instructions at top of demo files
- Include `.env.example` files with placeholder names (not values)

---

### Step 3: Add Pre-Commit Protection (Day 3-4)

**3.1 Install pre-commit framework:**
```bash
pip install pre-commit
```

**3.2 Create `.pre-commit-config.yaml`:**
```yaml
repos:
  # Detect secrets
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  # Check for common credential patterns
  - repo: local
    hooks:
      - id: no-hardcoded-credentials
        name: No hardcoded credentials
        entry: |
          (ghp_[a-zA-Z0-9]{36}|sk-[a-zA-Z0-9]{48}|api[_-]?key\s*=\s*["\'][^"\']+["\'])
        language: pygrep
        files: \.(py|yaml|yml|md|json)$
```

**3.3 Generate baseline:**
```bash
detect-secrets scan > .secrets.baseline
# Review and remove false positives
```

**3.4 Install hooks:**
```bash
pre-commit install
```

---

### Step 4: Create Credential Management Documentation (Day 4-5)

**4.1 Create `1-docs/operations/CREDENTIAL-MANAGEMENT.md`:**

```markdown
# Credential Management Guide

## Principles
1. Never commit credentials to git
2. Use environment variables for secrets
3. Rotate credentials regularly
4. Use different credentials for dev/prod
5. Audit credential access

## Environment Variable Naming

### Pattern
Use uppercase with underscores: `{SERVICE}_{CREDENTIAL_TYPE}`

### Examples
- `GITHUB_TOKEN` - GitHub personal access token
- `OPENAI_API_KEY` - OpenAI API key
- `POSTGRES_PASSWORD` - Database password
- `NEO4J_PASSWORD` - Neo4j password

### Configuration Files

#### Development
Create `.env` file (in `.gitignore`):
```
GITHUB_TOKEN=ghp_your_actual_token_here
OPENAI_API_KEY=sk-your_actual_key_here
POSTGRES_PASSWORD=your_actual_password_here
```

#### Template
Create `.env.example` (committed to git):
```
GITHUB_TOKEN=your_github_token_here
OPENAI_API_KEY=your_openai_key_here
POSTGRES_PASSWORD=your_postgres_password_here
```

## Secret Storage

### Development
- Use `.env` files (never committed)
- Use `.env.example` as template
- Load with `python-dotenv`

### Production
- Use environment variables (preferred)
- Or use secret management services:
  - HashiCorp Vault
  - AWS Secrets Manager
  - Azure Key Vault
  - Google Secret Manager

## Credential Rotation

### Regular Rotation
- GitHub tokens: Every 90 days
- API keys: Every 180 days
- Database passwords: Every 180 days

### Incident Rotation
- Rotate immediately if leaked
- Rotate immediately if team member leaves
- Rotate if suspected compromise

## Pre-Commit Hooks

Install pre-commit hooks to prevent credential leaks:
\`\`\`bash
pip install pre-commit
pre-commit install
\`\`\`

## Verification

Before committing, run:
\`\`\`bash
# Check for secrets
detect-secrets scan

# Check git diff for credentials
git diff --cached | grep -i "token\|key\|password"
\`\`\`
```

**4.2 Update CONTRIBUTING.md:**
Add section on credential handling best practices.

---

### Step 5: Test and Verify (Day 5)

**5.1 Test environment variable loading:**
```python
# tests/test_credential_handling.py
import os
import pytest

def test_github_token_from_env():
    """Test that GitHub token is loaded from environment variable."""
    os.environ['GITHUB_TOKEN'] = 'test_token'
    # Test that your code uses the env var
    assert get_github_token() == 'test_token'
    del os.environ['GITHUB_TOKEN']

def test_missing_credential_raises_error():
    """Test that missing credentials raise clear error."""
    with pytest.raises(EnvironmentError, match="GITHUB_TOKEN not set"):
        get_github_token()
```

**5.2 Verify pre-commit hooks:**
```bash
# Try to commit a file with fake credential
echo 'token = "ghp_test"' >> test.py
git add test.py
# Pre-commit should block this
pre-commit run --all-files
```

**5.3 Test with actual integrations:**
- Test GitHub integration with real token from env
- Test database connection with real password from env
- Verify no hard-coded credentials in logs

---

## Deliverables

1. Git history audit report
2. All placeholders replaced with environment variables
3. Pre-commit hooks installed and configured
4. Credential management documentation
5. Test coverage for credential handling
6. Team notification of changes

---

## Risk Mitigation

### Risk 1: Breaking existing workflows
**Mitigation:**
- Provide migration guide
- Support both old and new patterns temporarily
- Clear deprecation notices

### Risk 2: Credentials already leaked
**Mitigation:**
- Immediate rotation if found
- Incident response plan
- Team notification

### Risk 3: Developer friction
**Mitigation:**
- Provide `.env.example` templates
- Clear documentation
- Tooling support (auto-loading `.env`)

---

## References

- **Gap ID:** SEC-001
- **Related Documentation:** `gaps.md`, `phase-0-critical-fixes.md`
- **Tools:**
  - pre-commit: https://pre-commit.com/
  - detect-secrets: https://github.com/Yelp/detect-secrets
  - python-dotenv: https://github.com/theskumar/python-dotenv

---

## Notes

- **Why this is critical:** Hardcoded or placeholder credentials can accidentally be committed, leading to security breaches
- **Priority:** This should be completed before any other work to prevent accidental leaks
- **Ongoing:** Consider implementing secret scanning in CI/CD pipeline
