# PLAN-004: Fix Import Path Errors

**Priority:** 🔴 HIGH
**Status:** Planned
**Estimated Effort:** 1-2 days
**Dependencies:** None (can parallel with all)
**Validation Agent:** Agent 5 (Safety & Resilience)

---

## Problem Statement

Multiple modules have **broken import paths** causing tests to fail.

**Evidence:**
```python
# safety/circuit_breaker.py
from .kill_switch import KillSwitch  # Works
from ..utils.helpers import retry    # ERROR: utils doesn't exist

# agents/ArchitectAgent.py
from ..base_agent import BaseAgent   # Works
from ..skill_manager import SkillManager  # ERROR: wrong relative path
```

**Impact:**
- 5 safety module imports broken
- 3 agent imports broken
- Tests fail with ImportError
- Reduced code reliability

---

## Root Cause Analysis

### Issue 1: Missing `__init__.py` Files

```
blackbox5/2-engine/01-core/
├── agents/
│   ├── __init__.py  ✅
│   ├── core/
│   │   └── __init__.py  ✅
│   └── DeveloperAgent.py
└── safety/
    ├── __init__.py  ❌ MISSING
    ├── kill_switch.py
    └── circuit_breaker.py
```

### Issue 2: Wrong Relative Paths

```python
# agents/ArchitectAgent.py
# File location: blackbox5/2-engine/01-core/agents/ArchitectAgent.py
# Importing: from ..skill_manager import SkillManager
# Expected: from agents.core.skill_manager import SkillManager
```

### Issue 3: Module Structure Changes

Modules moved but imports not updated:
- `utils/` was removed/moved
- `middleware/` was reorganized
- `infrastructure/` was restructured

---

## Solution Design

### Phase 1: Audit Import Errors (4 hours)

**Step 1: Find all Python files**
```bash
find blackbox5 -name "*.py" -type f > /tmp/all_python_files.txt
```

**Step 2: Test imports for all files**
```python
# test_all_imports.py

import sys
import subprocess
from pathlib import Path

python_files = Path("blackbox5").rglob("*.py")

errors = []

for file in python_files:
    result = subprocess.run(
        ["python3", "-m", "py_compile", str(file)],
        capture_output=True
    )

    if result.returncode != 0:
        errors.append({
            "file": str(file),
            "error": result.stderr.decode()
        })

# Print report
for error in errors:
    print(f"❌ {error['file']}")
    print(f"   {error['error'][:200]}")
```

**Step 3: Categorize errors**
- Missing `__init__.py`
- Wrong relative paths
- Missing modules
- Circular imports

---

### Phase 2: Fix `__init__.py` Files (2 hours)

**Add missing `__init__.py` files:**
```bash
# Find directories without __init__.py
find blackbox5/2-engine -type d -exec sh -c 'if [ ! -f "$1/__init__.py" ] && [ $(find "$1" -name "*.py" | wc -l) -gt 0 ]; then echo "$1"; fi' _ {} \;

# Create __init__.py in needed directories
while read dir; do
    touch "$dir/__init__.py"
    echo "Created: $dir/__init__.py"
done < <(find blackbox5/2-engine -type d -exec sh -c 'if [ ! -f "$1/__init__.py" ] && [ $(find "$1" -name "*.py" | wc -l) -gt 0 ]; then echo "$1"; fi' _ {} \;)
```

---

### Phase 3: Fix Relative Imports (4 hours)

**Strategy:** Convert relative to absolute imports

**Before:**
```python
# agents/ArchitectAgent.py
from ..base_agent import BaseAgent
from ..skill_manager import SkillManager
```

**After:**
```python
# agents/ArchitectAgent.py
from blackbox5.engine.agents.core.base_agent import BaseAgent
from blackbox5.engine.agents.core.skill_manager import SkillManager
```

**Automation Script:**
```python
# fix_imports.py

import re
from pathlib import Path

# Map of relative to absolute imports
import_map = {
    r"from \.base_agent": "from blackbox5.engine.agents.core.base_agent",
    r"from \.core\.base_agent": "from blackbox5.engine.agents.core.base_agent",
    r"from \.\.skill_manager": "from blackbox5.engine.agents.core.skill_manager",
    r"from \.core\.skill_manager": "from blackbox5.engine.agents.core.skill_manager",
    # Add more mappings...
}

def fix_file(file_path: Path):
    """Fix imports in a file"""

    content = file_path.read_text()

    # Apply replacements
    for pattern, replacement in import_map.items():
        content = re.sub(pattern, replacement, content)

    # Write back
    file_path.write_text(content)

# Fix all Python files
for file in Path("blackbox5").rglob("*.py"):
    fix_file(file)
```

