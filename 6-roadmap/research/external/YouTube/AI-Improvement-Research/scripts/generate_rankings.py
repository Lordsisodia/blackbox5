#!/usr/bin/env python3
"""
Generate YouTube Channel Rankings

Main entry point for calculating channel scores and generating leaderboards.
Works with existing channel JSON files in database/channels/.
"""

import json
import yaml
from pathlib import Path
from datetime import datetime
import sys

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from scoring.engine import ChannelScorer
from ranking.calculator import calculate_rankings, generate_leaderboard
from ranking.categories import categorize_channel


def load_all_channels(db_dir: Path) -> dict:
    """
    Load all channel data from JSON files.

    Args:
        db_dir: Directory containing channel JSON files

    Returns:
        Dictionary mapping channel slug to channel data
    """
    channels = {}

    if not db_dir.exists():
        print(f"Warning: Database directory not found at {db_dir}")
        return channels

    for json_file in db_dir.glob('*.json'):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                channel_slug = json_file.stem
                channels[channel_slug] = data
        except Exception as e:
            print(f"  Warning: Could not load {json_file}: {e}")
            continue

    return channels


def load_channel_config(config_path: Path) -> dict:
    """
    Load channel configuration from YAML.

    Returns:
        Dictionary mapping channel slug to config
    """
    with open(config_path, 'r') as f:
        config = yaml.safe_load_all(f)
        # Skip metadata documents
        docs = list(config)

    # Extract channels from all documents
    channels = {}

    for doc in docs:
        if not isinstance(doc, dict):
            continue

        # Look for sources (channels)
        if 'sources' in doc:
            for source in doc['sources']:
                slug = source.get('slug')
                if slug:
                    channels[slug] = source

    return channels


def aggregate_channel_data(channel_slug: str, channel_data: dict, channel_config: dict) -> dict:
    """
    Aggregate channel data for scoring.

    Args:
        channel_slug: Channel slug from filename
        channel_data: Data from JSON file
        channel_config: Configuration from sources.yaml

    Returns:
        Dictionary with channel data ready for scoring
    """
    videos = channel_data.get('videos', [])

    if not videos:
        return None

    # Convert video data to expected format
    processed_videos = []
    for video in videos:
        processed_video = {
            'id': video.get('id'),
            'title': video.get('title', ''),
            'description': video.get('description', ''),
            'upload_date': video.get('upload_date'),
            'duration': parse_duration(video.get('duration', '0')),
            'view_count': parse_count(video.get('view_count', 0)),
            'like_count': parse_count(video.get('like_count', 0)),
            'height': video.get('height', 720),
            'chapters': video.get('chapters'),
            'subtitles': video.get('subtitles'),
            'abr': video.get('abr', 0),
        }
        processed_videos.append(processed_video)

    # Sort by upload date (newest first)
    processed_videos.sort(
        key=lambda x: x.get('upload_date', ''),
        reverse=True
    )

    return {
        'channel_id': channel_config.get('channel_id', channel_slug),
        'channel_name': channel_config.get('name', channel_slug.replace('_', ' ').title()),
        'subscriber_count': parse_count(channel_data.get('subscriber_count', 0)),
        'videos': processed_videos,
        'total_views': sum(v.get('view_count', 0) for v in processed_videos),
    }


def parse_duration(duration_str) -> int:
    """Parse duration string to seconds."""
    if isinstance(duration_str, int):
        return duration_str
    try:
        return int(duration_str)
    except:
        return 0


def parse_count(count_val) -> int:
    """Parse count value to integer."""
    if isinstance(count_val, int):
        return count_val
    try:
        return int(count_val)
    except:
        return 0


