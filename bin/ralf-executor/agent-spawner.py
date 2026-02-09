#!/usr/bin/env python3
"""
BB5 Agent Spawner Module
Handles spawning BB5 Core Agent Team members using the Task tool.
"""

import os
import sys
import json
import time
import uuid
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass, field
from enum import Enum
import subprocess
import threading
import queue

# BB5 Configuration - auto-detect or use environment variable
def _get_bb5_dir() -> Path:
    """Get BB5 directory from environment or auto-detect."""
    if "BB5_DIR" in os.environ:
        return Path(os.environ["BB5_DIR"])

    # Auto-detect: look for .blackbox5 in home directory
    home_bb5 = Path.home() / ".blackbox5"
    if home_bb5.exists():
        return home_bb5

    # Check current working directory
    cwd = Path.cwd()
    if (cwd / ".claude").exists() or (cwd / "5-project-memory").exists():
        return cwd

    # Check parent directories
    for parent in cwd.parents:
        if (parent / ".claude").exists() or (parent / "5-project-memory").exists():
            return parent

    # Default fallback
    return Path("/opt/blackbox5")


BB5_DIR = _get_bb5_dir()
AGENTS_DIR = BB5_DIR / ".claude" / "agents"
RUNS_DIR = BB5_DIR / "5-project-memory" / "blackbox5" / ".autonomous" / "runs"
COMMUNICATIONS_DIR = BB5_DIR / "5-project-memory" / "blackbox5" / ".autonomous" / "agents" / "communications"

# Agent Configuration
AGENT_CONFIG = {
    "bb5-context-collector": {
        "model": "claude-opus-4-6",
        "timeout": 600,  # 10 minutes
        "max_retries": 2,
        "description": "Gathers comprehensive context about BB5's current state",
    },
    "bb5-planner": {
        "model": "claude-opus-4-6",
        "timeout": 900,  # 15 minutes
        "max_retries": 2,
        "description": "Creates actionable implementation plans with tasks and dependencies",
    },
    "bb5-verifier": {
        "model": "claude-opus-4-6",
        "timeout": 600,  # 10 minutes
        "max_retries": 1,
        "description": "Validates task completion against requirements",
    },
    "bb5-scribe": {
        "model": "claude-opus-4-6",
        "timeout": 300,  # 5 minutes
        "max_retries": 2,
        "description": "Documents thinking, decisions, and learnings",
    },
    "bb5-executor": {
        "model": "claude-opus-4-6",
        "timeout": 1800,  # 30 minutes
        "max_retries": 1,
        "description": "Executes tasks and implements solutions",
    },
}


class AgentStatus(Enum):
    """Status of an agent execution."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    RETRYING = "retrying"


@dataclass
class AgentResult:
    """Result from an agent execution."""
    agent_id: str
    agent_type: str
    status: AgentStatus
    output: str = ""
    error: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    artifacts: List[str] = field(default_factory=list)

    @property
    def duration_seconds(self) -> float:
        """Calculate execution duration."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0

    @property
    def success(self) -> bool:
        """Check if execution was successful."""
        return self.status == AgentStatus.COMPLETED and not self.error


class AgentSpawner:
    """Spawns and manages BB5 agent team members."""

    def __init__(self, run_folder: Optional[Path] = None):
        self.run_folder = run_folder or self._create_run_folder()
        self.active_agents: Dict[str, AgentResult] = {}
        self.agent_lock = threading.Lock()
        self._ensure_directories()

    def _create_run_folder(self) -> Path:
        """Create a new run folder for this spawner session."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_id = f"spawner-{timestamp}"
        run_path = RUNS_DIR / run_id
        run_path.mkdir(parents=True, exist_ok=True)
        return run_path

    def _ensure_directories(self):
        """Ensure required directories exist."""
        COMMUNICATIONS_DIR.mkdir(parents=True, exist_ok=True)
        (self.run_folder / "agents").mkdir(parents=True, exist_ok=True)

    def _generate_agent_id(self, agent_type: str) -> str:
        """Generate a unique agent ID."""
        timestamp = datetime.now().strftime("%H%M%S")
        short_uuid = str(uuid.uuid4())[:8]
        return f"{agent_type}-{timestamp}-{short_uuid}"

    def _read_agent_definition(self, agent_type: str) -> Optional[str]:
        """Read the agent definition file."""
        agent_file = AGENTS_DIR / f"{agent_type}.md"
        if agent_file.exists():
            return agent_file.read_text()
        return None

    def _build_agent_prompt(self, agent_type: str, context: Dict[str, Any]) -> str:
        """Build the full prompt for an agent."""
        agent_def = self._read_agent_definition(agent_type) or ""

        # Build context section
        context_yaml = yaml.dump(context, default_flow_style=False)

        prompt = f"""{agent_def}

