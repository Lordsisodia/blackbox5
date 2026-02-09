#!/usr/bin/env python3
"""
Decision Registry Extractor

Extracts decisions from all DECISIONS.md files and generates a central registry.
Handles 4 format variants found in the codebase.
"""

import os
import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import glob

# Registry schema version
REGISTRY_VERSION = "1.0"

# Categories for classification
CATEGORIES = [
    "process",
    "technical",
    "architecture",
    "planning",
    "execution",
    "improvement",
    "infrastructure",
    "other"
]


def find_decisions_files(base_path: str) -> List[str]:
    """Find all DECISIONS.md files recursively, excluding archived/backup/migrated."""
    pattern = os.path.join(base_path, "**/DECISIONS.md")
    all_files = glob.glob(pattern, recursive=True)

    # Filter out archived, backup, and migrated directories
    filtered = []
    for f in all_files:
        # Skip if in archived, backup, or migrated directories
        if '/archived/' in f or '/backup/' in f or '.migrated' in f:
            continue
        # Skip if file is too small (likely empty/template)
        try:
            if os.path.getsize(f) < 100:  # Skip files under 100 bytes
                continue
        except:
            continue
        filtered.append(f)

    return sorted(filtered)


def parse_timestamp_from_filename(filepath: str) -> Optional[str]:
    """Extract timestamp from file path if available."""
    # Try to extract from run folder names like run-20260206-082558 or run-20260131_192605
    patterns = [
        r'run-(\d{8})[_-](\d{6})',
        r'run-(\d{4})(\d{2})(\d{2})[_-](\d{2})(\d{2})(\d{2})',
        r'(\d{4})-(\d{2})-(\d{2})',
    ]

    for pattern in patterns:
        match = re.search(pattern, filepath)
        if match:
            groups = match.groups()
            if len(groups) == 2:
                # run-20260206-082558 format
                date_part = groups[0]
                time_part = groups[1]
                return f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:]}T{time_part[:2]}:{time_part[2:4]}:{time_part[4:6]}Z"
            elif len(groups) == 6:
                # Already separated components
                return f"{groups[0]}-{groups[1]}-{groups[2]}T{groups[3]}:{groups[4]}:{groups[5]}Z"
            elif len(groups) == 3:
                # Date only
                return f"{groups[0]}-{groups[1]}-{groups[2]}T00:00:00Z"
    return None


def extract_decision_variant_1(content: str, source_file: str) -> List[Dict[str, Any]]:
    """
    Format Variant 1: Structured decisions with headers like '## Decision D-XXX: Title'
    Example: Planner Run 0073 format
    """
    decisions = []

    # Pattern for D-XXX format decisions
    pattern = r'## Decision (D-\d+): (.+?)\n\n\*\*Status:\*\* (\w+)'
    matches = list(re.finditer(pattern, content, re.DOTALL))

    for i, match in enumerate(matches):
        decision_id = match.group(1)
        title = match.group(2).strip()
        status = match.group(3).lower()

        # Extract section content
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        section = content[start:end]

        # Extract rationale
        rationale_match = re.search(r'### Decision\s*\n\n(.+?)(?:\n\n###|$)', section, re.DOTALL)
        rationale = rationale_match.group(1).strip() if rationale_match else ""

        # Extract alternatives
        alternatives = []
        alt_section = re.search(r'### Alternatives Considered\s*\n\n(.+?)(?:\n\n###|$)', section, re.DOTALL)
        if alt_section:
            alt_text = alt_section.group(1)
            # Find numbered alternatives
            alt_pattern = r'^(\d+)\.\s+\*\*(.+?)\*\*\s*\((.+?)\)'
            for alt_match in re.finditer(alt_pattern, alt_text, re.MULTILINE):
                alternatives.append({
                    "option": alt_match.group(2).strip(),
                    "outcome": alt_match.group(3).lower()
                })

        # Extract timestamp from content or use file timestamp
        timestamp_match = re.search(r'\*\*Timestamp:\*\* ([\d\-T:]+Z?)', content)
        timestamp = timestamp_match.group(1) if timestamp_match else parse_timestamp_from_filename(source_file)
        if not timestamp:
            timestamp = datetime.now().isoformat() + "Z"

        # Categorize
        category = categorize_decision(title, rationale)

        # Extract tags
        tags = extract_tags(title, rationale)

        decisions.append({
            "title": title,
            "status": status,
            "rationale": rationale[:500] if rationale else "",  # Truncate long rationale
            "alternatives": alternatives,
            "timestamp": timestamp,
            "category": category,
            "tags": tags,
            "format": "variant_1_structured"
        })

    return decisions


