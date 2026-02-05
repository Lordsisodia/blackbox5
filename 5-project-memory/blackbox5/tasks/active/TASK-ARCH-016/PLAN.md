# PLAN.md: Unified Configuration Management System

**Task:** TASK-ARCH-016 - Duplicate Configuration Management Systems
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 2-3 weeks
**Importance:** 90 (Critical)

---

## 1. First Principles Analysis

### The Core Problem
The BlackBox5 system has **20+ configuration files** scattered across the engine and project memory, with overlapping purposes and no clear hierarchy. This creates:

- **Configuration drift**: Same settings defined in multiple places
- **Maintenance burden**: Changes require updates to multiple files
- **Onboarding friction**: New agents cannot determine which config to use
- **Runtime confusion**: Scripts hardcode paths instead of using config values

### Root Cause: Organic Growth Without Coordination
Multiple config systems emerged independently:
1. ConfigManager (Python class) for runtime configuration
2. routes.yaml for project routing
3. SYSTEM-MAP.yaml for documentation
4. Multiple schema files for validation
5. Environment variables for deployment-specific values

No single authority coordinates these systems.

### First Principles Solution
- **Single Source of Truth**: One configuration hierarchy
- **Clear Separation of Concerns**: Each config layer has a distinct purpose
- **Validation at Load Time**: Invalid configs fail fast
- **Environment Override**: Deployment-specific values via env vars only

---

## 2. Current State Assessment

### Configuration Systems Inventory

| System | Location | Purpose | Issues |
|--------|----------|---------|--------|
| **ConfigManager** | `2-engine/.autonomous/lib/config_manager.py` | Runtime config loading | Hardcoded defaults, no validation |
| **routes.yaml (project)** | `5-project-memory/blackbox5/.autonomous/context/routes.yaml` | Project routing | Not used by scripts |
| **routes.yaml (engine)** | `2-engine/.autonomous/routes.yaml` | BMAD command routing | Duplicates project routes |
| **SYSTEM-MAP.yaml** | `SYSTEM-MAP.yaml` | Documentation | Out of sync with reality |
| **Core Interface Config** | `2-engine/core/interface/config.py` | Dataclass configs | Overlaps with ConfigManager |
| **default.yaml** | `2-engine/.autonomous/config/default.yaml` | RALF defaults | Not the actual defaults used |
| **config.schema.yaml** | `2-engine/.autonomous/config/config.schema.yaml` | Validation schema | Not enforced |
| **skill-usage.yaml** | Multiple locations | Skill tracking | 3 duplicate files |

### Critical Issues Found

1. **47+ hardcoded paths** instead of config values
2. **Documented hierarchy NOT implemented** (User > Project > Engine > Environment > Base > Default)
3. **Duplicate configs** - skill-usage.yaml exists in 3 locations
4. **No config validation** in practice despite schema existing
5. **Inconsistent environment variables** (RALF_PROJECT_ROOT, BB5_PROJECT_ROOT, BLACKBOX5_HOME)

---

## 3. Proposed Unified Configuration Schema

### Hierarchy (Highest to Lowest Precedence)

```
1. Environment Variables (deployment-specific)
2. User Config (~/.blackbox5/config/user.yaml)
3. Project Config (5-project-memory/[project]/.autonomous/config/project.yaml)
4. Engine Config (2-engine/.autonomous/config/engine.yaml)
5. Base Defaults (2-engine/.autonomous/config/base.yaml)
```

### Unified Schema

```yaml
# config.yaml - Single unified configuration
version: "2.0"

project:
  name: string
  root: string  # Resolved from env or computed
  memory_path: string  # Computed from root

paths:
  engine: string
  memory: string
  knowledge: string
  tools: string
  templates: string

routing:
  commands:
    cp: string
    vp: string
    ca: string
    va: string
  skills:
    registry: string
    auto_discover: boolean

thresholds:
  context:
    warning: 70
    critical: 85
    hard_limit: 95
  phase_gates:
    auto_advance: boolean
    require_verification: boolean

integrations:
  github:
    enabled: boolean
    token_env: string
  mcp:
    enabled: boolean
    servers: list

logging:
  level: enum(debug, info, warn, error)
  destination: enum(console, file, both)
  format: enum(json, text)
```

---

## 4. Implementation Steps

