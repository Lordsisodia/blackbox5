# Superintelligence Protocol CLI

A professional-grade command-line interface for orchestrating AI-driven development workflows.

## Overview

The Superintelligence CLI (`superintelligence` or `si`) provides developers with a powerful interface to interact with the Superintelligence Protocol - enabling task execution, project scanning, context management, and autonomous development workflows.

## Installation

### Quick Install

```bash
# Install from PyPI (when published)
pip install superintelligence-protocol

# Or install from source
git clone https://github.com/siso-ecosystem/superintelligence-protocol.git
cd superintelligence-protocol
pip install -e .
```

### Development Install

```bash
# Clone the repository
git clone https://github.com/siso-ecosystem/superintelligence-protocol.git
cd superintelligence-protocol

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Shell Completion

```bash
# Bash
superintelligence --install-completion bash

# Zsh
superintelligence --install-completion zsh

# Fish
superintelligence --install-completion fish
```

## Command Structure

```
superintelligence [GLOBAL_OPTIONS] <COMMAND> [COMMAND_OPTIONS] [ARGS]
```

### Global Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--config` | `-c` | Path to configuration file | `~/.superintelligence/config.yaml` |
| `--verbose` | `-v` | Enable verbose output | `false` |
| `--quiet` | `-q` | Suppress non-error output | `false` |
| `--format` | `-f` | Output format (json, yaml, human) | `human` |
| `--version` | `-V` | Show version information | - |
| `--help` | `-h` | Show help message | - |

### Commands

| Command | Description | Alias |
|---------|-------------|-------|
| `run` | Execute a task with the Superintelligence Protocol | `r` |
| `scan` | Scan and analyze project structure | `s` |
| `context` | Manage project contexts | `ctx` |
| `activate` | Activate autonomous mode | `auto` |
| `status` | Check system status and health | `st` |
| `config` | Manage configuration settings | `cfg` |
| `logs` | View execution logs | `log` |
| `history` | View task history | `hist` |

## Usage Examples

### Basic Task Execution

```bash
# Simple task execution
superintelligence "Refactor the authentication module to use JWT tokens"

# Task with explicit flag
superintelligence run --task "Optimize database queries"

# Multi-line task
superintelligence run --task "Create a user management system with:
- User registration and login
- Password reset functionality
- Role-based access control"
```

### Context-Aware Execution

```bash
# Execute with specific project context
superintelligence --task "Implement caching" --context "backend-api,redis-config"

# Use multiple contexts
superintelligence run \
  --task "Add payment processing" \
  --context "stripe-integration,billing-models,webhook-handlers" \
  --depth 5

# Auto-detect context from current directory
superintelligence run --task "Fix bug in user login" --auto-context
```

### Autonomous Mode

```bash
# Activate full autonomous mode
superintelligence activate --depth 7 --verbose

# Autonomous mode with constraints
superintelligence activate \
  --depth 5 \
  --max-iterations 50 \
  --budget 100 \
  --focus "security,performance"

# Autonomous mode with specific goal
superintelligence activate \
  --goal "Optimize application for production deployment" \
  --constraints "no-breaking-changes,test-coverage>80%"
```

### Project Scanning

```bash
# Quick scan of current directory
superintelligence scan

# Deep scan with specific depth
superintelligence scan --depth 5 --output scan-results.json

# Scan specific directory
superintelligence scan /path/to/project --format yaml

# Scan and generate context
superintelligence scan --generate-context --name "my-project-context"
```

### Context Management

```bash
# List available contexts
superintelligence context list

# Create new context from current directory
superintelligence context create --name "api-v2" --description "API version 2 development"

# Update context
superintelligence context update api-v2 --add-paths "src/api,tests/api"

# Delete context
superintelligence context delete api-v2

# Export context
superintelligence context export api-v2 --output api-v2-context.yaml

# Import context
superintelligence context import --file external-context.yaml
```

### Configuration Management

```bash
# View current configuration
superintelligence config show

# Set configuration value
superintelligence config set model.provider anthropic
superintelligence config set model.name claude-opus-4

# Get configuration value
superintelligence config get model.provider

# Edit configuration file
superintelligence config edit

# Reset to defaults
superintelligence config reset
```

### Monitoring and Logging

```bash
# Check system status
superintelligence status

# View recent logs
superintelligence logs --tail 50

# View logs for specific task
superintelligence logs --task-id task-12345

# View task history
superintelligence history --limit 20

# Export execution report
superintelligence history --export report.html
```

## Python Implementation

### Project Structure

```
superintelligence_protocol/
├── pyproject.toml
├── README.md
├── src/
│   └── superintelligence/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli/
│       │   ├── __init__.py
│       │   ├── main.py
│       │   ├── commands/
│       │   │   ├── __init__.py
│       │   │   ├── run.py
│       │   │   ├── scan.py
│       │   │   ├── context.py
│       │   │   ├── activate.py
│       │   │   ├── status.py
│       │   │   ├── config.py
│       │   │   ├── logs.py
│       │   │   └── history.py
│       │   ├── formatters/
│       │   │   ├── __init__.py
│       │   │   ├── json_formatter.py
│       │   │   ├── yaml_formatter.py
│       │   │   └── human_formatter.py
│       │   └── utils/
│       │       ├── __init__.py
│       │       ├── config.py
│       │       ├── progress.py
│       │       └── shell.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── protocol.py
│       │   ├── scanner.py
│       │   └── context.py
│       └── exceptions.py
└── tests/
    └── ...
```

