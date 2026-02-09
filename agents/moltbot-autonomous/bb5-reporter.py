#!/usr/bin/env python3
"""
BB5 Agent Activity Reporter
Periodically reports what BB5 agents have accomplished to Telegram.
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
from typing import Dict, List, Optional, Set
from collections import defaultdict
import yaml
import schedule

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8581639813:AAFA13wDTKEX2x6J-lVfpq9QHnsGRnB1EZo")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7643203581")
BB5_DIR = Path("/opt/blackbox5")
STATE_DIR = BB5_DIR / "agents" / "moltbot-autonomous" / "state"
LOG_DIR = BB5_DIR / ".logs" / "bb5-reporter"

# BB5 paths
PROJECT_MEMORY = BB5_DIR / "5-project-memory" / "blackbox5"
AUTONOMOUS_DIR = PROJECT_MEMORY / ".autonomous"
EVENTS_FILE = AUTONOMOUS_DIR / "agents" / "communications" / "events.yaml"
TASKS_DIR = AUTONOMOUS_DIR / "tasks"
RUNS_DIR = AUTONOMOUS_DIR / "runs"

# Setup logging
LOG_DIR.mkdir(parents=True, exist_ok=True)
STATE_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "bb5-reporter.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("bb5-reporter")


class TelegramNotifier:
    """Send notifications via Telegram"""

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

    def send_activity_report(self, report: Dict, topic_id: Optional[int] = None):
        """Send formatted activity report"""
        period = report.get('period', 'Unknown period')
        total_events = report.get('total_events', 0)
        agents_active = report.get('agents_active', [])
        tasks_completed = report.get('tasks_completed', [])
        tasks_started = report.get('tasks_started', [])
        discoveries = report.get('discoveries', [])

        message = f"📊 <b>BB5 Agent Activity Report</b>\n"
        message += f"<i>{period}</i>\n"
        message += "━" * 25 + "\n\n"

        # Summary stats
        message += f"<b>📈 Summary</b>\n"
        message += f"• Total Events: {total_events}\n"
        message += f"• Active Agents: {len(agents_active)}\n"
        message += f"• Tasks Started: {len(tasks_started)}\n"
        message += f"• Tasks Completed: {len(tasks_completed)}\n"
        message += f"• Discoveries: {len(discoveries)}\n\n"

        # Agents active
        if agents_active:
            message += f"<b>🤖 Active Agents</b>\n"
            for agent in agents_active[:5]:
                message += f"• {agent}\n"
            if len(agents_active) > 5:
                message += f"... and {len(agents_active) - 5} more\n"
            message += "\n"

        # Tasks completed
        if tasks_completed:
            message += f"<b>✅ Tasks Completed</b>\n"
            for task in tasks_completed[:3]:
                task_id = task.get('task_id', 'Unknown')
                agent = task.get('agent', 'Unknown')
                message += f"• {task_id} ({agent})\n"
            if len(tasks_completed) > 3:
                message += f"... and {len(tasks_completed) - 3} more\n"
            message += "\n"

        # Discoveries
        if discoveries:
            message += f"<b>💡 Key Discoveries</b>\n"
            for disc in discoveries[:3]:
                msg = disc.get('message', 'No details')
                message += f"• {msg[:60]}...\n" if len(msg) > 60 else f"• {msg}\n"
            if len(discoveries) > 3:
                message += f"... and {len(discoveries) - 3} more\n"
            message += "\n"

        # Current status
        current_tasks = report.get('current_tasks', [])
        if current_tasks:
            message += f"<b>🔄 In Progress</b>\n"
            for task in current_tasks[:3]:
                task_id = task.get('task_id', 'Unknown')
                message += f"• {task_id}\n"
            if len(current_tasks) > 3:
                message += f"... and {len(current_tasks) - 3} more\n"
            message += "\n"

        message += "<b>Reply:</b>\n"
        message += "• <code>status</code> - Full status\n"
        message += "• <code>tasks</code> - All tasks\n"
        message += "• <code>agents</code> - Agent details"

        self.send(message, topic_id=topic_id)


class BB5ActivityAnalyzer:
    """Analyze BB5 agent activity from events and state"""

    def __init__(self, bb5_dir: Path):
        self.bb5_dir = bb5_dir
        self.project_memory = bb5_dir / "5-project-memory" / "blackbox5"
        self.autonomous_dir = self.project_memory / ".autonomous"
        self.events_file = self.autonomous_dir / "agents" / "communications" / "events.yaml"

    def parse_timestamp(self, ts_str: str) -> Optional[datetime]:
        """Parse various timestamp formats"""
        formats = [
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%S.%f%z",
            "%Y-%m-%d %H:%M:%S",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(ts_str, fmt)
            except ValueError:
                continue
        # Try ISO format
        try:
            return datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
        except:
            pass
        return None

    def load_events(self, since: Optional[datetime] = None) -> List[Dict]:
        """Load events from events.yaml"""
        events = []

        if not self.events_file.exists():
            logger.warning(f"Events file not found: {self.events_file}")
            return events

        try:
            with open(self.events_file, 'r') as f:
                data = yaml.safe_load(f)
                if not data:
                    return events

                for event in data:
                    if not isinstance(event, dict):
                        continue

                    # Parse timestamp
                    ts_str = event.get('timestamp', '')
                    event_time = self.parse_timestamp(ts_str)

                    if event_time and since and event_time < since:
                        continue

                    events.append({
                        'timestamp': event_time or ts_str,
                        'type': event.get('type', 'unknown'),
                        'agent': event.get('agent', event.get('agent_type', 'unknown')),
                        'task_id': event.get('task_id', ''),
                        'run_id': event.get('run_id', ''),
                        'message': event.get('notes', event.get('message', '')),
                        'data': event.get('data', {}),
                        'raw': event
                    })

        except Exception as e:
            logger.error(f"Error loading events: {e}")

        # Sort by timestamp
        events.sort(key=lambda x: x['timestamp'] if isinstance(x['timestamp'], datetime) else datetime.min)
        return events

    def analyze_activity(self, hours: int = 1) -> Dict:
        """Analyze activity over the last N hours"""
        since = datetime.now() - timedelta(hours=hours)
        events = self.load_events(since=since)

        # Categorize events
        agents_active = set()
        tasks_started = []
        tasks_completed = []
        tasks_in_progress = []
        discoveries = []
        errors = []
        decisions = []

        for event in events:
            event_type = event['type'].lower()
            agent = event['agent']

            if agent and agent != 'unknown':
                agents_active.add(agent)

            if 'start' in event_type or event_type == 'started':
                tasks_started.append(event)
            elif 'complete' in event_type or event_type == 'completed':
                tasks_completed.append(event)
            elif 'progress' in event_type or event_type == 'in_progress':
                tasks_in_progress.append(event)
            elif 'discover' in event_type or event_type == 'discovery':
                discoveries.append(event)
            elif 'error' in event_type or event_type == 'failed':
                errors.append(event)
            elif 'decision' in event_type:
                decisions.append(event)

        # Get current tasks from filesystem
        current_tasks = self.get_current_tasks()

        return {
            'period': f"Last {hours} hour(s)",
            'since': since.isoformat(),
            'total_events': len(events),
            'agents_active': sorted(list(agents_active)),
            'tasks_started': tasks_started,
            'tasks_completed': tasks_completed,
            'tasks_in_progress': tasks_in_progress,
            'current_tasks': current_tasks,
            'discoveries': discoveries,
            'errors': errors,
            'decisions': decisions
        }

    def get_current_tasks(self) -> List[Dict]:
        """Get currently active tasks from filesystem"""
        tasks = []
        active_dir = self.autonomous_dir / "tasks" / "active"

        if not active_dir.exists():
            return tasks

        try:
            for task_file in active_dir.glob("TASK-*.md"):
                content = task_file.read_text()
                # Extract basic info
                task_id = task_file.stem
                status = "unknown"

                if "Status:** in_progress" in content or "Status: in_progress" in content:
                    status = "in_progress"
                elif "Status:** pending" in content or "Status: pending" in content:
                    status = "pending"

                tasks.append({
                    'task_id': task_id,
                    'status': status,
                    'file': str(task_file)
                })
        except Exception as e:
            logger.error(f"Error reading tasks: {e}")

        return tasks

    def get_recent_runs(self, limit: int = 5) -> List[Dict]:
        """Get recent run directories"""
        runs = []

        if not RUNS_DIR.exists():
            return runs

        try:
            run_dirs = sorted(RUNS_DIR.glob("run-*"), key=lambda x: x.stat().st_mtime, reverse=True)
            for run_dir in run_dirs[:limit]:
                results_file = run_dir / "RESULTS.md"
                status = "unknown"
                if results_file.exists():
                    content = results_file.read_text()
                    if "COMPLETE" in content or "COMPLETED" in content:
                        status = "completed"
                    elif "PARTIAL" in content:
                        status = "partial"
                    elif "FAILED" in content:
                        status = "failed"

                runs.append({
                    'run_id': run_dir.name,
                    'status': status,
                    'modified': datetime.fromtimestamp(run_dir.stat().st_mtime).isoformat()
                })
        except Exception as e:
            logger.error(f"Error reading runs: {e}")

        return runs


class BB5Reporter:
    """Main BB5 Reporter Agent"""

    def __init__(self):
        self.telegram = TelegramNotifier(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        self.analyzer = BB5ActivityAnalyzer(BB5_DIR)
        self.state_file = STATE_DIR / "reporter_state.json"
        self.running = True
        self.topic_id = None  # Telegram topic ID for Blackbox channel

        # Load state
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """Load reporter state from disk"""
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return {
            "last_report_time": None,
            "report_count": 0,
            "total_events_reported": 0
        }

    def _save_state(self):
        """Save reporter state to disk"""
        self.state_file.write_text(json.dumps(self.state, indent=2))

    def generate_report(self, hours: int = 1) -> Dict:
        """Generate activity report for the last N hours"""
        logger.info(f"Generating report for last {hours} hour(s)...")
        return self.analyzer.analyze_activity(hours=hours)

    def send_periodic_update(self, hours: int = 1, topic_id: Optional[int] = None):
        """Send periodic activity update"""
        report = self.generate_report(hours=hours)

        # Update state
        self.state["last_report_time"] = datetime.now().isoformat()
        self.state["report_count"] = self.state.get("report_count", 0) + 1
        self.state["total_events_reported"] = self.state.get("total_events_reported", 0) + report.get('total_events', 0)
        self._save_state()

        # Send to Telegram
        self.telegram.send_activity_report(report, topic_id=topic_id)
        logger.info(f"Periodic update sent. Events: {report['total_events']}")

    def send_daily_summary(self, topic_id: Optional[int] = None):
        """Send daily summary"""
        report = self.generate_report(hours=24)

        message = f"📊 <b>BB5 Daily Summary</b>\n"
        message += f"<i>{datetime.now().strftime('%Y-%m-%d')}</i>\n"
        message += "━" * 25 + "\n\n"

        # Key metrics
        tasks_completed = len(report.get('tasks_completed', []))
        agents_active = len(report.get('agents_active', []))
        discoveries = len(report.get('discoveries', []))

        message += f"<b>🎯 Key Metrics (24h)</b>\n"
        message += f"• Tasks Completed: {tasks_completed}\n"
        message += f"• Agents Active: {agents_active}\n"
        message += f"• Discoveries Made: {discoveries}\n\n"

        # Recent runs
        recent_runs = self.analyzer.get_recent_runs(3)
        if recent_runs:
            message += f"<b>🔄 Recent Runs</b>\n"
            for run in recent_runs:
                status_emoji = {"completed": "✅", "partial": "⚠️", "failed": "❌"}.get(run['status'], "⏳")
                message += f"{status_emoji} {run['run_id']}\n"
            message += "\n"

        # Current status
        current_tasks = report.get('current_tasks', [])
        pending = len([t for t in current_tasks if t.get('status') == 'pending'])
        in_progress = len([t for t in current_tasks if t.get('status') == 'in_progress'])

        message += f"<b>📋 Current Queue</b>\n"
        message += f"• Pending: {pending}\n"
        message += f"• In Progress: {in_progress}\n\n"

        message += "<i>Reply 'status' for detailed info</i>"

        self.telegram.send(message, topic_id=topic_id)
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

        # Check if message is in the Blackbox topic
        if message.get("is_topic_message"):
            self.topic_id = message.get("message_thread_id")

        logger.info(f"Received command: {text}")

        # Command handlers
        if text == "status":
            self._cmd_status()
        elif text == "tasks":
            self._cmd_tasks()
        elif text == "agents":
            self._cmd_agents()
        elif text == "report":
            self.send_periodic_update(hours=1, topic_id=self.topic_id)
        elif text == "daily":
            self.send_daily_summary(topic_id=self.topic_id)
        elif text.startswith("report "):
            try:
                hours = int(text[7:])
                self.send_periodic_update(hours=hours, topic_id=self.topic_id)
            except ValueError:
                self.telegram.send("Usage: report [hours]", topic_id=self.topic_id)

    def _cmd_status(self):
        """Send detailed status"""
        report = self.generate_report(hours=24)

        message = f"📊 <b>BB5 Detailed Status</b>\n\n"

        # Agent activity
        agents = report.get('agents_active', [])
        message += f"<b>Active Agents (24h):</b> {len(agents)}\n"
        for agent in agents:
            message += f"  • {agent}\n"
        message += "\n"

        # Task stats
        started = len(report.get('tasks_started', []))
        completed = len(report.get('tasks_completed', []))
        in_progress = len(report.get('tasks_in_progress', []))

        message += f"<b>Task Activity (24h):</b>\n"
        message += f"  Started: {started}\n"
        message += f"  Completed: {completed}\n"
        message += f"  In Progress: {in_progress}\n\n"

        # Errors
        errors = report.get('errors', [])
        if errors:
            message += f"<b>⚠️ Errors (24h):</b> {len(errors)}\n"
            for err in errors[:3]:
                msg = err.get('message', 'Unknown error')
                message += f"  • {msg[:50]}...\n" if len(msg) > 50 else f"  • {msg}\n"
            message += "\n"

        # Reporter stats
        message += f"<b>Reporter Stats:</b>\n"
        message += f"  Reports sent: {self.state.get('report_count', 0)}\n"
        message += f"  Total events: {self.state.get('total_events_reported', 0)}\n"

        self.telegram.send(message, topic_id=self.topic_id)

    def _cmd_tasks(self):
        """Send task list"""
        current_tasks = self.analyzer.get_current_tasks()

        message = f"📋 <b>Current Tasks</b>\n\n"

        pending = [t for t in current_tasks if t.get('status') == 'pending']
        in_progress = [t for t in current_tasks if t.get('status') == 'in_progress']

        if in_progress:
            message += f"<b>In Progress ({len(in_progress)}):</b>\n"
            for task in in_progress[:5]:
                message += f"  • {task['task_id']}\n"
            if len(in_progress) > 5:
                message += f"  ... and {len(in_progress) - 5} more\n"
            message += "\n"

        if pending:
            message += f"<b>Pending ({len(pending)}):</b>\n"
            for task in pending[:5]:
                message += f"  • {task['task_id']}\n"
            if len(pending) > 5:
                message += f"  ... and {len(pending) - 5} more\n"

        if not pending and not in_progress:
            message += "<i>No active tasks</i>"

        self.telegram.send(message, topic_id=self.topic_id)

    def _cmd_agents(self):
        """Send agent details"""
        report = self.generate_report(hours=24)

        message = f"🤖 <b>Agent Details (24h)</b>\n\n"

        agents = report.get('agents_active', [])
        if agents:
            for agent in agents:
                # Count events for this agent
                count = len([e for e in report.get('tasks_started', []) if e.get('agent') == agent])
                message += f"<b>{agent}</b>: {count} events\n"
        else:
            message += "<i>No agent activity recorded</i>"

        self.telegram.send(message, topic_id=self.topic_id)

    def run(self):
        """Main reporter loop"""
        logger.info("BB5 Reporter starting...")
        self.telegram.send(
            "📊 <b>BB5 Reporter</b> is now online!\n\n"
            "I'll send periodic updates about agent activity.\n"
            "Commands: status, tasks, agents, report, daily",
            topic_id=self.topic_id
        )

        # Schedule reports
        # Hourly updates during business hours (9 AM - 9 PM)
        schedule.every().hour.at(":00").do(
            lambda: self.send_periodic_update(hours=1, topic_id=self.topic_id)
            if 9 <= datetime.now().hour <= 21 else None
        )

        # Daily summary at 9 AM
        schedule.every().day.at("09:00").do(self.send_daily_summary, topic_id=self.topic_id)

        # Process Telegram commands every 30 seconds
        schedule.every(30).seconds.do(self.process_telegram_commands)

        # Main loop
        while True:
            try:
                if self.running:
                    schedule.run_pending()

                time.sleep(10)

            except KeyboardInterrupt:
                logger.info("Shutting down...")
                self.telegram.send("📊 BB5 Reporter shutting down", topic_id=self.topic_id)
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(10)


if __name__ == "__main__":
    reporter = BB5Reporter()
    reporter.run()
