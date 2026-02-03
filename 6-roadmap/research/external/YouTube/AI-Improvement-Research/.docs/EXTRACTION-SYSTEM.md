# Extraction System

**Date**: 2026-02-02
**Status**: Implemented and Tested

---

## Overview

The extraction system processes video transcripts with Claude to extract structured, actionable insights into organized markdown files.

---

## How It Works

### 1. Topic Detection

Automatically detects topics from transcript content:
- **MCP** - Model Context Protocol content
- **Claude Code** - Claude Code specific tutorials
- **AI Agents** - Agent frameworks and patterns
- **Voice AI** - Voice agents, TTS, STT
- **LLM Engineering** - Prompt engineering, fine-tuning
- **Coding Tools** - IDEs, editors, dev tools
- **n8n** - Workflow automation
- **Supabase** - Database and backend
- **Deployment** - Infrastructure, Docker, hosting
- **Business Automation** - SaaS, B2B tools

### 2. Claude Extraction

Sends transcript to Claude with structured prompt to extract:
- Summary (2-3 sentences)
- Key insights (actionable takeaways)
- Tools covered (with descriptions)
- Techniques (with step-by-step)
- Code examples
- Resources mentioned
- Difficulty level
- Prerequisites
- Project ideas

### 3. Output Organization

Creates markdown files in topic folders:
```
output/
├── mcps/
├── claude-code/
├── ai-agents/
├── voice-ai/
├── llm-engineering/
├── coding-tools/
├── n8n/
├── supabase/
├── deployment/
├── business-automation/
├── general/
└── project_map.yaml
```

### 4. Project Map

YAML file tracking all extractions by topic for easy navigation.

---

## Usage

```bash
# Extract all pending videos
python scripts/extract.py

# Dry run (see what would be extracted)
python scripts/extract.py --dry-run

# Extract specific video
python scripts/extract.py --video VIDEO_ID

# Extract only videos matching topic
python scripts/extract.py --topic claude_code

# Limit number of videos
python scripts/extract.py --limit 5
```

---

## Output Format

Each extraction creates a markdown file with:

```markdown
---
video_id: XXX
title: "Video Title"
creator: Creator Name
creator_tier: 1
url: https://youtube.com/watch?v=XXX
published_at: YYYYMMDD
duration: seconds
view_count: N
topics: [topic1, topic2]
tools_mentioned:
  - Tool 1
  - Tool 2
difficulty: beginner|intermediate|advanced
extracted_at: ISO timestamp
---

# Video Title

**Creator:** Name
**Video:** [URL](URL)
**Published:** Date

## Summary

Brief overview of what the video teaches.

## Key Insights

- Actionable insight 1
- Actionable insight 2

## Tools Covered

### Tool Name
Description of the tool.

**Use Case:** How it's used in the video.

## Techniques

### Technique Name
Description of the technique.

**Steps:**
1. Step one
2. Step two

## Code Examples

### Description
```
code here
```

## Resources Mentioned

- [Description](URL)

## Prerequisites

- Skill or tool needed

## Project Ideas

- Project you could build

## Full Transcript

<details>
<summary>Click to expand</summary>
...
</details>
```

---

## Current Status

- **Videos collected**: 63
- **Videos with transcripts**: 32
- **Videos extracted**: 1 (test)
- **Pending extraction**: 31

---

## Blocked Videos

The following sources need residential proxy to download transcripts:
- `in_the_world_of_ai`: 15 videos
- `vrsen`: 15 videos

Solution: Webshare free tier (10 proxies, 1GB/month)
