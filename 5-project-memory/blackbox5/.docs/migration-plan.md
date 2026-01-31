# Blackbox5 Project Memory Migration Plan

**Date**: 2026-01-31
**Status**: Planning
**Goal**: Transform blackbox5 project memory to match siso-internal gold standard

---

## Current State Analysis

### What Exists (Blackbox5)
- Folder structure (7-folder, needs migration to 6-folder)
- `project/context.yaml` (goals, vision)
- `.docs/` folder (patterns documented)
- `.autonomous/` folder (RALF runs, tasks - needs migration)
- `decisions/` (mostly empty)
- `knowledge/` (some content)
- `operations/` (some content)
- `plans/` (mostly empty)
- `tasks/` (FG-1769138998 folder)
- `domains/` (SHOULD BE REMOVED)

### What's Missing (vs siso-internal)
- [ ] STATE.yaml at root
- [ ] WORK-LOG.md at root
- [ ] ACTIVE.md at root
- [ ] timeline.yaml at root
- [ ] feature_backlog.yaml at root
- [ ] test_results.yaml at root
- [ ] CODE-INDEX.yaml at root
- [ ] _NAMING.md at root
- [ ] QUERIES.md at root
- [ ] 6-folder structure (remove domains/)
- [ ] Decision templates
- [ ] Research templates (4D framework)
- [ ] Task context bundle templates
- [ ] Epic folder templates

### What Needs Migration (from ralf-core)
- [ ] All tasks from `.autonomous/tasks/`
- [ ] Decision registry
- [ ] Validations
- [ ] Run history (optional - may archive)

---

## Phase 1: Analysis (Sub-agents)

### Task 1.1: Analyze siso-internal Structure
**Agent**: Analyst
**Input**: `5-project-memory/siso-internal/`
**Output**: Complete inventory of files, folders, templates
**Deliverable**: `analysis-siso-internal.md`

### Task 1.2: Analyze blackbox5 Current State
**Agent**: Analyst
**Input**: `5-project-memory/blackbox5/`
**Output**: Complete inventory of existing content
**Deliverable**: `analysis-blackbox5-current.md`

### Task 1.3: Analyze ralf-core Content
**Agent**: Analyst
**Input**: `5-project-memory/ralf-core/`
**Output**: What needs to be migrated to blackbox5
**Deliverable**: `analysis-ralf-core-migration.md`

### Task 1.4: Identify Templates Needed
**Agent**: Architect
**Input**: Results from 1.1, 1.2, 1.3
**Output**: List of all templates to create
**Deliverable**: `templates-needed.md`

---

## Phase 2: Template Creation (Sub-agents)

### Task 2.1: Root File Templates
**Agent**: Developer
**Templates**:
- STATE.yaml.template
- WORK-LOG.md.template
- ACTIVE.md.template
- feature_backlog.yaml.template
- test_results.yaml.template
- _NAMING.md.template
- QUERIES.md.template
- timeline.yaml.template

**Location**: `5-project-memory/blackbox5/.templates/root/`

### Task 2.2: Decision Templates
**Agent**: Developer
**Templates**:
- architectural.md.template
- scope.md.template
- technical.md.template

**Location**: `5-project-memory/blackbox5/.templates/decisions/`

### Task 2.3: Research Templates (4D Framework)
**Agent**: Developer
**Templates**:
- STACK.md.template
- FEATURES.md.template
- ARCHITECTURE.md.template
- PITFALLS.md.template
- SUMMARY.md.template

**Location**: `5-project-memory/blackbox5/.templates/research/`

### Task 2.4: Epic Templates
**Agent**: Developer
**Templates**:
- epic.md.template
- README.md.template
- INDEX.md.template
- XREF.md.template
- ARCHITECTURE.md.template
- TASK-SUMMARY.md.template
- metadata.yaml.template

**Location**: `5-project-memory/blackbox5/.templates/epic/`

### Task 2.5: Task Templates
**Agent**: Developer
**Templates**:
- task-specification.md.template
- task-context-bundle.md.template
- task-completion.md.template

**Location**: `5-project-memory/blackbox5/.templates/tasks/`

---

## Phase 3: Content Migration (Sub-agents)

### Task 3.1: Create Root Files
**Agent**: Developer
**Files to Create**:
- STATE.yaml (from context.yaml + analysis)
- WORK-LOG.md (from ralf-core runs)
- ACTIVE.md (generated from state)
- timeline.yaml (from ralf-core timeline)
- _NAMING.md (standard)
- QUERIES.md (standard)

### Task 3.2: Migrate RALF-Core Content
**Agent**: Developer
**Migrate**:
- Tasks from `ralf-core/.autonomous/tasks/` → `blackbox5/tasks/`
- Decision registry → `blackbox5/decisions/`
- Validations → `blackbox5/.docs/validations/`
- Archive runs → `blackbox5/.archived/runs/`

### Task 3.3: Restructure Folders
**Agent**: Developer
**Actions**:
- Remove `domains/` folder
- Move content to appropriate 6 folders
- Create `.docs/` in each folder
- Update README.md

### Task 3.4: Create Example Content
**Agent**: Developer
**Create**:
- Example decision using template
- Example epic with research folder
- Example task with context bundle

---

## Phase 4: Integration (Sub-agents)

### Task 4.1: Update Documentation
**Agent**: Technical Writer
**Update**:
- blackbox5/README.md
- .docs/ files with new structure
- AI guide with template locations

### Task 4.2: Create Template Usage Guide
**Agent**: Technical Writer
**Create**: `5-project-memory/_template/README.md`

### Task 4.3: Validate Structure
**Agent**: QA
**Check**:
- All templates exist
- All root files present
- No broken links
- Consistent structure

---

## Execution Order

1. Run Phase 1 analysis tasks (parallel)
2. Review analysis results
3. Run Phase 2 template creation (parallel)
4. Review templates
5. Run Phase 3 migration (sequential, dependencies)
6. Run Phase 4 integration (parallel)
7. Final validation

---

## Success Criteria

- [ ] All 8 root files present
- [ ] 6-folder structure (no domains/)
- [ ] All templates in .templates/
- [ ] RALF-core content migrated
- [ ] Example content created
- [ ] Documentation updated
- [ ] Validated by QA agent

---

## Next Steps

1. Launch Phase 1 analysis sub-agents
2. Review their findings
3. Proceed to Phase 2

**Ready to start Phase 1?**
