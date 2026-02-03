# Research Pipeline Cross-References

**Tracking relationships between patterns, tasks, and runs**

---

## Pattern to Source Mapping

| Pattern ID | Source | Extracted By | Date |
|------------|--------|--------------|------|
| P-001 | {source_url} | scout-worker-run-001 | {date} |

## Pattern to Analysis Mapping

| Pattern ID | Analysis ID | Analyst Run | Decision | Score |
|------------|-------------|-------------|----------|-------|
| P-001 | A-001 | analyst-worker-run-001 | recommend | 8.5 |

## Analysis to Task Mapping

| Analysis ID | Task ID | Planner Run | Status |
|-------------|---------|-------------|--------|
| A-001 | TASK-RAPS-001 | planner-worker-run-001 | pending |

## Task to BB5 Task Mapping

| RAPS Task ID | BB5 Task ID | Executor | Status |
|--------------|-------------|----------|--------|
| TASK-RAPS-001 | TASK-XXXXX | {executor} | pending |

---

## Run Relationships

### Scout Runs
| Run ID | Source | Patterns Found | Validator Feedback |
|--------|--------|----------------|-------------------|
| scout-001 | {url} | 3 | {feedback} |

### Analyst Runs
| Run ID | Patterns Analyzed | Recommendations | Validator Feedback |
|--------|-------------------|-----------------|-------------------|
| analyst-001 | 5 | 3 | {feedback} |

### Planner Runs
| Run ID | Recommendations | Tasks Created | Validator Feedback |
|--------|-----------------|---------------|-------------------|
| planner-001 | 2 | 2 | {feedback} |

---

## Concept Relationships

### Concept Graph
```
{Concept A} --implements--> {Pattern X}
{Concept B} --uses--> {Pattern X}
{Pattern X} --extracted_from--> {Source Y}
```

### Pattern Similarities
| Pattern 1 | Pattern 2 | Similarity Score | Notes |
|-----------|-----------|------------------|-------|
| P-001 | P-002 | 0.85 | Both auth-related |

---

## Learning References

| Learning ID | From Run | Category | Related To |
|-------------|----------|----------|------------|
| L-001 | scout-001 | extraction | JWT patterns |

---

## Decision Dependencies

| Decision ID | Depends On | Run ID |
|-------------|------------|--------|
| DEC-001 | DEC-000 | scout-001 |

---

*Auto-generated and maintained by validator agents*
*Last updated: 2026-02-04*
