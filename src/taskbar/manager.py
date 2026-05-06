"""
Task Manager module - Manages multiple tasks with persistence and operations.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable

from taskbar.task import Task, TaskStatus, TaskPriority


class TaskManager:
    """
    Task Manager for handling multiple tasks with persistence.
    
    Features:
    - Create, update, delete tasks
    - Task persistence to file
    - Task filtering and search
    - Dependency management
    - Progress tracking across all tasks
    """

    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize TaskManager.
        
        Args:
            storage_path: Path to storage file (default: ~/.taskbar/tasks.json)
        """
        self.tasks: Dict[str, Task] = {}
        self.storage_path = storage_path or str(Path.home() / ".taskbar" / "tasks.json")
        self._ensure_storage_dir()
        self.load()

    def _ensure_storage_dir(self) -> None:
        """Ensure storage directory exists."""
        storage_dir = os.path.dirname(self.storage_path)
        if storage_dir:
            os.makedirs(storage_dir, exist_ok=True)

    def create_task(
        self,
        name: str,
        description: str = "",
        priority: TaskPriority = TaskPriority.MEDIUM,
        total_steps: int = 100,
        tags: Optional[List[str]] = None,
        due_date: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Task:
        """
        Create a new task.
        
        Args:
            name: Task name
            description: Task description
            priority: Task priority
            total_steps: Total number of steps
            tags: List of tags
            due_date: Task due date
            metadata: Additional metadata
            
        Returns:
            Created Task object
        """
        task = Task(
            name=name,
            description=description,
            priority=priority,
            total_steps=total_steps,
            tags=tags or [],
            due_date=due_date,
            metadata=metadata or {},
        )
        self.tasks[task.id] = task
        self.save()
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get a task by ID.
        
        Args:
            task_id: Task ID
            
        Returns:
            Task object or None if not found
        """
        return self.tasks.get(task_id)

    def update_task(self, task_id: str, **kwargs) -> Optional[Task]:
        """
        Update task properties.
        
        Args:
            task_id: Task ID
            **kwargs: Properties to update
            
        Returns:
            Updated Task object or None if not found
        """
        task = self.get_task(task_id)
        if task is None:
            return None

        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)

        self.save()
        return task

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task by ID.
        
        Args:
            task_id: Task ID
            
        Returns:
            True if deleted, False if not found
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            # Remove from dependencies of other tasks
            for task in self.tasks.values():
                task.remove_dependency(task_id)
            self.save()
            return True
        return False

    def list_tasks(
        self,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        tag: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[Task]:
        """
        List tasks with optional filtering.
        
        Args:
            status: Filter by status
            priority: Filter by priority
            tag: Filter by tag
            search: Search in name and description
            
        Returns:
            List of matching tasks
        """
        tasks = list(self.tasks.values())

        if status:
            tasks = [t for t in tasks if t.status == status]
        if priority:
            tasks = [t for t in tasks if t.priority == priority]
        if tag:
            tasks = [t for t in tasks if tag in t.tags]
        if search:
            search_lower = search.lower()
            tasks = [
                t for t in tasks
                if search_lower in t.name.lower() or search_lower in t.description.lower()
            ]

        return tasks

    def get_active_tasks(self) -> List[Task]:
        """
        Get all active (in progress) tasks.
        
        Returns:
            List of active tasks
        """
        return self.list_tasks(status=TaskStatus.IN_PROGRESS)

    def get_completed_tasks(self) -> List[Task]:
        """
        Get all completed tasks.
        
        Returns:
            List of completed tasks
        """
        return self.list_tasks(status=TaskStatus.COMPLETED)

    def get_pending_tasks(self) -> List[Task]:
        """
        Get all pending tasks.
        
        Returns:
            List of pending tasks
        """
        return self.list_tasks(status=TaskStatus.PENDING)

    def get_overall_progress(self) -> float:
        """
        Calculate overall progress across all tasks.
        
        Returns:
            Overall progress percentage
        """
        if not self.tasks:
            return 0.0

        total_progress = sum(t.progress for t in self.tasks.values())
        return total_progress / len(self.tasks)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get task statistics.
        
        Returns:
            Dictionary with statistics
        """
        total = len(self.tasks)
        if total == 0:
            return {
                "total": 0,
                "pending": 0,
                "in_progress": 0,
                "completed": 0,
                "paused": 0,
                "cancelled": 0,
                "overall_progress": 0.0,
            }

        stats = {
            "total": total,
            "pending": len(self.get_pending_tasks()),
            "in_progress": len(self.get_active_tasks()),
            "completed": len(self.get_completed_tasks()),
            "paused": len(self.list_tasks(status=TaskStatus.PAUSED)),
            "cancelled": len(self.list_tasks(status=TaskStatus.CANCELLED)),
            "overall_progress": self.get_overall_progress(),
        }

        return stats

    def add_dependency(self, task_id: str, depends_on_id: str) -> bool:
        """
        Add a dependency between tasks.
        
        Args:
            task_id: Task to add dependency to
            depends_on_id: Task that the first task depends on
            
        Returns:
            True if dependency added, False if tasks not found
        """
        task = self.get_task(task_id)
        depends_on = self.get_task(depends_on_id)

        if task is None or depends_on is None:
            return False

        # Check for circular dependency
        if self._has_circular_dependency(depends_on_id, task_id):
            return False

        task.add_dependency(depends_on_id)
        self.save()
        return True

    def _has_circular_dependency(
        self,
        from_id: str,
        to_id: str,
        visited: Optional[set] = None
    ) -> bool:
        """
        Check for circular dependencies.
        
        Args:
            from_id: Starting task ID
            to_id: Target task ID
            visited: Set of visited task IDs
            
        Returns:
            True if circular dependency detected
        """
        if visited is None:
            visited = set()

        if from_id in visited:
            return False

        visited.add(from_id)

        task = self.get_task(from_id)
        if task is None:
            return False

        for dep_id in task.dependencies:
            if dep_id == to_id:
                return True
            if self._has_circular_dependency(dep_id, to_id, visited):
                return True

        return False

    def get_dependencies(self, task_id: str) -> List[Task]:
        """
        Get all tasks that a task depends on.
        
        Args:
            task_id: Task ID
            
        Returns:
            List of dependency tasks
        """
        task = self.get_task(task_id)
        if task is None:
            return []

        return [self.tasks[dep_id] for dep_id in task.dependencies if dep_id in self.tasks]

    def get_dependents(self, task_id: str) -> List[Task]:
        """
        Get all tasks that depend on a task.
        
        Args:
            task_id: Task ID
            
        Returns:
            List of dependent tasks
        """
        dependents = []
        for task in self.tasks.values():
            if task_id in task.dependencies:
                dependents.append(task)
        return dependents

    def save(self) -> None:
        """Save tasks to storage file."""
        data = {
            "version": "1.0.0",
            "saved_at": datetime.now().isoformat(),
            "tasks": [task.to_dict() for task in self.tasks.values()],
        }

        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load(self) -> None:
        """Load tasks from storage file."""
        if not os.path.exists(self.storage_path):
            return

        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.tasks.clear()
            for task_data in data.get("tasks", []):
                task = Task.from_dict(task_data)
                self.tasks[task.id] = task
        except (json.JSONDecodeError, KeyError):
            # If file is corrupted, start fresh
            self.tasks.clear()

    def export_tasks(self) -> List[Dict[str, Any]]:
        """
        Export all tasks as list of dictionaries.
        
        Returns:
            List of task dictionaries
        """
        return [task.to_dict() for task in self.tasks.values()]

    def import_tasks(self, tasks_data: List[Dict[str, Any]], merge: bool = True) -> int:
        """
        Import tasks from list of dictionaries.
        
        Args:
            tasks_data: List of task dictionaries
            merge: If True, merge with existing; if False, replace
            
        Returns:
            Number of tasks imported
        """
        if not merge:
            self.tasks.clear()

        count = 0
        for task_data in tasks_data:
            task = Task.from_dict(task_data)
            self.tasks[task.id] = task
            count += 1

        self.save()
        return count

    def clear_completed(self) -> int:
        """
        Remove all completed tasks.
        
        Returns:
            Number of tasks removed
        """
        completed_ids = [t.id for t in self.get_completed_tasks()]
        for task_id in completed_ids:
            del self.tasks[task_id]
        self.save()
        return len(completed_ids)

    def __len__(self) -> int:
        """Return number of tasks."""
        return len(self.tasks)

    def __iter__(self):
        """Iterate over tasks."""
        return iter(self.tasks.values())

    def __contains__(self, task_id: str) -> bool:
        """Check if task exists."""
        return task_id in self.tasks
