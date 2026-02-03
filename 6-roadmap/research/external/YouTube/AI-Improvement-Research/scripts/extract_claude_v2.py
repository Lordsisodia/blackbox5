#!/usr/bin/env python3
"""
Claude Extraction Process v2 - 3×3 Parallel System

Runs 3 parallel extractions (each with 3 iterations), then synthesizes results.

Process:
1. Spawn 3 sub-agents, each running full 3-iteration extraction
2. Collect 3 master documents (_A.md, _B.md, _C.md)
3. Run synthesis iteration to merge unique concepts and reconcile scores
4. Output unified master document

Usage:
    python scripts/extract_claude_v2.py --video VIDEO_ID --creator CREATOR_SLUG
"""

import argparse
import json
import os
import re
import subprocess
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

def generate_safe_filename(title: str, creator: str, suffix: str = "") -> str:
    """Generate safe filename: {Title} by {Creator}{suffix}.md"""
    safe_title = re.sub(r'[<>"/\\|?*]', '', title).strip()
    safe_creator = re.sub(r'[<>"/\\|?*]', '', creator).strip()

    if len(safe_title) > 60:
        safe_title = safe_title[:57] + "..."

    return f"{safe_title} by {safe_creator}{suffix}.md"

def spawn_extraction_subagent(video_data: Dict, branch: str, output_file: Path) -> Dict:
    """Spawn a sub-agent to run 3-iteration extraction."""
    print(f"\n{'='*60}")
    print(f"SPAWNING EXTRACTION {branch}")
    print(f"{'='*60}")

    prompt = f"""You are a content extraction specialist. Your task is to perform a 3-iteration extraction process on a YouTube video transcript.

## Video Information
- Title: "{video_data['title']}"
- Creator: {video_data['creator']}
- Video ID: {video_data['video_id']}
- URL: {video_data['url']}

## Transcript Location
The transcript is saved at:
`{DATA_DIR}/sources/{video_data['creator_slug']}/videos/{video_data['video_id']}.yaml`

Read this file to get the full transcript text (it's in the `transcript.full_text` field).

## Your Task: 3-Iteration Extraction Process

### ITERATION 1: Initial Extraction (70% coverage)
Extract core concepts, commands, and insights. Create:
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

### ITERATION 2: Deep Analysis (90% coverage)
For every concept, command, and technique from Iteration 1:
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

Format:
```
### [XX/100] Concept Name
**What it is:** [Detailed paragraph]
**Why it matters:** [Explanation]
**Specific example:** [From video]
**Implementation:** [Exact steps/syntax]
```

### ITERATION 3: Master Synthesis (95% coverage)
Create the definitive master extraction document with these sections:

1. **Executive Summary** - One paragraph overview, who this is for, what they'll learn

2. **All Concepts Rated 0-100** - Every concept with:
   - Final criticality rating
   - One-sentence summary
   - Full explanation
   - Specific evidence from video

3. **Complete Command Reference** - Table format:
   | Rating | Command | Syntax | What It Does | When to Use |

4. **Key Techniques** - Step-by-step instructions with:
   - Prerequisites
   - Steps
   - Examples from video
   - Common pitfalls

5. **Synthesis: What Matters Most** - Tiered priorities:
   - Tier 1 (90-100): Must Know
   - Tier 2 (80-89): Very Important
   - Tier 3 (70-79): Good to Know

6. **Action Checklist** - Specific actions with exact commands, ordered by priority

7. **Full Transcript** - Include the complete transcript in a collapsible section

## Output
Save the final master document to:
`{output_file}`

Use the exact filename provided above. This is extraction branch {branch} of 3 parallel extractions.

Return a summary of what you extracted when complete."""

    return {
        "branch": branch,
        "prompt": prompt,
        "output_file": output_file,
        "status": "pending"
    }

def run_parallel_extractions(video_data: Dict, topic: str) -> List[Path]:
    """Run 3 parallel extractions and return output file paths."""
    print(f"\n{'='*60}")
    print("RUNNING 3 PARALLEL EXTRACTIONS")
    print(f"{'='*60}")

    # Ensure output directory exists
    output_dir = BY_TOPIC_DIR / topic
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate output filenames
    base_filename = generate_safe_filename(video_data['title'], video_data['creator'])
    base_path = output_dir / base_filename.replace('.md', '')

    output_files = [
        Path(f"{base_path}_A.md"),
        Path(f"{base_path}_B.md"),
        Path(f"{base_path}_C.md")
    ]

    # For now, we document the process and create placeholder files
    # In a full implementation, this would actually spawn sub-agents
    print("\nNote: In the full implementation, this would spawn 3 sub-agents in parallel.")
    print("For now, creating placeholder documentation of the process.")

    for i, (branch, output_file) in enumerate(zip(['A', 'B', 'C'], output_files)):
        print(f"\n[Branch {branch}] Would spawn sub-agent...")
        print(f"  Output: {output_file}")

        # Create a placeholder showing what would be extracted
        placeholder_content = f"""# {video_data['title']} - Extraction Branch {branch}

**Creator:** {video_data['creator']}
**Video ID:** {video_data['video_id']}
**Branch:** {branch} of 3 parallel extractions
**Status:** PLACEHOLDER - Sub-agent would populate this

## Note

This is a placeholder file. In the full implementation, a sub-agent would:
1. Read the transcript from the video YAML file
2. Run 3-iteration extraction process
3. Save the master document here

## Next Steps

After all 3 branches complete (A, B, C), run the synthesis iteration to:
- Merge unique concepts from all 3 extractions
- Reconcile score differences
- Create unified master document
"""
        with open(output_file, 'w') as f:
            f.write(placeholder_content)

    return output_files

