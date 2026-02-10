"""
Scribe Integration - Logging to BlackBox5 Scribe
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class ScribeIntegration:
    """Integration with BlackBox5 Scribe for task logging"""

    def __init__(self, config: Dict[str, Any]):
        self.enabled = config.get('enabled', True)
        self.skill = config.get('skill', 'blackbox5-scribe')
        self.task_docs_path = Path(config.get('task_docs_path', '/opt/blackbox5/5-project-memory/blackbox5/tasks'))
        self.knowledge_base_path = Path(config.get('knowledge_base_path', '/opt/blackbox5/5-project-memory/blackbox5/knowledge/scribe-knowledge.md'))
        self.log_all_events = config.get('log_all_events', True)

        # Ensure directories exist
        self.task_docs_path.mkdir(parents=True, exist_ok=True)
        self.knowledge_base_path.parent.mkdir(parents=True, exist_ok=True)

    async def log_event(self, task_id: str, event_type: str,
                        message: str, metadata: Optional[Dict[str, Any]] = None):
        """Log a task event to Scribe"""
        if not self.enabled:
            return

        try:
            # Create task document if it doesn't exist
            task_doc_path = self.task_docs_path / f"{task_id}.md"

            if not task_doc_path.exists():
                await self._create_task_document(task_id, metadata or {})

            # Append event to task document
            timestamp = datetime.now().isoformat()
            event_entry = f"\n## {timestamp} - {event_type.upper()}\n\n{message}\n"

            if metadata:
                event_entry += f"\n**Metadata:**\n```json\n{json.dumps(metadata, indent=2)}\n```\n"

            with open(task_doc_path, 'a') as f:
                f.write(event_entry)

            logger.debug(f"Logged to scribe: {task_id} - {event_type}")

        except Exception as e:
            logger.error(f"Failed to log to scribe: {e}")

    async def log_status(self, agent_id: str, status: Dict[str, Any]):
        """Log executor/worker status"""
        if not self.enabled or not self.log_all_events:
            return

        try:
            status_doc_path = self.task_docs_path.parent / "executors" / f"{agent_id}.md"
            status_doc_path.parent.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().isoformat()
            status_entry = f"\n## {timestamp} - STATUS\n\n```\n{json.dumps(status, indent=2)}\n```\n"

            # Keep last 50 status entries
            if status_doc_path.exists():
                content = status_doc_path.read_text()
                lines = content.split('\n')
                if len(lines) > 500:  # Approximate limit
                    # Keep first 50 lines (header) + recent entries
                    content = '\n'.join(lines[:50] + lines[-450:])
                    status_doc_path.write_text(content)

            with open(status_doc_path, 'a') as f:
                f.write(status_entry)

        except Exception as e:
            logger.error(f"Failed to log status: {e}")

    async def _create_task_document(self, task_id: str, metadata: Dict[str, Any]):
        """Create initial task document"""
        task_doc_path = self.task_docs_path / f"{task_id}.md"

        content = f"""# Task: {task_id}

**Created:** {datetime.now().isoformat()}
**Type:** {metadata.get('task_type', 'unknown')}
**Priority:** {metadata.get('priority', 'medium')}
**Status:** pending

---

## Task Description

{metadata.get('description', 'No description provided')}

---

## Execution Log

"""
        if metadata.get('command'):
            content += f"\n**Command:** `{metadata['command']}`\n"
        if metadata.get('script_path'):
            content += f"\n**Script:** `{metadata['script_path']}`\n"

        task_doc_path.write_text(content)

    async def log_decision(self, title: str, context: str, decision: str, rationale: str):
        """Log a decision to the knowledge base"""
        if not self.enabled:
            return

        try:
            timestamp = datetime.now().isoformat()
            decision_entry = f"""

## [{timestamp}] - {title}

**Context:** {context}

**Decision:** {decision}

**Rationale:** {rationale}

---

"""

            with open(self.knowledge_base_path, 'a') as f:
                f.write(decision_entry)

            logger.debug(f"Logged decision to scribe: {title}")

        except Exception as e:
            logger.error(f"Failed to log decision: {e}")

    async def log_learning(self, topic: str, what_worked: list[str],
                          what_was_hard: list[str], patterns: list[str]):
        """Log learnings to the knowledge base"""
        if not self.enabled:
            return

        try:
            timestamp = datetime.now().isoformat()
            learning_entry = f"""

## [{timestamp}] - Learning: {topic}

**What Worked Well:**
{chr(10).join(f'- {item}' for item in what_worked)}

**What Was Harder Than Expected:**
{chr(10).join(f'- {item}' for item in what_was_hard)}

**Patterns Detected:**
{chr(10).join(f'- {item}' for item in patterns)}

---

"""

            with open(self.knowledge_base_path, 'a') as f:
                f.write(learning_entry)

            logger.debug(f"Logged learning to scribe: {topic}")

        except Exception as e:
            logger.error(f"Failed to log learning: {e}")

    async def generate_daily_summary(self, date: Optional[str] = None) -> str:
        """Generate a daily summary of task activity"""
        if not self.enabled:
            return ""

        date = date or datetime.now().strftime('%Y-%m-%d')
        summary_path = self.task_docs_path.parent / f"daily-summary-{date}.md"

        # This would read all task documents and compile a summary
        # For now, return a placeholder
        return f"# Daily Summary - {date}\n\nSummary generation not yet implemented.\n"
