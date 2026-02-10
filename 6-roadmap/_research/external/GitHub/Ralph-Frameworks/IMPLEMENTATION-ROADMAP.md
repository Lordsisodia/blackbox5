# BB5 Continuous Improvement Workflow - Implementation Roadmap

**Version:** 1.0.0
**Date:** 2026-02-10
**Status:** Draft - Ready for Review
**Estimated Duration:** 8 Weeks

---

## Executive Summary

This roadmap provides a practical, week-by-week implementation plan for the BB5 continuous improvement workflow. It builds upon the existing RALF infrastructure, addresses identified gaps from the audit, and integrates proven patterns from Ralph framework research.

**Key Deliverables:**
- 8 core agents with specialized responsibilities
- Circuit breaker safety system
- Structured memory management
- Event-driven communication
- Comprehensive monitoring

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    BB5 Continuous Improvement Architecture                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        Safety Layer                                  │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │   Circuit    │  │    Rate      │  │     Health Monitor       │  │   │
│  │  │   Breaker    │  │   Limiter    │  │                          │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        Agent Layer (8 Agents)                        │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │   │
│  │  │ Context  │ │ Planner  │ │ Executor │ │ Verifier │ │  Scribe  │  │   │
│  │  │Collector │ │          │ │          │ │          │ │          │  │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐                            │   │
│  │  │  Critic  │ │ Research │ │  Memory  │                            │   │
│  │  │          │ │   er     │ │ Manager  │                            │   │
│  │  └──────────┘ └──────────┘ └──────────┘                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      Communication Layer                             │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │   │
│  │  │ Event Bus   │  │  Queue      │  │   State     │  │  Memory    │ │   │
│  │  │  (Pub/Sub)  │  │  Manager    │  │   Store     │  │   Index    │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      Execution Layer                                 │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │  RALF-Core   │  │ Task Scanner │  │   Agent Spawner          │  │   │
│  │  │  (Enhanced)  │  │              │  │   (Task Tool)            │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      Observability Layer                             │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │   │
│  │  │  Metrics │ │   Logs   │ │  Events  │ │  Alerts  │ │Dashboard │  │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Foundation (Weeks 1-2)

**Goal:** Establish core infrastructure and minimum viable workflow

### Week 1: Safety & Core Infrastructure

#### Files to Create

| File | Path | Lines | Purpose |
|------|------|-------|---------|
| `circuit_breaker.py` | `bin/ralf-executor/circuit_breaker.py` | ~260 | Prevents runaway loops, tracks failures |
| `state_manager.py` | `bin/ralf-executor/state_manager.py` | ~180 | Centralized state management |
| `config.yaml` | `5-project-memory/blackbox5/.autonomous/config.yaml` | ~50 | System configuration |

#### Files to Modify

| File | Path | Changes |
|------|------|---------|
| `ralf-core.sh` | `bin/ralf-executor/ralf-core.sh` | Integrate circuit breaker, fix queue.yaml path |

#### Code Structure

**Circuit Breaker (`circuit_breaker.py`):**
```python
class CircuitState(Enum):
    CLOSED = "closed"
    HALF_OPEN = "half_open"
    OPEN = "open"

class CircuitBreaker:
    def __init__(self, state_file: str, config: CircuitBreakerConfig)
    def call(self, func: Callable, *args, **kwargs) -> Any
    def on_success(self)
    def on_failure(self, error: Exception)
    def on_no_progress(self)
    def get_status(self) -> dict
```

**State Manager (`state_manager.py`):**
```python
class StateManager:
    def __init__(self, state_file: str)
    def get_state(self) -> SystemState
    def update_state(self, updates: Dict)
    def acquire_lock(self, resource: str) -> bool
    def release_lock(self, resource: str)
```

#### Testing Approach

1. **Unit Tests:**
   ```python
   # test_circuit_breaker.py
   def test_opens_after_failures()
   def test_closes_after_success()
   def test_half_open_transition()
   ```

