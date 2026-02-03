"""
Unit tests for the scoring engine.
"""

import unittest
from datetime import datetime

from ..engine import ChannelScorer
from ..weights import get_tier, validate_weights


class TestWeights(unittest.TestCase):
    """Test weight configuration."""

    def test_weights_sum_to_one(self):
        """Verify default weights sum to 1.0."""
        weights = get_weights()
        total = sum(weights.values())
        self.assertAlmostEqual(total, 1.0, places=2)

    def test_tier_assignment(self):
        """Test tier assignment logic."""
        self.assertEqual(get_tier(95), 'S')
        self.assertEqual(get_tier(85), 'A')
        self.assertEqual(get_tier(75), 'B')
        self.assertEqual(get_tier(65), 'C')
        self.assertEqual(get_tier(55), 'D')


class TestChannelScorer(unittest.TestCase):
    """Test ChannelScorer functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.scorer = ChannelScorer()
        self.sample_channel = {
            'channel_id': 'UC_test',
            'channel_name': 'Test Channel',
            'subscriber_count': 10000,
            'videos': [
                {
                    'id': 'vid1',
                    'title': 'Python Tutorial: Complete Guide',
                    'description': 'Learn Python programming with examples and code. ' * 20,
                    'view_count': 50000,
                    'like_count': 2500,
                    'upload_date': '20240115',
                    'duration': 1200,
                    'height': 1080,
                    'chapters': [{'title': 'Introduction'}, {'title': 'Setup'}],
                    'subtitles': True,
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

    def test_overall_score_calculation(self):
        """Test that overall score is calculated correctly."""
        result = self.scorer.score_channel(self.sample_channel)

        self.assertIn('overall_score', result)
        self.assertIn('tier', result)
        self.assertIn('component_scores', result)

        # Score should be between 0 and 100
        self.assertGreaterEqual(result['overall_score'], 0)
        self.assertLessEqual(result['overall_score'], 100)

    def test_component_scores_present(self):
        """Test that all component scores are present."""
        result = self.scorer.score_channel(self.sample_channel)
        components = result['component_scores']

        required_components = [
            'knowledge', 'engagement', 'consistency',
            'quality', 'impact', 'novelty'
        ]

        for component in required_components:
            self.assertIn(component, components)
            self.assertGreaterEqual(components[component], 0)
            self.assertLessEqual(components[component], 100)

    def test_empty_channel_handling(self):
        """Test handling of channel with no videos."""
        empty_channel = {
            'channel_id': 'UC_empty',
            'channel_name': 'Empty Channel',
            'videos': [],
        }

        result = self.scorer.score_channel(empty_channel)
        self.assertEqual(result['overall_score'], 50)  # Default score
        self.assertEqual(result['tier'], 'C')

    def test_knowledge_score(self):
        """Test knowledge score calculation."""
        score = self.scorer.calculate_knowledge_score(self.sample_channel)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_engagement_score(self):
        """Test engagement score calculation."""
        score = self.scorer.calculate_engagement_score(self.sample_channel)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_consistency_score(self):
        """Test consistency score calculation."""
        score = self.scorer.calculate_consistency_score(self.sample_channel)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_quality_score(self):
        """Test quality score calculation."""
        score = self.scorer.calculate_quality_score(self.sample_channel)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_impact_score(self):
        """Test impact score calculation."""
        score = self.scorer.calculate_impact_score(self.sample_channel)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_novelty_score(self):
        """Test novelty score calculation."""
        score = self.scorer.calculate_novelty_score(self.sample_channel)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def setUp(self):
        self.scorer = ChannelScorer()

    def test_missing_subscriber_count(self):
        """Test channel without subscriber count."""
        channel = {
            'channel_id': 'UC_test',
            'videos': [
                {'view_count': 1000, 'upload_date': '20240101'},
            ],
        }
        result = self.scorer.score_channel(channel)
        self.assertIn('overall_score', result)

    def test_invalid_dates(self):
        """Test handling of invalid upload dates."""
        channel = {
            'channel_id': 'UC_test',
            'videos': [
                {'view_count': 1000, 'upload_date': 'invalid'},
                {'view_count': 2000, 'upload_date': '20240101'},
            ],
        }
        result = self.scorer.score_channel(channel)
        self.assertIn('overall_score', result)

    def test_zero_views(self):
        """Test channel with zero views."""
        channel = {
            'channel_id': 'UC_test',
            'videos': [
                {'view_count': 0, 'upload_date': '20240101'},
            ],
        }
        result = self.scorer.score_channel(channel)
        self.assertIn('overall_score', result)


if __name__ == '__main__':
    unittest.main()
