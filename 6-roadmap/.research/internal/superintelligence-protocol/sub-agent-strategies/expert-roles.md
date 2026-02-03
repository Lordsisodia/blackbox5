# Expert Role Definitions

**Purpose:** Specialized agent roles for the Superintelligence Protocol, each optimized for specific cognitive tasks

**Status:** Active Specification

---

## Overview

The Superintelligence Protocol deploys specialized expert agents to analyze problems from multiple dimensions. Each role has:
- **Distinct cognitive specialization** - What they see and how they think
- **Standardized prompt template** - Consistent activation interface
- **Clear decision criteria** - When to deploy this expert
- **Structured output format** - Predictable, actionable results

---

## The 5 Core Expert Roles

| Role | Primary Function | Cognitive Style |
|------|------------------|-----------------|
| **Architect** | System design and structure | Pattern recognition, abstraction |
| **Researcher** | Information gathering | Exploratory, exhaustive |
| **Critic** | Risk analysis and problem identification | Skeptical, adversarial |
| **Implementer** | Code/execution focus | Practical, concrete |
| **Validator** | Testing and verification | Systematic, evidence-based |

---

## 1. Architect

### Scope and Responsibilities

The Architect specializes in **system-level thinking**:
- Designing component relationships and interfaces
- Identifying patterns and abstractions
- Evaluating architectural trade-offs
- Ensuring scalability and maintainability
- Mapping dependencies and integration points

**Key Questions They Answer:**
- What is the optimal structure for this system?
- How do components interact?
- What patterns should we use?
- What are the long-term implications of this design?

### Prompt Template

```markdown
## Role: Architect

You are an expert software architect with 20+ years of experience designing
complex distributed systems. You think in terms of patterns, trade-offs, and
long-term maintainability.

### Task
{{TASK_DESCRIPTION}}

### Context
{{GATHERED_CONTEXT}}

### Your Analysis

Provide your architectural assessment in this format:

#### 1. Structural Analysis
- Current architecture summary
- Key components and their responsibilities
- Data flow patterns

#### 2. Design Options
For each viable approach:
- **Option Name**: Brief description
- **Pros**: 3-5 advantages
- **Cons**: 3-5 disadvantages
- **Best For**: When this option shines

#### 3. Recommendation
- **Primary Recommendation**: Your top choice with rationale
- **Alternative**: Second-best option if primary fails
- **Migration Path**: How to evolve from current to recommended

#### 4. Risk Assessment
- Technical risks
- Scalability concerns
- Integration challenges

#### 5. Implementation Guidance
- Key abstractions to define
- Interface contracts needed
- Critical decision points

### Constraints to Consider
- {{CONSTRAINT_1}}
- {{CONSTRAINT_2}}
- {{CONSTRAINT_3}}

### Output Rules
- Be specific about patterns (name the pattern, don't just describe it)
- Quantify trade-offs where possible
- Consider both immediate and 2-year horizon implications
```

### When to Deploy

| Scenario | Deploy? | Rationale |
|----------|---------|-----------|
| New feature requiring new components | **YES** | Need structural design |
| Refactoring existing system | **YES** | Need migration architecture |
| Performance optimization | Maybe | If architectural changes needed |
| Bug fix in existing code | No | Use Implementer instead |
| Adding test coverage | No | Use Validator instead |
| Researching a technology | No | Use Researcher instead |

**Decision Criteria:**
- Does this change component relationships? -> Deploy Architect
- Are there multiple valid approaches? -> Deploy Architect
- Is technical debt a concern? -> Deploy Architect

### Example Output 1: API Gateway Design

```yaml
architectural_analysis:
  current_state:
    structure: "Monolithic Flask application"
    components:
      - "Web layer (Flask routes)"
      - "Business logic layer"
      - "Data access layer"
    pain_points:
      - "Tight coupling between layers"
      - "No clear API boundaries"
      - "Difficult to scale independently"

  design_options:
    - name: "API Gateway Pattern"
      description: "Introduce gateway layer to route requests to microservices"
      pros:
        - "Clear separation of concerns"
        - "Independent service scaling"
        - "Technology diversity per service"
        - "Better fault isolation"
      cons:
        - "Increased operational complexity"
        - "Network latency between services"
        - "Data consistency challenges"
        - "Need service discovery"
      best_for: "Large team, independent deployment needs"

    - name: "Modular Monolith"
      description: "Keep single deployable but enforce module boundaries"
      pros:
        - "Simpler deployment model"
        - "Lower operational overhead"
        - "Easier testing and debugging"
        - "Can extract to microservices later"
      cons:
        - "Shared database remains bottleneck"
        - "Technology stack locked"
        - "Risk of tight coupling creeping back"
      best_for: "Small-medium team, rapid development phase"

  recommendation:
    primary: "Modular Monolith"
    rationale: |
      Team size (5 developers) doesn't justify microservice overhead.
      Current pain points can be addressed with clear module boundaries
      and internal APIs. Creates foundation for future extraction.
    alternative: "API Gateway Pattern"
    migration_path: |
      Phase 1: Define module boundaries with internal APIs
      Phase 2: Extract database per module
      Phase 3: Consider service extraction if team grows > 10

  risks:
    - category: "Technical"
      risk: "Module boundaries may degrade over time"
      mitigation: "Automated architecture testing with ArchUnit"
    - category: "Scalability"
      risk: "Database remains single bottleneck"
      mitigation: "Read replicas and caching layer"

  implementation_guidance:
    key_abstractions:
      - "ModuleFacade: Clean interface for each module"
      - "EventBus: Async communication between modules"
      - "Repository: Data access abstraction"
    interfaces:
      - "Module API contracts defined in OpenAPI"
      - "Event schemas with versioning"
    decision_points:
      - "Which modules to extract first (prioritize by change frequency)"
      - "Sync vs async communication per use case"
```

### Example Output 2: Real-Time Collaboration Architecture

```yaml
architectural_analysis:
  current_state:
    structure: "Request-response REST API"
    components:
      - "Flask web server"
      - "PostgreSQL database"
      - "Redis cache"
    constraints:
      - "Docker containerized deployment"
      - "Must maintain existing REST API compatibility"

  design_options:
    - name: "WebSocket + Redis Pub/Sub"
      description: "WebSocket connections for real-time, Redis for broadcasting"
      pros:
        - "Low latency updates"
        - "Proven pattern for real-time"
        - "Redis already in stack"
      cons:
        - "WebSocket state management complexity"
        - "Horizontal scaling challenges with sticky sessions"
        - "Connection overhead at scale"

    - name: "Server-Sent Events (SSE) + Event Sourcing"
      description: "SSE for server-to-client, event sourcing for state"
      pros:
        - "Simpler than WebSockets (HTTP-based)"
        - "Natural fit for event-driven architecture"
        - "Automatic reconnection handling"
      cons:
        - "One-way communication only"
        - "Requires event store implementation"
        - "Client-to-server still needs REST"

    - name: "Long Polling (Fallback)"
      description: "HTTP long polling for maximum compatibility"
      pros:
        - "Works everywhere"
        - "No new infrastructure"
        - "Simple implementation"
      cons:
        - "High latency compared to alternatives"
        - "Resource intensive (held connections)"
        - "Not truly real-time"

  recommendation:
    primary: "WebSocket + Redis Pub/Sub"
    rationale: |
      Best balance of real-time performance and implementation complexity.
      Redis Streams (not just pub/sub) provide persistence and replay.
      Can add SSE fallback for specific use cases later.
    migration_path: |
      1. Implement WebSocket server alongside existing API
      2. Add Redis Streams for message persistence
      3. Gradually migrate real-time features
      4. Keep REST API for non-real-time operations

  implementation_guidance:
    key_abstractions:
      - "ConnectionManager: WebSocket lifecycle management"
      - "MessageRouter: Route messages to correct handlers"
      - "PresenceService: Track user/session state"
    interfaces:
      - "WebSocket protocol definition"
      - "Message format (JSON with type field)"
    critical_decisions:
      - "Authentication: JWT in connection params vs cookie"
      - "Scaling: Sticky sessions vs shared connection state"
      - "Fallback strategy: SSE vs long polling"
```

### Example Output 3: Database Migration Strategy

```yaml
architectural_analysis:
  current_state:
    database: "PostgreSQL 13"
    schema: "Single database, 150+ tables"
    pain_points:
      - "No clear domain boundaries"
      - "Cross-table dependencies everywhere"
      - "Schema changes require full deployment"

  design_options:
    - name: "Database per Service"
      description: "Each service owns its database"
      pros:
        - "True service independence"
        - "Technology fit per domain"
        - "Isolated failure domains"
      cons:
        - "Complex data consistency"
        - "Joins across services impossible"
        - "Significant migration effort"

    - name: "Schema per Domain"
      description: "Single database, separate schemas for domains"
      pros:
        - "Logical separation without operational complexity"
        - "Can still do cross-domain queries when needed"
        - "Easier migration path to separate databases"
      cons:
        - "Shared database remains bottleneck"
        - "No technology diversity"
        - "Schema changes still coordinated"

    - name: "Read Replicas with CQRS"
      description: "Separate read models optimized for queries"
      pros:
        - "Read scaling without changing write model"
        - "Optimized query performance"
        - "Can evolve read models independently"
      cons:
        - "Eventual consistency complexity"
        - "Dual data models to maintain"
        - "Requires event sourcing or change data capture"

  recommendation:
    primary: "Schema per Domain + CQRS for reads"
    rationale: |
      Two-phase approach: First, organize by schema to establish boundaries.
      Second, add CQRS read models for performance-critical queries.
      Keeps operational complexity manageable while enabling future extraction.

  implementation_guidance:
    key_abstractions:
      - "DomainSchema: Logical boundary definition"
      - "ReadModel: Denormalized query-optimized views"
      - "ChangeDataCapture: Sync write to read models"
    migration_steps:
      - "1. Identify domain boundaries (user, content, analytics)"
      - "2. Create schemas and move tables incrementally"
      - "3. Implement CDC with Debezium or triggers"
      - "4. Build read models in separate schema"
      - "5. Migrate queries to use read models"
```

