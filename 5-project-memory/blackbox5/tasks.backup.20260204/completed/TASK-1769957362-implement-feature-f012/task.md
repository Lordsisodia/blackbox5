# TASK-[ID]: Implement Feature F-012 (API Gateway & External Service Integration)

**Type:** implement
**Priority:** medium
**Status:** pending
**Created:** 2026-02-01T14:50:00Z
**Feature ID:** F-012
**Estimated:** 180 minutes (~3 hours)
**Priority Score:** 12.0 (calibrated with IMP-001: (6 × 10) / (3 / 6))

## Objective

Implement API Gateway and External Service Integration layer to enable RALF to expose REST APIs, handle authentication, and integrate with external services (Slack, Jira, Trello, etc.).

## Context

**Why this matters now:**
- RALF is isolated from external tools (Slack, Jira, Trello, etc.)
- No programmatic access to RALF capabilities
- Cannot trigger RALF workflows from external events
- No way to send notifications to external systems

**User Value:**
- **Who:** RALF operators, external systems, DevOps engineers
- **Problem:** RALF can't integrate with external services. No API access or webhook support.
- **Value:** REST API for RALF capabilities, pre-built service connectors (Slack, Jira, Trello), webhook triggers for external events. Extensible framework reduces integration time by 80%.

## Success Criteria

### Must-Have (P0)
- [ ] HTTP server running and accessible
- [ ] Authentication with API keys working
- [ ] Core API endpoints functional (health, tasks, queue, metrics)
- [ ] Webhook receiver can parse payloads
- [ ] Configuration file for API settings
- [ ] Error handling for invalid requests

### Should-Have (P1)
- [ ] Slack connector sending notifications
- [ ] Jira connector creating issues
- [ ] Trello connector creating cards
- [ ] Generic connector framework implemented
- [ ] Rate limiting and security headers

### Nice-to-Have (P2)
- [ ] WebSocket support for real-time updates
- [ ] OpenAPI/Swagger documentation
- [ ] Additional connectors (GitHub, Discord, Email)

## Approach

1. **Create HTTP Server**
   - File: `2-engine/.autonomous/lib/api_server.py`
   - Framework: Flask (lightweight, mature)
   - Endpoints: Health, Task status, Queue info, Metrics
   - CORS support for web-based clients

2. **Implement Authentication Layer**
   - File: `2-engine/.autonomous/lib/api_auth.py`
   - API Keys: Simple key-based authentication
   - Rate limiting: Prevent API abuse
   - Request logging

3. **Implement Core API Endpoints**
   - GET /health - Health check
   - GET /api/v1/tasks - List all tasks
   - GET /api/v1/tasks/:id - Get task details
   - POST /api/v1/tasks - Create new task
   - PUT /api/v1/tasks/:id - Update task
   - GET /api/v1/queue - Get queue status
   - GET /api/v1/metrics - System metrics

4. **Implement Webhook Receiver**
   - File: `2-engine/.autonomous/lib/webhook_receiver.py`
   - Generic webhook endpoint: /api/v1/webhooks/:service
   - Payload validation and parsing
   - Trigger RALF workflows based on events

5. **Create Service Connectors**
   - File: `2-engine/.autonomous/lib/connectors/base_connector.py` - Base class
   - File: `2-engine/.autonomous/lib/connectors/slack_connector.py` - Slack notifications
   - File: `2-engine/.autonomous/lib/connectors/jira_connector.py` - Jira issues
   - File: `2-engine/.autonomous/lib/connectors/trello_connector.py` - Trello cards

6. **Create Configuration**
   - File: `~/.blackbox5/api-config.yaml`
   - API server settings (host, port, auth)
   - Connector configurations (Slack webhook, Jira API, Trello API)
   - Rate limiting and CORS settings

7. **Create Documentation**
   - Operations guide: `operations/.docs/api-gateway-guide.md`
   - Connector development: `operations/.docs/connector-development-guide.md`
   - API reference documentation

## Files to Create/Modify

- `plans/features/FEATURE-012-api-gateway.md` - Feature spec (ALREADY CREATED)
- `2-engine/.autonomous/lib/api_server.py` - HTTP server
- `2-engine/.autonomous/lib/api_auth.py` - Authentication layer
- `2-engine/.autonomous/lib/webhook_receiver.py` - Webhook handler
- `2-engine/.autonomous/lib/connectors/base_connector.py` - Base connector
- `2-engine/.autonomous/lib/connectors/slack_connector.py` - Slack connector
- `2-engine/.autonomous/lib/connectors/jira_connector.py` - Jira connector
- `2-engine/.autonomous/lib/connectors/trello_connector.py` - Trello connector
- `2-engine/.autonomous/config/api-config.yaml` - Configuration template
- `~/.blackbox5/api-config.yaml` - User config
- `operations/.docs/api-gateway-guide.md` - User guide
- `operations/.docs/connector-development-guide.md` - Connector dev guide

## Notes

**Dependencies:**
- Python packages: Flask, pyyaml, requests
- Existing task management system
- Existing queue management
- Existing event system (events.yaml)

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

**Estimated Complexity:** Medium-High (4 libraries + 3 connectors + infrastructure)

**Success Metrics:**
- API uptime > 99%
- API response time < 100ms (p95)
- Authentication success rate > 95%
- Webhook processing success rate > 90%
- Connector notification success rate > 85%
