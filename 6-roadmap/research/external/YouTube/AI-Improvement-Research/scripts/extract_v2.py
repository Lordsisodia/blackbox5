#!/usr/bin/env python3
"""
AI Improvement Research - Stage 4 V2: Multi-Dimensional Extraction
Extracts insights and organizes them across multiple dimensions:
- By Topic (claude-code, mcp, ai-agents, etc.)
- By Date (chronological organization)
- By Importance (critical, high, medium, low)
- Index files (queryable database)

Importance Markers:
[CRITICAL] - Game-changing insights, novel techniques, major frameworks
[HIGH]     - Very valuable, actionable, specific tools/techniques
[MEDIUM]   - Useful context, good to know
[LOW]      - Background info, general knowledge
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
QUEUE_DIR = BASE_DIR / "queue"
OUTPUT_DIR = BASE_DIR / "output"
TIMELINE_DIR = BASE_DIR / "timeline"
INDEX_DIR = BASE_DIR / "index"
BY_TOPIC_DIR = BASE_DIR / "by_topic"
BY_DATE_DIR = BASE_DIR / "by_date"
BY_IMPORTANCE_DIR = BASE_DIR / "by_importance"

# Topic definitions
TOPICS = {
    "mcp": {
        "name": "MCP (Model Context Protocol)",
        "patterns": [r"\bmcp\b", r"model context protocol", r"mcp server", r"mcp client"],
        "folder": "mcp"
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

# Importance levels
IMPORTANCE_LEVELS = ["critical", "high", "medium", "low"]


def ensure_directories():
    """Create all directory structures."""
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    BY_TOPIC_DIR.mkdir(parents=True, exist_ok=True)
    BY_DATE_DIR.mkdir(parents=True, exist_ok=True)
    BY_IMPORTANCE_DIR.mkdir(parents=True, exist_ok=True)

    for topic in TOPICS.values():
        (BY_TOPIC_DIR / topic["folder"]).mkdir(exist_ok=True)

    for level in IMPORTANCE_LEVELS:
        (BY_IMPORTANCE_DIR / level).mkdir(exist_ok=True)


def get_pending_videos():
    """Get videos ready for extraction."""
    pending = []

    for queue_file in (QUEUE_DIR / "pending").glob("*.yaml"):
        with open(queue_file) as f:
            data = yaml.safe_load(f)

        status = data.get("status", "")
        if status == "extracted":
            continue

        source_path = data.get("source_path", "")
        if source_path.startswith("data/"):
            source_path = BASE_DIR / source_path
        else:
            source_path = DATA_DIR / source_path

        if not source_path.exists():
            continue

        with open(source_path) as f:
            video_data = yaml.safe_load(f)

        transcript = video_data.get("transcript", {})
        full_text = transcript.get("full_text", "")
        if not full_text or len(full_text) < 100:
            continue

        pending.append({
            "video_id": data.get("video_id"),
            "title": data.get("title", ""),
            "creator": data.get("creator", ""),
            "creator_slug": data.get("creator_slug", ""),
            "url": data.get("url", ""),
            "source_path": source_path,
            "queue_file": queue_file,
            "transcript": transcript,
            "video_data": video_data,
            "ranking": data.get("ranking_v2", {})
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


def generate_extraction_prompt(transcript: str, title: str, creator: str) -> str:
    """Generate prompt for Claude to extract insights with importance rankings."""
    return f"""Analyze this YouTube video transcript and extract structured insights with IMPORTANCE RANKINGS.

Video: {title}
Creator: {creator}

Transcript:
{transcript[:15000]}

Extract and return ONLY a JSON object with this structure:
{{
    "overall_importance": "critical|high|medium|low",
    "importance_reasoning": "Why this importance level was assigned",
    "summary": "2-3 sentence summary",

    "key_insights": [
        {{
            "content": "The insight",
            "importance": "critical|high|medium|low",
            "reasoning": "Why this importance level"
        }}
    ],

    "tools_covered": [
        {{
            "name": "Tool name",
            "description": "What it does",
            "use_case": "How it's used",
            "importance": "critical|high|medium|low",
            "is_new_framework": true|false
        }}
    ],

    "techniques": [
        {{
            "name": "Technique name",
            "description": "What it is",
            "steps": ["step 1", "step 2"],
            "importance": "critical|high|medium|low"
        }}
    ],

    "frameworks": [
        {{
            "name": "Framework/Pattern name",
            "type": "pattern|methodology|architecture",
            "description": "What it is",
            "components": ["component 1", "component 2"],
            "importance": "critical|high|medium|low"
        }}
    ],

    "code_examples": [
        {{
            "description": "What the code does",
            "code": "code snippet",
            "language": "python|javascript|bash|etc",
            "importance": "critical|high|medium|low"
        }}
    ],

    "resources": [
        {{
            "type": "link|repo|doc|tool",
            "url": "URL if mentioned",
            "title": "Name of resource",
            "description": "What it's for",
            "importance": "critical|high|medium|low"
        }}
    ],

    "prerequisites": ["skill or tool needed"],
    "project_ideas": ["Project you could build"],
    "difficulty": "beginner|intermediate|advanced"
}}

