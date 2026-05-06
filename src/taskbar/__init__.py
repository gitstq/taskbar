"""
TaskBar - A powerful terminal-based task progress tracking tool.

Features:
- Multi-task parallel progress tracking
- Nested task support with unlimited depth
- Dependency visualization
- Time statistics and estimation
- Multi-format export (JSON, YAML, CSV, Markdown)
- Terminal UI with rich formatting
"""

__version__ = "1.0.0"
__author__ = "SOLO Agent"
__license__ = "MIT"

from taskbar.task import Task, TaskStatus, TaskPriority
from taskbar.manager import TaskManager
from taskbar.exporter import TaskExporter

__all__ = [
    "Task",
    "TaskStatus",
    "TaskPriority",
    "TaskManager",
    "TaskExporter",
]
