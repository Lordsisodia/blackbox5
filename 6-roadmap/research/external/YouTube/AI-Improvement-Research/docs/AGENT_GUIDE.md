# Agent Guide: YouTube Pipeline

## Quick Commands for Claude

### Add New Channel

```bash
# Add a new YouTube channel to scrape
python scripts/add_channel.py --handle @ChannelHandle --name "Channel Name" --tier 2

# Example:
python scripts/add_channel.py --handle @Fireship --name "Fireship" --tier 1
```

This will:
1. Validate the channel exists
2. Add to `config/sources.yaml`
3. Git commit and push
4. Next hourly scrape will include it

### Query Recent Videos

```bash
# Get videos from last 7 days
python scripts/query.py --days 7

# Get videos from specific channel
python scripts/query.py --channel david_ondrej --days 30

# Get top 50 recent videos
python scripts/query.py --days 7 --limit 50
```

### Get Ranked Videos

```bash
# Top 10 videos by relevance score
python scripts/rank_simple.py --days 7 --top 10

# Top videos from last 30 days
python scripts/rank_simple.py --days 30 --top 20
```

### Generate Daily Digest

```bash
# Create daily report of top videos
python scripts/digest.py

# Output saved to: reports/daily/{date}.md
```

## Data Locations

- **Raw data**: `database/channels/{slug}.json`
- **Config**: `config/sources.yaml`
- **Daily reports**: `reports/daily/{date}.md`

## Automation

- **Scraping**: Runs every hour via GitHub Actions (`.github/workflows/scrape.yml`)
- **Auto-commits**: Changes pushed to GitHub automatically
- **Manual trigger**: Go to Actions tab → Scrape workflow → Run workflow

## Adding Channels: Step by Step

1. Get channel handle (e.g., `@DavidOndrej`)
2. Decide tier:
   - Tier 1: Must watch (Anthropic, major creators)
   - Tier 2: High quality (regular good content)
   - Tier 3: Filtered (occasional good content)
3. Run add_channel.py
4. Verify in config/sources.yaml
5. Next hourly run will scrape it

## Troubleshooting

**Scraper not running?**
- Check Actions tab on GitHub
- Ensure GITHUB_TOKEN has write permissions

**Channel not found?**
- Verify handle is correct (case-sensitive)
- Check if channel has public videos

**Rate limited?**
- Script has built-in delays
- Reduce --workers if needed
