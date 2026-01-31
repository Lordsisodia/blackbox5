# Decisions - TASK-1769892005

## YAML vs Markdown for Project Map

**Context:** Needed to choose the primary format for the project relationship map.

**Selected:** Both YAML (machine-readable) and Markdown (human-readable)

**Rationale:**
- YAML for programmatic access by Planner/Executor agents
- Markdown for human review and understanding
- YAML can be parsed by tools like yq for analysis
- Markdown provides narrative context that YAML cannot

**Reversibility:** HIGH - Can generate one from the other if needed

## Project Scope

**Context:** Needed to decide which projects to include in the map.

**Selected:** All 5 projects in the ecosystem
- blackbox5 (this project)
- siso-internal
- 2-engine
- team-entrepreneurship-memory
- 6-roadmap

**Rationale:**
- Complete picture of ecosystem
- Even low-priority projects may have dependencies
- Template and management folders excluded (not active projects)

**Reversibility:** HIGH - Can add/remove projects as ecosystem evolves

## Relationship Type Definitions

**Context:** Needed to categorize the types of relationships between projects.

**Selected:** 5 relationship types
1. shared-config - Files shared across projects (CLAUDE.md)
2. ralf-integration - Engine connects to all project memories
3. pattern-replication - One project copies patterns from another
4. feedback-loop - Improvements flow between projects
5. cross-reference - Documentation references multiple projects

**Rationale:**
- Covers all observed relationship patterns
- Clear distinction between dependency types
- Helps identify risk levels

**Reversibility:** HIGH - Can add new relationship types as discovered

## Context Gathering Heuristics

**Context:** Needed to provide actionable guidance for agents.

**Selected:** Three heuristics based on task type
1. If BMAD commands involved → Read 2-engine/routes.yaml
2. If project structure involved → Reference siso-internal
3. If documentation involved → Check all .docs/ folders

**Rationale:**
- Simple rules that cover common scenarios
- Based on actual patterns found in codebase
- Easy to remember and apply

**Reversibility:** HIGH - Can refine based on usage patterns

## Risk Assessment

**Context:** Needed to identify potential issues from cross-project dependencies.

**Selected:** 4 risk areas with severity levels
1. CLAUDE.md Changes (HIGH) - Universal impact
2. Engine Updates (HIGH) - Breaks all projects
3. Path References (MEDIUM) - Structure changes break references
4. Skill Dependencies (MEDIUM) - Skills may reference non-existent files

**Rationale:**
- Focus on highest-impact risks
- Provide specific mitigation strategies
- Aligns with goals.yaml IG-003 objectives

**Reversibility:** N/A - Risk assessment is informational
