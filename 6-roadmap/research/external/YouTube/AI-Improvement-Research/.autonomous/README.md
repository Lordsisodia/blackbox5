# YouTube Transcript Analysis System

Based on BlackBox5's analysis architecture, this system analyzes YouTube transcripts to extract actionable insights.

## Architecture

```
Transcripts → Analyzer → Aggregator → Insights
```

## Components

### Agents
- **transcript-analyzer.md** - 3-loop analysis (Surface → Content → Insights)
- **insight-aggregator.md** - Cross-video synthesis

### Queues
- **transcript-queue.yaml** - Tracks transcripts ready for analysis

### Scripts
- **analyze-transcripts.sh** - Batch analysis runner

## Usage

### 1. Add Transcripts to Queue
Edit `queues/transcript-queue.yaml`:
```yaml
queue:
  - video_id: VIDEO_ID
    file: content/transcripts/channel/VIDEO_ID.md
    status: pending
    priority: P0
```

### 2. Run Analysis
```bash
cd .autonomous
./bin/analyze-transcripts.sh --batch-size 5
```

### 3. Review Output
Analyses saved to `output/analyses/{VIDEO_ID}-analysis.md`

## Scoring Framework

Videos scored on:
- **Relevance (1-5)** - Applicability to BlackBox5
- **Quality (1-5)** - Technical depth, accuracy
- **Actionability (1-5)** - Can we act on this?

**Total Score = (Relevance × 3) + (Quality × 2) + (Actionability × 1)**

## Analysis Template

Each analysis includes:
1. **Loop 1: Surface Scan** - Metadata, claims, credibility
2. **Loop 2: Content Archaeology** - Deep content analysis
3. **Loop 3: Insight Extraction** - Actionable recommendations

## Example Output

See: `output/analyses/aiLZMvMLYMg-analysis.md`

This demonstrates the full 3-loop analysis with scoring and recommendations.
