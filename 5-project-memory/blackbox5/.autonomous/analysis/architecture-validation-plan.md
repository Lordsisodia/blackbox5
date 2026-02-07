# Architecture Validation Plan

**Goal:** Test the assumption that BlackBox5 architecture is "good enough" and consolidated.

**Method:** 10 parallel validation agents, each testing a specific architectural principle.

---

## Validation Agents

### Agent 1: Path Abstraction Validator
**Tests:** Hardcoded paths eliminated
**Scope:** All Python/shell scripts in 2-engine/ and 5-project-memory/
**Checks:**
- No hardcoded `/Users/shaansisodia/.blackbox5/` paths
- All scripts use PathResolver or paths.sh
- Cross-boundary references use abstraction layer
**Deliverable:** Report with list of violations (if any)

### Agent 2: Storage Backend Validator
**Tests:** Storage abstraction working
**Scope:** All YAML/JSON file operations
**Checks:**
- Scripts use StorageBackend instead of raw yaml.load()
- SQLite backend operational
- Queue operations use QueueRepository
- Task operations use TaskRepository
**Deliverable:** Migration progress report, files still using raw I/O

### Agent 3: Single Source of Truth Validator
**Tests:** No duplicate information
**Scope:** Task files, goal files, state files
**Checks:**
- No task in both active/ and completed/
- STATE.yaml derived (has generated timestamp)
- Goal status matches across all files
- No duplicate events.yaml files
**Deliverable:** SSOT violation report

### Agent 4: Communication Unification Validator
**Tests:** Unified agent communication
**Scope:** events.yaml, agent scripts, communication patterns
**Checks:**
- Single canonical events.yaml location
- Python agents use CommunicationRepository
- Bash agents use events.yaml (not separate reports)
- No dual communication systems
**Deliverable:** Communication architecture report

### Agent 5: Configuration Centralization Validator
**Tests:** Config-driven architecture
**Scope:** agent-config.yaml, skill-registry.yaml, all configs
**Checks:**
- agent-config.yaml is source of truth
- No hardcoded configuration in scripts
- Skill registry centralized
- Prompts consolidated
**Deliverable:** Configuration centralization report

### Agent 6: Run Folder Consolidation Validator
**Tests:** Run folders organized
**Scope:** All runs/ directories
**Checks:**
- Runs in canonical location (runs/)
- No scattered run folders
- Run naming consistent
- Old run folders archived
**Deliverable:** Run folder organization report

### Agent 7: Decision Registry Validator
**Tests:** Decisions extracted and centralized
**Scope:** DECISIONS.md files, registry.md
**Checks:**
- Central registry exists and has content
- Run folder decisions extracted
- Decision IDs consistent
- Cross-references maintained
**Deliverable:** Decision registry status report

### Agent 8: Hook Consolidation Validator
**Tests:** Hooks unified
**Scope:** .claude/hooks/, all hook locations
**Checks:**
- Single canonical hooks location
- No duplicate hooks
- Hook symlink working
- All hooks functional
**Deliverable:** Hook consolidation report

### Agent 9: File Locking Validator
**Tests:** Race conditions prevented
**Scope:** Shell scripts that modify shared files
**Checks:**
- flock used for queue.yaml operations
- flock used for events.yaml operations
- Lock files created in correct locations
- No read-modify-write without locking
**Deliverable:** File locking coverage report

### Agent 10: Overall Architecture Score Validator
**Tests:** Big picture architecture health
**Scope:** Entire BlackBox5 system
**Checks:**
- IG-006 completion percentage
- Critical architecture debt remaining
- Blockers for multi-agent cluster
- Recommendations for next phase
**Deliverable:** Executive summary with go/no-go recommendation

---

## Success Criteria

**Architecture is "good enough" if:**
1. <5% of scripts have hardcoded paths (Agent 1)
2. >80% of storage operations use abstraction (Agent 2)
3. Zero SSOT violations in critical files (Agent 3)
4. Single communication system operational (Agent 4)
5. Config centralization >90% (Agent 5)
6. Run folders >80% consolidated (Agent 6)
7. Decision registry has >50 decisions (Agent 7)
8. Hooks 100% consolidated (Agent 8)
9. File locking on all critical scripts (Agent 9)
10. Overall score >85% (Agent 10)

---

## Execution

All 10 agents run in parallel.
Each agent has read access to entire BlackBox5.
Agents report findings in structured format.
Final report synthesizes all findings.
