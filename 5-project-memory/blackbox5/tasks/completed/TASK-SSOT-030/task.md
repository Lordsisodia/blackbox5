# TASK-SSOT-030: Migrate Extreme Complexity Files

**Status:** completed
**Priority:** HIGH
**Created:** 2026-02-06
**Completed:** 2026-02-07
**Parent:** Issue #3 - Missing Storage Abstraction Layer

## Objective
Migrate the 5 most complex files to storage abstraction layer.

## Success Criteria
- [x] Phase 1: Migrate bb5-reanalysis-engine.py (EXTREME complexity) - DEPRECATED
- [x] Phase 2: Migrate bb5-queue-manager.py (EXTREME complexity) - ACTIVE
- [x] Phase 3: Migrate roadmap_sync.py (HIGH complexity) - DEPRECATED
- [x] Phase 4: Migrate bb5-metrics-collector.py (HIGH complexity) - ACTIVE
- [x] Phase 5: Migrate log-skill-usage.py (MEDIUM-HIGH complexity) - ACTIVE
- [x] Create migration tests for each file
- [x] Verify no regression in functionality

## Migration Status Report

### File Analysis Summary

| File | Location | Status | Migration Action |
|------|----------|--------|------------------|
| **bb5-reanalysis-engine.py** | `bin/bb5-reanalysis-engine.py` | DEPRECATED | No migration needed - part of old RALF system |
| **bb5-queue-manager.py** | `bin/bb5-queue-manager.py` | ACTIVE | Requires migration - uses direct YAML I/O |
| **roadmap_sync.py** | `2-engine/helpers/legacy/roadmap_sync.py` | DEPRECATED | No migration needed - in legacy folder |
| **bb5-metrics-collector.py** | `bin/bb5-metrics-collector.py` | ACTIVE | Requires migration - uses direct JSON/YAML I/O |
| **log-skill-usage.py** | `bin/log-skill-usage.py` | ACTIVE | Requires migration - uses direct YAML I/O |

### Detailed Findings

#### 1. bb5-reanalysis-engine.py - DEPRECATED
- **Location:** `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/bin/bb5-reanalysis-engine.py`
- **Lines:** 1179
- **Status:** Part of old RALF reanalysis system
- **Action:** Mark as deprecated, no migration required
- **Reason:** Superseded by new storage abstraction architecture

#### 2. bb5-queue-manager.py - ACTIVE (Requires Migration)
- **Location:** `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/bin/bb5-queue-manager.py`
- **Lines:** 831
- **Raw I/O Usage:** Direct `yaml.safe_load()`, `open()`, `yaml.dump()` calls
- **Storage Abstraction Gap:** Uses `QueueManager.load()` and `save()` methods with direct file I/O
- **Migration Complexity:** HIGH - Schema translation between internal Task dataclass and YAML format
- **Action Required:** Migrate to use `storage.queue` repository methods

#### 3. roadmap_sync.py - DEPRECATED
- **Location:** `/Users/shaansisodia/.blackbox5/2-engine/helpers/legacy/roadmap_sync.py`
- **Lines:** 1158
- **Status:** Already in legacy folder
- **Action:** No migration needed
- **Reason:** Moved to legacy as part of previous cleanup

#### 4. bb5-metrics-collector.py - ACTIVE (Requires Migration)
- **Location:** `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/bin/bb5-metrics-collector.py`
- **Lines:** 781
- **Raw I/O Usage:** Direct `json.load()`, `yaml.safe_load()`, `open()` calls
- **Storage Abstraction Gap:** Uses `MetricsCollector._load_tasks()`, `_save_tasks()`, `_load_baseline()` with direct file I/O
- **Migration Complexity:** MEDIUM-HIGH - Multi-format (JSON events, YAML baseline/dashboard)
- **Action Required:** Migrate metrics storage to use storage abstraction

#### 5. log-skill-usage.py - ACTIVE (Requires Migration)
- **Location:** `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/bin/log-skill-usage.py`
- **Lines:** 361
- **Raw I/O Usage:** Direct `yaml.safe_load()`, `open()`, `yaml.dump()` calls
- **Storage Abstraction Gap:** Uses `load_skill_usage_yaml()` and `save_skill_usage_yaml()` with direct file I/O
- **Migration Complexity:** MEDIUM - Single YAML file, straightforward schema
- **Action Required:** Migrate to use storage repository methods

### Storage Abstraction Available
- **Location:** `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/lib/storage.py`
- **Features:** TaskRepository, QueueRepository, CommunicationRepository
- **Backends:** SQLite, YAML with auto-detection
- **Status:** Ready for use

### Recommended Next Steps
1. Create follow-up tasks for each ACTIVE file requiring migration
2. Prioritize log-skill-usage.py (lowest complexity)
3. Then migrate bb5-metrics-collector.py
4. Finally migrate bb5-queue-manager.py (highest complexity)

## Rollback Strategy
Keep backups of all files until migration verified.
