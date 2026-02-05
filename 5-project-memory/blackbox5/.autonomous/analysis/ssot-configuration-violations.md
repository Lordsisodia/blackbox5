# SSOT Configuration Violations Report

**Scout:** Architecture Analysis Agent
**Date:** 2026-02-06
**Status:** Complete

---

## Critical Violations Found

### 1. Path Configuration Duplication

**Two routes.yaml files with different structures:**
- `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/routes.yaml` (Engine routes)
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/context/routes.yaml` (Project routes)

**Conflict:** The engine routes.yaml defines BMAD commands and skill routing, while the project routes.yaml defines filesystem paths. They serve different purposes but both claim to be the "routes" configuration.

---

### 2. Skill Configuration Duplication (CRITICAL)

**Skills are defined in FOUR different places:**

| File | Location | Purpose |
|------|----------|---------|
| `skill-registry.yaml` | Engine | Master skill registry with 22 skills |
| `skill-selection.yaml` | Project | Domain-to-skill mapping with auto-trigger rules |
| `skill-metrics.yaml` | Project | Skill effectiveness metrics and task outcomes |
| `skill-usage.yaml` | Project | Usage tracking and logging |

**Specific Duplications:**
- `bmad-pm`, `bmad-architect`, `bmad-analyst`, `bmad-sm`, `bmad-ux`, `bmad-dev`, `bmad-qa`, `bmad-tea`, `bmad-quick-flow`, `superintelligence-protocol`, `continuous-improvement`, `web-search`, `codebase-navigation`, `supabase-operations`, `git-commit`, `task-selection`, `state-management`, `ralf-cloud-control`, `github-codespaces-control`, `legacy-cloud-control` - ALL defined in BOTH skill-registry.yaml AND skill-usage.yaml

**Inconsistency Example:**
- `skill-registry.yaml` lists skill `bmad-planning` but `skill-usage.yaml` does not include it
- `skill-registry.yaml` shows `author: Unknown` for many skills while `skill-usage.yaml` shows specific agent names

---

### 3. Hardcoded Paths in Scripts (Widespread)

**32+ bin scripts hardcode the path pattern `5-project-memory/blackbox5`:**

Key scripts with hardcoded paths:
- `bb5-goal`, `bb5-plan`, `bb5-task`, `bb5-goto`, `bb5-create`, `bb5-discover-context`, `bb5-link`
- `ralf`, `ralf-executor`, `ralf-planner`, `ralf-dual`, `ralf-verifier.sh`
- `ralf-session-start-hook.sh`, `ralf-stop-hook.sh`, `ralf-task-select.sh`

**Example from bb5-discover-context:**
```bash
BLACKBOX5_DIR="$PROJECT_ROOT/5-project-memory/blackbox5"
```

**This violates SSOT because:**
- The routes.yaml defines paths but scripts don't use it
- If the project structure changes, all 32+ scripts need updating
- No centralized path resolution

---

### 4. Agent Prompt Duplication

**Agent prompts exist in BOTH engine and project:**

| Engine | Project |
|--------|---------|
| `2-engine/.autonomous/prompts/agents/scout-validator.md` | `5-project-memory/blackbox5/.autonomous/prompts/agents/scout-agent-prompt.md` |
| `2-engine/.autonomous/prompts/agents/intelligent-scout.md` | (similar scout prompt) |
| `2-engine/.autonomous/prompts/agents/deep-repo-scout.md` | (similar scout prompt) |

Both scout prompts define similar directory structures and missions but are maintained separately.

---

### 5. Configuration Layering Issues

**Base/Environment configs have overlapping concerns:**
- `base.yaml` - Defines `storage.config_dir: "./config"` but this is overridden inconsistently
- `default.yaml` - Has `skill_invocation_confidence: 70`
- `skill-selection.yaml` - Also has confidence threshold of 70% (duplicated logic)
- `dev.yaml` and `prod.yaml` - Override base values but some keys exist in multiple files

---

### 6. CLAUDE.md Duplicates Skill Configuration

**The CLAUDE.md file duplicates skill-selection.yaml content:**

CLAUDE.md contains:
- Domain-to-Skill mapping table (duplicates skill-selection.yaml)
- Auto-trigger rules (duplicates skill-selection.yaml)
- Confidence threshold of 70% (duplicates default.yaml and skill-selection.yaml)

---

## Recommendations for Consolidation

### Immediate Actions:

1. **Create a single skill-registry.yaml** at the engine level that includes:
   - Skill definitions (from skill-registry.yaml)
   - Domain mappings (from skill-selection.yaml)
   - Metrics schema (from skill-metrics.yaml)
   - Usage tracking fields (from skill-usage.yaml)

2. **Create a paths.yaml** configuration file that defines all directory paths, and update all bin scripts to source this file instead of hardcoding paths.

3. **Remove duplicate agent prompts** - Keep only the engine versions and have the project reference them.

4. **Consolidate confidence thresholds** - Define the 70% threshold in ONE place (default.yaml) and have all other files reference it.

### Long-term:

5. **Implement a configuration loader** that merges configs in a predictable hierarchy:
   - Engine defaults -> Project overrides -> Environment variables

6. **Add validation** to ensure no configuration keys are defined in multiple files without explicit override semantics.
