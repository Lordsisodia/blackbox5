# BlackBox5 Roadmap → Project Memory Migration Map

**Created:** 2026-01-20
**Purpose:** Clear mapping of what moves from roadmap to project memory
**Principle:** Roadmap = What we're building next | Project Memory = What we know and why

---

## Part 1: Move to Project Memory `blackbox5/`

These items are **reference knowledge** about the project, not active improvement work.

### From `research/` → `knowledge/research/`

| Source | Destination | Rationale |
|--------|-------------|-----------|
| `BLACKBOX5-RESEARCH-CATEGORIES.md` | `knowledge/research/categories.md` | Reference document for 19 research categories |
| `BLACKBOX5-VISION-AND-FLOW.md` | `project/vision.md` | Core vision document - project identity |
| `FIRST-PRINCIPLES-ANALYSIS.md` | `knowledge/research/first-principles.md` | Foundational project knowledge |
| `VALIDATION-PLAN.md` | `knowledge/research/validation-plan.md` | Reference for validation methodology |
| `README.md` | `knowledge/research/README.md` | Research overview |

### From `first-principles/` → `knowledge/first-principles/`

**All first-principles documents** are project knowledge:

| Source | Destination | Rationale |
|--------|-------------|-----------|
| `first-principles/README.md` | `knowledge/first-principles/README.md` | Overview of first principles work |
| `first-principles/SYSTEM-GUIDE.md` | `knowledge/first-principles/system-guide.md` | System understanding |
| `first-principles/BLACKBOX5-CORE-FLOW.md` | `knowledge/architecture/core-flow.md` | Architecture knowledge |
| `first-principles/ASSUMPTION-REGISTRY.yaml` | `knowledge/first-principles/assumption-registry.yaml` | Assumptions tracking |
| `first-principles/ASSUMPTIONS-LIST.md` | `knowledge/first-principles/assumptions.md` | Assumptions reference |
| `first-principles/COMPREHENSIVE-ASSUMPTIONS-LIST.md` | `knowledge/first-principles/assumptions-comprehensive.md` | Detailed assumptions |
| `first-principles/AUTONOMOUS-SELF-IMPROVEMENT-SYSTEM.md` | `knowledge/first-principles/autonomous-improvement.md` | System design concept |
| `first-principles/RALPH-LOOP-PRD.md` | `plans/features/ralph-loop-prd.md` | Feature PRD |
| `first-principles/features/task-analyzer.md` | `knowledge/architecture/task-analyzer.md` | Architecture component |
| `first-principles/validations/` | `knowledge/first-principles/validations/` | Validation documentation |
| `first-principles/challenges/` | `knowledge/first-principles/challenges/` | Challenge tracking |
| `first-principles/ralph-loop-sessions/` | `knowledge/ralph-loop/sessions/` | Ralph loop research sessions |

### From `frameworks/` → `knowledge/frameworks/`

**Framework research** is reference knowledge:

| Source | Destination | Rationale |
|--------|-------------|-----------|
| `frameworks/README.md` | `knowledge/frameworks/README.md` | Framework overview |
| `frameworks/FRAMEWORKS-SUMMARY.md` | `knowledge/frameworks/summary.md` | Framework summary |
| `frameworks/01-core-agent-frameworks/` | `knowledge/frameworks/core-agent/` | Core agent research |
| `frameworks/06-autonomous-loop-frameworks/` | `knowledge/frameworks/autonomous-loops/` | Loop framework research |
| `frameworks/analysis-docs/` | `knowledge/frameworks/analysis/` | Analysis documentation |
| `frameworks/code-references/` | `knowledge/frameworks/code-references/` | Code reference patterns |

### From `framework-research/ralphy-integration/` → `knowledge/ralph-integration/`

| Source | Destination | Rationale |
|--------|-------------|-----------|
| `framework-research/ralphy-integration/README.md` | `knowledge/ralph-integration/README.md` | Ralph integration overview |
| `framework-research/ralphy-integration/SUMMARY.md` | `knowledge/ralph-integration/summary.md` | Integration summary |
| `framework-research/ralphy-integration/analysis/` | `knowledge/ralph-integration/analysis/` | Integration analysis |
| `framework-research/ralphy-integration/integration-plan/` | `knowledge/ralph-integration/plan/` | Integration plan reference |

### From `archives/` → `knowledge/archives/`

