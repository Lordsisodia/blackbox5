# PLAN.md: Consolidate Agent Registry

**Task:** TASK-SSOT-006 - Agent registry duplicates across engine and project
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 3-4 hours
**Importance:** 70 (High)

---

## 1. First Principles Analysis

### The Core Problem
Agent registry information is duplicated across:
- `2-engine/.autonomous/agents/` - Engine agent definitions
- `5-project-memory/blackbox5/.autonomous/agents/` - Project agent definitions

This creates:
1. **Version Conflicts**: Different versions of same agent
2. **Maintenance Overhead**: Updates needed in multiple places
3. **Discovery Complexity**: Finding agents requires checking both locations
4. **Inconsistent Behavior**: Same agent behaving differently

### Guiding Principle
- **Engine = Generic Agents**: Framework-level agents live in engine
- **Project = Specific Agents**: Project-specific agents live in project
- **No Duplication**: Each agent exists in exactly one location
- **Clear Inheritance**: Project agents can extend engine agents

---

## 2. Current State Analysis

### Directory Structure

```
2-engine/.autonomous/agents/
├── scout/
│   └── agent.yaml
├── executor/
│   └── agent.yaml
└── verifier/
    └── agent.yaml

5-project-memory/blackbox5/.autonomous/agents/
├── scout/
│   └── agent.yaml
├── executor/
│   └── agent.yaml
├── verifier/
│   └── agent.yaml
└── communications/
    └── events.yaml
```

### Issues

1. **Duplicate Agents**: Same agent type in both locations
2. **Divergent Configs**: Different settings for same agent
3. **Unclear Authority**: Which agent definition takes precedence?

---

## 3. Proposed Solution

### Decision: Hierarchical Agent Registry

**Engine Agents:** Generic, reusable across projects
- scout (base implementation)
- executor (base implementation)
- verifier (base implementation)

**Project Agents:** Project-specific or extending engine
- communications (project-specific)
- Any agent overriding engine defaults

### Implementation Plan

#### Phase 1: Audit (30 min)

1. List all agents in engine
2. List all agents in project
3. Identify:
   - True duplicates (same purpose)
   - Project-specific agents
   - Engine agents that should be generic

#### Phase 2: Consolidate (2 hours)

1. **For duplicates:**
   - Compare configurations
   - Keep engine version as base
   - Move project-specific overrides to project
   - Remove duplicate from project

2. **For project-specific:**
   - Keep in project
   - Document in registry

#### Phase 3: Create Unified Registry (1 hour)

**File:** `5-project-memory/blackbox5/.autonomous/agents/registry.yaml`

```yaml
version: "1.0"
agents:
  # Engine agents (inherited)
  scout:
    source: engine
    path: "2-engine/.autonomous/agents/scout/"
    description: "Base scout agent"

  executor:
    source: engine
    path: "2-engine/.autonomous/agents/executor/"
    description: "Base executor agent"

  # Project agents (local)
  communications:
    source: project
    path: "5-project-memory/blackbox5/.autonomous/agents/communications/"
    description: "Project communication handler"

  # Overrides
  scout-custom:
    source: project
    path: "5-project-memory/blackbox5/.autonomous/agents/scout-custom/"
    extends: scout
    description: "Custom scout with BlackBox5-specific logic"
```

#### Phase 4: Update Discovery (30 min)

Update agent discovery to check unified registry first:

```python
def get_agent_path(agent_name: str) -> str:
    registry = load_agent_registry()
    if agent_name in registry["agents"]:
        return registry["agents"][agent_name]["path"]
    raise AgentNotFoundError(agent_name)
```

---

## 4. Files to Modify

### New Files
1. `5-project-memory/blackbox5/.autonomous/agents/registry.yaml` - Unified registry

### Modified Files
1. Remove duplicate agent directories from project
2. Update agent loading scripts

### Scripts to Update
1. `2-engine/.autonomous/bin/scout-intelligent.py`
2. `2-engine/.autonomous/bin/executor-implement.py`
3. Any agent discovery/loading code

---

## 5. Success Criteria

- [ ] Unified agent registry created
- [ ] No duplicate agents between engine and project
- [ ] All agents discoverable via registry
- [ ] Agent loading works correctly
- [ ] Documentation updated

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Restore duplicate agents
2. **Fix**: Debug registry loading
3. **Re-apply**: Once fixed

---

## 7. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Audit | 30 min | 30 min |
| Phase 2: Consolidate | 2 hours | 2.5 hours |
| Phase 3: Registry | 1 hour | 3.5 hours |
| Phase 4: Discovery | 30 min | 4 hours |
| **Total** | | **3-4 hours** |

---

*Plan created based on SSOT violation analysis - Agent registry duplicates*
