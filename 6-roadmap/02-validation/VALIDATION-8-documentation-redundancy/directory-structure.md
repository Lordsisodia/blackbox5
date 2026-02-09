# BlackBox5 Directory Structure Documentation

## Complete Directory Tree

```
blackbox5/
│
├── 1-docs/                              # 162 files
│   ├── .docs/                           # Documentation about docs
│   ├── 01-theory/                       # Theoretical foundations
│   │   ├── 01-architecture/             # Architecture patterns
│   │   │   ├── anti-patterns/           # Anti-patterns to avoid
│   │   │   ├── core/                    # Core architecture docs
│   │   │   └── patterns/                # Design patterns
│   │   ├── 02-memory/                   # Memory system design
│   │   │   ├── design/                  # Memory architecture
│   │   │   ├── planning/                # Planning memory
│   │   │   └── separation/              # Memory separation concerns
│   │   ├── 03-workflows/                # Workflow definitions
│   │   │   ├── adaptive/                # Adaptive workflows
│   │   │   ├── production/              # Production workflows
│   │   │   └── spec-driven/             # Spec-driven development
│   │   └── 04-first-principles/         # First principles analysis (now in 1-docs/core)
│   │       ├── analysis/                # Analytical frameworks
│   │       └── framework-analysis/      # Framework comparisons
│   │
│   ├── 02-implementation/               # Implementation guides
│   │   ├── 01-agents/                   # Agent implementations
│   │   │   ├── epic/                    # Epic agent
│   │   │   ├── parallel/                # Parallel execution
│   │   │   └── task/                    # Task agent
│   │   ├── 01-core/                     # Core systems
│   │   │   ├── communication/           # Event bus
│   │   │   ├── general/                 # General core components
│   │   │   ├── integration/             # MCP integration
│   │   │   ├── middleware/              # Guide middleware
│   │   │   ├── orchestration/           # Orchestrator
│   │   │   ├── resilience/              # Circuit breakers
│   │   │   └── state/                   # State management
│   │   ├── 02-core-systems/             # Core GSD systems
│   │   │   ├── atomic-commits/          # Atomic commits
│   │   │   ├── checkpoint/              # Checkpoint protocol
│   │   │   ├── deviation/               # Deviation handling
│   │   │   └── state-management/        # State management
│   │   ├── 03-pipeline/                 # Pipeline systems
│   │   │   ├── feature/                 # Feature pipeline
│   │   │   ├── gsd/                     # GSD pipeline
│   │   │   └── spec-driven/             # Spec-driven pipeline
│   │   ├── 04-integrations/             # External integrations
│   │   │   ├── github/                  # GitHub integration
│   │   │   ├── mcp/                     # MCP integration
│   │   │   └── ralph/                   # Ralph integration
│   │   ├── 05-memory-implementation/    # Memory implementations
│   │   │   ├── context/                 # Context extraction
│   │   │   ├── project-memory/          # Project memory
│   │   │   ├── todo/                    # Todo management
│   │   │   └── token-compression/       # Token compression
│   │   ├── 06-tools/                    # Tool implementations
│   │   │   ├── skills/                  # Skills system
│   │   │   └── tools/                   # Tools system
│   │   └── 07-task-management/          # Task management
│   │       ├── design/                  # Design docs
│   │       └── wave-execution/          # Wave execution
│   │
│   ├── 03-guides/                       # User guides
│   │   ├── 01-getting-started/          # Getting started
│   │   │   ├── quickstart/              # Quickstart guides
│   │   │   ├── setup/                   # Setup guides
│   │   │   └── status/                  # Status checks
│   │   ├── 02-cli/                      # CLI documentation
│   │   │   ├── guides/                  # CLI guides
│   │   │   └── reference/               # CLI reference
│   │   ├── 02-tutorials/                # Tutorials
│   │   ├── 03-roadmap/                  # Roadmap docs
│   │   │   ├── design/                  # Design roadmaps
│   │   │   ├── implementation/          # Implementation roadmaps
│   │   │   └── strategy/                # Strategy docs
│   │   ├── 04-reference/                # Reference material
│   │   │   ├── inventory/               # File inventory
│   │   │   └── summaries/               # Topic summaries
│   │   │
│   ├── 04-project/                      # Project-specific docs
│   │   ├── competitive/                 # Competitive analysis
│   │   ├── meta/                        # Meta documentation
│   │   └── planning/                    # Project planning
│   │
│   └── 05-examples/                     # Examples
│       ├── code/                        # Code examples
│       └── guides/                      # Example guides
│
├── 2-engine/                            # Engine implementation
│   ├── 01-core/                         # Core engine
│   ├── 02-agents/                       # Agent implementations
│   ├── 03-knowledge/                    # Knowledge storage
│   ├── 04-work/                         # Work management
│   ├── 05-tools/                        # Tool implementations
│   ├── 06-integrations/                 # Integration modules
│   ├── 07-operations/                   # Operations tools
│   └── 08-development/                  # Development tools
│
├── 3-gui/                               # GUI components
│   ├── web/                             # Web interface
│   └── cli/                             # CLI interface
│
├── 5-project-memory/                    # 311 files - Active project memory
│   ├── .docs/                           # Documentation about structure
│   ├── _template/                       # Template structure
│   │   ├── blackbox/                    # Blackbox templates
│   │   │   └── _template/               # Nested templates
│   │   │       ├── agents/              # Agent templates
│   │   │       ├── experiments/         # Experiment templates
│   │   │       ├── snippets/            # Snippet templates
│   │   │       └── ...                  # More templates
│   │   ├── knowledge/                   # Knowledge templates
│   │   ├── plans/                       # Plan templates
│   │   └── project/                     # Project templates
│   │
│   └── siso-internal/                   # Active project memory
│       ├── knowledge/                   # Knowledge base
│       │   └── codebase/                # Codebase documentation
│       ├── operations/                  # Operations records
│       │   ├── agents/                  # Agent history
│       │   │   └── history/             # Session history
│       │   │       └── sessions/        # Individual sessions
│       │   └── ...                      # More operations
│       ├── plans/                       # Active plans
│       │   ├── prds/                    # PRD documents
│       │   └── ...                      # More plans
│       ├── decisions/                   # Decision records
│       │   ├── scope/                   # Scope decisions
│       │   ├── architectural/           # Architectural decisions
│       │   └── technical/              # Technical decisions
│       └── tasks/                       # Task records
│
├── 6-roadmap/                           # 138 files - Roadmap & planning
│   ├── .docs/                           # Documentation about roadmap
│   ├── 00-proposed/                     # Proposed research
│   │   ├── agent-types-research.md
│   │   ├── communication-collaboration-research.md
│   │   └── ...                          # 18 research topics
│   ├── 01-research/                     # Research status
│   │   ├── FINAL-STATUS-REPORT.md
│   │   ├── RESEARCH-ALL-COMPLETE.md
│   │   └── ...                          # Status reports
│   ├── 02-active/                       # Active work items
│   ├── 03-completed/                    # Completed items
│   ├── 04-archived/                     # Archived items
│   ├── 02-validation/                   # Validation reports
│   │   └── agent-8-documentation-redundancy/
│   │       ├── VALIDATION-FINDINGS.md   # This report
│   │       ├── cleanup-scripts.sh       # Cleanup scripts
│   │       ├── detailed-analysis.md     # Detailed analysis
│   │       └── directory-structure.md   # This file
│   ├── templates/                       # Roadmap templates
│   │   ├── design-template.md
│   │   ├── active-template.md
│   │   ├── completed-template.md
│   │   ├── proposal-template.md
│   │   ├── research-template.md
│   │   └── plan-template.md
│   ├── first-principles/                # MOVED to 1-docs/core/
│   ├── BLACKBOX5-RESEARCH-CATEGORIES.md
│   └── COMPLETE-SUMMARY.md
│
├── vibe-kanban/                         # 907 files - Project management
│   ├── node_modules/                    # ~850 files (NOT documentation)
│   ├── crates/                          # Rust source code
│   │   ├── db/                          # Database modules
│   │   ├── remote/                      # Remote execution
│   │   └── ...                          # More crates
│   ├── docs/                            # Actual documentation (~57 files)
│   ├── npx-cli/                         # CLI tools
│   └── ...                              # More project files
│
├── 01-core/                             # Core system files
│   └── .docs/
│
├── config.yml                           # Configuration
├── CORE-INFRASTRUCTURE-COMPLETE.md      # Core status
└── README.md                             # Main README
```

## File Type Distribution

### Markdown Files by Extension:
- `.md` files: 2,702 total
- `.md` in 1-docs: 162
- `.md` in 5-project-memory: 311
- `.md` in 6-roadmap: 138
- `.md` in vibe-kanban: 907
- `.md` in other: 1,184

### Code Files:
- TypeScript (.ts): ~500
- Python (.py): ~200
- Rust (.rs): ~300
- Shell (.sh): ~50

## Key Directories to Watch

### High Redundancy Areas:
1. `5-project-memory/_template/` - Many template duplicates
2. `5-project-memory/siso-internal/operations/agents/history/sessions/` - Old session data
3. `vibe-kanban/node_modules/` - Not documentation (exclude from analysis)

### High Value Areas:
1. `1-docs/01-theory/` - Core theoretical documentation
2. `1-docs/02-implementation/01-core/` - Core system documentation
3. `6-roadmap/` - Planning and status tracking

### Cleanup Candidates:
1. Orphaned implementation summaries (20+ files)
2. Duplicate code_index files (3 identical copies)
3. Empty README files (30+ files)
4. Old session output files (26+ files)

---

**End of Directory Structure Documentation**
