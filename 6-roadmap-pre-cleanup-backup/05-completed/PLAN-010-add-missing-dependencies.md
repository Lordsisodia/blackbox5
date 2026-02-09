# PLAN-010: Add Missing Dependencies to requirements.txt

**Priority:** 🟡 MEDIUM (Deployment Issue)
**Status:** Planned
**Estimated Effort:** 30 minutes
**Dependencies:** None
**Discovered By:** First Principles Analysis

---

## Problem Statement

**Redis is used but not listed in requirements.txt**, causing deployment failures.

**Impact:** System fails to boot on fresh installations

---

## Missing Dependencies

### 1. redis (Required for EventBus)

**Used in:** `state/event_bus.py`

**Import:**
```python
import redis.asyncio as aioredis
from redis.asyncio.connection import Connection
from redis.exceptions import RedisError
```

**Status:** ❌ NOT in requirements.txt

**Issue:** Fresh installations fail with:
```
ModuleNotFoundError: No module named 'redis'
```

---

### 2. Other Potential Missing Dependencies

**To be verified:**
- `yaml` or `pyyaml` (used by YAML agent loading)
- `chromadb` (used by episodic memory)
- `neo4j` (used by semantic memory)
- `llmlingua` (used by token compression)

---

## Solution Design

### Phase 1: Audit All Imports (15 min)

**Find all imports:**
```bash
cd blackbox5

# Find all Python files
find . -name "*.py" -type f > /tmp/all_py_files.txt

# Extract imports
cat /tmp/all_py_files.txt | xargs grep -h "^import\|^from" | sort -u > /tmp/all_imports.txt

# Check common missing ones
cat /tmp/all_imports.txt | grep -E "^(redis|yaml|chroma|neo4j|llmlingua)"
```

**Results to document:**
- List all external package imports
- Identify which are in requirements.txt
- Identify which are missing

---

### Phase 2: Update requirements.txt (10 min)

**Current requirements.txt location:**
```bash
# Find requirements.txt
find blackbox5 -name "requirements.txt" -o -name "requirements-*.txt"
```

**Add missing packages:**
```txt
# Existing requirements...

# Added for PLAN-010:
redis>=5.0.0              # Required for EventBus (async redis)
pyyaml>=6.0               # Required for YAML agent loading
chromadb>=0.4.0           # Required for episodic memory
neo4j>=5.0.0              # Required for semantic memory
llmlingua>=0.2.2          # Required for token compression
```

---

### Phase 3: Create requirements-dev.txt (5 min)

**Development-only dependencies:**
```txt
# Core requirements
-r requirements.txt

# Development
pytest>=7.0.0
pytest-asyncio>=0.21.0
black>=23.0.0
mypy>=1.0.0

# Testing
pytest-cov>=4.0.0
pytest-mock>=3.10.0

# Linting
flake8>=6.0.0
pylint>=2.17.0
```

---

## Implementation Plan

### Step 1: Find requirements.txt (5 min)

```bash
cd blackbox5
find . -name "requirements*.txt"

# Expected locations:
# - ./requirements.txt
# - ./2-engine/requirements.txt
# - Or similar
```

---

### Step 2: Audit imports (10 min)

```bash
cd blackbox5

# Create audit script
cat > /tmp/check_imports.py << 'EOF'
import sys
from pathlib import Path
import re

# Common external packages
external_packages = {
    'redis', 'yaml', 'pyyaml', 'chroma', 'chromadb',
    'neo4j', 'llmlingua', 'openai', 'anthropic',
    'fastapi', 'uvicorn', 'sqlalchemy', 'alembic'
}

found_imports = set()

# Scan all Python files
for py_file in Path('.').rglob('*.py'):
    try:
        content = py_file.read_text()
        for line in content.split('\n'):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                for package in external_packages:
                    if package in line.lower():
                        found_imports.add(package)
    except:
        pass

print("External packages used:")
for pkg in sorted(found_imports):
    print(f"  - {pkg}")
EOF

python3 /tmp/check_imports.py
```

