# RALF Configuration Management Guide
# ====================================
# Feature F-015: Enterprise Configuration Management
#
# Complete guide for using RALF's configuration management system.
#
# Author: RALF System
# Version: 2.0.0
# Feature: F-015

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Configuration Manager](#configuration-manager)
4. [Secrets Management](#secrets-management)
5. [Configuration Validation](#configuration-validation)
6. [Hot Reload](#hot-reload)
7. [Versioning and Rollback](#versioning-and-rollback)
8. [Configuration CLI](#configuration-cli)
9. [Environment Management](#environment-management)
10. [Security Best Practices](#security-best-practices)
11. [Troubleshooting](#troubleshooting)

---

## Overview

RALF Configuration Management System (F-015) provides enterprise-grade configuration management with:

- **Multi-environment support** (dev, staging, prod)
- **Secrets management** with AES-256-GCM encryption
- **Configuration validation** with JSON schema
- **Hot reload** - update config without restart
- **Versioning** - track changes and rollback
- **CLI tools** - manage configuration from command line

### Components

| Component | File | Purpose |
|-----------|------|---------|
| ConfigManagerV2 | `config_manager_v2.py` | Load and manage configuration |
| SecretsManager | `secrets_manager.py` | Encrypt and store secrets |
| ConfigValidator | `config_validator.py` | Validate configuration |
| ConfigWatcher | `config_watcher.py` | Hot reload on file changes |
| ConfigVersioner | `config_versioner.py` | Track versions and rollback |
| ConfigCLI | `config_cli.py` | Command-line interface |

---

## Quick Start

### 1. Basic Usage

```python
from config_manager_v2 import ConfigManagerV2

# Load configuration for environment
config = ConfigManagerV2(environment="dev")

# Get configuration value
api_port = config.get("api.port")  # 8080

# Set value at runtime
config.set("api.timeout", 60)

# Export configuration
yaml_config = config.export(format="yaml")
```

### 2. Environment-Specific Configuration

```bash
# Set environment
export RALF_ENV=production

# Configuration automatically loads prod.yaml
config = ConfigManagerV2()  # Auto-detects environment
```

### 3. Secrets Management

```python
from secrets_manager import SecretsManager

# Initialize (master password from environment)
sm = SecretsManager()  # Reads RALF_SECRETS_KEY

# Store secret
sm.set_secret("database_url", "postgresql://...")

# Retrieve secret
db_url = sm.get_secret("database_url")
```

### 4. Configuration CLI

```bash
# List all configuration
python config_cli.py list --env dev

# Get specific value
python config_cli.py get api.port --env dev

# Set value
python config_cli.py set api.timeout 60 --env dev --persist

# Validate configuration
python config_cli.py validate --env dev
```

---

## Configuration Manager

### Loading Configuration

```python
from config_manager_v2 import ConfigManagerV2

# Auto-detect environment from RALF_ENV
config = ConfigManagerV2()

# Specify environment explicitly
config = ConfigManagerV2(environment="staging")

# Custom config directory
config = ConfigManagerV2(
    environment="prod",
    config_dir="/etc/ralf/config"
)
```

### Accessing Values

```python
# Get nested value with dot notation
port = config.get("api.port")
host = config.get("api.host", "localhost")  # With default

# Get all configuration
all_config = config.get_all()

# Get current environment
env = config.get_environment()  # "dev", "staging", "prod"
```

### Setting Values

```python
# Set at runtime (not persisted)
config.set("api.timeout", 60)

# Set and persist to environment file
config.set("api.timeout", 60, persist=True)
```

### Configuration Hierarchy

Configuration is merged in this order:

1. **base.yaml** - Base configuration (inherited by all)
2. **{env}.yaml** - Environment-specific overrides

Example:
```yaml
# base.yaml
api:
  port: 8080
  timeout: 30

# dev.yaml
api:
  timeout: 60  # Overrides base

# Result in dev: port=8080 (from base), timeout=60 (from dev)
```

---

## Secrets Management

### Initialization

```python
from secrets_manager import SecretsManager

# From environment variable (recommended)
export RALF_SECRETS_KEY="your-master-password-here"
sm = SecretsManager()

# Or pass directly (less secure)
sm = SecretsManager(master_password="password")
```

### Storing Secrets

```python
# Store a secret
sm.set_secret("api_key", "sk-1234567890")
sm.set_secret("db_password", "securepassword")

# Secrets are encrypted and stored in secrets.enc
```

### Retrieving Secrets

```python
# Get secret
api_key = sm.get_secret("api_key")

# Get with default
api_key = sm.get_secret("missing_key", default="default-value")

# Raises exception if not found
try:
    api_key = sm.get_secret("missing_key")
except SecretsNotFoundError:
    api_key = None
```

### Managing Secrets

```python
# List all secret names
secrets = sm.list_secrets()  # ["api_key", "db_password"]

# Delete secret
sm.delete_secret("old_secret")

# Rotate (update) secret
sm.rotate_secret("api_key", "new-api-key-value")

# Export with masking
masked = sm.export_secrets(mask=True)
# {"api_key": "sk-****7890", "db_password": "****word"}
```

### Environment Variable Injection

```python
# Inject all secrets as environment variables
sm.inject_to_env(prefix="RALF_SECRET_")

# Now available via os.environ
import os
api_key = os.environ["RALF_SECRET_API_KEY"]
db_password = os.environ["RALF_SECRET_DB_PASSWORD"]
```

### Security Notes

**IMPORTANT:**
- Master password should come from secure source (ENV, KMS, file)
- Never hardcode master password in code
- Use strong passwords (32+ characters recommended)
- Store `secrets.enc` in secure location (permissions 600)
- Commit `secrets.enc` to Git is OK (encrypted), but master password is not

---

## Configuration Validation

### Using Schema Validation

```python
from config_validator import ConfigValidator

# Load schema
validator = ConfigValidator(schema_path="config/config.schema.yaml")

# Validate configuration
is_valid, errors = validator.validate(config.get_all())

if not is_valid:
    for error in errors:
        print(f"Error: {error}")
```

### Applying Defaults

```python
# Apply default values from schema
config_with_defaults = validator.apply_defaults(config.get_all())

# Now validate (should pass)
is_valid, errors = validator.validate(config_with_defaults)
```

### Schema Format

```yaml
api:
  type: dict
  properties:
    port:
      type: int
      validator: port  # Custom validator
      default: 8080
    timeout:
      type: int
      validator: positive_int
      default: 30
    url:
      type: string
      validator: url
      required: true
```

### Built-in Validators

| Validator | Description |
|-----------|-------------|
| `port` | Valid port number (1-65535) |
| `url` | Valid HTTP/HTTPS URL |
| `email` | Valid email address |
| `positive_int` | Positive integer |
| `non_empty_string` | Non-empty string |
| `api_key` | API key (min 10 chars) |
| `timeout` | Positive timeout value |

### Custom Validators

```python
# Add custom validator
def validate_even_number(value):
    return isinstance(value, int) and value % 2 == 0

validator.add_custom_validator("even", validate_even_number)

# Use in schema
# timeout:
#   type: int
#   validator: even
```

---

## Hot Reload

### Enabling Hot Reload

```python
from config_watcher import ConfigWatcher

# Define callback
def on_reload(config_file):
    print(f"Configuration changed: {config_file}")
    config_manager.reload()

# Create watcher
watcher = ConfigWatcher(
    config_files=["config/base.yaml", "config/dev.yaml"],
    on_change=on_reload,
    interval=5.0,  # Poll every 5 seconds
    debounce=2.0   # Wait 2s after last change
)

# Start watching
watcher.start()

# ... application runs ...

# Stop watching
watcher.stop()
```

### Manual Reload

```python
# Check for changes manually
changed_files = watcher.check_once()

if changed_files:
    print(f"Changed files: {changed_files}")
    config_manager.reload()
```

### Thread Safety

ConfigWatcher runs in a background thread and is thread-safe. Multiple threads can safely access the configuration manager.

---

## Versioning and Rollback

### Saving Versions

```python
from config_versioner import ConfigVersioner

versioner = ConfigVersioner(
    config_file="config/dev.yaml",
    history_dir="config/history"
)

# Save current configuration as version
version_id = versioner.save_version(
    message="Updated API timeout to 60",
    author="admin"
)
# Returns: "20250201-120000"
```

### Listing Versions

```python
# List all versions
versions = versioner.list_versions()

for v in versions:
    print(f"{v['version_id']}: {v['message']} ({v['timestamp']})")
```

### Rolling Back

```python
# Rollback to specific version (with backup)
versioner.rollback(version_id="20250201-120000", backup=True)

# Rollback without backup
versioner.rollback(version_id="20250201-120000", backup=False)
```

### Comparing Versions

```python
# Diff two versions
diff = versioner.diff_versions(
    version_id1="20250201-115000",
    version_id2="20250201-120000"
)

print(f"Only in v1: {diff['only_in_v1']}")
print(f"Only in v2: {diff['only_in_v2']}")
print(f"Different: {diff['different']}")
```

---

## Configuration CLI

### Available Commands

| Command | Description |
|---------|-------------|
| `list` | List all configuration values |
| `get <key>` | Get specific configuration value |
| `set <key> <value>` | Set configuration value |
| `validate` | Validate configuration |
| `diff <env>` | Compare environments |
| `rollback [version]` | Rollback to version (or list) |
| `version` | Show version information |
| `reload` | Reload configuration |
| `export` | Export configuration |

### Examples

```bash
# List configuration for dev environment
python config_cli.py list --env dev

# Get specific value
python config_cli.py get api.port --env dev

# Set value (runtime only)
python config_cli.py set api.timeout 60 --env dev

# Set value and persist to file
python config_cli.py set api.timeout 60 --env dev --persist

# Validate configuration
python config_cli.py validate --env dev

# Compare dev with staging
python config_cli.py diff staging --env dev

# List versions
python config_cli.py rollback --env dev

# Rollback to specific version
python config_cli.py rollback 20250201-120000 --env dev

# Show version info
python config_cli.py version --env dev

# Reload configuration
python config_cli.py reload --env dev

# Export to JSON
python config_cli.py export --format json --output config.json --env dev
```

### Global Options

```bash
# Specify environment
--env dev|staging|prod

# Custom config directory
--config-dir /etc/ralf/config

# Output format
--format text|json
```

---

## Environment Management

### Environment Detection

RALF automatically detects environment from variables (in order):

1. `RALF_ENV` (preferred)
2. `ENV`
3. `environment`
4. Defaults to `dev` if not set

```bash
# Set environment
export RALF_ENV=production
```

### Environment Files

| Environment | File | Purpose |
|-------------|------|---------|
| base | `base.yaml` | Base configuration (inherited by all) |
| dev | `dev.yaml` | Development (debug mode, verbose) |
| staging | `staging.yaml` | Pre-production testing |
| prod | `prod.yaml` | Production (optimized) |

### Switching Environments

```bash
# Method 1: Environment variable
export RALF_ENV=production

# Method 2: Specify explicitly
config = ConfigManagerV2(environment="prod")
```

---

## Security Best Practices

### 1. Master Password Management

**DO:**
- Store master password in environment variable
- Use strong password (32+ characters)
- Rotate master password periodically
- Use KMS or secret store for master password

**DON'T:**
- Hardcode master password in code
- Commit master password to Git
- Share master password via chat/email
- Use weak passwords

### 2. Secrets Storage

**DO:**
- Store `secrets.enc` with restricted permissions (600)
- Commit `secrets.enc` to Git (encrypted)
- Use different secrets for different environments
- Rotate secrets periodically

**DON'T:**
- Store plaintext secrets in config files
- Commit plaintext secrets to Git
- Use same secrets across environments
- Share secrets via unencrypted channels

### 3. Configuration Files

**DO:**
- Validate configuration before deployment
- Use schema validation
- Document configuration options
- Review changes before committing

**DON'T:**
- Commit secrets to config files
- Use default values in production
- Skip validation
- Make unreviewed changes

### 4. Access Control

**DO:**
- Restrict write access to configuration
- Use version control for all changes
- Audit configuration changes
- Use separate credentials per environment

**DON'T:**
- Allow unrestricted write access
- Make changes outside version control
- Ignore audit logs
- Share credentials across environments

---

## Troubleshooting

### Configuration Not Loading

**Problem:** Configuration loads as empty dict.

**Solutions:**
1. Check config directory path
2. Verify `base.yaml` exists
3. Verify `{env}.yaml` exists
4. Check file permissions

```python
# Debug
config = ConfigManagerV2(environment="dev")
print(f"Config dir: {config.config_dir}")
print(f"Base config: {config.base_config}")
print(f"Env config: {config.env_config}")
```

### Secrets Decryption Fails

**Problem:** `SecretsEncryptionError: Decryption failed`

**Solutions:**
1. Verify master password is correct
2. Check `RALF_SECRETS_KEY` environment variable
3. Verify `secrets.enc` file exists
4. Check if `secrets.enc` is corrupted

```python
# Validate secrets manager
sm = SecretsManager()
is_valid, errors = sm.validate()
print(f"Valid: {is_valid}, Errors: {errors}")
```

### Validation Fails

**Problem:** Configuration validation errors.

**Solutions:**
1. Check error messages for specific issues
2. Verify schema file exists
3. Apply defaults from schema
4. Fix type mismatches

```python
# Apply defaults and re-validate
validator = ConfigValidator(schema_path="config.schema.yaml")
config_with_defaults = validator.apply_defaults(config.get_all())
is_valid, errors = validator.validate(config_with_defaults)
```

### Hot Reload Not Working

**Problem:** Configuration changes not detected.

**Solutions:**
1. Verify watcher is running (`watcher.is_running()`)
2. Check file paths are correct
3. Increase polling interval
4. Check file system events

```python
# Debug
print(f"Watcher running: {watcher.is_running()}")
print(f"Watching files: {watcher.config_files}")
changed = watcher.check_once()
print(f"Changed files: {changed}")
```

### Rollback Fails

**Problem:** `FileNotFoundError: Version not found`

**Solutions:**
1. List available versions
2. Verify version ID is correct
3. Check history directory exists
4. Verify version file exists

```python
# List versions
versions = versioner.list_versions()
for v in versions:
    print(f"{v['version_id']}: {v['message']}")
```

---

## Advanced Topics

### Custom Configuration Directory

```python
config = ConfigManagerV2(
    environment="prod",
    config_dir="/etc/ralf/config"
)
```

### Multiple Configuration Managers

```python
# Main config
main_config = ConfigManagerV2(environment="dev")

# Feature-specific config
feature_config = ConfigManagerV2(
    environment="dev",
    config_dir="./config/features"
)
```

### Integration with F-006 (User Preferences)

F-015 is backward compatible with F-006:

```python
# Old F-006 code still works
from config_manager import ConfigManager

# New F-015 code extends F-006
from config_manager_v2 import ConfigManagerV2

# F-006 config files are still supported
```

---

## Migration Guide

### From F-006 to F-015

1. **Install dependencies:**
   ```bash
   pip install pyyaml cryptography
   ```

2. **Create environment files:**
   ```bash
   # Copy existing config to base.yaml
   cp config.yaml config/base.yaml

   # Create environment overrides
   cp config/base.yaml config/dev.yaml
   cp config/base.yaml config/prod.yaml
   ```

3. **Update code:**
   ```python
   # Old
   from config_manager import ConfigManager
   config = ConfigManager()

   # New
   from config_manager_v2 import ConfigManagerV2
   config = ConfigManagerV2(environment="dev")
   ```

4. **Validate configuration:**
   ```bash
   python config_cli.py validate --env dev
   ```

---

## API Reference

### ConfigManagerV2

| Method | Description |
|--------|-------------|
| `get(key, default=None)` | Get configuration value |
| `set(key, value, persist=False)` | Set configuration value |
| `get_all()` | Get all configuration |
| `get_environment()` | Get current environment |
| `reload()` | Reload from files |
| `validate()` | Validate configuration |
| `diff(other_env)` | Compare with other environment |
| `export(format="yaml")` | Export to string |

### SecretsManager

| Method | Description |
|--------|-------------|
| `set_secret(key, value)` | Store encrypted secret |
| `get_secret(key, default=None)` | Retrieve secret |
| `delete_secret(key)` | Delete secret |
| `list_secrets()` | List secret names |
| `rotate_secret(key, new_value)` | Update secret |
| `inject_to_env(prefix)` | Inject as env vars |
| `export_secrets(mask=True)` | Export secrets |
| `validate()` | Validate state |

### ConfigValidator

| Method | Description |
|--------|-------------|
| `validate(config, strict=False)` | Validate config |
| `apply_defaults(config)` | Apply defaults |
| `add_custom_validator(name, fn)` | Add validator |

### ConfigWatcher

| Method | Description |
|--------|-------------|
| `start()` | Start watching |
| `stop()` | Stop watching |
| `add_file(path)` | Add file to watch |
| `remove_file(path)` | Remove file |
| `check_once()` | Check for changes |
| `is_running()` | Check if running |

### ConfigVersioner

| Method | Description |
|--------|-------------|
| `save_version(message, author)` | Save version |
| `load_version(version_id)` | Load version |
| `rollback(version_id, backup=True)` | Rollback |
| `list_versions(limit=0)` | List versions |
| `diff_versions(v1, v2)` | Compare versions |

---

## Changelog

### Version 2.0.0 (Feature F-015)

**Added:**
- Multi-environment configuration support
- Secrets management with AES-256-GCM encryption
- Configuration validation with JSON schema
- Hot reload with file watching
- Configuration versioning and rollback
- CLI tools for configuration management
- Environment-specific config files
- Configuration schema

**Changed:**
- Extended F-006 ConfigManager with v2
- Improved error handling
- Better documentation

---

## Support

For issues, questions, or contributions:

- GitHub: https://github.com/anthropics/ralf
- Documentation: See `/operations/.docs/`
- Feature Specification: `plans/features/FEATURE-015-configuration-management.md`

---

**End of Configuration Management Guide**
