"""
Validation Module
=================

Validates assumptions through research and evidence gathering.

Uses multiple research strategies:
1. Internal semantic search (codebase, documentation)
2. External web search (when available)
3. First-principles reasoning
4. Git history analysis (what has been tried before)
"""

import asyncio
from typing import List, Optional, Dict, Any
from pathlib import Path
import re
from datetime import datetime

# Handle both relative and absolute imports
try:
    from .models import Assumption, AssumptionValidation, Evidence, Validity
except ImportError:
    from models import Assumption, AssumptionValidation, Evidence, Validity


class ValidationModule:
    """
    Validates assumptions through research.

    Research sources:
    - Internal: Codebase, documentation, git history
    - External: Web search, documentation sites
    - Reasoning: First-principles analysis
    """

    def __init__(
        self,
        project_root: Optional[Path] = None,
        enable_web_search: bool = False,
        enable_semantic_search: bool = True
    ):
        """
        Initialize validation module.

        Args:
            project_root: Root directory for internal research
            enable_web_search: Whether to use external web search
            enable_semantic_search: Whether to use semantic search
        """
        if project_root is None:
            project_root = Path.cwd()
        self.project_root = Path(project_root)

        self.enable_web_search = enable_web_search
        self.enable_semantic_search = enable_semantic_search

        # Lazy load research engines
        self._semantic_search = None
        self._git_analyzer = None

    async def validate(self, assumption: Assumption) -> AssumptionValidation:
        """
        Validate an assumption through research.

        Args:
            assumption: The assumption to validate

        Returns:
            Validation with evidence and confidence
        """
        supporting_evidence = []
        contradicting_evidence = []

        # Strategy 1: Internal semantic search
        if self.enable_semantic_search:
            internal_results = await self._search_internal(assumption.statement)
            for result in internal_results:
                evidence = Evidence(
                    text=result.get("content", ""),
                    source=result.get("file_path", "internal"),
                    url=result.get("url"),
                    supports=result.get("supports", True),
                    confidence=result.get("confidence", 0.7)
                )

                if evidence.supports:
                    supporting_evidence.append(evidence)
                else:
                    contradicting_evidence.append(evidence)

        # Strategy 2: Git history analysis
        git_results = await self._analyze_git_history(assumption.statement)
        for result in git_results:
            evidence = Evidence(
                text=result.get("message", ""),
                source="git_history",
                url=result.get("url"),
                supports=result.get("supports", True),
                confidence=result.get("confidence", 0.6)
            )

            if evidence.supports:
                supporting_evidence.append(evidence)
            else:
                contradicting_evidence.append(evidence)

        # Strategy 3: Web search (if enabled)
        if self.enable_web_search:
            web_results = await self._search_web(assumption.statement)
            for result in web_results:
                evidence = Evidence(
                    text=result.get("snippet", ""),
                    source=result.get("source", "web"),
                    url=result.get("url"),
                    supports=result.get("supports", True),
                    confidence=result.get("confidence", 0.5)
                )

                if evidence.supports:
                    supporting_evidence.append(evidence)
                else:
                    contradicting_evidence.append(evidence)

        # Determine validity
        validity, confidence, reasoning = self._assess_validity(
            assumption,
            supporting_evidence,
            contradicting_evidence
        )

        return AssumptionValidation(
            assumption=assumption,
            validity=validity,
            supporting_evidence=supporting_evidence,
            contradicting_evidence=contradicting_evidence,
            confidence=confidence,
            reasoning=reasoning
        )

    async def validate_batch(
        self,
        assumptions: List[Assumption],
        parallel: bool = True
    ) -> List[AssumptionValidation]:
        """
        Validate multiple assumptions (optionally in parallel).

        Args:
            assumptions: List of assumptions to validate
            parallel: Whether to validate in parallel

        Returns:
            List of validations
        """
        if parallel:
            tasks = [self.validate(assumption) for assumption in assumptions]
            return await asyncio.gather(*tasks)
        else:
            validations = []
            for assumption in assumptions:
                validation = await self.validate(assumption)
                validations.append(validation)
            return validations

    async def _search_internal(self, query: str) -> List[Dict[str, Any]]:
        """
        Search internal codebase and documentation.

        Args:
            query: Search query

        Returns:
            List of search results
        """
        results = []

        try:
            # Try to use semantic search engine
            if self._semantic_search is None:
                # Try to import semantic search
                try:
                    from ...skills_cap.research.semantic_search import SemanticSearchEngine

                    vector_db_path = self.project_root / "2-engine" / "03-knowledge" / "memory" / "extended" / "chroma-db"

                    if vector_db_path.exists():
                        self._semantic_search = SemanticSearchEngine(
                            vector_db_path=str(vector_db_path)
                        )
                except ImportError:
                    self._semantic_search = False

            # Use semantic search if available
            if self._semantic_search and hasattr(self._semantic_search, 'search'):
                search_results = self._semantic_search.search(query, n_results=5)

                for result in search_results:
                    # Determine if this supports or contradicts based on content
                    content = result.get("content", "").lower()
                    supports = self._assess_support(query, content)

                    results.append({
                        "content": result.get("content", "")[:500],
                        "file_path": result.get("file_path", ""),
                        "supports": supports,
                        "confidence": result.get("similarity", 0.7)
                    })

        except Exception as e:
            # Fallback to simple text search
            pass

        return results

    async def _analyze_git_history(self, query: str) -> List[Dict[str, Any]]:
        """
        Analyze git history for relevant commits.

        Args:
            query: Search query

        Returns:
            List of relevant commits
        """
        results = []

        try:
            # Check if we're in a git repo
            import subprocess

            result = subprocess.run(
                ["git", "log", "--all", "--grep", query, "-n", "5", "--pretty=%H|%s|%cd"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")

                for line in lines:
                    if not line:
                        continue

                    parts = line.split("|")
                    if len(parts) >= 2:
                        commit_hash = parts[0]
                        message = parts[1]
                        date = parts[2] if len(parts) > 2 else ""

                        # Determine if this supports or contradicts
                        message_lower = message.lower()
                        supports = self._assess_support(query, message_lower)

                        results.append({
                            "message": message,
                            "commit": commit_hash,
                            "date": date,
                            "supports": supports,
                            "confidence": 0.6,
                            "url": f"commit://{commit_hash}"
                        })

        except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
            pass

        return results

    async def _search_web(self, query: str) -> List[Dict[str, Any]]:
        """
        Search web for external evidence (placeholder).

        In production, this would use a web search API.

        Args:
            query: Search query

        Returns:
            List of search results
        """
        # Placeholder for web search integration
        # In production, integrate with:
        # - DuckDuckGo API
        # - Google Custom Search
        # - ArXiv API for academic papers
        # - GitHub API for code search

        return []

    def _assess_support(self, query: str, content: str) -> bool:
        """
        Assess whether content supports or contradicts the query.

        This is a simple heuristic-based implementation.
        In production, this would use more sophisticated NLP.

        Args:
            query: The original query/assumption
            content: The content to assess

        Returns:
            True if content supports, False if contradicts
        """
        query_lower = query.lower()

        # Contradiction indicators
        contradiction_patterns = [
            r"not\s+" + re.escape(query_lower),
            r"never\s+" + re.escape(query_lower),
            r"impossible",
            r"failed",
            r"error",
            r"bug",
            r"issue",
            r"problem",
            r"doesn't work",
            r"doesn't",
            r"won't"
        ]

        for pattern in contradiction_patterns:
            if re.search(pattern, content):
                return False

        # Support indicators
        support_patterns = [
            r"works",
            r"success",
            r"effective",
            r"proven",
            r"tested",
            r"verified",
            r"validated"
        ]

        for pattern in support_patterns:
            if re.search(pattern, content):
                return True

        # Default: assume support if query terms appear
        return bool(re.search(re.escape(query_lower[:20]), content))

    def _assess_validity(
        self,
        assumption: Assumption,
        supporting: List[Evidence],
        contradicting: List[Evidence]
    ) -> tuple[Validity, float, str]:
        """
        Assess overall validity based on evidence.

        Args:
            assumption: The assumption being validated
            supporting: Supporting evidence
            contradicting: Contradicting evidence

        Returns:
            Tuple of (validity, confidence, reasoning)
        """
        # Calculate evidence weights
        support_weight = sum(e.confidence for e in supporting)
        contradiction_weight = sum(e.confidence for e in contradicting)

        total_evidence = len(supporting) + len(contradicting)

        # No evidence found
        if total_evidence == 0:
            return (
                Validity.UNCERTAIN,
                0.3,
                f"No evidence found to validate or contradict '{assumption.statement}'"
            )

        # Strong supporting evidence
        if support_weight > contradiction_weight * 1.5:
            confidence = min(0.95, 0.5 + (support_weight / (support_weight + contradiction_weight)) * 0.4)
            return (
                Validity.VALID,
                confidence,
                f"Supported by {len(supporting)} evidence sources, {len(contradicting)} contradictions"
            )

        # Strong contradicting evidence
        if contradiction_weight > support_weight * 1.5:
            confidence = min(0.95, 0.5 + (contradiction_weight / (support_weight + contradiction_weight)) * 0.4)
            return (
                Validity.INVALID,
                confidence,
                f"Contradicted by {len(contradicting)} evidence sources, {len(supporting)} support"
            )

        # Mixed or weak evidence
        if support_weight > contradiction_weight:
            confidence = 0.5 + (support_weight / (support_weight + contradiction_weight)) * 0.2
        else:
            confidence = 0.5 + (contradiction_weight / (support_weight + contradiction_weight)) * 0.2

        return (
            Validity.UNCERTAIN,
            confidence,
            f"Mixed evidence: {len(supporting)} support, {len(contradicting)} contradict"
        )
