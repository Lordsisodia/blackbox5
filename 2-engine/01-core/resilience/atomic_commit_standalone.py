#!/usr/bin/env python3
"""
Standalone Atomic Commit Manager for BLACKBOX5

Simplified atomic commit manager without external git dependencies.
"""

import logging
import subprocess
from typing import List, Optional, Dict, Any
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class AtomicCommitManager:
    """
    Manages atomic commits with conventional commit format.

    Automatically creates commits after task completion with
    standardized commit messages.
    """

    def __init__(self, repo_path: str = "."):
        """Initialize commit manager."""
        self.repo_path = Path(repo_path).resolve()
        self._pending_files: List[str] = []

    def _git(self, *args: str) -> str:
        """Run git command."""
        result = subprocess.run(
            ["git"] + list(args),
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        return result.stdout.strip()

    def stage_files(self, files: List[str]) -> bool:
        """Stage files for commit."""
        try:
            self._git("add", *files)
            self._pending_files.extend(files)
            logger.info(f"Staged {len(files)} files")
            return True
        except Exception as e:
            logger.error(f"Failed to stage files: {e}")
            return False

    def create_commit(
        self,
        message: str,
        type_: str = "feat",
        scope: Optional[str] = None,
        body: Optional[str] = None
    ) -> Optional[str]:
        """
        Create a conventional commit.

        Args:
            message: Commit message
            type_: Commit type (feat, fix, docs, etc.)
            scope: Optional scope
            body: Optional commit body

        Returns:
            Commit hash if successful, None otherwise
        """
        try:
            # Format: type(scope): message
            if scope:
                header = f"{type_}({scope}): {message}"
            else:
                header = f"{type_}: {message}"

            # Build commit message
            commit_msg = header
            if body:
                commit_msg += f"\n\n{body}"

            result = self._git("commit", "-m", commit_msg)
            self._pending_files.clear()
            logger.info(f"Created commit: {header}")
            return result

        except Exception as e:
            logger.error(f"Failed to create commit: {e}")
            return None

    def get_status(self) -> Dict[str, Any]:
        """Get repository status."""
        status = self._git("status", "--short")
        branch = self._git("rev-parse", "--abbrev-ref", "HEAD")

        return {
            "branch": branch,
            "dirty": bool(status),
            "status": status,
            "pending_files": self._pending_files.copy()
        }

    def rollback(self, commits: int = 1) -> bool:
        """Rollback commits."""
        try:
            self._git("reset", "--hard", f"HEAD~{commits}")
            logger.info(f"Rolled back {commits} commit(s)")
            return True
        except Exception as e:
            logger.error(f"Failed to rollback: {e}")
            return False
