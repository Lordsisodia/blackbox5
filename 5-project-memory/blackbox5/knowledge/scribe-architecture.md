# BlackBox5 Scribe Agent - Architecture & Usage Guide

## Overview

The BlackBox5 Scribe Agent is a specialized documentation agent that monitors, tracks, and records all activity within the BlackBox5 system. It ensures continuity of knowledge, preserves decision rationale, and maintains a searchable knowledge base.

---

## Architecture

### Components

#### 1. Skill Definition
**Location:** `/root/.openclaw/skills/blackbox5-scribe/SKILL.md`

This file defines:
- When to invoke the scribe agent
- What commands to use
- What the scribe does
- Expected outputs

#### 2. Knowledge Base
**Location:** `/opt/blackbox5/5-project-memory/blackbox5/knowledge/scribe-knowledge.md`

This is the central repository containing:
- Documented tasks and their statuses
- Decision log with rationale
- What works vs. what doesn't
- Lessons learned
- Patterns and anti-patterns
- Configuration reference
- Glossary and search tags

#### 3. Daily Summary Template
**Location:** `/opt/blackbox5/5-project-memory/blackbox5/knowledge/daily-summary-template.md`

A structured template for generating daily activity summaries including:
- Task activity overview
- Decisions made
- Key learnings
- Knowledge base updates
- Agent activity
- System health
- Next steps

#### 4. Task Monitoring
**Location:** `/opt/blackbox5/5-project-memory/blackbox5/tasks/`

The scribe monitors this directory for:
- New task files
- Status changes (pending → in_progress → completed)
- Progress updates

---

## Interaction Model

### Main Agent → Scribe Communication

The main agent invokes the scribe for specific events:

#### Event Types

1. **Task Creation**
   ```
   Invoke blackbox5-scribe: Document task [TASK_ID] creation - "[task title]"
   ```

2. **Task Status Change**
   ```
   Invoke blackbox5-scribe: Task [TASK_ID] status changed from [old_status] to [new_status]
   ```

3. **Task Completion**
   ```
   Invoke blackbox5-scribe: Task [TASK_ID] completed with result [outcome details]
   ```

4. **Decision Made**
   ```
   Invoke blackbox5-scribe: Record decision - [decision title]
   Context: [situation description]
   Decision: [what was decided]
   Rationale: [why this path was chosen]
   ```

5. **Discovery/Learning**
   ```
   Invoke blackbox5-scribe: Record knowledge - [what was discovered]
   Category: pattern | antipattern | lesson | config
   ```

6. **Daily Summary Request**
   ```
   Invoke blackbox5-scribe: Generate daily summary for YYYY-MM-DD
   ```

### Scribe Response Format

The scribe provides concise responses confirming what was documented:

```
✓ Documented task [TASK_ID] creation: "[task title]"
  - Status: pending
  - Added to knowledge base
```

```
✓ Recorded decision: [decision title]
  - Rationale documented
  - Awaiting outcome
```

```
✓ Knowledge added: [discovery]
  - Tagged as: #pattern
  - Knowledge base updated
```

---

## Workflow Integration

### Typical Task Lifecycle with Scribe

```
1. Main Agent Creates Task
   ↓
   [Invoke scribe: Document task creation]
   ↓
   Scribe updates knowledge base

2. Main Agent Starts Work
   ↓
   [Invoke scribe: Update task status to in_progress]
   ↓
   Scribe tracks progress

3. Main Agent Makes Decision
   ↓
   [Invoke scribe: Record decision with rationale]
   ↓
   Scribe adds to decision log

4. Main Agent Discovers Something
   ↓
   [Invoke scribe: Record knowledge]
   ↓
   Scribe adds to appropriate section

5. Main Agent Completes Task
   ↓
   [Invoke scribe: Mark task complete]
   ↓
   Scribe updates task status and knowledge base
```

### Daily Summary Generation

```
1. Main Agent requests: "Invoke blackbox5-scribe: Generate daily summary"
   ↓
2. Scribe reads all task files in tasks/ directory
   ↓
3. Scribe reviews decision log and knowledge base
   ↓
4. Scribe fills in daily summary template
   ↓
5. Scribe saves summary to memory/ with date in filename
   ↓
6. Scribe confirms: "Daily summary generated: memory/YYYY-MM-DD.md"
```

