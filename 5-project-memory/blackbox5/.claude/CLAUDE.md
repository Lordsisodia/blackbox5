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

1. **Read skill-selection.yaml** at `~/.blackbox5/5-project-memory/blackbox5/operations/skill-registry.yaml` (section: selection_framework)
2. **Check domain_mapping** for matching keywords in your task
3. **Calculate confidence** using the formula in the file
4. **Document decision** in THOUGHTS.md under "## Skill Usage for This Task"

### Clear vs Discretionary Triggers

| Confidence | Action | Override Allowed |
|------------|--------|------------------|
| **>= 85%** | MUST invoke | NO - Automatic |
| **70-84%** | SHOULD invoke | YES - Agent discretion |
| **< 70%** | MAY check | YES - Agent discretion |

### Clear Trigger Examples (85%+ confidence)
- "implement" + exact domain match (e.g., "implement git commit")
- "Should we..." + architecture keyword
- "PRD" + feature definition

### Discretionary Examples (70-84% confidence)
- "implement" + related domain
- "analyze" + partial match
- "test" + unclear scope

**Auto-Trigger Rules:**

| Trigger Condition | Confidence | Action Required | Override Allowed |
|-------------------|------------|-----------------|------------------|
| "implement" + exact domain match (e.g., "implement git commit") | >= 85% | MUST invoke | NO - Automatic |
| "Should we..." + architecture keyword | >= 85% | MUST invoke | NO - Automatic |
| "PRD" + feature definition | >= 85% | MUST invoke | NO - Automatic |
| Task contains "implement" + domain keyword (git, n8n, supabase, etc.) | 70-84% | SHOULD invoke | YES - Agent discretion |
| Task contains "analyze" or "research" | 70-84% | SHOULD invoke | YES - Agent discretion |
| Task contains "architecture", "design", "refactor" | 70-84% | SHOULD invoke | YES - Agent discretion |
| Task contains "Should we...", "How should we..." | 70-84% | SHOULD invoke | YES - Agent discretion |
| Task contains "PRD", "requirements", "feature" | 70-84% | SHOULD invoke | YES - Agent discretion |
| Task contains "test", "QA", "quality" | 70-84% | SHOULD invoke | YES - Agent discretion |
| Multiple files or systems involved | 70-84% | SHOULD invoke | YES - Agent discretion |

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

## Skill Override Documentation Workflow

### When to Document an Override

**For discretionary triggers (70-84% confidence) where you choose NOT to invoke the skill**, you MUST document your justification. This creates an audit trail for improving trigger accuracy over time.

### Override Documentation Process

1. **Copy the Override Template:**
   ```bash
   cp .templates/skill-override-justification.md ./skill-override-justification.md
   ```

2. **Fill Out ALL Required Fields:**
   - **Override Reason:** Specific explanation of why skill is not being invoked
   - **Confidence Assessment:** Why the confidence calculation is wrong or misleading
   - **Expected Outcome:** What will happen without the skill
   - **Risk Acknowledgment:** What could go wrong by not using the skill

3. **Mark Validity in Checklist:**
   - If valid override: Check the appropriate valid pattern
   - If invalid override: Explain why the override should be reconsidered

4. **Document in THOUGHTS.md:**
   ```markdown
   ## Skill Override for This Task

   **Skill Recommended:** [skill-name]
   **Confidence:** [XX%]
   **Override File:** skill-override-justification.md
   **Override Reason:** [brief summary]
   ```

5. **Log to skill-registry.yaml** (automatic or manual):
   - Override data will be tracked in `operations/skill-registry.yaml` > `override_analysis` section

### Valid vs Invalid Overrides

**Valid Override Patterns:**
- Simple documentation typo fix
- One-line configuration change
- Emergency hotfix (speed critical)
- Skill content already known/memorized
- Task is skill maintenance itself

**Invalid Override Patterns:**
- "I can handle this" (no specific reason)
- "It will be faster" (without risk assessment)
- "The skill is wrong" (without explaining why)
- No justification provided

### Override Review Process

