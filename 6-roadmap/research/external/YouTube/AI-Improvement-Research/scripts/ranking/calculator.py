"""
Ranking Calculator

Calculates rankings and generates leaderboards from channel scores.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from .categories import categorize_channel, get_category_name, generate_category_rankings


def calculate_rankings(
    channel_scores: Dict[str, Dict],
    previous_rankings: Optional[Dict] = None
) -> Dict[str, Dict]:
    """
    Calculate overall and category rankings.

    Args:
        channel_scores: Dictionary mapping channel_id to score data
        previous_rankings: Optional previous rankings for trend calculation

    Returns:
        Dictionary with rankings and metadata
    """
    # Sort channels by overall score
    sorted_channels = sorted(
        channel_scores.items(),
        key=lambda x: x[1]['overall_score'],
        reverse=True
    )

    # Assign overall ranks
    for rank, (channel_id, score_data) in enumerate(sorted_channels, 1):
        score_data['overall_rank'] = rank

        # Calculate trend if previous rankings exist
        if previous_rankings and channel_id in previous_rankings:
            prev_rank = previous_rankings[channel_id].get('overall_rank')
            if prev_rank:
                rank_change = prev_rank - rank
                score_data['rank_change'] = rank_change
                if rank_change > 5:
                    score_data['trend'] = 'rising'
                elif rank_change < -5:
                    score_data['trend'] = 'falling'
                else:
                    score_data['trend'] = 'stable'
            else:
                score_data['trend'] = 'new'
        else:
            score_data['trend'] = 'new'

    # Generate category rankings
    category_rankings = generate_category_rankings(channel_scores)

    # Assign category ranks
    for cat_key, channels in category_rankings.items():
        for rank, channel in enumerate(channels, 1):
            channel['category_rank'] = rank
            channel['category'] = cat_key

    return {
        'overall': [data for _, data in sorted_channels],
        'by_category': category_rankings,
        'generated_at': datetime.now().isoformat(),
        'total_channels': len(channel_scores),
    }


def get_tier_distribution(rankings: Dict) -> Dict[str, int]:
    """Get distribution of channels across tiers."""
    distribution = {'S': 0, 'A': 0, 'B': 0, 'C': 0, 'D': 0}

    for channel in rankings['overall']:
        tier = channel.get('tier', 'C')
        distribution[tier] = distribution.get(tier, 0) + 1

    return distribution


def get_trending_channels(rankings: Dict, trend_type: str = 'rising') -> List[Dict]:
    """
    Get trending channels (rising or falling).

    Args:
        rankings: Rankings dictionary
        trend_type: 'rising', 'falling', or 'new'

    Returns:
        List of channel data
    """
    channels = rankings['overall']

    if trend_type == 'rising':
        trending = [c for c in channels if c.get('trend') == 'rising']
        trending.sort(key=lambda x: x.get('rank_change', 0), reverse=True)
    elif trend_type == 'falling':
        trending = [c for c in channels if c.get('trend') == 'falling']
        trending.sort(key=lambda x: x.get('rank_change', 0))
    elif trend_type == 'new':
        trending = [c for c in channels if c.get('trend') == 'new']
        trending.sort(key=lambda x: x['overall_score'], reverse=True)
    else:
        trending = []

    return trending[:20]  # Top 20


def generate_leaderboard(
    rankings: Dict,
    output_dir: Path,
    top_n: int = 100
) -> None:
    """
    Generate leaderboard report files.

    Args:
        rankings: Rankings dictionary from calculate_rankings
        output_dir: Directory to save reports
        top_n: Number of channels to include in top list
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate overall leaderboard
    generate_overall_leaderboard(rankings, output_dir / 'overall.md', top_n)

    # Generate category leaderboards
    for cat_key, channels in rankings['by_category'].items():
        if channels:  # Only generate if category has channels
            filename = f"category_{cat_key}.md"
            generate_category_leaderboard(
                cat_key, channels, output_dir / filename, top_n=50
            )

    # Generate trending report
    generate_trending_report(rankings, output_dir / 'trending.md')

    # Generate tier distribution
    generate_tier_report(rankings, output_dir / 'tiers.md')

    # Save JSON data
    save_rankings_json(rankings, output_dir / 'rankings.json')


