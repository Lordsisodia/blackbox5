"""
BLACKBOX5 Code Search Utility

Provides fast, comprehensive search across the entire codebase including:
- Source code files
- Documentation (Markdown, PDFs)
- Configuration files
- Archives and compressed files

Uses ripgrep-all (rga) for maximum file type support.
"""

import subprocess
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class SearchResult:
    """Represents a single search result."""
    path: str
    line_number: int
    content: str
    file_type: Optional[str] = None
    context_before: Optional[List[str]] = None
    context_after: Optional[List[str]] = None


@dataclass
class SearchResults:
    """Container for search results with metadata."""
    query: str
    total_matches: int
    results: List[SearchResult]
    search_time_ms: float
    files_searched: int


class CodeSearch:
    """
    Fast code search using ripgrep-all.

    Supports searching across:
    - 150+ file types including code, docs, PDFs, archives
    - Binary files with extracted text
    - Compressed files
    """

    def __init__(self, root_path: Optional[Path] = None):
        """
        Initialize the search engine.

        Args:
            root_path: Root directory to search in. Defaults to BLACKBOX5 root.
        """
        if root_path is None:
            # Default to BLACKBOX5 root (2-engine/01-core/utilities -> 2-engine -> blackbox5 root)
            root_path = Path(__file__).parent.parent.parent.parent

        self.root_path = Path(root_path).resolve()

    def search(
        self,
        query: str,
        *,
        file_pattern: Optional[str] = None,
        file_type: Optional[str] = None,
        case_sensitive: bool = False,
        context_lines: int = 2,
        max_results: int = 100,
        exclude_dirs: Optional[List[str]] = None
    ) -> SearchResults:
        """
        Search for a query across the codebase.

        Args:
            query: The search string or regex pattern
            file_pattern: Filter to files matching this glob pattern (e.g., "*.py")
            file_type: Filter by file type (e.g., "py", "md", "json")
            case_sensitive: Whether to match case (default: False)
            context_lines: Number of context lines before/after match
            max_results: Maximum number of results to return
            exclude_dirs: Directories to exclude (default: [.git, node_modules, __pycache__])

        Returns:
            SearchResults object with matches and metadata
        """
        import time

        start_time = time.time()

        # Default exclusions
        if exclude_dirs is None:
            exclude_dirs = ['.git', 'node_modules', '__pycache__', '.venv', 'venv',
                          'target', 'build', 'dist', '.next', 'out']

        # Build rga command
        cmd = [
            'rga',
            '--json',
            '--line-number',
            '--no-heading',
            f'-C{context_lines}',
        ]

        if not case_sensitive:
            cmd.append('--ignore-case')

        # Add exclusions
        for exclude in exclude_dirs:
            cmd.extend(['--glob', f'!{exclude}'])

        # Add file type filter if specified
        if file_type:
            cmd.extend(['-t', file_type])

        # Add file pattern filter if specified
        if file_pattern:
            cmd.extend(['--glob', file_pattern])

        # Add max results
        cmd.extend(['--max-count', str(max_results)])

        # Add query and path
        cmd.extend([query, str(self.root_path)])

        try:
            # Run search
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            search_time = (time.time() - start_time) * 1000  # Convert to ms

            # Parse results
            results = []
            files_searched = 0

            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue

                try:
                    data = json.loads(line)

                    if data.get('type') == 'begin':
                        files_searched += 1
                    elif data.get('type') == 'match':
                        # Extract match data
                        lines = data['data']['lines']
                        submatches = data['data']['submatches']

                        if submatches:
                            match_text = submatches[0]['match']['text']
                            results.append(SearchResult(
                                path=data['data']['path']['text'],
                                line_number=data['data']['line_number'],
                                content=lines['text'].strip(),
                                file_type=Path(data['data']['path']['text']).suffix.lstrip('.'),
                            ))

                except (json.JSONDecodeError, KeyError):
                    continue

            return SearchResults(
                query=query,
                total_matches=len(results),
                results=results,
                search_time_ms=search_time,
                files_searched=files_searched
            )

        except subprocess.TimeoutExpired:
            return SearchResults(
                query=query,
                total_matches=0,
                results=[],
                search_time_ms=30000,
                files_searched=0
            )
        except FileNotFoundError:
            raise RuntimeError(
                "ripgrep-all (rga) is not installed. "
                "Install it with: brew install ripgrep-all"
            )

    def search_files(self, pattern: str) -> List[str]:
        """
        Find files matching a pattern (filename search).

        Args:
            pattern: Glob pattern for filenames (e.g., "*.py" or "*agent*.yaml")

        Returns:
            List of matching file paths
        """
        try:
            result = subprocess.run(
                ['rga', '--files', '--glob', pattern, str(self.root_path)],
                capture_output=True,
                text=True,
                timeout=30
            )

            return [
                line.strip()
                for line in result.stdout.split('\n')
                if line.strip()
            ]

        except FileNotFoundError:
            raise RuntimeError(
                "ripgrep-all (rga) is not installed. "
                "Install it with: brew install ripgrep-all"
            )

    def find_references(self, symbol: str, file_type: Optional[str] = None) -> List[SearchResult]:
        """
        Find references to a symbol/identifier in the codebase.

        Args:
            symbol: The symbol name to search for
            file_type: Optional file type filter (e.g., "py", "ts")

        Returns:
            List of SearchResults with symbol references
        """
        # Search for word boundaries to match whole symbols
        pattern = f'\\b{symbol}\\b'

        results = self.search(
            pattern,
            file_type=file_type,
            context_lines=1,
            max_results=200
        )

        return results.results

    def find_definitions(self, symbol: str, file_type: Optional[str] = None) -> List[SearchResult]:
        """
        Find definitions of a symbol (functions, classes, variables).

        This is a heuristic search - for precise results, use the tree-sitter MCP.

        Args:
            symbol: The symbol name to find definitions for
            file_type: Optional file type filter

        Returns:
            List of potential definitions
        """
        # Common definition patterns
        patterns = [
            f'def {symbol}\\(',          # Python functions
            f'class {symbol}',            # Python classes
            f'{symbol}\\s*=',             # Variable assignments
            f'function {symbol}\\(',      # JavaScript/TypeScript
            f'const {symbol}\\s*=',       # JavaScript/TypeScript const
            f'let {symbol}\\s*=',         # JavaScript/TypeScript let
            f'interface {symbol}',        # TypeScript interfaces
            f'type {symbol}\\s*=',        # TypeScript types
        ]

        all_results = []

        for pattern in patterns:
            try:
                results = self.search(
                    pattern,
                    file_type=file_type,
                    context_lines=2,
                    max_results=50
                )
                all_results.extend(results.results)
            except Exception:
                continue

        return all_results

    def get_file_stats(self) -> Dict[str, int]:
        """
        Get statistics about files in the codebase.

        Returns:
            Dictionary with file counts by extension
        """
        try:
            result = subprocess.run(
                ['rga', '--files', str(self.root_path)],
                capture_output=True,
                text=True,
                timeout=60
            )

            extensions = {}

            for line in result.stdout.split('\n'):
                if not line:
                    continue

                ext = Path(line).suffix or '(no extension)'
                extensions[ext] = extensions.get(ext, 0) + 1

            return dict(sorted(extensions.items(), key=lambda x: x[1], reverse=True))

        except FileNotFoundError:
            raise RuntimeError(
                "ripgrep-all (rga) is not installed. "
                "Install it with: brew install ripgrep-all"
            )


