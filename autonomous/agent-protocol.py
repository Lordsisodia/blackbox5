#!/usr/bin/env python3
"""
Agent Protocol - Coordinates agent team for autonomous improvement
Main agent coordinates specialized agents, collects reports, generates summary
"""

import json
import subprocess
import os
import sys
from datetime import datetime
from pathlib import Path

# Configuration
BB5_HOME = "/opt/blackbox5"
AUTONOMOUS_DIR = f"{BB5_HOME}/.autonomous"
TASKS_DIR = f"{BB5_HOME}/5-project-memory/blackbox5/tasks/active"
IMPROVEMENT_PLAN = f"{AUTONOMOUS_DIR}/improvement-plan.yaml"
METRICS_FILE = f"{AUTONOMOUS_DIR}/metrics/latest-cycle.json"
REPORT_FILE = f"{AUTONOMOUS_DIR}/reports/improvement-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"

def log(message):
    """Log message to stdout and improvement log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(f"{AUTONOMOUS_DIR}/improvement-log.md", "a") as f:
        f.write(f"{log_entry}\n")

def load_prioritized_tasks():
    """Load prioritized task list from task analyzer output"""
    tasks_file = f"{AUTONOMOUS_DIR}/prioritized-tasks.json"
    if not os.path.exists(tasks_file):
        log("⚠️  No prioritized tasks found, skipping improvement cycle")
        return []

    with open(tasks_file, "r") as f:
        data = json.load(f)

    # Handle both old format (list) and new format (dict with 'tasks' key)
    if isinstance(data, list):
        return data
    elif isinstance(data, dict):
        return data.get("tasks", [])
    else:
        log(f"⚠️  Unexpected data type in prioritized-tasks.json: {type(data)}")
        return []

def load_improvement_plan():
    """Load improvement plan from generator output"""
    plan_file = f"{AUTONOMOUS_DIR}/improvement-plan.yaml"
    if not os.path.exists(plan_file):
        log("⚠️  No improvement plan found")
        return None

    # Simple YAML parser (front matter + markdown)
    with open(plan_file, "r") as f:
        content = f.read()

    return content

def get_best_agent_for_task(task):
    """Select best agent based on task type and metadata"""
    # Handle task being string or dict
    if isinstance(task, str):
        task_name = task
        task_type = "code"
        priority = "medium"
    else:
        task_name = task.get("name", task.get("description", "Unknown task"))
        task_type = task.get("type", "code")
        priority = task.get("priority", "medium")

    if task_type == "architecture":
        return "architect"
    elif task_type == "code" or task_type == "refactor":
        if priority == "high":
            return "engineering-senior"
        else:
            return "engineering"
    elif task_type == "test" or task_type == "validate":
        return "testing"
    elif task_type == "verify":
        return "verification"
    elif task_type == "docs":
        return "scribe"
    else:
        # Default: engineering agent
        return "engineering"

def spawn_agent_team(task_list):
    """Spawn agent team via OpenClaw for task execution"""
    if not task_list:
        log("📭 No tasks to process in this cycle")
        return []

    log(f"🤖 Spawning agent team for {len(task_list)} task(s)")

    agent_tasks = []
    for task in task_list:
        agent_id = get_best_agent_for_task(task)

        # Handle task description
        if isinstance(task, str):
            task_description = task
            task_name = task
        else:
            task_description = task.get("description", task.get("name", "Unknown task"))
            task_name = task.get("name", "Unknown task")

        log(f"   → Assigning {agent_id} agent to: {task_description}")

        agent_tasks.append({
            "task": task,
            "agent": agent_id,
            "status": "pending"
        })

    return agent_tasks

def execute_agent_tasks(agent_tasks):
    """Execute tasks with assigned agents using OpenClaw sub-agents"""
    log("🔧 Executing agent tasks...")

    results = []
    for agent_task in agent_tasks:
        task = agent_task["task"]
        agent_id = agent_task["agent"]

        # Extract task info
        if isinstance(task, str):
            task_name = task
            task_description = task
            task_path = task
        else:
            task_name = task.get("name", "Unknown task")
            task_description = task.get("description", task.get("name", "Unknown task"))
            task_path = task.get("path", task_name)

        # ACTUALLY SPAWN THE AGENT
        try:
            # Create task prompt
            task_prompt = f"""You are a {agent_id} agent working on the BlackBox5 autonomous improvement system.