def generate_overall_leaderboard(
    rankings: Dict,
    output_path: Path,
    top_n: int = 100
) -> None:
    """Generate overall top channels leaderboard."""

    lines = [
        "# YouTube Channel Leaderboard - Overall Rankings",
        "",
        f"> **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}",
        f"> **Total Channels:** {rankings['total_channels']}",
        "> **Scoring:** Composite score (Knowledge 25%, Engagement 20%, Consistency 20%, Quality 15%, Impact 15%, Novelty 5%)",
        "",
        "## Tier Legend",
        "",
        "| Tier | Score Range | Description |",
        "|------|-------------|-------------|",
        "| S | 90-100 | Exceptional, must-watch content |",
        "| A | 80-89 | Excellent, consistently valuable |",
        "| B | 70-79 | Good, worth subscribing |",
        "| C | 60-69 | Average, some good content |",
        "| D | <60 | Below average, limited value |",
        "",
        f"## Top {top_n} Channels",
        "",
        "| Rank | Tier | Channel | Score | Trend | Knowledge | Engagement | Consistency | Quality | Impact | Novelty |",
        "|------|------|---------|-------|-------|-----------|------------|-------------|---------|--------|---------|",
    ]

    for channel in rankings['overall'][:top_n]:
        rank = channel['overall_rank']
        tier = channel['tier']
        name = channel['channel_name']
        score = channel['overall_score']

        trend = channel.get('trend', 'stable')
        trend_icon = {'rising': '↑', 'falling': '↓', 'stable': '→', 'new': '✨'}.get(trend, '→')

        components = channel['component_scores']

        lines.append(
            f"| {rank} | {tier} | {name} | {score:.1f} | {trend_icon} | "
            f"{components['knowledge']:.0f} | {components['engagement']:.0f} | "
            f"{components['consistency']:.0f} | {components['quality']:.0f} | "
            f"{components['impact']:.0f} | {components['novelty']:.0f} |"
        )

    lines.extend([
        "",
        "---",
        "",
        "*Trend indicators: ↑ Rising | ↓ Falling | → Stable | ✨ New*",
    ])

    output_path.write_text('\n'.join(lines))
    print(f"Generated: {output_path}")


def generate_category_leaderboard(
    category_key: str,
    channels: List[Dict],
    output_path: Path,
    top_n: int = 50
) -> None:
    """Generate category-specific leaderboard."""

    cat_name = get_category_name(category_key)

    lines = [
        f"# {cat_name} - Category Rankings",
        "",
        f"> **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}",
        f"> **Channels in Category:** {len(channels)}",
        "",
        f"## Top {min(top_n, len(channels))} Channels",
        "",
        "| Rank | Tier | Channel | Overall Score | Category Rank |",
        "|------|------|---------|---------------|---------------|",
    ]

    for channel in channels[:top_n]:
        rank = channel['category_rank']
        tier = channel['tier']
        name = channel['channel_name']
        score = channel['overall_score']
        overall_rank = channel['overall_rank']

        lines.append(
            f"| {rank} | {tier} | {name} | {score:.1f} | #{overall_rank} overall |"
        )

    output_path.write_text('\n'.join(lines))
    print(f"Generated: {output_path}")


def generate_trending_report(rankings: Dict, output_path: Path) -> None:
    """Generate trending channels report."""

    rising = get_trending_channels(rankings, 'rising')
    falling = get_trending_channels(rankings, 'falling')
    new_channels = get_trending_channels(rankings, 'new')

    lines = [
        "# Trending Channels Report",
        "",
        f"> **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## 🚀 Rising Stars",
        "",
        "Channels with significant rank improvements:",
        "",
    ]

    if rising:
        lines.append("| Rank | Channel | Score | Rank Change |")
        lines.append("|------|---------|-------|-------------|")
        for ch in rising[:15]:
            change = ch.get('rank_change', 0)
            lines.append(
                f"| {ch['overall_rank']} | {ch['channel_name']} | "
                f"{ch['overall_score']:.1f} | +{change} |"
            )
    else:
        lines.append("*No significant risers in this period.*")

    lines.extend([
        "",
        "## 📉 Falling",
        "",
        "Channels with rank declines:",
        "",
    ])

    if falling:
        lines.append("| Rank | Channel | Score | Rank Change |")
        lines.append("|------|---------|-------|-------------|")
        for ch in falling[:10]:
            change = ch.get('rank_change', 0)
            lines.append(
                f"| {ch['overall_rank']} | {ch['channel_name']} | "
                f"{ch['overall_score']:.1f} | {change} |"
            )
    else:
        lines.append("*No significant declines in this period.*")

    lines.extend([
        "",
        "## ✨ New Entrants",
        "",
        "Recently added channels:",
        "",
    ])

    if new_channels:
        lines.append("| Rank | Channel | Score | Tier |")
        lines.append("|------|---------|-------|------|")
        for ch in new_channels[:15]:
            lines.append(
                f"| {ch['overall_rank']} | {ch['channel_name']} | "
                f"{ch['overall_score']:.1f} | {ch['tier']} |"
            )
    else:
        lines.append("*No new channels in this period.*")

    output_path.write_text('\n'.join(lines))
    print(f"Generated: {output_path}")


