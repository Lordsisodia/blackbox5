# SUBTASK-004C: Build bb5-watch Daemon

**Parent Task:** TASK-AUTONOMY-004
**Depends On:** SUBTASK-004A (Core Library), SUBTASK-004B (bb5-health)
**Status:** pending
**Priority:** HIGH
**Estimated Tokens:** 45K

---

## Objective

Create the `bb5-watch` daemon for continuous 24/7 monitoring with Telegram alerts. Runs on VPS and notifies when issues are detected.

---

## Success Criteria

- [ ] `bb5-watch start` runs daemon in background
- [ ] `bb5-watch stop` stops daemon
- [ ] `bb5-watch status` shows daemon status
- [ ] Telegram alerts sent for critical issues
- [ ] Configuration file supports all alert channels
- [ ] Systemd service file for auto-start
- [ ] Handles graceful shutdown

---

## Implementation Plan

### Step 1: Daemon Architecture (5K tokens)
Create `~/.blackbox5/bin/bb5-watch`:

```python
#!/usr/bin/env python3
"""BB5 Watch - Continuous monitoring daemon"""
import click
import daemon
import pidfile

@click.group()
def cli():
    """BB5 monitoring daemon"""
    pass

@cli.command()
@click.option('--config', '-c', default='~/.bb5/watch-config.yaml')
@click.option('--foreground', '-f', is_flag=True)
def start(config, foreground):
    """Start the monitoring daemon"""
    pass

@cli.command()
def stop():
    """Stop the monitoring daemon"""
    pass

@cli.command()
def status():
    """Show daemon status"""
    pass

@cli.command()
def config():
    """Edit configuration"""
    pass
```

### Step 2: Configuration System (6K tokens)
Create `~/.blackbox5/config/watch-config.yaml`:

```yaml
daemon:
  check_interval_seconds: 30
  health_score_threshold: 60
  alert_cooldown_seconds: 300  # 5 minutes between same alert

checks:
  agents:
    enabled: true
    heartbeat_timeout_seconds: 120
    alert_on_stuck: true

  queue:
    enabled: true
    alert_on_backlog_threshold: 20
    alert_on_empty: false

  tasks:
    enabled: true
    stuck_task_multiplier: 2.0  # >2x estimate = stuck

  system:
    enabled: true
    cpu_warning: 80
    cpu_critical: 95
    memory_warning: 80
    memory_critical: 95

alerts:
  telegram:
    enabled: true
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    chat_id: "${TELEGRAM_CHAT_ID}"
    min_severity: warning

  webhook:
    enabled: false
    url: "${WEBHOOK_URL}"
    min_severity: critical

logging:
  level: INFO
  file: ~/.blackbox5/.autonomous/health/watch.log
  max_size_mb: 100
  backup_count: 5
```

### Step 3: Alert Manager (8K tokens)
Create `~/.blackbox5/bin/lib/health_monitor/alerts.py`:

```python
class AlertManager:
    def __init__(self, config):
        self.config = config
        self.cooldowns = {}  # Track last alert time

    def send_alert(self, severity, component, message, context=None):
        """Send alert if not in cooldown"""
        alert_key = f"{severity}:{component}"
        if self._in_cooldown(alert_key):
            return

        if severity == 'critical':
            self._send_telegram(message, priority='high')
            self._send_webhook(message)
        elif severity == 'warning':
            self._send_telegram(message)

    def _send_telegram(self, message, priority='normal'):
        """Send Telegram notification"""
        import telegram
        bot = telegram.Bot(token=self.config.telegram.bot_token)
        bot.send_message(
            chat_id=self.config.telegram.chat_id,
            text=self._format_telegram(message, priority),
            parse_mode='Markdown'
        )
```

Telegram message format:
```
🚨 BB5 ALERT [CRITICAL]

Component: executor
Check: agent_heartbeat
Message: Agent timeout - no heartbeat for 145s

Health Score: 45/100
Queue: 60 pending, 5 in progress
Time: 2026-02-06 14:32:15 UTC

Run: bb5-health --component agents
```

### Step 4: Monitoring Loop (10K tokens)
Create `~/.blackbox5/bin/lib/health_monitor/daemon.py`:

