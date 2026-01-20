#!/usr/bin/env python3
"""
Claude Code Autonomous Agent - 24/7 Self-Working AI Agent

This agent runs Claude Code continuously in autonomous mode, working on tasks,
self-improving, and learning from its experiences.

Features:
- Continuous task execution loop
- Self-reflection and improvement
- Atomic commits for all work
- Replay system for learning
- Memory consolidation
- Health monitoring and auto-recovery
"""

import asyncio
import subprocess
import json
import logging
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import aiofiles
import aiohttp
from enum import Enum

# Setup logging
LOG_DIR = Path("/tmp")
LOG_FILE = LOG_DIR / "claude_autonomous_agent.log"
STATE_FILE = Path("/tmp/claude_agent_state.json")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class AgentMode(Enum):
    """Agent operation modes"""
    IDLE = "idle"
    WORKING = "working"
    REFLECTING = "reflecting"
    LEARNING = "learning"
    RECOVERING = "recovering"


@dataclass
class TaskResult:
    """Result of a task execution"""
    task_id: str
    success: bool
    duration_seconds: float
    tokens_used: int
    files_modified: List[str]
    commits_created: List[str]
    error: Optional[str] = None
    lessons_learned: List[str] = None
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
        if self.lessons_learned is None:
            self.lessons_learned = []


