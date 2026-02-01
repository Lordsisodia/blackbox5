# Decisions - TASK-1769957362

## Decision 1: Web Framework Selection

**Context:** Need HTTP framework for REST API server

**Options Considered:**
1. Flask - Lightweight, mature, simple deployment
2. FastAPI - Modern, async, automatic OpenAPI docs
3. aiohttp - Async, low-level, more complex
4. Django REST - Heavy, batteries-included, overkill

**Selected:** Flask

**Rationale:**
- Lightweight and easy to deploy (single file can run server)
- Mature ecosystem with extensive documentation
- Simple decorator-based routing (@app.route)
- Easy to integrate with existing codebase
- Low learning curve for maintenance
- Sufficient for current needs (async not required)
- FastAPI's async complexity not needed for I/O-bound operations
- aiohttp too low-level for rapid development
- Django REST too heavy for simple API gateway

**Reversibility:** MEDIUM - Would require rewriting api_server.py and api_auth.py decorators, but connector logic remains unchanged

**Impact:** Positive - Faster development, easier deployment, lower resource usage

---

## Decision 2: API Key Authentication

**Context:** Need authentication mechanism for API access

**Options Considered:**
1. API Keys (selected)
2. OAuth2
3. JWT (JSON Web Tokens)
4. Basic Auth

**Selected:** API Key-based authentication

**Rationale:**
- Simple to implement and understand
- Sufficient for internal RALF use case
- Easy to configure in YAML file
- No external dependencies (OAuth provider, token refresh)
- Can be rotated without code changes
- OAuth2 overkill for single-tenant system
- JWT adds complexity (stateless, token expiration, refresh)
- Basic auth less secure (credentials in every request)

**Implementation:**
- API keys stored in config file (hashed with SHA-256)
- Sent via `X-API-Key` header
- Scopes for fine-grained access control
- Rate limiting per API key

**Reversibility:** LOW - Would require rewriting api_auth.py but endpoints unchanged

**Impact:** Positive - Simpler architecture, easier deployment, sufficient security

---

## Decision 3: Rate Limiting Algorithm

**Context:** Need rate limiting to prevent API abuse

**Options Considered:**
1. Sliding Window (selected)
2. Token Bucket
3. Fixed Window
4. Leaky Bucket

**Selected:** Sliding Window algorithm

**Rationale:**
- Prevents bursts better than fixed window
- Simpler than token bucket (no refill logic)
- More accurate than leaky bucket for rate limiting
- In-memory implementation sufficient for single-instance
- Easy to implement with timestamps list
- Token bucket more complex (refill rate, burst capacity)
- Fixed window allows bursts at window boundaries
- Leaky bucket designed for traffic shaping, not rate limiting

**Implementation:**
- Store request timestamps per API key
- Clean timestamps older than 60 seconds
- Count requests in last 60 seconds
- Limit: 100 requests/minute (configurable)

**Reversibility:** LOW - Algorithm internal to RateLimiter class

**Impact:** Positive - Prevents abuse, simple implementation, fair limiting

---

## Decision 4: Abstract Base Connector Pattern

**Context:** Need extensible framework for service connectors

**Options Considered:**
1. Abstract Base Class (selected)
2. Protocol/Interface (Python 3.8+)
3. Duck typing (no base class)
4. Plugin system with entry points

**Selected:** Abstract Base Class with ABC module

**Rationale:**
- Clear contract for connector implementations
- Shared functionality (HTTP retry, error handling)
- Type hints and IDE support
- Easy to add new connectors (inherit from BaseConnector)
- Mixins for optional features (NotificationMixin, WebhookMixin)
- Protocol less explicit (no @abstractmethod)
- Duck typing no contract enforcement
- Plugin system overkill for current needs

**Implementation:**
- BaseConnector abstract class with @abstractmethod
- HTTP retry logic with exponential backoff
- Error classes (ConfigError, AuthError, APIError)
- NotificationMixin for formatted messages
- WebhookMixin for webhook registration

**Reversibility:** LOW - Would only affect new connectors, existing ones unaffected

**Impact:** Positive - Consistent interface, code reuse, extensibility

---

## Decision 5: HMAC-SHA256 for Webhook Signatures

**Context:** Need webhook signature verification

**Options Considered:**
1. HMAC-SHA256 (selected)
2. HMAC-SHA1
3. Ed25519 signatures
4. No signature verification

**Selected:** HMAC-SHA256

**Rationale:**
- Industry standard (GitHub, Slack, Stripe use it)
- Secure against tampering
- Fast computation
- Widely supported
- SHA-1 deprecated (security concerns)
- Ed25519 more complex (key management, less common)
- No verification unacceptable security risk

**Implementation:**
- Shared secret configured in api-config.yaml
- Signature header: `X-Webhook-Signature: sha256=<digest>`
- Verified before processing webhook
- Timestamp validation (reject > 5 minutes old)

**Reversibility:** LOW - Would only affect webhook_receiver.py

**Impact:** Positive - Secure webhook delivery, standard approach

---

## Decision 6: YAML Configuration

**Context:** Need configuration format for API gateway and connectors

**Options Considered:**
1. YAML (selected)
2. JSON
3. TOML
4. Environment variables only

**Selected:** YAML configuration file

