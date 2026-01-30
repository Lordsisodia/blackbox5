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
  "session_id": "tl-2026-01-20-001",
  "timestamp": "2026-01-20T10:00:00Z",
  "problem": "Should we add caching?",
  "context": "",
  "iterations": [
    {
      "iteration_number": 1,
      "understanding": "Addressing: Should we add caching?",
      "confidence": 0.5,
      "assumptions_identified": ["Caching improves performance"],
      "assumptions_validated": [
        {
          "assumption": "Caching improves performance",
          "validity": "uncertain",
          "confidence": 0.6,
          "supporting_evidence": 1,
          "contradicting_evidence": 0
        }
      ],
      "first_principles_check": {
        "necessary": false,
        "confidence": 0.8,
        "reasoning": "Optimizing before measuring is premature"
      }
    }
  ],
  "converged": true,
  "final_iteration": 3,
  "confidence": 0.92,
  "answer": "NO - Caching optimization on wrong bottleneck",
  "reasoning_trace": ["..."],
  "duration_seconds": 2.3,
  "metadata": {
    "max_iterations": 10,
    "confidence_threshold": 0.90
  }
}
```

## Insights Format

Insights in `insights.json` contain:

```json
{
  "assumptions_validated": [
    {
      "assumption": "Database is the bottleneck",
      "validity": "invalid",
      "confidence": 0.85,
      "source_session": "tl-2026-01-20-001",
      "timestamp": "2026-01-20T10:00:00Z",
      "evidence_summary": {
        "supporting": 1,
        "contradicting": 3
      }
    }
  ],
  "fallacies_detected": [
    {
      "fallacy_type": "premature_optimization",
      "description": "Optimizing before measuring",
      "source_session": "tl-2026-01-20-001",
      "timestamp": "2026-01-20T10:00:00Z",
      "frequency": 5
    }
  ],
  "decision_patterns": [
    {
      "pattern": "Optimization without measurement",
      "typical_answer": "NO",
      "frequency": 5,
      "confidence": 0.95
    }
  ]
}
```

## Metrics Format

Metrics in `metrics.json` track:

```json
{
  "performance": {
    "avg_duration_seconds": 2.5,
    "avg_iterations_per_session": 4.2,
    "total_duration_seconds": 150.0
  },
  "quality": {
    "convergence_rate": 0.85,
    "avg_confidence": 0.88,
    "high_confidence_rate": 0.70
  },
  "usage": {
    "total_sessions": 60,
    "sessions_this_week": 12,
    "sessions_this_month": 45,
    "most_common_problems": [
      {"problem": "caching", "count": 15},
      {"problem": "optimization", "count": 12}
    ]
  }
}
```

## Integration with Thought Loop Framework

The Thought Loop Framework automatically saves to this directory when:

1. **Session completes** - Appends to `sessions.json`
2. **Insights discovered** - Updates `insights.json`
3. **Patterns recognized** - Updates `patterns.json`
4. **Metrics calculated** - Updates `metrics.json`

## Usage

```python
from thought_loop import ThoughtLoop

# Create loop - it will automatically save to project memory
loop = ThoughtLoop(
    project_id="siso-internal",
    auto_save=True  # Default: True
)

# Run - automatically saves session
result = await loop.run("Should we add caching?")

# Session is now in:
# blackbox5/5-project-memory/siso-internal/operations/agents/history/sessions/thought-loop/sessions.json
```

## Archival

Old sessions are automatically archived to `archive/{year}/{month}/` to keep files manageable.

- Sessions older than 30 days are archived
- Archive structure: `archive/2026/01/tl-2026-01-20-001.json`
