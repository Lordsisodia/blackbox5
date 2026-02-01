# RALF Configuration Guide

**Feature:** F-006 (User Preference & Configuration System)
**Version:** 1.0.0
**Status:** Active

---

## Overview

RALF (Recursive Autonomous Learning Framework) now supports **user-configurable preferences** via a YAML configuration file. This allows you to customize agent behavior, thresholds, and routing rules **without modifying code**.

### What's Configurable

- **Skill Invocation Threshold:** Control when RALF invokes BMAD skills (default: 70%)
- **Queue Depth Targets:** Set minimum/maximum queue size for task planning (default: 3-5)
- **Loop Timeout:** Configure agent inactivity timeout (default: 120 seconds)
- **Task Routing:** Define which agent handles specific task types
- **Notifications:** Enable/disable notifications for various events

---

## Configuration File Locations

RALF uses a **two-tier configuration system**:

1. **User Configuration:** `~/.blackbox5/config.yaml` (optional, overrides defaults)
2. **Default Configuration:** `2-engine/.autonomous/config/default.yaml` (built-in defaults)

### Configuration Hierarchy

```
User Config (~/.blackbox5/config.yaml)
         ↓ (overrides)
Default Config (2-engine/.autonomous/config/default.yaml)
         ↓ (fallback)
Built-in Defaults (hardcoded in config_manager.py)
```

**How it works:**
- If user config exists → Use user values, fall back to defaults for missing keys
- If user config missing → Use all defaults
- If user config invalid → Fall back to defaults, log error

---

## Quick Start

### Step 1: Create User Configuration File

```bash
# Create config directory (if it doesn't exist)
mkdir -p ~/.blackbox5

# Copy default config to user config location
cp 2-engine/.autonomous/config/default.yaml ~/.blackbox5/config.yaml
```

### Step 2: Customize Values

Edit `~/.blackbox5/config.yaml`:

```yaml
thresholds:
  skill_invocation_confidence: 80  # More conservative (was 70)
  queue_depth_min: 2               # Smaller queue (was 3)
  queue_depth_max: 8               # Larger queue (was 5)

routing:
  default_agent: "executor"        # Unchanged
```

### Step 3: Verify Configuration

```bash
# Test configuration loading
python3 2-engine/.autonomous/lib/config_manager.py

# Expected output:
# Skill invocation threshold: 80
# Queue depth target: 2-8
# Default agent: executor
```

---

## Configuration Options

### Thresholds

Control when RALF takes certain actions.

#### skill_invocation_confidence (0-100)

**Purpose:** Minimum confidence score required to invoke a BMAD skill

**Range:** 0 (always invoke) to 100 (never invoke)

**Default:** 70 (balanced)

**Impact:**
- **Lower value (e.g., 60):** More aggressive skill invocation
  - ✅ Good for exploration, discovering new skills
  - ⚠️ May invoke inappropriate skills (false positives)
- **Higher value (e.g., 80):** More conservative skill invocation
  - ✅ Reduces false positives, only invokes high-confidence skills
  - ⚠️ May miss useful skills (false negatives)

**Example:**

```yaml
thresholds:
  skill_invocation_confidence: 60  # More aggressive exploration
```

#### queue_depth_min (0-10)

**Purpose:** Minimum number of tasks to keep in the planning queue

**Range:** 0 (no minimum) to 10 (maintain at least 10 tasks)

**Default:** 3 (maintain healthy queue)

**Impact:**
- **Lower value (e.g., 1):** Less proactive task generation
  - ✅ Focuses on immediate work, less overhead
  - ⚠️ May run out of tasks, requires frequent planning
- **Higher value (e.g., 5):** More proactive task generation
  - ✅ Queue always stocked, smooth workflow
  - ⚠️ More planning overhead, may include lower-priority work

**Example:**

```yaml
thresholds:
  queue_depth_min: 5  # Keep queue well-stocked
  queue_depth_max: 10  # Allow larger queue
```

#### queue_depth_max (0-20)

**Purpose:** Maximum number of tasks to keep in the planning queue

**Range:** 0 (no limit) to 20 (cap at 20 tasks)

**Default:** 5 (prevent queue overflow)

**Constraint:** Must be >= `queue_depth_min`

**Impact:**
- **Lower value (e.g., 3):** Smaller queue
  - ✅ Focus on current work, less planning ahead
  - ⚠️ May need frequent replanning
- **Higher value (e.g., 10):** Larger queue
  - ✅ Plans ahead, includes future work
  - ⚠️ May include lower-priority tasks

#### loop_timeout_seconds (30-600)

**Purpose:** Seconds before an agent is considered inactive/unresponsive

**Range:** 30 (30 seconds) to 600 (10 minutes)

