#!/usr/bin/env python3
"""
BLACKBOX5 Catalog Generator

Scans the entire BLACKBOX5 codebase and generates CATALOG.md - the universal
index that makes every component discoverable by AI agents and humans alike.

Usage:
    python scripts/generate_catalog.py
    python scripts/generate_catalog.py --output docs/CATALOG.md
    python scripts/generate_catalog.py --validate  # Check for missing docs
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import re
import ast

logger = logging.getLogger(__name__)


class CatalogGenerator:
    """Generates a universal catalog of BLACKBOX5 components."""

    def __init__(self, root_dir: Path = None):
        self.root_dir = root_dir or Path(__file__).parent.parent
        self.catalog_data = {
            "agents": [],
            "tools": [],
            "integrations": [],
            "capabilities": [],
            "workflows": [],
            "knowledge": [],
            "operations": [],
            "directories": {},
        }

    def scan(self) -> Dict[str, Any]:
        """Scan the entire BLACKBOX5 codebase."""
        print(f"🔍 Scanning BLACKBOX5 at: {self.root_dir}")

        # Scan each major directory
        self._scan_agents()
        self._scan_tools()
        self._scan_integrations()
        self._scan_capabilities()
        self._scan_knowledge()
        self._scan_operations()

        # Build directory map
        self._build_directory_map()

        return self.catalog_data

    def _scan_agents(self):
        """Scan all agent definitions."""
        agents_dir = self.root_dir / "2-engine" / "01-core" / "agents"

        # Python agents
        for py_file in agents_dir.glob("*Agent.py"):
            try:
                self._parse_python_agent(py_file)
            except Exception as e:
                print(f"⚠️  Error parsing {py_file}: {e}")

        # YAML agents (specialists)
        for yaml_file in agents_dir.glob("*specialist*.yaml"):
            try:
                self._parse_yaml_agent(yaml_file)
            except Exception as e:
                print(f"⚠️  Error parsing {yaml_file}: {e}")

    def _parse_python_agent(self, file_path: Path):
        """Parse a Python agent file."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name.endswith("Agent"):
                    docstring = ast.get_docstring(node)

                    self.catalog_data["agents"].append({
                        "name": node.name,
                        "type": "Python Agent",
                        "location": str(file_path.relative_to(self.root_dir)),
                        "description": docstring or "",
                        "category": "core" if node.name in ["ArchitectAgent", "AnalystAgent", "DeveloperAgent"] else "specialist"
                    })
        except (SyntaxError, ValueError, IOError):
            pass

    def _parse_yaml_agent(self, file_path: Path):
        """Parse a YAML agent definition."""
        try:
            import yaml

            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)

            if not data or 'agent' not in data:
                return

            agent = data['agent']
            metadata = agent.get('metadata', {})
            persona = agent.get('persona', {})

            self.catalog_data["agents"].append({
                "name": metadata.get('name', file_path.stem),
                "title": metadata.get('title', ''),
                "type": "YAML Agent",
                "location": str(file_path.relative_to(self.root_dir)),
                "id": metadata.get('id', ''),
                "category": "specialist",
                "role": persona.get('role', ''),
                "description": persona.get('identity', ''),
                "capabilities": agent.get('capabilities', []),
            })
        except ImportError:
            print("⚠️  PyYAML not installed, skipping YAML agents")
        except Exception as e:
            print(f"⚠️  Error parsing YAML {file_path}: {e}")

    def _scan_tools(self):
        """Scan all available tools."""
        tools_dir = self.root_dir / "2-engine" / "05-tools"

        if tools_dir.exists():
            for category_dir in tools_dir.iterdir():
                if category_dir.is_dir() and not category_dir.name.startswith('_'):
                    self._scan_tool_category(category_dir)

    def _scan_tool_category(self, category_dir: Path):
        """Scan a tool category directory."""
        category = category_dir.name

        for py_file in category_dir.glob("*.py"):
            if py_file.name.startswith('_'):
                continue

            try:
                with open(py_file, 'r') as f:
                    content = f.read()

                # Extract docstring
                tree = ast.parse(content)
                docstring = ast.get_docstring(tree)

                # Find functions (tools)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_doc = ast.get_docstring(node)

                        self.catalog_data["tools"].append({
                            "name": node.name,
                            "category": category,
                            "location": str(py_file.relative_to(self.root_dir)),
                            "description": func_doc or "",
                        })
            except (IOError, OSError) as e:
                logger.warning(f"Could not read file {py_file}: {e}")
            except SyntaxError as e:
                logger.debug(f"Skipping malformed Python file {py_file}: {e}")
            except Exception as e:
                logger.error(f"Unexpected error processing {py_file}: {e}")

    def _scan_integrations(self):
        """Scan all external integrations."""
        integrations_dir = self.root_dir / "2-engine" / "06-integrations"

        if integrations_dir.exists():
            for integration_dir in integrations_dir.iterdir():
                if integration_dir.is_dir() and not integration_dir.name.startswith('_'):
                    self.catalog_data["integrations"].append({
                        "name": integration_dir.name,
                        "location": str(integration_dir.relative_to(self.root_dir)),
                        "description": self._get_directory_description(integration_dir),
                    })

    def _scan_capabilities(self):
        """Scan all skills/capabilities."""
        caps_dir = self.root_dir / "2-engine" / "02-agents" / "capabilities"

        if caps_dir.exists():
            for cat_dir in caps_dir.iterdir():
                if cat_dir.is_dir() and not cat_dir.name.startswith('_'):
                    self._scan_capability_category(cat_dir)

    def _scan_capability_category(self, category_dir: Path):
        """Scan a capability category."""
        category = category_dir.name

        for md_file in category_dir.glob("*.md"):
            if md_file.name.startswith('_'):
                continue

            self.catalog_data["capabilities"].append({
                "name": md_file.stem,
                "category": category,
                "location": str(md_file.relative_to(self.root_dir)),
                "description": "",
            })

    def _scan_knowledge(self):
        """Scan knowledge systems."""
        knowledge_dir = self.root_dir / "2-engine" / "03-knowledge"

        if knowledge_dir.exists():
            for item in knowledge_dir.iterdir():
                if item.is_dir() and not item.name.startswith('_'):
                    self.catalog_data["knowledge"].append({
                        "name": item.name,
                        "location": str(item.relative_to(self.root_dir)),
                        "description": self._get_directory_description(item),
                    })

    def _scan_operations(self):
        """Scan operations and runtime systems."""
        ops_dir = self.root_dir / "2-engine" / "07-operations"

        if ops_dir.exists():
            for item in ops_dir.iterdir():
                if item.is_dir() and not item.name.startswith('_'):
                    self.catalog_data["operations"].append({
                        "name": item.name,
                        "location": str(item.relative_to(self.root_dir)),
                        "description": self._get_directory_description(item),
                    })

    def _get_directory_description(self, dir_path: Path) -> str:
        """Get description from README if available."""
        readme = dir_path / "README.md"
        if readme.exists():
            try:
                with open(readme, 'r') as f:
                    lines = f.readlines()
                    # Get first non-empty line after title
                    for line in lines[2:10]:  # Skip title
                        line = line.strip()
                        if line and not line.startswith('#'):
                            return line[:100]
            except (IOError, OSError) as e:
                logger.debug(f"Could not read README {readme}: {e}")
            except UnicodeDecodeError as e:
                logger.debug(f"Could not decode README {readme}: {e}")
        return ""

    def _build_directory_map(self):
        """Build a map of all major directories."""
        key_dirs = [
            "01-core",
            "2-engine",
            "3-gui",
            "5-project-memory",
            "6-roadmap",
        ]

        for dir_name in key_dirs:
            dir_path = self.root_dir / dir_name
            if dir_path.exists():
                self.catalog_data["directories"][dir_name] = {
                    "location": str(dir_path.relative_to(self.root_dir)),
                    "description": self._get_directory_description(dir_path),
                }

    def generate_markdown(self) -> str:
        """Generate the CATALOG.md markdown content."""
        data = self.catalog_data

        md = f"""---
catalog_type: blackbox5_universal_index
version: 5.0.0
generated: {datetime.now().isoformat()}
total_agents: {len(data['agents'])}
total_tools: {len(data['tools'])}
total_integrations: {len(data['integrations'])}
---

# BLACKBOX5 Universal Catalog

> The master index of all BLACKBOX5 components. This file makes every agent, tool, integration, and capability discoverable with minimal context.

## 📊 Quick Stats

| Category | Count |
|----------|-------|
| **Agents** | {len(data['agents'])} |
| **Tools** | {len(data['tools'])} |
| **Integrations** | {len(data['integrations'])} |
| **Capabilities** | {len(data['capabilities'])} |
| **Knowledge Systems** | {len(data['knowledge'])} |
| **Operations** | {len(data['operations'])} |

---

## 🤖 AGENTS ({len(data['agents'])})

### Core Agents ({len([a for a in data['agents'] if a.get('category') == 'core'])})
"""

        # Core agents
        for agent in [a for a in data['agents'] if a.get('category') == 'core']:
            md += f"""
**{agent['name']}**
- **Location:** `{agent['location']}`
- **Description:** {agent.get('description', 'No description')[:100]}...
"""

        # Specialist agents
        specialists = [a for a in data['agents'] if a.get('category') == 'specialist']
        md += f"\n### Specialist Agents ({len(specialists)})\n\n"

        for agent in specialists:
            md += f"""
**{agent.get('name', agent.get('title', agent['name']))}**
- **ID:** `{agent.get('id', 'N/A')}`
- **Role:** {agent.get('role', 'Specialist')}
- **Location:** `{agent['location']}`
- **Description:** {agent.get('description', 'No description')[:100]}...
"""

        # Tools
        md += f"\n---\n\n## 🛠️ TOOLS ({len(data['tools'])})\n\n"

        tools_by_category = {}
        for tool in data['tools']:
            cat = tool.get('category', 'other')
            if cat not in tools_by_category:
                tools_by_category[cat] = []
            tools_by_category[cat].append(tool)

        for category, tools in sorted(tools_by_category.items()):
            md += f"### {category.title()} ({len(tools)})\n\n"
            for tool in tools[:5]:  # Limit to first 5
                md += f"- **{tool['name']}** - `{tool['location']}`\n"
            if len(tools) > 5:
                md += f"- _... and {len(tools) - 5} more_\n"
            md += "\n"

        # Integrations
        md += f"---\n\n## 🔌 INTEGRATIONS ({len(data['integrations'])})\n\n"
        for integration in data['integrations']:
            md += f"- **{integration['name']}** - `{integration['location']}`\n"

        # Directory structure
        md += f"\n---\n\n## 📁 DIRECTORY STRUCTURE\n\n"
        for name, info in data['directories'].items():
            md += f"- **{name}** - `{info['location']}` - {info.get('description', '')}\n"

        # Search index
        md += """

---

## 🔍 SEARCH INDEX

Quick keyword lookup for common searches:

| Want to find... | Look in... |
|----------------|------------|
| Start Blackbox5 | `start.sh`, `blackbox.py` |
| All agents | `2-engine/01-core/agents/` |
| API server | `2-engine/01-core/interface/api/main.py` |
| Vibe Kanban | `3-gui/vibe-kanban/` |
| Tools | `2-engine/05-tools/` |
| Integrations | `2-engine/06-integrations/` |
| Agent capabilities | `2-engine/02-agents/capabilities/` |
| Knowledge systems | `2-engine/03-knowledge/` |
| Runtime operations | `2-engine/07-operations/` |
| Project memory | `5-project-memory/` |
| Roadmap | `6-roadmap/` |

---

## 💡 How AI Agents Use This Catalog

1. **Finding Components:** Read the relevant section to get exact file paths
2. **Understanding Structure:** Check DIRECTORY STRUCTURE for overview
3. **Locating Functions:** Use SEARCH INDEX for quick lookups
4. **Agent Selection:** Review AGENTS section to pick the right agent

---

## 🔄 Updating This Catalog

This catalog is auto-generated by `scripts/generate_catalog.py`. To update:

```bash
python scripts/generate_catalog.py > CATALOG.md
```

Always regenerate after:
- Adding new agents
- Adding new tools
- Restructuring directories
- Major code changes

---

*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*BLACKBOX5 Version: 5.0.0*
"""
        return md

    def validate(self) -> List[str]:
        """Validate catalog completeness and return issues."""
        issues = []

        # Check for components without descriptions
        for agent in self.catalog_data['agents']:
            if not agent.get('description'):
                issues.append(f"⚠️  Agent {agent.get('name', 'unknown')} has no description")

        # Check for missing READMEs in key directories
        for dir_name, dir_info in self.catalog_data['directories'].items():
            readme_path = self.root_dir / dir_info['location'] / 'README.md'
            if not readme_path.exists():
                issues.append(f"⚠️  {dir_name}/README.md is missing")

        return issues


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate BLACKBOX5 catalog")
    parser.add_argument('--output', '-o', default='CATALOG.md', help='Output file')
    parser.add_argument('--validate', '-v', action='store_true', help='Validate catalog')
    args = parser.parse_args()

    # Generate catalog
    generator = CatalogGenerator()
    generator.scan()

    if args.validate:
        print("\n🔍 Validating catalog...\n")
        issues = generator.validate()
        if issues:
            for issue in issues:
                print(issue)
        else:
            print("✅ Catalog is valid!")
        return

    # Generate markdown
    markdown = generator.generate_markdown()

    # Write output
    output_path = Path(args.output)
    output_path.write_text(markdown)

    print(f"✅ Catalog generated: {output_path}")
    print(f"   {len(generator.catalog_data['agents'])} agents")
    print(f"   {len(generator.catalog_data['tools'])} tools")
    print(f"   {len(generator.catalog_data['integrations'])} integrations")


if __name__ == '__main__':
    main()
