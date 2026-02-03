# DECISIONS: YouTube Auto-Scraper

## Architecture Decision: GitHub Actions over Render

**Decision:** Use GitHub Actions for cron/scheduling instead of Render

**Rationale:**
- Render free tier has no cron jobs
- Render has 750hr/month limit (tight)
- Render requires external ping service (complexity)
- GitHub Actions is truly unlimited for public repos

**Trade-offs:**
- 1-2 min startup time per run (acceptable)
- Must be public repo for unlimited minutes (acceptable)

## Storage Decision: Files over Database

**Decision:** Keep JSON file storage, no database

**Rationale:**
- Current data: 3.5MB (tiny)
- Growth: ~150KB/month
- Git tracks all changes naturally
- Zero complexity (no SQL, no client)
- Instant local access

## Integration Decision: Claude CLI Commands

**Decision:** Create simple CLI scripts for common operations

**Scripts:**
- `add_channel.py` - Add new YouTube channel
- `query.py` - Query videos by date/channel
- `rank.py` - Rank videos by relevance

**Usage:**
```bash
python scripts/add_channel.py --handle @NewCreator --name "Name"
python scripts/query.py --days 7
python scripts/rank.py --top 10
```
