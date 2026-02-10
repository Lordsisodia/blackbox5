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
BEFORE starting Phase 2 (Execution) of ANY task, you MUST check for applicable skills and invoke when confidence is clear.

## Confidence Thresholds

### Clear Triggers (MUST Invoke - No Override)
**Confidence >= 85%**
When confidence is 85% or higher, you MUST invoke the skill. No subjective judgment allowed.

**Examples:**
- "implement" + exact domain match (e.g., "implement git commit")
- "Should we..." + architecture keyword
- "PRD" + feature definition

### Discretionary Triggers (SHOULD Invoke - Agent Judgment)
**Confidence 70-84%**
When confidence is between 70-84%, you SHOULD invoke the skill but may use judgment.

**Examples:**
- "implement" + related domain
- "analyze" + partial match
- "test" + unclear scope

### Low Confidence (MAY Check - Agent Discretion)
**Confidence < 70%**
When confidence is below 70%, you MAY check the skill but invocation is optional.

## Process
1. Read `skill-selection.yaml` at `~/.blackbox5/5-project-memory/blackbox5/operations/skill-registry.yaml` (section: selection_framework)
2. Check `domain_mapping` for matching keywords in your task
3. Calculate confidence using the formula in the file
4. **If confidence >= 85% (Clear Trigger): MUST invoke skill** - no override allowed
5. **If confidence 70-84% (Discretionary): SHOULD invoke skill** - agent judgment allowed
6. **If confidence < 70%: MAY check skill** - invocation optional

## Documentation
Document in THOUGHTS.md under "## Skill Usage for This Task":
- Applicable skills found (or "None")
- Skill invoked (or "None")
- Confidence percentage
- Rationale for decision (especially if discretion was used)

## Auto-Trigger Rules

| Trigger Condition | Confidence Level | Action | Override Allowed |
|-------------------|------------------|--------|------------------|
| "implement" + exact domain match (git commit, PR, etc.) | >= 85% | MUST invoke | NO |
| "Should we..." + architecture keyword | >= 85% | MUST invoke | NO |
| "PRD" + feature definition | >= 85% | MUST invoke | NO |
| "analyze" or "research" | 70-84% | SHOULD invoke | YES |
| "architecture", "design", "refactor" | 70-84% | SHOULD invoke | YES |
| "implement" + related domain | 70-84% | SHOULD invoke | YES |
| "test", "QA", "quality" | 70-84% | SHOULD invoke | YES |
| Multiple files or systems involved | 70-84% | SHOULD invoke | YES |
| General keyword match | < 70% | MAY check | YES |

## Important
- For clear triggers (>= 85%), invocation is MANDATORY - no judgment or override allowed
- For discretionary triggers (70-84%), use your best judgment based on task complexity
- Failure to check for applicable skills is a protocol violation

## Source
- CLAUDE.md Phase 1.5 section
- skill-registry.yaml (selection_framework section)
