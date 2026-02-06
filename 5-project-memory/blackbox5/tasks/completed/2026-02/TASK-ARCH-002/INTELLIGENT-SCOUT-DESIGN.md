# Intelligent Scout Design

**Version:** 1.0.0
**Status:** Implementation Ready
**Date:** 2026-02-04

---

## Problem with Previous Scout

The original Scout (`scout-analyze.py`) was a **Python script** that:
- Parsed YAML files with regex patterns
- Used simple heuristics (counting null values)
- Had no real understanding of context
- Couldn't identify complex patterns
- Was essentially a "dumb" data processor

**Result:** It found 1 opportunity ("23 skills have null metrics") but missed nuanced issues.

---

## Solution: Intelligent Scout

The **Intelligent Scout** spawns **actual Claude Code instances** via the Task tool to perform real AI-powered analysis.

### Key Differences

| Aspect | Old Scout | Intelligent Scout |
|--------|-----------|-------------------|
| **Implementation** | Python script | Claude Code subagents |
| **Analysis** | Regex/pattern matching | AI-powered understanding |
| **Context awareness** | None | Full codebase context |
| **Pattern detection** | Simple counting | Complex relationship analysis |
| **Recommendations** | Template-based | Context-aware suggestions |
| **Cost** | Free (compute only) | ~$0.05-0.15 per analyzer |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    INTELLIGENT SCOUT                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────┐                                                  │
│  │  Scout Orchestrator │                                              │
│  │  (Python script)    │                                              │
│  └────────┬────────┘                                                  │
│           │ Spawns 5 Claude Code instances via Task tool             │
│           ▼                                                           │
│  ┌─────────┬─────────┬─────────┬─────────┬─────────┐                 │
│  │ Skill   │ Process │ Docs    │ Arch    │ Metrics │                 │
│  │Analyzer │Analyzer │Analyzer │Analyzer │Analyzer │                 │
│  │ (Claude)│ (Claude)│ (Claude)│ (Claude)│ (Claude)│                 │
│  └────┬────┴────┬────┴────┬────┴────┬────┴────┬────┘                 │
│       │         │         │         │         │                       │
│       └─────────┴────┬────┴─────────┴─────────┘                       │
│                      ▼                                                │
│           ┌─────────────────┐                                         │
│           │  Aggregate      │                                         │
│           │  & Score        │                                         │
│           └────────┬────────┘                                         │
│                    ▼                                                  │
│           ┌─────────────────┐                                         │
│           │  Generate Report│                                         │
│           │  (JSON + YAML)  │                                         │
│           └─────────────────┘                                         │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## How It Works

### Phase 1: Spawn Analyzers

The orchestrator spawns 5 Claude Code subagents, each with a specialized prompt:

```python
# Example: Skill Analyzer Prompt
prompt = """
You are a Skill Effectiveness Analyzer for BlackBox5.

MISSION: Analyze the skill system to find improvement opportunities.

FILES TO ANALYZE:
- operations/skill-metrics.yaml
- operations/skill-usage.yaml
- operations/skill-selection.yaml

WHAT TO LOOK FOR:
1. Skills with null effectiveness scores
2. Skills with low success rates
3. Skills that are never triggered
4. Skills with poor trigger accuracy
5. Gaps in skill coverage

OUTPUT: Return structured JSON with opportunities, scores, and recommendations.
"""

# Spawn via subprocess (simulating Task tool)
result = subprocess.run([
    "claude", "code",
    "--headless",
    "--prompt", prompt,
    "--allowed-tools", "Read,Glob,Grep",
    "--output-json"
])
```

### Phase 2: Parallel Execution

Each analyzer runs independently:
- **Skill Analyzer:** Reads skill configs, identifies gaps
- **Process Analyzer:** Reads recent runs, finds friction
- **Documentation Analyzer:** Checks docs vs reality
- **Architecture Analyzer:** Identifies structural issues
- **Metrics Analyzer:** Finds measurement gaps

### Phase 3: Aggregation

The orchestrator collects all results:
```python
# Combine opportunities from all analyzers
all_opportunities = []
for result in analyzer_results:
    all_opportunities.extend(result["opportunities"])

# Calculate scores: (impact × 3) + (frequency × 2) - (effort × 1.5)
for opp in all_opportunities:
    opp["total_score"] = calculate_score(opp)

# Sort by score
all_opportunities.sort(key=lambda x: x["total_score"], reverse=True)
```

### Phase 4: Report Generation

Generates both JSON (machine-readable) and YAML (human-readable) reports.

---

## Files Created

```
2-engine/.autonomous/bin/
├── scout-intelligent.py          # Main orchestrator
└── intelligent-scout.sh          # Bash wrapper (alternative)

5-project-memory/blackbox5/.autonomous/analysis/scout-reports/
└── scout-report-intelligent-{timestamp}.{json,yaml}
```

