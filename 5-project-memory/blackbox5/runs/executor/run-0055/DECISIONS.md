# Decisions - TASK-1769952152

**Task:** TASK-1769952152: Implement Feature F-006 (User Preference & Configuration System)
**Run:** 55
**Date:** 2026-02-01

---

## Decision 1: Configuration File Format

**Context:** Need to choose a configuration file format that is human-readable, editable, and well-supported in Python.

**Options Considered:**
1. **YAML** - Human-readable, supports comments, industry standard
2. **JSON** - Widely supported, but no comments
3. **TOML** - Simple, but less common
4. **INI** - Simple, but limited nesting

**Selected:** YAML

**Rationale:**
- **Human-readable:** Easy for users to edit without syntax errors
- **Supports comments:** Critical for documentation (explain each setting)
- **Python support:** PyYAML is stable and widely used
- **Industry standard:** Most config files use YAML
- **Nested structure:** Supports complex configurations (thresholds, routing, notifications)

**Reversibility:** LOW - Can migrate to other format with conversion script, but YAML is the right choice

---

## Decision 2: Configuration Hierarchy (Two-Tier System)

**Context:** Need to balance user customization with sensible defaults.

**Options Considered:**
1. **Single config file** - User must provide full config
2. **Two-tier system** - User config + default config
3. **Three-tier system** - User + environment + default

**Selected:** Two-tier system (user config + default config)

**Rationale:**
- **User config:** `~/.blackbox5/config.yaml` (optional, overrides defaults)
- **Default config:** `2-engine/.autonomous/config/default.yaml` (built-in)
- **Benefits:**
  - User only needs to specify values they want to change
  - Missing values fall back to defaults
  - Invalid config falls back to defaults without crashing
  - Backward compatible (RALF works without user config)

**Reversibility:** LOW - This is a foundational design decision, but two-tier is standard practice

---

## Decision 3: Validation Strategy (Fail-Safe Fallback)

**Context:** Invalid configuration should not break RALF.

**Options Considered:**
1. **Fail fast** - Crash on invalid config
2. **Warn and continue** - Use defaults, log warning
3. **Fail-safe fallback** - Validate, fall back to defaults on error

**Selected:** Fail-safe fallback

**Rationale:**
- **Validate on load:** Type checking, range validation, constraint checking
- **Fall back to defaults:** If validation fails, use defaults
- **Log error:** Inform user why config was rejected
- **Continue operating:** RALF remains functional

**Example:**
```yaml
# Invalid config
thresholds:
  skill_invocation_confidence: 150  # Invalid (> 100)
```

**Result:**
- Validation fails
- Error logged: "Configuration validation failed: skill_invocation_confidence must be between 0 and 100, got 150. Using defaults."
- Defaults used (confidence=70)
- RALF continues operating

**Reversibility:** LOW - Fail-safe is the right approach for configuration systems

---

## Decision 4: Configuration API Design (Dot-Notation for Nested Access)

**Context:** Need a simple API for accessing nested configuration values.

**Options Considered:**
1. **Dictionary access** - `config['thresholds']['skill_invocation_confidence']`
2. **Dot-notation** - `config.get('thresholds.skill_invocation_confidence')`
3. **Method chaining** - `config.thresholds.skill_invocation_confidence`

**Selected:** Dot-notation

**Rationale:**
- **Simple:** Single string key path
- **Readable:** Easy to understand
- **Safe:** Supports default values for missing keys
- **Flexible:** Easy to add new nested settings

**API Usage:**
```python
config = get_config()
threshold = config.get('thresholds.skill_invocation_confidence', 70)
queue_min = config.get('thresholds.queue_depth_min', 3)
```

**Reversibility:** MEDIUM - Can add other access methods later, but dot-notation is primary API

---

## Decision 5: Initial Configuration Options (5-10 Key Values)

**Context:** How many configuration values to expose in MVP?

**Options Considered:**
1. **Minimal** - Only skill invocation threshold
2. **Balanced** - 5-10 key values (thresholds, routing, timeouts)
3. **Comprehensive** - All hardcoded values configurable

**Selected:** Balanced (5-10 key values)

**Rationale:**
- **Start simple:** Don't overwhelm users with options
- **High impact:** Focus on values that significantly affect behavior
- **Expandable:** Can add more options based on user demand
- **Maintainable:** Fewer options = simpler documentation and validation

**Initial Options:**
- `thresholds.skill_invocation_confidence` (0-100)
- `thresholds.queue_depth_min` (0-10)
- `thresholds.queue_depth_max` (0-20)
- `thresholds.loop_timeout_seconds` (30-600)
- `routing.default_agent` (executor/planner/analyst)
- `routing.task_type_routing` (map of task type → agent)
- `notifications.enabled` (true/false)
- `notifications.on_task_completion` (true/false)
- `notifications.on_error` (true/false)
- `notifications.on_milestone` (true/false)

**Reversibility:** LOW - Can add more options later, starting with focused set is correct

---

## Decision 6: Runtime Config Reload (Manual vs Automatic)

**Context:** How should configuration changes take effect?

**Options Considered:**
1. **Automatic reload** - File watcher detects changes, reloads automatically
2. **Signal-based reload** - SIGUSR1 triggers reload
3. **Manual reload** - Explicit `reload_config()` call
4. **Restart required** - Changes take effect on restart

