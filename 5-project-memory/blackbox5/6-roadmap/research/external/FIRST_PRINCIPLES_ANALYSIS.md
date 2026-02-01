# First Principles Analysis: Deep Research Pipeline

## Core Question
What is the actual goal? What are we really trying to achieve?

**Answer:** Transform YouTube videos into actionable intelligence that improves how you build AI systems.

---

## First Principles Breakdown

### 1. What is a YouTube video, really?
- **Temporal data stream**: Audio/visual information over time
- **Knowledge container**: Creator's expertise packaged for consumption
- **Relationship artifact**: Links to other knowledge (repos, papers, people)
- **Signal of importance**: Creator thought this worth making

### 2. What makes video data valuable?
Not the transcript itself, but:
- **Novel concepts**: New tools, techniques, patterns you don't know
- **Actionable intelligence**: Things you can implement
- **Credibility signals**: Who said it, did they demonstrate it, what's their track record
- **Relationships**: How this connects to what you already know
- **Timeliness**: Is this emerging or established

### 3. What is "intelligent extraction"?
Not template-filling. It's:
- **Understanding context**: What domain is this? What level?
- **Detecting novelty**: What's new vs. known vs. hype
- **Assessing credibility**: Original research vs. repackaging
- **Identifying actionability**: Can you do something with this?
- **Recognizing patterns**: How does this fit the broader landscape

### 4. What is a "report"?
Not a summary. It's:
- **Decision support**: Should you watch this? Act on this?
- **Knowledge integration**: How does this fit your existing mental models
- **Action queue**: What to implement and in what order
- **Reference material**: Where to go back when you need it

---

## Re-evaluating the Original Design

### Original: Date-based organization
```
data/raw/2025-01-30/videos/
data/extracted/2025-01-30/
```

**Problem:** You think in creators, not dates. "What did Simon Willison say about MCP?" not "What was discovered on January 30th?"

### Original: Generic extraction template
Same structure for every video regardless of content type.

**Problem:** A news video about GPT-5 release needs different extraction than a 2-hour tutorial on MCP server architecture.

### Original: Daily synthesis report
One report combining all videos.

**Problem:** Loses creator context. Forces artificial connections between unrelated videos.

---

## Revised Architecture (First Principles)

### Core Insight: Creator-Centric Organization

You follow specific creators because you trust their thinking. The unit of value is the **creator's body of work**, not the date.

```
data/
├── by_creator/                    # Primary organization
│   ├── simon_willison/
│   │   ├── metadata.yaml          # Creator profile, tier, focus areas
│   │   ├── videos/                # All videos from this creator
│   │   │   └── {video_id}.yaml    # Complete video data (metadata + transcript + extraction)
│   │   ├── insights/              # Extracted intelligence
│   │   │   └── {video_id}.yaml    # Structured insights from this video
│   │   ├── concepts/              # Knowledge graph
│   │   │   └── {concept_name}.yaml    # All mentions across videos
│   │   └── reports/               # Creator-specific reports
│   │       └── weekly_digest.yaml
│   ├── anthropic/
│   ├── latent_space/
│   └── ...
│
├── by_date/                       # Secondary index (for "what's new")
│   └── YYYY-MM-DD/
│       └── index.yaml             # Links to videos processed that day
│
├── by_concept/                    # Knowledge graph
│   ├── mcp/
│   │   └── mentions.yaml          # All videos mentioning MCP
│   ├── claude_code/
│   ├── ai_agents/
│   └── ...
│
└── action_queue/                  # Your to-do list
    ├── pending.yaml
    ├── in_progress.yaml
    └── completed.yaml
```

---

## Stage 1: Intelligent Ingestion

### What we capture (maximum data)

