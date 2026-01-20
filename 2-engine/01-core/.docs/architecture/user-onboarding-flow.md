# User Onboarding Flow - System Architecture

**Version:** 1.0.0  
**Date:** 2026-01-20  
**Status:** Design Document  
**Author:** Architect Agent

---

## 1. Architecture Overview

### 1.1 High-Level System Design

The User Onboarding Flow is a multi-stage, event-driven system designed to guide new users through the Blackbox5 engine initialization process. It integrates with the existing agent-based architecture and provides a seamless, progressive experience for users setting up their development environment.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          USER ONBOARDING SYSTEM                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐  │
│  │  PRESENTER  │────▶│  ORCHESTRAT │────▶│  STATE      │────▶│ PERSISTENCE │  │
│  │   LAYER     │     │    OR       │     │  MANAGER    │     │   LAYER     │  │
│  └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘  │
│         │                   │                    │                   │         │
│         ▼                   ▼                    ▼                   ▼         │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐  │
│  │   CLI /     │     │  ONBOARDING │     │  PROGRESS   │     │  POSTGRES   │  │
│  │   API       │     │  AGENT      │     │  TRACKER    │     │  /  FILE    │  │
│  │  INTERFACES │     │  (BB5 AGENT)│     │  (TODO)     │     │  STORAGE    │  │
│  └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Component Decomposition

| Component | Responsibility | Interface |
|-----------|----------------|------------|
| **OnboardingPresenter** | UI/UX layer for presenting onboarding steps | `IOnboardingPresenter` |
| **OnboardingOrchestrator** | Coordinates onboarding flow and step transitions | `IOnboardingOrchestrator` |
| **OnboardingAgent** | BB5 agent that executes onboarding logic | Extends `BaseAgent` |
| **OnboardingStateManager** | Manages onboarding state and progress | `IOnboardingStateManager` |
| **ProgressTracker** | Integration with existing TODO system | Uses `TodoManager` |
| **OnboardingRepository** | Persistence layer for onboarding data | `IOnboardingRepository` |
| **EventPublisher** | Emits onboarding lifecycle events | Uses `EventBus` |

---

## 2. Architecture Diagram

### 2.1 Layer Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                            PRESENTATION LAYER                                 │
├──────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐          │
│  │   CLI Commands  │    │   FastAPI       │    │   WebSocket     │          │
│  │   (onboarding)  │    │   Endpoints     │    │   (Real-time)   │          │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘          │
└──────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                            APPLICATION LAYER                                   │
├──────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    ONBOARDING ORCHESTRATOR                            │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌─────────────┐ │   │
│  │  │ Step Factory │ │ Flow Builder │ │Validator     │ │Transition   │ │   │
│  │  │              │ │              │ │              │ │Handler      │ │   │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └─────────────┘ │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                            DOMAIN LAYER                                        │
├──────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐          │
│  │ Onboarding Flow │    │ Onboarding Step │    │  User Profile   │          │
│  │    (Aggregate)  │    │   (Entity)      │    │    (Entity)     │          │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘          │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐          │
│  │Step Definition  │    │ Onboarding State│    │ Completion Cert │          │
│  │   (Value Obj)   │    │   (Value Obj)   │    │   (Value Obj)   │          │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘          │
└──────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                            INFRASTRUCTURE LAYER                                 │
├──────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │Repository   │ │ Event Bus   │ │ Config      │ │ Logging     │            │
│  │(PostgreSQL) │ │ (Existing)  │ │ (Existing)  │ │ (Existing)  │            │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘            │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Sequence Diagram: Initial Onboarding Flow

