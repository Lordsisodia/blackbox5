#!/usr/bin/env python3
"""
BlackBox5 + Vibe Kanban Integration Module

This module enables BlackBox5 agents to:
1. Create tasks in Vibe Kanban
2. Spawn Claude Code agents on those tasks
3. Monitor progress and status updates
4. Handle completion and review workflow
"""

import requests
import time
import json
import subprocess
from typing import Optional, Dict, List, Any
from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    """Vibe Kanban task statuses"""
    TODO = "todo"
    IN_PROGRESS = "inprogress"
    IN_REVIEW = "inreview"
    DONE = "done"
    CANCELLED = "cancelled"


@dataclass
class Repository:
    """Repository configuration for Vibe Kanban"""
    repo_id: str
    base_branch: str = "main"


@dataclass
class Executor:
    """Executor type for running agents"""
    CLAUDE_CODE = "CLAUDE_CODE"
    AMP = "AMP"
    GEMINI = "GEMINI"
    CODEX = "CODEX"
    OPENCODE = "OPENCODE"
    CURSOR_AGENT = "CURSOR_AGENT"
    QWEN_CODE = "QWEN_CODE"
    COPILOT = "COPILOT"
    DROID = "DROID"


class VibeKanbanClient:
    """Client for interacting with Vibe Kanban REST API"""

    def __init__(self, base_url: str = "http://127.0.0.1:57276"):
        """
        Initialize Vibe Kanban client

        Args:
            base_url: Vibe Kanban API base URL (default: localhost:57276)
        """
        self.base_url = base_url.rstrip('/')
        self.api_base = f"{self.base_url}/api"

    def _api_call(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API call to Vibe Kanban"""
        url = f"{self.api_base}/{endpoint.lstrip('/')}"
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def create_task(
        self,
        project_id: str,
        title: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new task in Vibe Kanban

        Args:
            project_id: Vibe Kanban project UUID
            title: Task title
            description: Task description (markdown supported)

        Returns:
            Created task data with task_id
        """
        payload = {
            "project_id": project_id,
            "title": title
        }
        if description:
            payload["description"] = description

        result = self._api_call("POST", "/tasks", json=payload)
        return result["data"]

    def start_agent(
        self,
        task_id: str,
        executor: str = Executor.CLAUDE_CODE,
        repos: Optional[List[Repository]] = None
    ) -> Dict[str, Any]:
        """
        Start a Claude Code agent working on a task

        This creates:
        1. A git worktree for isolated work
        2. A workspace for tracking
        3. Spawns the agent process
        4. Updates task status to "inprogress"

        Args:
            task_id: Task UUID to work on
            executor: Executor type (default: CLAUDE_CODE)
            repos: List of repositories to work with

        Returns:
            Workspace data
        """
        if not repos:
            raise ValueError("Must specify at least one repository")

        payload = {
            "task_id": task_id,
            "executor_profile_id": {
                "executor": executor,
                "variant": None
            },
            "repos": [
                {
                    "repo_id": repo.repo_id,
                    "target_branch": repo.base_branch
                }
                for repo in repos
            ]
        }

        result = self._api_call("POST", "/task-attempts", json=payload)
        return result["data"]

    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get task details and current status"""
        result = self._api_call("GET", f"/tasks/{task_id}")
        return result["data"]

    def list_tasks(
        self,
        project_id: str,
        status: Optional[TaskStatus] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """List tasks in a project"""
        params = {"project_id": project_id, "limit": limit}
        if status:
            params["status"] = status.value

        result = self._api_call("GET", "/tasks", params=params)
        return result["data"]

    def update_task_status(
        self,
        task_id: str,
        status: TaskStatus
    ) -> Dict[str, Any]:
        """
        Update task status

        Args:
            task_id: Task UUID
            status: New status (TaskStatus enum)

        Returns:
            Updated task data
        """
        payload = {"status": status.value}
        result = self._api_call("PUT", f"/tasks/{task_id}", json=payload)
        return result["data"]

    def wait_for_completion(
        self,
        task_id: str,
        poll_interval: int = 5,
        timeout: int = 7200
    ) -> Dict[str, Any]:
        """
        Wait for task to complete (status becomes inreview or done)

        Args:
            task_id: Task UUID to monitor
            poll_interval: Seconds between status checks
            timeout: Maximum seconds to wait

        Returns:
            Final task state

        Raises:
            TimeoutError: If task doesn't complete within timeout
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            task = self.get_task(task_id)
            status = task["status"]
            has_in_progress = task.get("has_in_progress_attempt", False)
            last_failed = task.get("last_attempt_failed", False)

            print(f"Task status: {status}, in_progress: {has_in_progress}")

            # Check completion conditions
            if status == TaskStatus.IN_REVIEW.value:
                print("✅ Task completed, awaiting review")
                return task
            elif status == TaskStatus.DONE.value:
                print("✅ Task marked as done")
                return task
            elif last_failed:
                print("❌ Task execution failed")
                raise RuntimeError(f"Task {task_id} execution failed")
            elif not has_in_progress and status == TaskStatus.IN_PROGRESS.value:
                print("⚠️  Agent finished but task not auto-finalized")
                # Auto-move to inreview
                return self.update_task_status(task_id, TaskStatus.IN_REVIEW)

            time.sleep(poll_interval)

        raise TimeoutError(f"Task {task_id} did not complete within {timeout}s")


class BlackBox5Orchestrator:
    """
    Orchestrates BlackBox5 agents with Vibe Kanban tracking

    This is the main interface for BlackBox5 to use Vibe Kanban for
    task management and agent execution.
    """

    def __init__(
        self,
        vibe_kanban_url: str = "http://127.0.0.1:57276",
        project_id: str = "48ec7737-b706-4817-b86c-5786163a0139",
        repo_id: str = "b5b86bc2-fbfb-4276-b15e-01496d647a81"
    ):
        """
        Initialize BlackBox5 orchestrator

        Args:
            vibe_kanban_url: Vibe Kanban API URL
            project_id: BlackBox5 project UUID in Vibe Kanban
            repo_id: Default repository UUID to work with
        """
        self.client = VibeKanbanClient(vibe_kanban_url)
        self.project_id = project_id
        self.repo_id = repo_id

    def execute_plan(
        self,
        plan_name: str,
        description: str,
        branch_name: Optional[str] = None,
        executor: str = Executor.CLAUDE_CODE,
        wait: bool = True
    ) -> Dict[str, Any]:
        """
        Execute a BlackBox5 improvement plan with Vibe Kanban tracking

        This is the main method BlackBox5 will use to execute tasks.

        Args:
            plan_name: Name of the plan (e.g., "PLAN-008: Fix API Mismatches")
            description: Detailed task description
            branch_name: Git branch name (default: auto-generated from plan_name)
            executor: Agent executor to use
            wait: Whether to wait for completion

        Returns:
            Task data (with task_id, status, etc.)
        """
        print(f"🚀 Starting BlackBox5 plan: {plan_name}")
        print("=" * 60)

        # Step 1: Create task in Vibe Kanban
        print("📋 Creating task in Vibe Kanban...")
        task = self.client.create_task(
            project_id=self.project_id,
            title=plan_name,
            description=description
        )
        task_id = task["id"]
        print(f"✅ Task created: {task_id}")
        print(f"   Status: {task['status']}")

        # Step 2: Start agent
        print("\n🤖 Starting Claude Code agent...")
        branch = branch_name or self._generate_branch_name(plan_name)
        repos = [Repository(repo_id=self.repo_id, base_branch=branch)]

        workspace = self.client.start_agent(
            task_id=task_id,
            executor=executor,
            repos=repos
        )
        workspace_id = workspace["id"]
        print(f"✅ Agent started in workspace: {workspace_id}")
        print(f"   Branch: {workspace['branch']}")

        # Step 3: Monitor progress
        if wait:
            print("\n⏳ Monitoring progress...")
            try:
                final_task = self.client.wait_for_completion(task_id)
                print(f"\n🎉 Plan completed successfully!")
                print(f"   Final status: {final_task['status']}")
                return final_task
            except (RuntimeError, TimeoutError) as e:
                print(f"\n❌ Plan execution failed: {e}")
                raise

        return task

    def execute_parallel_plans(
        self,
        plans: List[Dict[str, str]],
        executor: str = Executor.CLAUDE_CODE
    ) -> List[Dict[str, Any]]:
        """
        Execute multiple plans in parallel

        Args:
            plans: List of {"name": str, "description": str}
            executor: Agent executor to use

        Returns:
            List of task data
        """
        print(f"🚀 Executing {len(plans)} plans in parallel...")
        print("=" * 60)

        # Create all tasks first
        tasks = []
        for plan in plans:
            task = self.client.create_task(
                project_id=self.project_id,
                title=plan["name"],
                description=plan["description"]
            )
            tasks.append(task)
            print(f"✅ Created task: {plan['name']} ({task['id']})")

        # Start all agents
        print("\n🤖 Starting agents...")
        for i, (task, plan) in enumerate(zip(tasks, plans), 1):
            branch = self._generate_branch_name(plan["name"])
            repos = [Repository(repo_id=self.repo_id, base_branch=branch)]

            workspace = self.client.start_agent(
                task_id=task["id"],
                executor=executor,
                repos=repos
            )
            print(f"{i}. {plan['name']}: {workspace['branch']}")

        print(f"\n✅ {len(tasks)} agents started in parallel")
        print(f"   Monitor in Vibe Kanban UI: {self.client.base_url}")

        return tasks

    def _generate_branch_name(self, plan_name: str) -> str:
        """Generate a git branch name from plan name"""
        # Extract plan identifier (e.g., "PLAN-008" from "PLAN-008: Fix API")
        parts = plan_name.split(":")
        identifier = parts[0].strip().lower().replace(" ", "-")
        return f"bb5/{identifier}"

    def mark_task_done(self, task_id: str) -> Dict[str, Any]:
        """Mark a task as done after review"""
        return self.client.update_task_status(task_id, TaskStatus.DONE)

    def mark_task_in_review(self, task_id: str) -> Dict[str, Any]:
        """Mark a task as ready for review"""
        return self.client.update_task_status(task_id, TaskStatus.IN_REVIEW)


# Convenience functions for BlackBox5
def execute_blackbox5_plan(
    plan_name: str,
    description: str,
    vibe_kanban_url: str = "http://127.0.0.1:57276",
    project_id: str = "48ec7737-b706-4817-b86c-5786163a0139",
    repo_id: str = "b5b86bc2-fbfb-4276-b15e-01496d647a81"
) -> Dict[str, Any]:
    """
    Execute a single BlackBox5 plan with Vibe Kanban tracking

    This is the main entry point for BlackBox5 agents.

    Example:
        result = execute_blackbox5_plan(
            plan_name="PLAN-008: Fix API Mismatches",
            description="Fix the critical API parameter mismatches in main.py..."
        )
    """
    orchestrator = BlackBox5Orchestrator(vibe_kanban_url, project_id, repo_id)
    return orchestrator.execute_plan(plan_name, description)


def execute_blackbox5_wave(
    plans: List[Dict[str, str]],
    vibe_kanban_url: str = "http://127.0.0.1:57276",
    project_id: str = "48ec7737-b706-4817-b86c-5786163a0139",
    repo_id: str = "b5b86bc2-fbfb-4276-b15e-01496d647a81"
) -> List[Dict[str, Any]]:
    """
    Execute multiple BlackBox5 plans in parallel (Wave execution)

    Example:
        plans = [
            {"name": "PLAN-008: Fix API", "description": "..."},
            {"name": "PLAN-007: Compression", "description": "..."},
            {"name": "PLAN-010: Dependencies", "description": "..."}
        ]
        results = execute_blackbox5_wave(plans)
    """
    orchestrator = BlackBox5Orchestrator(vibe_kanban_url, project_id, repo_id)
    return orchestrator.execute_parallel_plans(plans)


if __name__ == "__main__":
    # Example: Execute Wave 0
    wave0_plans = [
        {
            "name": "PLAN-008: Fix Critical API Mismatches",
            "description": """
Fix the 3 critical API parameter mismatches in main.py:
1. Task(task_id=...) → Task(id=...)
2. execute_wave_based() → execute_workflow()
3. AgentTask(id=...) → AgentTask(task_id=...)

See: blackbox5/6-roadmap/03-planned/PLAN-008-fix-critical-api-mismatches.md
"""
        },
        {
            "name": "PLAN-007: Enable 90% LLMLingua Compression",
            "description": """
Enable HuggingFace auth for LLMLingua to achieve 90% cost reduction.

Steps:
1. Create HuggingFace account
2. Login: huggingface-cli login
3. Accept license at https://huggingface.co/microsoft/llmlingua-2-x2
4. Verify import works

See: blackbox5/6-roadmap/03-planned/PLAN-007-enable-90-compression.md
"""
        },
        {
            "name": "PLAN-010: Add Missing Dependencies",
            "description": """
Add missing packages to requirements.txt:
- redis>=5.0.0
- pyyaml>=6.0.1
- chromadb>=0.4.22
- neo4j>=5.15.0

See: blackbox5/6-roadmap/03-planned/PLAN-010-add-missing-dependencies.md
"""
        },
        {
            "name": "PLAN-009: Fix Statistics Coroutine Warnings",
            "description": """
Fix get_statistics() async issues:
1. Make get_statistics() async
2. Add await to async calls
3. Update all callers

See: blackbox5/6-roadmap/03-planned/PLAN-009-fix-statistics-coroutine.md
"""
        },
        {
            "name": "PLAN-005: Initialize Vibe Kanban Database",
            "description": """
Initialize Vibe Kanban database for BlackBox5 workflow.

Steps:
1. Locate installation
2. Run migrations
3. Create project
4. Test API
5. Create columns

See: blackbox5/6-roadmap/03-planned/PLAN-005-initialize-vibe-kanban.md
"""
        }
    ]

    print("🚀 BlackBox5 + Vibe Kanban Integration")
    print("=" * 60)
    print("Executing Wave 0 plans in parallel...")
    print()

    results = execute_blackbox5_wave(wave0_plans)

    print("\n" + "=" * 60)
    print(f"✅ Launched {len(results)} parallel agents")
    print(f"📊 Monitor at: http://127.0.0.1:57276")
    print(f"🔑 Project ID: 48ec7737-b706-4817-b86c-5786163a0139")