```yaml
# data/by_creator/{creator}/videos/{video_id}.yaml
video:
  id: "video_id"
  url: "https://youtube.com/watch?v=..."

  # Basic metadata (from yt-dlp)
  title: "Video Title"
  description: "Full description text"
  published_at: "2025-01-30T10:00:00Z"
  duration: 1847  # seconds
  view_count: 45000
  like_count: 2300  # if available

  # Creator context
  creator:
    name: "Simon Willison"
    channel_id: "UC..."
    tier: 1  # Your prioritization
    expertise_areas: ["LLMs", "Django", "data journalism"]

  # Source tracking
  discovered_via: "vip_rss"  # or "manual", "backfill"
  discovered_at: "2025-01-30T14:00:00Z"
  processed_at: "2025-01-30T14:05:00Z"

  # Content classification (auto-detected)
  content_type: "tutorial"  # tutorial|news|analysis|demo|interview|opinion
  technical_level: "intermediate"  # beginner|intermediate|advanced

  # Raw transcript (full fidelity)
  transcript:
    full_text: "..."  # Clean text
    segments:
      - start: 0.0
        end: 5.2
        text: "Hello everyone..."
      - ...
    language: "en"
    is_auto_generated: true

  # Raw assets (optional)
  assets:
    thumbnail: "path/to/thumbnail.jpg"
    # Future: key frames, audio waveform
```

### Why this structure?
- **Single file per video**: Everything in one place
- **Creator-organized**: Natural mental model
- **Maximum data capture**: More data = more extraction possibilities
- **Raw + processed**: Can re-extract with better prompts later

---

## Stage 2: Intelligent Extraction (Content-Type Adaptive)

### Key Insight: Different video types need different extraction strategies

### Extraction Strategy Matrix

| Content Type | Primary Goal | Extraction Focus |
|--------------|--------------|------------------|
| **Tutorial** | Learn to do something | Steps, code, prerequisites, gotchas |
| **News** | Stay informed | Facts, implications, credibility |
| **Analysis** | Understand deeply | Arguments, evidence, counter-arguments |
| **Demo** | See what's possible | Capabilities, limitations, setup |
| **Interview** | Hear expert thinking | Key quotes, insights, references |
| **Opinion** | Understand perspectives | Position, reasoning, biases |

### Dynamic Extraction Prompt

```python
def generate_extraction_prompt(video_metadata, transcript):
    content_type = classify_content_type(transcript)

    base_prompt = f"""
    Analyze this {content_type} video by {video_metadata['creator']['name']}.

    Creator Context:
    - Name: {video_metadata['creator']['name']}
    - Known for: {video_metadata['creator']['expertise_areas']}
    - Tier: {video_metadata['creator']['tier']} (1 = highest trust)

    Video Context:
    - Title: {video_metadata['title']}
    - Duration: {video_metadata['duration']} seconds
    - Published: {video_metadata['published_at']}
    - Content Type: {content_type}

    Your Task:
    {get_extraction_focus(content_type)}
    """

    return base_prompt

def get_extraction_focus(content_type):
    prompts = {
        "tutorial": """
            Extract:
            1. What is being taught (main topic)
            2. Prerequisites (what you need to know first)
            3. Step-by-step breakdown with timestamps
            4. Code examples (exact or approximate)
            5. Common pitfalls mentioned
            6. Expected outcome (what you'll be able to do)
            7. Difficulty assessment (easy/medium/hard)
            8. Your confidence this works (high/medium/low)
        """,
        "news": """
            Extract:
            1. What happened (the news)
            2. Primary sources (who announced it)
            3. Implications for AI builders
            4. Your assessment (confirmed/rumor/speculation)
            5. Action needed now vs. later
            6. Related developments mentioned
        """,
        "analysis": """
            Extract:
            1. Core thesis/argument
            2. Evidence presented
            3. Reasoning quality (sound/weak/flawed)
            4. Counter-arguments acknowledged
            5. Your confidence in conclusion
            6. How this changes your understanding
        """,
        # ... etc for each type
    }
    return prompts.get(content_type, prompts["analysis"])
```

### Extraction Output Structure

