# FEATURE-006: User Preference & Configuration System

**Status:** active
**Priority:** high
**Type:** feature
**Estimated:** 90 minutes (~1.5 hours)

---

## User Value

**Who benefits:** RALF operators and system administrators

**What problem does it solve:** RALF currently uses hardcoded values for thresholds, timeouts, and behavior settings. Operators cannot customize agent behavior without modifying code, which creates barriers to adoption and prevents personalization.

**What value does it creates:**
- Enables personalized workflows tailored to operator preferences
- Allows threshold tuning (e.g., aggressive vs. conservative skill invocation)
- Supports custom routing rules for task distribution
- Eliminates need for code changes to customize behavior
- Lowers barrier to adoption for diverse use cases

---

## Feature Scope

**MVP (Minimum Viable Product):**
- [ ] Configuration file at ~/.blackbox5/config.yaml
- [ ] Configuration parser and validator
- [ ] Configurable thresholds (skill invocation, queue depth, timeouts)
- [ ] Default configuration with sensible defaults
- [ ] Configuration access library (get/set operations)
- [ ] Documentation for configuration options

**Future Enhancements (out of scope for this feature):**
- [ ] Per-agent configuration files
- [ ] Configuration validation web UI
- [ ] Configuration versioning and rollback
- [ ] Remote configuration management
- [ ] Configuration change notifications

**Scope Boundaries:**
- **IN SCOPE:** Single global config file, YAML format, validation, defaults, basic get/set API
- **OUT OF SCOPE:** Per-agent configs, remote config, config UI, versioning, notifications

---

## Context & Background

**Why this feature matters:**
- **Strategic:** Enables RALF to adapt to diverse user needs without code changes
- **Operational:** Reduces manual intervention (operators can tune thresholds themselves)
- **Adoption:** Lowers barrier for users with different preferences (aggressive vs. conservative automation)

**Related Features:**
- **Preceding:** F-001 (Multi-Agent Coordination) - benefits from configurable routing rules
- **Following:** F-007 (CI/CD Integration) - may need configurable quality gate thresholds

**Current State:**
- Skill invocation threshold: Hardcoded at 70% (skill-selection.yaml)
- Queue depth target: Hardcoded at 3-5 (planner logic)
- Loop timeout: Hardcoded at 120 seconds (heartbeat.yaml)
- No customization possible without code changes

**Desired State:**
- All thresholds configurable via ~/.blackbox5/config.yaml
- Invalid config falls back to defaults with error logging
- Config changes take effect on reload (SIGUSR1 or restart)
- Well-documented configuration options

---

## Success Criteria

### Must-Have (Required for completion)
- [ ] Configuration file loads from ~/.blackbox5/config.yaml
- [ ] ConfigManager library provides load, validate, get, set operations
- [ ] Default configuration provided (2-engine/.autonomous/config/default.yaml)
- [ ] Skill invocation threshold configurable (0-100)
- [ ] Queue depth targets configurable (min/max)
- [ ] Loop timeout configurable (seconds)
- [ ] Invalid config falls back to defaults without crashing
- [ ] Configuration guide documents all options

### Should-Have (Important but not blocking)
- [ ] Runtime config reload (SIGUSR1 handler or command)
- [ ] Custom routing rules (agent selection, task type routing)
- [ ] User preferences section (name, email, notification settings)

### Nice-to-Have (If time permits)
- [ ] Configuration validation with detailed error messages
- [ ] Config template generator (create config from template)
- [ ] Configuration migration tool (upgrade configs between versions)

### Verification Method
- [ ] **Manual testing:** Create invalid config, verify fallback to defaults
- [ ] **Integration testing:** Change threshold in config, verify behavior changes
- [ ] **Documentation review:** Verify all options documented with examples

---

## Technical Approach

### Implementation Plan

**Phase 1: Architecture Design (15 minutes)**
- [ ] Identify all hardcoded values in RALF system
- [ ] Design configuration schema (YAML structure)
- [ ] Define validation rules for each config value
- [ ] Specify config loading priority (user config > defaults)

**Phase 2: Configuration Library (35 minutes)**
- [ ] Create ConfigManager class (load, validate, get, set, save)
- [ ] Implement validation logic (type checking, range validation)
- [ ] Add fallback to defaults when config missing/invalid
- [ ] Support nested key access (e.g., "thresholds.skill_invocation")

**Phase 3: Default Configuration (10 minutes)**
- [ ] Create default.yaml with all configurable values
- [ ] Document each value (purpose, valid range, impact)
- [ ] Set sensible defaults (match current hardcoded values)

**Phase 4: Integration (20 minutes)**
- [ ] Update executor to use config for skill invocation threshold
- [ ] Update planner to use config for queue depth targets
- [ ] Update heartbeat to use config for timeout values
- [ ] Test: Change config values, verify behavior changes

**Phase 5: Documentation (10 minutes)**
- [ ] Create configuration guide (operations/.docs/configuration-guide.md)
- [ ] Document all options with examples
- [ ] Add troubleshooting section

### Architecture & Design

**Key Components:**

1. **ConfigManager Class** (`2-engine/.autonomous/lib/config_manager.py`)
   - `load_config(config_path)` - Load YAML config file
   - `validate_config(config_dict)` - Validate config values
   - `get(key_path, default=None)` - Get nested config value
   - `set(key_path, value)` - Set config value at runtime
   - `save_config(config_path)` - Save config to file
   - `reload_config()` - Reload config from file