2. **Integration Tests:**
   - Simulate 3 consecutive failures → verify circuit opens
   - Wait cooldown → verify half-open state
   - Success in half-open → verify closed state

3. **Validation Criteria:**
   - Circuit opens after 3 consecutive failures
   - Cooldown period enforced (30 min default)
   - State persists across restarts

#### Success Criteria

- [ ] Circuit breaker prevents runaway loops
- [ ] State manager handles concurrent access
- [ ] All tests pass
- [ ] Documentation complete

---

### Week 2: Memory & Configuration System

#### Files to Create

| File | Path | Lines | Purpose |
|------|------|-------|---------|
| `memory_manager.py` | `bin/ralf-executor/memory_manager.py` | ~350 | Structured memory storage/retrieval |
| `config_loader.py` | `bin/ralf-executor/config_loader.py` | ~120 | Configuration management |
| `memory_schema.yaml` | `5-project-memory/blackbox5/.autonomous/schemas/memory.yaml` | ~80 | Memory structure definition |

#### Files to Modify

| File | Path | Changes |
|------|------|---------|
| `ralf-core.sh` | `bin/ralf-executor/ralf-core.sh` | Add memory extraction after task completion |

#### Code Structure

**Memory Manager (`memory_manager.py`):**
```python
class MemoryType(Enum):
    PATTERN = "pattern"
    DECISION = "decision"
    FIX = "fix"
    CONTEXT = "context"

class Memory:
    id: str
    memory_type: str
    content: str
    tags: List[str]
    source_task: str
    created: str

class MemoryManager:
    def add_memory(self, memory_type: MemoryType, content: str, tags: List[str], source_task: str)
    def get_memories(self, memory_type: Optional[MemoryType], tags: Optional[List[str]]) -> List[Memory]
    def get_memories_for_prompt(self, query: str, max_tokens: int) -> str
    def consolidate_memories(self)
```

#### Testing Approach

1. **Unit Tests:**
   ```python
   def test_add_memory()
   def test_retrieve_by_type()
   def test_retrieve_by_tags()
   def test_token_budget_enforcement()
   ```

2. **Integration Tests:**
   - Add 100 memories → verify retrieval performance
   - Test memory consolidation
   - Verify prompt injection works

3. **Validation Criteria:**
   - Memories retrieved in < 100ms
   - Token budget enforced
   - Relevant memories match query

#### Success Criteria

- [ ] Memory system stores/retrieves learnings
- [ ] Token budget management works
- [ ] Integration with ralf-core complete
- [ ] All tests pass

---

## Phase 2: Core Agents (Weeks 3-4)

**Goal:** Implement the 8 core agents with communication system

### Week 3: Agent Definitions & Hat System

#### Files to Create

| File | Path | Lines | Purpose |
|------|------|-------|---------|
| `hat_manager.py` | `bin/ralf-executor/hat_manager.py` | ~200 | Agent specialization routing |
| `hat-definitions.yaml` | `.claude/agents/hat-definitions.yaml` | ~300 | Agent role definitions |
| `bb5-planner.md` | `.claude/agents/bb5-planner.md` | ~150 | Planner agent definition |
| `bb5-verifier.md` | `.claude/agents/bb5-verifier.md` | ~150 | Verifier agent definition |
| `bb5-critic.md` | `.claude/agents/bb5-critic.md` | ~150 | Critic agent definition |
| `bb5-researcher.md` | `.claude/agents/bb5-researcher.md` | ~150 | Researcher agent definition |
| `bb5-memory-manager.md` | `.claude/agents/bb5-memory-manager.md` | ~150 | Memory agent definition |

#### Files to Modify

| File | Path | Changes |
|------|------|---------|
| `bb5-context-collector.md` | `.claude/agents/bb5-context-collector.md` | Update with hat triggers |
| `bb5-executor.md` | `.claude/agents/bb5-executor.md` | Update with hat triggers |
| `bb5-scribe.md` | `.claude/agents/bb5-scribe.md` | Update with hat triggers |

