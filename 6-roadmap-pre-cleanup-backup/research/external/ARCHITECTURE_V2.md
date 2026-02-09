# Deep Research System V2 - First Principles Redesign

## Core Insight
You have TWO separate workflows:
1. **VIP Pipeline**: Specific YouTubers → ALL their videos → immediate processing
2. **On-Demand Pipeline**: You paste URL → instant analysis → stored

Both need: Extract → Categorize → Rank

---

## First Principles Analysis

### What is the actual value we're extracting?
Not just "transcripts" — we're extracting:
- **Knowledge artifacts**: Concepts, techniques, tools
- **Actionable intelligence**: Things you can implement
- **Relationships**: How ideas connect
- **Signals**: What's emerging, what's hype

### Why process locally?
- Privacy (your research stays yours)
- Cost (no per-minute API fees)
- Speed (no upload/download)
- Control (Claude Code can iterate)

### What does "categorize" actually mean?
We need a taxonomy that serves YOUR goals:
- By topic (AI, coding, business, etc.)
- By actionability (watch later vs implement now)
- By confidence (proven vs experimental)
- By relationship to your existing knowledge

### What does "rank" actually mean?
Not a single score — multi-dimensional:
- **Relevance**: How aligned with your current projects
- **Novelty**: How new is this information
- **Credibility**: Source reliability
- **Effort vs Impact**: Implementation cost vs benefit

---

## Revised Architecture: Two Pipelines

### Pipeline A: VIP Auto-Process

```
YouTube RSS/Check → New Video Detected → Download Captions → Extract → Categorize → Rank → Store → Notify
```

**Trigger**: New upload from VIP list
**Frequency**: Continuous (check every hour)
**Output**: Processed entry in your knowledge base

### Pipeline B: On-Demand

```
You Paste URL → Download Captions → Extract → Categorize → Rank → Store → Show Results
```

**Trigger**: Manual URL input
**Frequency**: On demand
**Output**: Immediate analysis + stored entry

---

## The Core Processing Engine (Shared)

### Step 1: Get Transcript (Local)

**Tool**: `yt-dlp` + local processing
```bash
# Gets auto-generated captions (no download needed)
yt-dlp --list-subs "URL"
yt-dlp --write-auto-sub --skip-download --sub-langs en "URL"
```

**Why yt-dlp**:
- Free, fast, local
- Gets YouTube's auto-captions (good enough for AI)
- No API keys needed
- Can extract metadata too

**Output**: `.srt` or `.vtt` file → parsed to clean text + timestamps

---

### Step 2: Extract Value (LLM)

**Input**: Clean transcript + metadata (title, channel, description)

**Extraction Prompt Structure**:
```
Analyze this video transcript and extract:

1. CORE CONCEPTS (2-5 items)
   - Name of concept/tool/technique
   - Brief explanation
   - Timestamp where introduced

2. ACTIONABLE TAKEAWAYS (1-3 items)
   - Specific thing viewer can do
   - Why it matters
   - Difficulty level (easy/medium/hard)

3. RESOURCES MENTIONED
   - Tools, links, papers, repos
   - With timestamps

4. KEY QUOTES (0-2 items)
   - Memorable/important statements

5. SUMMARY
   - 2-3 sentences on what this video delivers

6. QUALITY SIGNALS
   - Is this original research or repackaged?
   - Does the creator demonstrate or just talk?
   - Confidence level in information
```

**Output**: Structured JSON with all extractions

---

### Step 3: Categorize (LLM + Rules)

**Multi-dimensional tagging**:

```json
{
  "topic": ["AI", "vibe-coding", "Claude", "Cursor", "agents"],
  "type": ["tutorial", "news", "analysis", "opinion", "demo"],
  "actionability": "immediate|this-week|reference|entertainment",
  "technical_depth": "beginner|intermediate|advanced",
  "your_projects": ["siso-internal", "lifelock", "blackbox5"],
  "confidence": "high|medium|low"
}
```

**How it works**:
1. LLM suggests categories based on content
2. Rule-based overrides (certain channels = certain topics)
3. You can refine over time (learning system)

---

### Step 4: Rank (Multi-Factor)

**Not one score — ranked across dimensions**:

| Dimension | Weight | Factors |
|-----------|--------|---------|
| **Urgency** | 30% | Actionability + timeliness |
| **Relevance** | 25% | Match to your active projects |
| **Quality** | 20% | Creator tier + demonstrated expertise |
| **Novelty** | 15% | New info vs known concepts |
| **Effort** | 10% | Implementation difficulty |

**Output**: Ranked list per dimension + composite suggestion

