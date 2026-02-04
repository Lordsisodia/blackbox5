#!/usr/bin/env python3
"""
RETAIN Operation Prototype for Hindsight Memory Architecture

This prototype demonstrates the extraction pipeline that processes tasks/runs
and populates the 4 memory networks (World, Experience, Opinion, Observation).

Usage:
    python retain.py --source /path/to/TASK.md --output ./memories/
    python retain.py --source /path/to/run-folder/ --output ./memories/
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Optional


class MemoryNetwork(Enum):
    """Hindsight's 4 memory networks"""
    WORLD = "world"           # Objective facts
    EXPERIENCE = "experience" # First-person actions
    OPINION = "opinion"       # Beliefs with confidence
    OBSERVATION = "observation"  # Synthesized insights


@dataclass
class ExtractedMemory:
    """A single extracted memory unit"""
    network: MemoryNetwork
    content: str
    source: str  # File path or task ID
    confidence: float = 0.8  # Default confidence
    entities: List[str] = field(default_factory=list)
    timestamp: Optional[str] = None
    context: Optional[str] = None  # Surrounding context

    def to_dict(self) -> dict:
        return {
            "network": self.network.value,
            "content": self.content,
            "source": self.source,
            "confidence": self.confidence,
            "entities": self.entities,
            "timestamp": self.timestamp,
            "context": self.context
        }


