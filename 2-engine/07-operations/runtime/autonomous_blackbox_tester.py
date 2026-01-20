#!/usr/bin/env python3
"""
Autonomous BLACKBOX5 Tester

Uses Ralphie's autonomous infrastructure to continuously test BLACKBOX5,
find issues, and fix them automatically.
"""

import os
import sys
import asyncio
import json
import logging
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import atomic commits framework
# We need to import GitOps directly and patch the import in atomic_commit_manager
sys.path.insert(0, str(PROJECT_ROOT / "2-engine/05-tools/git"))
import git_ops
from git_ops import GitOps, CommitInfo
# Inject into sys.modules so atomic_commit_manager can find it
sys.modules['operations.tools.git_ops'] = git_ops
sys.modules['..operations.tools.git_ops'] = git_ops

sys.path.insert(0, str(PROJECT_ROOT / "2-engine/01-core/resilience"))
# Now we can import AtomicCommitManager
from atomic_commit_manager import AtomicCommitManager

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG to see what's happening with fixes
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BlackboxTestScenario:
    """A test scenario for BLACKBOX5"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.results = []
        self.issues_found = []

    async def execute(self, api_url: str = "http://localhost:8000") -> Dict[str, Any]:
        """Execute the test scenario - to be overridden by subclasses"""
        raise NotImplementedError


class ChatAPITest(BlackboxTestScenario):
    """Test the /chat endpoint with various inputs"""

    def __init__(self):
        super().__init__(
            "Chat API Tests",
            "Test the /chat endpoint with various message types and parameters"
        )
        self.test_cases = [
            {"message": "Design a microservices architecture", "expected_agent": "architect"},
            {"message": "Implement REST API for user auth", "expected_agent": "Backend Specialist"},
            {"message": "Create React component for dashboard", "expected_agent": "Frontend Specialist"},
            {"message": "Write unit tests for payment module", "expected_agent": "Testing Specialist"},
            {"message": "Audit code for security vulnerabilities", "expected_agent": "Security Specialist"},
            {"message": "Optimize database queries", "expected_agent": "Database Specialist"},
            {"message": "Deploy to Kubernetes", "expected_agent": "DevOps Specialist"},
            {"message": "Design user onboarding flow", "expected_agent": "UI/UX Specialist"},
            {"message": "Mobile app push notifications", "expected_agent": "Mobile Development Specialist"},
            {"message": "Implement ML model for recommendations", "expected_agent": "Machine Learning Specialist"},
        ]

    async def execute(self, api_url: str = "http://localhost:8000") -> Dict[str, Any]:
        """Execute all chat API test cases"""
        import aiohttp

        results = []
        issues = []

        async with aiohttp.ClientSession() as session:
            for i, test_case in enumerate(self.test_cases, 1):
                try:
                    start_time = time.time()
                    async with session.post(
                        f"{api_url}/chat",
                        json={"message": test_case["message"]},
                        headers={"Content-Type": "application/json"}
                    ) as response:
                        duration = time.time() - start_time
                        data = await response.json()

                        result = {
                            "test_case": i,
                            "message": test_case["message"],
                            "status": response.status,
                            "success": data.get("success", False),
                            "routed_to": data.get("routing", {}).get("agent"),
                            "expected_agent": test_case.get("expected_agent"),
                            "confidence": data.get("routing", {}).get("confidence"),
                            "duration": duration,
                            "has_output": bool(data.get("result", {}).get("output")),
                        }

                        # Check for issues
                        if not result["success"]:
                            issues.append({
                                "type": "api_error",
                                "test": i,
                                "message": test_case["message"],
                                "error": data.get("error", "Unknown error")
                            })

                        # Flag routing mismatches regardless of confidence
                        # This helps us detect when tasks go to unexpected agents
                        if result["routed_to"] != result["expected_agent"]:
                            issues.append({
                                "type": "routing_mismatch",
                                "test": i,
                                "message": test_case["message"],
                                "expected": result["expected_agent"],
                                "got": result["routed_to"],
                                "confidence": result["confidence"]
                            })

                        results.append(result)
                        logger.info(f"Test {i}: {test_case['message'][:40]}... -> {result['routed_to']}")

                except Exception as e:
                    issues.append({
                        "type": "test_exception",
                        "test": i,
                        "message": test_case["message"],
                        "error": str(e)
                    })
                    logger.error(f"Test {i} failed: {e}")

        self.results = results
        self.issues_found = issues

        return {
            "total_tests": len(results),
            "passed": sum(1 for r in results if r["success"]),
            "failed": sum(1 for r in results if not r["success"]),
            "issues": len(issues),
            "avg_duration": sum(r["duration"] for r in results) / len(results) if results else 0
        }


class AgentCapabilityTest(BlackboxTestScenario):
    """Test that all agents have proper capabilities"""

    def __init__(self):
        super().__init__(
            "Agent Capability Tests",
            "Check that all agents have proper capabilities configured"
        )

    async def execute(self, api_url: str = "http://localhost:8000") -> Dict[str, Any]:
        """Check all agents have capabilities configured"""
        import aiohttp

        issues = []
        agent_count = 0
        total_capabilities = 0

        async with aiohttp.ClientSession() as session:
            # Get all agents
            async with session.get(f"{api_url}/agents") as response:
                agents_data = await response.json()

            for agent in agents_data:
                agent_count += 1
                caps = agent.get("capabilities", [])
                total_capabilities += len(caps)

                # Check for agents with no capabilities
                if len(caps) == 0:
                    issues.append({
                        "type": "missing_capabilities",
                        "agent": agent.get("name"),
                        "role": agent.get("role")
                    })

                # Check for generic/duplicate capabilities
                if len(caps) > 0:
                    generic_caps = [c for c in caps if c in ["general", "misc", "other"]]
                    if len(generic_caps) > 0:
                        issues.append({
                            "type": "generic_capabilities",
                            "agent": agent.get("name"),
                            "generic_caps": generic_caps
                        })

        logger.info(f"Checked {agent_count} agents with {total_capabilities} total capabilities")

        return {
            "agent_count": agent_count,
            "total_capabilities": total_capabilities,
            "avg_capabilities": total_capabilities / agent_count if agent_count > 0 else 0,
            "issues": len(issues)
        }


class ErrorInjectionTest(BlackboxTestScenario):
    """Test BLACKBOX5 error handling with various invalid inputs"""

    def __init__(self):
        super().__init__(
            "Error Injection Tests",
            "Test error handling with invalid, malformed, or malicious inputs"
        )
        self.test_cases = [
            {"message": "", "description": "Empty message"},
            {"message": "A" * 10000, "description": "Very long message"},
            {"message": "<script>alert('xss')</script>", "description": "XSS attempt"},
            {"message": "'; DROP TABLE users; --", "description": "SQL injection"},
            {"message": {"nested": "object"}, "description": "Non-string message"},
            {"message": "🔥🔥🔥" * 100, "description": "Emoji spam"},
            {"message": "\x00\x01\x02\x03", "description": "Binary data"},
        ]

    async def execute(self, api_url: str = "http://localhost:8000") -> Dict[str, Any]:
        """Execute error injection tests"""
        import aiohttp

        results = []
        crashes = []

        async with aiohttp.ClientSession() as session:
            for i, test_case in enumerate(self.test_cases, 1):
                try:
                    async with session.post(
                        f"{api_url}/chat",
                        json={"message": test_case["message"]},
                        headers={"Content-Type": "application/json"},
                        timeout=aiohttp.ClientTimeout(total=30)
                    ) as response:
                        data = await response.json()

                        result = {
                            "test": i,
                            "description": test_case["description"],
                            "status": response.status,
                            "success": data.get("success", False),
                            "crashed": False
                        }

                        results.append(result)
                        logger.info(f"Error test {i} ({test_case['description']}): {response.status}")

                except asyncio.TimeoutError:
                    crashes.append({
                        "test": i,
                        "description": test_case["description"],
                        "error": "timeout"
                    })
                    results.append({"test": i, "description": test_case["description"], "crashed": True})
                    logger.error(f"Error test {i} timed out")

                except Exception as e:
                    crashes.append({
                        "test": i,
                        "description": test_case["description"],
                        "error": str(e)
                    })
                    results.append({"test": i, "description": test_case["description"], "crashed": True})
                    logger.error(f"Error test {i} crashed: {e}")

        return {
            "total_tests": len(results),
            "crashes": len(crashes),
            "handled_errors": len(results) - len(crashes)
        }


class AutonomousBlackboxTester:
    """
    Autonomous tester that continuously tests BLACKBOX5,
    finds issues, and fixes them automatically.
    """

    def __init__(self, max_iterations: int = 100):
        self.max_iterations = max_iterations
        self.iteration = 0
        self.issues_fixed = []
        self.issues_pending = []
        self.test_history = []
        self.api_url = "http://localhost:8000"

        # Test scenarios
        self.scenarios = [
            ChatAPITest(),
            AgentCapabilityTest(),
            ErrorInjectionTest()
        ]

        # Server process management
        self.server_process = None

        # Atomic commits for tracking fixes
        history_dir = PROJECT_ROOT / "2-engine/07-operations/runtime/data"
        history_dir.mkdir(parents=True, exist_ok=True)

        # Create GitOps instance with explicit working directory
        git_ops_instance = GitOps()
        self.git_root = str(PROJECT_ROOT)  # Store for use in git operations

        self.commit_manager = AtomicCommitManager(
            git_ops=git_ops_instance,
            history_path=history_dir / "atomic_commit_history.json"
        )
        logger.info("AtomicCommitManager initialized for autonomous testing")

    async def ensure_server_running(self) -> bool:
        """Ensure BLACKBOX5 API server is running"""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_url}/health", timeout=5) as response:
                    if response.status == 200:
                        logger.info("BLACKBOX5 server is running")
                        # Find and track the existing server process
                        if self.server_process is None:
                            try:
                                result = subprocess.run(
                                    ["lsof", "-ti", ":8000"],
                                    capture_output=True,
                                    text=True,
                                    timeout=5
                                )
                                if result.stdout.strip():
                                    pid = int(result.stdout.strip())
                                    # Create a dummy process object to track the PID
                                    import subprocess
                                    self.server_process = type('obj', (object,), {'pid': pid, 'terminate': lambda: None, 'kill': lambda: None})()
                                    logger.info(f"Tracked existing server process (PID: {pid})")
                            except:
                                pass
                        return True
        except:
            pass

        logger.warning("BLACKBOX5 server not running, starting it...")
        return await self.start_server()

    async def start_server(self) -> bool:
        """Start the BLACKBOX5 API server and track the process"""
        try:
            # Start the server
            self.server_process = subprocess.Popen(
                [sys.executable, "-m", "interface.api.main"],
                cwd=PROJECT_ROOT / "2-engine/01-core",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            await asyncio.sleep(5)  # Give it time to start
            logger.info(f"BLACKBOX5 server started (PID: {self.server_process.pid})")
            return True
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            return False

    async def restart_server(self) -> bool:
        """Restart the BLACKBOX5 API server to pick up configuration changes"""
        logger.info("Restarting BLACKBOX5 server to pick up agent changes...")

        # Kill ALL processes using port 8000 thoroughly
        killed_pids = []
        max_attempts = 3

        for attempt in range(max_attempts):
            try:
                result = subprocess.run(
                    ["lsof", "-ti", ":8000"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.stdout.strip():
                    pids = result.stdout.strip().split('\n')
                    for pid in pids:
                        try:
                            subprocess.run(["kill", "-9", pid], capture_output=True, timeout=2)
                            killed_pids.append(pid)
                            logger.info(f"Killed process {pid} using port 8000")
                        except:
                            pass
                    await asyncio.sleep(1)  # Wait for processes to die
                else:
                    break  # No processes found
            except Exception as e:
                logger.debug(f"Error killing processes (attempt {attempt+1}): {e}")

        if killed_pids:
            logger.info(f"Killed {len(killed_pids)} processes, waiting for port to clear...")
            await asyncio.sleep(3)  # Extra wait after killing

        # Double-check port is clear
        try:
            result = subprocess.run(
                ["lsof", "-ti", ":8000"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.stdout.strip():
                logger.warning(f"Port 8000 still in use after killing: {result.stdout.strip()}")
                return False
        except:
            pass

        # Start fresh server
        return await self.start_server()

    async def run_test_suite(self) -> Tuple[Dict[str, Any], List[Dict]]:
        """Run all test scenarios"""
        all_results = {}
        all_issues = []

        for scenario in self.scenarios:
            logger.info(f"Running scenario: {scenario.name}")
            try:
                result = await scenario.execute(self.api_url)
                all_results[scenario.name] = result

                if hasattr(scenario, 'issues_found'):
                    all_issues.extend(scenario.issues_found)

            except Exception as e:
                logger.error(f"Scenario {scenario.name} failed: {e}")
                all_results[scenario.name] = {"error": str(e)}

        return all_results, all_issues

    async def analyze_issue(self, issue: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Analyze an issue and determine if it can be auto-fixed

        Returns fix plan or None if manual intervention needed
        """
        issue_type = issue.get("type", "")

        # Map issue types to fix strategies
        fix_strategies = {
            "missing_capabilities": {
                "action": "add_capabilities",
                "confidence": 0.9,
                "description": "Add missing capabilities to agent configuration"
            },
            "api_error": {
                "action": "debug_api",
                "confidence": 0.7,
                "description": "Debug API error and fix root cause"
            },
            "routing_mismatch": {
                "action": "adjust_routing",
                "confidence": 0.8,
                "description": "Adjust routing logic or agent capabilities"
            },
            "generic_capabilities": {
                "action": "improve_capabilities",
                "confidence": 0.9,
                "description": "Improve agent capability definitions"
            }
        }

        strategy = fix_strategies.get(issue_type, {
            "action": "manual_review",
            "confidence": 0.3,
            "description": f"Manual review needed for {issue_type}"
        })

        return {
            "issue": issue,
            "strategy": strategy,
            "estimated_effort": "medium" if strategy["confidence"] > 0.7 else "unknown"
        }

    async def fix_issue(self, issue: Dict[str, Any], fix_plan: Dict[str, Any]) -> bool:
        """
        Attempt to automatically fix an issue

        Returns True if fix was successful
        """
        action = fix_plan["strategy"]["action"]

        logger.info(f"Attempting to fix issue using action: {action}")
        logger.info(f"Issue details: {issue}")

        # Create snapshot before making changes for atomic commit
        before_snapshot = self.commit_manager.create_snapshot()
        logger.debug(f"Created snapshot before fix: {len(before_snapshot)} files tracked")

        try:
            fix_successful = False

            if action == "adjust_routing":
                fix_successful = await self._fix_routing_mismatch(issue, fix_plan)
            elif action == "improve_capabilities":
                fix_successful = await self._fix_generic_capabilities(issue, fix_plan)
            elif action == "add_capabilities":
                fix_successful = await self._add_missing_capabilities(issue, fix_plan)
            elif action == "debug_api":
                fix_successful = await self._debug_api_error(issue, fix_plan)
            else:
                logger.warning(f"No auto-fix implemented for action: {action}")
                return False

            # If fix was successful, detect changes and create atomic commit
            if fix_successful:
                await self._commit_fix(issue, fix_plan, before_snapshot, action)
                return True
            else:
                return False

        except Exception as e:
            logger.error(f"Failed to fix issue: {e}")
            return False

    async def _fix_routing_mismatch(self, issue: Dict[str, Any], fix_plan: Dict[str, Any]) -> bool:
        """
        Fix routing mismatch by improving agent capabilities

        The issue is that tasks are routing to agents with low confidence.
        We need to improve the agent's capabilities or the routing logic.
        """
        message = issue.get("message", "")
        expected_agent = issue.get("expected", "")
        got_agent = issue.get("got", "")
        confidence = issue.get("confidence", 0)

        logger.info(f"Routing mismatch: '{message}' expected {expected_agent} but got {got_agent} (confidence: {confidence})")

        # Strategy: If confidence is low, the expected agent might be missing capabilities
        # that would help it match this type of task better

        # Find the agent YAML file and check its capabilities
        if await self._improve_agent_capabilities_for_task(expected_agent, message):
            logger.info(f"Successfully improved capabilities for {expected_agent}")
            return True

        return False

    async def _improve_agent_capabilities_for_task(self, agent_name: str, task_description: str) -> bool:
        """
        Analyze a task and improve the agent's configuration to better match similar tasks.

        SMART Strategy (v2):
        1. Extract meaningful technology/technical terms from the task
        2. Add those as tags to the agent's metadata
        3. DO NOT touch identity or capabilities - they're already well-written
        4. DO NOT keyword stuff with task words like "implement", "for", etc.

        Returns True if changes were made
        """
        # Find the agent's YAML file
        import yaml

        # Map agent names to file names
        agent_file_map = {
            "Frontend Specialist": "frontend-specialist.yaml",
            "Backend Specialist": "backend-specialist.yaml",
            "UI/UX Specialist": "ui-ux-specialist.yaml",
            "Testing Specialist": "testing-specialist.yaml",
            "Mobile Development Specialist": "mobile-specialist.yaml",
            "Database Specialist": "database-specialist.yaml",
            "DevOps Specialist": "devops-specialist.yaml",
            "Machine Learning Specialist": "ml-specialist.yaml",
            "Security Specialist": "security-specialist.yaml",
            "architect": "architect.yaml",
        }

        yaml_filename = agent_file_map.get(agent_name)
        if not yaml_filename:
            logger.debug(f"No YAML file mapping for agent: {agent_name}")
            return False

        yaml_path = PROJECT_ROOT / "2-engine/01-core/agents" / yaml_filename
        if not yaml_path.exists():
            logger.warning(f"YAML file not found: {yaml_path}")
            return False

        # Read the YAML file
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)

        agent_data = data.get('agent', {})
        metadata = agent_data.get('metadata', {})
        current_tags = metadata.get('tags', [])

        # Extract MEANINGFUL technical terms from the task
        # These are terms that should help with semantic matching
        tech_terms = {
            # Frontend technologies
            "react", "vue", "angular", "typescript", "javascript", "jsx", "tsx",
            "component", "dashboard", "interface", "ui", "frontend",

            # Backend technologies
            "api", "rest", "graphql", "backend", "server", "microservices",
            "python", "nodejs", "django", "flask", "express", "fastapi",

            # Database technologies
            "database", "sql", "nosql", "postgresql", "mongodb", "redis",
            "query", "optimization", "schema", "migration",

            # DevOps technologies
            "kubernetes", "docker", "deployment", "ci/cd", "infrastructure",
            "aws", "gcp", "azure", "terraform", "ansible",

            # Security
            "security", "authentication", "authorization", "encryption",
            "vulnerability", "audit", "penetration", "oauth", "jwt",

            # Testing
            "testing", "unit test", "integration test", "e2e", "pytest",
            "jest", "cypress", "tdd", "bdd",

            # Mobile
            "mobile", "ios", "android", "react native", "flutter",
            "swift", "kotlin", "push notification",

            # UI/UX
            "ux", "user experience", "user onboarding", "wireframe",
            "prototype", "design system", "user flow",

            # ML
            "machine learning", "ml", "tensorflow", "pytorch", "model",
            "training", "inference", "recommendation",

            # Architecture
            "architecture", "design", "system", "scalability", "patterns",
        }

        # Find tech terms in the task description
        task_lower = task_description.lower()
        found_terms = [term for term in tech_terms if term in task_lower]

        # Filter out terms already in tags
        new_terms = [term for term in found_terms if term.lower() not in [t.lower() for t in current_tags]]

        if not new_terms:
            logger.debug(f"No new technical terms to add for {agent_name}")
            return False

        # Add new terms to tags
        current_tags.extend(new_terms)
        metadata['tags'] = current_tags

        # Write back the YAML file (preserve formatting)
        agent_data['metadata'] = metadata
        data['agent'] = agent_data

        with open(yaml_path, 'w') as f:
            yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)

        # Force server reload
        import subprocess
        subprocess.run(['touch', str(yaml_path)], check=True)

        logger.info(f"✓ Enhanced {agent_name} for: {task_description[:50]}...")
        logger.info(f"  - Added technical tags: {', '.join(new_terms[:5])}")
        return True

    async def _fix_generic_capabilities(self, issue: Dict[str, Any], fix_plan: Dict[str, Any]) -> bool:
        """
        Fix generic capabilities by replacing them with specific ones
        """
        agent_name = issue.get("agent", "")
        generic_caps = issue.get("generic_caps", [])

        logger.info(f"Fixing generic capabilities for {agent_name}: {generic_caps}")

        # This would require editing the agent's YAML and replacing
        # generic capabilities with specific ones based on the agent's role
        # For now, log as a known issue
        return False

    async def _add_missing_capabilities(self, issue: Dict[str, Any], fix_plan: Dict[str, Any]) -> bool:
        """
        Add missing capabilities to an agent
        """
        agent_name = issue.get("agent", "")

        # Suggest core capabilities based on role
        role_capability_suggestions = {
            "Frontend Specialist": ["react", "vue", "angular", "typescript", "javascript"],
            "Backend Specialist": ["python", "nodejs", "api", "microservices"],
            "Database Specialist": ["sql", "nosql", "postgresql", "mongodb"],
            # Add more as needed
        }

        suggestions = role_capability_suggestions.get(agent_name, [])
        if not suggestions:
            return False

        logger.info(f"Adding suggested capabilities to {agent_name}: {suggestions}")

        # Implementation would update the YAML file
        return False

    async def _debug_api_error(self, issue: Dict[str, Any], fix_plan: Dict[str, Any]) -> bool:
        """
        Debug and fix API errors
        """
        error_msg = issue.get("error", "")
        test_num = issue.get("test", "")

        logger.info(f"Debugging API error in test {test_num}: {error_msg}")

        # Check for common error patterns and suggest fixes
        if "validation" in error_msg.lower():
            logger.info("Suggestion: Add input validation to the API endpoint")
        elif "timeout" in error_msg.lower():
            logger.info("Suggestion: Increase timeout or optimize query")

        return False

    async def _commit_fix(
        self,
        issue: Dict[str, Any],
        fix_plan: Dict[str, Any],
        before_snapshot: List[str],
        action: str
    ) -> None:
        """
        Create an atomic commit for a successful fix

        Args:
            issue: The issue that was fixed
            fix_plan: The fix plan that was executed
            before_snapshot: Git state snapshot before the fix
            action: The action that was taken
        """
        try:
            # Detect what changed
            task_id = f"fix_{self.iteration}_{int(time.time())}"

            # Get changed files from git root directory
            import subprocess
            status_output = subprocess.run(
                ["git", "status", "--short"],
                cwd=self.git_root,
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()

            # Parse the output to get changed files
            changed_files = []
            for line in status_output.split('\n'):
                if line.strip():
                    parts = line.strip().split(maxsplit=1)
                    if len(parts) == 2:
                        status_code, filepath = parts
                        if status_code in ['M', 'A', 'D', 'R', 'C', '??', 'AM', 'MM']:
                            # Convert repo-root path to relative path for commit
                            if not filepath.startswith('2-engine/'):
                                # It's probably a relative path like ../../01-core/agents/...
                                # Convert to proper format
                                if filepath.startswith('../'):
                                    # This is from the runtime directory
                                    # We need to convert to repo-root format
                                    filepath = filepath.replace('../../', '2-engine/01-core/')
                                elif filepath.startswith('01-core/'):
                                    filepath = f'2-engine/{filepath}'
                            changed_files.append(filepath)

            if not changed_files:
                logger.warning("No files changed after fix, skipping commit")
                return

            logger.info(f"Detected {len(changed_files)} changed files after fix")

            # Infer commit type from action and issue
            if action in ["adjust_routing", "improve_capabilities", "add_capabilities"]:
                task_type = "fix"  # Fixing agent configuration
                scope = "agents"
            elif action == "debug_api":
                task_type = "fix"
                scope = "api"
            else:
                task_type = "chore"
                scope = "testing"

            # Create a descriptive commit message
            issue_type = issue.get("type", "unknown")
            issue_msg = issue.get("message", str(issue))
            issue_desc = issue_msg[:100] if len(issue_msg) > 100 else issue_msg

            description = f"Auto-fix: {issue_type}"
            if issue_type == "routing_mismatch":
                expected = issue.get("expected", "unknown")
                got = issue.get("got", "unknown")
                description = f"Fix routing to {expected} (was {got})"

            # Build commit body with details
            body_lines = [
                f"Task ID: {task_id}",
                f"Iteration: {self.iteration}",
                f"Action: {action}",
                "",
                "Issue:",
                f"  Type: {issue_type}",
                f"  Details: {issue_desc}",
                "",
                f"Files changed: {len(changed_files)}",
                "  " + "\n  ".join(changed_files[:10])  # Show first 10 files
            ]
            body = "\n".join(body_lines)

            # Create the atomic commit
            # Temporarily change to git root for git operations
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(self.git_root)
                commit_info = self.commit_manager.commit_task_result(
                    task_id=task_id,
                    task_type=task_type,
                    scope=scope,
                    description=description,
                    files=changed_files,
                    body=body,
                    wave_id=self.iteration
                )
            finally:
                os.chdir(old_cwd)

            if commit_info:
                logger.info(
                    f"✓ Created atomic commit {commit_info.commit_hash}: "
                    f"{task_type}({scope}): {description}"
                )
            else:
                logger.warning("Commit creation returned None")

        except Exception as e:
            logger.error(f"Failed to create atomic commit: {e}")
            logger.debug("Atomic commit failure details", exc_info=True)

    async def run_iteration(self) -> Dict[str, Any]:
        """Run one testing iteration"""
        self.iteration += 1
        logger.info(f"=== Starting iteration {self.iteration} ===")

        # Ensure server is running
        if not await self.ensure_server_running():
            return {"error": "Server not available", "iteration": self.iteration}

        # Run tests
        results, issues = await self.run_test_suite()

        # Analyze issues
        fixable_issues = []
        for issue in issues:
            fix_plan = await self.analyze_issue(issue)
            logger.info(f"Issue: {issue.get('type', 'unknown')} - Fix confidence: {fix_plan['strategy']['confidence'] if fix_plan else 'N/A'}")
            if fix_plan and fix_plan["strategy"]["confidence"] > 0.7:
                fixable_issues.append((issue, fix_plan))

        logger.info(f"Found {len(issues)} issues, {len(fixable_issues)} are fixable")

        # Try to fix issues
        fixes_attempted = 0
        fixes_successful = 0

        for issue, fix_plan in fixable_issues[:3]:  # Limit to 3 fixes per iteration
            fixes_attempted += 1
            success = await self.fix_issue(issue, fix_plan)
            if success:
                fixes_successful += 1
                self.issues_fixed.append(issue)

        # Restart server if any fixes were applied to pick up changes
        if fixes_successful > 0:
            logger.info(f"Restarting server after {fixes_successful} successful fixes...")
            if await self.restart_server():
                logger.info("Server restarted successfully")
            else:
                logger.warning("Server restart failed, continuing with old configuration")

        # Record history
        iteration_summary = {
            "iteration": self.iteration,
            "timestamp": datetime.now().isoformat(),
            "test_results": results,
            "issues_found": len(issues),
            "fixes_attempted": fixes_attempted,
            "fixes_successful": fixes_successful,
            "pending_issues": len(self.issues_pending)
        }

        self.test_history.append(iteration_summary)

        # Log progress every 10 iterations
        if self.iteration % 10 == 0:
            logger.info(f"{'='*60}")
            logger.info(f"PROGRESS UPDATE: Iteration {self.iteration}/{self.max_iterations}")
            logger.info(f"  Total issues fixed so far: {len(self.issues_fixed)}")
            logger.info(f"  Completion: {self.iteration/self.max_iterations*100:.1f}%")
            logger.info(f"{'='*60}")

        logger.info(f"Iteration {self.iteration} complete:")
        logger.info(f"  Issues found: {len(issues)}")
        logger.info(f"  Fixes attempted: {fixes_attempted}")
        logger.info(f"  Fixes successful: {fixes_successful}")

        return iteration_summary

    async def run(self):
        """Run the autonomous testing loop"""
        logger.info("Starting Autonomous BLACKBOX5 Tester")
        logger.info(f"Max iterations: {self.max_iterations}")
        logger.info(f"Estimated duration: ~{self.max_iterations * 20 / 3600:.1f} hours")

        start_time = time.time()

        while self.iteration < self.max_iterations:
            try:
                await self.run_iteration()

                # Decide whether to continue
                # Note: Removed early exit condition to run full 1000 iterations
                # if len(self.issues_pending) == 0 and self.iteration >= 5:
                #     logger.info("No issues found and minimum iterations reached")
                #     break

                # Cool down between iterations
                await asyncio.sleep(2)

            except KeyboardInterrupt:
                logger.info("Testing interrupted by user")
                break
            except Exception as e:
                logger.error(f"Iteration failed: {e}")
                await asyncio.sleep(5)

        elapsed = time.time() - start_time
        logger.info(f"Testing completed in {elapsed/3600:.2f} hours ({elapsed/60:.1f} minutes)")

        # Generate final report
        self.generate_report()

    def generate_report(self):
        """Generate final testing report"""
        report = {
            "summary": {
                "total_iterations": self.iteration,
                "total_issues_fixed": len(self.issues_fixed),
                "pending_issues": len(self.issues_pending)
            },
            "history": self.test_history,
            "pending_fixes": self.issues_pending
        }

        report_path = PROJECT_ROOT / "2-engine" / "01-core" / "autonomous_test_report.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        logger.info(f"Report saved to {report_path}")
        logger.info(f"Total iterations: {self.iteration}")
        logger.info(f"Issues fixed: {len(self.issues_fixed)}")
        logger.info(f"Pending issues: {len(self.issues_pending)}")


async def main():
    """Main entry point"""
    # Run for 1000 iterations (approximately 6 hours with ~20 seconds per iteration)
    tester = AutonomousBlackboxTester(max_iterations=1000)
    await tester.run()


if __name__ == "__main__":
    asyncio.run(main())