---

## Usage

### Basic Usage
```bash
# Run all analyzers sequentially
python3 ~/.blackbox5/2-engine/.autonomous/bin/scout-intelligent.py

# Run in parallel (faster)
python3 ~/.blackbox5/2-engine/.autonomous/bin/scout-intelligent.py --parallel

# Run specific analyzers
python3 ~/.blackbox5/2-engine/.autonomous/bin/scout-intelligent.py \
    --analyzers skill-analyzer process-analyzer
```

### Output
```yaml
scout_report:
  id: "20260204-143022"
  timestamp: "2026-02-04T14:30:22Z"
  summary:
    total_opportunities: 15
    high_impact: 6
    quick_wins: 4
    patterns_found: 3

  opportunities:
    - id: "skill-analyzer-001"
      title: "23 skills lack effectiveness metrics"
      category: "skills"
      impact_score: 4
      effort_score: 3
      frequency_score: 3
      total_score: 13.5
      evidence: "skill-metrics.yaml shows all null values"
      suggested_action: "Implement automatic metrics collection"

  quick_wins:
    - id: "docs-analyzer-003"
      title: "Fix broken link in README"
      effort_minutes: 5
      impact: "high"

  recommendations:
    - priority: 1
      opportunity_id: "skill-analyzer-001"
      rationale: "Score: 13.5 | Impact: 4/5 | Effort: 3/5"
```

---

## Cost Analysis

| Component | Cost per Run | Notes |
|-----------|--------------|-------|
| Skill Analyzer | ~$0.03 | Reads 3 files, generates JSON |
| Process Analyzer | ~$0.04 | Reads 5-10 run folders |
| Documentation Analyzer | ~$0.03 | Scans docs directory |
| Architecture Analyzer | ~$0.05 | Deep code analysis |
| Metrics Analyzer | ~$0.02 | Reads YAML configs |
| **Total** | **~$0.15** | For ~50 opportunities found |

**ROI:** If the Scout finds 1 high-impact improvement that saves 30 minutes of developer time, it pays for itself 100x.

---

## Integration with RALF

The Intelligent Scout integrates with the existing RALF system:

```
RALF Executor
     │
     ▼ (triggers every 5 runs)
┌─────────────────┐
│ Intelligent Scout│
│ (spawn analyzers)│
└────────┬────────┘
         │
         ▼ (generates report)
┌─────────────────┐
│ Planner Agent   │
│ (convert to     │
│  IMP-*.md tasks)│
└────────┬────────┘
         │
         ▼ (queues tasks)
┌─────────────────┐
│ Task Queue      │
│ (queue.yaml)    │
└────────┬────────┘
         │
         ▼ (executes)
┌─────────────────┐
│ RALF Executor   │
│ (implements)    │
└─────────────────┘
```

---

## Future Enhancements

### Phase 2: Automated Execution
- Auto-trigger Scout every 5 runs
- Auto-create IMP-*.md tasks from opportunities
- Auto-queue high-priority items

### Phase 3: Learning Loop
- Scout learns from past improvements
- Adjusts scoring based on actual impact
- Identifies which analyzers are most effective

### Phase 4: Predictive Analysis
- Predict issues before they become problems
- Identify trends in metrics
- Suggest preventive improvements

---

## Comparison: Old vs New

### Old Scout (Python Script)
```python
# Simple regex matching
def analyze_skill_metrics():
    with open("skill-metrics.yaml") as f:
        content = f.read()
    # Count null occurrences
    null_count = content.count("null")
    if null_count > 50:
        return Opportunity(
            title=f"{null_count} null values found",
            description="Many skills lack metrics"
        )
```

### New Scout (Claude Code Subagent)
```python
# AI-powered analysis
prompt = """
Analyze skill-metrics.yaml and identify:
1. Which specific skills lack metrics
2. Why those skills might not be tracked
3. What the impact of missing metrics is
4. Concrete steps to fix the issue

Consider the context of the entire skill system.
"""

result = spawn_claude_subagent(prompt)
# Returns nuanced, context-aware findings
```

---

## Success Metrics

| Metric | Old Scout | Intelligent Scout (Target) |
|--------|-----------|---------------------------|
| Opportunities per run | 1-2 | 10-20 |
| False positives | Low | Lower (AI validation) |
| Context awareness | None | Full codebase |
| Actionable recommendations | Basic | Detailed |
| Time to generate | 2 seconds | 2 minutes |
| Cost | Free | ~$0.15 |

---

## Conclusion

The Intelligent Scout transforms improvement discovery from a **dumb data processor** into an **AI-powered analysis system**. By leveraging Claude Code's understanding of context, patterns, and relationships, it finds more valuable improvements with better recommendations.

**Key Achievement:** A Scout that actually understands what it's looking at.

**Next Step:** Run the Intelligent Scout and compare results to the old Scout.
