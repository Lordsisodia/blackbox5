# Decisions - TASK-1769899001

## Section Placement Decision
**Context:** Where to insert the "When to Use Skills" section in CLAUDE.md
**Selected:** After "Sub-Agent Rules" section, before "Context Management"
**Rationale:** Skills are an alternative approach to sub-agents and direct reads. Placing them together creates a logical flow: sub-agents → skills → context management. This keeps execution guidance in one area.
**Reversibility:** MEDIUM - Could be moved to a standalone section if it grows too large.

## Confidence Threshold Decision
**Context:** What confidence threshold to require for skill invocation
**Selected:** >80% baseline, with 85-90% for specialized domains
**Rationale:**
- 80% matches the task requirement
- Higher thresholds (85-90%) for architecture, UX, QA where wrong skill selection is costly
- Lower threshold (80%) acceptable for general development and research tasks
**Reversibility:** HIGH - Thresholds can be adjusted based on usage data in skill-metrics.yaml

## Domain Mapping Scope Decision
**Context:** How many skills to include in the mapping table
**Selected:** 15 most commonly used skills across all categories
**Rationale:**
- Full list of 23 skills would be overwhelming
- Focused on skills most likely to be invoked (BMAD agents + key utilities)
- Infrastructure skills (ralf-cloud-control, etc.) excluded as they're specialized
- Reference to skill-usage.yaml provided for complete list
**Reversibility:** HIGH - Table can be expanded or trimmed based on actual usage patterns

## Documentation Format Decision
**Context:** How to document skill usage requirements
**Selected:** YAML template example in the section
**Rationale:**
- Matches existing format in skill-metrics.yaml
- Easy to copy and fill in during task completion
- Consistent with BlackBox5's YAML-heavy documentation style
**Reversibility:** MEDIUM - Could be replaced with automated tracking in the future

## Skill Invocation Examples Decision
**Context:** What examples to provide for skill invocation patterns
**Selected:** 3 patterns with concrete examples (direct call, keyword detection, task type matching)
**Rationale:**
- Covers main ways skills get triggered
- Examples use realistic scenarios
- Shows confidence calculation for each
**Reversibility:** HIGH - Examples can be updated as new patterns emerge
