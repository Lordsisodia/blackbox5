# 6 Core Principles from IndyDevDan Video

## Principle 1: Task System as Foundation

**What it means:**
The built-in Claude Code Task System (task_create, task_get, task_list, task_update) is more valuable than hyped external tools. It provides the infrastructure for reliable multi-agent orchestration.

**Key capabilities:**
- Agents communicate through shared task list
- Dependencies block/unblock automatically
- Parallel execution where possible
- Real-time events as agents complete work

**Audit criteria:**
- Do we have structured task management?
- Can agents communicate via shared state?
- Are dependencies handled automatically?
- Can work run in parallel?

---

## Principle 2: Builder-Validator Pattern

**What it means:**
The simplest effective team is two agents: one builds, one validates. This 2x compute cost buys reliability through verification.

**Key capabilities:**
- Builder focuses on one task, reports work
- Validator independently checks correctness
- Builder can include micro-validation (linters, etc.)
- Validator does higher-level checks (compilation, tests)

**Audit criteria:**
- Do we have distinct builder/validator roles?
- Is there a verification layer?
- Can builders self-validate via hooks?
- Are validators separate from builders?

---

## Principle 3: Template Metaprompts

**What it means:**
Create prompts that generate other prompts in consistent, vetted formats. This ensures predictable outputs vs "vibe coding."

**Key capabilities:**
- Meta-prompt defines output structure
- Variables get filled in for specific tasks
- Generated prompts follow engineering standards
- Consistent format across all generated prompts

**Audit criteria:**
- Do we have prompt templates?
- Can prompts generate other prompts?
- Is output format predictable?
- Are there validation steps for generated prompts?

---

## Principle 4: Self-Validation via Hooks

**What it means:**
Agents validate their own work before claiming completion. Validation scripts run on hooks (stop, post-tool-use).

**Key capabilities:**
- validate_new_file: checks file created in right place
- validate_file_contains: verifies required content present
- post-tool-use hooks for micro-validation
- Failed validation returns to agent, doesn't complete

**Audit criteria:**
- Do we have hook system?
- Can agents self-validate?
- Are validation scripts standardized?
- Does failed validation prevent completion?

---

## Principle 5: Organization > Agent Count

**What it means:**
More agents doesn't mean better results. Organized agents with clear communication and focused context windows perform better.

**Key capabilities:**
- Each agent has focused context window
- Clear communication channels (task list)
- Common goals understood by all agents
- Specialized agents for specific tasks

**Audit criteria:**
- Are agents specialized or generalist?
- Is context focused or bloated?
- Do agents communicate clearly?
- Are goals aligned across agents?

---

## Principle 6: Real Engineering Workflows

**What it means:**
Apply agent teams to practical engineering tasks like updating old code, documentation, testing. Not just demos.

**Key capabilities:**
- Update legacy codebases
- Parallel documentation updates
- Multi-file refactoring
- Integration with existing workflows

**Audit criteria:**
- Are we solving real engineering problems?
- Can it handle existing codebases?
- Does it integrate with current workflows?
- Is it practical or just theoretical?