def extract_decision_variant_2(content: str, source_file: str) -> List[Dict[str, Any]]:
    """
    Format Variant 2: Simple numbered decisions
    Example: Planner Run 0016 format with **Decision:** or **Selected:**
    """
    decisions = []

    # Pattern for "## Decision X: Title" or "## Decision X - Title" followed by **Decision:** or **Selected:**
    pattern = r'## Decision (\d+):?\s*(.+?)\n\n\*\*(?:Decision|Selected):\*\*\s*(.+?)(?:\n\n|$)'
    matches = list(re.finditer(pattern, content, re.DOTALL))

    for i, match in enumerate(matches):
        decision_num = match.group(1)
        title = match.group(2).strip()
        decision_text = match.group(3).strip()

        # Extract section content
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        section = content[start:end]

        # Extract rationale
        rationale_match = re.search(r'\*\*Rationale:\*\*\s*\n(.+?)(?:\n\n\*\*|$)', section, re.DOTALL)
        rationale = rationale_match.group(1).strip() if rationale_match else ""

        # Extract alternatives
        alternatives = []
        alt_section = re.search(r'\*\*Alternatives Considered:\*\*\s*\n(.+?)(?:\n\n\*\*|$)', section, re.DOTALL)
        if alt_section:
            alt_text = alt_section.group(1)
            # Parse bullet points
            for line in alt_text.split('\n'):
                if line.strip().startswith('-') or line.strip().startswith('*'):
                    alt_text_clean = line.strip()[1:].strip()
                    if ' - ' in alt_text_clean:
                        parts = alt_text_clean.split(' - ')
                        alternatives.append({
                            "option": parts[0].strip(),
                            "outcome": parts[1].strip().lower()
                        })
                    else:
                        alternatives.append({
                            "option": alt_text_clean,
                            "outcome": "considered"
                        })

        # Extract timestamp
        timestamp_match = re.search(r'\*\*Date:\*\* ([\d\-]+)', content)
        if timestamp_match:
            date_str = timestamp_match.group(1)
            timestamp = f"{date_str}T00:00:00Z"
        else:
            timestamp = parse_timestamp_from_filename(source_file)
        if not timestamp:
            timestamp = datetime.now().isoformat() + "Z"

        # Categorize
        category = categorize_decision(title, rationale)
        tags = extract_tags(title, rationale)

        decisions.append({
            "title": title,
            "status": "approved",  # Default for this format
            "rationale": rationale[:500] if rationale else decision_text[:500],
            "alternatives": alternatives,
            "timestamp": timestamp,
            "category": category,
            "tags": tags,
            "format": "variant_2_numbered"
        })

    return decisions


def extract_decision_variant_3(content: str, source_file: str) -> List[Dict[str, Any]]:
    """
    Format Variant 3: Auditor/Worker format with simple list
    Example: Auditor Worker Run 001 format with ### X. Title and bullet points
    """
    decisions = []

    # Pattern for "### X. Title" format with bullet-style decision
    pattern = r'### (\d+)\.\s+(.+?)\n\n?-\s+\*\*Decision:\*\*\s*(.+?)(?:\n\n|$)'
    matches = list(re.finditer(pattern, content, re.DOTALL))

    for i, match in enumerate(matches):
        decision_num = match.group(1)
        title = match.group(2).strip()
        decision_text = match.group(3).strip()

        # Extract section content
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        section = content[start:end]

        # Extract rationale
        rationale_match = re.search(r'- \*\*Rationale:\*\*\s*(.+?)(?:\n|$)', section)
        rationale = rationale_match.group(1).strip() if rationale_match else ""

        # Extract timestamp
        timestamp_match = re.search(r'\*\*Date:\*\* ([\d\-]+)', content)
        if timestamp_match:
            date_str = timestamp_match.group(1)
            timestamp = f"{date_str}T00:00:00Z"
        else:
            timestamp = parse_timestamp_from_filename(source_file)
        if not timestamp:
            timestamp = datetime.now().isoformat() + "Z"

        # Categorize
        category = categorize_decision(title, rationale)
        tags = extract_tags(title, rationale)

        decisions.append({
            "title": title,
            "status": "approved",
            "rationale": rationale if rationale else decision_text,
            "alternatives": [],
            "timestamp": timestamp,
            "category": category,
            "tags": tags,
            "format": "variant_3_auditor"
        })

    return decisions