### Core CLI Implementation

#### `src/superintelligence/__main__.py`

```python
"""Entry point for the Superintelligence Protocol CLI."""

import sys
from superintelligence.cli.main import main

if __name__ == "__main__":
    sys.exit(main())
```

#### `src/superintelligence/cli/main.py`

```python
"""Main CLI entry point and argument parsing."""

import argparse
import sys
import os
from pathlib import Path
from typing import List, Optional

from superintelligence import __version__
from superintelligence.cli.commands import (
    run_command,
    scan_command,
    context_command,
    activate_command,
    status_command,
    config_command,
    logs_command,
    history_command,
)
from superintelligence.cli.utils.config import load_config, get_default_config_path
from superintelligence.cli.formatters import get_formatter
from superintelligence.exceptions import SuperintelligenceError


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""

    parser = argparse.ArgumentParser(
        prog="superintelligence",
        description="Superintelligence Protocol - AI-driven development orchestration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  superintelligence "Refactor authentication module"
  superintelligence run --task "Optimize queries" --context backend
  superintelligence activate --depth 7 --verbose
  superintelligence scan --depth 5 --output results.json

For more information: https://docs.superintelligence.sh
        """
    )

    parser.add_argument(
        "--version", "-V",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    parser.add_argument(
        "--config", "-c",
        type=str,
        default=None,
        help="Path to configuration file (default: ~/.superintelligence/config.yaml)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="count",
        default=0,
        help="Enable verbose output (use -vv for very verbose)"
    )

    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress non-error output"
    )

    parser.add_argument(
        "--format", "-f",
        choices=["json", "yaml", "human"],
        default="human",
        help="Output format (default: human)"
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )

    # Install completion
    parser.add_argument(
        "--install-completion",
        choices=["bash", "zsh", "fish"],
        help="Install shell completion"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Run command (default when positional argument provided)
    run_parser = subparsers.add_parser(
        "run",
        aliases=["r"],
        help="Execute a task with the Superintelligence Protocol"
    )
    run_parser.add_argument(
        "task",
        nargs="?",
        help="Task description to execute"
    )
    run_parser.add_argument(
        "--task", "-t",
        dest="task_flag",
        help="Task description (alternative to positional arg)"
    )
    run_parser.add_argument(
        "--context", "-C",
        type=str,
        help="Comma-separated list of context names"
    )
    run_parser.add_argument(
        "--auto-context",
        action="store_true",
        help="Auto-detect context from current directory"
    )
    run_parser.add_argument(
        "--depth", "-d",
        type=int,
        default=3,
        help="Analysis depth level (1-10, default: 3)"
    )
    run_parser.add_argument(
        "--model",
        type=str,
        help="Override default model for this execution"
    )
    run_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be executed without running"
    )
    run_parser.add_argument(
        "--output", "-o",
        type=str,
        help="Save output to file"
    )
    run_parser.set_defaults(func=run_command)

    # Scan command
    scan_parser = subparsers.add_parser(
        "scan",
        aliases=["s"],
        help="Scan and analyze project structure"
    )
    scan_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to scan (default: current directory)"
    )
    scan_parser.add_argument(
        "--depth", "-d",
        type=int,
        default=3,
        help="Scan depth level (1-10, default: 3)"
    )
    scan_parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output file path"
    )
    scan_parser.add_argument(
        "--generate-context",
        action="store_true",
        help="Generate context from scan results"
    )
    scan_parser.add_argument(
        "--name", "-n",
        type=str,
        help="Name for generated context"
    )
    scan_parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Include hidden files and directories"
    )
    scan_parser.add_argument(
        "--exclude",
        type=str,
        action="append",
        help="Patterns to exclude (can be used multiple times)"
    )
    scan_parser.set_defaults(func=scan_command)

    # Context command
    context_parser = subparsers.add_parser(
        "context",
        aliases=["ctx"],
        help="Manage project contexts"
    )
    context_subparsers = context_parser.add_subparsers(dest="context_action")

    # Context list
    context_list = context_subparsers.add_parser("list", help="List available contexts")
    context_list.add_argument("--json", action="store_true", help="Output as JSON")

    # Context create
    context_create = context_subparsers.add_parser("create", help="Create new context")
    context_create.add_argument("--name", "-n", required=True, help="Context name")
    context_create.add_argument("--description", "-d", help="Context description")
    context_create.add_argument("--paths", "-p", nargs="+", help="Paths to include")

    # Context update
    context_update = context_subparsers.add_parser("update", help="Update context")
    context_update.add_argument("name", help="Context name")
    context_update.add_argument("--add-paths", nargs="+", help="Paths to add")
    context_update.add_argument("--remove-paths", nargs="+", help="Paths to remove")
    context_update.add_argument("--description", "-d", help="New description")

    # Context delete
    context_delete = context_subparsers.add_parser("delete", help="Delete context")
    context_delete.add_argument("name", help="Context name")
    context_delete.add_argument("--force", "-f", action="store_true", help="Skip confirmation")

    # Context export
    context_export = context_subparsers.add_parser("export", help="Export context")
    context_export.add_argument("name", help="Context name")
    context_export.add_argument("--output", "-o", help="Output file")

    # Context import
    context_import = context_subparsers.add_parser("import", help="Import context")
    context_import.add_argument("--file", "-f", required=True, help="File to import")
    context_import.add_argument("--name", "-n", help="Rename on import")

    context_parser.set_defaults(func=context_command)

    # Activate command (autonomous mode)
    activate_parser = subparsers.add_parser(
        "activate",
        aliases=["auto"],
        help="Activate autonomous development mode"
    )
    activate_parser.add_argument(
        "--goal", "-g",
        type=str,
        help="High-level goal for autonomous mode"
    )
    activate_parser.add_argument(
        "--depth", "-d",
        type=int,
        default=5,
        help="Autonomy depth level (1-10, default: 5)"
    )
    activate_parser.add_argument(
        "--max-iterations", "-i",
        type=int,
        default=100,
        help="Maximum number of iterations"
    )
    activate_parser.add_argument(
        "--budget", "-b",
        type=float,
        help="Token/execution budget limit"
    )
    activate_parser.add_argument(
        "--focus",
        type=str,
        help="Comma-separated focus areas (e.g., 'security,performance')"
    )
    activate_parser.add_argument(
        "--constraints",
        type=str,
        help="Comma-separated constraints"
    )
    activate_parser.add_argument(
        "--context", "-C",
        type=str,
        help="Context to use"
    )
    activate_parser.add_argument(
        "--checkpoint",
        action="store_true",
        help="Enable checkpointing for resume capability"
    )
    activate_parser.set_defaults(func=activate_command)

    # Status command
    status_parser = subparsers.add_parser(
        "status",
        aliases=["st"],
        help="Check system status and health"
    )
    status_parser.add_argument(
        "--full",
        action="store_true",
        help="Show detailed status"
    )
    status_parser.set_defaults(func=status_command)

    # Config command
    config_parser = subparsers.add_parser(
        "config",
        aliases=["cfg"],
        help="Manage configuration settings"
    )
    config_subparsers = config_parser.add_subparsers(dest="config_action")

    config_show = config_subparsers.add_parser("show", help="Show current configuration")
    config_show.add_argument("--path", action="store_true", help="Show config file path")

    config_set = config_subparsers.add_parser("set", help="Set configuration value")
    config_set.add_argument("key", help="Configuration key (dot notation)")
    config_set.add_argument("value", help="Value to set")

    config_get = config_subparsers.add_parser("get", help="Get configuration value")
    config_get.add_argument("key", help="Configuration key")

    config_edit = config_subparsers.add_parser("edit", help="Edit configuration file")
    config_edit.add_argument("--editor", help="Editor to use")

    config_reset = config_subparsers.add_parser("reset", help="Reset to defaults")
    config_reset.add_argument("--force", "-f", action="store_true", help="Skip confirmation")

    config_parser.set_defaults(func=config_command)

    # Logs command
    logs_parser = subparsers.add_parser(
        "logs",
        aliases=["log"],
        help="View execution logs"
    )
    logs_parser.add_argument(
        "--tail", "-n",
        type=int,
        default=50,
        help="Number of lines to show"
    )
    logs_parser.add_argument(
        "--follow", "-f",
        action="store_true",
        help="Follow log output"
    )
    logs_parser.add_argument(
        "--task-id",
        type=str,
        help="Filter by task ID"
    )
    logs_parser.add_argument(
        "--level",
        choices=["debug", "info", "warning", "error"],
        help="Filter by log level"
    )
    logs_parser.add_argument(
        "--since",
        type=str,
        help="Show logs since timestamp"
    )
    logs_parser.set_defaults(func=logs_command)

    # History command
    history_parser = subparsers.add_parser(
        "history",
        aliases=["hist"],
        help="View task history"
    )
    history_parser.add_argument(
        "--limit", "-n",
        type=int,
        default=20,
        help="Number of entries to show"
    )
    history_parser.add_argument(
        "--since",
        type=str,
        help="Show entries since date"
    )
    history_parser.add_argument(
        "--export",
        type=str,
        help="Export to file"
    )
    history_parser.add_argument(
        "--search",
        type=str,
        help="Search in task descriptions"
    )
    history_parser.set_defaults(func=history_command)

    return parser


def handle_positional_task(parser: argparse.ArgumentParser, args: argparse.Namespace) -> argparse.Namespace:
    """Handle case where task is provided as positional argument without 'run' command."""
    # If no command specified but positional args exist, treat as 'run' command
    if args.command is None:
        # Check if there's a task in the remaining args
        remaining = parser._remaining_args if hasattr(parser, '_remaining_args') else []
        if remaining and not remaining[0].startswith('-'):
            args.command = "run"
            args.task = remaining[0]
            args.task_flag = None
            args.context = None
            args.auto_context = False
            args.depth = 3
            args.model = None
            args.dry_run = False
            args.output = None
            args.func = run_command
    return args


def install_completion(shell: str) -> int:
    """Install shell completion script."""
    from superintelligence.cli.utils.shell import generate_completion

    completion_script = generate_completion(shell)

    if shell == "bash":
        path = Path.home() / ".bash_completion.d"
        path.mkdir(parents=True, exist_ok=True)
        completion_file = path / "superintelligence"
    elif shell == "zsh":
        path = Path.home() / ".zsh_completions"
        path.mkdir(parents=True, exist_ok=True)
        completion_file = path / "_superintelligence"
    elif shell == "fish":
        path = Path.home() / ".config/fish/completions"
        path.mkdir(parents=True, exist_ok=True)
        completion_file = path / "superintelligence.fish"
    else:
        print(f"Unsupported shell: {shell}", file=sys.stderr)
        return 1

    completion_file.write_text(completion_script)
    print(f"Completion installed to: {completion_file}")
    print(f"Please restart your shell or source the completion file.")
    return 0


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()

    try:
        parsed_args = parser.parse_args(args)

        # Handle shell completion installation
        if parsed_args.install_completion:
            return install_completion(parsed_args.install_completion)

        # Handle positional task (superintelligence "task here")
        if parsed_args.command is None and not parsed_args.install_completion:
            # Check for positional argument
            import shlex
            cmd_line = shlex.join(args) if args else ""
            if cmd_line and not cmd_line.startswith('-'):
                parsed_args.command = "run"
                parsed_args.task = cmd_line
                parsed_args.task_flag = None
                parsed_args.context = None
                parsed_args.auto_context = False
                parsed_args.depth = 3
                parsed_args.model = None
                parsed_args.dry_run = False
                parsed_args.output = None
                parsed_args.func = run_command
            else:
                parser.print_help()
                return 0

        # Load configuration
        config_path = parsed_args.config or get_default_config_path()
        config = load_config(config_path)

        # Merge CLI args with config
        parsed_args.config_data = config

        # Get formatter
        formatter = get_formatter(parsed_args.format, no_color=parsed_args.no_color)
        parsed_args.formatter = formatter

        # Execute command
        if hasattr(parsed_args, 'func'):
            return parsed_args.func(parsed_args)
        else:
            parser.print_help()
            return 0

    except SuperintelligenceError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        return 130
    except Exception as e:
        if parsed_args and parsed_args.verbose > 0:
            import traceback
            traceback.print_exc()
        else:
            print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

#### `src/superintelligence/cli/commands/run.py`

```python
"""Run command implementation."""

