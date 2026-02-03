# Feature F-015: Configuration Management System

**Version:** 1.0.0
**Status:** planned
**Priority:** MEDIUM-HIGH (Score: 3.0)
**Estimated:** 120 minutes (~2 hours)
**Created:** 2026-02-01
**Feature ID:** F-015

---

## Overview

### User Value

**Who:** RALF operators (devops, system administrators)

**Problem:** Configuration scattered across multiple files, no environment-specific configs, no secrets management. RALF uses hardcoded values or simple F-006 config, but lacks enterprise-grade configuration management.

**Value:** Centralized configuration management with environment-specific configs, secrets management, and validation. Extends F-006 with production-ready configuration capabilities.

### Goals

1. **Environment Management:** Support multiple environments (dev, staging, prod)
2. **Secrets Management:** Secure storage and injection of sensitive data
3. **Configuration Validation:** Schema validation, type checking, defaults
4. **Hot Reload:** Update configuration without restart
5. **Configuration Versioning:** Track config changes, rollback support

### Success Criteria

**Must-Have:**
- [ ] Multi-environment support (dev, staging, prod)
- [ ] Secrets management (encrypted storage, secure injection)
- [ ] Configuration validation (schema, types, required fields)
- [ ] Environment-specific overrides
- [ ] Configuration CLI (list, get, set, validate)
- [ ] Documentation for configuration options

**Should-Have:**
- [ ] Hot reload (update config without restart)
- [ ] Configuration versioning (git-trackable changes)
- [ ] Rollback support (revert to previous config)
- [ ] Configuration diff (compare environments)

**Nice-to-Have:**
- [ ] Web UI for configuration management
- [ ] Configuration templates (share common settings)
- [ ] Integration with secret stores (HashiCorp Vault, AWS Secrets Manager)

---

## Requirements

### Functional Requirements

**FR-1: Environment Management**
- Support multiple environments (dev, staging, prod, custom)
- Environment-specific configuration files
- Environment detection (ENV variable or auto-detect)
- Environment inheritance (dev extends base, prod extends base)

**FR-2: Secrets Management**
- Encrypted secrets storage (file-based)
- Secure secrets injection (environment variables, in-place)
- Secret rotation support
- Audit log (who accessed which secret, when)

**FR-3: Configuration Validation**
- JSON schema validation
- Type checking (string, int, boolean, list, dict)
- Required fields validation
- Default values for missing fields
- Custom validators (e.g., port range, URL format)

**FR-4: Configuration CLI**
- `config list` - Show all configuration (with mask for secrets)
- `config get <key>` - Get specific configuration value
- `config set <key> <value>` - Set configuration value
- `config validate` - Validate configuration
- `config diff <env1> <env2>` - Compare environments
- `config rollback <version>` - Rollback to previous version

**FR-5: Hot Reload**
- Watch configuration files for changes
- Reload configuration without restart
- Validate new config before applying
- Notify components of configuration changes

**FR-6: Configuration Versioning**
- Track configuration changes (timestamp, who, what changed)
- Store previous versions (last N versions)
- Rollback to any previous version
- Diff between versions

### Non-Functional Requirements

**NFR-1: Security**
- Secrets encrypted at rest (AES-256 or similar)
- Secrets never logged (mask in output)
- Secure key derivation (PBKDF2 or similar)
- Access control (read-only for most, write for admins)

**NFR-2: Performance**
- Configuration load < 1 second
- Hot reload < 500ms
- Validation < 1 second
- No performance impact on runtime operations

**NFR-3: Usability**
- Clear error messages for validation failures
- Intuitive CLI commands
- Comprehensive documentation
- Example configurations for all environments

**NFR-4: Compatibility**
- Extends F-006 (User Preferences)
- Backward compatible with existing config
- Works with existing config files

---

## Architecture

### Components

**1. Configuration Manager (`config_manager_v2.py`)**
- Load configuration from environment-specific files
- Merge base + environment config
- Validate configuration (schema, types)
- Provide get/set/validate APIs

