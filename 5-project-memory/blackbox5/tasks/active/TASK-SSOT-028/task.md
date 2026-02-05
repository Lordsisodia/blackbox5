# TASK-SSOT-028: Implement Caching Layer for High-Volume Data

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-06
**Parent:** Issue #3 - Missing Storage Abstraction Layer

## Objective
Implement caching layer to reduce I/O operations and API costs.

## Success Criteria
- [ ] Create storage/cache/ module with CacheManager
- [ ] Implement file-based cache with mtime invalidation
- [ ] Implement in-memory LRU cache for hot data
- [ ] Add embedding query cache (vector_store.py)
- [ ] Add skill YAML file caching
- [ ] Add queue.yaml caching
- [ ] Add task directory scan caching
- [ ] Add metrics calculation caching
- [ ] Measure performance improvements

## Context
Major caching opportunities found:
- **Vector embeddings**: 80-95% API cost reduction
- **Skill YAML files**: 40-60% I/O reduction
- **Queue operations**: 30-50% load time reduction
- **Task directory scans**: 25-40% latency reduction

## Cache Strategies
```python
# File-based with mtime check
Key: "skill_usage:{file_path}:{mtime}:{size}"
TTL: 5 minutes

# In-memory LRU
Key: "embedding:{text_hash}:{model_version}"
Max entries: 1000
TTL: 24 hours

# Time-bucketed
Key: "health_data:{timestamp_bucket}"
TTL: 5 seconds
```

## Related Files
- caching-opportunities.md
- vector_store.py
- bb5-queue-manager.py
- bb5-health-dashboard.py

## Rollback Strategy
Can disable caching if consistency issues arise.