#### Code Structure

**Hat Manager (`hat_manager.py`):**
```python
class Hat:
    name: str
    triggers: List[str]
    instructions: str
    backend: str
    timeout: int

    def matches_trigger(self, event_type: str) -> bool
    def build_prompt(self, base_prompt: str, context: Dict) -> str

class HatManager:
    def __init__(self, config_file: str)
    def get_hat_for_event(self, event_type: str) -> Optional[Hat]
    def get_hat(self, name: str) -> Optional[Hat]
```

**Hat Definitions (`hat-definitions.yaml`):**
```yaml
hats:
  context-collector:
    name: "Context Collector"
    triggers: ["task.started", "context.needed"]
    backend: "claude-opus-4-6"
    timeout_minutes: 10

  planner:
    name: "Planner"
    triggers: ["context.collected"]
    backend: "claude-opus-4-6"
    timeout_minutes: 15

  executor:
    name: "Executor"
    triggers: ["plan.approved", "task.direct"]
    backend: "claude-opus-4-6"
    timeout_minutes: 30

  verifier:
    name: "Verifier"
    triggers: ["execution.completed"]
    backend: "claude-opus-4-6"
    timeout_minutes: 10

  scribe:
    name: "Scribe"
    triggers: ["*"]
    backend: "claude-opus-4-6"
    timeout_minutes: 5

  critic:
    name: "Critic"
    triggers: ["plan.created", "execution.completed"]
    backend: "claude-opus-4-6"
    timeout_minutes: 10

  researcher:
    name: "Researcher"
    triggers: ["research.needed", "context.needed"]
    backend: "claude-opus-4-6"
    timeout_minutes: 20

  memory-manager:
    name: "Memory Manager"
    triggers: ["execution.completed", "memory.consolidation.needed"]
    backend: "claude-opus-4-6"
    timeout_minutes: 10
```

#### Testing Approach

1. **Unit Tests:**
   ```python
   def test_hat_trigger_matching()
   def test_prompt_building()
   def test_hat_routing()
   ```

2. **Integration Tests:**
   - Test each hat trigger
   - Verify prompt generation
   - Test fallback routing

3. **Validation Criteria:**
   - All 8 hats defined
   - Triggers match correctly
   - Prompts include proper context

#### Success Criteria

- [ ] All 8 agent definitions complete
- [ ] Hat routing system functional
- [ ] Agent triggers documented
- [ ] All tests pass

---

### Week 4: Event Bus & Agent Spawner

#### Files to Create

| File | Path | Lines | Purpose |
|------|------|-------|---------|
| `event_bus.py` | `bin/ralf-executor/event_bus.py` | ~250 | Pub/sub event system |
| `agent_spawner_v2.py` | `bin/ralf-executor/agent_spawner_v2.py` | ~400 | Real agent spawning with Task tool |
| `event_schema.yaml` | `5-project-memory/blackbox5/.autonomous/schemas/events.yaml` | ~100 | Event structure definition |

#### Files to Modify

| File | Path | Changes |
|------|------|---------|
| `ralf-core.sh` | `bin/ralf-executor/ralf-core.sh` | Integrate event bus and agent spawner |
| `agent-spawner.py` | `bin/ralf-executor/agent-spawner.py` | Deprecate, redirect to v2 |

#### Code Structure

**Event Bus (`event_bus.py`):**
```python
@dataclass
class Event:
    type: str
    payload: Dict
    timestamp: str
    source: str
    id: str

class EventBus:
    def __init__(self, events_dir: str)
    def subscribe(self, event_type: str, handler: Callable)
    def publish(self, event_type: str, payload: Dict, source: str)
    def get_events(self, event_type: Optional[str], since: Optional[str]) -> List[Event]
```

