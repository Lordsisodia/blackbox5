# PLAN.md: Add Caching Layer to StorageBackend

**Task:** TASK-SSOT-028 - No caching layer for frequently accessed data
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 3-4 hours
**Importance:** 65 (Medium-High)

---

## 1. First Principles Analysis

### The Core Problem
Frequently accessed data is read from disk every time:
- Task lists read repeatedly
- Configuration files parsed multiple times
- State files loaded on every check
- No in-memory caching

This creates:
1. **Performance Issues**: Unnecessary disk I/O
2. **Latency**: Slow response times
3. **Resource Waste**: CPU spent on repeated parsing
4. **Battery Drain**: Unnecessary disk access
5. **Scalability Issues**: Doesn't scale with data size

### First Principles Solution
- **In-Memory Cache**: LRU cache for hot data
- **Cache Invalidation**: Time-based and event-based
- **Cache Consistency**: Ensure cache matches disk
- **Configurable**: Cache size and TTL settings
- **Transparent**: No code changes needed

---

## 2. Current State Analysis

### Current Access Patterns

```python
# Pattern 1: Repeated reads
def get_task(task_id):
    with open(f"tasks/{task_id}.yaml") as f:  # Disk read every time
        return yaml.safe_load(f)

# Called multiple times in same session
task = get_task("TASK-001")
# ... some code ...
task = get_task("TASK-001")  # Reads from disk again!
```

### Hot Data

| Data | Access Frequency | Cache Benefit |
|------|-----------------|---------------|
| Task lists | Very High | High |
| Configuration | High | High |
| State files | High | Medium |
| Run data | Medium | Low |
| Historical data | Low | None |

---

## 3. Proposed Solution

### Caching Layer

**File:** `2-engine/.autonomous/lib/caching_backend.py`

```python
import time
import hashlib
from typing import Any, Optional, Dict, Callable
from functools import lru_cache
from .storage_backend import StorageBackend

class CacheEntry:
    """Cache entry with metadata."""

    def __init__(self, data: Any, ttl: float):
        self.data = data
        self.created_at = time.time()
        self.ttl = ttl
        self.access_count = 1
        self.last_accessed = time.time()

    def is_expired(self) -> bool:
        """Check if entry has expired."""
        return time.time() - self.created_at > self.ttl

    def touch(self):
        """Update access metadata."""
        self.access_count += 1
        self.last_accessed = time.time()

class CachingBackend(StorageBackend):
    """Caching wrapper for StorageBackend."""

    def __init__(
        self,
        backend: StorageBackend,
        max_size: int = 1000,
        default_ttl: float = 300.0,  # 5 minutes
        cache_patterns: Optional[Dict[str, float]] = None
    ):
        self.backend = backend
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache_patterns = cache_patterns or {}
        self._cache: Dict[str, CacheEntry] = {}
        self._access_order: list = []  # LRU tracking

    def _get_cache_key(self, path: str) -> str:
        """Generate cache key for path."""
        return hashlib.md5(path.encode()).hexdigest()

    def _get_ttl(self, path: str) -> float:
        """Get TTL for path based on patterns."""
        for pattern, ttl in self.cache_patterns.items():
            if pattern in path:
                return ttl
        return self.default_ttl

    def _get_from_cache(self, path: str) -> Optional[Any]:
        """Get data from cache if available and not expired."""
        key = self._get_cache_key(path)
        entry = self._cache.get(key)

        if entry is None:
            return None

        if entry.is_expired():
            self._evict(key)
            return None

        entry.touch()
        self._update_lru(key)
        return entry.data

    def _put_in_cache(self, path: str, data: Any):
        """Store data in cache."""
        key = self._get_cache_key(path)
        ttl = self._get_ttl(path)

        # Evict if at capacity
        if len(self._cache) >= self.max_size:
            self._evict_lru()

        self._cache[key] = CacheEntry(data, ttl)
        self._access_order.append(key)

    def _evict(self, key: str):
        """Evict specific entry."""
        if key in self._cache:
            del self._cache[key]
        if key in self._access_order:
            self._access_order.remove(key)

    def _evict_lru(self):
        """Evict least recently used entry."""
        if self._access_order:
            lru_key = self._access_order.pop(0)
            self._evict(lru_key)

    def _update_lru(self, key: str):
        """Update LRU order."""
        if key in self._access_order:
            self._access_order.remove(key)
        self._access_order.append(key)

    def _invalidate(self, path: str):
        """Invalidate cache entry for path."""
        key = self._get_cache_key(path)
        self._evict(key)

    def read(self, path: str) -> Any:
        """Read with caching."""
        # Try cache first
        cached = self._get_from_cache(path)
        if cached is not None:
            return cached

        # Read from backend
        data = self.backend.read(path)

        # Cache the result
        self._put_in_cache(path, data)

        return data

    def write(self, path: str, data: Any) -> None:
        """Write with cache invalidation."""
        # Write to backend
        self.backend.write(path, data)

        # Invalidate cache
        self._invalidate(path)

        # Optionally cache the new value
        self._put_in_cache(path, data)

    def exists(self, path: str) -> bool:
        """Check existence (cached)."""
        # Check cache first
        key = self._get_cache_key(path)
        if key in self._cache:
            return True

        return self.backend.exists(path)

    def delete(self, path: str) -> None:
        """Delete with cache invalidation."""
        self.backend.delete(path)
        self._invalidate(path)

    def list(self, path: str) -> list:
        """List with caching."""
        # Use shorter TTL for listings
        cached = self._get_from_cache(f"_list_{path}")
        if cached is not None:
            return cached

        data = self.backend.list(path)
        self._put_in_cache(f"_list_{path}", data)

        return data

    def get_stats(self) -> Dict:
        """Get cache statistics."""
        total_entries = len(self._cache)
        total_accesses = sum(e.access_count for e in self._cache.values())
        expired_entries = sum(1 for e in self._cache.values() if e.is_expired())

        return {
            'total_entries': total_entries,
            'total_accesses': total_accesses,
            'expired_entries': expired_entries,
            'hit_rate': self._calculate_hit_rate()
        }

    def _calculate_hit_rate(self) -> float:
        """Calculate cache hit rate."""
        # Simplified - would need actual tracking
        return 0.0

    def clear(self):
        """Clear all cached data."""
        self._cache.clear()
        self._access_order.clear()

    def invalidate_pattern(self, pattern: str):
        """Invalidate all entries matching pattern."""
        keys_to_evict = [
            key for key in self._cache.keys()
            if pattern in key
        ]
        for key in keys_to_evict:
            self._evict(key)
```

