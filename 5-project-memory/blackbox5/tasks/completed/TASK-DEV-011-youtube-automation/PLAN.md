# PLAN.md: YouTube Auto-Scraper on Render

**Task:** TASK-DEV-011-youtube-automation - YouTube Auto-Scraper
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 1-2 days
**Importance:** 80 (High)

---

## 1. First Principles Analysis

### Why Automate YouTube Scraping?

1. **Continuous Learning**: AI improvement research requires up-to-date content from 23+ channels
2. **Scale**: Manual scraping of 23 channels hourly is impossible
3. **Consistency**: Automated system ensures regular, reliable data collection
4. **Resource Efficiency**: Runs on Render free tier instead of local laptop

### What Happens Without Automation?

- **Stale Data**: Videos become outdated, missing latest insights
- **Local Resource Drain**: Laptop must stay running, consuming power and bandwidth
- **Inconsistent Collection**: Manual runs lead to gaps in data
- **Limited Scale**: Cannot monitor all 23 channels effectively

### How Should the System Work?

1. **GitHub Actions Cron**: Trigger hourly workflow (recommended approach)
2. **Scrape & Store**: Collect videos from all configured channels
3. **Commit & Push**: Store data in JSON format, commit to repository
4. **Easy Extension**: Simple CLI to add new channels
5. **Query Support**: Documentation for data access patterns

---

## 2. Current State Assessment

### Existing Infrastructure

| Component | Location | Status |
|-----------|----------|--------|
| Channel Data | `database/channels/*.json` | 7,219 videos from 11 channels |
| Scraper Script | `collect_channel_optimized.py` | Works locally |
| Config | `config/sources.yaml` | 23 channels configured |
| Data Size | ~3.5MB | Manageable for Git |

### Current Limitations

1. **Local Only**: Scripts only run on local machine
2. **Manual Execution**: Must be triggered manually
3. **No Automation**: No scheduled runs
4. **No Documentation**: No guide for adding channels or querying data

### Render Free Tier Constraints

| Constraint | Limit | Impact |
|------------|-------|--------|
| Hours/Month | 750 (31.25 days) | Tight but workable |
| Persistent Disk | None (ephemeral only) | Must store data externally |
| Cron Jobs | Not native | Need GitHub Actions workaround |
| RAM | 512MB | Sufficient for scraping |
| CPU | Shared | Acceptable for hourly runs |

---

## 3. Proposed Solution

### Architecture: GitHub Actions Cron (Recommended)

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  GitHub Actions │────▶│  Scrape Script   │────▶│  YouTube API    │
│  (Cron: hourly) │     │  (Python)        │     │  (Data Source)  │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌──────────────────┐
                        │  Update JSON     │
                        │  Files           │
                        └──────────────────┘
                               │
                               ▼
                        ┌──────────────────┐
                        │  Commit & Push   │
                        │  to GitHub       │
                        └──────────────────┘
```

### Why GitHub Actions Over Render?

| Factor | GitHub Actions | Render |
|--------|----------------|--------|
| Cron Support | Native | Requires external ping |
| Runtime | Fresh each time | Must stay running |
| Hours Limit | Unlimited (for public repos) | 750/month |
| Complexity | Simple | Requires web service + ping |
| Reliability | High | Sleep/wake issues |

### Workflow Design

**GitHub Actions Workflow (`.github/workflows/scrape.yml`):**
```yaml
name: YouTube Scraper
on:
  schedule:
    - cron: '0 * * * *'  # Every hour
  workflow_dispatch:  # Manual trigger

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: python scripts/collect_github.py
      - run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add database/channels/
          git diff --staged --quiet || git commit -m "Update channel data [$(date)]"
          git push
```

---

## 4. Implementation Plan

### Phase 1: Create GitHub-Optimized Scraper (Day 1)

**File:** `scripts/collect_github.py`

**Features:**
- Read channel list from `config/sources.yaml`
- Scrape all 23 channels
- Update existing JSON files (merge, don't overwrite)
- Handle API rate limits gracefully
- Exit codes for workflow success/failure
- Minimal output (GitHub Actions friendly)

**Implementation Details:**
```python
#!/usr/bin/env python3
"""GitHub Actions optimized YouTube scraper."""
import json
import os
import sys
from pathlib import Path
import yaml

# Configuration
CONFIG_PATH = Path("config/sources.yaml")
DATABASE_DIR = Path("database/channels")

def load_channels():
    """Load channel list from config."""
    with open(CONFIG_PATH) as f:
        config = yaml.safe_load(f)
    return config.get("channels", [])

def scrape_channel(channel_id):
    """Scrape single channel, return video data."""
    # Implementation using existing logic
    pass

def update_channel_file(channel_id, new_videos):
    """Merge new videos with existing data."""
    file_path = DATABASE_DIR / f"{channel_id}.json"
    # Load existing, merge, save
    pass

