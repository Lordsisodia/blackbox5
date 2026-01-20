# Thought Loop Sessions

This folder contains **Thought Loop Framework** session history and learnings.

## Structure

```
thought-loop/
├── sessions.json       # All thought loop session records
├── insights.json       # Insights extracted from sessions
├── patterns.json       # Patterns discovered across sessions
├── metrics.json        # Performance and quality metrics
└── archive/            # Archived session data (by date)
    └── {year}/{month}/
        └── {session-id}.json
```

## Session Record Format

Each session in `sessions.json` contains:

```json
{
  "session_id": "tl-{date}-{sequence}",
  "timestamp": "ISO-8601 timestamp",
  "problem": "The problem statement",
  "context": "Additional context (optional)",
  "iterations": [
    {
      "iteration_number": 1,
      "understanding": "Current understanding",
      "confidence": 0.5,
      "assumptions_identified": ["List of assumptions"],
      "assumptions_validated": [
        {
          "assumption": "Assumption statement",
          "validity": "valid|invalid|uncertain",
          "confidence": 0.8,
          "supporting_evidence": 2,
          "contradicting_evidence": 0
        }
      ],
      "first_principles_check": {
        "necessary": false,
        "confidence": 0.8,
        "reasoning": "Explanation"
      }
    }
  ],
  "converged": true,
  "final_iteration": 3,
  "confidence": 0.92,
  "answer": "YES/NO/MAYBE with reasoning",
  "reasoning_trace": ["List of reasoning steps"],
  "duration_seconds": 2.3,
  "metadata": {
    "max_iterations": 10,
    "confidence_threshold": 0.90
  }
}
```

## Integration

The Thought Loop Framework automatically saves to this directory when configured with:

```python
loop = ThoughtLoop(
    project_id="{PROJECT_ID}",
    auto_save=True
)
```

## Archival

Sessions older than 30 days are automatically archived to `archive/{year}/{month}/`.
