# Multi-API Management Architecture
**Document Version:** 1.0
**Date:** 2026-02-10
**Related:** multi-api-research.md

---

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              BLACKBOX5 CORE                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  RALF Engine │  │    Scribe    │  │    Planner   │  │   Executor   │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
└─────────┼──────────────────┼──────────────────┼──────────────────┼──────────┘
          │                  │                  │                  │
          └──────────────────┼──────────────────┼──────────────────┘
                             │
                    ┌────────▼────────┐
                    │  AGENT LAYER    │
                    │                 │
                    │ ┌─────────────┐ │
                    │ │ Coder Agent │ │
                    │ └──────┬──────┘ │
                    │ ┌─────────────┐ │
                    │ │Research Agent│ │
                    │ └──────┬──────┘ │
                    │ ┌─────────────┐ │
                    │ │Vision Agent │ │
                    │ └──────┬──────┘ │
                    │ ┌─────────────┐ │
                    │ │Scribe Agent │ │
                    │ └──────┬──────┘ │
                    │ ┌─────────────┐ │
                    │ │Other Agents │ │
                    │ └──────┬──────┘ │
                    └────────┼─────────┘
                             │
                    ┌────────▼────────┐
                    │ API GATEWAY     │
                    │ (Load Balancer)│
                    │                 │
                    │ ┌─────────────┐ │
                    │ │ Request     │ │
                    │ │ Router      │ │
                    │ └──────┬──────┘ │
                    │ ┌─────────────┐ │
                    │ │ Health      │ │
                    │ │ Monitor     │ │
                    │ └──────┬──────┘ │
                    │ ┌─────────────┐ │
                    │ │ Rate Limit  │ │
                    │ │ Tracker     │ │
                    │ └──────┬──────┘ │
                    │ ┌─────────────┐ │
                    │ │ Circuit     │ │
                    │ │ Breaker     │ │
                    │ └──────┬──────┘ │
                    └────────┼─────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
   ┌──────▼──────┐    ┌─────▼──────┐    ┌──────▼──────┐
   │   KIMI      │    │   GOOGLE    │    │   CLAUDE    │
   │   CLUSTER   │    │   VERTEX    │    │   CODE      │
   │             │    │             │    │             │
   │ ┌─────────┐ │    │ ┌─────────┐ │    │ ┌─────────┐ │
   │ │ Key 1   │ │    │ │ Acct 1  │ │    │ │ Key 1   │ │
   │ ├─────────┤ │    │ ├─────────┤ │    │ ├─────────┤ │
   │ │ Key 2   │ │    │ │ Acct 2  │ │    │ │ Key 2   │ │
   │ ├─────────┤ │    │ ├─────────┤ │    │ └─────────┘ │
   │ │ Key 3   │ │    │ │ Acct 3  │ │    │             │
   │ ├─────────┤ │    │ └─────────┘ │    │             │
   │ │ Key 4   │ │    │             │    │             │
   │ ├─────────┤ │    │             │    │             │
   │ │ Key 5   │ │    │             │    │             │
   │ ├─────────┤ │    │             │    │             │
   │ │ Key 6   │ │    │             │    │             │
   │ ├─────────┤ │    │             │    │             │
   │ │ Key 7   │ │    │             │    │             │
   │ ├─────────┤ │    │             │    │             │
   │ │ Key 8   │ │    │             │    │             │
   │ ├─────────┤ │    │             │    │             │
   │ │ Key 9   │ │    │             │    │             │
   │ └─────────┘ │    │             │    │             │
   └─────────────┘    └─────────────┘    └─────────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
   ┌──────▼──────┐    ┌─────▼──────┐    ┌──────▼──────┐
   │   OPENAI    │    │  COHERE    │    │  TOGETHER   │
   │   (Backup)  │    │  (Backup)  │    │  AI (Backup)│
   └─────────────┘    └─────────────┘    └─────────────┘
