#!/usr/bin/env python3
"""
MoltBot Autonomous Agent v2
Intelligent BB5 monitoring with detailed metrics and meaningful reports.
"""

import os
import sys
import json
import time
import logging
import subprocess
import requests
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
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
    """Send intelligent notifications via Telegram"""

    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}"

    def send(self, message: str, parse_mode: str = "HTML", topic_id: Optional[int] = None) -> bool:
        """Send a message to Telegram"""
        try:
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": parse_mode,
                "disable_notification": False
            }
            if topic_id:
                payload["message_thread_id"] = topic_id

            response = requests.post(
                f"{self.base_url}/sendMessage",
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            logger.info(f"Telegram message sent: {message[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False

    def send_intelligent_report(self, report: Dict, topic_id: Optional[int] = None):
        """Send comprehensive intelligent activity report"""
        period = report.get('period', 'Last period')

        message = f"📊 <b>BB5 Activity Report</b>\n"
        message += f"<i>{period}</i>\n"
        message += "━" * 30 + "\n\n"

        # Git metrics
        git = report.get('git', {})
        if git.get('commits', 0) > 0:
            message += f"<b>🔄 Git Activity</b>\n"
            message += f"• Commits: {git.get('commits', 0)}\n"
            message += f"• Pushed: {git.get('pushed', 0)}\n"
            message += f"• Branches: {git.get('branches', 0)}\n"
            if git.get('authors'):
                message += f"• Authors: {', '.join(git['authors'][:3])}\n"
            message += "\n"

        # Task metrics
        tasks = report.get('tasks', {})
        message += f"<b>✅ Tasks</b>\n"
        message += f"• Completed: {tasks.get('completed', 0)}\n"
        message += f"• Started: {tasks.get('started', 0)}\n"
        message += f"• In Progress: {tasks.get('in_progress', 0)}\n"
        message += f"• Pending: {tasks.get('pending', 0)}\n\n"

        # Agent metrics
        agents = report.get('agents', {})
        if agents.get('active_count', 0) > 0:
            message += f"<b>🤖 Agents</b>\n"
            message += f"• Active: {agents.get('active_count', 0)}\n"
            message += f"• Runs: {agents.get('runs', 0)}\n"
            if agents.get('names'):
                message += f"• Types: {', '.join(agents['names'][:3])}\n"
            message += "\n"

        # Work output
        work = report.get('work', {})
        if work.get('files_changed', 0) > 0:
            message += f"<b>📁 Work Output</b>\n"
            message += f"• Files Changed: {work.get('files_changed', 0)}\n"
            message += f"• Insertions: +{work.get('insertions', 0)}\n"
            message += f"• Deletions: -{work.get('deletions', 0)}\n\n"

        # Token usage (if available)
        tokens = report.get('tokens', {})
        if tokens.get('total', 0) > 0:
            message += f"<b>💰 Token Usage</b>\n"
            message += f"• Total: {self._format_number(tokens.get('total', 0))}\n"
            message += f"• Input: {self._format_number(tokens.get('input', 0))}\n"
            message += f"• Output: {self._format_number(tokens.get('output', 0))}\n\n"

        # Key accomplishments
        accomplishments = report.get('accomplishments', [])
        if accomplishments:
            message += f"<b>🏆 Key Accomplishments</b>\n"
            for i, acc in enumerate(accomplishments[:5], 1):
                desc = acc.get('description', 'Unknown')[:60]
                message += f"{i}. {desc}{'...' if len(acc.get('description', '')) > 60 else ''}\n"
            message += "\n"

        # Current activity
        current = report.get('current', {})
        if current.get('active_tasks', 0) > 0:
            message += f"<b>🔄 Currently Active</b>\n"
            message += f"• Tasks: {current.get('active_tasks', 0)}\n"
            if current.get('latest_task'):
                message += f"• Latest: {current['latest_task'][:50]}...\n"
            message += "\n"

        message += "<i>Reply 'details' for full breakdown</i>"

        self.send(message, topic_id=topic_id)

    def send_detailed_breakdown(self, report: Dict, topic_id: Optional[int] = None):
        """Send detailed breakdown of all activity"""
        message = f"📋 <b>Detailed Activity Breakdown</b>\n"
        message += f"<i>{report.get('period', '')}</i>\n\n"

        # Git commits detail
        git = report.get('git', {})
        commits = git.get('commit_list', [])
        if commits:
            message += f"<b>📝 Commits ({len(commits)})</b>\n"
            for commit in commits[:10]:
                sha = commit.get('sha', '????')[:7]
                msg = commit.get('message', 'No message')[:50]
                message += f"<code>{sha}</code> {msg}{'...' if len(commit.get('message', '')) > 50 else ''}\n"
            if len(commits) > 10:
                message += f"... and {len(commits) - 10} more\n"
            message += "\n"

        # Task details
        tasks = report.get('tasks', {})
        completed_list = tasks.get('completed_list', [])
        if completed_list:
            message += f"<b>✅ Completed Tasks ({len(completed_list)})</b>\n"
            for task in completed_list[:10]:
                task_id = task.get('id', 'Unknown')
                desc = task.get('description', '')[:40]
                message += f"• {task_id}: {desc}{'...' if len(task.get('description', '')) > 40 else ''}\n"
            if len(completed_list) > 10:
                message += f"... and {len(completed_list) - 10} more\n"
            message += "\n"

        # Agent run details
        agents = report.get('agents', {})
        runs = agents.get('run_details', [])
        if runs:
            message += f"<b>🤖 Agent Runs ({len(runs)})</b>\n"
            for run in runs[:10]:
                agent = run.get('agent', 'Unknown')
                task = run.get('task_id', 'No task')
                message += f"• {agent}: {task[:40]}{'...' if len(task) > 40 else ''}\n"
            if len(runs) > 10:
                message += f"... and {len(runs) - 10} more\n"
            message += "\n"

        # Files changed
        work = report.get('work', {})
        files = work.get('file_list', [])
        if files:
            message += f"<b>📁 Files Changed ({len(files)})</b>\n"
            for f in files[:15]:
                message += f"• {f}\n"
            if len(files) > 15:
                message += f"... and {len(files) - 15} more\n"

        self.send(message, topic_id=topic_id)

    def _format_number(self, n: int) -> str:
        """Format large numbers with K/M suffixes"""
        if n >= 1_000_000:
            return f"{n/1_000_000:.1f}M"
        elif n >= 1_000:
            return f"{n/1_000:.1f}K"
        return str(n)


class BB5MetricsCollector:
    """Collect real metrics from BB5"""

    def __init__(self, bb5_dir: Path):
        self.bb5_dir = bb5_dir
        self.project_memory = bb5_dir / "5-project-memory" / "blackbox5"
        self.autonomous_dir = self.project_memory / ".autonomous"

    def collect_git_metrics(self, since_hours: int = 24) -> Dict:
        """Collect git metrics for the period"""
        since = (datetime.now() - timedelta(hours=since_hours)).strftime("%Y-%m-%d %H:%M:%S")

        metrics = {
            'commits': 0,
            'pushed': 0,
            'branches': 0,
            'authors': set(),
            'commit_list': [],
            'insertions': 0,
            'deletions': 0
        }

        try:
            # Get commits
            result = subprocess.run(
                ["git", "log", f"--since={since}", "--pretty=format:%H|%s|%an|%ci", "--shortstat"],
                cwd=self.bb5_dir,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                commits = result.stdout.strip().split('\n\n')
                for commit_block in commits:
                    lines = commit_block.split('\n')
                    if lines and '|' in lines[0]:
                        parts = lines[0].split('|')
                        if len(parts) >= 4:
                            metrics['commits'] += 1
                            metrics['authors'].add(parts[2])
                            metrics['commit_list'].append({
                                'sha': parts[0],
                                'message': parts[1],
                                'author': parts[2],
                                'date': parts[3]
                            })

                    # Parse shortstat for insertions/deletions
                    if len(lines) > 1:
                        stat_line = lines[1]
                        insertions = re.search(r'(\d+) insertions?', stat_line)
                        deletions = re.search(r'(\d+) deletions?', stat_line)
                        if insertions:
                            metrics['insertions'] += int(insertions.group(1))
                        if deletions:
                            metrics['deletions'] += int(deletions.group(1))

            # Count branches
            result = subprocess.run(
                ["git", "branch", "-a"],
                cwd=self.bb5_dir,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                metrics['branches'] = len([b for b in result.stdout.strip().split('\n') if b.strip()])

            # Check if commits were pushed (compare local vs remote)
            result = subprocess.run(
                ["git", "log", f"--since={since}", "--oneline", "--decorate"],
                cwd=self.bb5_dir,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                # Count commits that appear on remote branches
                pushed_commits = [l for l in result.stdout.split('\n') if '[origin/' in l or 'origin/' in l]
                metrics['pushed'] = len(pushed_commits)

        except Exception as e:
            logger.error(f"Error collecting git metrics: {e}")

        metrics['authors'] = list(metrics['authors'])
        return metrics

    def collect_task_metrics(self) -> Dict:
        """Collect task metrics from filesystem"""
        metrics = {
            'completed': 0,
            'started': 0,
            'in_progress': 0,
            'pending': 0,
            'completed_list': [],
            'in_progress_list': []
        }

        try:
            # Check active tasks
            active_dir = self.autonomous_dir / "tasks" / "active"
            if active_dir.exists():
                for task_file in active_dir.glob("TASK-*.md"):
                    content = task_file.read_text()
                    task_id = task_file.stem

                    if "Status:** completed" in content or "status: completed" in content:
                        metrics['completed'] += 1
                        metrics['completed_list'].append({
                            'id': task_id,
                            'description': self._extract_task_description(content)
                        })
                    elif "Status:** in_progress" in content or "status: in_progress" in content:
                        metrics['in_progress'] += 1
                        metrics['in_progress_list'].append({
                            'id': task_id,
                            'description': self._extract_task_description(content)
                        })
                    elif "Status:** pending" in content or "status: pending" in content:
                        metrics['pending'] += 1

            # Check completed tasks
            completed_dir = self.autonomous_dir / "tasks" / "completed"
            if completed_dir.exists():
                metrics['completed'] += len(list(completed_dir.glob("TASK-*.md")))

        except Exception as e:
            logger.error(f"Error collecting task metrics: {e}")

        return metrics

    def collect_agent_metrics(self, since_hours: int = 24) -> Dict:
        """Collect agent activity metrics from events"""
        metrics = {
            'active_count': 0,
            'runs': 0,
            'names': set(),
            'run_details': []
        }

        events_file = self.autonomous_dir / "agents" / "communications" / "events.yaml"
        if not events_file.exists():
            return metrics

        try:
            since = datetime.now() - timedelta(hours=since_hours)

            with open(events_file, 'r') as f:
                data = yaml.safe_load(f)
                if not data:
                    return metrics

                for event in data:
                    if not isinstance(event, dict):
                        continue

                    # Parse timestamp
                    ts_str = event.get('timestamp', '')
                    event_time = self._parse_timestamp(ts_str)
                    if not event_time or event_time < since:
                        continue

                    event_type = event.get('type', '').lower()
                    agent = event.get('agent', event.get('agent_type', ''))

                    if agent and agent != 'unknown':
                        metrics['names'].add(agent)

                    if 'start' in event_type or event_type == 'started':
                        metrics['runs'] += 1
                        metrics['run_details'].append({
                            'agent': agent,
                            'task_id': event.get('task_id', ''),
                            'timestamp': ts_str
                        })

        except Exception as e:
            logger.error(f"Error collecting agent metrics: {e}")

        metrics['active_count'] = len(metrics['names'])
        metrics['names'] = list(metrics['names'])
        return metrics

    def collect_work_metrics(self, since_hours: int = 24) -> Dict:
        """Collect work output metrics"""
        metrics = {
            'files_changed': 0,
            'insertions': 0,
            'deletions': 0,
            'file_list': []
        }

        try:
            since = (datetime.now() - timedelta(hours=since_hours)).strftime("%Y-%m-%d %H:%M:%S")

            # Get diff stats
            result = subprocess.run(
                ["git", "diff", f"--since={since}", "--stat"],
                cwd=self.bb5_dir,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if '|' in line:
                        parts = line.split('|')
                        if len(parts) >= 2:
                            filename = parts[0].strip()
                            metrics['file_list'].append(filename)

                            # Parse changes
                            changes = parts[1].strip()
                            if '+' in changes:
                                plus_count = changes.count('+')
                                metrics['insertions'] += plus_count
                            if '-' in changes:
                                minus_count = changes.count('-')
                                metrics['deletions'] += minus_count

                metrics['files_changed'] = len(metrics['file_list'])

        except Exception as e:
            logger.error(f"Error collecting work metrics: {e}")

        return metrics

    def collect_token_metrics(self, since_hours: int = 24) -> Dict:
        """Collect token usage from chat logs"""
        metrics = {
            'total': 0,
            'input': 0,
            'output': 0
        }

        try:
            # Look for token usage in recent chat logs
            memory_dir = self.autonomous_dir / "memory" / "chat-logs"
            if not memory_dir.exists():
                return metrics

            since = datetime.now() - timedelta(hours=since_hours)

            for log_file in memory_dir.glob("*.jsonl"):
                # Check if file is recent
                mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                if mtime < since:
                    continue

                with open(log_file, 'r') as f:
                    for line in f:
                        try:
                            entry = json.loads(line.strip())
                            # Look for token usage in metadata
                            metadata = entry.get('metadata', {})
                            if 'tokens' in metadata:
                                metrics['total'] += metadata['tokens']
                            if 'input_tokens' in metadata:
                                metrics['input'] += metadata['input_tokens']
                            if 'output_tokens' in metadata:
                                metrics['output'] += metadata['output_tokens']
                        except:
                            continue

        except Exception as e:
            logger.error(f"Error collecting token metrics: {e}")

        return metrics

    def collect_accomplishments(self, since_hours: int = 24) -> List[Dict]:
        """Collect accomplishments from RESULTS.md files"""
        accomplishments = []

        try:
            since = datetime.now() - timedelta(hours=since_hours)
            runs_dir = self.autonomous_dir / "runs"

            for run_dir in runs_dir.glob("run-*"):
                # Check if run is recent
                mtime = datetime.fromtimestamp(run_dir.stat().st_mtime)
                if mtime < since:
                    continue

                results_file = run_dir / "RESULTS.md"
                if results_file.exists():
                    content = results_file.read_text()

                    # Extract accomplishments from RESULTS.md
                    if "Status: COMPLETED" in content or "Status:** COMPLETED" in content:
                        # Extract first meaningful line after status
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if 'COMPLETED' in line and i + 1 < len(lines):
                                desc = lines[i + 1].strip()
                                if desc and not desc.startswith('#') and not desc.startswith('-'):
                                    accomplishments.append({
                                        'run': run_dir.name,
                                        'description': desc[:200],
                                        'timestamp': mtime.isoformat()
                                    })
                                    break

        except Exception as e:
            logger.error(f"Error collecting accomplishments: {e}")

        return accomplishments

    def get_current_activity(self) -> Dict:
        """Get currently active work"""
        activity = {
            'active_tasks': 0,
            'latest_task': None,
            'active_agents': []
        }

        try:
            # Count in-progress tasks
            active_dir = self.autonomous_dir / "tasks" / "active"
            if active_dir.exists():
                in_progress = []
                for task_file in active_dir.glob("TASK-*.md"):
                    content = task_file.read_text()
                    if "Status:** in_progress" in content or "status: in_progress" in content:
                        in_progress.append(task_file.stem)

                activity['active_tasks'] = len(in_progress)
                if in_progress:
                    activity['latest_task'] = in_progress[-1]

            # Check current run
            current_link = self.autonomous_dir / "runs" / "current"
            if current_link.exists() and current_link.is_symlink():
                current_run = current_link.resolve()
                if current_run.exists():
                    results = current_run / "RESULTS.md"
                    if results.exists():
                        content = results.read_text()
                        if "IN_PROGRESS" in content:
                            activity['active_agents'].append(f"Run: {current_run.name}")

        except Exception as e:
            logger.error(f"Error getting current activity: {e}")

        return activity

    def _extract_task_description(self, content: str) -> str:
        """Extract task description from task file content"""
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('**'):
                return line[:100]
        return "No description"

    def _parse_timestamp(self, ts_str: str) -> Optional[datetime]:
        """Parse various timestamp formats"""
        formats = [
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%S.%f%z",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(ts_str, fmt)
            except ValueError:
                continue
        try:
            return datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
        except:
            pass
        return None


class MoltBotAgent:
    """Main MoltBot Autonomous Agent"""

    def __init__(self):
        self.telegram = TelegramNotifier(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        self.metrics = BB5MetricsCollector(BB5_DIR)
        self.state_file = STATE_DIR / "agent_state.json"
        self.mode = "safe"
        self.running = True
        self.topic_id = None  # Set this to your Blackbox topic ID

        # Load state
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """Load agent state from disk"""
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return {
            "mode": "safe",
            "last_report": None,
            "report_count": 0,
            "total_commits_tracked": 0
        }

    def _save_state(self):
        """Save agent state to disk"""
        self.state_file.write_text(json.dumps(self.state, indent=2))

    def generate_report(self, hours: int = 1) -> Dict:
        """Generate comprehensive activity report"""
        logger.info(f"Generating report for last {hours} hour(s)...")

        report = {
            'period': f"Last {hours} hour(s)",
            'timestamp': datetime.now().isoformat(),
            'git': self.metrics.collect_git_metrics(hours),
            'tasks': self.metrics.collect_task_metrics(),
            'agents': self.metrics.collect_agent_metrics(hours),
            'work': self.metrics.collect_work_metrics(hours),
            'tokens': self.metrics.collect_token_metrics(hours),
            'accomplishments': self.metrics.collect_accomplishments(hours),
            'current': self.metrics.get_current_activity()
        }

        return report

    def send_periodic_report(self, hours: int = 1):
        """Send periodic activity report"""
        report = self.generate_report(hours)

        # Update state
        self.state["last_report"] = datetime.now().isoformat()
        self.state["report_count"] = self.state.get("report_count", 0) + 1
        self.state["total_commits_tracked"] = self.state.get("total_commits_tracked", 0) + report['git'].get('commits', 0)
        self._save_state()

        # Send to Telegram
        self.telegram.send_intelligent_report(report, topic_id=self.topic_id)
        logger.info(f"Report sent. Commits: {report['git'].get('commits', 0)}, Tasks: {report['tasks'].get('completed', 0)}")

    def send_daily_summary(self):
        """Send daily summary report"""
        report = self.generate_report(24)

        message = f"📊 <b>BB5 Daily Summary</b>\n"
        message += f"<i>{datetime.now().strftime('%Y-%m-%d')}</i>\n"
        message += "━" * 30 + "\n\n"

        # Key metrics
        git = report.get('git', {})
        tasks = report.get('tasks', {})
        agents = report.get('agents', {})
        work = report.get('work', {})

        message += f"<b>🎯 Key Metrics (24h)</b>\n"
        message += f"• Commits: {git.get('commits', 0)}\n"
        message += f"• Tasks Completed: {tasks.get('completed', 0)}\n"
        message += f"• Agent Runs: {agents.get('runs', 0)}\n"
        message += f"• Files Changed: {work.get('files_changed', 0)}\n"
        message += f"• Lines: +{work.get('insertions', 0)}/-{work.get('deletions', 0)}\n\n"

        # Top accomplishments
        accomplishments = report.get('accomplishments', [])
        if accomplishments:
            message += f"<b>🏆 Top Accomplishments</b>\n"
            for i, acc in enumerate(accomplishments[:3], 1):
                desc = acc.get('description', '')[:50]
                message += f"{i}. {desc}{'...' if len(acc.get('description', '')) > 50 else ''}\n"
            message += "\n"

        # Current status
        current = report.get('current', {})
        message += f"<b>📊 Current Status</b>\n"
        message += f"• Active Tasks: {current.get('active_tasks', 0)}\n"
        message += f"• Pending: {tasks.get('pending', 0)}\n"
        message += f"• In Progress: {tasks.get('in_progress', 0)}\n\n"

        message += "<i>Reply 'report' for detailed breakdown</i>"

        self.telegram.send(message, topic_id=self.topic_id)
        logger.info("Daily summary sent")

    def process_telegram_commands(self):
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

        # Check if message is in a topic
        if message.get("is_topic_message"):
            self.topic_id = message.get("message_thread_id")

        logger.info(f"Received command: {text}")

        # Command handlers
        if text == "status":
            self._cmd_status()
        elif text == "report":
            self.send_periodic_report(hours=1)
        elif text == "daily":
            self.send_daily_summary()
        elif text == "details":
            self._cmd_details()
        elif text == "git":
            self._cmd_git()
        elif text == "tasks":
            self._cmd_tasks()
        elif text == "pause":
            self._cmd_pause()
        elif text == "resume":
            self._cmd_resume()
        elif text.startswith("report "):
            try:
                hours = int(text[7:])
                self.send_periodic_report(hours=hours)
            except ValueError:
                self.telegram.send("Usage: report [hours]", topic_id=self.topic_id)
        else:
            self.telegram.send(
                "Commands: status, report, daily, details, git, tasks, pause, resume",
                topic_id=self.topic_id
            )

    def _cmd_status(self):
        """Send current status"""
        current = self.metrics.get_current_activity()
        tasks = self.metrics.collect_task_metrics()

        message = f"📊 <b>BB5 Current Status</b>\n\n"
        message += f"<b>Tasks</b>\n"
        message += f"• Active: {current.get('active_tasks', 0)}\n"
        message += f"• Pending: {tasks.get('pending', 0)}\n"
        message += f"• In Progress: {tasks.get('in_progress', 0)}\n"
        message += f"• Completed (total): {tasks.get('completed', 0)}\n\n"

        if current.get('latest_task'):
            message += f"<b>Latest Activity:</b> {current['latest_task']}\n\n"

        message += f"<b>Mode:</b> {self.mode.upper()}\n"
        message += f"<b>Reports Sent:</b> {self.state.get('report_count', 0)}"

        self.telegram.send(message, topic_id=self.topic_id)

    def _cmd_details(self):
        """Send detailed breakdown"""
        report = self.generate_report(hours=24)
        self.telegram.send_detailed_breakdown(report, topic_id=self.topic_id)

    def _cmd_git(self):
        """Send git stats"""
        git = self.metrics.collect_git_metrics(24)

        message = f"🔄 <b>Git Activity (24h)</b>\n\n"
        message += f"Commits: {git.get('commits', 0)}\n"
        message += f"Pushed: {git.get('pushed', 0)}\n"
        message += f"Branches: {git.get('branches', 0)}\n"
        message += f"Insertions: +{git.get('insertions', 0)}\n"
        message += f"Deletions: -{git.get('deletions', 0)}\n\n"

        if git.get('authors'):
            message += f"<b>Authors:</b> {', '.join(git['authors'])}"

        self.telegram.send(message, topic_id=self.topic_id)

    def _cmd_tasks(self):
        """Send task list"""
        tasks = self.metrics.collect_task_metrics()

        message = f"📋 <b>Tasks</b>\n\n"
        message += f"Completed: {tasks.get('completed', 0)}\n"
        message += f"In Progress: {tasks.get('in_progress', 0)}\n"
        message += f"Pending: {tasks.get('pending', 0)}\n\n"

        in_progress = tasks.get('in_progress_list', [])
        if in_progress:
            message += f"<b>In Progress:</b>\n"
            for task in in_progress[:5]:
                message += f"• {task['id']}\n"

        self.telegram.send(message, topic_id=self.topic_id)

    def _cmd_pause(self):
        """Pause autonomous operation"""
        self.running = False
        self.telegram.send("⏸️ MoltBot paused. Send 'resume' to restart.", topic_id=self.topic_id)

    def _cmd_resume(self):
        """Resume autonomous operation"""
        self.running = True
        self.telegram.send("▶️ MoltBot resumed.", topic_id=self.topic_id)

    def run(self):
        """Main agent loop"""
        logger.info("MoltBot Autonomous Agent v2 starting...")
        self.telegram.send(
            "🤖 <b>MoltBot v2</b> is now online!\n\n"
            "I'll send intelligent reports with real metrics.\n"
            "Commands: status, report, daily, details, git, tasks",
            topic_id=self.topic_id
        )

        # Schedule reports
        # Hourly reports during business hours
        schedule.every().hour.at(":00").do(
            lambda: self.send_periodic_report(hours=1)
            if 9 <= datetime.now().hour <= 21 else None
        )

        # Daily summary at 9 AM
        schedule.every().day.at("09:00").do(self.send_daily_summary)

        # Process Telegram commands every 30 seconds
        schedule.every(30).seconds.do(self.process_telegram_commands)

        # Main loop
        while True:
            try:
                if self.running:
                    schedule.run_pending()
                else:
                    self.process_telegram_commands()

                time.sleep(10)

            except KeyboardInterrupt:
                logger.info("Shutting down...")
                self.telegram.send("🛑 MoltBot shutting down", topic_id=self.topic_id)
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(10)


if __name__ == "__main__":
    agent = MoltBotAgent()
    agent.run()
