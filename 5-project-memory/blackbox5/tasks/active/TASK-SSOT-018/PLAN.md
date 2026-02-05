# PLAN.md: Consolidate Notification Configuration

**Task:** TASK-SSOT-018 - Notification config in events.yaml and elsewhere
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 2-3 hours
**Importance:** 60 (Medium)

---

## 1. First Principles Analysis

### The Core Problem
Notification configuration is scattered across:
- `5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml`
- `5-project-memory/blackbox5/.autonomous/agents/communications/queue.yaml`
- Potentially other agent configs
- Hardcoded in scripts

This creates:
1. **Inconsistent Routing**: Same event notified differently
2. **Configuration Drift**: Different settings in different places
3. **Maintenance Overhead**: Updates needed in multiple places
4. **Debugging Difficulty**: Hard to trace notification flow

### First Principles Solution
- **Central Configuration**: Single notification config file
- **Explicit Routing**: Clear event → channel mappings
- **Template Support**: Reusable notification templates
- **Environment Awareness**: Different configs per environment

---

## 2. Current State Analysis

### Notification Locations

| Location | Configuration Type |
|----------|-------------------|
| `events.yaml` | Event handlers with notifications |
| `queue.yaml` | Queue notifications |
| Agent configs | Agent-specific notifications |
| Scripts | Hardcoded notification logic |

### Issues

1. **Scattered Config**: 4+ places with notification logic
2. **Hardcoded Channels**: Telegram bot tokens in config files
3. **No Templates**: Notifications built ad-hoc

---

## 3. Proposed Solution

### Decision: Central Notification Configuration

**File:** `5-project-memory/blackbox5/.autonomous/notifications.yaml`

```yaml
version: "1.0"
description: "Central notification configuration"

# Channel configurations
channels:
  telegram:
    type: "telegram"
    enabled: true
    config:
      bot_token: "${TELEGRAM_BOT_TOKEN}"  # From env var
      chat_id: "${TELEGRAM_CHAT_ID}"
    rate_limit:
      max_per_minute: 10

  email:
    type: "email"
    enabled: false
    config:
      smtp_server: "${SMTP_SERVER}"
      from_address: "alerts@blackbox5.local"

  webhook:
    type: "webhook"
    enabled: true
    config:
      url: "${WEBHOOK_URL}"
      headers:
        Authorization: "Bearer ${WEBHOOK_TOKEN}"

# Event routing
event_routing:
  - event: "task.completed"
    channels:
      - telegram
    template: "task_completed"
    priority: "normal"

  - event: "task.failed"
    channels:
      - telegram
      - webhook
    template: "task_failed"
    priority: "high"

  - event: "goal.achieved"
    channels:
      - telegram
    template: "goal_achieved"
    priority: "normal"

  - event: "system.error"
    channels:
      - telegram
      - webhook
      - email
    template: "system_error"
    priority: "critical"

# Notification templates
templates:
  task_completed:
    title: "Task Completed"
    message: |
      Task {{task_id}} has been completed.

      Title: {{task_title}}
      Duration: {{duration_minutes}} minutes
      Status: {{status}}

  task_failed:
    title: "Task Failed"
    message: |
      Task {{task_id}} has failed.

      Title: {{task_title}}
      Error: {{error_message}}

  goal_achieved:
    title: "Goal Achieved"
    message: |
      Goal {{goal_id}} has been achieved!

      Title: {{goal_title}}
      Progress: {{progress_percentage}}%

  system_error:
    title: "System Error"
    message: |
      Critical system error occurred.

      Error: {{error_message}}
      Component: {{component}}
      Time: {{timestamp}}

# Default settings
defaults:
  retry_attempts: 3
  retry_delay_seconds: 5
  batch_notifications: false
  batch_window_seconds: 60
```

### Implementation Plan

#### Phase 1: Audit Current Notifications (30 min)

1. Find all notification configurations
2. Document current routing logic
3. Identify hardcoded notifications

#### Phase 2: Create Central Config (1 hour)

**File:** `5-project-memory/blackbox5/.autonomous/notifications.yaml`

- Define channels
- Set up event routing
- Create templates
- Configure defaults

#### Phase 3: Create Notification Service (1 hour)

**File:** `2-engine/.autonomous/lib/notification_service.py`

```python
class NotificationService:
    def __init__(self, config_path: str):
        self.config = load_notification_config(config_path)
        self.channels = self._init_channels()

    def notify(self, event_type: str, data: dict):
        """Send notification for an event."""
        routing = self._get_routing(event_type)

        for channel_name in routing['channels']:
            channel = self.channels.get(channel_name)
            if channel and channel.is_enabled():
                message = self._render_template(
                    routing['template'],
                    data
                )
                channel.send(message, priority=routing['priority'])
```

#### Phase 4: Migrate Existing Notifications (30 min)

1. Replace hardcoded notifications with service calls
2. Update event handlers to use central routing
3. Test all notification paths

---

## 4. Files to Modify

### New Files
1. `5-project-memory/blackbox5/.autonomous/notifications.yaml` - Central config
2. `2-engine/.autonomous/lib/notification_service.py` - Notification service

### Modified Files
1. Remove notification config from events.yaml
2. Remove notification config from queue.yaml
3. Update scripts with hardcoded notifications

---

## 5. Success Criteria

- [ ] Central notifications.yaml created
- [ ] Notification service implemented
- [ ] All notifications use central config
- [ ] Templates defined for common events
- [ ] No hardcoded notification logic
- [ ] Documentation updated

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Restore original notification configs
2. **Fix**: Debug notification service
3. **Re-apply**: Once fixed

---

## 7. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Audit | 30 min | 30 min |
| Phase 2: Config | 1 hour | 1.5 hours |
| Phase 3: Service | 1 hour | 2.5 hours |
| Phase 4: Migration | 30 min | 3 hours |
| **Total** | | **2-3 hours** |

---

*Plan created based on SSOT violation analysis - Notification config scattered*