---

### Step 3: Check current requirements.txt (5 min)

```bash
# List what's in requirements
cat requirements.txt

# Check for missing packages
for pkg in redis pyyaml chromadb neo4j llmlingua; do
    if grep -q "$pkg" requirements.txt; then
        echo "✅ $pkg found"
    else
        echo "❌ $pkg MISSING"
    fi
done
```

---

### Step 4: Update requirements.txt (5 min)

```bash
# Backup
cp requirements.txt requirements.txt.backup

# Add missing dependencies
cat >> requirements.txt << 'EOF'

# Added for PLAN-010 - Missing dependencies
redis>=5.0.0              # Required for EventBus (async redis)
pyyaml>=6.0               # Required for YAML agent loading
chromadb>=0.4.0           # Required for episodic memory
neo4j>=5.0.0              # Required for semantic memory (optional)
llmlingua>=0.2.2          # Required for token compression
EOF

# Verify
cat requirements.txt
```

---

### Step 5: Create requirements-dev.txt (5 min)

```bash
cat > requirements-dev.txt << 'EOF'
# Include all runtime dependencies
-r requirements.txt

# Development dependencies
pytest>=7.0.0
pytest-asyncio>=0.21.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0

# Code quality
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
pylint>=2.17.0
EOF
```

---

### Step 6: Test Installation (10 min)

```bash
# Create fresh virtual environment
python3 -m venv /tmp/test_env
source /tmp/test_env/bin/activate

# Install requirements
pip install -r requirements.txt

# Test imports
python3 << 'EOF'
import redis
import yaml
import chromadb
print("✅ All critical imports work")
EOF

deactivate
```

---

## Success Criteria

- ✅ All external packages identified
- ✅ Missing packages added to requirements.txt
- ✅ requirements-dev.txt created
- ✅ Fresh installation works
- ✅ All imports successful
- ✅ No ModuleNotFoundError

---

## Rollout Plan

### Pre-conditions
- [ ] requirements.txt located
- [ ] All imports audited

### Execution
1. Audit all imports
2. Update requirements.txt
3. Create requirements-dev.txt
4. Test fresh installation
5. Commit changes

### Post-conditions
- [ ] requirements.txt complete
- [ ] Fresh install works
- [ ] Documentation updated

---

## Requirements File Structure

```
blackbox5/
├── requirements.txt         # Runtime dependencies (updated)
├── requirements-dev.txt     # Development dependencies (new)
└── 2-engine/
    └── requirements.txt     # Engine-specific (if needed)
```

---

## Optional Dependencies

**Mark as optional with extras:**

```txt
# Core requirements
redis>=5.0.0
pyyaml>=6.0

# Optional features
[neo4j]
neo4j>=5.0.0              # For semantic memory (optional)

[vector]
chromadb>=0.4.0           # For episodic memory (optional)

[compression]
llmlingua>=0.2.2          # For token compression (optional)

# Install all: pip install -e ".[neo4j,vector,compression]"
```

---

## Dependencies

**Blocks:**
- Fresh installations
- Deployments
- CI/CD pipelines

**Blocked By:**
- None

**Can Parallel With:**
- All other plans (infrastructure task)

---

## Files to Modify/Create

| File | Action | Description |
|------|--------|-------------|
| `requirements.txt` | Modify | Add missing dependencies |
| `requirements-dev.txt` | Create | Development dependencies |
| `README.md` | Modify | Document installation |

---

## Next Steps

1. Find requirements.txt (5 min)
2. Audit imports (10 min)
3. Update requirements.txt (5 min)
4. Create requirements-dev.txt (5 min)
5. Test installation (10 min)

**Total Estimated Time:** 30 minutes

---

**Status:** Planned
**Ready to Execute:** Yes
**Assigned To:** Unassigned
**Priority:** 🟡 MEDIUM (deployment blocker, but local dev works)
