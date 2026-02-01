# Deep Research System - First Principles Architecture

## Core Purpose
Automatically discover, filter, transcribe, analyze, and deliver valuable AI/vibe coding content from YouTube on a daily basis.

---

## First Principles Breakdown

### 1. What are we actually doing?
- **Input**: YouTube videos (20+ creators, AI/coding keywords)
- **Process**: Discover → Filter → Transcribe → Analyze → Synthesize → Deliver
- **Output**: Structured insights delivered via Telegram

### 2. What are the atomic operations?
1. **Search** - Query YouTube API for recent videos
2. **Fetch Metadata** - Get titles, descriptions, channel info, view counts
3. **Score/Rank** - Evaluate relevance and quality
4. **Download** - Get audio/video for transcription
5. **Transcribe** - Convert speech to text
6. **Extract** - Pull key insights, timestamps, concepts
7. **Synthesize** - Organize into coherent learnings
8. **Deliver** - Send formatted output to Telegram

### 3. What data flows through?
```
Video ID → Metadata → Score → (if high) → Transcript → Insights → Report
```

---

## Proposed Agent-Based Architecture

### Agent 1: Discovery Agent (`agent_discovery.py`)
**Responsibility**: Find new videos

**Inputs**:
- List of YouTube channel IDs (20+ creators)
- Keywords: ["AI", "vibe coding", "Claude", "Cursor", "LLM", "agent", etc.]
- Time window: last 24 hours

**Outputs**:
- `discovered_videos.json` - Array of video objects with metadata

**Logic**:
- Query YouTube Data API v3 for each channel
- Filter by upload date (today only)
- Match against keywords (title + description)
- Store: video_id, title, description, channel, published_at, view_count, thumbnail

---

### Agent 2: Scoring Agent (`agent_scorer.py`)
**Responsibility**: Rank videos by value

**Inputs**:
- `discovered_videos.json`
- Scoring criteria weights

**Outputs**:
- `scored_videos.json` - Videos with relevance_score (0-100)

**Scoring Dimensions**:
1. **Creator Tier** (0-30): Known experts vs random channels
2. **Keyword Match** (0-25): Title match > description match
3. **Engagement** (0-20): View velocity (views/hours since publish)
4. **Recency** (0-15): Newer = higher
5. **Title Quality** (0-10): Has actionable terms ("how to", "tutorial", "breakdown")

**Logic**:
- Apply weighted scoring
- Sort by total score
- Keep top X% (configurable, default 30%)

---

### Agent 3: Transcription Agent (`agent_transcriber.py`)
**Responsibility**: Get transcripts for top videos

**Inputs**:
- `scored_videos.json` (filtered to top 30%)

**Outputs**:
- `transcripts/{video_id}.json` - Full transcript with timestamps

**Logic**:
- Try YouTube's native captions API first (free, fast)
- Fallback to Whisper API if no captions
- Store: segments with text + start_time + duration
- Save raw transcript to disk

---

### Agent 4: Extraction Agent (`agent_extractor.py`)
**Responsibility**: Pull key insights from transcripts

**Inputs**:
- `transcripts/{video_id}.json`
- Extraction prompt/template

**Outputs**:
- `extracted/{video_id}.md` - Structured insights

**Extraction Categories**:
1. **Key Concepts** - New tools, techniques, frameworks mentioned
2. **Actionable Takeaways** - Specific things to try
3. **Code Examples** - Any code shown/discussed
4. **Resources Mentioned** - Links, papers, repos
5. **Timestamps** - Key moments with brief descriptions
6. **Summary** - 2-3 paragraph overview

**Logic**:
- Use LLM (Claude API) with structured prompt
- Process each transcript independently
- Output markdown with clear sections

---

### Agent 5: Synthesis Agent (`agent_synthesizer.py`)
**Responsibility**: Combine daily extractions into cohesive report

**Inputs**:
- All `extracted/{video_id}.md` files for the day

**Outputs**:
- `daily_reports/YYYY-MM-DD.md` - Final daily digest

**Report Structure**:
```markdown
# AI Daily Digest - YYYY-MM-DD

## Today's Themes
[2-3 overarching themes across videos]

## Key Learnings

### 🛠️ New Tools Discovered
- Tool name: what it does (source: video title)

### 💡 Techniques & Patterns
- Pattern name: brief explanation

### 🔗 Resources
- Links mentioned across videos

### 📝 Detailed Breakdowns

#### [Video Title] by [Creator]
- **Key insight**: ...
- **Timestamp**: [MM:SS] - description
- **Action item**: ...

## Tomorrow's Exploration
[Questions or topics to investigate further]
```

