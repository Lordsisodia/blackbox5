#!/usr/bin/env python3
"""
Skill Usage Validation Script
BlackBox5 - Task Execution Validation

Purpose: Validate that skill checking was performed during task execution.
         Scans run folders to ensure Phase 1.5 (Skill Checking) was completed.

Usage:
    python validate-skill-usage.py [run_path]
    python validate-skill-usage.py --all
    python validate-skill-usage.py --latest
    python validate-skill-usage.py --task TASK-ID

Exit Codes:
    0 - All validations passed
    1 - Validation failed (skill checking not documented)
    2 - Invalid arguments or file not found
"""

import os
import sys
import re
import argparse
import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# Configuration
PROJECT_ROOT = Path("/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5")
RUNS_DIR = PROJECT_ROOT / "runs"
OPERATIONS_DIR = PROJECT_ROOT / "operations"
REQUIRED_SECTION = "## Skill Usage for This Task"
VALIDATION_VERSION = "1.0.0"

# Color codes for terminal output
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"


def print_success(message: str):
    print(f"{Colors.GREEN}✓{Colors.RESET} {message}")


def print_error(message: str):
    print(f"{Colors.RED}✗{Colors.RESET} {message}")


def print_warning(message: str):
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {message}")


def print_info(message: str):
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {message}")


def find_latest_run() -> Optional[Path]:
    """Find the most recent run folder."""
    if not RUNS_DIR.exists():
        return None

    run_folders = [
        d for d in RUNS_DIR.iterdir()
        if d.is_dir() and d.name.startswith("run-")
    ]

    if not run_folders:
        return None

    # Sort by folder name (timestamp is embedded)
    return max(run_folders, key=lambda p: p.name)


def find_runs_for_task(task_id: str) -> List[Path]:
    """Find all run folders associated with a specific task ID."""
    matching_runs = []

    if not RUNS_DIR.exists():
        return matching_runs

    for run_dir in RUNS_DIR.iterdir():
        if not run_dir.is_dir():
            continue

        # Check task-file.txt or other indicators
        task_file = run_dir / "task-file.txt"
        if task_file.exists():
            content = task_file.read_text()
            if task_id in content:
                matching_runs.append(run_dir)
                continue

        # Check THOUGHTS.md for task reference
        thoughts_file = run_dir / "THOUGHTS.md"
        if thoughts_file.exists():
            content = thoughts_file.read_text()
            if task_id in content:
                matching_runs.append(run_dir)

    return matching_runs


def get_all_runs() -> List[Path]:
    """Get all run folders sorted by date (newest first)."""
    if not RUNS_DIR.exists():
        return []

    run_folders = [
        d for d in RUNS_DIR.iterdir()
        if d.is_dir() and d.name.startswith("run-")
    ]

    return sorted(run_folders, key=lambda p: p.name, reverse=True)


def validate_thoughts_md(thoughts_path: Path) -> Tuple[bool, List[str]]:
    """
    Validate THOUGHTS.md contains proper skill usage documentation.

    Returns:
        Tuple of (is_valid, list of errors)
    """
    errors = []

    if not thoughts_path.exists():
        return False, ["THOUGHTS.md not found"]

    content = thoughts_path.read_text()

    # Check for required section header
    if REQUIRED_SECTION not in content:
        errors.append(f"Missing required section: '{REQUIRED_SECTION}'")
        return False, errors

    # Extract the skill usage section
    section_match = re.search(
        rf'{REQUIRED_SECTION}(.*?)(?=## |\Z)',
        content,
        re.DOTALL | re.IGNORECASE
    )

    if not section_match:
        errors.append("Could not parse skill usage section")
        return False, errors

    section_content = section_match.group(1)

    # Check for required fields
    required_fields = [
        ("Applicable skills", r'\*\*Applicable skills:\*\*'),
        ("Skill invoked", r'\*\*Skill invoked:\*\*'),
        ("Confidence", r'\*\*Confidence:\*\*'),
        ("Rationale", r'\*\*Rationale:\*\*'),
    ]

    for field_name, pattern in required_fields:
        if not re.search(pattern, section_content):
            errors.append(f"Missing field: '{field_name}'")

    # Check if skill-selection.yaml was referenced
    if "skill-selection.yaml" not in content:
        errors.append("No reference to skill-selection.yaml")

    # Validate confidence format if present
    confidence_match = re.search(r'\*\*Confidence:\*\*\s*(\d+)%?', section_content)
    if confidence_match:
        confidence = int(confidence_match.group(1))
        if confidence < 0 or confidence > 100:
            errors.append(f"Invalid confidence value: {confidence}%")

    is_valid = len(errors) == 0
    return is_valid, errors


def validate_skill_selection_yaml() -> Tuple[bool, List[str]]:
    """
    Validate that skill-selection.yaml exists and is properly formatted.

    Returns:
        Tuple of (is_valid, list of errors)
    """
    errors = []
    yaml_path = OPERATIONS_DIR / "skill-selection.yaml"

    if not yaml_path.exists():
        return False, ["skill-selection.yaml not found in operations/"]

    try:
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)

        # Check for required sections
        required_sections = [
            'auto_trigger_rules',
            'domain_mapping',
            'selection_process',
            'confidence_calculation',
        ]

        for section in required_sections:
            if section not in data:
                errors.append(f"Missing section in skill-selection.yaml: {section}")

        # Validate auto_trigger_rules
        if 'auto_trigger_rules' in data:
            rules = data['auto_trigger_rules']
            if not rules:
                errors.append("auto_trigger_rules section is empty")
            else:
                for i, rule in enumerate(rules):
                    if 'rule_id' not in rule:
                        errors.append(f"Rule {i+1} missing rule_id")
                    if 'keywords' not in rule and 'indicators' not in rule:
                        errors.append(f"Rule {i+1} missing keywords or indicators")

    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML in skill-selection.yaml: {e}")
    except Exception as e:
        errors.append(f"Error reading skill-selection.yaml: {e}")

    is_valid = len(errors) == 0
    return is_valid, errors


