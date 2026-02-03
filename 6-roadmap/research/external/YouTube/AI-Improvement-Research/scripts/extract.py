#!/usr/bin/env python3
"""
AI Improvement Research - Stage 4: Extract Insights
Processes transcripts with Claude to extract valuable insights into organized markdown files.

Organizes content by:
- Topics (MCPs, Claude Code, AI Agents, etc.)
- Tools mentioned
- Techniques covered
- Code examples
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import yaml

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
QUEUE_DIR = BASE_DIR / "queue"
OUTPUT_DIR = BASE_DIR / "output"
TIMELINE_DIR = BASE_DIR / "timeline"

# Topic definitions for organization
TOPICS = {
    "mcp": {
        "name": "MCP (Model Context Protocol)",
        "patterns": [r"\bmcp\b", r"model context protocol", r"mcp server", r"mcp client"],
        "folder": "mcps"
    },
    "claude_code": {
        "name": "Claude Code",
        "patterns": [r"\bclaude code\b", r"claude-code", r"claude.?code\b"],
        "folder": "claude-code"
    },
    "ai_agents": {
        "name": "AI Agents",
        "patterns": [r"\bai agents?\b", r"\bagentic\b", r"agent framework", r"autonomous agent"],
        "folder": "ai-agents"
    },
    "voice_ai": {
        "name": "Voice AI",
        "patterns": [r"\bvoice ai\b", r"\bvoice agent\b", r"text.?to.?speech", r"speech.?to.?text"],
        "folder": "voice-ai"
    },
    "llm_engineering": {
        "name": "LLM Engineering",
        "patterns": [r"\bllm\b", r"large language model", r"prompt engineering", r"fine.?tuning"],
        "folder": "llm-engineering"
    },
    "coding_tools": {
        "name": "Coding Tools & IDEs",
        "patterns": [r"\bide\b", r"cursor\b", r"windsurf", r"github copilot", r"code editor"],
        "folder": "coding-tools"
    },
    "n8n": {
        "name": "n8n Workflows",
        "patterns": [r"\bn8n\b", r"workflow automation"],
        "folder": "n8n"
    },
    "supabase": {
        "name": "Supabase",
        "patterns": [r"\bsupabase\b", r"postgresql", r"postgres"],
        "folder": "supabase"
    },
    "deployment": {
        "name": "Deployment & Infrastructure",
        "patterns": [r"\bdeploy\b", r"\bdocker\b", r"\bkubernetes\b", r"\bfly\.io\b", r"\bvercel\b"],
        "folder": "deployment"
    },
    "business_automation": {
        "name": "Business Automation",
        "patterns": [r"\bsaas\b", r"\bb2b\b", r"automation", r"workflow"],
        "folder": "business-automation"
    }
}


def ensure_directories():
    """Create output directory structure."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for topic in TOPICS.values():
        (OUTPUT_DIR / topic["folder"]).mkdir(exist_ok=True)
    (OUTPUT_DIR / "general").mkdir(exist_ok=True)
    (OUTPUT_DIR / "projects").mkdir(exist_ok=True)


def log_event(event_type: str, data: dict):
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


def get_pending_videos():
    """Get videos ready for extraction."""
    pending = []

    for queue_file in (QUEUE_DIR / "pending").glob("*.yaml"):
        with open(queue_file) as f:
            data = yaml.safe_load(f)

        # Check if already extracted or not ready
        status = data.get("status", "")
        if status == "extracted":
            continue

        # Get video data
        source_path = data.get("source_path", "")
        # Fix double data/ path issue
        if source_path.startswith("data/"):
            source_path = BASE_DIR / source_path
        else:
            source_path = DATA_DIR / source_path
        if not source_path.exists():
            continue

        with open(source_path) as f:
            video_data = yaml.safe_load(f)

        # Check if transcript exists
        transcript = video_data.get("transcript", {})
        if not transcript.get("full_text"):
            continue

        pending.append({
            "video_id": data.get("video_id"),
            "title": data.get("title", ""),
            "creator": data.get("creator", ""),
            "url": data.get("url", ""),
            "source_path": source_path,
            "queue_file": queue_file,
            "transcript": transcript,
            "video_data": video_data
        })

    return pending


