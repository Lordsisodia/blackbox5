#!/usr/bin/env python3
"""
Improvement Plan Generator - Generates structured improvement plans for prioritized tasks
Reads prioritized tasks and creates actionable improvement plans in YAML + Markdown format
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any

# Configuration
BB5_HOME = "/opt/blackbox5"
AUTONOMOUS_DIR = f"{BB5_HOME}/.autonomous"
INPUT_FILE = f"{AUTONOMOUS_DIR}/prioritized-tasks.json"
OUTPUT_FILE = f"{AUTONOMOUS_DIR}/improvement-plan.yaml"

def log(message):
    """Log message to stdout"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[{timestamp}] {message}")

def load_prioritized_tasks():
    """Load prioritized tasks from task analyzer"""
    if not os.path.exists(INPUT_FILE):
        log(f"⚠️  No prioritized tasks found: {INPUT_FILE}")
        return []

    with open(INPUT_FILE, "r") as f:
        data = json.load(f)

    return data.get("tasks", [])

def generate_acceptance_criteria(task: Dict[str, Any]) -> List[str]:
    """Generate acceptance criteria for a task"""
    criteria = []

    # Based on task type
    task_type = task.get("type", "code")

    if task_type == "code":
        criteria.extend([
            "Code changes are implemented correctly",
            "All existing tests still pass",
            "New tests added for new functionality",
            "Code follows BlackBox5 coding standards"
        ])
    elif task_type == "test":
        criteria.extend([
            "Tests cover the intended scenarios",
            "Tests are reliable and not flaky",
            "Test coverage increases",
            "Documentation explains what's being tested"
        ])
    elif task_type == "docs":
        criteria.extend([
            "Documentation is clear and accurate",
            "Examples are provided where applicable",
            "Spelling and grammar checked",
            "Documentation follows BlackBox5 style guide"
        ])
    elif task_type == "architecture":
        criteria.extend([
            "Architecture proposal is documented",
            "Implications are clearly explained",
            "Migration path is defined (if applicable)",
            "Team has reviewed and approved"
        ])
    else:
        criteria.extend([
            "Task requirements are met",
            "Changes are tested and validated",
            "Documentation is updated",
            "No regressions introduced"
        ])

    # Based on task-specific issues
    issues = task.get("current_issues", [])
    if "Task has been pending for >72 hours" in issues:
        criteria.append("Task is resolved or properly deferred")

    if "Missing or unclear description" in issues:
        criteria.append("Task description is clarified")

    return criteria

def generate_improvement_plan(task: Dict[str, Any]) -> str:
    """Generate improvement plan for a single task"""
    name = task.get("name", "Unknown")
    priority = task.get("priority", "medium")
    description = task.get("description", "No description provided")

    # Current issues
    current_issues = task.get("current_issues", [])
    if not current_issues:
        current_issues = ["No specific issues identified"]

    # Improvement opportunities
    improvement_opportunities = task.get("improvement_opportunities", [])
    if not improvement_opportunities:
        improvement_opportunities = ["General improvement possible"]

    # Complexity and time
    complexity = task.get("complexity", "medium")
    estimated_time = task.get("estimated_time", "2h")

    # Dependencies (simplified)
    dependencies = []
    if task.get("blocking", False):
        dependencies.append("Unblocks other tasks")

    # Acceptance criteria
    acceptance_criteria = generate_acceptance_criteria(task)

    # Generate YAML front matter
    yaml_content = f"""---
Task: {name}
Priority: {priority}
Type: {task.get("type", "code")}
Target: {description[:100] if len(description) > 100 else description}
Current Issues:
"""
    for issue in current_issues:
        yaml_content += f"  - {issue}\n"

    yaml_content += "Improvement Opportunities:\n"
    for opp in improvement_opportunities:
        yaml_content += f"  - {opp}\n"

    yaml_content += f"""Complexity: {complexity}
Estimated Time: {estimated_time}
Dependencies: {dependencies}
Acceptance Criteria:
"""
    for criteria in acceptance_criteria:
        yaml_content += f"  - {criteria}\n"

    yaml_content += "---\n\n"

    # Add detailed analysis
    yaml_content += f"""# Improvement Plan: {name}

## Overview
**Priority:** {priority.upper()}
**Complexity:** {complexity.capitalize()}
**Estimated Time:** {estimated_time}

## Current State

### Description
{description if description else "No description available"}

### Issues Identified
"""
    for issue in current_issues:
        yaml_content += f"- {issue}\n"

    yaml_content += "\n### Improvement Opportunities\n"
    for opp in improvement_opportunities:
        yaml_content += f"- {opp}\n"

    yaml_content += f"""
## Implementation Plan

### Recommended Agent
- **Agent Type:** {task.get("type", "engineering")}
- **Agent Selection:** Based on task type and complexity

### Steps to Complete
1. **Analyze** - Review current implementation and requirements
2. **Plan** - Create detailed implementation plan
3. **Implement** - Execute changes following BlackBox5 standards
4. **Test** - Write and run tests to validate changes
5. **Document** - Update documentation as needed
6. **Verify** - Ensure no regressions and acceptance criteria met

### Acceptance Criteria
"""
    for i, criteria in enumerate(acceptance_criteria, 1):
        yaml_content += f"{i}. {criteria}\n"

    if dependencies:
        yaml_content += "\n### Dependencies\n"
        for dep in dependencies:
            yaml_content += f"- {dep}\n"

    # Additional notes based on task metadata
    age_hours = task.get("age_hours", 0)
    if age_hours > 72:
        yaml_content += f"""
### ⚠️  Stale Task Notice
This task has been pending for {age_hours:.1f} hours. Consider:
- Is this task still relevant?
- Should it be reprioritized or closed?
- Are there blockers preventing progress?
"""

    return yaml_content