---

## Best Practices

### For Main Agents

**DO:**
- Invoke the scribe promptly when events occur
- Provide context and task IDs
- Include rationale for decisions
- Report outcomes (success or failure)
- Be specific and concise

**DON'T:**
- Batch multiple days of work without documentation
- Assume the scribe will know what happened
- Forget to update task status
- Skip documenting failures (they're valuable!)

### For the Scribe

**DO:**
- Read task files before updating status
- Maintain chronological order in decision log
- Use consistent formatting
- Link decisions to outcomes when available
- Tag knowledge items for easy searching

**DON'T:**
- Modify task files directly (track status only)
- Make up information that wasn't provided
- Mix unrelated decisions together
- Overwrite previous knowledge without backup

---

## File Structure

```
/opt/blackbox5/5-project-memory/blackbox5/
├── tasks/
│   ├── task-001.md
│   ├── task-002.md
│   └── task-003.md
└── knowledge/
    ├── scribe-knowledge.md          (central knowledge base)
    ├── daily-summary-template.md    (template for summaries)
    └── scribe-architecture.md       (this file)

/root/.openclaw/skills/
└── blackbox5-scribe/
    └── SKILL.md                     (invocation rules)

/opt/blackbox5/memory/               (daily summaries stored here)
├── 2026-02-10.md
├── 2026-02-11.md
└── ...
```

---

## Knowledge Base Sections

### Documented Tasks
- Active tasks currently being worked on
- Recently completed tasks
- Task IDs and quick status reference

### Decision Log
- Chronological record of decisions
- Rationale and alternatives considered
- Outcomes (when known)

### What Works
- Successful patterns and approaches
- Proven solutions
- Best practices

### What Doesn't Work
- Anti-patterns to avoid
- Failed attempts and why
- Obstacles and blockers

### Lessons Learned
- Insights from experience
- Things to remember for future
- Wisdom gained over time

### Patterns
- Reusable workflows
- Successful combinations
- Repeatable success formulas

### Anti-Patterns
- Things to avoid
- Warning signs
- Common pitfalls

### Configuration Reference
- System configuration details
- Network settings
- API endpoints and credentials locations

### Glossary
- Terms and definitions
- Acronyms and their meanings

### Search Tags
- Hashtag system for quick searching
- Categories and labels
- Cross-references

---

## Search and Retrieval

### Using Tags
Search the knowledge base by tags:
- `#task` - Task-related information
- `#decision` - Decision records and rationale
- `#pattern` - Successful patterns
- `#antipattern` - Things to avoid
- `#config` - Configuration details
- `#lesson` - Lessons learned

### Example Queries
- "Show me all decisions about #config"
- "What #patterns work for task tracking?"
- "Lessons from #task failures"

---

## Maintenance

### Weekly (Suggested)
- Review and update completed tasks
- Link decision outcomes where missing
- Archive old tasks if needed

### Monthly (Suggested)
- Clean up stale knowledge items
- Update glossary with new terms
- Review and refine patterns

### As Needed
- Update configuration when changes occur
- Add new search tags
- Adjust template structure

---

## Extension Points

The scribe system can be extended to:

1. **Automatic Monitoring** - Watch the tasks directory for file changes
2. **Integration with BB5 Commands** - Hook into `bb5 task:*` commands
3. **Web Dashboard** - Visual representation of task progress
4. **Analytics** - Track completion rates, decision quality
5. **AI Summaries** - Generate insights from patterns in the knowledge base

---

## Summary

The BlackBox5 Scribe Agent serves as the institutional memory of the system. By documenting decisions, tracking tasks, and building knowledge, it ensures that:

- No valuable insight is lost
- Decision rationale is preserved
- Past work informs future decisions
- Knowledge compounds over time

**Remember:** Documentation is not overhead—it's an investment in future efficiency.

---

*This architecture document is maintained by the BlackBox5 Scribe Agent*
*Last updated: 2026-02-10*