---

## Data Model

### Video Entry
```json
{
  "id": "youtube_video_id",
  "url": "https://youtube.com/watch?v=...",
  "metadata": {
    "title": "...",
    "channel": "...",
    "published_at": "2025-01-30T10:00:00Z",
    "duration": 1200,
    "view_count": 50000
  },
  "source": {
    "type": "vip|manual",
    "added_at": "2025-01-30T12:00:00Z",
    "added_by": "auto|user"
  },
  "transcript": {
    "full_text": "...",
    "segments": [{"start": 0, "text": "..."}],
    "language": "en"
  },
  "extraction": {
    "concepts": [...],
    "takeaways": [...],
    "resources": [...],
    "quotes": [...],
    "summary": "...",
    "quality_signals": {...}
  },
  "categorization": {
    "topics": [...],
    "type": "...",
    "actionability": "...",
    "technical_depth": "...",
    "project_relevance": [...],
    "confidence": "..."
  },
  "ranking": {
    "urgency_score": 85,
    "relevance_score": 90,
    "quality_score": 75,
    "novelty_score": 60,
    "effort_score": 40,
    "composite": 78
  },
  "status": {
    "processed": true,
    "reviewed": false,
    "archived": false,
    "notes": ""
  }
}
```

---

## Storage Structure (Local)

```
deep-research/
├── data/
│   ├── videos/
│   │   └── {video_id}.json          # Full video entry
│   ├── transcripts/
│   │   └── {video_id}.txt           # Raw transcript text
│   ├── extracts/
│   │   └── {video_id}.md            # Human-readable extraction
│   └── index.json                   # Searchable index of all videos
├── config/
│   ├── vip_channels.json            # Your 10-20 YouTubers
│   ├── categories.json              # Your taxonomy
│   ├── project_context.json         # What you're working on
│   └── ranking_weights.json         # Your preference weights
├── scripts/
│   ├── pipeline_vip.py              # Auto-process VIP videos
│   ├── pipeline_manual.py           # Process single URL
│   ├── extract.py                   # Core extraction logic
│   ├── categorize.py                # Categorization logic
│   ├── rank.py                      # Ranking logic
│   └── utils.py                     # Shared functions
├── cli.py                           # Command line interface
└── app.py                           # Simple web UI (future)
```

---

## CLI Interface (Phase 1)

```bash
# Add a YouTuber to VIP list
./research.py vip add "CHANNEL_NAME" "CHANNEL_URL"

# Process a URL manually
./research.py process "https://youtube.com/watch?v=..."

# Check for new VIP videos
./research.py vip check

# List recent extractions
./research.py list --limit 10 --sort-by composite

# Search your knowledge base
./research.py search "vibe coding" --topic AI --actionability immediate

# Review unreviewed items
./research.py review

# Export for a project
./research.py export --project siso-internal --format markdown
```

---

## Implementation Phases

### Phase 1: Manual Pipeline (This Week)
- [ ] `process` command - paste URL, get extraction
- [ ] Local transcript download via yt-dlp
- [ ] Basic extraction with Claude API
- [ ] Simple categorization
- [ ] Store to JSON

### Phase 2: VIP Pipeline (Next Week)
- [ ] RSS monitoring for VIP channels
- [ ] Auto-download on new upload
- [ ] Queue system for batch processing
- [ ] Notification when done

### Phase 3: Intelligence (Later)
- [ ] Ranking algorithm
- [ ] Project context awareness
- [ ] Duplicate detection
- [ ] Cross-video insight linking

### Phase 4: Interface
- [ ] Simple web UI
- [ ] Telegram bot for mobile
- [ ] Search and filtering

---

## Technical Stack (Local-First)

| Component | Tool | Why |
|-----------|------|-----|
| Transcript | yt-dlp | Free, local, no API |
| Extraction | Claude API | Best at structured extraction |
| Storage | JSON files | Simple, portable, Claude can read |
| CLI | Python + click | Easy to extend |
| Config | JSON | Easy to edit |

---

## Open Questions

1. **VIP Channels**: Which 10-20 YouTubers? (Need list)
2. **Project Context**: What are you actively working on? (for relevance scoring)
3. **Categories**: What taxonomy makes sense for you?
4. **Review Flow**: Do you want to approve before storing, or store everything and filter later?
5. **Output Format**: Markdown files? SQLite? Both?

---

## Immediate Next Step

Build the `process` command:
1. You paste a YouTube URL
2. Script downloads transcript locally
3. Claude extracts structured value
4. Saves to JSON + markdown
5. Shows you the extraction

This validates the core loop before building automation.
