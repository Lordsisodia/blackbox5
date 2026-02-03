# TASK-1769892005: Build Project Relationship Map

**Type:** analyze
**Priority:** high
**Status:** pending
**Created:** 2026-02-01T06:00:00Z
**Source:** goals.yaml IG-003

---

## Objective

Create a comprehensive map of cross-project dependencies within the BlackBox5 ecosystem to prevent "missed file" errors and improve context gathering efficiency.

## Context

Per goals.yaml IG-003 (Improve System Flow and Code Mapping):
- Current issue: "Cross-project dependencies sometimes missed"
- Impact: Context gathering is inefficient, files are missed
- Improvement idea: "Build project relationship map"

BlackBox5 contains multiple interconnected projects:
- 5-project-memory/blackbox5/ (this project)
- 5-project-memory/siso-internal/
- 2-engine/.autonomous/
- 6-roadmap/ (research and plans)

Understanding these relationships will improve planning and execution.

## Success Criteria

- [ ] Identify all projects in the BlackBox5 ecosystem
- [ ] Map dependencies between projects (which references which)
- [ ] Document common cross-project patterns
- [ ] Create operations/project-map.yaml with relationships
- [ ] Identify files commonly referenced across projects
- [ ] Provide recommendations for context gathering optimization

## Approach

1. List all projects in ~/.blackbox5/
2. Search for cross-references (file paths, imports, mentions)
3. Analyze STATE.yaml and goals.yaml for project references
4. Check runs/ for cross-project task patterns
5. Create structured map in operations/project-map.yaml
6. Document findings in knowledge/analysis/project-relationships.md

## Files to Read

- ~/.blackbox5/5-project-memory/*/STATE.yaml
- ~/.blackbox5/5-project-memory/*/goals.yaml
- ~/.blackbox5/2-engine/.autonomous/**/*.md
- ~/.blackbox5/6-roadmap/**/*.md
- runs/completed/*/THOUGHTS.md (sample for cross-project references)

## Files to Create

- operations/project-map.yaml
- knowledge/analysis/project-relationships.md

## Schema for project-map.yaml

```yaml
projects:
  - name: "blackbox5"
    path: "5-project-memory/blackbox5"
    type: "project-memory"
    dependencies:
      - project: "siso-internal"
        reason: "Shared patterns, cross-references"
        references:
          - "~/.claude/CLAUDE.md"
    referenced_by:
      - project: "2-engine"
        reason: "RALF system integration"

  - name: "siso-internal"
    path: "5-project-memory/siso-internal"
    type: "project-memory"
    dependencies: []
    referenced_by:
      - project: "blackbox5"

relationships:
  - type: "shared-config"
    description: "CLAUDE.md shared across projects"
    files:
      - "~/.claude/CLAUDE.md"

  - type: "ralf-integration"
    description: "RALF engine connects to project memories"
    projects:
      - "2-engine"
      - "blackbox5"
      - "siso-internal"
```

## Notes

- Focus on practical relationships that affect daily work
- Note any circular dependencies
- Identify which files are "source of truth" for shared concepts
- Consider how this map will be used by Planner and Executor
