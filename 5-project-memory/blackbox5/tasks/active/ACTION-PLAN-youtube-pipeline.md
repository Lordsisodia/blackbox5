# ACTION PLAN: YouTube Pipeline (Minimal Moves)

**Status:** ACTIVE
**Goal:** Get auto-scraping operational TODAY, then build analysis pipeline

---

## PHASE 1: Get Scraping Operational (Do This Now)

### Move 1: Create GitHub Repo (5 min)
```bash
# In your YouTube project folder
git init
git add .
git commit -m "Initial: 7,219 videos from 11 channels"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/youtube-ai-research.git
git push -u origin main
```

### Move 2: Create GitHub Actions Workflow (5 min)
Create `.github/workflows/scrape.yml`:
```yaml
name: Hourly Scrape
on:
  schedule:
    - cron: '0 * * * *'  # Every hour
  workflow_dispatch:

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python scripts/collect_all.py
      - run: |
          git config user.name "Bot"
          git config user.email "bot@example.com"
          git add database/
          git diff --staged --quiet || git commit -m "scrape: $(date)"
          git push
```

### Move 3: Create Master Scraper Script (10 min)
Create `scripts/collect_all.py`:
```python
#!/usr/bin/env python3
"""Scrape all channels from config/sources.yaml"""
import yaml
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "config" / "sources.yaml"

def load_channels():
    with open(CONFIG_PATH) as f:
        config = yaml.safe_load(f)
    return [s for s in config.get('sources', []) if s.get('active', True)]

def scrape_channel(source):
    slug = source['slug']
    url = source['url']
    name = source['name']

    print(f"Scraping: {name}")
    result = subprocess.run([
        sys.executable, "scripts/collect_channel_optimized.py",
        "--channel", url,
        "--name", name,
        "--slug", slug,
        "--batch-size", "25",
        "--workers", "5"
    ], capture_output=True, text=True)

    print(result.stdout)
    if result.stderr:
        print(result.stderr)

if __name__ == "__main__":
    channels = load_channels()
    print(f"Found {len(channels)} channels to scrape")

    for source in channels:
        scrape_channel(source)

    print("Done")
```

### Move 4: Test It (5 min)
```bash
python scripts/collect_all.py
# Should scrape all channels and update database/
```

**Result:** Scraping runs every hour automatically. Data commits to GitHub.

---

## PHASE 2: Add Channel Management (Do Today)

### Move 5: Create Add Channel Script (5 min)
Create `scripts/add_channel.py`:
```python
#!/usr/bin/env python3
"""Add new channel to config. Usage: python add_channel.py --handle @NewCreator --name "Name" --tier 2"""
import argparse
import yaml
import subprocess
from pathlib import Path

CONFIG_PATH = Path("config/sources.yaml")

def add_channel(handle, name, tier=2, areas=None, topics=None):
    # Load existing
    with open(CONFIG_PATH) as f:
        config = yaml.safe_load(f)

    # Create slug from handle
    slug = handle.replace('@', '').lower().replace('-', '_')

    # Check if exists
    existing = [s for s in config.get('sources', []) if s['slug'] == slug]
    if existing:
        print(f"Channel {slug} already exists")
        return

    # Add new source
    new_source = {
        'name': name,
        'slug': slug,
        'handle': handle,
        'url': f"https://www.youtube.com/{handle}",
        'tier': tier,
        'areas': areas or ['ai-engineering'],
        'topics': topics or [],
        'active': True
    }

    config['sources'].append(new_source)
    config['metadata']['total_sources'] = len(config['sources'])

    # Save
    with open(CONFIG_PATH, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    print(f"Added {name} ({slug})")

    # Git commit
    subprocess.run(['git', 'add', str(CONFIG_PATH)])
    subprocess.run(['git', 'commit', '-m', f'Add channel: {name}'])
    subprocess.run(['git', 'push'])
    print(f"Committed. Will be scraped in next hourly run.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--handle', required=True, help='@ChannelHandle')
    parser.add_argument('--name', required=True, help='Display name')
    parser.add_argument('--tier', type=int, default=2)
    args = parser.parse_args()

    add_channel(args.handle, args.name, args.tier)
```

### Move 6: Create Query Script (5 min)
Create `scripts/query.py`:
```python
#!/usr/bin/env python3
"""Query videos. Usage: python query.py --days 7 --channel david_ondrej"""
import argparse
import json
import glob
from datetime import datetime, timedelta
from pathlib import Path

def load_videos(channel=None, days=None):
    videos = []
    pattern = f"database/channels/{channel}.json" if channel else "database/channels/*.json"

    for file in glob.glob(pattern):
        with open(file) as f:
            data = json.load(f)
            for v in data.get('videos', []):
                v['channel'] = Path(file).stem
                videos.append(v)

    if days:
        cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
        videos = [v for v in videos if v.get('upload_date', '0') >= cutoff]

    return sorted(videos, key=lambda x: x.get('upload_date', ''), reverse=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--days', type=int, help='Last N days')
    parser.add_argument('--channel', help='Specific channel')
    parser.add_argument('--limit', type=int, default=20)
    args = parser.parse_args()

    videos = load_videos(args.channel, args.days)

    print(f"Found {len(videos)} videos")
    print("-" * 80)

    for v in videos[:args.limit]:
        date = v.get('upload_date', '??????')
        title = v.get('title', 'Unknown')[:60]
        channel = v.get('channel', 'unknown')
        views = v.get('view_count', 0)
        print(f"{date} | {channel:20} | {views:8} | {title}")
```