| Source | Destination | Rationale |
|--------|-------------|-----------|
| `archives/ROADMAP-SUMMARY.md` | `knowledge/archives/roadmap-summary.md` | Historical summary |
| `archives/COMPLETE-SUMMARY.md` | `knowledge/archives/complete-summary.md` | Complete history |
| `archives/QUICK-WINS-SUMMARY.md` | `knowledge/archives/quick-wins.md` | Quick wins history |
| `archives/SESSION-SUMMARY.md` | `knowledge/archives/session-summary.md` | Session history |
| `archives/RESUMPTION-POINT.md` | `knowledge/archives/resumption-point.md` | Resumption reference |

### From `02-validation/` → Split destinations

**Validation findings** are knowledge, but validation **activity** could be roadmap:

| Source | Destination | Rationale |
|--------|-------------|-----------|
| `02-validation/CONSOLIDATED-REPORT.md` | `knowledge/validation/consolidated-report.md` | Reference report |
| `02-validation/*/VALIDATION-FINDINGS.md` | `knowledge/validation/agent-{n}-findings.md` | Validation findings |
| `02-validation/*/README.md` | `knowledge/validation/agent-{n}-overview.md` | Agent validation overview |
| `02-validation/*/ARCHITECTURE-DIAGRAM.md` | `knowledge/architecture/agent-{n}-diagram.md` | Architecture diagrams |
| `02-validation/*/SKILLS-SYSTEM-DIAGRAM.md` | `knowledge/architecture/skills-diagram.md` | Skills architecture |
| `02-validation/*/WORKFLOW-DIAGRAM.md` | `knowledge/architecture/workflow-diagram.md` | Workflow architecture |
| `02-validation/*/ACTION-CHECKLIST.md` | `tasks/backlog/validation-actions.md` | Actionable items |

---

## Part 2: Keep in Roadmap `6-roadmap/`

These items are **active improvement work** or the **system for tracking improvements**.

### System Files (Essential - Keep)

| File | Keep As | Rationale |
|------|---------|-----------|
| `STRUCTURE.md` | Same | Roadmap system documentation |
| `QUERIES.md` | Same | Agent query guide for roadmap |
| `STATE.yaml` | Same | Single source of truth for roadmap |
| `INDEX.yaml` | Same | Master index |
| `roadmap.md` | Same | Human dashboard |

### Templates (Essential - Keep)

| Directory | Keep As | Rationale |
|----------|---------|-----------|
| `templates/` | Same | Templates for roadmap items |

### Guides (Essential - Keep)

| Directory | Keep As | Rationale |
|----------|---------|-----------|
| `guides/` | Same | Execution guides for roadmap |

### Proposals (00-proposed) - Keep

**All proposals** are potential future improvements - keep in roadmap.

| Directory | Status | Rationale |
|----------|--------|-----------|
| `00-proposed/PROPOSAL-*/` | Keep | Active improvement proposals |
| `00-proposed/2025-*/` | Keep | Date-based proposals |

### Research Activity (01-research) - Conditional

**Keep active research**, move reference findings:

| Category | Action | Rationale |
|----------|--------|-----------|
| `01-research/agent-types/` | **Keep** | Active research area |
| `01-research/memory-context/` | **Partial move** | Keep logs, move findings to knowledge |
| `01-research/execution-safety/` | **Partial move** | Keep logs, move findings to knowledge |
| `01-research/reasoning-planning/` | **Partial move** | Keep logs, move findings to knowledge |
| `01-research/skills-capabilities/` | **Partial move** | Keep logs, move findings to knowledge |
| `01-research/performance-optimization/` | **Partial move** | Keep logs, move findings to knowledge |
| Other categories | **Keep structure** | Research infrastructure |

**Research logs to keep:**
- `research-log.md` files
- `session-summaries/` folders
- `QUICK-STATUS.md`, `RESEARCH-STATUS-REPORT.md`

**Research findings to move:**
- `findings/` folders → `knowledge/research/{category}/findings/`
- Final summary reports → `knowledge/research/{category}/`

### Design (02-design) - Keep

| Directory | Status | Rationale |
|----------|--------|-----------|
| `02-design/` | Keep | Future design work |

### Validation Activity (02-validation) - Convert

**Convert validation from completed work to templates/future process:**

| Directory | Action | Rationale |
|----------|--------|-----------|
| `02-validation/` | **Archive → Templates** | Validation is complete, keep as template |

### Planned (03-planned) - Keep

| Directory | Status | Rationale |
|----------|--------|-----------|
| `03-planned/PLAN-*/` | Keep | Ready-to-implement improvements |

### Active (04-active) - Keep

| Directory | Status | Rationale |
|----------|--------|-----------|
| `04-active/PLAN-*/` | Keep | Currently implementing |

### Completed (05-completed) - Archive

| Directory | Action | Rationale |
|----------|--------|-----------|
| `05-completed/YYYY/` | **Archive to knowledge** | Completed work is now knowledge |

---

