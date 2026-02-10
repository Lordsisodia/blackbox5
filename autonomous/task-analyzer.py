#!/usr/bin/env python3
"""
Task Analyzer - Analyzes active tasks and prioritizes them for improvement
Reads tasks from /opt/blackbox5/5-project-memory/blackbox5/tasks/active/
Sorts by priority, age, and complexity
"""

import os
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

# Configuration
BB5_HOME = "/opt/blackbox5"
TASKS_DIR = f"{BB5_HOME}/5-project-memory/blackbox5/tasks/active"
AUTONOMOUS_DIR = f"{BB5_HOME}/.autonomous"
OUTPUT_FILE = f"{AUTONOMOUS_DIR}/prioritized-tasks.json"

def log(message):
    """Log message to stdout"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[{timestamp}] {message}")

def extract_task_metadata(task_path: str) -> Dict[str, Any]:
    """Extract metadata from task directory"""
    task_name = os.path.basename(task_path)

    # Default metadata
    metadata = {
        "name": task_name,
        "path": task_path,
        "priority": "medium",
        "type": "code",
        "status": "pending",
        "created_at": None,
        "complexity": "medium",
        "blocking": False,
        "description": ""
    }

    # Try to read task.md or README.md
    task_files = []
    for f in os.listdir(task_path):
        if f.lower().endswith(('.md', '.txt')):
            task_files.append(os.path.join(task_path, f))

    if task_files:
        for file_path in task_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()

                # Extract priority
                priority_match = re.search(r'priority:\s*(high|medium|low)', content, re.IGNORECASE)
                if priority_match:
                    metadata["priority"] = priority_match.group(1).lower()

                # Extract type
                type_match = re.search(r'type:\s*(\w+)', content, re.IGNORECASE)
                if type_match:
                    metadata["type"] = type_match.group(1).lower()

                # Extract status
                status_match = re.search(r'status:\s*(pending|in-progress|completed|blocked)', content, re.IGNORECASE)
                if status_match:
                    metadata["status"] = status_match.group(1).lower()

                # Extract complexity
                complexity_match = re.search(r'complexity:\s*(easy|medium|hard)', content, re.IGNORECASE)
                if complexity_match:
                    metadata["complexity"] = complexity_match.group(1).lower()

                # Check if blocking
                if 'blocking' in content.lower() or 'blocks' in content.lower():
                    metadata["blocking"] = True

                # Extract description (first paragraph after title)
                desc_match = re.search(r'^#\s+[^\n]+\n+(.+?)(?:\n\n|\n#|$)', content, re.DOTALL)
                if desc_match:
                    metadata["description"] = desc_match.group(1).strip()[:200]

                break  # Use first file found

            except Exception as e:
                log(f"⚠️  Error reading {file_path}: {str(e)}")

    # Extract created_at from directory modification time
    try:
        created_at = datetime.fromtimestamp(os.path.getctime(task_path))
        metadata["created_at"] = created_at.isoformat()
        metadata["age_hours"] = (datetime.now() - created_at).total_seconds() / 3600
    except Exception as e:
        log(f"⚠️  Error getting creation time for {task_name}: {str(e)}")
        metadata["created_at"] = datetime.now().isoformat()
        metadata["age_hours"] = 0

    return metadata

def calculate_task_score(metadata: Dict[str, Any]) -> float:
    """
    Calculate priority score for a task
    Higher score = higher priority
    """
    score = 0.0

    # Priority score (high=30, medium=20, low=10)
    priority_scores = {"high": 30, "medium": 20, "low": 10}
    score += priority_scores.get(metadata["priority"], 20)

    # Age score (older tasks get higher score)
    age_hours = metadata.get("age_hours", 0)
    if age_hours > 72:
        score += 25  # Very old tasks
    elif age_hours > 48:
        score += 20
    elif age_hours > 24:
        score += 15
    elif age_hours > 12:
        score += 10
    else:
        score += 5   # New tasks

    # Blocking tasks get bonus
    if metadata.get("blocking", False):
        score += 15

    # Complexity score (simple tasks get slight boost for quick wins)
    complexity = metadata.get("complexity", "medium")
    if complexity == "easy":
        score += 10
    elif complexity == "hard":
        score -= 5  # Hard tasks slightly deprioritized

    # Status adjustment
    status = metadata.get("status", "pending")
    if status == "in-progress":
        score += 10  # Already started, keep momentum
    elif status == "completed":
        score = -999  # Don't process completed tasks
    elif status == "blocked":
        score -= 20  # Blocked tasks should wait

    return score

def sort_tasks(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sort tasks by priority score"""
    # Calculate scores
    for task in tasks:
        task["score"] = calculate_task_score(task)

    # Filter out completed tasks
    active_tasks = [t for t in tasks if t["score"] > 0]

    # Sort by score (descending)
    sorted_tasks = sorted(active_tasks, key=lambda t: t["score"], reverse=True)

    return sorted_tasks