**Result:** You can add channels and query data easily.

---

## PHASE 3: Analysis Pipeline (Do This Week)

### Move 7: Create Ranking Script
Create `scripts/rank.py`:
```python
#!/usr/bin/env python3
"""Rank videos by relevance. Usage: python rank.py --days 7"""
import json
import glob
from datetime import datetime
from pathlib import Path

# Keywords that indicate high relevance
HIGH_VALUE_KEYWORDS = [
    'claude', 'mcp', 'model context protocol',
    'agent', 'autonomous', 'workflow',
    'tutorial', 'how to', 'guide',
    'announcement', 'release', 'new feature'
]

def score_video(video):
    score = 0
    title = video.get('title', '').lower()

    # Keyword scoring
    for kw in HIGH_VALUE_KEYWORDS:
        if kw in title:
            score += 10

    # View count (log scale)
    try:
        views = int(video.get('view_count', 0))
        score += min(views / 10000, 50)  # Cap at 50
    except:
        pass

    # Recency boost
    try:
        date = video.get('upload_date', '20000101')
        age_days = (datetime.now() - datetime.strptime(date, '%Y%m%d')).days
        if age_days < 7:
            score += 20
        elif age_days < 30:
            score += 10
    except:
        pass

    return score

def rank_videos(days=7):
    videos = []

    for file in glob.glob("database/channels/*.json"):
        with open(file) as f:
            data = json.load(f)
            channel = Path(file).stem
            for v in data.get('videos', []):
                v['channel'] = channel
                v['score'] = score_video(v)
                videos.append(v)

    # Sort by score
    videos.sort(key=lambda x: x['score'], reverse=True)
    return videos

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--days', type=int, default=7)
    parser.add_argument('--top', type=int, default=10)
    args = parser.parse_args()

    videos = rank_videos(args.days)

    print(f"TOP {args.top} VIDEOS (by relevance score)")
    print("=" * 80)

    for i, v in enumerate(videos[:args.top], 1):
        print(f"\n{i}. [{v['score']:.0f}] {v.get('title', 'Unknown')}")
        print(f"   Channel: {v['channel']}")
        print(f"   Date: {v.get('upload_date', 'Unknown')}")
        print(f"   Views: {v.get('view_count', 'Unknown')}")
        print(f"   URL: {v.get('url', 'Unknown')}")
```

### Move 8: Create Daily Digest Script
Create `scripts/digest.py`:
```python
#!/usr/bin/env python3
"""Generate daily digest of top content"""
import json
from datetime import datetime
from pathlib import Path

def generate_digest():
    today = datetime.now().strftime('%Y-%m-%d')

    # Import rank function
    from rank import rank_videos

    videos = rank_videos(days=1)[:5]  # Top 5 from last 24h

    output = f"""# Daily Digest: {today}

## Top 5 Videos (Last 24 Hours)

"""

    for i, v in enumerate(videos, 1):
        output += f"""### {i}. {v.get('title', 'Unknown')}
- **Channel:** {v['channel']}
- **Score:** {v['score']:.0f}/100
- **Views:** {v.get('view_count', 'Unknown')}
- **URL:** {v.get('url', 'Unknown')}

"""

    # Save to reports
    Path("reports/daily").mkdir(parents=True, exist_ok=True)
    with open(f"reports/daily/{today}.md", 'w') as f:
        f.write(output)

    print(output)

if __name__ == "__main__":
    generate_digest()
```

---

## PHASE 4: Integration (Do Next Week)

### Move 9: Claude Integration
Create `docs/AGENT_GUIDE.md`:
```markdown
# Agent Guide: YouTube Pipeline

## Quick Commands

### Add New Channel
```bash
python scripts/add_channel.py --handle @NewCreator --name "Creator Name" --tier 2
```

### Query Recent Videos
```bash
python scripts/query.py --days 7 --limit 20
```

### Get Top Ranked Videos
```bash
python scripts/rank.py --days 7 --top 10
```

### Generate Daily Report
```bash
python scripts/digest.py
```

## Data Locations
- Raw data: `database/channels/{slug}.json`
- Config: `config/sources.yaml`
- Reports: `reports/daily/{date}.md`

## Automation
- Scraping: Runs every hour via GitHub Actions
- Auto-commits to repo
- Check `.github/workflows/scrape.yml`
```

### Move 10: Create Master Pipeline Script
Create `scripts/pipeline.py`:
```python
#!/usr/bin/env python3
"""Full pipeline: scrape -> rank -> digest"""
import subprocess
import sys

def run(cmd):
    print(f"\n>>> {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"FAILED: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    # 1. Scrape all channels
    run("python scripts/collect_all.py")

    # 2. Generate rankings
    run("python scripts/rank.py --days 7 --top 20")

    # 3. Create digest
    run("python scripts/digest.py")

    print("\n✓ Pipeline complete")
```

---

## SUMMARY: What You Get

**Immediate (Today):**
- Auto-scraping every hour
- Data backed up to GitHub
- Can add channels via CLI

**This Week:**
- Ranking system
- Daily digests
- Query tools

**Next Week:**
- Full Claude integration
- Analysis pipeline
- Actionable insights

**Total Moves:** 10 scripts/files
**Time to Operational:** ~1 hour
**Cost:** $0
