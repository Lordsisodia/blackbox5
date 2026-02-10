#!/usr/bin/env python3
"""
YouTube Scraper for BlackBox5

A robust YouTube video scraper that extracts metadata and transcripts,
stores them in BlackBox5's memory system, and supports autonomous operation.

Usage:
    python3 scraper.py --query "machine learning tutorial" --max-results 10
    python3 scraper.py --config config/config.yaml
    python3 scraper.py --video abc123 --only-transcript
"""

import argparse
import logging
import sys
import time
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent))

import yt_dlp

from lib.rate_limiter import RateLimiter
from lib.state_tracker import StateTracker
from lib.memory_storage import MemoryStorage
from lib.transcript_extractor import TranscriptExtractor, format_timestamp

# Configure logging
def setup_logging(level: str = "INFO", log_dir: Path = Path("logs")):
    """Set up logging configuration."""
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / f"scraper_{datetime.now().strftime('%Y-%m-%d')}.log"

    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler() if level.upper() != "DEBUG" else None
        ]
    )

    # Filter out None handler
    logger = logging.getLogger()
    logger.handlers = [h for h in logger.handlers if h]

    return logger

logger = logging.getLogger(__name__)


class YouTubeScraper:
    """Main YouTube scraper class."""

    def __init__(
        self,
        config_path: Optional[Path] = None,
        sqlite_db: Path = Path("data/scraper.db"),
        transcripts_dir: Path = Path("/opt/blackbox5/5-project-memory/youtube-scraper/knowledge/transcripts"),
        metadata_dir: Path = Path("/opt/blackbox5/5-project-memory/youtube-scraper/knowledge/metadata"),
        rate_limits: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize YouTube scraper.

        Args:
            config_path: Path to config file (optional)
            sqlite_db: Path to SQLite database
            transcripts_dir: Directory for transcripts
            metadata_dir: Directory for metadata
            rate_limits: Rate limiting configuration
        """
        # Load configuration if provided
        self.config = {}
        if config_path and config_path.exists():
            import yaml
            self.config = yaml.safe_load(config_path.read_text())
            logger.info(f"Loaded configuration from {config_path}")

        # Initialize components
        self.state_tracker = StateTracker(sqlite_db)

        rate_config = rate_limits or self.config.get('rate_limits', {})
        self.rate_limiter = RateLimiter(
            search_delay=rate_config.get('search_delay', 5.0),
            metadata_delay=rate_config.get('metadata_delay', 1.0),
            transcript_delay=rate_config.get('transcript_delay', 2.0),
            max_retries=rate_config.get('max_retries', 5),
            base_delay=rate_config.get('base_delay', 2.0),
            jitter_percent=rate_config.get('jitter_percent', 30)
        )

        self.memory_storage = MemoryStorage(
            transcripts_dir=transcripts_dir,
            metadata_dir=metadata_dir,
            summaries_dir=Path(str(transcripts_dir).replace('/transcripts', '/summaries')) if transcripts_dir else None,
            use_memory_system=True
        )

        transcript_config = self.config.get('scraper', {})
        self.transcript_extractor = TranscriptExtractor(
            languages=transcript_config.get('transcript_languages', ['en', 'auto']),
            use_auto_transcript=transcript_config.get('use_auto_transcript', True)
        )

        logger.info("YouTube Scraper initialized")

    def search_videos(
        self,
        query: str,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for YouTube videos.

        Args:
            query: Search query
            max_results: Maximum number of results

        Returns:
            List of video data dictionaries
        """
        logger.info(f"Searching for: {query} (max {max_results} results)")

        def _search():
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': 'in_playlist',
                'max_results': max_results,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)

            if not result or 'entries' not in result:
                return []

            entries = result['entries']
            videos = []

            for entry in entries:
                if entry is None:
                    continue

                video_data = {
                    'video_id': entry.get('id'),
                    'title': entry.get('title', 'Unknown'),
                    'channel': entry.get('channel', 'Unknown'),
                    'channel_id': entry.get('channel_id'),
                    'url': entry.get('url'),
                    'duration': entry.get('duration'),
                    'view_count': entry.get('view_count'),
                    'upload_date': entry.get('upload_date'),
                    'thumbnail': entry.get('thumbnail'),
                }
                videos.append(video_data)

            return videos

        # Apply rate limiting
        self.rate_limiter.before_search()
        videos = self.rate_limiter.retry_with_backoff(_search, operation=f"search('{query}')")

        logger.info(f"Found {len(videos)} videos")
        return videos

    def scrape_video(
        self,
        video_id: str,
        query_used: Optional[str] = None,
        force_rescrape: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Scrape a single video (metadata + transcript).

        Args:
            video_id: YouTube video ID
            query_used: Query that led to this video (for tracking)
            force_rescrape: Force re-scraping even if already scraped

        Returns:
            Video data with transcript or None if failed
        """
        # Check if already scraped
        if not force_rescrape and self.state_tracker.is_scraped(video_id):
            logger.info(f"Video {video_id} already scraped, skipping")
            return None

        logger.info(f"Scraping video: {video_id}")

        try:
            # Get video metadata
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            def _get_metadata():
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'writesubtitles': False,
                    'writeautomaticsub': False,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=False)

                return info

            self.rate_limiter.before_metadata()
            info = self.rate_limiter.retry_with_backoff(_get_metadata, operation=f"metadata({video_id})")

            if not info:
                logger.error(f"Failed to get metadata for {video_id}")
                self.state_tracker.add_failed_video(video_id, None, "Failed to get metadata")
                return None

            # Extract video data
            video_data = {
                'video_id': video_id,
                'title': info.get('title', 'Unknown'),
                'channel': info.get('channel', 'Unknown'),
                'channel_id': info.get('channel_id'),
                'url': video_url,
                'duration': info.get('duration'),
                'views': info.get('view_count'),
                'upload_date': info.get('upload_date', '')[:10] if info.get('upload_date') else '',
                'description': info.get('description', ''),
                'tags': info.get('tags', []),
                'category': info.get('category'),
                'query_used': query_used,
            }

            # Get transcript
            transcript_data = None
            def _get_transcript():
                return self.transcript_extractor.extract_best_transcript(video_id)

            self.rate_limiter.before_transcript()
            transcript_data = self.rate_limiter.retry_with_backoff(_get_transcript, operation=f"transcript({video_id})")

            # Save to state tracker
            has_transcript = transcript_data is not None
            transcript_length = transcript_data.get('length', 0) if transcript_data else 0
            transcript_type = transcript_data.get('type', None) if transcript_data else None

            self.state_tracker.add_video(
                video_id=video_id,
                title=video_data['title'],
                channel=video_data['channel'],
                channel_id=video_data['channel_id'],
                has_transcript=has_transcript,
                transcript_length=transcript_length,
                transcript_type=transcript_type,
                duration=video_data['duration'],
                views=video_data['views'],
                upload_date=video_data['upload_date'],
                query_used=query_used
            )

            # Save to memory if transcript available
            if transcript_data:
                self.memory_storage.save_transcript(
                    video_id=video_id,
                    video_data=video_data,
                    transcript_data=transcript_data,
                    create_summary=True
                )
                logger.info(f"Successfully scraped {video_id}: {video_data['title']}")
            else:
                logger.warning(f"No transcript available for {video_id}")

            return video_data

        except Exception as e:
            logger.error(f"Error scraping video {video_id}: {e}")
            self.state_tracker.add_failed_video(video_id, video_id, str(e))
            return None

    def scrape_batch(
        self,
        video_ids: List[str],
        query_used: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Scrape multiple videos.

        Args:
            video_ids: List of video IDs
            query_used: Query that led to these videos

        Returns:
            List of successfully scraped video data
        """
        results = []

        for video_id in video_ids:
            video_data = self.scrape_video(video_id, query_used=query_used)
            if video_data:
                results.append(video_data)

        return results

    def search_and_scrape(
        self,
        query: str,
        max_results: int = 10,
        force_rescrape: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Search for videos and scrape them.

        Args:
            query: Search query
            max_results: Maximum number of results to scrape
            force_rescrape: Force re-scraping

        Returns:
            List of scraped video data
        """
        logger.info(f"Search and scrape: '{query}'")

        # Search for videos
        videos = self.search_videos(query, max_results)

        if not videos:
            logger.warning("No videos found")
            return []

        # Filter out already scraped videos (unless forced)
        new_videos = []
        for video in videos:
            video_id = video['video_id']
            if force_rescrape or not self.state_tracker.is_scraped(video_id):
                new_videos.append(video)

        logger.info(f"Found {len(videos)} total, {len(new_videos)} new to scrape")

        if not new_videos:
            return []

        # Scrape each video
        scraped = []
        for video in new_videos:
            result = self.scrape_video(
                video_id=video['video_id'],
                query_used=query,
                force_rescrape=force_rescrape
            )
            if result:
                scraped.append(result)

        # Update statistics
        self.state_tracker.update_stats(
            videos_scraped=len(scraped),
            transcripts_fetched=sum(1 for v in scraped if self.state_tracker.is_scraped(v['video_id'])),
            search_queries=1
        )

        logger.info(f"Scraped {len(scraped)}/{len(new_videos)} new videos")
        return scraped

    def run_scheduled_queries(self):
        """Run all scheduled queries from config."""
        queries = self.config.get('queries', [])

        for query_config in queries:
            if not query_config.get('enabled', True):
                continue

            query = query_config['query']
            max_results = query_config.get('max_results', 10)

            logger.info(f"Running scheduled query: {query}")
            self.search_and_scrape(query, max_results)

    def get_stats(self) -> Dict[str, Any]:
        """Get scraping statistics."""
        db_stats = self.state_tracker.get_total_stats()
        rate_stats = self.rate_limiter.get_stats()

        return {
            **db_stats,
            'rate_limiter': rate_stats
        }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="YouTube Scraper for BlackBox5",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search and scrape videos
  python3 scraper.py --query "machine learning tutorial" --max-results 10

  # Scrape a specific video
  python3 scraper.py --video abc123

  # Use config file
  python3 scraper.py --config config/config.yaml

  # Run scheduled queries from config
  python3 scraper.py --scheduled

  # Show statistics
  python3 scraper.py --stats
        """
    )

    parser.add_argument('--config', type=Path, help='Path to config file')
    parser.add_argument('--query', type=str, help='Search query')
    parser.add_argument('--max-results', type=int, default=10, help='Maximum results per search')
    parser.add_argument('--video', type=str, help='Specific video ID to scrape')
    parser.add_argument('--scheduled', action='store_true', help='Run scheduled queries from config')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--force', action='store_true', help='Force re-scraping of existing videos')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--db', type=Path, default=Path('data/scraper.db'), help='SQLite database path')

    args = parser.parse_args()

    # Setup logging
    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logging(level=log_level)

    # Initialize scraper
    scraper = YouTubeScraper(
        config_path=args.config,
        sqlite_db=args.db
    )

    # Handle commands
    if args.stats:
        stats = scraper.get_stats()
        print("\n=== YouTube Scraper Statistics ===")
        print(f"Total videos scraped: {stats['total_videos']}")
        print(f"Videos with transcripts: {stats['videos_with_transcripts']}")
        print(f"Unique channels: {stats['unique_channels']}")
        print(f"Total transcript characters: {stats['total_transcript_chars']:,}")
        print(f"Transcript coverage: {stats['transcript_coverage']:.1f}%")
        print(f"Total errors: {stats['total_errors']}")
        print(f"\nRequest counts:")
        print(f"  Searches: {stats['rate_limiter']['request_count']['search']}")
        print(f"  Metadata: {stats['rate_limiter']['request_count']['metadata']}")
        print(f"  Transcripts: {stats['rate_limiter']['request_count']['transcript']}")
        return

    if args.scheduled:
        logger.info("Running scheduled queries")
        scraper.run_scheduled_queries()
        return

    if args.video:
        logger.info(f"Scraping specific video: {args.video}")
        scraper.scrape_video(args.video, force_rescrape=args.force)
        return

    if args.query:
        logger.info(f"Searching for: {args.query}")
        scraper.search_and_scrape(args.query, max_results=args.max_results, force_rescrape=args.force)
        return

    # No action specified
    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
