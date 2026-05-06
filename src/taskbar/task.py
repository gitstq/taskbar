"""
Task module - Core task data structures and operations.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, List, Dict, Any
from uuid import uuid4


class TaskStatus(Enum):
    """Task status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"

    def __str__(self) -> str:
        return self.value


class TaskPriority(Enum):
    """Task priority enumeration."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

    def __str__(self) -> str:
        return self.name.lower()


@dataclass
class Task:
    """
    Task class representing a single task with progress tracking.
    
    Attributes:
        id: Unique task identifier
        name: Task name
        description: Task description
        status: Current task status
        priority: Task priority level
        progress: Progress percentage (0-100)
        total_steps: Total number of steps
        completed_steps: Number of completed steps
        created_at: Task creation timestamp
        started_at: Task start timestamp
        completed_at: Task completion timestamp
        due_date: Task due date
        tags: List of tags for categorization
        dependencies: List of task IDs this task depends on
        subtasks: List of subtask Task objects
        metadata: Additional metadata dictionary
    """
    id: str = field(default_factory=lambda: str(uuid4())[:8])
    name: str = ""
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    progress: float = 0.0
    total_steps: int = 100
    completed_steps: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    due_date: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    subtasks: List["Task"] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate task data after initialization."""
        if not self.name:
            raise ValueError("Task name cannot be empty")
        if self.progress < 0 or self.progress > 100:
            raise ValueError("Progress must be between 0 and 100")
        if self.completed_steps < 0 or self.completed_steps > self.total_steps:
            raise ValueError("Completed steps must be between 0 and total_steps")

    def start(self) -> None:
        """Start the task."""
        if self.status == TaskStatus.PENDING:
            self.status = TaskStatus.IN_PROGRESS
            self.started_at = datetime.now()

    def pause(self) -> None:
        """Pause the task."""
        if self.status == TaskStatus.IN_PROGRESS:
            self.status = TaskStatus.PAUSED

    def resume(self) -> None:
        """Resume a paused task."""
        if self.status == TaskStatus.PAUSED:
            self.status = TaskStatus.IN_PROGRESS

    def complete(self) -> None:
        """Mark the task as completed."""
        self.status = TaskStatus.COMPLETED
        self.progress = 100.0
        self.completed_steps = self.total_steps
        self.completed_at = datetime.now()

    def cancel(self) -> None:
        """Cancel the task."""
        self.status = TaskStatus.CANCELLED

    def update_progress(self, steps: int = 1) -> None:
        """
        Update task progress by incrementing completed steps.
        
        Args:
            steps: Number of steps to add (default: 1)
        """
        if self.status != TaskStatus.IN_PROGRESS:
            self.start()
        
        self.completed_steps = min(self.completed_steps + steps, self.total_steps)
        self.progress = (self.completed_steps / self.total_steps) * 100
        
        if self.progress >= 100:
            self.complete()

    def set_progress(self, percentage: float) -> None:
        """
        Set task progress directly.
        
        Args:
            percentage: Progress percentage (0-100)
        """
        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100")
        
        if self.status == TaskStatus.PENDING:
            self.start()
        
        self.progress = percentage
        self.completed_steps = int((percentage / 100) * self.total_steps)
        
        if self.progress >= 100:
            self.complete()

    def add_subtask(self, subtask: "Task") -> None:
        """
        Add a subtask to this task.
        
        Args:
            subtask: Task object to add as subtask
        """
        self.subtasks.append(subtask)

    def remove_subtask(self, subtask_id: str) -> bool:
        """
        Remove a subtask by ID.
        
        Args:
            subtask_id: ID of the subtask to remove
            
        Returns:
            True if subtask was removed, False if not found
        """
        for i, subtask in enumerate(self.subtasks):
            if subtask.id == subtask_id:
                self.subtasks.pop(i)
                return True
        return False

    def add_dependency(self, task_id: str) -> None:
        """
        Add a task dependency.
        
        Args:
            task_id: ID of the task this task depends on
        """
        if task_id not in self.dependencies and task_id != self.id:
            self.dependencies.append(task_id)

    def remove_dependency(self, task_id: str) -> bool:
        """
        Remove a task dependency.
        
        Args:
            task_id: ID of the dependency to remove
            
        Returns:
            True if dependency was removed, False if not found
        """
        if task_id in self.dependencies:
            self.dependencies.remove(task_id)
            return True
        return False

    def get_elapsed_time(self) -> Optional[timedelta]:
        """
        Get elapsed time since task started.
        
        Returns:
            Elapsed time as timedelta, or None if not started
        """
        if self.started_at is None:
            return None
        
        end_time = self.completed_at or datetime.now()
        return end_time - self.started_at

    def get_estimated_remaining(self) -> Optional[timedelta]:
        """
        Estimate remaining time based on current progress.
        
        Returns:
            Estimated remaining time as timedelta, or None if cannot estimate
        """
        elapsed = self.get_elapsed_time()
        if elapsed is None or self.progress == 0 or self.progress >= 100:
            return None
        
        remaining_progress = 100 - self.progress
        time_per_percent = elapsed.total_seconds() / self.progress
        remaining_seconds = time_per_percent * remaining_progress
        return timedelta(seconds=remaining_seconds)

    def get_subtask_progress(self) -> float:
        """
        Calculate overall progress from subtasks.
        
        Returns:
            Average progress of all subtasks, or 0 if no subtasks
        """
        if not self.subtasks:
            return 0.0
        
        total_progress = sum(s.progress for s in self.subtasks)
        return total_progress / len(self.subtasks)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert task to dictionary representation.
        
        Returns:
            Dictionary containing all task data
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "progress": self.progress,
            "total_steps": self.total_steps,
            "completed_steps": self.completed_steps,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "tags": self.tags,
            "dependencies": self.dependencies,
            "subtasks": [s.to_dict() for s in self.subtasks],
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """
        Create a Task from dictionary representation.
        
        Args:
            data: Dictionary containing task data
            
        Returns:
            Task object
        """
        subtasks = [cls.from_dict(s) for s in data.get("subtasks", [])]
        
        return cls(
            id=data.get("id", str(uuid4())[:8]),
            name=data["name"],
            description=data.get("description", ""),
            status=TaskStatus(data.get("status", "pending")),
            priority=TaskPriority(data.get("priority", 2)),
            progress=data.get("progress", 0.0),
            total_steps=data.get("total_steps", 100),
            completed_steps=data.get("completed_steps", 0),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else datetime.now(),
            started_at=datetime.fromisoformat(data["started_at"]) if data.get("started_at") else None,
            completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None,
            due_date=datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None,
            tags=data.get("tags", []),
            dependencies=data.get("dependencies", []),
            subtasks=subtasks,
            metadata=data.get("metadata", {}),
        )

    def __str__(self) -> str:
        """String representation of task."""
        status_icons = {
            TaskStatus.PENDING: "⏳",
            TaskStatus.IN_PROGRESS: "🔄",
            TaskStatus.COMPLETED: "✅",
            TaskStatus.PAUSED: "⏸️",
            TaskStatus.CANCELLED: "❌",
        }
        icon = status_icons.get(self.status, "📋")
        return f"{icon} [{self.id}] {self.name} ({self.progress:.1f}%)"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"Task(id='{self.id}', name='{self.name}', status={self.status}, progress={self.progress:.1f}%)"
