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
        channel_name = Path(file).stem
        with open(file) as f:
            data = json.load(f)
            for v in data.get("videos", []):
                v['channel'] = channel_name
                videos.append(v)

    if days:
        cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
        videos = [v for v in videos if v.get('upload_date', '0') >= cutoff]

    return sorted(videos, key=lambda x: x.get('upload_date', ''), reverse=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Query collected videos')
    parser.add_argument('--days', type=int, help='Last N days')
    parser.add_argument('--channel', help='Specific channel')
    parser.add_argument('--limit', type=int, default=20, help='Max results')
    args = parser.parse_args()

    videos = load_videos(args.channel, args.days)

    print(f"Found {len(videos)} videos")
    print("-" * 100)
    print(f"{'Date':<12} {'Channel':<20} {'Views':<10} {'Title'}")
    print("-" * 100)

    for v in videos[:args.limit]:
        date = v.get('upload_date', '????????')
        title = v.get('title', 'Unknown')[:55]
        channel = v.get('channel', 'unknown')[:18]
        views = v.get('view_count', 0)
        print(f"{date:<12} {channel:<20} {views:<10} {title}")
