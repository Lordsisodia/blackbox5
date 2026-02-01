#!/usr/bin/env python3
"""
AI Improvement Research - Video Relevance Ranking
Analyzes video titles and descriptions to score importance BEFORE extraction

This saves processing time by filtering low-value content early.
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
    with open(sources_file) as f:
        for doc in yaml.safe_load_all(f):
            if doc and "sources" in doc:
                return doc.get("sources", [])
    return []


def load_project_context():
    """Load project context for relevance scoring."""
    sources_file = CONFIG_DIR / "sources.yaml"
    with open(sources_file) as f:
        for doc in yaml.safe_load_all(f):
            if doc and "project_context" in doc:
                return doc.get("project_context", {})
    return {}


def load_tier_rules():
    """Load tier rules for filtering."""
    sources_file = CONFIG_DIR / "sources.yaml"
    with open(sources_file) as f:
        for doc in yaml.safe_load_all(f):
            if doc and "tier_rules" in doc:
                return doc.get("tier_rules", {})
    return {}


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


def calculate_relevance_score(video_data, project_context):
    """
    Calculate relevance score (0-100) based on match to project context.
    """
    title = video_data.get("source", {}).get("title", "").lower()
    description = video_data.get("source", {}).get("description", "").lower()
    text = f"{title} {description}"

    score = 0
    max_score = 100

    # Keyword matching from project context
    keywords = []
    for project in project_context.get("active_projects", []):
        keywords.extend(project.get("keywords", []))

    # Check for keyword matches
    keyword_matches = 0
    for keyword in keywords:
        if keyword.lower() in text:
            keyword_matches += 1

    # Score based on keyword density (max 40 points)
    score += min(40, keyword_matches * 10)

    # Check for high-priority topics
    high_priority_topics = [
        "claude code", "mcp", "model context protocol", "ai agent",
        "vibe coding", "autonomous", "llm", "prompt engineering"
    ]
    for topic in high_priority_topics:
        if topic in text:
            score += 15

    # Check for actionable keywords
    actionable_keywords = ["how to", "tutorial", "guide", "setup", "build", "create"]
    for keyword in actionable_keywords:
        if keyword in text:
            score += 5

    return min(max_score, score)


def calculate_importance_score(video_data):
    """
    Calculate importance score (0-100) based on creator tier and metadata.
    """
    score = 0
    creator_tier = video_data.get("creator", {}).get("tier", 3)
    view_count = video_data.get("source", {}).get("view_count", 0)

    # Creator tier weight (max 50 points)
    tier_scores = {1: 50, 2: 35, 3: 20}
    score += tier_scores.get(creator_tier, 10)

    # View count indicator (max 20 points)
    if view_count > 100000:
        score += 20
    elif view_count > 50000:
        score += 15
    elif view_count > 10000:
        score += 10
    elif view_count > 1000:
        score += 5

    # Recent content bonus (max 15 points)
    published = video_data.get("source", {}).get("published_at", "")
    if published:
        try:
            from datetime import datetime
            pub_date = datetime.strptime(str(published), "%Y%m%d")
            days_old = (datetime.now() - pub_date).days
            if days_old <= 7:
                score += 15
            elif days_old <= 30:
                score += 10
            elif days_old <= 90:
                score += 5
        except:
            pass

    # Title quality indicators (max 15 points)
    title = video_data.get("source", {}).get("title", "").lower()
    quality_indicators = [
        ("how to", 5), ("tutorial", 5), ("guide", 5),
        ("deep dive", 5), ("explained", 5), ("course", 5),
        ("best practices", 5), ("complete", 3), ("full", 3)
    ]
    for indicator, points in quality_indicators:
        if indicator in title:
            score += points

    return min(100, score)


def calculate_value_score(video_data, project_context):
    """
    Calculate value score (0-100) based on potential actionability and novelty.
    """
    score = 0
    title = video_data.get("source", {}).get("title", "").lower()
    description = video_data.get("source", {}).get("description", "").lower()
    text = f"{title} {description}"

    # Actionability indicators (max 50 points)
    actionable_patterns = [
        ("how to", 10), ("tutorial", 10), ("step by step", 10),
        ("guide", 8), ("setup", 8), ("build", 8), ("create", 8),
        ("implement", 8), ("deploy", 8), ("configure", 8),
        ("workflow", 5), ("automation", 5), ("integration", 5)
    ]
    for pattern, points in actionable_patterns:
        if pattern in text:
            score += points

    # Technical depth indicators (max 30 points)
    technical_patterns = [
        ("github", 10), ("code", 5), ("api", 5), ("sdk", 5),
        ("python", 5), ("javascript", 5), ("typescript", 5),
        ("repository", 5), ("open source", 5), ("documentation", 5)
    ]
    for pattern, points in technical_patterns:
        if pattern in text:
            score += points

    # Tool/resource mentions (max 20 points)
    learning_priorities = project_context.get("learning_priorities", [])
    for priority in learning_priorities:
        if priority.lower() in text:
            score += 10

    return min(100, score)


def calculate_composite_score(relevance, importance, value, tier):
    """
    Calculate weighted composite score.
    """
    # Weight by tier (higher tier = more lenient)
    tier_weights = {
        1: {"relevance": 0.25, "importance": 0.35, "value": 0.40},  # Must-watch tier
        2: {"relevance": 0.30, "importance": 0.30, "value": 0.40},  # High quality tier
        3: {"relevance": 0.40, "importance": 0.25, "value": 0.35}   # Filtered tier
    }

    weights = tier_weights.get(tier, tier_weights[3])

    composite = (
        relevance * weights["relevance"] +
        importance * weights["importance"] +
        value * weights["value"]
    )

    return round(composite, 1)


def should_process_video(composite_score, tier, tier_rules):
    """
    Determine if video should be processed based on score and tier.
    """
    tier_key = f"tier_{tier}"
    rules = tier_rules.get(tier_key, {})

    min_threshold = rules.get("min_score_threshold", 0)

    # Tier 1: Process almost everything
    if tier == 1:
        return composite_score >= min_threshold

    # Tier 2: Process if meets threshold
    if tier == 2:
        return composite_score >= min_threshold

    # Tier 3: Only high-value content
    if tier == 3:
        return composite_score >= min_threshold

    return False


def rank_video(video_file, project_context, tier_rules):
    """
    Rank a single video and return ranking data.
    """
    with open(video_file) as f:
        video_data = yaml.safe_load(f)

    video_id = video_data.get("source", {}).get("id")
    title = video_data.get("source", {}).get("title")
    tier = video_data.get("creator", {}).get("tier", 3)

    print(f"\n📊 Ranking: {title[:60]}...")

    # Calculate scores
    relevance = calculate_relevance_score(video_data, project_context)
    importance = calculate_importance_score(video_data)
    value = calculate_value_score(video_data, project_context)
    composite = calculate_composite_score(relevance, importance, value, tier)

    # Determine if should process
    should_process = should_process_video(composite, tier, tier_rules)

    ranking = {
        "video_id": video_id,
        "ranked_at": datetime.now().isoformat(),
        "scores": {
            "relevance": relevance,
            "importance": importance,
            "value": value,
            "composite": composite
        },
        "decision": {
            "should_process": should_process,
            "tier": tier,
            "reason": "meets_threshold" if should_process else "below_threshold"
        }
    }

    status = "✅ PASS" if should_process else "❌ FILTER"
    print(f"   Relevance: {relevance}/100 | Importance: {importance}/100 | Value: {value}/100")
    print(f"   Composite: {composite}/100 | {status}")

    return ranking, should_process


def update_queue_entry(video_id, ranking):
    """
    Update queue entry with ranking data.
    """
    queue_file = QUEUE_DIR / "pending" / f"{video_id}.yaml"

    if not queue_file.exists():
        print(f"   ⚠️  Queue entry not found for {video_id}")
        return False

    with open(queue_file) as f:
        queue_data = yaml.safe_load(f)

    # Add ranking data
    queue_data["ranking"] = ranking["scores"]
    queue_data["decision"] = ranking["decision"]

    with open(queue_file, "w") as f:
        yaml.dump(queue_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return True


def move_to_filtered(video_id):
    """
    Move queue entry to filtered folder.
    """
    pending_file = QUEUE_DIR / "pending" / f"{video_id}.yaml"
    filtered_file = QUEUE_DIR / "filtered" / f"{video_id}.yaml"

    if pending_file.exists():
        # Load and update status
        with open(pending_file) as f:
            data = yaml.safe_load(f)

        data["status"] = "filtered"
        data["filtered_at"] = datetime.now().isoformat()

        # Save to filtered
        with open(filtered_file, "w") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        # Remove from pending
        pending_file.unlink()


def process_all_unranked(dry_run=False):
    """
    Process all unranked videos in queue/pending.
    """
    project_context = load_project_context()
    tier_rules = load_tier_rules()

    pending_dir = QUEUE_DIR / "pending"
    if not pending_dir.exists():
        print("No pending queue found")
        return

    # Find all queue entries without ranking
    unranked = []
    for queue_file in pending_dir.glob("*.yaml"):
        with open(queue_file) as f:
            data = yaml.safe_load(f)

        if "ranking" not in data:
            unranked.append(queue_file)

    if not unranked:
        print("No unranked videos found")
        return

    print(f"\n{'='*60}")
    print(f"RANKING {len(unranked)} VIDEOS")
    print(f"{'='*60}")

    stats = {"passed": 0, "filtered": 0}

    for queue_file in unranked:
        video_id = queue_file.stem

        # Find the source video file
        source_path = None
        for source_dir in (DATA_DIR / "sources").iterdir():
            video_file = source_dir / "videos" / f"{video_id}.yaml"
            if video_file.exists():
                source_path = video_file
                break

        if not source_path:
            print(f"⚠️  Source file not found for {video_id}")
            continue

        # Rank the video
        ranking, should_process = rank_video(source_path, project_context, tier_rules)

        if not dry_run:
            # Update queue entry
            update_queue_entry(video_id, ranking)

            if should_process:
                stats["passed"] += 1
            else:
                # Move to filtered
                move_to_filtered(video_id)
                stats["filtered"] += 1

            # Log event
            log_event("video_ranked", {
                "video_id": video_id,
                "composite_score": ranking["scores"]["composite"],
                "should_process": should_process
            })

    print(f"\n{'='*60}")
    print("RANKING SUMMARY")
    print(f"{'='*60}")
    print(f"Total ranked: {len(unranked)}")
    if not dry_run:
        print(f"Passed: {stats['passed']}")
        print(f"Filtered: {stats['filtered']}")


def main():
    parser = argparse.ArgumentParser(description="Rank videos by relevance before extraction")
    parser.add_argument("--dry-run", action="store_true", help="Show rankings without updating")
    parser.add_argument("--video", help="Rank specific video by ID")

    args = parser.parse_args()

    if args.video:
        # Rank single video
        project_context = load_project_context()
        tier_rules = load_tier_rules()

        # Find video file
        video_file = None
        for source_dir in (DATA_DIR / "sources").iterdir():
            vf = source_dir / "videos" / f"{args.video}.yaml"
            if vf.exists():
                video_file = vf
                break

        if not video_file:
            print(f"Video {args.video} not found")
            return

        ranking, should_process = rank_video(video_file, project_context, tier_rules)

        if not args.dry_run:
            update_queue_entry(args.video, ranking)
            if not should_process:
                move_to_filtered(args.video)

    else:
        # Process all unranked
        process_all_unranked(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
