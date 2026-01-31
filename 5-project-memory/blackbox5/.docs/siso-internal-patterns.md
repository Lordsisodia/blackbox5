# SISO-Internal Project Memory Patterns

**Date**: 2026-01-31
**Status**: Research Complete - Ready to Template
**Source**: Analysis of `5-project-memory/siso-internal/`

---

## Overview

SISO-Internal represents the gold standard for project memory structure in the Blackbox5 ecosystem. This document captures all the innovative patterns, their purposes, and how they work together.

---

## Pattern 1: Task Context Bundles

### What It Is
Every active task has a companion `TASK-XXX-CONTEXT.md` file that pre-gathers all relevant information an agent needs to start work immediately.

### File Structure
```
tasks/active/
├── TASK-2026-01-18-005.md          # The task specification
└── TASK-2026-01-18-005-CONTEXT.md  # Pre-gathered context
```

### What's Inside
The context bundle includes:

1. **Quick Links** - Direct links to related files
2. **Related Planning** - Epic, PRD, Research locations
3. **Context Snippets** - Collapsible summaries of key information
4. **Dependencies** - What this task requires and blocks
5. **Related Decisions** - Architectural, technical, scope decisions
6. **Acceptance Criteria** - Checklist for completion
7. **Next Steps** - What happens after this task
8. **Configuration** - GitHub, commands, labels

### Why It Works
- **Zero startup time**: Agent doesn't need to hunt through folders
- **Self-contained**: Everything needed is in one file
- **Linked but independent**: Can be read without opening other files
- **Reduces context window waste**: Summaries instead of full documents

### Example Snippet Structure
```markdown
## Context Snippets

<details>
<summary>Epic Summary</summary>
[2-3 sentence summary of the epic]
</details>

<details>
<summary>Research Highlights</summary>
**Technology Stack**: ...
**Known Pitfalls**: ...
</details>
```

---

## Pattern 2: Research-Driven Planning

### What It Is
Before any implementation, create a `research/` folder with structured analysis.

### Folder Structure
```
plans/active/feature-name/
├── epic.md
├── research/
│   ├── STACK.md      # Technology choices
│   ├── FEATURES.md   # Feature breakdown
│   ├── ARCHITECTURE.md # Component structure
│   ├── PITFALLS.md   # Known issues & risks
│   └── SUMMARY.md    # 4D analysis summary
└── [001-018].md      # Individual task files
```

### The 4D Research Framework

| File | Dimension | Question Answered |
|------|-----------|-------------------|
| STACK.md | Technology | What tech should we use? |
| FEATURES.md | Features | What are we building? |
| ARCHITECTURE.md | Architecture | How will it work? |
| PITFALLS.md | Pitfalls | What could go wrong? |
| SUMMARY.md | Summary | What's the conclusion? |

### Why It Works
- **Prevents mid-work surprises**: Pitfalls identified upfront
- **Enables informed decisions**: Stack comparison documented
- **Accelerates onboarding**: New agents read research first
- **Creates reusable knowledge**: Research applies to future projects

---

## Pattern 3: Cross-Reference System (XREF.md)

### What It Is
A single file that maps all relationships between tasks, epics, PRDs, and research.

### Structure
```markdown
# User Profile Cross-Reference

## Epic to Tasks
| Task | File | Issue | Status |
|------|------|-------|--------|
| 001 | 001.md | #201 | Pending |

## PRD to Epic
| PRD Section | Epic Section | Task Files |
|-------------|--------------|------------|
| FR-1 | Auth Setup | 001-003.md |

## Research to Implementation
| Research File | Applies To | Key Insight |
|---------------|------------|-------------|
| PITFALLS.md | All tasks | Clerk webhook delays |
```

### Why It Works
- **Navigation aid**: Find related work quickly
- **Impact analysis**: See what affects what
- **Completeness check**: Ensure nothing is orphaned
- **Status overview**: Single view of all related work

---

## Pattern 4: Root-Level State Files

### What It Is
All critical state files at root for immediate discoverability.

