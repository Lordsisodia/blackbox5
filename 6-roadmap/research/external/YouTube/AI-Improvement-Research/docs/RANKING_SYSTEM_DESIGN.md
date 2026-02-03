# YouTube Channel Ranking System Design

> **Status:** Design Document
> **Last Updated:** 2026-02-04
> **Goal:** Create an ELO-style/benchmark leaderboard to rank channels by value provided

---

## 1. What is "Value" for Educational Content?

### Core Value Dimensions

| Dimension | Definition | Signals |
|-----------|------------|---------|
| **Knowledge Density** | Information per minute | Video length vs content depth, transcript analysis |
| **Production Quality** | Professional presentation | Audio/video quality, editing, structure |
| **Consistency** | Reliable output | Upload frequency, sustained quality over time |
| **Engagement Quality** | Meaningful interaction | Comment sentiment, watch time, community health |
| **Educational Impact** | Actual learning outcomes | Tutorial completion, project implementations |
| **Novelty** | Fresh, non-obvious content | Original research, unique perspectives |
| **Accessibility** | Approachable for target audience | Clear explanations, progressive difficulty |

---

## 2. Scoring Algorithm Options

### Option A: Aggregate Scoring (Recommended)

Composite score from multiple weighted factors:

```
Channel Score =
    (Knowledge × 0.25) +
    (Engagement × 0.20) +
    (Consistency × 0.20) +
    (Quality × 0.15) +
    (Impact × 0.15) +
    (Novelty × 0.05)
```

### Option B: ELO-Style Pairwise Comparison

```
ELO_Rating_new = ELO_Rating_old + K × (Actual_Outcome - Expected_Outcome)

Where:
- K = learning rate (32 for established channels, 64 for new)
- Expected_Outcome = 1 / (1 + 10^((Opponent_Rating - Your_Rating)/400))
```

**Comparison Triggers:**
- Same topic covered by different channels
- Viewer migration patterns (watched A then B)
- Community recommendations

### Recommendation: Hybrid Approach

Use **Aggregate Scoring** for initial ranking, then **ELO adjustments** based on:
- Head-to-head topic coverage
- Temporal performance (trending up/down)
- Community votes (future feature)

---

## 3. Metric Definitions

### 3.1 Knowledge Density Score (0-100)

```python
def calculate_knowledge_density(video):
    # Factors:
    # - Transcript word count / video duration
    # - Technical term density (NLP analysis)
    # - Code snippet count
    # - Concept explanations per minute

    words_per_minute = transcript_word_count / duration_minutes
    technical_density = technical_terms / total_words
    code_blocks = count_code_snippets(transcript)

    return normalize(
        (words_per_minute × 0.3) +
        (technical_density × 100 × 0.4) +
        (code_blocks × 5 × 0.3)
    )
```

### 3.2 Engagement Quality Score (0-100)

```python
def calculate_engagement(video, channel):
    # Raw metrics
    view_velocity = views / hours_since_upload
    like_ratio = likes / views
    comment_quality = analyze_comment_sentiment(comments)

    # Channel-level trends
    avg_watch_time = estimate_watch_time(analytics)
    subscriber_conversion = views / subscriber_count

    return normalize(
        (log(view_velocity) × 0.25) +
        (like_ratio × 100 × 0.25) +
        (comment_quality × 0.25) +
        (subscriber_conversion × 100 × 0.25)
    )
```

### 3.3 Consistency Score (0-100)

```python
def calculate_consistency(channel, last_n_videos=20):
    # Upload regularity
    upload_intervals = calculate_intervals(channel.uploads)
    regularity = 1 / std_dev(upload_intervals)

    # Quality consistency
    quality_variance = variance([v.quality_score for v in last_n_videos])

    # Longevity
    channel_age_days = (now - channel.created_at).days
    total_videos = len(channel.videos)

    return normalize(
        (regularity × 30 × 0.4) +
        ((100 - quality_variance) × 0.3) +
        (log(total_videos) × 10 × 0.2) +
        (log(channel_age_days) × 5 × 0.1)
    )
```

### 3.4 Production Quality Score (0-100)

```python
def estimate_production_quality(video):
    # Available signals from yt-dlp:
    # - Resolution (1080p, 4K, etc.)
    # - Audio bitrate
    # - Has chapters/sections
    # - Thumbnail quality (CV analysis)
    # - Has captions/subtitles

    resolution_score = parse_resolution(video.height)  # 1080p = 100
    has_chapters = 20 if video.chapters else 0
    has_captions = 15 if video.subtitles else 0
    audio_quality = normalize_bitrate(video.abr)

    return (
        (resolution_score × 0.4) +
        (audio_quality × 0.3) +
        has_chapters +
        has_captions
    )
```

### 3.5 Impact Score (0-100)

