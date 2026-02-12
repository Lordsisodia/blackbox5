# BlackBox5 Naming Conventions

**Last Updated:** 2026-02-12
**Purpose:** Standardize naming conventions across the BlackBox5 codebase to reduce confusion and prevent errors.

---

## Template Files

### Convention
**All template files MUST use the `.template` extension.**

### Why This Matters
Template files contain placeholder text like `{SERVICE_NAME}`, `{SERVICE_LOWER}`, `{ServiceName}` that:
1. Are **NOT valid syntax** in Python, JavaScript, YAML, or other languages
2. Cause **syntax errors** and false bug reports
3. Confuse linters and static analysis tools
4. Lead to wasted time investigating "bugs" that are actually features

### Examples

**✅ Correct:**
- `__init__.py.template`
- `manager.py.template`
- `types.py.template`
- `config.py.template`
- `demo.py.template`
- `test_integration.py.template`
- `task.md.template`
- `agent.md.template`
- `prompt.md.template`

**❌ Wrong:**
- `__init__.py` (contains `{SERVICE_NAME}` placeholder)
- `manager.py` (contains `{SERVICE_NAME}` placeholder)
- `config.py.yaml` (contains template placeholders)
- `task.md` (contains `{Task Name}` placeholder)
- `agent.md` (contains `<agent-name>` placeholder)

### How to Create a New Integration

1. **Copy template directory:**
   ```bash
   cp -r _template my_service
   ```

2. **Replace placeholders** in all `.template` files:
   ```bash
   sed -i 's/{SERVICE_NAME}/GitHub/g' *.template
   sed -i 's/{SERVICE_LOWER}/github/g' *.template
   sed -i 's/{ServiceName}/GitHub/g' *.template
   ```

3. **Remove `.template` extension** from all files:
   ```bash
   for f in *.template tests/*.template; do
     mv "$f" "${f%.template}"
   done
   ```

### Common Template Placeholders

**Python integration templates:**
- `{SERVICE_NAME}` - PascalCase service name
- `{SERVICE_LOWER}` - lowercase service name
- `{ServiceName}` - Mixed case service name
- `{PACKAGE_NAME}` - Package name
- `{MODULE_NAME}` - Module name
- `{CLASS_NAME}` - Class name

**Task templates:**
- `{Task Name}` - Task title
- `{YYYY-MM-DD}` - Date
- `{Agent Name}` - Agent assigned
- `{Brief description...}` - Task description
- `{Specific, testable criteria}` - Acceptance criteria

**Agent templates:**
- `<agent-name>` - Agent name
- `<agent-id>` - Agent ID (slugified)
- `<What this agent does...>` - Agent description
- `<short title>` - Plan title
- `<YYYY-MM-DD HH:MM>` - Timestamp

**Plan templates:**
- `<short title>` - Plan description
- `<YYYY-MM-DD HH:MM>` - Plan creation timestamp

### Pre-commit Hook

A pre-commit hook is installed at `.git/hooks/pre-commit` that automatically checks for:
- Files with template placeholders (all patterns listed above)
- Missing `.template` extension

**To bypass the hook (not recommended):**
```bash
git commit --no-verify
```

### Related Documentation
- Integration Template: `2-engine/helpers/integrations/_template/README.md`
- Implementation Guide: `2-engine/helpers/integrations/_template/IMPLEMENTATION-GUIDE.md`

---

## Task Files

### Format
- Active tasks: `tasks/active/TASK-{ID}/`
- Completed tasks: `tasks/completed/TASK-{ID}/`
- Task metadata: `task.md`

### Naming Patterns
- `TASK-HINDSIGHT-005` - Hindsight system tasks
- `TASK-INFR-010` - Infrastructure tasks
- `TASK-DOCU-025` - Documentation tasks
- `TASK-SKIL-018` - Skill-related tasks
- `IMP-1769903005` - Improvement tasks (timestamp-based)

---

## Goals

### Format
- `IG-{NNN}` - Improvement Goal
- `CG-{NNN}` - Core Goal

### Examples
- `IG-006` - Autonomous System
- `CG-001` - Multi-Agent Orchestration

---

## Plans

### Format
- Descriptive names in kebab-case
- Linked to goals: `PLAN-{GOAL_ID}-{description}`

### Examples
- `PLAN-HINDSIGHT-001`
- `user-profile-improvement`

---

## Agent Names

### Format
- Descriptive names in lowercase with hyphens
- Clear indication of role/function

### Examples
- `claude-code` - Claude Code MCP bridge
- `moltbot-vps-ai` - VPS AI agent
- `moltbot-macmini-01` - Mac Mini agent

---

## Integration Files

### Format
- `{service-name}/` - Directory name
- `{service_name}_integration.py` - Main integration file
- `types.py` - Type definitions
- `config.py` - Configuration
- `manager.py` - Main manager class

### Examples
- `github/github_integration.py`
- `notion/notion_integration.py`
- `vibe/vibe_integration.py`

---

## Configuration Files

### Format
- `{service}.yaml` or `{service}.yml`
- `config.{service}.yaml`

### Examples
- `agents.yaml`
- `ralf-config.yaml`
- `validation-checklist.yaml`

---

## Documentation Files

### Format
- Descriptive names in kebab-case
- Use ALL CAPS for important documents
- Use lowercase for guides and tutorials

### Examples
- `ARCHITECTURE.md`
- `README.md`
- `QUICKSTART.md`
- `naming-conventions.md`
- `implementation-guide.md`

---

## Run Logs

### Format
- `run-{timestamp}/` - Directory for each run
- `events.yaml` - Events log
- `analysis.md` - Analysis document
- `outcome.md` - Outcome document

### Examples
- `run-1769813746/`
- `run-20260212-120000/`

---

## Memory Files

### Format
- `EPISODE-{id}.md` - Episode learnings
- `{YYYY-MM-DD}.md` - Daily memory files
- `MEMORY.md` - Long-term curated memory

### Examples
- `EPISODE-001.md`
- `2026-02-12.md`
- `MEMORY.md`

---

## Enforcement

### Pre-commit Hooks
- Template file naming: `.git/hooks/pre-commit`
- Additional checks can be added as needed

### Linting Rules
- When available, configure linters to enforce these conventions

### Code Review Checklist
- [ ] Files follow naming conventions
- [ ] Template files use `.template` extension
- [ ] Descriptive names are clear and consistent
- [ ] No hardcoded paths or names

---

## Updating This Document

When adding new naming conventions:
1. Update this document
2. Add pre-commit hook check if needed
3. Update related documentation
4. Create examples if appropriate
5. Announce changes to team

---

**Questions or Issues?**
- Check: `2-engine/helpers/integrations/_template/README.md`
- Review: Pre-commit hook at `.git/hooks/pre-commit`
- Contact: DevOps team or maintainers
