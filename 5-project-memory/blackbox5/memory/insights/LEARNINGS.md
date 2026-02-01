# RALF Learnings

**Last Updated:** 2026-02-01T14:42:30Z
**Index Version:** 1.0.0
**Total Learnings:** 0

---

## Overview

This document captures structured learnings from RALF task runs. Learnings are automatically extracted from THOUGHTS.md and DECISIONS.md files and indexed in `learning-index.yaml`.

### Learning Categories

- **Technical**: Implementation details, code patterns, libraries, frameworks
- **Process**: Workflow improvements, methodologies, procedures
- **Architectural**: Design patterns, system structure, scalability
- **Operational**: Deployment, monitoring, infrastructure, logging

### Learning Types

- **Pattern**: Recurring patterns and best practices
- **Decision**: Architectural or approach decisions made
- **Challenge**: Difficulties encountered and how they were resolved
- **Optimization**: Performance or efficiency improvements
- **Bugfix**: Bugs fixed and lessons learned
- **Insight**: New understandings and discoveries

---

## Recent Learnings

*No learnings extracted yet. The learning system will populate this section automatically after task completions.*

---

## Top Learnings by Effectiveness

*Effectiveness tracking will begin after learnings are applied and feedback is collected.*

---

## Recurring Patterns

*Patterns will be identified automatically as learnings accumulate.*

---

## Statistics

### Learning Distribution

| Category | Count |
|----------|-------|
| Technical | 0 |
| Process | 0 |
| Architectural | 0 |
| Operational | 0 |

### Type Distribution

| Type | Count |
|------|-------|
| Pattern | 0 |
| Decision | 0 |
| Challenge | 0 |
| Optimization | 0 |
| Bugfix | 0 |
| Insight | 0 |

### Severity Distribution

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |

---

## How to Use This Knowledge Base

### Query Learnings

Use the knowledge_retriever CLI:

```bash
# Search for learnings
python3 2-engine/.autonomous/lib/knowledge_retriever.py -i memory/insights/learning-index.yaml search "import error"

# Get learning by ID
python3 2-engine/.autonomous/lib/knowledge_retriever.py -i memory/insights/learning-index.yaml get TASK-XXX-LEARNING-1

# Get statistics
python3 2-engine/.autonomous/lib/knowledge_retriever.py -i memory/insights/learning-index.yaml stats
```

### Find Patterns

Use the pattern_matcher CLI:

```bash
# Find similar tasks
python3 2-engine/.autonomous/lib/pattern_matcher.py -i memory/insights/learning-index.yaml similar "implement feature F-009"

# Identify patterns
python3 2-engine/.autonomous/lib/pattern_matcher.py -i memory/insights/learning-index.yaml patterns

# Detect recurring issues
python3 2-engine/.autonomous/lib/pattern_matcher.py -i memory/insights/learning-index.yaml issues
```

### Apply Learnings

Use the learning_applier CLI:

```bash
# Inject learnings into task context
python3 2-engine/.autonomous/lib/learning_applier.py -i memory/insights/learning-index.yaml inject \
  --task-id TASK-XXX \
  --title "My Task" \
  --description "Task description"

# Track effectiveness
python3 2-engine/.autonomous/lib/learning_applier.py -i memory/insights/learning-index.yaml \
  -e memory/insights/effectiveness-log.yaml track \
  --learning-id TASK-XXX-LEARNING-1 \
  --task-id TASK-YYY \
  --helpful true \
  --score 0.8
```

---

## Learning Structure

Each learning follows this structure:

```yaml
---
learning_id: TASK-XXX-LEARNING-N
task_id: TASK-XXX
task_title: "Task Title"
feature_id: F-XXX
timestamp: "2026-02-01T12:00:00Z"
source_file: "THOUGHTS.md"
learning_type: "pattern"
severity: "high"
effectiveness: 0.8
frequency: "recurring"
category: "technical"
tags:
  - import
  - path
  - dependency
related_tasks:
  - TASK-YYY
  - TASK-ZZZ
pattern: "Import errors from incorrect module paths"
action_item: "Always use absolute imports from project root"
---

# Learning Title

Full description of the learning and why it matters.
```

---

## Effectiveness Tracking

Learnings are tracked for effectiveness over time:

- **Application Count**: How many times a learning was suggested
- **Helpful Rate**: Percentage of times the learning was helpful
- **Average Effectiveness**: Mean effectiveness score (0.0 to 1.0)

Effectiveness is tracked when:
1. A learning is suggested via `learning_applier.py inject`
2. Feedback is provided via `learning_applier.py track`
3. The learning index is updated with new effectiveness scores

---

## Maintenance

### Automatic Updates

The learning index is automatically updated:
- After each task completion (via learning_extractor.py)
- When effectiveness feedback is provided (via learning_applier.py)

### Manual Updates

To manually extract learnings from a run:

```bash
python3 2-engine/.autonomous/lib/learning_extractor.py runs/executor/run-0060
```

To rebuild the entire index:

```bash
python3 2-engine/.autonomous/lib/learning_extractor.py --rebuild
```

---

## Integration with Executor

The learning system integrates with the RALF executor workflow:

1. **Post-Completion**: Learnings automatically extracted from THOUGHTS.md and DECISIONS.md
2. **Indexing**: Learnings added to learning-index.yaml with metadata
3. **Pattern Recognition**: Recurring patterns identified across tasks
4. **Pre-Execution**: Relevant learnings injected into executor context for new tasks
5. **Feedback Loop**: Effectiveness tracked to improve future recommendations

---

## Contributing Learnings

While most learnings are extracted automatically, you can manually add learnings:

1. Create a learning file in `memory/insights/learnings/` with YAML frontmatter
2. Follow the learning structure above
3. Run `python3 2-engine/.autonomous/lib/learning_extractor.py --index-learning path/to/learning.md`

---

## Related Documentation

- [Learning System Guide](memory/insights/.docs/learning-system-guide.md) - Technical details
- [Knowledge Base User Guide](operations/.docs/knowledge-base-guide.md) - Usage instructions
- [Learning Index](memory/insights/learning-index.yaml) - Raw learning data

---

**Note:** This document is auto-generated. Do not edit manually. Use the CLI tools to manage learnings.