def main():
    channels = load_channels()
    success_count = 0

    for channel in channels:
        try:
            videos = scrape_channel(channel["id"])
            update_channel_file(channel["id"], videos)
            success_count += 1
        except Exception as e:
            print(f"Error scraping {channel['id']}: {e}", file=sys.stderr)

    print(f"Scraped {success_count}/{len(channels)} channels")
    return 0 if success_count == len(channels) else 1

if __name__ == "__main__":
    sys.exit(main())
```

### Phase 2: Create GitHub Actions Workflow (Day 1)

**File:** `.github/workflows/scrape.yml`

**Features:**
- Hourly cron schedule
- Manual dispatch option
- Python setup and dependency install
- Scraper execution
- Automatic commit and push
- Error handling and notifications

### Phase 3: Create Channel Management CLI (Day 1)

**File:** `scripts/add_channel.py`

**Features:**
- Add new channel by URL or ID
- Validate channel exists
- Update `config/sources.yaml`
- Create empty JSON file
- Document usage for Claude

**Usage:**
```bash
# Add by channel ID
python scripts/add_channel.py --id UCxxxxxxxx --name "Channel Name"

# Add by URL
python scripts/add_channel.py --url "https://youtube.com/c/ChannelName"
```

### Phase 4: Create Query Tools (Day 1-2)

**File:** `scripts/query_local.py`

**Features:**
- Search videos by title, description
- Filter by date range
- Filter by channel
- Export to CSV/JSON
- Count statistics

**Usage Examples:**
```bash
# Search all videos
python scripts/query_local.py --search "Claude Code"

# Recent videos only
python scripts/query_local.py --days 7

# Specific channel
python scripts/query_local.py --channel "AI Explained"

# Export results
python scripts/query_local.py --search "tutorial" --export csv
```

### Phase 5: Create Documentation (Day 2)

**Files:**
1. `docs/AGENT_GUIDE.md` - How Claude adds channels
2. `docs/QUERY_GUIDE.md` - How to search data
3. `docs/ARCHITECTURE.md` - System overview

---

## 5. Files to Create/Modify

### New Files

| File | Purpose |
|------|---------|
| `scripts/collect_github.py` | GitHub Actions optimized scraper |
| `scripts/add_channel.py` | CLI for adding channels |
| `scripts/query_local.py` | Data query tool |
| `.github/workflows/scrape.yml` | GitHub Actions workflow |
| `docs/AGENT_GUIDE.md` | Agent usage documentation |
| `docs/QUERY_GUIDE.md` | Query documentation |
| `docs/ARCHITECTURE.md` | System architecture |

### Modified Files

| File | Changes |
|------|---------|
| `config/sources.yaml` | Add any missing channels |
| `requirements.txt` | Add dependencies if needed |

---

## 6. Success Criteria

- [ ] Scraper runs on GitHub Actions (not local laptop)
- [ ] Scrapes all 23 configured channels every hour
- [ ] Updates JSON files in `database/channels/`
- [ ] Commits changes back to GitHub repo
- [ ] Documentation exists for adding new channels
- [ ] Documentation exists for querying data
- [ ] Claude can add channels via CLI command

---

## 7. Rollback Strategy

If automation causes issues:

1. **Immediate**: Disable workflow in GitHub Actions UI
2. **Short-term**: Revert to manual scraping
3. **Full**: Delete workflow file and automation scripts

**Disable Workflow:**
```bash
# Via GitHub UI: Actions > Workflows > YouTube Scraper > Disable
```

---

## 8. Estimated Timeline

| Phase | Duration |
|-------|----------|
| Phase 1: GitHub Scraper | 4 hours |
| Phase 2: GitHub Actions | 2 hours |
| Phase 3: Channel CLI | 3 hours |
| Phase 4: Query Tools | 3 hours |
| Phase 5: Documentation | 2 hours |
| Testing & Validation | 2 hours |
| **Total** | **16 hours (1-2 days)** |

---

## 9. Key Design Decisions

### Decision 1: GitHub Actions vs Render
**Choice:** GitHub Actions cron
**Rationale:** Native cron support, unlimited hours for public repos, simpler architecture

### Decision 2: JSON vs Database
**Choice:** Keep existing JSON files
**Rationale:** Works with current structure, Git-friendly, no migration needed

### Decision 3: Merge vs Overwrite
**Choice:** Merge new videos with existing
**Rationale:** Preserves historical data, handles API limits gracefully

### Decision 4: File-based Config
**Choice:** YAML config for channels
**Rationale:** Human-readable, version controlled, easy to edit

---

## 10. Risk Mitigation

| Risk | Mitigation |
|------|------------|
| YouTube API limits | Implement rate limiting, exponential backoff |
| Large commits | Only commit if data changed |
| Workflow failures | Add error notifications, retry logic |
| Data corruption | Keep git history for recovery |

---

*Plan created based on task requirements and Render/GitHub Actions analysis*