```

---

## Component Details

### 1. API Gateway (Load Balancer)

```
┌─────────────────────────────────────────────────────────────┐
│                     API GATEWAY                               │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              REQUEST ROUTER                           │  │
│  │                                                        │  │
│  │  Input: Task + Agent + Priority                        │  │
│  │                                                        │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │  1. Analyze Task Type                          │  │  │
│  │  │     - coding, reasoning, vision, translation    │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  │           │                                            │  │
│  │  ┌────────▼────────────────────────────────────────┐  │  │
│  │  │  2. Check Agent Preferences                     │  │  │
│  │  │     - Coder Agent → prefers Claude              │  │  │
│  │  │     - Vision Agent → prefers Google Vertex      │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  │           │                                            │  │
│  │  ┌────────▼────────────────────────────────────────┐  │  │
│  │  │  3. Filter Available APIs                       │  │  │
│  │  │     - Check circuit breakers                    │  │  │
│  │  │     - Check rate limits                         │  │  │
│  │  │     - Check health status                       │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  │           │                                            │  │
│  │  ┌────────▼────────────────────────────────────────┐  │  │
│  │  │  4. Score APIs                                 │  │  │
│  │  │     - Performance score                        │  │  │
│  │  │     - Cost score                               │  │  │
│  │  │     - Availability score                       │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  │           │                                            │  │
│  │  ┌────────▼────────────────────────────────────────┐  │  │
│  │  │  5. Select Best API                             │  │  │
│  │  │     - Weighted selection                        │  │  │
│  │  │     - Return API endpoint + key                │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              HEALTH MONITOR                          │  │
│  │                                                        │  │
│  │  - Ping APIs every 30s                                 │  │
│  │  - Track response times                                │  │
│  │  - Detect failures                                     │  │
│  │  - Update health status in Redis                       │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              RATE LIMIT TRACKER                       │  │
│  │                                                        │  │
│  │  - Track requests per API                               │  │
│  │  - Track tokens per API                                │  │
│  │  - Predict rate limit exhaustion                        │  │
│  │  - Switch before hitting limit                         │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              CIRCUIT BREAKER                          │  │
│  │                                                        │  │
│  │  - Trip after 5 consecutive failures                   │  │
│  │  - Open circuit = stop routing to failed API           │  │
│  │  - Half-open = test recovery                            │  │
│  │  - Closed = fully recovered                            │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### 2. Self-Improvement Engine

