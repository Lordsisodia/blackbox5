# Query Guide: Searching Collected YouTube Data

This guide shows how AI agents can search and query the collected YouTube video data.

## Data Location

Collected data is stored in:

```
/opt/blackbox5/youtube-scraper/database/channels/
├── fireship.json
├── ai_grid.json
├── latent_space.json
└── ... (one file per channel)
```

Each file contains a `videos` array with video metadata.

## Quick Queries (Python)

### Query All Videos

```python
import json
from pathlib import Path

DATABASE_DIR = Path("/opt/blackbox5/youtube-scraper/database/channels")

def get_all_videos():
    """Get all videos from all channels."""
    all_videos = []

    for channel_file in DATABASE_DIR.glob("*.json"):
        with open(channel_file, 'r') as f:
            data = json.load(f)
            all_videos.extend(data.get('videos', []))

    return all_videos

# Usage
videos = get_all_videos()
print(f"Total videos: {len(videos)}")
```

### Search by Keywords

```python
def search_by_title(keyword: str, videos: list):
    """Search videos by title keyword."""
    keyword_lower = keyword.lower()
    results = [
        v for v in videos
        if keyword_lower in v.get('title', '').lower()
    ]
    return results

# Usage
results = search_by_title("machine learning", videos)
for video in results:
    print(f"{video['title']}")
    print(f"  {video['url']}")
    print()
```

### Search by Channel

```python
def get_videos_by_channel(channel_name: str):
    """Get all videos from a specific channel."""
    safe_name = channel_name.lower().replace(' ', '_').replace('/', '_')
    channel_file = DATABASE_DIR / f"{safe_name}.json"

    if not channel_file.exists():
        print(f"Channel not found: {channel_name}")
        return []

    with open(channel_file, 'r') as f:
        data = json.load(f)
        return data.get('videos', [])

# Usage
fireship_videos = get_videos_by_channel("Fireship")
print(f"Fireship videos: {len(fireship_videos)}")
```

### Filter by Duration

```python
def get_long_form_videos(videos: list, min_minutes: int = 10):
    """Get videos longer than specified duration."""
    min_seconds = min_minutes * 60
    return [
        v for v in videos
        if int(v.get('duration', 0)) >= min_seconds
    ]

# Usage
long_videos = get_long_form_videos(videos, min_minutes=15)
print(f"Long-form videos (15+ min): {len(long_videos)}")
```

### Get Recent Videos

```python
from datetime import datetime, timedelta

def get_recent_videos(videos: list, days: int = 7):
    """Get videos uploaded in the last N days."""
    cutoff = datetime.now() - timedelta(days=days)

    recent = []
    for video in videos:
        upload_date = video.get('upload_date', '')
        if upload_date:
            # Format: YYYYMMDD
            try:
                video_date = datetime.strptime(upload_date, '%Y%m%d')
                if video_date >= cutoff:
                    recent.append(video)
            except ValueError:
                continue

    return recent

# Usage
recent = get_recent_videos(videos, days=7)
print(f"Videos in last 7 days: {len(recent)}")
```

### Sort by View Count

```python
def sort_by_views(videos: list, limit: int = 10):
    """Sort videos by view count (descending)."""
    sorted_videos = sorted(
        videos,
        key=lambda x: int(x.get('view_count', 0)),
        reverse=True
    )
    return sorted_videos[:limit]

# Usage
top_videos = sort_by_views(videos, limit=5)
for i, video in enumerate(top_videos, 1):
    views = int(video.get('view_count', 0))
    print(f"{i}. {video['title'][:60]}...")
    print(f"   Views: {views:,}")
    print(f"   URL: {video['url']}")
    print()
```

## Advanced Queries

### Cross-Channel Search

```python
def search_all_channels(keyword: str):
    """Search across all channels for keyword."""
    all_results = []

    for channel_file in DATABASE_DIR.glob("*.json"):
        with open(channel_file, 'r') as f:
            data = json.load(f)
            videos = data.get('videos', [])

        results = [v for v in videos
                  if keyword.lower() in v.get('title', '').lower()]

        if results:
            all_results.extend(results)

    return all_results

# Usage
python_videos = search_all_channels("python")
print(f"Python videos across all channels: {len(python_videos)}")
```

### Channel Statistics