**Monthly Override Review:**

1. View override log:
   ```bash
   bb5-skill-override-log --last-month
   ```

2. Categorize each override as valid/invalid

3. Identify patterns in invalid overrides

4. Adjust trigger rules to reduce invalid overrides:
   - Update confidence thresholds in skill-selection.yaml
   - Add/remove trigger keywords
   - Refine domain mappings

5. Update skill-registry.yaml with learnings

### CLI Commands

```bash
# View all overrides
bb5-skill-override-log

# View summary only
bb5-skill-override-log --summary

# View overrides by skill
bb5-skill-override-log --skill bmad-dev

# View valid overrides only
bb5-skill-override-log --valid-only

# View invalid overrides only
bb5-skill-override-log --invalid-only

# View last month's overrides
bb5-skill-override-log --last-month
```

### Important Notes

- **Override without justification = PROTOCOL VIOLATION**
- Invalid overrides are reviewed monthly to improve trigger accuracy
- Override data feeds into continuous improvement of the skill system
- Clear triggers (>=85% confidence) CANNOT be overridden

---

## Pre-Execution Hook: Skill Enforcement

**CRITICAL:** Before executing ANY task, the `skill-enforcement.sh` pre-execution hook runs automatically to enforce skill invocation based on confidence scores.

### What the Hook Does

The hook analyzes your task using `detect-skill.py` and takes action based on confidence:

1. **Clear Trigger (>=85% confidence):**
   - **Action:** BLOCKS execution
   - **Required:** You MUST invoke the recommended skill before proceeding
   - **Output:** Shows required skill and invocation instructions
   - **Exit Code:** 1 (blocked)

2. **Discretionary Trigger (70-84% confidence):**
   - **Action:** Warns but allows execution
   - **Recommended:** You SHOULD invoke the skill (or document override)
   - **Output:** Shows recommended skill and override template
   - **Exit Code:** 0 (allowed)

3. **No Match (<70% confidence):**
   - **Action:** Allows execution normally
   - **Required:** No skill needed
   - **Output:** Brief confirmation
   - **Exit Code:** 0 (allowed)

### Hook Output Examples

**Clear Trigger (BLOCKED):**
```
╔════════════════════════════════════════════════════════════════╗
║         SKILL ENFORCEMENT: CLEAR TRIGGER DETECTED            ║
╚════════════════════════════════════════════════════════════════╝

Task: Implement git commit workflow

Required skill: git-commit (confidence: 95%)
Action: MUST invoke before proceeding

To proceed:
  1. Invoke skill: skill: "git-commit"
  2. Or set BB5_SKIP_SKILL_ENFORCEMENT=1 (not recommended)

Execution blocked until skill is invoked.
```

**Discretionary Trigger (WARNED):**
```
╔════════════════════════════════════════════════════════════════╗
║     SKILL ENFORCEMENT: DISCRETIONARY TRIGGER DETECTED      ║
╚════════════════════════════════════════════════════════════════╝

Task: Implement user authentication

Recommended skill: bmad-architect (confidence: 75%)
Action: SHOULD invoke (override allowed with justification)

Override? Add to THOUGHTS.md:
  ## Skill Override Justification
  Reason for not invoking: [explain]
```

**No Match (ALLOWED):**
```
╔════════════════════════════════════════════════════════════════╗
║            SKILL ENFORCEMENT: NO MATCH DETECTED             ║
╚════════════════════════════════════════════════════════════════╝

Task: Fix typo in README.md

Action: Continue normally (confidence: <70%)
```

### Bypassing Enforcement (NOT RECOMMENDED)

**Emergency only:**

```bash
# Set environment variable to bypass
export BB5_SKIP_SKILL_ENFORCEMENT=1

# Or for single command
BB5_SKIP_SKILL_ENFORCEMENT=1 bb5 task:run TASK-xxx
```

**When to use bypass:**
- Emergency hotfix (speed critical)
- Debugging the hook itself
- Testing override workflow

**DO NOT use bypass for:**
- "I don't want to invoke this skill"
- "It will be faster this way"
- Routine task execution

