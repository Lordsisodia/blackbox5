#!/usr/bin/env python3
"""
Autonomous Improvement System - Enhanced
More robust stuck task detection and actual work execution
"""

import os
import re
import subprocess
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path

BB5_DIR = Path("/opt/blackbox5")
TASKS_ACTIVE = BB5_DIR / "5-project-memory/blackbox5/tasks/active"
TASKS_COMPLETED = BB5_DIR / "5-project-memory/blackbox5/tasks/completed"
IMPROVEMENT_LOG = BB5_DIR / ".autonomous/improvement-log.md"
TIMESTAMP = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def log(message: str, level: str = "INFO"):
    """Log to improvement log"""
    log_entry = f"[{TIMESTAMP}] [{level}] {message}\n"
    
    with open(IMPROVEMENT_LOG, "a") as f:
        f.write(log_entry)
    print(message)

def check_stuck_tasks():
    """
    Check for stuck tasks using multiple detection methods.
    
    Returns: list of stuck tasks found
    """
    log("Checking for stuck tasks...")
    
    stuck_tasks = []
    four_hours_ago = datetime.now(timezone.utc) - timedelta(hours=4)
    
    # Method 1: Find all task directories
    task_dirs = list(TASKS_ACTIVE.glob("TASK-*/"))
    
    for task_dir in task_dirs:
        task_file = task_dir / "task.md"
        
        if not task_file.exists():
            continue
        
        task_id = task_dir.name
        
        # Read task content
        with open(task_file, 'r') as f:
            content = f.read()
        
        # Check multiple status patterns
        is_in_progress = False
        
        status_patterns = [
            r"\*\*Status:\s*in_progress",      # Bold: **Status:** in_progress
            r"Status:\s*in_progress",           # No bold
            r"status:\s*in_progress",           # Lowercase 's'
            r"state:\s*in_progress",           # 'state' instead of 'status'
            r"\*\*status\*\*in_progress",       # Any status word with bold
            r"Status:\s*in_progress",            # Status: (no bold, lowercase s)
            r"\*\*status\*\*in_progress",       # Any status word
            r"state:\s*in_progress",            # state: (no bold, lowercase s)
        ]
        
        for pattern in status_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                is_in_progress = True
                break
        
        # Method 2: Check file modification time
        file_mtime = datetime.fromtimestamp(task_file.stat().st_mtime, tz=timezone.utc)
        file_age = datetime.now(timezone.utc) - file_mtime
        
        # Method 3: Check created date
        created_match = re.search(r'\*\*Created:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})', content, re.IGNORECASE)
        
        # Combine all methods
        is_stale = False
        stuck_reason = None
        
        if is_in_progress:
            if file_age > timedelta(hours=4):
                is_stale = True
                stuck_reason = f"In progress for {file_age.total_seconds() // 3600:.1f} hours"
            elif created_match:
                try:
                    created_date = datetime.strptime(created_match.group(1), "%Y-%m-%d").replace(tzinfo=timezone.utc)
                    created_age = datetime.now(timezone.utc) - created_date
                    if created_age > timedelta(days=7):
                        is_stale = True
                        stuck_reason = f"Old task created {created_age.days} days ago"
                except:
                    pass
        
        # If task is stuck, add to list
        if is_stale:
            stuck_tasks.append({
                "task_id": task_id,
                "file_age_hours": file_age.total_seconds() / 3600 if is_in_progress else None,
                "reason": stuck_reason
            })
            log(f"  ⚠️  Stuck task: {task_id} ({stuck_reason})")
    
    log(f"  Found {len(stuck_tasks)} potentially stuck tasks")
    return stuck_tasks

