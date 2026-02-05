# Scout Report: Configuration System Analysis

**Scout:** Architecture Analysis Agent
**Date:** 2026-02-06
**Status:** Complete

---

## Configuration Files Identified

### Engine Configuration (2-engine/.autonomous/)

1. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/routes.yaml` - Main routing configuration with BMAD commands, skills, workflows
2. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/config/base.yaml` - Base configuration with system defaults
3. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/config/default.yaml` - RALF default configuration with thresholds, routing, notifications
4. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/config/dev.yaml` - Development environment overrides
5. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/config/prod.yaml` - Production environment overrides
6. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/config/staging.yaml` - Staging environment overrides
7. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/config/config.schema.yaml` - JSON schema for configuration validation
8. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/config/skill-registry.yaml` - Skill registry with 22 skills
9. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/config/cli-config.yaml` - CLI-specific configuration
10. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/config/github-config.yaml` - GitHub integration configuration
11. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/config/api-config.yaml` - API configuration
12. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/config/alert-config.yaml` - Alert configuration
13. `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/config/code-review-config.yaml` - Code review configuration

### Project Configuration (5-project-memory/blackbox5/)

1. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/context/routes.yaml` - Project-specific routes with full BlackBox5 access
2. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/skill-selection.yaml` - Skill selection framework
3. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/skill-metrics.yaml` - Skill effectiveness metrics
4. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/skill-usage.yaml` - Skill usage tracking
5. `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/operations/skill-usage.yaml` - Duplicate skill usage file

### Core Interface Configuration

1. `/Users/shaansisodia/.blackbox5/2-engine/core/interface/config.py` - Python configuration loader with dataclasses

---

## Configuration Hierarchy Map

```
User Config (~/.blackbox5/config.yaml) [NOT IMPLEMENTED - referenced but doesn't exist]
    |
    v
Project routes.yaml (5-project-memory/blackbox5/.autonomous/context/routes.yaml)
    |
    v
Engine routes.yaml (2-engine/.autonomous/routes.yaml)
    |
    v
Environment Config (dev.yaml/staging.yaml/prod.yaml) [inherit from base.yaml]
    |
    v
Base Config (2-engine/.autonomous/config/base.yaml)
    |
    v
Default Config (2-engine/.autonomous/config/default.yaml)
```

---

## Critical Issues Found

### 1. **No Centralized Config System**
- Configuration is scattered across 20+ YAML files
- No single source of truth
- Different config files use different schemas and formats

### 2. **Duplicate Configuration Files**
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/skill-usage.yaml` and `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/operations/skill-usage.yaml` are duplicates
- Skill registry exists in both `2-engine/.autonomous/config/skill-registry.yaml` and is referenced in operations

### 3. **Hardcoded Values in Scripts**
Multiple scripts have hardcoded paths instead of using configuration:

**bin/ralf-report:**
```bash
BLACKBOX5_DIR="/Users/shaansisodia/.blackbox5"  # Hardcoded absolute path
```

**bin/ralf-branch:**
```bash
BLACKBOX5_DIR="/Users/shaansisodia/.blackbox5"  # Hardcoded absolute path
```

**bin/ralf-analyze:**
```bash
BLACKBOX5_DIR="/Users/shaansisodia/.blackbox5"  # Hardcoded absolute path
```

**bin/blackbox:**
```bash
BLACKBOX_DIR="/Users/shaansisodia/DEV/SISO-ECOSYSTEM/SISO-INTERNAL/BLACKBOX5"  # Outdated hardcoded path
```

### 4. **No Config Validation in Practice**
- While `config.schema.yaml` exists, there's no evidence it's actively used
- Scripts don't validate configuration before use
- No error handling for missing config values

### 5. **Inconsistent Config Loading**
- Python code (`config.py`) looks for config in `blackbox5/config.yml`
- Shell scripts use various methods: hardcoded paths, relative paths, environment variables
- No standard config loader utility for shell scripts

### 6. **Missing User Config**
- `default.yaml` documents: "User config: ~/.blackbox5/config.yaml (overrides defaults)"
- This file does not exist and there's no mechanism to create it

### 7. **Config Override Hierarchy Not Implemented**
- The documented hierarchy (User > Project > Engine > Environment > Base > Default) is not actually implemented
- `config.py` only looks for `blackbox5/config.yml` in project root
- No mechanism to load and merge multiple config files

### 8. **Environment Variable Handling Inconsistent**
- Some scripts check `RALF_PROJECT_ROOT`, `BB5_PROJECT_ROOT`, `BLACKBOX5_HOME`
- No standardized environment variable naming
- No central env var configuration

### 9. **Routes.yaml Not Actually Used**
- Both engine and project have `routes.yaml` files
- Scripts like `bb5-discover-context` hardcode paths instead of reading from routes.yaml
- The routes.yaml files serve as documentation but not as active configuration

### 10. **Skill Configuration Duplication**
- Skills defined in `2-engine/.autonomous/config/skill-registry.yaml`
- Skill usage tracked in `5-project-memory/blackbox5/operations/skill-usage.yaml`
- Skill metrics in `5-project-memory/blackbox5/operations/skill-metrics.yaml`
- Skill selection rules in `5-project-memory/blackbox5/operations/skill-selection.yaml`
- No single skill configuration source

---

## Recommendations for Unified Config System

1. **Create a Central Config Loader**
   - Python module that implements the documented hierarchy
   - Shell script utility for bash scripts to source config
   - Validation against schema on load

2. **Eliminate Hardcoded Paths**
   - Replace all `/Users/shaansisodia/.blackbox5` hardcoded paths
   - Use `$BLACKBOX5_HOME` or `$RALF_PROJECT_ROOT` consistently
   - Add path resolution to central config

3. **Merge Duplicate Configs**
   - Consolidate skill configuration into single source
   - Remove duplicate `skill-usage.yaml` files
   - Create single operations config file

4. **Implement Config Hierarchy**
   - Actually implement the documented override hierarchy
   - Create default user config template
   - Add config merge logic with precedence

5. **Standardize Environment Variables**
   - Define standard: `$BLACKBOX5_HOME` for installation root
   - Define standard: `$BLACKBOX5_PROJECT` for current project
   - Document all environment variables

6. **Make routes.yaml Functional**
   - Update scripts to read paths from routes.yaml
   - Create routes loader utility
   - Validate routes on startup

7. **Add Config Validation**
   - Run validation on all config files
   - Fail fast on invalid configuration
   - Provide helpful error messages

8. **Create Config Documentation**
   - Document all configuration options
   - Provide config examples for common scenarios
   - Add config troubleshooting guide