---

## 2. Researcher

### Scope and Responsibilities

The Researcher specializes in **information acquisition and synthesis**:
- Gathering facts from multiple sources
- Comparing alternatives objectively
- Finding precedents and examples
- Identifying best practices
- Surfacing hidden constraints

**Key Questions They Answer:**
- What solutions already exist for this problem?
- What are the trade-offs between options?
- What do experts recommend?
- What are the hidden gotchas?

### Prompt Template

```markdown
## Role: Researcher

You are a thorough researcher who exhaustively explores all angles of a problem.
You find relevant information, compare alternatives, and surface facts that
others might miss. You cite sources and quantify where possible.

### Research Question
{{RESEARCH_QUESTION}}

### Context
{{GATHERED_CONTEXT}}

### Your Research

Provide comprehensive research in this format:

#### 1. Existing Solutions
For each solution found:
- **Name**: What it's called
- **Description**: How it works
- **Source**: Where you found it
- **Relevance**: How applicable to our situation

#### 2. Alternative Approaches
Compare at least 3 different approaches:
- Approach name
- Key characteristics
- Pros/cons
- When to use

#### 3. Best Practices
- Industry standards
- Common pitfalls to avoid
- Expert recommendations

#### 4. Precedents
- Similar implementations (with links if available)
- Lessons learned from others
- Case studies

#### 5. Hidden Constraints
- Non-obvious limitations
- Regulatory considerations
- Integration requirements
- Performance implications

#### 6. Recommendation
- **Top Finding**: Most important discovery
- **Key Insight**: What others usually miss
- **Further Research**: What still needs investigation

### Search Guidelines
- Check official documentation first
- Look for recent articles (within 2 years)
- Find multiple perspectives
- Quantify claims with data when possible
```

### When to Deploy

| Scenario | Deploy? | Rationale |
|----------|---------|-----------|
| Evaluating new technology | **YES** | Need comprehensive comparison |
| Unfamiliar problem domain | **YES** | Need to learn from others |
| Making technology choice | **YES** | Need objective comparison |
| Standard implementation task | No | Use Implementer instead |
| Code review | No | Use Critic instead |
| Architecture decision | Maybe | Use Architect for structure, Researcher for options |

**Decision Criteria:**
- Is this a "what should we use?" question? -> Deploy Researcher
- Are there multiple viable technologies? -> Deploy Researcher
- Do we need external data? -> Deploy Researcher

### Example Output 1: Message Queue Technology Research

```yaml
research_findings:
  question: "What message queue technology should we use for event-driven architecture?"

  existing_solutions:
    - name: "Apache Kafka"
      description: "Distributed event streaming platform with high throughput"
      characteristics:
        throughput: "Millions of messages/sec"
        latency: "~10ms at p99"
        persistence: "Disk-based, configurable retention"
        ordering: "Per-partition ordering guarantees"
      best_for:
        - "High throughput event streaming"
        - "Event sourcing architectures"
        - "Log aggregation"
      challenges:
        - "Operational complexity (ZooKeeper/KRaft)"
        - "Consumer group rebalancing delays"
        - "Not ideal for task queues with priorities"
      sources:
        - "Apache Kafka Documentation"
        - "Confluent Benchmarks 2024"

    - name: "RabbitMQ"
      description: "Traditional message broker with rich routing capabilities"
      characteristics:
        throughput: "~50K messages/sec per node"
        latency: "~1ms at p99"
        persistence: "Optional, per-queue configuration"
        routing: "Advanced (topic, headers, direct)"
      best_for:
        - "Complex routing requirements"
        - "Task queues with priorities"
        - "RPC patterns"
      challenges:
        - "Lower throughput than Kafka"
        - "Memory management under load"
        - "Clustering complexity"
      sources:
        - "RabbitMQ Documentation"
        - "CloudAMQP Benchmarks"

    - name: "Redis Streams"
      description: "Log data structure added in Redis 5.0"
      characteristics:
        throughput: "~100K messages/sec"
        latency: "Sub-millisecond"
        persistence: "Redis persistence (RDB/AOF)"
        ordering: "Global ordering per stream"
      best_for:
        - "Already using Redis"
        - "Simple event streaming needs"
        - "Real-time applications"
      challenges:
        - "Memory-bound (not for long retention)"
        - "No built-in consumer groups (must implement)"
        - "Single-node limitation (unless Redis Cluster)"
      sources:
        - "Redis Streams Documentation"
        - "Redis.io use cases"

    - name: "AWS SQS / SNS"
      description: "Managed message queue and pub/sub service"
      characteristics:
        throughput: "Nearly unlimited"
        latency: "~100ms"
        persistence: "Fully managed, 14 day retention"
        scaling: "Automatic"
      best_for:
        - "AWS-native applications"
        - "Don't want to manage infrastructure"
        - "Standard queue patterns"
      challenges:
        - "Vendor lock-in"
        - "Higher latency than self-hosted"
        - "Cost at scale"
      sources:
        - "AWS Documentation"
        - "AWS Pricing Calculator"

  comparison_matrix:
    criteria:
      - "Throughput"
      - "Latency"
      - "Operational Complexity"
      - "Routing Flexibility"
      - "Cost (self-hosted)"
    rankings:
      kafka: [5, 3, 2, 3, 4]
      rabbitmq: [3, 5, 3, 5, 4]
      redis_streams: [4, 5, 4, 2, 5]
      aws_sqs: [5, 2, 5, 3, 3]

  best_practices:
    - "Start with your throughput requirements - most teams overestimate"
    - "Consider operational burden, not just technical capabilities"
    - "Plan for message schema evolution from day one"
    - "Monitor consumer lag as primary health metric"
    - "Implement dead letter queues for failed messages"

  hidden_constraints:
    - "Network partitions: How does each handle split-brain?"
    - "Message ordering: Do you really need global ordering or per-entity?"
    - "Replay capability: Can you reprocess historical messages?"
    - "Exactly-once semantics: Most provide at-least-once, exactly-once is hard"

  recommendation:
    top_finding: |
      Redis Streams is surprisingly capable for moderate throughput needs
      and eliminates infrastructure complexity if already using Redis.
      Many teams jump to Kafka prematurely.
    key_insight: |
      The choice between "log" (Kafka) and "queue" (RabbitMQ) semantics
      is more important than performance benchmarks. Event sourcing needs
      logs; task distribution needs queues.
    further_research:
      - "Benchmark with our actual message sizes and patterns"
      - "Evaluate Pulsar as Kafka alternative with better ops story"
      - "Check if NATS Streaming meets our needs (simpler than Kafka)"
```

### Example Output 2: Authentication Library Research

```yaml
research_findings:
  question: "What authentication library should we use for Python Flask API?"

  existing_solutions:
    - name: "Flask-Login"
      description: "Session-based user authentication for Flask"
      maturity: "Stable, widely used"
      characteristics:
        - "Session-based (server-side sessions)"
        - "User loader callback pattern"
        - "Remember me functionality"
        - "No built-in registration/password reset"
      best_for:
        - "Traditional server-rendered applications"
        - "When you want session management"
      limitations:
        - "Not designed for APIs/JWT"
        - "Requires session storage (Redis, database)"

    - name: "Flask-JWT-Extended"
      description: "JWT authentication for Flask APIs"
      maturity: "Active, well-maintained"
      characteristics:
        - "Access and refresh tokens"
        - "Token freshness checking"
        - "Cookie or header transmission"
        - "Revocation support via blocklist"
      best_for:
        - "API-first applications"
        - "Mobile app backends"
        - "Microservices authentication"

    - name: "Authlib"
      description: "Comprehensive OAuth/OIDC library"
      maturity: "Active, spec-compliant"
      characteristics:
        - "OAuth 1.0, 2.0, OpenID Connect"
        - "Can be client or provider"
        - "JWT implementation included"
        - "Spec-compliant implementations"
      best_for:
        - "Social login integration"
        - "Building OAuth provider"
        - "OpenID Connect needs"

    - name: "Firebase Auth"
      description: "Managed authentication service by Google"
      maturity: "Enterprise-grade"
      characteristics:
        - "Managed user database"
        - "Social providers built-in"
        - "Email/password + verification"
        - "SDKs for all platforms"
      best_for:
        - "Don't want to manage auth infrastructure"
        - "Mobile + web + API consistency"
        - "Need enterprise features (MFA, etc.)"

  comparison:
    flask_login:
      pros: ["Simple", "Well-documented", "Flask-native"]
      cons: ["Not for APIs", "Session storage needed"]
    flask_jwt_extended:
      pros: ["Perfect for APIs", "Flexible", "Active development"]
      cons: ["Token management complexity", "No built-in user management"]
    authlib:
      pros: ["Spec-compliant", "Comprehensive", "Flexible"]
      cons: ["Steeper learning curve", "More than needed for simple cases"]
    firebase_auth:
      pros: ["Zero infrastructure", "Feature-rich", "Scales automatically"]
      cons: ["Vendor lock-in", "Cost at scale", "Offline development harder"]

  hidden_constraints:
    - "GDPR: User data residency requirements may rule out some cloud options"
    - "Token storage: JWT in localStorage vulnerable to XSS"
    - "Refresh strategy: How will you handle token refresh on mobile?"
    - "Logout: True logout requires token blocklist (stateful)"

  recommendation:
    top_finding: |
      Flask-JWT-Extended is the standard for Flask APIs, but requires
      building user management yourself. Firebase Auth is best if you
      want full-featured auth without infrastructure.
    key_insight: |
      Most teams underestimate the complexity of secure token refresh,
      password reset flows, and email verification. These "simple" features
      are why managed solutions often win despite lock-in concerns.
```

