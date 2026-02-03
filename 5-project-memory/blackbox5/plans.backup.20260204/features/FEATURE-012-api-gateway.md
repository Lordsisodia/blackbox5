# Feature Specification: F-012 API Gateway & External Service Integration

**Version:** 1.0.0
**Status:** planned
**Created:** 2026-02-01
**Task:** TBD
**Priority:** MEDIUM (Score: 12.0 after IMP-001 calibration)
**Estimated:** 180 minutes (~3 hours)
**Actual Expected:** ~12 minutes (15x speedup)
**Value Score:** 6/10
**Effort:** 3 hours (180 min / 60 = 3 hours)
**Category:** Integration

---

## Executive Summary

Implement an API Gateway and External Service Integration layer to enable RALF to expose REST APIs, handle authentication, and integrate with external services (Slack, Jira, Trello, etc.). The gateway provides a unified interface for external systems to interact with RALF, trigger workflows, and receive notifications.

**Strategic Value:**
- **Extensibility:** Easy integration with any external service
- **Interoperability:** Standard REST API for third-party tools
- **Automation:** Webhook triggers from external systems
- **Security:** Centralized authentication and authorization
- **Scalability:** Support multiple service integrations simultaneously

---

## User Value

**Who:** RALF operators, external systems, DevOps engineers

**Problem:**
- RALF is isolated from external tools (Slack, Jira, Trello, etc.)
- No programmatic access to RALF capabilities
- Cannot trigger RALF workflows from external events
- No way to send notifications to external systems
- Manual integration with each service is time-consuming

**Value:**
- **REST API:** Standard HTTP interface for RALF capabilities
- **Service Connectors:** Pre-built integrations for common services (Slack, Jira, Trello)
- **Webhook Support:** Trigger RALF workflows from external events
- **Authentication:** Secure API access with API keys and OAuth
- **Extensibility:** Easy to add new service integrations
- **Time savings:** Reusable connectors reduce integration time by 80%

**Use Cases:**
1. **Slack Notification:** Feature completed → Slack message posted automatically
2. **Jira Sync:** Task created → Jira issue opened with metadata
3. **Trello Card:** Feature spec → Trello card created on board
4. **Custom Webhook:** CI/CD pipeline complete → Trigger RALF workflow

---

## MVP Scope

### Phase 1: Core API Gateway (P0 - Must-Have)

**1. HTTP Server**
- File: `2-engine/.autonomous/lib/api_server.py`
- Framework: Flask or FastAPI (lightweight, async support)
- Endpoints: Health, Task status, Queue info, Metrics
- CORS support for web-based clients

**2. Authentication Layer**
- File: `2-engine/.autonomous/lib/api_auth.py`
- API Keys: Simple key-based authentication
- (Optional) OAuth 2.0: For third-party integrations
- Rate limiting: Prevent API abuse

**3. Core API Endpoints**
```
GET  /health                  - Health check
GET  /api/v1/tasks            - List all tasks
GET  /api/v1/tasks/:id        - Get task details
POST /api/v1/tasks            - Create new task
PUT  /api/v1/tasks/:id        - Update task
GET  /api/v1/queue            - Get queue status
GET  /api/v1/metrics          - System metrics
GET  /api/v1/features         - List features
```

**4. Webhook Receiver**
- File: `2-engine/.autonomous/lib/webhook_receiver.py`
- Generic webhook endpoint: `/api/v1/webhooks/:service`
- Payload validation and parsing
- Trigger RALF workflows based on webhook events

### Phase 2: Service Connectors (P1 - Should-Have)

**5. Slack Connector**
- File: `2-engine/.autonomous/lib/connectors/slack_connector.py`
- Send notifications: Feature completed, task failed, system alerts
- Incoming webhooks: Receive slash commands, interactive messages
- Bot support: (Optional) Interactive bot for task queries

**6. Jira Connector**
- File: `2-engine/.autonomous/lib/connectors/jira_connector.py`
- Create issues from tasks
- Sync task status to Jira status
- Comment on issues with task updates

**7. Trello Connector**
- File: `2-engine/.autonomous/lib/connectors/trello_connector.py`
- Create cards from features
- Move cards across lists based on task status
- Add comments to cards with task progress

**8. Generic Connector Framework**
- File: `2-engine/.autonomous/lib/connectors/base_connector.py`
- Base class for all connectors
- Standard methods: `send()`, `receive()`, `validate()`
- Config mapping for connector settings

### Phase 3: Advanced Features (P2 - Nice-to-Have)

**9. WebSocket Support**
- Real-time updates for task progress
- Live metrics streaming
- Bidirectional communication

**10. API Documentation**
- Auto-generated OpenAPI/Swagger docs
- Interactive API explorer
- Code examples in multiple languages