**Agent Spawner V2 (`agent_spawner_v2.py`):**
```python
class AgentSpawner:
    def __init__(self, event_bus: EventBus, hat_manager: HatManager)
    def spawn_agent(self, hat_name: str, context: Dict) -> str
    def spawn_for_event(self, event: Event) -> Optional[str]
    def wait_for_completion(self, agent_id: str, timeout: int) -> AgentResult
    def get_agent_status(self, agent_id: str) -> AgentStatus
```

#### Testing Approach

1. **Unit Tests:**
   ```python
   def test_event_publish_subscribe()
   def test_event_persistence()
   def test_agent_spawn()
   def test_agent_timeout()
   ```

2. **Integration Tests:**
   - Full event flow: task.started → context.collected → plan.created → execution.completed
   - Agent spawning with Task tool
   - Event persistence across restarts

3. **Validation Criteria:**
   - Events published and received correctly
   - Agents spawn within 5 seconds
   - Event log persists to disk

#### Success Criteria

- [ ] Event bus handles 100+ events/day
- [ ] Agent spawner uses actual Task tool
- [ ] Event-driven workflow functional
- [ ] All tests pass

---

## Phase 3: Integration (Weeks 5-6)

**Goal:** Connect to existing BB5, replace fake implementations

### Week 5: RALF-Core Integration

#### Files to Create

| File | Path | Lines | Purpose |
|------|------|-------|---------|
| `ralf_core_v2.py` | `bin/ralf-executor/ralf_core_v2.py` | ~500 | Enhanced executor with all features |
| `integration_adapter.py` | `bin/ralf-executor/integration_adapter.py` | ~200 | Bridge old and new systems |

#### Files to Modify

| File | Path | Changes |
|------|------|---------|
| `ralf-core.sh` | `bin/ralf-executor/ralf-core.sh` | Add feature flags for v2 components |
| `queue.yaml` | `5-project-memory/blackbox5/.autonomous/agents/communications/queue.yaml` | Add v2 fields |

#### Code Structure

**RALF Core V2 (`ralf_core_v2.py`):**
```python
class RalfCoreV2:
    def __init__(self):
        self.circuit_breaker = CircuitBreaker(...)
        self.memory_manager = MemoryManager(...)
        self.hat_manager = HatManager(...)
        self.event_bus = EventBus(...)
        self.agent_spawner = AgentSpawner(...)
        self.state_manager = StateManager(...)

    def run_loop(self):
        while True:
            if not self.circuit_breaker.can_execute():
                self.handle_circuit_open()
                continue

            task = self.find_next_task()
            if not task:
                break

            self.event_bus.publish("task.started", {"task_id": task.id})

            # Spawn context collector
            self.agent_spawner.spawn_for_event(
                Event("context.needed", {"task": task})
            )

            # Execute with circuit breaker
            result = self.circuit_breaker.call(
                self.execute_task, task
            )

            # Extract memories
            self.memory_manager.extract_and_store_memories(
                task.run_folder, task.id
            )

            self.event_bus.publish("execution.completed", {
                "task_id": task.id,
                "status": result.status
            })
```

#### Testing Approach

1. **Integration Tests:**
   ```python
   def test_full_task_lifecycle()
   def test_circuit_breaker_integration()
   def test_memory_extraction()
   def test_event_flow()
   ```

2. **End-to-End Tests:**
   - Create test task → verify execution
   - Verify all agents spawned correctly
   - Check memory storage
   - Validate event log

3. **Validation Criteria:**
   - Task completes end-to-end
   - All components integrated
   - No regression in existing functionality

#### Success Criteria

- [ ] V2 components integrate with existing system
- [ ] Feature flags control rollout
- [ ] No regression in task execution
- [ ] All integration tests pass

---

### Week 6: Migration & Rollback

#### Files to Create

| File | Path | Lines | Purpose |
|------|------|-------|---------|
| `migration_script.py` | `bin/ralf-executor/migrate_to_v2.py` | ~300 | Data migration tool |
| `rollback_script.py` | `bin/ralf-executor/rollback_to_v1.py` | ~200 | Rollback tool |
| `MIGRATION-GUIDE.md` | `bin/ralf-executor/MIGRATION-GUIDE.md` | ~150 | Migration documentation |

