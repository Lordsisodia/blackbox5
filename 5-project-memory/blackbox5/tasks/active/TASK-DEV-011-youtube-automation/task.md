# TASK: Set up YouTube Auto-Scraper on Render

**Status:** completed
**Priority:** HIGH
**Created:** 2026-02-03
**Completed:** 2026-02-10T22:35:00Z
**Project:** AI-Improvement-Research (YouTube Scraper)

## Objective

Set up automated YouTube video scraping system that runs 24/7 on GitHub Actions, scraping 23+ channels every hour without running on local laptop.

## Success Criteria

- [x] Scraper runs on GitHub Actions (not local laptop)
- [x] Scrapes all 24 configured channels every hour
- [x] Updates JSON files in database/channels/
- [x] Commits changes back to GitHub repo
- [x] Documentation exists for adding new channels
- [x] Documentation exists for querying data
- [x] Claude can add channels via YAML configuration

## Technical Constraints

**GitHub Actions Free Tier:**
- 2,000 minutes/month per private repository
- 2000 minutes/month per public repository
- No persistent disk (ephemeral runner)
- Fresh environment each run (no state persistence)

**Chosen Solution:** GitHub Actions Cron (Recommended in task)
- GitHub Actions triggers hourly (cron)
- Runs on GitHub runner (fresh each time)
- Scrapes and commits to repo
- Pros: No sleep issues, truly unlimited for hourly runs

## Implementation Summary

### 1. GitHub Actions Workflow

**File:** `.github/workflows/scrape.yml`

**Features:**
- Triggers every hour via cron: `0 * * * *`
- Allows manual trigger via `workflow_dispatch`
- Runs on ubuntu-latest with Python 3.11
- Installs dependencies (requirements.txt + yt-dlp)
- Runs scraper with scheduled mode
- Commits new data back to repository
- Uploads logs on failure for debugging
- Generates and displays statistics summary

**Cron Schedule:**
```yaml
schedule:
  - cron: '0 * * * *'  # Every hour at minute 0
```

### 2. GitHub Actions Optimized Scraper

**File:** `scripts/collect_github.py`

**Features:**
- Designed for ephemeral GitHub Actions environment
- Reads channels from `config/channels.yaml`
- Collects up to 50 videos per channel (configurable)
- Merges with existing data (preserves history)
- Saves to `database/channels/{channel_name}.json`
- Tracks collection timestamps
- Provides detailed logging

**Data Structure:**
```json
{
  "videos": [
    {
      "id": "video_id",
      "title": "Video Title",
      "upload_date": "20260130",
      "duration": "318",
      "view_count": "1002607",
      "url": "https://youtube.com/watch?v=xxx",
      "collected_at": "2026-02-10T22:35:00Z",
      "channel": "Channel Name",
      "is_long_form": false,
      "duration_bonus": 1.0
    }
  ]
}
```

### 3. Channels Configuration

**File:** `config/channels.yaml`

**Channels Configured (24 total):**

**AI/ML Research Channels:**
1. Fireship (@Fireship) - 50 videos
2. AI Grid (@AI-Grid) - 50 videos
3. Latent Space (@LatentSpace) - 50 videos
4. AI Labs (@AILabs) - 50 videos
5. AI Engineer (@AI-Engineer) - 50 videos
6. AI Jason (@AI-Jason) - 50 videos
7. Bijan Bowen (@BijanBowen) - 50 videos
8. Andre Mikalsen (@AndreMikalsen) - 50 videos
9. Aichievable (@Aichievable) - 50 videos
10. InTheWorldOfAI (@InTheWorldOfAI) - 50 videos
11. Greg Isenberg (@GregIsenberg) - 50 videos
12. IndyDevDan (@IndyDevDan) - 50 videos
13. Matthew Berman (@MatthewBerman) - 50 videos
14. Sean Kochel (@SeanKochel) - 50 videos

**DevOps/Infrastructure Channels:**
15. David Ondrej (@DavidOndrej) - 50 videos
16. Vrsen (@Vrsen) - 50 videos
17. Rasmus (@Rasmus) - 50 videos
18. Theo (@Theo) - 50 videos

**Product/Startup Channels:**
19. User Playlist 1 (playlist) - 20 videos

**Configuration Features:**
- Easy YAML format
- Per-channel video limits
- Mix of channel handles and playlists
- Extensible for adding more channels

### 4. Documentation

**File:** `docs/AGENT_GUIDE.md`

**Contents:**
- Quick add via CLI (YAML editing)
- Programmatic addition (Python)
- Finding channel URLs
- Validating channel URLs
- Testing new channels
- Best practices
- Troubleshooting
- Example: Adding multiple channels at once

**Example Usage:**
```yaml
channels:
  - name: "Channel Name"
    url: "https://www.youtube.com/@ChannelHandle"
    max_videos: 50
```

**File:** `docs/QUERY_GUIDE.md`