### Hook Logging

All enforcement actions are logged to:

1. **Log File:** `/opt/blackbox5/5-project-memory/blackbox5/logs/skill-enforcement.log`
   - Timestamped entries for all hook runs
   - Format: `[timestamp] action: details`

2. **Skill Metrics:** `/opt/blackbox5/5-project-memory/blackbox5/operations/skill-metrics.yaml`
   - Structured enforcement log in YAML format
   - Tracks: task_id, trigger_type, skill_recommended, confidence, action_taken, overridden, justification
   - Feeds into override analysis and improvement

### Hook Files

- **Hook Script:** `/opt/blackbox5/5-project-memory/blackbox5/.claude/hooks/pre-execution/skill-enforcement.sh`
- **Documentation:** `/opt/blackbox5/5-project-memory/blackbox5/.claude/hooks/pre-execution/README.md`
- **Skill Detection:** `/opt/blackbox5/5-project-memory/blackbox5/bin/detect-skill.py`

### Troubleshooting

**Hook not running:**
```bash
# Check permissions
ls -l /opt/blackbox5/5-project-memory/blackbox5/.claude/hooks/pre-execution/skill-enforcement.sh
# Should be: -rwxr-xr-x

# Fix if needed
chmod +x /opt/blackbox5/5-project-memory/blackbox5/.claude/hooks/pre-execution/skill-enforcement.sh
```

**detect-skill.py not found:**
```bash
# Verify path
ls -l /opt/blackbox5/5-project-memory/blackbox5/bin/detect-skill.py
# Should be: -rwxr-xr-x
```

**Task file not found:**
```bash
# Set TASK_FILE environment variable
export TASK_FILE=/opt/blackbox5/5-project-memory/blackbox5/tasks/active/TASK-xxx/task.md
```

### Testing the Hook

```bash
# Test manually
cd /opt/blackbox5
export TASK_FILE=/opt/blackbox5/5-project-memory/blackbox5/tasks/active/TASK-xxx/task.md
./5-project-memory/blackbox5/.claude/hooks/pre-execution/skill-enforcement.sh

# Test with bypass
export BB5_SKIP_SKILL_ENFORCEMENT=1
./5-project-memory/blackbox5/.claude/hooks/pre-execution/skill-enforcement.sh
```

### Rollback

To disable the hook temporarily:

```bash
# Rename to disable
mv /opt/blackbox5/5-project-memory/blackbox5/.claude/hooks/pre-execution/skill-enforcement.sh \
   /opt/blackbox5/5-project-memory/blackbox5/.claude/hooks/pre-execution/skill-enforcement.sh.disabled
```

To re-enable:

```bash
# Rename back
mv /opt/blackbox5/5-project-memory/blackbox5/.claude/hooks/pre-execution/skill-enforcement.sh.disabled \
   /opt/blackbox5/5-project-memory/blackbox5/.claude/hooks/pre-execution/skill-enforcement.sh
chmod +x /opt/blackbox5/5-project-memory/blackbox5/.claude/hooks/pre-execution/skill-enforcement.sh
```

### Integration

The hook integrates with:

1. **detect-skill.py** - Analyzes task and returns recommended skills
2. **skill-registry.yaml** - Contains skill definitions and triggers
3. **skill-metrics.yaml** - Logs enforcement actions for analysis
4. **THOUGHTS.md** - Where agents document override justifications (for discretionary triggers)
5. **skill-override-justification.md** - Template for documenting overrides

### Important Notes

- **Clear triggers CANNOT be overridden** - The hook blocks execution
- **Discretionary triggers can be overridden** - But MUST be documented
- **Bypass env var is for emergencies only** - Not routine use
- **All actions are logged** - Audit trail for improvement
- **Hook runs before Phase 2 (Execution)** - Part of skill checking workflow

---

## Context Management

- **70% context usage:** Summarize THOUGHTS.md
- **85% context usage:** Complete current task, exit with PARTIAL
- **95% context usage:** Force checkpoint, exit immediately