# Singleton instance for easy access
_search_instance: Optional[CodeSearch] = None


def get_search() -> CodeSearch:
    """Get the singleton CodeSearch instance."""
    global _search_instance
    if _search_instance is None:
        _search_instance = CodeSearch()
    return _search_instance


# Convenience functions for common operations

def quick_search(query: str, **kwargs) -> SearchResults:
    """
    Quick search with default settings.

    Example:
        results = quick_search("AgentLoader")
        for r in results.results:
            print(f"{r.path}:{r.line_number} - {r.content}")
    """
    return get_search().search(query, **kwargs)


def find_files(pattern: str) -> List[str]:
    """Find files by glob pattern."""
    return get_search().search_files(pattern)


def find_symbol(symbol: str, **kwargs) -> List[SearchResult]:
    """Find all references to a symbol."""
    return get_search().find_references(symbol, **kwargs)


if __name__ == "__main__":
    # Demo usage
    import sys

    if len(sys.argv) < 2:
        print("Usage: python code_search.py <query>")
        print("\nExamples:")
        print("  python code_search.py AgentLoader")
        print("  python code_search.py 'def.*execute' --type py")
        sys.exit(1)

    query = sys.argv[1]
    results = quick_search(query)

    print(f"\nFound {results.total_matches} matches in {results.search_time_ms:.2f}ms\n")

    for result in results.results[:20]:
        rel_path = Path(result.path).relative_to(get_search().root_path)
        print(f"  {rel_path}:{result.line_number}")
        if result.content:
            print(f"    {result.content[:100]}")
        print()