def extract_decision_variant_5(content: str, source_file: str) -> List[Dict[str, Any]]:
    """
    Format Variant 5: Executor style with ## Title and **Selected:**
    Example: Executor Run format
    """
    decisions = []

    # Pattern for "## Title" followed by **Context:** and **Selected:**
    pattern = r'## (.+?)\n\n\*\*Context:\*\*(.+?)\n\n\*\*Selected:\*\*\s*(.+?)(?:\n\n|$)'
    matches = list(re.finditer(pattern, content, re.DOTALL))

    for i, match in enumerate(matches):
        title = match.group(1).strip()
        context_text = match.group(2).strip()
        decision_text = match.group(3).strip()

        # Extract section content
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        section = content[start:end]

        # Extract rationale
        rationale_match = re.search(r'\*\*Rationale:\*\*\s*\n(.+?)(?:\n\n\*\*|$)', section, re.DOTALL)
        rationale = rationale_match.group(1).strip() if rationale_match else ""

        # Extract timestamp
        timestamp_match = re.search(r'\*\*Date:\*\* ([\d\-]+)', content)
        if timestamp_match:
            date_str = timestamp_match.group(1)
            timestamp = f"{date_str}T00:00:00Z"
        else:
            timestamp = parse_timestamp_from_filename(source_file)
        if not timestamp:
            timestamp = datetime.now().isoformat() + "Z"

        # Categorize
        category = categorize_decision(title, rationale)
        tags = extract_tags(title, rationale)

        decisions.append({
            "title": title,
            "status": "approved",
            "rationale": rationale[:500] if rationale else decision_text[:500],
            "alternatives": [],
            "timestamp": timestamp,
            "category": category,
            "tags": tags,
            "format": "variant_5_executor"
        })

    return decisions


def extract_decision_variant_4(content: str, source_file: str) -> List[Dict[str, Any]]:
    """
    Format Variant 4: Table format
    Example: Run with decision table
    """
    decisions = []

    # Look for decision tables
    table_pattern = r'\| Timestamp \| Decision \| Rationale \| Status \|\n\|[-|]+\n(.+?)(?:\n\n|$)'
    table_match = re.search(table_pattern, content, re.DOTALL)

    if table_match:
        table_content = table_match.group(1)
        rows = table_content.strip().split('\n')

        for row in rows:
            cells = [cell.strip() for cell in row.split('|')]
            if len(cells) >= 4:
                timestamp_str = cells[0]
                title = cells[1]
                rationale = cells[2]
                status = cells[3].lower()

                # Parse timestamp
                try:
                    dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    timestamp = dt.isoformat() + "Z"
                except:
                    timestamp = parse_timestamp_from_filename(source_file)
                    if not timestamp:
                        timestamp = datetime.now().isoformat() + "Z"

                category = categorize_decision(title, rationale)
                tags = extract_tags(title, rationale)

                decisions.append({
                    "title": title,
                    "status": status,
                    "rationale": rationale,
                    "alternatives": [],
                    "timestamp": timestamp,
                    "category": category,
                    "tags": tags,
                    "format": "variant_4_table"
                })

    return decisions


def categorize_decision(title: str, rationale: str) -> str:
    """Categorize a decision based on title and rationale."""
    text = (title + " " + rationale).lower()

    if any(word in text for word in ['process', 'workflow', 'pipeline', 'queue', 'task creation']):
        return "process"
    elif any(word in text for word in ['architecture', 'design', 'structure', 'pattern']):
        return "architecture"
    elif any(word in text for word in ['implement', 'code', 'function', 'class', 'module']):
        return "technical"
    elif any(word in text for word in ['plan', 'schedule', 'priority', 'milestone']):
        return "planning"
    elif any(word in text for word in ['execute', 'run', 'perform', 'complete']):
        return "execution"
    elif any(word in text for word in ['improve', 'optimize', 'refine', 'enhance', 'better']):
        return "improvement"
    elif any(word in text for word in ['infrastructure', 'deploy', 'server', 'config']):
        return "infrastructure"
    else:
        return "other"


def extract_tags(title: str, rationale: str) -> List[str]:
    """Extract relevant tags from decision content."""
    text = (title + " " + rationale).lower()
    tags = []

    tag_keywords = {
        "queue": ["queue", "depth", "refill"],
        "skills": ["skill", "invocation", "bmad-"],
        "estimation": ["estimate", "estimation", "formula", "lines-per-minute"],
        "specs": ["spec", "specification", "product spec", "implementation spec"],
        "monitoring": ["monitor", "automated", "trigger"],
        "priority": ["priority", "re-rank", "score"],
        "tasks": ["task", "create task"],
        "learning": ["learning", "improvement", "pipeline"],
        "review": ["review", "first principles"],
    }

    for tag, keywords in tag_keywords.items():
        if any(kw in text for kw in keywords):
            tags.append(tag)

    return tags[:5]  # Limit to 5 tags


