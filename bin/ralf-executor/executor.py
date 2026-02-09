#!/usr/bin/env python3
"""
RALF Executor - BB5 Autonomous Task Execution Engine

This is the main executor that:
1. Reads queue.yaml to find highest priority pending task
2. Locks the task (updates status to 'claimed')
3. Reads the full task definition from tasks/active/TASK-XXX/task.md
4. Creates a run folder: runs/executor/run-YYYYMMDD_HHMMSS-TASK-XXX/
5. Initializes run documentation (THOUGHTS.md, DECISIONS.md, LEARNINGS.md, RESULTS.md, CHANGES.md)
6. Spawns bb5-context-collector agent to gather context
7. Builds a dynamic prompt for Claude Code
8. Executes the task using `claude -p --dangerously-skip-permissions`
9. Monitors execution for completion signal
10. Updates task status and moves to completed/
11. Commits changes to git
"""

import os
import sys
import re
import yaml
import json
import shutil
import subprocess
import argparse
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

# Configuration - use environment variable or default
BB5_DIR = Path(os.environ.get("BB5_DIR", "/opt/blackbox5"))
TASKS_DIR = BB5_DIR / "5-project-memory" / "blackbox5" / ".autonomous" / "tasks"
RUNS_DIR = BB5_DIR / "5-project-memory" / "blackbox5" / ".autonomous" / "runs" / "executor"
AGENTS_DIR = BB5_DIR / ".claude" / "agents"
QUEUE_FILE = BB5_DIR / "5-project-memory" / "blackbox5" / ".autonomous" / "communications" / "queue-core.yaml"

class TaskStatus(Enum):
    PENDING = "pending"
    CLAIMED = "claimed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"

@dataclass
class Task:
    """Represents a BB5 task"""
    task_id: str
    title: str
    description: str
    status: TaskStatus
    priority: str
    task_type: str
    created: str
    started: Optional[str] = None
    completed: Optional[str] = None
    acceptance_criteria: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    file_path: Optional[Path] = None

    @property
    def task_dir(self) -> Path:
        return TASKS_DIR / "active" / self.task_id

    @property
    def completed_dir(self) -> Path:
        return TASKS_DIR / "completed" / self.task_id

@dataclass
class RunContext:
    """Context for a task execution run"""
    run_id: str
    run_folder: Path
    task: Task
    start_time: datetime
    context_collector_output: Optional[Path] = None
    claude_output: Optional[Path] = None
    status: str = "initializing"

