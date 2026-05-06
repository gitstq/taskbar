"""
Task Exporter module - Export tasks to various formats.
"""

import csv
import json
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import List, Optional, Dict, Any

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

from taskbar.task import Task, TaskStatus


class TaskExporter:
    """
    Export tasks to various file formats.
    
    Supported formats:
    - JSON
    - YAML (if PyYAML installed)
    - CSV
    - Markdown
    - HTML
    """

    @staticmethod
    def to_json(tasks: List[Task], indent: int = 2) -> str:
        """
        Export tasks to JSON format.
        
        Args:
            tasks: List of tasks to export
            indent: JSON indentation level
            
        Returns:
            JSON string
        """
        data = {
            "exported_at": datetime.now().isoformat(),
            "total_tasks": len(tasks),
            "tasks": [task.to_dict() for task in tasks],
        }
        return json.dumps(data, indent=indent, ensure_ascii=False)

    @staticmethod
    def to_yaml(tasks: List[Task]) -> str:
        """
        Export tasks to YAML format.
        
        Args:
            tasks: List of tasks to export
            
        Returns:
            YAML string
            
        Raises:
            ImportError: If PyYAML is not installed
        """
        if not YAML_AVAILABLE:
            raise ImportError("PyYAML is required for YAML export. Install with: pip install pyyaml")

        data = {
            "exported_at": datetime.now().isoformat(),
            "total_tasks": len(tasks),
            "tasks": [task.to_dict() for task in tasks],
        }
        return yaml.dump(data, default_flow_style=False, allow_unicode=True)

    @staticmethod
    def to_csv(tasks: List[Task]) -> str:
        """
        Export tasks to CSV format.
        
        Args:
            tasks: List of tasks to export
            
        Returns:
            CSV string
        """
        output = StringIO()
        fieldnames = [
            "id", "name", "description", "status", "priority",
            "progress", "total_steps", "completed_steps",
            "created_at", "started_at", "completed_at", "due_date",
            "tags", "dependencies"
        ]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for task in tasks:
            row = {
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "status": task.status.value,
                "priority": task.priority.name,
                "progress": f"{task.progress:.1f}%",
                "total_steps": task.total_steps,
                "completed_steps": task.completed_steps,
                "created_at": task.created_at.isoformat() if task.created_at else "",
                "started_at": task.started_at.isoformat() if task.started_at else "",
                "completed_at": task.completed_at.isoformat() if task.completed_at else "",
                "due_date": task.due_date.isoformat() if task.due_date else "",
                "tags": ", ".join(task.tags),
                "dependencies": ", ".join(task.dependencies),
            }
            writer.writerow(row)

        return output.getvalue()

    @staticmethod
    def to_markdown(tasks: List[Task], title: str = "Task List") -> str:
        """
        Export tasks to Markdown format.
        
        Args:
            tasks: List of tasks to export
            title: Document title
            
        Returns:
            Markdown string
        """
        lines = [
            f"# {title}",
            "",
            f"**Exported at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Total tasks:** {len(tasks)}",
            "",
            "## Task Summary",
            "",
        ]

        # Statistics
        status_counts = {}
        for status in TaskStatus:
            status_counts[status] = sum(1 for t in tasks if t.status == status)

        lines.extend([
            "| Status | Count |",
            "|--------|-------|",
        ])
        for status, count in status_counts.items():
            lines.append(f"| {status.value} | {count} |")

        lines.extend(["", "## Task Details", ""])

        for task in tasks:
            status_emoji = {
                TaskStatus.PENDING: "⏳",
                TaskStatus.IN_PROGRESS: "🔄",
                TaskStatus.COMPLETED: "✅",
                TaskStatus.PAUSED: "⏸️",
                TaskStatus.CANCELLED: "❌",
            }
            emoji = status_emoji.get(task.status, "📋")

            lines.extend([
                f"### {emoji} {task.name}",
                "",
                f"- **ID:** `{task.id}`",
                f"- **Status:** {task.status.value}",
                f"- **Priority:** {task.priority.name}",
                f"- **Progress:** {task.progress:.1f}%",
                f"- **Steps:** {task.completed_steps}/{task.total_steps}",
            ])

            if task.description:
                lines.extend(["", f"**Description:** {task.description}"])

            if task.tags:
                lines.extend(["", f"**Tags:** {', '.join(task.tags)}"])

            if task.due_date:
                lines.extend(["", f"**Due Date:** {task.due_date.strftime('%Y-%m-%d %H:%M')}"])

            elapsed = task.get_elapsed_time()
            if elapsed:
                lines.extend(["", f"**Elapsed Time:** {TaskExporter._format_duration(elapsed)}"])

            remaining = task.get_estimated_remaining()
            if remaining:
                lines.extend(["", f"**Estimated Remaining:** {TaskExporter._format_duration(remaining)}"])

            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def to_html(tasks: List[Task], title: str = "Task List") -> str:
        """
        Export tasks to HTML format.
        
        Args:
            tasks: List of tasks to export
            title: Document title
            
        Returns:
            HTML string
        """
        status_colors = {
            TaskStatus.PENDING: "#f0ad4e",
            TaskStatus.IN_PROGRESS: "#5bc0de",
            TaskStatus.COMPLETED: "#5cb85c",
            TaskStatus.PAUSED: "#777777",
            TaskStatus.CANCELLED: "#d9534f",
        }

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #4a90d9;
            padding-bottom: 10px;
        }}
        .task-card {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .task-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .task-name {{
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
        }}
        .task-status {{
            padding: 4px 12px;
            border-radius: 20px;
            color: white;
            font-size: 0.85em;
        }}
        .progress-bar {{
            background: #e0e0e0;
            border-radius: 10px;
            height: 20px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .progress-fill {{
            background: linear-gradient(90deg, #4a90d9, #67b26f);
            height: 100%;
            transition: width 0.3s ease;
        }}
        .task-meta {{
            color: #666;
            font-size: 0.9em;
        }}
        .tags {{
            display: flex;
            gap: 5px;
            flex-wrap: wrap;
            margin-top: 10px;
        }}
        .tag {{
            background: #e3f2fd;
            color: #1976d2;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8em;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p>Exported at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Total tasks: {len(tasks)}</p>
"""
        for task in tasks:
            color = status_colors.get(task.status, "#777777")
            html += f"""
    <div class="task-card">
        <div class="task-header">
            <span class="task-name">{task.name}</span>
            <span class="task-status" style="background-color: {color}">{task.status.value}</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {task.progress}%"></div>
        </div>
        <div class="task-meta">
            Progress: {task.progress:.1f}% | Steps: {task.completed_steps}/{task.total_steps} | Priority: {task.priority.name}
        </div>
"""
            if task.description:
                html += f'        <p>{task.description}</p>\n'

            if task.tags:
                html += '        <div class="tags">\n'
                for tag in task.tags:
                    html += f'            <span class="tag">{tag}</span>\n'
                html += '        </div>\n'

            html += "    </div>\n"

        html += """
</body>
</html>"""
        return html

    @staticmethod
    def _format_duration(duration) -> str:
        """Format timedelta to human-readable string."""
        total_seconds = int(duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    @staticmethod
    def export_to_file(
        tasks: List[Task],
        filepath: str,
        format: Optional[str] = None
    ) -> bool:
        """
        Export tasks to a file.
        
        Args:
            tasks: List of tasks to export
            filepath: Output file path
            format: Export format (json, yaml, csv, md, html). Auto-detected from extension if not provided.
            
        Returns:
            True if export successful
        """
        path = Path(filepath)
        format = format or path.suffix.lstrip(".").lower()

        format_map = {
            "json": TaskExporter.to_json,
            "yaml": TaskExporter.to_yaml,
            "yml": TaskExporter.to_yaml,
            "csv": TaskExporter.to_csv,
            "md": TaskExporter.to_markdown,
            "markdown": TaskExporter.to_markdown,
            "html": TaskExporter.to_html,
        }

        if format not in format_map:
            raise ValueError(f"Unsupported format: {format}. Supported: {list(format_map.keys())}")

        try:
            content = format_map[format](tasks)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            return True
        except Exception:
            return False
