#!/usr/bin/env python3
"""State management for BB5 CI system."""
import os
import yaml
from datetime import datetime
from pathlib import Path

# BB5 paths
BB5_ROOT = "/Users/shaansisodia/.blackbox5"
PROJECT_ROOT = f"{BB5_ROOT}/5-project-memory/blackbox5"
CI_ROOT = f"{PROJECT_ROOT}/.autonomous/ci"

ISSUES_DIR = f"{CI_ROOT}/issues"
PLANS_DIR = f"{CI_ROOT}/plans"
EXECUTIONS_DIR = f"{CI_ROOT}/executions"


class StateManager:
    """Manages CI state (issues, plans, executions)."""

    def __init__(self):
        self.issues_dir = ISSUES_DIR
        self.plans_dir = PLANS_DIR
        self.executions_dir = EXECUTIONS_DIR

        for d in [self.issues_dir, self.plans_dir, self.executions_dir]:
            os.makedirs(d, exist_ok=True)

    def _next_id(self, prefix, existing):
        """Generate next sequential ID."""
        nums = []
        for f in os.listdir(existing) if os.path.exists(existing) else []:
            if f.startswith(prefix) and f.endswith('.yaml'):
                try:
                    nums.append(int(f.replace(prefix, '').replace('.yaml', '')))
                except ValueError:
                    pass
        next_num = max(nums) + 1 if nums else 1
        return f"{prefix}{next_num:03d}"

    def create_issue(self, title, description, source, severity="medium"):
        """Create a new issue."""
        issue_id = self._next_id("ISS-", self.issues_dir)
        issue = {
            "issue_id": issue_id,
            "title": title,
            "description": description,
            "source": source,
            "severity": severity,
            "status": "detected",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "validation": None,
            "plan_id": None,
            "execution_id": None
        }
        self._write_yaml(f"{self.issues_dir}/{issue_id}.yaml", issue)
        return issue_id

    def get_issue(self, issue_id):
        """Get issue by ID."""
        path = f"{self.issues_dir}/{issue_id}.yaml"
        return self._read_yaml(path) if os.path.exists(path) else None

    def update_issue(self, issue_id, updates):
        """Update issue fields."""
        issue = self.get_issue(issue_id)
        if not issue:
            return False
        issue.update(updates)
        issue["updated_at"] = datetime.now().isoformat()
        self._write_yaml(f"{self.issues_dir}/{issue_id}.yaml", issue)
        return True

    def list_issues(self, status=None):
        """List all issues, optionally filtered by status."""
        issues = []
        if not os.path.exists(self.issues_dir):
            return issues
        for f in os.listdir(self.issues_dir):
            if f.endswith('.yaml'):
                issue = self._read_yaml(f"{self.issues_dir}/{f}")
                if issue and (status is None or issue.get('status') == status):
                    issues.append(issue)
        return sorted(issues, key=lambda x: x.get('created_at', ''), reverse=True)

    def create_plan(self, issue_id, title, steps, acceptance_criteria, **kwargs):
        """Create a new plan for an issue."""
        plan_id = self._next_id("PLAN-", self.plans_dir)
        plan = {
            "plan_id": plan_id,
            "issue_id": issue_id,
            "title": title,
            "steps": steps,
            "acceptance_criteria": acceptance_criteria,
            "status": "created",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            **kwargs
        }
        self._write_yaml(f"{self.plans_dir}/{plan_id}.yaml", plan)
        self.update_issue(issue_id, {"plan_id": plan_id, "status": "planned"})
        return plan_id

    def get_plan(self, plan_id):
        """Get plan by ID."""
        path = f"{self.plans_dir}/{plan_id}.yaml"
        return self._read_yaml(path) if os.path.exists(path) else None

    def update_plan(self, plan_id, updates):
        """Update plan fields."""
        plan = self.get_plan(plan_id)
        if not plan:
            return False
        plan.update(updates)
        plan["updated_at"] = datetime.now().isoformat()
        self._write_yaml(f"{self.plans_dir}/{plan_id}.yaml", plan)
        return True

    def create_execution(self, plan_id, steps):
        """Create a new execution record."""
        exec_id = self._next_id("EXEC-", self.executions_dir)
        execution = {
            "execution_id": exec_id,
            "plan_id": plan_id,
            "status": "pending",
            "steps": [{"step": i+1, "status": "pending", "result": None}
                      for i in range(len(steps))],
            "started_at": None,
            "completed_at": None,
            "created_at": datetime.now().isoformat()
        }
        self._write_yaml(f"{self.executions_dir}/{exec_id}.yaml", execution)

        # Update plan and issue
        plan = self.get_plan(plan_id)
        if plan:
            self.update_plan(plan_id, {"execution_id": exec_id})
            self.update_issue(plan.get('issue_id'), {"execution_id": exec_id})

        return exec_id

    def get_execution(self, exec_id):
        """Get execution by ID."""
        path = f"{self.executions_dir}/{exec_id}.yaml"
        return self._read_yaml(path) if os.path.exists(path) else None

    def update_execution(self, exec_id, updates):
        """Update execution fields."""
        execution = self.get_execution(exec_id)
        if not execution:
            return False
        execution.update(updates)
        self._write_yaml(f"{self.executions_dir}/{exec_id}.yaml", execution)
        return True

    def _read_yaml(self, path):
        """Read YAML file."""
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        except Exception:
            return None

    def _write_yaml(self, path, data):
        """Write YAML file."""
        with open(path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)


# Singleton for easy import
state_manager = StateManager()
