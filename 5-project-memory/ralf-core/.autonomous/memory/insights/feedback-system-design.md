# RALF Feedback System Design

**Version:** 1.0
**Created:** 2026-01-30
**Status:** Active

---

## Purpose

The feedback system collects insights from RALF runs to enable continuous self-improvement. It captures what worked, what didn't, and what should change.

---

## Architecture

### Three-Stage Pipeline

```
feedback/
├── incoming/      # Raw feedback from runs
├── processed/     # Reviewed and categorized
└── actions/       # Converted to actionable tasks
```

### Stage 1: Incoming

**Location:** `feedback/incoming/`

**Format:** Markdown files with YAML frontmatter

**Filename Pattern:** `FEEDBACK-{run-id}-{timestamp}.md`

**Template:**
```markdown
---
run_id: "run-0001"
timestamp: "2026-01-30T08:30:00Z"
type: "improvement"  # improvement | bug | observation | question
category: "shell"    # shell | prompt | lib | workflow | other
severity: "low"      # low | medium | high | critical
---

# Feedback Title

## Observation
What was noticed during the run.

## Context
When/where this occurred.

## Suggestion
What could be improved.

## Impact
How much this would help future runs.
```

### Stage 2: Processed

**Location:** `feedback/processed/`

**Actions:**
- Review incoming feedback
- Categorize and tag
- Deduplicate
- Prioritize

**Output:** Refined feedback ready for task creation

### Stage 3: Actions

**Location:** `feedback/actions/`

**Actions:**
- Convert high-value feedback to tasks
- Create task files in `tasks/active/`
- Link back to original feedback

---

## Feedback Types

| Type | Description | Example |
|------|-------------|---------|
| `improvement` | Suggestion to make something better | "Shell script could check prerequisites" |
| `bug` | Something that didn't work as expected | "Error handling fails on empty input" |
| `observation` | Notable pattern or behavior | "Most time spent on X" |
| `question` | Something to investigate | "Why does Y happen?" |

## Categories

| Category | Scope | Examples |
|----------|-------|----------|
| `shell` | Shell scripts | ralf-daemon.sh, utility scripts |
| `prompt` | LLM prompts | System prompts, agent prompts |
| `lib` | Library code | Shared functions, utilities |
| `workflow` | Workflow definitions | BMAD workflows |
| `skill` | BMAD skills | Skill definitions |
| `docs` | Documentation | READMEs, guides |
| `other` | Everything else | - |

---

## Collection Process

### During Run
1. RALF observes something worth noting
2. Records in run's LEARNINGS.md
3. If actionable, creates feedback file

### Post-Run
1. Review LEARNINGS.md
2. Extract feedback items
3. Create feedback files in `incoming/`

### Periodic Review
1. Process `incoming/` feedback
2. Prioritize and categorize
3. Create tasks for high-value items

---

## Success Metrics

- **Coverage:** % of runs that produce feedback
- **Quality:** % of feedback that leads to tasks
- **Impact:** Tasks completed that originated from feedback
- **Cycle Time:** From observation to task creation

---

## Future Enhancements

1. **Automated Tagging** - Use LLM to categorize feedback
2. **Trend Analysis** - Identify recurring patterns
3. **Sentiment Tracking** - Monitor improvement over time
4. **Cross-Reference** - Link related feedback items

---
