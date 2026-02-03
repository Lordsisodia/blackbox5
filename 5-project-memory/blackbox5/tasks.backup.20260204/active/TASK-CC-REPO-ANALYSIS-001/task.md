# TASK-CC-REPO-ANALYSIS-001: Claude Code GitHub Repo Analysis - Main Task

**Status:** pending
**Priority:** high
**Created:** 2026-02-04
**Parent:** None (Top-level research task)

---

## Goal

Analyze Claude Code related GitHub repositories using an autonomous multi-agent workflow with Claude Code's native Task system integration.

## Workflow Design

This task demonstrates the full Dual-RALF autonomous cycle integrated with Claude Code's Task primitives.

### Phase 1: Repository Discovery (Planner Agent)
**Claude Code Task:** `TASK-CC-001A`
- Search for Claude Code related GitHub repos
- Filter by relevance (stars, forks, recent activity)
- Create subtasks for each repo
- **Output:** List of repos to analyze with `TASK-CC-001A-{N}` subtasks

### Phase 2: Per-Repo Analysis Cycle (Executor Agent + Subagents)
**For each repo, create blocked task chain:**

```
TASK-CC-001B-{N}-1 (Research)
    → TASK-CC-001B-{N}-2 (Plan) [blockedBy: 1]
    → TASK-CC-001B-{N}-3 (Execute) [blockedBy: 2]
```

Each cycle:
1. **Research Subagent** (1 iteration): Clone repo, analyze structure, extract key files
2. **Plan Subagent** (1 iteration): Create implementation plan based on findings
3. **Execute Subagent** (1 iteration): Document findings, create artifacts

**Repeat 3x cycles per repo** = 9 subagent iterations total per repo

### Phase 3: Planner Analysis (Planner Agent)
**Claude Code Task:** `TASK-CC-001C`
**Blocked by:** All TASK-CC-001B-{N}-3 tasks

- Review all repo analysis results
- Identify patterns across repos
- Generate insights report
- **Output:** `analysis/synthesis-report.md`

### Phase 4: Additional Iteration Cycles (Executor Agent)
**Claude Code Tasks:** `TASK-CC-001D-{N}`
**Blocked by:** TASK-CC-001C

- Deep dive on interesting patterns found
- Cross-repo comparison analysis
- Extract reusable components/patterns

### Phase 5: Data Analysis (Analyst Agent)
**Claude Code Task:** `TASK-CC-001E`
**Blocked by:** All TASK-CC-001D-{N}

- Aggregate all findings
- Generate metrics (code complexity, test coverage, etc.)
- Create visualization data
- **Output:** `analysis/aggregated-metrics.yaml`

### Phase 6: Task Generation (Planner Agent)
**Claude Code Task:** `TASK-CC-001F`
**Blocked by:** TASK-CC-001E

- Based on analysis, generate new implementation tasks
- Prioritize tasks by impact/effort
- Add to queue.yaml for executor
- **Output:** New tasks in `tasks/active/`

### Phase 7: Execute Generated Tasks (Executor Agent)
**Claude Code Tasks:** Generated tasks from Phase 6
**Blocked by:** TASK-CC-001F

- Standard executor workflow
- Each task goes through 7-phase execution
- Update queue.yaml status

### Phase 8: Verification & Testing (QA Agent)
**Claude Code Task:** `TASK-CC-001G`
**Blocked by:** All generated tasks from Phase 7

- Verify all artifacts exist and are complete
- Check cross-references are valid
- Validate file structure
- Run any automated tests
- **Output:** `verification/report.md`

---

## Claude Code Task Integration

### Task Dependencies (blockedBy/addBlocks)

```yaml
# Main task creates children with dependencies
TASK-CC-REPO-ANALYSIS-001:
  children:
    - TASK-CC-001A  # Discovery (no blockers)

    - TASK-CC-001B-1-1  # Repo 1, Cycle 1, Research
    - TASK-CC-001B-1-2  # Repo 1, Cycle 1, Plan [blockedBy: B-1-1]
    - TASK-CC-001B-1-3  # Repo 1, Cycle 1, Execute [blockedBy: B-1-2]
    # ... repeat for 3 cycles per repo

    - TASK-CC-001C  # Planner analysis [blockedBy: all B-*-3]

    - TASK-CC-001D-1  # Deep dive 1 [blockedBy: C]
    - TASK-CC-001D-2  # Deep dive 2 [blockedBy: C]

    - TASK-CC-001E  # Data analysis [blockedBy: all D-*]

    - TASK-CC-001F  # Task generation [blockedBy: E]

    # Generated tasks added to queue.yaml

    - TASK-CC-001G  # Verification [blockedBy: all generated tasks]
```

### Integration with RALF System

1. **Top-level tasks** (TASK-CC-001*) are tracked in Claude Code's Task system
2. **Subagent iterations** use Task tool with subagent_type
3. **RALF queue.yaml** tracks executor work items
4. **Status sync:** When Claude Task completes, update queue.yaml

---

## Success Criteria

- [ ] 5+ Claude Code related repos analyzed
- [ ] 3 iteration cycles completed per repo (15 total)
- [ ] Synthesis report generated
- [ ] Aggregated metrics created
- [ ] 3+ new tasks generated from findings
- [ ] All tasks verified by QA agent
- [ ] All artifacts committed to git

---

## Artifacts

```
6-roadmap/.research/external/GitHub/
├── repos/
│   ├── {owner}-{repo}/
│   │   ├── analysis.md
│   │   ├── structure.yaml
│   │   └── key-findings.md
├── analysis/
│   ├── synthesis-report.md
│   ├── aggregated-metrics.yaml
│   └── patterns-identified.md
└── verification/
    └── report.md
```

---

## Notes

This task demonstrates the full integration:
- Claude Code Task system for orchestration
- RALF queue.yaml for executor work tracking
- Subagents for parallel iteration cycles
- Blocked dependencies for sequencing
