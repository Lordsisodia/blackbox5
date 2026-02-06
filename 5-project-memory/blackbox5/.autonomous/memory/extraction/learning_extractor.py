#!/usr/bin/env python3
"""
Learning Extractor - Extract and Index Learnings from Task Runs

This module extracts structured learnings from run directories (THOUGHTS.md,
DECISIONS.md, RESULTS.md) and populates learning-index.yaml.

Usage:
    # Extract from single run
    python learning_extractor.py --run-dir /path/to/run-0001

    # Backfill all runs
    python learning_extractor.py --backfill --runs-dir /path/to/runs

    # Rebuild entire index
    python learning_extractor.py --rebuild-index --runs-dir /path/to/runs

    # Health check
    python learning_extractor.py --health-check
"""

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Dict, Any, Set
from collections import defaultdict

import yaml


@dataclass
class Learning:
    """Represents a single learning extracted from a task run."""
    learning_id: str
    task_id: str
    task_title: str
    timestamp: str
    source_file: str
    learning_type: str  # pattern, decision, challenge, optimization, bugfix, insight
    title: str
    description: str
    severity: Optional[str] = None  # critical, high, medium, low
    effectiveness: float = 0.0
    frequency: str = "one-time"  # recurring, occasional, one-time
    category: str = "technical"  # technical, process, architectural, operational
    tags: List[str] = field(default_factory=list)
    related_tasks: List[str] = field(default_factory=list)
    pattern: Optional[str] = None
    action_item: Optional[str] = None
    content_hash: str = ""  # For deduplication

    def __post_init__(self):
        if not self.content_hash:
            # Generate hash from title + description for deduplication
            content = f"{self.title}:{self.description}"
            self.content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]


@dataclass
class Pattern:
    """Represents a recurring pattern identified across tasks."""
    pattern_id: str
    pattern_type: str  # keyword, context, error_type, decision
    description: str
    frequency: int
    related_tasks: List[str]
    confidence: float
    keywords: List[str]
    applicability: str = "specific"  # broad, specific, niche


