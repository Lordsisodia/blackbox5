#!/usr/bin/env python3
"""
Scrape additional videos that are likely to work
"""

from pathlib import Path
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._transcripts import NoTranscriptFound

# Videos that are more likely to work (older, popular, different categories)
VIDEOS_TO_SCRAPE = [
    {'id': '3k9nIjx3pKs', 'title': 'Python Programming Tutorial', 'category': 'Programming'},
    {'id': 'TCH_1BHY58I', 'title': 'AI Tutorial', 'category': 'AI'},
    {'id': 'c0qJkV6WqOQ', 'title': 'Introduction to Machine Learning', 'category': 'ML'},
    {'id': 'aircAruvnKk', 'title': 'Neural Networks Explained', 'category': 'Deep Learning'},
]

def extract_key_topics(text):
    """Extract key topics from transcript text"""
    words = text.lower().split()

    # Stop words to filter out
    stop_words = {'the', 'and', 'is', 'to', 'a', 'in', 'that', 'it', 'of', 'for', 'on', 'with', 'as', 'this', 'are', 'be', 'at', 'or', 'was', 'i', 'you', 'we', 'so', 'but', 'not', 'have', 'will', 'an', 'can', 'if', 'from', 'by', 'my', 'your', 'they', 'their', 'all', 'one', 'two', 'more', 'than', 'just', 'like', 'out', 'up', 'about', 'what', 'when', 'which', 'who', 'how', 'know', 'get', 'make', 'use', 'see', 'time', 'first', 'also', 'well', 'into', 'even', 'because', 'very', 'where', 'being', 'go', 'way', 'think', 'say', 'take', 'come', 'good', 'new', 'some', 'could', 'them', 'then', 'than', 'any', 'work', 'now', 'may', 'only', 'want', 'such', 'give', 'these', 'over', 'most', 'need', 'other', 'after', 'back', 'our', 'through', 'still', 'should', 'before', 'here', 'those', 'there', 'much', 'while', 'year', 'since', 'being', 'made', 'being', 'each', 'many', 'being', 'right'}

    word_freq = {}
    for word in words:
        # Clean word
        word = word.strip('.,!?()[]{}""\'')
        if len(word) > 3 and word not in stop_words:
            word_freq[word] = word_freq.get(word, 0) + 1

    # Get top 20 words
    return sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

def save_transcript_to_research(video_info, transcript_data):
    """Save transcript to research folder with analysis"""
    date = datetime.now().strftime('%Y-%m-%d')
    safe_title = video_info['title'][:50].replace(' ', '_').replace('/', '_').replace(':', '_')
    filename = f"{date}_{video_info['id']}_{safe_title}.md"

    # Research directory
    research_dir = Path('/opt/blackbox5/5-project-memory/blackbox5/knowledge/research')
    research_dir.mkdir(parents=True, exist_ok=True)

    filepath = research_dir / filename

    # Extract full text and key topics
    full_text = ' '.join([snippet.text for snippet in transcript_data])
    key_topics = extract_key_topics(full_text)

    word_count = len(full_text.split())

    # Create markdown content
    content = f"# Video Analysis: {video_info['title']}\n\n"

    content += "## Video Information\n\n"
    content += f"- **Video ID:** {video_info['id']}\n"
    content += f"- **Category:** {video_info['category']}\n"
    content += f"- **URL:** https://www.youtube.com/watch?v={video_info['id']}\n"
    content += f"- **Word Count:** {word_count:,}\n"
    content += f"- **Segments:** {len(transcript_data)}\n"
    content += f"- **Scraped:** {datetime.now().isoformat()}\n\n"

    content += "## Key Topics Identified\n\n"
    for word, count in key_topics:
        content += f"- **{word}** ({count} mentions)\n"

    content += "\n## Transcript\n\n"
    for i, snippet in enumerate(transcript_data[:150]):  # First 150 snippets
        start = snippet.start
        minutes = int(start // 60)
        seconds = int(start % 60)
        content += f"[{minutes}:{seconds:02d}] {snippet.text}\n"

        # Add break every 25 snippets for readability
        if (i + 1) % 25 == 0:
            content += "\n"

    if len(transcript_data) > 150:
        content += f"\n... ({len(transcript_data) - 150} more segments)\n"

    # Statistics at the end
    content += "\n## Statistics\n\n"
    content += f"- **Total words:** {word_count:,}\n"
    content += f"- **Unique words:** {len(set(word.lower() for word in full_text.split())):,}\n"
    content += f"- **Duration:** {transcript_data[-1].start / 60:.1f} minutes (approx)\n"
    content += f"- **Average segment length:** {word_count / len(transcript_data):.1f} words\n"

    # Save file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Saved: {filepath.name}")
    return filepath

def main():
    print("=" * 70)
    print("Additional YouTube Transcript Scraping")
    print("=" * 70)
    print()

    ytt = YouTubeTranscriptApi()

    saved_count = 0

    for video_info in VIDEOS_TO_SCRAPE:
        video_id = video_info['id']

        print(f"{'=' * 70}")
        print(f"Processing: {video_info['title']}")
        print(f"ID: {video_id}")
        print(f"{'=' * 70}")

        try:
            # Fetch transcript
            transcript = ytt.fetch(video_id)

            word_count = sum(len(snippet.text.split()) for snippet in transcript)
            print(f"✓ Transcript fetched: {len(transcript)} segments, {word_count:,} words")

            # Save to research folder
            save_transcript_to_research(video_info, transcript)
            saved_count += 1

            # Add delay to avoid blocking
            import time
            time.sleep(3)

        except NoTranscriptFound:
            print(f"✗ No transcript available for this video")
        except Exception as e:
            error_msg = str(e)
            if 'IP' in error_msg or 'blocked' in error_msg:
                print(f"✗ IP blocked - skipping remaining videos")
                break
            else:
                print(f"✗ Error: {str(e)[:100]}")

        print()

    print("=" * 70)
    print(f"✓ Complete! Saved {saved_count} additional transcripts")
    print("=" * 70)

if __name__ == '__main__':
    main()
