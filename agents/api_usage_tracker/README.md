# API Usage Tracker

## Purpose
Tracks token usage, rate limits, and costs across all API providers for BlackBox5.

## Features
- Real-time usage tracking per provider
- Rate limit monitoring and alerts
- Cost estimation and budget tracking
- Health monitoring per API key
- Automatic key rotation triggers
- Usage reports and recommendations

## Database Schema
```sql
CREATE TABLE api_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    provider TEXT NOT NULL,
    agent TEXT,
    task_type TEXT,
    tokens_used INTEGER,
    request_duration_ms INTEGER,
    success BOOLEAN,
    error_message TEXT
)
```

## Usage
```python
from agents.api_usage_tracker import APIUsageTracker

tracker = APIUsageTracker()

# Track an API call
tracker.track_usage(
    provider="kimi",
    agent="main",
    task_type="coding",
    tokens_used=5000,
    duration_ms=1234,
    success=True
)

# Get statistics
stats = tracker.get_stats(days=7)
print(stats)
```