```python
def calculate_impact(video, channel):
    # Long-term value signals:
    # - Evergreen ratio (views after 30 days / total views)
    # - Reference rate (linked in other videos)
    # - Playlist inclusion frequency
    # - Search ranking for key terms

    evergreen_ratio = views_after_30d / total_views
    reference_count = count_video_mentions(video.id)
    playlist_inclusions = count_playlist_appearances(video.id)

    return normalize(
        (evergreen_ratio × 100 × 0.4) +
        (log(reference_count + 1) × 20 × 0.3) +
        (playlist_inclusions × 5 × 0.3)
    )
```

### 3.6 Novelty Score (0-100)

```python
def calculate_novelty(video, all_videos):
    # Content uniqueness:
    # - Title/topic similarity to existing content
    # - First-mover advantage on new topics
    # - Original research/code

    topic_embedding = embed_topic(video.title + video.description)
    similarity_scores = [cosine_sim(topic_embedding, other) for other in all_videos]

    return 100 - (mean(similarity_scores) × 100)
```

---

## 4. Data Model

### 4.1 Channel Ranking Schema

```yaml
channel_rankings:
  channel_id: str          # YouTube channel ID
  channel_name: str

  # Current scores
  overall_score: float     # 0-100 composite
  rank: int                # Current position
  tier: str                # S/A/B/C/D

  # Component scores
  knowledge_score: float
  engagement_score: float
  consistency_score: float
  quality_score: float
  impact_score: float
  novelty_score: float

  # ELO system
  elo_rating: int          # Starting: 1500
  elo_matches: int         # Number of comparisons

  # Historical tracking
  score_history: list      # [{date, score, rank}, ...]
  trend_direction: str     # rising/falling/stable

  # Metadata
  last_calculated: datetime
  calculation_version: int # For algorithm updates
```

### 4.2 Video Scores Schema

```yaml
video_scores:
  video_id: str
  channel_id: str

  # Individual scores
  knowledge_density: float
  engagement_rate: float
  production_quality: float
  novelty_score: float

  # Derived metrics
  value_per_minute: float
  expected_watch_time: float

  # Category classification
  primary_topic: str
  difficulty_level: str   # beginner/intermediate/advanced
  content_type: str       # tutorial/explainer/review/news
```

### 4.3 Comparison Events (for ELO)

```yaml
comparison_events:
  event_id: str
  timestamp: datetime

  channel_a_id: str
  channel_b_id: str

  comparison_type: str    # topic_overlap/viewer_flow/community_vote
  topic: str              # What was compared

  outcome: float          # 1.0 = A wins, 0.0 = B wins, 0.5 = draw
  confidence: float       # How certain is this outcome

  # Context
  video_a_id: str         # Specific videos compared
  video_b_id: str
```

---

## 5. Implementation Pipeline

### Stage 1: Data Collection (Hourly)

```
scrape.yml (existing)
  ↓
Collect video metadata + transcripts
  ↓
Store in database/videos/
```

### Stage 2: Score Calculation (Daily)

```
rank_calculation.py
  ↓
For each new video:
  - Calculate individual scores
  - Update channel aggregates
  ↓
For each channel:
  - Recalculate component scores
  - Compute composite score
  - Determine tier/rank
  ↓
Generate leaderboard update
```

### Stage 3: ELO Adjustments (Weekly)

```
elo_update.py
  ↓
Identify comparison opportunities:
  - Same topic, different channels
  - Viewer migration patterns
  ↓
Calculate expected vs actual outcomes
  ↓
Update ELO ratings
  ↓
Blend with aggregate scores (70/30 split)
```

### Stage 4: Report Generation (Weekly)

```
leaderboard_report.py
  ↓
Generate:
  - Top 100 channels overall
  - Category-specific rankings
  - Trending (rising/falling)
  - New entrant highlights
  ↓
Commit to: reports/leaderboard_YYYY-MM-DD.md
```

---

## 6. Tier System

| Tier | Score Range | Description |
|------|-------------|-------------|
| **S** | 90-100 | Exceptional, must-watch content |
| **A** | 80-89 | Excellent, consistently valuable |
| **B** | 70-79 | Good, worth subscribing |
| **C** | 60-69 | Average, some good content |
| **D** | <60 | Below average, limited value |

### Category-Specific Rankings

Each channel gets both:
- **Overall Rank:** Across all categories
- **Category Rank:** Within their primary focus

Categories:
- Data Science / ML
- Programming / Software Engineering
- AI Research
- Web Development
- DevOps / Infrastructure
- Career / Business

---

## 7. Visualization Ideas

