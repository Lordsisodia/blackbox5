# Knowledge Base & Learning Engine - User Guide

**Version:** 1.0.0
**Last Updated:** 2026-02-01T14:42:30Z
**Target Audience:** RALF Operators, Executors, Planners

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [CLI Reference](#cli-reference)
3. [Python API Reference](#python-api-reference)
4. [Common Workflows](#common-workflows)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

---

## Quick Start

### Installation

No installation required - the learning system is part of the RALF engine:

```bash
# Libraries are in:
2-engine/.autonomous/lib/learning_extractor.py
2-engine/.autonomous/lib/pattern_matcher.py
2-engine/.autonomous/lib/knowledge_retriever.py
2-engine/.autonomous/lib/learning_applier.py

# Learning index:
memory/insights/learning-index.yaml

# Documentation:
memory/insights/.docs/learning-system-guide.md
```

### Basic Usage

**1. Extract Learnings from a Run**

```bash
cd /workspaces/blackbox5/5-project-memory/blackbox5

# Extract learnings from a completed run
python3 2-engine/.autonomous/lib/learning_extractor.py runs/executor/run-0060

# Output: runs/executor/run-0060/LEARNINGS.yaml
```

**2. Search for Learnings**

```bash
# Search by keywords
python3 2-engine/.autonomous/lib/knowledge_retriever.py -i memory/insights/learning-index.yaml search "import error"

# Filter by type
python3 2-engine/.autonomous/lib/knowledge_retriever.py search "database" --type bugfix

# Filter by severity
python3 2-engine/.autonomous/lib/knowledge_retriever.py search "path" --severity high
```

**3. Find Similar Tasks**

```bash
# Find tasks similar to a query
python3 2-engine/.autonomous/lib/pattern_matcher.py -i memory/insights/learning-index.yaml similar "implement feature F-009"

# Find related tasks for a specific task
python3 2-engine/.autonomous/lib/pattern_matcher.py related TASK-123
```

**4. Apply Learnings to a New Task**

```bash
# Inject learnings into task context
python3 2-engine/.autonomous/lib/learning_applier.py -i memory/insights/learning-index.yaml inject \
  --task-id TASK-XXX \
  --title "Implement Feature F-011" \
  --description "Add user authentication system" \
  --feature-id F-011

# Output: Formatted text with relevant learnings
```

**5. Track Effectiveness**

```bash
# Track whether a learning was helpful
python3 2-engine/.autonomous/lib/learning_applier.py \
  -i memory/insights/learning-index.yaml \
  -e memory/insights/effectiveness-log.yaml track \
  --learning-id TASK-123-LEARNING-1 \
  --task-id TASK-XXX \
  --helpful true \
  --score 0.9 \
  --feedback "Prevented import errors"
```

---

## CLI Reference

### learning_extractor.py

Extract structured learnings from THOUGHTS.md and DECISIONS.md.

**Usage:**

```bash
python3 learning_extractor.py <run_dir> [options]
```

**Arguments:**

- `run_dir`: Path to run directory (e.g., `runs/executor/run-0060`)

**Options:**

- `-o, --output PATH`: Output file path (default: `run_dir/LEARNINGS.yaml`)
- `-f, --format FORMAT`: Output format (`yaml` or `json`, default: `yaml`)
- `-v, --verbose`: Verbose output (show extracted learnings)

**Examples:**

```bash
# Extract learnings with verbose output
python3 learning_extractor.py runs/executor/run-0060 -v

# Extract and save to custom location
python3 learning_extractor.py runs/executor/run-0060 -o /tmp/learnings.yaml

# Extract as JSON
python3 learning_extractor.py runs/executor/run-0060 -f json -o learnings.json
```

**Output:**

```yaml
# Learnings

---
learning_id: "TASK-123-LEARNING-1"
task_id: "TASK-123"
timestamp: "2026-02-01T12:00:00Z"
source_file: "THOUGHTS.md"
learning_type: "bugfix"
title: "Import path errors"
description: "Import errors occur when using relative imports..."
---

```

### pattern_matcher.py

Find similar tasks and identify recurring patterns.

**Usage:**

```bash
python3 pattern_matcher.py [options] <command>
```

**Options:**

- `-i, --index PATH`: Path to learning index (default: `memory/insights/learning-index.yaml`)

**Commands:**

**1. similar** - Find tasks similar to a query

```bash
python3 pattern_matcher.py similar <query> [options]
```

Options:
- `-n, --top-n N`: Number of results (default: 5)
- `-t, --threshold THRESHOLD`: Similarity threshold (default: 0.3)

Example:
```bash
python3 pattern_matcher.py similar "implement feature" -n 3 -t 0.4
```

**2. patterns** - Identify recurring patterns

```bash
python3 pattern_matcher.py patterns [options]
```

Options:
- `-l, --learning-type TYPE`: Filter by learning type
- `-f, --min-frequency N`: Minimum frequency (default: 2)

Example:
```bash
python3 pattern_matcher.py patterns -l bugfix -f 3
```

**3. issues** - Detect recurring issues

```bash
python3 pattern_matcher.py issues
```

Example:
```bash
python3 pattern_matcher.py issues
```

**4. related** - Suggest related tasks

```bash
python3 pattern_matcher.py related <task_id> [options]
```

Options:
- `-n, --top-n N`: Number of results (default: 3)

Example:
```bash
python3 pattern_matcher.py related TASK-123 -n 5
```

### knowledge_retriever.py

Search and retrieve learnings from the knowledge base.

**Usage:**

```bash
python3 knowledge_retriever.py [options] <command>
```

**Options:**

- `-i, --index PATH`: Path to learning index (default: `memory/insights/learning-index.yaml`)

**Commands:**

**1. search** - Search for learnings

```bash
python3 knowledge_retriever.py search <query> [options]
```

Options:
- `-t, --type TYPE`: Filter by learning type
- `-c, --category CATEGORY`: Filter by category
- `-f, --feature FEATURE`: Filter by feature ID
- `-s, --severity SEVERITY`: Filter by severity
- `-n, --max-results N`: Maximum results (default: 10)
- `--threshold THRESHOLD`: Relevance threshold (default: 0.2)

Examples:
```bash
# Basic search
python3 knowledge_retriever.py search "import error"

# Filtered search
python3 knowledge_retriever.py search "database" --type bugfix --severity high

# High relevance only
python3 knowledge_retriever.py search "api" --threshold 0.5 -n 5
```

**2. get** - Get learning by ID

```bash
python3 knowledge_retriever.py get <learning_id>
```

Example:
```bash
python3 knowledge_retriever.py get TASK-123-LEARNING-1
```

**3. stats** - Get knowledge base statistics

```bash
python3 knowledge_retriever.py stats
```

Example:
```bash
python3 knowledge_retriever.py stats
```

Output:
```
Knowledge Base Statistics:
  Total learnings: 42
  Unique tasks: 15
  Unique features: 8

  Type breakdown:
    bugfix: 12
    pattern: 10
    decision: 8
    insight: 6
    challenge: 4
    optimization: 2

  Category breakdown:
    technical: 25
    process: 8
    architectural: 5
    operational: 4

  Severity breakdown:
    high: 8
    medium: 12
    low: 3

  Average effectiveness: 0.75

  Index version: 1.0.0
  Last updated: 2026-02-01T14:42:30Z
```

### learning_applier.py

Apply learnings to tasks and track effectiveness.

**Usage:**

```bash
python3 learning_applier.py [options] <command>
```

**Options:**

- `-i, --index PATH`: Path to learning index (default: `memory/insights/learning-index.yaml`)
- `-e, --effectiveness-log PATH`: Path to effectiveness log (default: `memory/insights/effectiveness-log.yaml`)

**Commands:**

**1. inject** - Inject learnings into task context

```bash
python3 learning_applier.py inject [options]
```

Required:
- `--task-id ID`: Task ID
- `--title TITLE`: Task title

Optional:
- `--description DESC`: Task description
- `--feature-id ID`: Feature ID
- `-n, --max N`: Maximum learnings to inject (default: 3)

Example:
```bash
python3 learning_applier.py inject \
  --task-id TASK-XXX \
  --title "Implement user authentication" \
  --description "Add login and registration" \
  --feature-id F-011 \
  --max 5
```

**2. apply** - Record learning application

```bash
python3 learning_applier.py apply [options]
```

Required:
- `--learning-id ID`: Learning ID
- `--task-id ID`: Task ID

Optional:
- `--notes NOTES`: Application notes

Example:
```bash
python3 learning_applier.py apply \
  --learning-id TASK-123-LEARNING-1 \
  --task-id TASK-XXX \
  --notes "Applied absolute import fix"
```

**3. track** - Track learning effectiveness

```bash
python3 learning_applier.py track [options]
```

Required:
- `--learning-id ID`: Learning ID
- `--task-id ID`: Task ID

Optional:
- `--helpful BOOL`: Whether learning was helpful (true/false)
- `--score SCORE`: Effectiveness score (0.0 to 1.0)
- `--feedback TEXT`: Feedback text

Example:
```bash
python3 learning_applier.py track \
  --learning-id TASK-123-LEARNING-1 \
  --task-id TASK-XXX \
  --helpful true \
  --score 0.9 \
  --feedback "Prevented import errors, saved 10 minutes"
```

**4. stats** - Get effectiveness statistics

```bash
python3 learning_applier.py stats [options]
```

Optional:
- `--learning-id ID`: Learning ID (if omitted, shows overall stats)

Examples:
```bash
# Overall statistics
python3 learning_applier.py stats

# Specific learning statistics
python3 learning_applier.py stats --learning-id TASK-123-LEARNING-1
```

---

## Python API Reference

### Quick Import

```python
import sys
sys.path.insert(0, "/workspaces/blackbox5/2-engine/.autonomous/lib")

from learning_extractor import LearningExtractor
from pattern_matcher import PatternMatcher
from knowledge_retriever import KnowledgeRetriever
from learning_applier import LearningApplier
```

### Learning Extractor

```python
# Initialize
extractor = LearningExtractor(run_dir="runs/executor/run-0060")

# Extract learnings
learnings = extractor.extract_learnings()

# Access learnings
for learning in learnings:
    print(f"Learning: {learning.title}")
    print(f"Type: {learning.learning_type}")
    print(f"Description: {learning.description}")

# Categorize learning
category = extractor.categorize_learning(learning)

# Assess impact
impact = extractor.assess_impact(learning)
print(f"Priority score: {impact['priority_score']}")

# Save to file
output_path = extractor.save_learnings_to_file()
```

### Pattern Matcher

```python
# Initialize
matcher = PatternMatcher(learning_index_path="memory/insights/learning-index.yaml")

# Find similar tasks
similar_tasks = matcher.find_similar_tasks(
    query="implement feature",
    top_n=5,
    threshold=0.3
)

for task in similar_tasks:
    print(f"{task.task_id}: {task.similarity_score}")
    print(f"Reasons: {task.similarity_reasons}")

# Identify patterns
patterns = matcher.identify_patterns(min_frequency=2)

for pattern in patterns:
    print(f"Pattern: {pattern.description}")
    print(f"Frequency: {pattern.frequency}")

# Detect recurring issues
issues = matcher.detect_recurring_issues()

for issue in issues:
    print(f"Issue: {issue.description}")
    print(f"Severity: {issue.severity}")

# Suggest related tasks
related = matcher.suggest_related_tasks(task_id="TASK-123", top_n=3)
```

### Knowledge Retriever

```python
# Initialize
retriever = KnowledgeRetriever(learning_index_path="memory/insights/learning-index.yaml")

# Search learnings
results = retriever.search_learnings(
    query="import error",
    learning_type="bugfix",
    max_results=10,
    threshold=0.2
)

for result in results:
    print(f"Learning: {result.title}")
    print(f"Relevance: {result.relevance_score}")
    print(f"Matched keywords: {result.matched_keywords}")

# Get relevant patterns
patterns = retriever.get_relevant_patterns(query="database")

# Suggest learnings for a task
suggestions = retriever.suggest_learnings(
    task_context={
        "task_id": "TASK-XXX",
        "title": "My Task",
        "description": "Task description",
        "feature_id": "F-011"
    },
    max_suggestions=3
)

# Get learning by ID
learning = retriever.get_learning_by_id("TASK-123-LEARNING-1")

# Get learnings by task
task_learnings = retriever.get_learnings_by_task("TASK-123")

# Get statistics
stats = retriever.get_stats()
print(f"Total learnings: {stats['total_learnings']}")
```

### Learning Applier

```python
# Initialize
applier = LearningApplier(
    learning_index_path="memory/insights/learning-index.yaml",
    effectiveness_log_path="memory/insights/effectiveness-log.yaml"
)

# Inject learnings into context
injected_text, suggestions = applier.inject_learnings_to_context(
    task_context={
        "task_id": "TASK-XXX",
        "title": "My Task",
        "description": "Task description",
        "feature_id": "F-011"
    },
    max_learnings=3
)

print(injected_text)

# Apply learning
result = applier.apply_learning(
    learning_id="TASK-123-LEARNING-1",
    task_id="TASK-XXX",
    applied=True,
    notes="Applied the fix"
)

# Track effectiveness
result = applier.track_effectiveness(
    learning_id="TASK-123-LEARNING-1",
    task_id="TASK-XXX",
    helpful=True,
    effectiveness_score=0.9,
    feedback="Very helpful"
)

# Get learning statistics
stats = applier.get_learning_statistics("TASK-123-LEARNING-1")
print(f"Total applications: {stats['total_applications']}")
print(f"Helpful rate: {stats['helpful_rate']:.2%}")

# Get overall statistics
overall_stats = applier.get_all_statistics()

# Update effectiveness in index
applier.update_learning_effectiveness_in_index("TASK-123-LEARNING-1")
```

---

## Common Workflows

### Workflow 1: Post-Task Learning Extraction

```bash
# After task completion, extract learnings
cd /workspaces/blackbox5/5-project-memory/blackbox5

python3 2-engine/.autonomous/lib/learning_extractor.py runs/executor/run-0060 -v

# Review extracted learnings
cat runs/executor/run-0060/LEARNINGS.yaml

# Manually add to learning index if needed
# (automatic in production)
```

### Workflow 2: Pre-Task Learning Retrieval

```bash
# Before starting a new task, find relevant learnings

# Option 1: Search for learnings
python3 2-engine/.autonomous/lib/knowledge_retriever.py search "feature implementation"

# Option 2: Find similar tasks
python3 2-engine/.autonomous/lib/pattern_matcher.py similar "implement authentication system"

# Option 3: Inject learnings into context (recommended)
python3 2-engine/.autonomous/lib/learning_applier.py inject \
  --task-id TASK-XXX \
  --title "Implement authentication" \
  --feature-id F-011
```

### Workflow 3: Continuous Improvement Loop

```bash
# 1. Extract learnings after task
python3 learning_extractor.py runs/executor/run-0060

# 2. Apply learnings to next task
python3 learning_applier.py inject --task-id TASK-XXX --title "Next Task"

# 3. Track effectiveness after completion
python3 learning_applier.py track \
  --learning-id TASK-123-LEARNING-1 \
  --task-id TASK-XXX \
  --helpful true \
  --score 0.8

# 4. View statistics
python3 learning_applier.py stats
```

### Workflow 4: Pattern Analysis

```bash
# Identify recurring patterns
python3 pattern_matcher.py patterns -f 3

# Detect recurring issues
python3 pattern_matcher.py issues

# Analyze specific task
python3 pattern_matcher.py related TASK-123
```

---

## Best Practices

### 1. Learning Extraction

- **Run after every task completion**: Extract learnings immediately after task completion
- **Review extracted learnings**: Verify extraction quality, adjust if needed
- **Use structured THOUGHTS.md**: Follow standard format for better extraction

### 2. Learning Application

- **Inject before starting task**: Always check for relevant learnings before task execution
- **Review suggestions critically**: Not all suggestions apply to every task
- **Provide feedback**: Track effectiveness to improve future recommendations

### 3. Effectiveness Tracking

- **Track consistently**: Track effectiveness for all applied learnings
- **Use objective scores**: Use 0.0-1.0 scale consistently
- **Add detailed feedback**: Feedback helps improve the system

### 4. Index Maintenance

- **Rebuild periodically**: Rebuild index from scratch to remove stale entries
- **Cleanup old learnings**: Archive or remove low-effectiveness learnings
- **Update statistics**: Run statistics updates after major changes

---

## Troubleshooting

### Issue: Learning extraction finds no learnings

**Symptoms:** `learning_extractor.py` runs but outputs "Extracted 0 learnings"

**Possible Causes:**
1. THOUGHTS.md or DECISIONS.md missing or empty
2. No learning-related sections found
3. Section headers don't match expected patterns

**Solutions:**
1. Verify THOUGHTS.md and DECISIONS.md exist and are non-empty
2. Check for section headers like "Key Insights", "Learnings", "Challenges"
3. Add manual learning entries if needed

### Issue: Pattern matching returns no results

**Symptoms:** `pattern_matcher.py similar` returns "Found 0 similar tasks"

**Possible Causes:**
1. Learning index is empty
2. Similarity threshold too high
3. Query too short or too specific

**Solutions:**
1. Check learning-index.yaml has learnings
2. Lower threshold with `-t` option (try 0.2)
3. Use broader query terms

### Issue: Learning suggestions not relevant

**Symptoms:** Injected learnings don't seem relevant to the task

**Possible Causes:**
1. Task context incomplete
2. Low learning count in index
3. Keyword extraction not matching

**Solutions:**
1. Provide full task description with `--description`
2. Add more learnings to index
3. Track effectiveness to improve future matches

### Issue: Effectiveness tracking not working

**Symptoms:** Effectiveness scores not updating or not being saved

**Possible Causes:**
1. effectiveness-log.yaml doesn't exist or isn't writable
2. Learning ID not found in index
3. File permissions issue

**Solutions:**
1. Create effectiveness-log.yaml with `touch memory/insights/effectiveness-log.yaml`
2. Verify learning ID exists in learning-index.yaml
3. Check file permissions on memory/insights/

---

## FAQ

**Q: How often should I extract learnings?**

A: After every task completion. The system is designed to extract learnings automatically.

**Q: What if the learning system suggests wrong learnings?**

A: Track effectiveness with low scores. The system uses effectiveness to rank future suggestions.

**Q: Can I manually add learnings?**

A: Yes. Create a YAML file with the learning structure and add it to the learning index.

**Q: How many learnings should I inject into a task?**

A: Default is 3, but you can adjust with `--max` option. More learnings = more context but longer prompt.

**Q: What's the difference between pattern matching and learning retrieval?**

A: Pattern matching finds similar tasks, while learning retrieval searches for specific learnings. Use both for best results.

**Q: How do I improve learning relevance?**

A: Track effectiveness consistently. The system learns from feedback over time.

**Q: Can I use the learning system across multiple RALF instances?**

A: Not in Phase 1. Phase 2 will support cross-instance learning sharing.

**Q: What happens if learning-index.yaml gets corrupted?**

A: Rebuild from scratch by running extraction on all completed runs.

**Q: How do I archive old learnings?**

A: Move low-effectiveness learnings to a separate archive file and rebuild the index.

**Q: Can I export learnings to JSON?**

A: Yes. Use `learning_extractor.py -f json -o output.json`.

---

## Related Documentation

- [Learning System Guide](../../../memory/insights/.docs/learning-system-guide.md) - Technical details
- [Feature F-010 Specification](../../../plans/features/FEATURE-010-knowledge-base.md) - Feature documentation
- [Executor Integration](../../../2-engine/.autonomous/prompts/) - Executor prompt integration

---

**End of User Guide**
