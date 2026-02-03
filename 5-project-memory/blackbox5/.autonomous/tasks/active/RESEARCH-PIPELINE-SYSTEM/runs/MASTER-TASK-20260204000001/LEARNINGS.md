# LEARNINGS: MASTER-TASK - Multi-Agent Research Pipeline

## What We Learned from BB5 Infrastructure

### Existing Systems
BB5 already has sophisticated autonomous infrastructure:
- Redis-based coordination (1ms latency)
- Orchestrator with wave-based parallelization
- 22+ BMAD skills with usage tracking
- Task registry with dependency management
- Multi-tier memory system (working, episodic, knowledge graph)

### Don't Reinvent
The temptation is to build custom pipeline infrastructure. But BB5 has:
- Communication protocols (file-based and pub/sub)
- Agent definitions and personas
- Task lifecycle management
- Storage backends (JSON, SQLite, Redis, Neo4j)

### Integration Points
Key integration points for our pipeline:
1. **Task Registry** - Create tasks programmatically
2. **Redis Coordinator** - Agent status and messaging
3. **Orchestrator** - Workflow execution
4. **BMAD Skills** - Invoke specialized agents
5. **Queue System** - Task assignment and tracking

## Design Insights

### Pipeline vs Multi-Agent
Pipeline (linear flow) is simpler but multi-agent (mesh) is more flexible.
We're choosing pipeline for v1 because:
- Clearer data flow
- Easier debugging
- Predictable resource usage

### Continuous vs Triggered
Not everything needs to run continuously:
- Scout: Continuous (always discovering)
- Analyst: Continuous (always evaluating)
- Planner: Triggered (when threshold met)
- Executor: Triggered (when task ready)

This optimizes compute costs.

### Human Gates
Full autonomy is risky. Human gates at key decision points:
- Prevents low-quality implementations
- Maintains human oversight
- Allows course correction

## Open Questions to Resolve

1. How does Scout prioritize which sources to scan?
2. What threshold triggers the Planner?
3. How does Executor select which task to work on?
4. What's the feedback mechanism from execution to research?

## Patterns to Apply

### From BMAD
- Persona-driven agent design
- Skill-based task execution
- Command trigger system (2-letter codes)

### From RALF
- ONE task at a time philosophy
- Run-based documentation
- Continuous self-improvement

### From Dual-RALF
- File-based communication protocol
- Queue-based task assignment
- Event-driven status updates
