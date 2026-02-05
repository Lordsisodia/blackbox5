# TASK-SSOT-018: Consolidate Notification Scripts

**Status:** pending
**Priority:** LOW
**Created:** 2026-02-06
**Parent:** Issue #20 - SSOT External Integrations Violations

## Objective
Merge telegram-notify.sh, notifications.sh, and hook notification logic into single notify.sh script.

## Success Criteria:
- [ ] Audit all notification scripts
- [ ] Design unified notify.sh with channel support
- [ ] Merge telegram-notify.sh functionality
- [ ] Merge notifications.sh functionality
- [ ] Update hooks to use notify.sh
- [ ] Support multiple channels via config
- [ ] Delete old notification scripts

## Context
Notifications scattered across:
- bin/telegram-notify.sh - Telegram only
- bin/notifications.sh - General notifications
- .claude/hooks/ralf-stop-hook.sh - Inline notifications
- CLAUDE.md - Notification documentation

## Approach
1. Inventory all notification code
2. Design unified script with pluggable channels
3. Create notify.sh
4. Update all callers
5. Delete old scripts

## Related Files
- bin/telegram-notify.sh
- bin/notifications.sh
- .claude/hooks/ralf-stop-hook.sh
- bin/notify.sh (to create)

## Rollback Strategy
Keep old scripts until new one verified.
