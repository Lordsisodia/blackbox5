#!/usr/bin/env python3
"""
AI-Centric Video Ranking System

Ranks individual videos based on:
1. Code/Framework value (can AI learn from this?)
2. Recency (your time-based multipliers)
3. Duration (17+ min = 1.5x bonus, <2 min = excluded)
4. Channel credibility (your trusted creators)
"""

import json
from pathlib import Path
from datetime import datetime
import sys

sys.path.insert(0, str(Path(__file__).parent))

from scoring.recency_weights import get_recency_multiplier, get_recency_label


# Your trusted creators (manual override)
CHANNEL_TIERS = {
    # S-Tier: Highest credibility (1.2x)
    'david_ondrej': {'tier': 'S', 'multiplier': 1.2, 'notes': 'Deep technical, always watch'},
    'vrsen': {'tier': 'S', 'multiplier': 1.2, 'notes': 'Credible, knows his stuff'},

    # A-Tier: Very good (1.1x)
    'bijan_bowen': {'tier': 'A', 'multiplier': 1.1, 'notes': 'Good technical content'},
    'andre_mikalsen': {'tier': 'A', 'multiplier': 1.1, 'notes': 'Quite good, vibe coding'},
    'ai_code_king': {'tier': 'A', 'multiplier': 1.1, 'notes': 'News + tutorials mixed'},

    # B-Tier: Good (1.05x)
    'ai_jason': {'tier': 'B', 'multiplier': 1.05, 'notes': 'Solid content'},
    'indydevdan': {'tier': 'B', 'multiplier': 1.05, 'notes': 'MCP, Claude Code focus'},
    'greg_isenberg': {'tier': 'B', 'multiplier': 1.05, 'notes': 'Business + AI'},

    # Default: Everyone else (1.0x)
    'default': {'tier': 'C', 'multiplier': 1.0, 'notes': 'Standard'},
}


def get_channel_multiplier(channel_slug: str) -> float:
    """Get credibility multiplier for channel."""
    channel_slug = channel_slug.lower()
    if channel_slug in CHANNEL_TIERS:
        return CHANNEL_TIERS[channel_slug]['multiplier']
    return CHANNEL_TIERS['default']['multiplier']


def score_video(video: dict, channel_slug: str) -> dict:
    """
    Score a single video for AI training value.

    Base score starts at 50, then modified by:
    - Recency (0.3x to 2.5x)
    - Duration bonus (1.0x to 1.5x)
    - Channel credibility (1.0x to 1.5x)
    """
    title = video.get('title', '')
    upload_date = video.get('upload_date')
    duration = video.get('duration', 0)

    # Parse duration
    try:
        duration_sec = int(duration)
    except:
        duration_sec = 0

    # Base score (50 = neutral)
    base_score = 50

    # Recency multiplier (0.3x to 2.5x)
    recency_mult = get_recency_multiplier(upload_date)
    recency_label = get_recency_label(upload_date)

    # Duration multiplier (18+ min = 1.2x)
    if duration_sec >= 1080:  # 18+ minutes
        duration_mult = 1.2
        duration_bonus = True
    else:
        duration_mult = 1.0
        duration_bonus = False

    # Channel credibility multiplier (S-tier = 1.2x)
    channel_mult = get_channel_multiplier(channel_slug)

    # Calculate final score
    final_score = base_score * recency_mult * duration_mult * channel_mult

    # Cap at 1000 for readability
    final_score = min(1000, round(final_score, 1))

    return {
        'video_id': video.get('id'),
        'title': title,
        'channel': channel_slug,
        'upload_date': upload_date,
        'duration_sec': duration_sec,
        'duration_min': round(duration_sec / 60, 1),
        'base_score': base_score,
        'recency_mult': recency_mult,
        'recency_label': recency_label,
        'duration_mult': duration_mult,
        'duration_bonus': duration_bonus,
        'channel_mult': channel_mult,
        'final_score': final_score,
        'url': f"https://youtube.com/watch?v={video.get('id')}"
    }


def rank_all_videos():
    """Rank all videos across all channels."""
    base_dir = Path(__file__).parent.parent
    channels_dir = base_dir / 'database' / 'channels'

    if not channels_dir.exists():
        print(f"Channels directory not found: {channels_dir}")
        return

    all_videos = []

    print("=" * 80)
    print("AI-Centric Video Ranking")
    print("Scoring all videos for AI training value")
    print("=" * 80)
    print()

    # Score all videos
    for json_file in sorted(channels_dir.glob('*.json')):
        channel_slug = json_file.stem

        try:
            with open(json_file, 'r') as f:
                channel_data = json.load(f)

            for video in channel_data.get('videos', []):
                # Skip if no ID
                if not video.get('id'):
                    continue

                scored = score_video(video, channel_slug)
                all_videos.append(scored)

        except Exception as e:
            print(f"Error processing {json_file}: {e}")

    # Sort by final score (descending)
    all_videos.sort(key=lambda x: x['final_score'], reverse=True)

    # Print top 50
    print(f"Top 50 Videos for AI Training (out of {len(all_videos)} total):")
    print("-" * 80)

    for i, v in enumerate(all_videos[:50], 1):
        # Format indicators
        boost_indicators = []
        if v['recency_mult'] >= 2.0:
            boost_indicators.append("🔥")
        elif v['recency_mult'] >= 1.5:
            boost_indicators.append("⚡")

        if v['duration_bonus']:
            boost_indicators.append("📹")

        if v['channel_mult'] >= 1.5:
            boost_indicators.append("⭐")
        elif v['channel_mult'] >= 1.3:
            boost_indicators.append("👍")

        indicator_str = " ".join(boost_indicators) if boost_indicators else ""

        print(f"{i:2}. [{v['final_score']:>6.1f}] {indicator_str}")
        print(f"    Channel: {v['channel']:<20} | Recency: {v['recency_label']:<12} | Duration: {v['duration_min']:.0f}min")
        print(f"    Title: {v['title'][:70]}{'...' if len(v['title']) > 70 else ''}")
        print(f"    URL: {v['url']}")
        print()

    # Save full rankings
    output_dir = base_dir / 'reports' / 'leaderboards'
    output_dir.mkdir(parents=True, exist_ok=True)

    rankings_file = output_dir / 'video_rankings.json'
    with open(rankings_file, 'w') as f:
        json.dump({
            'generated_at': datetime.now().isoformat(),
            'total_videos': len(all_videos),
            'top_100': all_videos[:100]
        }, f, indent=2)

    print("=" * 80)
    print(f"Rankings saved to: {rankings_file}")
    print("=" * 80)


if __name__ == '__main__':
    rank_all_videos()