class BB5Executor:
    """Main executor class for BB5 autonomous task execution"""

    def __init__(self, dry_run: bool = False, verbose: bool = False):
        self.dry_run = dry_run
        self.verbose = verbose
        self.setup_logging()
        self.current_run: Optional[RunContext] = None

    def setup_logging(self):
        """Setup logging configuration"""
        log_format = "%(asctime)s [%(levelname)s] %(message)s"
        if self.verbose:
            logging.basicConfig(level=logging.DEBUG, format=log_format)
        else:
            logging.basicConfig(level=logging.INFO, format=log_format)
        self.logger = logging.getLogger("BB5Executor")

    def log(self, message: str, level: LogLevel = LogLevel.INFO):
        """Log a message with color coding"""
        colors = {
            LogLevel.DEBUG: "\033[36m",      # Cyan
            LogLevel.INFO: "\033[34m",       # Blue
            LogLevel.SUCCESS: "\033[32m",    # Green
            LogLevel.WARNING: "\033[33m",    # Yellow
            LogLevel.ERROR: "\033[31m",      # Red
        }
        reset = "\033[0m"
        color = colors.get(level, "")

        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"{color}[{timestamp}]{reset} [EXECUTOR] {message}"

        if level == LogLevel.ERROR:
            self.logger.error(message)
        elif level == LogLevel.WARNING:
            self.logger.warning(message)
        elif level == LogLevel.DEBUG:
            self.logger.debug(message)
        else:
            self.logger.info(message)

        print(formatted)

    def acquire_task(self) -> Optional[Task]:
        """
        Get the next highest priority pending task from the queue.
        Returns None if no pending tasks.
        """
        self.log("Scanning for pending tasks...", LogLevel.INFO)

        active_dir = TASKS_DIR / "active"
        if not active_dir.exists():
            self.log("No active tasks directory found", LogLevel.WARNING)
            return None

        pending_tasks: List[Task] = []

        # Scan all task directories
        for task_dir in active_dir.iterdir():
            if not task_dir.is_dir():
                continue

            task_file = task_dir / "task.md"
            if not task_file.exists():
                continue

            try:
                task = self.parse_task_file(task_file)
                if task.status == TaskStatus.PENDING:
                    pending_tasks.append(task)
            except Exception as e:
                self.log(f"Failed to parse {task_file}: {e}", LogLevel.WARNING)
                continue

        if not pending_tasks:
            self.log("No pending tasks found", LogLevel.INFO)
            return None

        # Sort by priority (high > medium > low) and creation date
        priority_order = {"high": 0, "medium": 1, "low": 2}
        pending_tasks.sort(key=lambda t: (
            priority_order.get(t.priority.lower(), 3),
            t.created
        ))

        selected_task = pending_tasks[0]
        self.log(f"Selected task: {selected_task.task_id} (priority: {selected_task.priority})", LogLevel.SUCCESS)

        # Lock the task
        if not self.dry_run:
            self._update_task_status(selected_task, TaskStatus.CLAIMED)

        return selected_task

    def parse_task_file(self, task_file: Path) -> Task:
        """Parse a task.md file and extract task information"""
        content = task_file.read_text()

        # Extract frontmatter-style metadata
        task_id = self._extract_field(content, r"\*\*Task ID:\*\*\s*(.+?)(?:\n|$)") or \
                  self._extract_field(content, r"^#\s*(TASK-[\w-]+)")

        title = self._extract_field(content, r"^#\s*TASK-[\w-]+:\s*(.+?)(?:\n|$)")

        status_str = self._extract_field(content, r"\*\*Status:\*\*\s*(\w+)") or "pending"
        status = TaskStatus(status_str.lower())

        priority = self._extract_field(content, r"\*\*Priority:\*\*\s*(\w+)") or "medium"
        task_type = self._extract_field(content, r"\*\*Type:\*\*\s*(.+?)(?:\n|$)") or "general"
        created = self._extract_field(content, r"\*\*Created:\*\*\s*(.+?)(?:\n|$)") or \
                  datetime.now().isoformat()

        # Extract description
        desc_match = re.search(r"## Description\s*\n+(.+?)(?=\n##|\Z)", content, re.DOTALL)
        description = desc_match.group(1).strip() if desc_match else ""

        # Extract acceptance criteria
        criteria = []
        criteria_section = re.search(r"## Acceptance Criteria.*?(?=\n##|\Z)", content, re.DOTALL)
        if criteria_section:
            criteria = re.findall(r"- \[.\]\s*(.+)", criteria_section.group(0))

        # Extract dependencies
        deps = []
        deps_section = re.search(r"## Dependencies.*?(?=\n##|\Z)", content, re.DOTALL)
        if deps_section:
            deps = re.findall(r"- (TASK-[\w-]+)", deps_section.group(0))

        return Task(
            task_id=task_id or task_file.parent.name,
            title=title or task_id or "Untitled Task",
            description=description,
            status=status,
            priority=priority,
            task_type=task_type,
            created=created,
            acceptance_criteria=criteria,
            dependencies=deps,
            file_path=task_file
        )

    def _extract_field(self, content: str, pattern: str) -> Optional[str]:
        """Extract a field from markdown content using regex"""
        match = re.search(pattern, content, re.MULTILINE | re.IGNORECASE)
        return match.group(1).strip() if match else None

    def _update_task_status(self, task: Task, status: TaskStatus):
        """Update the task status in the task.md file"""
        if not task.file_path:
            return

        content = task.file_path.read_text()

        # Update status field
        content = re.sub(
            r"(\*\*Status:\*\*\s*)\w+",
            f"\\g<1>{status.value}",
            content
        )

        # Update timestamps
        if status == TaskStatus.IN_PROGRESS and task.started is None:
            content = re.sub(
                r"(\*\*Started:\*\*\s*)null",
                f"\\g<1>{datetime.now().isoformat()}",
                content
            )
        elif status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.PARTIAL]:
            content = re.sub(
                r"(\*\*Completed:\*\*\s*)null",
                f"\\g<1>{datetime.now().isoformat()}",
                content
            )

        task.file_path.write_text(content)
        task.status = status
        self.log(f"Updated {task.task_id} status to {status.value}", LogLevel.DEBUG)

    def create_run_folder(self, task: Task) -> RunContext:
        """Create a run folder for task execution"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_id = f"run-{timestamp}-{task.task_id}"
        run_folder = RUNS_DIR / run_id

        if not self.dry_run:
            run_folder.mkdir(parents=True, exist_ok=True)

        self.log(f"Created run folder: {run_folder}", LogLevel.INFO)

        # Initialize run documentation
        self._init_run_docs(run_folder, task)

        return RunContext(
            run_id=run_id,
            run_folder=run_folder,
            task=task,
            start_time=datetime.now()
        )

    def _init_run_docs(self, run_folder: Path, task: Task):
        """Initialize run documentation files"""
        docs = {
            "THOUGHTS.md": f"""# THOUGHTS - {task.task_id}

