#!/usr/bin/env python3
"""
SessionStart Memory Loader

Automatically recalls relevant memories at session start based on:
1. Current task context (active tasks)
2. Project context
3. Recent conversation patterns

Called by: ralf-session-start-hook.sh
Outputs: Memory context for AGENT_CONTEXT.md
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add memory module to path
sys.path.insert(0, str(Path(__file__).parent))

from vector_store import VectorStore


def get_active_task_context(project_dir: Path) -> List[str]:
    """Extract context from active tasks"""
    context_terms = []

    tasks_dir = project_dir / "tasks" / "active"
    if not tasks_dir.exists():
        return context_terms

    # Read active task files
    for task_file in tasks_dir.rglob("*.md"):
        try:
            content = task_file.read_text()
            # Extract title and key terms
            lines = content.split('\n')
            for line in lines[:20]:  # First 20 lines
                if line.startswith('# '):
                    context_terms.append(line.replace('# ', '').strip())
                elif line.startswith('**'):
                    context_terms.append(line.strip('*').strip())
        except Exception:
            pass

    return context_terms


def get_project_context(project_dir: Path) -> str:
    """Get project name from directory"""
    return project_dir.name


def build_search_queries(project_dir: Path) -> List[str]:
    """Build search queries from current context"""
    queries = []

    # Project name
    project = get_project_context(project_dir)
    queries.append(project)

    # Active tasks
    task_contexts = get_active_task_context(project_dir)
    queries.extend(task_contexts[:3])  # Limit to top 3

    # If no task context, use generic queries
    if not queries:
        queries = ["current task", "active work"]

    return queries


def recall_memories_for_session(
    project_dir: Path,
    top_k: int = 5,
    min_score: float = 0.1
) -> Dict[str, Any]:
    """
    Recall relevant memories for the current session.

    Args:
        project_dir: Path to project directory
        top_k: Number of memories per query
        min_score: Minimum similarity score

    Returns:
        Dictionary with memories and metadata
    """
    store = VectorStore()

    # Build search queries from context
    queries = build_search_queries(project_dir)

    # Collect memories from all queries
    all_memories = []
    seen_ids = set()

    for query in queries:
        results = store.search(query, top_k=top_k)
        for memory, score in results:
            if score >= min_score and memory.id not in seen_ids:
                all_memories.append((memory, score))
                seen_ids.add(memory.id)

    # Sort by score and take top results
    all_memories.sort(key=lambda x: x[1], reverse=True)
    top_memories = all_memories[:top_k]

    return {
        "memories": [
            {
                "id": m.id,
                "content": m.content,
                "network": m.network,
                "score": score,
                "metadata": m.metadata
            }
            for m, score in top_memories
        ],
        "queries_used": queries,
        "total_recall": len(top_memories),
        "store_stats": store.get_stats()
    }


def format_memory_context(result: Dict[str, Any]) -> str:
    """Format memories for injection into AGENT_CONTEXT.md"""
    lines = []

    lines.append("## Relevant Memories")
    lines.append("")

    if not result["memories"]:
        lines.append("*No relevant memories found.*")
        return "\n".join(lines)

    # Group by network
    by_network: Dict[str, List[Dict]] = {}
    for mem in result["memories"]:
        net = mem["network"]
        if net not in by_network:
            by_network[net] = []
        by_network[net].append(mem)

    # Output by network
    network_order = ["world", "experience", "opinion", "observation"]
    for network in network_order:
        if network in by_network:
            lines.append(f"### {network.upper()}")
            lines.append("")
            for mem in by_network[network]:
                confidence = mem["metadata"].get("confidence", "N/A")
                lines.append(f"- **{mem['content'][:120]}...**")
                lines.append(f"  (confidence: {confidence}, relevance: {mem['score']:.2f})")
                lines.append("")

    lines.append(f"---")
    lines.append(f"*Recalled {result['total_recall']} memories from {result['store_stats']['total_memories']} total*")

    return "\n".join(lines)


def main():
    """CLI entry point for hook integration"""
    import argparse

    parser = argparse.ArgumentParser(description="SessionStart memory loader")
    parser.add_argument("--project-dir", help="Project directory path")
    parser.add_argument("--top-k", type=int, default=5, help="Number of memories")
    parser.add_argument("--format", choices=["context", "json"], default="context",
                       help="Output format")
    args = parser.parse_args()

    # Determine project directory
    if args.project_dir:
        project_dir = Path(args.project_dir)
    else:
        # Try to find from environment or default
        project_dir = Path(os.getenv("RALF_PROJECT_ROOT", "."))

    if not project_dir.exists():
        print(f"Error: Project directory not found: {project_dir}", file=sys.stderr)
        return 1

    # Recall memories
    result = recall_memories_for_session(project_dir, top_k=args.top_k)

    # Output
    if args.format == "json":
        import json
        print(json.dumps(result, indent=2, default=str))
    else:
        print(format_memory_context(result))

    return 0


if __name__ == "__main__":
    sys.exit(main())
