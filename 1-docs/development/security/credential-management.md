# Credential Management Guide

**Version:** 1.0.0
**Last Updated:** 2026-02-01
**Owner:** Security Team

---

## Overview

This guide establishes secure credential management practices for the Blackbox5 project. It covers environment setup, credential storage, rotation procedures, and incident response.

## Quick Start

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Fill in your actual credentials** in `.env` (never commit this file)

3. **Install pre-commit hooks:**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

4. **Verify setup:**
   ```bash
   pre-commit run --all-files
   ```

---

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GITHUB_TOKEN` | GitHub personal access token | `ghp_xxxxxxxxxxxx` |
| `SUPABASE_PROJECT_REF` | Supabase project reference | `abcdefgh12345678` |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key | `eyJ...` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |
| `NOTION_TOKEN` | Notion integration token | `secret_...` |
| `VERCEL_TOKEN` | Vercel API token | `...` |
| `CLOUDFLARE_API_TOKEN` | Cloudflare API token | `...` |

### File Locations

- **Project root:** `~/.blackbox5/.env` (for global settings)
- **Component-specific:** `2-engine/runtime/memory/brain/databases/.env`
- **Integration-specific:** Each integration manager reads from environment

---

## Security Patterns

### ✅ DO: Use Environment Variables

```python
# Good - credentials from environment
import os

token = os.environ.get("GITHUB_TOKEN")
if not token:
    raise ValueError("GITHUB_TOKEN environment variable is required")
```

### ❌ DON'T: Hardcode Credentials

```python
# Bad - never do this
token = "ghp_actual_token_here"  # NEVER commit this!
```

### ✅ DO: Use Placeholders in Documentation

```python
# Good - clear placeholders in examples
manager = GitHubManager(token="ghp_xxx", repo="owner/repo")
```

### ✅ DO: Validate Credentials at Runtime

```python
# Good - validate before use
def get_github_client():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError(
            "GITHUB_TOKEN not set. "
            "Get one at: https://github.com/settings/tokens"
        )
    return GitHubManager(token=token)
```

---

## Pre-commit Hooks

We use pre-commit hooks to prevent credential leaks:

### Installed Hooks

1. **detect-private-key** - Detects private keys
2. **detect-aws-credentials** - Detects AWS credentials
3. **detect-secrets** - Comprehensive secret detection (Yelp)
4. **bandit** - Python security linter
5. **gitleaks** - Comprehensive secret scanning

### Bypassing Hooks (Emergency Only)

```bash
# Only use in emergencies - requires justification
SKIP=detect-secrets git commit -m "..."
```

---

## Credential Rotation

### When to Rotate

- **Immediately:** If credential is leaked or suspected leaked
- **Quarterly:** Regular rotation schedule
- **On departure:** When team members leave

### Rotation Procedure

1. **Generate new credential** at the provider
2. **Update environment variables** locally
3. **Update CI/CD secrets** if applicable
4. **Test** the new credential works
5. **Revoke old credential** at the provider
6. **Document rotation** in incident log

### Provider-Specific Instructions

#### GitHub Token
1. Go to https://github.com/settings/tokens
2. Generate new token with required scopes
3. Update `GITHUB_TOKEN` environment variable
4. Revoke old token

#### Supabase
1. Go to Project Settings > API
2. Regenerate service role key
3. Update `SUPABASE_SERVICE_ROLE_KEY`
4. Old key expires in 24 hours

#### OpenAI
1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Update `OPENAI_API_KEY`
4. Delete old key

---

## Incident Response

### If Credentials Are Leaked

1. **IMMEDIATE (within 5 minutes):**
   - Rotate the leaked credential
   - Notify security team

2. **SHORT TERM (within 1 hour):**
   - Audit what the credential accessed
   - Check logs for unauthorized access
   - Document the incident

3. **LONG TERM (within 24 hours):**
   - Clean git history if needed (see below)
   - Update procedures to prevent recurrence
   - Team notification

### Cleaning Git History

If credentials were committed to git:

```bash
# Option 1: BFG Repo-Cleaner (recommended)
java -jar bfg.jar --replace-text passwords.txt

# Option 2: git filter-branch
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/file' \
  --prune-empty --tag-name-filter cat -- --all

# Force push (coordinate with team)
git push origin --force --all
git push origin --force --tags
```

**WARNING:** Force pushing rewrites history. Coordinate with the team first.

---

## Audit Findings

### 2026-02-01: Initial Security Audit (TASK-1769908019)

**Auditor:** RALF Executor
**Scope:** Full codebase and git history

#### Findings

| Category | Status | Details |
|----------|--------|---------|
| Git History | ✅ Clean | No leaked credentials found |
| Placeholder Usage | ✅ Acceptable | All examples use clear placeholders (ghp_xxx, your_token) |
| Environment Variables | ✅ Compliant | All code uses os.environ.get() pattern |
| Pre-commit Hooks | ✅ Installed | detect-secrets, gitleaks, bandit configured |
| Documentation | ✅ Complete | This guide created |

#### Placeholder Patterns Found

The following placeholder patterns are used in documentation (acceptable):

- `ghp_xxx`, `ghp_xxxxxxxxxxxx` - GitHub token examples
- `your_token`, `your_api_token` - Generic token examples
- `your_project_ref_here` - Supabase project reference
- `your_service_role_key_here` - Supabase key example

All patterns are clearly placeholders and not actual credentials.

#### Recommendations Applied

1. ✅ Created `.pre-commit-config.yaml` with secret detection
2. ✅ Created `.secrets.baseline` for detect-secrets
3. ✅ Created this credential management guide
4. ✅ Documented rotation procedures
5. ✅ Established incident response process

---

## Compliance Checklist

- [ ] `.env` is in `.gitignore`
- [ ] `.env.example` exists with placeholder values
- [ ] Pre-commit hooks installed
- [ ] No hardcoded credentials in code
- [ ] All credentials use environment variables
- [ ] Rotation schedule established
- [ ] Team trained on procedures

---

## Resources

- [GitHub Token Security](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [Pre-commit Framework](https://pre-commit.com/)
- [detect-secrets](https://github.com/Yelp/detect-secrets)
- [gitleaks](https://github.com/gitleaks/gitleaks)
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

---

## Contact

For security issues or questions:
- **Security Team:** security@blackbox5.local
- **Incident Response:** incident@blackbox5.local
- **Emergency:** Follow incident response procedure above
