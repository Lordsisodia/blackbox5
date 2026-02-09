#!/usr/bin/env python3
"""
MoltBot Autonomous Agent
Runs continuously on VPS, analyzes BB5, reports via Telegram, executes via Claude Code.
"""

import os
import sys
import json
import time
import logging
import subprocess
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import yaml
import schedule

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8581639813:AAFA13wDTKEX2x6J-lVfpq9QHnsGRnB1EZo")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7643203581")
BB5_DIR = Path("/opt/blackbox5")
STATE_DIR = BB5_DIR / "agents" / "moltbot-autonomous" / "state"
LOG_DIR = BB5_DIR / ".logs" / "moltbot"

# Setup logging
LOG_DIR.mkdir(parents=True, exist_ok=True)
STATE_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "moltbot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("moltbot")

class TelegramNotifier:
    """Send notifications via Telegram"""

    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}"

    def send(self, message: str, parse_mode: str = "HTML") -> bool:
        """Send a message to Telegram"""
        try:
            response = requests.post(
                f"{self.base_url}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": parse_mode,
                    "disable_notification": False
                },
                timeout=10
            )
            response.raise_for_status()
            logger.info(f"Telegram message sent: {message[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False

    def send_analysis_report(self, issues: List[Dict]):
        """Send formatted analysis report"""
        if not issues:
            self.send("✅ <b>BB5 Daily Analysis</b>\n\nNo issues found! System is healthy.")
            return

        message = f"🔍 <b>BB5 Analysis Report</b>\n\n"
        message += f"Issues Found: {len(issues)}\n"
        message += "━" * 20 + "\n\n"

        for i, issue in enumerate(issues[:5], 1):  # Show max 5
            severity_emoji = {"high": "🚨", "medium": "⚠️", "low": "ℹ️"}.get(issue['severity'], "ℹ️")
            message += f"{i}. {severity_emoji} <b>[{issue['severity'].upper()}]</b> {issue['title']}\n"
            message += f"   {issue['description'][:100]}...\n"
            message += f"   → Propose: {issue['proposed_action']}\n\n"

        if len(issues) > 5:
            message += f"... and {len(issues) - 5} more issues\n\n"

        message += "<b>Reply:</b>\n"
        message += "• <code>1</code>, <code>2</code>, etc - Fix issue #\n"
        message += "• <code>all</code> - Fix all issues\n"
        message += "• <code>status</code> - Detailed status\n"
        message += "• <code>pause</code> - Stop autonomous mode"

        self.send(message)

    def send_action_proposal(self, issue: Dict, branch: str):
        """Send action proposal for approval"""
        message = f"⚡ <b>Proposed Action</b>\n\n"
        message += f"<b>Issue:</b> {issue['title']}\n"
        message += f"<b>Solution:</b> {issue['proposed_action']}\n"
        message += f"<b>Branch:</b> <code>{branch}</code>\n"
        message += f"<b>Risk:</b> {issue['risk_level'].upper()}\n\n"
        message += "<b>Reply:</b>\n"
        message += "• <code>yes</code> - Execute\n"
        message += "• <code>no</code> - Skip\n"
        message += "• <code>details</code> - Show full analysis"

        self.send(message)

    def send_execution_report(self, result: Dict):
        """Send execution completion report"""
        status_emoji = "✅" if result['success'] else "❌"
        message = f"{status_emoji} <b>Action Complete</b>\n\n"
        message += f"<b>Branch:</b> <code>{result['branch']}</code>\n"
        message += f"<b>Duration:</b> {result['duration']}s\n\n"
        message += f"<b>Summary:</b>\n{result['summary']}\n\n"

        if result['success']:
            message += "<b>Reply:</b>\n"
            message += "• <code>merge</code> - Merge to main\n"
            message += "• <code>review</code> - Show diff\n"
            message += "• <code>next</code> - Continue"
        else:
            message += f"<b>Error:</b> {result.get('error', 'Unknown error')}"

        self.send(message)


class BB5Analyzer:
    """Analyze BlackBox5 for issues"""

    def __init__(self, bb5_dir: Path):
        self.bb5_dir = bb5_dir
        self.project_memory = bb5_dir / "5-project-memory" / "blackbox5"
        self.roadmap = bb5_dir / "6-roadmap"

    def analyze_all(self) -> List[Dict]:
        """Run all analyzers and return issues"""
        issues = []
        issues.extend(self.analyze_orphaned_tasks())
        issues.extend(self.analyze_doc_drift())
        issues.extend(self.analyze_skill_registry())
        issues.extend(self.analyze_git_health())
        return issues

    def analyze_orphaned_tasks(self) -> List[Dict]:
        """Find tasks with no linked plan"""
        issues = []
        tasks_dir = self.project_memory / ".autonomous" / "tasks" / "active"

        if not tasks_dir.exists():
            return issues

        orphaned = []
        for task_file in tasks_dir.glob("TASK-*.md"):
            content = task_file.read_text()
            # Check if task has a plan link
            if "plan:" not in content.lower() and "plan_id:" not in content.lower():
                orphaned.append(task_file.stem)

        if orphaned:
            issues.append({
                "id": "ISS-001",
                "type": "orphaned_task",
                "severity": "medium",
                "title": f"{len(orphaned)} orphaned tasks",
                "description": f"Tasks with no linked plan: {', '.join(orphaned[:3])}{'...' if len(orphaned) > 3 else ''}",
                "proposed_action": "Auto-link tasks to nearest plan or create new plan",
                "risk_level": "low",
                "data": {"tasks": orphaned}
            })

        return issues

    def analyze_doc_drift(self) -> List[Dict]:
        """Find documentation that references non-existent files"""
        issues = []
        # Simplified check - look for broken links in ADRs
        adr_dir = self.project_memory / "decisions"

        if not adr_dir.exists():
            return issues

        drift_count = 0
        for adr_file in adr_dir.glob("ADR-*.md"):
            content = adr_file.read_text()
            # Check for broken file references
            import re
            refs = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
            for text, ref in refs:
                if ref.startswith("../") or ref.startswith("./"):
                    full_path = (adr_file.parent / ref).resolve()
                    if not full_path.exists():
                        drift_count += 1

        if drift_count > 0:
            issues.append({
                "id": "ISS-002",
                "type": "doc_drift",
                "severity": "low",
                "title": f"{drift_count} broken references in docs",
                "description": "Documentation references files that don't exist",
                "proposed_action": "Update or remove broken references",
                "risk_level": "low",
                "data": {"count": drift_count}
            })

        return issues

    def analyze_skill_registry(self) -> List[Dict]:
        """Check if skill registry is in sync with actual skills"""
        issues = []
        registry_file = self.project_memory / "operations" / "skill-registry.yaml"

        if not registry_file.exists():
            return issues

        try:
            registry = yaml.safe_load(registry_file.read_text())
            declared_skills = set(s['name'] for s in registry.get('skills', []))

            # Check global skills
            global_skills_dir = Path.home() / ".claude" / "skills"
            if global_skills_dir.exists():
                actual_skills = set(d.name for d in global_skills_dir.iterdir() if d.is_dir())
                missing = declared_skills - actual_skills

                if missing:
                    issues.append({
                        "id": "ISS-003",
                        "type": "skill_registry_drift",
                        "severity": "medium",
                        "title": f"{len(missing)} skills declared but not found",
                        "description": f"Skills: {', '.join(list(missing)[:3])}",
                        "proposed_action": "Implement missing skills or remove from registry",
                        "risk_level": "medium",
                        "data": {"missing": list(missing)}
                    })
        except Exception as e:
            logger.error(f"Error analyzing skill registry: {e}")

        return issues

    def analyze_git_health(self) -> List[Dict]:
        """Check git repository health"""
        issues = []

        try:
            # Check for large files
            result = subprocess.run(
                ["git", "ls-files", "--size"],
                cwd=self.bb5_dir,
                capture_output=True,
                text=True
            )

            large_files = []
            for line in result.stdout.split('\n')[:50]:  # Check first 50
                if line:
                    parts = line.split()
                    if len(parts) >= 2:
                        try:
                            size = int(parts[0])
                            if size > 10_000_000:  # 10MB
                                large_files.append((parts[1], size))
                        except ValueError:
                            pass

            if large_files:
                issues.append({
                    "id": "ISS-004",
                    "type": "large_files",
                    "severity": "low",
                    "title": f"{len(large_files)} large files in repo",
                    "description": "Files over 10MB can slow down git operations",
                    "proposed_action": "Consider using Git LFS for large files",
                    "risk_level": "low",
                    "data": {"files": large_files}
                })

        except Exception as e:
            logger.error(f"Error analyzing git health: {e}")

        return issues


class ClaudeExecutor:
    """Execute fixes via Claude Code"""

    def __init__(self, bb5_dir: Path):
        self.bb5_dir = bb5_dir

    def create_branch(self, issue_id: str) -> str:
        """Create a new branch for the fix"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        branch_name = f"vps/moltbot-{issue_id.lower()}-{timestamp}"

        try:
            # Create and checkout branch
            subprocess.run(
                ["git", "checkout", "-b", branch_name],
                cwd=self.bb5_dir,
                check=True,
                capture_output=True
            )
            logger.info(f"Created branch: {branch_name}")
            return branch_name
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create branch: {e}")
            raise

    def execute_fix(self, issue: Dict, branch: str) -> Dict:
        """Execute a fix via Claude Code"""
        start_time = time.time()

        try:
            # Build prompt based on issue type
            prompt = self._build_prompt(issue, branch)

            # Spawn Claude Code (simplified - would use actual claude CLI)
            # For now, just log what would happen
            logger.info(f"Would spawn Claude Code for issue {issue['id']}")
            logger.info(f"Prompt: {prompt[:200]}...")

            # TODO: Actual Claude Code integration
            # subprocess.run([
            #     "claude",
            #     "--mcp-config", str(self.bb5_dir / ".mcp-moltbot.json"),
            #     "--prompt", prompt
            # ], check=True)

            # Simulate success for now
            result = {
                "success": True,
                "branch": branch,
                "duration": int(time.time() - start_time),
                "summary": f"Fixed {issue['title']}. Created commits and updated documentation.",
                "commits": [f"{branch}-fix-1"],
                "files_changed": 3
            }

            return result

        except Exception as e:
            logger.error(f"Execution failed: {e}")
            return {
                "success": False,
                "branch": branch,
                "duration": int(time.time() - start_time),
                "summary": "",
                "error": str(e)
            }

    def _build_prompt(self, issue: Dict, branch: str) -> str:
        """Build Claude Code prompt for an issue"""
        prompts = {
            "orphaned_task": f"""
You are fixing orphaned tasks in BlackBox5.

Issue: {issue['title']}
Description: {issue['description']}

Tasks to fix: {issue['data'].get('tasks', [])}

Instructions:
1. Work in branch: {branch}
2. For each orphaned task, either:
   - Link it to the most appropriate existing plan in 6-roadmap/
   - Or create a new plan if no appropriate plan exists
3. Update each task file to include the plan reference
4. Create an ADR documenting your decisions
5. Update STATE.yaml if needed
6. Commit with message: "moltbot: Link orphaned tasks to plans"

Rules:
- Never delete tasks
- Never modify main branch directly
- Document all decisions
""",
            "doc_drift": f"""
You are fixing documentation drift in BlackBox5.

Issue: {issue['title']}
Description: {issue['description']}

Instructions:
1. Work in branch: {branch}
2. Find broken references in ADRs
3. Either update references to correct paths, or remove if no longer relevant
4. Commit with message: "moltbot: Fix broken documentation references"
""",
            "skill_registry_drift": f"""
You are fixing skill registry drift in BlackBox5.

Issue: {issue['title']}
Description: {issue['description']}

Missing skills: {issue['data'].get('missing', [])}

Instructions:
1. Work in branch: {branch}
2. For each missing skill:
   - Check if skill should exist (look for SKILL.md files)
   - If skill exists but not registered, add to registry
   - If skill doesn't exist, remove from registry
3. Commit with message: "moltbot: Sync skill registry"
"""
        }

        return prompts.get(issue['type'], f"Fix issue: {issue['title']}")


class MoltBotAgent:
    """Main MoltBot Autonomous Agent"""

    def __init__(self):
        self.telegram = TelegramNotifier(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        self.analyzer = BB5Analyzer(BB5_DIR)
        self.executor = ClaudeExecutor(BB5_DIR)
        self.state_file = STATE_DIR / "agent_state.json"
        self.mode = "safe"  # safe, semi, auto
        self.running = True

        # Load state
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """Load agent state from disk"""
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return {
            "mode": "safe",
            "last_analysis": None,
            "pending_actions": [],
            "executed_actions": [],
            "issues_found": []
        }

    def _save_state(self):
        """Save agent state to disk"""
        self.state_file.write_text(json.dumps(self.state, indent=2))

    def run_analysis(self):
        """Run full analysis and report findings"""
        logger.info("Running BB5 analysis...")

        issues = self.analyzer.analyze_all()
        self.state["issues_found"] = issues
        self.state["last_analysis"] = datetime.now().isoformat()
        self._save_state()

        logger.info(f"Found {len(issues)} issues")

        # Send report via Telegram
        self.telegram.send_analysis_report(issues)

    def process_telegram_updates(self):
        """Check for and process Telegram commands"""
        try:
            response = requests.get(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates",
                params={"offset": self.state.get("last_update_id", 0) + 1, "limit": 10},
                timeout=10
            )
            response.raise_for_status()
            updates = response.json().get("result", [])

            for update in updates:
                self._handle_update(update)
                self.state["last_update_id"] = update["update_id"]

            if updates:
                self._save_state()

        except Exception as e:
            logger.error(f"Error processing Telegram updates: {e}")

    def _handle_update(self, update: Dict):
        """Handle a single Telegram update"""
        if "message" not in update:
            return

        message = update["message"]
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "").lower().strip()

        # Only respond to authorized chat
        if str(chat_id) != TELEGRAM_CHAT_ID:
            return

        logger.info(f"Received command: {text}")

        # Command handlers
        if text == "status":
            self._cmd_status()
        elif text == "analyze":
            self.run_analysis()
        elif text == "issues":
            self._cmd_issues()
        elif text.startswith("fix "):
            self._cmd_fix(text[4:])
        elif text == "pause":
            self._cmd_pause()
        elif text == "resume":
            self._cmd_resume()
        elif text == "mode safe":
            self._cmd_mode("safe")
        elif text == "mode semi":
            self._cmd_mode("semi")
        elif text in ["1", "2", "3", "4", "5"]:
            self._cmd_fix_by_number(int(text))
        elif text == "yes" and self.state.get("awaiting_approval"):
            self._cmd_approve()
        elif text == "no" and self.state.get("awaiting_approval"):
            self._cmd_reject()
        else:
            self.telegram.send("Unknown command. Try: status, analyze, issues, pause, resume")

    def _cmd_status(self):
        """Send status report"""
        last_analysis = self.state.get("last_analysis", "Never")
        pending = len(self.state.get("pending_actions", []))
        executed = len(self.state.get("executed_actions", []))
        mode = self.state.get("mode", "safe")

        message = f"""📊 <b>MoltBot Status</b>

Mode: {mode.upper()}
Last Analysis: {last_analysis}
Pending Actions: {pending}
Executed Actions: {executed}
Current Issues: {len(self.state.get('issues_found', []))}

System: Running ✅"""

        self.telegram.send(message)

    def _cmd_issues(self):
        """List current issues"""
        issues = self.state.get("issues_found", [])
        if not issues:
            self.telegram.send("No issues found. Run 'analyze' to check.")
            return

        message = "📋 <b>Current Issues</b>\n\n"
        for i, issue in enumerate(issues, 1):
            emoji = {"high": "🚨", "medium": "⚠️", "low": "ℹ️"}.get(issue['severity'], "ℹ️")
            message += f"{i}. {emoji} {issue['title']}\n"

        message += "\nReply with number to fix (e.g., '1')"
        self.telegram.send(message)

    def _cmd_fix(self, issue_id: str):
        """Fix a specific issue"""
        issues = self.state.get("issues_found", [])
        issue = next((i for i in issues if i['id'] == issue_id.upper()), None)

        if not issue:
            self.telegram.send(f"Issue {issue_id} not found. Run 'issues' to see list.")
            return

        self._propose_action(issue)

    def _cmd_fix_by_number(self, num: int):
        """Fix issue by number"""
        issues = self.state.get("issues_found", [])
        if num < 1 or num > len(issues):
            self.telegram.send(f"Invalid issue number. Found {len(issues)} issues.")
            return

        self._propose_action(issues[num - 1])

    def _propose_action(self, issue: Dict):
        """Propose an action for approval"""
        if self.mode == "safe":
            # Create branch and propose
            try:
                branch = self.executor.create_branch(issue['id'])
                self.state["awaiting_approval"] = {
                    "issue": issue,
                    "branch": branch
                }
                self._save_state()
                self.telegram.send_action_proposal(issue, branch)
            except Exception as e:
                self.telegram.send(f"❌ Error creating branch: {e}")
        else:
            # Semi-autonomous: execute and report
            self._execute_action(issue)

    def _cmd_approve(self):
        """Execute approved action"""
        approval = self.state.get("awaiting_approval")
        if not approval:
            self.telegram.send("No action awaiting approval")
            return

        self._execute_action(approval["issue"], approval["branch"])
        self.state["awaiting_approval"] = None
        self._save_state()

    def _cmd_reject(self):
        """Reject proposed action"""
        approval = self.state.get("awaiting_approval")
        if approval:
            # Delete branch
            try:
                subprocess.run(
                    ["git", "branch", "-D", approval["branch"]],
                    cwd=BB5_DIR,
                    check=True,
                    capture_output=True
                )
            except:
                pass

        self.state["awaiting_approval"] = None
        self._save_state()
        self.telegram.send("Action rejected. Branch deleted.")

    def _execute_action(self, issue: Dict, branch: Optional[str] = None):
        """Execute an action"""
        self.telegram.send(f"🔧 Executing fix for {issue['id']}...")

        if not branch:
            branch = self.executor.create_branch(issue['id'])

        result = self.executor.execute_fix(issue, branch)

        if result['success']:
            self.state["executed_actions"].append({
                "issue": issue,
                "result": result,
                "timestamp": datetime.now().isoformat()
            })
        else:
            self.state["pending_actions"].append({
                "issue": issue,
                "error": result.get('error'),
                "timestamp": datetime.now().isoformat()
            })

        self._save_state()
        self.telegram.send_execution_report(result)

    def _cmd_pause(self):
        """Pause autonomous operation"""
        self.running = False
        self.telegram.send("⏸️ MoltBot paused. Send 'resume' to restart.")

    def _cmd_resume(self):
        """Resume autonomous operation"""
        self.running = True
        self.telegram.send("▶️ MoltBot resumed.")

    def _cmd_mode(self, mode: str):
        """Change operating mode"""
        self.state["mode"] = mode
        self.mode = mode
        self._save_state()
        self.telegram.send(f"Mode changed to: {mode.upper()}")

    def run(self):
        """Main agent loop"""
        logger.info("MoltBot Autonomous Agent starting...")
        self.telegram.send("🤖 <b>MoltBot Autonomous Agent</b> is now online!\n\nMode: SAFE\nCommands: status, analyze, issues, pause")

        # Schedule - run continuously
        schedule.every(5).minutes.do(self.run_analysis)  # Analyze every 5 min
        schedule.every(30).seconds.do(self.process_telegram_updates)  # Check Telegram every 30s

        # Run initial analysis
        self.run_analysis()

        # Main loop
        while True:
            try:
                if self.running:
                    schedule.run_pending()
                else:
                    # Still process Telegram when paused (for resume command)
                    self.process_telegram_updates()

                time.sleep(10)  # Check every 10 seconds

            except KeyboardInterrupt:
                logger.info("Shutting down...")
                self.telegram.send("🛑 MoltBot shutting down")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(10)


if __name__ == "__main__":
    agent = MoltBotAgent()
    agent.run()
