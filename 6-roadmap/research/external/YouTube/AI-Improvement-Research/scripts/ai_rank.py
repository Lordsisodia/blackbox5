#!/usr/bin/env python3
"""
AI Improvement Research - AI-Powered Video Ranking
Uses GLM API to rank borderline videos based on title + description only

This is the second pass of the hybrid ranking system:
1. Keyword ranking (fast, free) - already done by rank.py
2. AI ranking (accurate, cheap) - this script for borderline videos

Only processes videos with keyword scores 20-60 (borderline)
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import yaml

# Try to import OpenAI client for GLM
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: openai package not available. Install with: pip install openai")

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = BASE_DIR / "config"
QUEUE_DIR = BASE_DIR / "queue"
TIMELINE_DIR = BASE_DIR / "timeline"

# GLM API Configuration
GLM_BASE_URL = "https://open.bigmodel.cn/api/paas/v4/"
GLM_MODEL = "glm-4-flash"  # Cheapest model, good for ranking


def get_glm_client():
    """Initialize GLM API client."""
    api_key = os.environ.get("GLM_API_KEY")
    if not api_key:
        print("❌ GLM_API_KEY not found in environment variables")
        print("   Set it with: export GLM_API_KEY='your-key-here'")
        return None

    if not OPENAI_AVAILABLE:
        print("❌ OpenAI package not installed")
        print("   Install with: pip install openai")
        return None

    return OpenAI(
        api_key=api_key,
        base_url=GLM_BASE_URL
    )


def load_project_context():
    """Load project context for relevance scoring."""
    sources_file = CONFIG_DIR / "sources.yaml"
    with open(sources_file) as f:
        for doc in yaml.safe_load_all(f):
            if doc and "project_context" in doc:
                return doc.get("project_context", {})
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


def build_ranking_prompt(video_data, project_context, keyword_scores):
    """Build prompt for GLM API ranking."""

    title = video_data.get("source", {}).get("title", "")
    description = video_data.get("source", {}).get("description", "")
    creator = video_data.get("creator", {}).get("name", "")
    tier = video_data.get("creator", {}).get("tier", 3)

    # Get user's active projects
    projects = project_context.get("active_projects", [])
    project_names = [p.get("name", "") for p in projects]
    learning_priorities = project_context.get("learning_priorities", [])

    prompt = f"""You are an expert at evaluating AI/tech video content for relevance and value.

Your task: Rank this video based on its title and description for someone researching AI tools and workflows.

## VIDEO INFORMATION
Title: {title}
Creator: {creator} (Tier {tier}/3, where 1=top expert, 3=general creator)
Description: {description[:800]}...

## USER'S PROJECTS (rank higher if relevant to these)
{chr(10).join(f"- {p}" for p in project_names)}

## LEARNING PRIORITIES (rank higher if matches)
{chr(10).join(f"- {p}" for p in learning_priorities)}

## KEYWORD SCORES (from first-pass analysis)
- Relevance: {keyword_scores.get('relevance', 0)}/100
- Importance: {keyword_scores.get('importance', 0)}/100
- Value: {keyword_scores.get('value', 0)}/100
- Composite: {keyword_scores.get('composite', 0)}/100

## RANKING CRITERIA
Score each dimension 0-100:

1. **RELEVANCE** - How relevant is this to the user's projects?
   - 90-100: Directly about Claude Code, MCP, AI agents, or vibe coding
   - 70-89: Related to AI tools, workflows, or development
   - 50-69: General AI/tech content
   - 0-49: Not relevant to user's focus

2. **IMPORTANCE** - How significant is this content?
   - 90-100: From top expert (Tier 1), trending topic, or major announcement
   - 70-89: Solid creator, good engagement, timely
   - 50-69: Average creator or older content
   - 0-49: Low engagement or outdated

3. **VALUE** - How actionable and useful is this?
   - 90-100: Step-by-step tutorial, code examples, implementation guide
   - 70-89: Good explanation with practical takeaways
   - 50-69: Overview or news without deep implementation details
   - 0-49: Vague, theoretical, or entertainment-focused

4. **NOVELTY** - How new/unique is this information?
   - 90-100: Cutting edge, new technique, or unique insight
   - 70-89: Recent development with good synthesis
   - 50-69: Known information but well presented
   - 0-49: Repackaged or outdated content

## OUTPUT FORMAT
Respond with ONLY a JSON object in this exact format:
```json
{{
  "relevance": 85,
  "importance": 75,
  "value": 90,
  "novelty": 70,
  "composite": 82,
  "reasoning": "Brief explanation of why these scores were given",
  "should_process": true,
  "key_topics": ["topic1", "topic2"]
}}
```