import sys
import time
from argparse import Namespace
from typing import Optional

from superintelligence.cli.utils.progress import ProgressIndicator
from superintelligence.core.protocol import SuperintelligenceProtocol
from superintelligence.core.context import ContextManager
from superintelligence.exceptions import TaskExecutionError


def run_command(args: Namespace) -> int:
    """Execute the run command."""

    # Get task from positional arg or flag
    task = args.task or args.task_flag
    if not task:
        print("Error: No task specified. Use: superintelligence 'your task'", file=sys.stderr)
        return 1

    # Initialize components
    config = args.config_data
    formatter = args.formatter

    # Create progress indicator
    progress = ProgressIndicator(
        quiet=args.quiet,
        verbose=args.verbose,
        no_color=args.no_color
    )

    try:
        # Initialize protocol
        protocol = SuperintelligenceProtocol(config)

        # Build context
        context_manager = ContextManager(config)
        context = None

        if args.context:
            context_names = [c.strip() for c in args.context.split(',')]
            context = context_manager.load_contexts(context_names)
            progress.info(f"Loaded contexts: {', '.join(context_names)}")
        elif args.auto_context:
            progress.info("Auto-detecting context from current directory...")
            context = context_manager.detect_context()

        # Show dry-run info
        if args.dry_run:
            formatter.output({
                "mode": "dry-run",
                "task": task,
                "context": context,
                "depth": args.depth,
                "model": args.model or config.get('model', {}).get('name', 'default')
            })
            return 0

        # Execute task
        progress.start_task("Initializing Superintelligence Protocol")

        with progress.spinner("Analyzing task and context"):
            execution_plan = protocol.plan_execution(task, context, depth=args.depth)

        progress.info(f"Execution plan: {execution_plan.get('steps', [])}")

        # Execute with progress tracking
        results = []
        total_steps = len(execution_plan.get('steps', []))

        for i, step in enumerate(execution_plan.get('steps', []), 1):
            progress.update_progress(i, total_steps, f"Step {i}/{total_steps}: {step.get('description', 'Executing')}")

            with progress.spinner(f"Executing: {step.get('description', 'Processing')}"):
                result = protocol.execute_step(step, context)
                results.append(result)

            if args.verbose > 0:
                progress.info(f"Step {i} result: {result.get('status', 'unknown')}")

        progress.complete_task("Task execution complete")

        # Format and output results
        output_data = {
            "task": task,
            "status": "success",
            "execution_time": progress.elapsed_time(),
            "steps_executed": len(results),
            "results": results,
            "summary": protocol.generate_summary(results)
        }

        formatter.output(output_data)

        # Save to file if requested
        if args.output:
            formatter.save(output_data, args.output)
            progress.info(f"Output saved to: {args.output}")

        return 0

    except TaskExecutionError as e:
        progress.error(f"Task execution failed: {e}")
        if args.verbose > 0:
            import traceback
            traceback.print_exc()
        return 1
    except Exception as e:
        progress.error(f"Unexpected error: {e}")
        if args.verbose > 0:
            import traceback
            traceback.print_exc()
        return 1
