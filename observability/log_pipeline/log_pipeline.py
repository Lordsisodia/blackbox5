#!/usr/bin/env python3
"""
Log Aggregation Pipeline for BlackBox5 Observability System.

Collects, parses, indexes, and serves logs from all agents.
Supports real-time streaming and historical queries.
"""

import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import sys

# Parent imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "bin" / "lib"))

from health_monitor.database import _get_connection

try:
    import redis
except ImportError:
    redis = None
    logging.warning("Redis not available - log streaming disabled")

logger = logging.getLogger(__name__)


class LogLevel(Enum):
    """Log levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogSource(Enum):
    """Log sources."""
    AGENT = "agent"
    SYSTEM = "system"
    API = "api"
    CRON = "cron"
    UNKNOWN = "unknown"


@dataclass
class LogEntry:
    """Represents a single log entry."""
    timestamp: datetime
    level: LogLevel
    source: LogSource
    agent: Optional[str]
    message: str
    metadata: Dict = field(default_factory=dict)
    request_id: Optional[str] = None
    task_id: Optional[str] = None
    error: Optional[Dict] = None
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "level": self.level.value,
            "source": self.source.value,
            "agent": self.agent,
            "message": self.message,
            "metadata": self.metadata,
            "request_id": self.request_id,
            "task_id": self.task_id,
            "error": self.error,
            "tags": self.tags,
        }


class LogParser:
    """Parse log entries from various formats."""

    # Regex patterns for different log formats
    PATTERNS = [
        # Standard format: [TIMESTAMP] LEVEL AGENT: MESSAGE
        re.compile(r'^\[(\d{4}-\d{2}-\d{2}T?\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?)\]\s+(\w+)\s+(\w+):\s*(.+)$'),
        # Simple format: TIMESTAMP LEVEL: MESSAGE
        re.compile(r'^(\d{4}-\d{2}-\d{2}T?\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?)\s+(\w+):\s*(.+)$'),
        # Agent format: AGENT [TIMESTAMP] LEVEL: MESSAGE
        re.compile(r'^(\w+)\s+\[(\d{4}-\d{2}-\d{2}T?\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?)\]\s+(\w+):\s*(.+)$'),
    ]

    @classmethod
    def parse(cls, raw_log: str, default_agent: Optional[str] = None) -> Optional[LogEntry]:
        """Parse a raw log string into a LogEntry."""
        for pattern in cls.PATTERNS:
            match = pattern.match(raw_log)
            if match:
                groups = match.groups()

                # Determine format based on number of groups
                if len(groups) == 4:
                    # [TIMESTAMP] LEVEL AGENT: MESSAGE
                    timestamp_str, level_str, agent, message = groups
                elif len(groups) == 3:
                    if re.match(r'^\w+$', groups[0]):
                        # AGENT [TIMESTAMP] LEVEL: MESSAGE
                        agent, timestamp_str, level_str, message = groups
                    else:
                        # TIMESTAMP LEVEL: MESSAGE
                        timestamp_str, level_str, message = groups
                        agent = default_agent
                else:
                    continue

                # Parse timestamp
                try:
                    if 'Z' in timestamp_str or '+' in timestamp_str:
                        timestamp = datetime.fromisoformat(timestamp_str)
                    else:
                        timestamp = datetime.fromisoformat(timestamp_str + 'Z')
                except ValueError:
                    timestamp = datetime.now()

                # Parse level
                try:
                    level = LogLevel(level_str.upper())
                except ValueError:
                    level = LogLevel.INFO

                # Determine source
                source = LogSource.AGENT if agent else LogSource.SYSTEM

                # Extract metadata from message
                metadata, cleaned_message = cls._extract_metadata(message)

                # Extract tags
                tags = re.findall(r'#(\w+)', message)

                return LogEntry(
                    timestamp=timestamp,
                    level=level,
                    source=source,
                    agent=agent,
                    message=cleaned_message,
                    metadata=metadata,
                    tags=tags,
                )

        # No pattern matched - create basic entry
        return LogEntry(
            timestamp=datetime.now(),
            level=LogLevel.INFO,
            source=LogSource.UNKNOWN,
            agent=default_agent,
            message=raw_log.strip(),
        )

    @staticmethod
    def _extract_metadata(message: str) -> Tuple[Dict, str]:
        """Extract key=value pairs from message."""
        metadata = {}
        cleaned = message

        # Find key=value pairs
        pattern = r'(\w+)=([^\s]+)'
        for match in re.finditer(pattern, message):
            key, value = match.groups()
            metadata[key] = value

        # Remove metadata from message
        cleaned = re.sub(pattern, '', cleaned).strip()

        return metadata, cleaned


class LogPipeline:
    """Main log aggregation pipeline."""

    def __init__(
        self,
        redis_host: str = "77.42.66.40",
        redis_port: int = 6379,
        redis_password: Optional[str] = None,
    ):
        """Initialize log pipeline."""
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_password = redis_password

        self._redis_client: Optional[redis.Redis] = None
        self._init_database()

    def _init_database(self):
        """Initialize log tables."""
        with _get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp INTEGER NOT NULL,
                    level TEXT NOT NULL,
                    source TEXT NOT NULL,
                    agent TEXT,
                    message TEXT NOT NULL,
                    metadata TEXT,
                    request_id TEXT,
                    task_id TEXT,
                    error TEXT,
                    tags TEXT,
                    INDEX idx_timestamp (timestamp),
                    INDEX idx_level (level),
                    INDEX idx_source (source),
                    INDEX idx_agent (agent),
                    INDEX idx_request_id (request_id),
                    INDEX idx_task_id (task_id),
                    INDEX idx_tags (tags)
                )
            """)

            conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS logs_fts USING fts5(
                    message, metadata, content='logs', content_rowid='id'
                )
            """)

            conn.commit()

        logger.info("Log pipeline database initialized")

    def _get_redis(self) -> Optional[redis.Redis]:
        """Get Redis client."""
        if redis is None:
            return None

        if self._redis_client is None:
            try:
                self._redis_client = redis.Redis(
                    host=self.redis_host,
                    port=self.redis_port,
                    password=self.redis_password,
                    decode_responses=True,
                )
                # Test connection
                self._redis_client.ping()
                logger.info(f"Connected to Redis at {self.redis_host}:{self.redis_port}")
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {e}")
                self._redis_client = None

        return self._redis_client

    def ingest_log(self, log: LogEntry) -> None:
        """Ingest a log entry into the database."""
        with _get_connection() as conn:
            conn.execute("""
                INSERT INTO logs
                (timestamp, level, source, agent, message, metadata, request_id, task_id, error, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                int(log.timestamp.timestamp()),
                log.level.value,
                log.source.value,
                log.agent,
                log.message,
                json.dumps(log.metadata) if log.metadata else None,
                log.request_id,
                log.task_id,
                json.dumps(log.error) if log.error else None,
                json.dumps(log.tags) if log.tags else None,
            ))
            conn.commit()

    def ingest_raw(self, raw_log: str, agent: Optional[str] = None) -> Optional[LogEntry]:
        """Parse and ingest a raw log string."""
        log = LogParser.parse(raw_log, default_agent=agent)
        if log:
            self.ingest_log(log)
        return log

    def ingest_from_redis_stream(
        self,
        stream_name: str,
        batch_size: int = 100,
        auto_ack: bool = False,
    ) -> int:
        """Read logs from a Redis stream."""
        redis_client = self._get_redis()
        if not redis_client:
            logger.warning("Redis not available - skipping stream ingestion")
            return 0

        count = 0
        try:
            # Read entries from stream
            entries = redis_client.xread(
                {stream_name: '0'},
                count=batch_size,
                block=1000,  # 1 second timeout
            )

            for stream, messages in entries:
                for message_id, data in messages:
                    # Parse log entry
                    raw_log = data.get(b'message', data.get('log', b'')).decode('utf-8')
                    agent = data.get(b'agent', b'').decode('utf-8')

                    log = self.ingest_raw(raw_log, agent)
                    if log:
                        count += 1

                    # Acknowledge if enabled
                    if auto_ack:
                        redis_client.xack(stream_name, 'observability', message_id)

        except Exception as e:
            logger.error(f"Error reading from Redis stream {stream_name}: {e}")

        return count

    def search_logs(
        self,
        query: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        level: Optional[LogLevel] = None,
        agent: Optional[str] = None,
        source: Optional[LogSource] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[LogEntry]:
        """Search logs with filters."""
        conditions = []
        params = []

        if start_date:
            conditions.append("timestamp >= ?")
            params.append(int(start_date.timestamp()))

        if end_date:
            conditions.append("timestamp <= ?")
            params.append(int(end_date.timestamp()))

        if level:
            conditions.append("level = ?")
            params.append(level.value)

        if agent:
            conditions.append("agent = ?")
            params.append(agent)

        if source:
            conditions.append("source = ?")
            params.append(source.value)

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        logs = []
        with _get_connection() as conn:
            rows = conn.execute(f"""
                SELECT * FROM logs
                WHERE {where_clause}
                ORDER BY timestamp DESC
                LIMIT ? OFFSET ?
            """, params + [limit, offset]).fetchall()

            for row in rows:
                logs.append(LogEntry(
                    timestamp=datetime.fromtimestamp(row[1]),
                    level=LogLevel(row[2]),
                    source=LogSource(row[3]),
                    agent=row[4],
                    message=row[5],
                    metadata=json.loads(row[6]) if row[6] else {},
                    request_id=row[7],
                    task_id=row[8],
                    error=json.loads(row[9]) if row[9] else None,
                    tags=json.loads(row[10]) if row[10] else [],
                ))

        # Full-text search if query provided
        if query and query.strip():
            with _get_connection() as conn:
                fts_rows = conn.execute("""
                    SELECT * FROM logs
                    WHERE id IN (
                        SELECT rowid FROM logs_fts
                        WHERE logs_fts MATCH ?
                    )
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (query, limit)).fetchall()

                fts_logs = []
                for row in fts_rows:
                    fts_logs.append(LogEntry(
                        timestamp=datetime.fromtimestamp(row[1]),
                        level=LogLevel(row[2]),
                        source=LogSource(row[3]),
                        agent=row[4],
                        message=row[5],
                        metadata=json.loads(row[6]) if row[6] else {},
                        request_id=row[7],
                        task_id=row[8],
                        error=json.loads(row[9]) if row[9] else None,
                        tags=json.loads(row[10]) if row[10] else [],
                    ))

                # Combine results, removing duplicates
                seen_ids = {log.id for log in logs}  # type: ignore
                for log in fts_logs:
                    if log.id not in seen_ids:  # type: ignore
                        logs.append(log)

        return logs[:limit]

    def get_logs_by_agent(
        self,
        agent: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        level: Optional[LogLevel] = None,
        limit: int = 100,
    ) -> List[LogEntry]:
        """Get logs for a specific agent."""
        return self.search_logs(
            query="",
            start_date=start_date,
            end_date=end_date,
            level=level,
            agent=agent,
            limit=limit,
        )

    def get_logs_by_task(
        self,
        task_id: str,
        limit: int = 100,
    ) -> List[LogEntry]:
        """Get logs for a specific task."""
        with _get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM logs
                WHERE task_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (task_id, limit)).fetchall()

        logs = []
        for row in rows:
            logs.append(LogEntry(
                timestamp=datetime.fromtimestamp(row[1]),
                level=LogLevel(row[2]),
                source=LogSource(row[3]),
                agent=row[4],
                message=row[5],
                metadata=json.loads(row[6]) if row[6] else {},
                request_id=row[7],
                task_id=row[8],
                error=json.loads(row[9]) if row[9] else None,
                tags=json.loads(row[10]) if row[10] else [],
            ))

        return logs

    def get_log_stats(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict:
        """Get log statistics."""
        conditions = []
        params = []

        if start_date:
            conditions.append("timestamp >= ?")
            params.append(int(start_date.timestamp()))

        if end_date:
            conditions.append("timestamp <= ?")
            params.append(int(end_date.timestamp()))

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        stats = {}
        with _get_connection() as conn:
            # Total count
            row = conn.execute(f"""
                SELECT COUNT(*) as total FROM logs WHERE {where_clause}
            """, params).fetchone()
            stats["total"] = row[0]

            # By level
            by_level = {}
            for row in conn.execute(f"""
                SELECT level, COUNT(*) as count
                FROM logs
                WHERE {where_clause}
                GROUP BY level
            """, params).fetchall():
                by_level[row[0]] = row[1]
            stats["by_level"] = by_level

            # By agent
            by_agent = {}
            for row in conn.execute(f"""
                SELECT agent, COUNT(*) as count
                FROM logs
                WHERE {where_clause}
                GROUP BY agent
            """, params).fetchall():
                by_agent[row[0]] = row[1]
            stats["by_agent"] = by_agent

            # By source
            by_source = {}
            for row in conn.execute(f"""
                SELECT source, COUNT(*) as count
                FROM logs
                WHERE {where_clause}
                GROUP BY source
            """, params).fetchall():
                by_source[row[0]] = row[1]
            stats["by_source"] = by_source

            # Error rate
            row = conn.execute(f"""
                SELECT
                    COUNT(*) as total,
                    SUM(CASE WHEN level IN ('ERROR', 'CRITICAL') THEN 1 ELSE 0 END) as errors
                FROM logs
                WHERE {where_clause}
            """, params).fetchone()
            total, errors = row
            stats["error_rate"] = errors / total if total > 0 else 0.0

        return stats

    def cleanup_old_logs(self, days: int = 30) -> int:
        """Delete logs older than specified days."""
        cutoff = int((datetime.now() - timedelta(days=days)).timestamp())

        with _get_connection() as conn:
            cursor = conn.execute("""
                DELETE FROM logs
                WHERE timestamp < ?
            """, (cutoff,))
            deleted = cursor.rowcount
            conn.commit()

        logger.info(f"Deleted {deleted} logs older than {days} days")
        return deleted


def main():
    """CLI for log pipeline."""
    import argparse

    parser = argparse.ArgumentParser(description="BlackBox5 Log Pipeline")
    parser.add_argument("--search", type=str, help="Search query")
    parser.add_argument("--agent", type=str, help="Filter by agent")
    parser.add_argument("--level", type=str, help="Filter by level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
    parser.add_argument("--task", type=str, help="Filter by task ID")
    parser.add_argument("--since", type=int, default=24, help="Hours to look back")
    parser.add_argument("--limit", type=int, default=100, help="Max results")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    parser.add_argument("--cleanup", type=int, help="Delete logs older than N days")

    args = parser.parse_args()

    pipeline = LogPipeline()

    if args.cleanup:
        deleted = pipeline.cleanup_old_logs(args.cleanup)
        print(f"Deleted {deleted} old logs")
        return

    if args.stats:
        start_date = datetime.now() - timedelta(hours=args.since)
        stats = pipeline.get_log_stats(start_date=start_date)

        print("📊 Log Statistics")
        print("=" * 50)
        print(f"  Total logs: {stats['total']:,}")
        print(f"  Error rate: {stats['error_rate']:.1%}")
        print()
        print("  By Level:")
        for level, count in sorted(stats['by_level'].items(), key=lambda x: x[1], reverse=True):
            print(f"    {level}: {count:,}")
        print()
        print("  By Agent:")
        for agent, count in sorted(stats['by_agent'].items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"    {agent}: {count:,}")
        return

    if args.task:
        logs = pipeline.get_logs_by_task(args.task, limit=args.limit)
        print(f"📋 Logs for task {args.task}")
    elif args.search:
        start_date = datetime.now() - timedelta(hours=args.since)
        logs = pipeline.search_logs(
            query=args.search,
            start_date=start_date,
            agent=args.agent,
            level=LogLevel(args.level.upper()) if args.level else None,
            limit=args.limit,
        )
        print(f"🔍 Search results for: {args.search}")
    else:
        start_date = datetime.now() - timedelta(hours=args.since)
        logs = pipeline.search_logs(
            query="",
            start_date=start_date,
            agent=args.agent,
            level=LogLevel(args.level.upper()) if args.level else None,
            limit=args.limit,
        )
        print(f"📝 Recent logs (last {args.since}h)")

    print("=" * 80)
    for log in logs:
        level_emoji = {
            "DEBUG": "🔍",
            "INFO": "ℹ️",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "CRITICAL": "🚨",
        }.get(log.level.value, "📝")

        print(f"{level_emoji} [{log.timestamp.isoformat()}] {log.level.value} {log.agent or 'SYSTEM'}: {log.message}")
        if log.metadata:
            print(f"   {json.dumps(log.metadata)}")


if __name__ == "__main__":
    main()
