"""
Transcript Fetcher using youtube-transcript-api with Tor proxy

Fetches transcripts with rate limiting and error handling.
Uses Tor to bypass IP blocks from YouTube.
"""

import os
import re
import time
from pathlib import Path
from typing import Optional, Dict, Tuple
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from youtube_transcript_api.proxies import GenericProxyConfig


class TranscriptFetcher:
    """Fetches YouTube transcripts with rate limiting via Tor."""

    def __init__(self, output_dir: Path, delay: float = 2.0, use_tor: bool = True):
        """
        Initialize fetcher.

        Args:
            output_dir: Directory to save transcripts
            delay: Seconds between requests (rate limiting)
            use_tor: Whether to route requests through Tor
        """
        self.output_dir = output_dir
        self.delay = delay
        self.use_tor = use_tor
        self.last_request_time = 0
        self.proxy_config = None

        # Check environment variable for Tor setting (GitHub Actions sets USE_TOR=false)
        env_use_tor = os.environ.get('USE_TOR', 'true').lower()
        if env_use_tor == 'false':
            self.use_tor = False

        # Set up Tor proxy via Privoxy (HTTP proxy -> SOCKS5)
        if self.use_tor:
            self.proxy_config = GenericProxyConfig(
                http_url="http://127.0.0.1:8118",
                https_url="http://127.0.0.1:8118"
            )

    def _rate_limit(self):
        """Enforce rate limiting between requests."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()

    def fetch(self, video_id: str, video_data: Dict) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Fetch transcript for a video.

        Args:
            video_id: YouTube video ID
            video_data: Dict with title, channel, etc.

        Returns:
            (success, transcript_text, error_message)
        """
        self._rate_limit()

        try:
            # Fetch transcript (with or without Tor proxy)
            if self.use_tor and self.proxy_config:
                ytt_api = YouTubeTranscriptApi(proxy_config=self.proxy_config)
            else:
                ytt_api = YouTubeTranscriptApi()
            transcript = ytt_api.fetch(video_id)

            # Combine all text segments
            full_text = ' '.join(segment.text for segment in transcript)

            # Clean up the text
            full_text = self._clean_transcript(full_text)

            return True, full_text, None

        except TranscriptsDisabled:
            return False, None, "Transcripts disabled for this video"
        except NoTranscriptFound:
            return False, None, "No transcript found"
        except VideoUnavailable:
            return False, None, "Video unavailable"
        except Exception as e:
            error_msg = str(e)
            if "IP" in error_msg or "blocked" in error_msg.lower():
                return False, None, "IP blocked by YouTube - need to rotate Tor circuit"
            return False, None, f"Error: {error_msg}"

    def _clean_transcript(self, text: str) -> str:
        """Clean up transcript text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove music notes and sound effects
        text = re.sub(r'\[.*?\]', '', text)
        text = re.sub(r'\(.*?\)', '', text)
        # Clean up punctuation spacing
        text = re.sub(r'\s+([.,!?])', r'\1', text)
        return text.strip()

    def save_transcript(self, video_id: str, video_data: Dict, transcript: str) -> Path:
        """
        Save transcript as markdown file.

        Args:
            video_id: YouTube video ID
            video_data: Video metadata
            transcript: Transcript text

        Returns:
            Path to saved file
        """
        channel_slug = video_data.get('channel_slug', 'unknown')
        channel_dir = self.output_dir / channel_slug
        channel_dir.mkdir(parents=True, exist_ok=True)

        output_path = channel_dir / f"{video_id}.md"

        # Build metadata
        metadata = {
            'video_id': video_id,
            'title': video_data.get('title', 'Unknown'),
            'channel': video_data.get('channel_name', 'Unknown'),
            'channel_slug': channel_slug,
            'upload_date': video_data.get('upload_date', ''),
            'duration': video_data.get('duration', 0),
            'score': video_data.get('score', 0),
            'priority': video_data.get('priority', 'P3'),
            'url': f"https://youtube.com/watch?v={video_id}",
            'fetched_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        }

        # Write markdown
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("---\n")
            for key, value in metadata.items():
                f.write(f"{key}: {value}\n")
            f.write("---\n\n")
            f.write(f"# {metadata['title']}\n\n")
            f.write(transcript)

        return output_path