```
User                CLI               Orchestrator         Agent           StateMgr
 │                   │                    │                 │                │
 │──onboard start───▶│                    │                 │                │
 │                   │──initiate()──────▶│                 │                │
 │                   │                    │──create flow──▶│                │
 │                   │                    │                 │──get state───▶│
 │                   │                    │                 │◀──────────────│
 │                   │                    │◀──flow config──│                │
 │                   │◀──show step 1──────│                 │                │
 │◀──────────────────│                    │                 │                │
 │                   │                    │                 │                │
 │──provide input────│                    │                 │                │
 │                   │──submit(input)────▶│                 │                │
 │                   │                    │──validate──────▶│                │
 │                   │                    │◀──valid────────│                │
 │                   │                    │──save progress─▶│                │
 │                   │                    │◀──saved────────│                │
 │                   │◀──show step 2──────│                 │                │
 │◀──────────────────│                    │                 │                │
 ... (repeats for each step)                                     │
 │                   │                    │                 │                │
 │                   │                    │──complete──────▶│                │
 │                   │                    │──emit event────▶│                │
 │                   │◀──cert generated───│                 │                │
 │◀──────────────────│                    │                 │                │
```

---

## 3. Component Details

### 3.1 OnboardingOrchestrator

**Purpose:** Central coordinator for the onboarding flow lifecycle.

**Responsibilities:**
- Build and configure onboarding flows based on user type
- Manage step transitions and validation
- Handle skip/redo logic for optional steps
- Emit lifecycle events via EventBus

**Interface:**

```python
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

class OnboardingState(Enum):
    """States in the onboarding lifecycle."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    FAILED = "failed"

class StepTransition(Enum):
    """Allowed step transitions."""
    NEXT = "next"
    PREVIOUS = "previous"
    SKIP = "skip"
    JUMP = "jump"
    COMPLETE = "complete"

@dataclass
class OnboardingFlow:
    """Represents a complete onboarding flow configuration."""
    flow_id: str
    name: str
    description: str
    user_type: str
    steps: List['OnboardingStep']
    allow_skip: bool = True
    allow_redo: bool = True
    required_for_completion: float = 0.8  # 80% of steps required

@dataclass
class OnboardingStep:
    """Represents a single onboarding step."""
    step_id: str
    name: str
    description: str
    optional: bool = False
    dependencies: List[str] = None  # step_ids that must complete first
    input_schema: Dict[str, Any] = None
    validator: str = None  # Validator function name
    agent_required: bool = False
    estimated_duration: int = 5  # minutes

@dataclass
class OnboardingProgress:
    """Tracks user progress through onboarding."""
    user_id: str
    flow_id: str
    current_step_index: int
    completed_steps: List[str]
    skipped_steps: List[str]
    step_data: Dict[str, Any]  # Data collected from each step
    state: OnboardingState
    started_at: str
    last_activity: str
    completed_at: Optional[str] = None

class IOnboardingOrchestrator(ABC):
    """Interface for onboarding orchestration."""
    
    @abstractmethod
    async def initiate_onboarding(
        self, 
        user_id: str, 
        user_type: str = "default"
    ) -> OnboardingFlow:
        """Initialize onboarding for a new user."""
        pass
    
    @abstractmethod
    async def get_current_step(
        self, 
        user_id: str
    ) -> Optional[OnboardingStep]:
        """Get the current step for a user."""
        pass
    
    @abstractmethod
    async def submit_step_input(
        self, 
        user_id: str, 
        step_id: str, 
        input_data: Dict[str, Any]
    ) -> StepTransition:
        """Process input for a step and determine next action."""
        pass
    
    @abstractmethod
    async def skip_step(
        self, 
        user_id: str, 
        step_id: str
    ) -> bool:
        """Skip an optional step."""
        pass
    
    @abstractmethod
    async def redo_step(
        self, 
        user_id: str, 
        step_id: str
    ) -> bool:
        """Redo a previously completed step."""
        pass
    
    @abstractmethod
    async def pause_onboarding(self, user_id: str) -> bool:
        """Pause the onboarding flow."""
        pass
    
    @abstractmethod
    async def resume_onboarding(self, user_id: str) -> Optional[OnboardingStep]:
        """Resume a paused onboarding flow."""
        pass
    
    @abstractmethod
    async def get_progress(self, user_id: str) -> OnboardingProgress:
        """Get current onboarding progress."""
        pass
    
    @abstractmethod
    async def complete_onboarding(self, user_id: str) -> Dict[str, Any]:
        """Finalize onboarding and generate completion artifacts."""
        pass
```