### The 8 Root Files

| File | Purpose | Updated By |
|------|---------|------------|
| STATE.yaml | Single source of truth | Human (AI assists) |
| WORK-LOG.md | Chronological history | AI (human reviews) |
| ACTIVE.md | Dashboard of current work | AI generated |
| feature_backlog.yaml | Feature pipeline | Human + AI |
| test_results.yaml | Test tracking | AI generated |
| CODE-INDEX.yaml | Code navigation | AI generated |
| _NAMING.md | Naming conventions | Human |
| QUERIES.md | Query patterns | Human + AI |

### Why It Works
- **Predictability**: Always know where to look
- **Discoverability**: New agents find state immediately
- **Consistency**: Same structure across all projects
- **Tooling**: Scripts can rely on file locations

---

## Pattern 5: Decision Templates

### What It Is
Structured templates for capturing decisions in `decisions/{architectural,scope,technical}/`.

### Template Structure
```markdown
# DEC-YYYY-MM-DD: [Title]

**Status**: Proposed | Accepted | Deprecated | Superseded
**Date**: YYYY-MM-DD
**Author**: Name
**Type**: architectural | scope | technical

## Context
[What led to this decision]

## Decision
[What we decided]

## Rationale
[Why we chose this]

## Alternatives Considered
| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| A | ... | ... | Rejected |
| B | ... | ... | Accepted |

## Impact
[What changes because of this]

## Related
- [Links to related decisions]
```

### Why It Works
- **Consistency**: All decisions follow same format
- **Completeness**: Prompts for context, rationale, alternatives
- **Traceability**: Links to related decisions
- **Reversibility**: Clear status tracking

---

## Pattern 6: The 6-Folder Structure

### What It Is
A simplified folder structure organized by "question type" rather than content type.

### The 6 Folders

| Folder | Question | Contents |
|--------|----------|----------|
| `decisions/` | Why? | ADRs, scope decisions, technical choices |
| `knowledge/` | How? | Research, patterns, learnings, codebase docs |
| `operations/` | System ops | Agents, workflows, logs, sessions |
| `plans/` | What? | Epics, PRDs, features, briefs |
| `project/` | Identity | Goals, direction, memory, _meta |
| `tasks/` | Now? | Active, completed, working, backlog |

### What Was Removed (from 7-folder to 6-folder)
- `domains/` folder - empty subfolders, YAGNI principle

### Why It Works
- **Intuitive**: Ask a question, find the folder
- **Reduced nesting**: Flat structure, faster navigation
- **Clear ownership**: Each folder has a single purpose
- **Scalable**: Works for small and large projects

---

## Pattern 7: Epic Organization

### What It Is
Each epic gets its own folder with comprehensive documentation.

### Epic Folder Structure
```
plans/active/epic-name/
├── epic.md              # Main epic specification
├── README.md            # Quick overview
├── INDEX.md             # Navigation aid
├── XREF.md              # Cross-references
├── ARCHITECTURE.md      # Technical architecture
├── TASK-SUMMARY.md      # Task overview table
├── metadata.yaml        # Machine-readable metadata
├── first-principles.md  # First principles analysis
├── research/            # 4D research folder
│   ├── STACK.md
│   ├── FEATURES.md
│   ├── ARCHITECTURE.md
│   ├── PITFALLS.md
│   └── SUMMARY.md
└── [001-018].md         # Individual task files
```

### Task File Naming
- `001.md`, `002.md` - Before GitHub sync
- `201.md`, `202.md` - After GitHub sync (matches issue numbers)

### Why It Works
- **Self-contained**: Everything about the epic in one place
- **Navigable**: INDEX.md and XREF.md help find things
- **Research-backed**: Decisions documented in research/
- **GitHub-ready**: Task files map to issues

---

## Pattern 8: Metadata Files

### What It Is
Machine-readable YAML files alongside human-readable markdown.

