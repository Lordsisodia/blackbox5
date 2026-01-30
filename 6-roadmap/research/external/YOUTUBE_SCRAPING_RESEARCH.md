# YouTube Channel Scraping Research - Rate Limits & Solutions

## Executive Summary

For your VIP pipeline (10-20 channels, all videos auto-processed), the best approach is:
1. **RSS feeds** for monitoring new uploads (no rate limits)
2. **youtube-transcript-api** for transcript extraction (no API key needed)
3. **Smart throttling** to avoid IP blocks

---

## 1. The Rate Limit Problem

### YouTube's Defenses
| Method | Rate Limit | Consequence |
|--------|-----------|-------------|
| YouTube Data API | 10,000 units/day | Hard limit, requires payment for more |
| Scraping without care | ~100-200 requests/hour/IP | IP ban, CAPTCHA |
| Aggressive scraping | Immediate | Account termination |

### What Triggers Blocks
- Too many requests from same IP
- No delays between requests
- Missing/consistent User-Agent headers
- No cookie/session persistence
- Scraping during peak hours

---

## 2. Best Solutions (Ranked)

### Option A: RSS + youtube-transcript-api (RECOMMENDED)

**How it works:**
1. Poll RSS feeds every 15-30 minutes (completely free, no limits)
2. When new video detected, extract video ID
3. Use `youtube-transcript-api` to get captions (no API key, HTTP only)
4. Add random delays (2-5 seconds) between transcript fetches

**Pros:**
- 100% free
- No API keys needed for transcript extraction
- RSS has no rate limits
- Proven, stable approach

**Cons:**
- RSS only shows last 15 videos
- For backfill (all historical videos), need different approach

**Code pattern:**
```python
from youtube_transcript_api import YouTubeTranscriptApi
import feedparser
import time
import random

# RSS monitoring (no rate limit)
feed = feedparser.parse(f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}")

# Transcript extraction (no API key, but throttle)
for video in new_videos:
    transcript = YouTubeTranscriptApi().fetch(video['id'])
    time.sleep(random.uniform(2, 5))  # Be polite
```

---

### Option B: yt-dlp with Throttling

**How it works:**
- yt-dlp extracts from YouTube's internal API
- Built-in rate limiting options
- Can process entire channel with `--download-archive` to resume

**Best for:**
- Initial backfill of all historical videos
- Batch processing with resume capability

**Command:**
```bash
yt-dlp \
  --write-auto-subs \
  --sub-langs en \
  --skip-download \
  --sleep-interval 3 \
  --max-sleep-interval 8 \
  --download-archive processed.txt \
  -o "transcripts/%(id)s.%(ext)s" \
  "https://www.youtube.com/channel/CHANNEL_ID/videos"
```

**Rate limiting flags:**
| Flag | Purpose |
|------|---------|
| `--sleep-interval 3` | Wait 3 seconds between downloads |
| `--max-sleep-interval 8` | Randomize up to 8 seconds |
| `--limit-rate 1M` | Limit bandwidth |
| `--download-archive` | Skip already processed |

---

### Option C: Proxy Rotation (For Scale)

If you need to process 1000+ videos quickly:
- Residential proxy services (Bright Data, Oxylabs)
- Rotate IP every 10-20 requests
- Cost: ~$10-15/GB or ~$5/1000 requests

**Not needed for your use case** (20 channels, daily monitoring)

---

## 3. Recommended Architecture

### For Ongoing Monitoring (Daily)
```
RSS Feed Polling (every 15 min)
    ↓
Detect New Video
    ↓
Queue for Processing
    ↓
youtube-transcript-api (with 2-5s delays)
    ↓
Extract → Categorize → Save
```

### For Initial Backfill (One-time)
```
yt-dlp with throttling
    ↓
Process in batches of 50
    ↓
Wait 10-15 min between batches
    ↓
Store all transcripts locally
```

---

## 4. Open Source Tools to Use

### Primary: youtube-transcript-api
- **GitHub:** https://github.com/jdepoix/youtube-transcript-api
- **Why:** No API key, no browser, pure HTTP
- **Install:** `pip install youtube-transcript-api`

```python
from youtube_transcript_api import YouTubeTranscriptApi

# Get transcript
transcript = YouTubeTranscriptApi().fetch('video_id')

# With timestamps
for snippet in transcript:
    print(f"[{snippet.start}] {snippet.text}")
```

### Secondary: virtonen's channel downloader
- **GitHub:** https://github.com/virtonen/youtube-channel-transcript-downloader
- **Why:** Combines Data API for video list + transcript-api for captions
- **Note:** Needs YouTube Data API key for video discovery

### For Complex Scraping: Crawlee
- **Guide:** https://crawlee.dev/blog/scrape-youtube-python
- **Why:** Handles proxy rotation, retries, structured data
- **Use if:** You need metadata + transcripts at scale

---

## 5. Anti-Detection Best Practices

### Request Headers
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.youtube.com/',
}
```

### Timing Strategy
```python
import time
import random

# Random delays (jitter prevents pattern detection)
def polite_delay():
    time.sleep(random.uniform(2, 5))

# Exponential backoff on errors
def backoff(attempt):
    time.sleep(2 ** attempt + random.uniform(0, 1))
```

### Session Management
```python
import requests

# Reuse session (maintains cookies)
session = requests.Session()
session.headers.update(headers)

# Use for all requests
response = session.get(url)
```

---

## 6. What You Need to Provide

### Minimum Setup
1. **List of channel IDs** (not just names)
   - Go to channel → About → Share → Copy channel ID
   - Or use: https://www.youtube.com/@CHANNEL_NAME and view source, search for `"channelId"`

2. **Storage location** (already set up)

3. **Your IP/network** (for initial backfill, home IP is fine with throttling)

### Optional: YouTube Data API Key
Only if you want:
- Video view counts, likes, detailed metadata
- More than 15 recent videos from RSS
- Search functionality

**Get it:** https://console.cloud.google.com/apis/credentials
**Cost:** Free tier = 10,000 units/day (sufficient for 20 channels)

---

## 7. Implementation Plan

### Phase 1: RSS Monitoring (This Week)
- [ ] Set up RSS feed polling for 8 starter channels
- [ ] Build queue system for new videos
- [ ] Integrate youtube-transcript-api with throttling
- [ ] Test with 1-2 channels

### Phase 2: Backfill (Next Week)
- [ ] Use yt-dlp to download historical transcripts
- [ ] Process in batches with delays
- [ ] Build resume capability

### Phase 3: VIP Pipeline (Week 3)
- [ ] Auto-process new uploads within 1 hour
- [ ] Integration with extraction agent
- [ ] Notification system

---

## Sources

- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) - No API key transcript extraction
- [virtonen/youtube-channel-transcript-downloader](https://github.com/virtonen/youtube-channel-transcript-downloader) - Channel batch downloader
- [Crawlee YouTube Scraping Guide](https://crawlee.dev/blog/scrape-youtube-python) - Python scraping framework
- [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp) - YouTube downloader with rate limiting
- [YouTube RSS Feeds](https://www.youtube.com/feeds/videos.xml?channel_id=UCxxxx) - Rate-limit free monitoring
