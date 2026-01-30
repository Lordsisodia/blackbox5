# PLAN-002: Fix YAML Agent Loading

**Priority:** 🔴 HIGH
**Status:** Planned
**Estimated Effort:** 1 day
**Dependencies:** None (can parallel with PLAN-001)
**Validation Agent:** Agent 3 (Agent System)

---

## Problem Statement

YAML-based specialist agents are **not loading at all**. Only 3 of 21 agents work.

**Current State:**
```
Core Agents Loaded: 3/3 (100%) ✅
Specialist Agents Loaded: 0/18 (0%) ❌ COMPLETE FAILURE
```

**Impact:** Reduced capability coverage, 18 specialist agents inaccessible

---

## Root Cause Analysis

### Path Mismatch in AgentLoader

**Current AgentLoader Code:**
```python
# blackbox5/2-engine/01-core/agents/core/agent_loader.py

class AgentLoader:
    def __init__(self, agents_path: str):
        self.agents_path = Path(agents_path)
        # Only looks in ONE directory!
```

**Problem:** AgentLoader only scans:
```
blackbox5/2-engine/01-core/agents/
```

But YAML agents are at:
```
blackbox5/2-engine/02-agents/specialists/
```

### Missing YAML Parsing

AgentLoader expects Python modules:
```python
module = importlib.import_module(agent_file)
agent_class = getattr(module, "Agent")
```

But YAML agents need:
```python
import yaml
agent_def = yaml.safe_load(agent_file)
agent_class = type_from_yaml(agent_def)
```

---

## Solution Design

### Phase 1: Extend AgentLoader (4 hours)

**Update AgentLoader to support multiple paths:**

```python
# blackbox5/2-engine/01-core/agents/core/agent_loader.py

class AgentLoader:
    def __init__(self, agents_paths: List[str]):
        """Support multiple agent directories"""
        self.agents_paths = [Path(p) for p in agents_paths]
        self.registry = {}

    async def load_all(self):
        """Load from all paths"""
        for path in self.agents_paths:
            await self._load_from_path(path)

    async def _load_from_path(self, path: Path):
        """Load agents from single path"""
        for agent_file in path.rglob("*.py"):
            await self._load_python_agent(agent_file)

        for agent_file in path.rglob("*.yaml"):
            await self._load_yaml_agent(agent_file)
```

### Phase 2: Add YAML Parsing (3 hours)

**Implement YAML agent loading:**

```python
async def _load_yaml_agent(self, agent_file: Path):
    """Load agent from YAML definition"""

    with open(agent_file) as f:
        agent_def = yaml.safe_load(f)

    # Extract agent metadata
    name = agent_def.get("name")
    role = agent_def.get("role")
    capabilities = agent_def.get("capabilities", [])
    tools = agent_def.get("tools", [])

    # Create agent instance
    config = AgentConfig(
        name=name,
        full_name=agent_def.get("full_name", name),
        role=role,
        category=agent_def.get("category", "specialists"),
        description=agent_def.get("description", ""),
        capabilities=capabilities,
        tools=tools
    )

    # Create agent class dynamically
    agent_class = type(
        f"{name.capitalize()}Agent",
        (BaseAgent,),
        {
            "__init__": lambda self, cfg: BaseAgent.__init__(self, cfg)
        }
    )

    # Instantiate and register
    agent = agent_class(config)
    self.registry[name] = agent

    return agent
```

### Phase 3: Update Main Entry Point (1 hour)

**Update main.py to use both paths:**

```python
# blackbox5/2-engine/01-core/infrastructure/main.py

async def bootstrap():
    """Bootstrap BlackBox5"""

    # Load agents from multiple paths
    agent_loader = AgentLoader([
        "blackbox5/2-engine/01-core/agents/",      # Core agents
        "blackbox5/2-engine/02-agents/specialists/" # YAML agents
    ])

    agents = await agent_loader.load_all()

    print(f"Loaded {len(agents)} agents")
    # Expected: 21 agents (3 core + 18 specialists)
```

---

## Implementation Plan

### Step 1: Audit YAML Agents (1 hour)