**2. Secrets Manager (`secrets_manager.py`)**
- Encrypt/decrypt secrets (AES-256)
- Load secrets from encrypted storage
- Inject secrets (environment variables, in-place)
- Audit log (access tracking)

**3. Configuration Validator (`config_validator.py`)**
- JSON schema validation
- Type checking
- Required fields validation
- Custom validators
- Default value injection

**4. Configuration Watcher (`config_watcher.py`)**
- Watch config files for changes
- Validate new config
- Trigger hot reload
- Notify components

**5. Configuration Versioner (`config_versioner.py`)**
- Track configuration changes
- Store previous versions
- Rollback support
- Diff between versions

**6. Configuration CLI (`config_cli.py`)**
- List/get/set/validate commands
- Diff and rollback commands
- Environment switching
- Masked output for secrets

### Data Flow

```
[Environment Selection] → [Load Config]
    ↓
[Config Manager] → [Merge Base + Environment]
    ↓
[Config Validator] ← [JSON Schema]
    ↓
[Secrets Manager] → [Inject Secrets]
    ↓
[Application Start]
    ↓
[Config Watcher] → [Detect Changes]
    ↓
[Hot Reload] → [Validate & Apply]
```

### File Structure

```
~/.blackbox5/
├── config/
│   ├── base.yaml              # Base configuration (shared)
│   ├── dev.yaml               # Dev environment overrides
│   ├── staging.yaml           # Staging environment overrides
│   ├── prod.yaml              # Prod environment overrides
│   └── secrets.enc            # Encrypted secrets (all envs)
├── config.versions/           # Configuration history
│   ├── v1.yaml
│   ├── v2.yaml
│   └── ...
└── config.schema.yaml         # JSON schema for validation
```

### Integration Points

**F-006 (User Preferences):** Extend with environment management, validation, secrets
**All Components:** Use centralized config manager (no scattered config)
**CI/CD (F-007):** Environment-specific configs for deployments

---

## Implementation Plan

### Phase 1: Configuration Manager & Environments (40 min)
- [ ] Create `config_manager_v2.py` (extends F-006)
- [ ] Implement environment loading (base + overrides)
- [ ] Create config file structure (base, dev, staging, prod)
- [ ] Implement environment detection (ENV variable)
- [ ] Create get/set APIs

### Phase 2: Secrets Management (30 min)
- [ ] Create `secrets_manager.py`
- [ ] Implement encryption/decryption (AES-256)
- [ ] Create secrets.enc file format
- [ ] Implement secrets injection
- [ ] Add audit logging

### Phase 3: Configuration Validation (20 min)
- [ ] Create `config_validator.py`
- [ ] Define JSON schema for all config
- [ ] Implement type checking
- [ ] Implement required fields validation
- [ ] Add default value injection

### Phase 4: Configuration CLI (20 min)
- [ ] Create `config_cli.py`
- [ ] Implement list/get/set/validate commands
- [ ] Implement diff command
- [ ] Implement rollback command
- [ ] Add masked output for secrets

### Phase 5: Hot Reload & Versioning (30 min)
- [ ] Create `config_watcher.py` (file watching)
- [ ] Create `config_versioner.py` (change tracking)
- [ ] Implement hot reload logic
- [ ] Implement rollback logic
- [ ] Add change notifications

### Phase 6: Documentation & Testing (remaining time)
- [ ] Create user guide (operations/.docs/config-management-guide.md)
- [ ] Document all configuration options
- [ ] Create example configs (dev, staging, prod)
- [ ] Test hot reload, validation, rollback

---

## Dependencies

**Required Features:**
- F-006 (User Preferences) - Base configuration system

**Required Tools:**
- cryptography (AES-256 encryption)
- jsonschema (schema validation)
- pyyaml or toml (config file format)
- watchdog (file watching for hot reload)

**Data Required:**
- Existing F-006 config file
- Current configuration keys and defaults

---

## Testing Strategy

### Unit Tests
- Test environment loading (base + overrides)
- Test secrets encryption/decryption
- Test validation (valid, invalid, missing fields)
- Test hot reload logic
- Test versioning and rollback

