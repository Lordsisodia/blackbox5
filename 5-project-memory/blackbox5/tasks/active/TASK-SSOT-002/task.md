# TASK-SSOT-002: Remove Hardcoded Credentials

**Status:** pending
**Priority:** CRITICAL
**Created:** 2026-02-06
**Parent:** Issue #20 - SSOT External Integrations Violations

## Objective
Remove all hardcoded API keys and tokens from the codebase. Implement environment variable pattern.

## Success Criteria
- [ ] Remove hardcoded Telegram bot token from bin/telegram-notify.sh
- [ ] Remove hardcoded Telegram bot token from .claude/settings.json
- [ ] Remove hardcoded ZAI API key from 2-engine/.autonomous/config/secrets.yaml
- [ ] Create .env.example template file
- [ ] Add .env to .gitignore
- [ ] Update scripts to use environment variables
- [ ] Rotate exposed credentials (generate new tokens)

## Context
CRITICAL SECURITY ISSUE: Hardcoded credentials found in:
- bin/telegram-notify.sh: TELEGRAM_BOT_TOKEN
- .claude/settings.json: Telegram configuration
- 2-engine/.autonomous/config/secrets.yaml: ZAI_API_KEY

## Approach
1. Identify all hardcoded credentials
2. Create .env.example with placeholder values
3. Update scripts to load from environment
4. Remove hardcoded values
5. Rotate credentials immediately after
6. Test that integrations still work

## Security Impact
HIGH - Credentials are currently exposed in git history

## Rollback Strategy
If integrations break, restore from backup and fix environment variable loading.