### Example Output 3: CSS Framework Research

```yaml
research_findings:
  question: "What CSS framework should we use for new React dashboard?"

  existing_solutions:
    - name: "Tailwind CSS"
      description: "Utility-first CSS framework"
      popularity: "#1 on State of CSS 2024"
      characteristics:
        - "Utility classes (flex, pt-4, text-center)"
        - "Highly customizable via config"
        - "JIT compiler for small bundles"
        - "No pre-built components"
      learning_curve: "Medium (unlearning component classes)"
      bundle_size: "~10KB compressed (tree-shaken)"

    - name: "Material-UI (MUI)"
      description: "React components following Material Design"
      popularity: "Most popular React component library"
      characteristics:
        - "Pre-built React components"
        - "Theming system"
        - "Material Design aesthetics"
        - "Comprehensive component set"
      learning_curve: "Low-Medium"
      bundle_size: "~100KB+ (depends on components used)"

    - name: "Chakra UI"
      description: "Modular React component library"
      popularity: "Growing rapidly"
      characteristics:
        - "Composable component design"
        - "Style props similar to Tailwind"
        - "Accessibility built-in"
        - "Dark mode support"
      learning_curve: "Low"
      bundle_size: "~50KB+ (depends on components)"

    - name: "CSS Modules + PostCSS"
      description: "Write CSS, scope to components"
      popularity: "Stable, widely used"
      characteristics:
        - "Traditional CSS authoring"
        - "Automatic scoping"
        - "No runtime overhead"
        - "Full CSS feature support"
      learning_curve: "Low (if you know CSS)"
      bundle_size: "Depends on your CSS"

  comparison_matrix:
                    | Tailwind | MUI    | Chakra | CSS Modules |
    ----------------|----------|--------|--------|-------------|
    Customization   | High     | Medium | High   | High        |
    Dev Speed       | Medium   | Fast   | Fast   | Slow        |
    Bundle Size     | Small    | Large  | Medium | Minimal     |
    Learning Curve  | Medium   | Low    | Low    | Low         |
    Design Freedom  | High     | Low    | Medium | High        |

  best_practices:
    - "Don't mix utility and component approaches - pick one"
    - "Consider design system needs: Tailwind for custom, MUI for Material"
    - "Factor in team CSS expertise"
    - "Check accessibility features (all three score well)"

  hidden_constraints:
    - "Tailwind requires design system investment (no free components)"
    - "MUI customization can be verbose (override default styles)"
    - "Designer collaboration: Tailwind requires designer to learn utilities"
    - "Migration cost: Hard to switch once committed"

  recommendation:
    top_finding: |
      Tailwind is best for custom-designed products with dedicated design
      resources. MUI/Chakra are better for rapid prototyping or when
      following established design systems.
    key_insight: |
      The "utility vs component" debate misses the real question: Do you
      have design resources? Without a designer, Tailwind leads to
      inconsistent UIs. With a designer, Tailwind enables perfect
      implementation of their vision.
```

---

## 3. Critic

### Scope and Responsibilities

The Critic specializes in **adversarial analysis and risk identification**:
- Finding flaws in proposed solutions
- Identifying edge cases and failure modes
- Challenging assumptions
- Assessing security implications
- Evaluating maintainability risks

**Key Questions They Answer:**
- What could go wrong?
- What assumptions are we making?
- What are the edge cases?
- Is this solution too complex?

### Prompt Template

```markdown
## Role: Critic

You are a skeptical, detail-oriented analyst who finds problems others miss.
Your job is to poke holes in proposals, identify risks, and challenge
assumptions. Be thorough but constructive - your goal is improvement, not
just criticism.

### Proposal to Analyze
{{PROPOSAL_DESCRIPTION}}

### Context
{{GATHERED_CONTEXT}}

### Your Analysis

Provide critical analysis in this format:

#### 1. Assumption Challenge
List key assumptions and challenge each:
- **Assumption**: What was assumed
- **Challenge**: Why it might be wrong
- **Impact**: If assumption fails

#### 2. Failure Modes
Identify ways this could fail:
- **Failure Mode**: What goes wrong
- **Trigger**: What causes it
- **Impact**: Severity (High/Medium/Low)
- **Likelihood**: Probability (High/Medium/Low)
- **Mitigation**: How to prevent or handle

#### 3. Edge Cases
Consider boundary conditions:
- Input extremes (empty, huge, malformed)
- Timing issues (race conditions, ordering)
- Scale limits (what breaks at 10x scale?)
- Environmental variations

#### 4. Complexity Assessment
- **Cyclomatic Complexity**: Estimate or measure
- **Cognitive Load**: How hard to understand
- **Hidden Dependencies**: What relies on this
- **Ripple Effects**: What else changes

#### 5. Security Concerns
- Attack vectors introduced
- Data exposure risks
- Authentication/authorization gaps
- Input validation gaps

#### 6. Maintainability Risks
- Technical debt introduced
- Documentation needs
- Testing challenges
- Knowledge silos created

#### 7. Constructive Recommendations
For each major issue:
- **Issue**: What's wrong
- **Recommendation**: How to fix
- **Priority**: Must/Should/Could fix

### Critical Thinking Prompts
- What would make this fail in production?
- What would a malicious user do?
- What happens at 10x the expected load?
- What if the requirements change?
- What would the next developer struggle with?
```

### When to Deploy

| Scenario | Deploy? | Rationale |
|----------|---------|-----------|
| Major architecture decision | **YES** | Need risk analysis |
| Security-sensitive feature | **YES** | Must find vulnerabilities |
| Complex implementation | **YES** | Need edge case analysis |
| Before production deployment | **YES** | Final safety check |
| Simple bug fix | No | Overkill for small changes |
| Research phase | No | Use Researcher first |
| Greenfield exploration | Maybe | After initial ideas generated |

**Decision Criteria:**
- Is there significant risk if this fails? -> Deploy Critic
- Are there security implications? -> Deploy Critic
- Is the solution complex? -> Deploy Critic

### Example Output 1: API Rate Limiting Implementation

```yaml
critical_analysis:
  proposal: "Implement API rate limiting using Redis with sliding window algorithm"

  assumption_challenges:
    - assumption: "Redis will always be available"
      challenge: |
        Redis can fail, network partition, or be slow under load.
        Current proposal doesn't specify fallback behavior.
      impact: |
        If Redis is down, either all requests fail (denial of service)
        or rate limiting is bypassed (security issue).
      recommendation: |
        Implement circuit breaker pattern. If Redis unavailable,
        either allow requests with reduced limits (fail open) or
        queue for later processing (fail closed) based on risk tolerance.

    - assumption: "Sliding window is the right algorithm"
      challenge: |
        Sliding window requires storing multiple timestamps per client.
        At high scale, this is memory-intensive in Redis.
      impact: |
        Redis memory exhaustion, eviction of rate limit data,
        effectively disabling rate limiting.
      recommendation: |
        Consider token bucket or fixed window for high-scale scenarios.
        Benchmark memory usage before committing to sliding window.

  failure_modes:
    - mode: "Race condition on counter increment"
      trigger: "Concurrent requests from same client"
      impact: "Medium"
      likelihood: "High"
      mitigation: |
        Use Redis Lua script or WATCH/MULTI/EXEC for atomic operations.
        Current GET then INCR approach is racy.

    - mode: "Clock skew between application servers"
      trigger: "Multiple servers with different system clocks"
      impact: "Medium"
      likelihood: "Medium"
      mitigation: |
        Use Redis TIME command for consistent timestamps.
        Or use relative TTLs instead of absolute timestamps.

    - mode: "Redis key explosion"
      trigger: "Unique client identifier per request (e.g., session ID)"
      impact: "High"
      likelihood: "Medium"
      mitigation: |
        Validate client identifier stability.
        Implement key expiration aggressively.
        Monitor Redis key count.

  edge_cases:
    - case: "Client makes burst of requests at window boundary"
      issue: "Sliding window allows 2x rate limit in short period"
      example: "100 req/min limit: 100 at 0:59, 100 at 1:00 = 200 in 1 second"
      mitigation: "Consider strict rate limit or shorter windows"

    - case: "Clock jumps (NTP sync, leap second)"
      issue: "Rate limit calculations become incorrect"
      mitigation: "Use monotonic clocks where possible; accept some drift"

    - case: "Redis memory pressure"
      issue: "Redis evicts rate limit keys; limits reset unexpectedly"
      mitigation: "Separate Redis instance for rate limiting; monitor memory"

  complexity_assessment:
    cyclomatic_complexity: "Medium (3-4 paths: check limit, increment, handle failure)"
    cognitive_load: "High - distributed state reasoning required"
    hidden_dependencies:
      - "Redis availability"
      - "Clock synchronization"
      - "Network latency to Redis"
    ripple_effects:
      - "All API endpoints need decorator/wrapper"
      - "Error responses need rate limit headers"
      - "Monitoring/alerting on rate limit hits"

  security_concerns:
    - concern: "Client identifier spoofing"
      risk: "Attacker uses other client's identifier to exhaust their quota"
      mitigation: "Use authenticated user ID, not IP or header"

    - concern: "Redis injection"
      risk: "If client ID is used in Redis key without sanitization"
      mitigation: "Hash client ID or validate format strictly"

    - concern: "Timing side channel"
      risk: "Response time reveals if rate limit check failed before auth"
      mitigation: "Perform rate limit check after authentication when possible"

  maintainability_risks:
    - risk: "Distributed debugging difficulty"
      description: "Rate limit failures require checking Redis state"
      mitigation: "Comprehensive logging; expose current limit status in headers"

    - risk: "Configuration drift"
      description: "Different endpoints with different limits become confusing"
      mitigation: "Centralized rate limit configuration; clear documentation"

  constructive_recommendations:
    - issue: "No fallback for Redis failure"
      recommendation: "Implement circuit breaker with fail-open or fail-closed strategy"
      priority: "Must"

    - issue: "Race condition in counter"
      recommendation: "Use Redis Lua script for atomic check-and-increment"
      priority: "Must"

    - issue: "Memory usage unbounded"
      recommendation: "Add key expiration; monitor Redis memory; consider algorithm change"
      priority: "Should"

    - issue: "Missing rate limit headers"
      recommendation: "Return X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset headers"
      priority: "Should"
```