```

#### `src/superintelligence/cli/commands/scan.py`

```python
"""Scan command implementation."""

import json
from argparse import Namespace
from pathlib import Path

from superintelligence.cli.utils.progress import ProgressIndicator
from superintelligence.core.scanner import ProjectScanner
from superintelligence.core.context import ContextManager


def scan_command(args: Namespace) -> int:
    """Execute the scan command."""

    config = args.config_data
    formatter = args.formatter
    progress = ProgressIndicator(
        quiet=args.quiet,
        verbose=args.verbose,
        no_color=args.no_color
    )

    scan_path = Path(args.path).resolve()

    if not scan_path.exists():
        progress.error(f"Path not found: {scan_path}")
        return 1

    try:
        progress.info(f"Scanning: {scan_path}")

        scanner = ProjectScanner(
            depth=args.depth,
            include_hidden=args.include_hidden,
            exclude_patterns=args.exclude or []
        )

        with progress.spinner("Scanning project structure"):
            scan_result = scanner.scan(scan_path)

        progress.info(f"Found {scan_result.get('file_count', 0)} files in {scan_result.get('directory_count', 0)} directories")

        # Generate context if requested
        if args.generate_context:
            context_name = args.name or scan_path.name
            context_manager = ContextManager(config)

            with progress.spinner(f"Generating context: {context_name}"):
                context_manager.create_from_scan(context_name, scan_result)

            progress.info(f"Context created: {context_name}")

        # Format output
        output_data = {
            "path": str(scan_path),
            "scan_depth": args.depth,
            **scan_result
        }

        formatter.output(output_data)

        # Save to file if requested
        if args.output:
            formatter.save(output_data, args.output)
            progress.info(f"Scan results saved to: {args.output}")

        return 0

    except Exception as e:
        progress.error(f"Scan failed: {e}")
        if args.verbose > 0:
            import traceback
            traceback.print_exc()
        return 1