### 3.2 OnboardingAgent

**Purpose:** BB5 agent that handles complex onboarding tasks requiring LLM assistance.

**Integration:** Extends `BaseAgent` from `agents/core/base_agent.py`

**Agent Configuration:**

```python
ONBOARDING_AGENT_CONFIG = AgentConfig(
    name="onboarding",
    full_name="Onboarding Specialist",
    role="Guide users through the Blackbox5 onboarding process",
    category="specialist",
    description="Specializes in user onboarding, setup guidance, and configuration assistance",
    capabilities=[
        "analyze_user_needs",
        "suggest_configuration",
        "generate_setup_scripts",
        "troubleshoot_setup_issues",
        "create_checklist"
    ],
    tools=[
        "file_operations",
        "config_manager",
        "template_generator"
    ],
    temperature=0.7,
    max_tokens=2048
)
```

### 3.3 OnboardingStateManager

**Purpose:** Manages the state of user onboarding flows.

**Integration:** Uses existing `StateManager` from `state/state_manager.py`

**State Schema:**

```python
ONBOARDING_STATE_SCHEMA = {
    "user_id": "str",
    "flow_id": "str",
    "state": "OnboardingState",
    "current_step": "str",
    "completed_steps": "list[str]",
    "step_data": "dict",
    "metadata": {
        "started_at": "datetime",
        "last_activity": "datetime",
        "completed_at": "datetime"
    }
}
```

### 3.4 ProgressTracker Integration

**Purpose:** Track onboarding tasks using the existing TODO system.

**Integration:** Uses `TodoManager` from `tracking/todo_manager.py`

```python
class OnboardingProgressTracker:
    """Integration with TodoManager for onboarding tasks."""
    
    def __init__(self, todo_manager: TodoManager):
        self.todo_manager = todo_manager
    
    async def create_onboarding_task_list(
        self, 
        user_id: str, 
        flow: OnboardingFlow
    ) -> str:
        """Create a TODO list for the onboarding flow."""
        tasks = [
            {
                "content": f"Complete: {step.name}",
                "activeForm": f"Completing {step.name}...",
                "status": "pending" if not step.optional else "skipped"
            }
            for step in flow.steps
        ]
        
        return await self.todo_manager.create_list(
            name=f"Onboarding: {flow.name}",
            tasks=tasks,
            metadata={"user_id": user_id, "flow_id": flow.flow_id}
        )
```

### 3.5 Data Flow

**Configuration Loading Flow:**

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ User/CLI    │────▶│ Orchestrator│────▶│ConfigManager│────▶│Config File  │
│ Request     │     │             │     │             │     │or Cache     │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │Onboarding   │
                    │Flow Builder │
                    └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │State Manager│
                    │(Save State) │
                    └─────────────┘
```

**Step Execution Flow:**

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│User Input   │────▶│ Orchestrator│────▶│ Validator   │────▶│ Onboarding  │
│             │     │             │     │             │     │ Agent       │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │State Manager│
                    │(Update)     │
                    └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │EventBus     │
                    │(Publish)    │
                    └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │TodoManager  │
                    │(Update)     │
                    └─────────────┘
```

---

## 4. Quality Attributes

### 4.1 Scalability

**Horizontal Scaling:**
- Stateless orchestrator design allows multiple instances
- PostgreSQL connection pooling for concurrent users
- Event-driven architecture enables async processing

**Vertical Scaling:**
- Lazy loading of onboarding agent (only when needed)
- Caching of flow definitions

**Scaling Strategy:**

```python
class OnboardingOrchestratorConfig:
    """Configuration for scaling the orchestrator."""
    max_concurrent_users: int = 1000
    state_cache_ttl: int = 3600  # 1 hour
    flow_definition_cache_size: int = 100
    agent_pool_size: int = 10
```

### 4.2 Reliability

