# ASSUMPTIONS: MASTER-TASK - Multi-Agent Research Pipeline

## Technical Assumptions

1. **Redis Available:** Redis server running for pub/sub coordination
2. **Neo4j Available:** Neo4j instance for concept graph storage
3. **Python 3.11+:** All agents use Python 3.11 or higher
4. **BMAD Skills:** Existing skills can be invoked by pipeline agents
5. **GitHub API:** Rate limits sufficient for continuous scanning

## Resource Assumptions

1. **Compute Budget:** Continuous agents (Scout, Analyst) run on low-cost compute
2. **Storage:** Concept graph grows linearly with sources scanned
3. **API Limits:** YouTube/GitHub APIs sufficient for research volume
4. **Network:** Reliable connectivity for continuous scanning

## Functional Assumptions

1. **Pattern Extractable:** Code patterns can be automatically extracted from repos
2. **Complexity Measurable:** Integration/maintenance complexity can be estimated
3. **Value Comparable:** Pattern value can be ranked across sources
4. **Tasks Auto-Generatable:** Proper BB5 tasks can be created from recommendations

## Human Assumptions

1. **Approval Availability:** Humans available to review at 4 gates
2. **Domain Knowledge:** Humans can evaluate pattern recommendations
3. **Feedback Loop:** Humans provide feedback on implementation quality

## BB5 Integration Assumptions

1. **Task Format:** Existing task format sufficient for auto-generated tasks
2. **Queue System:** queue.yaml can handle auto-generated tasks
3. **Skill Invocation:** BMAD skills can be invoked programmatically
4. **Run Folders:** Auto-created run folders follow BB5 conventions
