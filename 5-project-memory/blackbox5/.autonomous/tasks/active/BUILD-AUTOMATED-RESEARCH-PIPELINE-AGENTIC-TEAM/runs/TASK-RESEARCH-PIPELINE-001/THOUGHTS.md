# THOUGHTS: Research Pipeline System (RAPS)

## Initial Thinking

The goal is to build a multi-agent research pipeline that:
1. Discovers patterns from external sources (GitHub, YouTube, docs)
2. Ranks them by value/cost ratio
3. Plans implementation tasks
4. Executes selectively

## Key Insight: Best of Both Worlds

BB5 already has TWO proven architectures:
1. **Dual-RALF** - File-based coordination, human-readable, audit trail
2. **BB5 Autonomous** - Redis coordination, 1ms latency, production-ready

Instead of choosing, we combine:
- **Redis** for fast agent coordination (events, status, claiming)
- **Files** for audit trail and human readability
- **Neo4j** for concept relationships (graph queries)

## Agent Design Philosophy

Specialized agents work better than generalists in pipelines:
- Scout: Only scans, doesn't analyze
- Analyst: Only ranks, doesn't execute
- Planner: Only plans, doesn't implement
- Executor: Only executes, one at a time

This mirrors Unix philosophy: do one thing well, compose via pipes.

## Compute Efficiency

Not all agents need to run continuously:
- Scout/Analyst: Continuous (low cost, high value)
- Planner: Triggered (medium cost, on approval)
- Executor: Selective (controlled cost, one task)

This balances responsiveness with cost.

## Human-in-the-Loop

Full automation is risky. Full manual is slow.

4 gates provide oversight without bottleneck:
1. Research validation (concepts make sense)
2. Integration approval (worth the effort)
3. Task plan review (correct breakdown)
4. Implementation review (quality check)

Auto-approval thresholds prevent stalling.

## BB5 Integration Strategy

Reuse, don't reinvent:
- TaskRegistry → Store research tasks
- RedisCoordinator → Agent communication
- AgentOrchestrator → Workflow management
- AutonomousAgent → Execution loop
- BMAD skills → Intelligence (analyst, architect)

Only build what's unique:
- Scout agent (source scanning)
- Analyst agent (ranking algorithm)
- Neo4j schema (concept graph)

## Open Questions

1. How to handle GitHub API rate limits?
2. What's the scoring threshold for auto-approval?
3. How to deduplicate similar patterns?
4. Should we incorporate execution feedback into rankings?
5. How to scale Scout to 100+ sources?

## Next Steps

1. Research BB5 infrastructure in detail
2. Design agent interfaces
3. Set up Neo4j
4. Build Scout MVP
5. Iterate based on usage

---

*Thinking evolves as we build. Document assumptions and validate.*
