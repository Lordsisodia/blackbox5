# YouTube Scraper - Quick Start Guide

**Created:** 2025-02-10
**Purpose:** Get started with YouTube scraper in 5 minutes

---

## Installation (1 minute)

```bash
cd /opt/blackbox5/youtube-scraper
pip install -r requirements.txt
```

That's it! The scraper is ready.

---

## Your First Scrape (2 minutes)

### Option 1: Command Line

```bash
# Search and scrape 5 videos about machine learning
python3 scraper.py --query "machine learning tutorial" --max-results 5

# View verbose output
python3 scraper.py --query "AI agents" -v
```

### Option 2: Python API

```python
from scraper import YouTubeScraper

scraper = YouTubeScraper()
results = scraper.search_and_scrape("AI tutorial", max_results=3)

print(f"Scraped {len(results)} videos")
for video in results:
    print(f"- {video['title']}")
```

---

## Check Results (30 seconds)

```bash
# View statistics
python3 scraper.py --stats

# List recent transcripts
ls -lh /opt/blackbox5/5-project-memory/youtube-scraper/knowledge/transcripts/

# View a transcript
cat /opt/blackbox5/5-project-memory/youtube-scraper/knowledge/transcripts/*.md | head -50
```

---

## Schedule Automatic Scraping (2 minutes)

### Edit Config

```bash
nano /opt/blackbox5/youtube-scraper/config/config.yaml
```

Add your queries:

```yaml
queries:
  - query: "your topic here"
    max_results: 10
    schedule: "0 */6 * * *"  # Every 6 hours
    enabled: true
```

### Add to Cron

```bash
crontab -e

# Add this line (scrape every 6 hours)
0 */6 * * * cd /opt/blackbox5/youtube-scraper && python3 scraper.py --scheduled >> logs/cron.log 2>&1
```

---

## Use from BlackBox5 Agents (1 minute)

### Moltbot / OpenClaw

```python
import sys
sys.path.insert(0, '/opt/blackbox5/youtube-scraper')
from scraper import YouTubeScraper

# Autonomous research
scraper = YouTubeScraper()
videos = scraper.search_and_scrape("topic I'm researching", max_results=5)

# Videos are now in BlackBox5 knowledge base!
# Transcripts are in:
# /opt/blackbox5/5-project-memory/youtube-scraper/knowledge/transcripts/
```

### Via OpenClaw Skill

```bash
# From any agent that can use OpenClaw skills
youtube-scraper scrape --query "your topic" --max-results 10
```

---

## Common Tasks

### Scrape a Specific Video

```bash
python3 scraper.py --video dQw4w9WgXcQ
```

### Force Re-scrape

```bash
python3 scraper.py --query "topic" --force
```

### Run All Scheduled Queries

```bash
python3 scraper.py --scheduled
```

### View Detailed Statistics

```bash
python3 scraper.py --stats
```

---

## Troubleshooting

### "No module named 'yt_dlp'"

```bash
pip install yt-dlp
```

### "No transcripts found"

- Not all videos have transcripts
- Check if video is age-restricted (needs cookies)
- Try different video

### "Too Many Requests"

- Wait a few minutes
- Increase `search_delay` in config.yaml
- Reduce `max_results`

### Database Locked

```bash
# Check for running processes
ps aux | grep scraper

# Wait or kill if needed
```

---

## Where Data Goes

```
/opt/blackbox5/5-project-memory/youtube-scraper/
├── knowledge/
│   ├── transcripts/     # Video transcripts (.md)
│   ├── metadata/        # Video metadata (.json)
│   └── summaries/       # Quick summaries
├── data/
│   └── scraper.db       # SQLite database (state)
└── logs/                # Scraper logs
```

---

## Next Steps

1. **Customize config**: Edit `config/config.yaml` for your needs
2. **Add cron jobs**: Schedule periodic scraping
3. **Integrate with agents**: Use from Moltbot, OpenClaw, etc.
4. **Monitor stats**: Check regularly with `--stats`
5. **Read docs**: See `docs/RESEARCH.md` and `docs/ARCHITECTURE.md`

---

**Need Help?**

- Check logs: `tail -f logs/scraper_*.log`
- Read README: `cat README.md`
- See architecture: `cat docs/ARCHITECTURE.md`

---

**Happy Scraping!** 🎬
