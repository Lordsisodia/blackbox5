---
name: BlackBox5 Project Configuration
version: 1.0.0
project: blackbox5
hierarchy: project
---

# BlackBox5 Project CLAUDE.md

This file contains BlackBox5-specific instructions. It extends the global `~/.claude/CLAUDE.md` with project-level workflows and commands.

## Hierarchy Loading Order

1. **Global** (`~/.claude/CLAUDE.md`) - Universal coding standards
2. **Project** (this file) - BlackBox5-specific workflows
3. **Rules** (`.claude/rules/*.md`) - Specific behavioral rules
4. **Task** (task-level CLAUDE.md when present) - Task-specific context

---

## BlackBox5 Navigation Commands

Use the `bb5` CLI to navigate the goals/plans/tasks hierarchy:

### Navigation
- `bb5 whereami` - Show current location in hierarchy
- `bb5 goal:list` - List all goals
- `bb5 goal:show [ID]` - Show goal details
- `bb5 plan:list` - List all plans
- `bb5 plan:show [ID]` - Show plan details
- `bb5 task:list` - List all tasks
- `bb5 task:show [ID]` - Show task details
- `bb5 task:current` - Show current task
- `bb5 up` - Go up one level (task → plan → goal)
- `bb5 down [ID]` - Go down to child
- `bb5 root` - Go to project root
- `bb5 goto [ID]` - Jump to specific item

### Creating Items
- `bb5 goal:create "Goal Name"` - Create new goal from template
- `bb5 plan:create "Plan Name"` - Create new plan from template
- `bb5 task:create "Task Name"` - Create new task from template
- `bb5 subtask:create "Subtask Name"` - Create subtask (run from task dir)

### Linking Items
- `bb5 link:goal [GOAL-ID]` - Link current plan to goal
- `bb5 link:plan [PLAN-ID]` - Link current task to plan

---

## BlackBox5 Workflow Integration

### Workspace & Task Management

**For EVERY new task, you MUST:**

1. **Create/Use Workspace**
   - Work in `~/.blackbox5/5-project-memory/[project]/.autonomous/`
   - Create run folder: `runs/run-YYYYMMDD_HHMMSS/`
   - Initialize with: THOUGHTS.md, DECISIONS.md, ASSUMPTIONS.md, LEARNINGS.md, RESULTS.md
   - Check `CURRENT_CONTEXT.md` for auto-discovered context

2. **Select ONE Task**
   - Use `bb5 task:list` to see pending tasks
   - Use `bb5 task:current` to see current task
   - Read task file completely before starting
   - ONE task per session - never batch multiple tasks

3. **Track Progress**
   - Update `fix_plan.md` after each task completion
   - Update `prd.json` with task status
   - Document in run folder files

4. **Commit & Update BlackBox5**
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

5. **Exit Properly**
   - Return `PROMISE_COMPLETE` when done
   - Status: COMPLETE | PARTIAL | BLOCKED
   - Document next steps

---

## BlackBox5 Directory Structure

```
~/.blackbox5/
├── 1-docs/              # Documentation
├── 2-engine/            # Core engine (RALF, agents)
├── 5-project-memory/    # Project workspaces
│   └── [project]/
│       └── .autonomous/
│           ├── tasks/active/      # Pending tasks
│           ├── tasks/completed/   # Done tasks
│           ├── runs/              # Session history
│           ├── memory/            # Insights, decisions
│           └── timeline/          # Project timeline
├── 6-roadmap/           # Plans and roadmaps
└── bin/                 # Executables
```

---

## Integration with Superintelligence Protocol

When working on BlackBox5:
- Reference the Superintelligence Protocol at `/Users/shaansisodia/.blackbox5/6-roadmap/01-research/superintelligence-protocol/`
- Use the Project Scanner for context gathering
- Follow the Iterative Improvement Framework
- Document learnings in the protocol research directory
- Update BlackBox5 state after every significant change

---

## Task File Format

Tasks in `tasks/active/` follow this structure:

```markdown
# TASK-[ID]: [Title]

**Status:** pending | in_progress | completed
**Priority:** CRITICAL | HIGH | MEDIUM | LOW
**Created:** YYYY-MM-DDTHH:MM:SSZ

## Objective
Clear one-sentence goal.

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Context
Background information needed to complete the task.

## Approach
1. Step 1
2. Step 2

## Rollback Strategy
How to undo if things go wrong.
```

