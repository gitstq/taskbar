"""
Tests for TaskBar task module.
"""

import pytest
from datetime import datetime, timedelta

from taskbar.task import Task, TaskStatus, TaskPriority


class TestTask:
    """Tests for Task class."""

    def test_create_task(self):
        """Test basic task creation."""
        task = Task(name="Test Task")
        assert task.name == "Test Task"
        assert task.status == TaskStatus.PENDING
        assert task.progress == 0.0
        assert len(task.id) == 8

    def test_create_task_with_description(self):
        """Test task creation with description."""
        task = Task(name="Test", description="A test task")
        assert task.description == "A test task"

    def test_create_task_empty_name_raises(self):
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError):
            Task(name="")

    def test_start_task(self):
        """Test starting a task."""
        task = Task(name="Test")
        task.start()
        assert task.status == TaskStatus.IN_PROGRESS
        assert task.started_at is not None

    def test_pause_task(self):
        """Test pausing a task."""
        task = Task(name="Test")
        task.start()
        task.pause()
        assert task.status == TaskStatus.PAUSED

    def test_resume_task(self):
        """Test resuming a paused task."""
        task = Task(name="Test")
        task.start()
        task.pause()
        task.resume()
        assert task.status == TaskStatus.IN_PROGRESS

    def test_complete_task(self):
        """Test completing a task."""
        task = Task(name="Test")
        task.start()
        task.complete()
        assert task.status == TaskStatus.COMPLETED
        assert task.progress == 100.0
        assert task.completed_at is not None

    def test_cancel_task(self):
        """Test cancelling a task."""
        task = Task(name="Test")
        task.start()
        task.cancel()
        assert task.status == TaskStatus.CANCELLED

    def test_update_progress(self):
        """Test updating progress by steps."""
        task = Task(name="Test", total_steps=10)
        task.update_progress(3)
        assert task.completed_steps == 3
        assert task.progress == 30.0

    def test_update_progress_auto_complete(self):
        """Test that progress update auto-completes at 100%."""
        task = Task(name="Test", total_steps=10)
        task.update_progress(10)
        assert task.status == TaskStatus.COMPLETED
        assert task.progress == 100.0

    def test_set_progress(self):
        """Test setting progress directly."""
        task = Task(name="Test")
        task.set_progress(50.0)
        assert task.progress == 50.0

    def test_set_progress_invalid(self):
        """Test that invalid progress raises ValueError."""
        task = Task(name="Test")
        with pytest.raises(ValueError):
            task.set_progress(150.0)
        with pytest.raises(ValueError):
            task.set_progress(-10.0)

    def test_add_subtask(self):
        """Test adding subtasks."""
        task = Task(name="Parent")
        subtask = Task(name="Child")
        task.add_subtask(subtask)
        assert len(task.subtasks) == 1
        assert task.subtasks[0].name == "Child"

    def test_remove_subtask(self):
        """Test removing subtasks."""
        task = Task(name="Parent")
        subtask = Task(name="Child")
        task.add_subtask(subtask)
        assert task.remove_subtask(subtask.id)
        assert len(task.subtasks) == 0

    def test_add_dependency(self):
        """Test adding dependencies."""
        task = Task(name="Test")
        task.add_dependency("other-id")
        assert "other-id" in task.dependencies

    def test_remove_dependency(self):
        """Test removing dependencies."""
        task = Task(name="Test")
        task.add_dependency("other-id")
        assert task.remove_dependency("other-id")
        assert "other-id" not in task.dependencies

    def test_get_elapsed_time(self):
        """Test elapsed time calculation."""
        task = Task(name="Test")
        assert task.get_elapsed_time() is None
        task.start()
        elapsed = task.get_elapsed_time()
        assert elapsed is not None
        assert elapsed.total_seconds() >= 0

    def test_get_estimated_remaining(self):
        """Test remaining time estimation."""
        task = Task(name="Test")
        assert task.get_estimated_remaining() is None
        task.start()
        task.set_progress(50.0)
        remaining = task.get_estimated_remaining()
        assert remaining is not None

    def test_get_subtask_progress(self):
        """Test subtask progress calculation."""
        task = Task(name="Parent")
        sub1 = Task(name="Child 1")
        sub1.set_progress(50.0)
        sub2 = Task(name="Child 2")
        sub2.set_progress(100.0)
        task.add_subtask(sub1)
        task.add_subtask(sub2)
        assert task.get_subtask_progress() == 75.0

    def test_to_dict(self):
        """Test task serialization."""
        task = Task(name="Test", description="A test")
        data = task.to_dict()
        assert data["name"] == "Test"
        assert data["description"] == "A test"
        assert data["status"] == "pending"

    def test_from_dict(self):
        """Test task deserialization."""
        data = {
            "name": "Test",
            "description": "A test",
            "status": "in_progress",
            "progress": 50.0,
        }
        task = Task.from_dict(data)
        assert task.name == "Test"
        assert task.status == TaskStatus.IN_PROGRESS
        assert task.progress == 50.0

    def test_str_representation(self):
        """Test string representation."""
        task = Task(name="Test")
        assert "Test" in str(task)
        assert "⏳" in str(task)  # Pending icon


class TestTaskStatus:
    """Tests for TaskStatus enum."""

    def test_status_values(self):
        """Test status enum values."""
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.IN_PROGRESS.value == "in_progress"
        assert TaskStatus.COMPLETED.value == "completed"
        assert TaskStatus.PAUSED.value == "paused"
        assert TaskStatus.CANCELLED.value == "cancelled"


class TestTaskPriority:
    """Tests for TaskPriority enum."""

    def test_priority_values(self):
        """Test priority enum values."""
        assert TaskPriority.LOW.value == 1
        assert TaskPriority.MEDIUM.value == 2
        assert TaskPriority.HIGH.value == 3
        assert TaskPriority.URGENT.value == 4
