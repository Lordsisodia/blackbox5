-- Transcript Queue Database Schema
-- SQLite database for tracking transcript fetching status

-- Main queue table
CREATE TABLE IF NOT EXISTS video_queue (
    video_id TEXT PRIMARY KEY,
    channel_slug TEXT NOT NULL,
    channel_name TEXT,
    title TEXT NOT NULL,
    upload_date TEXT,
    duration INTEGER,
    score REAL DEFAULT 0,
    priority TEXT DEFAULT 'P3',  -- P0 (critical), P1 (high), P2 (medium), P3 (low)
    status TEXT DEFAULT 'pending',  -- pending, fetching, completed, failed
    attempts INTEGER DEFAULT 0,
    error_message TEXT,
    transcript_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for efficient queries
CREATE INDEX IF NOT EXISTS idx_status_priority ON video_queue(status, priority, score DESC);
CREATE INDEX IF NOT EXISTS idx_channel ON video_queue(channel_slug);
CREATE INDEX IF NOT EXISTS idx_upload_date ON video_queue(upload_date);
CREATE INDEX IF NOT EXISTS idx_status_attempts ON video_queue(status, attempts);

-- Stats table for tracking progress
CREATE TABLE IF NOT EXISTS queue_stats (
    date TEXT PRIMARY KEY,
    total_videos INTEGER DEFAULT 0,
    completed INTEGER DEFAULT 0,
    pending INTEGER DEFAULT 0,
    failed INTEGER DEFAULT 0,
    fetched_today INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Log table for debugging
CREATE TABLE IF NOT EXISTS queue_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id TEXT,
    action TEXT,  -- fetch_started, fetch_completed, fetch_failed
    message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