## Part 3: New Structure Overview

### After Migration

```
blackbox5/
├── 5-project-memory/
│   └── blackbox5/                    # NEW: Project memory for BlackBox5
│       ├── project/                  # Project identity & direction
│       │   ├── context.yaml          # Project context
│       │   ├── goals.md              # Main goals
│       │   ├── vision.md             # FROM: research/BLACKBOX5-VISION-AND-FLOW.md
│       │   └── direction.md          # Strategic direction
│       │
│       ├── decisions/                # Why we made choices
│       │   └── architectural/        # Architecture decisions
│       │
│       ├── plans/                    # What we're building
│       │   ├── active/               # Current work (from roadmap 03-04)
│       │   ├── features/             # Feature specs
│       │   │   └── ralph-loop-prd.md # FROM: first-principles/RALPH-LOOP-PRD.md
│       │   └── prds/                 # Product requirements
│       │
│       ├── knowledge/                # What we know
│       │   ├── research/             # Research findings
│       │   │   ├── categories.md     # FROM: research/BLACKBOX5-RESEARCH-CATEGORIES.md
│       │   │   ├── first-principles.md # FROM: research/FIRST-PRINCIPLES-ANALYSIS.md
│       │   │   ├── validation-plan.md # FROM: research/VALIDATION-PLAN.md
│       │   │   ├── agent-types/      # FROM: 01-research/agent-types/findings/
│       │   │   ├── memory-context/   # FROM: 01-research/memory-context/findings/
│       │   │   ├── execution-safety/ # FROM: 01-research/execution-safety/findings/
│       │   │   ├── reasoning-planning/ # FROM: 01-research/reasoning-planning/findings/
│       │   │   ├── skills-capabilities/ # FROM: 01-research/skills-capabilities/findings/
│       │   │   └── performance/      # FROM: 01-research/performance-optimization/findings/
│       │   │
│       │   ├── frameworks/           # Framework research
│       │   │   ├── README.md         # FROM: frameworks/README.md
│       │   │   ├── summary.md        # FROM: frameworks/FRAMEWORKS-SUMMARY.md
│       │   │   ├── core-agent/       # FROM: frameworks/01-core-agent-frameworks/
│       │   │   └── autonomous-loops/ # FROM: frameworks/06-autonomous-loop-frameworks/
│       │   │
│       │   ├── architecture/         # Architecture knowledge
│       │   │   ├── core-flow.md      # FROM: first-principles/BLACKBOX5-CORE-FLOW.md
│       │   │   ├── task-analyzer.md  # FROM: first-principles/features/task-analyzer.md
│       │   │   └── validation/       # Architecture from validation/
│       │   │
│       │   ├── first-principles/     # First principles analysis
│       │   │   ├── README.md         # FROM: first-principles/README.md
│       │   │   ├── system-guide.md   # FROM: first-principles/SYSTEM-GUIDE.md
│       │   │   ├── assumptions.md    # FROM: first-principles/ASSUMPTIONS-LIST.md
│       │   │   ├── assumption-registry.yaml # FROM: first-principles/ASSUMPTION-REGISTRY.yaml
│       │   │   ├── autonomous-improvement.md # FROM: first-principles/AUTONOMOUS-SELF-IMPROVEMENT-SYSTEM.md
│       │   │   ├── validations/      # FROM: first-principles/validations/
│       │   │   └── challenges/       # FROM: first-principles/challenges/
│       │   │
│       │   ├── ralph-integration/    # Ralph integration research
│       │   │   ├── README.md         # FROM: framework-research/ralphy-integration/README.md
│       │   │   ├── summary.md        # FROM: framework-research/ralphy-integration/SUMMARY.md
│       │   │   ├── analysis/         # FROM: framework-research/ralphy-integration/analysis/
│       │   │   └── plan/             # FROM: framework-research/ralphy-integration/integration-plan/
│       │   │
│       │   ├── ralph-loop/           # Ralph loop sessions
│       │   │   └── sessions/         # FROM: first-principles/ralph-loop-sessions/
│       │   │
│       │   ├── validation/           # Validation findings
│       │   │   ├── consolidated-report.md # FROM: 02-validation/CONSOLIDATED-REPORT.md
│       │   │   ├── agent-1-findings.md # FROM: 02-validation/agent-1-core-infrastructure/
│       │   │   ├── agent-2-findings.md # FROM: 02-validation/agent-2-memory-context/
│       │   │   └── ...               # All validation findings
│       │   │
│       │   └── archives/             # Historical records
│       │       ├── roadmap-summary.md # FROM: archives/ROADMAP-SUMMARY.md
│       │       └── ...               # Other archives
│       │
│       ├── tasks/                    # What we're working on
│       │   ├── working/              # Active tasks (from 04-active)
│       │   ├── backlog/              # Backlog tasks
│       │   └── completed/            # Completed tasks
│       │
│       ├── operations/               # System operations
│       │   ├── agents/               # Agent configuration
│       │   ├── architecture/         # Architecture validation
│       │   └── workflows/            # Workflow definitions
│       │
│       └── domains/                  # Domain-specific knowledge
│           └── [existing domains]
│
└── 6-roadmap/                        # Streamlined: Improvement tracking only
    ├── STATE.yaml                    # Single source of truth
    ├── INDEX.yaml                    # Master index
    ├── STRUCTURE.md                  # System documentation
    ├── QUERIES.md                    # Agent query guide
    ├── roadmap.md                    # Human dashboard
    │
    ├── templates/                    # Item templates
    ├── guides/                       # Execution guides
    │
    ├── 00-proposed/                  # Improvement proposals
    │   ├── PROPOSAL-001 through PROPOSAL-019
    │   └── [date-based proposals]
    │
    ├── 01-research/                  # Active research (LOGS ONLY)
    │   ├── agent-types/
    │   │   ├── research-log.md       # Keep
    │   │   ├── session-summaries/    # Keep
    │   │   └── findings/             # → MOVE TO knowledge/research/agent-types/
    │   ├── memory-context/
    │   │   ├── research-log.md       # Keep
    │   │   ├── session-summaries/    # Keep
    │   │   └── findings/             # → MOVE TO knowledge/research/memory-context/
    │   └── [other categories]        # Same pattern
    │
    ├── 02-design/                    # Future: Technical designs
    ├── 03-planned/                   # Ready to implement
    │   └── PLAN-001 through PLAN-010
    ├── 04-active/                    # Currently implementing
    │   └── PLAN-008-fix-critical-api-mismatches
    ├── 05-completed/                 # Shipped improvements
    ├── 06-cancelled/                 # Cancelled items
    └── 07-backlog/                   # Not prioritized
```