```
┌─────────────────────────────────────────────────────────────┐
│               SELF-IMPROVEMENT ENGINE                         │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           PERFORMANCE TRACKER                          │  │
│  │                                                        │  │
│  │  Metrics per API + Task Type:                         │  │
│  │  ┌─────────────────┬────────┬────────┬──────────┐    │  │
│  │  │ API             │ Success│ Avg RT │ Quality  │    │  │
│  │  ├─────────────────┼────────┼────────┼──────────┤    │  │
│  │  │ claude_code     │  99.2% │  1.8s  │  4.7/5   │    │  │
│  │  │ kimi             │  98.5% │  2.3s  │  4.5/5   │    │  │
│  │  │ google_vertex    │  99.0% │  2.1s  │  4.6/5   │    │  │
│  │  └─────────────────┴────────┴────────┴──────────┘    │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
│                              ▼                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           COST OPTIMIZER                              │  │
│  │                                                        │  │
│  │  Track costs per API + Task Type:                    │  │
│  │  ┌─────────────────┬──────────┬──────────┐          │  │
│  │  │ API             │ Daily    │ Monthly  │          │  │
│  │  ├─────────────────┼──────────┼──────────┤          │  │
│  │  │ claude_code     │  $2.50   │  $75.00  │          │  │
│  │  │ kimi             │  $0.00   │   $0.00  │          │  │
│  │  │ google_vertex   │  $1.20   │  $36.00  │          │  │
│  │  └─────────────────┴──────────┴──────────┘          │  │
│  │                                                        │  │
│  │  Optimization Actions:                                 │  │
│  │  - Prefer free tiers for background tasks            │  │
│  │  - Downgrade low-priority tasks                        │  │
│  │  - Alert when budget at 80%                           │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
│                              ▼                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           DECISION ENGINE                             │  │
│  │                                                        │  │
│  │  Learning Rules:                                      │  │
│  │                                                        │  │
│  │  Rule 1: Coding Tasks                                 │  │
│  │    IF task_type = coding                             │  │
│  │    AND claude_code.success_rate > 98%                │  │
│  │    THEN prefer claude_code (weight: 4)                │  │
│  │                                                        │  │
│  │  Rule 2: Cost Optimization                            │  │
│  │    IF task_type = summarization                       │  │
│  │    AND priority = low                                 │  │
│  │    THEN prefer kimi (free)                            │  │
│  │                                                        │  │
│  │  Rule 3: Vision Tasks                                 │  │
│  │    IF task_type = vision                              │  │
│  │    THEN prefer google_vertex (best multimodal)        │  │
│  │                                                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
│                              ▼                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           A/B TESTING FRAMEWORK                      │  │
│  │                                                        │  │
│  │  Running Experiments:                                │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │ Experiment: claude_vs_kimi_coding             │  │  │
│  │  │ Duration: 24h | Sample: 100                    │  │  │
│  │  │ Results:                                        │  │  │
│  │  │   - Claude: 99.2% success, 1.8s avg            │  │  │
│  │  │   - Kimi: 98.5% success, 2.3s avg             │  │  │
│  │  │ Winner: Claude (+15% quality, -22% latency)    │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### 3. API Provider Details

#### Kimi Cluster
```
┌─────────────────────────────────────────────────────────┐
│                    KIMI CLUSTER                          │
│                                                          │
│  Load Balancing: Round-Robin with Weights               │
│                                                          │
│  ┌─────────┬──────────┬──────────┬─────────────┐        │
│  │ Key     │ Status   │ Used     │ Limit       │        │
│  ├─────────┼──────────┼──────────┼─────────────┤        │
│  │ kimi_1  │ ACTIVE   │ 750/1000 │ 90d expiry  │        │
│  │ kimi_2  │ STANDBY  │ 100/500  │ 88d expiry  │        │
│  │ kimi_3  │ ACTIVE   │ 600/1000 │ 85d expiry  │        │
│  │ kimi_4  │ STANDBY  │ 50/500   │ 82d expiry  │        │
│  │ kimi_5  │ ACTIVE   │ 800/1000 │ 80d expiry  │        │
│  │ kimi_6  │ STANDBY  │ 0/500    │ 77d expiry  │        │
│  │ kimi_7  │ ACTIVE   │ 400/1000 │ 75d expiry  │        │
│  │ kimi_8  │ STANDBY  │ 200/500  │ 72d expiry  │        │
│  │ kimi_9  │ ACTIVE   │ 300/1000 │ 70d expiry  │        │
│  └─────────┴──────────┴──────────┴─────────────┘        │
│                                                          │
│  Total Active: 5 keys | Total Standby: 4 keys           │
│  Total Usage: 3,200/7,000 (45.7%)                       │
│                                                          │
│  Capabilities:                                          │
│  ✓ Long Context (128K+ tokens)                          │
│  ✓ Code Generation                                       │
│  ✓ Reasoning                                             │
│  ✓ Summarization                                         │
│                                                          │
│  Best For:                                               │
│  • Long-form text tasks                                  │
│  • Cost-effective operations                             │
│  • Background tasks                                      │
└──────────────────────────────────────────────────────────┘
```

#### Google Vertex AI
```
┌─────────────────────────────────────────────────────────┐
│                  GOOGLE VERTEX AI                         │
│                                                          │
│  Service Accounts:                                       │
│  ┌────────────────┬──────────────┬──────────┐           │
│  │ Account       │ Status       │ Usage     │           │
│  ├────────────────┼──────────────┼──────────┤           │
│  │ bb5-prod-1     │ ACTIVE       │ 60%      │           │
│  │ bb5-backup-1   │ STANDBY      │ 0%       │           │
│  └────────────────┴──────────────┴──────────┘           │
│                                                          │
│  Free Tier Benefits:                                     │
│  • $300 credit (90 days)                                │
│  • 15 predictions/month (Gemini)                         │
│  • 60 min/month Speech-to-Text                          │
│  • 500K chars/month Translation                         │
│  • 4M chars/month Text-to-Speech                        │
│                                                          │
│  Capabilities:                                          │
│  ✓ Vision/Image Analysis                                │
│  ✓ Video Processing (Native)                            │
│  ✓ Speech-to-Text                                       │
│  ✓ Translation                                           │
│  ✓ Text-to-Speech                                       │
│  ✓ Long Context (1M tokens - Gemini 1.5 Pro)            │
│                                                          │
│  Best For:                                               │
│  • Multimodal tasks (vision, video)                      │
│  • Speech processing                                     │
│  • Translation                                           │
│  • Very long context requirements                        │
└──────────────────────────────────────────────────────────┘
```

#### Claude Code CLI
```
┌─────────────────────────────────────────────────────────┐
│                  CLAUDE CODE CLI                          │
│                                                          │
│  API Keys:                                               │
│  ┌────────────────┬──────────────┬──────────┐           │
│  │ Key            │ Agent Type   │ Status   │           │
│  ├────────────────┼──────────────┼──────────┤           │
│  │ sk-ant-...01   │ coder        │ ACTIVE   │           │
│  │ sk-ant-...02   │ architect    │ ACTIVE   │           │
│  └────────────────┴──────────────┴──────────┘           │
│                                                          │
│  Access Methods:                                         │
│  1. CLI: /usr/bin/claude                                │
│  2. HTTP: api.anthropic.com/v1/messages                 │
│  3. OpenClaw integration via exec tool                   │
│                                                          │
│  Capabilities:                                          │
│  ✓ Excellent Code Generation                             │
│  ✓ File System Access (native)                          │
│  ✓ Interactive Editing                                  │
│  ✓ Terminal Integration                                 │
│  ✓ MCP Tools (extensible)                               │
│  ✓ Context Window: 200K tokens                          │
│                                                          │
│  Best For:                                               │
│  • Code generation and debugging                        │
│  • File operations                                      │
│  • Interactive coding sessions                           │
│  • MCP tool integration                                  │
└──────────────────────────────────────────────────────────┘
```

---

## Data Flow Examples

### Example 1: Code Generation Request

```
┌──────────────┐
│ SISO: "Debug │
│  this code"  │
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 1. Agent Layer: Coder Agent receives request              │
│    - Task type: coding                                   │
│    - Priority: high                                      │
└─────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 2. API Gateway: Request Router                           │
│    - Analyze task: coding                                │
│    - Check agent preference: Coder → prefers Claude      │
│    - Filter available APIs:                             │
│      • claude_code: ✓ available, healthy                │
│      • kimi: ✓ available, healthy                        │
│      • google_vertex: ✓ available, healthy              │
│    - Score APIs:                                         │
│      • claude_code: 0.85 (best for coding)              │
│      • kimi: 0.70 (good, free)                          │
│      • google_vertex: 0.65 (good)                        │
│    - Select: claude_code                                 │
└─────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 3. Claude Code CLI                                       │
│    - Use key: sk-ant-...01 (coder)                      │
│    - Model: claude-3-5-sonnet-20241022                 │
│    - Execute code debugging                             │
│    - Return: Fixed code + explanation                   │
└─────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 4. Self-Improvement Engine                               │
│    - Log metrics:                                        │
│      • API: claude_code                                  │
│      • Task: coding                                     │
│      • Success: ✓                                       │
│      • Response time: 1.8s                              │
│      • Quality: 4.8/5                                   │
│    - Update performance history                          │
└─────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 5. Scribe: Log to database                                │
│    - API usage: claude_code +1                           │
│    - Cost tracking: +$0.15                               │
│    - Agent activity: coder +1                            │
└─────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────┐
│ SISO: "Your  │
│  code is     │
│  fixed! ✓"   │
└──────────────┘
```

### Example 2: Failover Scenario

```
┌──────────────┐
│ Request:     │
│ "Summarize   │
│  this doc"   │
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 1. API Gateway: Try Kimi (preferred for long text)       │
│    - API: kimi_key_1                                    │
│    - Request: Summarization                             │
└─────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 2. ERROR: Rate limit exceeded (429)                      │
└─────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 3. Circuit Breaker:                                      │
│    - Increment failure count: 1/5                       │
│    - Check rate limit status: WARNING (95% used)         │
│    - Mark kimi_key_1 as approaching limit               │
└─────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 4. Failover: Try next API                                │
│    - Check kimi_key_2: ✓ Available                      │
│    - Route to kimi_key_2                                 │
└─────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 5. Success: Kimi key 2 handles request                  │
│    - Return: Summary                                    │
└─────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 6. Self-Improvement:                                    │
│    - Log failover event                                 │
│    - Update rate limit tracker                          │
│    - Mark kimi_key_1 as WARNING state                   │
│    - Prefer kimi_key_2 for future requests              │
└─────────────────────────────────────────────────────────┘
```

### Example 3: Parallel Processing

```
┌──────────────┐
│ SISO: "Analyze│
│  this video + │
│  transcribe"  │
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 1. Task Analysis:                                        │
│    - Task 1: Vision analysis (video)                     │
│    - Task 2: Speech-to-text (transcription)             │
│    - Can run in parallel!                                │
└─────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 2. API Gateway: Parallel Routing                         │
│    ┌────────────────────────────────────────────────┐   │
│    │ Task 1: Vision Analysis                        │   │
│    │ → Google Vertex AI (best for video)            │   │
│    │ → Model: gemini-1.5-pro                        │   │
│    └────────────────────────────────────────────────┘   │
│                                                          │
│    ┌────────────────────────────────────────────────┐   │
│    │ Task 2: Speech-to-Text                         │   │
│    │ → Google Vertex AI (Speech API)                │   │
│    │ → Model: chirp-2                               │   │
│    └────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 3. Parallel Execution:                                   │
│    ┌─────────────────────┬─────────────────────────┐    │
│    │ Vision Analysis     │ Speech-to-Text          │    │
│    │ Google Vertex       │ Google Vertex           │    │
│    │ ─────────────────   │ ─────────────────       │    │
│    │ Analyzing video...  │ Transcribing audio...   │    │
│    │ ✓ Detected: Person │ ✓ Transcribed: "Hello"  │    │
│    │ ✓ Detected: Car    │                         │    │
│    │ ✓ Detected: Dog    │                         │    │
│    └─────────────────────┴─────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 4. Combine Results:                                      │
│    - Vision: Detected person, car, dog in video         │
│    - Audio: Transcribed "Hello, this is a test"        │
│    - Combined: Multimodal analysis complete              │
└─────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────┐
│ SISO: "Video  │
│  has a person │
│  saying..."   │
└──────────────┘
```

---

## Technology Stack

```
┌─────────────────────────────────────────────────────────┐
│                    TECHNOLOGY STACK                      │
│                                                          │
│  Core:                                                   │
│  ┌──────────────────────────────────────────────────┐  │
│  │ BlackBox5 Engine (RALF)                         │  │
│  │ - Python 3.12+                                  │  │
│  │ - Redis (state, pub/sub)                        │  │
│  │ - NATS (JetStream, guaranteed delivery)          │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  API Gateway:                                            │
│  ┌──────────────────────────────────────────────────┐  │
│  │ FastAPI + Uvicorn                               │  │
│  │ - Rate limiting (slowapi)                       │  │
│  │ - Circuit breaker (circuitbreaker)              │  │
│  │ - Health checks                                 │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  Database:                                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │ PostgreSQL (primary)                            │  │
│  │ - API usage logs                               │  │
│  │ - Cost tracking                                │  │
│  │ - Performance metrics                          │  │
│  │ - A/B test results                             │  │
│  │                                                  │  │
│  │ Redis (cache)                                  │  │
│  │ - API health status                            │  │
│  │ - Rate limit counters                         │  │
│  │ - Circuit breaker state                       │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  Monitoring:                                             │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Prometheus + Grafana                            │  │
│  │ - API performance metrics                       │  │
│  │ - Cost tracking                                 │  │
│  │ - Health dashboards                            │  │
│  │                                                  │  │
│  │ BlackBox5 Scribe                               │  │
│  │ - Logging                                      │  │
│  │ - Reports                                      │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  External APIs:                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │ • Kimi (Moonshot AI)                            │  │
│  │ • Google Vertex AI                              │  │
│  │ • Claude Code CLI (Anthropic)                   │  │
│  │ • OpenAI (fallback)                             │  │
│  │ • Cohere (backup)                               │  │
│  │ • Together AI (backup)                           │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Configuration File Structure

