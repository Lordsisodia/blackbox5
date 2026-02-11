# TASK-INT-002: Fix Redis Connection Pool API Usage

**Status:** in_progress
**Priority:** CRITICAL
**Type:** infrastructure
**Category:** redis_api
**Created:** 2026-02-11T16:58:00Z
**Agent:** main
**Parent Task:** TASK-INT-001
**Estimated Effort:** 30 minutes

## Problem Statement

Shared Memory Service failing with Redis connection pool API errors:
```
AttributeError: 'ConnectionPool' object has no attribute 'get_connection'
AttributeError: 'ConnectionPool' object has no attribute 'release_connection'
```

The API method names are incorrect for the version of redis-py being used.

## Current State

**File:** `/opt/blackbox5/services/shared_memory_service.py`
**Error:** Using `redis.ConnectionPool` with methods `get_connection()` and `release_connection()`
**Issue:** These methods may not exist or have different names in current redis-py version

## Investigation Needed

Check redis-py documentation for correct ConnectionPool API:
- Correct method to get connection from pool
- Correct method to return connection to pool
- Alternative: Use connection directly without pool

## Proposed Solutions

### Option A: Use Simple Redis Client
Change from `ConnectionPool` to `redis.Redis()`:
```python
import redis

class SharedMemoryService:
    def __init__(self):
        self.redis = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            db=int(os.getenv("REDIS_DB", "0")),
            decode_responses=True
        )
    
    def _get_redis(self):
        return self.redis  # No pooling needed for low-traffic service
    
    def _return_redis(self, conn):
        # No return needed - connection is not borrowed
        pass
    
    def add_insight(self, ...):
        insight = Insight(...)
        
        # Store in Redis
        insight_key = f"shared_memory:insight:{insight['id']}"
        self.redis.hset(insight_key, "data", json.dumps(insight))
        
        # Add to category index
        category_key = f"shared_memory:category:{insight['namespace']}:{insight['category']}"
        self.redis.sadd(category_key, insight['id'])
        
        return insight['id']
```

### Option B: Fix ConnectionPool Method Names
Check actual API and update method names:
```python
# Get connection (not 'get_connection')
conn = self.redis_pool.get_connection()

# Return connection (not 'release_connection')
self.redis_pool.release(conn)

# Or using context manager
with self.redis_pool.get_connection() as conn:
    # Use connection
    pass  # Auto-released
```

### Option C: Check redis-py Version
```bash
python3 -c "import redis; print(redis.__version__)"
```

Use correct API based on version.

## Implementation Plan

1. Check redis-py version
2. Choose appropriate solution (A or B)
3. Update `/opt/blackbox5/services/shared_memory_service.py`
4. Update `/opt/blackbox5/services/test_shared_memory.py`
5. Re-test all tests
6. Verify tests pass
7. Commit to git
8. Update Task-INT-001 with solution details

## Success Criteria

- [ ] Correct redis-py API usage
- [ ] All tests in test_shared_memory.py pass
- [ ] Shared Memory Service runs successfully
- [ ] Documentation updated
- [ ] Solution committed to git