---

### Agent 6: Delivery Agent (`agent_delivery.py`)
**Responsibility**: Send report via Telegram

**Inputs**:
- `daily_reports/YYYY-MM-DD.md`
- Telegram bot credentials

**Outputs**:
- Message sent to configured chat

**Options**:
1. Send full markdown as message
2. Send as file attachment
3. Send summary + link to full report

---

## Data Storage Structure

```
data/
├── config/
│   ├── channels.json          # List of YouTube channels to monitor
│   ├── keywords.json          # Search keywords
│   ├── scoring_weights.json   # Scoring configuration
│   └── telegram_config.json   # Bot token, chat ID
├── daily_runs/
│   └── YYYY-MM-DD/
│       ├── discovered_videos.json
│       ├── scored_videos.json
│       ├── transcripts/
│       │   └── {video_id}.json
│       ├── extracted/
│       │   └── {video_id}.md
│       └── daily_report.md
└── archive/
    └── all_time_videos.json   # Deduplication database
```

---

## Orchestration Options

### Option A: Sequential Pipeline
Each agent runs in order, triggered by previous completion.
Good for: Testing, debugging, clear data lineage

### Option B: Event-Driven
Agents subscribe to events (file creation, message queue)
Good for: Scaling, independent failures, parallel processing

### Option C: Scheduled Cron
Master script runs all agents in sequence on schedule
Good for: Simplicity, daily automation

**Recommendation**: Start with Option C, evolve to B if needed.

---

## Daily Workflow

```
06:00 AM - Discovery Agent runs
         ↓
         Scoring Agent runs
         ↓
         Transcription Agent runs (parallel per video)
         ↓
         Extraction Agent runs (parallel per transcript)
         ↓
         Synthesis Agent runs
         ↓
         Delivery Agent sends to Telegram
         ↓
06:30 AM - You get your digest
```

---

## API Requirements

| Service | Purpose | Cost |
|---------|---------|------|
| YouTube Data API v3 | Search, metadata | Free tier: 10k units/day |
| OpenAI Whisper | Transcription (fallback) | $0.006/minute |
| Anthropic Claude | Extraction, synthesis | ~$0.03-0.10 per video |
| Telegram Bot API | Delivery | Free |

---

## Configuration Files Needed

### channels.json
```json
{
  "creators": [
    {"name": "Fireship", "channel_id": "UCsBjURrPoezykLs9EqgamOA", "tier": 1},
    {"name": "Theo", "channel_id": "UCbRP3c757lWg9M-U7KfjVRQ", "tier": 1},
    {"name": "NetworkChuck", "channel_id": "UC9x0AN7LWHuX_aVHqmlCA", "tier": 2}
  ]
}
```

### keywords.json
```json
{
  "primary": ["AI", "Claude", "GPT", "LLM", "agent"],
  "secondary": ["vibe coding", "Cursor IDE", "Claude Code", "autonomous"],
  "tertiary": ["tutorial", "how to", "build", "implementation"]
}
```

---

## MVP vs Full System

### MVP (Week 1)
- [ ] Discovery Agent - search 5 channels, save to JSON
- [ ] Scoring Agent - simple keyword matching
- [ ] Transcription Agent - YouTube captions only
- [ ] Extraction Agent - basic LLM extraction
- [ ] Delivery Agent - simple Telegram message

### Full System (Week 2-3)
- [ ] Expand to 20+ channels
- [ ] Whisper fallback for transcripts
- [ ] Advanced scoring with engagement metrics
- [ ] Synthesis Agent for combined reports
- [ ] Scheduled automation (cron/systemd)
- [ ] Deduplication across days
- [ ] Web UI for configuration

---

## Open Questions

1. **How many videos per day max?** (affects cost)
2. **What time should delivery happen?**
3. **Should we include video thumbnails in Telegram?**
4. **Do you want to review before delivery initially?**
5. **Should extracted content link back to original timestamps?**
6. **Any specific 20 YouTubers you want to start with?**

---

## Next Steps

1. Review this architecture
2. Answer open questions
3. Create `config/` with your channels and preferences
4. Build Discovery Agent first (simplest, validates API access)
5. Iterate through remaining agents
6. Set up scheduling
