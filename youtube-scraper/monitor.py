#!/usr/bin/env python3
"""
YouTube Scraper Monitoring Dashboard
Shows scraping status, statistics, and recent activity

Usage:
    python monitor.py [options]

Options:
    --config FILE       Configuration file (default: config/config.yaml)
    --watch             Auto-refresh every 5 seconds
    --json              Output as JSON instead of formatted text
"""

import os
import sys
import json
import argparse
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

import yaml


class Monitor:
    """Monitor class for YouTube scraper metrics"""

    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config = self.load_config()
        self.db_path = self.config.get('storage.state_db')

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def get_db_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_stats(self) -> Dict[str, Any]:
        """Get overall statistics"""
        conn = self.get_db_connection()
        cursor = conn.cursor()

        # Total videos
        cursor.execute("SELECT COUNT(*) FROM videos")
        total = cursor.fetchone()[0]

        # Processed
        cursor.execute("SELECT COUNT(*) FROM videos WHERE processed = 1")
        processed = cursor.fetchone()[0]

        # With transcripts
        cursor.execute("SELECT COUNT(*) FROM videos WHERE has_transcript = 1")
        with_transcripts = cursor.fetchone()[0]

        # With errors
        cursor.execute("SELECT COUNT(*) FROM videos WHERE error_count > 0")
        with_errors = cursor.fetchone()[0]

        # Transcript stats
        cursor.execute("SELECT AVG(transcript_length) FROM videos WHERE transcript_length > 0")
        avg_transcript_length = cursor.fetchone()[0] or 0

        cursor.execute("SELECT SUM(transcript_length) FROM videos WHERE transcript_length > 0")
        total_transcript_length = cursor.fetchone()[0] or 0

        conn.close()

        return {
            'total_videos': total,
            'processed': processed,
            'with_transcripts': with_transcripts,
            'with_errors': with_errors,
            'avg_transcript_length': int(avg_transcript_length),
            'total_transcript_length': total_transcript_length,
        }

    def get_recent_videos(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recently scraped videos"""
        conn = self.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT video_id, title, channel, scraped_at, has_transcript, processed
            FROM videos
            ORDER BY scraped_at DESC
            LIMIT ?
        """, (limit,))

        videos = []
        for row in cursor.fetchall():
            videos.append({
                'video_id': row['video_id'],
                'title': row['title'],
                'channel': row['channel'],
                'scraped_at': row['scraped_at'],
                'has_transcript': bool(row['has_transcript']),
                'processed': bool(row['processed']),
            })

        conn.close()
        return videos

    def get_recent_metrics(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent run metrics"""
        conn = self.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT timestamp, videos_scraped, transcripts_fetched, errors, runtime_seconds
            FROM metrics
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))

        metrics = []
        for row in cursor.fetchall():
            metrics.append({
                'timestamp': row['timestamp'],
                'videos_scraped': row['videos_scraped'],
                'transcripts_fetched': row['transcripts_fetched'],
                'errors': row['errors'],
                'runtime_seconds': row['runtime_seconds'],
            })

        conn.close()
        return metrics

    def get_error_videos(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get videos with errors"""
        conn = self.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT video_id, title, channel, error_count, last_error
            FROM videos
            WHERE error_count > 0
            ORDER BY error_count DESC
            LIMIT ?
        """, (limit,))

        videos = []
        for row in cursor.fetchall():
            videos.append({
                'video_id': row['video_id'],
                'title': row['title'],
                'channel': row['channel'],
                'error_count': row['error_count'],
                'last_error': row['last_error'],
            })

        conn.close()
        return videos

    def get_channel_stats(self) -> List[Dict[str, Any]]:
        """Get statistics by channel"""
        conn = self.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT channel, COUNT(*) as video_count, SUM(has_transcript) as transcript_count
            FROM videos
            GROUP BY channel
            ORDER BY video_count DESC
        """)

        channels = []
        for row in cursor.fetchall():
            channels.append({
                'channel': row['channel'],
                'video_count': row['video_count'],
                'transcript_count': row['transcript_count'],
            })

        conn.close()
        return channels

    def get_activity_heatmap(self, days: int = 7) -> Dict[str, Any]:
        """Get activity heatmap for last N days"""
        conn = self.get_db_connection()
        cursor = conn.cursor()

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        heatmap = {}
        for i in range(days):
            date = (end_date - timedelta(days=i)).strftime('%Y-%m-%d')
            heatmap[date] = 0

        cursor.execute("""
            SELECT DATE(scraped_at) as date, COUNT(*) as count
            FROM videos
            WHERE scraped_at >= ?
            GROUP BY DATE(scraped_at)
        """, (start_date.strftime('%Y-%m-%d'),))

        for row in cursor.fetchall():
            date_key = row['date']
            if date_key in heatmap:
                heatmap[date_key] = row['count']

        conn.close()
        return heatmap

    def format_size(self, bytes_size: int) -> str:
        """Format bytes to human-readable size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.1f} TB"

    def format_duration(self, seconds: float) -> str:
        """Format seconds to human-readable duration"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"

    def print_dashboard(self):
        """Print formatted dashboard"""
        print("\n" + "=" * 70)
        print(" " * 20 + "YOUTUBE SCRAPER MONITOR")
        print("=" * 70)

        # Stats
        stats = self.get_stats()

        print("\n📊 Overall Statistics")
        print("-" * 70)
        print(f"  Total Videos:        {stats['total_videos']:,}")
        print(f"  Processed:           {stats['processed']:,} ({stats['processed']/max(stats['total_videos'], 1)*100:.1f}%)")
        print(f"  With Transcripts:    {stats['with_transcripts']:,} ({stats['with_transcripts']/max(stats['total_videos'], 1)*100:.1f}%)")
        print(f"  With Errors:         {stats['with_errors']:,} ({stats['with_errors']/max(stats['total_videos'], 1)*100:.1f}%)")
        print(f"  Avg Transcript:      {self.format_size(stats['avg_transcript_length'])}")
        print(f"  Total Content:       {self.format_size(stats['total_transcript_length'])}")

        # Recent activity
        recent_metrics = self.get_recent_metrics(5)

        if recent_metrics:
            print("\n📈 Recent Runs")
            print("-" * 70)
            for metric in reversed(recent_metrics):
                timestamp = metric['timestamp'].replace('T', ' ').split('.')[0]
                print(f"  {timestamp}")
                print(f"    Videos: {metric['videos_scraped']}, "
                      f"Transcripts: {metric['transcripts_fetched']}, "
                      f"Errors: {metric['errors']}, "
                      f"Time: {self.format_duration(metric['runtime_seconds'])}")

        # Recent videos
        recent_videos = self.get_recent_videos(5)

        if recent_videos:
            print("\n📺 Recently Scraped Videos")
            print("-" * 70)
            for video in recent_videos:
                timestamp = video['scraped_at'].replace('T', ' ').split('.')[0]
                status = "✓" if video['processed'] else "○"
                transcript = "📝" if video['has_transcript'] else "✗"
                title = video['title'][:50] + "..." if len(video['title']) > 50 else video['title']
                print(f"  {status} {transcript} {title}")
                print(f"    {video['channel']} • {timestamp}")

        # Error videos
        error_videos = self.get_error_videos(5)

        if error_videos:
            print("\n⚠️  Videos with Errors")
            print("-" * 70)
            for video in error_videos:
                title = video['title'][:50] + "..." if len(video['title']) > 50 else video['title']
                print(f"  ❌ {title} ({video['error_count']} errors)")
                print(f"     {video['last_error'][:60]}...")

        # Channel stats
        channel_stats = self.get_channel_stats()[:5]

        if channel_stats:
            print("\n📺 Top Channels")
            print("-" * 70)
            for channel in channel_stats:
                transcript_rate = (channel['transcript_count'] / max(channel['video_count'], 1)) * 100
                print(f"  {channel['channel']}")
                print(f"    Videos: {channel['video_count']}, "
                      f"Transcripts: {channel['transcript_count']} "
                      f"({transcript_rate:.0f}%)")

        # Activity heatmap
        heatmap = self.get_activity_heatmap(7)
        print("\n📅 Activity (Last 7 Days)")
        print("-" * 70)

        dates = sorted(heatmap.keys(), reverse=True)
        for date in dates:
            count = heatmap[date]
            bar = "█" * min(count, 20)
            print(f"  {date}: {bar} ({count})")

        print("\n" + "=" * 70 + "\n")

    def print_json(self):
        """Print dashboard as JSON"""
        data = {
            'stats': self.get_stats(),
            'recent_videos': self.get_recent_videos(20),
            'recent_metrics': self.get_recent_metrics(20),
            'error_videos': self.get_error_videos(20),
            'channel_stats': self.get_channel_stats(),
            'activity_heatmap': self.get_activity_heatmap(7),
        }

        print(json.dumps(data, indent=2))


def main():
    parser = argparse.ArgumentParser(description='YouTube Scraper Monitor')
    parser.add_argument('--config', default='config/config.yaml', help='Config file path')
    parser.add_argument('--watch', action='store_true', help='Auto-refresh every 5 seconds')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    monitor = Monitor(args.config)

    if args.watch:
        import time

        try:
            while True:
                os.system('clear' if os.name == 'posix' else 'cls')

                if args.json:
                    monitor.print_json()
                else:
                    monitor.print_dashboard()

                print("Refreshing in 5 seconds (Ctrl+C to stop)...")
                time.sleep(5)
        except KeyboardInterrupt:
            print("\nStopped by user")
    else:
        if args.json:
            monitor.print_json()
        else:
            monitor.print_dashboard()


if __name__ == '__main__':
    main()
