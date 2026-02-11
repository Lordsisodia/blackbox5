# Common Queries for AI Agents

**Project:** SISO-Internal
**Purpose:** Quick reference for common questions

---

## Project Structure

### Where is X?

| Item | Location |
|------|----------|
| Project state | `STATE.yaml` |
| Active work | `ACTIVE.md` |
| Timeline | `timeline.yaml` |
| Goals | `goals/` |
| Plans | `plans/active/` |
| Tasks | `tasks/active/` |
| Decisions | `decisions/` |
| Knowledge | `knowledge/` |
| Templates | `.templates/` |

---

## Quick Commands

### Navigation

```bash
# Check current location
bb5 whereami

# List goals
bb5 goal:list

# List plans
bb5 plan:list

# List tasks
bb5 task:list

# Navigate up
bb5 up

# Go to root
bb5 root
```

---

## Common Patterns

### Starting a New Task

1. Check `STATE.yaml` for current status
2. Check `ACTIVE.md` for active work
3. Create task in `tasks/active/`
4. Link to plan if applicable

### Completing a Task

1. Update task file with results
2. Move to `tasks/completed/`
3. Update `STATE.yaml`
4. Update `ACTIVE.md`
5. Update `WORK-LOG.md`

---

## Decision Making

### When to Create a Decision Record

- Architecture changes
- Scope changes
- Technology choices
- Process changes

### Decision Location

- `decisions/architectural/`
- `decisions/scope/`
- `decisions/technical/`
