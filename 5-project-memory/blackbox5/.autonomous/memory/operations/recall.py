#!/usr/bin/env python3
"""
RECALL Operation - Production Implementation with Vector Store

Multi-strategy memory retrieval using JSON + in-memory vectors:
- Semantic search (vector similarity)
- Keyword search (BM25-style)
- Network filtering
- Confidence filtering

Usage:
    python recall.py --query "authentication patterns"
    python recall.py --query "database" --network world
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from vector_store import VectorStore


def format_results(results, verbose: bool = False) -> str:
    """Format search results for display"""
    if not results:
        return "No memories found."

    lines = []
    lines.append(f"\n{'='*70}")
    lines.append(f"RECALL RESULTS ({len(results)} memories)")
    lines.append(f"{'='*70}\n")

    for i, (memory, score) in enumerate(results, 1):
        lines.append(f"{i}. [{memory.network.upper()}] Score: {score:.3f}")

        metadata = memory.metadata
        confidence = metadata.get('confidence', 'N/A')
        source = metadata.get('source', 'unknown')

        lines.append(f"   Confidence: {confidence} | Source: {source}")

        content = memory.content.replace('\n', ' ')
        if len(content) > 200:
            content = content[:200] + "..."
        lines.append(f"   Content: {content}")

        entities = metadata.get('entities', [])
        if entities:
            lines.append(f"   Entities: {', '.join(entities[:5])}")

        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="RECALL operation - retrieve memories")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--network", choices=["world", "experience", "opinion", "observation"],
                       help="Filter by network")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    # Initialize vector store
    store = VectorStore()

    # Search
    results = store.search(
        query=args.query,
        top_k=args.top_k,
        network=args.network
    )

    # Display results
    print(format_results(results, verbose=args.verbose))

    # Show stats
    stats = store.get_stats()
    print(f"\nStore stats: {stats['total_memories']} total memories")


if __name__ == "__main__":
    main()
