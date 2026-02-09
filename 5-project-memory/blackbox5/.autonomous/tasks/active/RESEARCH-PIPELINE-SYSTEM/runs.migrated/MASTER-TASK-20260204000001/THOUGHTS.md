# THOUGHTS: MASTER-TASK - Multi-Agent Research Pipeline

## Vision

Transform BB5 from manual repo-by-repo analysis to a continuous autonomous research pipeline. Instead of one agent analyzing one source at a time, have specialized agents working in parallel:

1. Scout constantly discovers patterns
2. Analyst ranks by complexity/value
3. Planner breaks into executable tasks
4. Executor implements selectively

## Why This Matters

Current state:
- Sequential analysis is slow
- Manual task creation is error-prone
- No comparison between sources
- Context gets lost between sessions

Future state:
- Parallel discovery from unlimited sources
- Automatic ranking and prioritization
- Consistent task structure
- Persistent knowledge graph

## BB5 Infrastructure Advantage

We don't need to build from scratch:
- Redis coordination (1ms latency)
- Task registry with dependencies
- Orchestrator with parallelization
- 22+ BMAD skills
- File-based + pub/sub protocols

The infrastructure exists. We just need to wire it together for this specific pipeline.

## Key Design Decisions

### Agent Specialization vs Generalization
More agents = better specialization = faster processing
But we need to balance against compute cost and coordination overhead

4 agents feels right:
- Scout: Pure research, no decisions
- Analyst: Pure evaluation, no implementation
- Planner: Pure organization, no execution
- Executor: Pure implementation, no research

### Communication Pattern
Agent 1 → Agent 2 → Agent 3 → Agent 4 is a pipeline
But we also need feedback loops:
- Executor reports back to Scout (what worked/didn't)
- Analyst adjusts rankings based on execution results

### Storage Strategy
Concept map needs to be queryable:
- Neo4j for concept relationships
- Redis for real-time coordination
- Files for persistent task storage

### Human Gates
Full autonomy is risky. Human approval at:
1. Concept overlaps identified
2. Recommendations ranked
3. Tasks planned
4. Implementation complete

## Open Questions

1. How does Scout know which sources to scan?
2. What triggers Agent 3 to plan tasks?
3. How does Executor pick which task to work on?
4. What's the feedback loop from execution to research?

## Next Steps

1. Design detailed architecture
2. Map BB5 infrastructure components
3. Build Scout agent first (foundation)
4. Add Analyst, Planner, Executor sequentially
5. Test end-to-end