### Example Output 2: Database Schema Change

```yaml
critical_analysis:
  proposal: "Add JSONB column 'metadata' to users table for flexible user attributes"

  assumption_challenges:
    - assumption: "JSONB is the right choice over separate columns"
      challenge: |
        JSONB loses type safety, constraints, and indexing efficiency.
        Querying nested JSON is verbose and error-prone.
      impact: |
        Application bugs from malformed data; performance degradation
        on queries that need to filter by metadata fields.
      recommendation: |
        Document which fields truly need flexibility vs structured storage.
        Consider hybrid: common fields as columns, truly dynamic in JSONB.

    - assumption: "Current queries won't be affected"
      challenge: |
        SELECT * queries will now include large JSONB payload.
        ORM may try to parse/deserialize on every load.
      impact: |
        Increased memory usage; slower query performance;
        potential ORM issues.
      recommendation: |
        Audit all SELECT * usage. Update ORM models to lazy-load JSONB.

  failure_modes:
    - mode: "Query performance degradation"
      trigger: "Filtering or sorting by JSONB field"
      impact: "High"
      likelihood: "High"
      mitigation: |
        Create GIN indexes on JSONB fields that will be queried.
        Set query planner hints if needed.

    - mode: "Data corruption on concurrent updates"
      trigger: "Two processes update different metadata keys simultaneously"
      impact: "Medium"
      likelihood: "Medium"
      mitigation: |
        Use JSONB concatenation operators, not read-modify-write.
        Or implement optimistic locking.

    - mode: "Migration failure on large table"
      trigger: "Adding column to table with millions of rows"
      impact: "High"
      likelihood: "Medium"
      mitigation: |
        Use pt-online-schema-change or similar for zero-downtime migration.
        Test migration on production-sized dataset first.

  edge_cases:
    - case: "Metadata exceeds PostgreSQL JSONB limit (1GB)"
      issue: "Insertion fails with error"
      mitigation: "Add application-level size validation before insert"

    - case: "Non-JSON data inserted"
      issue: "PostgreSQL rejects insert"
      mitigation: "Application validation; database constraint if possible"

    - case: "Deeply nested JSON"
      issue: "Query complexity increases; indexing less effective"
      mitigation: "Enforce maximum nesting depth in application"

  complexity_assessment:
    cognitive_load: "High - developers must know which fields are where"
    hidden_dependencies:
      - "All user-related queries may be affected"
      - "Backup/restore processes need JSONB handling"
      - "Analytics queries may break"
    ripple_effects:
      - "API responses may change if metadata exposed"
      - "Data export/import needs JSONB handling"
      - "Reporting queries need updates"

  security_concerns:
    - concern: "No schema validation on JSONB content"
      risk: "Malicious or malformed data stored without detection"
      mitigation: "Add JSON Schema validation in application layer"

    - concern: "Sensitive data in metadata"
      risk: "PII stored in unencrypted JSONB field"
      mitigation: "Encrypt sensitive fields; audit metadata content"

  maintainability_risks:
    - risk: "Implicit schema"
      description: "No single source of truth for what metadata contains"
      mitigation: "Document expected keys; consider JSON Schema"

    - risk: "Query complexity"
      description: "Developers write complex JSONB queries inline"
      mitigation: "Create views or functions for common JSONB access patterns"

  constructive_recommendations:
    - issue: "No validation strategy"
      recommendation: "Implement JSON Schema validation before storage"
      priority: "Must"

    - issue: "Migration strategy unclear"
      recommendation: "Use online schema change tool; test on production data"
      priority: "Must"

    - issue: "Query performance risk"
      recommendation: "Create GIN indexes; benchmark common queries"
      priority: "Should"
```

### Example Output 3: Third-Party Integration

```yaml
critical_analysis:
  proposal: "Integrate with Stripe for payment processing using webhooks"

  assumption_challenges:
    - assumption: "Webhooks will be delivered reliably"
      challenge: |
        Stripe retries webhooks but only for 3 days. Network issues,
        downtime, or bugs can cause missed events.
      impact: |
        Payment state out of sync; customer charged but order not fulfilled
        or vice versa.
      recommendation: |
        Implement reconciliation job that polls Stripe API periodically
        to catch missed webhooks. Design for at-least-once delivery.

    - assumption: "Webhook payload structure is stable"
      challenge: |
        Stripe API versions change. Webhooks sent with different API
        versions have different payload structures.
      impact: |
        Parsing errors; data extraction failures; potential security issues.
      recommendation: |
        Pin webhook API version explicitly. Handle unknown fields gracefully.

  failure_modes:
    - mode: "Webhook endpoint down during deployment"
      trigger: "Deployment coincides with Stripe event"
      impact: "High"
      likelihood: "Medium"
      mitigation: |
        Use rolling deployments with health checks.
        Implement webhook queue for replay capability.

    - mode: "Duplicate webhook delivery"
      trigger: "Stripe retry logic or network issues"
      impact: "High"
      likelihood: "High"
      mitigation: |
        Implement idempotency key check. Store processed event IDs.

    - mode: "Webhook signature verification failure"
      trigger: "Clock skew, wrong secret, or tampering"
      impact: "Medium"
      likelihood: "Low"
      mitigation: |
        Log verification failures. Alert on high failure rate.
        Allow manual verification bypass for recovery.

    - mode: "Database transaction failure after Stripe call"
      trigger: "Database constraint violation or deadlock"
      impact: "High"
      likelihood: "Medium"
      mitigation: |
        Use outbox pattern or saga pattern for distributed transaction.
        Never leave Stripe and local DB in inconsistent state.

  edge_cases:
    - case: "Rapid successive webhooks for same object"
      issue: "Race conditions in webhook processing"
      mitigation: "Object-level locking or serial processing per object"

    - case: "Very large webhook payload"
      issue: "Memory pressure or timeout"
      mitigation: "Stream processing; size limits; async handling"

    - case: "Stripe API rate limit during reconciliation"
      issue: "Cannot sync state"
      mitigation: "Exponential backoff; prioritize critical events"

  security_concerns:
    - concern: "Webhook endpoint exposed to internet"
      risk: "Attackers can send fake webhooks"
      mitigation: |
        Verify Stripe signature on every request.
        Use constant-time comparison to prevent timing attacks.

    - concern: "Webhook secret in environment variables"
      risk: "Secret exposure in logs or process listing"
      mitigation: |
        Use secret management service. Rotate secrets regularly.

    - concern: "Sensitive data in webhook logs"
      risk: "PII or payment data in application logs"
      mitigation: |
        Sanitize logs. Don't log full webhook payloads.

  constructive_recommendations:
    - issue: "No idempotency handling"
      recommendation: "Store processed event IDs; check before processing"
      priority: "Must"

    - issue: "No reconciliation mechanism"
      recommendation: "Daily job to sync payment state with Stripe"
      priority: "Must"

    - issue: "Synchronous webhook processing"
      recommendation: "Queue webhooks for async processing; return 200 immediately"
      priority: "Should"

    - issue: "No API version pinning"
      recommendation: "Pin to specific Stripe API version in webhook settings"
      priority: "Should"
```

---

## 4. Implementer

### Scope and Responsibilities

The Implementer specializes in **practical execution and code generation**:
- Writing production-ready code
- Following existing patterns and conventions
- Making pragmatic trade-offs
- Ensuring code is testable
- Documenting implementation details

**Key Questions They Answer:**
- How do we build this?
- What patterns should we follow?
- What are the implementation details?
- How do we handle errors?

### Prompt Template

```markdown
## Role: Implementer

You are a pragmatic software engineer who writes clean, production-ready code.
You follow existing patterns, handle edge cases, and prioritize working
solutions over perfect ones. You think about maintainability and testing.

### Task
{{IMPLEMENTATION_TASK}}

### Context
{{GATHERED_CONTEXT}}

### Existing Patterns
{{CODE_PATTERNS_FROM_CONTEXT}}

### Your Implementation

Provide implementation in this format:

#### 1. Approach Overview
- High-level strategy
- Key design decisions
- Libraries/frameworks used

#### 2. Code Implementation
```python
# Production-ready code with:
# - Type hints
# - Docstrings
# - Error handling
# - Logging
```

#### 3. Error Handling Strategy
- Expected errors and how handled
- Unexpected errors and logging
- Recovery mechanisms

#### 4. Testing Approach
- Unit test strategy
- Integration test needs
- Edge cases to test

#### 5. Usage Example
```python
# Show how to use the implementation
```

#### 6. Implementation Notes
- Performance considerations
- Thread safety
- Resource cleanup
- Configuration needed

### Constraints
- Follow existing code style
- Match current architecture patterns
- Include proper error handling
- Make it testable
```

### When to Deploy

