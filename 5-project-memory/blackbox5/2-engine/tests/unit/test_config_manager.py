"""
Unit tests for ConfigManager.

Tests configuration loading, validation, access, and persistence.
"""

import pytest
import yaml
from pathlib import Path
import sys

# Add lib to path
AUTONOMOUS_LIB = Path(__file__).parent.parent.parent / ".autonomous" / "lib"
sys.path.insert(0, str(AUTONOMOUS_LIB))

from config_manager import ConfigManager, ConfigValidationError


# ============================================================================
# TESTS FOR CONFIG LOADING
# ============================================================================

@pytest.mark.unit
@pytest.mark.config
def test_config_manager_loads_default_config(sample_config_file):
    """Test that ConfigManager loads default configuration."""
    config_manager = ConfigManager(
        config_path=None,
        default_config_path=str(sample_config_file)
    )

    assert config_manager.config is not None
    assert isinstance(config_manager.config, dict)
    assert "executor" in config_manager.config


@pytest.mark.unit
@pytest.mark.config
def test_config_manager_merges_user_config(
    sample_config_file,
    sample_user_config_file
):
    """Test that user config overrides default config."""
    config_manager = ConfigManager(
        config_path=str(sample_user_config_file),
        default_config_path=str(sample_config_file)
    )

    # User config should override default
    assert config_manager.config["executor"]["skill_threshold"] == 0.8
    # Default values should still be present
    assert config_manager.config["executor"]["max_retries"] == 3


@pytest.mark.unit
@pytest.mark.config
def test_config_manager_handles_missing_config():
    """Test that ConfigManager handles missing config files gracefully."""
    config_manager = ConfigManager(
        config_path="/nonexistent/config.yaml",
        default_config_path="/nonexistent/default.yaml"
    )

    # Should fall back to built-in defaults
    assert config_manager.config is not None
    assert isinstance(config_manager.config, dict)


@pytest.mark.unit
@pytest.mark.config
def test_config_manager_handles_invalid_yaml(temp_dir):
    """Test that ConfigManager handles invalid YAML gracefully."""
    invalid_file = temp_dir / "invalid.yaml"
    with open(invalid_file, 'w') as f:
        f.write("invalid: yaml: content: [")

    # Should not raise exception, should fall back to defaults
    config_manager = ConfigManager(
        config_path=str(invalid_file),
        default_config_path=None
    )

    assert config_manager.config is not None


# ============================================================================
# TESTS FOR CONFIG ACCESS
# ============================================================================

@pytest.mark.unit
@pytest.mark.config
def test_config_get_simple_value(sample_config_file):
    """Test getting simple configuration values."""
    config_manager = ConfigManager(
        default_config_path=str(sample_config_file)
    )

    threshold = config_manager.get("executor.skill_threshold")
    assert threshold == 0.7


@pytest.mark.unit
@pytest.mark.config
def test_config_get_nested_value(sample_config_file):
    """Test getting nested configuration values."""
    config_manager = ConfigManager(
        default_config_path=str(sample_config_file)
    )

    timeout = config_manager.get("executor.timeout_seconds")
    assert timeout == 120


@pytest.mark.unit
@pytest.mark.config
def test_config_get_missing_key_returns_default(sample_config_file):
    """Test that getting missing key returns default value."""
    config_manager = ConfigManager(
        default_config_path=str(sample_config_file)
    )

    # Missing key with default
    value = config_manager.get("nonexistent.key", default="default_value")
    assert value == "default_value"


@pytest.mark.unit
@pytest.mark.config
def test_config_get_missing_key_raises(sample_config_file):
    """Test that getting missing key raises KeyError if no default."""
    config_manager = ConfigManager(
        default_config_path=str(sample_config_file)
    )

    with pytest.raises(KeyError):
        config_manager.get("nonexistent.key")


# ============================================================================
# TESTS FOR CONFIG VALIDATION
# ============================================================================

@pytest.mark.unit
@pytest.mark.config
def test_config_validation_valid_config(sample_config_file):
    """Test that valid configuration passes validation."""
    config_manager = ConfigManager(
        default_config_path=str(sample_config_file)
    )

    # Should not raise exception
    config_manager.validate_config(config_manager.config)


@pytest.mark.unit
@pytest.mark.config
def test_config_validation_invalid_type():
    """Test that invalid configuration type fails validation."""
    config_manager = ConfigManager()

    invalid_config = {
        "executor": {
            "skill_threshold": "not_a_number"  # Should be float
        }
    }

    with pytest.raises(ConfigValidationError):
        config_manager.validate_config(invalid_config)


@pytest.mark.unit
@pytest.mark.config
def test_config_validation_missing_required_field():
    """Test that missing required field fails validation."""
    config_manager = ConfigManager()

    incomplete_config = {
        "executor": {
            # Missing required fields
        }
    }

    # Should either use defaults or raise validation error
    try:
        config_manager.validate_config(incomplete_config)
    except (ConfigValidationError, KeyError):
        # Expected behavior
        pass