#### Migration Steps

1. **Pre-Migration Checklist:**
   - [ ] Backup all data
   - [ ] Verify tests pass
   - [ ] Document current state
   - [ ] Prepare rollback plan

2. **Migration Process:**
   ```bash
   # 1. Stop RALF
   sudo systemctl stop bb5-ralf-executor

   # 2. Backup
   cp -r 5-project-memory/blackbox5/.autonomous ~/backups/autonomous-$(date +%Y%m%d)

   # 3. Run migration
   python bin/ralf-executor/migrate_to_v2.py

   # 4. Verify
   python bin/ralf-executor/verify_migration.py

   # 5. Start with v2
   sudo systemctl start bb5-ralf-executor
   ```

3. **Rollback Process:**
   ```bash
   # 1. Stop RALF
   sudo systemctl stop bb5-ralf-executor

   # 2. Run rollback
   python bin/ralf-executor/rollback_to_v1.py

   # 3. Restore data
   cp -r ~/backups/autonomous-$(date +%Y%m%d)/* 5-project-memory/blackbox5/.autonomous/

   # 4. Start v1
   sudo systemctl start bb5-ralf-executor
   ```

#### Testing Approach

1. **Migration Tests:**
   ```python
   def test_migration_preserves_tasks()
   def test_migration_preserves_memories()
   def test_migration_creates_v2_structure()
   ```

2. **Rollback Tests:**
   ```python
   def test_rollback_restores_v1_state()
   def test_rollback_preserves_new_data()
   ```

3. **Validation Criteria:**
   - Migration completes without data loss
   - Rollback restores original state
   - Both paths tested in staging

#### Success Criteria

- [ ] Migration script tested
- [ ] Rollback script tested
- [ ] Documentation complete
- [ ] Staging deployment successful

---

## Phase 4: Safety & Monitoring (Weeks 7-8)

**Goal:** Circuit breaker hardening, error handling, observability

### Week 7: Safety Hardening

#### Files to Create

| File | Path | Lines | Purpose |
|------|------|-------|---------|
| `error_handler.py` | `bin/ralf-executor/error_handler.py` | ~250 | Centralized error handling |
| `retry_manager.py` | `bin/ralf-executor/retry_manager.py` | ~180 | Exponential backoff retry |
| `safety_checks.py` | `bin/ralf-executor/safety_checks.py` | ~200 | Pre-execution validation |
| `alert_manager.py` | `bin/ralf-executor/alert_manager.py` | ~150 | Alert generation/dispatch |

#### Files to Modify

| File | Path | Changes |
|------|------|---------|
| `circuit_breaker.py` | `bin/ralf-executor/circuit_breaker.py` | Add alert integration |
| `ralf_core_v2.py` | `bin/ralf-executor/ralf_core_v2.py` | Integrate error handling |

#### Code Structure

**Error Handler (`error_handler.py`):**
```python
class ErrorCategory(Enum):
    TRANSIENT = "transient"  # Can retry
    PERMANENT = "permanent"  # Don't retry
    PERMISSION = "permission"  # Need user
    RESOURCE = "resource"  # Out of resources

class ErrorHandler:
    def __init__(self, circuit_breaker: CircuitBreaker, alert_manager: AlertManager)
    def handle_error(self, error: Exception, context: Dict) -> ErrorAction
    def classify_error(self, error: Exception) -> ErrorCategory
    def should_retry(self, error: Exception, attempt: int) -> bool
```

**Retry Manager (`retry_manager.py`):**
```python
class RetryConfig:
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0

class RetryManager:
    def __init__(self, config: RetryConfig)
    def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any
    def get_delay(self, attempt: int) -> float
```

#### Testing Approach

1. **Unit Tests:**
   ```python
   def test_error_classification()
   def test_retry_with_backoff()
   def test_circuit_breaker_integration()
   ```