---

## Part 4: Key Principles

### What Goes Where?

| Question | Roadmap | Project Memory |
|----------|---------|----------------|
| **What are we building next?** | ✅ Proposals, plans, active work | ❌ |
| **How does it work?** | ❌ | ✅ knowledge/architecture/ |
| **Why did we decide this?** | ❌ | ✅ decisions/ |
| **What have we learned?** | ❌ | ✅ knowledge/research/ |
| **What's the plan?** | ✅ 03-planned/ | ✅ plans/ (strategic) |
| **What are we working on?** | ✅ 04-active/ | ✅ tasks/ (tactical) |

### Decision Flow

```
Is it an improvement to BlackBox5?
├── YES → Is it actively being worked or planned?
│   ├── YES → Roadmap (00-04)
│   └── NO → Roadmap (07-backlog) or discard
└── NO → Is it reference knowledge?
    ├── YES → Project Memory (knowledge/)
    └── NO → Is it a decision?
        ├── YES → Project Memory (decisions/)
        └── NO → Is it project identity?
            ├── YES → Project Memory (project/)
            └── NO → Re-evaluate
```

---

## Part 5: Migration Checklist

### Phase 1: Create Structure

- [ ] Create `5-project-memory/blackbox5/` directory
- [ ] Copy template structure from `_template/`
- [ ] Create initial context.yaml

### Phase 2: Move Reference Knowledge

- [ ] Move `research/` reference docs to `knowledge/research/`
- [ ] Move `first-principles/` to `knowledge/first-principles/`
- [ ] Move `frameworks/` to `knowledge/frameworks/`
- [ ] Move `framework-research/` to `knowledge/ralph-integration/`
- [ ] Move `archives/` to `knowledge/archives/`
- [ ] Move `02-validation/` findings to `knowledge/validation/`

### Phase 3: Extract Research Findings

- [ ] For each `01-research/{category}/`:
  - [ ] Move `findings/` → `knowledge/research/{category}/findings/`
  - [ ] Keep `research-log.md` in roadmap
  - [ ] Keep `session-summaries/` in roadmap
  - [ ] Move summary reports to knowledge

### Phase 4: Clean Up Roadmap

- [ ] Remove moved content from roadmap
- [ ] Update STATE.yaml to reflect changes
- [ ] Update INDEX.yaml
- [ ] Update roadmap.md dashboard
- [ ] Update STRUCTURE.md if needed

### Phase 5: Update Links

- [ ] Update internal links in moved documents
- [ ] Update references from engine code
- [ ] Add redirect notices where helpful

---

**Status:** Ready for execution
**Next Action:** Create project memory structure and begin migration
