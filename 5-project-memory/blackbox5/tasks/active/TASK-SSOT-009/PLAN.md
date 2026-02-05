# PLAN.md: Consolidate MCP Configuration

**Task:** TASK-SSOT-009 - MCP configuration in multiple places
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 2-3 hours
**Importance:** 65 (Medium-High)

---

## 1. First Principles Analysis

### The Core Problem
MCP (Model Context Protocol) configuration is scattered across:
- `2-engine/.autonomous/mcp/config.yaml`
- `5-project-memory/blackbox5/.autonomous/mcp/config.yaml`
- Potentially `.claude/mcp.json` or similar

This creates:
1. **Configuration Drift**: Different settings in different places
2. **Discovery Issues**: Hard to find all MCP configurations
3. **Maintenance Overhead**: Updates needed in multiple places
4. **Inconsistent Behavior**: Same MCP behaving differently

### Guiding Principle
- **Project-Owned Config**: MCP settings are project-specific
- **Engine = Framework**: Engine provides MCP tools, not configuration
- **Clear Hierarchy**: Project config extends/overrides engine defaults

---

## 2. Current State Analysis

### Files Involved

| File | Purpose |
|------|---------|
| `2-engine/.autonomous/mcp/config.yaml` | Engine MCP config |
| `5-project-memory/blackbox5/.autonomous/mcp/config.yaml` | Project MCP config |

### Configuration Overlap

Both files may define:
- MCP server endpoints
- Authentication tokens
- Tool configurations
- Rate limits

---

## 3. Proposed Solution

### Decision: Project-Owned MCP Configuration

**Canonical Location:** `5-project-memory/blackbox5/.autonomous/mcp/config.yaml`

**Rationale:**
- MCP configurations are project-specific
- Different projects may use different MCP servers
- Engine provides the MCP framework/tools

### Implementation Plan

#### Phase 1: Audit (30 min)

1. Read engine MCP config
2. Read project MCP config
3. Identify:
   - Unique configs in engine (need migration)
   - Unique configs in project (keep)
   - Overlapping configs (merge)

#### Phase 2: Merge (1 hour)

1. Merge all MCP configs into project file
2. Use hierarchical structure:

```yaml
# Project MCP config
version: "1.0"

# Project-specific MCP servers
servers:
  notion:
    url: "${NOTION_MCP_URL}"
    auth:
      token: "${NOTION_TOKEN}"

# Inherits from engine (documented but not duplicated)
# Engine provides: filesystem, database, etc.
```

#### Phase 3: Update MCP Loading (1 hour)

**Update:** MCP initialization to load from project first

```python
def load_mcp_config():
    """Load MCP config with project taking precedence."""
    project_config = load_project_mcp_config()
    engine_config = load_engine_mcp_config()

    # Project config takes precedence
    return merge_configs(engine_config, project_config)
```

#### Phase 4: Cleanup (30 min)

1. Remove engine MCP config (or keep minimal defaults)
2. Update documentation
3. Test all MCP connections

---

## 4. Files to Modify

### Modified Files
1. `5-project-memory/blackbox5/.autonomous/mcp/config.yaml` - Merge engine config
2. `2-engine/.autonomous/mcp/config.yaml` - Remove or minimize

### Scripts to Update
1. MCP initialization code
2. Any scripts loading MCP config

---

## 5. Success Criteria

- [ ] All MCP configs consolidated to project
- [ ] MCP loading works correctly
- [ ] All MCP connections functional
- [ ] Documentation updated
- [ ] No duplicate configurations

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Restore engine MCP config
2. **Fix**: Debug config loading
3. **Re-apply**: Once fixed

---

## 7. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Audit | 30 min | 30 min |
| Phase 2: Merge | 1 hour | 1.5 hours |
| Phase 3: Loading | 1 hour | 2.5 hours |
| Phase 4: Cleanup | 30 min | 3 hours |
| **Total** | | **2-3 hours** |

---

*Plan created based on SSOT violation analysis - MCP configuration scattered*