IMPORTANCE RANKINGS:
- **critical**: Game-changing insight, novel technique, major framework, something that changes how you work
- **high**: Very valuable, actionable, specific tools/techniques you should learn
- **medium**: Useful context, good to know, supports understanding
- **low**: Background info, general knowledge, nice to have

Be STRICT with importance rankings. Most content should be medium or low. Only mark truly exceptional insights as critical or high.

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
            system="You are an expert at analyzing technical content and extracting structured, actionable insights with accurate importance rankings. Be strict - most content is medium or low importance.",
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.content[0].text

        # Extract JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]

        return json.loads(content.strip())

    except Exception as e:
        print(f"    Claude extraction failed: {e}")
        return None


def create_importance_markdown(video_data: Dict, extraction: Dict, topics: List[str]) -> Tuple[str, str]:
    """Create markdown with importance brackets. Returns (full_content, importance_only_content)."""
    video = video_data["video_data"]
    transcript = video_data["transcript"]
    source = video.get("source", {})
    creator = video.get("creator", {})

    overall_importance = extraction.get("overall_importance", "medium").upper()

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
overall_importance: {overall_importance}
"""

    # Add tools
    frontmatter += "tools_mentioned:\n"
    for tool in extraction.get("tools_covered", []):
        frontmatter += f"  - {tool.get('name', '')}\n"

    # Add frameworks
    if extraction.get("frameworks"):
        frontmatter += "frameworks:\n"
        for fw in extraction["frameworks"]:
            frontmatter += f"  - {fw.get('name', '')}\n"

    frontmatter += f"difficulty: {extraction.get('difficulty', 'intermediate')}\n"
    frontmatter += f"extracted_at: {datetime.now().isoformat()}\n"
    frontmatter += "---\n\n"

    # Build content with importance markers
    content = f"# [{overall_importance}] {source.get('title', '')}\n\n"
    content += f"**Creator:** {creator.get('name', '')}  \n"
    content += f"**Video:** [{source.get('url', '')}]({source.get('url', '')})  \n"
    content += f"**Published:** {source.get('published_at', '')}  \n"
    content += f"**Overall Importance:** [{overall_importance}]  \n\n"

    # Summary
    content += "## Summary\n\n"
    content += f"{extraction.get('summary', 'No summary available.')}\n\n"

    # Key Insights with importance
    if extraction.get("key_insights"):
        content += "## Key Insights\n\n"
        for insight in extraction["key_insights"]:
            importance = insight.get("importance", "medium").upper()
            content += f"**[{importance}]** {insight.get('content', '')}\n\n"

    # Frameworks (new section)
    if extraction.get("frameworks"):
        content += "## Frameworks & Patterns\n\n"
        for fw in extraction["frameworks"]:
            importance = fw.get("importance", "medium").upper()
            content += f"### [{importance}] {fw.get('name', '')}\n"
            content += f"**Type:** {fw.get('type', 'pattern')}  \n"
            content += f"{fw.get('description', '')}\n\n"
            if fw.get("components"):
                content += "**Components:**\n"
                for comp in fw["components"]:
                    content += f"- {comp}\n"
                content += "\n"

    # Tools Covered with importance
    if extraction.get("tools_covered"):
        content += "## Tools Covered\n\n"
        for tool in extraction["tools_covered"]:
            importance = tool.get("importance", "medium").upper()
            content += f"### [{importance}] {tool.get('name', '')}\n"
            content += f"{tool.get('description', '')}\n\n"
            if tool.get("use_case"):
                content += f"**Use Case:** {tool['use_case']}\n\n"
            if tool.get("is_new_framework"):
                content += "**Note:** This is a new framework/pattern\n\n"

    # Techniques with importance
    if extraction.get("techniques"):
        content += "## Techniques\n\n"
        for technique in extraction["techniques"]:
            importance = technique.get("importance", "medium").upper()
            content += f"### [{importance}] {technique.get('name', '')}\n"
            content += f"{technique.get('description', '')}\n\n"
            if technique.get("steps"):
                content += "**Steps:**\n"
                for i, step in enumerate(technique["steps"], 1):
                    content += f"{i}. {step}\n"
                content += "\n"

    # Code Examples with importance
    if extraction.get("code_examples"):
        content += "## Code Examples\n\n"
        for example in extraction["code_examples"]:
            importance = example.get("importance", "medium").upper()
            content += f"### [{importance}] {example.get('description', 'Code Example')}\n\n"
            lang = example.get("language", "")
            content += f"```{lang}\n{example.get('code', '')}\n```\n\n"

    # Resources with importance
    if extraction.get("resources"):
        content += "## Resources Mentioned\n\n"
        for resource in extraction["resources"]:
            importance = resource.get("importance", "medium").upper()
            url = resource.get("url", "")
            title = resource.get("title", url)
            content += f"**[{importance}]** [{title}]({url}) - {resource.get('description', '')}\n\n"

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

    full_content = frontmatter + content

    # Create importance-only version (only CRITICAL and HIGH)
    importance_only = frontmatter + content
    # This will be filtered when saving to by_importance/

    return full_content, importance_only, overall_importance


def update_index_files(video_data: Dict, extraction: Dict, topics: List[str], locations: Dict):
    """Update all index files with new extraction data."""
    video_id = video_data["video_id"]
    video = video_data["video_data"]
    source = video.get("source", {})
    creator = video.get("creator", {})
    overall_importance = extraction.get("overall_importance", "medium")

    # Update index/videos.yaml
    videos_index_path = INDEX_DIR / "videos.yaml"
    if videos_index_path.exists():
        with open(videos_index_path) as f:
            videos_index = yaml.safe_load(f) or {"videos": {}}
    else:
        videos_index = {"videos": {}}

    videos_index["videos"][video_id] = {
        "title": source.get("title", ""),
        "creator": creator.get("name", ""),
        "creator_tier": creator.get("tier", 3),
        "published_at": source.get("published_at", ""),
        "extracted_at": datetime.now().isoformat(),
        "topics": topics,
        "importance": overall_importance,
        "tools_mentioned": [t.get("name") for t in extraction.get("tools_covered", [])],
        "frameworks": [f.get("name") for f in extraction.get("frameworks", [])],
        "has_code_examples": len(extraction.get("code_examples", [])) > 0,
        "locations": locations
    }

    with open(videos_index_path, "w") as f:
        yaml.dump(videos_index, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    # Update index/insights.yaml
    insights_index_path = INDEX_DIR / "insights.yaml"
    if insights_index_path.exists():
        with open(insights_index_path) as f:
            insights_index = yaml.safe_load(f) or {"insights": []}
    else:
        insights_index = {"insights": []}

    # Add key insights
    for i, insight in enumerate(extraction.get("key_insights", [])):
        insights_index["insights"].append({
            "id": f"{video_id}-{i:03d}",
            "video_id": video_id,
            "type": "insight",
            "importance": insight.get("importance", "medium"),
            "content": insight.get("content", ""),
            "topics": topics,
            "tools": [t.get("name") for t in extraction.get("tools_covered", []) if t.get("importance") in ["critical", "high"]],
            "extracted_at": datetime.now().isoformat()
        })

    # Add frameworks as insights
    for fw in extraction.get("frameworks", []):
        insights_index["insights"].append({
            "id": f"{video_id}-fw-{fw.get('name', '').replace(' ', '-')[:20]}",
            "video_id": video_id,
            "type": "framework",
            "importance": fw.get("importance", "medium"),
            "content": f"{fw.get('name')}: {fw.get('description', '')}",
            "topics": topics,
            "tools": [],
            "extracted_at": datetime.now().isoformat()
        })

    with open(insights_index_path, "w") as f:
        yaml.dump(insights_index, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    # Update index/tools.yaml
    tools_index_path = INDEX_DIR / "tools.yaml"
    if tools_index_path.exists():
        with open(tools_index_path) as f:
            tools_index = yaml.safe_load(f) or {"tools": {}}
    else:
        tools_index = {"tools": {}}

    for tool in extraction.get("tools_covered", []):
        tool_name = tool.get("name", "")
        if tool_name not in tools_index["tools"]:
            tools_index["tools"][tool_name] = {
                "mentions": 0,
                "videos": [],
                "first_seen": datetime.now().isoformat(),
                "last_seen": datetime.now().isoformat(),
                "description": tool.get("description", ""),
                "categories": topics
            }

        tools_index["tools"][tool_name]["mentions"] += 1
        if video_id not in tools_index["tools"][tool_name]["videos"]:
            tools_index["tools"][tool_name]["videos"].append(video_id)
        tools_index["tools"][tool_name]["last_seen"] = datetime.now().isoformat()

    with open(tools_index_path, "w") as f:
        yaml.dump(tools_index, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    # Update index/frameworks.yaml
    frameworks_index_path = INDEX_DIR / "frameworks.yaml"
    if frameworks_index_path.exists():
        with open(frameworks_index_path) as f:
            frameworks_index = yaml.safe_load(f) or {"frameworks": {}}
    else:
        frameworks_index = {"frameworks": {}}

    for fw in extraction.get("frameworks", []):
        fw_name = fw.get("name", "")
        if fw_name not in frameworks_index["frameworks"]:
            frameworks_index["frameworks"][fw_name] = {
                "type": fw.get("type", "pattern"),
                "videos": [],
                "description": fw.get("description", ""),
                "components": fw.get("components", []),
                "related_tools": [],
                "first_seen": datetime.now().isoformat()
            }

        if video_id not in frameworks_index["frameworks"][fw_name]["videos"]:
            frameworks_index["frameworks"][fw_name]["videos"].append(video_id)

    with open(frameworks_index_path, "w") as f:
        yaml.dump(frameworks_index, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    # Update index/links.yaml
    links_index_path = INDEX_DIR / "links.yaml"
    if links_index_path.exists():
        with open(links_index_path) as f:
            links_index = yaml.safe_load(f) or {"links": []}
    else:
        links_index = {"links": []}

    for resource in extraction.get("resources", []):
        if resource.get("url"):
            links_index["links"].append({
                "url": resource["url"],
                "title": resource.get("title", ""),
                "source_video": video_id,
                "source_creator": creator.get("name", ""),
                "discovered_at": datetime.now().isoformat(),
                "category": resource.get("type", "link"),
                "topic": topics[0] if topics else "general",
                "importance": resource.get("importance", "medium")
            })

    with open(links_index_path, "w") as f:
        yaml.dump(links_index, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def update_topic_index(topic: str, video_data: Dict, extraction: Dict):
    """Update the topic's _index.yaml file."""
    topic_info = TOPICS.get(topic, {"name": topic, "folder": topic})
    folder = topic_info["folder"]
    index_path = BY_TOPIC_DIR / folder / "_index.yaml"

    if index_path.exists():
        with open(index_path) as f:
            index = yaml.safe_load(f) or {}
    else:
        index = {
            "topic": topic,
            "name": topic_info["name"],
            "description": f"Content about {topic_info['name']}",
            "total_videos": 0,
            "total_insights": 0,
            "tools_covered": [],
            "videos": []
        }

    video_id = video_data["video_id"]

    # Check if video already in index
    existing = [v for v in index["videos"] if v["id"] == video_id]
    if not existing:
        index["videos"].append({
            "id": video_id,
            "title": video_data["title"],
            "importance": extraction.get("overall_importance", "medium"),
            "extracted_at": datetime.now().isoformat(),
            "file": f"{datetime.now().strftime('%Y-%m-%d')}_{video_id}.md"
        })
        index["total_videos"] += 1

    # Update tools
    for tool in extraction.get("tools_covered", []):
        tool_name = tool.get("name", "")
        if tool_name not in index["tools_covered"]:
            index["tools_covered"].append(tool_name)

    index["last_updated"] = datetime.now().isoformat()

    with open(index_path, "w") as f:
        yaml.dump(index, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def update_daily_key_sources(video_data: Dict, extraction: Dict, topics: List[str]):
    """Update the daily _key-sources.md file."""
    today = datetime.now()
    year_dir = BY_DATE_DIR / str(today.year)
    month_dir = year_dir / f"{today.month:02d}-{today.strftime('%B').lower()}"
    month_dir.mkdir(parents=True, exist_ok=True)

    key_sources_path = month_dir / "_key-sources.md"

    video_id = video_data["video_id"]
    creator = video_data["creator"]
    overall_importance = extraction.get("overall_importance", "medium").upper()

    # Build entry for this video
    video_entry = f"""
## [{overall_importance}] {video_data['title']}
- **Creator:** {creator}
- **Video:** [{video_id}]({video_data['url']})
- **Topics:** {', '.join(topics)}
- **File:** `{today.strftime('%Y-%m-%d')}_{video_id}.md`
"""

    if key_sources_path.exists():
        with open(key_sources_path) as f:
            content = f.read()

        # Check if video already added
        if video_id not in content:
            # Add to videos processed section
            if "## Videos Processed" in content:
                content = content.replace("## Videos Processed", f"## Videos Processed{video_entry}")

            # Add frameworks
            for fw in extraction.get("frameworks", []):
                fw_importance = fw.get("importance", "medium").upper()
                fw_entry = f"\n### [{fw_importance}] {fw.get('name', '')}\n- {fw.get('description', '')}\n- Source: {video_id} ({creator})\n"

                if fw_importance == "CRITICAL" and "## Key AI Frameworks" in content:
                    content = content.replace("### [CRITICAL]", f"{fw_entry}### [CRITICAL]", 1)

            with open(key_sources_path, "w") as f:
                f.write(content)
    else:
        # Create new file
        content = f"""# Key Sources - {today.strftime('%B %d, %Y')}

**Generated:** {datetime.now().isoformat()}
**Videos Processed:** 1

## Key Links Found Today

### [CRITICAL]
"""

        # Add resources
        for resource in extraction.get("resources", []):
            if resource.get("importance") == "critical" and resource.get("url"):
                content += f"- [{resource.get('title', resource['url'])}]({resource['url']}) - From {creator}\n"

        content += "\n### [HIGH]\n"
        for resource in extraction.get("resources", []):
            if resource.get("importance") == "high" and resource.get("url"):
                content += f"- [{resource.get('title', resource['url'])}]({resource['url']}) - From {creator}\n"

        content += "\n## Key AI Frameworks Found Today\n\n### [CRITICAL]\n"

        # Add frameworks
        for fw in extraction.get("frameworks", []):
            fw_importance = fw.get("importance", "medium").upper()
            if fw_importance == "CRITICAL":
                content += f"- **{fw.get('name', '')}** - {fw.get('description', '')}\n"
                if fw.get("components"):
                    content += f"  - Components: {', '.join(fw['components'])}\n"
                content += f"  - Source: {video_id} ({creator})\n"

        content += "\n### [HIGH]\n"
        for fw in extraction.get("frameworks", []):
            fw_importance = fw.get("importance", "medium").upper()
            if fw_importance == "HIGH":
                content += f"- **{fw.get('name', '')}** - {fw.get('description', '')}\n"
                content += f"  - Source: {video_id} ({creator})\n"

        content += "\n## Key Tools Found Today\n\n### [CRITICAL]\n"

        # Add tools
        for tool in extraction.get("tools_covered", []):
            tool_importance = tool.get("importance", "medium").upper()
            if tool_importance == "CRITICAL":
                content += f"- **{tool.get('name', '')}** - {tool.get('description', '')}\n"

        content += "\n### [HIGH]\n"
        for tool in extraction.get("tools_covered", []):
            tool_importance = tool.get("importance", "medium").upper()
            if tool_importance == "HIGH":
                content += f"- **{tool.get('name', '')}** - {tool.get('description', '')}\n"

        content += f"\n## Videos Processed{video_entry}"

        with open(key_sources_path, "w") as f:
            f.write(content)


def save_extraction_multi(video_data: Dict, extraction: Dict, topics: List[str]) -> Dict:
    """Save extraction to multiple locations. Returns dict of all paths."""
    video_id = video_data["video_id"]
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")

    # Create safe filename
    safe_title = re.sub(r'[^\w\s-]', '', video_data["title"])[:40].strip().replace(" ", "-")
    filename = f"{date_str}_{video_id}.md"

    # Generate markdown content
    full_content, importance_only, overall_importance = create_importance_markdown(video_data, extraction, topics)

    locations = {
        "by_topic": [],
        "by_date": [],
        "by_importance": []
    }

    # Save to topic folders
    for topic in topics:
        if topic in TOPICS:
            folder = TOPICS[topic]["folder"]
        else:
            folder = "general"

        topic_path = BY_TOPIC_DIR / folder / filename
        with open(topic_path, "w") as f:
            f.write(full_content)
        locations["by_topic"].append(str(topic_path.relative_to(BASE_DIR)))

        # Update topic index
        update_topic_index(topic, video_data, extraction)

    # Save to date folder
    year_dir = BY_DATE_DIR / str(today.year)
    month_dir = year_dir / f"{today.month:02d}-{today.strftime('%B').lower()}"
    month_dir.mkdir(parents=True, exist_ok=True)

    date_path = month_dir / filename
    with open(date_path, "w") as f:
        f.write(full_content)
    locations["by_date"].append(str(date_path.relative_to(BASE_DIR)))

    # Save to importance folder (only critical and high)
    if overall_importance.lower() in ["critical", "high"]:
        importance_path = BY_IMPORTANCE_DIR / overall_importance.lower() / filename
        with open(importance_path, "w") as f:
            f.write(full_content)
        locations["by_importance"].append(str(importance_path.relative_to(BASE_DIR)))

    # Update daily key sources
    update_daily_key_sources(video_data, extraction, topics)

    return locations


def update_queue_status(queue_file: Path, status: str, output_paths: Dict):
    """Update queue file with extraction status."""
    with open(queue_file) as f:
        data = yaml.safe_load(f)

    data["status"] = status
    data["extracted_at"] = datetime.now().isoformat()
    data["output_paths"] = output_paths

    with open(queue_file, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


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
    print("    Extracting insights with Claude (V2 with importance rankings)...")
    extraction = extract_with_claude(
        transcript.get("full_text", ""),
        title,
        creator
    )

    if not extraction:
        print("    ❌ Extraction failed")
        return False

    print(f"    Overall importance: {extraction.get('overall_importance', 'medium').upper()}")
    print(f"    Key insights: {len(extraction.get('key_insights', []))}")
    print(f"    Tools: {len(extraction.get('tools_covered', []))}")
    print(f"    Frameworks: {len(extraction.get('frameworks', []))}")

    # Save to multiple locations
    print("    Saving to multiple locations...")
    locations = save_extraction_multi(video_data, extraction, topics)

    for category, paths in locations.items():
        for path in paths:
            print(f"    ✓ {path}")

    # Update index files
    print("    Updating index files...")
    update_index_files(video_data, extraction, topics, locations)
    print("    ✓ Index updated")

    # Update queue status
    update_queue_status(video_data["queue_file"], "extracted", locations)

    print("    ✓ Extraction complete")
    return True


def main():
    parser = argparse.ArgumentParser(description="Extract insights with multi-dimensional organization")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be extracted")
    parser.add_argument("--limit", type=int, help="Limit number of videos to process")
    parser.add_argument("--video", help="Process specific video by ID")
    parser.add_argument("--topic", help="Only process videos matching topic")

    args = parser.parse_args()

    # Ensure directories exist
    ensure_directories()

    # Get pending videos
    if args.video:
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
    print(f"EXTRACTING INSIGHTS FROM {len(pending)} VIDEOS (V2)")
    print(f"{'='*60}")
    print(f"Output directories:")
    print(f"  - by_topic/     (topic-based organization)")
    print(f"  - by_date/      (chronological organization)")
    print(f"  - by_importance/ (importance-ranked)")
    print(f"  - index/        (queryable indexes)")
    print()

    stats = {"success": 0, "failed": 0}

    for i, video in enumerate(pending, 1):
        print(f"\n[{i}/{len(pending)}]", end="")

        success = extract_video(video, dry_run=args.dry_run)

        if success:
            stats["success"] += 1
        else:
            stats["failed"] += 1

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Success: {stats['success']}")
    print(f"Failed: {stats['failed']}")

    if not args.dry_run and stats["success"] > 0:
        print(f"\nOutput locations:")
        print(f"  index/videos.yaml       - Master video index")
        print(f"  index/insights.yaml     - Queryable insights")
        print(f"  index/tools.yaml        - Tool catalog")
        print(f"  index/frameworks.yaml   - Framework catalog")
        print(f"  index/links.yaml        - URL database")
        print(f"  by_topic/*/             - Topic-organized extractions")
        print(f"  by_date/*/              - Date-organized extractions")
        print(f"  by_importance/*/        - Importance-ranked extractions")


if __name__ == "__main__":
    main()
