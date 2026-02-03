# Transcript Server Deployment Guide

## Overview

Dedicated server for fetching YouTube transcripts using `youtube-transcript-api` (free, no quota limits).

**Server Specs (Recommended)**:
- Hetzner CX23: 2 vCPUs, 4GB RAM, 40GB SSD
- Cost: €4.51/month
- Throughput: ~200 videos/day
- Time to complete 7,814 videos: ~39 days

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Transcript Server                         │
│                                                              │
│  ┌─────────────────┐    ┌──────────────────────────────┐   │
│  │  RSS Scraper    │    │     Transcript Worker        │   │
│  │  (every 4h)     │    │     (continuous)             │   │
│  │                 │    │                              │   │
│  │  • Check RSS    │    │  • Fetch from queue          │   │
│  │  • Add new      │    │  • Rate limit (2s delay)     │   │
│  │    videos       │    │  • Save to disk              │   │
│  └────────┬────────┘    └──────────────┬───────────────┘   │
│           │                            │                    │
│           ▼                            ▼                    │
│  ┌──────────────────────────────────────────────┐          │
│  │              SQLite Queue                     │          │
│  │           (database/queue.db)                 │          │
│  └──────────────────────────────────────────────┘          │
│                                                              │
│  Output: /opt/transcripts/content/{channel}/{video_id}.md   │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Setup

### 1. Buy Server