### Configuration

**File:** `5-project-memory/blackbox5/.autonomous/cache-config.yaml`

```yaml
cache:
  enabled: true
  max_size: 1000
  default_ttl: 300  # 5 minutes

  # Pattern-specific TTLs
  patterns:
    "tasks/": 60      # 1 minute for tasks (frequently changing)
    "config/": 600    # 10 minutes for config (rarely changing)
    "state/": 30      # 30 seconds for state (very frequently changing)
    ".yaml": 300        # Default for YAML files
```

### Implementation Plan

#### Phase 1: Create Caching Backend (2 hours)

1. Implement CachingBackend class
2. Implement LRU eviction
3. Implement TTL expiration
4. Add cache statistics

#### Phase 2: Add Cache Configuration (30 min)

1. Create cache-config.yaml
2. Add pattern-based TTLs
3. Add cache settings

#### Phase 3: Integrate with Storage (1 hour)

```python
# Create caching storage
base_backend = FileSystemBackend(project_path)
storage = CachingBackend(
    backend=base_backend,
    max_size=1000,
    default_ttl=300,
    cache_patterns={
        "tasks/": 60,
        "config/": 600
    }
)
```

#### Phase 4: Add Monitoring (30 min)

Add cache statistics to health dashboard:
- Hit rate
- Cache size
- Eviction count
- Average TTL

---

## 4. Files to Modify

### New Files
1. `2-engine/.autonomous/lib/caching_backend.py` - Caching layer
2. `5-project-memory/blackbox5/.autonomous/cache-config.yaml` - Cache config

### Modified Files
1. Storage initialization code
2. Health dashboard to show cache stats

---

## 5. Success Criteria

- [ ] CachingBackend implemented
- [ ] LRU eviction working
- [ ] TTL expiration working
- [ ] Cache statistics available
- [ ] Performance improved (measure before/after)
- [ ] Memory usage acceptable

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Disable caching (set enabled: false)
2. **Fix**: Debug caching backend
3. **Re-enable**: Once fixed

---

## 7. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Caching Backend | 2 hours | 2 hours |
| Phase 2: Configuration | 30 min | 2.5 hours |
| Phase 3: Integration | 1 hour | 3.5 hours |
| Phase 4: Monitoring | 30 min | 4 hours |
| **Total** | | **3-4 hours** |

---

*Plan created based on SSOT violation analysis - No caching layer*
