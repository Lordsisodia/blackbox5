"""
YouTube Channel Scoring Engine

Calculates composite scores for channels based on multiple dimensions
of educational value and content quality.
"""

import json
import math
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime, timedelta

from .weights import get_weights, get_tier, DEFAULT_SCORES


class ChannelScorer:
    """Main scoring engine for YouTube channels."""

    def __init__(self, weights=None):
        """
        Initialize scorer with optional custom weights.

        Args:
            weights: Dictionary of dimension weights (must sum to 1.0)
        """
        self.weights = weights or get_weights()
        self.default_scores = DEFAULT_SCORES

    def calculate_overall_score(self, component_scores: Dict[str, float]) -> float:
        """
        Calculate weighted composite score from component scores.

        Args:
            component_scores: Dictionary with keys for each dimension

        Returns:
            float: Overall score (0-100)
        """
        total = 0.0
        for dimension, weight in self.weights.items():
            score = component_scores.get(dimension, self.default_scores[dimension])
            # Ensure score is in valid range
            score = max(0, min(100, score))
            total += score * weight

        return round(total, 2)

    def calculate_knowledge_score(self, channel_data: Dict) -> float:
        """
        Calculate knowledge density score.

        Factors:
        - Average video information density
        - Technical term usage
        - Tutorial/code content ratio
        - Educational structure

        Args:
            channel_data: Channel metadata and video statistics

        Returns:
            float: Knowledge score (0-100)
        """
        videos = channel_data.get('videos', [])
        if not videos:
            return self.default_scores['knowledge']

        scores = []
        for video in videos:
            score = self._score_video_knowledge(video)
            scores.append(score)

        # Use weighted average favoring recent content
        if len(scores) >= 5:
            # Weight recent videos more heavily
            recent = scores[:5]
            older = scores[5:]
            avg_score = (sum(recent) * 0.7 / len(recent)) + (sum(older) * 0.3 / len(older)) if older else sum(recent) / len(recent)
        else:
            avg_score = sum(scores) / len(scores)

        return round(avg_score, 2)

    def _score_video_knowledge(self, video: Dict) -> float:
        """Score individual video knowledge density."""
        score = 50  # Base score

        # Factor 1: Description length (proxy for detail)
        desc = video.get('description', '')
        if len(desc) > 1000:
            score += 15
        elif len(desc) > 500:
            score += 10
        elif len(desc) > 200:
            score += 5

        # Factor 2: Has chapters/sections (well-structured)
        if video.get('chapters'):
            score += 10

        # Factor 3: Has code/tutorial keywords
        code_keywords = ['tutorial', 'guide', 'how to', 'code', 'programming', 'example', 'demo']
        title_desc = (video.get('title', '') + ' ' + desc).lower()
        code_matches = sum(1 for kw in code_keywords if kw in title_desc)
        score += min(code_matches * 3, 15)

        # Factor 4: Duration (sweet spot for tutorials: 10-30 min)
        duration = video.get('duration', 0)
        if 600 <= duration <= 1800:  # 10-30 minutes
            score += 10
        elif 300 <= duration < 600:  # 5-10 minutes
            score += 5
        elif duration > 3600:  # Over 1 hour
            score -= 5

        return min(100, max(0, score))

    def calculate_engagement_score(self, channel_data: Dict) -> float:
        """
        Calculate engagement quality score.

        Factors:
        - Like-to-view ratio
        - Comment quality and volume
        - Subscriber conversion rate
        - View velocity

        Args:
            channel_data: Channel metadata and statistics

        Returns:
            float: Engagement score (0-100)
        """
        videos = channel_data.get('videos', [])
        if not videos:
            return self.default_scores['engagement']

        total_views = sum(v.get('view_count', 0) for v in videos)
        total_likes = sum(v.get('like_count', 0) for v in videos)

        if total_views == 0:
            return self.default_scores['engagement']

        # Like ratio (typical range: 1-10%)
        like_ratio = total_likes / total_views
        like_score = min(like_ratio * 1000, 40)  # Cap at 40 points

        # View velocity (views per day since upload)
        velocity_scores = []
        for video in videos:
            views = video.get('view_count', 0)
            uploaded = video.get('upload_date')
            if uploaded and views > 0:
                try:
                    upload_dt = datetime.strptime(uploaded, '%Y%m%d')
                    days_since = (datetime.now() - upload_dt).days
                    if days_since > 0:
                        velocity = views / days_since
                        # Normalize: 1000 views/day = good
                        velocity_scores.append(min(velocity / 100, 30))
                except:
                    pass

        velocity_score = sum(velocity_scores) / len(velocity_scores) if velocity_scores else 15

        # Subscriber conversion (views per subscriber)
        subscriber_count = channel_data.get('subscriber_count', 0)
        if subscriber_count > 0:
            conversion = total_views / subscriber_count
            conversion_score = min(conversion * 2, 30)
        else:
            conversion_score = 15

        total = like_score + velocity_score + conversion_score
        return round(min(100, total), 2)

    def calculate_consistency_score(self, channel_data: Dict) -> float:
        """
        Calculate consistency score.

        Factors:
        - Upload regularity
        - Quality consistency over time
        - Longevity and total output
        - Recent activity

        Args:
            channel_data: Channel metadata

        Returns:
            float: Consistency score (0-100)
        """
        videos = channel_data.get('videos', [])
        if len(videos) < 2:
            return self.default_scores['consistency']

        # Upload regularity
        upload_dates = []
        for video in videos:
            date_str = video.get('upload_date')
            if date_str:
                try:
                    upload_dates.append(datetime.strptime(date_str, '%Y%m%d'))
                except:
                    pass

        if len(upload_dates) < 2:
            return 50

        upload_dates.sort(reverse=True)
        intervals = [(upload_dates[i] - upload_dates[i+1]).days
                     for i in range(len(upload_dates)-1)]

        if not intervals:
            return 50

        # Calculate regularity (lower std dev = more regular)
        avg_interval = sum(intervals) / len(intervals)
        std_dev = math.sqrt(sum((x - avg_interval) ** 2 for x in intervals) / len(intervals))

        # Score: ideal is 7-14 days between uploads with low variance
        if 3 <= avg_interval <= 30:
            regularity_score = 30 - min(std_dev, 30)
        else:
            regularity_score = max(0, 20 - min(std_dev, 20))

        # Total output score (logarithmic scale)
        total_videos = len(videos)
        output_score = min(math.log10(total_videos + 1) * 15, 30)

        # Recent activity (uploaded in last 90 days)
        recent_count = sum(1 for d in upload_dates if (datetime.now() - d).days <= 90)
        activity_score = min(recent_count * 5, 20)

        # Quality consistency (based on view variance)
        view_counts = [v.get('view_count', 0) for v in videos if v.get('view_count', 0) > 0]
        if len(view_counts) > 1:
            avg_views = sum(view_counts) / len(view_counts)
            variance = sum((v - avg_views) ** 2 for v in view_counts) / len(view_counts)
            cv = math.sqrt(variance) / avg_views if avg_views > 0 else 1  # Coefficient of variation
            consistency_bonus = max(0, 20 - cv * 10)
        else:
            consistency_bonus = 10

        total = regularity_score + output_score + activity_score + consistency_bonus
        return round(min(100, total), 2)

    def calculate_quality_score(self, channel_data: Dict) -> float:
        """
        Calculate production quality score.

        Factors:
        - Video resolution
        - Has captions/subtitles
        - Has chapters
        - Audio quality indicators

        Args:
            channel_data: Channel metadata

        Returns:
            float: Quality score (0-100)
        """
        videos = channel_data.get('videos', [])
        if not videos:
            return self.default_scores['quality']

        scores = []
        for video in videos:
            score = 50  # Base

            # Resolution score
            height = video.get('height', 720)
            if height >= 2160:
                score += 20
            elif height >= 1440:
                score += 15
            elif height >= 1080:
                score += 10
            elif height >= 720:
                score += 5

            # Has chapters (well-structured content)
            if video.get('chapters'):
                score += 10

            # Has subtitles/captions (accessibility)
            if video.get('subtitles') or video.get('automatic_captions'):
                score += 10

            # Audio bitrate indicator
            abr = video.get('abr', 0)
            if abr >= 128:
                score += 10
            elif abr >= 96:
                score += 5

            scores.append(min(100, score))

        return round(sum(scores) / len(scores), 2)

    def calculate_impact_score(self, channel_data: Dict) -> float:
        """
        Calculate long-term impact score.

        Factors:
        - Evergreen content ratio
        - Total reach
        - Playlist inclusions
        - Reference rate

        Args:
            channel_data: Channel metadata

        Returns:
            float: Impact score (0-100)
        """
        videos = channel_data.get('videos', [])
        if not videos:
            return self.default_scores['impact']

        total_views = sum(v.get('view_count', 0) for v in videos)

        # Total reach (logarithmic scale)
        if total_views > 0:
            reach_score = min(math.log10(total_views) * 10, 40)
        else:
            reach_score = 0

        # Evergreen ratio (views on older videos)
        now = datetime.now()
        old_videos = [v for v in videos if v.get('upload_date') and
                      (now - datetime.strptime(v['upload_date'], '%Y%m%d')).days > 365]
        old_views = sum(v.get('view_count', 0) for v in old_videos)

        if total_views > 0:
            evergreen_ratio = old_views / total_views
            evergreen_score = evergreen_ratio * 30
        else:
            evergreen_score = 15

        # Channel longevity
        if videos:
            oldest_date = min(v['upload_date'] for v in videos if v.get('upload_date'))
            if oldest_date:
                try:
                    oldest = datetime.strptime(oldest_date, '%Y%m%d')
                    years_active = (now - oldest).days / 365
                    longevity_score = min(years_active * 5, 20)
                except:
                    longevity_score = 10
            else:
                longevity_score = 10
        else:
            longevity_score = 10

        # High-performing videos (viral threshold)
        viral_count = sum(1 for v in videos if v.get('view_count', 0) > 100000)
        viral_score = min(viral_count * 2, 10)

        total = reach_score + evergreen_score + longevity_score + viral_score
        return round(min(100, total), 2)

    def calculate_novelty_score(self, channel_data: Dict) -> float:
        """
        Calculate content novelty/uniqueness score.

        Factors:
        - Topic diversity
        - Unique positioning
        - Original content ratio

        Args:
            channel_data: Channel metadata

        Returns:
            float: Novelty score (0-100)
        """
        videos = channel_data.get('videos', [])
        if not videos:
            return self.default_scores['novelty']

        # Topic diversity (based on title keyword analysis)
        titles = [v.get('title', '').lower() for v in videos]
        words = []
        for title in titles:
            words.extend(title.split())

        # Count unique meaningful words
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                     'how', 'what', 'when', 'where', 'why', 'this', 'that', 'these', 'those'}

        meaningful = [w for w in words if w not in stopwords and len(w) > 3]
        unique_words = set(meaningful)

        if meaningful:
            diversity_ratio = len(unique_words) / len(meaningful)
            diversity_score = diversity_ratio * 50
        else:
            diversity_score = 25

        # Content type variety
        content_types = set()
        for video in videos:
            title = video.get('title', '').lower()
            if any(kw in title for kw in ['tutorial', 'how to', 'guide']):
                content_types.add('tutorial')
            if any(kw in title for kw in ['review', 'comparison']):
                content_types.add('review')
            if any(kw in title for kw in ['news', 'update', 'latest']):
                content_types.add('news')
            if any(kw in title for kw in ['explained', 'what is', 'understanding']):
                content_types.add('explainer')
            if any(kw in title for kw in ['live', 'stream', 'q&a']):
                content_types.add('live')

        variety_score = len(content_types) * 8

        total = diversity_score + variety_score
        return round(min(100, total), 2)

    def score_channel(self, channel_data: Dict) -> Dict:
        """
        Calculate complete score breakdown for a channel.

        Args:
            channel_data: Channel metadata and videos

        Returns:
            Dictionary with all scores and metadata
        """
        component_scores = {
            'knowledge': self.calculate_knowledge_score(channel_data),
            'engagement': self.calculate_engagement_score(channel_data),
            'consistency': self.calculate_consistency_score(channel_data),
            'quality': self.calculate_quality_score(channel_data),
            'impact': self.calculate_impact_score(channel_data),
            'novelty': self.calculate_novelty_score(channel_data),
        }

        overall = self.calculate_overall_score(component_scores)
        tier = get_tier(overall)

        return {
            'channel_id': channel_data.get('channel_id'),
            'channel_name': channel_data.get('channel_name'),
            'overall_score': overall,
            'tier': tier,
            'component_scores': component_scores,
            'metadata': {
                'total_videos': len(channel_data.get('videos', [])),
                'subscriber_count': channel_data.get('subscriber_count'),
                'total_views': sum(v.get('view_count', 0) for v in channel_data.get('videos', [])),
                'last_upload': channel_data.get('videos', [{}])[0].get('upload_date') if channel_data.get('videos') else None,
            },
            'calculated_at': datetime.now().isoformat(),
        }


