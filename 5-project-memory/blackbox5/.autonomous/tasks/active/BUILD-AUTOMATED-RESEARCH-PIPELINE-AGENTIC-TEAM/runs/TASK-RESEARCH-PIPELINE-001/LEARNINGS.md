# LEARNINGS: Research Pipeline System (RAPS)

## What Worked Well

### 1. Leveraging Existing Infrastructure
- BB5 already has robust agent framework
- Redis coordination is production-ready
- TaskRegistry with SQLite is solid
- Don't reinvent what exists

### 2. Hybrid Communication Approach
- Dual-RALF's file-based approach is great for auditability
- BB5's Redis approach is great for speed
- Combining both gives best of both worlds

### 3. Specialized Agents
- Clear separation of concerns makes design easier
- Each agent has single responsibility
- Can optimize each independently

## What Was Harder Than Expected

### 1. Agent Granularity
- Initially unclear how many agents to have
- 2 felt too coarse, 6+ felt complex
- Settled on 4 after analyzing data flow

### 2. Human Gate Placement
- Unclear where humans should intervene
- Too many gates = bottleneck
- Too few gates = risk
- Settled on 4 based on decision points

### 3. Scoring Algorithm
- Value/cost ratio seems simple
- But defining "value" and "cost" is complex
- Needs iteration based on real data

## What Would Do Differently

### 1. Start With Scout Only
- Build Scout first, validate concept extraction
- Then add Analyst, then Planner, then Executor
- Incremental validation beats big bang

### 2. Mock Human Gates Initially
- Build auto-approval from day one
- Add human review as enhancement
- Prevents blocking during development

### 3. Define Metrics First
- What does "success" mean?
- How many patterns/day?
- What's a "good" ranking?
- Need concrete targets

## Patterns Detected

### 1. Pipeline Pattern
- Data flows in one direction
- Each stage transforms data
- Easy to parallelize stages

### 2. Event-Driven Coordination
- Agents react to events
- Loose coupling
- Easy to add new agents

### 3. Human-in-the-Loop
- Automation with oversight
- Gates at decision points
- Auto-approval for efficiency

## Open Questions

1. Will Neo4j scale to 100K+ relationships?
2. Will humans actually review the gates?
3. Will rankings correlate with integration success?
4. What's the right threshold for auto-approval?

## Recommendations for Future

1. **Build incrementally** - One agent at a time
2. **Measure everything** - Track all metrics from day one
3. **Validate assumptions** - Test assumptions in Phase 1
4. **Document learnings** - Update this file after each phase

---

*Learning is continuous. Update this file as we build.*