**List all YAML agents:**
```bash
find blackbox5/2-engine/02-agents/specialists/ -name "*.yaml" -o -name "*.yml"

# Sample output expected:
# - blackbox5/2-engine/02-agents/specialists/ux-designer/agent.yaml
# - blackbox5/2-engine/02-agents/specialists/tech-writer/agent.yaml
# - ... (18 total)
```

**Analyze YAML structure:**
```bash
# Check first few YAML files
head -20 blackbox5/2-engine/02-agents/specialists/*/agent.yaml
```

**Document YAML schema:**
What fields exist? (name, role, capabilities, tools, etc.)

### Step 2: Extend AgentLoader (4 hours)

1. Update `__init__` to accept list of paths
2. Add `_load_from_path()` method
3. Add `_load_yaml_agent()` method
4. Update `load_all()` to iterate paths

### Step 3: Update main.py (1 hour)

1. Change AgentLoader instantiation
2. Pass list of paths
3. Add logging for loaded agents

### Step 4: Test (2 hours)

**Test suite:**
```python
# test_yaml_agent_loading.py

async def test_multiple_paths():
    """AgentLoader loads from multiple paths"""
    loader = AgentLoader([
        "blackbox5/2-engine/01-core/agents/",
        "blackbox5/2-engine/02-agents/specialists/"
    ])
    agents = await loader.load_all()
    assert len(agents) >= 21, f"Expected 21+, got {len(agents)}"

async def test_yaml_agents_loaded():
    """All 18 YAML agents load"""
    loader = AgentLoader(agents_paths)
    agents = await loader.load_all()

    yaml_agents = [a for a in agents.values() if a.config.category == "specialists"]
    assert len(yaml_agents) == 18, f"Expected 18, got {len(yaml_agents)}"

async def test_agent_registry():
    """All agents in registry"""
    loader = AgentLoader(agents_paths)
    agents = await loader.load_all()

    expected_agents = [
        "developer", "analyst", "architect",  # Core
        "ux-designer", "tech-writer", "test-engineer", # Specialists
        # ... 15 more
    ]

    for name in expected_agents:
        assert name in agents, f"Missing: {name}"
```

---

## Success Criteria

- ✅ AgentLoader accepts list of paths
- ✅ AgentLoader loads from all paths
- ✅ YAML parsing implemented and working
- ✅ 18 YAML agents load successfully
- ✅ Total 21 agents in registry (3 core + 18 specialists)
- ✅ All agents accessible by name
- ✅ Tests pass (5/5)

---

## Rollout Plan

### Pre-conditions
- [ ] YAML agent locations documented
- [ ] YAML schema understood
- [ ] Backup created

### Execution
1. Update AgentLoader class
2. Add YAML parsing logic
3. Update main.py
4. Run test suite
5. Verify 21 agents loaded

### Post-conditions
- [ ] 18 YAML agents loading
- [ ] All tests passing
- [ ] main.py boots with 21 agents
- [ ] Documentation updated

---

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| YAML schema varies | High | Medium | Handle variations gracefully |
| YAML parsing errors | Medium | High | Comprehensive error handling |
| Broken YAML files | Medium | Medium | Validation before loading |
| Performance issues | Low | Low | Cache loaded agents |

---

## Dependencies

**Blocks:**
- PLAN-003: Implement Planning Agent (needs all agents loaded)
- End-to-end workflow testing (needs all agents)

**Blocked By:**
- None (can start immediately)

**Can Parallel With:**
- PLAN-001: Fix Skills System
- PLAN-004: Fix Import Paths
- PLAN-005: Initialize Vibe Kanban

---

## Next Steps

1. Audit YAML agents (1 hour)
2. Document YAML schema (30 min)
3. Extend AgentLoader (4 hours)
4. Add YAML parsing (3 hours)
5. Update main.py (1 hour)
6. Test and verify (2 hours)

**Total Estimated Time:** 1 day

---

**Status:** Planned
**Ready to Execute:** Yes
**Assigned To:** Unassigned
**Priority:** 🔴 HIGH (reduces agent availability to 14%)
