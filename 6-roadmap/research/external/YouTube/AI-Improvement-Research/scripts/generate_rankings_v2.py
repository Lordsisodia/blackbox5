#!/usr/bin/env python3
"""
Generate SISO-Relevant YouTube Channel Rankings v2

Ranks channels based on relevance to YOUR tech stack using last 50 videos.
"""

import json
import yaml
from pathlib import Path
from datetime import datetime
import sys

sys.path.insert(0, str(Path(__file__).parent))

from scoring.engine_v2 import SISOChannelScorer
from ranking.calculator import calculate_rankings
from ranking.categories import categorize_channel


def load_all_channels(db_dir: Path) -> dict:
    """Load all channel data from JSON files."""
    channels = {}
    if not db_dir.exists():
        return channels

    for json_file in db_dir.glob('*.json'):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                channel_slug = json_file.stem
                channels[channel_slug] = data
        except Exception as e:
            print(f"  Warning: Could not load {json_file}: {e}")
    return channels


def load_channel_config(config_path: Path) -> dict:
    """Load channel configuration from YAML."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load_all(f)
        docs = list(config)

    channels = {}
    for doc in docs:
        if not isinstance(doc, dict):
            continue
        if 'sources' in doc:
            for source in doc['sources']:
                slug = source.get('slug')
                if slug:
                    channels[slug] = source
    return channels


def parse_duration(duration_str) -> int:
    """Parse duration string to seconds."""
    if isinstance(duration_str, int):
        return duration_str
    try:
        return int(duration_str)
    except:
        return 0


def aggregate_channel_data(channel_slug: str, channel_data: dict, channel_config: dict) -> dict:
    """Aggregate channel data for scoring."""
    videos = channel_data.get('videos', [])
    if not videos:
        return None

    processed_videos = []
    for video in videos:
        processed_video = {
            'id': video.get('id'),
            'title': video.get('title', ''),
            'description': video.get('description', ''),
            'upload_date': video.get('upload_date'),
            'duration': parse_duration(video.get('duration', '0')),
        }
        processed_videos.append(processed_video)

    processed_videos.sort(key=lambda x: x.get('upload_date', ''), reverse=True)

    return {
        'channel_id': channel_config.get('channel_id', channel_slug),
        'channel_name': channel_config.get('name', channel_slug.replace('_', ' ').title()),
        'subscriber_count': channel_data.get('subscriber_count', 0),
        'videos': processed_videos,
    }


def generate_siso_report(rankings: dict, output_path: Path):
    """Generate SISO-focused markdown report."""
    lines = [
        "# SISO-Relevant Channel Rankings",
        "",
        f"> **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}",
        f"> **Total Channels:** {rankings['total_channels']}",
        f"> **Videos Analyzed:** Last 50 per channel",
        "",
        "## Scoring Criteria (SISO-Optimized)",
        "",
        "| Dimension | Weight | Description |",
        "|-----------|--------|-------------|",
        "| SISO Relevance | 35% | Mentions Claude Code, MCP, AI agents, YOUR stack |",
        "| Content Freshness | 25% | How recent are the videos |",
        "| Tech Recency | 20% | Discusses 2025/2026 tech vs old news |",
        "| Actionability | 15% | Can you actually use this? (tutorials > news) |",
        "| Consistency | 5% | Regularly posts relevant content |",
        "",
        "## Tier Legend",
        "",
        "| Tier | Score | Meaning |",
        "|------|-------|---------|",
        "| S | 85-100 | Must watch - directly applicable to your work |",
        "| A | 70-84 | Excellent - highly relevant, check regularly |",
        "| B | 55-69 | Good - worth subscribing for occasional gems |",
        "| C | 40-54 | Average - some relevant content |",
        "| D | <40 | Low relevance to current stack |",
        "",
        "---",
        "",
    ]

    # Top channels by tier
    for tier in ['S', 'A', 'B', 'C', 'D']:
        tier_channels = [c for c in rankings['overall'] if c['tier'] == tier]
        if tier_channels:
            lines.append(f"## {tier}-Tier Channels")
            lines.append("")

            for ch in tier_channels:
                lines.append(f"### #{ch['overall_rank']} {ch['channel_name']} - {ch['overall_score']:.1f}")
                lines.append("")

                # Component scores
                comp = ch['component_scores']
                lines.append(f"**Scores:** SISO: {comp['siso_relevance']:.0f} | Fresh: {comp['freshness']:.0f} | Tech: {comp['tech_recency']:.0f} | Action: {comp['actionability']:.0f}")
                lines.append("")

                # SISO matches
                if ch.get('siso_matches'):
                    lines.append(f"**Keywords:** {', '.join(ch['siso_matches'][:5])}")
                    lines.append("")

                # Top videos
                if ch.get('top_videos'):
                    lines.append("**Top Videos:**")
                    for v in ch['top_videos'][:3]:
                        lines.append(f"- {v['title']} (SISO: {v['siso_relevance']:.0f})")
                    lines.append("")

                lines.append("---")
                lines.append("")

    output_path.write_text('\n'.join(lines))
    print(f"Generated: {output_path}")


def main():
    """Main execution."""
    print("=" * 70)
    print("SISO-Relevant Channel Ranking Generator v2")
    print("Analyzing last 50 videos per channel")
    print("=" * 70)

    base_dir = Path(__file__).parent.parent
    channels_dir = base_dir / 'database' / 'channels'
    config_path = base_dir / 'config' / 'sources.yaml'
    output_dir = base_dir / 'reports' / 'leaderboards'
    rankings_path = base_dir / 'database' / 'channel_rankings_v2.json'

    print(f"\nLoading channel data from: {channels_dir}")
    all_channels = load_all_channels(channels_dir)
    print(f"Loaded {len(all_channels)} channel files")

    print(f"\nLoading channel config from: {config_path}")
    channels_config = load_channel_config(config_path)
    print(f"Found {len(channels_config)} channels in config")

    scorer = SISOChannelScorer()

    print("\nScoring channels (last 50 videos each)...")
    print("-" * 70)
    channel_scores = {}

    for channel_slug, channel_data in all_channels.items():
        config = channels_config.get(channel_slug, {})
        channel_name = config.get('name', channel_slug.replace('_', ' ').title())

        aggregated = aggregate_channel_data(channel_slug, channel_data, config)
        if not aggregated or not aggregated['videos']:
            print(f"  ⚠️  No videos: {channel_name}")
            continue

        try:
            score_result = scorer.score_channel(aggregated, max_videos=50)
            video_titles = [v.get('title', '') for v in aggregated['videos'][:10]]
            categories = categorize_channel(channel_name, video_titles)
            score_result['categories'] = categories
            score_result['slug'] = channel_slug

            channel_scores[channel_slug] = score_result

            tier_icon = {"S": "🔥", "A": "⭐", "B": "👍", "C": "😐", "D": "❌"}.get(score_result['tier'], "❓")
            print(f"  {tier_icon} {channel_name:<30} | Score: {score_result['overall_score']:>5.1f} | Tier: {score_result['tier']} | Videos: {score_result['videos_scored']}")

        except Exception as e:
            print(f"  ✗ Error scoring {channel_name}: {e}")

    print("-" * 70)
    print(f"Successfully scored {len(channel_scores)} channels")

    if not channel_scores:
        print("\nNo channels to rank. Exiting.")
        return

    print("\nCalculating rankings...")
    rankings = calculate_rankings(channel_scores)

    print(f"\nSaving rankings to: {rankings_path}")
    rankings_path.parent.mkdir(parents=True, exist_ok=True)
    with open(rankings_path, 'w') as f:
        json.dump(rankings, f, indent=2)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate SISO-focused report
    generate_siso_report(rankings, output_dir / 'siso_rankings.md')

    # Print summary
    print("\n" + "=" * 70)
    print("SISO-RELEVANT RANKING SUMMARY")
    print("=" * 70)
    print(f"Total channels: {rankings['total_channels']}")

    from collections import Counter
    tiers = [ch['tier'] for ch in rankings['overall']]
    tier_counts = Counter(tiers)

    print(f"\nTier Distribution:")
    for tier in ['S', 'A', 'B', 'C', 'D']:
        count = tier_counts.get(tier, 0)
        pct = (count / len(rankings['overall']) * 100) if rankings['overall'] else 0
        bar = '█' * int(pct / 2)
        print(f"  {tier}-tier: {count:3} channels ({pct:5.1f}%) {bar}")

    print(f"\nTop 10 Most Relevant Channels:")
    print("-" * 70)
    for i, ch in enumerate(rankings['overall'][:10], 1):
        comp = ch['component_scores']
        matches = ', '.join(ch.get('siso_matches', [])[:3])
        print(f"{i:2}. [{ch['tier']}-tier] {ch['channel_name']:<28} {ch['overall_score']:>5.1f}")
        print(f"    SISO: {comp['siso_relevance']:.0f} | Fresh: {comp['freshness']:.0f} | Tech: {comp['tech_recency']:.0f}")
        if matches:
            print(f"    Keywords: {matches}")

    print("\n" + "=" * 70)
    print("SISO-relevant ranking complete!")
    print(f"Reports saved to: {output_dir}")
    print("=" * 70)


if __name__ == '__main__':
    main()