2. **Chaos Tests:**
   - Simulate network failures
   - Simulate disk full
   - Simulate API rate limiting
   - Verify graceful degradation

3. **Validation Criteria:**
   - Transient errors retried with backoff
   - Permanent errors trigger circuit breaker
   - Alerts generated for critical errors

#### Success Criteria

- [ ] Error classification accurate
- [ ] Retry logic works with backoff
- [ ] Circuit breaker prevents runaway loops
- [ ] All safety tests pass

---

### Week 8: Observability & Monitoring

#### Files to Create

| File | Path | Lines | Purpose |
|------|------|-------|---------|
| `metrics_collector.py` | `bin/ralf-executor/metrics_collector.py` | ~200 | Metrics collection |
| `dashboard.py` | `bin/ralf-executor/dashboard.py` | ~300 | Web dashboard (optional) |
| `health_checker.py` | `bin/ralf-executor/health_checker.py` | ~150 | Health check endpoint |
| `MONITORING.md` | `bin/ralf-executor/MONITORING.md` | ~100 | Monitoring documentation |

#### Files to Modify

| File | Path | Changes |
|------|------|---------|
| `ralf-status.sh` | `bin/ralf-executor/ralf-status.sh` | Add metrics display |
| `ralf-redis-reporter.sh` | `bin/ralf-executor/ralf-redis-reporter.sh` | Add v2 metrics |

#### Code Structure

**Metrics Collector (`metrics_collector.py`):**
```python
class MetricsCollector:
    def __init__(self, metrics_dir: str)
    def record_task_start(self, task_id: str)
    def record_task_completion(self, task_id: str, status: str, duration: float)
    def record_agent_spawn(self, agent_type: str)
    def record_event(self, event_type: str)
    def get_metrics(self, since: datetime) -> MetricsReport
```

**Health Checker (`health_checker.py`):**
```python
class HealthChecker:
    def __init__(self, state_manager: StateManager)
    def check_health(self) -> HealthStatus
    def check_circuit_breaker(self) -> CircuitStatus
    def check_queue_depth(self) -> QueueStatus
    def check_agent_health(self) -> AgentStatus
```

#### Testing Approach

1. **Unit Tests:**
   ```python
   def test_metrics_collection()
   def test_health_check()
   def test_dashboard_rendering()
   ```

2. **Monitoring Tests:**
   - Verify metrics recorded correctly
   - Test alert thresholds
   - Validate dashboard displays

3. **Validation Criteria:**
   - Metrics accurate within 1%
   - Health checks complete in < 5s
   - Alerts fire within 30s of threshold breach

#### Success Criteria

- [ ] Metrics collection operational
- [ ] Health checks functional
- [ ] Dashboard displays key metrics
- [ ] Alerts configured and tested

---

## Testing Strategy Summary

### Test Pyramid

```
                    ┌─────────┐
                    │   E2E   │  (5%)
                    │  Tests  │
                   ┌┴─────────┴┐
                   │ Integration│  (15%)
                   │   Tests   │
                  ┌┴───────────┴┐
                  │    Unit      │  (80%)
                  │    Tests     │
                  └──────────────┘
```

### Test Coverage Targets

| Component | Target Coverage |
|-----------|-----------------|
| Circuit Breaker | 95% |
| Memory Manager | 90% |
| Event Bus | 90% |
| Agent Spawner | 85% |
| State Manager | 90% |
| Error Handler | 85% |

### CI/CD Integration

```yaml
# .github/workflows/ralf-tests.yml
name: RALF Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Unit Tests
        run: pytest bin/ralf-executor/tests/unit/
      - name: Run Integration Tests
        run: pytest bin/ralf-executor/tests/integration/
      - name: Coverage Report
        run: pytest --cov=bin/ralf-executor --cov-report=xml
```

---

## Risk Mitigation

