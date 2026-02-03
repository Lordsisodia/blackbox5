# Results - TASK-1769899001

**Task:** TASK-1769899001 - Create Skill Selection Guidance Framework
**Status:** completed

## What Was Done

Added comprehensive "When to Use Skills" section to ~/.claude/CLAUDE.md after the "Sub-Agent Rules" section. The new section includes:

### 1. Skill Selection Process
- **Check**: Determine if task matches a skill domain using keywords
- **Match**: Find best skill from operations/skill-usage.yaml with >80% confidence
- **Apply**: Read SKILL.md and follow defined process

### 2. Domain-to-Skill Mapping Table
| Domain | Skill | Trigger Keywords | Threshold |
|--------|-------|------------------|-----------|
| Product Management | bmad-pm | PRD, requirements | 85% |
| Architecture | bmad-architect | architecture, design | 90% |
| Research/Analysis | bmad-analyst | research, analyze | 80% |
| Scrum/Process | bmad-sm | sprint, process | 80% |
| UX/Design | bmad-ux | UI, UX, design | 85% |
| Development | bmad-dev | implement, code | 80% |
| QA/Testing | bmad-qa | test strategy | 85% |
| Task Execution | bmad-tea | RALF, autonomous | 80% |
| Quick Tasks | bmad-quick-flow | simple, quick fix | 85% |
| Complex Problems | superintelligence-protocol | "Should we..." | 90% |
| Continuous Improvement | continuous-improvement | improve, optimize | 80% |
| Git Operations | git-commit | commit, PR | 90% |
| Codebase Navigation | codebase-navigation | find code | 80% |
| Supabase/Database | supabase-operations | supabase, database | 90% |
| Web Research | web-search | search, current events | 80% |

### 3. Skill Invocation Patterns
- Direct Skill Call (explicit user request)
- Keyword Detection (pattern matching)
- Task Type Matching (task description analysis)

### 4. Documentation Requirements
- Template for updating operations/skill-metrics.yaml
- Fields: task_id, timestamp, skill_used, outcome, trigger_was_correct, would_use_again

### 5. When NOT to Use Skills
- Confidence <80%
- Simple tasks
- No matching domain
- Emergency fixes

## Validation

- [x] Section inserted at appropriate location in CLAUDE.md
- [x] Skill selection process documented (check → match → apply)
- [x] Domain-to-skill mapping provided
- [x] Confidence threshold defined (>80%)
- [x] Skill usage documentation requirements specified
- [x] Examples of skill invocation patterns included
- [x] Cross-references to skill-usage.yaml and skill-metrics.yaml

## Files Modified

- ~/.claude/CLAUDE.md: Added "When to Use Skills" section (lines 184-268)
