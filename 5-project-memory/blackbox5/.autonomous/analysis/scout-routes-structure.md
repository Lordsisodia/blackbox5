# Scout Report: Routes.yaml Structure Analysis

**Scout:** Architecture Analysis Agent
**Date:** 2026-02-06
**Status:** Complete

---

## Current State Analysis

**Two routes.yaml files exist:**

### 1. Engine routes.yaml (2-engine/.autonomous/routes.yaml)
- **Purpose:** Defines BMAD command system, skills registry, workflows
- **Contains:** 38 BMAD commands, skill paths, workflow patterns
- **Routes:** Points to engine-relative paths (./skills, ./workflows, etc.)
- **Run path:** `../../../5-project-memory/ralf-core/.autonomous/runs` (outdated)

### 2. Project routes.yaml (5-project-memory/blackbox5/.autonomous/context/routes.yaml)
- **Purpose:** Project-specific routing with full blackbox5 access
- **Contains:** Project metadata, memory paths, tool routes
- **Routes:** Absolute paths to all blackbox5 directories

---

## Critical Issues Identified

### Issue #1: Incorrect Path Nesting in Project routes.yaml

The following paths in project routes.yaml are INCORRECT (they suggest 2-engine is nested inside 5-project-memory/blackbox5):

```yaml
engine: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine"
engine_shell: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine/.autonomous/shell"
engine_lib: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine/.autonomous/lib"
engine_prompts: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine/.autonomous/prompts"
engine_skills: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine/.autonomous/skills"
engine_schemas: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine/.autonomous/schemas"
engine_routes: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine/.autonomous/routes.yaml"
bmad_skills: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine/.autonomous/skills"
bmad_workflows: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine/.autonomous/workflows"
bmad_wip: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine/.autonomous/wip"
```

**Verification:** The path `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine/.autonomous/` does NOT exist. The correct path is `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/`.

### Issue #2: Duplicated Memory Paths

Project routes.yaml has paths like:
```yaml
memory:
  tasks: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/5-project-memory/blackbox5/tasks"
```

This incorrectly duplicates `5-project-memory/blackbox5` in the path.

### Issue #3: Overlapping Functionality

Both files define routes, but with different structures:
- Engine uses relative paths (./skills, ./workflows)
- Project uses absolute paths with incorrect nesting

---

## Proposed Hierarchical Structure

**Design Principle:**
- Engine routes.yaml = Base/Template configuration (generic, applies to ALL projects)
- Project routes.yaml = Project-specific overrides/extensions only

### New Structure

**Engine routes.yaml** (2-engine/.autonomous/routes.yaml):
```yaml
# Base configuration for ALL projects
engine:
  version: "2.0.0"
  path: "{{ENGINE_PATH}}"  # Template variable

bmad:
  enabled: true
  commands: { ... }  # All BMAD commands
  artifact_paths: { ... }

skills:
  path: "{{ENGINE_PATH}}/skills"

workflows:
  path: "{{ENGINE_PATH}}/workflows"

# Template for project extension
project:
  extends: true
  # Projects define their own routes below this
```

**Project routes.yaml** (5-project-memory/blackbox5/.autonomous/context/routes.yaml):
```yaml
# Project-specific configuration ONLY
project:
  name: "blackbox5"
  root: "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5"

# Reference to engine (correct path)
engine:
  path: "/Users/shaansisodia/.blackbox5/2-engine/.autonomous"
  routes: "/Users/shaansisodia/.blackbox5/2-engine/.autonomous/routes.yaml"

# Project-specific routes only (no duplication of engine routes)
routes:
  tasks: "./tasks"
  runs: "./runs"
  decisions: "./.autonomous/memory/decisions"
  # ... other project-specific paths

# Project-specific extensions
extensions:
  bmad_commands: { ... }  # Additional project-specific commands
  custom_workflows: { ... }
```

---

## Migration Plan

### Phase 1: Fix Incorrect Paths (Immediate)
1. Correct all paths in project routes.yaml that incorrectly nest 2-engine
2. Fix duplicated path segments (5-project-memory/blackbox5/5-project-memory/blackbox5)
3. Verify all paths exist

### Phase 2: Implement Hierarchical Loading
1. Define precedence rules: Project overrides Engine
2. Create path resolution utility
3. Update all scripts to use the resolution utility

### Phase 3: Content Separation
1. Move generic BMAD commands to engine only
2. Keep project-specific commands in project
3. Remove duplicate route definitions

### Phase 4: Validation
1. Create validation script to check all routes
2. Test path resolution in both files
3. Verify no broken references

---

## Path Resolution Algorithm

```python
def resolve_route(route_name, project_routes_file):
    """
    1. Load engine routes.yaml (base)
    2. Load project routes.yaml (overlay)
    3. Project routes override engine routes for same keys
    4. Engine-only routes remain available
    5. Return merged configuration
    """
    engine_config = load_yaml(ENGINE_ROUTES_PATH)
    project_config = load_yaml(project_routes_file)

    # Project takes precedence
    merged = deep_merge(engine_config, project_config)
    return merged
```

---

## Key Files

- **Engine routes.yaml**: `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/routes.yaml`
- **Project routes.yaml**: `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/context/routes.yaml`
- **Routes template**: `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/context/routes.yaml.template`
- **Init script**: `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/context/init-routes.sh`
- **Project map**: `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/project-map.yaml`
- **Engine/Project analysis**: `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/analysis/engine-project-split-analysis.md`

---

## Summary

The routes.yaml system has structural issues where project routes.yaml contains incorrect absolute paths that suggest 2-engine is nested inside the project directory. The solution is to implement a hierarchical structure where engine routes.yaml serves as the base configuration and project routes.yaml contains only project-specific overrides. This requires fixing 10+ incorrect paths and establishing clear precedence rules for route resolution.
