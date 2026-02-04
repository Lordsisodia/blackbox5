#!/usr/bin/env python3
"""
REFLECT Operation - Belief Consolidation and Pattern Detection

Analyzes memories across the 4-network architecture to:
1. Detect contradictions (especially in opinion network)
2. Identify patterns and synthesize insights
3. Update confidence scores based on evidence
4. Consolidate related memories

Usage:
    python reflect.py --dry-run              # Preview what would be consolidated
    python reflect.py --network opinion      # Reflect on specific network
    python reflect.py --full                 # Run full reflection pipeline
"""

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from vector_store import VectorStore


@dataclass
class Contradiction:
    """Detected contradiction between memories"""
    memory_id_1: str
    memory_id_2: str
    content_1: str
    content_2: str
    confidence_delta: float
    suggested_resolution: str


@dataclass
class Pattern:
    """Detected pattern across memories"""
    pattern_type: str  # "recurring_theme", "trend", "correlation"
    description: str
    memory_ids: List[str]
    confidence: float
    synthesized_memory: Optional[str] = None


class ReflectEngine:
    """
    REFLECT operation for Hindsight memory architecture.

    Implements belief updating through contradiction detection,
    pattern recognition, and memory consolidation.
    """

    def __init__(self, openai_api_key: Optional[str] = None):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.vector_store = VectorStore()
        self.contradictions: List[Contradiction] = []
        self.patterns: List[Pattern] = []

    async def reflect(self, network: Optional[str] = None, dry_run: bool = True) -> Dict[str, Any]:
        """
        Run reflection on memories.

        Args:
            network: Specific network to reflect on (or None for all)
            dry_run: If True, don't actually modify memories

        Returns:
            Reflection results summary
        """
        print(f"REFLECT: Analyzing memories{' in ' + network if network else ''}...")

        # Get all memories (or filtered by network)
        memories = list(self.vector_store.memories.values())
        if network:
            memories = [m for m in memories if m.network == network]

        if not memories:
            return {"status": "no_memories", "count": 0}

        print(f"  Loaded {len(memories)} memories for analysis")

        # Phase 1: Detect contradictions
        print("\n[Phase 1] Detecting contradictions...")
        self.contradictions = await self._detect_contradictions(memories)
        print(f"  Found {len(self.contradictions)} contradictions")

        # Phase 2: Identify patterns
        print("\n[Phase 2] Identifying patterns...")
        self.patterns = await self._identify_patterns(memories)
        print(f"  Found {len(self.patterns)} patterns")

        # Phase 3: Synthesize new insights
        print("\n[Phase 3] Synthesizing insights...")
        new_insights = await self._synthesize_insights(memories, self.patterns)
        print(f"  Generated {len(new_insights)} new insights")

        # Phase 4: Update confidences (if not dry-run)
        if not dry_run:
            print("\n[Phase 4] Updating memory confidences...")
            updates = await self._update_confidences(memories)
            print(f"  Updated {updates} memories")

        # Build result summary
        result = {
            "status": "completed",
            "memories_analyzed": len(memories),
            "contradictions_found": len(self.contradictions),
            "patterns_found": len(self.patterns),
            "new_insights": len(new_insights),
            "dry_run": dry_run,
            "contradictions": [
                {
                    "memory_1": c.content_1[:80] + "...",
                    "memory_2": c.content_2[:80] + "...",
                    "resolution": c.suggested_resolution[:100]
                }
                for c in self.contradictions[:5]  # Limit output
            ],
            "patterns": [
                {
                    "type": p.pattern_type,
                    "description": p.description[:100],
                    "memory_count": len(p.memory_ids)
                }
                for p in self.patterns[:5]
            ]
        }

        return result

    async def _detect_contradictions(self, memories: List) -> List[Contradiction]:
        """Detect contradictions between memories using LLM"""
        contradictions = []

        # Focus on opinion network for contradictions
        opinion_memories = [m for m in memories if m.network == "opinion"]

        if len(opinion_memories) < 2:
            return contradictions

        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=self.openai_api_key)

            # Build prompt with opinion memories
            memories_text = "\n".join([
                f"{i+1}. [{m.metadata.get('confidence', 0.8)}] {m.content}"
                for i, m in enumerate(opinion_memories[:20])  # Limit for context
            ])

            system_prompt = """You are a contradiction detection specialist.
Analyze the provided memories (opinions/beliefs) and identify any contradictions.

A contradiction occurs when two beliefs cannot both be true.
Look for:
- Direct logical conflicts
- Opposing recommendations
- Inconsistent evaluations
- Conflicting preferences

Output JSON array of contradictions with:
- memory_indices: [index1, index2] (1-based)
- explanation: Why they contradict
- suggested_resolution: How to resolve or which to prefer"""

            user_prompt = f"""Analyze these opinion memories for contradictions:

{memories_text}

Output JSON array of detected contradictions."""

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
            contradictions_data = result.get("contradictions", [])

            for data in contradictions_data:
                indices = data.get("memory_indices", [])
                if len(indices) == 2:
                    idx1, idx2 = indices[0] - 1, indices[1] - 1
                    if 0 <= idx1 < len(opinion_memories) and 0 <= idx2 < len(opinion_memories):
                        m1, m2 = opinion_memories[idx1], opinion_memories[idx2]
                        contradictions.append(Contradiction(
                            memory_id_1=m1.id,
                            memory_id_2=m2.id,
                            content_1=m1.content,
                            content_2=m2.content,
                            confidence_delta=abs(
                                m1.metadata.get("confidence", 0.8) -
                                m2.metadata.get("confidence", 0.8)
                            ),
                            suggested_resolution=data.get("suggested_resolution", "")
                        ))

        except Exception as e:
            print(f"  LLM contradiction detection failed: {e}")
            # Fallback: Simple keyword-based contradiction detection
            contradictions = self._detect_contradictions_fallback(opinion_memories)

        return contradictions

    def _detect_contradictions_fallback(self, memories: List) -> List[Contradiction]:
        """Simple fallback contradiction detection"""
        contradictions = []

        # Look for negation patterns
        negation_words = ["not", "never", "no ", "don't", "doesn't", "shouldn't"]

        for i, m1 in enumerate(memories):
            for m2 in memories[i+1:]:
                # Check if one negates the other
                m1_lower = m1.content.lower()
                m2_lower = m2.content.lower()

                has_negation_1 = any(w in m1_lower for w in negation_words)
                has_negation_2 = any(w in m2_lower for w in negation_words)

                if has_negation_1 != has_negation_2:
                    # Check for similar content (simple word overlap)
                    words1 = set(m1_lower.split())
                    words2 = set(m2_lower.split())
                    overlap = len(words1 & words2) / max(len(words1), len(words2))

                    if overlap > 0.5:
                        contradictions.append(Contradiction(
                            memory_id_1=m1.id,
                            memory_id_2=m2.id,
                            content_1=m1.content,
                            content_2=m2.content,
                            confidence_delta=0.2,
                            suggested_resolution="Review both beliefs and determine which has stronger evidence"
                        ))

        return contradictions

    async def _identify_patterns(self, memories: List) -> List[Pattern]:
        """Identify patterns across memories"""
        patterns = []

        # Group memories by network
        by_network = {}
        for m in memories:
            net = m.network
            if net not in by_network:
                by_network[net] = []
            by_network[net].append(m)

        # Look for recurring themes within each network
        for network, net_memories in by_network.items():
            if len(net_memories) < 3:
                continue

            # Use LLM to identify patterns
            try:
                from openai import AsyncOpenAI
                client = AsyncOpenAI(api_key=self.openai_api_key)

                memories_text = "\n".join([
                    f"{i+1}. {m.content}"
                    for i, m in enumerate(net_memories[:15])
                ])

                system_prompt = """Identify patterns across these memories.

Pattern types:
- recurring_theme: Topic that appears multiple times
- trend: Direction of change over time
- correlation: Things that appear together

Output JSON array with:
- pattern_type: type of pattern
- description: What the pattern shows
- memory_indices: List of memory indices (1-based) that support this pattern"""

                user_prompt = f"""Network: {network}

Memories:
{memories_text}

Identify patterns."""

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
                patterns_data = result.get("patterns", [])

                for data in patterns_data:
                    indices = data.get("memory_indices", [])
                    memory_ids = [
                        net_memories[i-1].id for i in indices
                        if 0 < i <= len(net_memories)
                    ]

                    if memory_ids:
                        patterns.append(Pattern(
                            pattern_type=data.get("pattern_type", "recurring_theme"),
                            description=data.get("description", ""),
                            memory_ids=memory_ids,
                            confidence=0.7,
                        ))

            except Exception as e:
                print(f"  Pattern detection failed for {network}: {e}")

        return patterns

    async def _synthesize_insights(self, memories: List, patterns: List[Pattern]) -> List[str]:
        """Synthesize new insights from patterns"""
        new_insights = []

        for pattern in patterns:
            if len(pattern.memory_ids) >= 3 and pattern.pattern_type == "recurring_theme":
                # Create a synthesized observation memory
                insight_content = f"Pattern detected: {pattern.description}"

                # Only add if not already exists
                existing = self.vector_store.search(insight_content, top_k=1)
                if not existing or existing[0][1] < 0.9:
                    self.vector_store.add_memory(
                        content=insight_content,
                        network="observation",
                        metadata={
                            "confidence": pattern.confidence,
                            "synthesized_from": pattern.memory_ids,
                            "pattern_type": pattern.pattern_type,
                            "created_by": "reflect_operation"
                        }
                    )
                    new_insights.append(insight_content)

        return new_insights

    async def _update_confidences(self, memories: List) -> int:
        """Update confidence scores based on evidence"""
        updates = 0

        # For now, simple confidence adjustment based on contradictions
        for contradiction in self.contradictions:
            # Reduce confidence of both contradictory memories slightly
            for memory_id in [contradiction.memory_id_1, contradiction.memory_id_2]:
                memory = self.vector_store.get_memory(memory_id)
                if memory and "confidence" in memory.metadata:
                    old_conf = memory.metadata["confidence"]
                    new_conf = max(0.1, old_conf - 0.1)
                    memory.metadata["confidence"] = new_conf
                    updates += 1

        # Save changes
        if updates > 0:
            self.vector_store._save_all()

        return updates

    def format_report(self) -> str:
        """Format reflection results as readable report"""
        lines = []
        lines.append("\n" + "="*70)
        lines.append("REFLECTION REPORT")
        lines.append("="*70)

        # Contradictions
        lines.append(f"\n## Contradictions Found: {len(self.contradictions)}")
        if self.contradictions:
            for i, c in enumerate(self.contradictions[:5], 1):
                lines.append(f"\n{i}. Confidence delta: {c.confidence_delta:.2f}")
                lines.append(f"   Memory 1: {c.content_1[:60]}...")
                lines.append(f"   Memory 2: {c.content_2[:60]}...")
                lines.append(f"   Resolution: {c.suggested_resolution[:80]}...")
        else:
            lines.append("   No contradictions detected.")

        # Patterns
        lines.append(f"\n## Patterns Found: {len(self.patterns)}")
        if self.patterns:
            for i, p in enumerate(self.patterns[:5], 1):
                lines.append(f"\n{i}. [{p.pattern_type.upper()}]")
                lines.append(f"   {p.description[:100]}...")
                lines.append(f"   Based on {len(p.memory_ids)} memories")
        else:
            lines.append("   No patterns detected.")

        lines.append("\n" + "="*70)
        return "\n".join(lines)


async def main():
    parser = argparse.ArgumentParser(description="REFLECT operation - consolidate memories")
    parser.add_argument("--network", choices=["world", "experience", "opinion", "observation"],
                       help="Reflect on specific network only")
    parser.add_argument("--full", action="store_true", help="Apply changes (not dry-run)")
    parser.add_argument("--api-key", help="OpenAI API key")
    args = parser.parse_args()

    engine = ReflectEngine(openai_api_key=args.api_key)

    result = await engine.reflect(
        network=args.network,
        dry_run=not args.full
    )

    # Print report
    print(engine.format_report())

    # Print summary
    print(f"\nSummary:")
    print(f"  Memories analyzed: {result['memories_analyzed']}")
    print(f"  Contradictions: {result['contradictions_found']}")
    print(f"  Patterns: {result['patterns_found']}")
    print(f"  New insights: {result['new_insights']}")
    print(f"  Mode: {'DRY-RUN (no changes)' if result['dry_run'] else 'APPLIED'}")


if __name__ == "__main__":
    asyncio.run(main())