**11. Connector Library Expansion**
- GitHub (issues, PRs)
- GitLab (issues, MRs)
- Discord (notifications)
- Email (SMTP notifications)
- PagerDuty (alerts)

---

## Success Criteria

### Must-Have (P0)
- [ ] HTTP server running and accessible
- [ ] Authentication with API keys working
- [ ] Core API endpoints functional (health, tasks, queue, metrics)
- [ ] Webhook receiver can parse payloads
- [ ] Configuration file for API settings (`~/.blackbox5/api-config.yaml`)
- [ ] Error handling for invalid requests

### Should-Have (P1)
- [ ] Slack connector sending notifications
- [ ] Jira connector creating issues
- [ ] Trello connector creating cards
- [ ] Generic connector framework implemented
- [ ] Rate limiting and security headers
- [ ] Documentation for API usage

### Nice-to-Have (P2)
- [ ] WebSocket support for real-time updates
- [ ] OpenAPI/Swagger documentation
- [ ] Additional connectors (GitHub, Discord, Email)
- [ ] API usage analytics

---

## Technical Approach

### Architecture

**Component Layers:**
1. **API Layer** (`api_server.py`)
   - HTTP server (Flask/FastAPI)
   - Route definitions and handlers
   - Request/response validation

2. **Authentication Layer** (`api_auth.py`)
   - API key validation
   - Rate limiting
   - Request logging

3. **Business Logic Layer**
   - Task CRUD operations
   - Queue management
   - Metrics calculation

4. **Connector Layer** (`connectors/`)
   - Base connector class
   - Service-specific connectors
   - Webhook handlers

### Data Flow

**External Request → API:**
```
HTTP Request → api_server.py → api_auth.py (validate key) →
Business logic → Response → api_server.py → HTTP Response
```

**RALF Event → External Service:**
```
Task Complete → Event in events.yaml → Connector triggered →
Service API → Notification sent → Result logged
```

**Webhook → RALF Workflow:**
```
External Event → webhook_receiver.py → Parse payload →
Trigger RALF action → Task created/updated → Response
```

### Configuration File

**Location:** `~/.blackbox5/api-config.yaml`

```yaml
api:
  # Server
  host: "127.0.0.1"
  port: 8080
  debug: false

  # Authentication
  auth_type: "api_key"  # api_key, oauth, none
  api_keys:
    - "${RALF_API_KEY}"  # Primary API key

  # Rate Limiting
  rate_limit:
    enabled: true
    requests_per_minute: 60

  # CORS
  cors:
    enabled: true
    origins:
      - "http://localhost:3000"
      - "https://dashboard.blackbox5.com"

# Service Connectors
connectors:
  slack:
    enabled: true
    webhook_url: "${SLACK_WEBHOOK_URL}"
    bot_token: "${SLACK_BOT_TOKEN}"
    channel: "#ralf-updates"
    events:
      - "task_completed"
      - "task_failed"
      - "feature_delivered"

  jira:
    enabled: false
    base_url: "https://your-domain.atlassian.net"
    email: "${JIRA_EMAIL}"
    api_token: "${JIRA_API_TOKEN}"
    project_key: "RALF"
    default_issue_type: "Task"

  trello:
    enabled: false
    api_key: "${TRELLO_API_KEY}"
    token: "${TRELLO_TOKEN}"
    board_id: "${TRELLO_BOARD_ID}"
    default_list: "To Do"

# Webhooks
webhooks:
  # Incoming webhooks (external → RALF)
  incoming:
    - service: "github"
      path: "/api/v1/webhooks/github"
      secret: "${GITHUB_WEBHOOK_SECRET}"
      enabled: true

  # Outgoing webhooks (RALF → external)
  outgoing:
    - event: "task_completed"
      url: "${SLACK_WEBHOOK_URL}"
      enabled: true
```

---

## Files to Create/Modify

### New Files
- `plans/features/FEATURE-012-api-gateway.md` - Feature spec (this file)
- `2-engine/.autonomous/lib/api_server.py` - HTTP server (~250 lines)
- `2-engine/.autonomous/lib/api_auth.py` - Authentication (~150 lines)
- `2-engine/.autonomous/lib/webhook_receiver.py` - Webhook handler (~150 lines)
- `2-engine/.autonomous/lib/connectors/base_connector.py` - Base connector (~100 lines)
- `2-engine/.autonomous/lib/connectors/slack_connector.py` - Slack (~150 lines)
- `2-engine/.autonomous/lib/connectors/jira_connector.py` - Jira (~150 lines)
- `2-engine/.autonomous/lib/connectors/trello_connector.py` - Trello (~120 lines)
- `2-engine/.autonomous/config/api-config.yaml` - Configuration template (~80 lines)
- `~/.blackbox5/api-config.yaml` - User config (created on init)
- `operations/.docs/api-gateway-guide.md` - User guide (~350 lines)
- `operations/.docs/connector-development-guide.md` - Connector dev guide (~200 lines)

