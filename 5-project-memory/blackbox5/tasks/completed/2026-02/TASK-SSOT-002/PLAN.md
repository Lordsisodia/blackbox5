# PLAN.md: Remove Credentials from events.yaml

**Task:** TASK-SSOT-002 - Credentials stored in events.yaml (should be env vars)
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 1-2 hours
**Importance:** 95 (Critical)

---

## 1. First Principles Analysis

### The Core Problem
Sensitive credentials (Telegram bot tokens, API keys) are stored in:
- `5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml`

This violates:
1. **Security Best Practices**: Credentials should never be in version control
2. **SSOT Principle**: Configuration should be separate from event data
3. **Environment Isolation**: Different environments need different credentials

### Security Risk
- Credentials visible in git history
- Anyone with repo access has credentials
- Cannot rotate credentials without code changes
- Violates principle of least privilege

### First Principles Solution
- **Environment Variables**: Credentials from env vars only
- **Configuration Separation**: Events.yaml for events, .env for secrets
- **No Hardcoded Secrets**: Zero tolerance for credentials in code/config

---

## 2. Current State Analysis

### File Analysis

**File:** `5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml`

**Expected Content:**
```yaml
events:
  - id: "evt-001"
    timestamp: "2026-02-05T10:00:00Z"
    type: "task_completed"
    data:
      task_id: "TASK-001"
```

**Problem:** Credentials may be embedded in:
- Event data payloads
- Configuration sections
- Comments (less critical but still bad)

### Credentials to Find

1. **Telegram Bot Token** - Format: `bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`
2. **ZAI API Key** - Format: `sk-zai-*` or similar
3. **Any other API keys** - Look for `key`, `token`, `secret`, `password`

---

## 3. Proposed Solution

### Step 1: Audit and Extract (30 min)

1. Search events.yaml for credential patterns
2. Document all found credentials
3. Identify which services they belong to

### Step 2: Environment Setup (30 min)

**Create:** `5-project-memory/blackbox5/.env` (gitignored)

```bash
# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# ZAI API Configuration
ZAI_API_KEY=your_api_key_here
ZAI_API_URL=https://api.zai.com/v1

# Other credentials...
```

**Update:** `.gitignore`
```
.env
.env.local
*.pem
*.key
```

### Step 3: Code Updates (30 min)

**Update:** Scripts that read credentials

```python
# Before (BAD)
import yaml
with open('events.yaml') as f:
    config = yaml.safe_load(f)
token = config['telegram']['bot_token']

# After (GOOD)
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('TELEGRAM_BOT_TOKEN')
```

### Step 4: Cleanup (30 min)

1. Remove credentials from events.yaml
2. Verify no credentials in git history (git filter-branch if needed)
3. Rotate exposed credentials
4. Update documentation

---

## 4. Files to Modify

### Immediate Changes
1. `5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml` - Remove credentials
2. `5-project-memory/blackbox5/.env` - Create (gitignored)
3. `.gitignore` - Add .env

### Scripts to Update
1. Any script reading credentials from events.yaml
2. Notification scripts (Telegram)
3. API clients (ZAI)

### Documentation
1. `5-project-memory/blackbox5/README.md` - Add environment setup section
2. `5-project-memory/blackbox5/.docs/setup.md` - Document credential configuration

---

## 5. Success Criteria

- [ ] Zero credentials in events.yaml
- [ ] .env file created with all credentials
- [ ] .env in .gitignore
- [ ] All scripts updated to use environment variables
- [ ] Exposed credentials rotated
- [ ] Documentation updated with setup instructions
- [ ] Security audit passed (grep for credentials returns nothing)

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Restore credentials to events.yaml (temporary)
2. **Fix**: Debug environment variable loading
3. **Re-apply**: Remove credentials once fixed

---

## 7. Security Checklist

- [ ] No hardcoded credentials in any YAML file
- [ ] No credentials in JSON files
- [ ] No credentials in shell scripts
- [ ] No credentials in Python files
- [ ] .env properly gitignored
- [ ] Credentials rotated after removal
- [ ] Team notified of new setup process

---

## 8. Estimated Timeline

| Step | Duration | Cumulative |
|------|----------|------------|
| Step 1: Audit | 30 min | 30 min |
| Step 2: Environment Setup | 30 min | 1 hour |
| Step 3: Code Updates | 30 min | 1.5 hours |
| Step 4: Cleanup | 30 min | 2 hours |
| **Total** | | **1-2 hours** |

---

**CRITICAL SECURITY ISSUE** - This should be prioritized above other tasks.

*Plan created based on SSOT violation analysis - Credentials in events.yaml*