def main():
    """Main execution function."""
    print("=" * 70)
    print("YouTube Channel Ranking Generator")
    print("=" * 70)

    # Setup paths
    base_dir = Path(__file__).parent.parent
    channels_dir = base_dir / 'database' / 'channels'
    config_path = base_dir / 'config' / 'sources.yaml'
    output_dir = base_dir / 'reports' / 'leaderboards'
    rankings_path = base_dir / 'database' / 'channel_rankings.json'

    print(f"\nLoading channel data from: {channels_dir}")
    all_channels = load_all_channels(channels_dir)
    print(f"Loaded {len(all_channels)} channel files")

    print(f"\nLoading channel config from: {config_path}")
    channels_config = load_channel_config(config_path)
    print(f"Found {len(channels_config)} channels in config")

    # Initialize scorer
    scorer = ChannelScorer()

    # Score all channels
    print("\nCalculating channel scores...")
    print("-" * 70)
    channel_scores = {}

    for channel_slug, channel_data in all_channels.items():
        # Get config for this channel
        config = channels_config.get(channel_slug, {})
        channel_name = config.get('name', channel_slug.replace('_', ' ').title())

        # Aggregate data
        aggregated = aggregate_channel_data(channel_slug, channel_data, config)

        if not aggregated or not aggregated['videos']:
            print(f"  ⚠️  No videos found for: {channel_name}")
            continue

        # Calculate scores
        try:
            score_result = scorer.score_channel(aggregated)

            # Add categories
            video_titles = [v.get('title', '') for v in aggregated['videos'][:10]]
            categories = categorize_channel(channel_name, video_titles)
            score_result['categories'] = categories
            score_result['slug'] = channel_slug

            channel_scores[channel_slug] = score_result

            trend_icon = "→"
            print(f"  ✓ {channel_name:<30} | Score: {score_result['overall_score']:>5.1f} | Tier: {score_result['tier']} {trend_icon}")

        except Exception as e:
            print(f"  ✗ Error scoring {channel_name}: {e}")
            continue

    print("-" * 70)
    print(f"\nSuccessfully scored {len(channel_scores)} channels")

    if not channel_scores:
        print("\nNo channels to rank. Exiting.")
        return

    # Load previous rankings for trend calculation
    previous_rankings = {}
    if rankings_path.exists():
        try:
            with open(rankings_path, 'r') as f:
                prev_data = json.load(f)
                for ch in prev_data.get('overall', []):
                    prev_slug = ch.get('slug') or ch.get('channel_id')
                    if prev_slug:
                        previous_rankings[prev_slug] = ch
            print(f"Loaded previous rankings for trend calculation")
        except Exception as e:
            print(f"Warning: Could not load previous rankings: {e}")

    # Calculate rankings
    print("\nCalculating rankings...")
    rankings = calculate_rankings(channel_scores, previous_rankings)

    # Save rankings to database
    print(f"\nSaving rankings to: {rankings_path}")
    rankings_path.parent.mkdir(parents=True, exist_ok=True)
    with open(rankings_path, 'w') as f:
        json.dump(rankings, f, indent=2)

    # Generate leaderboard reports
    print(f"\nGenerating leaderboard reports in: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    generate_leaderboard(rankings, output_dir, top_n=100)

    # Print summary
    print("\n" + "=" * 70)
    print("RANKING SUMMARY")
    print("=" * 70)
    print(f"Total channels scored: {rankings['total_channels']}")
    print(f"\nTop 15 Channels:")
    print("-" * 70)

    for i, ch in enumerate(rankings['overall'][:15], 1):
        trend = ch.get('trend', 'stable')
        trend_icon = {'rising': '↑', 'falling': '↓', 'stable': '→', 'new': '✨'}.get(trend, '→')
        components = ch['component_scores']
        print(f"{i:2}. [{ch['tier']}-tier] {ch['channel_name']:<28} "
              f"Score: {ch['overall_score']:>5.1f} {trend_icon}  "
              f"(K:{components['knowledge']:>2.0f} E:{components['engagement']:>2.0f} "
              f"C:{components['consistency']:>2.0f})")

    print("\n" + "-" * 70)
    print("Tier Distribution:")
    from collections import Counter
    tiers = [ch['tier'] for ch in rankings['overall']]
    tier_counts = Counter(tiers)
    for tier in ['S', 'A', 'B', 'C', 'D']:
        count = tier_counts.get(tier, 0)
        pct = (count / len(rankings['overall']) * 100) if rankings['overall'] else 0
        bar = '█' * int(pct / 2)
        print(f"  {tier}-tier: {count:3} channels ({pct:5.1f}%) {bar}")

    print("\n" + "=" * 70)
    print("Leaderboard generation complete!")
    print(f"Reports saved to: {output_dir}")
    print("=" * 70)


if __name__ == '__main__':
    main()