| Scenario | Deploy? | Rationale |
|----------|---------|-----------|
| Feature implementation | **YES** | Need working code |
| Bug fix | **YES** | Need targeted fix |
| Refactoring | **YES** | Need code transformation |
| Architecture decision | No | Use Architect first |
| Technology evaluation | No | Use Researcher first |
| Security review | No | Use Critic first |

**Decision Criteria:**
- Do we know what to build? -> Deploy Implementer
- Is the design settled? -> Deploy Implementer
- Is this a coding task? -> Deploy Implementer

### Example Output 1: API Endpoint Implementation

```python
# /Users/shaansisodia/.blackbox5/2-engine/api/routes/webhook_handler.py
"""
Stripe webhook handler for payment events.

Follows the pattern established in other webhook handlers:
- Async processing via queue
- Idempotency check
- Signature verification
- Structured logging
"""

import logging
from typing import Any
from datetime import datetime

from flask import request, jsonify
from pydantic import BaseModel, ValidationError

from engine.core.queue import enqueue_task
from engine.core.security import verify_stripe_signature
from engine.models.payment import PaymentEvent, PaymentStatus
from engine.db.session import db_session

logger = logging.getLogger(__name__)


class StripeWebhookPayload(BaseModel):
    """Validated Stripe webhook payload structure."""
    id: str
    object: str
    type: str
    data: dict[str, Any]
    created: int


class WebhookHandler:
    """Handles Stripe webhook events with idempotency and verification."""

    PROCESSED_EVENTS = set()  # In production: use Redis with TTL

    def __init__(self):
        self.event_handlers = {
            'payment_intent.succeeded': self._handle_payment_success,
            'payment_intent.payment_failed': self._handle_payment_failure,
            'charge.refunded': self._handle_refund,
        }

    def handle(self, payload: bytes, signature: str) -> tuple[dict, int]:
        """
        Process incoming Stripe webhook.

        Args:
            payload: Raw request body
            signature: Stripe-Signature header value

        Returns:
            Tuple of (response_dict, http_status)
        """
        # 1. Verify signature
        if not verify_stripe_signature(payload, signature):
            logger.warning("Invalid webhook signature")
            return {'error': 'Invalid signature'}, 401

        # 2. Parse and validate payload
        try:
            data = StripeWebhookPayload.parse_raw(payload)
        except ValidationError as e:
            logger.error(f"Invalid webhook payload: {e}")
            return {'error': 'Invalid payload'}, 400

        # 3. Idempotency check
        if self._is_duplicate(data.id):
            logger.info(f"Duplicate webhook received: {data.id}")
            return {'status': 'already_processed'}, 200

        # 4. Queue for async processing
        enqueue_task(
            'process_stripe_webhook',
            event_id=data.id,
            event_type=data.type,
            event_data=data.data,
            received_at=datetime.utcnow().isoformat()
        )

        logger.info(f"Webhook queued: {data.type} ({data.id})")
        return {'status': 'queued'}, 200

    def _is_duplicate(self, event_id: str) -> bool:
        """Check if event was already processed."""
        # Production: Check Redis set with TTL
        return event_id in self.PROCESSED_EVENTS

    def _handle_payment_success(self, event_data: dict) -> None:
        """Process successful payment."""
        payment_intent = event_data.get('object', {})

        with db_session() as session:
            # Update payment record
            payment = session.query(Payment).filter_by(
                stripe_payment_intent_id=payment_intent['id']
            ).first()

            if payment:
                payment.status = PaymentStatus.COMPLETED
                payment.completed_at = datetime.utcnow()
                session.commit()

                # Trigger fulfillment
                enqueue_task('fulfill_order', order_id=payment.order_id)
                logger.info(f"Payment completed: {payment.id}")
            else:
                logger.warning(f"Payment not found for intent: {payment_intent['id']}")

    def _handle_payment_failure(self, event_data: dict) -> None:
        """Process failed payment."""
        payment_intent = event_data.get('object', {})
        error = payment_intent.get('last_payment_error', {})

        with db_session() as session:
            payment = session.query(Payment).filter_by(
                stripe_payment_intent_id=payment_intent['id']
            ).first()

            if payment:
                payment.status = PaymentStatus.FAILED
                payment.failure_reason = error.get('message')
                session.commit()

                logger.info(f"Payment failed: {payment.id} - {error.get('message')}")

    def _handle_refund(self, event_data: dict) -> None:
        """Process refund."""
        charge = event_data.get('object', {})

        with db_session() as session:
            payment = session.query(Payment).filter_by(
                stripe_charge_id=charge['id']
            ).first()

            if payment:
                payment.status = PaymentStatus.REFUNDED
                payment.refunded_at = datetime.utcnow()
                payment.refund_amount = charge.get('amount_refunded', 0)
                session.commit()

                logger.info(f"Payment refunded: {payment.id}")


# Flask route
from flask import Blueprint
webhook_bp = Blueprint('webhooks', __name__)
handler = WebhookHandler()

@webhook_bp.route('/webhooks/stripe', methods=['POST'])
def stripe_webhook():
    """Stripe webhook endpoint."""
    payload = request.get_data()
    signature = request.headers.get('Stripe-Signature', '')

    response, status = handler.handle(payload, signature)
    return jsonify(response), status
```

**Implementation Notes:**

```yaml
implementation_details:
  approach:
    - "Async processing via queue to handle load"
    - "Immediate 200 response to prevent Stripe retries"
    - "Idempotency via event ID tracking"
    - "Signature verification for security"

  error_handling:
    - "Invalid signature: 401 response"
    - "Invalid payload: 400 response with details"
    - "Processing errors logged; don't fail HTTP response"
    - "Database errors rollback transaction"

  testing:
    unit_tests:
      - "Test signature verification with valid/invalid signatures"
      - "Test idempotency check"
      - "Test each event handler with mock data"
    integration_tests:
      - "End-to-end with Stripe test events"
      - "Database state verification"
      - "Queue job verification"

  configuration:
    - "STRIPE_WEBHOOK_SECRET: Required for signature verification"
    - "WEBHOOK_EVENT_TTL: How long to track processed events"
```

### Example Output 2: Database Migration

```python
# /Users/shaansisodia/.blackbox5/2-engine/db/migrations/20260131_add_user_metadata.py
"""
Migration: Add metadata JSONB column to users table.

Uses Alembic migration pattern with online schema change consideration.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# Revision identifiers
revision = 'a1b2c3d4e5f6'
down_revision = '9876543210ab'
branch_labels = None
depends_on = None


def upgrade():
    """
    Add metadata column with GIN index for query performance.

    For large tables (>1M rows), consider using:
    - pt-online-schema-change (Percona)
    - pg_repack
    - Or run during low-traffic period
    """
    # Add column with default empty object
    op.add_column(
        'users',
        sa.Column(
            'metadata',
            JSONB,
            nullable=False,
            server_default='{}',
            comment='Flexible user attributes (preferences, settings, etc.)'
        )
    )

    # Create GIN index for JSONB queries
    # Note: This may take time on large tables
    op.create_index(
        'ix_users_metadata_gin',
        'users',
        ['metadata'],
        postgresql_using='gin'
    )

    # Add partial index for common query pattern
    op.execute("""
        CREATE INDEX ix_users_metadata_notifications
        ON users ((metadata->>'notifications_enabled'))
        WHERE metadata->>'notifications_enabled' IS NOT NULL
    """)


def downgrade():
    """Remove metadata column and indexes."""
    op.drop_index('ix_users_metadata_notifications', table_name='users')
    op.drop_index('ix_users_metadata_gin', table_name='users')
    op.drop_column('users', 'metadata')


# Application model update
# /Users/shaansisodia/.blackbox5/2-engine/models/user.py

from typing import Any, Optional
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from pydantic import BaseModel, validator

from engine.db.base import Base
from engine.core.exceptions import ValidationError


class UserMetadata(BaseModel):
    """Validated user metadata structure."""
    notifications_enabled: bool = True
    theme: str = 'light'
    timezone: str = 'UTC'
    custom_fields: dict[str, Any] = {}

    @validator('theme')
    def validate_theme(cls, v):
        allowed = {'light', 'dark', 'auto'}
        if v not in allowed:
            raise ValueError(f'theme must be one of {allowed}')
        return v

    @validator('timezone')
    def validate_timezone(cls, v):
        # Could use pytz for validation
        if not isinstance(v, str) or len(v) > 50:
            raise ValueError('invalid timezone')
        return v


class User(Base):
    """User model with metadata support."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # JSONB column for flexible attributes
    metadata = Column(
        JSONB,
        nullable=False,
        default=dict,
        comment='User preferences and settings'
    )

    def get_metadata(self) -> UserMetadata:
        """Get validated metadata."""
        return UserMetadata.parse_obj(self.metadata or {})

    def set_metadata(self, metadata: UserMetadata) -> None:
        """Set metadata with validation."""
        self.metadata = metadata.dict()

    def update_metadata(self, **kwargs) -> None:
        """Update specific metadata fields."""
        current = self.get_metadata()
        updated_data = {**current.dict(), **kwargs}
        self.set_metadata(UserMetadata.parse_obj(updated_data))
```

**Implementation Notes:**

```yaml
implementation_details:
  migration_strategy:
    - "Default empty object prevents null issues"
    - "GIN index for general JSONB queries"
    - "Partial index for specific common queries"
    - "Consider online schema change for large tables"

  validation:
    - "Pydantic model validates metadata structure"
    - "Type safety via get_metadata/set_metadata methods"
    - "Custom fields allowed but validated"

  query_patterns:
    - "Filter by metadata: User.metadata['key'].astext == 'value'"
    - "Use GIN index for contains queries"
    - "Partial index optimizes common lookups"

  testing:
    - "Test migration up/down"
    - "Test metadata validation"
    - "Test query performance with explain"
```

### Example Output 3: Background Job Worker