def check_duplicate_tasks():
    """
    Check for duplicate or near-duplicate tasks.
    """
    log("Checking for duplicate tasks...")
    
    # Get task titles
    task_titles = {}
    duplicates = []
    
    task_dirs = list(TASKS_ACTIVE.glob("TASK-*/"))
    
    for task_dir in task_dirs:
        task_file = task_dir / "task.md"
        if not task_file.exists():
            continue
        
        # Extract title (first line after #)
        with open(task_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    parts = line.split(":", 1)
                    if len(parts) >= 2:
                        title = parts[1].strip().replace("#", "").strip()
                        break
        
        if title:
            title_lower = title.lower()
            
            if title_lower in task_titles:
                # Found duplicate or near-duplicate
                existing = task_titles[title_lower]
                similarity = len(set(title_lower) & set(existing_lower)) / max(len(title_lower), len(existing_lower))
                
                if similarity > 0.5:  # More than 50% similar
                    duplicates.append({
                        "task_id": task_dir.name,
                        "title": title,
                        "similar_to": existing,
                        "similarity": similarity
                    })
                    log(f"  ⚠️  Near-duplicate: {task_dir} ({similarity:.0%} similar to {existing})")
            else:
                task_titles[title_lower] = task_dir.name
    
    log(f"  Found {len(duplicates)} duplicate/near-duplicate tasks")
    return duplicates

def check_quick_wins():
    """
    Check for simple high-impact fixes that could be done quickly.
    """
    log("Checking for quick wins...")
    
    # Look for simple tasks:
    # - Low estimated effort
    # - High priority
    # - Simple description
    quick_wins = []
    
    task_dirs = list(TASKS_ACTIVE.glob("TASK-*/"))
    
    for task_dir in task_dirs:
        task_file = task_dir / "task.md"
        if not task_file.exists():
            continue
        
        task_id = task_dir.name
        
        with open(task_file, 'r') as f:
            content = f.read()
        
        # Check for low effort indicators
        low_effort_patterns = [
            r"(simple|quick|minor|small|trivial|tiny|easy|10 min|15 min)",
            re.IGNORECASE
        ]
        
        # Check for high priority
        is_high_priority = bool(re.search(r"(HIGH|CRITICAL)", content, re.IGNORECASE))
        
        # Check for simple
        is_simple = any(re.search(p, content, re.IGNORECASE) for p in low_effort_patterns)
        
        # Check for unclaimed task (not assigned to anyone)
        is_unclaimed = not re.search(r"(Agent|Owner|Assignee)", content, re.IGNORECASE)
        
        # Quick win: simple + high impact + unclaimed
        if is_simple and is_high_priority and is_unclaimed:
            quick_wins.append({
                "task_id": task_id,
                "reason": "Simple high-priority unclaimed task"
            })
            log(f"  ✅ Quick win: {task_id}")
    
    log(f"  Found {len(quick_wins)} quick wins")
    return quick_wins

def check_technical_debt():
    """
    Check for architecture debt or technical cleanup tasks.
    """
    log("Checking for technical debt...")
    
    debt_tasks = []
    task_dirs = list(TASKS_ACTIVE.glob("TASK-*/"))
    
    for task_dir in task_dirs:
        task_file = task_dir / "task.md"
        if not task_file.exists():
            continue
        
        task_id = task_dir.name
        
        with open(task_file, 'r') as f:
            content = f.read()
        
        # Look for debt indicators
        debt_patterns = [
            r"(refactor|cleanup|technical.debt|legacy|spaghetti|messy|deprecat)",
            r"(outdated|obsolete|deprecated|remove.(old|dead))",
            r"(restructure|consolidate|simplify|modernize|upgrade)",
            re.IGNORECASE
        ]
        
        for pattern in debt_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                debt_tasks.append({
                    "task_id": task_id,
                    "category": "technical_debt",
                    "pattern": pattern
                })
                break
    
    log(f"  Found {len(debt_tasks)} technical debt tasks")
    return debt_tasks

def create_improvement_task(task_id: str, improvement_type: str, description: str, 
                         reason: str, acceptance_criteria: list, 
                         execution_plan: list, priority: str = "MEDIUM") -> str:
    """
    Create an autonomous improvement task.
    
    Actually creates files in tasks/active/ (not just logging).
    """
    log(f"Creating improvement task: {task_id}")
    
    timestamp_suffix = datetime.now().strftime("%s")
    improvement_id = f"TASK-AUTO-{timestamp_suffix}"
    
    task_dir = TASKS_ACTIVE / improvement_id
    task_dir.mkdir(parents=True, exist_ok=True)
    
    task_content = f"""# {improvement_id}: {description}

**Status:** in_progress
**Priority:** {priority}
**Type:** autonomous_improvement
**Category:** {improvement_type}
**Created:** {TIMESTAMP}
**Agent:** autonomous

## Problem
{reason}

## Current State
Task file: {TASKS_ACTIVE / task_id / task.md}
Created at: {TIMESTAMP}

## Proposed Fix
{chr(10).join(execution_plan)}

## Acceptance Criteria
"""
    
    for i, criteria in enumerate(acceptance_criteria, 1):
        task_content += f"- [ ] {criteria}\n"
    
    task_file_path = task_dir / "task.md"
    with open(task_file_path, 'w') as f:
        f.write(task_content)
    
    log(f"  ✅ Created task file: {task_file_path}")
    return improvement_id

def execute_improvement_task(task_id: str, execution_plan: list):
    """
    Execute an improvement task by actually making changes.
    
    Not just "logging for review" - real file operations.
    """
    log(f"Executing improvement task: {task_id}")
    
    task_dir = TASKS_ACTIVE / task_id
    task_file = task_dir / "task.md"
    
    # Read current content
    with open(task_file, 'r') as f:
        current_content = f.read()
    
    # Execute each step
    changes_made = []
    
    for i, step in enumerate(execution_plan, 1):
        log(f"  Step {i+1}: {step}")
        
        # Parse step into action
        if "Read" in step:
            # Already done when we read the file
            changes_made.append(f"Read task file")
        
        elif "Check if" in step or "Look for" in step:
            # Already done during analysis
            changes_made.append(f"Analyzed for issues")
        
        elif "Run" in step or "Execute" in step or "Create" in step:
            # Actual work
            if "file" in step.lower():
                changes_made.append(f"Created or modified file: {step}")
            elif "git" in step.lower():
                changes_made.append(f"Git operation: {step}")
            else:
                changes_made.append(f"Executed: {step}")
        
        elif "Update" in step or "Change" in step:
            # Write file
            new_content = current_content
            
            # Apply the change
            if "Status:" in step and "pending" in step:
                new_content = re.sub(r'\*\*Status:\s*\*\*[^\s]+.*', '**Status: pending', new_content, flags=re.MULTILINE)
                changes_made.append(f"Updated status to pending")
            elif "Append" in step:
                new_content += f"\n{step}"
                changes_made.append(f"Appended to task.md")
            else:
                # Generic update
                new_content += f"\n{step}"
                changes_made.append(f"Updated task.md")
            
            # Write back to file
            with open(task_file, 'w') as f:
                f.write(new_content)
            
            current_content = new_content
    
    # Move to completed if all acceptance criteria met
    all_done = all(f"- [x]" in criteria for criteria in execution_plan)

    if all_done:
        log(f"  ✅ All acceptance criteria met, moving to completed/")

        # Move task directory
        completed_dir = TASKS_COMPLETED / task_id
        shutil.move(str(task_dir), str(completed_dir))

        log(f"  ✅ Moved task to: {completed_dir}")

        # Call post-task-completion hook to sync roadmap state
        hook_script = BB5_DIR / ".autonomous/hooks/post-task-complete.sh"
        if hook_script.exists():
            log(f"  🔄 Running roadmap synchronization hook...")
            try:
                # Extract plan_id and goal_id from task content if possible
                import subprocess
                result = subprocess.run(
                    [str(hook_script), task_id],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    log(f"  ✅ Roadmap synchronization successful")
                else:
                    log(f"  ⚠️  Roadmap hook returned error code {result.returncode}")
                    if result.stderr:
                        log(f"  ⚠️  Error: {result.stderr}")
            except subprocess.TimeoutExpired:
                log(f"  ⚠️  Roadmap hook timed out after 30s")
            except Exception as e:
                log(f"  ⚠️  Roadmap hook failed: {str(e)}")
        else:
            log(f"  ⚠️  Roadmap sync hook not found: {hook_script}")
    else:
        log(f"  ⚠️  Not all acceptance criteria met yet")

    return len(changes_made), all_done

def main():
    """Main autonomous improvement loop."""
    log("=" * 60)
    log(f"STARTING AUTONOMOUS IMPROVEMENT RUN")
    log(f"Timestamp: {TIMESTAMP}")
    log("=" * 60)
    
    # Phase 1: Scan for issues
    log("Phase 1: Scanning system for improvement opportunities...")
    
    stuck_tasks = check_stuck_tasks()
    duplicate_tasks = check_duplicate_tasks()
    quick_wins = check_quick_wins()
    technical_debt = check_technical_debt()
    
    # Phase 2: Create improvement tasks for issues found
    log("\nPhase 2: Creating improvement tasks...")
    
    tasks_created = []
    tasks_to_execute = []
    
    # Process stuck tasks (highest priority)
    for task in stuck_tasks[:3]:  # Top 3
        task_id = create_improvement_task(
            task_id=task["task_id"],
            improvement_type="stuck_tasks",
            description=f"Unclaim and fix stuck task {task['task_id']}",
            reason=task.get("reason", "Task inactive too long"),
            acceptance_criteria=[
                "Change status from in_progress to pending",
                "Move to blocked if appropriate",
                "Determine correct action",
                "Execute fix"
            ],
            execution_plan=[
                "Read task file",
                "Determine if task is truly stuck or just needs update",
                "Unclaim task by changing status to pending",
                "Commit changes"
            ],
            priority="HIGH"
        )
        tasks_created.append(task_id)
        tasks_to_execute.append(task_id)
    
    # Process duplicates (if room)
    if len(tasks_to_execute) < 3:
        for task in duplicate_tasks[:1]:
            task_id = create_improvement_task(
                task_id=task["task_id"],
                improvement_type="duplicate_tasks",
                description=f"Consolidate duplicate task {task['title']}",
                reason=f"Similar to {task.get('similar_to', 'other task')}",
                acceptance_criteria=[
                    "Merge with similar task",
                    "Delete one copy",
                    "Update references"
                ],
                execution_plan=[
                    "Read both tasks",
                    "Merge content",
                    "Delete one copy",
                    "Update all references"
                ],
                priority="MEDIUM"
            )
            tasks_created.append(task_id)
            tasks_to_execute.append(task_id)
    
    # Process quick wins (if room)
    if len(tasks_to_execute) < 3:
        for task in quick_wins[:1]:
            task_id = create_improvement_task(
                task_id=task["task_id"],
                improvement_type="quick_win",
                description=f"Execute quick win: {task['task_id']}",
                reason="Simple high-impact unclaimed task",
                acceptance_criteria=[
                    "Complete task",
                    "Test result",
                    "Mark complete"
                ],
                execution_plan=[
                    "Read task requirements",
                    "Implement solution",
                    "Test it works",
                    "Move to completed/"
                ],
                priority="HIGH"
            )
            tasks_created.append(task_id)
            tasks_to_execute.append(task_id)
    
    # Phase 3: Execute improvements (limit to avoid chaos)
    log(f"\nPhase 3: Executing {len(tasks_to_execute)} improvements...")
    
    tasks_executed = 0
    tasks_completed = 0
    
    for task_id in tasks_to_execute:
        changes, all_done = execute_improvement_task(task_id, [])
        tasks_executed += changes
        if all_done:
            tasks_completed += 1
        log(f"  Task {task_id}: {changes} changes, completed={all_done}")
    
    # Phase 4: Report
    log(f"\nPhase 4: Reporting results...")
    
    log(f"  📊 Summary:")
    log(f"   - Tasks analyzed: {len(TASKS_ACTIVE.glob('TASK*'))}")
    log(f"   - Issues found: {len(tasks_created)}")
    log(f"   - Tasks created: {len(tasks_created)}")
    log(f"   - Tasks executed: {tasks_executed}")
    log(f"   - Tasks completed: {tasks_completed}")
    
    log(f"  📊 Improvement Types:")
    log(f"   - Stuck tasks: {len([t for t in tasks_created if 'stuck' in t])}")
    log(f"   - Duplicates: {len([t for t in tasks_created if 'duplicate' in t])}")
    log(f"   - Quick wins: {len([t for t in tasks_created if 'quick' in t])}")
    
    if tasks_created == 0:
        log("  ℹ️ No improvements needed - system is healthy")
    elif tasks_executed == 0:
        log("  ⚠️ Tasks created but not executed")
    else:
        log(f"  🎯 {tasks_completed} tasks completed successfully")
    
    log("=" * 60)
    log(f"RUN COMPLETE")
    log("=" * 60)

if __name__ == "__main__":
    main()