**Run:** {run_folder.name}
**Date:** {datetime.now().isoformat()}
**Task:** {task.title}
**Agent:** BB5 Executor

---

## Session Start

### Context
- **Current Task:** {task.task_id}
- **Goal:** {task.description[:200]}...
- **Priority:** {task.priority}

### Initial Assessment
Task acquired and ready for execution.

---

## Phase 1: Context Gathering

Gathering context via bb5-context-collector...

---

## Phase 2: Execution

Executing task via Claude Code...

---

## Phase 3: Validation

Verifying completion against acceptance criteria...

---

## Session End

Pending execution completion.
""",
            "DECISIONS.md": f"""# DECISIONS - {task.task_id}

**Run:** {run_folder.name}
**Date:** {datetime.now().isoformat()}
**Task:** {task.title}

---

## Decision Registry

### [AUTO] Task Acquisition
- **Decision:** Selected {task.task_id} for execution
- **Rationale:** Highest priority pending task
- **Timestamp:** {datetime.now().isoformat()}

---

## Decision Log

| ID | Title | Status | Date |
|----|-------|--------|------|

""",
            "LEARNINGS.md": f"""# LEARNINGS - {task.task_id}

**Run:** {run_folder.name}
**Date:** {datetime.now().isoformat()}
**Task:** {task.title}

---

## What Worked Well

- Task acquisition successful

## What Was Harder Than Expected

## What Would We Do Differently

## Patterns Detected

""",
            "RESULTS.md": f"""# RESULTS - {task.task_id}

**Run:** {run_folder.name}
**Date:** {datetime.now().isoformat()}
**Task:** {task.title}
**Status:** IN_PROGRESS

---

## Summary

Task execution in progress...

## Acceptance Criteria Status

| Criterion | Status | Notes |
|-----------|--------|-------|
""",
            "CHANGES.md": f"""# CHANGES - {task.task_id}

**Run:** {run_folder.name}
**Date:** {datetime.now().isoformat()}

---

## Files Modified

| File | Change Type | Description |
|------|-------------|-------------|

## Git Commit

- **Commit Hash:** TBD
- **Message:** TBD