```python
# /Users/shaansisodia/.blackbox5/2-engine/core/workers/email_worker.py
"""
Email sending worker with retry logic and rate limiting.

Follows the established worker pattern:
- Decorator-based job registration
- Automatic retry with exponential backoff
- Dead letter queue for failed jobs
- Metrics and monitoring hooks
"""

import logging
import time
from typing import Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

import requests
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

from engine.core.queue import job, JobContext
from engine.core.metrics import increment_counter, record_timing
from engine.services.email import EmailService, EmailError

logger = logging.getLogger(__name__)


@dataclass
class EmailJobConfig:
    """Configuration for email job processing."""
    max_retries: int = 3
    rate_limit_per_minute: int = 100
    timeout_seconds: int = 30


class RateLimiter:
    """Simple in-memory rate limiter (use Redis in production)."""

    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: list[float] = []

    def acquire(self) -> bool:
        """Try to acquire a slot. Returns True if allowed."""
        now = time.time()
        cutoff = now - self.window_seconds

        # Remove old requests
        self.requests = [t for t in self.requests if t > cutoff]

        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False

    def time_until_next_slot(self) -> float:
        """Seconds until a slot becomes available."""
        if len(self.requests) < self.max_requests:
            return 0
        oldest = min(self.requests)
        return (oldest + self.window_seconds) - time.time()


# Global rate limiter instance
_email_rate_limiter = RateLimiter(
    max_requests=100,
    window_seconds=60
)


@job(
    queue='email',
    max_retries=3,
    dead_letter_queue='email_dlq'
)
def send_email(
    context: JobContext,
    to_address: str,
    subject: str,
    body_html: Optional[str] = None,
    body_text: Optional[str] = None,
    from_address: Optional[str] = None,
    reply_to: Optional[str] = None,
    attachments: Optional[list] = None
) -> dict:
    """
    Send email job with retry and rate limiting.

    Args:
        context: Job execution context
        to_address: Recipient email
        subject: Email subject
        body_html: HTML content
        body_text: Plain text content
        from_address: Sender (default: noreply@example.com)
        reply_to: Reply-to address
        attachments: List of attachment dicts

    Returns:
        Dict with message_id and status
    """
    start_time = time.time()

    try:
        # Rate limiting
        if not _email_rate_limiter.acquire():
            delay = _email_rate_limiter.time_until_next_slot()
            logger.info(f"Rate limit hit, requeuing in {delay:.1f}s")
            context.retry_in(timedelta(seconds=delay))
            return {'status': 'rate_limited', 'retry_in': delay}

        # Validate inputs
        if not body_html and not body_text:
            raise ValueError("Either body_html or body_text required")

        # Send via email service
        email_service = EmailService()

        result = _send_with_retry(
            email_service=email_service,
            to_address=to_address,
            subject=subject,
            body_html=body_html,
            body_text=body_text,
            from_address=from_address,
            reply_to=reply_to,
            attachments=attachments
        )

        # Success metrics
        duration = time.time() - start_time
        increment_counter('email.sent.success')
        record_timing('email.send_duration', duration)

        logger.info(f"Email sent to {to_address}: {result['message_id']}")

        return {
            'status': 'sent',
            'message_id': result['message_id'],
            'duration_ms': int(duration * 1000)
        }

    except EmailError as e:
        # Permanent failure - don't retry
        increment_counter('email.sent.permanent_failure')
        logger.error(f"Permanent email failure: {e}")
        raise  # Goes to DLQ

    except Exception as e:
        # Retryable failure
        increment_counter('email.sent.retryable_failure')
        logger.warning(f"Email failed (will retry): {e}")
        raise context.retry()


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=retry_if_exception_type((requests.Timeout, requests.ConnectionError)),
    reraise=True
)
def _send_with_retry(email_service: EmailService, **kwargs) -> dict:
    """
    Send email with retry logic.

    Retries on timeout/connection errors.
    Does not retry on 4xx errors (permanent failure).
    """
    return email_service.send(**kwargs)


@job(queue='email_dlq')
def handle_failed_email(context: JobContext, original_job: dict) -> None:
    """
    Process emails that failed after max retries.

    Actions:
    - Alert operations team
    - Store for manual review
    - Potentially notify user of failure
    """
    logger.error(f"Email permanently failed: {original_job}")

    # Store for manual review
    from engine.db.session import db_session
    from engine.models.failed_job import FailedJob

    with db_session() as session:
        failed = FailedJob(
            job_type='email',
            payload=original_job,
            failed_at=datetime.utcnow(),
            error=context.last_error
        )
        session.add(failed)
        session.commit()

    # Alert on high failure rate
    increment_counter('email.dead_letter')

    # Could also: send PagerDuty alert, Slack notification, etc.
```

---

## 5. Validator

### Scope and Responsibilities

The Validator specializes in **verification and quality assurance**:
- Testing implementations thoroughly
- Verifying requirements are met
- Checking edge cases
- Validating against specifications
- Measuring coverage and quality

**Key Questions They Answer:**
- Does this work correctly?
- Are all requirements covered?
- What tests are needed?
- Are there gaps in coverage?

### Prompt Template

```markdown
## Role: Validator

You are a meticulous quality assurance engineer who verifies that
implementations meet requirements and work correctly. You design tests,
identify gaps, and ensure nothing is missed.

### Implementation to Validate
{{IMPLEMENTATION_CODE}}

### Requirements
{{REQUIREMENTS_SPECIFICATION}}

### Context
{{GATHERED_CONTEXT}}

### Your Validation

Provide validation analysis in this format:

#### 1. Requirements Coverage
Map each requirement to implementation:
- **Requirement**: What was required
- **Status**: Met / Partial / Missing
- **Location**: Where in code
- **Evidence**: How you verified

#### 2. Test Strategy
Design comprehensive tests:
- **Unit Tests**: Individual component tests
- **Integration Tests**: End-to-end scenarios
- **Edge Cases**: Boundary conditions
- **Negative Tests**: Error conditions

#### 3. Coverage Analysis
- **Code Paths**: Which paths are tested?
- **Branches**: Condition coverage
- **Error Handling**: Exception paths
- **Gaps**: What's not covered

#### 4. Verification Checklist
Specific items to verify:
- [ ] Input validation
- [ ] Error handling
- [ ] Security checks
- [ ] Performance characteristics
- [ ] Resource cleanup

#### 5. Test Implementation
```python
# Actual test code
```

#### 6. Recommendations
- Critical gaps to address
- Priority order for testing
- Automation suggestions

### Validation Standards
- Every requirement must have evidence
- Every error path must be tested
- Every boundary must be checked
- Security must be verified
```

### When to Deploy

| Scenario | Deploy? | Rationale |
|----------|---------|-----------|
| Implementation complete | **YES** | Verify correctness |
| Before production | **YES** | Final validation |
| Requirements change | **YES** | Check coverage |
| Bug reported | **YES** | Design regression test |
| Architecture phase | No | Too early |
| Research phase | No | Use Researcher |

**Decision Criteria:**
- Is there code to validate? -> Deploy Validator
- Are requirements defined? -> Deploy Validator
- Is quality assurance needed? -> Deploy Validator

### Example Output 1: API Endpoint Validation