**Default:** 120 (2 minutes)

**Impact:**
- **Lower value (e.g., 60):** Faster timeout detection
  - ✅ Quickly detects dead agents
  - ⚠️ May falsely flag slow agents as dead
- **Higher value (e.g., 300):** Slower timeout detection
  - ✅ Allows longer-running tasks
  - ⚠️ Slower to detect actual dead agents

**Example:**

```yaml
thresholds:
  loop_timeout_seconds: 180  # 3 minutes (for slow tasks)
```

---

### Routing

Control how tasks are routed to agents.

#### default_agent

**Purpose:** Default agent to handle tasks when no specific routing rule matches

**Valid values:** `"executor"`, `"planner"`, `"analyst"`

**Default:** `"executor"`

**Impact:** Determines which agent handles tasks by default

**Example:**

```yaml
routing:
  default_agent: "executor"  # Most tasks are execution tasks
```

#### task_type_routing

**Purpose:** Route specific task types to specific agents

**Format:** Map of task type → agent name

**Impact:** Overrides `default_agent` for matching task types

**Valid task types:** `feature`, `fix`, `research`, `refactor`, `analyze`, `organize`, `improve`

**Example:**

```yaml
routing:
  default_agent: "executor"
  task_type_routing:
    feature: "executor"     # Feature implementation → executor
    fix: "executor"         # Bug fixes → executor
    research: "executor"    # Research → executor (can be changed to "analyst")
    analyze: "executor"     # Analysis → executor (can be changed to "analyst")
```

---

### Notifications

Control when and how RALF sends notifications (currently foundational, future expansion planned).

#### enabled

**Purpose:** Master switch for notifications

**Valid values:** `true` (enabled), `false` (disabled)

**Default:** `false` (notifications disabled by default)

**Impact:** When `false`, no notifications are sent regardless of other settings

**Example:**

```yaml
notifications:
  enabled: true  # Enable notifications
  on_task_completion: true  # Notify when tasks complete
  on_error: true  # Notify on errors
  on_milestone: false  # Don't notify on milestones
```

---

## Configuration Validation

RALF automatically validates configuration on load. Invalid values trigger fallback to defaults.

### Validation Rules

| Setting | Validation Rule | Invalid Example | Fallback |
|---------|----------------|-----------------|----------|
| `skill_invocation_confidence` | Must be 0-100 | `150` | Use default (70) |
| `queue_depth_min` | Must be >= 0 | `-1` | Use default (3) |
| `queue_depth_max` | Must be >= min | `2` when min is `5` | Use default (5) |
| `loop_timeout_seconds` | Must be >= 0 | `-10` | Use default (120) |
| `default_agent` | Must be valid agent | `"invalid"` | Use default ("executor") |

### What Happens on Invalid Config?

1. RALF logs an error: `Configuration validation failed: [reason]. Using defaults.`
2. Invalid values are ignored, defaults are used
3. Valid values are still applied
4. RALF continues operating normally

**Example:**

```yaml
# Invalid config
thresholds:
  skill_invocation_confidence: 150  # Invalid (> 100)
  queue_depth_min: 2                # Valid
```

**Result:**
- `skill_invocation_confidence`: Falls back to default (70)
- `queue_depth_min`: Uses user value (2)
- RALF logs error but continues operating

---

## Runtime Configuration Access

### Python API

```python
import sys
sys.path.insert(0, '2-engine/.autonomous/lib')
from config_manager import get_config

# Get configuration instance
config = get_config()

# Access configuration values
threshold = config.get('thresholds.skill_invocation_confidence')
print(f"Skill invocation threshold: {threshold}")

# Get nested value with default
agent = config.get('routing.default_agent', 'executor')
print(f"Default agent: {agent}")

# Set value at runtime (not persisted)
config.set('thresholds.skill_invocation_confidence', 80)

# Reload configuration from file
config.reload_config()

# Save current configuration to file
config.save_config('~/.blackbox5/config.yaml')
```

### Bash API

```bash
# Get skill invocation threshold
CONFIG_FILE="$HOME/.blackbox5/config.yaml"
DEFAULT_CONFIG="2-engine/.autonomous/config/default.yaml"

THRESHOLD=$(python3 -c "
import sys
sys.path.insert(0, '2-engine/.autonomous/lib')
from config_manager import get_config
config = get_config('$CONFIG_FILE', '$DEFAULT_CONFIG')
print(config.get('thresholds.skill_invocation_confidence', 70))
")

echo "Skill invocation threshold: ${THRESHOLD}%"
```

---

## Common Configuration Patterns

### Pattern 1: Aggressive Automation

For users who want RALF to be more proactive:

