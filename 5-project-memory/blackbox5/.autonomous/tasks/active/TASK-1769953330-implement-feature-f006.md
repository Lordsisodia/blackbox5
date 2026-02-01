# TASK-1769953330: Implement Feature F-006 (User Preference & Configuration System)

**Type:** implement (feature)
**Priority:** high
**Status:** pending
**Created:** 2026-02-01T18:35:30Z
**Estimated Minutes:** 90 (~1.5 hours)

## Objective

Implement the User Preference & Configuration System (F-006), enabling RALF operators to customize agent behavior, set preferences, and define custom routing rules. This personalizes RALF workflows and makes the system more adaptable to individual use cases.

## Context

**Strategic Importance:**
- **Second highest priority feature:** Score 8.0 (high value/effort ratio)
- **Quick win:** 90 minutes estimated, immediate user benefit
- **Velocity accelerator:** Second of two 90-min features that will boost feature delivery 3.35x

**Feature Context (from BACKLOG.md):**
- **User Value:** RALF operators can customize behavior
- **Problem:** Operators can't customize RALF behavior or set preferences. System uses hardcoded values.
- **Value:** Personalized workflows, configurable thresholds, custom routing rules

**Why This Task Matters:**
Different operators have different preferences. Some may want aggressive skill invocation (lower threshold), others conservative. Some may want specific task routing rules. A configuration system enables this customization without code changes.

**Dependencies:**
- TASK-1769916004 (Feature Framework) - ✅ COMPLETE (Run 48)
- TASK-1769916006 (Feature Backlog) - ✅ COMPLETE (Run 51)

## Success Criteria

- [ ] Config file created and parsed (~/.blackbox5/config.yaml)
- [ ] Preference persistence layer working
- [ ] Thresholds configurable (skill invocation, queue depth)
- [ ] Custom routing rules supported
- [ ] Default config provided
- [ ] Config validation working
- [ ] Documented in operations/.docs/config-guide.md

## Approach

### Phase 1: Feature Specification Creation (10 minutes)

**NOTE:** The feature specification file (FEATURE-006-user-preferences.md) does not exist yet. Create it first:

1. **Read the backlog entry** for F-006 from plans/features/BACKLOG.md
2. **Create feature specification** at plans/features/FEATURE-006-user-preferences.md using the template
3. **Document:**
   - User value (who benefits, what problem, what value)
   - MVP scope (config file, thresholds, routing rules)
   - Success criteria (from backlog)
   - Technical approach (YAML parsing, validation, defaults)
   - Dependencies (existing hardcoded values)
   - Rollout plan (identify hardcoded values, make configurable)
   - Risk assessment (config errors, backward compatibility)

### Phase 2: Config Schema Design (15 minutes)

**Identify hardcoded values to make configurable:**
- Skill invocation threshold (currently 70% in skill-selection.yaml)
- Queue depth target (currently 3-5 in planner logic)
- Task priority weights (if any)
- Logging levels
- Timeout values

**Design config schema:**
```yaml
# RALF Configuration
# Location: ~/.blackbox5/config.yaml

version: "1.0"

# Skill Selection
skills:
  invocation_threshold: 0.7  # 0.0 to 1.0 (default: 0.7)
  max_skills_per_task: 3     # Maximum skills to invoke per task

# Queue Management
queue:
  depth_target_min: 3        # Minimum queue depth
  depth_target_max: 5        # Maximum queue depth

# Task Routing
routing:
  custom_rules:              # Custom routing rules
    - pattern: ".*research.*"
      route_to: "analyst"
    - pattern: ".*implement.*"
      route_to: "executor"

# Logging
logging:
  level: "INFO"              # DEBUG, INFO, WARNING, ERROR
  file: "~/.blackbox5/logs/ralf.log"

# Timeouts
timeouts:
  agent_heartbeat: 120       # Seconds before agent considered dead
  task_claim: 30             # Seconds before task considered unclaimed
```

### Phase 3: Implementation (50 minutes)