```yaml
validation_report:
  implementation: "Stripe webhook handler"

  requirements_coverage:
    - requirement: "Verify webhook signature"
      status: "Met"
      location: "WebhookHandler.handle() line 42"
      evidence: "Calls verify_stripe_signature() before processing"
      test_needed: "Test with valid/invalid signatures"

    - requirement: "Handle duplicate webhooks"
      status: "Met"
      location: "WebhookHandler._is_duplicate() line 67"
      evidence: "Checks PROCESSED_EVENTS set before processing"
      test_needed: "Test duplicate event ID handling"

    - requirement: "Queue for async processing"
      status: "Met"
      location: "WebhookHandler.handle() line 78"
      evidence: "Calls enqueue_task with event data"
      test_needed: "Mock queue and verify enqueue called"

    - requirement: "Handle payment success"
      status: "Met"
      location: "WebhookHandler._handle_payment_success() line 89"
      evidence: "Updates payment status and triggers fulfillment"
      test_needed: "Test payment state transitions"

    - requirement: "Handle payment failure"
      status: "Met"
      location: "WebhookHandler._handle_payment_failure() line 108"
      evidence: "Updates payment status with failure reason"
      test_needed: "Test failure reason capture"

    - requirement: "Log all webhook events"
      status: "Partial"
      location: "Various"
      evidence: "Logs at info level, but missing debug details"
      gap: "No structured logging of full event for debugging"
      recommendation: "Add debug log with sanitized event data"

  test_strategy:
    unit_tests:
      - name: "test_valid_signature_accepted"
        description: "Webhook with valid signature is processed"
        mocks: ["verify_stripe_signature"]
        assertions:
          - "Returns 200 status"
          - "Event is queued"

      - name: "test_invalid_signature_rejected"
        description: "Webhook with invalid signature returns 401"
        mocks: ["verify_stripe_signature"]
        assertions:
          - "Returns 401 status"
          - "Event not queued"

      - name: "test_duplicate_event_ignored"
        description: "Duplicate event ID returns already_processed"
        setup: "Add event ID to PROCESSED_EVENTS"
        assertions:
          - "Returns 200 with already_processed"
          - "Event not queued again"

      - name: "test_payment_success_updates_status"
        description: "Payment success updates database and triggers fulfillment"
        mocks: ["db_session", "enqueue_task"]
        assertions:
          - "Payment status set to COMPLETED"
          - "Fulfillment job queued"

      - name: "test_payment_failure_captures_reason"
        description: "Payment failure stores error message"
        mocks: ["db_session"]
        assertions:
          - "Payment status set to FAILED"
          - "Failure reason stored"

    integration_tests:
      - name: "test_end_to_end_webhook_flow"
        description: "Full flow from webhook to order fulfillment"
        setup: "Create pending payment in database"
        actions:
          - "Send Stripe test webhook"
          - "Wait for processing"
        assertions:
          - "Payment status updated"
          - "Order marked for fulfillment"

    edge_cases:
      - "Webhook with missing event type"
      - "Webhook with unknown event type"
      - "Payment not found in database"
      - "Database unavailable during processing"
      - "Malformed JSON in webhook payload"
      - "Very large webhook payload"

  coverage_analysis:
    code_paths:
      - path: "Signature verification"
        coverage: "Full"
        tested: "Yes"
      - path: "Payload validation"
        coverage: "Partial"
        gap: "Only valid/invalid cases; missing edge cases"
      - path: "Idempotency check"
        coverage: "Full"
        tested: "Yes"
      - path: "Event queuing"
        coverage: "Full"
        tested: "Yes"
      - path: "Payment success handler"
        coverage: "Partial"
        gap: "Missing: payment not found case"
      - path: "Payment failure handler"
        coverage: "Partial"
        gap: "Missing: payment not found case"
      - path: "Refund handler"
        coverage: "Unknown"
        gap: "Not reviewed in detail"

    error_handling:
      - "Invalid signature: Covered"
      - "Invalid payload: Covered"
      - "Database errors: Not covered"
      - "Queue errors: Not covered"

  verification_checklist:
    input_validation:
      - item: "Signature header present"
        status: "Verified"
      - item: "Payload is valid JSON"
        status: "Verified"
      - item: "Event type is recognized"
        status: "Partial - no validation for unknown types"

    error_handling:
      - item: "Database connection failures"
        status: "Gap - no specific handling"
      - item: "Queue service unavailable"
        status: "Gap - no specific handling"
      - item: "Malformed webhook data"
        status: "Verified - ValidationError caught"

    security:
      - item: "Signature verification"
        status: "Verified"
      - item: "No sensitive data logged"
        status: "Gap - need to verify"
      - item: "Input sanitization"
        status: "Partial - relies on Pydantic"

    performance:
      - item: "Async processing"
        status: "Verified"
      - item: "Database query optimization"
        status: "Gap - no index on stripe_payment_intent_id"
        recommendation: "Add database index"

  test_implementation:
    code: |
      # tests/test_webhook_handler.py
      import pytest
      from unittest.mock import Mock, patch
      from engine.api.routes.webhook_handler import WebhookHandler

      class TestWebhookHandler:
          @pytest.fixture
          def handler(self):
              return WebhookHandler()

          @patch('engine.api.routes.webhook_handler.verify_stripe_signature')
          @patch('engine.api.routes.webhook_handler.enqueue_task')
          def test_valid_webhook_processed(self, mock_enqueue, mock_verify, handler):
              mock_verify.return_value = True

              payload = b'{"id": "evt_123", "type": "payment_intent.succeeded"}'
              response, status = handler.handle(payload, "valid_sig")

              assert status == 200
              assert response['status'] == 'queued'
              mock_enqueue.assert_called_once()

          @patch('engine.api.routes.webhook_handler.verify_stripe_signature')
          def test_invalid_signature_rejected(self, mock_verify, handler):
              mock_verify.return_value = False

              payload = b'{"id": "evt_123"}'
              response, status = handler.handle(payload, "invalid_sig")

              assert status == 401

          def test_duplicate_event_ignored(self, handler):
              handler.PROCESSED_EVENTS.add("evt_123")

              with patch.object(handler, '_is_duplicate', return_value=True):
                  payload = b'{"id": "evt_123"}'
                  response, status = handler.handle(payload, "sig")

                  assert response['status'] == 'already_processed'

  recommendations:
    critical:
      - "Add database index on stripe_payment_intent_id for performance"
      - "Implement proper Redis-based idempotency (current in-memory won't work across workers)"
      - "Add error handling for database and queue failures"

    high:
      - "Add tests for payment not found scenarios"
      - "Verify no sensitive data in logs"
      - "Add test for unknown event types"

    medium:
      - "Add structured logging with correlation IDs"
      - "Add metrics for webhook processing time"
      - "Document expected webhook format"
```

### Example Output 2: Database Migration Validation

```yaml
validation_report:
  implementation: "Add metadata JSONB column to users table"

  requirements_coverage:
    - requirement: "Add metadata column to users table"
      status: "Met"
      location: "Migration file, upgrade() function"
      evidence: "Column added with JSONB type, nullable=False, default={}"

    - requirement: "Create index for metadata queries"
      status: "Met"
      location: "Migration file, op.create_index()"
      evidence: "GIN index created on metadata column"

    - requirement: "Validate metadata structure"
      status: "Met"
      location: "UserMetadata Pydantic model"
      evidence: "Fields defined with types and validators"

    - requirement: "Provide type-safe access methods"
      status: "Met"
      location: "User.get_metadata(), User.set_metadata()"
      evidence: "Methods use UserMetadata for validation"

  test_strategy:
    migration_tests:
      - name: "test_migration_applies_cleanly"
        description: "Migration runs without errors on empty database"

      - name: "test_migration_with_existing_data"
        description: "Migration runs with existing users"
        setup: "Insert 1000 test users"
        assertions:
          - "Migration completes in < 5 seconds"
          - "All users have metadata = {}"

      - name: "test_rollback_works"
        description: "Downgrade removes column and indexes"
        assertions:
          - "Column removed"
          - "Indexes removed"

    model_tests:
      - name: "test_get_metadata_returns_validated_object"
        description: "get_metadata() returns UserMetadata instance"

      - name: "test_set_metadata_validates_input"
        description: "set_metadata() raises on invalid data"

      - name: "test_update_metadata_merges_fields"
        description: "update_metadata() preserves existing fields"

      - name: "test_metadata_validation_errors"
        description: "Invalid metadata raises appropriate errors"
        test_cases:
          - "Invalid theme value"
          - "Timezone too long"
          - "Non-boolean notifications_enabled"

    integration_tests:
      - name: "test_metadata_query_performance"
        description: "Queries using metadata index are fast"
        setup: "Insert 100K users with varied metadata"
        assertions:
          - "Query by metadata uses index scan"
          - "Query time < 100ms"

  coverage_analysis:
    migration_paths:
      - path: "Fresh database"
        coverage: "Full"
      - path: "Existing data migration"
        coverage: "Partial"
        gap: "No test with production-sized dataset"
      - path: "Rollback"
        coverage: "Full"

    validation_paths:
      - path: "Valid metadata"
        coverage: "Full"
      - path: "Invalid theme"
        coverage: "Full"
      - path: "Invalid timezone"
        coverage: "Full"
      - path: "Extra fields in custom_fields"
        coverage: "Partial"
        gap: "No validation of custom_fields content"

  verification_checklist:
    schema:
      - item: "Column type is JSONB"
        status: "Verified"
      - item: "Column is NOT NULL"
        status: "Verified"
      - item: "Default value is '{}'"
        status: "Verified"
      - item: "GIN index exists"
        status: "Verified"
      - item: "Partial index for notifications"
        status: "Verified"

    validation:
      - item: "Theme values restricted"
        status: "Verified"
      - item: "Timezone length limited"
        status: "Verified"
      - item: "Notifications is boolean"
        status: "Verified"
      - item: "Custom fields accepted"
        status: "Verified"

    performance:
      - item: "Index is used for queries"
        status: "Gap - need to verify with EXPLAIN"
      - item: "Migration time acceptable"
        status: "Gap - need to test with large dataset"

  recommendations:
    critical:
      - "Test migration on production-sized dataset before deploying"
      - "Verify GIN index is used for typical queries"

    high:
      - "Add validation for custom_fields (max size, allowed keys)"
      - "Add test for concurrent metadata updates"

    medium:
      - "Document JSONB query patterns for developers"
      - "Add monitoring for metadata size growth"
```

### Example Output 3: Background Job Validation

