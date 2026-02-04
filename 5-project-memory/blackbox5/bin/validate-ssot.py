#!/usr/bin/env python3
"""
SSOT Validation Script

Validates that STATE.yaml references exist and are consistent with canonical sources.
Run this after any structural changes to catch SSOT violations early.
"""

import yaml
import os
import sys
from pathlib import Path
from typing import List, Tuple

# Colors for output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

class SSOTValidator:
    def __init__(self, project_root: str):
        self.root = Path(project_root)
        self.errors: List[Tuple[str, str]] = []
        self.warnings: List[Tuple[str, str]] = []

    def load_yaml(self, path: Path) -> dict:
        """Load YAML file, return empty dict if missing."""
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            return {}
        except yaml.YAMLError as e:
            self.errors.append((str(path), f"YAML parse error: {e}"))
            return {}

    def validate_state_yaml(self) -> bool:
        """Validate STATE.yaml references."""
        print("\n📋 Validating STATE.yaml...")

        state_path = self.root / "STATE.yaml"
        if not state_path.exists():
            self.errors.append(("STATE.yaml", "File does not exist"))
            return False

        state = self.load_yaml(state_path)

        # Check root_files references
        root_files = state.get('root_files', {})
        for key, info in root_files.items():
            if isinstance(info, dict) and 'file' in info:
                file_path = self.root / info['file']
                if not file_path.exists():
                    self.errors.append(
                        (f"STATE.yaml:root_files.{key}",
                         f"References {info['file']} which does not exist")
                    )

        # Check project/context.yaml exists
        context_path = self.root / "project" / "context.yaml"
        if not context_path.exists():
            self.errors.append(("Project context", "project/context.yaml missing"))
        else:
            # Validate version consistency
            context = self.load_yaml(context_path)
            state_version = state.get('project', {}).get('version')
            context_version = context.get('project', {}).get('version')

            if state_version and context_version and state_version != context_version:
                self.warnings.append(
                    ("Version mismatch",
                     f"STATE.yaml:{state_version} vs context.yaml:{context_version}")
                )

        print(f"  {GREEN}✓{RESET} STATE.yaml structure valid" if not self.errors else f"  {RED}✗{RESET} Issues found")
        return len(self.errors) == 0

    def validate_decisions(self) -> bool:
        """Validate decisions are in decisions/ folder, not just STATE.yaml."""
        print("\n📋 Validating decisions...")

        state_path = self.root / "STATE.yaml"
        state = self.load_yaml(state_path)

        # Get decisions listed in STATE.yaml
        state_decisions = state.get('decisions', {})
        state_arch_decisions = state_decisions.get('architectural', [])

        # Check they exist in decisions/architectural/
        decisions_dir = self.root / "decisions" / "architectural"
        if decisions_dir.exists():
            existing_decisions = list(decisions_dir.glob("DEC-*.md"))
            existing_ids = {d.stem for d in existing_decisions}

            for dec in state_arch_decisions:
                dec_id = dec.get('id', '')
                if dec_id and dec_id not in existing_ids:
                    self.warnings.append(
                        (f"Decision {dec_id}",
                         "Listed in STATE.yaml but no file in decisions/architectural/")
                    )

        print(f"  {GREEN}✓{RESET} Decisions valid" if not self.warnings else f"  {YELLOW}⚠{RESET} Warnings found")
        return True

    def validate_goals_tasks(self) -> bool:
        """Validate goals and tasks cross-references."""
        print("\n📋 Validating goals and tasks...")

        goals_dir = self.root / "goals" / "active"
        tasks_dir = self.root / "tasks" / "active"

        # Check goals reference existing tasks
        if goals_dir.exists():
            for goal_file in goals_dir.glob("*/goal.yaml"):
                goal = self.load_yaml(goal_file)
                sub_goals = goal.get('sub_goals', [])

                for sg in sub_goals:
                    linked_tasks = sg.get('linked_tasks', [])
                    for task_id in linked_tasks:
                        task_path = tasks_dir / task_id / "task.md"
                        if not task_path.exists():
                            self.errors.append(
                                (f"Goal {goal_file.parent.name}",
                                 f"References task {task_id} which does not exist")
                            )

        print(f"  {GREEN}✓{RESET} Goals/tasks valid" if not self.errors else f"  {RED}✗{RESET} Issues found")
        return len(self.errors) == 0

    def validate_ralf_context(self) -> bool:
        """Validate Ralf-context.md can be generated from sources."""
        print("\n📋 Validating Ralf-context.md...")

        ralf_context_path = self.root / "Ralf-context.md"
        if not ralf_context_path.exists():
            self.warnings.append(
                ("Ralf-context.md", "File missing - needed for RALF loop")
            )

        print(f"  {GREEN}✓{RESET} Ralf-context.md valid" if not self.warnings else f"  {YELLOW}⚠{RESET} Warnings found")
        return True

    def run_all_validations(self) -> bool:
        """Run all validations and report results."""
        print("\n" + "="*60)
        print("🔍 SSOT VALIDATION")
        print("="*60)

        self.validate_state_yaml()
        self.validate_decisions()
        self.validate_goals_tasks()
        self.validate_ralf_context()

        # Report results
        print("\n" + "="*60)
        print("📊 RESULTS")
        print("="*60)

        if self.errors:
            print(f"\n{RED}❌ ERRORS ({len(self.errors)}):{RESET}")
            for location, message in self.errors:
                print(f"  {RED}•{RESET} {location}")
                print(f"    {message}")

        if self.warnings:
            print(f"\n{YELLOW}⚠️  WARNINGS ({len(self.warnings)}):{RESET}")
            for location, message in self.warnings:
                print(f"  {YELLOW}•{RESET} {location}")
                print(f"    {message}")

        if not self.errors and not self.warnings:
            print(f"\n{GREEN}✅ All validations passed!{RESET}")
            return True
        elif not self.errors:
            print(f"\n{YELLOW}⚠️  Validation passed with warnings{RESET}")
            return True
        else:
            print(f"\n{RED}❌ Validation failed{RESET}")
            return False


def main():
    # Find project root (where STATE.yaml exists)
    current_dir = Path.cwd()
    project_root = current_dir

    # Walk up until we find STATE.yaml or hit root
    while not (project_root / "STATE.yaml").exists() and project_root.parent != project_root:
        project_root = project_root.parent

    if not (project_root / "STATE.yaml").exists():
        print(f"{RED}Error:{RESET} Could not find STATE.yaml in current or parent directories")
        sys.exit(1)

    print(f"📁 Project root: {project_root}")

    validator = SSOTValidator(project_root)
    success = validator.run_all_validations()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