```yaml
# data/by_creator/{creator}/insights/{video_id}.yaml
extraction:
  video_id: "video_id"
  extracted_at: "2025-01-30T14:10:00Z"
  extractor_version: "1.0"
  content_type: "tutorial"  # Auto-detected

  # Core intelligence
  summary:
    one_sentence: "Simon shows how to build an MCP server from scratch"
    overview: "2-3 paragraph summary"
    key_thesis: "Main point being made"

  # What you'll learn (tutorial-specific)
  learning_outcomes:
    - "How to structure an MCP server"
    - "How to define tool schemas"
    - "How to handle authentication"

  # Concepts introduced or discussed
  concepts:
    - name: "MCP Server Architecture"
      definition: "The pattern for building Model Context Protocol servers"
      novelty: "new"  # new|known|emerging
      importance: "high"  # high|medium|low
      first_introduced_at: "03:45"
      related_to: ["LSP", "Language Server Protocol"]

    - name: "Tool Definition Schema"
      definition: "JSON schema for describing tool capabilities"
      novelty: "new"
      importance: "high"
      first_introduced_at: "07:20"

  # Actionable items
  actions:
    - description: "Set up your first MCP server"
      difficulty: "medium"
      impact: "high"
      time_estimate: "1 hour"
      prerequisites: ["Node.js installed", "Basic TypeScript"]
      demonstrated_in_video: true
      timestamp: "12:30"
      code_provided: true

  # Resources mentioned
  resources:
    - name: "mcp-server-github"
      type: "github_repo"  # github_repo|paper|article|tool|person
      url: "https://github.com/modelcontextprotocol/servers"
      mentioned_at: "05:15"
      context: "Official MCP server implementations"
      relevance: "essential"  # essential|useful|reference

  # Code from video
  code_examples:
    - description: "Basic MCP server setup"
      timestamp: "08:45"
      language: "typescript"
      approximate_code: |
        import { Server } from "@modelcontextprotocol/sdk";
        // ... approximate code from transcript
      completeness: "partial"  # complete|partial|inferred

  # Key moments
  key_moments:
    - timestamp: "03:45"
      description: "Introduction to MCP architecture"
      importance: "critical"

    - timestamp: "15:20"
      description: "Live demo of server working"
      importance: "high"

  # Critical thinking
  assessment:
    originality: "original"  # original|repackaged|curated
    demonstrated: true  # Did they actually build it?
    depth: "deep"  # surface|moderate|deep
    accuracy_confidence: "high"  # Based on creator track record
    your_confidence: "high"  # After watching

    # Critical evaluation
    strengths:
      - "Clear step-by-step explanation"
      - "Actually builds working example"
    limitations:
      - "Doesn't cover error handling"
      - "Assumes familiarity with TypeScript"

  # Categorization
  categories:
    topics: ["MCP", "Claude Code", "AI Tools"]
    your_projects: ["SISO Internal", "AI Systems Research"]

  # Ranking
  value_assessment:
    novelty: 8  # 1-10: How new is this to you?
    relevance: 9  # 1-10: How relevant to current projects?
    quality: 9  # 1-10: Information density and clarity
    actionability: 8  # 1-10: Can you act on this?
    credibility: 9  # 1-10: Trust in source
    composite: 8.6  # Weighted average

  # Recommendation
  recommendation:
    tier: "must_watch"  # must_watch|recommended|reference|skip
    watch_priority: 1  # Order in your queue
    rewatch_value: "high"  # Will you come back to this?

  # Cross-references (populated later)
  related_videos:
    - creator: "anthropic"
      video_id: "..."
      relationship: "complements"  # complements|contradicts|extends
```

---

## Stage 3: Per-Video Report Generation

### Key Insight: Report per video, not per day

You want to know: "Should I watch this specific video?" not "What happened across all videos today?"

### Report Structure

