#!/usr/bin/env python3
"""
Transcript Worker - Main Worker Loop

Continuously fetches transcripts from the queue with rate limiting.
Designed to run as a systemd service on a dedicated server.
"""

import sys
import time
import signal
import argparse
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from queue.manager import QueueManager
from queue.database import QueueDatabase
from worker.transcript_fetcher import TranscriptFetcher
from worker.rate_limiter import RateLimiter


class TranscriptWorker:
    """Main worker that fetches transcripts continuously."""

    def __init__(
        self,
        output_dir: Path,
        state_dir: Path,
        daily_limit: int = 200,
        request_delay: float = 2.0,
        batch_size: int = 10
    ):
        """
        Initialize worker.

        Args:
            output_dir: Directory to save transcripts
            state_dir: Directory for state files
            daily_limit: Max videos per day
            request_delay: Seconds between requests
            batch_size: Videos to fetch per batch
        """
        self.output_dir = output_dir
        self.state_dir = state_dir
        self.batch_size = batch_size
        self.running = False

        # Initialize components
        self.db = QueueDatabase()
        self.manager = QueueManager(self.db)
        self.fetcher = TranscriptFetcher(output_dir, delay=request_delay)
        self.rate_limiter = RateLimiter(
            state_file=state_dir / 'rate_limiter.json',
            daily_limit=daily_limit,
            request_delay=request_delay
        )

        # Stats
        self.stats = {
            'started_at': datetime.now().isoformat(),
            'fetched': 0,
            'failed': 0,
            'skipped': 0
        }

        # Setup signal handlers
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)

    def _handle_signal(self, signum, frame):
        """Handle shutdown signals gracefully."""
        print(f"\nReceived signal {signum}, shutting down...")
        self.running = False

    def _log(self, message: str):
        """Log with timestamp."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {message}")

    def process_single(self, video: dict) -> bool:
        """
        Process a single video.

        Args:
            video: Video data from queue

        Returns:
            True if successful, False otherwise
        """
        video_id = video['video_id']
        channel = video.get('channel_slug', 'unknown')
        priority = video.get('priority', 'P3')

        self._log(f"Processing {video_id} ({channel}, {priority})")

        # Mark as fetching
        self.manager.mark_fetching(video_id)

        # Fetch transcript
        success, transcript, error = self.fetcher.fetch(video_id, video)

        if success and transcript:
            # Save transcript
            try:
                output_path = self.fetcher.save_transcript(video_id, video, transcript)
                self.manager.mark_completed(video_id, str(output_path))
                self._log(f"  ✓ Saved to {output_path}")
                self.stats['fetched'] += 1
                self.rate_limiter.record_request(success=True)
                return True
            except Exception as e:
                error_msg = f"Save error: {str(e)}"
                self.manager.mark_failed(video_id, error_msg)
                self._log(f"  ✗ {error_msg}")
                self.stats['failed'] += 1
                self.rate_limiter.record_request(success=False)
                return False
        else:
            # Fetch failed
            self.manager.mark_failed(video_id, error or "Unknown error")
            self._log(f"  ✗ {error or 'Unknown error'}")
            self.stats['failed'] += 1
            self.rate_limiter.record_request(success=False)
            return False

    def run_batch(self, limit: int = None) -> dict:
        """
        Run a single batch of fetches.

        Args:
            limit: Max videos to process (None = use batch_size)

        Returns:
            Stats dict
        """
        if limit is None:
            limit = self.batch_size

        self._log(f"Starting batch (limit: {limit})")
        self._log(f"Rate limiter: {self.rate_limiter.get_status()}")

        # Get pending videos
        videos = self.manager.get_next_batch(limit)

        if not videos:
            self._log("No pending videos in queue")
            return self.stats

        self._log(f"Found {len(videos)} videos to process")

        for video in videos:
            # Check rate limits
            if not self.rate_limiter.can_proceed():
                self._log("Rate limit reached, stopping batch")
                break

            # Process video
            self.process_single(video)

            # Small delay between videos (handled by fetcher, but extra safety)
            time.sleep(0.5)

        self._log(f"Batch complete. Stats: {self.stats}")
        return self.stats

    def run_continuous(self):
        """Run worker continuously until stopped."""
        self.running = True
        self._log("Starting continuous worker...")
        self._log(f"Output directory: {self.output_dir}")
        self._log(f"State directory: {self.state_dir}")

        while self.running:
            # Check if we should stop for the day
            if self.rate_limiter.should_stop_for_today():
                status = self.rate_limiter.get_status()
                self._log(f"Daily limit reached ({status['used_today']}/{status['daily_limit']})")
                self._log("Sleeping until tomorrow...")

                # Sleep for an hour and check again
                for _ in range(3600):
                    if not self.running:
                        break
                    time.sleep(1)
                continue

            # Run a batch
            self.run_batch()

            # Show queue stats
            queue_stats = self.manager.get_stats()
            self._log(f"Queue status: {queue_stats}")

            # If no more pending videos, sleep longer
            if queue_stats['pending'] == 0:
                self._log("No pending videos, sleeping for 1 hour...")
                for _ in range(3600):
                    if not self.running:
                        break
                    time.sleep(1)
            else:
                # Short sleep between batches
                self._log("Sleeping for 10 seconds...")
                for _ in range(10):
                    if not self.running:
                        break
                    time.sleep(1)

        self._log("Worker stopped")
        return self.stats


def main():
    parser = argparse.ArgumentParser(description='Transcript Worker')
    parser.add_argument('--output-dir', type=Path, default=Path('/opt/transcripts/content'),
                        help='Directory to save transcripts')
    parser.add_argument('--state-dir', type=Path, default=Path('/opt/transcripts/state'),
                        help='Directory for state files')
    parser.add_argument('--daily-limit', type=int, default=200,
                        help='Maximum videos per day')
    parser.add_argument('--request-delay', type=float, default=2.0,
                        help='Seconds between requests')
    parser.add_argument('--batch-size', type=int, default=10,
                        help='Videos per batch')
    parser.add_argument('--continuous', action='store_true',
                        help='Run continuously (for systemd service)')
    parser.add_argument('--limit', type=int, default=None,
                        help='Limit total videos (for testing)')

    args = parser.parse_args()

    # Create directories
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.state_dir.mkdir(parents=True, exist_ok=True)

    # Initialize worker
    worker = TranscriptWorker(
        output_dir=args.output_dir,
        state_dir=args.state_dir,
        daily_limit=args.daily_limit,
        request_delay=args.request_delay,
        batch_size=args.batch_size
    )

    if args.continuous:
        # Run continuously (for systemd service)
        worker.run_continuous()
    else:
        # Run single batch
        limit = args.limit or args.batch_size
        stats = worker.run_batch(limit=limit)
        print(f"\nFinal stats: {stats}")


if __name__ == '__main__':
    main()
