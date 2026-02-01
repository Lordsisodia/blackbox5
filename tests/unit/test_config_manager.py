"""
Unit Tests for ConfigManager
============================

Tests configuration loading, validation, and access.
"""

import pytest
import sys
from pathlib import Path

# Add engine lib to path
ENGINE_LIB = Path("/workspaces/blackbox5/2-engine/.autonomous/lib")
if str(ENGINE_LIB) not in sys.path:
    sys.path.insert(0, str(ENGINE_LIB))

from config_manager import ConfigManager, ConfigValidationError

# Import test utilities
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from test_utils import (
    mock_config,
    create_temp_yaml_file,
    cleanup_test_files,
    assert_valid_confidence,
    assert_valid_queue_depth
)


class TestConfigManager:
    """Test ConfigManager functionality."""

    def test_load_default_config(self, temp_dir):
        """Test loading default configuration when no user config exists."""
        # Create default config file
        default_config_path = temp_dir / "default.yaml"
        default_config = mock_config()
        import yaml
        with open(default_config_path, 'w') as f:
            yaml.dump(default_config, f)

        # Load config without user config
        config = ConfigManager(
            config_path=None,
            default_config_path=str(default_config_path)
        )

        # Verify defaults loaded
        assert config.config == default_config
        assert config.get('thresholds.skill_invocation_confidence') == 70

    def test_load_user_config(self, temp_dir):
        """Test loading user config and overriding defaults."""
        # Create default config
        default_config_path = temp_dir / "default.yaml"
        default_config = mock_config()
        import yaml
        with open(default_config_path, 'w') as f:
            yaml.dump(default_config, f)

        # Create user config with custom values
        user_config_path = temp_dir / "user.yaml"
        user_config = mock_config(skill_invocation_confidence=80)
        with open(user_config_path, 'w') as f:
            yaml.dump(user_config, f)

        # Load config with user override
        config = ConfigManager(
            config_path=str(user_config_path),
            default_config_path=str(default_config_path)
        )

        # Verify user config overrides defaults
        assert config.get('thresholds.skill_invocation_confidence') == 80

    def test_invalid_config_fallback(self, temp_dir):
        """Test invalid config falls back to defaults."""
        # Create default config
        default_config_path = temp_dir / "default.yaml"
        default_config = mock_config()
        import yaml
        with open(default_config_path, 'w') as f:
            yaml.dump(default_config, f)

        # Create invalid user config (confidence > 100)
        user_config_path = temp_dir / "user.yaml"
        invalid_config = mock_config(skill_invocation_confidence=150)
        with open(user_config_path, 'w') as f:
            yaml.dump(invalid_config, f)

        # Load config (should fall back to defaults)
        config = ConfigManager(
            config_path=str(user_config_path),
            default_config_path=str(default_config_path)
        )

        # Verify fallback to defaults
        assert config.get('thresholds.skill_invocation_confidence') == 70

    def test_get_nested_key(self, temp_dir):
        """Test nested key access with dot notation."""
        # Create default config
        default_config_path = temp_dir / "default.yaml"
        default_config = mock_config()
        import yaml
        with open(default_config_path, 'w') as f:
            yaml.dump(default_config, f)

        # Load config
        config = ConfigManager(
            config_path=None,
            default_config_path=str(default_config_path)
        )

        # Test nested key access
        assert config.get('thresholds.skill_invocation_confidence') == 70
        assert config.get('routing.default_agent') == 'executor'
        assert config.get('notifications.enabled') is False

    def test_get_missing_key_returns_none(self, temp_dir):
        """Test getting missing key returns None."""
        # Create default config
        default_config_path = temp_dir / "default.yaml"
        default_config = mock_config()
        import yaml
        with open(default_config_path, 'w') as f:
            yaml.dump(default_config, f)

        # Load config
        config = ConfigManager(
            config_path=None,
            default_config_path=str(default_config_path)
        )

        # Test missing key
        assert config.get('missing.key') is None

    def test_set_nested_key(self, temp_dir):
        """Test setting nested keys."""
        # Create default config
        default_config_path = temp_dir / "default.yaml"
        default_config = mock_config()
        import yaml
        with open(default_config_path, 'w') as f:
            yaml.dump(default_config, f)

        # Load config
        config = ConfigManager(
            config_path=None,
            default_config_path=str(default_config_path)
        )

        # Set nested key
        config.set('thresholds.skill_invocation_confidence', 85)

        # Verify value changed
        assert config.get('thresholds.skill_invocation_confidence') == 85

    def test_validate_confidence_range(self, temp_dir):
        """Test confidence validation (0-100)."""
        # Create default config
        default_config_path = temp_dir / "default.yaml"
        default_config = mock_config()
        import yaml
        with open(default_config_path, 'w') as f:
            yaml.dump(default_config, f)

        # Load config
        config = ConfigManager(
            config_path=None,
            default_config_path=str(default_config_path)
        )

        # Test valid confidence values
        assert_valid_confidence(config.get('thresholds.skill_invocation_confidence'))

        # Test invalid confidence (should not be in valid config)
        # If we set it to 150, validation should fail or clamp it
        config.set('thresholds.skill_invocation_confidence', 150)
        # The config manager should handle this gracefully
        # (either by rejecting the value or falling back to defaults)

    def test_validate_queue_depth_range(self, temp_dir):
        """Test queue depth validation (min >= 0, min <= max)."""
        # Create default config
        default_config_path = temp_dir / "default.yaml"
        default_config = mock_config()
        import yaml
        with open(default_config_path, 'w') as f:
            yaml.dump(default_config, f)

        # Load config
        config = ConfigManager(
            config_path=None,
            default_config_path=str(default_config_path)
        )

        # Test valid queue depth
        min_depth = config.get('thresholds.queue_depth_min')
        max_depth = config.get('thresholds.queue_depth_max')
        assert_valid_queue_depth(min_depth, max_depth)

    def test_save_config(self, temp_dir):
        """Test saving configuration to file."""
        # Create default config
        default_config_path = temp_dir / "default.yaml"
        default_config = mock_config()
        import yaml
        with open(default_config_path, 'w') as f:
            yaml.dump(default_config, f)

        # Create save path
        save_path = temp_dir / "saved.yaml"

        # Load config
        config = ConfigManager(
            config_path=None,
            default_config_path=str(default_config_path)
        )

        # Modify and save
        config.set('thresholds.skill_invocation_confidence', 90)
        config.save_config(str(save_path))

        # Verify saved file exists and has correct content
        assert save_path.exists()
        with open(save_path, 'r') as f:
            saved_config = yaml.safe_load(f)
        assert saved_config['thresholds']['skill_invocation_confidence'] == 90


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