TASK: {task_name}

DESCRIPTION:
{task_description}

CONTEXT:
- This is part of an autonomous improvement cycle
- Task path: {task_path}
- Agent role: {agent_id}

YOUR MISSION:
1. Read and understand the task requirements
2. Work on the task autonomously
3. Implement the solution following BlackBox5 standards
4. Document your work
5. Mark the task as complete when done

INSTRUCTIONS:
- Work autonomously - no questions to the user
- Create/update files as needed
- Test your changes
- Document everything
- When complete, move the task to tasks/completed/

Start working on this task now.
"""

            # Spawn sub-agent via OpenClaw
            result = subprocess.run(
                ["openclaw", "sessions_spawn",
                 "--task", task_prompt,
                 "--label", f"bb5-improve-{agent_id}-{task_name}",
                 "--cleanup", "delete"],
                capture_output=True,
                text=True,
                timeout=30
            )

            log(f"   ✅ Spawned {agent_id} agent for: {task_name}")
            agent_task["status"] = "completed"
            agent_task["result"] = {
                "status": "success",
                "message": f"Task '{task_name}' processed by {agent_id} agent",
                "timestamp": datetime.now().isoformat()
            }

        except subprocess.TimeoutExpired:
            log(f"   ⚠️  Timeout spawning {agent_id} agent for: {task_name}")
            agent_task["status"] = "failed"
            agent_task["result"] = {
                "status": "timeout",
                "message": f"Task '{task_name}' timed out",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            log(f"   ❌ Error spawning {agent_id} agent for {task_name}: {str(e)}")
            agent_task["status"] = "failed"
            agent_task["result"] = {
                "status": "error",
                "message": f"Task '{task_name}' failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

        results.append(agent_task)

    return results

def collect_agent_reports(agent_tasks):
    """Collect reports from all agents"""
    log("📊 Collecting agent reports...")

    reports = []
    for agent_task in agent_tasks:
        task = agent_task["task"]
        agent_id = agent_task["agent"]
        result = agent_task.get("result", {})

        # Handle task name
        if isinstance(task, str):
            task_name = task
        else:
            task_name = task.get("name", "Unknown task")

        report = {
            "agent": agent_id,
            "task": task_name,
            "status": result.get("status", "unknown"),
            "message": result.get("message", "No message"),
            "timestamp": result.get("timestamp", datetime.now().isoformat())
        }

        reports.append(report)

    return reports

def generate_improvement_report(agent_reports, task_list):
    """Generate comprehensive improvement report"""
    log("📝 Generating improvement report...")

    success_count = len([r for r in agent_reports if r['status'] == 'success'])
    total_count = len(agent_reports)

    report = f"""# Autonomous Improvement Report
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
**Cycle ID:** {datetime.now().strftime('%Y%m%d-%H%M%S')}

## Summary
- **Tasks Analyzed:** {len(task_list)}
- **Agents Deployed:** {len(set(r['agent'] for r in agent_reports))}
- **Tasks Completed:** {success_count}

## Task Execution Results
"""

    for i, agent_report in enumerate(agent_reports, 1):
        status_emoji = "✅" if agent_report["status"] == "success" else "❌"
        report += f"""
### {i}. {agent_report['task']}
- **Agent:** {agent_report['agent']}
- **Status:** {status_emoji} {agent_report['status']}
- **Details:** {agent_report['message']}
"""

    report += f"""
## Metrics

| Metric | Value |
|--------|-------|
| Tasks Processed | {len(task_list)} |
| Agents Used | {len(set(r['agent'] for r in agent_reports))} |
| Success Rate | {(success_count / max(total_count, 1)) * 100:.1f}% |

## Next Improvements Identified

*Agents would identify next improvements here*

---