def validate_run(run_path: Path, verbose: bool = False) -> Dict:
    """
    Validate a single run folder.

    Returns:
        Dictionary with validation results
    """
    result = {
        "run_path": str(run_path),
        "run_name": run_path.name,
        "valid": True,
        "errors": [],
        "warnings": [],
        "checks_performed": [],
    }

    # Check THOUGHTS.md
    thoughts_path = run_path / "THOUGHTS.md"
    if thoughts_path.exists():
        result["checks_performed"].append("THOUGHTS.md found")
        is_valid, errors = validate_thoughts_md(thoughts_path)
        if not is_valid:
            result["valid"] = False
            result["errors"].extend(errors)
        else:
            result["checks_performed"].append("Skill usage section valid")
    else:
        result["valid"] = False
        result["errors"].append("THOUGHTS.md not found")

    # Check for RESULTS.md
    results_path = run_path / "RESULTS.md"
    if results_path.exists():
        result["checks_performed"].append("RESULTS.md found")
    else:
        result["warnings"].append("RESULTS.md not found")

    # Check for DECISIONS.md
    decisions_path = run_path / "DECISIONS.md"
    if decisions_path.exists():
        result["checks_performed"].append("DECISIONS.md found")

    return result


def print_validation_report(results: List[Dict], summary_only: bool = False):
    """Print a formatted validation report."""
    total = len(results)
    passed = sum(1 for r in results if r["valid"])
    failed = total - passed

    print("\n" + "=" * 70)
    print(f"SKILL USAGE VALIDATION REPORT v{VALIDATION_VERSION}")
    print("=" * 70)
    print(f"Total runs checked: {total}")
    print_success(f"Passed: {passed}")
    if failed > 0:
        print_error(f"Failed: {failed}")
    print("=" * 70)

    if summary_only:
        return

    for result in results:
        print(f"\n📁 {result['run_name']}")
        print(f"   Path: {result['run_path']}")

        if result["valid"]:
            print_success("   Status: PASSED")
        else:
            print_error("   Status: FAILED")

        if result["checks_performed"] and not summary_only:
            for check in result["checks_performed"]:
                print(f"   ✓ {check}")

        if result["errors"]:
            for error in result["errors"]:
                print_error(f"   Error: {error}")

        if result["warnings"]:
            for warning in result["warnings"]:
                print_warning(f"   Warning: {warning}")

    print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Validate skill usage documentation in run folders",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s                          # Validate latest run
    %(prog)s --all                    # Validate all runs
    %(prog)s --latest                 # Validate latest run (explicit)
    %(prog)s --task TASK-001          # Validate runs for specific task
    %(prog)s runs/run-20260205-120000 # Validate specific run
    %(prog)s --summary                # Show summary only
        """
    )

    parser.add_argument(
        "run_path",
        nargs="?",
        help="Path to specific run folder to validate"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Validate all run folders"
    )
    parser.add_argument(
        "--latest", "-l",
        action="store_true",
        help="Validate the most recent run (default behavior)"
    )
    parser.add_argument(
        "--task", "-t",
        metavar="TASK-ID",
        help="Validate runs associated with specific task ID"
    )
    parser.add_argument(
        "--summary", "-s",
        action="store_true",
        help="Show summary only, skip detailed output"
    )
    parser.add_argument(
        "--check-framework",
        action="store_true",
        help="Validate skill-selection.yaml framework file"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()

    # Validate framework if requested
    if args.check_framework:
        print_info("Validating skill-selection.yaml framework...")
        is_valid, errors = validate_skill_selection_yaml()
        if is_valid:
            print_success("skill-selection.yaml is valid")
            return 0
        else:
            print_error("skill-selection.yaml has errors:")
            for error in errors:
                print_error(f"  - {error}")
            return 1

    # Determine which runs to validate
    runs_to_validate = []

    if args.run_path:
        run_path = Path(args.run_path)
        if not run_path.exists():
            print_error(f"Run path not found: {run_path}")
            return 2
        runs_to_validate.append(run_path)

    elif args.all:
        runs_to_validate = get_all_runs()
        if not runs_to_validate:
            print_warning("No run folders found")
            return 0

    elif args.task:
        runs_to_validate = find_runs_for_task(args.task)
        if not runs_to_validate:
            print_warning(f"No runs found for task: {args.task}")
            return 0
        print_info(f"Found {len(runs_to_validate)} run(s) for task {args.task}")

    else:
        # Default: validate latest run
        latest = find_latest_run()
        if not latest:
            print_warning("No run folders found")
            return 0
        runs_to_validate.append(latest)

    # Validate each run
    results = []
    for run_path in runs_to_validate:
        if args.verbose:
            print_info(f"Validating {run_path.name}...")
        result = validate_run(run_path, verbose=args.verbose)
        results.append(result)

    # Print report
    print_validation_report(results, summary_only=args.summary)

    # Return appropriate exit code
    failed_count = sum(1 for r in results if not r["valid"])
    return 1 if failed_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