---

### Phase 4: Fix Missing Modules (3 hours)

**Issue 1: `utils/helpers` doesn't exist**

**Solution:** Create utility module or inline function

```python
# blackbox5/2-engine/utils/__init__.py
# blackbox5/2-engine/utils/helpers.py

import asyncio
from functools import wraps
from typing import Callable

def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry decorator for async functions"""

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_error = None

            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(delay)

            raise last_error

        return wrapper
    return decorator
```

**Issue 2: `middleware/event_bus` moved**

**Solution:** Update all references

```python
# Old location
from blackbox5.engine.middleware.event_bus import EventBus

# New location
from blackbox5.engine.core.infrastructure.event_bus import EventBus
```

---

### Phase 5: Verify Fixes (2 hours)

**Run comprehensive test:**
```python
# test_imports_fixed.py

import sys
import subprocess
from pathlib import Path

def test_all_imports():
    """Test all Python files can be imported"""

    python_files = list(Path("blackbox5").rglob("*.py"))

    passed = 0
    failed = 0
    errors = []

    for file in python_files:
        result = subprocess.run(
            ["python3", "-m", "py_compile", str(file)],
            capture_output=True,
            timeout=10
        )

        if result.returncode == 0:
            passed += 1
        else:
            failed += 1
            errors.append({
                "file": str(file),
                "error": result.stderr.decode()
            })

    # Print report
    print(f"\n{'='*60}")
    print(f"Import Test Results")
    print(f"{'='*60}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Total: {passed + failed}")

    if failed > 0:
        print(f"\n{'='*60}")
        print("Failed Files:")
        print(f"{'='*60}")
        for error in errors:
            print(f"\n❌ {error['file']}")
            print(f"   {error['error'][:300]}")

    return failed == 0

if __name__ == "__main__":
    success = test_all_imports()
    sys.exit(0 if success else 1)
```

---

## Implementation Plan

### Step 1: Audit (4 hours)
1. Find all Python files
2. Test imports for all
3. Categorize errors
4. Create report

### Step 2: Fix __init__.py (2 hours)
1. Find missing `__init__.py`
2. Create files
3. Verify structure

### Step 3: Fix Relative Imports (4 hours)
1. Create import map
2. Run fix script
3. Verify changes

### Step 4: Fix Missing Modules (3 hours)
1. Create utils module
2. Update references
3. Test imports

### Step 5: Verify (2 hours)
1. Run comprehensive test
2. Fix remaining issues
3. Final verification

---

## Success Criteria

- ✅ All Python files compile without ImportError
- ✅ All `__init__.py` files present
- ✅ Relative imports converted to absolute
- ✅ Missing modules created or references updated
- ✅ Test suite passes (100% import success)
- ✅ No broken imports

---

## Files to Modify

**Estimated:** 50-100 files

**Categories:**
1. Agent files (3-5 files)
   - `agents/ArchitectAgent.py`
   - `agents/AnalystAgent.py`
   - `agents/DeveloperAgent.py`

2. Safety files (5-7 files)
   - `safety/circuit_breaker.py`
   - `safety/anti_patterns.py`
   - `safety/kill_switch.py`
   - Plus 4 more

3. Test files (20-30 files)
   - All test files with import issues

4. Other files (30-50 files)
   - Various modules with import issues

---

## Rollout Plan

### Pre-conditions
- [ ] Audit complete
- [ ] Import map created
- [ ] Backup created

### Execution
1. Add missing `__init__.py` files
2. Fix relative imports
3. Create missing modules
4. Run test suite
5. Fix remaining issues

### Post-conditions
- [ ] All imports working
- [ ] Tests passing
- [ ] No ImportError messages
- [ ] Documentation updated

---

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Breaking working imports | Medium | High | Test each change |
| Circular dependencies | Low | Medium | Detect and refactor |
| Performance impact | Low | Low | Absolute imports faster |
| Missed files | Medium | Low | Comprehensive testing |

---

## Dependencies

**Blocks:**
- Full test suite execution
- Reliable agent loading
- Production deployment

**Blocked By:**
- None

**Can Parallel With:**
- ALL other plans (PLAN-001 through PLAN-008)

---

## Next Steps

1. Run audit script (4 hours)
2. Create error report (30 min)
3. Fix `__init__.py` files (2 hours)
4. Fix relative imports (4 hours)
5. Create missing modules (3 hours)
6. Verify all imports (2 hours)

**Total Estimated Time:** 1-2 days

---

**Status:** Planned
**Ready to Execute:** Yes
**Assigned To:** Unassigned
**Priority:** 🔴 HIGH (blocks testing and reliability)
