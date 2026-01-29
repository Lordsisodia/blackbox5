# RALF Skills

**Location:** `$RALF_ENGINE_DIR/skills/` (in the engine)
**Purpose:** Transferable capabilities for autonomous task execution

---

## Philosophy

Skills are modular capabilities that Legacy can invoke:

1. **Single Responsibility** — Each skill does one thing well
2. **Documented Interface** — Clear inputs and outputs
3. **Tested** — Skills have verification steps
4. **Composable** — Skills can combine for complex workflows

---

## Skill Categories

### Core Skills (from BB5)

| Skill | Source | Purpose |
|-------|--------|---------|
| `first-principles-analysis` | BB5 1-agents/.skills/ | Structured problem decomposition |
| `testing-frameworks` | BB5 1-agents/.skills/ | Test writing and execution |
| `documentation-standards` | BB5 1-agents/.skills/ | Consistent documentation |

### MCP Integration Skills

| Skill | MCP | Purpose |
|-------|-----|---------|
| `supabase-operations` | Supabase | DDL, RLS, migrations |
| `file-operations` | File System | Read/write files |
| `browser-testing` | Chrome DevTools | UI testing, debugging |
| `complex-reasoning` | Sequential Thinking | Multi-step problems |
| `code-search` | Serena | Find patterns, references |

### Legacy-Specific Skills

| Skill | Purpose | Status |
|-------|---------|--------|
| `task-selection` | Choose next task from STATE.yaml | Active |
| `run-initialization` | Set up new run folder | Active |
| `git-commit` | Safe commit to dev branch | Active |
| `context-management` | Preserve/restore context | Active |

---

## Skill Format

Each skill is a markdown file:

```markdown
# Skill Name

**Purpose:** One-line description
**Trigger:** When to use
**Input:** Required inputs
**Output:** Expected outputs

## Procedure

1. Step one
2. Step two

## Verification

How to verify skill executed correctly

## Example

Example usage
```

---

## Usage

RALF invokes skills by:

1. **Inline** — "Using [skill-name], do X"
2. **Sub-agent** — Spawn agent with skill context
3. **Reference** — Link to skill file for complex procedures

Skills are loaded from the engine (`$RALF_ENGINE_DIR/skills/`) and applied to the project.

---

## Adding Skills

To add a new skill:

1. Create `[skill-name].md` in `$RALF_ENGINE_DIR/skills/`
2. Follow skill format template
3. Add to index above
4. Test before relying on
5. All projects get the skill automatically (it's in the engine)