def detect_topics(text: str) -> List[str]:
    """Detect which topics are covered in the text."""
    text_lower = text.lower()
    detected = []

    for topic_key, topic_info in TOPICS.items():
        for pattern in topic_info["patterns"]:
            if re.search(pattern, text_lower, re.IGNORECASE):
                detected.append(topic_key)
                break

    return detected if detected else ["general"]


def extract_tools_mentioned(text: str) -> List[Dict]:
    """Extract tool mentions from transcript."""
    tools = []

    # Common AI/development tools to look for
    tool_patterns = {
        "Claude Code": r"\bclaude code\b|\bclaude-code\b",
        "Claude": r"\bclaude\b(?!\s+code)",
        "Cursor": r"\bcursor\b",
        "Windsurf": r"\bwindsurf\b",
        "GitHub Copilot": r"\bgithub copilot\b|\bcopilot\b",
        "Vapi": r"\bvapi\b",
        "n8n": r"\bn8n\b",
        "Supabase": r"\bsupabase\b",
        "OpenAI": r"\bopenai\b|\bgpt-4\b|\bgpt4\b",
        "Anthropic": r"\banthropic\b",
        "LangChain": r"\blangchain\b",
        "LlamaIndex": r"\bellamaindex\b",
        "Pinecone": r"\bpinecone\b",
        "Weaviate": r"\bweaviate\b",
        "Docker": r"\bdocker\b",
        "Kubernetes": r"\bkubernetes\b|\bk8s\b",
        "Fly.io": r"\bfly\.io\b",
        "Vercel": r"\bvercel\b",
        "Railway": r"\brailway\b",
        "Render": r"\brender\b",
        "Next.js": r"\bnext\.?js\b",
        "React": r"\breact\b(?!\s*to)",
        "Express": r"\bexpress\b(?!\s+server)",
        "FastAPI": r"\bfastapi\b",
        "Django": r"\bdjango\b",
        "Flask": r"\bflask\b",
        "Node.js": r"\bnode\.?js\b",
        "Python": r"\bpython\b",
        "TypeScript": r"\btypescript\b",
        "JavaScript": r"\bjavascript\b|\bjs\b",
        "MCP": r"\bmcp\b|\bmodel context protocol\b",
        "ElevenLabs": r"\belevenlabs\b|\b11labs\b",
        "Twilio": r"\btwilio\b",
    }

    text_lower = text.lower()
    for tool_name, pattern in tool_patterns.items():
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        if matches:
            # Count unique mentions (not duplicates)
            count = len(set(m.lower() if isinstance(m, str) else str(m).lower() for m in matches))
            tools.append({
                "name": tool_name,
                "mentions": count
            })

    return sorted(tools, key=lambda x: x["mentions"], reverse=True)


def extract_code_snippets(text: str) -> List[Dict]:
    """Extract code snippets from transcript."""
    snippets = []

    # Look for code blocks or inline code mentions
    code_patterns = [
        (r'`([^`]+)`', 'inline'),
        (r'```(\w+)?\n(.*?)```', 'block'),
    ]

    for pattern, snippet_type in code_patterns:
        matches = re.finditer(pattern, text, re.DOTALL)
        for match in matches:
            if snippet_type == 'block':
                language = match.group(1) or 'text'
                code = match.group(2).strip()
            else:
                language = 'inline'
                code = match.group(1).strip()

            if len(code) > 10:  # Only meaningful snippets
                snippets.append({
                    "type": snippet_type,
                    "language": language,
                    "code": code[:500]  # Limit length
                })

    return snippets[:10]  # Max 10 snippets


