# Learning System Guide - RALF Knowledge Base & Learning Engine

**Version:** 1.0.0
**Last Updated:** 2026-02-01T14:42:30Z
**Authors:** RALF Executor

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Core Components](#core-components)
4. [Data Flow](#data-flow)
5. [Algorithms](#algorithms)
6. [Integration Points](#integration-points)
7. [API Reference](#api-reference)
8. [Configuration](#configuration)

---

## Overview

The RALF Learning System is a knowledge capture and retrieval engine that enables continuous improvement through systematic learning extraction, pattern recognition, and knowledge application.

### Key Capabilities

- **Automatic Learning Extraction**: Extracts learnings from THOUGHTS.md and DECISIONS.md
- **Pattern Recognition**: Identifies recurring patterns and similar tasks
- **Knowledge Retrieval**: Searches and retrieves relevant learnings
- **Learning Application**: Injects relevant learnings into executor context
- **Effectiveness Tracking**: Tracks learning effectiveness over time

### Design Principles

1. **Non-Invasive**: Works with existing run output, no changes to core workflow
2. **Transparent**: All learnings stored in human-readable YAML format
3. **Extensible**: Plugin architecture for new learning types and algorithms
4. **Efficient**: Keyword-based matching with optional semantic similarity (Phase 2)
5. **Measurable**: Effectiveness tracking with quantifiable metrics

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    RALF Learning System                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐                    │
│  │   Task Run   │      │  New Task    │                    │
│  │  Completion  │      │  Execution   │                    │
│  └──────┬───────┘      └──────┬───────┘                    │
│         │                     │                              │
│         v                     v                              │
│  ┌──────────────┐      ┌──────────────┐                    │
│  │   Learning   │      │  Pattern     │                    │
│  │   Extractor  │      │   Matcher    │                    │
│  └──────┬───────┘      └──────┬───────┘                    │
│         │                     │                              │
│         v                     v                              │
│  ┌──────────────┐      ┌──────────────┐                    │
│  │    Learning  │<─────┤  Knowledge   │                    │
│  │     Index    │      │  Retriever   │                    │
│  │(YAML File)   │      └──────┬───────┘                    │
│  └──────┬───────┘             │                              │
│         │                     v                              │
│         └──────────────> ┌──────────────┐                   │
│                         │   Learning    │                   │
│                         │    Applier    │                   │
│                         └──────┬───────┘                   │
│                                │                            │
│                                v                            │
│                         ┌──────────────┐                   │
│                         │ Effectiveness│                   │
│                         │    Tracker   │                   │
│                         └──────────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

### Data Structures

#### Learning Object

```python
@dataclass
class Learning:
    task_id: str
    learning_id: str
    timestamp: str
    source_file: str
    learning_type: str
    title: str
    description: str
    pattern: Optional[str]
    action_item: Optional[str]
    related_tasks: Optional[List[str]]
    feature_id: Optional[str]
    severity: Optional[str]
    effectiveness: Optional[float]
    frequency: Optional[str]
    tags: Optional[List[str]]
    category: Optional[str]
```

#### Pattern Object

```python
@dataclass
class TaskPattern:
    pattern_id: str
    pattern_type: str
    description: str
    frequency: int
    related_tasks: List[str]
    confidence: float
    keywords: List[str]
    context: Optional[str]
    severity: Optional[str]
```

---

## Core Components

### 1. Learning Extractor

**Location:** `2-engine/.autonomous/lib/learning_extractor.py`

**Purpose:** Extract structured learnings from THOUGHTS.md and DECISIONS.md

**Key Functions:**

- `extract_learnings()`: Main extraction function
- `_extract_from_thoughts()`: Parses THOUGHTS.md for learnings
- `_extract_from_decisions()`: Parses DECISIONS.md for decisions
- `categorize_learning()`: Categorizes learning by type
- `assess_impact()`: Assesses learning impact and priority

**Extraction Strategy:**

1. **Section Analysis**: Scans for learning-related sections (Key Insights, Learnings, Challenges)
2. **Pattern Matching**: Uses regex patterns to identify learning types
3. **Metadata Extraction**: Extracts severity, category, tags
4. **Impact Assessment**: Scores learning by reusability and applicability

**Learning Types Detected:**

- **Pattern**: Recurring patterns or best practices
- **Decision**: Architectural or approach decisions
- **Challenge**: Difficulties encountered
- **Optimization**: Performance or efficiency improvements
- **Bugfix**: Bugs fixed and lessons learned
- **Insight**: New understandings or discoveries

### 2. Pattern Matcher

**Location:** `2-engine/.autonomous/lib/pattern_matcher.py`

**Purpose:** Find similar tasks and identify recurring patterns

**Key Functions:**

- `find_similar_tasks()`: Finds tasks similar to a query
- `identify_patterns()`: Identifies recurring patterns
- `detect_recurring_issues()`: Detects recurring negative patterns
- `suggest_related_tasks()`: Suggests related tasks for a given task

**Similarity Algorithm:**

```
Similarity = (Keyword Similarity × 0.50) +
             (Context Similarity × 0.30) +
             (Error Type Similarity × 0.20)
```

- **Keyword Similarity**: Jaccard index of keyword sets
- **Context Similarity**: Feature ID and error type matching
- **Error Type Similarity**: Direct error type comparison

**Pattern Detection:**

1. **Keyword Frequency Analysis**: Counts keyword occurrences across learnings
2. **Pattern Clustering**: Groups learnings by keyword overlap
3. **Issue Detection**: Identifies recurring bugs and challenges
4. **Confidence Scoring**: Calculates pattern confidence based on frequency

### 3. Knowledge Retriever

**Location:** `2-engine/.autonomous/lib/knowledge_retriever.py`

**Purpose:** Search and retrieve relevant learnings

**Key Functions:**

- `search_learnings()`: Search with filters and relevance scoring
- `get_relevant_patterns()`: Get patterns relevant to query
- `suggest_learnings()`: Suggest learnings based on task context
- `get_stats()`: Get knowledge base statistics

**Relevance Scoring:**

```
Relevance = (Title Match × 0.50) +
            (Keyword Overlap × 0.30) +
            (Description Match × 0.20) +
            (Effectiveness Bonus × 0.10)
```

**Search Filters:**

- Learning type (pattern, decision, challenge, etc.)
- Category (technical, process, architectural, operational)
- Feature ID (F-XXX)
- Severity (critical, high, medium, low)
- Minimum effectiveness score

### 4. Learning Applier

**Location:** `2-engine/.autonomous/lib/learning_applier.py`

**Purpose:** Apply learnings to new tasks and track effectiveness

**Key Functions:**

- `inject_learnings_to_context()`: Inject learnings into executor prompt
- `apply_learning()`: Record learning application
- `track_effectiveness()`: Track learning effectiveness after task completion
- `get_learning_statistics()`: Get statistics for a specific learning

**Application Strategy:**

1. **Context Analysis**: Analyzes task context (title, description, feature_id)
2. **Learning Retrieval**: Gets top N most relevant learnings
3. **Relevance Boosting**: Boosts learnings by effectiveness and recency
4. **Context Injection**: Formats learnings as structured text for executor
5. **Effectiveness Tracking**: Tracks whether learnings were helpful

---

## Data Flow

### Learning Extraction Flow

```
Task Completion
    ↓
THOUGHTS.md + DECISIONS.md
    ↓
Learning Extractor
    ├─ Extract sections
    ├─ Parse patterns
    ├─ Categorize learnings
    └─ Assess impact
    ↓
Structured Learnings (YAML)
    ↓
Learning Index Update
    ↓
learning-index.yaml
```

### Learning Application Flow

```
New Task Execution
    ↓
Task Context (title, description, feature_id)
    ↓
Pattern Matcher
    ├─ Find similar tasks
    └─ Identify patterns
    ↓
Knowledge Retriever
    ├─ Search learnings
    ├─ Calculate relevance
    └─ Rank by effectiveness
    ↓
Learning Applier
    ├─ Select top N learnings
    ├─ Format as context
    └─ Inject into executor prompt
    ↓
Executor with Enhanced Context
    ↓
Task Execution (with learnings applied)
    ↓
Effectiveness Tracking
    └─ Record helpfulness and score
```

---

## Algorithms

### Jaccard Similarity

Used for keyword overlap calculation:

```python
def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """Calculate Jaccard similarity between two sets."""
    if not set1 or not set2:
        return 0.0

    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))

    return intersection / union if union > 0 else 0.0
```

### Keyword Extraction

Extracts meaningful keywords from text:

```python
def extract_keywords(text: str) -> Set[str]:
    """Extract keywords from text."""
    text = text.lower()

    # Remove stopwords
    stopwords = {"the", "a", "an", "and", "or", "but", ...}

    # Extract words (3+ characters)
    words = re.findall(r"\b[a-z]{3,}\b", text)

    # Filter stopwords
    keywords = {word for word in words if word not in stopwords}

    return keywords
```

### Effectiveness Tracking

Exponential Moving Average (EMA) for effectiveness:

```python
def update_effectiveness(current_ema: float, new_score: float, alpha: float = 0.3) -> float:
    """Update effectiveness using EMA."""
    if current_ema is None:
        return new_score

    return alpha * new_score + (1 - alpha) * current_ema
```

---

## Integration Points

### Executor Integration

The learning system integrates with the executor via prompt enhancement:

**Executor Prompt Enhancement:**

```markdown
# Relevant Learnings

Based on similar tasks, here are 3 relevant learning(s) that may help:

## Learning 1: Import Path Errors

**Source:** TASK-123
**Type:** bugfix
**Relevance:** 0.85
**Applicability:** high

**Description:** Import errors occur when using relative imports...
**Suggested Action:** Always use absolute imports from project root
**Historical Effectiveness:** 0.90

---

## How to Use These Learnings

1. Review each learning and determine if it applies
2. Apply relevant learnings to your approach
3. Provide feedback after task completion
```

### Storage Integration

**Learning Index:** `memory/insights/learning-index.yaml`

```yaml
metadata:
  version: "1.0.0"
  last_updated: "2026-02-01T14:42:30Z"
  total_learnings: 42

learnings:
  - learning_id: "TASK-123-LEARNING-1"
    task_id: "TASK-123"
    learning_type: "bugfix"
    title: "Import path errors"
    description: "..."
    effectiveness: 0.90
    ...

patterns: []
statistics: {}
```

### CLI Integration

All libraries provide CLI interfaces:

```bash
# Extract learnings
python3 learning_extractor.py runs/executor/run-0060

# Search learnings
python3 knowledge_retriever.py search "import error"

# Find patterns
python3 pattern_matcher.py patterns

# Apply learnings
python3 learning_applier.py inject --task-id TASK-XXX --title "My Task"
```

---

## API Reference

### Learning Extractor API

```python
from learning_extractor import LearningExtractor

# Initialize
extractor = LearningExtractor(run_dir="runs/executor/run-0060")

# Extract learnings
learnings = extractor.extract_learnings()

# Categorize learning
category = extractor.categorize_learning(learning)

# Assess impact
impact = extractor.assess_impact(learning)

# Save to file
output_path = extractor.save_learnings_to_file()
```

### Pattern Matcher API

```python
from pattern_matcher import PatternMatcher

# Initialize
matcher = PatternMatcher(learning_index_path="memory/insights/learning-index.yaml")

# Find similar tasks
similar = matcher.find_similar_tasks(query="implement feature", top_n=5)

# Identify patterns
patterns = matcher.identify_patterns(min_frequency=2)

# Detect recurring issues
issues = matcher.detect_recurring_issues()

# Suggest related tasks
related = matcher.suggest_related_tasks(task_id="TASK-123")
```

### Knowledge Retriever API

```python
from knowledge_retriever import KnowledgeRetriever

# Initialize
retriever = KnowledgeRetriever(learning_index_path="memory/insights/learning-index.yaml")

# Search learnings
results = retriever.search_learnings(
    query="import error",
    learning_type="bugfix",
    max_results=10
)

# Get relevant patterns
patterns = retriever.get_relevant_patterns(query="database")

# Suggest learnings
suggestions = retriever.suggest_learnings(
    task_context={"title": "My Task", "description": "..."}
)

# Get statistics
stats = retriever.get_stats()
```

### Learning Applier API

```python
from learning_applier import LearningApplier

# Initialize
applier = LearningApplier(
    learning_index_path="memory/insights/learning-index.yaml",
    effectiveness_log_path="memory/insights/effectiveness-log.yaml"
)

# Inject learnings into context
injected_text, suggestions = applier.inject_learnings_to_context(
    task_context={"task_id": "TASK-XXX", "title": "My Task"},
    max_learnings=3
)

# Apply learning
result = applier.apply_learning(
    learning_id="TASK-123-LEARNING-1",
    task_id="TASK-XXX",
    applied=True
)

# Track effectiveness
result = applier.track_effectiveness(
    learning_id="TASK-123-LEARNING-1",
    task_id="TASK-XXX",
    helpful=True,
    effectiveness_score=0.8
)
```

---

## Configuration

### Learning Index Configuration

**Location:** `memory/insights/learning-index.yaml`

**Configuration Options:**

```yaml
metadata:
  version: "1.0.0"
  auto_extract: true
  auto_index: true
  cleanup_threshold: 30  # days
```

### Threshold Configuration

**Similarity Thresholds:**

- Pattern matching: 0.3 (30%)
- Learning retrieval: 0.2 (20%)
- Learning injection: 0.25 (25%)

**Effectiveness Thresholds:**

- High effectiveness: 0.7+
- Medium effectiveness: 0.4-0.7
- Low effectiveness: <0.4

### Weights Configuration

**Similarity Weights:**

```python
KEYWORD_WEIGHT = 0.50
CONTEXT_WEIGHT = 0.30
ERROR_TYPE_WEIGHT = 0.20
```

**Relevance Weights:**

```python
TITLE_WEIGHT = 0.50
KEYWORD_WEIGHT = 0.30
DESCRIPTION_WEIGHT = 0.20
EFFECTIVENESS_BONUS = 0.10
```

---

## Performance Considerations

### Scalability

- **Index Size**: Supports 10,000+ learnings with linear search
- **Query Performance**: <100ms for typical queries
- **Memory Usage**: ~100KB per 100 learnings

### Optimization Strategies

1. **Lazy Loading**: Load learning index on first use
2. **Caching**: Cache pattern matching results
3. **Batch Operations**: Batch index updates
4. **Incremental Updates**: Only update changed learnings

### Phase 2 Enhancements (Future)

- SQLite backend for large-scale indexing
- Semantic similarity using embeddings
- Distributed index for multi-instance deployments
- Real-time index synchronization

---

## Troubleshooting

### Common Issues

**Issue:** Learning extraction finds no learnings
- **Solution:** Check THOUGHTS.md and DECISIONS.md have proper section headers

**Issue:** Pattern matching returns no results
- **Solution:** Lower similarity threshold or check learning-index.yaml has learnings

**Issue:** Effectiveness tracking not working
- **Solution:** Verify effectiveness-log.yaml exists and is writable

---

## Future Enhancements

### Phase 2 Features

1. **Machine Learning Integration**
   - Semantic similarity using sentence embeddings
   - Automatic learning categorization
   - Effectiveness prediction

2. **Advanced Analytics**
   - Learning trend analysis
   - Pattern evolution tracking
   - Knowledge gap identification

3. **Multi-Instance Support**
   - Cross-instance learning sharing
   - Distributed knowledge base
   - Federated learning

4. **Visualization Dashboard**
   - Learning statistics dashboard
   - Pattern visualization
   - Effectiveness tracking charts

---

## Related Documentation

- [Knowledge Base User Guide](../../../operations/.docs/knowledge-base-guide.md)
- [Feature F-010 Specification](../../../plans/features/FEATURE-010-knowledge-base.md)
- [Learning Index](../learning-index.yaml)

---

**End of Learning System Guide**
