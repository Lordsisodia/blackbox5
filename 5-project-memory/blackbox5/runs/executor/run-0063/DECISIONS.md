# Decisions - TASK-1769958452

## Decision 1: Invoke bmad-dev Skill
**Context:** Feature F-015 is a multi-component implementation task requiring structured development approach.

**Selected:** Invoke bmad-dev (Amelia) with DS (Develop Story) workflow

**Rationale:**
- Task type "implement" matches bmad-dev's "feature development" trigger
- High confidence (85%) due to clear implementation requirements
- DS workflow provides structured approach: Understand → Explore → Write Tests → Implement → Refactor → Verify → Document
- Proven effective for feature implementation (used in F-009, F-010, F-011)

**Alternatives Considered:**
- Direct implementation without skill: Less structured, higher risk of missing steps
- bmad-architect: Overkill for this task (no major architectural decisions)
- bmad-quick-flow (QD): Too complex for 13-file implementation

**Reversibility:** LOW (code written, but can be refactored)

**Result:** Successful delivery following DS workflow, all components tested and working

---

## Decision 2: Extend F-006 Rather Than Replace
**Context:** F-015 requirements specify "extend F-006 with production-ready capabilities"

**Selected:** Create ConfigManagerV2 alongside ConfigManager (F-006), maintain both

**Rationale:**
- Backward compatibility: Existing code using F-006 continues to work
- Gradual migration: Users can migrate from F-006 to F-015 at their own pace
- Risk mitigation: New code (v2) doesn't break existing functionality
- Clear separation: F-006 for simple use cases, F-015 for enterprise needs

**Alternatives Considered:**
- Replace F-006 entirely: Breaking change, high risk
- Fork and modify F-006: Confusing version history
- Separate system: Duplicated effort, maintenance burden

**Reversibility:** LOW (design decision, affects architecture)

**Result:** Backward compatible, both managers work independently

---

## Decision 3: Polling-Based File Watching
**Context:** Hot reload requires detecting configuration file changes

**Selected:** Polling-based file watching (5-second interval)

**Rationale:**
- Portability: Works on all platforms (Linux, macOS, Windows)
- Simplicity: No external dependencies (no inotify, FSEvents)
- Reliability: No edge cases with network drives, container mounts
- Low overhead: 5-second polling = minimal CPU usage

**Alternatives Considered:**
- inotify (Linux): Not portable, requires pyinotify
- FSEvents (macOS): Platform-specific, requires pyobjc
- watchdog library: Additional dependency, abstraction layer

**Trade-offs:**
- Pro: Portable, simple, reliable
- Con: 5-second delay vs instant notification (acceptable for config)

**Reversibility:** MEDIUM (can replace with event-based system if needed)

**Result:** Hot reload works reliably across all platforms

---

## Decision 4: AES-256-GCM for Secrets Encryption
**Context:** Secrets manager requires encryption at rest

**Selected:** AES-256-GCM with PBKDF2 key derivation

**Rationale:**
- Industry standard: Used by GitHub, Stripe, AWS
- Authenticated encryption: GCM mode includes integrity verification
- NIST approved: AES-256 is FIPS 140-2 compliant
- Python support: cryptography library provides stable implementation
- Key derivation: PBKDF2 prevents brute force attacks (100k iterations)

**Alternatives Considered:**
- AES-256-CBC: Requires separate HMAC for integrity
- Fernet (cryptography): High-level, but less transparent
- HashiCorp Vault: External dependency, overkill for file-based

**Trade-offs:**
- Pro: Secure, standard, well-tested
- Con: Requires cryptography library (optional dependency)

**Reversibility:** LOW (cryptographic choice, hard to change later)

**Result:** Industry-standard encryption, graceful fallback if library unavailable

---

## Decision 5: Graceful Degradation for Missing Dependencies
**Context:** cryptography library may not be installed in all environments

**Selected:** Allow SecretsManager to fail gracefully with clear error message

