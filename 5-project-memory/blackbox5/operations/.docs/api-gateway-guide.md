# RALF API Gateway - User Guide

**Version:** 1.0.0
**Feature:** F-012 (API Gateway & External Service Integration)
**Last Updated:** 2026-02-01

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [API Reference](#api-reference)
4. [Service Connectors](#service-connectors)
5. [Webhook Integration](#webhook-integration)
6. [Security](#security)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Configuration](#advanced-configuration)

---

## Overview

The RALF API Gateway provides a REST API for interacting with RALF, integrating with external services (Slack, Jira, Trello), and receiving webhooks. It includes:

- **REST API** for task management, queue status, and metrics
- **Authentication** via API keys with rate limiting
- **Service Connectors** for Slack, Jira, and Trello
- **Webhook Receiver** for external events
- **Security** features (CORS, rate limiting, signature verification)

---

## Quick Start

### Installation

1. **Install dependencies:**

```bash
pip install flask flask-cors pyyaml requests
```

For production deployment:
```bash
pip install gunicorn
```

2. **Copy configuration template:**

```bash
cp 2-engine/.autonomous/config/api-config.yaml ~/.blackbox5/api-config.yaml
```

3. **Edit configuration:**

```bash
vim ~/.blackbox5/api-config.yaml
```

Update at minimum:
- Generate API key: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- Add to `auth.api_keys[0].key`
- Enable and configure connectors as needed

4. **Start the server:**

```bash
# Development
python -m 2_engine.autonomous.lib.api_server

# Or with custom config
python -m 2_engine.autonomous.lib.api_server --config ~/.blackbox5/api-config.yaml

# Production with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 \
  "2_engine.autonomous.lib.api_server:create_app('~/.blackbox5/api-config.yaml')"
```

5. **Test the API:**

```bash
# Health check (no auth)
curl http://localhost:5000/health

# Get tasks (requires API key)
curl -H "X-API-Key: your-api-key-here" \
  http://localhost:5000/api/v1/tasks
```

---

## API Reference

### Authentication

All endpoints except `/health` require authentication via API key.

**Header:**
```
X-API-Key: your-api-key-here
```

**Generate API Key:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

### Endpoints

#### 1. Health Check

```
GET /health
```

No authentication required.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-02-01T12:00:00Z",
  "connectors": {
    "slack": {
      "name": "slack",
      "enabled": true,
      "status": "enabled"
    }
  }
}
```

#### 2. List Tasks

```
GET /api/v1/tasks
```

**Response:**
```json
{
  "tasks": [],
  "total": 0,
  "message": "Task management not fully implemented"
}
```

#### 3. Get Task Details

```
GET /api/v1/tasks/:id
```

**Response:**
```json
{
  "error": "Not Implemented",
  "message": "Task details not implemented"
}
```

#### 4. Create Task

```
POST /api/v1/tasks
Content-Type: application/json
X-API-Key: your-key

{
  "title": "New task",
  "type": "implement",
  "priority": "medium"
}
```

Requires `write:tasks` scope.

#### 5. Get Queue Status

```
GET /api/v1/queue
```

**Response:**
```json
{
  "depth": 0,
  "tasks": [],
  "last_updated": "2026-02-01T12:00:00Z"
}
```

#### 6. Get Metrics

```
GET /api/v1/metrics
```

**Response:**
```json
{
  "tasks_completed": 100,
  "success_rate": 0.95,
  "average_duration": 300,
  "uptime": "99.9%"
}
```

#### 7. List Connectors

```
GET /api/v1/connectors
```

**Response:**
```json
{
  "connectors": {
    "slack": {
      "name": "slack",
      "enabled": true,
      "status": "enabled"
    }
  },
  "total": 1
}
```

#### 8. Test Connector

```
POST /api/v1/connectors/:name/test
```

**Response:**
```json
{
  "success": true,
  "message": "Slack connection successful"
}
```

#### 9. Send Notification

```
POST /api/v1/connectors/:name/notify
Content-Type: application/json

{
  "message": "Hello from RALF!",
  "params": {
    "channel": "#general"
  }
}
```

---

## Service Connectors

### Slack Connector

#### Setup

1. **Create Incoming Webhook:**
   - Go to https://api.slack.com/messaging/webhooks
   - Create new webhook
   - Copy webhook URL

2. **Or Create Bot App:**
   - Go to https://api.slack.com/apps
   - Create new app
   - Enable bot user
   - Install to workspace
   - Copy bot token

3. **Configure:**

```yaml
connectors:
  slack:
    enabled: true
    webhook_url: "https://hooks.slack.com/services/..."
    bot_token: "xoxb-..."
    default_channel: "#ralf-notifications"
```

#### Usage

**Send simple message:**
```python
from connectors import SlackConnector

connector = SlackConnector(config={
    'enabled': True,
    'webhook_url': 'https://hooks.slack.com/services/...'
})

result = connector.send_notification('Hello from RALF!')
```

**Send formatted message:**
```python
result = connector.send_formatted_message(
    title='Task Completed',
    message='TASK-001 has been completed successfully',
    level='success',
    metadata={'task_id': 'TASK-001', 'duration': '300s'}
)
```

**Send rich message:**
```python
result = connector.send_rich_message(
    title='Task Update',
    fields=[
        {'title': 'Task ID', 'value': 'TASK-001'},
        {'title': 'Status', 'value': 'In Progress'},
        {'title': 'Assignee', 'value': 'RALF'}
    ],
    color='good'
)
```

**Upload file:**
```python
result = connector.upload_file(
    file_content='File content here',
    filename='report.txt',
    title='Task Report',
    channels=['#general']
)
```

### Jira Connector

#### Setup

1. **Get API Token:**
   - Go to https://id.atlassian.com/manage-profile/security/api-tokens
   - Create API token
   - Copy token

2. **Configure:**

```yaml
connectors:
  jira:
    enabled: true
    base_url: "https://your-domain.atlassian.net"
    email: "your-email@example.com"
    api_token: "your-api-token"
    project_key: "RALF"
    default_issue_type: "Task"
```

#### Usage

**Create issue:**
```python
from connectors import JiraConnector

connector = JiraConnector(config={
    'enabled': True,
    'base_url': 'https://your-domain.atlassian.net',
    'email': 'your-email@example.com',
    'api_token': 'your-token',
    'project_key': 'RALF'
})

result = connector.create_issue(
    task_id='TASK-001',
    summary='Implement feature X',
    description='Detailed description here',
    priority='High',
    labels=['feature', 'backend']
)
```

**Update issue status:**
```python
result = connector.update_issue_status(
    issue_key='RALF-123',
    status='In Progress'
)
```

**Add comment:**
```python
result = connector.add_comment(
    issue_key='RALF-123',
    comment='Task completed successfully'
)
```

**Search issues:**
```python
result = connector.search_issues(
    jql='project = RALF AND status = "In Progress"',
    max_results=50
)
```

### Trello Connector

#### Setup

1. **Get API Key:**
   - Go to https://trello.com/app-key
   - Copy API key

2. **Authorize Token:**
   - Click "Token" link
   - Authorize application
   - Copy token

3. **Configure:**

```yaml
connectors:
  trello:
    enabled: true
    api_key: "your-api-key"
    token: "your-token"
    default_board: "RALF Tasks"
    default_list: "To Do"
```

#### Usage

**Create card:**
```python
from connectors import TrelloConnector

connector = TrelloConnector(config={
    'enabled': True,
    'api_key': 'your-key',
    'token': 'your-token',
    'default_board': 'RALF Tasks'
})

result = connector.create_card(
    task_id='TASK-001',
    name='Implement feature X',
    description='Detailed description',
    list_name='To Do',
    labels=['feature', 'backend']
)
```

**Update card status:**
```python
result = connector.update_card_status(
    card_id='card-id-here',
    list_name='In Progress'
)
```

**Add comment:**
```python
result = connector.add_comment(
    card_id='card-id-here',
    comment='Task completed'
)
```

---

## Webhook Integration

### Setup

1. **Generate webhook secret:**

```python
import secrets
print(secrets.token_urlsafe(32))
```

2. **Configure in api-config.yaml:**

```yaml
webhooks:
  secret: "your-webhook-secret"
  signature_algorithm: "sha256"
  services:
    slack:
      enabled: true
```

3. **Register webhook URL with external service:**

```
https://your-domain.com/api/v1/webhooks/slack
```

### Webhook Signature Verification

Webhooks are signed using HMAC-SHA256.

**Signature header:** `X-Webhook-Signature: sha256=<signature>`

**Verify signature (Python example):**
```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    expected = signature.split('=')[1]
    mac = hmac.new(secret.encode(), payload, hashlib.sha256)
    calculated = mac.hexdigest()
    return hmac.compare_digest(calculated, expected)
```

### Receiving Webhooks

Webhook endpoint:
```
POST /api/v1/webhooks/:service
```

**Request:**
```json
{
  "event": "task.created",
  "data": {
    "task_id": "TASK-001",
    "title": "New task"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "service": "slack",
  "handlers_called": 1
}
```

---

## Security

### API Key Management

**Generate strong keys:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

**Best practices:**
- Use different keys for different applications
- Rotate keys regularly (monthly)
- Use minimal scopes
- Never commit keys to git
- Use environment variables in production

### Rate Limiting

Configure in `api-config.yaml`:
```yaml
auth:
  rate_limit:
    enabled: true
    requests_per_minute: 100
```

**Rate limit headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1643724000
```

**Rate limit exceeded response:**
```json
{
  "error": "Too Many Requests",
  "message": "Rate limit exceeded",
  "rate_limit": {
    "enabled": true,
    "limit": 100,
    "remaining": 0,
    "reset": 1643724000
  }
}
```

### CORS Configuration

Configure allowed origins:
```yaml
server:
  cors_enabled: true
  cors_origins:
    - "http://localhost:3000"
    - "https://dashboard.blackbox5.com"
```

### Security Headers

The API automatically adds:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000`

---

## Troubleshooting

### Common Issues

**1. API returns 401 Unauthorized**
- Check API key in config
- Verify `X-API-Key` header
- Check key has required scopes

**2. API returns 429 Too Many Requests**
- Rate limit exceeded
- Wait until reset time
- Increase rate limit in config

**3. Connector not working**
- Check connector enabled in config
- Verify credentials
- Test connector: `POST /api/v1/connectors/:name/test`
- Check logs: `~/.blackbox5/logs/api-errors.log`

**4. Webhook signature verification fails**
- Verify webhook secret matches
- Check signature format: `sha256=...`
- Ensure payload not modified

**5. CORS errors**
- Add origin to cors_origins
- Check browser console for preflight errors

### Logs

**API access log:** `~/.blackbox5/logs/api-access.log`
**Error log:** `~/.blackbox5/logs/api-errors.log`
**Webhook log:** `~/.blackbox5/logs/webhooks.log`

**Enable file logging:**
```yaml
logging:
  level: "DEBUG"
  file: "~/.blackbox5/logs/api-server.log"
```

### Testing

**Test API manually:**
```bash
# Health check
curl http://localhost:5000/health

# Get tasks
curl -H "X-API-Key: your-key" http://localhost:5000/api/v1/tasks

# Send Slack notification
curl -X POST \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"message": "Test"}' \
  http://localhost:5000/api/v1/connectors/slack/notify
```

**Test with Python:**
```python
import requests

headers = {'X-API-Key': 'your-key'}
response = requests.get('http://localhost:5000/health', headers=headers)
print(response.json())
```

---

## Advanced Configuration

### Systemd Service

Create `/etc/systemd/system/ralf-api.service`:

```ini
[Unit]
Description=RALF API Gateway
After=network.target

[Service]
Type=simple
User=ralf
WorkingDirectory=/home/ralf/blackbox5
Environment="RALF_CONFIG=/home/ralf/.blackbox5/api-config.yaml"
ExecStart=/usr/bin/python3 -m gunicorn \
  -w 4 -b 0.0.0.0:5000 \
  --access-logfile /var/log/ralf-api/access.log \
  --error-logfile /var/log/ralf-api/error.log \
  "2_engine.autonomous.lib.api_server:create_app('~/.blackbox5/api-config.yaml')"
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable ralf-api
sudo systemctl start ralf-api
sudo systemctl status ralf-api
```

### Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name api.blackbox5.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install flask flask-cors pyyaml requests gunicorn

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "2_engine.autonomous.lib.api_server:create_app()"]
```

**docker-compose.yml:**
```yaml
version: '3'
services:
  api:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ~/.blackbox5:/root/.blackbox5
    environment:
      - RALF_CONFIG=/root/.blackbox5/api-config.yaml
    restart: always
```

### Environment Variables

For production, use environment variables:

```python
import os

config_file = os.getenv('RALF_CONFIG', '~/.blackbox5/api-config.yaml')
api_key = os.getenv('RALF_API_KEY')
slack_webhook = os.getenv('SLACK_WEBHOOK_URL')
```

---

## End of Guide

For more information, see:
- Feature specification: `plans/features/FEATURE-012-api-gateway.md`
- Configuration template: `2-engine/.autonomous/config/api-config.yaml`
- Connector development: `operations/.docs/connector-development-guide.md`