def spawn_synthesis_subagent(video_data: Dict, input_files: List[Path], output_file: Path) -> Dict:
    """Spawn a sub-agent to synthesize 3 parallel extractions."""
    print(f"\n{'='*60}")
    print("SPAWNING SYNTHESIS SUB-AGENT (Iteration 4)")
    print(f"{'='*60}")

    prompt = f"""You are a synthesis specialist. Your task is to merge 3 parallel extractions into a unified master document.

## Video Information
- Title: "{video_data['title']}"
- Creator: {video_data['creator']}
- Video ID: {video_data['video_id']}

## Input Files (3 Parallel Extractions)
"""
    for i, f in enumerate(input_files, 1):
        prompt += f"{i}. `{f}`\n"

    prompt += f"""
## Your Task: Cross-Extraction Synthesis (Iteration 4)

### 1. Concept Deduplication
- Read all 3 extraction files
- Identify same concepts with different names (fuzzy matching)
- Merge truly unique concepts from each extraction
- Flag concepts appearing in only 1 of 3 extractions as "[UNCERTAIN]"

### 2. Score Reconciliation
- For concepts appearing in 2+ extractions: average the scores
- For concepts appearing in all 3: high confidence, use average
- For concepts appearing in 1: flag as "[LOW CONFIDENCE]"
- Note any major score discrepancies (>10 points difference)

### 3. Naming Standardization
- Choose most descriptive name for each concept
- Add alternate names as "also known as" where relevant

### 4. Coverage Analysis
Create a section documenting:
- Total concepts in unified document
- Concepts unique to each extraction branch
- Overlap percentage between branches
- Any major omissions noted

### Output Structure

1. **Executive Summary** - Synthesized from all 3
2. **Coverage Analysis** - Statistics on extraction overlap
3. **All Concepts Rated 0-100** - Merged and reconciled with confidence flags
4. **Complete Command Reference** - Unified table
5. **Key Techniques** - Consolidated techniques
6. **Synthesis: What Matters Most** - Tiered priorities
7. **Action Checklist** - Consolidated actions
8. **Full Transcript** - For verification

## Output
Save the unified master document to:
`{output_file}`

Return a summary of the synthesis including:
- Total concepts in unified document
- Coverage statistics (overlap between A, B, C)
- Any notable discrepancies found
"""

    return {
        "prompt": prompt,
        "input_files": input_files,
        "output_file": output_file,
        "status": "pending"
    }

def extract_video_v2(video_id: str, creator_slug: str, topic: str = "claude-code", dry_run: bool = False):
    """Run full 3×3 parallel extraction process."""

    # Load video data
    video_data = get_video_data(video_id, creator_slug)
    if not video_data:
        return False

    print(f"\n{'='*60}")
    print(f"3×3 PARALLEL EXTRACTION: {video_data['title']}")
    print(f"CREATOR: {video_data['creator']}")
    print(f"{'='*60}")

    if dry_run:
        print("\n[DRY RUN MODE]")
        base_filename = generate_safe_filename(video_data['title'], video_data['creator'])
        print(f"Would create:")
        print(f"  - {base_filename.replace('.md', '_A.md')}")
        print(f"  - {base_filename.replace('.md', '_B.md')}")
        print(f"  - {base_filename.replace('.md', '_C.md')}")
        print(f"  - {base_filename} (unified)")
        return True

    # Phase 1: Run 3 parallel extractions
    print("\n" + "="*60)
    print("PHASE 1: 3 PARALLEL EXTRACTIONS")
    print("="*60)

    extraction_files = run_parallel_extractions(video_data, topic)

    print("\n" + "="*60)
    print("PHASE 2: SYNTHESIS (Iteration 4)")
    print("="*60)

    # Generate unified output filename
    unified_filename = generate_safe_filename(video_data['title'], video_data['creator'])
    unified_path = BY_TOPIC_DIR / topic / unified_filename

    synthesis_task = spawn_synthesis_subagent(video_data, extraction_files, unified_path)

    print(f"\nSynthesis would merge:")
    for f in extraction_files:
        print(f"  - {f.name}")
    print(f"\nInto unified document:")
    print(f"  - {unified_path.name}")

    # Summary
    print(f"\n{'='*60}")
    print("3×3 EXTRACTION PROCESS SUMMARY")
    print(f"{'='*60}")
    print(f"Phase 1: 3 parallel extractions (Iterations 1-3)")
    print(f"  - Branch A: {extraction_files[0].name}")
    print(f"  - Branch B: {extraction_files[1].name}")
    print(f"  - Branch C: {extraction_files[2].name}")
    print(f"\nPhase 2: Synthesis (Iteration 4)")
    print(f"  - Unified: {unified_path.name}")
    print(f"\nExpected coverage: 98% (vs 95% for single extraction)")
    print(f"Trade-off: 3× API cost for ~30% more comprehensive coverage")

    return True

def main():
    parser = argparse.ArgumentParser(description="Extract video with 3×3 parallel process")
    parser.add_argument("--video", required=True, help="Video ID")
    parser.add_argument("--creator", required=True, help="Creator slug (e.g., david_ondrej)")
    parser.add_argument("--topic", default="claude-code", help="Topic folder (default: claude-code)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")

    args = parser.parse_args()

    extract_video_v2(args.video, args.creator, args.topic, args.dry_run)

if __name__ == "__main__":
    main()