### Modified Files
- `2-engine/.autonomous/lib/task_completor.py` - Add connector triggers
- `~/.blackbox5/config.yaml` - Add API gateway settings

---

## Dependencies

**External:**
- (Optional) Slack workspace with webhook URL
- (Optional) Jira instance with API access
- (Optional) Trello account with API key

**Internal:**
- Existing task management system
- Existing queue management
- Existing event system (events.yaml)

**Python Packages:**
- Flask or FastAPI (HTTP framework)
- pyyaml (config parsing)
- requests (HTTP client for connectors)

**Risks:**
- API security (exposed endpoints need authentication)
- Rate limiting abuse (API spam)
- Connector failures (external services unavailable)
- Webhook spoofing (need signature verification)

**Mitigation:**
- Require API key for all endpoints
- Implement rate limiting
- Graceful degradation on connector failures
- Use webhook signature verification

---

## Implementation Plan

### Step 1: Core API Server (45 min)
- Implement `api_server.py` with Flask
- Add health check endpoint
- Test server startup and accessibility

### Step 2: Authentication Layer (30 min)
- Implement `api_auth.py` with API key validation
- Add rate limiting
- Test authentication (valid key, invalid key, rate limit exceeded)

### Step 3: Core API Endpoints (45 min)
- Implement task endpoints (list, get, create, update)
- Implement queue endpoint
- Implement metrics endpoint
- Test with curl/Postman

### Step 4: Webhook Receiver (30 min)
- Implement `webhook_receiver.py`
- Add payload validation
- Test with sample webhook payload

### Step 5: Slack Connector (30 min)
- Implement `slack_connector.py`
- Add notification triggers in task completion
- Test with Slack webhook URL

### Step 6: Configuration and Docs (30 min)
- Create `api-config.yaml` template
- Write setup guide in `operations/.docs/api-gateway-guide.md`
- Document authentication setup

### Step 7: Testing and Validation (15 min)
- End-to-end test: Create task via API → Verify task created
- Test connector: Complete task → Verify Slack notification
- Test webhook: Send webhook → Verify workflow triggered
- Document any issues or workarounds

**Total Estimated Time:** 225 minutes (~3.75 hours of actual work)
**With 15x Speedup:** Expected ~15 minutes

---

## Rollout Plan

**Phase 1: Core API** (Loop 22)
- Implement API server and authentication
- Deploy locally for testing
- No external connectors enabled

**Phase 2: Slack Integration** (Loop 23)
- Enable Slack connector
- Monitor notifications for 5-10 tasks
- Fix any issues discovered

**Phase 3: Multi-Connector** (Loop 24+)
- Enable Jira and Trello connectors
- Add more connectors as needed
- Optimize and refine

---

## Metrics

**Success Metrics:**
- API uptime > 99% (reliable service)
- API response time < 100ms (p95 latency)
- Authentication success rate > 95% (valid keys)
- Webhook processing success rate > 90% (valid webhooks)
- Connector notification success rate > 85% (messages delivered)

**Quality Metrics:**
- API endpoint coverage > 80% (all core operations exposed)
- Connector test coverage > 70% (reliable integrations)
- Documentation completeness > 90% (all endpoints documented)

---

## Open Questions

1. **HTTP Framework:** Flask (simple, mature) or FastAPI (modern, async)?
   - **Recommendation:** Flask (simpler, async not critical for our use case)

2. **Authentication Strategy:** API keys only or OAuth 2.0 also?
   - **Recommendation:** API keys only for MVP, OAuth deferred to Phase 2

3. **Connector Priority:** Which connectors to implement first?
   - **Recommendation:** Slack (highest value, simplest), Jira (common), Trello (nice-to-have)

4. **WebSocket Support:** Is real-time updates critical?
   - **Recommendation:** Defer to Phase 2 (polling sufficient for MVP)

---

## Related Documents

- `plans/features/FEATURE-008-realtime-dashboard.md` - Real-time dashboard (API consumer)
- `plans/features/FEATURE-011-github-integration.md` - GitHub integration (similar pattern)
- `operations/.docs/api-gateway-guide.md` - User guide (to be created)
- `operations/.docs/connector-development-guide.md` - Connector dev guide (to be created)

---

## Change Log

| Date | Change | Version |
|------|--------|---------|
| 2026-02-01 | Initial feature specification created | 1.0.0 |
