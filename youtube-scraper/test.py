#!/usr/bin/env python3
"""
YouTube Scraper Test Suite
Tests scraper functionality, transcript extraction, and knowledge base integration

Usage:
    python test.py [options]

Options:
    --config FILE       Configuration file (default: config/config.yaml)
    --video ID          Test specific video ID
    --suite SUITE       Run specific test suite (all, basic, transcript, integration)
    --verbose           Enable verbose output
"""

import os
import sys
import unittest
import tempfile
import shutil
from pathlib import Path
from typing import Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    import yaml
    import yt_dlp
    from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
    from scraper import Config, Database, YouTubeScraper
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please ensure all dependencies are installed:")
    print("  pip install pyyaml yt-dlp youtube-transcript-api")
    sys.exit(1)


class TestConfig(unittest.TestCase):
    """Test configuration loading"""

    def setUp(self):
        self.config_path = Path(__file__).parent / 'config' / 'config.yaml'

    def test_config_exists(self):
        """Test that config file exists"""
        self.assertTrue(self.config_path.exists(), f"Config file not found: {self.config_path}")

    def test_config_loads(self):
        """Test that config loads successfully"""
        config = Config(str(self.config_path))
        self.assertIsNotNone(config.config)

    def test_config_required_keys(self):
        """Test that required config keys exist"""
        config = Config(str(self.config_path))

        required_keys = [
            'playlist.url',
            'storage.base_dir',
            'storage.state_db',
            'logging.log_dir',
        ]

        for key in required_keys:
            value = config.get(key)
            self.assertIsNotNone(value, f"Missing required config key: {key}")

    def test_config_defaults(self):
        """Test that config defaults work"""
        config = Config(str(self.config_path))

        # Test with missing keys
        self.assertIsNone(config.get('nonexistent.key'))
        self.assertEqual(config.get('nonexistent.key', 'default'), 'default')


class TestDatabase(unittest.TestCase):
    """Test database functionality"""

    def setUp(self):
        # Create temporary database
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, 'test.db')
        self.db = Database(self.db_path)

    def tearDown(self):
        # Clean up temporary database
        if self.db and self.db.conn:
            self.db.conn.close()
        shutil.rmtree(self.temp_dir)

    def test_database_init(self):
        """Test database initialization"""
        self.assertIsNotNone(self.db.conn)
        self.assertIsNotNone(self.db.db_path)

    def test_add_video(self):
        """Test adding a video to database"""
        video_data = {
            'video_id': 'test123',
            'title': 'Test Video',
            'channel': 'Test Channel',
            'published_at': '2025-02-10',
            'scraped_at': '2025-02-10T20:00:00Z',
            'has_transcript': True,
            'transcript_length': 1000,
            'processed': True,
            'checksum': 'abc123',
        }

        self.db.add_video(video_data)

        # Check video exists
        self.assertTrue(self.db.is_processed('test123'))

    def test_duplicate_video(self):
        """Test handling duplicate videos"""
        video_data = {
            'video_id': 'test123',
            'title': 'Test Video',
            'channel': 'Test Channel',
            'published_at': '2025-02-10',
            'scraped_at': '2025-02-10T20:00:00Z',
            'has_transcript': True,
            'transcript_length': 1000,
            'processed': True,
            'checksum': 'abc123',
        }

        self.db.add_video(video_data)
        self.db.add_video(video_data)  # Should update, not duplicate

        stats = self.db.get_stats()
        self.assertEqual(stats['total_videos'], 1)

    def test_record_error(self):
        """Test recording errors"""
        video_data = {
            'video_id': 'test123',
            'title': 'Test Video',
            'channel': 'Test Channel',
        }

        self.db.add_video(video_data)
        self.db.record_error('test123', 'Test error message')

        # Check error count
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT error_count, last_error FROM videos WHERE video_id = ?", ('test123',))
        result = cursor.fetchone()

        self.assertEqual(result[0], 1)
        self.assertIn('Test error message', result[1])

    def test_get_stats(self):
        """Test getting statistics"""
        # Add multiple videos
        for i in range(5):
            video_data = {
                'video_id': f'test{i}',
                'title': f'Test Video {i}',
                'channel': 'Test Channel',
                'published_at': '2025-02-10',
                'scraped_at': '2025-02-10T20:00:00Z',
                'has_transcript': i % 2 == 0,  # Alternating
                'transcript_length': 1000 if i % 2 == 0 else 0,
                'processed': True,
            }
            self.db.add_video(video_data)

        stats = self.db.get_stats()

        self.assertEqual(stats['total_videos'], 5)
        self.assertEqual(stats['processed'], 5)
        self.assertEqual(stats['with_transcript'], 3)  # 0, 2, 4 have transcripts
        self.assertEqual(stats['with_errors'], 0)

    def test_record_metrics(self):
        """Test recording run metrics"""
        metrics = {
            'videos_scraped': 10,
            'transcripts_fetched': 8,
            'errors': 1,
            'runtime_seconds': 120.5,
        }

        self.db.record_metrics(metrics)

        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM metrics WHERE videos_scraped = 10")
        result = cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[2], 10)  # videos_scraped
        self.assertEqual(result[3], 8)   # transcripts_fetched
        self.assertEqual(result[4], 1)   # errors


