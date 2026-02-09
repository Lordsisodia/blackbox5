# Feature F-012: API Gateway & External Service Integration

**Status:** Implemented
**Priority:** Medium (Score: 12.0)
**Estimated Complexity:** Medium-High
**Created:** 2026-02-01
**Delivered:** 2026-02-01

---

## Overview

API Gateway and External Service Integration layer to enable RALF to expose REST APIs, handle authentication, and integrate with external services (Slack, Jira, Trello, etc.).

---

## Problem Statement

**Current Issues:**
- RALF is isolated from external tools (Slack, Jira, Trello, etc.)
- No programmatic access to RALF capabilities
- Cannot trigger RALF workflows from external events
- No way to send notifications to external systems

**Impact:**
- Manual coordination required for external integrations
- No real-time notifications to team chat
- Cannot sync tasks with external project management tools
- Limited visibility into RALF operations from external systems

---

## Objectives

### Primary Goals
1. Expose RALF capabilities via REST API
2. Enable secure authentication and authorization
3. Provide webhook support for external events
4. Implement service connectors for popular tools (Slack, Jira, Trello)
5. Create extensible framework for future connectors

### Success Metrics
- API uptime > 99%
- API response time < 100ms (p95)
- Authentication success rate > 95%
- Webhook processing success rate > 90%
- Connector notification success rate > 85%

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway Layer                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  API Server  │  │ API Auth     │  │ Webhook      │      │
│  │  (Flask)     │  │ (API Keys)   │  │ Receiver     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                            │                                 │
│                            v                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Service Connectors Layer                 │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │                                                        │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │   │
│  │  │  Slack   │  │  Jira    │  │  Trello  │          │   │
│  │  │Connector │  │Connector │  │Connector │          │   │
│  │  └──────────┘  └──────────┘  └──────────┘          │   │
│  │                                                        │   │
│  └──────────────────────────────────────────────────────┘   │
│                            │                                 │
└────────────────────────────┼─────────────────────────────────┘
                             │
                             v
┌─────────────────────────────────────────────────────────────┐
│                     RALF Core System                         │
│  (Tasks, Queue, Events, Metrics, Knowledge Base)            │
└─────────────────────────────────────────────────────────────┘
```

### Component Details

#### 1. API Server (`api_server.py`)
- **Framework:** Flask (lightweight, mature, easy to deploy)
- **Port:** 5000 (configurable)
- **Endpoints:**
  - `GET /health` - Health check
  - `GET /api/v1/tasks` - List all tasks
  - `GET /api/v1/tasks/:id` - Get task details
  - `POST /api/v1/tasks` - Create new task
  - `PUT /api/v1/tasks/:id` - Update task
  - `GET /api/v1/queue` - Get queue status
  - `GET /api/v1/metrics` - System metrics
- **Features:** CORS support, error handling, request logging

#### 2. API Authentication (`api_auth.py`)
- **Method:** API Key-based authentication
- **Features:**
  - API key validation
  - Rate limiting (100 requests/minute)
  - Request logging
  - Security headers

#### 3. Webhook Receiver (`webhook_receiver.py`)
- **Endpoint:** `POST /api/v1/webhooks/:service`
- **Services:** slack, jira, trello, github, custom
- **Features:**
  - Payload validation and parsing
  - Signature verification (HMAC-SHA256)
  - Trigger RALF workflows based on events
  - Event logging

#### 4. Service Connectors

##### Base Connector (`base_connector.py`)
- Abstract base class for all connectors
- Common interface and utilities
- Error handling and retry logic

##### Slack Connector (`slack_connector.py`)
- **Features:**
  - Send notifications to channels
  - Post messages as bot
  - Upload files
  - Slash command integration
- **API:** Slack Web API and Incoming Webhooks

##### Jira Connector (`jira_connector.py`)
- **Features:**
  - Create issues from RALF tasks
  - Update issue status
  - Add comments to issues
  - Sync task progress
- **API:** Jira REST API

##### Trello Connector (`trello_connector.py`)
- **Features:**
  - Create cards from RALF tasks
  - Update card status
  - Add comments to cards
  - Move cards between lists
- **API:** Trello REST API

---

## API Specification

### Authentication
All API endpoints (except `/health`) require authentication via API key.

**Header:**
```
X-API-Key: your-api-key-here
```

### Endpoints

#### 1. Health Check
```
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-02-01T12:00:00Z"
}
```

#### 2. List Tasks
```
GET /api/v1/tasks?status=pending&limit=10
```
**Response:**
```json
{
  "tasks": [
    {
      "id": "TASK-001",
      "title": "Implement feature X",
      "status": "pending",
      "priority": "high"
    }
  ],
  "total": 1
}
```

#### 3. Get Task Details
```
GET /api/v1/tasks/TASK-001
```
**Response:**
```json
{
  "id": "TASK-001",
  "title": "Implement feature X",
  "status": "pending",
  "priority": "high",
  "objective": "...",
  "success_criteria": [...]
}
```

#### 4. Create Task
```
POST /api/v1/tasks
Content-Type: application/json

{
  "title": "New task",
  "type": "implement",
  "priority": "medium",
  "objective": "...",
  "approach": "..."
}
```

#### 5. Get Queue Status
```
GET /api/v1/queue
```
**Response:**
```json
{
  "depth": 5,
  "tasks": [...],
  "last_updated": "2026-02-01T12:00:00Z"
}
```

#### 6. Get System Metrics
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

#### 7. Webhook Receiver
```
POST /api/v1/webhooks/:service
Content-Type: application/json
X-Webhook-Signature: sha256=...

{
  "event": "task.created",
  "data": {...}
}
```

---

## Configuration

### Configuration File: `~/.blackbox5/api-config.yaml`

```yaml
# API Server Configuration
server:
  host: "localhost"
  port: 5000
  debug: false
  cors_enabled: true
  cors_origins:
    - "http://localhost:3000"
    - "https://dashboard.blackbox5.com"

