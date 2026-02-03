# Scout Worker Timeline Memory

**Purpose:** Long-term chronological memory of all work performed across runs
**Updated:** Automatically at the end of each run
**Format:** YAML frontmatter with markdown body
**Injected via:** SessionStart hook

---

```yaml
timeline_memory:
  version: "1.0.0"
  agent: scout-worker
  created: "2026-02-04T00:00:00Z"
  last_updated: "2026-02-04T00:00:00Z"
  total_runs: 0

# Chronological history of all work performed
history:
  # Example entry (populated automatically):
  # - run_id: "run-20260204-001"
  #   timestamp: "2026-02-04T10:00:00Z"
  #   source: "github.com/user/repo"
  #   source_type: "github"
  #   patterns_extracted: 3
  #   pattern_ids: ["P-001", "P-002", "P-003"]
  #   status: "success"
  #   tokens_used: 2800
  #   validator_feedback: "incorporated"
  #   notes: "Extracted auth patterns successfully"

# Current work context (what to do next)
current_context:
  last_source_scanned: null
  next_in_queue: null
  queue_depth: 0
  patterns_awaiting_analysis: []

# Work statistics by source type
stats_by_source:
  github:
    total_scanned: 0
    patterns_found: 0
    avg_patterns_per_source: 0
  youtube:
    total_scanned: 0
    patterns_found: 0
    avg_patterns_per_source: 0
  docs:
    total_scanned: 0
    patterns_found: 0
    avg_patterns_per_source: 0

# Learning progression
skill_progression:
  extraction_accuracy: 0.0  # 0-1 scale
  token_efficiency: 0.0     # patterns per token
  validator_satisfaction: 0.0  # based on feedback
  common_mistakes: []       # mistakes to avoid
  mastered_patterns: []     # pattern types mastered

# Active work queue (what needs to be done)
work_queue:
  priority_sources: []      # high-priority sources to scan
  backlog: []               # pending sources
  in_progress: null         # currently scanning
  completed_today: 0
  failed_today: 0
```

---

## How to Use This Memory

**At the start of each run:**
1. Read this file to understand what you've done before
2. Check `current_context` for what to work on next
3. Review `history` to avoid re-scanning recent sources
4. Apply lessons from `skill_progression`

**At the end of each run:**
1. Append new entry to `history`
2. Update `current_context` with next work item
3. Update `stats_by_source` and `skill_progression`
4. Update `work_queue` priorities

## Work Assignment Logic

**How you know what to do:**

1. **Check `work_queue.priority_sources`** - These are your highest priority tasks
2. **If empty, check communications/scout-state.yaml** - Shared queue with other agents
3. **Select one source** - Never batch multiple sources
4. **Update `work_queue.in_progress`** - Mark what you're working on
5. **Do the work** - Extract patterns from the source
6. **Update timeline** - Save what you accomplished

## Integration with Validator

The validator reads this timeline to:
- Track your progress over time
- Identify patterns in your work
- Suggest improvements based on history
- Ensure you're following priorities

---

*This file is automatically injected into your context via the SessionStart hook.*