**Fault Tolerance:**
- State persistence after each step completion
- Automatic recovery from pause state
- Circuit breaker for external dependencies

**Resilience Patterns:**

```python
from core.resilience.circuit_breaker import CircuitBreaker, CircuitBreakerConfig

class OnboardingService:
    """Onboarding service with resilience patterns."""
    
    def __init__(self):
        # Circuit breaker for external service calls
        self.cb_config = CircuitBreakerConfig(
            failure_threshold=3,
            recovery_timeout=60,
            expected_exception=Exception
        )
        self.circuit_breaker = CircuitBreaker(
            "onboarding_service",
            self.cb_config
        )
    
    @circuit_breaker
    async def call_external_service(self, user_id: str):
        """External service call with circuit breaker protection."""
        pass
```

### 4.3 Security Considerations

**Input Validation:**
- JSON schema validation for all step inputs
- Sanitization of user-provided configuration
- Rate limiting on onboarding endpoints

**Data Protection:**

```python
class OnboardingValidator:
    """Validator for onboarding inputs."""
    
    INPUT_SCHEMAS = {
        "api_key": {
            "type": "string",
            "pattern": r"^[a-zA-Z0-9_-]{20,}$",
            "minLength": 20,
            "description": "API key validation"
        },
        "project_path": {
            "type": "string",
            "pattern": r"^[\w\-./]+$",
            "description": "Project path validation"
        }
    }
    
    @staticmethod
    def validate_input(step_id: str, input_data: Dict[str, Any]) -> bool:
        """Validate input against schema."""
        # Implementation using jsonschema
        pass
```

**Authentication/Authorization:**
- User session validation before onboarding access
- Permission checks for administrative user types

### 4.4 Performance Characteristics

**Target Metrics:**
- Step transition latency: < 100ms (cached) / < 500ms (uncached)
- Concurrent user support: 1000+ simultaneous onboarding sessions
- State persistence: < 50ms
- Flow initialization: < 200ms

**Optimization Strategies:**

```python
from functools import lru_cache
import asyncio

class PerformanceOptimizedOrchestrator:
    """Orchestrator with performance optimizations."""
    
    @lru_cache(maxsize=100)
    def _get_flow_definition(self, flow_id: str) -> OnboardingFlow:
        """Cache flow definitions in memory."""
        pass
    
    async def batch_update_progress(
        self, 
        user_ids: List[str]
    ) -> Dict[str, OnboardingProgress]:
        """Batch progress updates for efficiency."""
        tasks = [self.get_progress(uid) for uid in user_ids]
        return await asyncio.gather(*tasks)
```

---

## 5. Technology Recommendations

### 5.1 Programming Languages

| Component | Language | Rationale |
|-----------|----------|-----------|
| Core System | Python 3.11+ | Consistent with existing BB5 codebase |
| CLI | Python 3.11+ | Uses existing CLI framework |
| API | Python 3.11+ | FastAPI integration |
| Database | PostgreSQL | Existing infrastructure, ACID compliance |
| Frontend | TypeScript | Type safety for web interface (optional) |

### 5.2 Frameworks and Libraries

```python
# requirements.txt for onboarding module

# Core dependencies
fastapi==0.104.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.23
asyncpg==0.29.0  # Async PostgreSQL driver

# Validation
jsonschema==4.20.0
python-dotenv==1.0.0

# Existing BB5 dependencies
# - core modules (already present)
# - agents/core/base_agent.py
# - state/state_manager.py
# - tracking/todo_manager.py
# - communication/event_bus.py

# CLI enhancement
rich==13.7.0  # Pretty CLI output
questionary==2.0.1  # Interactive prompts

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-mock==3.12.0
```

### 5.3 Database Schema

**PostgreSQL Tables:**