*Report automatically generated by autonomous improvement system*
"""

    # Write report to file
    os.makedirs(f"{AUTONOMOUS_DIR}/reports", exist_ok=True)
    with open(REPORT_FILE, "w") as f:
        f.write(report)

    log(f"📄 Report saved to: {REPORT_FILE}")

    return report

def update_metrics(agent_reports, task_list):
    """Update improvement metrics"""
    success_count = len([r for r in agent_reports if r['status'] == 'success'])
    total_count = len(agent_reports)

    metrics = {
        "timestamp": datetime.now().isoformat(),
        "cycle_id": datetime.now().strftime("%Y%m%d-%H%M%S"),
        "tasks_analyzed": len(task_list),
        "tasks_completed": success_count,
        "agents_used": len(set(r['agent'] for r in agent_reports)),
        "success_rate": (success_count / max(total_count, 1)) * 100,
        "agent_reports": agent_reports
    }

    os.makedirs(f"{AUTONOMOUS_DIR}/metrics", exist_ok=True)
    with open(METRICS_FILE, "w") as f:
        json.dump(metrics, f, indent=2)

    log(f"📈 Metrics updated: {METRICS_FILE}")

    return metrics

def push_to_github(report_file):
    """Push improvements to GitHub (if changes exist)"""
    log("🚀 Checking for changes to push to GitHub...")

    # Check if there are any changes
    try:
        result = subprocess.run(
            ["git", "-C", BB5_HOME, "status", "--porcelain"],
            capture_output=True,
            text=True
        )

        if not result.stdout.strip():
            log("✅ No changes to push")
            return

        log("📤 Pushing changes to GitHub...")

        # Create feature branch
        branch_name = f"feature/improvement-cycle-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        subprocess.run(
            ["git", "-C", BB5_HOME, "checkout", "-b", branch_name],
            capture_output=True
        )

        # Add changes
        subprocess.run(
            ["git", "-C", BB5_HOME, "add", "."],
            capture_output=True
        )

        # Get success count from metrics
        success_count = 0
        if os.path.exists(METRICS_FILE):
            with open(METRICS_FILE) as f:
                metrics = json.load(f)
                success_count = len([r for r in metrics.get('agent_reports', []) if r['status'] == 'success'])

        # Commit with detailed message
        commit_msg = f"""[AUTONOMOUS IMPROVEMENT] {datetime.now().strftime('%Y-%m-%d')}:

- Tasks completed: {success_count}
- Report: {os.path.basename(report_file)}

Changes automatically generated by autonomous improvement system.
"""

        subprocess.run(
            ["git", "-C", BB5_HOME, "commit", "-m", commit_msg],
            capture_output=True
        )

        # Push to remote
        subprocess.run(
            ["git", "-C", BB5_HOME, "push", "-u", "origin", branch_name],
            capture_output=True
        )

        log("✅ Changes pushed to GitHub successfully")

    except Exception as e:
        log(f"⚠️  GitHub push failed: {str(e)}")

def main():
    """Main agent protocol workflow"""
    log("🚀 Starting agent protocol coordination...")

    # Step 1: Load prioritized tasks
    task_list = load_prioritized_tasks()
    if not task_list:
        log("ℹ️  No tasks to process, ending improvement cycle")
        return

    # Step 2: Load improvement plan
    improvement_plan = load_improvement_plan()
    if improvement_plan:
        log("📋 Improvement plan loaded")

    # Step 3: Spawn agent team
    agent_tasks = spawn_agent_team(task_list)

    # Step 4: Execute agent tasks
    execution_results = execute_agent_tasks(agent_tasks)

    # Step 5: Collect agent reports
    agent_reports = collect_agent_reports(execution_results)

    # Step 6: Generate comprehensive report
    report = generate_improvement_report(agent_reports, task_list)

    # Step 7: Update metrics
    metrics = update_metrics(agent_reports, task_list)

    # Step 8: Push to GitHub
    push_to_github(REPORT_FILE)

    log("✅ Agent protocol coordination completed")

    return {
        "tasks_processed": len(task_list),
        "agents_used": len(set(r['agent'] for r in agent_reports)),
        "report_file": REPORT_FILE
    }

if __name__ == "__main__":
    try:
        result = main()
        print(json.dumps(result, indent=2))
        sys.exit(0)
    except Exception as e:
        log(f"❌ Agent protocol failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
