"""Epic import module for parsing epic.md and creating tasks in the registry."""

import re
from pathlib import Path
from typing import List, Dict, Optional, Union
from datetime import datetime


class EpicParser:
    """Parses epic.md files to extract task information."""
    
    def __init__(self, epic_path: Union[str, Path]):
        self.epic_path = Path(epic_path)
        self.content = self.epic_path.read_text()
    
    def parse(self) -> Dict:
        """Parse the epic.md file and extract task information.
        
        Returns:
            Dictionary with epic metadata and tasks
        """
        # Parse frontmatter
        frontmatter = self._parse_frontmatter()
        
        # Parse tasks from the epic
        tasks = self._parse_tasks()
        
        return {
            "name": frontmatter.get("name", "Unknown Epic"),
            "status": frontmatter.get("status", "planned"),
            "created": frontmatter.get("created"),
            "tasks": tasks,
        }
    
    def _parse_frontmatter(self) -> Dict:
        """Parse YAML frontmatter from the epic.md file."""
        frontmatter = {}
        
        # Extract content between --- markers
        match = re.match(r"^---\n(.*?)\n---", self.content, re.DOTALL)
        if match:
            frontmatter_text = match.group(1)
            for line in frontmatter_text.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    frontmatter[key.strip()] = value.strip()
        
        return frontmatter
    
    def _parse_tasks(self) -> List[Dict]:
        """Parse tasks from the epic.md file.
        
        Task format in epic.md:
        **Task X.Y**: Task title
        - Description line 1
        - Description line 2
        - **Dependencies**: Task A.B, Task C.D
        - **Parallel**: Yes/No
        - **Estimated**: X hours
        """
        tasks = []
        current_phase = None
        
        lines = self.content.split("\n")
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Detect phase headers (### Phase X: ...)
            phase_match = re.match(r"^### Phase (\d+): (.+)", line)
            if phase_match:
                current_phase = f"phase-{phase_match.group(1)}"
                i += 1
                continue
            
            # Detect task headers (**Task X.Y**: ...)
            task_match = re.match(r"^\*\*Task ([\d.]+)\*\*:\s*(.+)", line)
            if task_match:
                task_number = task_match.group(1)
                task_title = task_match.group(2).strip()
                
                # Parse task details (bulleted lines after task header)
                details = self._parse_task_details(lines, i + 1)
                
                # Build task ID from epic name and task number
                task_id = f"TASK-{task_number.replace('.', '-')}"
                
                tasks.append({
                    "id": task_id,
                    "number": task_number,
                    "title": task_title,
                    "description": "\n".join(details.get("description", [])),
                    "phase": current_phase,
                    "dependencies": details.get("dependencies", []),
                    "parallel": details.get("parallel", False),
                    "estimated_hours": details.get("estimated_hours"),
                })
            
            i += 1
        
        return tasks
    
    def _parse_task_details(self, lines: List[str], start_index: int) -> Dict:
        """Parse task details from bulleted lines following task header."""
        details = {
            "description": [],
            "dependencies": [],
            "parallel": False,
            "estimated_hours": None,
        }
        
        i = start_index
        while i < len(lines):
            line = lines[i]
            
            # Stop at next task, phase, or empty line
            if line.startswith("**Task") or line.startswith("###") or line.strip() == "":
                break
            
            # Parse bulleted lines
            if line.strip().startswith("-"):
                content = line.strip()[1:].strip()
                
                if content.startswith("**Dependencies**:"):
                    deps_str = content.replace("**Dependencies**:", "").strip()
                    if deps_str != "None":
                        # Parse "Task 1.1, Task 1.2" or similar formats
                        deps = re.findall(r"Task ([\d.]+)", deps_str)
                        details["dependencies"] = [
                            f"TASK-{dep.replace('.', '-')}" for dep in deps
                        ]
                
                elif content.startswith("**Parallel**:"):
                    parallel_str = content.replace("**Parallel**:", "").strip()
                    details["parallel"] = parallel_str.lower() == "yes"
                
                elif content.startswith("**Estimated**:"):
                    estimated_str = content.replace("**Estimated**:", "").strip()
                    # Extract number from "2 hours" or "2h" or "2"
                    hours_match = re.search(r"(\d+)", estimated_str)
                    if hours_match:
                        details["estimated_hours"] = int(hours_match.group(1))
                
                else:
                    # Regular description line
                    details["description"].append(content)
            
            i += 1
        
        return details


def import_from_epic(
    epic_path: Union[str, Path],
    registry_manager,
    objective_name: Optional[str] = None,
) -> List[str]:
    """Import tasks from an epic.md file into the task registry.
    
    Args:
        epic_path: Path to the epic.md file
        registry_manager: TaskRegistryManager instance
        objective_name: Objective name (defaults to epic name)
    
    Returns:
        List of created task IDs
    """
    parser = EpicParser(epic_path)
    epic_data = parser.parse()
    
    if objective_name is None:
        # Derive objective name from epic name (lowercase, replace spaces with hyphens)
        objective_name = epic_data["name"].lower().replace(" ", "-")
    
    created_tasks = []
    
    for task_data in epic_data["tasks"]:
        # Create task in registry
        task = registry_manager.create_task(
            task_id=task_data["id"],
            title=task_data["title"],
            description=task_data.get("description", ""),
            objective=objective_name,
            phase=task_data.get("phase"),
            dependencies=task_data.get("dependencies", []),
            priority="high",  # Default priority
            tags=[task_data.get("phase", "")] if task_data.get("phase") else [],
        )
        
        created_tasks.append(task.id)
        
        print(f"✅ Created task {task.id}: {task.title}")
        if task_data.get("estimated_hours"):
            print(f"   Estimated: {task_data['estimated_hours']}h")
        if task_data.get("dependencies"):
            print(f"   Dependencies: {', '.join(task_data['dependencies'])}")
    
    print(f"\n📊 Imported {len(created_tasks)} tasks from epic '{epic_data['name']}'")
    
    return created_tasks


def import_with_breakdown(
    epic_path: Union[str, Path],
    breakdown_path: Union[str, Path],
    registry_manager,
    objective_name: Optional[str] = None,
) -> List[str]:
    """Import tasks from epic.md and TASK-BREAKDOWN.md for enhanced dependency info.
    
    Args:
        epic_path: Path to the epic.md file
        breakdown_path: Path to the TASK-BREAKDOWN.md file
        registry_manager: TaskRegistryManager instance
        objective_name: Objective name (defaults to epic name)
    
    Returns:
        List of created task IDs
    """
    # First import from epic
    created_tasks = import_from_epic(epic_path, registry_manager, objective_name)
    
    # Then parse breakdown for enhanced dependency info
    breakdown_path = Path(breakdown_path)
    if breakdown_path.exists():
        breakdown_content = breakdown_path.read_text()
        
        # Parse the dependencies matrix table
        # Format: | Task | Depends On | Blocks | Parallel With |
        in_table = False
        for line in breakdown_content.split("\n"):
            if "| Task | Depends On" in line:
                in_table = True
                continue
            
            if in_table and line.startswith("|"):
                parts = [p.strip() for p in line.split("|")[1:-1]]  # Skip empty start/end
                if len(parts) >= 2 and parts[0] and not parts[0].startswith("-"):
                    # This is a task row
                    task_number = parts[0].strip()
                    depends_on_str = parts[1].strip()
                    blocks_str = parts[2].strip() if len(parts) > 2 else ""
                    
                    task_id = f"TASK-{task_number.replace('.', '-')}"
                    
                    # Parse dependencies
                    dependencies = []
                    if depends_on_str and depends_on_str != "None":
                        deps = re.findall(r"([\d.]+)", depends_on_str)
                        dependencies = [f"TASK-{dep.replace('.', '-')}" for dep in deps]
                    
                    # Update task with enhanced dependencies
                    if dependencies:
                        task = registry_manager.get_task(task_id)
                        if task:
                            registry_manager.update_task(task_id, dependencies=dependencies)
                            print(f"  Updated dependencies for {task_id}: {dependencies}")
    
    return created_tasks


# CLI command for epic import
def import_epic_command(
    epic_path: str,
    breakdown_path: Optional[str] = None,
    registry_path: str = "data/task_registry.json",
    objective: Optional[str] = None,
):
    """CLI command to import tasks from an epic.md file."""
    from .registry import TaskRegistryManager
    
    registry_manager = TaskRegistryManager(registry_path)
    
    print(f"📥 Importing tasks from epic: {epic_path}")
    
    if breakdown_path:
        created_tasks = import_with_breakdown(
            epic_path,
            breakdown_path,
            registry_manager,
            objective,
        )
    else:
        created_tasks = import_from_epic(
            epic_path,
            registry_manager,
            objective,
        )
    
    print(f"\n✅ Successfully imported {len(created_tasks)} tasks")
    print("\nRun 'task list' to see all imported tasks.")
    print("Run 'task available' to see tasks ready for assignment.")


if __name__ == "__main__":
    import sys
    
    epic_path = sys.argv[1] if len(sys.argv) > 1 else "plans/active/user-profile/epic.md"
    breakdown_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    import_epic_command(epic_path, breakdown_path)