class LearningExtractor:
    """
    Extracts learnings from task run directories and manages the learning index.
    """

    VALID_LEARNING_TYPES = {"pattern", "decision", "challenge", "optimization", "bugfix", "insight"}
    VALID_CATEGORIES = {"technical", "process", "architectural", "operational"}
    VALID_SEVERITIES = {"critical", "high", "medium", "low"}
    VALID_FREQUENCIES = {"recurring", "occasional", "one-time"}

    def __init__(self, index_path: Optional[Path] = None):
        """
        Initialize the learning extractor.

        Args:
            index_path: Path to learning-index.yaml (default: standard location)
        """
        if index_path is None:
            self.index_path = Path("/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/memory/insights/learning-index.yaml")
        else:
            self.index_path = Path(index_path)

        self.learnings: List[Learning] = []
        self.patterns: List[Pattern] = []
        self.existing_hashes: Set[str] = set()
        self._load_index()

    def _load_index(self):
        """Load existing learning index if it exists."""
        if self.index_path.exists():
            try:
                with open(self.index_path, 'r') as f:
                    data = yaml.safe_load(f) or {}

                # Load existing learnings
                for learning_data in data.get('learnings', []):
                    learning = Learning(**learning_data)
                    self.learnings.append(learning)
                    self.existing_hashes.add(learning.content_hash)

                # Load existing patterns
                for pattern_data in data.get('patterns', []):
                    pattern = Pattern(**pattern_data)
                    self.patterns.append(pattern)

                print(f"Loaded {len(self.learnings)} existing learnings from index")
            except Exception as e:
                print(f"Warning: Could not load existing index: {e}")
                self.learnings = []
                self.patterns = []

    def _save_index(self):
        """Save learnings to the index file."""
        # Calculate statistics
        stats = self._calculate_statistics()

        # Build index data
        index_data = {
            'metadata': {
                'version': '1.0.0',
                'created': '2026-02-01T14:42:30Z',
                'last_updated': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                'total_learnings': len(self.learnings),
                'last_task_id': self.learnings[-1].task_id if self.learnings else 'UNKNOWN',
            },
            'learnings': [asdict(l) for l in self.learnings],
            'patterns': [asdict(p) for p in self.patterns],
            'statistics': stats,
            'maintenance': {
                'last_rebuild': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                'last_cleanup': None,
                'last_effectiveness_update': None,
                'total_rebuilds': 1,
            },
            'notes': """Learning Index Auto-Generated

This index is automatically populated by the learning_extractor.py library
after each task completion. Manual edits should maintain the YAML structure.

Index structure:
- learnings: Array of learning objects extracted from tasks
- patterns: Array of recurring patterns identified across tasks
- statistics: Aggregated statistics for quick querying
- maintenance: Index maintenance tracking

Usage:
- Query with knowledge_retriever.py: python3 -m knowledge_retriever search "import error"
- Find patterns with pattern_matcher.py: python3 -m pattern_matcher patterns
- Apply learnings with learning_applier.py: python3 -m learning_applier inject --task-id TASK-XXX --title "My Task"

Maintenance:
- Rebuild: python3 -m learning_extractor rebuild-index
- Cleanup: python3 -m learning_extractor cleanup-index
- Update effectiveness: python3 -m learning_applier update-effectiveness
"""
        }

        # Ensure directory exists
        self.index_path.parent.mkdir(parents=True, exist_ok=True)

        # Write with custom YAML formatting
        with open(self.index_path, 'w') as f:
            f.write("# Learning Index - RALF Knowledge Base & Learning Engine\n")
            f.write("# Central index of all learnings extracted from task runs\n")
            f.write("# Format: YAML for easy parsing and human readability\n")
            f.write("#\n")
            f.write("# This file is auto-populated by the learning_extractor.py library\n")
            f.write("# Manual edits should follow the same structure\n")
            f.write("\n")
            yaml.dump(index_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

        print(f"Saved {len(self.learnings)} learnings to {self.index_path}")

    def _calculate_statistics(self) -> Dict[str, Any]:
        """Calculate statistics for the index."""
        by_type = defaultdict(int)
        by_category = defaultdict(int)
        by_severity = defaultdict(int)
        by_frequency = defaultdict(int)
        effectiveness_scores = []

        for learning in self.learnings:
            by_type[learning.learning_type] += 1
            by_category[learning.category] += 1
            if learning.severity:
                by_severity[learning.severity] += 1
            by_frequency[learning.frequency] += 1
            if learning.effectiveness > 0:
                effectiveness_scores.append(learning.effectiveness)

        return {
            'by_type': dict(by_type),
            'by_category': dict(by_category),
            'by_severity': dict(by_severity),
            'by_frequency': dict(by_frequency),
            'effectiveness': {
                'average': sum(effectiveness_scores) / len(effectiveness_scores) if effectiveness_scores else None,
                'min': min(effectiveness_scores) if effectiveness_scores else None,
                'max': max(effectiveness_scores) if effectiveness_scores else None,
                'total_tracked': len(effectiveness_scores),
            },
            'frequency': {
                'recurring': by_frequency.get('recurring', 0),
                'occasional': by_frequency.get('occasional', 0),
                'one_time': by_frequency.get('one-time', 0),
            }
        }

    def extract_from_run(self, run_dir: Path) -> List[Learning]:
        """
        Extract learnings from a single run directory.

        Args:
            run_dir: Path to run directory (e.g., run-0001)

        Returns:
            List of extracted learnings
        """
        run_dir = Path(run_dir)
        if not run_dir.exists():
            print(f"Error: Run directory not found: {run_dir}")
            return []

        print(f"Extracting from {run_dir.name}...")

        learnings = []

        # Extract from THOUGHTS.md
        thoughts_file = run_dir / "THOUGHTS.md"
        if thoughts_file.exists():
            thoughts_learnings = self._extract_from_thoughts(thoughts_file)
            learnings.extend(thoughts_learnings)
            print(f"  THOUGHTS.md: {len(thoughts_learnings)} learnings")

        # Extract from DECISIONS.md
        decisions_file = run_dir / "DECISIONS.md"
        if decisions_file.exists():
            decisions_learnings = self._extract_from_decisions(decisions_file)
            learnings.extend(decisions_learnings)
            print(f"  DECISIONS.md: {len(decisions_learnings)} learnings")

        # Extract from RESULTS.md
        results_file = run_dir / "RESULTS.md"
        if results_file.exists():
            results_learnings = self._extract_from_results(results_file)
            learnings.extend(results_learnings)
            print(f"  RESULTS.md: {len(results_learnings)} learnings")

        # Deduplicate against existing learnings
        new_learnings = []
        for learning in learnings:
            if learning.content_hash not in self.existing_hashes:
                new_learnings.append(learning)
                self.existing_hashes.add(learning.content_hash)

        print(f"  Total new learnings: {len(new_learnings)} (filtered {len(learnings) - len(new_learnings)} duplicates)")
        return new_learnings

    def _extract_from_thoughts(self, filepath: Path) -> List[Learning]:
        """Extract learnings from THOUGHTS.md file."""
        content = filepath.read_text()
        learnings = []

        # Extract task info from header
        task_id = self._extract_task_id(content)
        task_title = self._extract_task_title(content)

        # Pattern 1: Extract "Challenges & Resolution" section
        challenges = self._extract_section(content, "Challenges & Resolution", "##")
        if challenges:
            for challenge_text in self._split_entries(challenges):
                learning = self._parse_challenge(challenge_text, task_id, task_title, filepath.name)
                if learning:
                    learnings.append(learning)

        # Pattern 2: Extract "Key Decisions" section
        key_decisions = self._extract_section(content, "Key Decisions", "##")
        if key_decisions:
            for decision_text in self._split_entries(key_decisions):
                learning = self._parse_decision(decision_text, task_id, task_title, filepath.name)
                if learning:
                    learnings.append(learning)

        # Pattern 3: Extract "Insights" or "Key Insights"
        insights = self._extract_section(content, "Insights", "##") or self._extract_section(content, "Key Insights", "##")
        if insights:
            for insight_text in self._split_entries(insights):
                learning = self._parse_insight(insight_text, task_id, task_title, filepath.name)
                if learning:
                    learnings.append(learning)

        # Pattern 4: Extract "What Worked Well" / "What Didn't Work"
        worked_well = self._extract_section(content, "What Worked Well", "##")
        if worked_well:
            for item in self._split_entries(worked_well):
                learning = self._parse_pattern(item, task_id, task_title, filepath.name, "positive")
                if learning:
                    learnings.append(learning)

        didnt_work = self._extract_section(content, "What Didn't Work", "##")
        if didnt_work:
            for item in self._split_entries(didnt_work):
                learning = self._parse_pattern(item, task_id, task_title, filepath.name, "negative")
                if learning:
                    learnings.append(learning)

        # Pattern 5: Look for explicit "Learning:" or "Lesson:" markers
        for match in re.finditer(r'(?:Learning|Lesson|Insight)[\s:]*(.+?)(?=\n\n|\n##|$)', content, re.IGNORECASE | re.DOTALL):
            text = match.group(1).strip()
            if len(text) > 20:  # Filter out very short matches
                learning = self._parse_generic_learning(text, task_id, task_title, filepath.name)
                if learning:
                    learnings.append(learning)

        return learnings

    def _extract_from_decisions(self, filepath: Path) -> List[Learning]:
        """Extract learnings from DECISIONS.md file."""
        content = filepath.read_text()
        learnings = []

        # Extract task info
        task_id = self._extract_task_id(content)
        task_title = self._extract_task_title(content)

        # Pattern: Extract decision blocks (## Decision X: or ## Decision Title)
        decision_pattern = r'##\s*(?:Decision\s*\d*[:\-]?\s*)?(.+?)\n\n\*\*Context:\*\*(.+?)\n\n\*\*Selected:\*\*(.+?)\n\n\*\*Rationale:\*\*(.+?)(?=\n\n---|\n\n##|$)'

        for match in re.finditer(decision_pattern, content, re.DOTALL):
            title = match.group(1).strip()
            context = match.group(2).strip()
            selected = match.group(3).strip()
            rationale = match.group(4).strip()

            learning = Learning(
                learning_id=f"{task_id}-DECISION-{len(learnings)+1}",
                task_id=task_id,
                task_title=task_title,
                timestamp=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                source_file=filepath.name,
                learning_type="decision",
                title=title[:100],
                description=f"Context: {context[:200]}...\n\nSelected: {selected[:200]}...\n\nRationale: {rationale[:300]}...",
                category="architectural" if "architecture" in title.lower() or "design" in title.lower() else "technical",
                tags=self._extract_tags(title + " " + context),
            )
            learnings.append(learning)

        # Alternative pattern: simpler decision format
        if not learnings:
            # Look for ## headers followed by decision-like content
            sections = re.findall(r'##\s+(.+?)\n\n(.+?)(?=\n\n##|\Z)', content, re.DOTALL)
            for title, body in sections:
                if any(keyword in body.lower() for keyword in ['selected', 'chose', 'decided', 'option']):
                    learning = Learning(
                        learning_id=f"{task_id}-DECISION-{len(learnings)+1}",
                        task_id=task_id,
                        task_title=task_title,
                        timestamp=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                        source_file=filepath.name,
                        learning_type="decision",
                        title=title[:100],
                        description=body[:500],
                        category="technical",
                        tags=self._extract_tags(title + " " + body),
                    )
                    learnings.append(learning)

        return learnings

    def _extract_from_results(self, filepath: Path) -> List[Learning]:
        """Extract learnings from RESULTS.md file."""
        content = filepath.read_text()
        learnings = []

        # Extract task info
        task_id = self._extract_task_id(content)
        task_title = self._extract_task_title(content)

        # Pattern 1: Look for validation/checklist items that failed then succeeded
        validation_section = self._extract_section(content, "Validation", "##")
        if validation_section:
            # Failed items that were fixed indicate learnings
            failed_items = re.findall(r'-\s*\[\s*\]\s*(.+?)(?=\n|$)', validation_section)
            for item in failed_items:
                learning = Learning(
                    learning_id=f"{task_id}-RESULT-{len(learnings)+1}",
                    task_id=task_id,
                    task_title=task_title,
                    timestamp=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                    source_file=filepath.name,
                    learning_type="challenge",
                    title=f"Unresolved: {item[:80]}",
                    description=f"Validation item not completed: {item}",
                    severity="medium",
                    category="technical",
                    tags=self._extract_tags(item),
                )
                learnings.append(learning)

        # Pattern 2: Extract "Files Modified" as technical learnings
        files_section = self._extract_section(content, "Files Modified", "##")
        if files_section and len(files_section) < 1000:  # Don't create huge entries
            learning = Learning(
                learning_id=f"{task_id}-RESULT-{len(learnings)+1}",
                task_id=task_id,
                task_title=task_title,
                timestamp=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                source_file=filepath.name,
                learning_type="insight",
                title=f"Files modified in {task_id}",
                description=f"Modified files:\n{files_section[:800]}",
                category="technical",
                tags=["files", "modifications"],
            )
            learnings.append(learning)

        return learnings

    def _extract_task_id(self, content: str) -> str:
        """Extract task ID from content."""
        # Try header pattern: # Title - TASK-XXX
        match = re.search(r'TASK-[^\s\n]+', content)
        if match:
            return match.group(0)

        # Try metadata pattern
        match = re.search(r'task_id:\s*"?([^"\n]+)"?', content)
        if match:
            return match.group(1).strip()

        return "UNKNOWN"

    def _extract_task_title(self, content: str) -> str:
        """Extract task title from content."""
        # Try header pattern
        match = re.search(r'#\s+(.+?)(?:\s+-\s+TASK-|$)', content)
        if match:
            return match.group(1).strip()

        # Try Task: pattern
        match = re.search(r'(?:Task|## Task)[:\s]+(.+?)(?=\n|$)', content, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        return "Unknown Task"

    def _extract_section(self, content: str, section_name: str, header_level: str = "##") -> Optional[str]:
        """Extract a section from markdown content."""
        pattern = rf'{header_level}\s+{re.escape(section_name)}\s*\n(.+?)(?=\n{header_level}\s+|\Z)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None

    def _split_entries(self, content: str) -> List[str]:
        """Split content into individual entries."""
        # Split by bullet points or numbered lists
        entries = re.split(r'\n\s*[-*\d]+[.\)]\s+', content)
        return [e.strip() for e in entries if len(e.strip()) > 10]

    def _parse_challenge(self, text: str, task_id: str, task_title: str, source_file: str) -> Optional[Learning]:
        """Parse a challenge entry into a learning."""
        # Look for "Challenge: ... Resolution: ..." pattern
        challenge_match = re.search(r'(?:Challenge|Problem)[:\s]*(.+?)(?:Resolution|Solution|Fix)[:\s]*(.+)', text, re.DOTALL | re.IGNORECASE)

        if challenge_match:
            challenge = challenge_match.group(1).strip()
            resolution = challenge_match.group(2).strip()
        else:
            # Just use the whole text as challenge
            challenge = text[:300]
            resolution = None

        title = challenge[:80] + "..." if len(challenge) > 80 else challenge

        return Learning(
            learning_id=f"{task_id}-CHALLENGE-{hash(challenge) % 10000}",
            task_id=task_id,
            task_title=task_title,
            timestamp=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            source_file=source_file,
            learning_type="challenge",
            title=title,
            description=f"Challenge: {challenge[:400]}\n\nResolution: {resolution[:400] if resolution else 'N/A'}",
            severity="medium",
            category="technical",
            tags=self._extract_tags(challenge),
        )

    def _parse_decision(self, text: str, task_id: str, task_title: str, source_file: str) -> Optional[Learning]:
        """Parse a decision entry into a learning."""
        title = text[:80] + "..." if len(text) > 80 else text

        return Learning(
            learning_id=f"{task_id}-DECISION-{hash(text) % 10000}",
            task_id=task_id,
            task_title=task_title,
            timestamp=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            source_file=source_file,
            learning_type="decision",
            title=title,
            description=text[:500],
            category="architectural" if any(kw in text.lower() for kw in ["architecture", "design", "pattern"]) else "technical",
            tags=self._extract_tags(text),
        )

    def _parse_insight(self, text: str, task_id: str, task_title: str, source_file: str) -> Optional[Learning]:
        """Parse an insight entry into a learning."""
        title = text[:80] + "..." if len(text) > 80 else text

        return Learning(
            learning_id=f"{task_id}-INSIGHT-{hash(text) % 10000}",
            task_id=task_id,
            task_title=task_title,
            timestamp=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            source_file=source_file,
            learning_type="insight",
            title=title,
            description=text[:500],
            category="technical",
            tags=self._extract_tags(text),
        )

    def _parse_pattern(self, text: str, task_id: str, task_title: str, source_file: str, sentiment: str) -> Optional[Learning]:
        """Parse a pattern (positive/negative) into a learning."""
        title = text[:80] + "..." if len(text) > 80 else text

        return Learning(
            learning_id=f"{task_id}-PATTERN-{hash(text) % 10000}",
            task_id=task_id,
            task_title=task_title,
            timestamp=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            source_file=source_file,
            learning_type="pattern",
            title=title,
            description=text[:500],
            category="process" if "process" in text.lower() else "technical",
            tags=self._extract_tags(text) + [sentiment],
        )

    def _parse_generic_learning(self, text: str, task_id: str, task_title: str, source_file: str) -> Optional[Learning]:
        """Parse a generic learning entry."""
        title = text[:80] + "..." if len(text) > 80 else text

        # Determine type based on content
        learning_type = "insight"
        if any(kw in text.lower() for kw in ["error", "bug", "fix", "issue"]):
            learning_type = "bugfix"
        elif any(kw in text.lower() for kw in ["optimize", "performance", "speed", "improve"]):
            learning_type = "optimization"
        elif any(kw in text.lower() for kw in ["pattern", "always", "never", "should"]):
            learning_type = "pattern"

        return Learning(
            learning_id=f"{task_id}-LEARNING-{hash(text) % 10000}",
            task_id=task_id,
            task_title=task_title,
            timestamp=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            source_file=source_file,
            learning_type=learning_type,
            title=title,
            description=text[:500],
            category="technical",
            tags=self._extract_tags(text),
        )

    def _extract_tags(self, text: str) -> List[str]:
        """Extract relevant tags from text."""
        tags = []
        keywords = {
            "python": "python",
            "yaml": "yaml",
            "json": "json",
            "bash": "bash",
            "shell": "shell",
            "git": "git",
            "test": "testing",
            "error": "error-handling",
            "exception": "error-handling",
            "api": "api",
            "database": "database",
            "db": "database",
            "sql": "sql",
            "async": "async",
            "sync": "sync",
            "file": "file-io",
            "path": "file-io",
            "directory": "file-io",
            "config": "configuration",
            "setup": "setup",
            "install": "setup",
            "dependency": "dependencies",
            "import": "imports",
            "module": "modules",
            "class": "oop",
            "function": "functions",
            "method": "functions",
            "performance": "performance",
            "slow": "performance",
            "fast": "performance",
            "memory": "memory",
            "cache": "caching",
            "security": "security",
            "auth": "security",
            "validation": "validation",
            "schema": "schema",
            "parse": "parsing",
            "extract": "extraction",
            "transform": "transformation",
        }

        text_lower = text.lower()
        for keyword, tag in keywords.items():
            if keyword in text_lower and tag not in tags:
                tags.append(tag)

        return tags[:5]  # Limit to 5 tags

    def process_run(self, run_dir: Path, save: bool = True) -> List[Learning]:
        """
        Process a single run directory and optionally save to index.

        Args:
            run_dir: Path to run directory
            save: Whether to save to index immediately

        Returns:
            List of new learnings extracted
        """
        new_learnings = self.extract_from_run(run_dir)

        if new_learnings:
            self.learnings.extend(new_learnings)

            if save:
                self._save_index()

        return new_learnings

    def backfill(self, runs_dir: Path, dry_run: bool = False) -> List[Learning]:
        """
        Process all runs in a directory and backfill the index.

        Args:
            runs_dir: Directory containing run directories
            dry_run: If True, don't save to index

        Returns:
            List of all new learnings extracted
        """
        runs_dir = Path(runs_dir)
        if not runs_dir.exists():
            print(f"Error: Runs directory not found: {runs_dir}")
            return []

        # Find all run directories
        run_dirs = sorted([d for d in runs_dir.iterdir() if d.is_dir() and d.name.startswith("run-")])

        print(f"Found {len(run_dirs)} run directories to process")
        print("-" * 50)

        all_new_learnings = []

        for i, run_dir in enumerate(run_dirs, 1):
            print(f"\n[{i}/{len(run_dirs)}] ", end="")
            new_learnings = self.extract_from_run(run_dir)
            all_new_learnings.extend(new_learnings)

        print("\n" + "-" * 50)
        print(f"Backfill complete: {len(all_new_learnings)} new learnings extracted")

        if all_new_learnings and not dry_run:
            self.learnings.extend(all_new_learnings)
            self._save_index()

        return all_new_learnings

    def rebuild_index(self, runs_dir: Path):
        """
        Rebuild the entire index from scratch.

        Args:
            runs_dir: Directory containing run directories
        """
        print("Rebuilding index from scratch...")

        # Clear existing data
        self.learnings = []
        self.patterns = []
        self.existing_hashes = set()

        # Process all runs
        self.backfill(runs_dir, dry_run=False)

        print(f"Index rebuilt with {len(self.learnings)} learnings")

    def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the learning index.

        Returns:
            Dictionary with health check results
        """
        results = {
            "status": "healthy",
            "issues": [],
            "stats": {},
        }

        # Check index file exists
        if not self.index_path.exists():
            results["status"] = "error"
            results["issues"].append("Index file does not exist")
            return results

        # Load and validate
        try:
            with open(self.index_path, 'r') as f:
                data = yaml.safe_load(f)

            # Check metadata
            metadata = data.get('metadata', {})
            total_learnings = metadata.get('total_learnings', 0)
            actual_learnings = len(data.get('learnings', []))

            results["stats"]["total_learnings"] = actual_learnings
            results["stats"]["total_patterns"] = len(data.get('patterns', []))

            # Validate consistency
            if total_learnings != actual_learnings:
                results["status"] = "warning"
                results["issues"].append(f"Metadata mismatch: claims {total_learnings} but has {actual_learnings}")

            # Check for empty learnings
            if actual_learnings == 0:
                results["status"] = "warning"
                results["issues"].append("No learnings in index")

            # Check for duplicates
            hashes = [l.get('content_hash', '') for l in data.get('learnings', [])]
            duplicates = len(hashes) - len(set(hashes))
            if duplicates > 0:
                results["status"] = "warning"
                results["issues"].append(f"Found {duplicates} duplicate learnings")

            # Check statistics
            stats = data.get('statistics', {})
            by_type = stats.get('by_type', {})
            by_category = stats.get('by_category', {})

            results["stats"]["types"] = by_type
            results["stats"]["categories"] = by_category

        except Exception as e:
            results["status"] = "error"
            results["issues"].append(f"Failed to parse index: {e}")

        return results


def main():
    parser = argparse.ArgumentParser(
        description="Learning Extractor - Extract and index learnings from task runs"
    )
    parser.add_argument("--run-dir", help="Process a single run directory")
    parser.add_argument("--runs-dir", help="Directory containing multiple runs")
    parser.add_argument("--backfill", action="store_true", help="Backfill all runs")
    parser.add_argument("--rebuild-index", action="store_true", help="Rebuild entire index")
    parser.add_argument("--health-check", action="store_true", help="Check index health")
    parser.add_argument("--index-path", help="Custom path to learning-index.yaml")
    parser.add_argument("--dry-run", action="store_true", help="Don't save changes")

    args = parser.parse_args()

    # Initialize extractor
    extractor = LearningExtractor(index_path=args.index_path)

    if args.health_check:
        results = extractor.health_check()
        print("\n" + "=" * 50)
        print("HEALTH CHECK RESULTS")
        print("=" * 50)
        print(f"Status: {results['status'].upper()}")
        print(f"\nStats:")
        for key, value in results['stats'].items():
            print(f"  {key}: {value}")
        if results['issues']:
            print(f"\nIssues ({len(results['issues'])}):")
            for issue in results['issues']:
                print(f"  - {issue}")
        print("=" * 50)
        return 0 if results['status'] == 'healthy' else 1

    elif args.rebuild_index:
        if not args.runs_dir:
            print("Error: --runs-dir required for rebuild")
            return 1
        extractor.rebuild_index(Path(args.runs_dir))

    elif args.backfill:
        if not args.runs_dir:
            # Use default runs directory
            args.runs_dir = "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/agents/executor/runs"
        extractor.backfill(Path(args.runs_dir), dry_run=args.dry_run)

    elif args.run_dir:
        new_learnings = extractor.process_run(Path(args.run_dir), save=not args.dry_run)
        print(f"\nExtracted {len(new_learnings)} new learnings")

    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