def generate_tier_report(rankings: Dict, output_path: Path) -> None:
    """Generate tier distribution report."""

    distribution = get_tier_distribution(rankings)
    total = sum(distribution.values())

    lines = [
        "# Tier Distribution Report",
        "",
        f"> **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}",
        f"> **Total Channels:** {total}",
        "",
        "## Distribution by Tier",
        "",
        "| Tier | Count | Percentage | Description |",
        "|------|-------|------------|-------------|",
    ]

    for tier in ['S', 'A', 'B', 'C', 'D']:
        count = distribution.get(tier, 0)
        pct = (count / total * 100) if total > 0 else 0
        desc = {
            'S': 'Exceptional',
            'A': 'Excellent',
            'B': 'Good',
            'C': 'Average',
            'D': 'Below Average'
        }.get(tier, '')

        lines.append(f"| {tier} | {count} | {pct:.1f}% | {desc} |")

    lines.extend([
        "",
        "## S-Tier Channels (Exceptional)",
        "",
    ])

    s_tier = [c for c in rankings['overall'] if c['tier'] == 'S']
    if s_tier:
        for ch in s_tier:
            lines.append(f"- **{ch['channel_name']}** - {ch['overall_score']:.1f}")
    else:
        lines.append("*No S-tier channels currently.*")

    lines.extend([
        "",
        "## A-Tier Channels (Excellent)",
        "",
    ])

    a_tier = [c for c in rankings['overall'] if c['tier'] == 'A'][:20]
    if a_tier:
        for ch in a_tier:
            lines.append(f"- **{ch['channel_name']}** - {ch['overall_score']:.1f}")
    else:
        lines.append("*No A-tier channels currently.*")

    output_path.write_text('\n'.join(lines))
    print(f"Generated: {output_path}")


def save_rankings_json(rankings: Dict, output_path: Path) -> None:
    """Save rankings as JSON for programmatic access."""

    # Convert to serializable format
    data = {
        'generated_at': rankings['generated_at'],
        'total_channels': rankings['total_channels'],
        'overall': rankings['overall'],
        'by_category': {
            cat: [ch for ch in channels]
            for cat, channels in rankings['by_category'].items()
        },
    }

    output_path.write_text(json.dumps(data, indent=2))
    print(f"Generated: {output_path}")


if __name__ == '__main__':
    # Test with sample data
    sample_scores = {
        'UC1': {
            'channel_name': 'Fireship',
            'overall_score': 89.5,
            'tier': 'A',
            'component_scores': {
                'knowledge': 85, 'engagement': 95, 'consistency': 92,
                'quality': 88, 'impact': 87, 'novelty': 91
            },
            'categories': ['web_development', 'programming'],
        },
        'UC2': {
            'channel_name': 'Krish Naik',
            'overall_score': 87.2,
            'tier': 'A',
            'component_scores': {
                'knowledge': 92, 'engagement': 85, 'consistency': 88,
                'quality': 82, 'impact': 90, 'novelty': 75
            },
            'categories': ['data_science', 'machine_learning'],
        },
        'UC3': {
            'channel_name': 'Yannic Kilcher',
            'overall_score': 91.3,
            'tier': 'S',
            'component_scores': {
                'knowledge': 95, 'engagement': 88, 'consistency': 85,
                'quality': 90, 'impact': 93, 'novelty': 92
            },
            'categories': ['ai_research', 'machine_learning'],
        },
    }

    rankings = calculate_rankings(sample_scores)
    print(f"Total channels: {rankings['total_channels']}")
    print(f"Top channel: {rankings['overall'][0]['channel_name']}")

    # Generate reports
    output_dir = Path('test_reports')
    generate_leaderboard(rankings, output_dir, top_n=10)