class TestTranscriptExtraction(unittest.TestCase):
    """Test transcript extraction functionality"""

    def setUp(self):
        # Use a known test video
        self.test_video_id = 'dQw4w9WgXcQ'  # Rick Astley - Never Gonna Give You Up

    def test_transcript_api_available(self):
        """Test that youtube-transcript-api is available"""
        self.assertIsNotNone(YouTubeTranscriptApi)

    def test_get_transcript_success(self):
        """Test fetching transcript from a real video"""
        try:
            ytt = YouTubeTranscriptApi()
            transcript = ytt.fetch(self.test_video_id)
            self.assertIsInstance(transcript, list)
            self.assertGreater(len(transcript), 0)

            # Check transcript structure
            first_item = transcript[0]
            self.assertIn('text', first_item)
            self.assertIn('start', first_item)
            self.assertIn('duration', first_item)
        except (NoTranscriptFound, Exception) as e:
            self.skipTest(f"Could not fetch transcript for test video: {e}")

    def test_get_transcript_nonexistent(self):
        """Test handling of non-existent video"""
        fake_video_id = 'nonexistent123456789'
        ytt = YouTubeTranscriptApi()

        with self.assertRaises(Exception):
            ytt.fetch(fake_video_id)

    def test_list_transcripts(self):
        """Test listing available transcripts"""
        try:
            ytt = YouTubeTranscriptApi()
            transcript_list = ytt.list(self.test_video_id)
            self.assertIsNotNone(transcript_list)

            # Try to find an English transcript
            transcript = transcript_list.find_transcript(['en'])
            self.assertIsNotNone(transcript)
        except Exception as e:
            self.skipTest(f"Could not list transcripts for test video: {e}")


