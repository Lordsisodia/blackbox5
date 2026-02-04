"""
RETAIN Operation Prompts for LLM-based Memory Extraction

These prompts guide the LLM to extract structured memories from task/run content
and classify them into Hindsight's 4 networks (World, Experience, Opinion, Observation).
"""

from typing import Dict, List


def get_retain_system_prompt() -> str:
    """System prompt for RETAIN extraction"""
    return """You are a memory extraction specialist for the Hindsight memory architecture.

Your task is to analyze content from agent tasks/runs and extract structured memories,
classifying them into one of four networks:

1. WORLD (W) - Objective facts about the world
   - Technical facts, configurations, code patterns
   - Decisions made (what was decided)
   - Entities discovered (people, technologies, concepts)
   - Relationships established

2. EXPERIENCE (B) - First-person actions and experiences
   - Actions taken (what was done, step by step)
   - Tools and commands used
   - Learning moments (challenges overcome)
   - Interactions (questions, feedback)

3. OPINION (O) - Beliefs with confidence scores
   - Beliefs formed (what is believed to be true)
   - Judgments and evaluations
   - Preferences (what is preferred and why)
   - Confidence levels (how certain)

4. OBSERVATION (S) - Synthesized insights
   - Patterns detected
   - Cross-task connections
   - Key insights (what it all means)
   - Anomalies and surprises

For each memory extracted, provide:
- network: One of ["world", "experience", "opinion", "observation"]
- content: Clear, specific text of the memory
- confidence: Score 0.0-1.0 (how certain is this memory)
- entities: List of entities mentioned (people, technologies, concepts)
- category: Sub-category (technical, strategic, learning, etc.)

Guidelines:
- Be specific and concrete, not vague
- Extract multiple memories if the content is rich
- Focus on novel information, not routine steps
- Include confidence scores based on evidence strength
- Link related memories when possible
- Use the exact text from the source when appropriate
"""


def get_retain_user_prompt(content: str, source: str, content_type: str = "task") -> str:
    """
    User prompt for RETAIN extraction

    Args:
        content: The markdown content to extract from
        source: Path or identifier of the source
        content_type: Type of content (task, run, thoughts, decisions)
    """
    return f"""Extract structured memories from the following {content_type} content.

Source: {source}

Content:
```markdown
{content}
```

Extract memories following these guidelines:

1. WORLD memories: Extract facts, decisions, entities, relationships
2. EXPERIENCE memories: Extract actions, tools used, learnings, interactions
3. OPINION memories: Extract beliefs, judgments, preferences with confidence
4. OBSERVATION memories: Extract patterns, insights, connections, anomalies

For each memory, output a JSON object with:
- network: "world" | "experience" | "opinion" | "observation"
- content: The memory text (be specific and concrete)
- confidence: 0.0-1.0 score
- entities: List of entities mentioned
- category: Sub-category (e.g., "technical", "strategic", "learning")

Output format: JSON array of memory objects

Example output:
```json
[
  {{
    "network": "world",
    "content": "PostgreSQL with pgvector extension is used for vector similarity search",
    "confidence": 0.95,
    "entities": ["PostgreSQL", "pgvector"],
    "category": "technical"
  }},
  {{
    "network": "experience",
    "content": "Implemented embedding pipeline using OpenAI text-embedding-3-small",
    "confidence": 0.9,
    "entities": ["OpenAI", "text-embedding-3-small"],
    "category": "implementation"
  }},
  {{
    "network": "opinion",
    "content": "text-embedding-3-small is cost-effective for most use cases while maintaining good quality",
    "confidence": 0.8,
    "entities": ["text-embedding-3-small"],
    "category": "evaluation"
  }},
  {{
    "network": "observation",
    "content": "Memory systems are converging on hybrid architectures: vector DB + structured store + LLM consolidation",
    "confidence": 0.85,
    "entities": ["vector DB", "LLM"],
    "category": "pattern"
  }}
]
```

Now extract memories from the provided content. Return ONLY valid JSON, no markdown formatting.
"""