### Phase 1: Create Unified Config System (Week 1)

**Files to Create:**
1. `2-engine/.autonomous/lib/unified_config.py` - New config manager
2. `2-engine/.autonomous/config/base.yaml` - Base defaults
3. `2-engine/.autonomous/config/schema.yaml` - Validation schema

**Key Features:**
- Hierarchical loading with precedence
- Validation against schema
- Environment variable substitution
- Caching for performance

### Phase 2: Migrate Existing Configs (Week 1-2)

**Files to Modify:**
1. `2-engine/.autonomous/lib/config_manager.py` - Deprecate, delegate to unified_config
2. `2-engine/core/interface/config.py` - Use unified config
3. `5-project-memory/blackbox5/.autonomous/context/routes.yaml` - Migrate to project.yaml
4. `2-engine/.autonomous/routes.yaml` - Migrate to engine.yaml

### Phase 3: Replace Hardcoded Paths (Week 2)

**Target Files:**
- All scripts in `bin/` that hardcode paths
- All Python files with hardcoded strings
- Shell scripts with hardcoded references

**Approach:**
1. Identify hardcoded paths (grep for `/.blackbox5/`)
2. Replace with config lookups
3. Add fallback for backward compatibility

### Phase 4: Validation and Testing (Week 3)

**Testing:**
1. Unit tests for unified_config.py
2. Integration tests for config loading
3. Validation that all hardcoded paths are removed
4. Migration verification

---

## 5. Files to Modify/Create

### New Files
| File | Purpose |
|------|---------|
| `2-engine/.autonomous/lib/unified_config.py` | New config manager class |
| `2-engine/.autonomous/config/base.yaml` | Base defaults |
| `2-engine/.autonomous/config/schema.yaml` | Validation schema |
| `2-engine/.autonomous/config/migration.py` | Migration helper |

### Modified Files
| File | Changes |
|------|---------|
| `2-engine/.autonomous/lib/config_manager.py` | Deprecate, delegate to unified |
| `2-engine/core/interface/config.py` | Use unified config |
| `bin/*` | Replace hardcoded paths |
| `5-project-memory/blackbox5/.autonomous/context/routes.yaml` | Migrate format |

### Deleted Files (Post-Migration)
| File | Reason |
|------|--------|
| `2-engine/.autonomous/config/default.yaml` | Replaced by base.yaml |
| `2-engine/.autonomous/config/api-config.yaml` | Consolidated |
| `2-engine/.autonomous/config/cli-config.yaml` | Consolidated |
| Duplicate skill-usage.yaml files | Consolidated |

---

## 6. Success Criteria

- [ ] Single unified config hierarchy implemented
- [ ] All 20+ config files consolidated to 5 or fewer
- [ ] Zero hardcoded paths (all use config)
- [ ] Config validation enforced at load time
- [ ] Environment variable override works
- [ ] Backward compatibility maintained (old configs still work)
- [ ] Migration guide documented
- [ ] All tests pass

---

## 7. Rollback Strategy

If changes cause issues:

1. **Immediate**: Restore original config files from git
2. **Short-term**: Revert to ConfigManager as primary
3. **Full**: Complete rollback using git history

**Rollback Commands:**
```bash
git checkout -- 2-engine/.autonomous/lib/config_manager.py
git checkout -- 2-engine/.autonomous/config/
rm -f 2-engine/.autonomous/lib/unified_config.py
```

---

## 8. Estimated Timeline

| Phase | Duration |
|-------|----------|
| Phase 1: Create Unified Config | 3-4 days |
| Phase 2: Migrate Existing Configs | 4-5 days |
| Phase 3: Replace Hardcoded Paths | 3-4 days |
| Phase 4: Validation and Testing | 2-3 days |
| **Total** | **2-3 weeks** |

---

## 9. Key Design Decisions

### Decision 1: Hierarchical vs Flat
**Choice:** Hierarchical with precedence
**Rationale:** Allows deployment-specific overrides while maintaining defaults

### Decision 2: YAML vs JSON vs TOML
**Choice:** YAML (consistent with existing)
**Rationale:** Existing familiarity, comments support

### Decision 3: Validation Timing
**Choice:** At load time, fail fast
**Rationale:** Catch config errors early, not at runtime

---

*Plan created based on comprehensive analysis of 20+ configuration files*
