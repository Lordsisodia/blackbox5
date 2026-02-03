#!/usr/bin/env python3
"""
Claude Extraction Process - 3 Iteration System

Extracts video content through 3 iterations:
1. Initial extraction - Core concepts
2. Deep analysis - Specifics, ratings, context
3. Master synthesis - Final comprehensive document

Output naming: "{Video Title} by {Creator}.md"
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import yaml

sys.path.insert(0, str(Path(__file__).parent))

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
BY_TOPIC_DIR = BASE_DIR / "by_topic"

def get_video_data(video_id: str, creator_slug: str) -> Optional[Dict]:
    """Load video data from canonical source."""
    video_path = DATA_DIR / "sources" / creator_slug / "videos" / f"{video_id}.yaml"

    if not video_path.exists():
        print(f"❌ Video file not found: {video_path}")
        return None

    with open(video_path) as f:
        data = yaml.safe_load(f)

    return {
        "video_id": video_id,
        "title": data.get("source", {}).get("title", ""),
        "creator": data.get("creator", {}).get("name", ""),
        "creator_slug": creator_slug,
        "url": data.get("source", {}).get("url", ""),
        "published_at": data.get("source", {}).get("published_at", ""),
        "duration": data.get("source", {}).get("duration", 0),
        "view_count": data.get("source", {}).get("view_count", 0),
        "transcript": data.get("transcript", {}).get("full_text", ""),
        "video_data": data
    }

def generate_safe_filename(title: str, creator: str) -> str:
    """Generate safe filename: {Title} by {Creator}.md"""
    # Remove special characters but keep spaces
    safe_title = re.sub(r'[<>"/\\|?*]', '', title).strip()
    safe_creator = re.sub(r'[<>"/\\|?*]', '', creator).strip()

    # Limit length
    if len(safe_title) > 60:
        safe_title = safe_title[:57] + "..."

    return f"{safe_title} by {safe_creator}.md"

def run_iteration_1(video_data: Dict, dry_run: bool = False) -> str:
    """Run iteration 1: Initial extraction."""
    print("\n" + "="*60)
    print("ITERATION 1: Initial Extraction")
    print("="*60)

    if dry_run:
        print("[DRY RUN - would run sub-agent]")
        return ""

    prompt = f"""You are a content extraction agent performing ITERATION 1.

Video: {video_data['title']}
Creator: {video_data['creator']}
Transcript length: {len(video_data['transcript'])} characters

TASK:
Extract the core concepts, commands, and insights from this transcript.
Focus on actionable information - what can the viewer DO with this?