```

#### `src/superintelligence/cli/utils/progress.py`

```python
"""Progress indicators and UI utilities."""

import sys
import time
from contextlib import contextmanager
from typing import Optional, Iterator


class Colors:
    """ANSI color codes."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'

    @classmethod
    def disable(cls):
        """Disable all colors."""
        for attr in dir(cls):
            if not attr.startswith('_') and isinstance(getattr(cls, attr), str):
                setattr(cls, attr, '')


class Spinner:
    """Terminal spinner animation."""

    SPINNERS = {
        'dots': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
        'line': ['-', '\\', '|', '/'],
        'arrow': ['←', '↖', '↑', '↗', '→', '↘', '↓', '↙'],
    }

    def __init__(self, message: str = "Processing", style: str = 'dots'):
        self.message = message
        self.frames = self.SPINNERS.get(style, self.SPINNERS['dots'])
        self.current = 0
        self.running = False
        self.start_time = time.time()

    def __iter__(self):
        return self

    def __next__(self):
        if not self.running:
            raise StopIteration

        frame = self.frames[self.current % len(self.frames)]
        self.current += 1
        return frame

    def start(self):
        self.running = True
        self.start_time = time.time()

    def stop(self):
        self.running = False

    def get_frame(self) -> str:
        frame = self.frames[self.current % len(self.frames)]
        self.current += 1
        return frame


class ProgressIndicator:
    """Manages progress indication and output formatting."""

    def __init__(self, quiet: bool = False, verbose: int = 0, no_color: bool = False):
        self.quiet = quiet
        self.verbose = verbose
        self.no_color = no_color
        self._start_time: Optional[float] = None
        self._current_spinner: Optional[Spinner] = None

        if no_color:
            Colors.disable()

    def elapsed_time(self) -> float:
        """Get elapsed time since start."""
        if self._start_time is None:
            return 0.0
        return time.time() - self._start_time

    def _print(self, message: str, color: str = '', file=sys.stdout):
        """Print message if not quiet."""
        if not self.quiet:
            if color and not self.no_color:
                print(f"{color}{message}{Colors.RESET}", file=file)
            else:
                print(message, file=file)

    def info(self, message: str):
        """Print info message."""
        if self.verbose > 0:
            self._print(f"{Colors.BLUE}ℹ{Colors.RESET} {message}")

    def success(self, message: str):
        """Print success message."""
        self._print(f"{Colors.GREEN}✓{Colors.RESET} {message}")

    def warning(self, message: str):
        """Print warning message."""
        self._print(f"{Colors.YELLOW}⚠{Colors.RESET} {message}", file=sys.stderr)

    def error(self, message: str):
        """Print error message."""
        self._print(f"{Colors.RED}✗{Colors.RESET} {message}", file=sys.stderr)

    def start_task(self, description: str):
        """Mark the start of a task."""
        self._start_time = time.time()
        if not self.quiet:
            self._print(f"{Colors.CYAN}▶{Colors.RESET} {Colors.BOLD}{description}{Colors.RESET}")

    def complete_task(self, message: str = "Complete"):
        """Mark the completion of a task."""
        elapsed = self.elapsed_time()
        if not self.quiet:
            self._print(f"{Colors.GREEN}✓{Colors.RESET} {message} {Colors.DIM}({elapsed:.2f}s){Colors.RESET}")

    @contextmanager
    def spinner(self, message: str = "Processing") -> Iterator[None]:
        """Context manager for spinner animation."""
        if self.quiet:
            yield
            return

        import threading

        spinner = Spinner(message)
        spinner.start()
        stop_event = threading.Event()

        def spin():
            while not stop_event.is_set():
                frame = spinner.get_frame()
                sys.stdout.write(f"\r{Colors.CYAN}{frame}{Colors.RESET} {message}")
                sys.stdout.flush()
                time.sleep(0.1)
            # Clear line
            sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
            sys.stdout.flush()

        thread = threading.Thread(target=spin)
        thread.start()

        try:
            yield
        finally:
            stop_event.set()
            thread.join()

    def update_progress(self, current: int, total: int, message: str = ""):
        """Update progress bar."""
        if self.quiet:
            return

        width = 30
        filled = int(width * current / total) if total > 0 else 0
        bar = f"{'█' * filled}{'░' * (width - filled)}"

        progress_text = f"{Colors.CYAN}[{bar}]{Colors.RESET} {current}/{total}"
        if message:
            progress_text += f" {message}"

        # Clear line and print
        sys.stdout.write("\r" + " " * 100 + "\r")
        sys.stdout.write(progress_text)
        sys.stdout.flush()

        if current >= total:
            sys.stdout.write("\n")
            sys.stdout.flush()
```

#### `src/superintelligence/cli/formatters/__init__.py`

```python
"""Output formatters for CLI."""

from typing import Union
from argparse import Namespace

from .json_formatter import JsonFormatter
from .yaml_formatter import YamlFormatter
from .human_formatter import HumanFormatter


def get_formatter(format_type: str, no_color: bool = False):
    """Get formatter instance by type."""
    formatters = {
        'json': JsonFormatter,
        'yaml': YamlFormatter,
        'human': HumanFormatter,
    }

    formatter_class = formatters.get(format_type, HumanFormatter)
    return formatter_class(no_color=no_color)
```

#### `src/superintelligence/cli/formatters/json_formatter.py`

```python
"""JSON output formatter."""

import json
from typing import Any, Dict


class JsonFormatter:
    """Format output as JSON."""

    def __init__(self, no_color: bool = False):
        self.no_color = no_color

    def output(self, data: Dict[str, Any], indent: int = 2):
        """Output data as formatted JSON."""
        print(json.dumps(data, indent=indent, default=str))

    def save(self, data: Dict[str, Any], filepath: str, indent: int = 2):
        """Save data as JSON to file."""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=indent, default=str)
```

#### `src/superintelligence/cli/formatters/yaml_formatter.py`

```python
"""YAML output formatter."""

from typing import Any, Dict


class YamlFormatter:
    """Format output as YAML."""

    def __init__(self, no_color: bool = False):
        self.no_color = no_color

    def output(self, data: Dict[str, Any]):
        """Output data as formatted YAML."""
        try:
            import yaml
            print(yaml.dump(data, default_flow_style=False, sort_keys=False))
        except ImportError:
            # Fallback to simple representation
            self._simple_output(data)

    def save(self, data: Dict[str, Any], filepath: str):
        """Save data as YAML to file."""
        try:
            import yaml
            with open(filepath, 'w') as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        except ImportError:
            raise ImportError("PyYAML is required for YAML output. Install with: pip install pyyaml")

    def _simple_output(self, data: Dict[str, Any], indent: int = 0):
        """Simple YAML-like output without PyYAML."""
        prefix = "  " * indent
        for key, value in data.items():
            if isinstance(value, dict):
                print(f"{prefix}{key}:")
                self._simple_output(value, indent + 1)
            elif isinstance(value, list):
                print(f"{prefix}{key}:")
                for item in value:
                    if isinstance(item, dict):
                        print(f"{prefix}  -")
                        self._simple_output(item, indent + 2)
                    else:
                        print(f"{prefix}  - {item}")
            else:
                print(f"{prefix}{key}: {value}")
```

#### `src/superintelligence/cli/formatters/human_formatter.py`

```python
"""Human-readable output formatter."""

from typing import Any, Dict
from datetime import datetime


class Colors:
    """ANSI color codes."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'

    @classmethod
    def disable(cls):
        for attr in dir(cls):
            if not attr.startswith('_') and isinstance(getattr(cls, attr), str):
                setattr(cls, attr, '')