def score_all_channels(channels_data: Dict[str, Dict]) -> Dict[str, Dict]:
    """
    Score all channels and return rankings.

    Args:
        channels_data: Dictionary mapping channel_id to channel data

    Returns:
        Dictionary mapping channel_id to score results
    """
    scorer = ChannelScorer()
    results = {}

    for channel_id, channel_data in channels_data.items():
        try:
            results[channel_id] = scorer.score_channel(channel_data)
        except Exception as e:
            print(f"Error scoring channel {channel_id}: {e}")
            # Add default scores for failed channels
            results[channel_id] = {
                'channel_id': channel_id,
                'channel_name': channel_data.get('channel_name', 'Unknown'),
                'overall_score': 50,
                'tier': 'C',
                'component_scores': DEFAULT_SCORES,
                'error': str(e),
            }

    return results


if __name__ == '__main__':
    # Test with sample data
    sample_channel = {
        'channel_id': 'UC_test',
        'channel_name': 'Test Channel',
        'subscriber_count': 10000,
        'videos': [
            {
                'id': 'vid1',
                'title': 'Python Tutorial: Complete Guide',
                'description': 'Learn Python programming with examples and code.',
                'view_count': 50000,
                'like_count': 2500,
                'upload_date': '20240115',
                'duration': 1200,
                'height': 1080,
                'chapters': [{'title': 'Introduction'}, {'title': 'Setup'}],
            },
            {
                'id': 'vid2',
                'title': 'Advanced Python Tips',
                'description': 'Expert techniques for Python developers.',
                'view_count': 30000,
                'like_count': 1500,
                'upload_date': '20240108',
                'duration': 900,
                'height': 1080,
            },
        ],
    }

    scorer = ChannelScorer()
    result = scorer.score_channel(sample_channel)
    print(json.dumps(result, indent=2))