```
/opt/blackbox5/config/
├── api-gateway/
│   ├── config.yaml              # Main gateway config
│   ├── providers/                # Provider-specific configs
│   │   ├── kimi.yaml
│   │   ├── google-vertex.yaml
│   │   ├── claude-code.yaml
│   │   └── openai.yaml
│   ├── agents/                   # Agent-specific configs
│   │   ├── coder.yaml
│   │   ├── research.yaml
│   │   ├── vision.yaml
│   │   └── scribe.yaml
│   ├── failover.yaml             # Failover policies
│   └── circuit-breakers.yaml    # Circuit breaker rules
│
├── self-improvement/
│   ├── learning-rules.yaml       # API selection rules
│   ├── a-b-tests.yaml            # A/B test configs
│   └── metrics.yaml              # Metrics to track
│
└── monitoring/
    ├── alerts.yaml               # Alert thresholds
    └── reports.yaml              # Report schedules
```

---

## Security Considerations

```
┌─────────────────────────────────────────────────────────┐
│                    SECURITY MODEL                        │
│                                                          │
│  API Keys:                                               │
│  ✓ Stored in encrypted secrets (/opt/blackbox5/.secrets)│
│  ✓ Never committed to Git                                │
│  ✓ Rotate every 90 days                                   │
│  ✓ Separate keys for different environments             │
│                                                          │
│  Access Control:                                          │
│  ✓ API Gateway requires authentication                  │
│  ✓ Rate limiting per API key                            │
│  ✓ Circuit breakers prevent cascading failures          │
│                                                          │
│  Data Privacy:                                           │
│  ✓ No sensitive data logged                             │
│  ✓ Anonymized metrics only                              │
│  ✓ Comply with provider terms                            │
│                                                          │
│  Fail-Safe:                                              │
│  ✓ System degrades gracefully on API failures           │
│  ✓ Queue requests when all APIs unavailable             │
│  ✓ Notify SISO on critical failures                      │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

**Document Version:** 1.0
**Last Updated:** 2026-02-10
**Maintained By:** BlackBox5 Knowledge Base
