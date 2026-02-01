# TASK-1769952152: Implement Feature F-006 (User Preference & Configuration System)

**Type:** implement (feature)
**Priority:** high
**Status:** pending
**Created:** 2026-02-01T18:30:00Z
**Estimated Minutes:** 90 (~1.5 hours)

## Objective

Implement the User Preference & Configuration System (F-006), enabling RALF operators to customize agent behavior, set configurable thresholds, and define custom routing rules. This transforms RALF from a rigid system to a personalized, user-controlled platform.

## Context

**Strategic Importance:**
- **HIGH priority feature:** Score 8.0 (second highest value/effort ratio)
- **Quick win:** 90 minutes estimated, immediate user benefit
- **Validates:** Feature delivery framework (third feature execution)

**Feature Context (from BACKLOG.md):**
- **User Value:** RALF operators can customize behavior and preferences
- **Problem:** System uses hardcoded values, no customization possible
- **Value:** Personalized workflows, configurable thresholds, custom routing rules

**Why This Task Matters:**
Different operators have different preferences. Some want aggressive automation, others prefer manual control. Some want detailed notifications, others want summaries only. A configuration system enables RALF to adapt to user needs without code changes.

**Dependencies:**
- TASK-1769916004 (Feature Framework) - ✅ COMPLETE (Run 48)
- TASK-1769916006 (Feature Backlog) - ✅ COMPLETE (Run 51)

## Success Criteria

- [ ] Configuration file created (~/.blackbox5/config.yaml)
- [ ] Preference persistence layer implemented
- [ ] Thresholds configurable (skill invocation, queue depth, etc.)
- [ ] Custom routing rules supported
- [ ] Configuration parser and validator working
- [ ] Documented in operations/.docs/configuration-guide.md
- [ ] Default configuration provided with sensible defaults

## Approach

### Phase 1: Feature Specification Creation (10 minutes)

**NOTE:** Feature specification does not exist yet. Create it first:

1. **Read the backlog entry** for F-006 from plans/features/BACKLOG.md
2. **Create feature specification** at plans/features/FEATURE-006-user-preferences.md
3. **Document:**
   - User value (who benefits, what problem, what value)
   - MVP scope (config file, threshold customization, routing rules)
   - Success criteria (from backlog)
   - Technical approach (YAML parser, config loader, validator)
   - Dependencies (existing hardcoded values)
   - Rollout plan (start with thresholds, expand to routing)
   - Risk assessment (config errors, backward compatibility)

### Phase 2: Architecture Design (15 minutes)

**Analyze current hardcoded values:**
- Skill invocation threshold: 70% (hardcoded in executor)
- Queue depth target: 3-5 tasks (hardcoded in planner)
- Loop timeout: 120 seconds (hardcoded in heartbeat)
- Notification preferences: None (all hardcoded)

**Design configuration system:**

1. **Configuration File Structure:**
   ```yaml
   # ~/.blackbox5/config.yaml
   user_preferences:
     name: "Operator Name"
     email: "operator@example.com"

   thresholds:
     skill_invocation_confidence: 70  # 0-100
     queue_depth_min: 3
     queue_depth_max: 5
     loop_timeout_seconds: 120

   routing:
     default_agent: "executor"
     task_type_routing:
       feature: "executor"
       fix: "executor"
       research: "executor"

   notifications:
     enabled: true
     on_task_completion: true
     on_error: true
     on_milestone: true
     digest: "daily"  # none, daily, weekly
   ```

2. **Configuration Loading:**
   - On startup: Read config file
   - Validation: Check values are valid (0-100, positive integers, etc.)
   - Fallback: Use defaults if config missing/invalid

3. **Configuration Access:**
   - Library function: `get_config(key, default=None)`
   - Used by: Planner, Executor, Analyst
   - Runtime updates: Support config reload without restart

**Document architecture decision:** Choose config format and loading strategy

### Phase 3: Implementation (45 minutes)

**Component 1: Configuration Library (20 min)**
- Create `2-engine/.autonomous/lib/config_manager.py`
- Implement class: `ConfigManager`
- Methods:
  - `load_config(config_path)` - loads YAML config
  - `validate_config(config_dict)` - validates values
  - `get(key, default=None)` - gets config value
  - `set(key, value)` - sets config value at runtime
  - `save_config(config_path)` - saves config to file
- Test: Load config, validate values, get/set operations

**Component 2: Configuration Integration (15 min)**
- Update executor to use config for thresholds
  - Skill invocation threshold: `config.get('thresholds.skill_invocation_confidence', 70)`
  - Loop timeout: `config.get('thresholds.loop_timeout_seconds', 120)`
- Update planner to use config for queue depth
  - Queue min: `config.get('thresholds.queue_depth_min', 3)`
  - Queue max: `config.get('thresholds.queue_depth_max', 5)`
- Test: Change config values, verify behavior changes

**Component 3: Default Configuration (10 min)**
- Create `2-engine/.autonomous/config/default.yaml`
- Include all configurable values with sensible defaults
- Document each value (purpose, valid range, impact)
- Test: System works with default config

### Phase 4: Integration (10 minutes)

**Add config loading to startup:**
- Planner loop: Load config at start
- Executor loop: Load config at start
- Analyst loop: Load config at start (if exists)

