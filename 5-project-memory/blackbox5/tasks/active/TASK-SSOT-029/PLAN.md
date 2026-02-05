# PLAN.md: Optimize YAML Serialization/Deserialization

**Task:** TASK-SSOT-029 - YAML parsing is slow for large files
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 3-4 hours
**Importance:** 60 (Medium)

---

## 1. First Principles Analysis

### The Core Problem
YAML parsing is a bottleneck:
- Large YAML files take significant time to parse
- PyYAML is pure Python and slow
- Same files parsed multiple times
- No streaming for large files
- No binary cache of parsed data

This creates:
1. **Performance Issues**: Slow startup and operations
2. **CPU Usage**: High CPU for parsing
3. **Latency**: Slow response times
4. **Battery Drain**: Unnecessary processing
5. **Scalability Issues**: Doesn't scale with file size

### First Principles Solution
- **Fast YAML Library**: Use libyaml-based parser
- **Streaming**: Parse large files incrementally
- **Binary Cache**: Cache parsed data in binary format
- **Lazy Loading**: Only parse what's needed
- **Optimization**: Profile and optimize hot paths

---

## 2. Current State Analysis

### Current YAML Usage

```python
import yaml

# Pattern 1: Standard parsing (slow)
with open('large-file.yaml') as f:
    data = yaml.safe_load(f)  # Can take seconds for large files

# Pattern 2: Repeated parsing
for i in range(100):
    with open('config.yaml') as f:
        config = yaml.safe_load(f)  # Parsed 100 times!
```

### Performance Characteristics

| File Size | Parse Time | Issue |
|-----------|-----------|-------|
| 10 KB | 10 ms | OK |
| 100 KB | 100 ms | Noticeable |
| 1 MB | 1 second | Problematic |
| 10 MB | 10 seconds | Unacceptable |

---

## 3. Proposed Solution

### Fast YAML Parser

**Option 1: Use libyaml (CSafeLoader)**

```python
from yaml import CSafeLoader, CDumper

# Use C-based parser (much faster)
def fast_load(path):
    with open(path) as f:
        return yaml.load(f, Loader=CSafeLoader)

def fast_dump(data, path):
    with open(path, 'w') as f:
        yaml.dump(data, f, Dumper=CDumper)
```

**Option 2: Use ruamel.yaml**

```python
from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True

# Faster and preserves formatting
def load_with_ruamel(path):
    with open(path) as f:
        return yaml.load(f)
```

### Binary Cache

**File:** `2-engine/.autonomous/lib/yaml_cache.py`

```python
import pickle
import hashlib
from pathlib import Path
from typing import Any

class YAMLCache:
    """Cache for parsed YAML files."""

    def __init__(self, cache_dir: str = ".yaml_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _get_cache_key(self, path: str, mtime: float) -> str:
        """Generate cache key from path and modification time."""
        content = f"{path}:{mtime}"
        return hashlib.md5(content.encode()).hexdigest()

    def _get_cache_path(self, cache_key: str) -> Path:
        """Get cache file path."""
        return self.cache_dir / f"{cache_key}.pkl"

    def load(self, path: str) -> Any:
        """Load YAML with caching."""
        path_obj = Path(path)
        mtime = path_obj.stat().st_mtime
        cache_key = self._get_cache_key(path, mtime)
        cache_path = self._get_cache_path(cache_key)

        # Try cache first
        if cache_path.exists():
            with open(cache_path, 'rb') as f:
                return pickle.load(f)

        # Parse YAML
        import yaml
        with open(path) as f:
            data = yaml.safe_load(f)

        # Save to cache
        with open(cache_path, 'wb') as f:
            pickle.dump(data, f)

        return data

    def clear(self):
        """Clear all cached data."""
        for cache_file in self.cache_dir.glob("*.pkl"):
            cache_file.unlink()

    def cleanup(self, max_age_days: int = 7):
        """Remove old cache entries."""
        import time
        cutoff = time.time() - (max_age_days * 24 * 60 * 60)

        for cache_file in self.cache_dir.glob("*.pkl"):
            if cache_file.stat().st_mtime < cutoff:
                cache_file.unlink()
```

### Streaming for Large Files