```python
class MonitoringDaemon:
    def __init__(self, config):
        self.config = config
        self.running = False
        self.alert_manager = AlertManager(config)

    def run(self):
        """Main monitoring loop"""
        self.running = True
        while self.running:
            try:
                self._check_all()
                time.sleep(self.config.daemon.check_interval_seconds)
            except Exception as e:
                logger.error(f"Check failed: {e}")

    def _check_all(self):
        """Run all enabled checks"""
        if self.config.checks.agents.enabled:
            self._check_agents()
        if self.config.checks.queue.enabled:
            self._check_queue()
        if self.config.checks.tasks.enabled:
            self._check_tasks()

    def _check_agents(self):
        """Check agent heartbeats"""
        agents = collect_heartbeat()
        for agent in agents:
            if agent.is_stale(self.config.checks.agents.heartbeat_timeout_seconds):
                self.alert_manager.send_alert(
                    severity='critical',
                    component=f'agent:{agent.name}',
                    message=f'Agent {agent.name} timeout - no heartbeat for {agent.seconds_since_seen()}s',
                    context={'agent': agent.to_dict()}
                )

    def _check_tasks(self):
        """Check for stuck tasks"""
        tasks = collect_queue()
        events = collect_events()
        stuck = detect_stuck_tasks(tasks, events,
                                   multiplier=self.config.checks.tasks.stuck_task_multiplier)
        for task in stuck:
            self.alert_manager.send_alert(
                severity='warning',
                component=f'task:{task.id}',
                message=f'Task {task.id} stuck for {task.stuck_duration}',
                context={'task': task.to_dict()}
            )
```

### Step 5: Process Management (6K tokens)
Handle daemon lifecycle:
- PID file at `/var/run/bb5-watch.pid` or `~/.blackbox5/.autonomous/health/watch.pid`
- Signal handlers for graceful shutdown (SIGTERM, SIGINT)
- Status command reads PID file and checks process
- Stop command sends SIGTERM

### Step 6: Systemd Integration (5K tokens)
Create systemd service file:

```ini
# /etc/systemd/system/bb5-watch.service
[Unit]
Description=BB5 Health Monitor Daemon
After=network.target

[Service]
Type=simple
User=shaansisodia
WorkingDirectory=/Users/shaansisodia/.blackbox5
Environment=PYTHONPATH=/Users/shaansisodia/.blackbox5/bin/lib
EnvironmentFile=/Users/shaansisodia/.blackbox5/config/watch.env
ExecStart=/Users/shaansisodia/.blackbox5/bin/bb5-watch start --foreground
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

### Step 7: Log Management (5K tokens)
- Rotating file handler (100MB max, 5 backups)
- Structured logging (JSON format option)
- Separate alert log for audit trail
- Logrotate configuration

---

## Files to Create

1. `~/.blackbox5/bin/bb5-watch` (executable)
2. `~/.blackbox5/bin/lib/health_monitor/alerts.py`
3. `~/.blackbox5/bin/lib/health_monitor/daemon.py`
4. `~/.blackbox5/config/watch-config.yaml` (template)
5. `~/.blackbox5/config/watch-config.example.yaml` (documentation)
6. `~/.blackbox5/.autonomous/health/` (directory for DB and logs)
7. `/etc/systemd/system/bb5-watch.service` (systemd file)

---

## Usage Examples

```bash
# Start daemon
bb5-watch start

# Start in foreground for testing
bb5-watch start --foreground

# Check status
bb5-watch status
# Output: Daemon running (PID 12345), last check: 15s ago, health: 68%

# Stop daemon
bb5-watch stop

# Edit config
bb5-watch config  # Opens $EDITOR

# Test alerts
bb5-watch test-alert telegram
```

---

## Testing

```bash
# Test daemon start/stop
./bb5-watch start --foreground &
sleep 5
./bb5-watch status
./bb5-watch stop

# Test Telegram alert
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_CHAT_ID="your_chat_id"
./bb5-watch test-alert telegram
```

---

## Definition of Done

- [ ] Daemon starts and stops cleanly
- [ ] Status command shows accurate info
- [ ] Telegram alerts work
- [ ] Configuration file is loaded correctly
- [ ] Systemd service works
- [ ] Logs rotate properly
- [ ] Handles signals gracefully
- [ ] Survives BB5 file changes (doesn't crash)