**Create configuration service:**
- File: `2-engine/.autonomous/lib/config.py`
- Functions:
  - `load_config(config_path="~/.blackbox5/config.yaml")` - Load config file
  - `get_default_config()` - Return default config schema
  - `validate_config(config)` - Validate config values
  - `get_config_value(key_path)` - Get nested config value
  - `merge_with_defaults(user_config)` - Merge user config with defaults

**Create default config file:**
- File: `2-engine/.autonomous/config/default.yaml`
- Contains default values for all settings
- Well-documented (comments explain each setting)

**Integrate with existing systems:**
1. **Skill Selection:**
   - Update skill-selection.yaml logic to read threshold from config
   - Modify `get_skills_for_task()` to use configurable threshold

2. **Queue Management:**
   - Update planner logic to read queue depth targets from config
   - Modify queue depth check to use configurable values

3. **Routing:**
   - Implement custom routing rules (if pattern match, route to specific agent)

**Config initialization:**
- On first run, create default config at ~/.blackbox5/config.yaml
- If config missing, use defaults
- If config invalid, log warning and use defaults

### Phase 4: Testing (10 minutes)

**Test config loading:**
- Create test config file
- Verify load_config() parses correctly
- Check validation catches invalid values (e.g., threshold > 1.0)

**Test config integration:**
- Modify skill invocation threshold in config
- Verify skill selection uses new threshold
- Modify queue depth targets in config
- Verify planner uses new targets

**Test defaults:**
- Delete config file
- Verify system uses defaults
- Check no errors when config missing

**Test validation:**
- Create invalid config (threshold: 1.5)
- Verify validation catches error
- Check system falls back to defaults

### Phase 5: Documentation (5 minutes)

**Create user guide:**
- File: `operations/.docs/config-guide.md`
- Sections:
  - Overview (what is configurable)
  - Config file location (~/.blackbox5/config.yaml)
  - Schema reference (all settings explained)
  - Examples (common customizations)
  - Validation (what happens if config invalid)
  - Troubleshooting (config not loading, wrong values)

## Files to Modify

- `plans/features/FEATURE-006-user-preferences.md` (CREATE)
- `2-engine/.autonomous/lib/config.py` (CREATE)
- `2-engine/.autonomous/config/default.yaml` (CREATE)
- `2-engine/.autonomous/prompts/skill-selection.yaml` (MODIFY - read threshold from config)
- `2-engine/.autonomous/prompts/ralf-planner.md` (MODIFY - read queue targets from config)
- `operations/.docs/config-guide.md` (CREATE)

## Notes

**Warnings:**
- Config errors can break system if not validated properly
- Backward compatibility needed (system must work without config)
- Default values must be well-chosen (system usable out of box)

**Dependencies:**
- All feature framework tasks complete
- No external dependencies (pure Python, PyYAML)

**Integration Points:**
- skill-selection.yaml (read threshold from config)
- ralf-planner.md (read queue targets from config)
- ralf-executor.md (read routing rules from config)

**Testing Strategy:**
- Test config loading with valid/invalid/missing config
- Test integration with skill selection
- Test integration with queue management
- Verify backward compatibility (works without config)

**Risk Assessment:**
- **Risk:** Invalid config breaks system
- **Mitigation:** Strong validation, fallback to defaults
- **Risk:** Config file location varies across systems
- **Mitigation:** Support multiple locations, document clearly

**Success Indicators:**
- Config loads without errors
- Invalid config caught and logged
- System works without config (backward compatible)
- Changes to config affect behavior immediately

**Estimated Breakdown:**
- Feature spec: 10 min
- Schema design: 15 min
- Implementation: 50 min
- Testing: 10 min
- Documentation: 5 min
- **Total: 90 min**

**Priority Score:** 8.0
- Value: 8/10 (immediate user benefit, personalization)
- Effort: 1.5 hours
- Score: (8 × 10) / 1.5 = 53.3 / 6.7 ≈ 8.0
