#!/usr/bin/env python3
"""Generate daily digest of top content. Usage: python digest.py"""
import json
import glob
from datetime import datetime, timedelta
from pathlib import Path

# Import rank function
import sys
sys.path.insert(0, str(Path(__file__).parent))
from rank_simple import rank_videos

def generate_digest():
    today = datetime.now().strftime('%Y-%m-%d')

    # Get top videos from last 24 hours
    videos = rank_videos(days=1)[:5]

    # Get top videos from last 7 days
    weekly_videos = rank_videos(days=7)[:10]

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

    output += f"""## Top 10 Videos (Last 7 Days)

"""

    for i, v in enumerate(weekly_videos, 1):
        output += f"{i}. [{v['score']:.0f}] {v.get('title', 'Unknown')} - {v['channel']}\n"

    output += f"""
## Stats

- **Total channels:** {len(glob.glob('database/channels/*.json'))}
- **Total videos:** {sum(len(json.load(open(f)).get('videos', [])) for f in glob.glob('database/channels/*.json'))}
- **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""

    # Save to reports
    Path("reports/daily").mkdir(parents=True, exist_ok=True)
    with open(f"reports/daily/{today}.md", 'w') as f:
        f.write(output)

    print(output)
    print(f"\nSaved to: reports/daily/{today}.md")

if __name__ == "__main__":
    generate_digest()
