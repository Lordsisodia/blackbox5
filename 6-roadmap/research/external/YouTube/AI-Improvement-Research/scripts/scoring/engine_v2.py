"""
SISO-Relevant Channel Scoring Engine v2

Scores channels based on:
1. Relevance to YOUR tech stack (Claude Code, MCP, AI agents)
2. Last 50 videos (recent content matters more)
3. Video duration (17-20+ min = better educational content)
4. Tech recency (2025/2026 tech vs old news)
5. Actionability (can you actually use this?)
"""

import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime

from .weights_v2 import (
    get_siso_stack_matches,
    get_recency_score,
    get_actionability_score,
    get_freshness_score,
    get_tier,
    SCORING_DIMENSIONS,
)


class SISOChannelScorer:
    """Scores channels based on relevance to SISO's tech stack."""

    def __init__(self):
        self.weights = SCORING_DIMENSIONS

    def score_channel(self, channel_data: Dict, max_videos: int = 50) -> Dict:
        """
        Score a channel based on SISO-relevant criteria.

        Args:
            channel_data: Channel metadata and videos
            max_videos: Only consider last N videos (default 50)

        Returns:
            Dictionary with scores and metadata
        """
        videos = channel_data.get('videos', [])

        # Sort by upload date (newest first) and take last N
        videos = sorted(
            videos,
            key=lambda x: x.get('upload_date', ''),
            reverse=True
        )[:max_videos]

        if not videos:
            return self._empty_score(channel_data)

        # Score each video
        video_scores = []
        siso_matches_all = []

        for video in videos:
            score = self._score_video(video)
            video_scores.append(score)
            siso_matches_all.extend(score.get('siso_matches', []))

        # Calculate aggregate scores
        siso_relevance = sum(v['siso_relevance'] for v in video_scores) / len(video_scores)
        freshness = sum(v['freshness'] for v in video_scores) / len(video_scores)
        tech_recency = sum(v['tech_recency'] for v in video_scores) / len(video_scores)
        actionability = sum(v['actionability'] for v in video_scores) / len(video_scores)
        duration_score = sum(v['duration_score'] for v in video_scores) / len(video_scores)

        # Consistency bonus (are they regularly posting relevant content?)
        consistency = self._calculate_consistency(video_scores)

        # Calculate overall score
        overall = (
            siso_relevance * self.weights['siso_relevance'] +
            freshness * self.weights['content_freshness'] +
            tech_recency * self.weights['tech_recency'] +
            actionability * self.weights['actionability'] +
            consistency * self.weights['consistency']
        )

        # Cap at 100
        overall = min(100, round(overall, 1))

        # Get unique SISO matches
        unique_matches = list(set(m['keyword'] for m in siso_matches_all))

        return {
            'channel_id': channel_data.get('channel_id'),
            'channel_name': channel_data.get('channel_name'),
            'overall_score': overall,
            'tier': get_tier(overall),
            'component_scores': {
                'siso_relevance': round(siso_relevance, 1),
                'freshness': round(freshness, 1),
                'tech_recency': round(tech_recency, 1),
                'actionability': round(actionability, 1),
                'duration_score': round(duration_score, 1),
                'consistency': round(consistency, 1),
            },
            'siso_matches': unique_matches[:10],  # Top 10 unique matches
            'videos_scored': len(videos),
            'top_videos': self._get_top_videos(video_scores, 5),
            'metadata': {
                'total_videos': len(channel_data.get('videos', [])),
                'subscriber_count': channel_data.get('subscriber_count'),
                'last_upload': videos[0].get('upload_date') if videos else None,
            },
            'calculated_at': datetime.now().isoformat(),
        }

    def _score_video(self, video: Dict) -> Dict:
        """Score an individual video."""
        title = video.get('title', '')
        description = video.get('description', '')
        upload_date = video.get('upload_date')
        duration = self._parse_duration(video.get('duration', 0))

        # Combine title and description for analysis
        text = f"{title} {description}"

        # 1. SISO Relevance (0-100)
        siso_matches, siso_weight = get_siso_stack_matches(text)
        siso_relevance = min(100, siso_weight * 20)  # Scale up

        # 2. Content Freshness (0-100)
        freshness = get_freshness_score(upload_date)

        # 3. Tech Recency (0-100)
        tech_recency, _ = get_recency_score(text)

        # 4. Actionability (0-100)
        actionability, _ = get_actionability_score(text)

        # 5. Duration Score (17-25 min is sweet spot for tutorials)
        duration_score = self._score_duration(duration)

        return {
            'video_id': video.get('id'),
            'title': title,
            'siso_relevance': siso_relevance,
            'freshness': freshness,
            'tech_recency': tech_recency,
            'actionability': actionability,
            'duration_score': duration_score,
            'duration_seconds': duration,
            'siso_matches': siso_matches,
            'upload_date': upload_date,
        }

    def _score_duration(self, duration_seconds: int) -> float:
        """
        Score video duration.

        Sweet spot for educational content: 17-25 minutes
        - Under 10 min: too short for deep content
        - 17-25 min: ideal tutorial length
        - 25-40 min: good for comprehensive topics
        - Over 40 min: may be too long
        """
        minutes = duration_seconds / 60

        if minutes < 10:
            return 30  # Too short
        elif 10 <= minutes < 17:
            return 60  # Getting good
        elif 17 <= minutes <= 25:
            return 100  # Sweet spot
        elif 25 < minutes <= 40:
            return 85  # Good but longer
        elif 40 < minutes <= 60:
            return 60  # Might be too long
        else:
            return 40  # Probably too long

    def _calculate_consistency(self, video_scores: List[Dict]) -> float:
        """Calculate consistency of relevant content."""
        if not video_scores:
            return 0

        # Count how many videos have good SISO relevance
        relevant_count = sum(1 for v in video_scores if v['siso_relevance'] >= 40)

        # Percentage of recent videos that are relevant
        consistency = (relevant_count / len(video_scores)) * 100

        return consistency

    def _get_top_videos(self, video_scores: List[Dict], n: int = 5) -> List[Dict]:
        """Get top N videos by SISO relevance."""
        sorted_videos = sorted(
            video_scores,
            key=lambda x: (
                x['siso_relevance'] * 0.4 +
                x['actionability'] * 0.3 +
                x['tech_recency'] * 0.2 +
                x['freshness'] * 0.1
            ),
            reverse=True
        )

        return [
            {
                'video_id': v['video_id'],
                'title': v['title'][:80] + '...' if len(v['title']) > 80 else v['title'],
                'siso_relevance': round(v['siso_relevance'], 1),
                'upload_date': v['upload_date'],
            }
            for v in sorted_videos[:n]
        ]

    def _parse_duration(self, duration) -> int:
        """Parse duration to seconds."""
        if isinstance(duration, int):
            return duration
        try:
            return int(duration)
        except:
            return 0

    def _empty_score(self, channel_data: Dict) -> Dict:
        """Return default score for channel with no videos."""
        return {
            'channel_id': channel_data.get('channel_id'),
            'channel_name': channel_data.get('channel_name'),
            'overall_score': 0,
            'tier': 'D',
            'component_scores': {
                'siso_relevance': 0,
                'freshness': 0,
                'tech_recency': 0,
                'actionability': 0,
                'duration_score': 0,
                'consistency': 0,
            },
            'siso_matches': [],
            'videos_scored': 0,
            'top_videos': [],
            'metadata': {
                'total_videos': 0,
                'subscriber_count': channel_data.get('subscriber_count'),
                'last_upload': None,
            },
            'calculated_at': datetime.now().isoformat(),
        }


