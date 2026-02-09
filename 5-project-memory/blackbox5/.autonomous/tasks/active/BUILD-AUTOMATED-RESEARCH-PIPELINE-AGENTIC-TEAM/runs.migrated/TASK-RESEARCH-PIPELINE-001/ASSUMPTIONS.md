# ASSUMPTIONS: Research Pipeline System (RAPS)

## Technical Assumptions

1. **Redis Available**
   - Assumption: Redis is running and accessible
   - Risk: If Redis down, coordination fails
   - Mitigation: Fallback to file-based coordination

2. **Neo4j Can Handle Load**
   - Assumption: Neo4j can store 10K+ concepts, 100K+ relationships
   - Risk: Performance degradation at scale
   - Mitigation: Partitioning, indexing, query optimization

3. **GitHub API Rate Limits**
   - Assumption: We can stay within GitHub API limits
   - Risk: Rate limiting blocks Scout
   - Mitigation: Exponential backoff, caching, multiple tokens

4. **BB5 Infrastructure Stable**
   - Assumption: TaskRegistry, RedisCoordinator work as documented
   - Risk: Undocumented behavior or bugs
   - Mitigation: Thorough testing, fallback mechanisms

5. **Human Availability**
   - Assumption: Humans will review gates within timeout windows
   - Risk: Bottleneck if humans unavailable
   - Mitigation: Auto-approval thresholds, async notifications

## Business Assumptions

1. **Patterns Have Value**
   - Assumption: External patterns are worth integrating
   - Risk: Wasting effort on low-value patterns
   - Mitigation: Analyst ranking, human gate 2

2. **Compute Costs Acceptable**
   - Assumption: Continuous Scout/Analyst cost is acceptable
   - Risk: Unexpected cloud bills
   - Mitigation: Monitoring, auto-scaling limits

3. **One Task At A Time Sufficient**
   - Assumption: 3 tasks/day executor throughput is enough
   - Risk: Backlog grows faster than execution
   - Mitigation: Monitor queue depth, scale if needed

## User Assumptions

1. **Users Want Autonomy**
   - Assumption: Users want automated research with oversight
   - Risk: Users prefer full manual control
   - Mitigation: Configurable automation levels

2. **Users Trust Rankings**
   - Assumption: Users will trust Analyst rankings
   - Risk: Users override all recommendations
   - Mitigation: Transparent scoring, explainability

3. **Users Will Review**
   - Assumption: Users will engage with approval gates
   - Risk: Users ignore notifications
   - Mitigation: Email/Slack notifications, dashboards

## Validation Plan

| Assumption | How to Validate | When |
|------------|----------------|------|
| Redis available | Health checks | Phase 1 |
| Neo4j load | Load testing | Phase 5 |
| GitHub limits | Monitor rate limit headers | Phase 1 |
| BB5 stable | Integration tests | Phase 1 |
| Human availability | Track response times | Phase 2 |
| Pattern value | Measure integration success | Phase 4 |
| Compute costs | Cost tracking | All phases |
| Throughput sufficiency | Queue depth monitoring | Phase 4 |

---

*Assumptions are risks in disguise. Validate early and often.*
