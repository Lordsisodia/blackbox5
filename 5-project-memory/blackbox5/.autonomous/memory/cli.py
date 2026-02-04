#!/usr/bin/env python3
"""
bb5 memory CLI - Unified interface for Hindsight memory operations

Commands:
    retain      Extract memories from files/tasks
    recall      Search memories
    reflect     Run belief consolidation
    stats       Show memory statistics
    export      Export memories to JSON
    import      Import memories from JSON

Usage:
    bb5-memory retain <file_or_directory>
    bb5-memory recall "search query" --top-k 5
    bb5-memory reflect --full
    bb5-memory stats
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Optional

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from vector_store import VectorStore


def cmd_retain(args):
    """RETAIN command - extract memories from files"""
    from operations.retain import RetainEngine

    source = Path(args.source)
    if not source.exists():
        print(f"Error: Source not found: {source}")
        return 1

    async def run():
        engine = RetainEngine()

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

        if args.dry_run and args.output:
            engine.save_to_files(Path(args.output))

        print("\nRETAIN complete.")

    asyncio.run(run())
    return 0


def cmd_recall(args):
    """RECALL command - search memories"""
    store = VectorStore()

    results = store.search(
        query=args.query,
        top_k=args.top_k,
        network=args.network
    )

    if not results:
        print("No memories found.")
        return 0

    print(f"\n{'='*70}")
    print(f"RECALL RESULTS ({len(results)} memories)")
    print(f"{'='*70}\n")

    for i, (memory, score) in enumerate(results, 1):
        print(f"{i}. [{memory.network.upper()}] Score: {score:.3f}")

        metadata = memory.metadata
        confidence = metadata.get('confidence', 'N/A')
        source = metadata.get('source', 'unknown')

        print(f"   Confidence: {confidence} | Source: {source}")

        content = memory.content.replace('\n', ' ')
        if len(content) > 200:
            content = content[:200] + "..."
        print(f"   Content: {content}")

        entities = metadata.get('entities', [])
        if entities:
            print(f"   Entities: {', '.join(entities[:5])}")

        print()

    # Show stats
    stats = store.get_stats()
    print(f"Store stats: {stats['total_memories']} total memories")

    return 0


def cmd_reflect(args):
    """REFLECT command - run belief consolidation"""
    from operations.reflect import ReflectEngine

    async def run():
        engine = ReflectEngine()
        result = await engine.reflect(
            network=args.network,
            dry_run=not args.full
        )

        print(engine.format_report())

        print(f"\nSummary:")
        print(f"  Memories analyzed: {result['memories_analyzed']}")
        print(f"  Contradictions: {result['contradictions_found']}")
        print(f"  Patterns: {result['patterns_found']}")
        print(f"  New insights: {result['new_insights']}")
        print(f"  Mode: {'DRY-RUN' if result['dry_run'] else 'APPLIED'}")

    asyncio.run(run())
    return 0


def cmd_stats(args):
    """STATS command - show memory statistics"""
    store = VectorStore()
    stats = store.get_stats()

    print("\n" + "="*70)
    print("MEMORY STATISTICS")
    print("="*70)

    print(f"\nTotal Memories: {stats['total_memories']}")

    print("\nBy Network:")
    for network, count in sorted(stats['networks'].items()):
        bar = "█" * (count * 2)
        print(f"  {network:15} {count:4} {bar}")

    print(f"\nStorage: {stats['storage_dir']}")

    # Memory file size
    mem_file = Path(stats['storage_dir']) / "memories.json"
    if mem_file.exists():
        size_kb = mem_file.stat().st_size / 1024
        print(f"File Size: {size_kb:.1f} KB")

    print("\n" + "="*70)
    return 0


def cmd_export(args):
    """EXPORT command - export memories to JSON"""
    store = VectorStore()

    output_file = Path(args.output)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Export all memories
    memories = [m.to_dict() for m in store.memories.values()]

    with open(output_file, 'w') as f:
        json.dump(memories, f, indent=2)

    print(f"Exported {len(memories)} memories to {output_file}")
    return 0


def cmd_import(args):
    """IMPORT command - import memories from JSON"""
    store = VectorStore()

    input_file = Path(args.input)
    if not input_file.exists():
        print(f"Error: File not found: {input_file}")
        return 1

    with open(input_file) as f:
        memories = json.load(f)

    imported = 0
    for mem_data in memories:
        try:
            store.add_memory(
                content=mem_data['content'],
                network=mem_data['network'],
                metadata=mem_data.get('metadata', {})
            )
            imported += 1
        except Exception as e:
            print(f"  Error importing memory: {e}")

    print(f"Imported {imported} memories from {input_file}")
    return 0


def cmd_add(args):
    """ADD command - quickly add a memory"""
    store = VectorStore()

    memory_id = store.add_memory(
        content=args.content,
        network=args.network,
        metadata={"confidence": args.confidence, "source": "cli_add"}
    )

    print(f"Added memory: {memory_id}")
    return 0


def cmd_dashboard(args):
    """DASHBOARD command - visual memory overview"""
    store = VectorStore()
    stats = store.get_stats()

    # Try to use rich for better formatting
    try:
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        from rich.columns import Columns
        from rich import box

        console = Console()

        # Header
        console.print(Panel.fit(
            f"[bold blue]Hindsight Memory Dashboard[/bold blue]\n"
            f"[dim]{stats['storage_dir']}[/dim]",
            title="bb5 memory",
            border_style="blue"
        ))

        # Stats grid
        console.print(f"\n[bold]Total Memories:[/bold] {stats['total_memories']}")
        console.print(f"[bold]Embedding Cache:[/bold] {stats.get('embedding_cache_size', 0)} entries\n")

        # Network distribution table
        table = Table(title="Memory Distribution by Network", box=box.ROUNDED)
        table.add_column("Network", style="cyan", no_wrap=True)
        table.add_column("Count", justify="right", style="magenta")
        table.add_column("Bar", style="green")

        max_count = max(stats['networks'].values()) if stats['networks'] else 1
        for network, count in sorted(stats['networks'].items()):
            bar_width = int((count / max_count) * 30)
            bar = "█" * bar_width
            table.add_row(network.upper(), str(count), bar)

        console.print(table)

        # Timeline
        if stats.get('timeline'):
            console.print("\n[bold]Memory Timeline:[/bold]")
            timeline_table = Table(box=box.SIMPLE)
            timeline_table.add_column("Date", style="cyan")
            timeline_table.add_column("Memories Added", style="magenta")

            for date, count in sorted(stats['timeline'].items())[-7:]:  # Last 7 days
                timeline_table.add_row(date, str(count))
            console.print(timeline_table)

        # Recent memories
        if stats.get('recent_memories'):
            console.print("\n[bold]Recent Memories:[/bold]")
            for mem in stats['recent_memories'][:5]:
                console.print(f"  [{mem['network'][:3].upper()}] {mem['content'][:70]}...")

        console.print()

    except ImportError:
        # Fallback to plain text
        print("\n" + "="*70)
        print("HINDSIGHT MEMORY DASHBOARD")
        print("="*70)

        print(f"\nTotal Memories: {stats['total_memories']}")
        print(f"Embedding Cache: {stats.get('embedding_cache_size', 0)} entries")

        print("\nBy Network:")
        max_count = max(stats['networks'].values()) if stats['networks'] else 1
        for network, count in sorted(stats['networks'].items()):
            bar_width = int((count / max_count) * 30)
            bar = "█" * bar_width
            print(f"  {network:15} {count:4} {bar}")

        if stats.get('timeline'):
            print("\nTimeline (last 7 days):")
            for date, count in sorted(stats['timeline'].items())[-7:]:
                print(f"  {date}: {count} memories")

        if stats.get('recent_memories'):
            print("\nRecent Memories:")
            for mem in stats['recent_memories'][:5]:
                print(f"  [{mem['network'][:3].upper()}] {mem['content'][:60]}...")

        print("\n" + "="*70)

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="bb5 memory CLI - Hindsight memory operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  bb5-memory retain tasks/active/TASK-001/task.md
  bb5-memory recall "vector database" --top-k 5
  bb5-memory reflect --full
  bb5-memory stats
  bb5-memory add "New insight" --network observation --confidence 0.9
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # RETAIN command
    retain_parser = subparsers.add_parser('retain', help='Extract memories from files')
    retain_parser.add_argument('source', help='File or directory to process')
    retain_parser.add_argument('--dry-run', action='store_true', help='Don\'t store, just preview')
    retain_parser.add_argument('--output', default='./retain_output', help='Output for dry-run')
    retain_parser.set_defaults(func=cmd_retain)

    # RECALL command
    recall_parser = subparsers.add_parser('recall', help='Search memories')
    recall_parser.add_argument('query', help='Search query')
    recall_parser.add_argument('--top-k', type=int, default=5, help='Number of results')
    recall_parser.add_argument('--network', choices=['world', 'experience', 'opinion', 'observation'],
                              help='Filter by network')
    recall_parser.set_defaults(func=cmd_recall)

    # REFLECT command
    reflect_parser = subparsers.add_parser('reflect', help='Run belief consolidation')
    reflect_parser.add_argument('--network', choices=['world', 'experience', 'opinion', 'observation'],
                               help='Reflect on specific network')
    reflect_parser.add_argument('--full', action='store_true', help='Apply changes (not dry-run)')
    reflect_parser.set_defaults(func=cmd_reflect)

    # STATS command
    stats_parser = subparsers.add_parser('stats', help='Show memory statistics')
    stats_parser.set_defaults(func=cmd_stats)

    # EXPORT command
    export_parser = subparsers.add_parser('export', help='Export memories to JSON')
    export_parser.add_argument('--output', default='./memories_export.json', help='Output file')
    export_parser.set_defaults(func=cmd_export)

    # IMPORT command
    import_parser = subparsers.add_parser('import', help='Import memories from JSON')
    import_parser.add_argument('input', help='Input JSON file')
    import_parser.set_defaults(func=cmd_import)

    # ADD command
    add_parser = subparsers.add_parser('add', help='Quickly add a memory')
    add_parser.add_argument('content', help='Memory content')
    add_parser.add_argument('--network', default='observation',
                           choices=['world', 'experience', 'opinion', 'observation'],
                           help='Memory network')
    add_parser.add_argument('--confidence', type=float, default=0.8, help='Confidence score')
    add_parser.set_defaults(func=cmd_add)

    # DASHBOARD command
    dashboard_parser = subparsers.add_parser('dashboard', help='Visual memory overview')
    dashboard_parser.set_defaults(func=cmd_dashboard)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