def analyze_tasks():
    """Main analysis workflow"""
    log("🔍 Analyzing active tasks...")

    if not os.path.exists(TASKS_DIR):
        log(f"⚠️  Tasks directory not found: {TASKS_DIR}")
        return []

    # Get all task directories
    task_dirs = []
    for item in os.listdir(TASKS_DIR):
        item_path = os.path.join(TASKS_DIR, item)
        if os.path.isdir(item_path) and not item.startswith('.'):
            task_dirs.append(item_path)

    log(f"📂 Found {len(task_dirs)} task directories")

    # Extract metadata for each task
    tasks = []
    for task_dir in task_dirs:
        try:
            metadata = extract_task_metadata(task_dir)
            tasks.append(metadata)
        except Exception as e:
            log(f"⚠️  Error analyzing task {task_dir}: {str(e)}")

    log(f"📊 Analyzed {len(tasks)} tasks")

    # Sort tasks by priority
    sorted_tasks = sort_tasks(tasks)

    log(f"✅ Prioritized {len(sorted_tasks)} active tasks")

    return sorted_tasks

def generate_improvement_opportunities(task: Dict[str, Any]) -> List[str]:
    """Generate improvement opportunities for a task"""
    opportunities = []

    priority = task.get("priority", "medium")
    complexity = task.get("complexity", "medium")
    task_type = task.get("type", "code")

    # Priority-based suggestions
    if priority == "high":
        opportunities.append("High priority - consider accelerating")
    elif priority == "low":
        opportunities.append("Low priority - evaluate if still relevant")

    # Complexity-based suggestions
    if complexity == "hard":
        opportunities.append("Complex - break down into sub-tasks")
    elif complexity == "easy":
        opportunities.append("Quick win - can complete quickly")

    # Type-based suggestions
    if task_type == "code":
        opportunities.append("Code task - ensure tests are written")
    elif task_type == "docs":
        opportunities.append("Documentation - ensure accuracy and completeness")
    elif task_type == "test":
        opportunities.append("Testing - focus on edge cases and coverage")

    # Age-based suggestions
    age_hours = task.get("age_hours", 0)
    if age_hours > 72:
        opportunities.append("Stale task - evaluate if still needed")

    # Blocking tasks
    if task.get("blocking", False):
        opportunities.append("Blocking other work - unblock soon")

    return opportunities

def analyze_current_issues(task: Dict[str, Any]) -> List[str]:
    """Analyze current issues for a task"""
    issues = []

    status = task.get("status", "pending")
    if status == "blocked":
        issues.append("Task is currently blocked")
    elif status == "in-progress":
        issues.append("Task in progress - check if stalled")

    # Check for missing description
    if not task.get("description"):
        issues.append("Missing or unclear description")

    # Check age
    age_hours = task.get("age_hours", 0)
    if age_hours > 72 and status == "pending":
        issues.append("Task has been pending for >72 hours")

    return issues

def enrich_tasks_with_analysis(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Enrich tasks with improvement opportunities and issues"""
    for task in tasks:
        task["improvement_opportunities"] = generate_improvement_opportunities(task)
        task["current_issues"] = analyze_current_issues(task)

        # Estimate completion time based on complexity
        complexity = task.get("complexity", "medium")
        time_estimates = {"easy": "30m", "medium": "2h", "hard": "4h+"}
        task["estimated_time"] = time_estimates.get(complexity, "2h")

    return tasks

def main():
    """Main entry point"""
    log("🚀 Starting task analysis...")

    # Create output directory
    os.makedirs(AUTONOMOUS_DIR, exist_ok=True)

    # Analyze tasks
    tasks = analyze_tasks()

    # Enrich with analysis
    enriched_tasks = enrich_tasks_with_analysis(tasks)

    # Sort again after enrichment
    enriched_tasks = sorted(enriched_tasks, key=lambda t: t["score"], reverse=True)

    # Save to output file
    output = {
        "generated_at": datetime.now().isoformat(),
        "total_tasks": len(enriched_tasks),
        "tasks": enriched_tasks
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    log(f"💾 Saved prioritized tasks to: {OUTPUT_FILE}")

    # Print summary
    log(f"\n📋 Task Summary:")
    log(f"   Total tasks: {len(enriched_tasks)}")
    high_priority = [t for t in enriched_tasks if t["priority"] == "high"]
    log(f"   High priority: {len(high_priority)}")
    medium_priority = [t for t in enriched_tasks if t["priority"] == "medium"]
    log(f"   Medium priority: {len(medium_priority)}")

    if enriched_tasks:
        log(f"\n🎯 Top 5 Priority Tasks:")
        for i, task in enumerate(enriched_tasks[:5], 1):
            log(f"   {i}. {task['name']} (Score: {task['score']:.1f})")
            log(f"      Priority: {task['priority']}, Age: {task['age_hours']:.1f}h")

    return enriched_tasks

if __name__ == "__main__":
    try:
        tasks = main()
        print(json.dumps({"status": "success", "task_count": len(tasks)}, indent=2))
    except Exception as e:
        log(f"❌ Task analysis failed: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
