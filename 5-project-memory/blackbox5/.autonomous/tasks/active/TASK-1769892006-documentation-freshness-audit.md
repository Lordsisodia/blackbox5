# TASK-1769892006: Audit Documentation Freshness

**Type:** analyze
**Priority:** medium
**Status:** pending
**Created:** 2026-02-01T06:00:00Z
**Source:** goals.yaml IG-005

---

## Objective

Audit all documentation in the blackbox5 project to identify stale content and ensure documentation quality and utility.

## Context

Per goals.yaml IG-005 (Improve Documentation Quality and Utility):
- Current issue: "Some docs may be outdated"
- Current issue: "Template adoption unknown"
- Improvement idea: "Auto-flag docs not touched in 30 days"
- Success criteria: "All docs referenced at least once per month"

Documentation is spread across:
- Root .docs/ folder
- Per-folder .docs/ folders
- Template files in .templates/
- Decision records in decisions/

## Success Criteria

- [ ] Inventory all documentation files (*.md in .docs/, decisions/, knowledge/)
- [ ] Check last modified date for each doc
- [ ] Identify docs not touched in >30 days
- [ ] Check for orphaned docs (not referenced anywhere)
- [ ] Flag docs with outdated content (references to removed features)
- [ ] Create operations/documentation-audit.yaml with findings
- [ ] Provide recommendations for doc maintenance

## Approach

1. Find all documentation files recursively
2. Get last modified timestamps (git log or stat)
3. Search for references to each doc in codebase
4. Identify docs with outdated content patterns
5. Categorize findings by severity
6. Create actionable recommendations

## Files to Check

**Documentation locations:**
- .docs/*.md
- */.docs/*.md
- decisions/**/*.md
- knowledge/**/*.md
- .templates/**/*.md

**Reference sources:**
- STATE.yaml (references docs)
- QUERIES.md (references docs)
- Run files (THOUGHTS.md, DECISIONS.md reference docs)

## Files to Create

- operations/documentation-audit.yaml
- knowledge/analysis/documentation-freshness-20260201.md

## Schema for documentation-audit.yaml

```yaml
audit:
  date: "2026-02-01T06:00:00Z"
  total_docs: 0
  stale_docs: []
  orphaned_docs: []
  outdated_content_docs: []

docs:
  - path: ".docs/ai-template-usage-guide.md"
    last_modified: "2026-01-31"
    days_since_touch: 1
    references_found: 5
    status: "fresh"
    action: "none"

  - path: "knowledge/analysis/autonomous-runs-analysis.md"
    last_modified: "2026-01-15"
    days_since_touch: 17
    references_found: 0
    status: "stale"
    action: "review"

recommendations:
  - priority: "high"
    action: "Update knowledge/analysis/autonomous-runs-analysis.md"
    reason: "17 days stale, 0 references"

  - priority: "medium"
    action: "Add reference tracking to run completion"
    reason: "Cannot verify doc usage without tracking"
```

## Notes

- Be thorough but practical - focus on high-impact docs
- Consider docs "stale" if >30 days without modification
- Consider docs "orphaned" if 0 references found
- Look for patterns like "TODO: update this doc" or references to removed features
- The goal is actionable insights, not just a list