def generate_extraction_prompt(transcript: str, title: str, creator: str) -> str:
    """Generate prompt for Claude to extract insights."""
    return f"""Analyze this YouTube video transcript and extract structured insights.

Video: {title}
Creator: {creator}

Transcript:
{transcript[:15000]}  # First 15k chars to stay within context

Extract and return ONLY a JSON object with this structure:
{{
    "summary": "2-3 sentence summary of what this video teaches",
    "key_insights": [
        "Specific actionable insight 1",
        "Specific actionable insight 2",
        ...
    ],
    "tools_covered": [
        {{"name": "Tool name", "description": "What it does", "use_case": "How it's used in video"}}
    ],
    "techniques": [
        {{"name": "Technique name", "description": "What it is", "steps": ["step 1", "step 2"]}}
    ],
    "code_examples": [
        {{"description": "What the code does", "code": "code snippet"}}
    ],
    "resources": [
        {{"type": "link|repo|doc", "url": "URL mentioned", "description": "What it's for"}}
    ],
    "difficulty": "beginner|intermediate|advanced",
    "prerequisites": ["skill or tool needed"],
    "project_ideas": ["Project you could build based on this"]
}}

Focus on:
1. Actionable information (can the viewer DO something with this?)
2. Specific tools and techniques mentioned
3. Step-by-step processes explained
4. Code examples or implementation details
5. Links to resources mentioned

Return ONLY the JSON, no markdown formatting."""


def extract_with_claude(transcript: str, title: str, creator: str) -> Optional[Dict]:
    """Use Claude to extract structured insights from transcript."""
    try:
        import anthropic

        client = anthropic.Anthropic()

        prompt = generate_extraction_prompt(transcript, title, creator)

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            temperature=0.2,
            system="You are an expert at analyzing technical content and extracting structured, actionable insights. Be thorough and specific.",
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse JSON response
        import json
        content = response.content[0].text

        # Try to extract JSON if wrapped in markdown
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]

        return json.loads(content.strip())

    except Exception as e:
        print(f"    Claude extraction failed: {e}")
        return None


def create_extraction_template(video_data: Dict, extraction: Dict, topics: List[str]) -> str:
    """Create markdown file from extraction."""
    video = video_data["video_data"]
    transcript = video_data["transcript"]
    source = video.get("source", {})
    creator = video.get("creator", {})

    # Build frontmatter
    frontmatter = f"""---
video_id: {source.get('id')}
title: "{source.get('title', '')}"
creator: {creator.get('name', '')}
creator_tier: {creator.get('tier', 3)}
url: {source.get('url', '')}
published_at: {source.get('published_at', '')}
duration: {source.get('duration', 0)}
view_count: {source.get('view_count', 0)}
topics: {topics}
tools_mentioned:
"""

    # Add tools
    for tool in extraction.get("tools_covered", []):
        frontmatter += f"  - {tool.get('name', '')}\n"

    frontmatter += f"difficulty: {extraction.get('difficulty', 'intermediate')}\n"
    frontmatter += f"extracted_at: {datetime.now().isoformat()}\n"
    frontmatter += "---\n\n"

    # Build content
    content = f"# {source.get('title', '')}\n\n"
    content += f"**Creator:** {creator.get('name', '')}  \n"
    content += f"**Video:** [{source.get('url', '')}]({source.get('url', '')})  \n"
    content += f"**Published:** {source.get('published_at', '')}  \n\n"

    # Summary
    content += "## Summary\n\n"
    content += f"{extraction.get('summary', 'No summary available.')}\n\n"

    # Key Insights
    if extraction.get("key_insights"):
        content += "## Key Insights\n\n"
        for insight in extraction["key_insights"]:
            content += f"- {insight}\n"
        content += "\n"

    # Tools Covered
    if extraction.get("tools_covered"):
        content += "## Tools Covered\n\n"
        for tool in extraction["tools_covered"]:
            content += f"### {tool.get('name', '')}\n"
            content += f"{tool.get('description', '')}\n\n"
            if tool.get("use_case"):
                content += f"**Use Case:** {tool['use_case']}\n\n"

    # Techniques
    if extraction.get("techniques"):
        content += "## Techniques\n\n"
        for technique in extraction["techniques"]:
            content += f"### {technique.get('name', '')}\n"
            content += f"{technique.get('description', '')}\n\n"
            if technique.get("steps"):
                content += "**Steps:**\n"
                for i, step in enumerate(technique["steps"], 1):
                    content += f"{i}. {step}\n"
                content += "\n"

    # Code Examples
    if extraction.get("code_examples"):
        content += "## Code Examples\n\n"
        for example in extraction["code_examples"]:
            content += f"### {example.get('description', 'Code Example')}\n\n"
            content += f"```\n{example.get('code', '')}\n```\n\n"

    # Resources
    if extraction.get("resources"):
        content += "## Resources Mentioned\n\n"
        for resource in extraction["resources"]:
            content += f"- [{resource.get('description', resource.get('url', ''))}]({resource.get('url', '')})\n"
        content += "\n"

    # Prerequisites
    if extraction.get("prerequisites"):
        content += "## Prerequisites\n\n"
        for prereq in extraction["prerequisites"]:
            content += f"- {prereq}\n"
        content += "\n"

    # Project Ideas
    if extraction.get("project_ideas"):
        content += "## Project Ideas\n\n"
        for idea in extraction["project_ideas"]:
            content += f"- {idea}\n"
        content += "\n"

    # Full transcript (collapsed)
    content += "## Full Transcript\n\n"
    content += "<details>\n<summary>Click to expand</summary>\n\n"
    content += f"{transcript.get('full_text', '')[:5000]}...\n"
    content += "</details>\n"

    return frontmatter + content