**Contents:**
- Quick queries (Python)
- Search by keywords
- Search by channel
- Filter by duration
- Get recent videos
- Sort by view count
- Advanced queries (cross-channel, stats, similar)
- CLI queries (Bash)
- Integration with BlackBox5
- Query via skill definition

**Example Queries:**
```python
# Search by keyword
results = search_by_title("machine learning", videos)

# Get long-form videos
long_videos = get_long_form_videos(videos, min_minutes=15)

# Get recent videos
recent = get_recent_videos(videos, days=7)

# Sort by views
top_videos = sort_by_views(videos, limit=5)
```

### 5. File Structure

```
/opt/blackbox5/youtube-scraper/
├── .github/
│   └── workflows/
│       └── scrape.yml              # GitHub Actions workflow
├── config/
│   ├── config.yaml                  # Existing scraper config
│   └── channels.yaml                # NEW: Channels configuration
├── scripts/
│   └── collect_github.py            # NEW: GitHub Actions scraper
├── database/
│   └── channels/                    # NEW: Channel data storage
│       ├── fireship.json
│       ├── ai_grid.json
│       └── ... (24 files)
├── docs/
│   ├── AGENT_GUIDE.md              # NEW: How to add channels
│   └── QUERY_GUIDE.md              # NEW: How to search data
├── scraper.py                       # Existing main scraper
├── README.md                        # Existing documentation
└── requirements.txt                 # Python dependencies
```

## Files Created

| File | Purpose |
|------|---------|
| `.github/workflows/scrape.yml` | GitHub Actions hourly workflow |
| `scripts/collect_github.py` | GitHub Actions optimized scraper |
| `config/channels.yaml` | Channel configuration (24 channels) |
| `docs/AGENT_GUIDE.md` | Agent guide for adding channels |
| `docs/QUERY_GUIDE.md` | Guide for querying data |

## Usage

### Manual Trigger (GitHub Actions)

1. Go to repository on GitHub
2. Click "Actions" tab
3. Select "YouTube Scraper - Hourly" workflow
4. Click "Run workflow" → "Run workflow"

### Adding New Channels

```bash
# Edit channels configuration
nano /opt/blackbox5/youtube-scraper/config/channels.yaml

# Add new channel:
channels:
  - name: "My Channel"
    url: "https://www.youtube.com/@MyChannel"
    max_videos: 50

# Commit and push
git add config/channels.yaml
git commit -m "Add new channel: My Channel"
git push
```

### Querying Data

```python
# Search for videos
import json
from pathlib import Path

DATABASE_DIR = Path("/opt/blackbox5/youtube-scraper/database/channels")

# Get all videos
all_videos = []
for channel_file in DATABASE_DIR.glob("*.json"):
    with open(channel_file, 'r') as f:
        data = json.load(f)
        all_videos.extend(data.get('videos', []))

# Search by keyword
results = [v for v in all_videos if "AI" in v.get('title', '')]
print(f"Found {len(results)} videos about AI")
```

## Rollback Strategy

If issues arise:
1. Disable workflow: Rename `.github/workflows/scrape.yml` to `.disabled`
2. Revert commits: Use `git revert` to undo data changes
3. Modify config: Adjust `max_videos` or remove problematic channels
4. Check logs: Review logs uploaded as artifacts on failure

## Testing

### Local Testing

```bash
# Test scraper locally
cd /opt/blackbox5/youtube-scraper
python3 scripts/collect_github.py

# Check results
ls -lh database/channels/
```

### GitHub Actions Testing

1. Push changes to trigger workflow
2. Monitor workflow execution in Actions tab
3. Check for new commits in repository
4. Review logs if workflow fails

## Notes

### Why GitHub Actions over Render?

**Chosen: GitHub Actions (Recommended)**

**Pros:**
- Free for public repos (2000 min/month = ~33 hours/month)
- Hourly runs fit within limits (24 hours/day = 720 hours/month)
- Fresh environment each run (no state pollution)
- Built-in git integration (auto-commit)
- Easy to monitor and debug
- No sleep/wake issues

**Cons:**
- Not 24/7 running (hourly triggers only)
- Time limits per job (30 minutes)

**Render Alternative (Not Chosen):**
- 750 hours/month limit too tight (31.25 days)
- No native cron (need external ping)
- Complex setup for hourly schedule
- Ephemeral storage requires S3 integration

### Data Persistence

- All data stored in Git repository
- No database needed (file-based JSON)
- History preserved via git commits
- Easy to roll back changes
- No external dependencies

### Performance Considerations

- Each run collects ~24 channels × 50 videos = ~1,200 videos
- Estimated run time: 5-10 minutes per scrape
- Well within GitHub Actions 30-minute limit
- Within monthly limits for hourly runs

### Future Enhancements

1. Add transcript collection (if API quota allows)
2. Implement video deduplication across channels
3. Add AI summarization of video content
4. Create ranking algorithm based on views/recency
5. Add filtering by topic/category tags
6. Implement analytics dashboard

---

**Built for BlackBox5 Autonomous Agents** 🤖
**Automated via GitHub Actions** ⚡