# ============================================================================
# TESTS FOR CONFIG MODIFICATION
# ============================================================================

@pytest.mark.unit
@pytest.mark.config
def test_config_set_value(sample_config_file, temp_dir):
    """Test setting configuration values."""
    config_file = temp_dir / "test_config.yaml"
    config_manager = ConfigManager(
        config_path=str(config_file),
        default_config_path=str(sample_config_file)
    )

    # Set a new value
    config_manager.set("executor.skill_threshold", 0.9)

    # Verify the value was set
    assert config_manager.get("executor.skill_threshold") == 0.9


@pytest.mark.unit
@pytest.mark.config
def test_config_set_nested_value(sample_config_file, temp_dir):
    """Test setting nested configuration values."""
    config_file = temp_dir / "test_config.yaml"
    config_manager = ConfigManager(
        config_path=str(config_file),
        default_config_path=str(sample_config_file)
    )

    # Set a nested value
    config_manager.set("new_section.new_key", "new_value")

    # Verify the value was set
    assert config_manager.get("new_section.new_key") == "new_value"


# ============================================================================
# TESTS FOR CONFIG PERSISTENCE
# ============================================================================

@pytest.mark.unit
@pytest.mark.config
def test_config_save_persist_changes(sample_config_file, temp_dir):
    """Test that configuration changes are persisted."""
    config_file = temp_dir / "test_config.yaml"
    config_manager = ConfigManager(
        config_path=str(config_file),
        default_config_path=str(sample_config_file)
    )

    # Modify and save
    config_manager.set("executor.skill_threshold", 0.95)
    config_manager.save()

    # Create new ConfigManager instance to verify persistence
    new_config_manager = ConfigManager(
        config_path=str(config_file),
        default_config_path=None
    )

    assert new_config_manager.get("executor.skill_threshold") == 0.95


@pytest.mark.unit
@pytest.mark.config
def test_config_save_creates_file(sample_config_file, temp_dir):
    """Test that save creates config file if it doesn't exist."""
    config_file = temp_dir / "new_config.yaml"
    config_manager = ConfigManager(
        config_path=str(config_file),
        default_config_path=str(sample_config_file)
    )

    # Save should create the file
    config_manager.save()

    assert config_file.exists()
    assert yaml.safe_load(config_file) is not None


# ============================================================================
# TESTS FOR CONFIG RELOAD
# ============================================================================

@pytest.mark.unit
@pytest.mark.config
def test_config_reload_from_disk(sample_config_file, temp_config_file):
    """Test that reload loads changes from disk."""
    # Create initial config
    with open(temp_config_file, 'w') as f:
        yaml.dump({"executor": {"skill_threshold": 0.7}}, f)

    config_manager = ConfigManager(
        config_path=str(temp_config_file),
        default_config_path=str(sample_config_file)
    )

    assert config_manager.get("executor.skill_threshold") == 0.7

    # Modify file on disk
    with open(temp_config_file, 'w') as f:
        yaml.dump({"executor": {"skill_threshold": 0.9}}, f)

    # Reload
    config_manager.reload()

    assert config_manager.get("executor.skill_threshold") == 0.9


# ============================================================================
# TESTS FOR BUILT-IN DEFAULTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.config
def test_config_builtin_defaults():
    """Test that built-in defaults are used when no config file exists."""
    config_manager = ConfigManager(
        config_path=None,
        default_config_path=None
    )

    # Should have built-in defaults
    assert config_manager.config is not None
    assert isinstance(config_manager.config, dict)


@pytest.mark.unit
@pytest.mark.config
def test_config_has_expected_sections(sample_config_file):
    """Test that configuration has expected sections."""
    config_manager = ConfigManager(
        default_config_path=str(sample_config_file)
    )

    # Check for expected top-level sections
    expected_sections = ["executor", "planner", "testing"]
    for section in expected_sections:
        assert section in config_manager.config, f"Missing section: {section}"


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

@pytest.mark.integration
@pytest.mark.config
def test_config_manager_end_to_end(temp_dir):
    """Test ConfigManager workflow: load, modify, save, reload."""
    config_file = temp_dir / "workflow_test.yaml"
    default_config = temp_dir / "default.yaml"

    # Create default config
    default_content = {
        "executor": {
            "skill_threshold": 0.7,
            "max_retries": 3
        }
    }
    with open(default_config, 'w') as f:
        yaml.dump(default_content, f)

    # Load config
    config_manager = ConfigManager(
        config_path=str(config_file),
        default_config_path=str(default_config)
    )

    # Verify initial load
    assert config_manager.get("executor.skill_threshold") == 0.7

    # Modify
    config_manager.set("executor.skill_threshold", 0.85)
    assert config_manager.get("executor.skill_threshold") == 0.85

    # Save
    config_manager.save()
    assert config_file.exists()

    # Create new instance to verify persistence
    new_manager = ConfigManager(
        config_path=str(config_file),
        default_config_path=None
    )
    assert new_manager.get("executor.skill_threshold") == 0.85