2. **Default Configuration** (`2-engine/.autonomous/config/default.yaml`)
   - Contains all configurable values with defaults
   - Well-documented (comments explain each setting)
   - Used as fallback when user config missing/invalid

3. **Configuration File** (`~/.blackbox5/config.yaml`)
   - User-provided configuration (optional)
   - Overrides default values
   - Validated on load

**Integration Points:**
- **RALF-Executor:** Read skill invocation threshold from config
- **RALF-Planner:** Read queue depth targets from config
- **RALF-Heartbeat:** Read timeout values from config

**Data Flow:**
```
User Config (~/.blackbox5/config.yaml)
    ↓ (if missing/invalid)
Default Config (2-engine/.autonomous/config/default.yaml)
    ↓ (merged)
ConfigManager (validated config in memory)
    ↓ (get operations)
RALF Components (executor, planner, heartbeat)
```

---

## Dependencies

### Requires (Prerequisites)
- [ ] TASK-1769916004 (Feature Framework) - ✅ COMPLETE (Run 48)
- [ ] TASK-1769916006 (Feature Backlog) - ✅ COMPLETE (Run 51)

### Blocks (Dependents)
- [F-007 (CI/CD Integration)]: May need configurable quality gate thresholds
- [Future features]: May need additional config options

### External Dependencies
- [ ] PyYAML: Python YAML library (already in standard library)
- [ ] No external dependencies required

---

## Rollout Plan

### Testing Strategy

**Unit Tests:**
- [ConfigManager.load_config]: Load valid YAML, missing file, invalid YAML
- [ConfigManager.validate_config]: Valid values, invalid values (out of range, wrong type)
- [ConfigManager.get]: Nested key access, missing keys, default values
- [ConfigManager.set]: Set value at runtime, persist to file

**Integration Tests:**
- [Executor integration]: Change skill threshold in config, verify skill selection changes
- [Planner integration]: Change queue depth targets, verify planner respects new limits
- [Fallback behavior]: Delete config file, verify system uses defaults

**User Acceptance Tests:**
- [Create custom config]: User creates config file, customizes threshold
- [Invalid config handling]: User provides invalid config, system falls back to defaults
- [Runtime reload]: User modifies config, triggers reload, behavior changes

### Deployment Strategy
- **Deployment Method:** Progressive rollout (no breaking changes)
- **Rollback Plan:** Delete config file, system uses hardcoded defaults
- **Monitoring:** Track config load errors, fallback rate, config reloads

---

## Files to Modify

### New Files (Create)
- `plans/features/FEATURE-006-user-preferences.md` (this file)
- `2-engine/.autonomous/lib/config_manager.py` (Configuration library)
- `2-engine/.autonomous/config/default.yaml` (Default configuration)
- `operations/.docs/configuration-guide.md` (User guide)

### Existing Files (Modify)
- `2-engine/.autonomous/prompts/ralf-executor.md` (Use config for thresholds)
- `2-engine/.autonomous/prompts/ralf-planner.md` (Use config for queue depth)
- `.autonomous/communications/heartbeat.yaml` (Use config for timeout - future)

---

## Risk Assessment

### Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Invalid config breaks system | High | Medium | Strong validation, fallback to defaults, error logging |
| Config file location varies | Medium | Low | Support multiple locations, document clearly |
| Too many config options | Medium | Medium | Start with 5-10 key values, expand based on demand |
| Config conflicts (old vs new) | Low | Low | Version field in config, migration guide |

### Operational Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Users don't know about config | Low | Medium | Document prominently in README, guide |
| Config errors hard to debug | Medium | Medium | Detailed error messages, validation errors |
| Config changes lost on update | Low | Low | Document config location, don't overwrite user configs |

---

## Effort Estimation

**Estimated Breakdown:**
- Design: 15 minutes (architecture, schema, validation rules)
- Implementation: 35 minutes (ConfigManager library, validation)
- Default config: 10 minutes (create default.yaml with documentation)
- Integration: 20 minutes (update executor, planner, heartbeat)
- Testing: 10 minutes (unit tests, integration tests)
- Documentation: 10 minutes (configuration guide)
- **Total:** 90 minutes (~1.5 hours)

**Complexity Factors:**
- [x] Integration complexity (medium) - Multiple integration points
- [x] Technical uncertainty (low) - Well-understood problem (config management)
- [ ] Dependencies (low) - No external dependencies

---

## Dates

**Created:** 2026-02-01
**Started:** 2026-02-01
**Completed:** TBD

---

## Notes

**Strategic Value:**
- Transforms RALF from "one-size-fits-all" to flexible, user-controlled platform
- Enables personalization without code changes
- Lowers barrier to adoption for diverse use cases
- Foundation for future enhancements (per-agent configs, remote config)

**Success Metrics:**
- **Adoption:** % of operators with custom config (target: >20% within 1 month)
- **Reliability:** Config load error rate (target: <1%)
- **Usability:** Time to create custom config (target: <5 minutes)

**Open Questions:**
- [Config reload mechanism]: Should we use SIGUSR1 or explicit command? → Decision: Start with explicit command, add SIGUSR1 if demand exists
- [Per-agent configs]: Should agents have separate config files? → Decision: No, single global config for MVP

**Learnings (to be filled after completion):**
- [What went well]
- [What could be improved]
- [Recommendations for future features]