class HumanFormatter:
    """Format output for human readability."""

    def __init__(self, no_color: bool = False):
        self.no_color = no_color
        if no_color:
            Colors.disable()

    def output(self, data: Dict[str, Any]):
        """Output data in human-readable format."""
        if 'task' in data:
            self._format_task_result(data)
        elif 'path' in data and 'file_count' in data:
            self._format_scan_result(data)
        elif 'status' in data:
            self._format_status(data)
        else:
            self._format_generic(data)

    def save(self, data: Dict[str, Any], filepath: str):
        """Save data to file (always as JSON for human format)."""
        import json
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def _format_task_result(self, data: Dict[str, Any]):
        """Format task execution result."""
        print()
        print(f"{Colors.BOLD}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.CYAN}Task Execution Result{Colors.RESET}")
        print(f"{Colors.BOLD}{'=' * 60}{Colors.RESET}")
        print()

        print(f"{Colors.BOLD}Task:{Colors.RESET}")
        print(f"  {data.get('task', 'N/A')}")
        print()

        status = data.get('status', 'unknown')
        status_color = Colors.GREEN if status == 'success' else Colors.RED
        print(f"{Colors.BOLD}Status:{Colors.RESET} {status_color}{status.upper()}{Colors.RESET}")
        print(f"{Colors.BOLD}Execution Time:{Colors.RESET} {data.get('execution_time', 0):.2f}s")
        print(f"{Colors.BOLD}Steps Executed:{Colors.RESET} {data.get('steps_executed', 0)}")
        print()

        summary = data.get('summary', {})
        if summary:
            print(f"{Colors.BOLD}Summary:{Colors.RESET}")
            for key, value in summary.items():
                print(f"  {Colors.DIM}{key}:{Colors.RESET} {value}")

        print()

    def _format_scan_result(self, data: Dict[str, Any]):
        """Format scan result."""
        print()
        print(f"{Colors.BOLD}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.CYAN}Project Scan Results{Colors.RESET}")
        print(f"{Colors.BOLD}{'=' * 60}{Colors.RESET}")
        print()

        print(f"{Colors.BOLD}Path:{Colors.RESET} {data.get('path', 'N/A')}")
        print(f"{Colors.BOLD}Scan Depth:{Colors.RESET} {data.get('scan_depth', 'N/A')}")
        print()

        print(f"{Colors.BOLD}Statistics:{Colors.RESET}")
        print(f"  {Colors.DIM}Files:{Colors.RESET} {data.get('file_count', 0):,}")
        print(f"  {Colors.DIM}Directories:{Colors.RESET} {data.get('directory_count', 0):,}")
        print(f"  {Colors.DIM}Total Size:{Colors.RESET} {self._format_size(data.get('total_size', 0))}")
        print()

        file_types = data.get('file_types', {})
        if file_types:
            print(f"{Colors.BOLD}File Types:{Colors.RESET}")
            sorted_types = sorted(file_types.items(), key=lambda x: x[1], reverse=True)[:10]
            for ext, count in sorted_types:
                print(f"  {ext or '(no extension)'}: {count}")

        print()

    def _format_status(self, data: Dict[str, Any]):
        """Format status output."""
        print()
        print(f"{Colors.BOLD}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.CYAN}System Status{Colors.RESET}")
        print(f"{Colors.BOLD}{'=' * 60}{Colors.RESET}")
        print()

        for key, value in data.items():
            if isinstance(value, bool):
                color = Colors.GREEN if value else Colors.RED
                status = "✓" if value else "✗"
                print(f"{Colors.BOLD}{key}:{Colors.RESET} {color}{status}{Colors.RESET}")
            else:
                print(f"{Colors.BOLD}{key}:{Colors.RESET} {value}")

        print()

    def _format_generic(self, data: Dict[str, Any], indent: int = 0):
        """Format generic data structure."""
        prefix = "  " * indent
        for key, value in data.items():
            if isinstance(value, dict):
                print(f"{prefix}{Colors.BOLD}{key}:{Colors.RESET}")
                self._format_generic(value, indent + 1)
            elif isinstance(value, list):
                print(f"{prefix}{Colors.BOLD}{key}:{Colors.RESET}")
                for item in value:
                    if isinstance(item, dict):
                        self._format_generic(item, indent + 1)
                        print()
                    else:
                        print(f"{prefix}  • {item}")
            else:
                print(f"{prefix}{Colors.BOLD}{key}:{Colors.RESET} {value}")

    def _format_size(self, size_bytes: int) -> str:
        """Format byte size to human readable."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} PB"
```

#### `src/superintelligence/cli/utils/config.py`

```python
"""Configuration management utilities."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