**Rationale:**
- Matches existing RALF patterns (other configs use YAML)
- Supports comments (documentation inline)
- More readable than JSON
- Flexible (loose typing, optional values)
- Easy to edit by hand
- JSON no comments (harder to document)
- TOML less common
- Environment variables insufficient for complex config

**Implementation:**
- Config file: `~/.blackbox5/api-config.yaml`
- Template: `2-engine/.autonomous/config/api-config.yaml`
- Sections: server, auth, webhooks, connectors
- Secrets documented but placeholder values

**Reversibility:** LOW - Would only affect config loading code

**Impact:** Positive - Consistent with RALF, documented, maintainable

---

## Decision 7: Slack Connector Implementation Approach

**Context:** Need to send notifications to Slack

**Options Considered:**
1. Incoming Webhooks only
2. Bot API only
3. Both (selected)

**Selected:** Support both Incoming Webhooks and Bot API

**Rationale:**
- Webhooks simpler (just POST message URL)
- Bot API richer (attachments, blocks, file uploads)
- User choice based on complexity needs
- Fallback from webhooks to bot API
- Webhooks sufficient for simple notifications
- Bot API required for interactive features
- Supporting both provides maximum flexibility

**Implementation:**
- Try webhook first if configured
- Fallback to bot API if webhook fails
- Rich message formatting via bot API
- File uploads only via bot API
- User configures one or both

**Reversibility:** LOW - Implementation detail internal to SlackConnector

**Impact:** Positive - Flexibility, simple + advanced use cases

---

## Decision 8: Jira Authentication Method

**Context:** Need to authenticate with Jira API

**Options Considered:**
1. Email + API Token (selected)
2. OAuth 2.0
3. Basic Auth (username/password)
4. PAT (Personal Access Token)

**Selected:** Email + API Token

**Rationale:**
- Recommended by Atlassian
- More secure than password (can revoke tokens)
- Easier than OAuth (no redirect flow)
- API tokens scoped to account
- Basic auth deprecated (security risk)
- OAuth overkill for server-to-server
- PAT not supported by Jira Cloud

**Implementation:**
- Basic auth with email as username, API token as password
- Base64 encoded in Authorization header
- Token generated from Atlassian account settings

**Reversibility:** LOW - Authentication detail internal to JiraConnector

**Impact:** Positive - Secure, recommended approach, easy setup

---

## Decision 9: Trello Board/List Management

**Context:** Need to map RALF tasks to Trello cards

**Options Considered:**
1. User-specified board and list names (selected)
2. Auto-create board and lists
3. Configuration-driven mapping
4. Query Trello for first available board

**Selected:** User specifies board and list names in config

**Rationale:**
- User control over organization
- No auto-creation (unwanted boards/lists)
- Simple configuration (board name, list name)
- Caching of board/list IDs for performance
- Auto-creation intrusive (clutters Trello)
- Config mapping complex for simple use case
- Query for first board unpredictable

**Implementation:**
- Config: `default_board` and `default_list`
- API queries to find board ID by name
- API queries to find list ID by name
- Cache IDs in instance variables

**Reversibility:** LOW - Implementation detail internal to TrelloConnector

**Impact:** Positive - User control, predictable behavior, caching for performance

---

## Decision 10: Placeholder Implementation for Task Endpoints

**Context:** API spec includes task endpoints, but task system integration not in scope

**Options Considered:**
1. Full implementation (read task files)
2. Placeholder endpoints (selected)
3. Skip task endpoints entirely
4. Mock implementation with sample data

**Selected:** Placeholder endpoints with "Not Implemented" responses

**Rationale:**
- API structure complete (endpoints exist)
- Clear that integration is needed
- No false expectations (501 status code)
- Easy to implement later
- Full implementation out of scope (F-012 is API gateway, not task system)
- Skipping breaks API completeness
- Mock implementation misleading

**Implementation:**
- Endpoints return 501 Not Implemented
- Error message: "Task management not fully implemented"
- Ready for future integration

**Reversibility:** LOW - Easy to replace with real implementation

**Impact:** Positive - API complete, clear next steps, no misleading data

---

## Summary of Technical Decisions

| Decision | Selected | Reversibility | Rationale |
|----------|----------|---------------|-----------|
| Web Framework | Flask | Medium | Lightweight, mature, simple |
| Authentication | API Keys | Low | Simple, sufficient, secure |
| Rate Limiting | Sliding Window | Low | Prevents bursts, accurate |
| Connector Pattern | Abstract Base Class | Low | Extensible, code reuse |
| Webhook Security | HMAC-SHA256 | Low | Industry standard, secure |
| Configuration | YAML | Low | Matches RALF patterns |
| Slack Implementation | Webhook + Bot API | Low | Flexibility, simple + rich |
| Jira Auth | Email + Token | Low | Recommended, secure |
| Trello Management | User-specified names | Low | User control, predictable |
| Task Endpoints | Placeholder | Low | API complete, clear scope |

**Key Themes:**
1. Simplicity over complexity when possible
2. Industry standards for security (HMAC, API tokens)
3. User control and configurability
4. Extensibility for future enhancements
5. Clear communication of limitations (placeholders)
6. Matching existing RALF patterns (YAML, structure)