---

## Task Context

```yaml
{context_yaml}
```

## Your Mission

You are being spawned as part of the BB5 autonomous execution system.
Execute your responsibilities according to your agent definition above.

### Critical Instructions:
1. Read all provided context carefully
2. Execute your specific responsibilities
3. Document your work in the run folder
4. Return results in the specified format
5. Signal completion with: <agent_complete status="COMPLETE|PARTIAL|FAILED" />

### Output Location:
Run folder: {self.run_folder}
Agent artifacts: {self.run_folder}/agents/

Begin execution now.
"""
        return prompt

    def _spawn_agent_task(
        self,
        agent_type: str,
        agent_id: str,
        prompt: str,
        timeout: int,
    ) -> AgentResult:
        """
        Spawn an agent using the Task tool (simulated via subprocess for now).
        In production, this would use the actual Task tool API.
        """
        result = AgentResult(
            agent_id=agent_id,
            agent_type=agent_type,
            status=AgentStatus.RUNNING,
            start_time=datetime.now(),
        )

        # Create agent working directory
        agent_dir = self.run_folder / "agents" / agent_id
        agent_dir.mkdir(parents=True, exist_ok=True)

        # Write prompt to file
        prompt_file = agent_dir / "prompt.md"
        prompt_file.write_text(prompt)

        # Write spawn signal
        spawn_signal = {
            "agent_id": agent_id,
            "agent_type": agent_type,
            "spawned_at": datetime.now().isoformat(),
            "status": "running",
            "run_folder": str(self.run_folder),
            "agent_dir": str(agent_dir),
        }
        (agent_dir / "signal.yaml").write_text(yaml.dump(spawn_signal))

        # For now, simulate the Task tool with a marker file
        # In production, this would call the actual Task tool:
        # result = task(prompt=prompt, subagent_type=agent_type, timeout=timeout)

        # Create a completion marker that external systems can check
        completion_file = agent_dir / "completion.json"
        completion_file.write_text(json.dumps({
            "agent_id": agent_id,
            "status": "pending",
            "message": "Agent spawned, awaiting completion"
        }))

        # Store in active agents
        with self.agent_lock:
            self.active_agents[agent_id] = result

        return result

    def _wait_for_completion(
        self,
        agent_id: str,
        timeout: int,
        poll_interval: float = 1.0,
    ) -> AgentResult:
        """Wait for an agent to complete."""
        result = self.active_agents.get(agent_id)
        if not result:
            raise ValueError(f"Unknown agent: {agent_id}")

        agent_dir = self.run_folder / "agents" / agent_id
        completion_file = agent_dir / "completion.json"

        start_time = time.time()
        while (time.time() - start_time) < timeout:
            # Check for completion
            if completion_file.exists():
                try:
                    completion_data = json.loads(completion_file.read_text())
                    status = completion_data.get("status", "pending")

                    if status == "COMPLETE":
                        result.status = AgentStatus.COMPLETED
                        result.output = completion_data.get("output", "")
                        result.artifacts = completion_data.get("artifacts", [])
                        break
                    elif status == "FAILED":
                        result.status = AgentStatus.FAILED
                        result.error = completion_data.get("error", "Unknown error")
                        break
                    elif status == "PARTIAL":
                        result.status = AgentStatus.COMPLETED  # Partial is still completed
                        result.output = completion_data.get("output", "")
                        result.metadata["partial"] = True
                        break

                except (json.JSONDecodeError, KeyError) as e:
                    result.error = f"Error reading completion: {e}"
                    result.status = AgentStatus.FAILED
                    break

            time.sleep(poll_interval)
        else:
            # Timeout reached
            result.status = AgentStatus.TIMEOUT
            result.error = f"Agent timed out after {timeout} seconds"

        result.end_time = datetime.now()

        # Update signal file
        signal_file = agent_dir / "signal.yaml"
        if signal_file.exists():
            signal = yaml.safe_load(signal_file.read_text())
            signal["status"] = result.status.value
            signal["completed_at"] = datetime.now().isoformat()
            signal["duration"] = result.duration_seconds
            signal_file.write_text(yaml.dump(signal))

        return result

    def spawn_context_collector(
        self,
        task_id: str,
        task_path: Optional[str] = None,
        run_folder: Optional[str] = None,
        wait: bool = True,
    ) -> AgentResult:
        """
        Spawn the bb5-context-collector agent.

        Args:
            task_id: The task ID to gather context for
            task_path: Path to the task file
            run_folder: Override run folder (uses spawner's run folder if not provided)
            wait: Whether to wait for completion

        Returns:
            AgentResult with context gathering results
        """
        agent_type = "bb5-context-collector"
        agent_id = self._generate_agent_id(agent_type)
        config = AGENT_CONFIG[agent_type]

        context = {
            "task_id": task_id,
            "task_path": task_path,
            "run_folder": run_folder or str(self.run_folder),
            "agent_id": agent_id,
            "spawned_at": datetime.now().isoformat(),
            "bb5_dir": str(BB5_DIR),
        }

        prompt = self._build_agent_prompt(agent_type, context)

        result = self._spawn_agent_task(
            agent_type=agent_type,
            agent_id=agent_id,
            prompt=prompt,
            timeout=config["timeout"],
        )

        if wait:
            result = self._wait_for_completion(agent_id, config["timeout"])

        return result

    def spawn_planner(
        self,
        task_id: str,
        context: Dict[str, Any],
        run_folder: Optional[str] = None,
        wait: bool = True,
    ) -> AgentResult:
        """
        Spawn the bb5-planner agent for complex tasks.

        Args:
            task_id: The task ID to plan for
            context: Context dictionary with requirements, constraints, etc.
            run_folder: Override run folder
            wait: Whether to wait for completion

        Returns:
            AgentResult with planning results
        """
        agent_type = "bb5-planner"
        agent_id = self._generate_agent_id(agent_type)
        config = AGENT_CONFIG[agent_type]

        planner_context = {
            "task_id": task_id,
            "run_folder": run_folder or str(self.run_folder),
            "agent_id": agent_id,
            "spawned_at": datetime.now().isoformat(),
            "bb5_dir": str(BB5_DIR),
            "context": context,
        }

        prompt = self._build_agent_prompt(agent_type, planner_context)

        result = self._spawn_agent_task(
            agent_type=agent_type,
            agent_id=agent_id,
            prompt=prompt,
            timeout=config["timeout"],
        )

        if wait:
            result = self._wait_for_completion(agent_id, config["timeout"])

        return result

    def spawn_verifier(
        self,
        task_id: str,
        run_folder: Optional[str] = None,
        strictness: str = "standard",
        wait: bool = True,
    ) -> AgentResult:
        """
        Spawn the bb5-verifier agent to check task completion.

        Args:
            task_id: The task ID to verify
            run_folder: Run folder containing task artifacts
            strictness: Verification strictness (lenient|standard|strict)
            wait: Whether to wait for completion

        Returns:
            AgentResult with verification results
        """
        agent_type = "bb5-verifier"
        agent_id = self._generate_agent_id(agent_type)
        config = AGENT_CONFIG[agent_type]

        context = {
            "task_id": task_id,
            "run_folder": run_folder or str(self.run_folder),
            "agent_id": agent_id,
            "spawned_at": datetime.now().isoformat(),
            "bb5_dir": str(BB5_DIR),
            "strictness": strictness,
        }

        prompt = self._build_agent_prompt(agent_type, context)

        result = self._spawn_agent_task(
            agent_type=agent_type,
            agent_id=agent_id,
            prompt=prompt,
            timeout=config["timeout"],
        )

        if wait:
            result = self._wait_for_completion(agent_id, config["timeout"])

        return result

    def spawn_scribe(
        self,
        run_folder: Optional[str] = None,
        document_type: str = "all",
        wait: bool = False,
    ) -> AgentResult:
        """
        Spawn the bb5-scribe agent for documentation.

        Args:
            run_folder: Run folder to document
            document_type: Type of documentation (thoughts|decisions|learnings|all)
            wait: Whether to wait for completion

        Returns:
            AgentResult with documentation results
        """
        agent_type = "bb5-scribe"
        agent_id = self._generate_agent_id(agent_type)
        config = AGENT_CONFIG[agent_type]

        context = {
            "run_folder": run_folder or str(self.run_folder),
            "agent_id": agent_id,
            "spawned_at": datetime.now().isoformat(),
            "bb5_dir": str(BB5_DIR),
            "document_type": document_type,
        }

        prompt = self._build_agent_prompt(agent_type, context)

        result = self._spawn_agent_task(
            agent_type=agent_type,
            agent_id=agent_id,
            prompt=prompt,
            timeout=config["timeout"],
        )

        if wait:
            result = self._wait_for_completion(agent_id, config["timeout"])

        return result

    def spawn_executor(
        self,
        task_id: str,
        plan: Dict[str, Any],
        run_folder: Optional[str] = None,
        wait: bool = True,
    ) -> AgentResult:
        """
        Spawn the bb5-executor agent to execute a task.

        Args:
            task_id: The task ID to execute
            plan: Execution plan with steps and requirements
            run_folder: Override run folder
            wait: Whether to wait for completion

        Returns:
            AgentResult with execution results
        """
        agent_type = "bb5-executor"
        agent_id = self._generate_agent_id(agent_type)
        config = AGENT_CONFIG[agent_type]

        context = {
            "task_id": task_id,
            "run_folder": run_folder or str(self.run_folder),
            "agent_id": agent_id,
            "spawned_at": datetime.now().isoformat(),
            "bb5_dir": str(BB5_DIR),
            "plan": plan,
        }

        prompt = self._build_agent_prompt(agent_type, context)

        result = self._spawn_agent_task(
            agent_type=agent_type,
            agent_id=agent_id,
            prompt=prompt,
            timeout=config["timeout"],
        )

        if wait:
            result = self._wait_for_completion(agent_id, config["timeout"])

        return result

    def wait_for_agent(self, agent_id: str, timeout: Optional[int] = None) -> AgentResult:
        """
        Wait for a specific agent to complete.

        Args:
            agent_id: The agent ID to wait for
            timeout: Maximum time to wait (uses agent config if not provided)

        Returns:
            AgentResult with final status
        """
        result = self.active_agents.get(agent_id)
        if not result:
            raise ValueError(f"Unknown agent: {agent_id}")

        if timeout is None:
            agent_type = result.agent_type
            timeout = AGENT_CONFIG.get(agent_type, {}).get("timeout", 600)

        return self._wait_for_completion(agent_id, timeout)

    def wait_for_all(self, timeout: Optional[int] = None) -> Dict[str, AgentResult]:
        """
        Wait for all active agents to complete.

        Args:
            timeout: Maximum time to wait per agent

        Returns:
            Dictionary of agent_id -> AgentResult
        """
        results = {}
        for agent_id in list(self.active_agents.keys()):
            results[agent_id] = self.wait_for_agent(agent_id, timeout)
        return results

    def get_agent_status(self, agent_id: str) -> Optional[AgentStatus]:
        """Get the current status of an agent."""
        result = self.active_agents.get(agent_id)
        return result.status if result else None

    def retry_agent(self, agent_id: str) -> AgentResult:
        """
        Retry a failed agent.

        Args:
            agent_id: The failed agent ID to retry

        Returns:
            New AgentResult
        """
        old_result = self.active_agents.get(agent_id)
        if not old_result:
            raise ValueError(f"Unknown agent: {agent_id}")

        if old_result.status not in (AgentStatus.FAILED, AgentStatus.TIMEOUT):
            raise ValueError(f"Cannot retry agent with status {old_result.status}")

        agent_type = old_result.agent_type
        config = AGENT_CONFIG[agent_type]

        # Generate new agent ID for retry
        new_agent_id = self._generate_agent_id(f"{agent_type}-retry")

        # Read the original prompt
        agent_dir = self.run_folder / "agents" / agent_id
        prompt_file = agent_dir / "prompt.md"
        prompt = prompt_file.read_text() if prompt_file.exists() else ""

        # Add retry context
        retry_context = f"""

---

## Retry Context

This is a retry of agent {agent_id}.
Previous attempt failed with: {old_result.error}
Retry number: 1

Please review the previous failure and adjust your approach accordingly.
"""
        prompt += retry_context

        result = self._spawn_agent_task(
            agent_type=agent_type,
            agent_id=new_agent_id,
            prompt=prompt,
            timeout=config["timeout"],
        )

        return result

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of all agent activity."""
        total = len(self.active_agents)
        completed = sum(1 for r in self.active_agents.values() if r.status == AgentStatus.COMPLETED)
        failed = sum(1 for r in self.active_agents.values() if r.status == AgentStatus.FAILED)
        pending = sum(1 for r in self.active_agents.values() if r.status == AgentStatus.PENDING)
        running = sum(1 for r in self.active_agents.values() if r.status == AgentStatus.RUNNING)

        return {
            "total_agents": total,
            "completed": completed,
            "failed": failed,
            "pending": pending,
            "running": running,
            "success_rate": (completed / total * 100) if total > 0 else 0,
            "run_folder": str(self.run_folder),
        }


def spawn_context_collector(
    task_id: str,
    task_path: Optional[str] = None,
    run_folder: Optional[str] = None,
) -> AgentResult:
    """
    Convenience function to spawn a context collector.

    Usage:
        result = spawn_context_collector("TASK-001", "/path/to/task.md")
        print(result.output)
    """
    spawner = AgentSpawner(run_folder=Path(run_folder) if run_folder else None)
    return spawner.spawn_context_collector(task_id, task_path, run_folder)


def spawn_planner(
    task_id: str,
    context: Dict[str, Any],
    run_folder: Optional[str] = None,
) -> AgentResult:
    """Convenience function to spawn a planner."""
    spawner = AgentSpawner(run_folder=Path(run_folder) if run_folder else None)
    return spawner.spawn_planner(task_id, context, run_folder)


def spawn_verifier(
    task_id: str,
    run_folder: Optional[str] = None,
    strictness: str = "standard",
) -> AgentResult:
    """Convenience function to spawn a verifier."""
    spawner = AgentSpawner(run_folder=Path(run_folder) if run_folder else None)
    return spawner.spawn_verifier(task_id, run_folder, strictness)


def spawn_scribe(
    run_folder: Optional[str] = None,
    document_type: str = "all",
) -> AgentResult:
    """Convenience function to spawn a scribe."""
    spawner = AgentSpawner(run_folder=Path(run_folder) if run_folder else None)
    return spawner.spawn_scribe(run_folder, document_type)


def wait_for_agent(agent_id: str, run_folder: Optional[str] = None) -> AgentResult:
    """Convenience function to wait for an agent."""
    spawner = AgentSpawner(run_folder=Path(run_folder) if run_folder else None)
    return spawner.wait_for_agent(agent_id)


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="BB5 Agent Spawner")
    parser.add_argument("command", choices=[
        "context-collector",
        "planner",
        "verifier",
        "scribe",
        "status",
        "wait",
    ])
    parser.add_argument("--task-id", help="Task ID")
    parser.add_argument("--task-path", help="Path to task file")
    parser.add_argument("--run-folder", help="Run folder path")
    parser.add_argument("--agent-id", help="Agent ID (for wait/status)")
    parser.add_argument("--strictness", default="standard", help="Verifier strictness")
    parser.add_argument("--document-type", default="all", help="Scribe document type")
    parser.add_argument("--context-file", help="JSON file with planner context")

    args = parser.parse_args()

    spawner = AgentSpawner(run_folder=Path(args.run_folder) if args.run_folder else None)

    if args.command == "context-collector":
        if not args.task_id:
            print("Error: --task-id required")
            sys.exit(1)
        result = spawner.spawn_context_collector(
            task_id=args.task_id,
            task_path=args.task_path,
            run_folder=args.run_folder,
        )
        print(json.dumps({
            "agent_id": result.agent_id,
            "status": result.status.value,
            "success": result.success,
            "output": result.output,
            "error": result.error,
        }, indent=2))

    elif args.command == "planner":
        if not args.task_id:
            print("Error: --task-id required")
            sys.exit(1)
        context = {}
        if args.context_file:
            context = json.loads(Path(args.context_file).read_text())
        result = spawner.spawn_planner(
            task_id=args.task_id,
            context=context,
            run_folder=args.run_folder,
        )
        print(json.dumps({
            "agent_id": result.agent_id,
            "status": result.status.value,
            "success": result.success,
            "output": result.output,
        }, indent=2))

    elif args.command == "verifier":
        if not args.task_id:
            print("Error: --task-id required")
            sys.exit(1)
        result = spawner.spawn_verifier(
            task_id=args.task_id,
            run_folder=args.run_folder,
            strictness=args.strictness,
        )
        print(json.dumps({
            "agent_id": result.agent_id,
            "status": result.status.value,
            "success": result.success,
            "output": result.output,
        }, indent=2))

    elif args.command == "scribe":
        result = spawner.spawn_scribe(
            run_folder=args.run_folder,
            document_type=args.document_type,
        )
        print(json.dumps({
            "agent_id": result.agent_id,
            "status": result.status.value,
            "success": result.success,
        }, indent=2))

    elif args.command == "status":
        summary = spawner.get_summary()
        print(json.dumps(summary, indent=2))

    elif args.command == "wait":
        if not args.agent_id:
            print("Error: --agent-id required")
            sys.exit(1)
        result = spawner.wait_for_agent(args.agent_id)
        print(json.dumps({
            "agent_id": result.agent_id,
            "status": result.status.value,
            "success": result.success,
            "duration": result.duration_seconds,
        }, indent=2))