---

## Decision Framework

### When to Just Do It
- Clear bug fix (< 30 min)
- Simple edit (< 10 min)
- Documentation typo
- Single file change

### When to Create Formal Task
- > 30 minutes of work
- Touches multiple files
- Requires research
- Has dependencies

### When to Hand Off to RALF
- Task queue is empty (let RALF generate)
- Requires continuous iteration
- Long-running improvement
- Fits RALF's autonomous loop pattern

### When to Ask User
- Requirements unclear
- Scope creep detected
- External dependency blocked
- High-risk change (affects critical path)
- Uncertain about approach

---

## Project Rules

This project uses the rules-based approach. See `.claude/rules/` for specific behavioral rules:

1. **001-one-task-per-session.md** - One task per session rule
2. **002-read-before-change.md** - Read before change rule
3. **003-git-safety.md** - Git safety protocol
4. **004-phase-1-5-skill-check.md** - Mandatory skill checking
5. **005-superintelligence-auto-activation.md** - Superintelligence protocol activation
6. **006-stop-conditions.md** - When to pause and exit
7. **007-sub-agent-deployment.md** - Sub-agent deployment rules
8. **008-output-style.md** - Output style guidelines

---

## Skill Selection for BlackBox5

**Phase 1.5: Mandatory Skill Checking (CRITICAL)**

BEFORE starting Phase 2 (Execution) of ANY task, you MUST:

1. **Read skill-selection.yaml** at `~/.blackbox5/5-project-memory/blackbox5/operations/skill-selection.yaml`
2. **Check domain_mapping** for matching keywords in your task
3. **Calculate confidence** using the formula in the file
4. **Document decision** in THOUGHTS.md under "## Skill Usage for This Task"

**Auto-Trigger Rules:**

| Trigger Condition | Action Required |
|-------------------|-----------------|
| Task contains "implement" + domain keyword (git, n8n, supabase, etc.) | MUST check for matching skill |
| Task contains "analyze" or "research" | MUST check bmad-analyst, web-search |
| Task contains "architecture", "design", "refactor" | MUST check bmad-architect |
| Task contains "Should we...", "How should we..." | MUST check superintelligence-protocol |
| Task contains "PRD", "requirements", "feature" | MUST check bmad-pm |
| Task contains "test", "QA", "quality" | MUST check bmad-qa |
| Multiple files or systems involved | MUST check relevant skills |

### Domain-to-Skill Mapping

| Domain | Skill | Trigger Keywords | Confidence Threshold |
|--------|-------|------------------|---------------------|
| **Product Management** | `bmad-pm` | PRD, requirements, feature definition | 70% |
| **Architecture** | `bmad-architect` | architecture, design, refactor, integrate | 70% |
| **Research/Analysis** | `bmad-analyst` | research, analyze, pattern, investigate | 70% |
| **Scrum/Process** | `bmad-sm` | sprint, process, coordination, planning | 70% |
| **UX/Design** | `bmad-ux` | UI, UX, design, user flow, interface | 70% |
| **Development** | `bmad-dev` | implement, code, test, review | 70% |
| **QA/Testing** | `bmad-qa` | test strategy, quality, test plan | 70% |
| **Task Execution** | `bmad-tea` | RALF, autonomous, execute workflow | 70% |
| **Quick Tasks** | `bmad-quick-flow` | simple, quick fix, straightforward | 70% |
| **Complex Problems** | `superintelligence-protocol` | "Should we...", "How should we...", architecture, strategy | 70% |
| **Continuous Improvement** | `continuous-improvement` | improve, optimize, refine, iterate | 70% |
| **Git Operations** | `git-commit` | commit, PR, git workflow | 70% |
| **Codebase Navigation** | `codebase-navigation` | find code, explore, understand structure | 70% |
| **Supabase/Database** | `supabase-operations` | supabase, database, RLS, migration | 70% |
| **Web Research** | `web-search` | search, current events, documentation | 70% |

---

## Context Management

- **70% context usage:** Summarize THOUGHTS.md
- **85% context usage:** Complete current task, exit with PARTIAL
- **95% context usage:** Force checkpoint, exit immediately
