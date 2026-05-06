"""
Tests for TaskBar manager module.
"""

import os
import json
import pytest
from datetime import datetime
from pathlib import Path

from taskbar.manager import TaskManager
from taskbar.task import Task, TaskStatus, TaskPriority


@pytest.fixture
def temp_storage(tmp_path):
    """Create a temporary storage file."""
    return str(tmp_path / "test_tasks.json")


@pytest.fixture
def manager(temp_storage):
    """Create a TaskManager with temporary storage."""
    return TaskManager(storage_path=temp_storage)


class TestTaskManager:
    """Tests for TaskManager class."""

    def test_create_task(self, manager):
        """Test task creation."""
        task = manager.create_task(name="Test Task")
        assert task.name == "Test Task"
        assert task.id in manager.tasks

    def test_create_task_with_options(self, manager):
        """Test task creation with all options."""
        task = manager.create_task(
            name="Test",
            description="Description",
            priority=TaskPriority.HIGH,
            total_steps=50,
            tags=["work", "urgent"],
        )
        assert task.description == "Description"
        assert task.priority == TaskPriority.HIGH
        assert task.total_steps == 50
        assert task.tags == ["work", "urgent"]

    def test_get_task(self, manager):
        """Test getting a task by ID."""
        created = manager.create_task(name="Test")
        task = manager.get_task(created.id)
        assert task is not None
        assert task.name == "Test"

    def test_get_task_not_found(self, manager):
        """Test getting a non-existent task."""
        task = manager.get_task("nonexistent")
        assert task is None

    def test_update_task(self, manager):
        """Test updating a task."""
        task = manager.create_task(name="Test")
        updated = manager.update_task(task.id, name="Updated", progress=50.0)
        assert updated.name == "Updated"
        assert updated.progress == 50.0

    def test_delete_task(self, manager):
        """Test deleting a task."""
        task = manager.create_task(name="Test")
        assert manager.delete_task(task.id)
        assert task.id not in manager.tasks

    def test_delete_task_not_found(self, manager):
        """Test deleting a non-existent task."""
        assert not manager.delete_task("nonexistent")

    def test_list_tasks(self, manager):
        """Test listing tasks."""
        manager.create_task(name="Task 1")
        manager.create_task(name="Task 2")
        tasks = manager.list_tasks()
        assert len(tasks) == 2

    def test_list_tasks_filter_status(self, manager):
        """Test filtering tasks by status."""
        task1 = manager.create_task(name="Task 1")
        task2 = manager.create_task(name="Task 2")
        task1.start()
        manager.save()

        pending = manager.list_tasks(status=TaskStatus.PENDING)
        active = manager.list_tasks(status=TaskStatus.IN_PROGRESS)

        assert len(pending) == 1
        assert len(active) == 1

    def test_list_tasks_filter_priority(self, manager):
        """Test filtering tasks by priority."""
        manager.create_task(name="Low", priority=TaskPriority.LOW)
        manager.create_task(name="High", priority=TaskPriority.HIGH)

        high = manager.list_tasks(priority=TaskPriority.HIGH)
        assert len(high) == 1
        assert high[0].name == "High"

    def test_list_tasks_filter_tag(self, manager):
        """Test filtering tasks by tag."""
        manager.create_task(name="Task 1", tags=["work"])
        manager.create_task(name="Task 2", tags=["personal"])

        work = manager.list_tasks(tag="work")
        assert len(work) == 1
        assert work[0].name == "Task 1"

    def test_list_tasks_search(self, manager):
        """Test searching tasks."""
        manager.create_task(name="Important Task", description="Very important")
        manager.create_task(name="Regular Task", description="Not important")

        results = manager.list_tasks(search="important")
        assert len(results) == 2  # Both match in name or description

    def test_get_active_tasks(self, manager):
        """Test getting active tasks."""
        task1 = manager.create_task(name="Task 1")
        task2 = manager.create_task(name="Task 2")
        task1.start()
        manager.save()

        active = manager.get_active_tasks()
        assert len(active) == 1

    def test_get_completed_tasks(self, manager):
        """Test getting completed tasks."""
        task = manager.create_task(name="Task")
        task.complete()
        manager.save()

        completed = manager.get_completed_tasks()
        assert len(completed) == 1

    def test_get_pending_tasks(self, manager):
        """Test getting pending tasks."""
        manager.create_task(name="Task 1")
        task2 = manager.create_task(name="Task 2")
        task2.start()
        manager.save()

        pending = manager.get_pending_tasks()
        assert len(pending) == 1

    def test_get_overall_progress(self, manager):
        """Test overall progress calculation."""
        task1 = manager.create_task(name="Task 1")
        task2 = manager.create_task(name="Task 2")
        task1.set_progress(50.0)
        task2.set_progress(100.0)
        manager.save()

        progress = manager.get_overall_progress()
        assert progress == 75.0

    def test_get_statistics(self, manager):
        """Test statistics calculation."""
        task1 = manager.create_task(name="Task 1")
        task2 = manager.create_task(name="Task 2")
        task1.start()
        task2.complete()
        manager.save()

        stats = manager.get_statistics()
        assert stats["total"] == 2
        assert stats["in_progress"] == 1
        assert stats["completed"] == 1

    def test_add_dependency(self, manager):
        """Test adding dependency."""
        task1 = manager.create_task(name="Task 1")
        task2 = manager.create_task(name="Task 2")
        assert manager.add_dependency(task2.id, task1.id)
        assert task1.id in task2.dependencies

    def test_add_dependency_circular(self, manager):
        """Test that circular dependencies are prevented."""
        task1 = manager.create_task(name="Task 1")
        task2 = manager.create_task(name="Task 2")
        manager.add_dependency(task2.id, task1.id)
        # Try to create circular dependency
        assert not manager.add_dependency(task1.id, task2.id)

    def test_get_dependencies(self, manager):
        """Test getting dependencies."""
        task1 = manager.create_task(name="Task 1")
        task2 = manager.create_task(name="Task 2")
        manager.add_dependency(task2.id, task1.id)

        deps = manager.get_dependencies(task2.id)
        assert len(deps) == 1
        assert deps[0].name == "Task 1"

    def test_get_dependents(self, manager):
        """Test getting dependents."""
        task1 = manager.create_task(name="Task 1")
        task2 = manager.create_task(name="Task 2")
        manager.add_dependency(task2.id, task1.id)

        dependents = manager.get_dependents(task1.id)
        assert len(dependents) == 1
        assert dependents[0].name == "Task 2"

    def test_save_and_load(self, temp_storage):
        """Test persistence."""
        manager1 = TaskManager(storage_path=temp_storage)
        manager1.create_task(name="Persistent Task")
        manager1.save()

        manager2 = TaskManager(storage_path=temp_storage)
        assert len(manager2.tasks) == 1
        assert "Persistent Task" in [t.name for t in manager2.tasks.values()]

    def test_export_tasks(self, manager):
        """Test exporting tasks."""
        manager.create_task(name="Task 1")
        manager.create_task(name="Task 2")

        exported = manager.export_tasks()
        assert len(exported) == 2

    def test_import_tasks(self, manager):
        """Test importing tasks."""
        data = [
            {"name": "Imported 1"},
            {"name": "Imported 2"},
        ]
        count = manager.import_tasks(data)
        assert count == 2
        assert len(manager.tasks) == 2

    def test_clear_completed(self, manager):
        """Test clearing completed tasks."""
        task1 = manager.create_task(name="Task 1")
        task2 = manager.create_task(name="Task 2")
        task1.complete()
        manager.save()

        count = manager.clear_completed()
        assert count == 1
        assert len(manager.tasks) == 1

    def test_len(self, manager):
        """Test len() on manager."""
        manager.create_task(name="Task 1")
        manager.create_task(name="Task 2")
        assert len(manager) == 2

    def test_iter(self, manager):
        """Test iteration over manager."""
        manager.create_task(name="Task 1")
        manager.create_task(name="Task 2")
        names = [t.name for t in manager]
        assert len(names) == 2

    def test_contains(self, manager):
        """Test 'in' operator."""
        task = manager.create_task(name="Test")
        assert task.id in manager
        assert "nonexistent" not in manager
