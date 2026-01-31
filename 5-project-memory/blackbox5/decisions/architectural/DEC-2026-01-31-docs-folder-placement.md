# DEC-2026-01-31: .docs Folder Placement Strategy

**Status**: Accepted
**Date**: 2026-01-31
**Author**: Claude (with User)
**Type**: Architectural

---

## Context

We debated whether to place `.docs/` folders:
- A) Only at root of project memory
- B) Only in each subfolder
- C) Both root and subfolders

## Decision

**Use BOTH root `.docs/` and per-folder `.docs/`**

---

## Root `.docs/` (Project-Wide)

**Location**: `5-project-memory/blackbox5/.docs/`

**Purpose**: Cross-cutting, project-wide AI documentation

**Contains**:
| File/Folder | Purpose |
|-------------|---------|
| `README.md` | Explains the .docs system |
| `patterns.md` | Patterns detected across entire project |
| `health.md` | Overall project health analysis |
| `recommendations.md` | Project-wide improvement suggestions |
| `index.md` | Auto-generated master index |
| `architecture/` | System architecture documentation |
| `siso-internal-patterns.md` | Pattern documentation (imported) |
| `ai-template-usage-guide.md` | AI template usage guide |
| `dot-docs-system.md` | This system specification |

**Rule**: If it spans multiple folders, it goes here.

---

## Per-Folder `.docs/` (Contextual)

**Location**: Inside each main folder

**Purpose**: Folder-specific context and relationships

### decisions/.docs/
| File | Purpose |
|------|---------|
| `context.md` | Why decisions matter in current context |
| `related.md` | Links between decisions |
| `evolution.md` | How decisions have changed |

### knowledge/.docs/
| File | Purpose |
|------|---------|
| `summaries/` | Auto-generated summaries |
| `patterns/` | Detected patterns |
| `questions.md` | Open questions |
| `connections.md` | Links between knowledge areas |

### plans/.docs/
| File | Purpose |
|------|---------|
| `context.md` | Current epic/feature status |
| `dependencies.md` | Dependency status |
| `risks.md` | Updated risk assessment |
| `recommendations.md` | Suggested next steps |

### tasks/.docs/
| File | Purpose |
|------|---------|
| `notes.md` | Working notes |
| `progress.md` | Progress tracking |
| `learnings.md` | What was learned |
| `blockers.md` | Current blockers |

### project/.docs/
| File | Purpose |
|------|---------|
| `goals-status.md` | Goal progress |
| `direction-changes.md` | Direction evolution |

### operations/.docs/
| File | Purpose |
|------|---------|
| `run-summaries/` | Summaries of agent runs |
| `workflow-status.md` | Workflow health |

**Rule**: If it's specific to the parent folder's content, it goes here.

---

## The Principle

**Write context as close to content as possible, but elevate cross-cutting concerns to root.**

### Examples

| Content | Placement | Reason |
|---------|-----------|--------|
| Task working notes | `tasks/.docs/notes.md` | Specific to tasks |
| Decision relationships | `decisions/.docs/related.md` | Specific to decisions |
| Project-wide patterns | `.docs/patterns.md` | Spans all folders |
| Epic status | `plans/active/epic/.docs/status.md` | Specific to that epic |
| Overall health | `.docs/health.md` | Aggregates all folders |

---

## Implementation

1. Root `.docs/` already created with initial content
2. Create per-folder `.docs/` as needed
3. Document in each folder's README what its .docs/ contains
4. Update AI guide with placement rules

---

## Related

- `.docs/dot-docs-system.md` - Full system specification
- `.docs/ai-template-usage-guide.md` - AI usage instructions