The "should_process" field should be true if composite >= 65, false otherwise.
Be honest and critical - most videos should score 40-70, only exceptional ones 80+.
"""

    return prompt


def rank_with_ai(client, video_data, project_context, keyword_scores):
    """Use GLM API to rank a video."""

    prompt = build_ranking_prompt(video_data, project_context, keyword_scores)

    try:
        response = client.chat.completions.create(
            model=GLM_MODEL,
            messages=[
                {"role": "system", "content": "You are a content evaluation expert. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Lower = more consistent
            max_tokens=500
        )

        # Parse JSON response
        content = response.choices[0].message.content

        # Extract JSON from markdown code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]

        result = json.loads(content.strip())

        # Add metadata
        result["ranked_by"] = "ai"
        result["model"] = GLM_MODEL
        result["ranked_at"] = datetime.now().isoformat()
        result["cost_estimate"] = "~0.002 CNY"  # GLM-4-flash is very cheap

        return result

    except Exception as e:
        print(f"   ❌ AI ranking failed: {e}")
        return None


def update_queue_with_ai_ranking(video_id, ai_ranking, keyword_scores):
    """Update queue entry with AI-enhanced ranking."""
    queue_file = QUEUE_DIR / "pending" / f"{video_id}.yaml"

    if not queue_file.exists():
        return False

    with open(queue_file) as f:
        queue_data = yaml.safe_load(f)

    # Store both keyword and AI scores for comparison
    queue_data["ranking"] = {
        "ai": {
            "relevance": ai_ranking.get("relevance", 0),
            "importance": ai_ranking.get("importance", 0),
            "value": ai_ranking.get("value", 0),
            "novelty": ai_ranking.get("novelty", 0),
            "composite": ai_ranking.get("composite", 0),
            "reasoning": ai_ranking.get("reasoning", ""),
            "key_topics": ai_ranking.get("key_topics", []),
            "model": ai_ranking.get("model", GLM_MODEL),
            "ranked_at": ai_ranking.get("ranked_at", datetime.now().isoformat())
        },
        "keyword": keyword_scores,  # Keep original keyword scores
        "final_composite": ai_ranking.get("composite", 0)  # Use AI composite as final
    }

    queue_data["decision"] = {
        "should_process": ai_ranking.get("should_process", False),
        "method": "ai_ranked",
        "reason": ai_ranking.get("reasoning", "")[:100]  # Truncate for storage
    }

    with open(queue_file, "w") as f:
        yaml.dump(queue_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return True


def get_borderline_videos():
    """Get videos with keyword scores between 20-60 (borderline)."""
    pending_dir = QUEUE_DIR / "pending"
    borderline = []

    if not pending_dir.exists():
        return borderline

    for queue_file in pending_dir.glob("*.yaml"):
        with open(queue_file) as f:
            data = yaml.safe_load(f)

        # Skip if already AI-ranked
        if data.get("ranking", {}).get("ai"):
            continue

        # Check if has keyword ranking
        keyword_scores = data.get("ranking", {})
        if not keyword_scores:
            continue

        # Get composite score (handle both old and new formats)
        if "composite" in keyword_scores:
            composite = keyword_scores["composite"]
        elif "final_composite" in keyword_scores:
            composite = keyword_scores["final_composite"]
        else:
            continue

        # Borderline: 20-60 (needs AI review)
        # Below 20: already filtered by rank.py
        # Above 60: already approved by rank.py
        if 20 <= composite <= 60:
            borderline.append({
                "video_id": queue_file.stem,
                "keyword_scores": keyword_scores,
                "queue_file": queue_file
            })

    return borderline


def process_borderline_videos(dry_run=False):
    """Process all borderline videos with AI ranking."""
    client = get_glm_client()
    if not client:
        print("❌ Cannot initialize GLM client")
        return

    project_context = load_project_context()
    borderline = get_borderline_videos()

    if not borderline:
        print("No borderline videos found for AI ranking")
        print("(Videos with keyword scores 20-60)")
        return

    print(f"\n{'='*60}")
    print(f"AI RANKING {len(borderline)} BORDERLINE VIDEOS")
    print(f"{'='*60}")
    print(f"Using model: {GLM_MODEL}")
    print(f"Estimated cost: ~{len(borderline) * 0.002:.3f} CNY")
    print()

    stats = {"upgraded": 0, "downgraded": 0, "unchanged": 0}

    for item in borderline:
        video_id = item["video_id"]
        keyword_scores = item["keyword_scores"]

        # Find source video file
        source_path = None
        for source_dir in (DATA_DIR / "sources").iterdir():
            video_file = source_dir / "videos" / f"{video_id}.yaml"
            if video_file.exists():
                source_path = video_file
                break

        if not source_path:
            print(f"⚠️  Source not found for {video_id}")
            continue

        with open(source_path) as f:
            video_data = yaml.safe_load(f)

        title = video_data.get("source", {}).get("title", "")[:60]
        print(f"\n🤖 Ranking: {title}...")
        print(f"   Keyword composite: {keyword_scores.get('composite', 0)}")

        if dry_run:
            print("   [DRY RUN - skipping API call]")
            continue

        # Call AI for ranking
        ai_ranking = rank_with_ai(client, video_data, project_context, keyword_scores)

        if not ai_ranking:
            print("   ❌ Failed to get AI ranking")
            continue

        # Update queue
        update_queue_with_ai_ranking(video_id, ai_ranking, keyword_scores)

        # Show results
        old_score = keyword_scores.get("composite", 0)
        new_score = ai_ranking.get("composite", 0)
        delta = new_score - old_score

        status = "⬆️ UP" if delta > 5 else "⬇️ DOWN" if delta < -5 else "➡️ SAME"
        print(f"   AI composite: {new_score} ({delta:+.0f}) {status}")
        print(f"   Reasoning: {ai_ranking.get('reasoning', '')[:80]}...")

        # Track stats
        if delta > 5:
            stats["upgraded"] += 1
        elif delta < -5:
            stats["downgraded"] += 1
        else:
            stats["unchanged"] += 1

        # Log event
        log_event("video_ai_ranked", {
            "video_id": video_id,
            "keyword_composite": old_score,
            "ai_composite": new_score,
            "delta": delta,
            "should_process": ai_ranking.get("should_process", False)
        })

    print(f"\n{'='*60}")
    print("AI RANKING SUMMARY")
    print(f"{'='*60}")
    print(f"Total processed: {len(borderline)}")
    print(f"Upgraded: {stats['upgraded']}")
    print(f"Downgraded: {stats['downgraded']}")
    print(f"Unchanged: {stats['unchanged']}")


def show_ranking_comparison():
    """Show comparison between keyword and AI rankings."""
    pending_dir = QUEUE_DIR / "pending"

    if not pending_dir.exists():
        print("No pending videos")
        return

    print(f"\n{'='*80}")
    print("RANKING COMPARISON (Keyword vs AI)")
    print(f"{'='*80}")
    print(f"{'Video ID':<15} {'Keyword':<10} {'AI':<10} {'Delta':<10} {'Status':<10}")
    print("-" * 80)

    for queue_file in sorted(pending_dir.glob("*.yaml")):
        with open(queue_file) as f:
            data = yaml.safe_load(f)

        ranking = data.get("ranking", {})

        # Skip if no AI ranking
        if "ai" not in ranking:
            continue

        video_id = queue_file.stem[:12]
        keyword_score = ranking.get("keyword", {}).get("composite", 0)
        ai_score = ranking["ai"].get("composite", 0)
        delta = ai_score - keyword_score
        should_process = data.get("decision", {}).get("should_process", False)

        status = "✅ PASS" if should_process else "❌ SKIP"

        print(f"{video_id:<15} {keyword_score:<10.1f} {ai_score:<10.1f} {delta:+.1f}      {status}")


def main():
    parser = argparse.ArgumentParser(description="AI-powered video ranking for borderline videos")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be ranked without calling API")
    parser.add_argument("--compare", action="store_true", help="Show keyword vs AI ranking comparison")
    parser.add_argument("--video", help="Rank specific video by ID")

    args = parser.parse_args()

    if args.compare:
        show_ranking_comparison()
        return

    if args.video:
        # Rank single video
        client = get_glm_client()
        if not client:
            return

        project_context = load_project_context()

        # Find video
        source_path = None
        for source_dir in (DATA_DIR / "sources").iterdir():
            vf = source_dir / "videos" / f"{args.video}.yaml"
            if vf.exists():
                source_path = vf
                break

        if not source_path:
            print(f"Video {args.video} not found")
            return

        # Load queue data for keyword scores
        queue_file = QUEUE_DIR / "pending" / f"{args.video}.yaml"
        keyword_scores = {}
        if queue_file.exists():
            with open(queue_file) as f:
                qd = yaml.safe_load(f)
                keyword_scores = qd.get("ranking", {})

        with open(source_path) as f:
            video_data = yaml.safe_load(f)

        print(f"Ranking: {video_data.get('source', {}).get('title', '')}")
        print(f"Keyword scores: {keyword_scores}")

        if not args.dry_run:
            ai_ranking = rank_with_ai(client, video_data, project_context, keyword_scores)
            if ai_ranking:
                print(f"\nAI Ranking: {json.dumps(ai_ranking, indent=2)}")
                update_queue_with_ai_ranking(args.video, ai_ranking, keyword_scores)
    else:
        # Process all borderline videos
        process_borderline_videos(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