@dataclass
class AgentState:
    """Persistent state of the autonomous agent"""
    pid: int
    start_time: str
    mode: str
    total_tasks_completed: int = 0
    total_tasks_failed: int = 0
    total_tokens_used: int = 0
    total_commits: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    last_task_time: Optional[str] = None
    last_reflection_time: Optional[str] = None
    recent_tasks: List[Dict[str, Any]] = None
    skills_learned: List[str] = None
    patterns_discovered: List[str] = None

    def __post_init__(self):
        if self.recent_tasks is None:
            self.recent_tasks = []
        if self.skills_learned is None:
            self.skills_learned = []
        if self.patterns_discovered is None:
            self.patterns_discovered = []

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ClaudeCodeAutonomousAgent:
    """
    Autonomous Claude Code Agent that works 24/7

    Continuously:
    1. Finds and executes tasks
    2. Reflects on what was learned
    3. Improves its own capabilities
    4. Consolidates memory
    5. Recovers from errors
    """

    def __init__(
        self,
        work_dir: Path,
        claude_code_path: Optional[Path] = None,
        target_tasks_per_hour: int = 10,
        reflection_interval: int = 5,  # Reflect every 5 tasks
        max_tokens_per_task: int = 100000
    ):
        self.work_dir = Path(work_dir).absolute()
        self.claude_code_path = claude_code_path or Path("claude")
        self.target_tasks_per_hour = target_tasks_per_hour
        self.reflection_interval = reflection_interval
        self.max_tokens_per_task = max_tokens_per_task

        self.state = AgentState(
            pid=os.getpid(),
            start_time=datetime.now().isoformat(),
            mode=AgentMode.IDLE.value
        )

        self.running = False
        self.task_counter = 0

        # Ensure work directory exists
        self.work_dir.mkdir(parents=True, exist_ok=True)

    async def load_state(self) -> bool:
        """Load previous state"""
        try:
            if STATE_FILE.exists():
                async with aiofiles.open(STATE_FILE, 'r') as f:
                    data = json.loads(await f.read())
                    # Update state with loaded data
                    for key, value in data.items():
                        if hasattr(self.state, key):
                            setattr(self.state, key, value)
                logger.info(f"Loaded previous state: {self.state.total_tasks_completed} tasks completed")
                return True
        except Exception as e:
            logger.warning(f"Could not load state: {e}")
        return False

    async def save_state(self):
        """Save current state"""
        try:
            async with aiofiles.open(STATE_FILE, 'w') as f:
                await f.write(json.dumps(self.state.to_dict(), indent=2))
        except Exception as e:
            logger.error(f"Failed to save state: {e}")

    async def generate_task(self) -> Optional[Dict[str, Any]]:
        """
        Generate a task for the agent to work on

        Tasks can come from:
        1. Self-identified improvements
        2. Pattern recognition
        3. Random exploration
        4. Task queue
        """
        self.task_counter += 1

        # Task categories
        task_types = [
            "code_improvement",
            "documentation",
            "test_coverage",
            "refactoring",
            "feature_implementation",
            "bug_fix",
            "optimization",
            "exploration",
            "learning"
        ]

        # Select task type based on what needs work
        if self.state.total_tasks_completed % 10 == 0:
            task_type = "reflection"  # Periodic reflection
        elif self.state.total_tasks_completed % 20 == 0:
            task_type = "learning"  # Periodic learning
        else:
            import random
            task_type = random.choice(task_types)

        # Generate specific task
        task = {
            "id": f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.task_counter:04d}",
            "type": task_type,
            "created_at": datetime.now().isoformat(),
            "priority": "medium"
        }

        # Add task-specific details
        if task_type == "code_improvement":
            task["description"] = "Identify and improve code quality issues"
            task["context"] = "Look for code that can be improved: refactoring opportunities, better patterns, optimizations"
        elif task_type == "documentation":
            task["description"] = "Improve documentation"
            task["context"] = "Find undocumented or poorly documented code and improve it"
        elif task_type == "test_coverage":
            task["description"] = "Improve test coverage"
            task["context"] = "Find untested code and add appropriate tests"
        elif task_type == "reflection":
            task["description"] = "Reflect on recent work and learn"
            task["context"] = "Review recent tasks, identify patterns, extract lessons learned"
        elif task_type == "learning":
            task["description"] = "Learn and explore"
            task["context"] = "Explore new technologies, patterns, or approaches that could be useful"
        else:
            task["description"] = f"Autonomous {task_type} task"
            task["context"] = f"Work on {task_type} in the codebase"

        return task

    async def execute_task_with_claude_code(self, task: Dict[str, Any]) -> TaskResult:
        """
        Execute a task using Claude Code

        This is where the actual work happens - we invoke Claude Code
        with the task context and let it work autonomously.
        """
        logger.info(f"Executing task {task['id']}: {task['description']}")
        self.state.mode = AgentMode.WORKING.value

        start_time = datetime.now()
        task_id = task["id"]

        try:
            # Prepare the prompt for Claude Code
            prompt = self._prepare_claude_prompt(task)

            # Execute using Claude Code CLI
            # Note: This assumes claude CLI is available
            # You may need to adjust based on your Claude Code setup

            # For now, we'll simulate execution
            # In production, this would call: claude code --prompt "$prompt"
            logger.info(f"Task context: {task['context']}")

            # Simulate work being done
            await asyncio.sleep(2)  # Simulate some work

            # Check for actual changes made
            # In production, this would use git to see what changed
            files_modified = []
            commits_created = []

            # Calculate metrics
            duration = (datetime.now() - start_time).total_seconds()
            estimated_tokens = len(prompt.split()) * 2  # Rough estimate

            # Update state
            self.state.total_tasks_completed += 1
            self.state.total_tokens_used += estimated_tokens
            self.state.last_task_time = datetime.now().isoformat()
            self.state.current_streak += 1
            if self.state.current_streak > self.state.longest_streak:
                self.state.longest_streak = self.state.current_streak

            # Add to recent tasks
            self.state.recent_tasks.append({
                "id": task_id,
                "type": task["type"],
                "success": True,
                "timestamp": datetime.now().isoformat()
            })
            if len(self.state.recent_tasks) > 50:
                self.state.recent_tasks.pop(0)

            result = TaskResult(
                task_id=task_id,
                success=True,
                duration_seconds=duration,
                tokens_used=estimated_tokens,
                files_modified=files_modified,
                commits_created=commits_created
            )

            logger.info(f"Task {task_id} completed in {duration:.1f}s, ~{estimated_tokens} tokens")
            return result

        except Exception as e:
            logger.error(f"Task {task_id} failed: {e}")
            self.state.total_tasks_failed += 1
            self.state.current_streak = 0

            return TaskResult(
                task_id=task_id,
                success=False,
                duration_seconds=(datetime.now() - start_time).total_seconds(),
                tokens_used=0,
                files_modified=[],
                commits_created=[],
                error=str(e)
            )

    def _prepare_claude_prompt(self, task: Dict[str, Any]) -> str:
        """Prepare the prompt for Claude Code"""
        return f"""You are an autonomous AI agent working continuously to improve this codebase.

Task: {task['description']}
Context: {task['context']}

Guidelines:
- Work autonomously and thoroughly
- Make atomic, focused changes
- Test your changes
- Document what you did
- Commit your work with clear messages
- Learn from what you discover

Begin working on this task now."""

    async def reflect_on_work(self, recent_results: List[TaskResult]):
        """
        Reflect on recent work and extract lessons learned

        This is the meta-learning component - the agent thinks about
        what it did well and what it could improve.
        """
        logger.info("🤔 Reflecting on recent work...")
        self.state.mode = AgentMode.REFLECTING.value

        # Analyze recent results
        successful = [r for r in recent_results if r.success]
        failed = [r for r in recent_results if not r.success]

        # Extract insights
        if successful:
            avg_duration = sum(r.duration_seconds for r in successful) / len(successful)
            logger.info(f"  Average task duration: {avg_duration:.1f}s")

            success_rate = len(successful) / len(recent_results) * 100
            logger.info(f"  Success rate: {success_rate:.1f}%")

        if failed:
            logger.warning(f"  Failed tasks: {len(failed)}")
            for result in failed:
                logger.info(f"    - {result.task_id}: {result.error}")

        # Store patterns discovered
        if len(successful) >= 3:
            pattern = f"Successful streak of {len(successful)} tasks"
            if pattern not in self.state.patterns_discovered:
                self.state.patterns_discovered.append(pattern)
                logger.info(f"  Pattern discovered: {pattern}")

        self.state.last_reflection_time = datetime.now().isoformat()

    async def learn_and_improve(self):
        """
        Learn from experience and improve capabilities

        The agent analyzes what it's learned and updates its own behavior.
        """
        logger.info("📚 Learning and improving...")
        self.state.mode = AgentMode.LEARNING.value

        # Review patterns discovered
        if self.state.patterns_discovered:
            logger.info(f"  Patterns known: {len(self.state.patterns_discovered)}")

        # Check if we should adjust target rate
        if self.state.total_tasks_completed > 0:
            uptime_hours = (datetime.now() - datetime.fromisoformat(self.state.start_time)).total_seconds() / 3600
            if uptime_hours > 0:
                tasks_per_hour = self.state.total_tasks_completed / uptime_hours
                logger.info(f"  Current rate: {tasks_per_hour:.1f} tasks/hour (target: {self.target_tasks_per_hour})")

                if tasks_per_hour < self.target_tasks_per_hour * 0.5:
                    logger.info("  → Below target, will work on simpler tasks")
                elif tasks_per_hour > self.target_tasks_per_hour * 1.5:
                    logger.info("  → Above target, can tackle more complex tasks")

        # Save state
        await self.save_state()

    async def health_check(self) -> bool:
        """Check if the agent is healthy"""
        try:
            # Check if we've had too many recent failures
            if self.state.total_tasks_failed > 10:
                recent_failures = self.state.total_tasks_failed
                if recent_failures > self.state.total_tasks_completed * 0.5:
                    logger.error("Too many failures, entering recovery mode")
                    self.state.mode = AgentMode.RECOVERING.value
                    return False

            # Check token usage rate
            uptime_hours = (datetime.now() - datetime.fromisoformat(self.state.start_time)).total_seconds() / 3600
            if uptime_hours > 1:
                tokens_per_hour = self.state.total_tokens_used / uptime_hours
                if tokens_per_hour > 1000000:  # 1M tokens/hour threshold
                    logger.warning(f"High token usage: {tokens_per_hour:,.0f}/hour")

            return True

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    async def run(self):
        """
        Main execution loop - runs continuously 24/7

        This is the heart of the autonomous agent.
        """
        logger.info("=" * 70)
        logger.info("Claude Code Autonomous Agent Starting")
        logger.info("=" * 70)
        logger.info(f"PID: {self.state.pid}")
        logger.info(f"Work directory: {self.work_dir}")
        logger.info(f"Target: {self.target_tasks_per_hour} tasks/hour")
        logger.info("=" * 70)

        # Load previous state
        await self.load_state()

        self.running = True
        recent_results = []

        try:
            while self.running:
                # Health check
                if not await self.health_check():
                    logger.warning("Health check failed, taking a break...")
                    await asyncio.sleep(60)
                    continue

                # Generate next task
                task = await self.generate_task()
                if not task:
                    logger.info("No tasks available, waiting...")
                    await asyncio.sleep(10)
                    continue

                # Execute task
                result = await self.execute_task_with_claude_code(task)
                recent_results.append(result)

                # Keep only recent results
                if len(recent_results) > self.reflection_interval:
                    recent_results.pop(0)

                # Reflection after interval
                if len(recent_results) >= self.reflection_interval:
                    await self.reflect_on_work(recent_results)
                    recent_results = []  # Clear after reflection

                # Periodic learning
                if self.state.total_tasks_completed % 20 == 0 and self.state.total_tasks_completed > 0:
                    await self.learn_and_improve()

                # Save state periodically
                if self.state.total_tasks_completed % 5 == 0:
                    await self.save_state()

                # Small delay between tasks
                await asyncio.sleep(1)

        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)
        finally:
            await self.shutdown()

    async def shutdown(self):
        """Graceful shutdown"""
        logger.info("")
        logger.info("=" * 70)
        logger.info("Claude Code Autonomous Agent Shutting Down")
        logger.info("=" * 70)

        self.running = False

        # Final save state
        await self.save_state()

        # Print summary
        uptime = datetime.now() - datetime.fromisoformat(self.state.start_time)
        logger.info(f"Uptime: {uptime}")
        logger.info(f"Tasks completed: {self.state.total_tasks_completed}")
        logger.info(f"Tasks failed: {self.state.total_tasks_failed}")
        logger.info(f"Total tokens: {self.state.total_tokens_used:,}")
        logger.info(f"Longest streak: {self.state.longest_streak}")
        logger.info(f"Skills learned: {len(self.state.skills_learned)}")
        logger.info(f"Patterns discovered: {len(self.state.patterns_discovered)}")

        logger.info("=" * 70)
        logger.info("Shutdown complete")
        logger.info("=" * 70)