**Add config reload command:**
- SIGUSR1 handler: Reload config without restart
- Log message: "Configuration reloaded from /path/to/config.yaml"

**Test end-to-end:**
- Start without config: Uses defaults
- Start with config: Uses config values
- Modify config: Reload, verify new values used
- Invalid config: Falls back to defaults, logs error

### Phase 5: Documentation (10 minutes)

**Create `operations/.docs/configuration-guide.md`:**
1. **Overview:** What is the configuration system?
2. **Configuration File:** Where is it? What format?
3. **Configuration Options:** All keys documented
   - thresholds (skill invocation, queue depth, timeout)
   - routing (agent selection, task type routing)
   - notifications (enabled, events, digest)
4. **Examples:** Sample configurations
   - Minimal config (just thresholds)
   - Aggressive automation (low thresholds, high routing)
   - Conservative (high thresholds, manual approval)
5. **Troubleshooting:** Common issues
   - Config not loading
   - Invalid values
   - How to reset to defaults
6. **Runtime Updates:** How to reload config without restart

## Files to Modify

- `plans/features/FEATURE-006-user-preferences.md` (create) - Feature specification
- `2-engine/.autonomous/lib/config_manager.py` (create) - Configuration library
- `2-engine/.autonomous/config/default.yaml` (create) - Default configuration
- RALF-Planner integration (use config for queue depth)
- RALF-Executor integration (use config for thresholds)
- `operations/.docs/configuration-guide.md` (create) - User documentation

## Notes

**Context Level:** 2 (Moderate complexity)
- Clear scope (config file, parser, integration)
- Multiple integration points (planner, executor)
- Validation required (config errors, fallbacks)

**Skill System Validation:**
- This is a MODERATE task (context level 2)
- Expected skill invocation: POSSIBLE but not certain
- Confidence score: ~60-70% (may or may not invoke)
- **This provides additional data point for skill invocation baseline**

**Strategic Importance:**
- **HIGH priority feature** (score 8.0)
- Immediate user benefit (personalization)
- Validates feature delivery framework (third feature)
- Enables RALF to adapt to diverse user needs

**Risk Mitigation:**
- **Risk:** Invalid config breaks system
- **Mitigation:** Validation + fallback to defaults, clear error messages
- **Risk:** Too many config options (complexity)
- **Mitigation:** Start with 5-10 key values, expand based on demand
- **Risk:** Config file location unclear
- **Mitigation:** Standard location (~/.blackbox5/config.yaml), document clearly

**Dependencies:**
- TASK-1769916004 (Feature Framework) ✅ COMPLETE
- TASK-1769916006 (Feature Backlog) ✅ COMPLETE
- No technical dependencies (can start immediately)

**Expected Outcome:**
- **Immediate:** Operators can customize thresholds and behavior
- **Short-term:** Personalized workflows, reduced manual intervention
- **Long-term:** RALF adapts to diverse user needs, wider adoption

## Acceptance Criteria Validation

After completion, verify:

1. **Feature Specification Exists:**
   ```bash
   cat plans/features/FEATURE-006-user-preferences.md
   # Should show complete specification using template
   ```

2. **Configuration System Working:**
   - Config file loads from ~/.blackbox5/config.yaml
   - Invalid config falls back to defaults
   - Config values accessible via config_manager.get()
   - Runtime config reload works (SIGUSR1 or command)

3. **Thresholds Configurable:**
   - Skill invocation threshold: Configurable (0-100)
   - Queue depth min/max: Configurable
   - Loop timeout: Configurable
   - Changes in config file affect behavior

4. **Routing Rules Supported:**
   - Default agent: Configurable
   - Task type routing: Configurable
   - Custom routing logic: Supported

5. **Documentation Complete:**
   - Configuration guide exists
   - All options documented with examples
   - Troubleshooting section included

6. **Framework Validated:**
   - Feature specification template usable
   - Feature delivery process validated
   - Third feature delivered successfully ✅

## Example Task Flow

**For Executor Reference:**

1. **Read Feature Backlog:**
   ```bash
   cat plans/features/BACKLOG.md | grep -A 20 "F-006"
   ```

2. **Create Feature Specification:**
   ```bash
   # Read template
   cat .templates/tasks/feature-specification.md.template

   # Create feature spec
   # plans/features/FEATURE-006-user-preferences.md
   ```

3. **Implement Components:**
   - config_manager.py (load, validate, get/set, save)
   - default.yaml (sensible defaults)
   - Integration (planner, executor use config)

4. **Integrate and Test:**
   - Test: Load config, change values, reload config
   - Validate: Invalid config falls back to defaults
   - Verify: Behavior changes with config

5. **Document:**
   - operations/.docs/configuration-guide.md

6. **Complete:**
   - Move task to completed/
   - Write completion event
   - Update metrics dashboard

## Impact

**Immediate:**
- Third feature delivered ✅
- Feature framework validated
- Configuration system operational

**Short-Term:**
- Operators can customize RALF behavior
- Personalized workflows enabled
- Reduced manual intervention

**Long-Term:**
- RALF adapts to diverse user needs
- Wider adoption (personalization lowers barrier)
- Configurable system scales to use cases

**Milestone:**
This feature transforms RALF from a "one-size-fits-all" system to a flexible, user-controlled platform. By enabling configuration without code changes, RALF becomes accessible to a broader range of users with diverse needs and preferences.