```yaml
validation_report:
  implementation: "Email worker with retry and rate limiting"

  requirements_coverage:
    - requirement: "Send emails asynchronously"
      status: "Met"
      location: "send_email() job function"
      evidence: "Decorated with @job(queue='email')"

    - requirement: "Retry failed emails"
      status: "Met"
      location: "_send_with_retry() decorator"
      evidence: "@retry with exponential backoff"

    - requirement: "Rate limit email sending"
      status: "Met"
      location: "RateLimiter class and acquire() check"
      evidence: "Rate limiting before send attempt"

    - requirement: "Handle permanent failures"
      status: "Met"
      location: "EmailError exception handling"
      evidence: "Raises without retry for EmailError"

    - requirement: "Dead letter queue for max retries"
      status: "Met"
      location: "dead_letter_queue parameter and handle_failed_email()"
      evidence: "Failed jobs routed to email_dlq"

  test_strategy:
    unit_tests:
      - name: "test_email_sent_successfully"
        description: "Valid email is sent and metrics recorded"

      - name: "test_rate_limit_delays_retry"
        description: "Rate limit hit triggers retry with delay"

      - name: "test_retry_on_timeout"
        description: "Timeout error triggers retry"

      - name: "test_no_retry_on_4xx_error"
        description: "Client error doesn't retry"

      - name: "test_permanent_failure_to_dlq"
        description: "EmailError goes to DLQ handler"

      - name: "test_missing_body_raises_error"
        description: "Validation error for missing content"

    integration_tests:
      - name: "test_end_to_end_email_flow"
        description: "Job queued, processed, delivered"

      - name: "test_rate_limit_enforced_across_workers"
        description: "Multiple workers respect shared rate limit"
        note: "Requires Redis-based rate limiter"

    performance_tests:
      - name: "test_throughput_under_load"
        description: "System handles 1000 emails/minute"

  coverage_analysis:
    happy_paths:
      - "Email sent successfully: Covered"
      - "Rate limit available: Covered"

    error_paths:
      - "Timeout error: Covered (retry decorator)"
      - "Connection error: Covered (retry decorator)"
      - "EmailError: Covered (permanent failure)"
      - "Rate limit exceeded: Covered"
      - "Validation error: Covered"

    gaps:
      - "Rate limiter is in-memory (won't work across workers)"
      - "No test for attachment handling"
      - "No test for large email bodies"
      - "No test for DLQ handler"

  verification_checklist:
    functionality:
      - item: "Emails are queued"
        status: "Verified"
      - item: "Retry with exponential backoff"
        status: "Verified"
      - item: "Rate limiting prevents overload"
        status: "Partial - in-memory only"
      - item: "Dead letter queue captures failures"
        status: "Verified"

    observability:
      - item: "Success metrics incremented"
        status: "Verified"
      - item: "Failure metrics incremented"
        status: "Verified"
      - item: "Timing metrics recorded"
        status: "Verified"
      - item: "Structured logging"
        status: "Partial - basic logging only"

    reliability:
      - item: "Idempotent retry logic"
        status: "Gap - not verified"
      - item: "Resource cleanup on failure"
        status: "Gap - not verified"
      - item: "Graceful degradation"
        status: "Partial - rate limit handling"

  recommendations:
    critical:
      - "Replace in-memory rate limiter with Redis implementation"
      - "Add idempotency key to prevent duplicate sends on retry"

    high:
      - "Add test for attachment handling"
      - "Add test for DLQ handler"
      - "Verify email service connection cleanup"

    medium:
      - "Add structured logging with correlation IDs"
      - "Add alerting on DLQ growth"
      - "Document rate limit configuration"
```

---

## Role Interactions

### How Experts Collaborate

```
┌─────────────────────────────────────────────────────────────────┐
│                    SUPERINTELLIGENCE AGENT                      │
│                         (Orchestrator)                          │
└────────────────────┬────────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │Architect│  │Researcher│  │  Critic │
   │         │  │         │  │         │
   │"Structure│  │"What are │  │"What   │
   │ this"   │  │ options"│  │could    │
   └────┬────┘  └────┬────┘  │go wrong"│
        │            │       └────┬────┘
        │            │            │
        └────────────┼────────────┘
                     │
                     ▼
              ┌─────────────┐
              │  Synthesis  │
              │  (Decision) │
              └──────┬──────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │Implementer│ │Validator│  │  Critic │
   │         │  │         │  │(Review) │
   │"Build    │  │"Does it │  │"Final   │
   │ it"     │  │ work"   │  │check"   │
   └─────────┘  └─────────┘  └─────────┘
```

### Interaction Patterns

**Pattern 1: Architecture Decision**
```
Researcher -> Architect -> Critic -> Decision
(Gather options) (Design) (Find issues) (Choose)
```

**Pattern 2: Feature Implementation**
```
Architect -> Implementer -> Validator -> Critic
(Design) (Build) (Test) (Review)
```

**Pattern 3: Technology Selection**
```
Researcher -> Critic -> Architect
(Options) (Risks) (Integration)
```

**Pattern 4: Production Issue**
```
Researcher -> Critic -> Implementer -> Validator
(Investigate) (Root cause) (Fix) (Verify)
```

---

## Deployment Strategy

### When to Deploy Multiple Roles vs One

| Scenario | Roles to Deploy | Rationale |
|----------|-----------------|-----------|
| New feature, high impact | Architect + Researcher + Critic | Need design, options, and risk analysis |
| Technology choice | Researcher + Critic | Need comparison and risk assessment |
| Simple bug fix | Implementer + Validator | Fix and verify |
| Security review | Critic + Validator | Find issues and verify fixes |
| Performance optimization | Architect + Implementer + Validator | Design change, implement, measure |
| Refactoring | Critic + Implementer + Validator | Risk assessment, execution, verification |
| Greenfield project | All 5 in sequence | Full analysis before building |

### Single Role Deployment

Deploy a single expert when:
- **Architect**: Designing a new subsystem
- **Researcher**: Evaluating a specific technology
- **Critic**: Reviewing an existing implementation
- **Implementer**: Executing a well-defined task
- **Validator**: Testing a completed implementation

### Multi-Role Deployment

Deploy multiple experts when:
- **Complex decisions**: Need multiple perspectives
- **High stakes**: Production-critical changes
- **Unknown domain**: Need research + design + risk analysis
- **Team learning**: Multiple viewpoints for education

### Conflict Resolution

When experts disagree:

**1. Identify Conflict Type**
- **Facts**: Disagreement about reality -> Researcher decides
- **Values**: Disagreement about priorities -> Stakeholder decides
- **Predictions**: Disagreement about future -> Critic decides (risk-averse)
- **Trade-offs**: Disagreement about balance -> Architect decides

**2. Escalation Path**
```
Expert Disagreement
       │
       ▼
┌──────────────┐
│ Can we test? │──Yes──► Run experiment
└──────────────┘
       │ No
       ▼
┌──────────────┐
│ Impact of    │
│ being wrong? │
└──────────────┘
       │
   High│      Low
       │        │
       ▼        ▼
  ┌──────┐  ┌──────┐
  │Critic│  │Either│
  │Wins  │  │OK    │
  └──────┘  └──────┘
```

**3. Resolution Strategies**

| Conflict | Resolution Strategy |
|----------|---------------------|
| Architect vs Critic | Critic identifies risks; Architect addresses or accepts |
| Researcher vs Implementer | Researcher provides options; Implementer chooses pragmatic |
| Validator vs Implementer | Validator finds gaps; Implementer fixes |
| All disagree on approach | Researcher finds precedent; if none, prototype both |

**4. Documentation**
Always document:
- What each expert recommended
- Why the chosen path was selected
- What risks were accepted
- How to monitor for issues

---

## Quick Reference

### Role Selection Flowchart

```
                    Start
                      │
                      ▼
            ┌─────────────────┐
            │  Need to decide │
            │   what to do?   │
            └────────┬────────┘
                     │
           ┌─────────┴─────────┐
           │                   │
          Yes                  No
           │                   │
           ▼                   ▼
    ┌────────────┐      ┌────────────┐
    │ Researcher │      │  Need to   │
    │  + Critic  │      │   build?   │
    └────────────┘      └─────┬──────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                   Yes                  No
                    │                   │
                    ▼                   ▼
             ┌────────────┐      ┌────────────┐
             │  Architect │      │  Need to   │
             │Implementer │      │   check?   │
             │ Validator  │      └─────┬──────┘
             │  + Critic  │            │
             └────────────┘   ┌────────┴────────┐
                              │                 │
                             Yes                No
                              │                 │
                              ▼                 ▼
                       ┌────────────┐     ┌──────────┐
                       │  Validator │     │  Critic  │
                       │  + Critic  │     │  (Review)│
                       └────────────┘     └──────────┘
```

### Activation Cheat Sheet

| You Need... | Activate |
|-------------|----------|
| Design a system | Architect |
| Compare options | Researcher |
| Find problems | Critic |
| Write code | Implementer |
| Verify quality | Validator |
| Make big decision | Architect + Researcher + Critic |
| Build feature | Architect + Implementer + Validator |
| Fix production issue | Researcher + Critic + Implementer |
| Choose technology | Researcher + Critic |
| Review code | Critic + Validator |

---

## Integration with Superintelligence Protocol

```python
def activate_expert_role(role: str, task: str, context: ContextBundle) -> ExpertOutput:
    """
    Activate a specific expert role for analysis.

    Args:
        role: One of 'architect', 'researcher', 'critic', 'implementer', 'validator'
        task: Description of what to analyze
        context: Gathered context from context gatherers

    Returns:
        ExpertOutput with structured analysis
    """
    prompts = {
        'architect': ARCHITECT_PROMPT,
        'researcher': RESEARCHER_PROMPT,
        'critic': CRITIC_PROMPT,
        'implementer': IMPLEMENTER_PROMPT,
        'validator': VALIDATOR_PROMPT
    }

    expert = SubAgent(
        role=role,
        instructions=prompts[role],
        context_budget="high"
    )

    return expert.execute(task=task, context=context)


def resolve_expert_conflicts(expert_outputs: list[ExpertOutput]) -> Resolution:
    """
    Resolve conflicts between expert recommendations.

    Strategy:
    1. Identify points of disagreement
    2. Classify conflict type (fact, value, prediction)
    3. Apply resolution rules
    4. Document decision rationale
    """
    conflicts = find_disagreements(expert_outputs)

    for conflict in conflicts:
        if conflict.type == 'fact':
            # Researcher has authority on facts
            resolution = accept_researcher_view(conflict)
        elif conflict.type == 'risk':
            # Critic has authority on risk acceptance
            resolution = accept_critic_view(conflict)
        elif conflict.type == 'design':
            # Architect has authority on structure
            resolution = accept_architect_view(conflict)
        else:
            # Escalate to super-agent
            resolution = escalate_to_super_agent(conflict)

        document_resolution(conflict, resolution)

    return compile_final_resolution(expert_outputs, conflicts)
```

---

## Next Steps

1. **Create prompt templates** for each role in your system
2. **Define output schemas** for structured expert responses
3. **Build conflict resolution** logic for disagreements
4. **Create expert selection** flowchart for your domain
5. **Test with real scenarios** to refine prompts

---

**Related:**
- [Context Gatherers](./context-gatherers.md)
- [Deployment Patterns](./deployment-patterns.md)
- [Hierarchical Context](../context-management/hierarchical-context.md)