```sql
-- Onboarding flows definition
CREATE TABLE onboarding_flows (
    flow_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    user_type VARCHAR(50) NOT NULL,
    flow_definition JSONB NOT NULL,
    version INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User onboarding state
CREATE TABLE user_onboarding (
    user_id VARCHAR(100) PRIMARY KEY,
    flow_id VARCHAR(50) REFERENCES onboarding_flows(flow_id),
    state VARCHAR(20) NOT NULL,
    current_step_index INT DEFAULT 0,
    completed_steps TEXT[] DEFAULT '{}',
    skipped_steps TEXT[] DEFAULT '{}',
    step_data JSONB DEFAULT '{}',
    started_at TIMESTAMP NOT NULL,
    last_activity TIMESTAMP NOT NULL,
    completed_at TIMESTAMP
);

-- Onboarding audit log
CREATE TABLE onboarding_audit_log (
    log_id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    step_id VARCHAR(50),
    old_state VARCHAR(20),
    new_state VARCHAR(20),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_user_onboarding_flow ON user_onboarding(flow_id);
CREATE INDEX idx_user_onboarding_state ON user_onboarding(state);
CREATE INDEX idx_audit_log_user ON onboarding_audit_log(user_id);
CREATE INDEX idx_audit_log_event ON onboarding_audit_log(event_type);
```

### 5.4 Infrastructure Tools

| Tool | Purpose | Integration |
|------|---------|-------------|
| Docker | Containerization | Consistent deployment |
| PostgreSQL | State persistence | Existing infrastructure |
| Redis | Caching layer | Optional, for performance |
| Prometheus | Metrics collection | Existing monitoring |
| Grafana | Monitoring dashboard | Existing observability |

---

## 6. Trade-offs and Decisions

### 6.1 Key Architectural Decisions

| Decision | Choice | Rationale | Trade-off |
|----------|--------|-----------|-----------|
| **State Management** | Centralized StateManager | Consistency with BB5 architecture | Single point of failure (mitigated by persistence) |
| **Flow Definition Storage** | PostgreSQL | ACID compliance, queryable | Slower than in-memory (mitigated by caching) |
| **Agent Usage** | Optional per step | Cost efficiency, faster simple steps | Complex steps require LLM latency |
| **Event Bus Integration** | EventBus for all events | Decoupling, extensibility | Slight latency overhead |
| **TODO Integration** | TodoManager for tracking | User visibility, existing system | Dependency on TODO system |

### 6.2 Alternative Approaches Considered

**1. Flow Definition: Hardcoded vs Database-Driven**

**Decision:** Database-driven flows

**Rationale:**
- Enables runtime flow modifications
- Supports A/B testing of onboarding flows
- Easier to add new user types

**Trade-off:** More complex initialization vs simple hardcoded flows

**2. State Storage: In-Memory vs Persistent**

**Decision:** Persistent with in-memory cache

**Rationale:**
- Survives service restarts
- Supports long onboarding sessions (days)
- Enables multi-instance deployments

**Trade-off:** Additional I/O overhead vs pure in-memory

**3. Step Validation: Client-side vs Server-side**

**Decision:** Server-side with optional client-side hints

**Rationale:**
- Security: cannot trust client validation
- Consistency: single source of truth
- Auditability: all validations logged

**Trade-off:** Higher latency vs pure client-side validation

**4. Agent Architecture: Dedicated Agent vs Shared Agent Pool**

**Decision:** Dedicated OnboardingAgent with shared capability

**Rationale:**
- Specialized prompts for onboarding
- Consistent user experience
- Can use shared agent pool for scale

**Trade-off:** Resource commitment vs on-demand allocation

### 6.3 Extensibility Considerations

**Adding New User Types:**

```python
# Simply add a new flow definition
NEW_USER_FLOW = OnboardingFlow(
    flow_id="enterprise_user",
    name="Enterprise Onboarding",
    user_type="enterprise",
    steps=[
        # Define enterprise-specific steps
    ]
)

# Register with orchestrator
await orchestrator.register_flow(NEW_USER_FLOW)
```

**Adding New Step Types:**