DEFAULT_CONFIG = {
    'version': '1.0.0',
    'model': {
        'provider': 'anthropic',
        'name': 'claude-opus-4',
        'temperature': 0.7,
        'max_tokens': 4096,
    },
    'protocol': {
        'default_depth': 3,
        'max_depth': 10,
        'auto_save': True,
        'checkpoint_interval': 10,
    },
    'scan': {
        'default_depth': 3,
        'exclude_patterns': [
            '.git',
            '__pycache__',
            'node_modules',
            '.venv',
            'venv',
            '*.pyc',
            '.DS_Store',
        ],
        'include_hidden': False,
    },
    'output': {
        'default_format': 'human',
        'save_history': True,
        'history_limit': 100,
    },
    'logging': {
        'level': 'info',
        'file': '~/.superintelligence/logs/superintelligence.log',
        'max_size': '10MB',
        'backup_count': 5,
    },
    'contexts': {
        'directory': '~/.superintelligence/contexts',
    },
}


def get_default_config_path() -> Path:
    """Get the default configuration file path."""
    config_dir = Path.home() / '.superintelligence'
    return config_dir / 'config.yaml'


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from file or create default."""
    path = Path(config_path) if config_path else get_default_config_path()

    if path.exists():
        with open(path, 'r') as f:
            user_config = yaml.safe_load(f) or {}
        # Merge with defaults
        return merge_config(DEFAULT_CONFIG, user_config)

    # Create default config if it doesn't exist
    save_config(DEFAULT_CONFIG, path)
    return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any], path: Optional[Path] = None):
    """Save configuration to file."""
    path = path or get_default_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)


def merge_config(default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge user config into default config."""
    result = default.copy()

    for key, value in user.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_config(result[key], value)
        else:
            result[key] = value

    return result


def get_config_value(config: Dict[str, Any], key: str) -> Any:
    """Get configuration value using dot notation (e.g., 'model.name')."""
    keys = key.split('.')
    value = config

    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return None

    return value


def set_config_value(config: Dict[str, Any], key: str, value: Any):
    """Set configuration value using dot notation."""
    keys = key.split('.')
    target = config

    for k in keys[:-1]:
        if k not in target:
            target[k] = {}
        target = target[k]

    target[keys[-1]] = value