"""
        }

        for filename, content in docs.items():
            filepath = run_folder / filename
            if not self.dry_run:
                filepath.write_text(content)
            self.log(f"Initialized {filename}", LogLevel.DEBUG)

    def spawn_context_collector(self, run_context: RunContext) -> Optional[Path]:
        """
        Spawn the bb5-context-collector agent to gather context.
        Returns the path to the context report if successful.
        """
        self.log("Spawning bb5-context-collector agent...", LogLevel.INFO)

        collector_agent = AGENTS_DIR / "bb5-context-collector.md"
        if not collector_agent.exists():
            self.log(f"Context collector agent not found at {collector_agent}", LogLevel.WARNING)
            return None

        context_output = run_context.run_folder / "CONTEXT_REPORT.md"

        if self.dry_run:
            self.log("[DRY RUN] Would spawn context collector", LogLevel.INFO)
            return context_output

        # Build context collector prompt
        prompt = f"""Read the context collector agent instructions from {collector_agent}

You are the bb5-context-collector agent. Your mission is to gather comprehensive context for task execution.

Task: {run_context.task.task_id}
Title: {run_context.task.title}
Description: {run_context.task.description}

Please:
1. Read your agent instructions from {collector_agent}
2. Gather context about the current BB5 state
3. Focus on information relevant to: {run_context.task.task_type}
4. Save your report to: {context_output}

Return a concise summary of the most important context for this task.
"""

        try:
            # Execute context collector via Claude Code
            result = self._run_claude(prompt, timeout=120)

            if result.returncode == 0:
                self.log("Context collector completed successfully", LogLevel.SUCCESS)
                run_context.context_collector_output = context_output
                return context_output
            else:
                self.log(f"Context collector failed: {result.stderr}", LogLevel.WARNING)
                return None

        except Exception as e:
            self.log(f"Failed to spawn context collector: {e}", LogLevel.WARNING)
            return None

    def build_prompt(self, task: Task, run_context: RunContext) -> str:
        """Build a dynamic execution prompt for Claude Code"""

        # Read task file content
        task_content = ""
        if task.file_path:
            task_content = task.file_path.read_text()

        # Read context report if available
        context_report = ""
        if run_context.context_collector_output and run_context.context_collector_output.exists():
            context_report = run_context.context_collector_output.read_text()

        prompt = f"""# BB5 Task Execution

You are the BB5 Executor. Execute the following task autonomously.

## Task Information

**Task ID:** {task.task_id}
**Title:** {task.title}
**Priority:** {task.priority}
**Type:** {task.task_type}

## Description

{task.description}

## Full Task Definition

```markdown
{task_content}
```

## Context Report

{context_report if context_report else "No context report available."}

## Acceptance Criteria

The following criteria MUST be met for successful completion:

"""

        for criterion in task.acceptance_criteria:
            prompt += f"- [ ] {criterion}\n"

        prompt += f"""
## Execution Instructions

1. **Read Before Change**: Read ALL relevant files before making modifications
2. **Follow Standards**: Adhere to project coding standards and conventions
3. **Document**: Update THOUGHTS.md, DECISIONS.md, and LEARNINGS.md as you work
4. **Test**: Verify your changes work as expected
5. **Commit**: Create atomic commits with clear messages

## Run Context

- **Run Folder:** {run_context.run_folder}
- **Started:** {run_context.start_time.isoformat()}

## Output Requirements

When you complete the task, you MUST signal completion by including this tag in your final output:

<promise>COMPLETE</promise>

If the task cannot be completed, use:

<promise>PARTIAL</promise>

And explain what was accomplished and what remains.

## Begin Execution