```python
# Implement step interface
class CustomOnboardingStep(OnboardingStep):
    async def execute(self, input_data: Dict[str, Any]) -> StepResult:
        # Custom logic
        pass
    
    async def validate(self, input_data: Dict[str, Any]) -> bool:
        # Custom validation
        pass
```

---

## 7. Implementation Roadmap

### Phase 1: Core Foundation (Week 1)
- [ ] Create domain models and interfaces
- [ ] Implement OnboardingOrchestrator
- [ ] Set up database schema
- [ ] Integrate with StateManager

### Phase 2: Agent Integration (Week 2)
- [ ] Implement OnboardingAgent
- [ ] Create step validators
- [ ] Integrate with EventBus
- [ ] Unit tests for core logic

### Phase 3: CLI Integration (Week 3)
- [ ] Add CLI commands for onboarding
- [ ] Implement progress display
- [ ] Add pause/resume functionality
- [ ] Integration tests

### Phase 4: API Integration (Week 4)
- [ ] FastAPI endpoints
- [ ] WebSocket support for real-time updates
- [ ] Authentication integration
- [ ] Documentation

### Phase 5: Polish & Optimization (Week 5)
- [ ] Performance optimization
- [ ] Error handling refinement
- [ ] User experience improvements
- [ ] Monitoring and observability

---

## 8. Appendix

### A. Example Flow Definitions

```python
# Default developer onboarding flow
DEFAULT_ONBOARDING_FLOW = OnboardingFlow(
    flow_id="default_developer",
    name="Default Developer Onboarding",
    description="Get started with Blackbox5 for development",
    user_type="developer",
    steps=[
        OnboardingStep(
            step_id="welcome",
            name="Welcome to Blackbox5",
            description="Learn about the BB5 engine and its capabilities",
            optional=False,
            agent_required=False
        ),
        OnboardingStep(
            step_id="config_setup",
            name="Configuration Setup",
            description="Configure your BB5 environment",
            optional=False,
            input_schema={
                "project_name": {"type": "string"},
                "api_key": {"type": "string"},
                "workspace_path": {"type": "string"}
            },
            validator="validate_config",
            agent_required=True
        ),
        OnboardingStep(
            step_id="first_project",
            name="Create Your First Project",
            description="Initialize a new BB5 project",
            optional=False,
            dependencies=["config_setup"],
            agent_required=True
        ),
        OnboardingStep(
            step_id="agent_intro",
            name="Meet Your Agents",
            description="Introduction to BB5 agent system",
            optional=True,
            agent_required=False
        ),
        OnboardingStep(
            step_id="completion",
            name="Onboarding Complete",
            description="Review your setup and get started",
            optional=False,
            dependencies=["first_project"],
            agent_required=False
        )
    ]
)
```

### B. Event Schema

```python
# Events published during onboarding
ONBOARDING_EVENTS = {
    "onboarding.started": {
        "user_id": "str",
        "flow_id": "str",
        "timestamp": "datetime"
    },
    "onboarding.step_started": {
        "user_id": "str",
        "step_id": "str",
        "timestamp": "datetime"
    },
    "onboarding.step_completed": {
        "user_id": "str",
        "step_id": "str",
        "duration_ms": "int",
        "timestamp": "datetime"
    },
    "onboarding.step_skipped": {
        "user_id": "str",
        "step_id": "str",
        "reason": "str",
        "timestamp": "datetime"
    },
    "onboarding.paused": {
        "user_id": "str",
        "current_step": "str",
        "timestamp": "datetime"
    },
    "onboarding.resumed": {
        "user_id": "str",
        "timestamp": "datetime"
    },
    "onboarding.completed": {
        "user_id": "str",
        "flow_id": "str",
        "duration_seconds": "int",
        "steps_completed": "int",
        "steps_skipped": "int",
        "timestamp": "datetime"
    },
    "onboarding.failed": {
        "user_id": "str",
        "error": "str",
        "step_id": "str",
        "timestamp": "datetime"
    }
}
```

---

**Document Status:** Complete  
**Next Review:** After Phase 1 implementation  
**Approvals:** Pending technical review
