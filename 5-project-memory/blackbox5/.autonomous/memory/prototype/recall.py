#!/usr/bin/env python3
"""
RECALL Operation Prototype for Hindsight Memory Architecture

This prototype demonstrates the multi-strategy retrieval system:
- Semantic search (using simple keyword matching as placeholder)
- Keyword search (BM25-style)
- Network filtering (World/Experience/Opinion/Observation)
- Temporal filtering (recency)

Usage:
    python recall.py --query "authentication patterns" --memories ./memories/
    python recall.py --query "Hindsight" --network world --limit 5
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict
import math


@dataclass
class MemoryResult:
    """A memory result with relevance score"""
    memory: dict
    score: float
    strategy: str  # Which search strategy found this

    def __repr__(self):
        return f"[{self.strategy}:{self.score:.2f}] {self.memory['content'][:80]}..."


class RecallEngine:
    """
    RECALL operation engine for multi-strategy memory retrieval.

    In the full implementation, this would use:
    - pgvector for semantic search
    - PostgreSQL full-text for keyword search
    - Neo4j for graph traversal
    """

    def __init__(self, memories_dir: Path):
        self.memories_dir = memories_dir
        self.memories: List[dict] = []
        self._load_memories()

    def _load_memories(self):
        """Load all memories from the memories directory"""
        all_file = self.memories_dir / "all_memories.json"
        if all_file.exists():
            with open(all_file) as f:
                self.memories = json.load(f)
        else:
            # Load individual network files
            for network in ["world", "experience", "opinion", "observation"]:
                network_file = self.memories_dir / f"{network}_memories.json"
                if network_file.exists():
                    with open(network_file) as f:
                        self.memories.extend(json.load(f))

        print(f"Loaded {len(self.memories)} memories")

    def recall(self, query: str, network: Optional[str] = None,
               strategies: List[str] = None, limit: int = 5) -> List[MemoryResult]:
        """
        Multi-strategy recall operation.

        Args:
            query: Search query
            network: Filter by network (world/experience/opinion/observation)
            strategies: List of strategies to use (semantic, keyword, temporal)
            limit: Maximum results to return
        """
        if strategies is None:
            strategies = ["semantic", "keyword"]

        # Filter by network if specified
        memories = self.memories
        if network:
            memories = [m for m in memories if m.get("network") == network]

        # Run each strategy
        all_results: Dict[str, List[MemoryResult]] = {}

        if "semantic" in strategies:
            all_results["semantic"] = self._semantic_search(query, memories)

        if "keyword" in strategies:
            all_results["keyword"] = self._keyword_search(query, memories)

        if "temporal" in strategies:
            all_results["temporal"] = self._temporal_search(memories)

        # Merge results using Reciprocal Rank Fusion (RRF)
        merged = self._reciprocal_rank_fusion(all_results, k=60)

        return merged[:limit]

    def _semantic_search(self, query: str, memories: List[dict]) -> List[MemoryResult]:
        """
        Semantic search using keyword overlap as placeholder.
        In production: use pgvector cosine similarity.
        """
        query_terms = set(self._tokenize(query))
        results = []

        for memory in memories:
            content = memory.get("content", "")
            content_terms = set(self._tokenize(content))

            # Jaccard similarity as placeholder for semantic similarity
            intersection = query_terms & content_terms
            union = query_terms | content_terms
            similarity = len(intersection) / len(union) if union else 0

            # Boost by entity overlap
            entities = set(memory.get("entities", []))
            entity_overlap = len(query_terms & entities)
            similarity += entity_overlap * 0.1

            if similarity > 0.1:
                results.append(MemoryResult(
                    memory=memory,
                    score=similarity,
                    strategy="semantic"
                ))

        return sorted(results, key=lambda x: x.score, reverse=True)

    def _keyword_search(self, query: str, memories: List[dict]) -> List[MemoryResult]:
        """
        Keyword search using BM25-style scoring.
        In production: use PostgreSQL full-text search.
        """
        query_terms = self._tokenize(query)
        results = []

        # Calculate IDF for each term
        idf = {}
        for term in set(query_terms):
            doc_freq = sum(1 for m in memories if term in self._tokenize(m.get("content", "")))
            idf[term] = math.log((len(memories) - doc_freq + 0.5) / (doc_freq + 0.5) + 1)

        for memory in memories:
            content = memory.get("content", "")
            content_terms = self._tokenize(content)

            # BM25-style scoring
            score = 0
            k1 = 1.5
            b = 0.75
            avgdl = sum(len(self._tokenize(m.get("content", ""))) for m in memories) / len(memories)

            for term in query_terms:
                if term in content_terms:
                    tf = content_terms.count(term)
                    doc_len = len(content_terms)
                    score += idf.get(term, 0) * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_len / avgdl))

            if score > 0:
                results.append(MemoryResult(
                    memory=memory,
                    score=score,
                    strategy="keyword"
                ))

        return sorted(results, key=lambda x: x.score, reverse=True)

    def _temporal_search(self, memories: List[dict]) -> List[MemoryResult]:
        """
        Temporal search - prioritize recent memories.
        """
        results = []
        now = datetime.now()

        for memory in memories:
            timestamp = memory.get("timestamp")
            if timestamp:
                try:
                    memory_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    days_old = (now - memory_time).days
                    # Recency score: newer = higher score
                    recency = 1.0 / (1 + days_old / 30)  # Decay over 30 days
                except:
                    recency = 0.5
            else:
                recency = 0.5

            results.append(MemoryResult(
                memory=memory,
                score=recency,
                strategy="temporal"
            ))

        return sorted(results, key=lambda x: x.score, reverse=True)

    def _reciprocal_rank_fusion(self, results_by_strategy: Dict[str, List[MemoryResult]], k: int = 60) -> List[MemoryResult]:
        """
        Merge results from multiple strategies using Reciprocal Rank Fusion.

        RRF score = sum(1 / (k + rank)) for each strategy
        """
        # Track ranks for each memory
        memory_ranks: Dict[str, Dict[str, int]] = {}

        for strategy, results in results_by_strategy.items():
            for rank, result in enumerate(results, start=1):
                memory_id = result.memory.get("content", "")[:100]  # Simple ID
                if memory_id not in memory_ranks:
                    memory_ranks[memory_id] = {"memory": result.memory, "ranks": {}}
                memory_ranks[memory_id]["ranks"][strategy] = rank

        # Calculate RRF scores
        rrf_results = []
        for memory_id, data in memory_ranks.items():
            rrf_score = sum(1.0 / (k + rank) for rank in data["ranks"].values())
            rrf_results.append(MemoryResult(
                memory=data["memory"],
                score=rrf_score,
                strategy="rrf_merged"
            ))

        return sorted(rrf_results, key=lambda x: x.score, reverse=True)

    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization"""
        # Lowercase and extract words
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        # Filter short words
        return [w for w in words if len(w) > 2]

    def format_results(self, results: List[MemoryResult]) -> str:
        """Format results for display"""
        lines = []
        lines.append(f"\n{'='*60}")
        lines.append(f"RECALL RESULTS ({len(results)} memories)")
        lines.append(f"{'='*60}\n")

        for i, result in enumerate(results, 1):
            memory = result.memory
            lines.append(f"{i}. [{result.strategy}] Score: {result.score:.3f}")
            lines.append(f"   Network: {memory.get('network', 'unknown').upper()}")
            lines.append(f"   Confidence: {memory.get('confidence', 'N/A')}")
            lines.append(f"   Source: {memory.get('source', 'unknown')}")
            lines.append(f"   Content: {memory.get('content', 'N/A')[:150]}...")
            if memory.get('entities'):
                lines.append(f"   Entities: {', '.join(memory['entities'][:5])}")
            lines.append("")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="RECALL operation prototype")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--memories", default="./memories", help="Memories directory")
    parser.add_argument("--network", choices=["world", "experience", "opinion", "observation"],
                       help="Filter by network")
    parser.add_argument("--strategies", nargs="+", choices=["semantic", "keyword", "temporal"],
                       default=["semantic", "keyword"], help="Search strategies")
    parser.add_argument("--limit", type=int, default=5, help="Maximum results")
    args = parser.parse_args()

    memories_dir = Path(args.memories)
    if not memories_dir.exists():
        print(f"Memories directory not found: {memories_dir}")
        print("Run retain.py first to extract memories.")
        sys.exit(1)

    engine = RecallEngine(memories_dir)
    results = engine.recall(
        query=args.query,
        network=args.network,
        strategies=args.strategies,
        limit=args.limit
    )

    print(engine.format_results(results))


if __name__ == "__main__":
    main()