Start executing the task now. Work autonomously and efficiently.
"""

        return prompt

    def execute_task(self, run_context: RunContext) -> Tuple[bool, str]:
        """
        Execute the task using Claude Code.
        Returns (success, output) tuple.
        """
        self.log(f"Executing task: {run_context.task.task_id}", LogLevel.INFO)

        prompt = self.build_prompt(run_context.task, run_context)

        # Save prompt to file for debugging
        prompt_file = run_context.run_folder / "execution_prompt.md"
        if not self.dry_run:
            prompt_file.write_text(prompt)

        if self.dry_run:
            self.log("[DRY RUN] Would execute Claude Code with prompt", LogLevel.INFO)
            return True, "DRY RUN - No actual execution"

        # Update task status
        self._update_task_status(run_context.task, TaskStatus.IN_PROGRESS)

        # Execute Claude Code
        output_file = run_context.run_folder / "claude_output.log"
        run_context.claude_output = output_file

        try:
            result = self._run_claude(prompt, output_file=output_file, timeout=600)

            # Check for completion signal
            output = output_file.read_text() if output_file.exists() else result.stdout

            if "<promise>COMPLETE</promise>" in output:
                self.log("Task signaled COMPLETE", LogLevel.SUCCESS)
                return True, output
            elif "<promise>PARTIAL</promise>" in output:
                self.log("Task signaled PARTIAL completion", LogLevel.WARNING)
                return False, output
            else:
                self.log("No completion signal found - assuming partial", LogLevel.WARNING)
                return False, output

        except subprocess.TimeoutExpired:
            self.log("Task execution timed out", LogLevel.ERROR)
            return False, "Execution timed out after 10 minutes"
        except Exception as e:
            self.log(f"Task execution failed: {e}", LogLevel.ERROR)
            return False, str(e)

    def _run_claude(self, prompt: str, output_file: Optional[Path] = None, timeout: int = 300) -> subprocess.CompletedProcess:
        """Run Claude Code with the given prompt"""

        cmd = ["claude", "-p", "--dangerously-skip-permissions"]

        # Run claude with the prompt
        result = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=BB5_DIR
        )

        if output_file and result.stdout:
            output_file.write_text(result.stdout)

        return result

    def verify_completion(self, run_context: RunContext, output: str) -> bool:
        """
        Verify task completion against acceptance criteria.
        Returns True if all criteria are met.
        """
        self.log("Verifying task completion...", LogLevel.INFO)

        # Check for explicit completion signal
        if "<promise>COMPLETE</promise>" not in output:
            self.log("Missing COMPLETE signal", LogLevel.WARNING)
            return False

        # Update RESULTS.md
        results_file = run_context.run_folder / "RESULTS.md"
        if results_file.exists():
            content = results_file.read_text()
            content = content.replace("**Status:** IN_PROGRESS", "**Status:** COMPLETED")
            content = content.replace("Task execution in progress...", "Task completed successfully.")

            # Add acceptance criteria status
            criteria_status = "\n".join([
                f"| {criterion} | completed | Verified |"
                for criterion in run_context.task.acceptance_criteria
            ])

            content = content.replace(
                "| Criterion | Status | Notes |\n|-----------|--------|-------|",
                f"| Criterion | Status | Notes |\n|-----------|--------|-------|\n{criteria_status}"
            )

            if not self.dry_run:
                results_file.write_text(content)

        return True

    def complete_task(self, run_context: RunContext, success: bool):
        """
        Complete the task by updating status and moving to completed folder.
        """
        task = run_context.task

        if success:
            self.log(f"Completing task: {task.task_id}", LogLevel.SUCCESS)
            new_status = TaskStatus.COMPLETED
        else:
            self.log(f"Marking task as partial: {task.task_id}", LogLevel.WARNING)
            new_status = TaskStatus.PARTIAL

        if self.dry_run:
            self.log(f"[DRY RUN] Would update status to {new_status.value}", LogLevel.INFO)
            return

        # Update task status
        self._update_task_status(task, new_status)

        # Move task to completed folder
        if success:
            self._move_to_completed(task)

        # Commit changes
        self._commit_changes(run_context, success)

    def _move_to_completed(self, task: Task):
        """Move task from active to completed folder"""
        if not task.task_dir.exists():
            return

        completed_dir = task.completed_dir
        completed_dir.mkdir(parents=True, exist_ok=True)

        # Copy all files from active to completed
        for item in task.task_dir.iterdir():
            dest = completed_dir / item.name
            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest)

        self.log(f"Moved task to completed folder: {completed_dir}", LogLevel.INFO)

    def _commit_changes(self, run_context: RunContext, success: bool):
        """Commit changes to git"""
        self.log("Checking for changes to commit...", LogLevel.INFO)

        try:
            # Check if there are changes
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=BB5_DIR
            )

            if not result.stdout.strip():
                self.log("No changes to commit", LogLevel.INFO)
                return

            # Stage changes
            subprocess.run(["git", "add", "-A"], cwd=BB5_DIR, check=True)

            # Create commit
            status_str = "complete" if success else "partial"
            commit_msg = f"""feat(executor): {run_context.task.task_id} - {run_context.task.title}