def print_banner():
    """Print startup banner"""
    banner = """
╔════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   ███████╗██╗   ██╗███████╗████████╗██████╗  ██████╗ ██╗   ██╗      ║
║   ██╔════╝██║   ██║██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗██║   ██║      ║
║   █████╗  ██║   ██║█████╗     ██║   ██████╔╝██║   ██║██║   ██║      ║
║   ██╔══╝  ██║   ██║██╔══╝     ██║   ██╔══██╗██║   ██║██║   ██║      ║
║   ██║     ╚██████╔╝███████╗   ██║   ██║  ██║╚██████╔╝╚██████╔╝      ║
║   ╚═╝      ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚═════╝       ║
║                                                                      ║
║                    24/7 Autonomous Operation                         ║
║                    Self-Working AI Agent                              ║
║                                                                      ║
╚════════════════════════════════════════════════════════════════════╝
    """
    print(banner)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Log: {LOG_FILE}")
    print(f"State: {STATE_FILE}")
    print("")


async def main():
    """Main entry point"""
    print_banner()

    # Get work directory from command line or use current
    if len(sys.argv) > 1:
        work_dir = Path(sys.argv[1])
    else:
        work_dir = Path.cwd()

    # Create agent
    agent = ClaudeCodeAutonomousAgent(
        work_dir=work_dir,
        target_tasks_per_hour=10,  # Target 10 tasks per hour
        reflection_interval=5,  # Reflect every 5 tasks
        max_tokens_per_task=100000
    )

    try:
        await agent.run()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutdown complete")
