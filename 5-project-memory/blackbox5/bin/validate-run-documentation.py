#!/usr/bin/env python3
"""
Run Documentation Validation Script
BlackBox5 - Ensures run folder documentation is properly populated

Purpose: Validate that run folder documentation files (THOUGHTS.md, LEARNINGS.md,
         DECISIONS.md, RESULTS.md) contain meaningful content and are not just
         unfilled templates.

Usage:
    python validate-run-documentation.py [run_path]
    python validate-run-documentation.py --all
    python validate-run-documentation.py --latest
    python validate-run-documentation.py --check-config

Exit Codes:
    0 - All validations passed (or mode is "warn")
    1 - Validation failed and mode is "block" or "strict"
    2 - Invalid arguments or configuration error
"""

import os
import sys
import re
import json
import argparse
import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any

# Configuration
PROJECT_ROOT = Path("/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5")
RUNS_DIR = PROJECT_ROOT / "runs"
OPERATIONS_DIR = PROJECT_ROOT / "operations"
CONFIG_FILE = OPERATIONS_DIR / "run-validation.yaml"
VALIDATION_VERSION = "1.0.0"

# Color codes for terminal output
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"


def print_success(message: str):
    print(f"{Colors.GREEN}✓{Colors.RESET} {message}")


def print_error(message: str):
    print(f"{Colors.RED}✗{Colors.RESET} {message}")


def print_warning(message: str):
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {message}")


def print_info(message: str):
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {message}")


def print_header(message: str):
    print(f"{Colors.CYAN}{message}{Colors.RESET}")


def load_config() -> Optional[Dict]:
    """Load validation configuration from YAML file."""
    if not CONFIG_FILE.exists():
        return None

    try:
        with open(CONFIG_FILE, 'r') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        print_error(f"Invalid YAML in config file: {e}")
        return None
    except Exception as e:
        print_error(f"Error reading config file: {e}")
        return None


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


def get_all_runs() -> List[Path]:
    """Get all run folders sorted by date (newest first)."""
    if not RUNS_DIR.exists():
        return []

    run_folders = [
        d for d in RUNS_DIR.iterdir()
        if d.is_dir() and d.name.startswith("run-")
    ]

    return sorted(run_folders, key=lambda p: p.name, reverse=True)


def count_sections(content: str) -> int:
    """Count the number of markdown sections (## headers)."""
    return len(re.findall(r'^##\s+', content, re.MULTILINE))


def find_template_placeholders(content: str, forbidden_patterns: List[str]) -> List[str]:
    """Find template placeholders that haven't been replaced."""
    found = []
    for pattern in forbidden_patterns:
        # Escape special regex characters in the pattern
        escaped_pattern = re.escape(pattern)
        if re.search(escaped_pattern, content):
            found.append(pattern)
    return found


def validate_file(file_path: Path, config: Dict, file_name: str) -> Dict:
    """
    Validate a single documentation file.

    Returns:
        Dictionary with validation results
    """
    result = {
        "file_name": file_name,
        "file_path": str(file_path),
        "exists": False,
        "valid": True,
        "errors": [],
        "warnings": [],
        "stats": {
            "char_count": 0,
            "section_count": 0,
            "line_count": 0,
        }
    }

    # Get thresholds for this file
    thresholds = config.get("thresholds", {}).get(file_name, {})
    if not thresholds:
        result["warnings"].append(f"No thresholds defined for {file_name}")
        return result

    # Check if file is optional
    is_optional = thresholds.get("optional", False)

    # Check if file exists
    if not file_path.exists():
        result["exists"] = False
        if is_optional:
            result["warnings"].append(f"Optional file {file_name} not found")
        else:
            result["valid"] = False
            result["errors"].append(f"Required file {file_name} not found")
        return result

    result["exists"] = True

    # Read file content
    try:
        content = file_path.read_text()
    except Exception as e:
        result["valid"] = False
        result["errors"].append(f"Error reading file: {e}")
        return result

    # Calculate stats
    result["stats"]["char_count"] = len(content)
    result["stats"]["line_count"] = len(content.splitlines())
    result["stats"]["section_count"] = count_sections(content)

    # Check minimum character count
    min_chars = thresholds.get("min_chars", 0)
    if result["stats"]["char_count"] < min_chars:
        severity = config.get("severity", {}).get("insufficient_content", "warning")
        msg = f"Content too short: {result['stats']['char_count']} chars (min: {min_chars})"
        if severity == "error":
            result["valid"] = False
            result["errors"].append(msg)
        else:
            result["warnings"].append(msg)

    # Check minimum sections
    min_sections = thresholds.get("min_sections", 0)
    if result["stats"]["section_count"] < min_sections:
        severity = config.get("severity", {}).get("missing_sections", "warning")
        msg = f"Too few sections: {result['stats']['section_count']} (min: {min_sections})"
        if severity == "error":
            result["valid"] = False
            result["errors"].append(msg)
        else:
            result["warnings"].append(msg)

    # Check required headers
    required_headers = thresholds.get("required_headers", [])
    for header in required_headers:
        if header not in content:
            result["warnings"].append(f"Missing required header: {header}")

    # Check for template placeholders
    forbidden_patterns = thresholds.get("forbidden_patterns", [])
    placeholders = find_template_placeholders(content, forbidden_patterns)
    if placeholders:
        severity = config.get("severity", {}).get("template_placeholders", "error")
        for placeholder in placeholders[:3]:  # Limit to first 3
            msg = f"Template placeholder found: {placeholder[:50]}..."
            if severity == "error":
                result["valid"] = False
                result["errors"].append(msg)
            else:
                result["warnings"].append(msg)
        if len(placeholders) > 3:
            remaining = len(placeholders) - 3
            result["warnings"].append(f"... and {remaining} more placeholders")

    return result