### Integration Tests
- Test full config pipeline (load → validate → inject → use)
- Test hot reload (change file, verify reload)
- Test rollback (apply bad config, rollback, verify)
- Test environment switching

### Security Tests
- Test secrets encryption strength
- Test secrets masking (no leakage in logs)
- Test audit logging (all accesses tracked)
- Test key derivation (slow, secure)

### Manual Tests
- Create configs for dev, staging, prod
- Test environment switching
- Test secrets management (add, use, rotate)
- Test hot reload (modify config, verify no restart)
- Test rollback (break config, rollback)

### Success Metrics
- Configuration load time < 1 second
- Secrets encryption strength: AES-256
- Hot reload time < 500ms
- Zero secrets leaked in logs

---

## Documentation

### User Documentation
**File:** `operations/.docs/config-management-guide.md`

**Sections:**
1. Overview and benefits
2. Installation and setup
3. Configuration file structure
4. Managing environments
5. Managing secrets
6. Using the CLI
7. Hot reload and rollback
8. Troubleshooting

### Developer Documentation
**File:** `2-engine/.autonomous/.docs/config-management-architecture.md`

**Sections:**
1. Architecture overview
2. Configuration schema
3. Adding new configuration keys
4. Extending the validator
5. Integration points

### Configuration Reference
**File:** `2-engine/.autonomous/config/config.schema.yaml`

**Sections:**
1. JSON schema for all config
2. Type definitions
3. Required fields
4. Default values
5. Custom validators

### Example Configurations
**Files:**
- `2-engine/.autonomous/config/base.yaml` - Base config
- `2-engine/.autonomous/config/dev.yaml` - Dev overrides
- `2-engine/.autonomous/config/staging.yaml` - Staging overrides
- `2-engine/.autonomous/config/prod.yaml` - Prod overrides

---

## Tasks

1. **TASK-<timestamp>-implement-f015**
   - Implement Feature F-015 (Configuration Management System)
   - Status: pending
   - Priority: medium-high (Score: 3.0)

---

## Configuration Schema

**Example schema (simplified):**

```yaml
# Base configuration
system:
  name: "blackbox5"
  version: "5.0.0"
  environment: "dev"  # dev, staging, prod

logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR
  file: "/var/log/blackbox5/ralf.log"

queue:
  min_depth: 3
  max_depth: 5
  refill_threshold: 2

executor:
  max_retries: 3
  timeout_minutes: 60

# Secrets (encrypted)
secrets:
  github_token: "..."
  api_key: "..."
```

---

## Metrics to Track

**Configuration Metrics:**
- Configuration load time (seconds)
- Hot reload frequency (count per hour)
- Validation failure rate (percentage)
- Rollback frequency (count per hour)

**Security Metrics:**
- Secrets access attempts (count)
- Secrets encryption/decryption time (seconds)
- Audit log entries (count)
- Configuration changes (count per day)

---

## Rollout Plan

### Phase 1: Alpha (Internal)
- New config system alongside F-006
- Manual migration of existing config
- Internal testing only

### Phase 2: Beta (Opt-in)
- Optional migration for early adopters
- Gather feedback, refine features
- Fix bugs, improve UX

### Phase 3: Production (Full Rollout)
- Migrate all existing config
- Deprecate old F-006 config system
- Full documentation and support

---

## Open Questions

1. **Q:** What encryption algorithm for secrets?
   **A:** AES-256-GCM (authenticated encryption). Standard, secure, widely supported.

2. **Q:** How to derive encryption key?
   **A:** PBKDF2-HMAC-SHA256 with user passphrase. Slow, secure, standard.

3. **Q:** Should we support external secret stores (Vault, AWS)?
   **A:** Not in MVP. Future enhancement via pluggable secrets backend.

4. **Q:** How to handle config migration from F-006?
   **A:** Provide migration script (F-006 → F-015). Manual verification required.

---

## Change Log

| Date | Change | Version |
|------|--------|---------|
| 2026-02-01 | Initial specification | 1.0.0 |

---

**End of Feature F-015 Specification**
