# BlackBox5 Claude Code Rules Guide

> **Version:** 1.0.0
> **Created:** 2026-02-06
> **Status:** Draft

---

## Table of Contents

1. [Introduction](#introduction)
2. [Why .claude/rules/ Over skill-registry.yaml](#why-clauderules-over-skill-registryyaml)
3. [Directory Structure](#directory-structure)
4. [Rule File Format](#rule-file-format)
5. [Migration Guide](#migration-guide)
6. [Example Rules](#example-rules)
7. [Auto-Trigger Behavior](#auto-trigger-behavior)
8. [Best Practices](#best-practices)

---

## Introduction

Claude Code's `.claude/rules/` directory provides a **declarative, context-aware instruction system** that replaces manual skill checking and trigger detection. Unlike the current `skill-registry.yaml` approach that requires explicit Phase 1.5 checks, rules automatically apply based on:

- **File paths** being edited
- **Keywords** in user prompts
- **Directory context** of the workspace

This guide shows how BlackBox5 can migrate from the YAML-based skill registry to Claude's native rules system for more seamless, automatic behavior.

---

## Why .claude/rules/ Over skill-registry.yaml

### Current Approach (skill-registry.yaml)

```yaml
# BEFORE: Manual skill checking required
selection:
  triggers: ["architecture", "design", "refactor"]
  confidence_threshold: 70
  when_to_use: "Architecture questions..."
```

**Problems:**
- Requires explicit Phase 1.5 compliance checks
- Manual confidence calculation
- Must document in THOUGHTS.md
- Easy to forget or skip
- Static configuration

### New Approach (.claude/rules/)

```markdown
---
description: "Architecture and Design Rules"
globs: ["**/*.md"]
alwaysApply: false
---

# Architecture Decision Protocol

When user asks architecture questions ("Should we...", "How should we..."):

1. Activate superintelligence protocol
2. Follow 7-step analysis process
3. Return structured recommendation
```

**Benefits:**
- **Automatic application** - No manual checking needed
- **Context-aware** - Applies based on files/paths being edited
- **Composable** - Multiple rules can apply simultaneously
- **Version controlled** - Rules live in repo, tracked with code
- **No THOUGHTS.md boilerplate** - Behavior is implicit

---

## Directory Structure

### Recommended BB5 Layout

```
~/.blackbox5/
├── .claude/                          # NEW: Claude Code configuration
│   ├── rules/                        # Rule files directory
│   │   ├── 00-core-workflow.md       # Core BB5 workflow rules
│   │   ├── 01-superintelligence.md   # Complex problem protocol
│   │   ├── 02-git-safety.md          # Git operation safety
│   │   ├── 03-bmad-skills.md         # BMAD agent triggers
│   │   ├── 04-task-execution.md      # Task/run management
│   │   ├── 05-infrastructure.md      # K8s, Codespaces rules
│   │   └── 99-always-apply.md        # Universal rules
│   └── CLAUDE.md                     # Global BB5 configuration
├── 1-docs/
├── 2-engine/
├── 5-project-memory/
│   └── [project]/
│       └── .claude/
│           └── rules/                # Project-specific rules
├── 6-roadmap/
└── bin/
```

### Rule Naming Convention

| Prefix | Purpose | Example |
|--------|---------|---------|
| `00-` | Core workflow (highest priority) | `00-core-workflow.md` |
| `01-` | Protocols and complex decisions | `01-superintelligence.md` |
| `02-` | Safety and git operations | `02-git-safety.md` |
| `03-` | BMAD agent triggers | `03-bmad-skills.md` |
| `04-` | Task execution | `04-task-execution.md` |
| `05-` | Infrastructure | `05-infrastructure.md` |
| `99-` | Universal/always apply | `99-always-apply.md` |

---

## Rule File Format

### Frontmatter Options

```markdown
---
# Required
description: "Brief description of what this rule does"

# Optional - File path matching
globs:                    # Apply when editing files matching these patterns
  - "**/*.py"
  - "**/specs/**/*.md"
  - "**/.autonomous/**"

# Optional - Directory matching
dirs:                     # Apply when working in these directories
  - "5-project-memory/**"
  - "2-engine/**"

# Optional - Auto-trigger behavior
alwaysApply: false        # If true, applies to ALL prompts
trigger:                  # Keywords that trigger this rule
  - "architecture"
  - "design"
  - "Should we"

# Optional - Priority (higher = applied first)
priority: 10              # Default is 0

# Optional - Rule relationships
requires:                 # Other rules that must also apply
  - "core-workflow"
conflicts:                # Rules that cannot apply together
  - "quick-flow"
---
```

### Markdown Content

After the frontmatter, write instructions in markdown:

```markdown
---
description: "BMAD Architect Agent Rules"
globs: ["**/*.md", "**/*.yaml"]
trigger: ["architecture", "design", "refactor", "structure"]
alwaysApply: false
---

# BMAD Architect Agent

## When to Activate

Activate the architect agent when:
- User asks "Should we..." or "How should we..."
- Keywords: architecture, design, refactor, structure, pattern, scalability
- Task involves multiple systems or complex integration

## Activation Process

1. Read `/Users/shaansisodia/.blackbox5/6-roadmap/01-research/superintelligence-protocol/`
2. Execute 7-step analysis:
   - Context Gathering
   - First Principles
   - Information Gap
   - Active Research
   - Multi-Perspective
   - Meta-Cognitive Check
   - Synthesis

## Output Format

```
**Recommendation:** [Clear answer]
**Confidence:** [0-100%]
**Key Assumptions:** [What we're betting on]
**Risks:** [What could go wrong]
**Implementation Path:** [Next steps]
```

## Stop Conditions

- PAUSE if requirements are unclear
- EXIT with PARTIAL if context exceeds 85%
```

---

## Migration Guide

### Converting skill-registry.yaml to Rules

#### Step 1: Map Skills to Rule Files

| Skill ID | Rule File | Trigger Type |
|----------|-----------|--------------|
| `bmad-pm` | `03-bmad-pm.md` | Keywords: PRD, requirements, feature |
| `bmad-architect` | `03-bmad-architect.md` | Keywords: architecture, design, "Should we" |
| `bmad-analyst` | `03-bmad-analyst.md` | Keywords: analyze, research, investigate |
| `bmad-sm` | `03-bmad-sm.md` | Keywords: sprint, process, coordinate |
| `bmad-ux` | `03-bmad-ux.md` | Keywords: UI, UX, design, interface |
| `bmad-dev` | `03-bmad-dev.md` | Keywords: implement, code, develop |
| `bmad-qa` | `03-bmad-qa.md` | Keywords: test, quality, QA, verify |
| `superintelligence-protocol` | `01-superintelligence.md` | Keywords: "Should we", "How should we", complex |
| `git-commit` | `02-git-safety.md` | globs: ["**/.git/**"], keywords: commit, PR |
| `supabase-operations` | `05-supabase.md` | globs: ["**/supabase/**"], keywords: supabase, RLS |

#### Step 2: Extract Skill Content

From skill-registry.yaml:

```yaml
bmad-architect:
  name: "System Architect"
  description: "System design, architecture, and patterns"
  selection:
    triggers: ["architecture", "design", "refactor", "structure", "pattern", "scalability"]
    confidence_threshold: 70
    when_to_use: "Architecture questions, design decisions, refactoring, integration planning"
    when_to_avoid: "Quick fixes, documentation-only tasks"
```

To rule file:

```markdown
---
description: "BMAD Architect Agent - System design and architecture"
trigger: ["architecture", "design", "refactor", "structure", "pattern", "scalability"]
alwaysApply: false
---

# BMAD Architect Agent

## When to Use

Activate for:
- Architecture questions
- Design decisions
- Refactoring planning
- Integration planning
- Keywords: architecture, design, refactor, structure, pattern, scalability

## When to Avoid

- Quick fixes (< 30 min)
- Documentation-only tasks
- Simple, single-file changes

## Activation Confidence

Minimum 70% confidence required. Calculate based on:
- Keyword match (40%)
- Task type alignment (30%)
- Complexity fit (20%)
- Historical success (10%)
```

#### Step 3: Remove Phase 1.5 Boilerplate

**Before (in THOUGHTS.md):**
```markdown
## Skill Usage for This Task

- Applicable skills found: bmad-architect, bmad-analyst
- Skill invoked: bmad-architect
- Confidence: 85%
- Rationale: Task involves architecture decisions
```

**After:**
- No documentation needed - rules apply automatically
- Optional: Note which rule activated in DECISIONS.md

#### Step 4: Update CLAUDE.md

Remove Phase 1.5 section and replace with:

```markdown
## Rule-Based Skill Activation

Claude Code automatically applies rules from `.claude/rules/` based on:
- File paths being edited
- Keywords in prompts
- Directory context

Rules are defined in YAML frontmatter with markdown content.
See `.docs/CLAUDE-RULES-GUIDE.md` for details.
```

---

## Example Rules

### Example 1: Superintelligence Protocol Trigger

**File:** `.claude/rules/01-superintelligence.md`

```markdown
---
description: "Superintelligence Protocol - Complex problem solving"
trigger:
  - "Should we"
  - "How should we"
  - "What's the best way"
  - "best approach"
  - "architecture"
  - "design"
  - "refactor"
  - "optimize"
  - "strategy"
  - "complex"
  - "integrate"
alwaysApply: false
priority: 100
---

# Superintelligence Protocol

## Auto-Activation Triggers

**Activate WITHOUT asking when:**
- User asks architecture/design questions ("Should we...", "How should we...")
- Task involves multiple files or systems
- High uncertainty or novel problem
- User seems to be making a significant decision
- Keywords: architecture, design, refactor, optimize, strategy, complex, integrate

**Don't activate for:**
- Simple file edits
- Clear bug fixes
- Information lookups
- Routine tasks

## 7-Step Process

When activated:

1. **Context Gathering**
   - Scan relevant projects/folders
   - Use sub-agents for large codebases
   - Cache context for reuse

2. **First Principles**
   - Break down the problem
   - Identify core requirements
   - Question assumptions

3. **Information Gap**
   - Identify unknowns
   - List missing information
   - Note areas of uncertainty

4. **Active Research**
   - Search codebase
   - Verify patterns
   - Test assumptions

5. **Multi-Perspective**
   - Deploy expert agents as needed:
     - **Architect** - System design, patterns, scalability
     - **Researcher** - Information gathering, best practices
     - **Critic** - Risk analysis, edge cases, failure modes
     - **Synthesizer** - Integration of multiple perspectives

6. **Meta-Cognitive Check**
   - Verify reasoning
   - Check for biases
   - Validate assumptions

7. **Synthesis**
   - Integrate into recommendation
   - Structure output clearly

## Output Format

Always return:

```
**Recommendation:** [Clear answer]
**Confidence:** [0-100%]
**Key Assumptions:** [What we're betting on]
**Risks:** [What could go wrong]
**Implementation Path:** [Next steps]
```

## Examples

**User:** "Should we refactor the auth system?"
→ **Response:** "I'll activate the superintelligence protocol for this." [Proceed with 7-step analysis]

**User:** "Fix this typo"
→ **Response:** [Fix directly, no protocol needed]
```

---

### Example 2: Git Safety Rules

**File:** `.claude/rules/02-git-safety.md`

```markdown
---
description: "Git operation safety and best practices"
globs:
  - "**/.git/**"
  - "**/.gitignore"
trigger:
  - "commit"
  - "git"
  - "PR"
  - "branch"
  - "merge"
  - "repository"
alwaysApply: false
priority: 90
---

# Git Safety Protocol

## Safety Rules

### NEVER do these:
- `git push --force` to main/master (unless explicitly requested)
- `git reset --hard` without confirming
- Skip hooks with `--no-verify` (unless user explicitly requests)
- Amend commits that have been pushed
- Run destructive commands without backup

### ALWAYS do these:
- Create new branch for changes: `git checkout -b claude/[task-slug]`
- Stage specific files (not `git add -A`)
- Write descriptive commit messages with:
  - Component name
  - Description
  - Task ID
  - Validation results
- Use HEREDOC for multi-line commits

## Commit Message Format

```bash
git commit -m "$(cat <<'EOF'
[component]: [description]

- Detailed change 1
- Detailed change 2
- Task: [TASK-ID]
- Validation: [results]

Co-authored-by: Claude <claude@blackbox5.local>
EOF
)"
```

## Pre-Commit Checklist

- [ ] No secrets in staged files (.env, credentials.json)
- [ ] No large binaries accidentally included
- [ ] Tests pass (if applicable)
- [ ] Linting passes (if applicable)

## Branch Naming

- Format: `claude/[task-slug]`
- Examples:
  - `claude/TASK-123-fix-auth-bug`
  - `claude/TASK-456-add-user-profile`
```

---

### Example 3: BMAD Skills Trigger

**File:** `.claude/rules/03-bmad-skills.md`

```markdown
---
description: "BMAD Agent skill activation rules"
alwaysApply: true
priority: 50
---

# BMAD Agent Skill Activation

## Automatic Triggers

| Domain | Agent | Trigger Keywords | Confidence |
|--------|-------|------------------|------------|
| **Product Management** | John (bmad-pm) | PRD, requirements, feature definition, roadmap, user story, epic | 70% |
| **Architecture** | Alex (bmad-architect) | architecture, design, refactor, integrate | 70% |
| **Research/Analysis** | Mary (bmad-analyst) | research, analyze, pattern, investigate | 70% |
| **Scrum/Process** | Sam (bmad-sm) | sprint, process, coordination, planning | 70% |
| **UX/Design** | Uma (bmad-ux) | UI, UX, design, user flow, interface | 70% |
| **Development** | Amelia (bmad-dev) | implement, code, test, review | 70% |
| **QA/Testing** | Quinn (bmad-qa) | test strategy, quality, test plan | 70% |
| **Task Execution** | TEA (bmad-tea) | RALF, autonomous, execute workflow | 70% |
| **Quick Tasks** | Barry (bmad-quick-flow) | simple, quick fix, straightforward | 70% |

## Activation Process

When keywords match:

1. Calculate confidence using:
   ```
   confidence = (keyword_match * 0.40) +
                (type_alignment * 0.30) +
                (complexity_fit * 0.20) +
                (historical_success * 0.10)
   ```

2. If confidence >= 70%:
   - Read agent's SKILL.md file
   - Follow agent's defined process
   - Document in RESULTS.md

3. If confidence < 70%:
   - Proceed with standard execution
   - Note in THOUGHTS.md: "Agent X considered but confidence too low (Y%)"

## Agent Directory Structure

Agents are located at:
```
~/.blackbox5/2-engine/.autonomous/agents/[agent-name]/
├── SKILL.md          # Agent instructions
├── personality.yaml  # Agent configuration
└── tools/            # Agent-specific tools
```
```

---

### Example 4: Task Execution Rules

**File:** `.claude/rules/04-task-execution.md`

```markdown
---
description: "BlackBox5 task execution workflow"
globs:
  - "**/.autonomous/**"
  - "**/tasks/**"
  - "**/runs/**"
alwaysApply: true
priority: 80
---

# BB5 Task Execution Protocol

## For EVERY New Task

### 1. Create/Use Workspace
- Work in `~/.blackbox5/5-project-memory/[project]/.autonomous/`
- Create run folder: `runs/run-YYYYMMDD_HHMMSS/`
- Initialize with: THOUGHTS.md, DECISIONS.md, ASSUMPTIONS.md, LEARNINGS.md, RESULTS.md
- Check `CURRENT_CONTEXT.md` for auto-discovered context

### 2. Select ONE Task
- Use `bb5 task:list` to see pending tasks
- Use `bb5 task:current` to see current task
- Read task file completely before starting
- **ONE task per session** - never batch multiple tasks

### 3. Track Progress
- Update `fix_plan.md` after each task completion
- Update `prd.json` with task status
- Document in run folder files

### 4. Commit & Update BlackBox5
```bash
git checkout -b claude/[task-slug]
git add [files]
git commit -m "claude: [component] [description]

- Detailed changes
- Task: [TASK-ID]
- Validation: [results]

Co-authored-by: Claude <claude@blackbox5.local>"
git push origin claude/[task-slug]
```

### 5. Exit Properly
- Return `PROMISE_COMPLETE` when done
- Status: COMPLETE | PARTIAL | BLOCKED
- Document next steps

## Sub-Agent Rules

**ALWAYS spawn sub-agents when:**
- Searching across >15 files
- Complex pattern matching needed (regex, multiline searches)
- Cross-project exploration (>2 projects involved)
- Estimated search time >5 minutes
- Open-ended codebase exploration
- Validation of complex work

**USE DIRECT READS when:**
- <15 files needed
- Files at known paths
- Simple pattern matching (single grep)
- Known directory structure
- Implementation work (do it yourself)

## Stop Conditions

**PAUSE and ask user when:**
1. Unclear Requirements
2. Scope Creep
3. Blocked on external input
4. High Risk change
5. Context Overflow (85% token usage)
6. Contradiction found
7. No Clear Path

**EXIT with status when:**
- COMPLETE: All success criteria met
- PARTIAL: Progress made, more work needed
- BLOCKED: Cannot proceed without human input
```

---

### Example 5: Infrastructure Rules

**File:** `.claude/rules/05-infrastructure.md`

```markdown
---
description: "Infrastructure and deployment rules"
globs:
  - "**/k8s/**"
  - "**/kubernetes/**"
  - "**/.github/codespaces/**"
  - "**/infrastructure/**"
trigger:
  - "RALF"
  - "K8s"
  - "Kubernetes"
  - "Codespaces"
  - "deploy"
  - "infrastructure"
alwaysApply: false
priority: 40
---

# Infrastructure Protocol

## RALF Cloud Control

**When to use:** RALF agent management, K8s operations
**When to avoid:** Local development, non-infrastructure work

### Commands
- Spawn agent: `ralf spawn [agent-type]`
- Check status: `ralf status`
- Scale: `ralf scale [count]`

## GitHub Codespaces Control

**When to use:** GitHub Codespaces agent spawning
**When to avoid:** Local development, non-Codespaces work

### Process
1. Check Codespaces quota
2. Spawn agent with proper labels
3. Monitor agent health
4. Cleanup on completion

## Safety Rules

- Never deploy to production without approval
- Always test in staging first
- Use proper labels for all resources
- Monitor resource usage
- Cleanup temporary resources
```

---

## Auto-Trigger Behavior

### How Rules Are Applied

1. **Path Matching**
   - Rules with `globs` matching edited files are loaded
   - Rules with `dirs` matching current directory are loaded

2. **Keyword Matching**
   - Rules with `trigger` keywords found in prompt are loaded
   - Partial matches count (e.g., "architect" matches "architecture")

3. **Always Apply**
   - Rules with `alwaysApply: true` are always loaded
   - Use sparingly to avoid context bloat

4. **Priority Ordering**
   - Rules sorted by `priority` (higher first)
   - Within same priority, alphabetical by filename

### Rule Composition

Multiple rules can apply simultaneously:

```
User prompt: "Should we refactor the auth system?"

Rules triggered:
1. 01-superintelligence.md (trigger: "Should we")
2. 02-git-safety.md (alwaysApply: true)
3. 03-bmad-architect.md (trigger: "refactor")
4. 04-task-execution.md (alwaysApply: true)

Result: All rules' instructions are combined and applied
```

### Conflict Resolution

If rules conflict:
- Higher priority wins
- If same priority, later filename wins (alphabetically)
- Use `conflicts` frontmatter to explicitly prevent combinations

---

## Best Practices

### Naming Conventions

1. **Use numeric prefixes** for ordering (00-, 01-, etc.)
2. **Use descriptive names** that indicate purpose
3. **Group related rules** with same prefix
4. **Reserve 99-** for universal rules

### Organization

```
.claude/rules/
├── 00-core-workflow.md      # Essential BB5 workflow
├── 01-superintelligence.md  # Complex problem protocol
├── 02-git-safety.md         # Git operations
├── 03-bmad-pm.md            # Product management
├── 03-bmad-architect.md     # Architecture
├── 03-bmad-analyst.md       # Research
├── 03-bmad-dev.md           # Development
├── 03-bmad-qa.md            # Quality assurance
├── 04-task-execution.md     # Task/run management
├── 05-infrastructure.md     # K8s, Codespaces
└── 99-always-apply.md       # Universal rules
```

### Maintenance

1. **Version control** - Rules live in repo
2. **Test changes** - Verify rule triggers correctly
3. **Document decisions** - Use DECISIONS.md for rule changes
4. **Review periodically** - Check for outdated rules
5. **Keep focused** - One rule per concern

### Performance

1. **Minimize alwaysApply rules** - They load on every prompt
2. **Use specific globs** - Avoid `**/*` when possible
3. **Keep rules concise** - Long rules consume context
4. **Use priority wisely** - Critical rules first

### Migration Checklist

- [ ] Create `.claude/rules/` directory
- [ ] Convert each skill to rule file
- [ ] Test rule triggers
- [ ] Update CLAUDE.md to remove Phase 1.5
- [ ] Archive skill-registry.yaml
- [ ] Document in LEARNINGS.md

---

## Appendix: Complete Rule Reference

### Frontmatter Schema

```yaml
---
# Required
description: string

# Optional - Matching
globs: string[]
dirs: string[]
trigger: string[]

# Optional - Behavior
alwaysApply: boolean    # default: false
priority: number        # default: 0
requires: string[]      # rule IDs that must also apply
conflicts: string[]     # rule IDs that cannot apply

# Optional - Metadata
tags: string[]
author: string
created: date
updated: date
version: string
---
```

### Rule Template

```markdown
---
description: "[Brief description]"
globs: ["**/*.ext"]
trigger: ["keyword1", "keyword2"]
alwaysApply: false
priority: 50
---

# [Rule Title]

## When to Apply

- Condition 1
- Condition 2

## Instructions

1. Step one
2. Step two
3. Step three

## Stop Conditions

- When to pause
- When to exit

## Examples

**Input:** "..."
**Output:** "..."
```

---

*End of Guide*