def score_all_channels(channels_data: Dict[str, Dict], max_videos: int = 50) -> Dict[str, Dict]:
    """Score all channels."""
    scorer = SISOChannelScorer()
    results = {}

    for channel_id, channel_data in channels_data.items():
        try:
            results[channel_id] = scorer.score_channel(channel_data, max_videos)
        except Exception as e:
            print(f"Error scoring channel {channel_id}: {e}")
            results[channel_id] = {
                'channel_id': channel_id,
                'channel_name': channel_data.get('channel_name', 'Unknown'),
                'overall_score': 0,
                'tier': 'D',
                'error': str(e),
            }

    return results


if __name__ == '__main__':
    # Test with sample data
    sample_channel = {
        'channel_id': 'UC_test',
        'channel_name': 'AI Engineering',
        'subscriber_count': 50000,
        'videos': [
            {
                'id': 'vid1',
                'title': 'Building AI Agents with Claude Code - Full Tutorial',
                'description': 'Learn how to build AI agents using Claude Code and MCP. Step by step guide.',
                'upload_date': '20260130',
                'duration': 1200,  # 20 min
            },
            {
                'id': 'vid2',
                'title': 'MCP Server Development in 2025',
                'description': 'Complete walkthrough of Model Context Protocol servers.',
                'upload_date': '20260125',
                'duration': 1500,  # 25 min
            },
            {
                'id': 'vid3',
                'title': 'Random tech news',
                'description': 'Some general tech news not related to AI.',
                'upload_date': '20260120',
                'duration': 600,  # 10 min
            },
        ],
    }

    scorer = SISOChannelScorer()
    result = scorer.score_channel(sample_channel, max_videos=50)
    print(json.dumps(result, indent=2))
