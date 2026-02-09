# Decisions: TASK-SSOT-025

## Decision 1: Create New SkillRepository vs Extend CommunicationRepository

**Context:** Both skill-usage.yaml and events.yaml are event logs, but with different structures.

**Decision:** Create a new `SkillRepository` class.

**Rationale:**
- skill-usage.yaml has a specific structure with `usage_log`, `skills`, and `metadata` sections
- events.yaml is a flat list of events
- SkillRepository needs skill-specific aggregation logic (updating skill stats)
- Keeping them separate maintains single responsibility principle

**Consequences:**
- (+) Cleaner, more focused APIs
- (+) Skill-specific operations are encapsulated
- (-) Slightly more code than extending an existing class

## Decision 2: Keep DEPRECATED Wrappers

**Context:** The old functions `load_skill_usage_yaml()`, `save_skill_usage_yaml()`, and `update_skill_stats()` are used by other scripts.

**Decision:** Keep them as DEPRECATED wrappers that delegate to SkillRepository.

**Rationale:**
- Prevents breaking changes to other scripts during migration
- Allows gradual migration of dependent code
- Clear documentation that new code should use SkillRepository directly

**Consequences:**
- (+) Backward compatibility maintained
- (+) Safe to migrate incrementally
- (-) Slight code duplication until all scripts are migrated

## Decision 3: Use Atomic File Writes

**Context:** skill-usage.yaml may be written by concurrent processes.

**Decision:** Implement temp-file-and-rename pattern in SkillRepository._save_data().

**Rationale:**
- Prevents data corruption during concurrent writes
- Atomic operation ensures file is never in a partially-written state
- Industry standard pattern for safe file updates

**Consequences:**
- (+) Data integrity guaranteed
- (+) No need for file locking during write (atomicity handles it)
- (-) Slightly more complex than direct write