```

### Configuration File

#### Default Configuration (`~/.superintelligence/config.yaml`)

```yaml
version: '1.0.0'

# Model configuration
model:
  provider: anthropic
  name: claude-opus-4
  temperature: 0.7
  max_tokens: 4096

# Protocol settings
protocol:
  default_depth: 3
  max_depth: 10
  auto_save: true
  checkpoint_interval: 10

# Project scanning
scan:
  default_depth: 3
  exclude_patterns:
    - .git
    - __pycache__
    - node_modules
    - .venv
    - venv
    - '*.pyc'
    - .DS_Store
  include_hidden: false

# Output settings
output:
  default_format: human
  save_history: true
  history_limit: 100

# Logging configuration
logging:
  level: info
  file: ~/.superintelligence/logs/superintelligence.log
  max_size: 10MB
  backup_count: 5

# Context storage
contexts:
  directory: ~/.superintelligence/contexts
```

### Setup and Installation Files

#### `pyproject.toml`

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "superintelligence-protocol"
version = "1.0.0"
description = "AI-driven development orchestration CLI"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.9"
authors = [
    {name = "SISO Ecosystem", email = "hello@siso.sh"}
]
keywords = ["ai", "cli", "development", "automation", "superintelligence"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Tools",
]

dependencies = [
    "pyyaml>=6.0",
    "rich>=13.0.0",
    "click>=8.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "mypy>=1.0.0",
    "flake8>=6.0.0",
]

[project.scripts]
superintelligence = "superintelligence.cli.main:main"
si = "superintelligence.cli.main:main"

[project.urls]
Homepage = "https://github.com/siso-ecosystem/superintelligence-protocol"
Documentation = "https://docs.superintelligence.sh"
Repository = "https://github.com/siso-ecosystem/superintelligence-protocol"
Issues = "https://github.com/siso-ecosystem/superintelligence-protocol/issues"

[tool.hatch.build.targets.wheel]
packages = ["src/superintelligence"]

[tool.black]
line-length = 100
target-version = ['py39']

[tool.isort]
profile = "black"
line_length = 100

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

## Error Handling

The CLI implements comprehensive error handling:

### Error Types

| Error Code | Description | Exit Code |
|------------|-------------|-----------|
| `SUCCESS` | Operation completed successfully | 0 |
| `GENERAL_ERROR` | Unspecified error | 1 |
| `INVALID_ARGUMENTS` | Invalid command-line arguments | 2 |
| `CONFIG_ERROR` | Configuration file error | 3 |
| `TASK_EXECUTION_ERROR` | Task execution failed | 10 |
| `SCAN_ERROR` | Project scan failed | 20 |
| `CONTEXT_ERROR` | Context operation failed | 30 |
| `NETWORK_ERROR` | Network/API error | 40 |
| `AUTHENTICATION_ERROR` | Authentication failed | 41 |
| `PERMISSION_DENIED` | Insufficient permissions | 42 |
| `NOT_FOUND` | Resource not found | 44 |
| `TIMEOUT_ERROR` | Operation timed out | 50 |
| `USER_INTERRUPT` | User cancelled operation | 130 |

### Exception Hierarchy

```python
# src/superintelligence/exceptions.py

class SuperintelligenceError(Exception):
    """Base exception for all CLI errors."""
    exit_code = 1

    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ConfigurationError(SuperintelligenceError):
    """Configuration-related errors."""
    exit_code = 3


class TaskExecutionError(SuperintelligenceError):
    """Task execution errors."""
    exit_code = 10


class ScanError(SuperintelligenceError):
    """Project scanning errors."""
    exit_code = 20


class ContextError(SuperintelligenceError):
    """Context management errors."""
    exit_code = 30


class NetworkError(SuperintelligenceError):
    """Network/API errors."""
    exit_code = 40


class AuthenticationError(SuperintelligenceError):
    """Authentication errors."""
    exit_code = 41
```

## Integration with Project Scanner

The CLI integrates seamlessly with the Project Scanner module:

```python
# Example integration flow
from superintelligence.core.scanner import ProjectScanner
from superintelligence.core.context import ContextManager

# 1. Scan project
scanner = ProjectScanner(depth=5)
scan_result = scanner.scan("/path/to/project")

# 2. Create context from scan
context_manager = ContextManager(config)
context = context_manager.create_from_scan("my-project", scan_result)

# 3. Use context in task execution
protocol = SuperintelligenceProtocol(config)
result = protocol.execute_task(task, context=context)
```

## Testing

### Unit Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=superintelligence --cov-report=html

# Run specific test file
pytest tests/test_cli.py

# Run with verbose output
pytest -v
```

### Integration Tests

```bash
# Test CLI commands
superintelligence --version
superintelligence status
superintelligence scan --depth 2

# Test with dry-run
superintelligence run --task "test" --dry-run
```

## Future Enhancements

1. **Plugin System**: Allow third-party extensions
2. **Web Dashboard**: Real-time monitoring interface
3. **Team Collaboration**: Shared contexts and history
4. **CI/CD Integration**: Native GitHub Actions, GitLab CI support
5. **IDE Extensions**: VS Code, IntelliJ plugins
6. **Voice Interface**: Speech-to-task capabilities

## License

MIT License - See LICENSE file for details.

---

Built with ♥ by the SISO Ecosystem