def save_extraction(video_data: Dict, extraction: Dict, topics: List[str]):
    """Save extracted content to appropriate topic folders."""
    video_id = video_data["video_id"]
    title = video_data["title"]

    # Create safe filename
    safe_title = re.sub(r'[^\w\s-]', '', title)[:50].strip().replace(" ", "-")
    filename = f"{video_id}_{safe_title}.md"

    # Generate markdown content
    markdown = create_extraction_template(video_data, extraction, topics)

    saved_paths = []

    # Save to each relevant topic folder
    for topic in topics:
        if topic in TOPICS:
            folder = TOPICS[topic]["folder"]
        else:
            folder = "general"

        output_path = OUTPUT_DIR / folder / filename
        with open(output_path, "w") as f:
            f.write(markdown)
        saved_paths.append(str(output_path.relative_to(BASE_DIR)))

    return saved_paths


def update_queue_status(queue_file: Path, status: str, output_paths: List[str]):
    """Update queue file with extraction status."""
    with open(queue_file) as f:
        data = yaml.safe_load(f)

    data["status"] = status
    data["extracted_at"] = datetime.now().isoformat()
    data["output_paths"] = output_paths

    with open(queue_file, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def update_video_status(video_path: Path):
    """Update video file with extraction completion."""
    with open(video_path) as f:
        data = yaml.safe_load(f)

    data["processing"]["stage"] = "extracted"
    data["processing"]["stages_completed"].append("extract")
    data["processing"]["next_stage"] = "complete"
    data["processing"]["extracted_at"] = datetime.now().isoformat()

    with open(video_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def generate_project_map():
    """Generate YAML project map of all extractions."""
    project_map = {
        "generated_at": datetime.now().isoformat(),
        "topics": {},
        "total_extractions": 0,
        "videos_by_topic": {}
    }

    for topic_key, topic_info in TOPICS.items():
        folder = OUTPUT_DIR / topic_info["folder"]
        if folder.exists():
            files = list(folder.glob("*.md"))
            project_map["topics"][topic_key] = {
                "name": topic_info["name"],
                "folder": topic_info["folder"],
                "video_count": len(files),
                "videos": [f.stem for f in files]
            }
            project_map["total_extractions"] += len(files)

    # General folder
    general_folder = OUTPUT_DIR / "general"
    if general_folder.exists():
        files = list(general_folder.glob("*.md"))
        project_map["topics"]["general"] = {
            "name": "General",
            "folder": "general",
            "video_count": len(files),
            "videos": [f.stem for f in files]
        }
        project_map["total_extractions"] += len(files)

    # Save project map
    map_path = OUTPUT_DIR / "project_map.yaml"
    with open(map_path, "w") as f:
        yaml.dump(project_map, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return map_path


def extract_video(video_data: Dict, dry_run: bool = False) -> bool:
    """Extract insights from a single video."""
    video_id = video_data["video_id"]
    title = video_data["title"]
    creator = video_data["creator"]
    transcript = video_data["transcript"]

    print(f"\n📹 {title[:60]}...")
    print(f"    Creator: {creator}")
    print(f"    Transcript: {len(transcript.get('full_text', '')):,} chars")

    if dry_run:
        print("    [DRY RUN - skipping extraction]")
        return True

    # Detect topics
    topics = detect_topics(transcript.get("full_text", ""))
    print(f"    Topics detected: {', '.join(topics)}")

    # Extract with Claude
    print("    Extracting insights with Claude...")
    extraction = extract_with_claude(
        transcript.get("full_text", ""),
        title,
        creator
    )

    if not extraction:
        print("    ❌ Extraction failed")
        return False

    # Save extraction
    print("    Saving to topic folders...")
    output_paths = save_extraction(video_data, extraction, topics)
    for path in output_paths:
        print(f"    ✓ {path}")

    # Update statuses
    update_queue_status(video_data["queue_file"], "extracted", output_paths)
    update_video_status(video_data["source_path"])

    # Log event
    log_event("video_extracted", {
        "video_id": video_id,
        "title": title[:100],
        "creator": creator,
        "topics": topics,
        "tools_count": len(extraction.get("tools_covered", [])),
        "insights_count": len(extraction.get("key_insights", []))
    })

    print("    ✓ Extraction complete")
    return True


def main():
    parser = argparse.ArgumentParser(description="Extract insights from video transcripts")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be extracted")
    parser.add_argument("--limit", type=int, help="Limit number of videos to process")
    parser.add_argument("--video", help="Process specific video by ID")
    parser.add_argument("--topic", help="Only process videos matching topic")

    args = parser.parse_args()

    # Ensure directories exist
    ensure_directories()

    # Get pending videos
    if args.video:
        # Find specific video
        pending = []
        for video in get_pending_videos():
            if video["video_id"] == args.video:
                pending.append(video)
                break
    else:
        pending = get_pending_videos()

    # Filter by topic if specified
    if args.topic:
        filtered = []
        for video in pending:
            topics = detect_topics(video["transcript"].get("full_text", ""))
            if args.topic.lower() in [t.lower() for t in topics]:
                filtered.append(video)
        pending = filtered

    if args.limit:
        pending = pending[:args.limit]

    if not pending:
        print("No videos ready for extraction")
        return

    print(f"\n{'='*60}")
    print(f"EXTRACTING INSIGHTS FROM {len(pending)} VIDEOS")
    print(f"{'='*60}")
    print(f"Output directory: {OUTPUT_DIR.relative_to(BASE_DIR)}")
    print()

    stats = {"success": 0, "failed": 0}

    for i, video in enumerate(pending, 1):
        print(f"\n[{i}/{len(pending)}]", end="")

        success = extract_video(video, dry_run=args.dry_run)

        if success:
            stats["success"] += 1
        else:
            stats["failed"] += 1

    # Generate project map
    if not args.dry_run and stats["success"] > 0:
        print(f"\n\nGenerating project map...")
        map_path = generate_project_map()
        print(f"✓ Project map saved: {map_path.relative_to(BASE_DIR)}")

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Success: {stats['success']}")
    print(f"Failed: {stats['failed']}")

    if args.dry_run:
        print("\n[DRY RUN - no files were created]")
    else:
        print(f"\nOutput: {OUTPUT_DIR.relative_to(BASE_DIR)}/")
        for topic in TOPICS.values():
            folder = OUTPUT_DIR / topic["folder"]
            if folder.exists():
                count = len(list(folder.glob("*.md")))
                if count > 0:
                    print(f"  - {topic['folder']}/: {count} files")


if __name__ == "__main__":
    main()