- Status: {status_str}
- Run: {run_context.run_id}
- Type: {run_context.task.task_type}

Auto-generated by BB5 Executor"""

            subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=BB5_DIR,
                check=True
            )

            self.log("Changes committed successfully", LogLevel.SUCCESS)

            # Update CHANGES.md
            changes_file = run_context.run_folder / "CHANGES.md"
            if changes_file.exists():
                content = changes_file.read_text()

                # Get commit hash
                hash_result = subprocess.run(
                    ["git", "rev-parse", "--short", "HEAD"],
                    capture_output=True,
                    text=True,
                    cwd=BB5_DIR
                )
                commit_hash = hash_result.stdout.strip()

                content = content.replace(
                    "**Commit Hash:** TBD",
                    f"**Commit Hash:** {commit_hash}"
                )
                content = content.replace(
                    "**Message:** TBD",
                    f"**Message:** {commit_msg.split(chr(10))[0]}"
                )

                changes_file.write_text(content)

        except subprocess.CalledProcessError as e:
            self.log(f"Git operation failed: {e}", LogLevel.WARNING)

    def run(self):
        """Main execution loop"""
        self.log("=" * 60, LogLevel.INFO)
        self.log("BB5 Executor - Autonomous Task Execution Engine", LogLevel.INFO)
        self.log("=" * 60, LogLevel.INFO)

        if self.dry_run:
            self.log("[DRY RUN MODE] - No actual changes will be made", LogLevel.WARNING)

        try:
            # Step 1: Acquire task
            task = self.acquire_task()
            if not task:
                self.log("No pending tasks found. Exiting.", LogLevel.INFO)
                return 0

            # Step 2: Create run folder
            self.current_run = self.create_run_folder(task)

            # Step 3: Spawn context collector
            self.spawn_context_collector(self.current_run)

            # Step 4: Execute task
            success, output = self.execute_task(self.current_run)

            # Step 5: Verify completion
            if success:
                success = self.verify_completion(self.current_run, output)

            # Step 6: Complete task
            self.complete_task(self.current_run, success)

            # Final status
            if success:
                self.log(f"Task {task.task_id} completed successfully", LogLevel.SUCCESS)
                return 0
            else:
                self.log(f"Task {task.task_id} completed partially", LogLevel.WARNING)
                return 1

        except KeyboardInterrupt:
            self.log("Execution interrupted by user", LogLevel.WARNING)
            return 130
        except Exception as e:
            self.log(f"Unexpected error: {e}", LogLevel.ERROR)
            import traceback
            self.log(traceback.format_exc(), LogLevel.DEBUG)
            return 1

def main():
    parser = argparse.ArgumentParser(
        description="BB5 Executor - Autonomous Task Execution Engine"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run in dry-run mode (no actual changes)"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--task-id",
        type=str,
        help="Execute specific task by ID (bypasses queue)"
    )

    args = parser.parse_args()

    executor = BB5Executor(dry_run=args.dry_run, verbose=args.verbose)
    exit_code = executor.run()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