```yaml
# data/by_creator/{creator}/reports/{video_id}_digest.yaml
video_digest:
  video_id: "video_id"
  generated_at: "2025-01-30T14:15:00Z"

  # Quick decision support
  verdict:
    watch_this: true
    priority: "high"  # high|medium|low
    why: "Original tutorial with working code on MCP servers"

  # If you only have 30 seconds
  tl_dr:
    what: "Build an MCP server from scratch"
    why_matters: "MCP is becoming the standard for AI tool integration"
    key_takeaway: "Use the SDK, define tool schemas, handle auth"
    action_needed: "Try building one this weekend"

  # If you have 5 minutes
  executive_summary:
    overview: "..."
    what_youll_learn: ["...", "..."]
    key_insights: ["...", "..."]
    resources_discovered: ["...", "..."]

  # If you have 30 minutes (the full breakdown)
  detailed_breakdown:
    sections:
      - title: "Introduction (0:00-3:00)"
        summary: "..."
        key_points: ["..."]

      - title: "Architecture Overview (3:00-8:00)"
        summary: "..."
        key_points: ["..."]

  # Your action items from this video
  your_actions:
    immediate:
      - "Clone the MCP SDK repo"
      - "Watch the demo section again"
    this_week:
      - "Build a simple filesystem MCP server"
    this_month:
      - "Integrate MCP into SISO Internal workflow"

  # Reference material
  for_future_reference:
    code_snippets:
      - description: "Server initialization pattern"
        timestamp: "08:45"
    resources_to_bookmark:
      - name: "MCP Official Docs"
        url: "https://..."
    related_videos_to_watch:
      - creator: "anthropic"
        title: "MCP Best Practices"
        why_related: "Builds on this tutorial"
```

### Threshold for Report Generation

```python
def should_generate_report(extraction):
    """Only generate reports for valuable content."""

    # Always report on tier 1 creators
    if extraction['creator']['tier'] == 1:
        return True

    # Report if composite score is high enough
    if extraction['value_assessment']['composite'] >= 7.0:
        return True

    # Report if highly actionable
    if extraction['value_assessment']['actionability'] >= 8:
        return True

    # Report if novel concept from trusted source
    if (extraction['value_assessment']['novelty'] >= 8 and
        extraction['value_assessment']['credibility'] >= 8):
        return True

    return False
```

---

## Stage 4: Cross-Video Intelligence (Weekly)

### When: Once per week, not daily
### What: Detect patterns across creator's recent videos

```yaml
# data/by_creator/{creator}/reports/weekly_synthesis.yaml
weekly_synthesis:
  creator: "simon_willison"
  week_of: "2025-01-27"
  videos_processed: 3

  # What this creator is focused on
  emerging_themes:
    - theme: "MCP adoption patterns"
      evidence:
        - video: "Building MCP Servers"
          insight: "MCP is the new standard"
        - video: "Claude Code Tips"
          insight: "MCP servers extend Claude Code"
      trajectory: "increasing"  # increasing|stable|decreasing

  # How this creator's thinking is evolving
  intellectual_evolution:
    new_positions: ["MCP > plugins for AI tools"]
    shifted_positions: []
    consistent_themes: ["LLM practical applications", "Django"]

  # What you should pay attention to
  attention_recommendations:
    watch_immediately: []
    watch_this_week: []
    bookmark_for_later: []
```

---

## Summary: Revised Pipeline

| Stage | What | Output | Trigger |
|-------|------|--------|---------|
| 1. Ingest | Download video + metadata + transcript | `by_creator/{creator}/videos/{id}.yaml` | New video detected |
| 2. Classify | Detect content type (tutorial/news/etc) | Content type tag | After ingestion |
| 3. Extract | Content-type-specific extraction | `by_creator/{creator}/insights/{id}.yaml` | After classification |
| 4. Report | Generate per-video digest | `by_creator/{creator}/reports/{id}_digest.yaml` | If meets threshold |
| 5. Synthesize | Weekly cross-video analysis | `by_creator/{creator}/reports/weekly_synthesis.yaml` | Weekly cron |

---

## Key Changes from Original Design

| Aspect | Original | Revised |
|--------|----------|---------|
| Organization | By date | By creator (primary) |
| Extraction | Generic template | Content-type adaptive |
| Reports | Daily combined | Per-video (if valuable) |
| Synthesis | Daily | Weekly |
| Data capture | Minimal | Maximum |
| Threshold | Process all | Only report on valuable |

---

## Open Questions

1. **Content type detection**: Rule-based or LLM-based classification?
2. **Threshold tuning**: What composite score warrants a report?
3. **Creator tiers**: How do you want to categorize your VIPs?
4. **Action queue**: Should this be global or per-creator?
