#!/usr/bin/env python3
"""
AI Improvement Research - Video Relevance Ranking V2
Improved ranking based on actionability, specificity, and depth

Key insight: All sources are AI/tech channels, so "AI" is meaningless.
We need to distinguish USEFUL content from hype/bullshit.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import yaml

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = BASE_DIR / "config"
QUEUE_DIR = BASE_DIR / "queue"
TIMELINE_DIR = BASE_DIR / "timeline"

# Ensure directories exist
(QUEUE_DIR / "pending").mkdir(parents=True, exist_ok=True)
(QUEUE_DIR / "filtered").mkdir(parents=True, exist_ok=True)


def load_sources():
    """Load source configuration from sources.yaml."""
    sources_file = CONFIG_DIR / "sources.yaml"
    all_sources = []
    with open(sources_file) as f:
        for doc in yaml.safe_load_all(f):
            if doc and "sources" in doc:
                for source in doc.get("sources", []):
                    source["source_type"] = "channel"
                    all_sources.append(source)
            if doc and "playlists" in doc:
                for playlist in doc.get("playlists", []):
                    playlist["source_type"] = "playlist"
                    all_sources.append(playlist)
    return all_sources


def log_event(event_type, data):
    """Log an event to the timeline."""
    today = datetime.now().strftime("%Y-%m-%d")
    events_file = TIMELINE_DIR / "events" / f"{today}.yaml"

    if events_file.exists():
        with open(events_file) as f:
            events_data = yaml.safe_load(f) or {}
    else:
        events_data = {"date": today, "events": []}

    event = {
        "timestamp": datetime.now().isoformat(),
        "type": event_type,
        **data
    }
    events_data["events"].append(event)

    with open(events_file, "w") as f:
        yaml.dump(events_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def calculate_actionability_score(title, description):
    """
    Calculate actionability score (0-40).
    Can you DO something with this information?
    """
    text = f"{title} {description}".lower()
    score = 0

    # Strong actionability signals
    actionable_patterns = [
        ("how to", 20),
        ("tutorial", 20),
        ("step by step", 20),
        ("build ", 15),
        ("deploy ", 15),
        ("setup ", 15),
        ("configure ", 15),
        ("implement ", 15),
        ("masterclass", 15),
        ("workshop", 15),
        ("course", 15),
        ("guide", 10),
        ("from scratch", 10),
        ("complete guide", 10),
    ]

    for pattern, points in actionable_patterns:
        if pattern in text:
            score += points

    # Code/technical implementation
    if any(kw in text for kw in ["code", "github", "repository", "api", "sdk"]):
        score += 10

    # Vague business advice (penalty)
    vague_business = [
        "business model",
        "get customers",
        "make money",
        "secret to",
        "mindset",
    ]
    for pattern in vague_business:
        if pattern in text:
            score -= 10

    return max(0, min(40, score))


def calculate_specificity_score(title, description):
    """
    Calculate specificity score (0-30).
    Does it mention concrete tools, techniques, or outcomes?
    """
    text = f"{title} {description}".lower()
    score = 0

    # Specific tools we care about
    specific_tools = [
        "claude code", "claude-code", "claude",
        "mcp", "model context protocol",
        "antigravity", "anti-gravity",
        "stitch",
        "opencode", "open-code",
        "vibe coding", "vibe-coding",
        "gemini", "gpt-4", "gpt-5", "opus", "llama",
        "n8n", "make.com", "zapier",
        "cursor", "windsurf", "aider",
    ]

    for tool in specific_tools:
        if tool in text:
            score += 10

    # Specific techniques
    techniques = [
        "agent", "agents",
        "automation", "automate",
        "workflow", "workflows",
        "integration",
        "api integration",
        "code execution",
        "skill", "skills",
    ]

    for technique in techniques:
        if technique in text:
            score += 5

    # Hype words (penalty)
    hype_words = [
        "insane", "greatest ever", "mind-blowing",
        "revolutionary", "game changer", "kills",
        "destroyed", "obliterated", "unbelievable",
    ]

    for hype in hype_words:
        if hype in text:
            score -= 5

    return max(0, min(30, score))


def calculate_depth_score(title, description):
    """
    Calculate depth score (0-20).
    Is this surface-level news or deep content?
    """
    text = f"{title} {description}".lower()
    score = 0

    # Deep content indicators
    deep_indicators = [
        ("masterclass", 10),
        ("deep dive", 10),
        ("architecture", 10),
        ("implementation", 10),
        ("case study", 10),
        ("complete guide", 5),
        ("from scratch", 5),
        ("advanced", 5),
        ("internals", 5),
    ]

    for indicator, points in deep_indicators:
        if indicator in text:
            score += points

    # Specific numbers (often indicate case studies)
    import re
    if re.search(r'\$[\d,]+[KkMm]?', text):  # Dollar amounts like $2.5M
        score += 5
    if re.search(r'\d+\s*(hours?|days?|weeks?)', text):  # Time commitments
        score += 3

    # Surface-level indicators (penalty)
    surface_indicators = [
        "news", "update", "announcement",
        "first look", "impressions", "reacting to",
        "my thoughts on", "let's talk about",
    ]

    for indicator in surface_indicators:
        if indicator in text:
            score -= 5

    return max(0, min(20, score))


def calculate_creator_score(tier):
    """
    Calculate creator tier score (0-10).
    """
    tier_scores = {1: 10, 2: 5, 3: 0}
    return tier_scores.get(tier, 0)


def detect_clickbait(title, description):
    """
    Detect clickbait patterns and return penalty.
    """
    text = f"{title} {description}".lower()
    penalty = 0

    clickbait_patterns = [
        "you won't believe",
        "they don't want you to know",
        "i might delete this",
        "...is a trap",
        "...is a scam",
        "the truth about",
        "what they won't tell you",
        "exposed",
        "shocking",
    ]

    for pattern in clickbait_patterns:
        if pattern in text:
            penalty += 15

    # Excessive punctuation
    if title.count("!") > 2:
        penalty += 5

    # ALL CAPS words (excluding acronyms)
    import re
    caps_words = re.findall(r'\b[A-Z]{4,}\b', title)
    if len(caps_words) > 1:
        penalty += 5

    return penalty


def rank_video_v2(video_data):
    """
    Rank a video using the new V2 criteria.
    """
    title = video_data.get("source", {}).get("title", "")
    description = video_data.get("source", {}).get("description", "")
    tier = video_data.get("creator", {}).get("tier", 3)

    if not title:
        return None, False

    # Calculate component scores
    actionability = calculate_actionability_score(title, description)
    specificity = calculate_specificity_score(title, description)
    depth = calculate_depth_score(title, description)
    creator = calculate_creator_score(tier)

    # Base score
    base_score = actionability + specificity + depth + creator

    # Apply clickbait penalty
    clickbait_penalty = detect_clickbait(title, description)
    final_score = max(0, base_score - clickbait_penalty)

    # Determine if should process
    # Tier 1: Process if >= 45 (must be actionable + specific)
    # Tier 2: Process if >= 50 (higher bar for mid-tier)
    # Tier 3: Process if >= 55 (only the best from low-tier)
    thresholds = {1: 45, 2: 50, 3: 55}
    threshold = thresholds.get(tier, 55)

    should_process = final_score >= threshold

    ranking = {
        "actionability": actionability,
        "specificity": specificity,
        "depth": depth,
        "creator": creator,
        "clickbait_penalty": clickbait_penalty,
        "base_score": base_score,
        "final_score": final_score,
        "threshold": threshold,
        "should_process": should_process,
        "ranked_at": datetime.now().isoformat(),
        "version": "2.0"
    }

    return ranking, should_process


def add_to_queue(video_id, creator, metadata, ranking):
    """Add or update queue entry with ranking."""
    queue_file = QUEUE_DIR / "pending" / f"{video_id}.yaml"

    # Check if already exists
    if queue_file.exists():
        with open(queue_file) as f:
            queue_data = yaml.safe_load(f)
    else:
        queue_data = {
            "video_id": video_id,
            "title": metadata.get("title", ""),
            "creator": creator.get("name", ""),
            "creator_slug": creator.get("slug", ""),
            "url": metadata.get("url", ""),
            "queued_at": datetime.now().isoformat(),
        }

    queue_data["ranking_v2"] = ranking
    queue_data["decision"] = {
        "should_process": ranking["should_process"],
        "method": "rank_v2",
        "score": ranking["final_score"],
        "threshold": ranking["threshold"]
    }

    with open(queue_file, "w") as f:
        yaml.dump(queue_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def move_to_filtered(video_id):
    """Move queue entry to filtered folder."""
    pending_file = QUEUE_DIR / "pending" / f"{video_id}.yaml"
    filtered_file = QUEUE_DIR / "filtered" / f"{video_id}.yaml"

    if pending_file.exists():
        with open(pending_file) as f:
            data = yaml.safe_load(f)

        data["status"] = "filtered"
        data["filtered_at"] = datetime.now().isoformat()

        with open(filtered_file, "w") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        pending_file.unlink()


def process_all_videos(dry_run=False):
    """Process all videos in data/sources."""
    print(f"\n{'='*60}")
    print("RANKING ALL VIDEOS (V2)")
    print(f"{'='*60}")

    stats = {"processed": 0, "passed": 0, "filtered": 0}

    for source_dir in (DATA_DIR / "sources").iterdir():
        if not source_dir.is_dir():
            continue

        videos_dir = source_dir / "videos"
        if not videos_dir.exists():
            continue

        for video_file in videos_dir.glob("*.yaml"):
            with open(video_file) as f:
                video_data = yaml.safe_load(f)

            video_id = video_data.get("source", {}).get("id")
            title = video_data.get("source", {}).get("title", "")[:60]

            if not title:
                continue

            print(f"\n📊 {title}...")

            ranking, should_process = rank_video_v2(video_data)

            if not ranking:
                print("   ❌ Could not rank")
                continue

            print(f"   Actionability: {ranking['actionability']}/40 | "
                  f"Specificity: {ranking['specificity']}/30 | "
                  f"Depth: {ranking['depth']}/20 | "
                  f"Creator: {ranking['creator']}/10")

            if ranking['clickbait_penalty'] > 0:
                print(f"   ⚠️  Clickbait penalty: -{ranking['clickbait_penalty']}")

            print(f"   Final: {ranking['final_score']}/100 (threshold: {ranking['threshold']})")

            status = "✅ PASS" if should_process else "❌ FILTER"
            print(f"   {status}")

            if not dry_run:
                add_to_queue(video_id, video_data.get("creator", {}),
                           video_data.get("source", {}), ranking)

                if should_process:
                    stats["passed"] += 1
                else:
                    move_to_filtered(video_id)
                    stats["filtered"] += 1

            stats["processed"] += 1

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Processed: {stats['processed']}")
    if not dry_run:
        print(f"Passed: {stats['passed']}")
        print(f"Filtered: {stats['filtered']}")


def main():
    parser = argparse.ArgumentParser(description="Rank videos using improved V2 criteria")
    parser.add_argument("--dry-run", action="store_true", help="Show rankings without updating")
    parser.add_argument("--video", help="Rank specific video by ID")

    args = parser.parse_args()

    if args.video:
        # Rank single video
        for source_dir in (DATA_DIR / "sources").iterdir():
            video_file = source_dir / "videos" / f"{args.video}.yaml"
            if video_file.exists():
                with open(video_file) as f:
                    video_data = yaml.safe_load(f)

                ranking, should_process = rank_video_v2(video_data)
                print(json.dumps(ranking, indent=2))
                return

        print(f"Video {args.video} not found")
    else:
        process_all_videos(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