**Rationale:**
- Developer experience: Clear error message guides installation
- Non-blocking: Other F-015 components work without cryptography
- Optional dependency: Secrets management is one feature of many
- Documentation: Installation instructions in guide

**Alternatives Considered:**
- Fail fast: ImportError on module load (too aggressive)
- Fallback encryption: Implement AES in pure Python (unsafe)
- Required dependency: Force cryptography installation (reduces flexibility)

**Trade-offs:**
- Pro: Flexible, clear error messages
- Con: Secrets manager unavailable until library installed

**Reversibility:** MEDIUM (can make cryptography required in future)

**Result:** Clear warning message, other components work fine

---

## Decision 6: Argparse Parent Parser for CLI Global Options
**Context:** CLI needs global options (--env, --config-dir) that work with subcommands

**Selected:** Use argparse parent_parser pattern for global options

**Rationale:**
- Standard pattern: Documented in argparse documentation
- Clean: Global options appear before or after subcommand
- Flexible: Easy to add new global options
- Maintainable: Clear separation of global vs subcommand options

**Issue Fixed:**
- Original: --env not recognized after subcommand (argparse limitation)
- Solution: parent_parser shared by main parser and subparsers
- Bug: Also fixed --format conflict (renamed to --output-format)

**Alternatives Considered:**
- Parse args manually: Complex, error-prone
- Click library: Additional dependency
- Require global options before subcommand: Poor UX

**Reversibility:** LOW (implementation detail, can be refactored)

**Result:** CLI works correctly with global options

---

## Decision 7: JSON Schema for Configuration Validation
**Context:** Need to validate configuration structure and types

**Selected:** YAML-based schema following JSON Schema pattern

**Rationale:**
- Familiar: JSON Schema is widely known and understood
- Expressive: Supports types, required fields, patterns, custom validators
- YAML format: Easier to read than JSON
- Extensible: Easy to add custom validators

**Alternatives Considered:**
- Pure Python validation: Code-based, less declarative
- Cerberus library: Additional dependency
- Marshmallow: Overkill for this use case

**Trade-offs:**
- Pro: Declarative, readable, extensible
- Con: Custom implementation (not full JSON Schema compliant)

**Reversibility:** MEDIUM (can switch to jsonschema library if needed)

**Result:** Validation works well, easy to understand and extend

---

## Decision 8: Configuration File Hierarchy (Base + Environment)
**Context:** Need to support multiple environments with shared settings

**Selected:** Base configuration + environment-specific overrides (deep merge)

**Rationale:**
- DRY principle: Common settings in base.yaml
- Flexibility: Environments override what they need
- Simplicity: Deep merge is intuitive
- Proven pattern: Used by Docker Compose, Terraform, etc.

**Alternatives Considered:**
- Complete separation: Duplication, hard to maintain
- Inheritance chain: Complex (base → dev → staging → prod)
- Template system: Overkill for this use case

**Trade-offs:**
- Pro: Simple, DRY, flexible
- Con: Need to understand merge behavior

**Reversibility:** LOW (design pattern, hard to change)

**Result:** Intuitive configuration hierarchy, works as expected

---

## Summary

| Decision | Impact | Risk | Outcome |
|----------|--------|------|---------|
| Invoke bmad-dev skill | High | Low | ✓ Successful |
| Extend F-006 | High | Low | ✓ Backward compatible |
| Polling file watch | Medium | Low | ✓ Portable |
| AES-256-GCM encryption | High | Low | ✓ Industry standard |
| Graceful degradation | Medium | Low | ✓ Clear errors |
| Argparse parent parser | Medium | Low | ✓ Fixed CLI |
| JSON Schema validation | Medium | Low | ✓ Declarative |
| Config hierarchy | High | Low | ✓ DRY + flexible |

**Key Insight:** All decisions balanced simplicity, portability, and industry standards. No high-risk choices.

**Future Considerations:**
- Consider event-based file watching if 5-second delay becomes issue
- Make cryptography required if secrets management becomes core feature
- Add full JSON Schema library if validation needs grow complex