**Hetzner Cloud**:
1. Log into [Hetzner Cloud Console](https://console.hetzner.cloud/)
2. Create project → Add server
3. Location: Nuremberg or Falkenstein
4. Image: Ubuntu 22.04
5. Type: CX23 (4GB RAM)
6. Name: `transcript-worker`
7. Add your SSH key

**Cost**: €4.51/month (~$5 USD)

### 2. Run Setup Script

```bash
# SSH into the new server
ssh root@YOUR_SERVER_IP

# Download and run setup script
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/deploy/setup-server.sh | bash

# Or manually copy the script:
scp deploy/setup-server.sh root@YOUR_SERVER_IP:/tmp/
ssh root@YOUR_SERVER_IP "bash /tmp/setup-server.sh"
```

### 3. Copy Queue Database

```bash
# From your local machine
scp database/queue.db root@YOUR_SERVER_IP:/opt/transcripts/repo/database/
ssh root@YOUR_SERVER_IP "chown transcript:transcript /opt/transcripts/repo/database/queue.db"
```

### 4. Start Services

```bash
# Start transcript worker
sudo systemctl start transcript-worker

# Enable RSS scraper timer
sudo systemctl enable --now rss-scraper.timer

# Check status
sudo systemctl status transcript-worker
sudo systemctl status rss-scraper.timer
```

---

## Monitoring

### View Logs

```bash
# Transcript worker logs
sudo journalctl -u transcript-worker -f

# RSS scraper logs
sudo journalctl -u rss-scraper -f

# All logs
sudo journalctl -u transcript-worker -u rss-scraper --since "1 hour ago"
```

### Check Queue Status

```bash
cd /opt/transcripts/repo
sudo -u transcript venv/bin/python -c "
from scripts.queue.manager import QueueManager
m = QueueManager()
print(m.get_stats())
print(m.get_priority_distribution())
"
```

### Resource Usage

```bash
# CPU/Memory
htop

# Disk usage
df -h /opt/transcripts

# Network (if needed)
iftop
```

---

## File Structure

```
/opt/transcripts/
├── content/                    # Transcript output
│   ├── david_ondrej/
│   │   ├── abc123.md
│   │   └── def456.md
│   ├── vrsen/
│   └── ...
├── state/                      # Worker state
│   ├── rate_limiter.json       # Daily quota tracking
│   └── worker.log             # (optional)
└── repo/                       # Git repository
    ├── scripts/
    │   ├── worker/
    │   │   ├── worker.py
    │   │   ├── transcript_fetcher.py
    │   │   └── rate_limiter.py
    │   └── queue/
    │       ├── manager.py
    │       └── database.py
    ├── database/
    │   └── queue.db
    └── venv/                   # Python environment
```

---

## Configuration

### Adjust Rate Limits

Edit `/etc/systemd/system/transcript-worker.service`:

```ini
ExecStart=/opt/transcripts/repo/venv/bin/python scripts/worker/worker.py \
    --daily-limit 300 \      # Increase to 300/day
    --request-delay 1.5 \    # Faster (1.5s between requests)
    --batch-size 20 \        # Larger batches
    --continuous
```

Then reload:
```bash
sudo systemctl daemon-reload
sudo systemctl restart transcript-worker
```

### RSS Scraper Frequency

Edit `/etc/systemd/system/rss-scraper.timer`:

```ini
[Timer]
OnBootSec=5min
OnUnitActiveSec=2h    # Change from 4h to 2h
```

---

## Backup Strategy

### Automated Backup Script

Create `/opt/transcripts/backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/opt/transcripts/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# Backup queue database
cp /opt/transcripts/repo/database/queue.db "$BACKUP_DIR/queue_$DATE.db"

# Sync transcripts to S3 (optional)
# aws s3 sync /opt/transcripts/content/ s3://your-bucket/transcripts/

# Keep only last 7 backups
ls -t "$BACKUP_DIR"/queue_*.db | tail -n +8 | xargs -r rm
```

Add to crontab:
```bash
0 2 * * * /opt/transcripts/backup.sh
```

---

## Troubleshooting

### Worker Not Starting

```bash
# Check for errors
sudo journalctl -u transcript-worker --no-pager | tail -50

# Check Python environment
sudo -u transcript /opt/transcripts/repo/venv/bin/python --version

# Test manually
sudo -u transcript bash
cd /opt/transcripts/repo
PYTHONPATH=scripts venv/bin/python scripts/worker/worker.py --limit 1
```

### Rate Limit Hit Too Fast

```bash
# Check current rate limiter state
cat /opt/transcripts/state/rate_limiter.json

# Reset if needed
sudo -u transcript rm /opt/transcripts/state/rate_limiter.json
sudo systemctl restart transcript-worker
```

### Queue Database Locked

```bash
# Check for locks
sudo lsof /opt/transcripts/repo/database/queue.db

# Restart worker (will release lock)
sudo systemctl restart transcript-worker
```

### Disk Space Full

```bash
# Check usage
du -sh /opt/transcripts/content/* | sort -hr | head -20

# Clean old logs
sudo journalctl --vacuum-time=7d

# Archive old transcripts (optional)
tar czf /opt/transcripts/archive_$(date +%Y%m).tar.gz /opt/transcripts/content/
```

---

## Security

### Firewall (UFW)

```bash
# Allow SSH only
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw enable
```

### SSH Hardening

Edit `/etc/ssh/sshd_config`:

```
PermitRootLogin no
PasswordAuthentication no
MaxAuthTries 3
```

```bash
systemctl restart sshd
```

---

## Migration from GitHub Actions

If you started with GitHub Actions and want to migrate:

1. **Stop GitHub Actions workflow**
   - Disable the `fetch-transcripts.yml` workflow

2. **Copy existing transcripts**
   ```bash
   # From GitHub repo to server
   rsync -avz content/transcripts/ root@SERVER_IP:/opt/transcripts/content/
   ```

3. **Update queue status**
   ```bash
   # Mark already-fetched videos as completed
   sudo -u transcript venv/bin/python scripts/queue/sync_existing.py
   ```

---

## Cost Analysis

| Option | Monthly Cost | Throughput | Pros | Cons |
|--------|-------------|------------|------|------|
| **Hetzner CX23** | €4.51 | 200/day | Cheap, dedicated, no limits | 39 days to complete |
| **GitHub Actions** | $0 (within limits) | 50/day | Free, integrated | 2000 min/month limit, slower |
| **AWS EC2 t3.micro** | ~$8.50 | 200/day | Scalable | More expensive |
| **Google Cloud e2-micro** | ~$6 | 150/day | Free tier available | Lower throughput |

**Recommendation**: Hetzner CX23 is the best value for this workload.

---

## Next Steps

1. **Buy the server** (Hetzner CX23)
2. **Run setup script**
3. **Copy queue.db**
4. **Start services**
5. **Monitor for 24h** to ensure stability
6. **Set up backups** (optional but recommended)

Once transcripts are flowing, you can build the AI analysis pipeline on top.
