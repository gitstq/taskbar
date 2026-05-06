"""
Tests for TaskBar exporter module.
"""

import pytest
from datetime import datetime

from taskbar.task import Task, TaskStatus, TaskPriority
from taskbar.exporter import TaskExporter


@pytest.fixture
def sample_tasks():
    """Create sample tasks for testing."""
    task1 = Task(name="Task 1", description="First task")
    task1.set_progress(50.0)

    task2 = Task(name="Task 2", description="Second task")
    task2.set_progress(100.0)
    task2.complete()

    task3 = Task(name="Task 3", tags=["work", "urgent"])

    return [task1, task2, task3]


class TestTaskExporter:
    """Tests for TaskExporter class."""

    def test_to_json(self, sample_tasks):
        """Test JSON export."""
        json_str = TaskExporter.to_json(sample_tasks)
        assert '"Task 1"' in json_str
        assert '"Task 2"' in json_str
        assert '"total_tasks": 3' in json_str

    def test_to_csv(self, sample_tasks):
        """Test CSV export."""
        csv_str = TaskExporter.to_csv(sample_tasks)
        assert "Task 1" in csv_str
        assert "Task 2" in csv_str
        assert "id,name,description" in csv_str

    def test_to_markdown(self, sample_tasks):
        """Test Markdown export."""
        md_str = TaskExporter.to_markdown(sample_tasks)
        assert "# Task List" in md_str
        assert "Task 1" in md_str
        assert "Task 2" in md_str

    def test_to_html(self, sample_tasks):
        """Test HTML export."""
        html_str = TaskExporter.to_html(sample_tasks)
        assert "<!DOCTYPE html>" in html_str
        assert "Task 1" in html_str
        assert "Task 2" in html_str

    def test_format_duration(self):
        """Test duration formatting."""
        from datetime import timedelta

        assert TaskExporter._format_duration(timedelta(seconds=30)) == "30s"
        assert TaskExporter._format_duration(timedelta(minutes=5, seconds=30)) == "5m 30s"
        assert TaskExporter._format_duration(timedelta(hours=2, minutes=30)) == "2h 30m"

    def test_export_to_file_json(self, sample_tasks, tmp_path):
        """Test exporting to JSON file."""
        filepath = str(tmp_path / "tasks.json")
        result = TaskExporter.export_to_file(sample_tasks, filepath)
        assert result
        assert tmp_path.joinpath("tasks.json").exists()

    def test_export_to_file_csv(self, sample_tasks, tmp_path):
        """Test exporting to CSV file."""
        filepath = str(tmp_path / "tasks.csv")
        result = TaskExporter.export_to_file(sample_tasks, filepath)
        assert result
        assert tmp_path.joinpath("tasks.csv").exists()

    def test_export_to_file_markdown(self, sample_tasks, tmp_path):
        """Test exporting to Markdown file."""
        filepath = str(tmp_path / "tasks.md")
        result = TaskExporter.export_to_file(sample_tasks, filepath)
        assert result
        assert tmp_path.joinpath("tasks.md").exists()

    def test_export_to_file_html(self, sample_tasks, tmp_path):
        """Test exporting to HTML file."""
        filepath = str(tmp_path / "tasks.html")
        result = TaskExporter.export_to_file(sample_tasks, filepath)
        assert result
        assert tmp_path.joinpath("tasks.html").exists()

    def test_export_unsupported_format(self, sample_tasks, tmp_path):
        """Test that unsupported format raises error."""
        filepath = str(tmp_path / "tasks.xyz")
        with pytest.raises(ValueError):
            TaskExporter.export_to_file(sample_tasks, filepath)