def get_entity_extraction_prompt(content: str) -> str:
    """Prompt for extracting entities from content"""
    return f"""Extract named entities from the following content.

Entities include:
- People (names, roles)
- Organizations (companies, teams, projects)
- Technologies (databases, frameworks, APIs, tools)
- Concepts (architectures, patterns, theories)
- Locations (physical or virtual)
- Events (meetings, releases, milestones)

Content:
```
{content[:2000]}  # Limit content length
```

Output format: JSON array of entity objects with:
- name: The entity name
- type: One of ["person", "organization", "technology", "concept", "location", "event"]
- mentions: Count of mentions in content

Example:
```json
[
  {{"name": "PostgreSQL", "type": "technology", "mentions": 3}},
  {{"name": "Hindsight", "type": "concept", "mentions": 5}},
  {{"name": "OpenAI", "type": "organization", "mentions": 2}}
]
```

Return ONLY valid JSON.
"""


def get_relationship_extraction_prompt(content: str, entities: List[str]) -> str:
    """Prompt for extracting relationships between entities"""
    entities_str = ", ".join(entities[:20])  # Limit to 20 entities

    return f"""Extract relationships between the following entities found in the content.

Entities: {entities_str}

Content:
```
{content[:2000]}
```

Identify relationships like:
- uses/used_by (technology relationships)
- part_of/has_part (compositional)
- relates_to (general association)
- implements/implemented_by (implementation)
- depends_on/depended_on_by (dependencies)
- created_by/creates (authorship)

Output format: JSON array of relationship objects with:
- subject: Source entity
- predicate: Relationship type
- object: Target entity
- confidence: 0.0-1.0 score

Example:
```json
[
  {{"subject": "Hindsight", "predicate": "uses", "object": "PostgreSQL", "confidence": 0.9}},
  {{"subject": "RETAIN", "predicate": "part_of", "object": "Hindsight", "confidence": 0.95}}
]
```

Return ONLY valid JSON.
"""


# Prompt templates for specific content types
CONTENT_TYPE_PROMPTS: Dict[str, Dict[str, str]] = {
    "task": {
        "focus": "task objectives, success criteria, approach, dependencies",
        "network_hints": {
            "world": "Extract objectives as facts, decisions about approach",
            "experience": "Extract planned actions, tools to be used",
            "opinion": "Extract assumptions, risk assessments",
            "observation": "Extract patterns from similar tasks"
        }
    },
    "thoughts": {
        "focus": "reasoning process, analysis, conclusions",
        "network_hints": {
            "world": "Extract discovered facts, identified entities",
            "experience": "Extract analysis steps, tools used for investigation",
            "opinion": "Extract conclusions reached, confidence levels",
            "observation": "Extract insights, patterns noticed"
        }
    },
    "decisions": {
        "focus": "decisions made, rationale, alternatives considered",
        "network_hints": {
            "world": "Extract decisions as facts, chosen options",
            "experience": "Extract decision process, who was involved",
            "opinion": "Extract rationale as beliefs, confidence in decision",
            "observation": "Extract implications, patterns in decision-making"
        }
    },
    "results": {
        "focus": "outcomes, metrics, what was accomplished",
        "network_hints": {
            "world": "Extract outcomes as facts, metrics achieved",
            "experience": "Extract what was actually done vs planned",
            "opinion": "Extract evaluation of success, lessons learned",
            "observation": "Extract insights from results, unexpected findings"
        }
    }
}


def get_content_type_guidance(content_type: str) -> str:
    """Get guidance for a specific content type"""
    if content_type not in CONTENT_TYPE_PROMPTS:
        return ""

    prompt_info = CONTENT_TYPE_PROMPTS[content_type]
    hints = "\n".join([
        f"  {network}: {hint}"
        for network, hint in prompt_info["network_hints"].items()
    ])

    return f"""
Content Type Guidance ({content_type}):
- Focus on: {prompt_info['focus']}
- Network hints:
{hints}
"""
