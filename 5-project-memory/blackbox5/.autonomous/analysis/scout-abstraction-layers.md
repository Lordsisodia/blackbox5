# Scout Report: Abstraction Layer Analysis

**Scout:** Architecture Analysis Agent
**Date:** 2026-02-06
**Status:** Complete

---

## Abstraction Layer Map

| Layer | Status | Implementation | Issues |
|-------|--------|----------------|--------|
| **Storage** | PARTIAL | VectorStore class exists for memory, but raw YAML/JSON everywhere else | No unified storage interface |
| **Queue** | MISSING | Direct YAML manipulation in bb5-queue-manager.py | No Queue abstraction class |
| **Task** | PARTIAL | Task dataclass in bb5-queue-manager.py, bb5-reanalysis-engine.py, bb5-metrics-collector.py | Multiple incompatible Task classes |
| **Agent** | MISSING | Standalone shell scripts in 2-engine/.autonomous/bin/ | No base Agent class |
| **Event** | PARTIAL | EventType enum in bb5-metrics-collector.py, raw YAML in events.yaml | No Event interface/abstraction |
| **Configuration** | MISSING | Direct routes.yaml access, hardcoded paths | No Config service |

---

## Critical Violations Found

### 1. Multiple Incompatible Task Classes
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/bin/bb5-queue-manager.py` line 60: `class Task`
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/bin/bb5-reanalysis-engine.py` line 127: `class Task`
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/bin/bb5-metrics-collector.py` line 90: `TaskMetrics` (different purpose)
- Each has different fields and methods - no shared interface

### 2. Raw File I/O Everywhere
- 38 files use direct `yaml.safe_load()`, `json.load()`, `open()`
- No centralized storage abstraction
- Pattern repeated in: queue-manager, reanalysis-engine, metrics-collector, sync-state, validate-ssot, etc.

### 3. Queue is Just YAML Manipulation
- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/bin/bb5-queue-manager.py` lines 241-332
- Direct file read/write with no abstraction layer
- Queue operations mixed with file I/O logic

### 4. No Agent Base Class
- Agents in `/Users/shaansisodia/.blackbox5/2-engine/.autonomous/bin/` are standalone scripts
- No common interface, lifecycle, or shared functionality
- Each agent implements its own argument parsing, logging, error handling

### 5. Configuration Access is Ad-Hoc
- Routes.yaml accessed directly by multiple scripts
- Hardcoded paths scattered throughout codebase
- No configuration service or environment abstraction

---

## Priority Recommendations

### HIGH: Create Unified Storage Abstraction
- Abstract class: `StorageBackend` with methods `load()`, `save()`, `query()`
- Implementations: `YAMLStorage`, `JSONStorage`, `VectorStorage`
- Eliminates 38+ instances of raw file I/O

### HIGH: Single Task Abstraction
- One `Task` class in shared module
- Used by queue-manager, reanalysis-engine, and all task operations
- Eliminates duplication and incompatibility

### MEDIUM: Queue Interface
- `Queue` class with methods `enqueue()`, `dequeue()`, `peek()`, `list()`
- Hides YAML structure from callers
- Enables queue backend changes without code changes

### MEDIUM: Agent Base Class
- `BaseAgent` with lifecycle methods: `initialize()`, `execute()`, `cleanup()`
- Common logging, error handling, metrics collection
- All agents inherit and implement `execute()`

### LOW: Configuration Service
- `Config` class with caching and validation
- Environment-based path resolution
- Schema validation for config files
