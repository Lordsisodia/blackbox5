#!/usr/bin/env python3
"""
RETAIN Operation - Production Implementation

Extracts structured memories from tasks/runs and stores them in:
- PostgreSQL + pgvector (memories with embeddings)
- Neo4j (entities and relationships)

Usage:
    # Extract from single file
    python retain.py --source tasks/active/TASK-001/task.md

    # Extract from run directory
    python retain.py --source runs/unknown/completed/run-XXX/

    # Dry run (don't store)
    python retain.py --source TASK.md --dry-run
"""

import argparse
import asyncio
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import asdict

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.memory import Memory, MemoryNetwork, Entity, Relationship


class RetainEngine:
    """
    Production RETAIN operation for Hindsight memory architecture.

    Uses LLM for extraction, generates embeddings, stores in databases.
    """

    def __init__(self, openai_api_key: Optional[str] = None):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.memories: List[Memory] = []
        self.entities: List[Entity] = []
        self.relationships: List[Relationship] = []

    async def process_file(self, file_path: Path, dry_run: bool = False) -> List[Memory]:
        """Process a single file and extract memories"""
        print(f"Processing: {file_path}")

        content = file_path.read_text()

        # Determine content type from filename
        content_type = self._detect_content_type(file_path)

        # Extract frontmatter and body
        frontmatter = self._extract_frontmatter(content)
        body = self._extract_body(content)

        # Extract memories using LLM
        memories = await self._extract_memories_llm(body, str(file_path), content_type)

        # Extract entities
        entities = await self._extract_entities_llm(body)

        # Extract relationships between entities
        entity_names = [e.name for e in entities]
        relationships = await self._extract_relationships_llm(body, entity_names)

        # Generate embeddings for memories
        for memory in memories:
            memory.embedding = await self._generate_embedding(memory.content)
            memory.entities = [e for e in entity_names if e.lower() in memory.content.lower()]

        self.memories.extend(memories)
        self.entities.extend(entities)
        self.relationships.extend(relationships)

        if not dry_run:
            await self._store_memories(memories)
            await self._store_entities(entities)
            await self._store_relationships(relationships)

        print(f"  Extracted: {len(memories)} memories, {len(entities)} entities, {len(relationships)} relationships")
        return memories

    def _detect_content_type(self, file_path: Path) -> str:
        """Detect content type from filename"""
        name = file_path.name.lower()
        if "thoughts" in name:
            return "thoughts"
        elif "decisions" in name:
            return "decisions"
        elif "results" in name:
            return "results"
        elif "task" in name:
            return "task"
        else:
            return "generic"

    def _extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """Extract YAML frontmatter from markdown"""
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    import yaml
                    return yaml.safe_load(parts[1]) or {}
                except ImportError:
                    pass
        return {}

    def _extract_body(self, content: str) -> str:
        """Extract body content (without frontmatter)"""
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                return parts[2]
        return content

    async def _extract_memories_llm(self, content: str, source: str, content_type: str) -> List[Memory]:
        """Extract memories using LLM"""
        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=self.openai_api_key)

            # Build prompt
            system_prompt = """You are a memory extraction specialist. Extract structured memories from the provided content and classify them into one of four networks:

1. WORLD (world) - Objective facts: technical facts, decisions, entities, relationships
2. EXPERIENCE (experience) - First-person actions: what was done, tools used, learnings
3. OPINION (opinion) - Beliefs with confidence: judgments, evaluations, preferences
4. OBSERVATION (observation) - Synthesized insights: patterns, connections, anomalies

For each memory, provide:
- network: "world" | "experience" | "opinion" | "observation"
- content: Clear, specific text (be concrete, not vague)
- confidence: 0.0-1.0 score based on evidence strength
- category: Sub-category (e.g., "technical", "strategic", "learning")
- entities: List of entities mentioned (people, technologies, concepts)

Output as JSON array. Be specific and extract multiple memories if content is rich."""

            user_prompt = f"""Extract memories from this {content_type} content:

Source: {source}

Content:
```markdown
{content[:8000]}  # Limit content length
```

Output JSON array of memory objects with fields: network, content, confidence, category, entities"""

            response = await client.chat.completions.create(
                model="gpt-4o-mini",  # Cost-effective for extraction
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3,  # Low temperature for consistent extraction
            )

            result = json.loads(response.choices[0].message.content)
            memories_data = result.get("memories", [])

            # Convert to Memory objects
            memories = []
            for data in memories_data:
                memory = Memory(
                    network=MemoryNetwork.from_string(data.get("network", "world")),
                    content=data.get("content", ""),
                    confidence=data.get("confidence", 0.8),
                    category=data.get("category"),
                    entities=data.get("entities", []),
                    source=source,
                    source_type=content_type,
                    created_at=datetime.utcnow(),
                )
                memories.append(memory)

            return memories

        except Exception as e:
            print(f"  LLM extraction failed: {e}")
            # Fallback: create a simple memory from the content
            return [Memory(
                network=MemoryNetwork.OBSERVATION,
                content=f"Content from {source}: {content[:500]}...",
                confidence=0.5,
                source=source,
                source_type=content_type,
            )]

    async def _extract_entities_llm(self, content: str) -> List[Entity]:
        """Extract entities using LLM"""
        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=self.openai_api_key)

            system_prompt = """Extract named entities from the content. Entities include:
- People (names, roles)
- Organizations (companies, teams, projects)
- Technologies (databases, frameworks, APIs, tools)
- Concepts (architectures, patterns, theories)

Output JSON array with: name, type (person/organization/technology/concept), mentions"""

            user_prompt = f"""Extract entities from:

```
{content[:4000]}
```

Output JSON array."""

            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
            )

            result = json.loads(response.choices[0].message.content)
            entities_data = result.get("entities", [])

            entities = []
            for data in entities_data:
                entity = Entity(
                    name=data.get("name", ""),
                    type=data.get("type", "concept"),
                    mention_count=data.get("mentions", 1),
                    first_seen=datetime.utcnow(),
                )
                entities.append(entity)

            return entities

        except Exception as e:
            print(f"  Entity extraction failed: {e}")
            return []

    async def _extract_relationships_llm(self, content: str, entities: List[str]) -> List[Relationship]:
        """Extract relationships between entities"""
        if len(entities) < 2:
            return []

        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=self.openai_api_key)

            entities_str = ", ".join(entities[:15])  # Limit entities

            system_prompt = """Extract relationships between the provided entities.
Relationship types: uses, part_of, relates_to, implements, depends_on, created_by

Output JSON array with: subject, predicate (relationship type), object, confidence (0.0-1.0)"""

            user_prompt = f"""Entities: {entities_str}

Content:
```
{content[:3000]}
```

Output JSON array of relationships."""

            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
            )

            result = json.loads(response.choices[0].message.content)
            relationships_data = result.get("relationships", [])

            relationships = []
            for data in relationships_data:
                rel = Relationship(
                    subject=data.get("subject", ""),
                    predicate=data.get("predicate", "relates_to"),
                    object=data.get("object", ""),
                    confidence=data.get("confidence", 0.7),
                    first_observed=datetime.utcnow(),
                )
                relationships.append(rel)

            return relationships

        except Exception as e:
            print(f"  Relationship extraction failed: {e}")
            return []

    async def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding using OpenAI"""
        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=self.openai_api_key)

            response = await client.embeddings.create(
                model="text-embedding-3-small",
                input=text[:8000],  # Limit text length
            )

            return response.data[0].embedding

        except Exception as e:
            print(f"  Embedding generation failed: {e}")
            return []

    async def _store_memories(self, memories: List[Memory]):
        """Store memories in vector store"""
        from vector_store import VectorStore

        store = VectorStore()

        for memory in memories:
            # Generate embedding if not present
            if not memory.embedding:
                memory.embedding = await self._generate_embedding(memory.content)

            # Add to vector store
            store.add_memory(
                content=memory.content,
                network=memory.network.value,
                metadata={
                    "confidence": memory.confidence,
                    "source": memory.source,
                    "source_type": memory.source_type,
                    "category": memory.category,
                    "entities": memory.entities,
                    "created_at": memory.created_at.isoformat() if memory.created_at else None,
                }
            )

        print(f"  Stored {len(memories)} memories in vector store")

    async def _store_entities(self, entities: List[Entity]):
        """Store entities in vector store as special memory type"""
        from vector_store import VectorStore

        store = VectorStore()

        for entity in entities:
            # Create a memory for each entity (for searchability)
            content = f"Entity: {entity.name} (type: {entity.type})"
            if entity.mention_count > 1:
                content += f" - mentioned {entity.mention_count} times"

            store.add_memory(
                content=content,
                network="world",  # Entities are world facts
                metadata={
                    "entity_name": entity.name,
                    "entity_type": entity.type,
                    "mention_count": entity.mention_count,
                    "first_seen": entity.first_seen.isoformat() if entity.first_seen else None,
                    "is_entity": True,
                }
            )

        print(f"  Stored {len(entities)} entities")

    async def _store_relationships(self, relationships: List[Relationship]):
        """Store relationships in vector store"""
        from vector_store import VectorStore

        store = VectorStore()

        for rel in relationships:
            # Create a memory for each relationship
            content = f"Relationship: {rel.subject} {rel.predicate} {rel.object}"

            store.add_memory(
                content=content,
                network="observation",  # Relationships are synthesized observations
                metadata={
                    "subject": rel.subject,
                    "predicate": rel.predicate,
                    "object": rel.object,
                    "confidence": rel.confidence,
                    "is_relationship": True,
                }
            )

        print(f"  Stored {len(relationships)} relationships")

    def save_to_files(self, output_dir: Path):
        """Save extracted data to JSON files (for testing)"""
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save memories by network
        by_network: Dict[str, List[Dict]] = {}
        for memory in self.memories:
            network = memory.network.value
            if network not in by_network:
                by_network[network] = []
            by_network[network].append(memory.to_dict())

        for network, memories in by_network.items():
            with open(output_dir / f"{network}_memories.json", "w") as f:
                json.dump(memories, f, indent=2, default=str)

        # Save all memories
        with open(output_dir / "all_memories.json", "w") as f:
            json.dump([m.to_dict() for m in self.memories], f, indent=2, default=str)

        # Save entities
        with open(output_dir / "entities.json", "w") as f:
            json.dump([e.to_dict() for e in self.entities], f, indent=2, default=str)

        # Save relationships
        with open(output_dir / "relationships.json", "w") as f:
            json.dump([r.to_dict() for r in self.relationships], f, indent=2, default=str)

        print(f"\nSaved to {output_dir}:")
        print(f"  - {len(self.memories)} memories")
        print(f"  - {len(self.entities)} entities")
        print(f"  - {len(self.relationships)} relationships")


async def main():
    parser = argparse.ArgumentParser(description="RETAIN operation - extract and store memories")
    parser.add_argument("--source", required=True, help="Source file or directory")
    parser.add_argument("--output", default="./retain_output", help="Output directory (for dry-run)")
    parser.add_argument("--dry-run", action="store_true", help="Don't store to database, just output")
    parser.add_argument("--api-key", help="OpenAI API key (or set OPENAI_API_KEY env var)")
    args = parser.parse_args()

    source = Path(args.source)
    output = Path(args.output)

    if not source.exists():
        print(f"Source not found: {source}")
        sys.exit(1)

    engine = RetainEngine(openai_api_key=args.api_key)

    if source.is_file():
        await engine.process_file(source, dry_run=args.dry_run)
    elif source.is_dir():
        md_files = list(source.rglob("*.md"))
        print(f"Found {len(md_files)} markdown files")
        for md_file in md_files:
            try:
                await engine.process_file(md_file, dry_run=args.dry_run)
            except Exception as e:
                print(f"  Error processing {md_file}: {e}")

    if args.dry_run:
        engine.save_to_files(output)

    print("\nRETAIN complete.")


if __name__ == "__main__":
    asyncio.run(main())
