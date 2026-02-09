# 02 - Implementation

This section contains implementation details, code architecture, and system design documentation for Blackbox5.

## Subsections

### 01-core/
Core system implementation, base classes, and fundamental infrastructure.
- [Communication](01-core/communication/) - Event bus and inter-agent communication
- [General](01-core/general/) - General implementation guidelines
- [Integration](01-core/integration/) - System integrations
- [Middleware](01-core/middleware/) - Middleware components
- [Orchestration](01-core/orchestration/) - Orchestrator implementation
- [Resilience](01-core/resilience/) - Fault tolerance and circuit breakers
- [State](01-core/state/) - State management

### 01-agents/
Agent implementations, agent types, and agent-specific code.
- [Epic Agents](01-agents/epic/) - Epic-level agent implementation
- [Parallel Agents](01-agents/parallel/) - Parallel agent execution
- [Task Agents](01-agents/task/) - Task-level agent implementation

### 02-core-systems/
Core system components and their implementations.
- [Atomic Commits](02-core-systems/atomic-commits/) - Atomic commit patterns
- [Checkpoint](02-core-systems/checkpoint/) - Checkpoint systems
- [Deviation Handling](02-core-systems/deviation/) - Deviation detection
- [State Management](02-core-systems/state-management/) - State management systems

### 03-pipeline/
Pipeline architecture, data flow, and processing stages.
- [Feature Pipeline](03-pipeline/feature/) - Feature development pipelines
- [GSD Pipeline](03-pipeline/gsd/) - Get Stuff Done pipelines
- [Spec-driven Pipeline](03-pipeline/spec-driven/) - Spec-driven pipelines

### 04-integrations/
Third-party integrations, APIs, and external service connections.
- [GitHub](04-integrations/github/) - GitHub integration
- [MCP](04-integrations/mcp/) - Model Context Protocol integration
- [Ralph](04-integrations/ralph/) - RALF autonomous daemon integration

### 05-memory-implementation/
Memory system implementation, storage backends, and retrieval mechanisms.
- [Context](05-memory-implementation/context/) - Context management
- [Project Memory](05-memory-implementation/project-memory/) - Project memory systems
- [Todo](05-memory-implementation/todo/) - Todo/task memory
- [Token Compression](05-memory-implementation/token-compression/) - Token compression

### 06-tools/
Tools, skills, and utilities available to agents.
- [Skills](06-tools/skills/) - Skills registry and documentation
- [Tools](06-tools/tools/) - Tool system implementation

### 07-task-management/
Task management implementation, scheduling, and execution.
- [Design](07-task-management/design/) - Task design patterns
- [Wave Execution](07-task-management/wave-execution/) - Wave-based execution

### Additional Implementation Docs
- [Agents](./02-agents/README.md) - Agent implementations
- [Modules](./03-modules/README.md) - Module implementations
- [Interfaces](./04-interfaces/README.md) - System interfaces

## Purpose

This section bridges theory and practice. It documents:
- How systems are built
- Code organization and patterns
- Integration points
- Configuration details

## Contributing

When documenting implementation:
1. Include code examples where helpful
2. Link to relevant theory in `01-theory/`
3. Reference related guides in `03-guides/`
4. Keep architecture diagrams up to date