### Identified Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Task tool API changes | Medium | High | Abstract agent spawning behind interface |
| Context window overflow | High | Medium | Token budget enforcement, summarization |
| Circuit breaker false positives | Low | High | Configurable thresholds, manual override |
| Memory bloat | Medium | Medium | Consolidation, archiving old memories |
| Event log corruption | Low | High | Atomic writes, backup/restore |
| Agent coordination failures | Medium | High | Timeouts, retry logic, circuit breaker |

### Rollback Plan

**Level 1: Feature Flag Disable**
```python
if config.v2_features_enabled:
    use_v2_components()
else:
    use_v1_components()
```

**Level 2: Component Rollback**
```bash
# Revert specific component
git checkout HEAD~1 -- bin/ralf-executor/circuit_breaker.py
```

**Level 3: Full Rollback**
```bash
# Run rollback script
python bin/ralf-executor/rollback_to_v1.py
```

---

## Success Metrics

### Phase 1 (Foundation)
- [ ] Zero runaway loops (circuit breaker catches all)
- [ ] State management handles 1000+ tasks
- [ ] Memory system retrieves in < 100ms

### Phase 2 (Core Agents)
- [ ] All 8 agents defined and functional
- [ ] Hat routing accuracy > 95%
- [ ] Event bus handles 1000+ events/day

### Phase 3 (Integration)
- [ ] No regression in task completion rate
- [ ] Migration completes in < 30 minutes
- [ ] Rollback tested and functional

### Phase 4 (Safety & Monitoring)
- [ ] Error detection < 5 seconds
- [ ] Alert delivery < 30 seconds
- [ ] Dashboard shows real-time metrics

### Overall Success Criteria
- [ ] Task completion rate > 90%
- [ ] Average task duration reduced by 20%
- [ ] Zero critical failures in 30 days
- [ ] Documentation coverage 100%

---

## File Summary

### New Files (Total: 25)

| Phase | Count | Files |
|-------|-------|-------|
| 1 | 5 | circuit_breaker.py, state_manager.py, config.yaml, config_loader.py, memory_schema.yaml |
| 2 | 9 | hat_manager.py, hat-definitions.yaml, 6 agent definitions, event_bus.py, agent_spawner_v2.py, event_schema.yaml |
| 3 | 5 | ralf_core_v2.py, integration_adapter.py, migration_script.py, rollback_script.py, MIGRATION-GUIDE.md |
| 4 | 6 | error_handler.py, retry_manager.py, safety_checks.py, alert_manager.py, metrics_collector.py, health_checker.py |

### Modified Files (Total: 8)

| Phase | Files |
|-------|-------|
| 1 | ralf-core.sh (x2) |
| 2 | 3 agent definitions |
| 3 | ralf-core.sh, queue.yaml, agent-spawner.py |
| 4 | circuit_breaker.py, ralf_core_v2.py, ralf-status.sh, ralf-redis-reporter.sh |

### Estimated Total Lines of Code

- Python: ~4,500 lines
- YAML: ~800 lines
- Markdown: ~1,200 lines
- Shell: ~200 lines
- **Total: ~6,700 lines**

---

## Timeline Summary

```
Week 1-2:   [Foundation]     Safety + Memory + Config
Week 3-4:   [Core Agents]    8 Agents + Event Bus + Spawner
Week 5-6:   [Integration]    V2 Integration + Migration
Week 7-8:   [Safety/Monitor] Error Handling + Observability

Milestones:
├── Week 2: Foundation Complete
├── Week 4: Agents Functional
├── Week 6: Integration Complete
└── Week 8: Production Ready
```

---

## Next Steps

1. **Review this roadmap** with stakeholders
2. **Create detailed task breakdown** for Week 1
3. **Set up development environment** for v2 work
4. **Begin Phase 1 implementation**

---

*Roadmap Version: 1.0.0*
*Last Updated: 2026-02-10*
*For questions, see BB5-IMPLEMENTATION-AUDIT.md and BB5-INTEGRATION-GUIDE.md*
