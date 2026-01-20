"""
Project Memory Integration for Thought Loop Framework
===================================================

Integrates the Thought Loop with Blackbox5 project memory system.

Usage:
    from project_memory import ProjectMemoryIntegration

    memory = ProjectMemoryIntegration(project_id="siso-internal")
    await memory.save_session(result)
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import asyncio

try:
    from .models import ThoughtLoopResult, Iteration, AssumptionValidation
except ImportError:
    from models import ThoughtLoopResult, Iteration, AssumptionValidation


class ProjectMemoryIntegration:
    """
    Integrates Thought Loop with Blackbox5 project memory.

    Automatically saves sessions, extracts insights, and updates patterns.
    """

    def __init__(
        self,
        project_id: str = "siso-internal",
        project_memory_path: Optional[Path] = None,
        auto_save: bool = True
    ):
        """
        Initialize project memory integration.

        Args:
            project_id: Project identifier (e.g., "siso-internal")
            project_memory_path: Path to project memory (default: blackbox5/5-project-memory/)
            auto_save: Whether to automatically save after each session
        """
        self.project_id = project_id
        self.auto_save = auto_save

        # Determine project memory path
        if project_memory_path is None:
            # Default: blackbox5/5-project-memory/
            current_dir = Path(__file__).parent
            # Navigate from loops/ -> knowledge/ -> engine/ -> 2-engine/ -> blackbox5/
            project_memory_path = current_dir.parent.parent.parent / "5-project-memory"

        self.project_memory_path = project_memory_path
        self.session_path = self.project_memory_path / project_id / "operations" / "agents" / "history" / "sessions" / "thought-loop"
        self.active_path = self.project_memory_path / project_id / "operations" / "agents" / "active" / "thought-loop"
        self.research_path = self.project_memory_path / project_id / "knowledge" / "research" / "thought-loop-framework"

        # Ensure directories exist
        self.session_path.mkdir(parents=True, exist_ok=True)
        self.active_path.mkdir(parents=True, exist_ok=True)
        self.research_path.mkdir(parents=True, exist_ok=True)
        (self.research_path / "sessions").mkdir(exist_ok=True)

        # File paths
        self.sessions_file = self.session_path / "sessions.json"
        self.insights_file = self.session_path / "insights.json"
        self.patterns_file = self.session_path / "patterns.json"
        self.metrics_file = self.session_path / "metrics.json"

        # Initialize files if they don't exist
        self._initialize_files()

    def _initialize_files(self):
        """Initialize memory files with default structure if they don't exist."""
        default_files = {
            "sessions.json": {
                "sessions": [],
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat(),
                    "total_sessions": 0,
                    "total_converged": 0,
                    "avg_iterations": 0,
                    "avg_confidence": 0.0
                }
            },
            "insights.json": {
                "assumptions_validated": [],
                "fallacies_detected": [],
                "decision_patterns": [],
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat(),
                    "total_insights": 0
                }
            },
            "patterns.json": {
                "decision_patterns": [],
                "convergence_patterns": [],
                "assumption_patterns": [],
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat(),
                    "total_patterns": 0
                }
            },
            "metrics.json": {
                "performance": {
                    "avg_duration_seconds": 0,
                    "avg_iterations_per_session": 0,
                    "total_duration_seconds": 0
                },
                "quality": {
                    "convergence_rate": 0,
                    "avg_confidence": 0,
                    "high_confidence_rate": 0
                },
                "usage": {
                    "total_sessions": 0,
                    "sessions_this_week": 0,
                    "sessions_this_month": 0,
                    "most_common_problems": []
                },
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat()
                }
            }
        }

        for filename, default_content in default_files.items():
            file_path = self.session_path / filename
            if not file_path.exists():
                with open(file_path, 'w') as f:
                    json.dump(default_content, f, indent=2)

    def _generate_session_id(self, problem: str) -> str:
        """Generate unique session ID from problem and timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        # Create hash of problem for uniqueness
        problem_hash = hashlib.md5(problem.encode()).hexdigest()[:6]
        return f"tl-{timestamp}-{problem_hash}"

    async def save_session(
        self,
        result: ThoughtLoopResult,
        duration_seconds: float = 0.0
    ) -> str:
        """
        Save a thought loop session to project memory.

        Args:
            result: Thought loop result
            duration_seconds: Duration of the session

        Returns:
            Session ID
        """
        # Generate session ID
        problem = result.metadata.get("problem", "unknown")
        session_id = self._generate_session_id(problem)

        # Create session record
        session_record = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "problem": problem,
            "context": "",  # Could be passed separately
            "iterations": self._serialize_iterations(result.iterations),
            "converged": result.converged,
            "final_iteration": result.final_iteration,
            "confidence": result.confidence,
            "answer": result.answer,
            "reasoning_trace": result.reasoning_trace,
            "duration_seconds": duration_seconds,
            "metadata": result.metadata
        }

        # Load existing sessions
        with open(self.sessions_file, 'r') as f:
            data = json.load(f)

        # Add new session
        data["sessions"].append(session_record)

        # Update metadata
        data["metadata"]["last_updated"] = datetime.now().isoformat()
        data["metadata"]["total_sessions"] = len(data["sessions"])
        data["metadata"]["total_converged"] = sum(1 for s in data["sessions"] if s.get("converged", False))

        # Calculate averages
        if data["sessions"]:
            data["metadata"]["avg_iterations"] = sum(
                s.get("final_iteration", 0) for s in data["sessions"]
            ) / len(data["sessions"])
            data["metadata"]["avg_confidence"] = sum(
                s.get("confidence", 0) for s in data["sessions"]
            ) / len(data["sessions"])

        # Save sessions (atomic write)
        temp_file = self.sessions_file.with_suffix('.tmp')
        with open(temp_file, 'w') as f:
            json.dump(data, f, indent=2)
        temp_file.replace(self.sessions_file)

        # Extract and save insights
        await self._extract_insights(session_record)

        # Update patterns
        await self._update_patterns(session_record)

        # Update metrics
        await self._update_metrics(session_record)

        # Archive to research folder
        await self._archive_session(session_record)

        return session_id

    def _serialize_iterations(self, iterations: List[Iteration]) -> List[Dict]:
        """Serialize iterations to dict format."""
        serialized = []
        for iteration in iterations:
            # Serialize assumptions identified
            assumptions_identified = []
            for a in iteration.assumptions_identified:
                if hasattr(a, 'statement'):
                    assumptions_identified.append(a.statement)
                elif isinstance(a, str):
                    assumptions_identified.append(a)
                else:
                    assumptions_identified.append(str(a))

            # Serialize assumptions validated
            assumptions_validated = []
            for v in iteration.assumptions_validated:
                validated = {
                    "assumption": v.assumption.statement if hasattr(v.assumption, 'statement') else str(v.assumption),
                    "validity": v.validity.value if hasattr(v.validity, 'value') else str(v.validity),
                    "confidence": v.confidence,
                    "reasoning": v.reasoning,
                    "supporting_evidence": len(v.supporting_evidence),
                    "contradicting_evidence": len(v.contradicting_evidence)
                }
                assumptions_validated.append(validated)

            # Serialize first principles check
            first_principles_check = None
            if iteration.first_principles_check:
                first_principles_check = {
                    "necessary": iteration.first_principles_check.necessary,
                    "confidence": iteration.first_principles_check.confidence,
                    "reasoning": iteration.first_principles_check.reasoning,
                    "alternatives": iteration.first_principles_check.alternatives or []
                }

            serialized.append({
                "iteration_number": iteration.iteration_number,
                "understanding": iteration.understanding,
                "confidence": iteration.confidence,
                "assumptions_identified": assumptions_identified,
                "assumptions_validated": assumptions_validated,
                "first_principles_check": first_principles_check
            })
        return serialized

    async def _extract_insights(self, session: Dict[str, Any]):
        """Extract insights from session and save to insights.json."""
        with open(self.insights_file, 'r') as f:
            insights = json.load(f)

        timestamp = session["timestamp"]
        session_id = session["session_id"]

        # Extract validated assumptions
        for iteration in session.get("iterations", []):
            for validation in iteration.get("assumptions_validated", []):
                insights["assumptions_validated"].append({
                    "assumption": validation["assumption"],
                    "validity": validation["validity"],
                    "confidence": validation["confidence"],
                    "source_session": session_id,
                    "timestamp": timestamp,
                    "evidence_summary": {
                        "supporting": validation["supporting_evidence"],
                        "contradicting": validation["contradicting_evidence"]
                    }
                })

        # Extract decision patterns from answer
        answer = session.get("answer", "")
        if "NO -" in answer:
            insights["decision_patterns"].append({
                "pattern": self._extract_pattern_key(session["problem"]),
                "typical_answer": "NO",
                "reasoning": answer,
                "source_session": session_id,
                "timestamp": timestamp,
                "frequency": 1
            })

        # Update metadata
        insights["metadata"]["last_updated"] = datetime.now().isoformat()
        insights["metadata"]["total_insights"] = (
            len(insights["assumptions_validated"]) +
            len(insights["fallacies_detected"]) +
            len(insights["decision_patterns"])
        )

        # Save insights (atomic write)
        temp_file = self.insights_file.with_suffix('.tmp')
        with open(temp_file, 'w') as f:
            json.dump(insights, f, indent=2)
        temp_file.replace(self.insights_file)

    async def _update_patterns(self, session: Dict[str, Any]):
        """Update patterns from session."""
        with open(self.patterns_file, 'r') as f:
            patterns = json.load(f)

        # Update convergence patterns
        if session.get("converged"):
            pattern_key = self._extract_pattern_key(session["problem"])
            existing = next(
                (p for p in patterns["convergence_patterns"] if p["pattern"] == pattern_key),
                None
            )

            if existing:
                existing["frequency"] += 1
                existing["last_seen"] = session["timestamp"]
            else:
                patterns["convergence_patterns"].append({
                    "pattern": pattern_key,
                    "frequency": 1,
                    "first_seen": session["timestamp"],
                    "last_seen": session["timestamp"],
                    "avg_confidence": session["confidence"]
                })

        # Update metadata
        patterns["metadata"]["last_updated"] = datetime.now().isoformat()
        patterns["metadata"]["total_patterns"] = (
            len(patterns["decision_patterns"]) +
            len(patterns["convergence_patterns"]) +
            len(patterns["assumption_patterns"])
        )

        # Save patterns (atomic write)
        temp_file = self.patterns_file.with_suffix('.tmp')
        with open(temp_file, 'w') as f:
            json.dump(patterns, f, indent=2)
        temp_file.replace(self.patterns_file)

    async def _update_metrics(self, session: Dict[str, Any]):
        """Update metrics from session."""
        with open(self.metrics_file, 'r') as f:
            metrics = json.load(f)

        # Update performance metrics
        total_sessions = metrics["usage"]["total_sessions"] + 1
        duration = session.get("duration_seconds", 0)
        iterations = session.get("final_iteration", 0)

        metrics["performance"]["total_duration_seconds"] += duration
        metrics["performance"]["avg_duration_seconds"] = (
            metrics["performance"]["total_duration_seconds"] / total_sessions
        )
        metrics["performance"]["avg_iterations_per_session"] = (
            (metrics["performance"]["avg_iterations_per_session"] * (total_sessions - 1) + iterations) / total_sessions
        )

        # Update quality metrics
        if session.get("converged"):
            metrics["quality"]["convergence_rate"] = (
                (metrics["quality"]["convergence_rate"] * (total_sessions - 1) + 1.0) / total_sessions
            )

        metrics["quality"]["avg_confidence"] = (
            (metrics["quality"]["avg_confidence"] * (total_sessions - 1) + session["confidence"]) / total_sessions
        )

        if session["confidence"] >= 0.9:
            metrics["quality"]["high_confidence_rate"] = (
                (metrics["quality"]["high_confidence_rate"] * (total_sessions - 1) + 1.0) / total_sessions
            )

        # Update usage metrics
        metrics["usage"]["total_sessions"] = total_sessions

        # Update problem frequency
        pattern_key = self._extract_pattern_key(session["problem"])
        problem_found = False
        for problem in metrics["usage"]["most_common_problems"]:
            if problem["problem"] == pattern_key:
                problem["count"] += 1
                problem_found = True
                break

        if not problem_found:
            metrics["usage"]["most_common_problems"].append({
                "problem": pattern_key,
                "count": 1
            })

        # Sort by frequency
        metrics["usage"]["most_common_problems"].sort(key=lambda x: x["count"], reverse=True)
        metrics["usage"]["most_common_problems"] = metrics["usage"]["most_common_problems"][:10]

        # Update metadata
        metrics["metadata"]["last_updated"] = datetime.now().isoformat()

        # Save metrics (atomic write)
        temp_file = self.metrics_file.with_suffix('.tmp')
        with open(temp_file, 'w') as f:
            json.dump(metrics, f, indent=2)
        temp_file.replace(self.metrics_file)

    async def _archive_session(self, session: Dict[str, Any]):
        """Archive session to research folder."""
        # Create date-based archive structure
        date = datetime.fromisoformat(session["timestamp"])
        archive_path = self.research_path / "sessions" / str(date.year) / f"{date.month:02d}"
        archive_path.mkdir(parents=True, exist_ok=True)

        # Save session
        session_file = archive_path / f"{session['session_id']}.json"
        with open(session_file, 'w') as f:
            json.dump(session, f, indent=2)

    def _extract_pattern_key(self, problem: str) -> str:
        """Extract pattern key from problem statement."""
        # Simple extraction: lowercase and remove common words
        words = problem.lower().split()
        stop_words = {"should", "we", "the", "a", "an", "is", "are", "to", "for", "in", "on", "at"}
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        return " ".join(keywords[:5]) if keywords else problem.lower()[:50]

    async def get_recent_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent thought loop sessions."""
        with open(self.sessions_file, 'r') as f:
            data = json.load(f)

        # Sort by timestamp (newest first) and limit
        sessions = sorted(
            data["sessions"],
            key=lambda x: x.get("timestamp", ""),
            reverse=True
        )[:limit]

        return sessions

    async def get_patterns(self) -> Dict[str, Any]:
        """Get learned patterns."""
        with open(self.patterns_file, 'r') as f:
            return json.load(f)

    async def get_insights(self) -> Dict[str, Any]:
        """Get extracted insights."""
        with open(self.insights_file, 'r') as f:
            return json.load(f)

    async def get_metrics(self) -> Dict[str, Any]:
        """Get performance and quality metrics."""
        with open(self.metrics_file, 'r') as f:
            return json.load(f)

    def cleanup_old_sessions(self, days: int = 30):
        """Archive sessions older than specified days."""
        cutoff = datetime.now() - timedelta(days=days)

        with open(self.sessions_file, 'r') as f:
            data = json.load(f)

        # Find old sessions
        active_sessions = []
        for session in data["sessions"]:
            session_time = datetime.fromisoformat(session["timestamp"])
            if session_time < cutoff:
                # Already archived, but keep in main file for reference
                active_sessions.append(session)

        # Keep only recent sessions in main file
        data["sessions"] = active_sessions

        with open(self.sessions_file, 'w') as f:
            json.dump(data, f, indent=2)
        # Note: Cleanup not using atomic write since it's a maintenance operation
