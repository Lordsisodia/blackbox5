# Mac Mini Server Setup

Your Mac Mini is now configured as a development server accessible via SSH.

## Connection Details

```bash
# Quick connect
ssh mac-mini

# Full command (if needed)
ssh shaansisodia@100.66.34.21

# Via Tailscale hostname
ssh shaansisodia@shaans-mac-mini.tailnet-name.ts.net
```

## What's Installed

### Repositories
- `~/Projects/youtube-ai-research/` - YouTube transcript pipeline
- `~/.blackbox5/` - Blackbox5 project (already existed)

### YouTube Pipeline
Location: `~/Projects/youtube-ai-research/`

**Scripts:**
- `start-worker.sh` - Start transcript fetching worker
- `scripts/analyze_transcripts.py` - Analyze with Claude
- `scripts/generate_hourly_digest.py` - Generate digests
- `scripts/claude_bot_query.py` - Query for your Claude bot

**Usage:**
```bash
# SSH to Mac Mini
ssh mac-mini

# Start transcript worker (run in tmux/screen)
cd ~/Projects/youtube-ai-research
./start-worker.sh

# Or run one-time batch
source venv/bin/activate
python scripts/worker/worker.py --limit 10
```

## Running Worker Continuously

### Option 1: tmux (Recommended)
```bash
ssh mac-mini
tmux new -s youtube-worker
cd ~/Projects/youtube-ai-research
./start-worker.sh
# Detach: Ctrl+B, then D
# Reattach: tmux attach -t youtube-worker
```

### Option 2: nohup
```bash
ssh mac-mini "cd ~/Projects/youtube-ai-research && nohup ./start-worker.sh > .logs/worker.log 2>&1 &"
```

### Option 3: LaunchAgent (Auto-start on boot)
```bash
# Load the service
ssh mac-mini "launchctl load ~/Library/LaunchAgents/com.siso.youtube-transcript-worker.plist"

# Check status
ssh mac-mini "launchctl list | grep youtube"

# Unload
ssh mac-mini "launchctl unload ~/Library/LaunchAgents/com.siso.youtube-transcript-worker.plist"
```

## For Your Claude Bot

Add this to your Claude bot's hourly check:

```bash
# Get latest digest
ssh mac-mini "cd ~/Projects/youtube-ai-research && source venv/bin/activate && python scripts/claude_bot_query.py --latest"

# Or check stats
ssh mac-mini "cd ~/Projects/youtube-ai-research && sqlite3 database/queue.db 'SELECT status, COUNT(*) FROM video_queue GROUP BY status;'"
```

## Security

- SSH key-only authentication (no passwords)
- Tailscale VPN (encrypted mesh network)
- No ports forwarded on router
- Accessible only via Tailscale (100.66.34.21)

## Monitoring

Check worker status remotely:
```bash
# Check if running
ssh mac-mini "ps aux | grep worker.py | grep -v grep"

# View logs
ssh mac-mini "tail -f ~/Projects/youtube-ai-research/.logs/worker.log"

# Check queue status
ssh mac-mini "cd ~/Projects/youtube-ai-research && sqlite3 database/queue.db 'SELECT status, COUNT(*) FROM video_queue GROUP BY status;'"
```

## File Locations

| Purpose | Path |
|---------|------|
| Transcripts | `~/Projects/youtube-ai-research/content/transcripts/` |
| Database | `~/Projects/youtube-ai-research/database/queue.db` |
| Logs | `~/Projects/youtube-ai-research/.logs/` |
| Analysis | `~/Projects/youtube-ai-research/analysis/` |
| State | `~/Projects/youtube-ai-research/.state/` |

## Troubleshooting

### Worker not starting
```bash
ssh mac-mini "cd ~/Projects/youtube-ai-research && source venv/bin/activate && python scripts/worker/worker.py --limit 1"
```

### IP blocked by YouTube
This is normal from residential IPs. The worker has rate limiting built-in.
Consider:
- Reducing `--daily-limit` (default: 100)
- Increasing `--request-delay` (default: 3.0 seconds)
- Using Tor (if configured)

### Can't SSH
1. Check Tailscale is running on both machines
2. Try: `tailscale status` (should show Mac Mini)
3. Restart Tailscale if needed: `sudo tailscale down && sudo tailscale up`

## Next Steps

1. [ ] Start the worker: `ssh mac-mini`, then `cd ~/Projects/youtube-ai-research && ./start-worker.sh`
2. [ ] Set up your Claude bot to query hourly
3. [ ] Configure GitHub Actions to sync data back (optional)
4. [ ] Set up monitoring/alerting for downtime (optional)

## Comparison: Mac Mini vs Hetzner

| Factor | Mac Mini | Hetzner |
|--------|----------|---------|
| Cost | $0 (owned) | $10/month |
| RAM | 16GB | 8GB |
| Storage | 228GB | 40GB |
| CPU | M4 (fast) | Shared (adequate) |
| Network | Residential | Datacenter |
| Uptime | 99% (your power/internet) | 99.9% |
| Control | Full | Limited |

**Winner for your use case: Mac Mini** (already owned, more resources, no ongoing cost)