### 7.1 Leaderboard Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│  SISO AI/ML Channel Leaderboard      Last Updated: 2/4/26  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🏆 TOP 10 OVERALL                                          │
│  ─────────────────────────────────────────────────────────  │
│  #1  [S] Andrej Karpathy          94.2  ↑ +0.3             │
│  #2  [S] 3Blue1Brown              93.8  ↑ +1.2             │
│  #3  [S] StatQuest                92.1  → stable           │
│  #4  [A] Fireship                 89.5  ↑ +2.1             │
│  #5  [A] Yannic Kilcher           88.9  ↓ -0.5             │
│  ...                                                        │
│                                                             │
│  📈 TRENDING THIS WEEK                                      │
│  ─────────────────────────────────────────────────────────  │
│  +12  Dave Ebbelaar        [Knowledge +15%]                │
│  +8   Riley Brown          [Engagement +22%]               │
│  +5   AI Revolution        [Consistency improved]          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Channel Detail Card

```
┌────────────────────────────────────┐
│  Fireship                          │
│  ═════════════════════════════════ │
│  Rank: #4 Overall | #1 Web Dev     │
│  Tier: A (89.5/100)                │
│  Trend: ↑ Rising (+2.1 this month) │
│                                    │
│  Score Breakdown:                  │
│  ├─ Knowledge:    85 ████████░░   │
│  ├─ Engagement:   95 ██████████   │
│  ├─ Consistency:  92 █████████▌   │
│  ├─ Quality:      88 ████████▊    │
│  ├─ Impact:       87 ████████▋    │
│  └─ Novelty:      91 █████████▏   │
│                                    │
│  Recent Top Videos:                │
│  • "React in 100 Seconds" - 98 KD  │
│  • "CSS Grid Guide" - 94 KD        │
│                                    │
│  [View Full Profile] [Compare]     │
└────────────────────────────────────┘
```

### 7.3 Comparison Tool

```
┌────────────────────────────────────────────────────────────┐
│  Head-to-Head Comparison                                   │
├────────────────────────────────────────────────────────────┤
│                                                            │
│         Fireship          vs         Traversy Media       │
│         ─────────                    ─────────────        │
│         Rank: #4                     Rank: #12            │
│         Score: 89.5                  Score: 82.3          │
│                                                            │
│  Knowledge    ████████░░ 85    ███████░░░ 78              │
│  Engagement   ██████████ 95    ████████░░ 85              │
│  Consistency  █████████▌ 92    ████████▌  88              │
│  Quality      ████████▊  88    ████████░  82              │
│  Impact       ████████▋  87    ███████▌   76              │
│                                                            │
│  Common Topics: React, JavaScript, CSS                    │
│  Fireship wins on: Engagement, Novelty                    │
│  Traversy wins on: Consistency                            │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 8. Implementation Phases

### Phase 1: Basic Scoring (Week 1)
- [ ] Implement aggregate scoring for existing metrics
- [ ] Calculate scores for all scraped channels
- [ ] Generate simple leaderboard report

### Phase 2: Advanced Metrics (Week 2-3)
- [ ] Add transcript analysis for knowledge density
- [ ] Implement comment sentiment analysis
- [ ] Build novelty detection (topic clustering)

### Phase 3: ELO System (Week 4)
- [ ] Implement pairwise comparison detection
- [ ] Build ELO rating updates
- [ ] Blend ELO with aggregate scores

### Phase 4: Dashboard (Week 5-6)
- [ ] Build static HTML leaderboard
- [ ] Add trend visualizations
- [ ] Create comparison tool

### Phase 5: Automation (Week 7)
- [ ] Schedule daily score recalculation
- [ ] Auto-generate weekly reports
- [ ] Set up change alerts (significant rank changes)

---

## 9. Open Questions

1. **Transcript Analysis:** Do we have transcripts for all videos? If not, how do we handle knowledge density for transcript-less videos?

2. **Comment Analysis:** Can we scrape comments at scale? YouTube API has quota limits.

3. **Category Classification:** Manual categorization or automatic topic modeling?

4. **Weight Tuning:** How to validate the scoring weights? A/B testing with user feedback?

5. **Bias Prevention:** How to prevent "rich get richer" (popular channels getting higher engagement scores)?

---

## 10. Files to Create

```
scripts/
├── calculate_rankings.py      # Main scoring algorithm
├── elo_system.py              # ELO rating management
├── analyze_transcripts.py     # NLP for knowledge density
├── generate_leaderboard.py    # Report generation
└── compare_channels.py        # Head-to-head comparison

database/
├── channel_rankings.json      # Current rankings
├── video_scores.json          # Individual video scores
└── comparison_history.json    # ELO match history

reports/
├── leaderboard_latest.md      # Current leaderboard
├── trending.md                # Rising/falling channels
└── category_rankings/         # Per-category boards

docs/
├── RANKING_SYSTEM_DESIGN.md   # This document
├── SCORING_EXPLAINED.md       # How scores work
└── TIER_DEFINITIONS.md        # What each tier means
```

---

## Next Steps

1. **Review this design** - Any changes to weights or approach?
2. **Implement Phase 1** - Basic scoring with existing data
3. **Test on subset** - Validate scores make intuitive sense
4. **Iterate** - Adjust based on results

Should I start implementing Phase 1 (basic aggregate scoring)?
