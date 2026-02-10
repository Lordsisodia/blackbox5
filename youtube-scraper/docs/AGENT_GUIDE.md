# Agent Guide: Adding YouTube Channels

This guide shows how AI agents (Claude, Moltbot, etc.) can add new YouTube channels to the scraper.

## Quick Add via CLI

### Adding a Single Channel

```bash
# Edit channels.yaml
nano /opt/blackbox5/youtube-scraper/config/channels.yaml

# Add new channel entry:
# - name: "Channel Name"
#   url: "https://www.youtube.com/@ChannelHandle"
#   max_videos: 50
```

### Adding Multiple Channels

```bash
# Edit channels.yaml
nano /opt/blackbox5/youtube-scraper/config/channels.yaml

# Add multiple entries:
channels:
  - name: "Channel 1"
    url: "https://www.youtube.com/@Channel1"
    max_videos: 50

  - name: "Channel 2"
    url: "https://www.youtube.com/@Channel2"
    max_videos: 50
```

## Programmatic Addition (Python)

```python
import yaml
from pathlib import Path

CHANNELS_FILE = Path("/opt/blackbox5/youtube-scraper/config/channels.yaml")

def add_channel(name: str, url: str, max_videos: int = 50):
    """Add a new channel to the configuration."""
    with open(CHANNELS_FILE, 'r') as f:
        config = yaml.safe_load(f)

    # Add new channel
    config['channels'].append({
        'name': name,
        'url': url,
        'max_videos': max_videos
    })

    # Save updated config
    with open(CHANNELS_FILE, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    print(f"✓ Added channel: {name}")

# Example usage
add_channel("My Favorite Channel", "https://www.youtube.com/@MyChannel", max_videos=30)
```

## Finding Channel URLs

### Method 1: From Channel Page

1. Go to the channel on YouTube
2. Look for the handle in the URL or header
3. URL format: `https://www.youtube.com/@ChannelHandle`

### Method 2: From Video

1. Find any video from the channel
2. Click on channel name
3. Copy the channel URL

### Method 3: API Search (yt-dlp)

```bash
# Search for a channel
yt-dlp "ytsearch:channel name" --flat-playlist

# Get channel info
yt-dlp --get-id --get-title "https://youtube.com/@ChannelHandle"
```

## Channel URL Formats

**Channel Handle (Recommended):**
```
https://www.youtube.com/@ChannelHandle
```

**Channel ID:**
```
https://www.youtube.com/channel/UCxxxxxxxxxxxxxxxxxxxxxx
```

**Custom URL:**
```
https://www.youtube.com/c/CustomName
```

**Playlist:**
```
https://www.youtube.com/playlist?list=PLxxxxxxxxxxxxxxxxxxxxxx
```

## Validating Channel URLs

```python
def is_valid_youtube_url(url: str) -> bool:
    """Check if URL is a valid YouTube channel or playlist."""
    valid_patterns = [
        'youtube.com/@',
        'youtube.com/channel/',
        'youtube.com/c/',
        'youtube.com/playlist'
    ]
    return any(pattern in url for pattern in valid_patterns)

# Usage
if is_valid_youtube_url("https://www.youtube.com/@Fireship"):
    print("Valid URL")
```

## Testing New Channels

Before adding to production:

```bash
# Test collection of a single channel
python3 /opt/blackbox5/youtube-scraper/scraper.py \
  --channel "https://www.youtube.com/@TestChannel" \
  --max-videos 5

# Check collected data
cat /opt/blackbox5/youtube-scraper/database/channels/test_channel.json
```

## Best Practices

1. **Use Handles**: Prefer `@ChannelHandle` format over channel IDs
2. **Set Appropriate Limits**: Use 20-50 videos for active channels, 10 for inactive
3. **Test First**: Collect a few videos to verify channel is accessible
4. **Monitor Logs**: Check for errors in `/opt/blackbox5/youtube-scraper/logs/`
5. **Avoid Duplicates**: Check if channel already exists before adding

## Troubleshooting

### Channel Not Found

```
ERROR: No videos found for Channel Name
```

**Solutions:**
- Verify URL is correct
- Check if channel is public (not private)
- Try alternative URL format

### Rate Limiting

```
WARNING: HTTP Error 429: Too Many Requests
```

**Solutions:**
- Reduce `max_videos` value
- Add delay between channels
- Use YouTube API key if available

### No Transcripts

Some videos don't have transcripts. This is normal and handled gracefully.

## Example: Adding Multiple Channels at Once

```python
import yaml

channels_to_add = [
    ("Channel A", "https://www.youtube.com/@ChannelA", 50),
    ("Channel B", "https://www.youtube.com/@ChannelB", 30),
    ("Channel C", "https://www.youtube.com/@ChannelC", 20),
]

config_file = "/opt/blackbox5/youtube-scraper/config/channels.yaml"

with open(config_file, 'r') as f:
    config = yaml.safe_load(f)

for name, url, max_vids in channels_to_add:
    config['channels'].append({
        'name': name,
        'url': url,
        'max_videos': max_vids
    })

with open(config_file, 'w') as f:
    yaml.dump(config, f, default_flow_style=False, sort_keys=False)

print(f"✓ Added {len(channels_to_add)} channels")
```

---

**For more information, see:** `QUERY_GUIDE.md` (how to search collected data)
