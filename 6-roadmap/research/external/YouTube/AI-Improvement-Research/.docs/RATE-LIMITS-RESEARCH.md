# YouTube Scraping Rate Limits - Research Summary

**Date**: 2026-02-02
**Status**: Research Complete

---

## Current Data Collection Status

From our test run on David Ondrej:
- **19 videos** collected (9 existing + 10 new)
- **8 videos** queued for extraction
- **Transcript sizes**: 445-537 characters for Shorts (~20 sec videos)
- **Processing time**: ~2.5 seconds per video (with 2-5s delays)

---

## Rate Limits Research

### 1. YouTube RSS Feeds

**Status**: Undocumented/Unofficial endpoints

| Aspect | Details |
|--------|---------|
| Official documentation | ❌ None - RSS feeds are unofficial |
| Rate limit | ❌ Not documented |
| Current status | ⚠️ Reports of 404 errors in late 2025 |
| Recommended frequency | Every 15-60 minutes per channel |

**Best Practices**:
- Poll RSS no more than once per hour per channel
- Add delays between requests (2-5 seconds)
- Cache channel IDs to avoid repeated lookups
- Monitor for 404 errors (possible deprecation)

### 2. yt-dlp Rate Limits

**Status**: No hard limits, but polite scraping required

| Aspect | Details |
|--------|---------|
| Official rate limit | ❌ None enforced |
| Practical limit | ~1 request per 2-5 seconds |
| IP blocking risk | ⚠️ Yes, if too aggressive |
| Recommended delay | 2-5 seconds between videos |

**Current Implementation**:
```python
delay = random.uniform(2, 5)  # 2-5 seconds
time.sleep(delay)
```

**Safe Rate Calculation**:
- 1 video per 3 seconds (average)
- = 20 videos per minute
- = 1,200 videos per hour
- = ~28,800 videos per day (theoretical max)

**Recommended Conservative Rate**:
- 100-200 videos per hour
- 1,000-2,000 videos per day
- Spread across 23 sources = ~40-90 videos per source per day

### 3. youtube-transcript-api

**Status**: No rate limits (uses internal YouTube API)

| Aspect | Details |
|--------|---------|
| Rate limit | ✅ None documented |
| Blocking risk | Low (uses same endpoints as YouTube player) |
| Speed | Fast (~1-2 seconds per video) |
| Reliability | High |

---

## Safe Scraping Guidelines

### Recommended Configuration

```yaml
# config/scraping.yaml
rate_limits:
  rss_poll_interval: 3600  # seconds (1 hour)
  min_delay_between_videos: 2  # seconds
  max_delay_between_videos: 5  # seconds
  max_videos_per_hour: 200
  max_videos_per_day: 2000

politeness:
  respect_robots_txt: true
  user_agent: "AI-Research-Bot/1.0 (Research Project)"
  concurrent_downloads: 1  # Sequential only
```

### Daily Capacity Estimate

| Scenario | Videos/Day | Notes |
|----------|------------|-------|
| **Conservative** | 500-1000 | Very safe, minimal risk |
| **Moderate** | 1000-2000 | Safe with delays |
| **Aggressive** | 2000-5000 | Higher risk of blocks |

**Our 23 Sources - Realistic Expectations**:
- Tier 1 (8 sources): ~5-10 videos/day each = 40-80 videos
- Tier 2 (9 sources): ~3-5 videos/day each = 27-45 videos
- Tier 3 (6 sources): ~1-3 videos/day each = 6-18 videos
- **Total**: ~70-140 videos/day across all sources

This is well within safe limits.

---

## What Data We Extract

### From RSS Feed (per video)
```yaml
video:
  id: "E3A4JXcFB9Q"
  title: "Learn anything in 2026 with these tools"
  published_at: "20260201"
  url: "https://youtube.com/watch?v=E3A4JXcFB9Q"
```

### From yt-dlp (per video)
```yaml
metadata:
  description: "Full video description with links..."
  duration: 19  # seconds
  view_count: 872
  like_count: 31
  thumbnail: "https://i.ytimg.com/vi/..."
  channel: "David Ondrej"
  channel_id: "UCPGrgwfbkjTIgPoOh2q1BAg"
```

### From youtube-transcript-api (per video)
```yaml
transcript:
  full_text: "Learning without AI is crazy..."
  segments:
    - start: "00:00:00"
      text: "Learning without AI is crazy..."
    - start: "00:00:02"
      text: "slow. You can ask it personalized..."
  segment_count: 12
  language: "en"
  is_auto_generated: true
```

### Data Size Estimates

| Video Type | Transcript Size | YAML Size |
|------------|-----------------|-----------|
| Short (20s) | ~500 chars | ~2-3 KB |
| Medium (10m) | ~10K chars | ~15-20 KB |
| Long (1h) | ~100K chars | ~120-150 KB |

**Storage Estimate** (100 videos/day):
- Average 20 KB per video = 2 MB/day
- 60 MB/month
- 720 MB/year

---

## Playlist Scraping - Design

### Is It Possible?

**Yes**, with yt-dlp:

```bash
# Extract all videos from a playlist
yt-dlp --flat-playlist --print "%(id)s" "PLAYLIST_URL"
```

### Implementation Plan

1. **Add playlist source type** to `config/sources.yaml`:
```yaml
sources:
  - name: "My Learning Playlist"
    type: playlist  # new type
    url: "https://www.youtube.com/playlist?list=PLxxx"
    tier: 1
    areas: [ai-engineering]
```

2. **Update ingest.py** to handle playlists:
```python
def process_playlist(playlist):
    # Get all video IDs from playlist
    cmd = ["yt-dlp", "--flat-playlist", "--print", "%(id)s", playlist["url"]]
    result = subprocess.run(cmd, capture_output=True, text=True)
    video_ids = result.stdout.strip().split("\n")

    # Process each video
    for video_id in video_ids:
        process_video(video_id, playlist)
```

3. **Requirements for playlists**:
   - Must be public or unlisted
   - Playlist URL (e.g., `https://www.youtube.com/playlist?list=PL...`)
   - Same rate limits apply

### Playlist Data Flow

```
User provides playlist URL
    ↓
ingest.py extracts all video IDs
    ↓
For each video ID:
    - Check if already in data/sources/
    - If not: download metadata + transcript
    - Add to queue/pending/
    - Log to timeline/events/
```

### Duplicate Handling

Playlists may overlap with RSS sources:
- Check `data/sources/{creator}/videos/{id}.yaml` before downloading
- Skip if already exists
- Log as "already_processed" event

---

## Recommendations

### Immediate Actions

1. ✅ **Current rate is safe** (~70-140 videos/day expected)
2. ✅ **Keep 2-5s delays** between videos
3. ✅ **Poll RSS every 1 hour** (not more frequent)
4. ⏳ **Add playlist support** (next feature)

### Monitoring

Track these metrics:
- Videos collected per day
- Failed requests per day
- Average processing time
- Queue depth

### Alerts

Set up alerts for:
- >10 failed requests in a row (possible block)
- RSS returns 404 (endpoint deprecated)
- Queue depth >100 (processing backlog)

---

## Sources

- [Stack Overflow - Rate limits on RSS feeds](https://stackoverflow.com/questions/68849421/rate-limits-on-rss-feeds-youtube)
- [YouTube Data API Quota Documentation](https://developers.google.com/youtube/v3/getting-started#quota)
- [yt-dlp GitHub Repository](https://github.com/yt-dlp/yt-dlp)
- [n8n Community - YouTube RSS 404 Errors](https://community.n8n.io/t/youtube-rss-feed-endpoint-returns-404-errors/241692)