class RetainEngine:
    """
    RETAIN operation engine for extracting structured memories.

    In the full implementation, this would use LLM for extraction.
    This prototype uses rule-based extraction for demonstration.
    """

    def __init__(self):
        self.memories: List[ExtractedMemory] = []

    def process_file(self, file_path: Path) -> List[ExtractedMemory]:
        """Process a single markdown file and extract memories"""
        content = file_path.read_text()

        # Extract frontmatter if present
        frontmatter = self._extract_frontmatter(content)
        body = self._extract_body(content)

        memories = []

        # Extract based on file type
        if "TASK" in file_path.name.upper() or "task.md" in str(file_path):
            memories.extend(self._extract_from_task(body, str(file_path), frontmatter))
        elif "THOUGHTS" in file_path.name.upper():
            memories.extend(self._extract_from_thoughts(body, str(file_path)))
        elif "DECISIONS" in file_path.name.upper():
            memories.extend(self._extract_from_decisions(body, str(file_path)))
        else:
            # Generic extraction
            memories.extend(self._extract_generic(body, str(file_path)))

        self.memories.extend(memories)
        return memories

    def _extract_frontmatter(self, content: str) -> dict:
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

    def _extract_from_task(self, body: str, source: str, frontmatter: dict) -> List[ExtractedMemory]:
        """Extract memories from task files"""
        memories = []

        # Extract objective as World fact
        objective_match = re.search(r'## Objective\s*\n(.+?)(?=\n##|\Z)', body, re.DOTALL)
        if objective_match:
            memories.append(ExtractedMemory(
                network=MemoryNetwork.WORLD,
                content=f"Task objective: {objective_match.group(1).strip()}",
                source=source,
                confidence=0.95,
                entities=self._extract_entities(objective_match.group(1)),
                timestamp=frontmatter.get("created")
            ))

        # Extract success criteria as Observations
        success_match = re.search(r'## Success Criteria\s*\n(.+?)(?=\n##|\Z)', body, re.DOTALL)
        if success_match:
            criteria = success_match.group(1).strip()
            for line in criteria.split('\n'):
                if line.strip().startswith('- ['):
                    content = re.sub(r'- \[[ x]\] ', '', line).strip()
                    memories.append(ExtractedMemory(
                        network=MemoryNetwork.OBSERVATION,
                        content=f"Success criterion: {content}",
                        source=source,
                        confidence=0.85,
                        entities=self._extract_entities(content)
                    ))

        # Extract approach as Experience
        approach_match = re.search(r'## Approach\s*\n(.+?)(?=\n##|\Z)', body, re.DOTALL)
        if approach_match:
            memories.append(ExtractedMemory(
                network=MemoryNetwork.EXPERIENCE,
                content=f"Approach: {approach_match.group(1).strip()[:500]}",
                source=source,
                confidence=0.8,
                entities=self._extract_entities(approach_match.group(1))
            ))

        # Extract context insights as Opinions
        context_match = re.search(r'## Context\s*\n(.+?)(?=\n##|\Z)', body, re.DOTALL)
        if context_match:
            context_text = context_match.group(1).strip()
            # Look for insight patterns ("This means...", "The key insight...")
            for line in context_text.split('\n'):
                if any(marker in line for marker in ['insight', 'means that', 'suggests', 'indicates']):
                    memories.append(ExtractedMemory(
                        network=MemoryNetwork.OPINION,
                        content=f"Insight: {line.strip()}",
                        source=source,
                        confidence=0.75,
                        entities=self._extract_entities(line)
                    ))

        return memories

    def _extract_from_thoughts(self, body: str, source: str) -> List[ExtractedMemory]:
        """Extract memories from THOUGHTS.md files"""
        memories = []

        # Analysis section contains experiences
        analysis_match = re.search(r'## Analysis\s*\n(.+?)(?=\n##|\Z)', body, re.DOTALL)
        if analysis_match:
            analysis_text = analysis_match.group(1).strip()
            if len(analysis_text) > 50:  # Only if there's actual content
                memories.append(ExtractedMemory(
                    network=MemoryNetwork.EXPERIENCE,
                    content=f"Analysis: {analysis_text[:500]}",
                    source=source,
                    confidence=0.7,
                    entities=self._extract_entities(analysis_text)
                ))

        # Next steps are experiences (actions taken)
        next_steps_match = re.search(r'## Next Steps\s*\n(.+?)(?=\n##|\Z)', body, re.DOTALL)
        if next_steps_match:
            steps_text = next_steps_match.group(1).strip()
            for line in steps_text.split('\n'):
                if line.strip().startswith(('1.', '2.', '3.', '-', '*')):
                    content = re.sub(r'^[\d\-\*\.\s]+', '', line).strip()
                    if content:
                        memories.append(ExtractedMemory(
                            network=MemoryNetwork.EXPERIENCE,
                            content=f"Action: {content}",
                            source=source,
                            confidence=0.8,
                            entities=self._extract_entities(content)
                        ))

        return memories

    def _extract_from_decisions(self, body: str, source: str) -> List[ExtractedMemory]:
        """Extract memories from DECISIONS.md files"""
        memories = []

        # Extract decision blocks
        decision_pattern = r'### (D-\d+):\s*(.+?)\n\s*\*\*Context:\*\*(.+?)\n\s*\*\*Decision:\*\*(.+?)\n\s*\*\*Rationale:\*\*(.+?)(?=\n###|\Z)'
        decisions = re.findall(decision_pattern, body, re.DOTALL)

        for decision_id, title, context, decision, rationale in decisions:
            # Decision is a World fact (what was decided)
            memories.append(ExtractedMemory(
                network=MemoryNetwork.WORLD,
                content=f"Decision {decision_id}: {title.strip()} - {decision.strip()}",
                source=source,
                confidence=0.95,
                entities=self._extract_entities(title + decision)
            ))

            # Rationale contains Opinions (beliefs)
            memories.append(ExtractedMemory(
                network=MemoryNetwork.OPINION,
                content=f"Rationale for {decision_id}: {rationale.strip()[:300]}",
                source=source,
                confidence=0.8,
                entities=self._extract_entities(rationale)
            ))

        return memories

    def _extract_generic(self, body: str, source: str) -> List[ExtractedMemory]:
        """Generic extraction for unknown file types"""
        memories = []

        # Extract headers as potential observations
        headers = re.findall(r'##+\s*(.+?)\n', body)
        for header in headers[:5]:  # Limit to first 5
            memories.append(ExtractedMemory(
                network=MemoryNetwork.OBSERVATION,
                content=f"Section: {header.strip()}",
                source=source,
                confidence=0.6
            ))

        return memories

    def _extract_entities(self, text: str) -> List[str]:
        """Extract named entities from text (simplified)"""
        entities = []

        # Look for capitalized phrases (potential entities)
        capitalized = re.findall(r'\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\b', text)
        entities.extend([e for e in capitalized if len(e) > 3][:10])  # Limit to 10

        # Look for code-like terms (backticks)
        code_terms = re.findall(r'`([^`]+)`', text)
        entities.extend(code_terms[:5])

        # Look for file paths
        paths = re.findall(r'[\w\-/]+\.(md|py|yaml|json|sh)', text)
        entities.extend(paths[:5])

        return list(set(entities))  # Deduplicate

    def save_memories(self, output_dir: Path):
        """Save extracted memories to files"""
        output_dir.mkdir(parents=True, exist_ok=True)

        # Group by network
        by_network = {}
        for memory in self.memories:
            network = memory.network.value
            if network not in by_network:
                by_network[network] = []
            by_network[network].append(memory.to_dict())

        # Save each network
        for network, memories in by_network.items():
            output_file = output_dir / f"{network}_memories.json"
            with open(output_file, 'w') as f:
                json.dump(memories, f, indent=2)
            print(f"Saved {len(memories)} {network} memories to {output_file}")

        # Save combined
        all_memories = [m.to_dict() for m in self.memories]
        combined_file = output_dir / "all_memories.json"
        with open(combined_file, 'w') as f:
            json.dump(all_memories, f, indent=2)
        print(f"Saved {len(all_memories)} total memories to {combined_file}")


def main():
    parser = argparse.ArgumentParser(description="RETAIN operation prototype")
    parser.add_argument("--source", required=True, help="Source file or directory")
    parser.add_argument("--output", default="./memories", help="Output directory")
    args = parser.parse_args()

    source = Path(args.source)
    output = Path(args.output)

    engine = RetainEngine()

    if source.is_file():
        print(f"Processing file: {source}")
        memories = engine.process_file(source)
        print(f"Extracted {len(memories)} memories")
    elif source.is_dir():
        print(f"Processing directory: {source}")
        md_files = list(source.rglob("*.md"))
        print(f"Found {len(md_files)} markdown files")
        for md_file in md_files:
            try:
                memories = engine.process_file(md_file)
                print(f"  {md_file.name}: {len(memories)} memories")
            except Exception as e:
                print(f"  {md_file.name}: ERROR - {e}")
    else:
        print(f"Source not found: {source}")
        sys.exit(1)

    engine.save_memories(output)
    print(f"\nRETAIN complete. Memories saved to {output}")


if __name__ == "__main__":
    main()