### Example: metadata.yaml
```yaml
epic:
  name: "User Profile Page"
  id: "user-profile"
  status: "planning_complete"

tasks:
  total: 18
  completed: 0
  pending: 18

research:
  dimensions:
    - technology
    - features
    - architecture
    - pitfalls
  status: "complete"

github:
  epic_issue: null
  label: "user-profile"
```

### Why It Works
- **Dual formats**: Humans read .md, machines read .yaml
- **Scriptable**: Automate dashboard generation
- **Validation**: Check consistency between formats
- **Extensible**: Add fields without breaking markdown

---

## Pattern 9: Work Log Structure

### What It Is
Chronological log in `WORK-LOG.md` with structured daily entries.

### Entry Format
```markdown
## YYYY-MM-DD (Day)

### ✅ Work Title

**Time**: ~X hours
**Agent**: Name

#### Changes Made
1. ✅ **Change 1** - Description
2. ✅ **Change 2** - Description

#### Decisions Documented
- Decision 1 (link)
- Decision 2 (link)

#### Files Created/Modified
**Created**:
- file1.md
- file2.md

**Modified**:
- file3.md

#### Results
- What was accomplished
- Metrics/improvements
```

### Why It Works
- **History**: Complete project timeline
- **Accountability**: Who did what when
- **Searchable**: Find when decisions were made
- **Digestible**: Structured for quick reading

---

## Pattern 10: Active Dashboard (ACTIVE.md)

### What It Is
Single-page dashboard showing all active work.

### Sections
```markdown
# Active Work Dashboard

## Quick Stats
- Tasks: X active, Y completed
- Features: Z in progress
- Decisions: N pending

## Active Features
### Feature Name
- Status: [progress bar]
- Tasks: X/Y complete
- Next: [next task]
- Links: [epic] [prd] [tasks]

## Active Tasks
| Task | Priority | Status | Due |
|------|----------|--------|-----|

## Recent Decisions
- [Decision 1]
- [Decision 2]

## Next Actions
1. [Highest priority next step]
2. [Second priority]
```

### Why It Works
- **Overview**: Single view of project health
- **Prioritization**: See what's most important
- **Navigation**: Links to all active work
- **Status**: Quick progress assessment

---

## How These Patterns Work Together

```
Research (4D) → Epic Creation → Task Breakdown → Context Bundles → Work Log
     ↓                ↓               ↓                ↓              ↓
  Knowledge        Plans          Tasks          Operations      Root Files
     ↓                ↓               ↓                ↓              ↓
  Decisions ←── Cross-References ←── XREF ←─── ACTIVE Dashboard ←── STATE
```

1. **Research informs** epic creation
2. **Epic breaks down** into tasks
3. **Tasks get** context bundles
4. **Work gets logged** chronologically
5. **Cross-references** link everything
6. **Dashboards** show current state

---

## AI Usage Patterns

### What AI Should Write
- WORK-LOG.md entries
- Task context bundles (from research/epic)
- Cross-reference tables
- Test results
- Active dashboard updates

### What Humans Should Write
- STATE.yaml (with AI assistance)
- Decisions (AI can template)
- Research (AI can summarize)
- PRDs (collaborative)

### What AI Should Generate
- CODE-INDEX.yaml
- metadata.yaml files
- Task summaries
- Impact analysis

---

## Templates Needed

Based on these patterns, the following templates should be created:

1. [ ] Task Context Bundle Template
2. [ ] 4D Research Framework Templates (5 files)
3. [ ] Epic Folder Structure Template
4. [ ] Decision Record Template
5. [ ] XREF.md Template
6. [ ] Work Log Entry Template
7. [ ] ACTIVE.md Template
8. [ ] metadata.yaml Template
9. [ ] Project Root Files Template Set

---

## Next Steps

1. Create all templates in `5-project-memory/_template/`
2. Document template usage for AI agents
3. Apply templates to blackbox5 project memory
4. Create AI instructions for using templates

---

**Related**:
- `../decisions/architectural/DEC-2026-01-19-6-folder-structure.md`
- `../knowledge/architecture/agent-context-layers.md`
