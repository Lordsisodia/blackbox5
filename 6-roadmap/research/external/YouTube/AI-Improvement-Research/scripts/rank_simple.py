#!/usr/bin/env python3
"""Simple video ranking by relevance. Usage: python rank_simple.py --days 7 --top 10"""
import argparse
import json
import glob
import math
from datetime import datetime, timedelta
from pathlib import Path

# Keywords that indicate high relevance
HIGH_VALUE_KEYWORDS = [
    'claude', 'mcp', 'model context protocol',
    'agent', 'autonomous', 'workflow',
    'tutorial', 'how to', 'guide',
    'announcement', 'release', 'new feature',
    'vibe coding', 'ai coding',
    'openai', 'anthropic', 'gpt', 'llm'
]

def score_video(video):
    score = 0
    title = video.get('title', '').lower()

    # Keyword scoring
    for kw in HIGH_VALUE_KEYWORDS:
        if kw in title:
            score += 10

    # View count (log scale, capped)
    try:
        views = int(video.get('view_count', 0))
        if views > 0:
            score += min(math.log10(views) * 5, 50)
    except:
        pass

    # Recency boost
    try:
        date = video.get('upload_date', '20000101')
        age_days = (datetime.now() - datetime.strptime(date, '%Y%m%d')).days
        if age_days < 3:
            score += 30
        elif age_days < 7:
            score += 20
        elif age_days < 30:
            score += 10
    except:
        pass

    return score

def rank_videos(days=None):
    videos = []

    for file in glob.glob("database/channels/*.json"):
        channel = Path(file).stem
        with open(file) as f:
            data = json.load(f)
            for v in data.get('videos', []):
                v['channel'] = channel
                v['score'] = score_video(v)
                videos.append(v)

    # Filter by days if specified
    if days:
        cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
        videos = [v for v in videos if v.get('upload_date', '0') >= cutoff]

    # Sort by score
    videos.sort(key=lambda x: x['score'], reverse=True)
    return videos

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rank videos by relevance')
    parser.add_argument('--days', type=int, help='Only videos from last N days')
    parser.add_argument('--top', type=int, default=10, help='Number of results')
    args = parser.parse_args()

    videos = rank_videos(args.days)

    print(f"\n{'='*100}")
    print(f"TOP {args.top} VIDEOS (by relevance score)")
    if args.days:
        print(f"From last {args.days} days")
    print(f"{'='*100}\n")

    for i, v in enumerate(videos[:args.top], 1):
        print(f"{i}. [Score: {v['score']:.0f}] {v.get('title', 'Unknown')}")
        print(f"   Channel: {v['channel']}")
        print(f"   Date: {v.get('upload_date', 'Unknown')}")
        print(f"   Views: {v.get('view_count', 'Unknown')}")
        print(f"   URL: {v.get('url', 'Unknown')}")
        print()