```python
def get_channel_stats():
    """Get statistics for each channel."""
    stats = {}

    for channel_file in DATABASE_DIR.glob("*.json"):
        with open(channel_file, 'r') as f:
            data = json.load(f)
            videos = data.get('videos', [])

        channel_name = channel_file.stem.replace('_', ' ').title()
        total_views = sum(int(v.get('view_count', 0)) for v in videos)
        avg_duration = sum(int(v.get('duration', 0)) for v in videos) / len(videos) if videos else 0

        stats[channel_name] = {
            'video_count': len(videos),
            'total_views': total_views,
            'avg_duration': avg_duration
        }

    return stats

# Usage
stats = get_channel_stats()
for channel, data in sorted(stats.items(), key=lambda x: x[1]['video_count'], reverse=True):
    print(f"{channel}:")
    print(f"  Videos: {data['video_count']}")
    print(f"  Total Views: {data['total_views']:,}")
    print(f"  Avg Duration: {data['avg_duration']:.1f} sec")
    print()
```

### Find Similar Videos

```python
def find_similar_videos(keyword: str, videos: list, limit: int = 5):
    """Find videos with similar titles using keyword overlap."""
    keyword_words = set(keyword.lower().split())
    scored = []

    for video in videos:
        title_words = set(video.get('title', '').lower().split())
        overlap = len(keyword_words & title_words)
        if overlap > 0:
            scored.append((video, overlap))

    # Sort by overlap count
    scored.sort(key=lambda x: x[1], reverse=True)
    return [v[0] for v in scored[:limit]]

# Usage
similar = find_similar_videos("machine learning", videos)
for video in similar:
    print(video['title'])
```

## CLI Queries (Bash)

### Quick Search

```bash
# Search for keyword across all channel files
grep -l "machine learning" /opt/blackbox5/youtube-scraper/database/channels/*.json

# Count videos per channel
wc -l /opt/blackbox5/youtube-scraper/database/channels/*.json
```

### Find by View Count

```bash
# Find videos with >100K views
python3 -c "
import json
from pathlib import Path

for f in Path('/opt/blackbox5/youtube-scraper/database/channels').glob('*.json'):
    with open(f) as file:
        data = json.load(file)
        for v in data['videos']:
            if int(v.get('view_count', 0)) > 100000:
                print(f\"{v['title'][:60]}... ({v['view_count']} views)\")
"
```

### Recent Videos

```bash
# Find videos from last 30 days
python3 -c "
import json
from pathlib import Path
from datetime import datetime, timedelta

cutoff = datetime.now() - timedelta(days=30)

for f in Path('/opt/blackbox5/youtube-scraper/database/channels').glob('*.json'):
    with open(f) as file:
        data = json.load(file)
        for v in data['videos']:
            upload = v.get('upload_date', '')
            if upload:
                try:
                    if datetime.strptime(upload, '%Y%m%d') >= cutoff:
                        print(f\"{v['title'][:60]}... ({upload})\")
                except: pass
"
```

## Integration with BlackBox5

### Using from Task Context

```python
# In a BlackBox5 task context
import sys
sys.path.insert(0, '/opt/blackbox5/youtube-scraper')

from scripts.collect_github import get_all_videos

def research_topic(topic: str):
    """Research a topic using YouTube video metadata."""
    videos = get_all_videos()

    # Search for topic
    relevant = [
        v for v in videos
        if topic.lower() in v.get('title', '').lower()
    ]

    # Return top results
    return sorted(relevant, key=lambda x: int(x.get('view_count', 0)), reverse=True)[:5]

# Usage in task
results = research_topic("AI agents")
print("Found relevant videos:")
for video in results:
    print(f"- {video['title']}")
    print(f"  {video['url']}")
```

### Query via Skill Definition

Add to `/opt/blackbox5/.skills/youtube-query.json`:

```json
{
  "name": "youtube-query",
  "description": "Search collected YouTube video data",
  "commands": [
    {
      "name": "search",
      "description": "Search videos by keyword",
      "exec": "python3",
      "args": [
        "-c",
        "import sys, json; from pathlib import Path; videos = sum([json.load(open(f)).get('videos', []) for f in Path('/opt/blackbox5/youtube-scraper/database/channels').glob('*.json')], []); results = [v for v in videos if '{{keyword}}'.lower() in v.get('title', '').lower()]; print(json.dumps(results[:10], indent=2))"
      ]
    },
    {
      "name": "stats",
      "description": "Get channel statistics",
      "exec": "python3",
      "args": ["-c", "import json; from pathlib import Path; stats = {f.stem: len(json.load(open(f)).get('videos', [])) for f in Path('/opt/blackbox5/youtube-scraper/database/channels').glob('*.json')}; print(json.dumps(stats, indent=2))"]
    }
  ]
}
```

---

**For more information, see:** `AGENT_GUIDE.md` (how to add channels)