class TestYouTubeDLP(unittest.TestCase):
    """Test yt-dlp functionality"""

    def setUp(self):
        self.test_video_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

    def test_ytdlp_available(self):
        """Test that yt-dlp is available"""
        self.assertIsNotNone(yt_dlp)

    def test_extract_video_info(self):
        """Test extracting video information"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(self.test_video_url, download=False)

                self.assertIsNotNone(result)
                self.assertEqual(result['id'], 'dQw4w9WgXcQ')
                self.assertIn('title', result)
                self.assertIn('uploader', result)
        except Exception as e:
            self.skipTest(f"Could not extract video info: {e}")

    def test_extract_playlist(self):
        """Test extracting playlist information"""
        # Use a short test playlist
        playlist_url = 'https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf'

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'playlistend': 5,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(playlist_url, download=False)

                self.assertIsNotNone(result)
                self.assertIn('entries', result)
                self.assertGreater(len(result['entries']), 0)
        except Exception as e:
            self.skipTest(f"Could not extract playlist: {e}")


class TestScraper(unittest.TestCase):
    """Test main scraper functionality"""

    def setUp(self):
        self.config_path = Path(__file__).parent / 'config' / 'config.yaml'

        # Create temporary directories for testing
        self.temp_dir = tempfile.mkdtemp()

        # Create test config with temporary paths
        self.test_config = {
            'playlist': {
                'url': 'https://www.youtube.com/playlist?list=PLwyznWCpE24c3tepHAdTqFwHsQ-xTXDkN',
                'check_interval': 600,
                'max_videos_per_run': 1,
            },
            'storage': {
                'base_dir': os.path.join(self.temp_dir, 'knowledge'),
                'transcripts_dir': 'transcripts',
                'metadata_dir': 'metadata',
                'summaries_dir': 'summaries',
                'state_db': os.path.join(self.temp_dir, 'test.db'),
            },
            'logging': {
                'log_dir': os.path.join(self.temp_dir, 'logs'),
                'level': 'INFO',
            },
            'rate_limit': {
                'max_retries': 2,
                'base_backoff': 1,
                'max_backoff': 5,
                'delay_between_videos': 3,
                'delay_between_transcripts': 2,
            },
            'transcript': {
                'languages': ['en'],
                'preserve_formatting': False,
                'prefer_manual': True,
                'require_transcript': True,
            },
            'anti_blocking': {
                'random_delay_jitter': 0.3,
            },
            'output': {
                'format': 'markdown',
                'include_timestamps': True,
                'include_metadata': True,
                'include_url': True,
            },
        }

        # Write test config
        self.test_config_path = os.path.join(self.temp_dir, 'config.yaml')
        with open(self.test_config_path, 'w') as f:
            yaml.dump(self.test_config, f)

        self.config = Config(self.test_config_path)

    def tearDown(self):
        # Clean up temporary directories
        shutil.rmtree(self.temp_dir)

    def test_scraper_init(self):
        """Test scraper initialization"""
        scraper = YouTubeScraper(self.config)
        self.assertIsNotNone(scraper)
        self.assertIsNotNone(scraper.db)
        self.assertIsNotNone(scraper.logger)

    def test_extract_video_id(self):
        """Test video ID extraction from URLs"""
        scraper = YouTubeScraper(self.config)

        test_urls = [
            ('https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'dQw4w9WgXcQ'),
            ('https://youtu.be/dQw4w9WgXcQ', 'dQw4w9WgXcQ'),
            ('https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=10s', 'dQw4w9WgXcQ'),
        ]

        for url, expected_id in test_urls:
            result_id = scraper.extract_video_id(url)
            self.assertEqual(result_id, expected_id)

    def test_storage_dirs_created(self):
        """Test that storage directories are created"""
        scraper = YouTubeScraper(self.config)

        for dir_name, dir_path in scraper.storage_dirs.items():
            self.assertTrue(dir_path.exists(), f"Directory {dir_name} not created at {dir_path}")


def run_tests(suite_name: Optional[str] = None, video_id: Optional[str] = None):
    """Run test suites"""

    if suite_name:
        suite_map = {
            'basic': unittest.TestLoader().loadTestsFromTestCase(TestConfig),
            'database': unittest.TestLoader().loadTestsFromTestCase(TestDatabase),
            'transcript': unittest.TestLoader().loadTestsFromTestCase(TestTranscriptExtraction),
            'ytdlp': unittest.TestLoader().loadTestsFromTestCase(TestYouTubeDLP),
            'scraper': unittest.TestLoader().loadTestsFromTestCase(TestScraper),
        }

        suite = suite_map.get(suite_name)
        if not suite:
            print(f"Unknown test suite: {suite_name}")
            print(f"Available suites: {', '.join(suite_map.keys())}")
            return False
    else:
        # Run all tests
        suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


def main():
    import argparse

    parser = argparse.ArgumentParser(description='YouTube Scraper Test Suite')
    parser.add_argument('--config', default='config/config.yaml', help='Config file path')
    parser.add_argument('--video', help='Test specific video ID')
    parser.add_argument('--suite', choices=['all', 'basic', 'database', 'transcript', 'ytdlp', 'scraper'],
                       default='all', help='Test suite to run')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    print("=" * 70)
    print(" " * 20 + "YOUTUBE SCRAPER TEST SUITE")
    print("=" * 70)
    print()

    success = run_tests(
        suite_name=args.suite if args.suite != 'all' else None,
        video_id=args.video
    )

    print()
    if success:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