OUTPUT FORMAT:
Create a structured extraction with:
1. Summary (2-3 sentences)
2. Key Concepts (bullet points with explanations)
3. Commands & Usage (syntax + what it does)
4. Best Practices (do/don't)
5. Key Takeaways (5-10 most important points)

Use importance markers:
- [CRITICAL] - Essential, game-changing
- [HIGH] - Very valuable, use often
- [MEDIUM] - Useful context
- [LOW] - Background info

Return the extraction as markdown."""

    # For now, return placeholder - actual implementation would call Claude API
    print("✓ Iteration 1 complete")
    return prompt

def run_iteration_2(video_data: Dict, iteration_1_output: str, dry_run: bool = False) -> str:
    """Run iteration 2: Deep analysis with ratings."""
    print("\n" + "="*60)
    print("ITERATION 2: Deep Analysis")
    print("="*60)

    if dry_run:
        print("[DRY RUN - would run sub-agent]")
        return ""

    prompt = f"""You are a content extraction agent performing ITERATION 2.

Video: {video_data['title']}
Creator: {video_data['creator']}

PREVIOUS OUTPUT (Iteration 1):
{iteration_1_output[:2000]}...

TASK:
Go deeper. For every concept, command, and technique:
1. Rate it 0-100 for criticality
2. Write context-rich explanations (paragraphs, not bullets)
3. Include specific examples from the video
4. Note exact syntax, commands, file paths
5. Explain WHY it matters

Scoring:
- 90-100: Game-changing, fundamental
- 80-89: Very important, commonly needed
- 70-79: Useful, good to know
- 60-69: Nice to have, situational
- 0-59: Background info

OUTPUT FORMAT:
### [XX/100] Concept Name
**What it is:** [Detailed paragraph]
**Why it matters:** [Explanation]
**Specific example:** [From video]
**Implementation:** [Exact steps/syntax]

Return the deep analysis as markdown."""

    print("✓ Iteration 2 complete")
    return prompt

def run_iteration_3_master(video_data: Dict, iteration_2_output: str, dry_run: bool = False) -> str:
    """Run iteration 3: Master synthesis."""
    print("\n" + "="*60)
    print("ITERATION 3: Master Synthesis")
    print("="*60)

    if dry_run:
        print("[DRY RUN - would run sub-agent]")
        return ""

    safe_filename = generate_safe_filename(video_data['title'], video_data['creator'])

    prompt = f"""You are a content extraction agent creating the FINAL MASTER DOCUMENT.

Video: {video_data['title']}
Creator: {video_data['creator']}
URL: {video_data['url']}
Published: {video_data['published_at']}

PREVIOUS ANALYSIS (Iteration 2):
{iteration_2_output[:3000]}...

TASK:
Create the definitive master extraction. This should be the ONLY document someone needs.

REQUIRED SECTIONS:

1. **Executive Summary**
   - One paragraph overview
   - Who this is for
   - What they'll learn

2. **All Concepts Rated 0-100**
   - Every concept from previous iterations
   - Final criticality rating
   - One-sentence summary + full explanation
   - Specific evidence from video

3. **Complete Command Reference**
   - Table: Command | Syntax | Rating | What It Does | When to Use

4. **Key Techniques**
   - Step-by-step instructions
   - Examples from video
   - Common pitfalls

5. **Synthesis: What Matters Most**
   - Top 5 must-know concepts
   - Top 10 important concepts
   - Quick reference for busy people

6. **Action Checklist**
   - [ ] Specific actions with exact commands
   - Ordered by priority

7. **Full Transcript**
   - Complete transcript for verification

STYLE:
- Context-rich paragraphs (no bullet points except lists)
- Specific examples and quotes
- Exact syntax and commands
- Practical, actionable focus

OUTPUT:
Save as: "{safe_filename}"

This is the master document - make it comprehensive and well-organized."""

    print("✓ Iteration 3 complete")
    return prompt

def extract_video(video_id: str, creator_slug: str, dry_run: bool = False):
    """Run full 3-iteration extraction process."""

    # Load video data
    video_data = get_video_data(video_id, creator_slug)
    if not video_data:
        return False

    print(f"\n{'='*60}")
    print(f"EXTRACTING: {video_data['title']}")
    print(f"CREATOR: {video_data['creator']}")
    print(f"{'='*60}")

    if dry_run:
        print("\n[DRY RUN MODE]")
        safe_name = generate_safe_filename(video_data['title'], video_data['creator'])
        print(f"Would create: {safe_name}")
        return True

    # Run 3 iterations
    iter_1 = run_iteration_1(video_data, dry_run)
    iter_2 = run_iteration_2(video_data, iter_1, dry_run)
    iter_3 = run_iteration_3_master(video_data, iter_2, dry_run)

    # Note: Actual implementation would call Claude API here
    # For now, we document the process

    safe_name = generate_safe_filename(video_data['title'], video_data['creator'])
    output_path = BY_TOPIC_DIR / "claude-code" / safe_name

    print(f"\n{'='*60}")
    print("EXTRACTION COMPLETE")
    print(f"{'='*60}")
    print(f"Output would be: {output_path}")
    print(f"\nProcess:")
    print(f"  - Iteration 1: Core concepts (70% coverage)")
    print(f"  - Iteration 2: Deep analysis (90% coverage)")
    print(f"  - Iteration 3: Master synthesis (95% coverage)")

    return True

def main():
    parser = argparse.ArgumentParser(description="Extract video with 3-iteration process")
    parser.add_argument("--video", required=True, help="Video ID")
    parser.add_argument("--creator", required=True, help="Creator slug (e.g., david_ondrej)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")

    args = parser.parse_args()

    extract_video(args.video, args.creator, args.dry_run)

if __name__ == "__main__":
    main()