```python
import yaml

def stream_yaml_documents(path: str):
    """Stream YAML documents one at a time."""
    with open(path) as f:
        for document in yaml.safe_load_all(f):
            yield document

# Usage - process without loading entire file
for doc in stream_yaml_documents('large-file.yaml'):
    process_document(doc)
```

### Optimized YAML Utilities

**File:** `2-engine/.autonomous/lib/fast_yaml.py`

```python
"""Fast YAML utilities with caching and optimization."""

import yaml
from pathlib import Path
from typing import Any, Optional

# Try to use C-based parser
try:
    from yaml import CSafeLoader as Loader
    from yaml import CDumper as Dumper
    HAS_CYAML = True
except ImportError:
    from yaml import SafeLoader as Loader
    from yaml import SafeDumper as Dumper
    HAS_CYAML = False

# Global cache instance
_yaml_cache: Optional['YAMLCache'] = None

def get_yaml_cache() -> 'YAMLCache':
    """Get or create YAML cache."""
    global _yaml_cache
    if _yaml_cache is None:
        from .yaml_cache import YAMLCache
        _yaml_cache = YAMLCache()
    return _yaml_cache

def fast_load(path: str, use_cache: bool = True) -> Any:
    """Fast YAML load with optional caching."""
    if use_cache:
        return get_yaml_cache().load(path)

    with open(path) as f:
        return yaml.load(f, Loader=Loader)

def fast_dump(data: Any, path: str) -> None:
    """Fast YAML dump."""
    with open(path, 'w') as f:
        yaml.dump(data, f, Dumper=Dumper)

def load_stream(path: str):
    """Stream YAML documents."""
    with open(path) as f:
        for doc in yaml.load_all(f, Loader=Loader):
            yield doc

def get_loader_info() -> dict:
    """Get information about YAML loader."""
    return {
        'has_cyaml': HAS_CYAML,
        'loader': Loader.__name__,
        'dumper': Dumper.__name__
    }
```

### Implementation Plan

#### Phase 1: Benchmark Current Performance (30 min)

```python
import time
import yaml

# Benchmark current parsing
def benchmark_yaml_parsing():
    files = [
        'timeline.yaml',
        'STATE.yaml',
        '.autonomous/agents/communications/queue.yaml'
    ]

    for file in files:
        start = time.time()
        with open(file) as f:
            data = yaml.safe_load(f)
        elapsed = time.time() - start
        print(f"{file}: {elapsed:.3f}s")
```

#### Phase 2: Implement Fast YAML (1 hour)

1. Create fast_yaml.py with optimized loader
2. Implement YAMLCache
3. Add streaming support

#### Phase 3: Update Storage Backend (1 hour)

Update StorageBackend to use fast_yaml:

```python
from .fast_yaml import fast_load, fast_dump

class FileSystemBackend(StorageBackend):
    def read(self, path: str) -> Any:
        return fast_load(path, use_cache=True)

    def write(self, path: str, data: Any) -> None:
        fast_dump(data, path)
```

#### Phase 4: Add Cache Management (1 hour)

1. Add cache cleanup command
2. Add cache statistics
3. Add cache invalidation hooks

---

## 4. Files to Modify

### New Files
1. `2-engine/.autonomous/lib/fast_yaml.py` - Fast YAML utilities
2. `2-engine/.autonomous/lib/yaml_cache.py` - YAML cache

### Modified Files
1. `2-engine/.autonomous/lib/storage_backend.py` - Use fast YAML
2. Add cache management commands

---

## 5. Success Criteria

- [ ] Fast YAML parser implemented
- [ ] YAML cache working
- [ ] Performance improved (measure before/after)
- [ ] Streaming for large files working
- [ ] Cache management tools available

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Use standard yaml.safe_load
2. **Fix**: Debug fast YAML implementation
3. **Re-enable**: Once fixed

---

## 7. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Benchmark | 30 min | 30 min |
| Phase 2: Fast YAML | 1 hour | 1.5 hours |
| Phase 3: Storage Backend | 1 hour | 2.5 hours |
| Phase 4: Cache Management | 1 hour | 3.5 hours |
| **Total** | | **3-4 hours** |

---

*Plan created based on SSOT violation analysis - YAML parsing is slow*