def generate_full_improvement_plan(tasks: List[Dict[str, Any]]) -> str:
    """Generate complete improvement plan for all tasks"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    header = f"""# BlackBox5 Autonomous Improvement Plan
**Generated:** {timestamp}
**Total Tasks:** {len(tasks)}

---

## Executive Summary

This improvement plan outlines the prioritized tasks for the current autonomous improvement cycle. Tasks are sorted by priority score, considering:

- Priority level (high/medium/low)
- Task age (older tasks prioritized)
- Complexity (with bonus for quick wins)
- Blocking status

---

"""

    # Generate individual task plans
    task_plans = []
    for i, task in enumerate(tasks, 1):
        task_plans.append(f"\n## Task {i}: {task['name']}\n")
        task_plans.append(generate_improvement_plan(task))
        task_plans.append("\n---\n")

    # Combine all sections
    full_plan = header + "".join(task_plans)

    # Add footer
    footer = """
## Next Steps

1. **Agent Assignment** - Assign tasks to appropriate specialized agents
2. **Execution** - Agents work on assigned tasks in priority order
3. **Verification** - Testing and verification agents validate changes
4. **Documentation** - Scribe agent documents all changes
5. **Reporting** - Comprehensive report generated for the cycle

## Metrics Tracking

This cycle will track:
- Tasks completed
- Bugs fixed
- Performance improvements
- Code quality metrics
- Documentation updates
- Team efficiency

---

*Plan automatically generated by autonomous improvement system*
"""

    full_plan += footer

    return full_plan

def main():
    """Main entry point"""
    log("🚀 Starting improvement plan generation...")

    # Load prioritized tasks
    tasks = load_prioritized_tasks()

    if not tasks:
        log("⚠️  No tasks to generate improvement plan for")
        # Create empty plan
        with open(OUTPUT_FILE, "w") as f:
            f.write(f"""# BlackBox5 Autonomous Improvement Plan
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}
**Total Tasks:** 0

No tasks found in current cycle. Next cycle will analyze new tasks.
""")
        log(f"💾 Empty plan saved to: {OUTPUT_FILE}")
        return []

    # Limit to top 10 tasks for the plan (to avoid overwhelming)
    top_tasks = tasks[:10]

    log(f"📝 Generating improvement plan for {len(top_tasks)} task(s)")

    # Generate full plan
    full_plan = generate_full_improvement_plan(top_tasks)

    # Save to output file
    os.makedirs(AUTONOMOUS_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        f.write(full_plan)

    log(f"💾 Improvement plan saved to: {OUTPUT_FILE}")

    # Print summary
    log(f"\n📋 Plan Summary:")
    log(f"   Tasks in plan: {len(top_tasks)}")
    high_priority = [t for t in top_tasks if t["priority"] == "high"]
    log(f"   High priority: {len(high_priority)}")

    return top_tasks

if __name__ == "__main__":
    try:
        tasks = main()
        print(json.dumps({"status": "success", "plan_count": len(tasks)}, indent=2))
    except Exception as e:
        log(f"❌ Improvement plan generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
