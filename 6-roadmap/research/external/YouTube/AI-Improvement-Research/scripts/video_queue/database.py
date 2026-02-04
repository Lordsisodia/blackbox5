"""
Queue Database Operations

Handles all SQLite database operations for the transcript queue.
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class QueueDatabase:
    """Manages the transcript queue database."""

    def __init__(self, db_path: Optional[Path] = None):
        """Initialize database connection."""
        if db_path is None:
            base_dir = Path(__file__).parent.parent.parent
            db_path = base_dir / 'database' / 'queue.db'

        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initialize database schema."""
        schema_path = Path(__file__).parent.parent.parent / 'database' / 'schema' / 'queue_schema.sql'

        with sqlite3.connect(self.db_path) as conn:
            if schema_path.exists():
                with open(schema_path, 'r') as f:
                    conn.executescript(f.read())
            conn.commit()

    def add_video(self, video_data: Dict) -> bool:
        """Add a video to the queue."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR IGNORE INTO video_queue
                    (video_id, channel_slug, channel_name, title, upload_date, duration, score, priority)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    video_data['video_id'],
                    video_data['channel_slug'],
                    video_data.get('channel_name', ''),
                    video_data['title'],
                    video_data.get('upload_date'),
                    video_data.get('duration', 0),
                    video_data.get('score', 0),
                    video_data.get('priority', 'P3')
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error adding video {video_data.get('video_id')}: {e}")
            return False

    def get_next_pending(self, limit: int = 1) -> List[Dict]:
        """Get next pending videos ordered by priority and score."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM video_queue
                WHERE status = 'pending' AND attempts < 3
                ORDER BY
                    CASE priority
                        WHEN 'P0' THEN 1
                        WHEN 'P1' THEN 2
                        WHEN 'P2' THEN 3
                        WHEN 'P3' THEN 4
                    END,
                    score DESC,
                    created_at ASC
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def update_status(self, video_id: str, status: str, error_message: str = None, transcript_path: str = None):
        """Update video status."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE video_queue
                SET status = ?,
                    error_message = ?,
                    transcript_path = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE video_id = ?
            """, (status, error_message, transcript_path, video_id))
            conn.commit()

    def increment_attempts(self, video_id: str):
        """Increment attempt counter."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE video_queue
                SET attempts = attempts + 1,
                    updated_at = CURRENT_TIMESTAMP
                WHERE video_id = ?
            """, (video_id,))
            conn.commit()

    def get_stats(self) -> Dict:
        """Get queue statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                    SUM(CASE WHEN status = 'fetching' THEN 1 ELSE 0 END) as fetching,
                    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed
                FROM video_queue
            """)
            row = cursor.fetchone()
            return {
                'total': row[0] or 0,
                'completed': row[1] or 0,
                'pending': row[2] or 0,
                'fetching': row[3] or 0,
                'failed': row[4] or 0,
            }

    def get_channel_stats(self) -> List[Dict]:
        """Get stats grouped by channel."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT
                    channel_slug,
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed
                FROM video_queue
                GROUP BY channel_slug
                ORDER BY total DESC
            """)
            return [
                {
                    'channel': row[0],
                    'total': row[1],
                    'completed': row[2],
                    'pending': row[1] - row[2]
                }
                for row in cursor.fetchall()
            ]

    def log_action(self, video_id: str, action: str, message: str = ''):
        """Log an action for debugging."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO queue_log (video_id, action, message)
                VALUES (?, ?, ?)
            """, (video_id, action, message))
            conn.commit()

    def video_exists(self, video_id: str) -> bool:
        """Check if video is already in queue."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT 1 FROM video_queue WHERE video_id = ?",
                (video_id,)
            )
            return cursor.fetchone() is not None