```yaml
thresholds:
  skill_invocation_confidence: 60  # Lower threshold = more skills
  queue_depth_min: 5               # Keep queue well-stocked
  queue_depth_max: 10              # Allow more planning ahead

routing:
  default_agent: "executor"        # Execute tasks immediately
```

**Result:** More skill usage, proactive planning, immediate execution

---

### Pattern 2: Conservative Control

For users who want careful, deliberate automation:

```yaml
thresholds:
  skill_invocation_confidence: 80  # Higher threshold = fewer skills
  queue_depth_min: 2               # Smaller queue
  queue_depth_max: 4               # Focus on current work

routing:
  default_agent: "executor"        # Still execute tasks
```

**Result:** Selective skill usage, focused queue, deliberate execution

---

### Pattern 3: Balanced Default

The default configuration (recommended for most users):

```yaml
thresholds:
  skill_invocation_confidence: 70  # Balanced threshold
  queue_depth_min: 3               # Healthy queue
  queue_depth_max: 5               # Reasonable lookahead

routing:
  default_agent: "executor"
```

**Result:** Balanced automation, good for most use cases

---

## Troubleshooting

### Issue: Configuration Not Loading

**Symptoms:** RALF ignores your config file, uses defaults

**Solutions:**
1. Check file path: `ls -la ~/.blackbox5/config.yaml`
2. Check YAML syntax: `python3 -c "import yaml; yaml.safe_load(open('~/.blackbox5/config.yaml'))"`
3. Check file permissions: `chmod 644 ~/.blackbox5/config.yaml`
4. Check logs for validation errors

---

### Issue: Invalid Configuration

**Symptoms:** RALF logs "Configuration validation failed"

**Solutions:**
1. Check value ranges (e.g., confidence must be 0-100)
2. Check data types (e.g., queue depth must be integer, not string)
3. Check constraints (e.g., queue_depth_max must be >= queue_depth_min)
4. Fix invalid values, reload config

---

### Issue: How Do I Know My Config Is Being Used?

**Verification:**

```bash
# Test configuration loading
python3 2-engine/.autonomous/lib/config_manager.py

# Expected output shows your custom values, not defaults
```

If you see default values (70, 3-5, executor), your config is not being loaded.

---

### Issue: How Do I Reset to Defaults?

**Solution:** Delete or rename your config file:

```bash
# Backup current config
mv ~/.blackbox5/config.yaml ~/.blackbox5/config.yaml.backup

# RALF will use defaults
# To restore: mv ~/.blackbox5/config.yaml.backup ~/.blackbox5/config.yaml
```

---

## Advanced Usage

### Per-Agent Configuration (Future)

Not currently supported, but planned for future enhancement:

```yaml
# Future feature (not yet implemented)
advanced:
  per_agent_config:
    executor:
      thresholds:
        skill_invocation_confidence: 70
    planner:
      thresholds:
        skill_invocation_confidence: 80
```

### Configuration Reload Trigger (Future)

Currently, config reload requires manual trigger. Future versions may support:

```yaml
# Future feature (not yet implemented)
advanced:
  config_reload_trigger: "signal"  # SIGUSR1 to reload
```

---

## FAQ

### Q: Do I need to create a config file?

**A:** No. RALF works fine with defaults. Create a config file only if you want to customize behavior.

---

### Q: Can I break RALF with a bad config?

**A:** No. Invalid config falls back to defaults with error logging. RALF continues operating.

---

### Q: How do I know what values to set?

**A:** Start with defaults, then adjust gradually. Monitor behavior after each change.

---

### Q: Can I change config while RALF is running?

**A:** Yes, but changes won't take effect until RALF reloads config (currently requires restart). Future versions will support runtime reload.

---

### Q: Where can I find the default configuration?

**A:** `2-engine/.autonomous/config/default.yaml` - contains all configurable values with documentation.

---

## Related Documentation

- **Feature Specification:** `plans/features/FEATURE-006-user-preferences.md`
- **Configuration Manager:** `2-engine/.autonomous/lib/config_manager.py`
- **Default Config:** `2-engine/.autonomous/config/default.yaml`
- **Executor Prompt:** `2-engine/.autonomous/prompts/ralf-executor.md`

---

## Changelog

### Version 1.0.0 (2026-02-01)
- Initial configuration system
- Configurable thresholds (skill invocation, queue depth, timeout)
- Configurable routing (default agent, task type routing)
- Notification settings (foundational)
- Configuration validation and fallback
- User guide documentation

---

## Support

For issues or questions:
1. Check this guide's troubleshooting section
2. Review logs for configuration errors
3. Verify config file syntax and values
4. Test with `python3 2-engine/.autonomous/lib/config_manager.py`

---

**End of Configuration Guide**