# Authentication
auth:
  api_keys:
    - name: "default"
      key: "your-api-key-here"
      scopes:
        - "read:tasks"
        - "write:tasks"
        - "read:metrics"
  rate_limit:
    enabled: true
    requests_per_minute: 100

# Webhook Configuration
webhooks:
  secret: "your-webhook-secret-here"
  signature_algorithm: "sha256"
  services:
    slack:
      enabled: true
    jira:
      enabled: false
    trello:
      enabled: false

# Service Connectors
connectors:
  slack:
    enabled: true
    webhook_url: "https://hooks.slack.com/services/..."
    bot_token: "xoxb-..."
    default_channel: "#ralf-notifications"

  jira:
    enabled: false
    base_url: "https://your-domain.atlassian.net"
    username: "your-email@example.com"
    api_token: "your-api-token"
    project_key: "RALF"

  trello:
    enabled: false
    api_key: "your-api-key"
    api_secret: "your-api-secret"
    token: "your-token"
    default_board: "Your Board Name"
    default_list: "To Do"
```

---

## Security Considerations

### API Security
1. **API Keys:** Never commit to version control
2. **Rate Limiting:** Prevent API abuse and DoS attacks
3. **CORS:** Configure allowed origins
4. **HTTPS:** Use in production (TLS termination)
5. **Input Validation:** Validate all request inputs

### Webhook Security
1. **Signature Verification:** HMAC-SHA256 signatures
2. **Timestamp Validation:** Reject old webhooks (> 5 minutes)
3. **Payload Validation:** JSON schema validation
4. **Replay Protection:** nonce or timestamp-based

### Connector Security
1. **Token Storage:** Store in environment variables or encrypted config
2. **Least Privilege:** Use minimal required scopes
3. **Secret Rotation:** Rotate tokens regularly
4. **Error Handling:** Don't leak sensitive data in errors

---

## Testing

### Unit Tests
- API endpoint handlers
- Authentication logic
- Rate limiting
- Webhook parsing
- Connector methods

### Integration Tests
- End-to-end API calls
- Webhook delivery
- Connector API calls (mocked)

### Load Tests
- Concurrent requests
- Rate limiting
- Webhook burst handling

---

## Deployment

### Development
```bash
# Install dependencies
pip install flask pyyaml requests

# Copy config template
cp 2-engine/.autonomous/config/api-config.yaml ~/.blackbox5/api-config.yaml

# Edit config with your API keys
vim ~/.blackbox5/api-config.yaml

# Start server
python -m 2-engine/.autonomous/lib/api_server
```

### Production
```bash
# Use gunicorn for production
pip install gunicorn

# Start with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 \
  "2_engine.autonomous.lib.api_server:app"
```

### Systemd Service
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
  "2_engine.autonomous.lib.api_server:app"
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## Future Enhancements

### Phase 2 (Nice-to-Have)
- WebSocket support for real-time updates
- OpenAPI/Swagger documentation
- GraphQL endpoint
- Additional connectors (GitHub, Discord, Email)
- Webhook retry queue
- API request analytics

### Phase 3 (Advanced)
- API versioning (v1, v2)
- OAuth2 authentication
- Batch operations
- Webhook subscriptions
- Custom connector plugins
- API marketplace

---

## Dependencies

### Python Packages
- `flask` - Web framework
- `pyyaml` - Configuration parsing
- `requests` - HTTP client for connectors
- `gunicorn` - Production WSGI server (optional)

### System Requirements
- Python 3.8+
- 512MB RAM minimum
- Network access for external connectors

### Internal Dependencies
- Task management system
- Queue management
- Event system (events.yaml)
- Metrics collection (F-008)

---

## Troubleshooting

### Common Issues

**1. API returns 401 Unauthorized**
- Check API key in config
- Verify X-API-Key header
- Check rate limiting logs

**2. Webhook signature verification fails**
- Verify webhook secret matches
- Check signature algorithm (sha256)
- Ensure payload not modified

**3. Connector notification fails**
- Check connector API credentials
- Verify network connectivity
- Check connector service status

**4. High memory usage**
- Reduce Flask worker count
- Enable request logging debug
- Check for connection leaks

---

## Success Criteria Tracking

### Must-Have (P0)
- [x] HTTP server running and accessible
- [x] Authentication with API keys working
- [x] Core API endpoints functional (health, tasks, queue, metrics)
- [x] Webhook receiver can parse payloads
- [x] Configuration file for API settings
- [x] Error handling for invalid requests

### Should-Have (P1)
- [x] Slack connector sending notifications
- [x] Jira connector creating issues
- [x] Trello connector creating cards
- [x] Generic connector framework implemented
- [x] Rate limiting and security headers

### Nice-to-Have (P2)
- [ ] WebSocket support for real-time updates
- [ ] OpenAPI/Swagger documentation
- [ ] Additional connectors (GitHub, Discord, Email)

**Completion:** 11/14 criteria met (79%)
- P0: 6/6 (100%)
- P1: 5/5 (100%)
- P2: 0/3 (0%)

---

## Maintenance

### Log Files
- API access logs: `~/.blackbox5/logs/api-access.log`
- Error logs: `~/.blackbox5/logs/api-errors.log`
- Webhook logs: `~/.blackbox5/logs/webhooks.log`

### Monitoring
- API uptime: Check `/health` endpoint
- Request rate: Monitor access logs
- Error rate: Monitor error logs
- Connector success: Check connector logs

### Backups
- Configuration: Backup `api-config.yaml`
- API keys: Rotate monthly
- Connector tokens: Rotate quarterly

---

## End of Specification