def parse_decisions_file(filepath: str) -> List[Dict[str, Any]]:
    """Parse a single DECISIONS.md file and extract all decisions."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return []

    # Skip files with no decisions
    if "No decisions" in content or "No decisions yet" in content or len(content.strip()) < 50:
        return []

    source_file = filepath.replace(os.path.expanduser("~/.blackbox5/"), "")

    all_decisions = []

    # Try all format variants
    all_decisions.extend(extract_decision_variant_1(content, source_file))
    all_decisions.extend(extract_decision_variant_2(content, source_file))
    all_decisions.extend(extract_decision_variant_3(content, source_file))
    all_decisions.extend(extract_decision_variant_4(content, source_file))
    all_decisions.extend(extract_decision_variant_5(content, source_file))

    # Add source file info to each decision
    for decision in all_decisions:
        decision["source_file"] = source_file
        # Extract run ID from path
        run_match = re.search(r'runs/([^/]+/[^/]+)', source_file)
        decision["source_run"] = run_match.group(1) if run_match else "unknown"

    return all_decisions


def deduplicate_decisions(decisions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate decisions based on title + rationale content."""
    seen = set()
    unique = []

    for d in decisions:
        # Create a fingerprint from title + first 100 chars of rationale
        fingerprint = (d.get("title", "").strip().lower()[:100],
                      d.get("rationale", "").strip().lower()[:100])

        if fingerprint not in seen:
            seen.add(fingerprint)
            unique.append(d)

    return unique


def generate_registry(decisions: List[Dict[str, Any]], output_path: str):
    """Generate the central registry YAML file."""

    # Deduplicate decisions
    decisions = deduplicate_decisions(decisions)

    # Sort decisions by timestamp
    decisions.sort(key=lambda x: x.get("timestamp", ""))

    # Assign sequential IDs
    for i, decision in enumerate(decisions, 1):
        decision["id"] = f"DEC-{i:04d}"

    # Build registry structure
    registry = {
        "registry": {
            "version": REGISTRY_VERSION,
            "last_updated": datetime.now().isoformat() + "Z",
            "total_decisions": len(decisions),
            "source_files_analyzed": len(set(d["source_file"] for d in decisions))
        },
        "decisions": []
    }

    for decision in decisions:
        # Clean up title - extract just the title, not extra content
        title = decision["title"]
        if "\n" in title:
            title = title.split("\n")[0].strip()
        if title.startswith("**"):
            title = title.strip("*")

        registry["decisions"].append({
            "id": decision["id"],
            "source_file": decision["source_file"],
            "source_run": decision["source_run"],
            "timestamp": decision["timestamp"],
            "title": title[:200],  # Limit title length
            "category": decision["category"],
            "status": decision["status"],
            "rationale": decision["rationale"][:300] if decision["rationale"] else "",  # Truncate
            "tags": decision["tags"],
            "alternatives": decision.get("alternatives", []),
            "format": decision.get("format", "unknown")
        })

    # Write YAML file
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(registry, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    return registry


def main():
    base_path = os.path.expanduser("~/.blackbox5")
    output_path = os.path.expanduser("~/.blackbox5/5-project-memory/blackbox5/.autonomous/decisions/decision_registry.yaml")

    print(f"Scanning for DECISIONS.md files in {base_path}...")

    # Find all decisions files
    files = find_decisions_files(base_path)
    print(f"Found {len(files)} DECISIONS.md files")

    # Parse all files
    all_decisions = []
    files_with_decisions = 0
    files_without_decisions = 0

    for filepath in files:
        decisions = parse_decisions_file(filepath)
        if decisions:
            all_decisions.extend(decisions)
            files_with_decisions += 1
        else:
            files_without_decisions += 1

    print(f"Files with decisions: {files_with_decisions}")
    print(f"Files without decisions: {files_without_decisions}")
    print(f"Total decisions extracted: {len(all_decisions)}")

    # Generate registry
    registry = generate_registry(all_decisions, output_path)

    print(f"\nRegistry generated: {output_path}")
    print(f"Total decisions: {registry['registry']['total_decisions']}")
    print(f"Source files analyzed: {registry['registry']['source_files_analyzed']}")

    # Print category breakdown
    categories = {}
    for d in all_decisions:
        cat = d.get("category", "other")
        categories[cat] = categories.get(cat, 0) + 1

    print("\nDecisions by category:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

    return registry


if __name__ == "__main__":
    main()
