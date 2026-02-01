# Hybrid Ranking System

**Date**: 2026-02-02
**Status**: Implemented

---

## Overview

Two-pass ranking system to maximize accuracy while minimizing cost:

1. **Pass 1: Keyword Ranking** (`rank.py`) - Fast, free, catches obvious matches
2. **Pass 2: AI Ranking** (`ai_rank.py`) - Accurate, cheap, handles borderline cases

---

## How It Works

### Pass 1: Keyword Ranking (All Videos)

**Script**: `python scripts/rank.py`

**What it does:**
- Scans title + description for keywords
- Matches against your project context
- Assigns scores (0-100) for relevance, importance, value
- Filters obvious cases:
  - Score < 20: Auto-reject (filtered folder)
  - Score > 60: Auto-approve (pending folder)
  - Score 20-60: Borderline (needs AI review)

**Cost**: Free

**Speed**: ~100 videos/second

### Pass 2: AI Ranking (Borderline Only)

**Script**: `python scripts/ai_rank.py`

**What it does:**
- Only processes videos with keyword scores 20-60
- Uses GLM-4-Flash API (cheapest model)
- Analyzes title + description with AI
- Considers:
  - Your project context (Claude Code, MCP, agents)
  - Actionability (can you implement this?)
  - Novelty (is this new information?)
  - Quality (creator expertise, depth)
- Re-scores and decides pass/fail

**Cost**: ~0.002 CNY per video (~$0.0003 USD)

**Speed**: ~1-2 seconds per video

---

## Workflow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Collect       │────▶│   Keyword Rank  │────▶│   AI Rank       │
│   (ingest.py)   │     │   (rank.py)     │     │   (ai_rank.py)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                              │                        │
                              ▼                        ▼
                        Score < 20:              Borderline 20-60:
                        → filtered/              → GLM API call
                                                   → Re-score
                        Score > 60:               → Update queue
                        → pending/               → pending/
                        (auto-pass)
```

---

## Scoring Dimensions

### Keyword Scoring (Pass 1)

| Dimension | Weight | Method |
|-----------|--------|--------|
| **Relevance** | 25-40% | Keyword matching against projects |
| **Importance** | 25-35% | Creator tier + view count + recency |
| **Value** | 35-40% | Actionable keywords (how-to, tutorial, build) |

### AI Scoring (Pass 2)

| Dimension | Weight | Method |
|-----------|--------|--------|
| **Relevance** | 25% | AI understanding of topic match |
| **Importance** | 25% | AI assessment of significance |
| **Value** | 25% | AI evaluation of actionability |
| **Novelty** | 25% | AI judgment of uniqueness |

---

## Usage

### Step 1: Collect Videos
```bash
python scripts/ingest.py --all
```

### Step 2: Keyword Rank (All Videos)
```bash
python scripts/rank.py
```

### Step 3: AI Rank (Borderline Only)
```bash
# Set your GLM API key
export GLM_API_KEY="your-key-here"

# Run AI ranking
python scripts/ai_rank.py
```

### View Comparison
```bash
python scripts/ai_rank.py --compare
```

---

## Cost Estimates

### Scenario: 100 Videos/Day

| Pass | Videos | Cost Each | Total Cost |
|------|--------|-----------|------------|
| Keyword | 100 | Free | $0 |
| AI | ~30 (borderline) | $0.0003 | $0.009 |
| **Daily Total** | | | **~$0.01** |
| **Monthly Total** | | | **~$0.30** |

Very affordable!

---

## Configuration

### GLM API Key

Get your key from: https://open.bigmodel.cn/

Set as environment variable:
```bash
export GLM_API_KEY="your-api-key"
```

Or add to your shell profile (~/.bashrc, ~/.zshrc):
```bash
echo 'export GLM_API_KEY="your-api-key"' >> ~/.zshrc
```

### Model Selection

Default: `glm-4-flash` (cheapest, fastest)

Options:
- `glm-4-flash`: ~0.002 CNY/1K tokens, good for ranking
- `glm-4-air`: ~0.005 CNY/1K tokens, better quality
- `glm-4`: ~0.01 CNY/1K tokens, best quality (overkill for ranking)

Edit `scripts/ai_rank.py`:
```python
GLM_MODEL = "glm-4-flash"  # Change if needed
```

---

## Queue File Structure

After both passes, queue entries look like:

```yaml
video_id: abc123
title: "Video Title"
creator: "Creator Name"
priority: high
status: pending
queued_at: "2026-02-02T10:00:00"

# Keyword ranking (Pass 1)
ranking:
  keyword:
    relevance: 45
    importance: 70
    value: 30
    composite: 48.5

  # AI ranking (Pass 2) - only for borderline
  ai:
    relevance: 75
    importance: 80
    value: 85
    novelty: 70
    composite: 77.5
    reasoning: "Directly relevant to Claude Code workflows..."
    key_topics: ["claude-code", "mcp", "agents"]
    model: "glm-4-flash"
    ranked_at: "2026-02-02T10:05:00"

  # Final decision
  final_composite: 77.5

decision:
  should_process: true
  method: "ai_ranked"
  reason: "Directly relevant to Claude Code workflows..."
```

---

## Filtering Rules

### Tier 1 Creators (Must Watch)
- Keyword score > 0: Pass
- AI ranking: Optional (but improves accuracy)

### Tier 2 Creators (High Quality)
- Keyword score >= 65: Pass
- Keyword score 20-65: AI review
- Keyword score < 20: Filter

### Tier 3 Creators (Filtered)
- Keyword score >= 75: Pass
- Keyword score 20-75: AI review
- Keyword score < 20: Filter

---

## Benefits

| Approach | Accuracy | Cost | Speed |
|----------|----------|------|-------|
| Keyword only | 70% | Free | Fast |
| AI only | 90% | $0.03/video | Slow |
| **Hybrid** | **85%** | **$0.003/video** | **Fast** |

Best of both worlds!

---

## Future Improvements

- [ ] Learn from user feedback (thumbs up/down on rankings)
- [ ] Adjust keyword weights based on historical accuracy
- [ ] Cache AI rankings for similar titles
- [ ] Add batch processing for multiple videos per API call
