# PLAN.md: YouTube Pipeline Implementation

**Task ID:** TASK-DOCS-010-youtube-pipeline-plan  
**Status:** ACTIVE  
**Priority:** HIGH  
**Type:** Action Plan / Implementation Guide

---

## 1. First Principles Analysis

### Why Automated YouTube Scraping?

1. **Continuous Intelligence** - Stay current with AI/ML developments without manual monitoring
2. **Scalable Research** - Process content from 23+ channels simultaneously
3. **Structured Data** - Transform unstructured video content into queryable format
4. **Cost Efficiency** - Free tier (GitHub Actions) vs paid services

### What Happens Without Automation?

- **Manual Monitoring** - Hours spent checking channels individually
- **Missed Content** - Important videos slip through cracks
- **No Historical Data** - Can't track trends or analyze patterns
- **Inconsistent Coverage** - Some channels get more attention than others

### How to Build a Robust Pipeline?

**GitHub Actions Approach (Recommended):**
- Cron-triggered workflow (hourly)
- Self-hosted runner compatibility
- Automatic commits back to repo
- No server maintenance required

---

## 2. Current State Assessment

### Existing Assets

| Component | Status | Location |
|-----------|--------|----------|
| Videos Collected | 7,219 videos | database/channels/*.json |
| Channels | 11 active | config/sources.yaml |
| Scripts | Working locally | collect_channel_optimized.py |
| Data Size | ~3.5MB | JSON + YAML |

### What's Missing

1. **GitHub Repository** - Not yet created/pushed
2. **GitHub Actions Workflow** - No automation
3. **Master Scraper Script** - Needs collect_all.py
4. **Channel Management** - Needs add_channel.py
5. **Query Tools** - Needs query.py
6. **Ranking System** - Needs rank.py
7. **Documentation** - Needs AGENT_GUIDE.md

---

## 3. Proposed Solution

### Architecture

```
GitHub Actions (cron: hourly)
    ↓
Checkout repository
    ↓
Install dependencies
    ↓
Run collect_all.py
    ↓
Commit changes (if any)
    ↓
Push to main
```

### File Structure

```
youtube-ai-research/
├── .github/workflows/scrape.yml    # Automation
├── scripts/
│   ├── collect_all.py              # Master scraper
│   ├── collect_channel_optimized.py # Per-channel scraper
│   ├── add_channel.py              # Channel management
│   ├── query.py                    # Data querying
│   ├── rank.py                     # Video ranking
│   └── digest.py                   # Daily report
├── database/channels/*.json        # Video data
├── config/sources.yaml             # Channel config
└── docs/AGENT_GUIDE.md             # Documentation
```

---

## 4. Implementation Plan

### Phase 1: Repository Setup (15 min)

1. Initialize git repository
2. Create GitHub repository
3. Push initial commit with existing data
4. Verify data is accessible

### Phase 2: GitHub Actions (15 min)

1. Create `.github/workflows/scrape.yml`
2. Configure hourly cron schedule
3. Set up Python environment
4. Test workflow manually

### Phase 3: Master Scraper (15 min)

1. Create `scripts/collect_all.py`
2. Load channels from config/sources.yaml
3. Iterate and scrape each channel
4. Handle errors gracefully

### Phase 4: Channel Management (10 min)

1. Create `scripts/add_channel.py`
2. Implement CLI arguments (--handle, --name, --tier)
3. Update config/sources.yaml
4. Auto-commit new channels

### Phase 5: Query Tools (10 min)

1. Create `scripts/query.py`
2. Filter by days, channel, limit
3. Format output for readability
4. Sort by upload date

### Phase 6: Ranking System (15 min)

1. Create `scripts/rank.py`
2. Define scoring algorithm:
   - Keyword matching (10 pts each)
   - View count (up to 50 pts)
   - Recency (10-20 pts)
3. Generate top N list

### Phase 7: Documentation (10 min)

1. Create `docs/AGENT_GUIDE.md`
2. Document all commands
3. Explain data structure
4. Add troubleshooting section

---

## 5. Success Criteria

| Criterion | Verification |
|-----------|--------------|
| Repository created | github.com/YOUR_USERNAME/youtube-ai-research exists |
| Workflow running | Actions tab shows successful runs |
| Hourly scraping | Data updates every hour |
| All 23 channels | config/sources.yaml has 23 entries |
| Auto-commit | Changes pushed without manual intervention |
| Add channel works | `python add_channel.py --handle @New --name "Name"` succeeds |
| Query works | `python query.py --days 7` returns results |
| Ranking works | `python rank.py --top 10` shows scored videos |

---

## 6. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Repository | 15 min | 15 min |
| Phase 2: Actions | 15 min | 30 min |
| Phase 3: Scraper | 15 min | 45 min |
| Phase 4: Channel Mgmt | 10 min | 55 min |
| Phase 5: Query | 10 min | 65 min |
| Phase 6: Ranking | 15 min | 80 min |
| Phase 7: Docs | 10 min | 90 min |
| **Total** | **~1.5 hours** | |

---

## 7. Files to Create

1. `.github/workflows/scrape.yml` - GitHub Actions workflow
2. `scripts/collect_all.py` - Master scraper script
3. `scripts/add_channel.py` - Channel management CLI
4. `scripts/query.py` - Data query tool
5. `scripts/rank.py` - Video ranking algorithm
6. `scripts/digest.py` - Daily digest generator
7. `docs/AGENT_GUIDE.md` - Agent documentation

---

## 8. Rollback Strategy

If issues arise:
1. Disable GitHub Actions workflow
2. Revert to last known good commit
3. Fix issues locally
4. Re-enable workflow

---

*Plan based on action plan document in task.md*
