---
name: Phase 1.5 Skill Checking
trigger:
  - before execution
  - phase 2
  - implement
  - analyze
  - refactor
alwaysApply: true
priority: 95
---

# Phase 1.5: Mandatory Skill Checking

## Rule
BEFORE starting Phase 2 (Execution) of ANY task, you MUST check for applicable skills.

## Process
1. Read `skill-selection.yaml` at `~/.blackbox5/5-project-memory/blackbox5/operations/skill-selection.yaml`
2. Check `domain_mapping` for matching keywords in your task
3. Calculate confidence using the formula in the file
4. Invoke skill only if confidence >= 70%

## Documentation
Document in THOUGHTS.md under "## Skill Usage for This Task":
- Applicable skills found (or "None")
- Skill invoked (or "None")
- Confidence percentage
- Rationale for decision

## Auto-Trigger Rules
| Trigger Condition | Action Required |
|-------------------|-----------------|
| Task contains "implement" + domain keyword (git, n8n, supabase, etc.) | MUST check for matching skill |
| Task contains "analyze" or "research" | MUST check bmad-analyst, web-search |
| Task contains "architecture", "design", "refactor" | MUST check bmad-architect |
| Task contains "Should we...", "How should we..." | MUST check superintelligence-protocol |
| Task contains "PRD", "requirements", "feature" | MUST check bmad-pm |
| Task contains "test", "QA", "quality" | MUST check bmad-qa |
| Multiple files or systems involved | MUST check relevant skills |

## Important
Failure to check skills is a protocol violation.

## Source
- CLAUDE.md Phase 1.5 section
- skill-selection.yaml
