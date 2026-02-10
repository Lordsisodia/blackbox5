# YouTube Scraper - Deployment Guide

**Created:** 2025-02-10
**Purpose:** Deploy and configure YouTube scraper for production use

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Cron Setup](#cron-setup)
5. [OpenClaw Integration](#openclaw-integration)
6. [Monitoring](#monitoring)
7. [Maintenance](#maintenance)
8. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum

- Python 3.8+
- 500 MB disk space
- Internet connection
- Linux/macOS (Windows untested but should work)

### Recommended

- Python 3.10+
- 2 GB disk space (for transcripts)
- Stable internet connection
- VPS or always-on machine for automated scraping

---

## Installation

### Step 1: Clone/Verify Location

The scraper should be at:
```
/opt/blackbox5/youtube-scraper/
```

### Step 2: Install Dependencies

```bash
cd /opt/blackbox5/youtube-scraper
pip install -r requirements.txt
```

### Step 3: Verify Installation

```bash
# Test import
python3 -c "import yt_dlp; import youtube_transcript_api; print('OK')"

# Run help
python3 scraper.py --help

# Check stats (empty initially)
python3 scraper.py --stats
```

### Step 4: Create Directories

```bash
cd /opt/blackbox5/youtube-scraper
mkdir -p data logs

# BlackBox5 memory directories
mkdir -p /opt/blackbox5/5-project-memory/youtube-scraper/knowledge/{transcripts,metadata,summaries}
```

### Step 5: Test Scraping

```bash
# Small test (3 videos)
python3 scraper.py --query "test" --max-results 3 -v
```

---

## Configuration

### Main Configuration File

Edit `/opt/blackbox5/youtube-scraper/config/config.yaml`:

```yaml
scraper:
  max_videos_per_search: 20
  enable_video_download: false
  transcript_languages:
    - en
    - auto

rate_limits:
  search_delay: 5
  metadata_delay: 1
  transcript_delay: 2
  max_retries: 5

storage:
  sqlite_db: data/scraper.db
  transcripts_dir: /opt/blackbox5/5-project-memory/youtube-scraper/knowledge/transcripts
  metadata_dir: /opt/blackbox5/5-project-memory/youtube-scraper/knowledge/metadata

queries:
  - query: "machine learning tutorial"
    max_results: 10
    schedule: "0 */6 * * *"
    enabled: true
```

### Rate Limiting

Adjust based on your needs:

- **Conservative**: Increase all delays by 2-3x
- **Aggressive**: Decrease delays (risk of blocking)
- **Recommended**: Use defaults

### Scraping Schedule

Add queries to `config.yaml` with cron schedules:

```yaml
queries:
  # Every 6 hours
  - query: "topic 1"
    schedule: "0 */6 * * *"
    enabled: true

  # Daily at 2 AM
  - query: "topic 2"
    schedule: "0 2 * * *"
    enabled: true

  # Weekly on Sunday
  - query: "topic 3"
    schedule: "0 10 * * 0"
    enabled: true
```

---

## Cron Setup

### Step 1: Edit Crontab

```bash
crontab -e
```

### Step 2: Add Cron Jobs

```bash
# YouTube Scraper - Every 6 hours
0 */6 * * * cd /opt/blackbox5/youtube-scraper && python3 scraper.py --scheduled >> logs/cron.log 2>&1

# YouTube Scraper - Daily statistics at 8 AM
0 8 * * * cd /opt/blackbox5/youtube-scraper && python3 scraper.py --stats >> logs/daily_stats.txt 2>&1

# YouTube Scraper - Weekly database backup on Sunday at 3 AM
0 3 * * 0 mkdir -p backups && cp data/scraper.db backups/scraper_$(date +\%Y\%m\%d).db
```

### Step 3: Verify Cron

```bash
# List cron jobs
crontab -l

# Check cron log
tail -f logs/cron.log
```

---

## OpenClaw Integration

### Skill Configuration

The skill is at `/opt/blackbox5/.skills/youtube-scraper.json`

It provides commands:
- `youtube-scraper scrape --query "topic"`
- `youtube-scraper video --video VIDEO_ID`
- `youtube-scraper stats`
- `youtube-scraper scheduled`

### Agent Usage

#### From Moltbot

```python
import sys
sys.path.insert(0, '/opt/blackbox5/youtube-scraper')
from scraper import YouTubeScraper

scraper = YouTubeScraper()
results = scraper.search_and_scrape("topic", max_results=5)
```

#### From OpenClaw

```python
# Hook: /opt/blackbox5/2-engine/runtime/hooks/youtube_scrape_hook.py
def on_new_goal(goal):
    if "research" in goal.get('title', '').lower():
        scraper = YouTubeScraper()
        scraper.search_and_scrape(goal['title'], max_results=5)
```

#### From ClawDBot

```python
# Log statistics
scraper = YouTubeScraper()
stats = scraper.get_stats()
clawdbot.log_activity(stats)
```

---

## Monitoring

### Check Logs

```bash
# Real-time log
tail -f logs/scraper_$(date +%Y-%m-%d).log

# Recent errors
grep ERROR logs/scraper_*.log | tail -20

# Cron log
tail -f logs/cron.log
```

### View Statistics

```bash
# Basic stats
python3 scraper.py --stats

# Detailed stats
python3 scraper.py --stats | jq '.'

# Daily stats
cat logs/daily_stats.txt
```

### Database Queries

```bash
# Connect to SQLite
sqlite3 data/scraper.db

# Run queries
sqlite> SELECT COUNT(*) FROM scraped_videos;
sqlite> SELECT channel, COUNT(*) as cnt FROM scraped_videos GROUP BY channel ORDER BY cnt DESC LIMIT 10;
sqlite> SELECT * FROM scraping_stats ORDER BY date DESC LIMIT 7;

# Exit
sqlite> .quit
```

### Monitor Disk Usage

```bash
# Check transcript directory size
du -sh /opt/blackbox5/5-project-memory/youtube-scraper/knowledge/transcripts/

# Check database size
ls -lh data/scraper.db

# Check log directory
du -sh logs/
```

---

## Maintenance

### Daily Tasks

- Check logs for errors
- Review statistics
- Verify cron jobs ran

```bash
# Quick daily check
echo "=== Statistics ==="
python3 scraper.py --stats
echo -e "\n=== Recent Errors ==="
grep ERROR logs/scraper_$(date +%Y-%m-%d).log | tail -5
```

### Weekly Tasks

- Backup database
- Clean up old logs
- Review failed videos

```bash
# Backup
cp data/scraper.db backups/scraper_$(date +%Y%m%d).db

# Clean old logs (>7 days)
find logs/ -name "*.log" -mtime +7 -delete

# Review failed
sqlite3 data/scraper.db "SELECT video_id, error_message, retry_count FROM failed_videos WHERE retry_count < 3;"
```

### Monthly Tasks

- Review scraping effectiveness
- Update queries in config
- Check disk usage
- Review and retry failed videos

```bash
# Disk usage
du -sh /opt/blackbox5/5-project-memory/youtube-scraper/knowledge/

# Update queries
nano config/config.yaml

# Retry failed videos
python3 -c "
from scraper import YouTubeScraper
s = YouTubeScraper()
failed = s.state_tracker.get_failed_videos(max_retries=3)
for f in failed:
    s.scrape_video(f['video_id'], force_rescrape=True)
    print(f'Retried: {f[\"video_id\"]}')
"
```

---

## Troubleshooting

### Problem: "No module named 'yt_dlp'"

**Solution:**
```bash
pip install yt-dlp
```

### Problem: "Too Many Requests"

**Solution:**
1. Wait 15-30 minutes
2. Increase delays in `config.yaml`
3. Check if another process is running

```bash
# Check for running scrapers
ps aux | grep scraper
```

### Problem: Database Locked

**Solution:**
```bash
# Check for processes using DB
lsof data/scraper.db

# Wait or kill if safe
kill -9 <PID>
```

### Problem: No Transcripts

**Possible causes:**
1. Video doesn't have transcripts
2. Video is age-restricted
3. Transcript API temporarily down

**Solution:**
```bash
# Check logs for specific errors
grep "No transcript found" logs/scraper_*.log
```

### Problem: Cron Not Running

**Solution:**
```bash
# Check cron service
systemctl status cron

# Check cron logs
grep CRON /var/log/syslog

# Verify crontab
crontab -l
```

### Problem: High Disk Usage

**Solution:**
```bash
# Find large files
find /opt/blackbox5/5-project-memory/youtube-scraper/knowledge/ -type f -size +10M

# Compress old transcripts
find /opt/blackbox5/5-project-memory/youtube-scraper/knowledge/transcripts/ -mtime +30 -exec gzip {} \;
```

---

## Performance Tuning

### Increase Scraping Speed

Adjust `config.yaml`:
```yaml
rate_limits:
  search_delay: 3      # Reduce from 5
  metadata_delay: 0.5  # Reduce from 1
  transcript_delay: 1  # Reduce from 2
```

**Warning**: May trigger rate limits

### Reduce Disk Usage

```yaml
scraper:
  # Don't save transcripts for all videos
  create_summary: false

  # Or compress old ones manually
  # find ... -mtime +30 -exec gzip {} \;
```

### Improve Reliability

```yaml
rate_limits:
  max_retries: 10     # Increase retries
  base_delay: 5       # Increase base delay
  jitter_percent: 50  # More random jitter
```

---

## Backup and Recovery

### Backup Script

```bash
#!/bin/bash
# backup-scraper.sh

BACKUP_DIR="/opt/blackbox5/youtube-scraper/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# Backup database
cp data/scraper.db "$BACKUP_DIR/scraper_$DATE.db"

# Backup config
cp config/config.yaml "$BACKUP_DIR/config_$DATE.yaml"

# Compress transcripts
tar -czf "$BACKUP_DIR/transcripts_$DATE.tar.gz" \
  /opt/blackbox5/5-project-memory/youtube-scraper/knowledge/

echo "Backup complete: $DATE"
```

### Recovery

```bash
# Restore database
cp backups/scraper_YYYYMMDD.db data/scraper.db

# Restore config
cp backups/config_YYYYMMDD.yaml config/config.yaml

# Restore transcripts
tar -xzf backups/transcripts_YYYYMMDD.tar.gz \
  -C /opt/blackbox5/5-project-memory/youtube-scraper/knowledge/
```

---

## Security

### API Keys

If using YouTube Data API:

```bash
# Store in secrets
echo "YOUTUBE_API_KEY=your_key_here" >> /opt/blackbox5/.secrets/youtube

# In config, reference as environment variable
# youtube_api_key: ${YOUTUBE_API_KEY}
```

### File Permissions

```bash
# Restrict config and database
chmod 600 config/config.yaml
chmod 600 data/scraper.db

# Restrict secrets directory
chmod 700 /opt/blackbox5/.secrets/
```

### Network

If running on VPS:
- Use firewall to restrict access
- Don't expose scraper ports
- Run as non-root user

---

## Upgrading

### Update Dependencies

```bash
cd /opt/blackbox5/youtube-scraper
pip install --upgrade -r requirements.txt
```

### Update Code

```bash
# Pull latest (if using git)
git pull

# Or manually update files
```

### Migrate Database

```bash
# Backup first
cp data/scraper.db backups/scraper_before_migration.db

# If schema changes, run migration script
# python3 lib/migrate.py
```

---

## Contact & Support

For issues or questions:
- Check logs: `logs/scraper_*.log`
- Review docs: `docs/`
- Check BlackBox5 documentation: `/opt/blackbox5/1-docs/`

---

**Deployment Status:** 🟢 Ready for production
**Last Updated:** 2025-02-10
