"""
Queue Manager for Transcript Pipeline

High-level queue management with priority calculation.
"""

from datetime import datetime
from typing import List, Dict, Optional
from .database import QueueDatabase


# Channel tier multipliers
CHANNEL_TIERS = {
    'david_ondrej': {'tier': 'S', 'multiplier': 1.2},
    'vrsen': {'tier': 'S', 'multiplier': 1.2},
    'bijan_bowen': {'tier': 'A', 'multiplier': 1.1},
    'andre_mikalsen': {'tier': 'A', 'multiplier': 1.1},
    'ai_code_king': {'tier': 'A', 'multiplier': 1.1},
    'ai_jason': {'tier': 'B', 'multiplier': 1.05},
    'indydevdan': {'tier': 'B', 'multiplier': 1.05},
    'greg_isenberg': {'tier': 'B', 'multiplier': 1.05},
}


def get_channel_tier(channel_slug: str) -> tuple:
    """Get tier and multiplier for channel."""
    channel_slug = channel_slug.lower()
    if channel_slug in CHANNEL_TIERS:
        data = CHANNEL_TIERS[channel_slug]
        return data['tier'], data['multiplier']
    return 'C', 1.0


def calculate_priority(channel_slug: str, upload_date: str, duration: int, score: float) -> str:
    """
    Calculate priority based on channel tier, recency, and duration.

    P0: S-tier + this week + 18+ min
    P1: A-tier + 2 weeks + 18+ min OR S-tier + this week
    P2: Any + this month + 18+ min OR A-tier + 2 weeks
    P3: Everything else
    """
    tier, _ = get_channel_tier(channel_slug)

    # Parse recency
    try:
        upload = datetime.strptime(upload_date, '%Y%m%d')
        days_ago = (datetime.now() - upload).days
    except:
        days_ago = 999

    is_long = duration >= 1080  # 18+ minutes
    is_this_week = days_ago <= 7
    is_two_weeks = days_ago <= 14
    is_this_month = days_ago <= 30

    # P0: S-tier + this week + long
    if tier == 'S' and is_this_week and is_long:
        return 'P0'

    # P1: (A-tier + 2 weeks + long) OR (S-tier + this week)
    if (tier == 'A' and is_two_weeks and is_long) or (tier == 'S' and is_this_week):
        return 'P1'

    # P2: (Any + this month + long) OR (A-tier + 2 weeks)
    if (is_this_month and is_long) or (tier == 'A' and is_two_weeks):
        return 'P2'

    # P3: Everything else
    return 'P3'


class QueueManager:
    """High-level queue management."""

    def __init__(self, db: Optional[QueueDatabase] = None):
        self.db = db or QueueDatabase()

    def add_video(self, video_data: Dict) -> bool:
        """Add video with calculated priority."""
        # Calculate priority
        priority = calculate_priority(
            video_data.get('channel_slug', ''),
            video_data.get('upload_date', ''),
            video_data.get('duration', 0),
            video_data.get('score', 0)
        )
        video_data['priority'] = priority

        return self.db.add_video(video_data)

    def get_next_batch(self, limit: int = 50) -> List[Dict]:
        """Get next batch of pending videos."""
        return self.db.get_next_pending(limit)

    def mark_completed(self, video_id: str, transcript_path: str):
        """Mark video as completed."""
        self.db.update_status(video_id, 'completed', transcript_path=transcript_path)
        self.db.log_action(video_id, 'fetch_completed', f'Saved to {transcript_path}')

    def mark_failed(self, video_id: str, error_message: str):
        """Mark video as failed."""
        self.db.increment_attempts(video_id)
        self.db.update_status(video_id, 'failed', error_message=error_message)
        self.db.log_action(video_id, 'fetch_failed', error_message)

    def mark_fetching(self, video_id: str):
        """Mark video as currently fetching."""
        self.db.update_status(video_id, 'fetching')
        self.db.log_action(video_id, 'fetch_started')

    def get_stats(self) -> Dict:
        """Get queue statistics."""
        return self.db.get_stats()

    def get_priority_distribution(self) -> Dict[str, int]:
        """Get count of videos by priority."""
        import sqlite3
        with sqlite3.connect(self.db.db_path) as conn:
            cursor = conn.execute("""
                SELECT priority, COUNT(*)
                FROM video_queue
                GROUP BY priority
                ORDER BY priority
            """)
            return {row[0]: row[1] for row in cursor.fetchall()}