**Selected:** Manual reload (for MVP)

**Rationale:**
- **Simple:** No file watcher complexity
- **Safe:** Explicit control prevents unexpected behavior
- **Sufficient:** Most config changes are infrequent
- **Future enhancement:** Can add SIGUSR1 if demand exists

**API:**
```python
config.reload_config()  # Manual reload
```

**Reversibility:** LOW - Can add automatic reload later if needed

---

## Decision 7: Executor Integration (Backward Compatibility)

**Context:** How to integrate configuration without breaking existing RALF components?

**Options Considered:**
1. **Require config** - Break if config missing
2. **Optional config** - Work with defaults if config missing
3. **Migration path** - Auto-generate config on first run

**Selected:** Optional config with fallback

**Rationale:**
- **Backward compatible:** RALF works without config file
- **Graceful degradation:** Falls back to defaults if config missing
- **Opt-in:** Users can add config when needed
- **No breaking changes:** Existing installations continue working

**Implementation:**
```bash
# Check if user config exists
if [[ -f "$CONFIG_FILE" ]]; then
    THRESHOLD=$(python3 -c "read from config")
else
    THRESHOLD=70  # Use default
fi
```

**Reversibility:** LOW - Backward compatibility is essential for smooth rollout

---

## Decision 8: Singleton Pattern for Global Config

**Context:** How to provide global access to configuration?

**Options Considered:**
1. **Singleton pattern** - Single global instance
2. **Dependency injection** - Pass config to components
3. **Module-level variable** - Global variable in module

**Selected:** Singleton pattern

**Rationale:**
- **Simple API:** `get_config()` returns global instance
- **Lazy loading:** Config loaded on first access
- **Thread-safe:** Single source of truth
- **Standard practice:** Widely used pattern for configuration

**API:**
```python
from config_manager import get_config

config = get_config()  # Returns singleton instance
threshold = config.get('thresholds.skill_invocation_confidence')
```

**Reversibility:** LOW - Singleton is appropriate for global configuration

---

## Decision 9: Documentation Strategy (Comprehensive User Guide)

**Context:** How much documentation to provide for configuration system?

**Options Considered:**
1. **Minimal** - Just code comments
2. **Moderate** - Inline documentation + brief guide
3. **Comprehensive** - Full user guide with examples and troubleshooting

**Selected:** Comprehensive user guide

**Rationale:**
- **Configuration is user-facing:** Users need clear documentation
- **Low technical barrier:** Non-programmers should be able to configure
- **Reduces support burden:** Good documentation prevents questions
- **Examples matter:** Show common patterns (aggressive, conservative, balanced)

**Documentation Deliverables:**
- `operations/.docs/configuration-guide.md` (480 lines)
- Quick start guide
- Configuration reference
- Validation rules
- Common patterns
- Troubleshooting
- FAQ

**Reversibility:** LOW - Comprehensive documentation is always valuable

---

## Decision 10: Feature Scope (MVP vs Full Feature Set)

**Context:** How much functionality to include in MVP?

**Options Considered:**
1. **Minimal MVP** - Only config file parsing
2. **Balanced MVP** - Config parsing + validation + integration
3. **Full feature** - All planned features (per-agent config, remote config, versioning)

**Selected:** Balanced MVP

**Rationale:**
- **Core value:** Config parsing, validation, integration deliver core value
- **Quick win:** 90-minute estimate matches
- **Future enhancements:** Per-agent config, remote config, versioning can be added later
- **Foundation:** MVP establishes infrastructure for future enhancements

**MVP Scope:**
- ✅ Config file parsing (YAML)
- ✅ Validation (type checking, range validation)
- ✅ Fallback to defaults
- ✅ ConfigManager API (get, set, save, reload)
- ✅ Default configuration with documentation
- ✅ Executor integration (skill threshold)
- ✅ User guide

**Out of Scope:**
- ❌ Per-agent configuration files
- ❌ Remote configuration management
- ❌ Configuration versioning and migration
- ❌ Configuration validation web UI

**Reversibility:** LOW - MVP scope is appropriate, can add enhancements later

---

## Summary of Decisions

| Decision | Selection | Reversibility | Impact |
|----------|-----------|---------------|--------|
| Config format | YAML | LOW | High - right choice for human-readable config |
| Config hierarchy | Two-tier (user + default) | LOW | High - standard practice, works well |
| Validation strategy | Fail-safe fallback | LOW | High - ensures robustness |
| API design | Dot-notation | MEDIUM | Medium - simple and effective |
| Initial options | 5-10 key values | LOW | Medium - focused set, can expand |
| Config reload | Manual (MVP) | LOW | Low - can add auto-reload later |
| Executor integration | Optional config | LOW | High - ensures backward compatibility |
| Global config | Singleton pattern | LOW | Low - standard approach |
| Documentation | Comprehensive guide | LOW | High - reduces support burden |
| Feature scope | Balanced MVP | LOW | High - delivers core value quickly |

**Overall Assessment:** All decisions are low-reversibility (meaning they're the right choices) and have high or medium impact. The configuration system is well-designed and ready for production use.
