# Agent Interface Specifications

**Version:** 1.0.0
**Status:** Complete
**Date:** 2026-02-10

---

## Overview

This document defines the detailed interface specifications for the 4-agent research pipeline. All interfaces use YAML frontmatter-style schemas for machine-readable validation and human readability.

---

## Table of Contents

1. [Scout Agent Interface](#1-scout-agent-interface)
2. [Analyst Agent Interface](#2-analyst-agent-interface)
3. [Planner Agent Interface](#3-planner-agent-interface)
4. [Executor Agent Interface](#4-executor-agent-interface)
5. [Communication Protocol](#5-communication-protocol)
6. [Storage Interfaces](#6-storage-interfaces)
7. [State Management](#7-state-management)
8. [Error Handling](#8-error-handling)

---

## 1. Scout Agent Interface

**Agent Type:** Scout Worker
**Pair:** Scout-Validator
**Input/Output:** Public-facing contracts

### 1.1 Input Contracts

#### Source Selection Queue
```yaml
# Timeline memory: scout-worker/timeline-memory.md
work_queue:
  priority_sources:
    - source_id: "SRC-001"
      source_url: "github.com/user/auth-system"
      source_type: github
      priority: high
      first_seen: "2026-02-10T00:00:00Z"
      last_checked: "2026-02-10T00:00:00Z"

    - source_id: "SRC-002"
      source_url: "youtube.com/watch?v=xyz"
      source_type: youtube
      priority: medium
      first_seen: "2026-02-10T01:00:00Z"
      last_checked: "2026-02-10T01:00:00Z"

  backlog:
    - source_id: "SRC-003"
      source_url: "https://example.com/docs"
      source_type: docs
      priority: low
      first_seen: "2026-02-10T02:00:00Z"
      last_checked: "2026-02-10T02:00:00Z"

  in_progress: null
  completed_today: 0
  failed_today: 0

scoring_model:
  extraction_accuracy: 0.0  # 0-1
  common_mistakes: []
  extraction_temperature: "balanced"  # aggressive, balanced, conservative

swarm_context:
  agent: scout-worker
  pipeline_phase: scout
  pair_agent: scout-validator
  upstream_agents: []
  downstream_agents: [analyst-worker]
```

#### Source Configuration
```yaml
# context/sources.yaml
sources:
  github:
    - repo: "user/auth-system"
      branch: "main"
      token: "${GITHUB_TOKEN}"
      patterns_to_look_for:
        - "middleware"
        - "decorator"
        - "authentication"

  youtube:
    - channel: "tech-channel"
      token: "${YOUTUBE_TOKEN}"
      max_videos: 5
      focus: "authentication"
```

#### Validator Feedback
```yaml
# agents/scout-validator/memory/improvement-suggestions.yaml
suggestions_for_worker:
  - run_id: "run-001"
    timestamp: "2026-02-10T10:00:00Z"
    observation: "Worker focused on middleware, missed auth decorators"
    suggestion: "Check auth/decorators.py for @require_role pattern"
    based_on: "Previous 5 similar repos all had decorator patterns"

  - run_id: "run-002"
    timestamp: "2026-02-10T11:00:00Z"
    observation: "Worker not checking test files"
    suggestion: "Check test files for usage patterns before implementation"
    based_on: "Test-driven repos show higher quality patterns"
```

### 1.2 Output Contracts

#### Extracted Pattern
```yaml
# data/patterns/P-001.yaml
pattern:
  id: "P-001"
  name: "JWT Refresh Token Rotation"
  category: "authentication"
  source:
    type: github
    url: "github.com/user/auth-system"
    repo: "user/auth-system"
    branch: "main"
    file_path: "src/auth/jwt_tokens.py"

  confidence: 0.92
  complexity: "medium"

  concepts:
    - name: "refresh_token"
      description: "Long-lived token for obtaining short-lived tokens"
    - name: "rotation"
      description: "Replacing old refresh token with new one"
    - name: "jti_claim"
      description: "Unique token ID for revocation"

  code_examples:
    - language: "python"
      file: "src/auth/jwt_tokens.py"
      function: "rotate_refresh_token"
      code: |
        def rotate_refresh_token(old_token):
            payload = decode(old_token)
            jti = payload['jti']
            new_token = create_token(refresh=True)
            revoke_old_token(jti)
            return new_token
      explanation: "This function rotates the refresh token by creating a new one and invalidating the old"

  relationships:
    - to: "P-002"  # Referenced pattern
      type: "implements"
      strength: 0.8

    - to: "P-003"
      type: "used_by"
      strength: 0.9

  extracted_at: "2026-02-10T10:30:00Z"
  extraction_method: "manual_analysis"
  tools_used: ["claude", "github-api"]
```

#### Pattern Extraction Event
```yaml
# communications/events.yaml
- timestamp: "2026-02-10T10:30:00Z"
  event_type: pattern.extracted
  agent: scout-worker
  run_id: "scout-001"
  correlation_id: "P-001"
  data:
    pattern_id: "P-001"
    pattern_name: "JWT Refresh Token Rotation"
    category: "authentication"
    source_url: "github.com/user/auth-system"
    confidence: 0.92
    complexity: "medium"
    concepts_count: 3
    code_examples_count: 1
    relationships_count: 2
```

#### Scout State Update
```yaml
# communications/scout-state.yaml
status: "scanning"
worker_run_id: "scout-001"
current_source:
  source_id: "SRC-001"
  source_url: "github.com/user/auth-system"
  source_type: github
  started_at: "2026-02-10T10:00:00Z"

progress:
  sources_scanned: 1
  patterns_extracted: 1
  sources_remaining: 9

worker_status: "completed"
completed_at: "2026-02-10T10:45:00Z"
patterns_extracted: 1

metadata:
  tokens_used: 2850
  tokens_budget: 3000
  efficiency: 0.95
```

#### Run Documentation
```yaml
# scout-worker/runs/run-001/metadata.yaml
run:
  id: "run-001"
  agent: scout-worker
  agent_type: worker
  pair: scout
  phase: extraction
  timestamp_start: "2026-02-10T10:00:00Z"
  timestamp_end: "2026-02-10T10:45:00Z"
  duration_seconds: 2700

state:
  source_id: "SRC-001"
  source_url: "github.com/user/auth-system"
  patterns_found: 1
  concepts_extracted: 3
  code_examples_found: 1
  status: "success"

tokens:
  used: 2850
  budget: 3000
  percentage: 95

results:
  status: "success"
  patterns:
    - id: "P-001"
      name: "JWT Refresh Token Rotation"
      confidence: 0.92

next_steps:
  - "Publish pattern:extracted event"
  - "Update scout-state.yaml"
  - "Update timeline-memory.md"

notes: |
  Pattern extraction completed successfully.
  Recommended next: Analyst worker will analyze this pattern.
```

---

## 2. Analyst Agent Interface

**Agent Type:** Analyst Worker
**Pair:** Analyst-Validator
**Input/Output:** Public-facing contracts

### 2.1 Input Contracts

#### Pattern to Analyze
```yaml
# data/patterns/P-001.yaml
pattern:
  id: "P-001"
  name: "JWT Refresh Token Rotation"
  category: "authentication"
  source:
    type: github
    url: "github.com/user/auth-system"
  confidence: 0.92
  complexity: "medium"
  concepts:
    - name: "refresh_token"
      description: "Long-lived token for obtaining short-lived tokens"
  code_examples:
    - language: "python"
      code: |
        def rotate_refresh_token(old_token):
            payload = decode(old_token)
            jti = payload['jti']
            new_token = create_token(refresh=True)
            revoke_old_token(jti)
            return new_token
```

#### BB5 Context
```yaml
# BB5 stack (injected via routes/context-checkpointing)
bb5_stack:
  current_framework: "claude-code"
  current_architecture: "agent-swarm"
  tech_stack: ["python", "yaml", "redis"]

bb5_context:
  existing_auth_patterns:
    - name: "session-based-auth"
      status: "implemented"
      files: ["src/auth/session.py"]
    - name: "basic-api-key"
      status: "implemented"
      files: ["src/api/key.py"]

  recent_commits:
    - commit: "abc123"
      date: "2026-02-09"
      changes: "Added user model, removed old auth"
```

#### Validator Feedback
```yaml
# agents/analyst-validator/memory/model-improvements.yaml
model_improvements:
  - run_id: "analyst-001"
    timestamp: "2026-02-10T11:00:00Z"
    observation: "Analyst consistently underestimates complexity by 1-2 points"
    correction: "Add +1.5 to complexity for patterns with async operations"
    based_on: "Executor task data shows 30% longer than estimated"

  - run_id: "analyst-002"
    timestamp: "2026-02-10T12:00:00Z"
    observation: "Good at identifying high-value patterns, sometimes misses medium-value"
    correction: "Include patterns with value_score 6-8 as 'medium' priority"
    based_on: "Current backlog composition"
```

### 2.2 Output Contracts

#### Analysis Result
```yaml
# data/analysis/P-001.yaml
analysis:
  pattern_id: "P-001"

  decision:
    recommendation: "recommend"  # recommend, defer, reject
    confidence: 0.85
    threshold_check:
      auto_approve_if: "complexity < 4 AND value > 7"
      auto_reject_if: "value < 3"
      human_review_if: "complexity > 7 OR value > 8"

  rationale: |
    Pattern has excellent fit for BB5. BB5 needs robust authentication
    and the refresh token rotation is a security best practice.
    Medium complexity is acceptable given the high value.

  value_score: 9.0
  complexity_score: 6.0
  total_score: 8.5

  value_factors:
    relevance_to_bb5:
      score: 9
      rationale: "BB5 needs enterprise-grade authentication"
    innovation_factor:
      score: 7
      rationale: "Rotation is industry standard, not novel"
    community_adoption:
      score: 10
      rationale: "Widely adopted in production systems"
    maintainer_quality:
      score: 9
      rationale: "Well-maintained, tested, documented"
    documentation_quality:
      score: 8
      rationale: "Good inline comments and docstrings"

  complexity_factors:
    integration_cost:
      lines_of_code: 45
      score: 5
      rationale: "Moderate code changes needed"

    dependency_count:
      count: 2
      score: 3
      rationale: "JWT library and token storage"

    breaking_changes_risk:
      level: medium
      score: 6
      rationale: "Requires migration from current auth approach"

    testing_effort:
      estimate_hours: 6
      score: 5
      rationale: "Security tests, integration tests"

    learning_curve:
      description: "Team needs to learn JWT patterns"
      score: 6
      rationale: "Standard JWT knowledge needed"

  maintenance_cost:
    update_frequency:
      score: 4
      rationale: "Rarely updated"
    issue_resolution_time:
      score: 9
      rationale: "JWT issues are well-documented"
    community_health:
      score: 9
      rationale: "Active development"
    documentation_maintenance:
      score: 8
      rationale: "Pattern is well-documented"

  estimated_integration_hours: 7
  estimated_maintenance_hours_per_year: 4

  task_estimation:
    difficulty: "medium"
    estimated_complexity_score: 6
    estimation_method: "historical_data"
    confidence: 0.8

  recommendations:
    priority: high
    phasing: "Phase 2"  # Phase 1, 2, or 3

  approval_required: false

  analyzed_at: "2026-02-10T11:30:00Z"
  analyzed_by: "analyst-worker"
```

#### Analysis Event
```yaml
# communications/events.yaml
- timestamp: "2026-02-10T11:30:00Z"
  event_type: analysis.complete
  agent: analyst-worker
  run_id: "analyst-001"
  correlation_id: "P-001"
  data:
    pattern_id: "P-001"
    decision: "recommend"
    value_score: 9.0
    complexity_score: 6.0
    total_score: 8.5
    confidence: 0.85
    estimated_hours: 7
    priority: high
```

#### Analyst State Update
```yaml
# communications/analyst-state.yaml
status: "analyzing"
worker_run_id: "analyst-001"
current_pattern:
  pattern_id: "P-001"
  name: "JWT Refresh Token Rotation"
  confidence: 0.92
  started_at: "2026-02-10T11:00:00Z"

progress:
  patterns_analyzed: 1
  recommendations_made: 1
  patterns_remaining: 9

worker_status: "completed"
completed_at: "2026-02-10T11:45:00Z"
patterns_analyzed: 1

metadata:
  tokens_used: 4520
  tokens_budget: 4800
  efficiency: 0.94
```

---

## 3. Planner Agent Interface

**Agent Type:** Planner Worker
**Pair:** Planner-Validator
**Input/Output:** Public-facing contracts

### 3.1 Input Contracts

#### Recommendation to Plan
```yaml
# data/analysis/P-001.yaml
analysis:
  pattern_id: "P-001"
  decision:
    recommendation: "recommend"
    confidence: 0.85
  value_score: 9.0
  complexity_score: 6.0
  total_score: 8.5
  estimated_integration_hours: 7
  estimated_maintenance_hours_per_year: 4
  difficulty: "medium"
```

#### BB5 Task Structure Template
```yaml
# agents/planner-worker/memory/task-templates.md
task_templates:
  authentication:
    subtasks:
      - title: "Implement JWT refresh token rotation"
        type: implementation
        estimated_hours: 3
        dependencies: []
        acceptance_criteria:
          - "Function rotate_refresh_token exists"
          - "Old token revocation working"
          - "Tests pass"

      - title: "Add security tests for token rotation"
        type: testing
        estimated_hours: 2
        dependencies: ["Implement JWT refresh token rotation"]
        acceptance_criteria:
          - "Integration tests added"
          - "Test coverage > 80%"

      - title: "Update authentication documentation"
        type: documentation
        estimated_hours: 1
        dependencies: ["Implement JWT refresh token rotation"]
        acceptance_criteria:
          - "README updated"
          - "Docstring added to function"

  caching:
    subtasks:
      - title: "Implement caching layer"
        type: implementation
        estimated_hours: 4
        dependencies: []
      - title: "Add cache invalidation tests"
        type: testing
        estimated_hours: 2
        dependencies: ["Implement caching layer"]
      - title: "Document cache behavior"
        type: documentation
        estimated_hours: 1
        dependencies: ["Implement caching layer"]
```

#### Validator Feedback
```yaml
# agents/planner-validator/memory/strategy-evolution.yaml
strategy_improvements:
  - run_id: "planner-001"
    timestamp: "2026-02-10T12:00:00Z"
    observation: "Planner sometimes omits integration tests"
    correction: "Always add integration test subtask for external integrations"
    based_on: "Executor reports 40% tasks missing tests"

  - run_id: "planner-002"
    timestamp: "2026-02-10T13:00:00Z"
    observation: "Dependency ordering sometimes incorrect"
    correction: "Validate dependencies DAG before creating tasks"
    based_on: "Executor reports dependency errors in 15% of tasks"
```

### 3.2 Output Contracts

#### BB5 Task Entry
```yaml
# communications/queue.yaml
queue:
  - task_id: "TASK-RAPS-001"
    pattern_id: "P-001"
    title: "Implement JWT Refresh Token Rotation"
    priority: high
    priority_score: 8.5
    estimated_hours: 7
    estimated_complexity: medium
    value_score: 9.0
    status: pending
    created_at: "2026-02-10T12:30:00Z"
    planned_by: "planner-worker-run-001"
    notes: |
      Pattern provides JWT refresh token rotation for BB5 authentication.
      Estimated 7 hours. Medium complexity.

      Key subtasks:
      1. Implement rotation function
      2. Add security tests
      3. Update documentation

    task_metadata:
      pattern_category: "authentication"
      difficulty: "medium"
      phasing: "Phase 2"
      approval_required: false

    subtasks:
      - task_id: "TASK-RAPS-001-01"
        title: "Implement JWT refresh token rotation"
        type: implementation
        estimated_hours: 3
        dependencies: []
        acceptance_criteria:
          - "Function rotate_refresh_token exists"
          - "Old token revocation working"
          - "Tests pass"

      - task_id: "TASK-RAPS-001-02"
        title: "Add security tests for token rotation"
        type: testing
        estimated_hours: 2
        dependencies: ["TASK-RAPS-001-01"]
        acceptance_criteria:
          - "Integration tests added"
          - "Test coverage > 80%"

      - task_id: "TASK-RAPS-001-03"
        title: "Update authentication documentation"
        type: documentation
        estimated_hours: 1
        dependencies: ["TASK-RAPS-001-01"]
        acceptance_criteria:
          - "README updated"
          - "Docstring added to function"

metadata:
  last_updated: "2026-02-10T12:35:00Z"
  updated_by: planner-worker
  queue_depth_target: 3-5
  current_depth: 2
  last_completed: null
```

#### Task Event
```yaml
# communications/events.yaml
- timestamp: "2026-02-10T12:35:00Z"
  event_type: tasks.new
  agent: planner-worker
  run_id: "planner-001"
  correlation_id: "TASK-RAPS-001"
  data:
    task_id: "TASK-RAPS-001"
    pattern_id: "P-001"
    subtasks_count: 3
    estimated_hours: 7
    priority: high
```

#### Task Package (Full Task Structure)
```yaml
# tasks/active/TASK-RAPS-001/TASK-RAPS-001.md
# Task: Implement JWT Refresh Token Rotation
# Created: 2026-02-10
# Priority: High
# Estimated: 7 hours

## Overview
Implement JWT refresh token rotation as described in pattern P-001 from github.com/user/auth-system.

## Goals
- Add rotate_refresh_token function
- Implement old token revocation
- Maintain security best practices
- Update documentation

## Acceptance Criteria
- [ ] Function rotate_refresh_token exists in src/auth/jwt_tokens.py
- [ ] Old tokens are revoked using jti claim
- [ ] New tokens are created with proper expiration
- [ ] Tests added and passing
- [ ] Documentation updated

## Subtasks
1. **Implement JWT refresh token rotation** (3h)
   - Dependencies: None
   - Acceptance: rotate_refresh_token function exists

2. **Add security tests** (2h)
   - Dependencies: Subtask 1
   - Acceptance: Integration tests passing

3. **Update documentation** (1h)
   - Dependencies: Subtask 1
   - Acceptance: README and docstrings updated

## Context
```yaml
# tasks/active/TASK-RAPS-001/context/pattern-analysis.yaml
pattern_id: "P-001"
source_url: "github.com/user/auth-system"
pattern_data:
  name: "JWT Refresh Token Rotation"
  category: "authentication"
  confidence: 0.92
  complexity: "medium"
```

# tasks/active/TASK-RAPS-001/context/source-reference.yaml
source_type: github
repo: "user/auth-system"
file_path: "src/auth/jwt_tokens.py"
commit: "abc123"
branch: "main"
```

#### Planner State Update
```yaml
# communications/planner-state.yaml
status: "planning"
worker_run_id: "planner-001"
current_recommendation:
  pattern_id: "P-001"
  name: "JWT Refresh Token Rotation"
  value_score: 9.0
  complexity_score: 6.0
  started_at: "2026-02-10T12:00:00Z"

progress:
  tasks_created: 1
  recommendations_planned: 1
  recommendations_remaining: 9

worker_status: "completed"
completed_at: "2026-02-10T12:35:00Z"
tasks_created: 1

metadata:
  tokens_used: 3250
  tokens_budget: 3600
  efficiency: 0.90
```

---

## 4. Executor Agent Interface

**Agent Type:** Executor (BB5 Executor)
**Input/Output:** Uses BB5's existing executor interface

### 4.1 Input Contracts

#### Task Queue
```yaml
# communications/queue.yaml (read by executor)
queue:
  - task_id: "TASK-RAPS-001"
    title: "Implement JWT Refresh Token Rotation"
    priority: high
    status: pending
    estimated_hours: 7
    created_at: "2026-02-10T12:30:00Z"
    planned_by: "planner-worker-run-001"

  - task_id: "TASK-RAPS-002"
    title: "Add Caching Layer"
    priority: medium
    status: pending
    estimated_hours: 6
    created_at: "2026-02-10T12:35:00Z"
    planned_by: "planner-worker-run-002"

metadata:
  last_updated: "2026-02-10T13:00:00Z"
  queue_depth: 2
```

### 4.2 Output Contracts

#### Task Execution Event
```yaml
# communications/events.yaml
- timestamp: "2026-02-10T13:00:00Z"
  event_type: task.started
  agent: executor
  run_id: "executor-001"
  correlation_id: "TASK-RAPS-001"
  data:
    task_id: "TASK-RAPS-001"
    subtasks: ["TASK-RAPS-001-01", "TASK-RAPS-001-02", "TASK-RAPS-001-03"]
    estimated_hours: 7
    started_at: "2026-02-10T13:00:00Z"
```

#### Task Completion Event
```yaml
# communications/events.yaml
- timestamp: "2026-02-10T14:00:00Z"
  event_type: task.completed
  agent: executor
  run_id: "executor-001"
  correlation_id: "TASK-RAPS-001"
  data:
    task_id: "TASK-RAPS-001"
    actual_hours: 8
    status: success
    completed_at: "2026-02-10T14:00:00Z"
    subtasks_completed: 3
    issues_encountered: []
```

#### Task Failure Event
```yaml
# communications/events.yaml
- timestamp: "2026-02-10T13:30:00Z"
  event_type: task.failed
  agent: executor
  run_id: "executor-001"
  correlation_id: "TASK-RAPS-001"
  data:
    task_id: "TASK-RAPS-001"
    error_type: "dependency_error"
    error_message: "Dependency TASK-RAPS-001-01 not found"
    status: failed
    completed_at: "2026-02-10T13:30:00Z"
    subtasks_failed: 1
    issues_encountered:
      - type: "dependency_not_found"
        subtask: "TASK-RAPS-001-01"
        message: "Subtask file not found in tasks/active/TASK-RAPS-001/subtasks/"
```

#### Executor Run Documentation
```yaml
# executor/runs/run-001/metadata.yaml
run:
  id: "run-001"
  agent: executor
  agent_type: executor
  phase: execution
  timestamp_start: "2026-02-10T13:00:00Z"
  timestamp_end: "2026-02-10T14:00:00Z"
  duration_seconds: 3600

state:
  tasks_in_queue: 2
  tasks_completed: 1
  tasks_failed: 0
  tasks_in_progress: 1
  status: "healthy"

tasks:
  - id: "TASK-RAPS-001"
    status: completed
    actual_hours: 8
    priority: high
    created_at: "2026-02-10T12:30:00Z"

metadata:
  tokens_used: 5200
  tokens_budget: 7500
  efficiency: 0.69

results:
  status: success
  completed_tasks: ["TASK-RAPS-001"]
  failed_tasks: []

notes: |
  Task TASK-RAPS-001 completed successfully.
  Estimated 7 hours, actual 8 hours (18% overestimate).

next_steps:
  - "Process next tasks in queue"
  - "Update queue status"
  - "Notify planner if quality concerns"
```

---

## 5. Communication Protocol

### 5.1 Event Schema

All events in `communications/events.yaml` follow this schema:

```yaml
# communications/events.yaml
events:
  - timestamp: "2026-02-10T12:00:00Z"
    event_type: "<event_name>"
    agent: "<agent_name>"
    run_id: "<run_id>"
    correlation_id: "<correlation_id or null>"
    data:
      "<field>": "<value>"

metadata:
  last_updated: "2026-02-10T12:00:00Z"
  event_count: 10
  version: "1.0.0"
```

### 5.2 Event Types

| Event Type | Agent | Direction | Purpose |
|------------|-------|-----------|---------|
| `source.discovered` | Scout Worker | Out | New source added to queue |
| `pattern.extracted` | Scout Worker | Out | Pattern extracted from source |
| `analysis.complete` | Analyst Worker | Out | Pattern analyzed |
| `tasks.new` | Planner Worker | Out | New BB5 task created |
| `task.started` | Executor | Out | Task execution started |
| `task.completed` | Executor | Out | Task completed successfully |
| `task.failed` | Executor | Out | Task failed |

### 5.3 Message Schema (Chat Log)

```yaml
# communications/chat-log.yaml
messages:
  - from: scout-worker
    to: scout-validator
    timestamp: "2026-02-10T10:15:00Z"
    type: question
    context:
      worker_run: "run-001"
      pattern_id: "P-001"
    content: "Should I extract test files for this repository?"

  - from: scout-validator
    to: scout-worker
    timestamp: "2026-02-10T10:20:00Z"
    type: answer
    context:
      worker_run: "run-001"
      pattern_id: "P-001"
    content: "Yes, test files often reveal usage patterns."

  - from: analyst-worker
    to: planner-worker
    timestamp: "2026-02-10T11:45:00Z"
    type: discovery
    context:
      worker_run: "run-001"
      pattern_id: "P-001"
    content: "High-value pattern found: JWT refresh token rotation."

  - from: planner-validator
    to: planner-worker
    timestamp: "2026-02-10T12:30:00Z"
    type: feedback
    context:
      worker_run: "run-001"
      task_id: "TASK-RAPS-001"
    content: "Consider adding integration tests as a separate subtask."

metadata:
  last_updated: "2026-02-10T12:30:00Z"
  message_count: 5
```

### 5.4 File-Based Protocol

#### Scout Worker → All Agents
- Writes to: `communications/events.yaml`, `communications/scout-state.yaml`
- Reads from: `communications/chat-log.yaml`

#### Analyst Worker → All Agents
- Writes to: `communications/events.yaml`, `communications/analyst-state.yaml`
- Reads from: `communications/chat-log.yaml`, `data/analysis/`

#### Planner Worker → All Agents
- Writes to: `communications/events.yaml`, `communications/planner-state.yaml`, `communications/queue.yaml`
- Reads from: `communications/chat-log.yaml`, `data/analysis/`

#### Executor Agent → All Agents
- Writes to: `communications/events.yaml`
- Reads from: `communications/queue.yaml`, `communications/chat-log.yaml`

---

## 6. Storage Interfaces

### 6.1 Neo4j Graph Schema

**Node Types:**

```cypher
// Pattern Node
CREATE (p:PatternNode {
  id: "P-001",
  name: "JWT Refresh Token Rotation",
  category: "authentication",
  confidence: 0.92,
  complexity_score: 6.0,
  value_score: 9.0,
  status: "approved",
  created_at: "2026-02-10T10:30:00Z"
})

// Concept Node
CREATE (c:ConceptNode {
  id: "C-001",
  name: "refresh_token",
  description: "Long-lived token for obtaining short-lived tokens"
})

// Source Node
CREATE (s:SourceNode {
  id: "SRC-001",
  source_type: "github",
  url: "github.com/user/auth-system",
  repo: "user/auth-system",
  branch: "main"
})
```

**Edge Types:**

```cypher
// Pattern implements concept
MATCH (p:PatternNode {id: "P-001"})
MATCH (c:ConceptNode {id: "C-001"})
CREATE (p)-[:IMPLEMENTS {strength: 0.9, discovered_at: "2026-02-10T10:30:00Z"}]->(c)

// Pattern used by source
MATCH (p:PatternNode {id: "P-001"})
MATCH (s:SourceNode {id: "SRC-001"})
CREATE (p)-[:USED_BY {strength: 1.0, discovered_at: "2026-02-10T10:30:00Z"}]->(s)

// Pattern derives from another
MATCH (p:PatternNode {id: "P-001"})
MATCH (c:PatternNode {id: "P-002"})
CREATE (p)-[:DERIVED_FROM {strength: 0.8, discovered_at: "2026-02-10T10:35:00Z"}]->(c)
```

**Query Patterns:**

```cypher
// Find all patterns by category
MATCH (p:PatternNode {category: "authentication"})
RETURN p

// Find patterns implementing a concept
MATCH (p:PatternNode)-[:IMPLEMENTS]->(c:ConceptNode {name: "refresh_token"})
RETURN p

// Find high-value patterns with low complexity
MATCH (p:PatternNode)
WHERE p.value_score >= 8 AND p.complexity_score <= 5
RETURN p

// Find pattern relationships
MATCH (p1:PatternNode)-[:IMPLEMENTS|DERIVED_FROM]-(p2:PatternNode)
RETURN p1, p2
```

### 6.2 Redis Data Structures

**Pattern Cache:**

```
# Key pattern: pattern:{id}
Key: pattern:P-001
Value: {"id": "P-001", "name": "JWT Refresh Token Rotation", "confidence": 0.92}
TTL: 3600 seconds

# Key pattern: pattern:{id}
Key: pattern:P-002
Value: {"id": "P-002", "name": "Role-Based Access Control", "confidence": 0.88}
TTL: 3600 seconds
```

**Work Queues:**

```
# Priority queue (list)
Key: queue:priority
Value: ["SRC-001", "SRC-003", "SRC-005"]

# Backlog queue (list)
Key: queue:backlog
Value: ["SRC-002", "SRC-004"]

# In-progress tracking (set)
Key: queue:in_progress
Value: ["SRC-006"]

# Completed today counter
Key: queue:completed:today
Value: 5
```

**Extraction Cache:**

```
# Source extraction cache
Key: cache:extraction:github.com/user/auth-system
Value: {"extracted_at": "2026-02-10T10:00:00Z", "patterns_found": 3}
TTL: 86400 seconds (24 hours)

# Test extraction cache
Key: cache:extraction:youtube.com/watch?v=xyz
Value: {"extracted_at": "2026-02-10T11:00:00Z", "transcript_length": 12000}
TTL: 86400 seconds
```

**Agent Heartbeats:**

```
# Agent last seen timestamps
Key: agent:scout-worker:last_seen
Value: "2026-02-10T12:00:00Z"

Key: agent:analyst-worker:last_seen
Value: "2026-02-10T11:45:00Z"

Key: agent:planner-worker:last_seen
Value: "2026-02-10T12:35:00Z"

TTL: 60 seconds
```

**Token Usage Tracking:**

```
# Daily token usage per agent
Key: usage:scout-worker:daily:2026-02-10
Value: {"tokens_used": 28500, "runs": 10}

Key: usage:analyst-worker:daily:2026-02-10
Value: {"tokens_used": 48000, "runs": 10}
```

### 6.3 File System Layout

```
blackbox5/
├── .autonomous/
│   └── research-pipeline/
│       ├── agents/
│       │   ├── scout-worker/
│       │   │   ├── memory/
│       │   │   │   ├── extraction-strategies.md
│       │   │   │   ├── patterns-learned.md
│       │   │   │   └── source-history.yaml
│       │   │   ├── metrics/
│       │   │   ├── runs/
│       │   │   └── state/
│       │   ├── analyst-worker/
│       │   │   ├── memory/
│       │   │   │   ├── scoring-models.md
│       │   │   │   ├── value-patterns.md
│       │   │   │   └── complexity-history.yaml
│       │   │   ├── metrics/
│       │   │   ├── runs/
│       │   │   └── state/
│       │   ├── planner-worker/
│       │   │   ├── memory/
│       │   │   │   ├── task-templates.md
│       │   │   │   └── estimation-models.md
│       │   │   ├── metrics/
│       │   │   ├── runs/
│       │   │   └── state/
│       │   └── executor/
│       │       └── runs/
│       │
│       ├── communications/
│       │   ├── events.yaml
│       │   ├── queue.yaml
│       │   ├── chat-log.yaml
│       │   ├── heartbeat.yaml
│       │   ├── scout-state.yaml
│       │   ├── analyst-state.yaml
│       │   └── planner-state.yaml
│       │
│       ├── context/
│       │   ├── routes.yaml
│       │   ├── sources.yaml
│       │   └── patterns-index.yaml
│       │
│       ├── data/
│       │   ├── patterns/
│       │   │   ├── P-001.yaml
│       │   │   └── ...
│       │   ├── analysis/
│       │   │   ├── P-001.yaml
│       │   │   └── ...
│       │   └── tasks/
│       │       ├── TASK-RAPS-001/
│       │       │   ├── TASK-RAPS-001.md
│       │       │   ├── subtasks/
│       │       │   │   ├── TASK-RAPS-001-01.md
│       │       │   │   └── ...
│       │       │   └── context/
│       │       │       ├── pattern-analysis.yaml
│       │       │       └── source-reference.yaml
│       │       └── ...
│       │
│       ├── swarm/
│       │   ├── heartbeat.yaml
│       │   ├── events.yaml
│       │   ├── state.yaml
│       │   └── ledger.md
│       │
│       └── operations/
│           ├── skill-usage.yaml
│           └── token-usage.yaml
```

---

## 7. State Management

### 7.1 Timeline Memory Structure

```yaml
# agents/{agent}/timeline-memory.md
timeline_memory:
  version: "1.0.0"
  agent: "scout-worker"
  total_runs: 0

swarm_context:
  swarm_role: worker
  pipeline_phase: scout
  pair_agent: scout-validator
  upstream_agents: []
  downstream_agents: [analyst-worker]

work_queue:
  priority_sources: []
  backlog: []
  in_progress: null
  completed_today: 0

scoring_model:
  extraction_accuracy: 0.0
  common_mistakes: []
  extraction_temperature: "balanced"

history: []

next_work:
  wait_for: null
  timeout_seconds: 3600
```

### 7.2 Running Memory Structure

```yaml
# agents/{agent}/running-memory.md
running_memory:
  current_run_id: null
  last_completed_run_id: null
  started_at: null
  last_updated: null

state:
  status: "idle"
  current_work: null
  progress: 0

notifications:
  pending: []
  read: []
```

### 7.3 State Synchronization

**Worker updates timeline-memory after each run:**

```yaml
# Update work_queue
work_queue:
  priority_sources: ["SRC-002"]
  backlog: ["SRC-003"]
  in_progress: null
  completed_today: 1

# Add to history
history:
  - run_id: "run-001"
    timestamp: "2026-02-10T10:30:00Z"
    source: "github.com/user/auth-system"
    patterns_extracted: 1
    pattern_ids: ["P-001"]
    status: "success"
```

---

## 8. Error Handling

### 8.1 Error Types

```yaml
# Error handling strategy
error_categories:
  transient:
    examples:
      - "Network timeout"
      - "API rate limit"
      - "Temporary service unavailability"
    strategy: "retry"
    max_retries: 3
    backoff: [1, 2, 4]
    backoff_unit: "seconds"

  recoverable:
    examples:
      - "Token limit reached"
      - "Partial extraction completed"
      - "Checkpoint save failed"
    strategy: "checkpoint"
    exit_status: "PARTIAL"
    checkpoint_files:
      - "THOUGHTS.md"
      - "RESULTS.md"
      - "DECISIONS.md"
      - "metadata.yaml"

  fatal:
    examples:
      - "Invalid source URL"
      - "Corrupted data"
      - "Validation failure"
      - "Missing required field"
    strategy: "fail-closed"
    exit_status: "BLOCKED"
    recovery: "manual_intervention"
    notification: true
```

### 8.2 Retry Logic

```yaml
# Retry configuration
retry_config:
  max_retries: 3
  initial_delay_seconds: 1
  max_delay_seconds: 8
  exponential_base: 2

retry_cases:
  - error_code: "ECONNRESET"
    retry: true
    priority: high

  - error_code: "429_RATE_LIMIT"
    retry: true
    backoff: 5  # seconds

  - error_code: "EINVALID_URL"
    retry: false
```

### 8.3 Checkpoint Recovery

```yaml
# Checkpoint format
checkpoint:
  status: "PARTIAL"
  agent: "scout-worker"
  run_id: "run-001"
  timestamp: "2026-02-10T10:45:00Z"

  work_context:
    current_source: "github.com/user/auth-system"
    patterns_extracted: 2
    remaining_patterns: 1

  checkpoint_data:
    last_processed_pattern: "P-001"
    thoughts_snapshot: "..."
    results_snapshot: "..."

  recovery_instructions: |
    Resume extraction from pattern P-003.
    Continue from last_checkpoint_point.

next_run:
  should_resume: true
  checkpoint_file: "agents/scout-worker/runs/run-001/THOUGHTS.md"
```

---

## 8. Error Handling (continued from above)

### 8.4 Recovery Patterns

**Pattern 1: Source Scan Failure**

```yaml
# scout-worker running-memory.md
error_recovery:
  error_type: "source_scan_failed"
  error_message: "Unable to clone repository"
  timestamp: "2026-02-10T10:00:00Z"

  action_taken:
    status: "defer"
    reason: "Network connectivity issue"
    suggested_action: "Retry after 5 minutes"
    user_notification: true
```

**Pattern 2: Token Budget Exceeded**

```yaml
# scout-worker/runs/run-002/RESULTS.md
status: "PARTIAL"
tokens_used: 3000
tokens_budget: 3000

checkpoint_at: "2026-02-10T11:30:00Z"
last_action: "Extracted concepts for pattern P-003"
remaining_work: |
  Remaining:
  - Analyze P-003 concepts
  - Write code examples
  - Save to data/patterns/

next_run:
  should_resume: true
  last_checkpoint: "concepts_analysis_complete"
```

**Pattern 3: Validation Failure**

```yaml
# scout-worker/runs/run-003/RESULTS.md
status: "BLOCKED"
blocker_type: "validation_error"
validation_failures:
  - field: "pattern_id"
    value: "P-003"
    reason: "ID collision with existing pattern"
  - field: "confidence"
    value: 0.1
    reason: "Confidence too low for valid pattern"

recovery_actions:
  - action: "review_and_fix"
    details: "Review and fix validation errors"
  - action: "notify_validator"
    details: "Alert scout-validator of validation failure"
```

### 8.5 Notification System

```yaml
# notifications/config.yaml
notification_levels:
  critical:
    - "fatal_errors"
    - "validation_failures"
    - "security_issues"

  high:
    - "transient_errors_with_exponential_backoff"
    - "blocker_errors"

  medium:
    - "recoverable_errors"
    - "quality_warnings"

notification_channels:
  - "chat-log.yaml"
  - "swarm/events.yaml"
  - "heartbeat.yaml"

notification_template_critical:
  type: "error"
  severity: "critical"
  message: "Critical error occurred: {error_message}"
  affected_agent: "{agent_name}"
  affected_task: "{task_id or null}"
```

---

## Summary

This document defines comprehensive interface specifications for the 4-agent research pipeline:

1. **Scout Agent** - Input: work_queue, Source config, Validator feedback; Output: pattern.yaml, events, state
2. **Analyst Agent** - Input: pattern.yaml, BB5 context, Validator feedback; Output: analysis.yaml, events, state
3. **Planner Agent** - Input: analysis.yaml, templates, Validator feedback; Output: task.yaml, queue.yaml, events
4. **Executor Agent** - Input: queue.yaml; Output: task events, run metadata

All interfaces use YAML schemas for machine-readable validation and human readability. The communication protocol uses event-driven messaging, and storage interfaces are defined for Neo4j, Redis, and the filesystem.