def validate_run(run_path: Path, config: Dict, verbose: bool = False) -> Dict:
    """
    Validate all documentation files in a run folder.

    Returns:
        Dictionary with complete validation results
    """
    result = {
        "run_path": str(run_path),
        "run_name": run_path.name,
        "valid": True,
        "files": {},
        "errors": [],
        "warnings": [],
        "summary": {
            "total_files": 0,
            "valid_files": 0,
            "invalid_files": 0,
            "missing_files": 0,
        }
    }

    # Files to validate
    files_to_check = [
        "THOUGHTS.md",
        "LEARNINGS.md",
        "DECISIONS.md",
        "RESULTS.md",
        "ASSUMPTIONS.md",
    ]

    for file_name in files_to_check:
        file_path = run_path / file_name
        file_result = validate_file(file_path, config, file_name)
        result["files"][file_name] = file_result

        # Update summary
        if file_result["exists"]:
            result["summary"]["total_files"] += 1
            if file_result["valid"]:
                result["summary"]["valid_files"] += 1
            else:
                result["summary"]["invalid_files"] += 1
                result["valid"] = False
        else:
            # Check if file is optional
            thresholds = config.get("thresholds", {}).get(file_name, {})
            if not thresholds.get("optional", False):
                result["summary"]["missing_files"] += 1
                result["valid"] = False

        # Collect errors and warnings
        result["errors"].extend(file_result["errors"])
        result["warnings"].extend(file_result["warnings"])

    return result


def print_validation_report(results: List[Dict], config: Dict, summary_only: bool = False):
    """Print a formatted validation report."""
    total = len(results)
    passed = sum(1 for r in results if r["valid"])
    failed = total - passed

    print("\n" + "=" * 70)
    print_header(f"RUN DOCUMENTATION VALIDATION REPORT v{VALIDATION_VERSION}")
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

        # Print file details
        for file_name, file_result in result["files"].items():
            if not file_result["exists"]:
                if file_result.get("errors"):
                    print_error(f"   {file_name}: MISSING")
                else:
                    print_warning(f"   {file_name}: MISSING (optional)")
                continue

            stats = file_result["stats"]
            status_icon = "✓" if file_result["valid"] else "✗"
            color = Colors.GREEN if file_result["valid"] else Colors.RED

            print(f"   {color}{status_icon}{Colors.RESET} {file_name}: "
                  f"{stats['char_count']} chars, {stats['section_count']} sections")

            # Print errors and warnings
            max_errors = config.get("output", {}).get("max_errors_per_file", 5)

            if file_result["errors"] and not summary_only:
                for error in file_result["errors"][:max_errors]:
                    print_error(f"      Error: {error}")
                if len(file_result["errors"]) > max_errors:
                    remaining = len(file_result["errors"]) - max_errors
                    print_error(f"      ... and {remaining} more errors")

            if file_result["warnings"] and not summary_only:
                for warning in file_result["warnings"][:max_errors]:
                    print_warning(f"      Warning: {warning}")
                if len(file_result["warnings"]) > max_errors:
                    remaining = len(file_result["warnings"]) - max_errors
                    print_warning(f"      ... and {remaining} more warnings")

    print("\n" + "=" * 70)


def save_validation_report(result: Dict, run_path: Path, config: Dict):
    """Save validation report to JSON file in run folder."""
    if not config.get("integration", {}).get("create_report", True):
        return

    report_filename = config.get("integration", {}).get("report_filename", "validation-report.json")
    report_path = run_path / report_filename

    report = {
        "validation_version": VALIDATION_VERSION,
        "timestamp": datetime.now().isoformat(),
        "run_name": result["run_name"],
        "valid": result["valid"],
        "summary": result["summary"],
        "files": {}
    }

    # Include file results (without full error lists to keep it concise)
    for file_name, file_result in result["files"].items():
        report["files"][file_name] = {
            "exists": file_result["exists"],
            "valid": file_result["valid"],
            "stats": file_result["stats"],
            "error_count": len(file_result["errors"]),
            "warning_count": len(file_result["warnings"]),
        }

    try:
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        print_info(f"Validation report saved to: {report_path}")
    except Exception as e:
        print_warning(f"Could not save validation report: {e}")


def check_bypass() -> bool:
    """Check if validation should be bypassed via environment variable."""
    bypass_var = "BB5_SKIP_RUN_VALIDATION"
    return os.environ.get(bypass_var, "").lower() in ("1", "true", "yes")


def validate_config(config: Dict) -> Tuple[bool, List[str]]:
    """Validate the configuration file structure."""
    errors = []

    if not config:
        errors.append("Configuration is empty")
        return False, errors

    # Check required top-level sections
    if "validation" not in config:
        errors.append("Missing 'validation' section")

    if "thresholds" not in config:
        errors.append("Missing 'thresholds' section")
    else:
        thresholds = config["thresholds"]
        required_files = ["THOUGHTS.md", "LEARNINGS.md", "DECISIONS.md", "RESULTS.md"]
        for file_name in required_files:
            if file_name not in thresholds:
                errors.append(f"Missing thresholds for {file_name}")

    if "severity" not in config:
        errors.append("Missing 'severity' section")

    return len(errors) == 0, errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate run folder documentation is properly populated",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s                          # Validate latest run
    %(prog)s --all                    # Validate all runs
    %(prog)s --latest                 # Validate latest run (explicit)
    %(prog)s runs/run-20260205-120000 # Validate specific run
    %(prog)s --check-config           # Validate configuration file
    %(prog)s --summary                # Show summary only

Environment Variables:
    BB5_SKIP_RUN_VALIDATION=1         # Bypass validation (if enabled in config)
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
        "--check-config", "-c",
        action="store_true",
        help="Validate the configuration file"
    )
    parser.add_argument(
        "--summary", "-s",
        action="store_true",
        help="Show summary only, skip detailed output"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colorized output"
    )

    args = parser.parse_args()

    # Disable colors if requested
    if args.no_color:
        global Colors
        for attr in dir(Colors):
            if not attr.startswith('_'):
                setattr(Colors, attr, "")

    # Load configuration
    config = load_config()
    if not config:
        print_error(f"Could not load configuration from {CONFIG_FILE}")
        return 2

    # Validate configuration if requested
    if args.check_config:
        print_info("Validating configuration file...")
        is_valid, errors = validate_config(config)
        if is_valid:
            print_success("Configuration is valid")
            mode = config.get("validation", {}).get("mode", "warn")
            print_info(f"Validation mode: {mode}")
            return 0
        else:
            print_error("Configuration has errors:")
            for error in errors:
                print_error(f"  - {error}")
            return 2

    # Check for bypass
    if check_bypass():
        print_warning("Validation bypassed via BB5_SKIP_RUN_VALIDATION")
        return 0

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
        result = validate_run(run_path, config, verbose=args.verbose)
        results.append(result)

        # Save validation report for each run
        save_validation_report(result, run_path, config)

    # Print report
    print_validation_report(results, config, summary_only=args.summary)

    # Determine exit code based on mode
    mode = config.get("validation", {}).get("mode", "warn")
    exit_codes = config.get("exit_codes", {}).get(mode, {})

    failed_count = sum(1 for r in results if not r["valid"])

    if failed_count > 0:
        exit_code = exit_codes.get("validation_failed", 0)
        if exit_code != 0:
            print_error(f"Validation failed. Mode: {mode}. Blocking session end.")
        else:
            print_warning(f"Validation issues found. Mode: {mode}. Warnings only.")
        return exit_code
    else:
        print_success("All validations passed!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
