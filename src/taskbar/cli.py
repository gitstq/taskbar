"""
CLI module - Command-line interface for TaskBar.
"""

import os
import sys
from datetime import datetime
from typing import Optional

import click
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich.live import Live
from rich.layout import Layout

from taskbar.task import Task, TaskStatus, TaskPriority
from taskbar.manager import TaskManager
from taskbar.exporter import TaskExporter

console = Console()


def get_manager() -> TaskManager:
    """Get TaskManager instance."""
    return TaskManager()


def format_priority(priority: TaskPriority) -> str:
    """Format priority with color."""
    colors = {
        TaskPriority.LOW: "dim",
        TaskPriority.MEDIUM: "white",
        TaskPriority.HIGH: "yellow",
        TaskPriority.URGENT: "red bold",
    }
    color = colors.get(priority, "white")
    return f"[{color}]{priority.name}[/{color}]"


def format_status(status: TaskStatus) -> str:
    """Format status with icon and color."""
    formats = {
        TaskStatus.PENDING: "[yellow]⏳ pending[/yellow]",
        TaskStatus.IN_PROGRESS: "[blue]🔄 in_progress[/blue]",
        TaskStatus.COMPLETED: "[green]✅ completed[/green]",
        TaskStatus.PAUSED: "[dim]⏸️ paused[/dim]",
        TaskStatus.CANCELLED: "[red]❌ cancelled[/red]",
    }
    return formats.get(status, str(status))


@click.group(invoke_without_command=True)
@click.option("--version", "-v", is_flag=True, help="Show version")
@click.pass_context
def main(ctx: click.Context, version: bool) -> None:
    """TaskBar - Terminal-based task progress tracking tool."""
    if version:
        from taskbar import __version__
        console.print(f"TaskBar version {__version__}")
        return

    if ctx.invoked_subcommand is None:
        # Default: show task list
        ctx.invoke(list_tasks)


@main.command()
@click.argument("name")
@click.option("--description", "-d", default="", help="Task description")
@click.option("--priority", "-p", type=click.Choice(["low", "medium", "high", "urgent"]), default="medium", help="Task priority")
@click.option("--steps", "-s", default=100, help="Total steps")
@click.option("--tags", "-t", multiple=True, help="Tags for the task")
@click.option("--due", help="Due date (YYYY-MM-DD or YYYY-MM-DD HH:MM)")
def add(name: str, description: str, priority: str, steps: int, tags: tuple, due: Optional[str]) -> None:
    """Create a new task."""
    manager = get_manager()

    priority_map = {
        "low": TaskPriority.LOW,
        "medium": TaskPriority.MEDIUM,
        "high": TaskPriority.HIGH,
        "urgent": TaskPriority.URGENT,
    }

    due_date = None
    if due:
        try:
            due_date = datetime.strptime(due, "%Y-%m-%d %H:%M")
        except ValueError:
            try:
                due_date = datetime.strptime(due, "%Y-%m-%d")
            except ValueError:
                console.print("[red]Invalid due date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM[/red]")
                return

    task = manager.create_task(
        name=name,
        description=description,
        priority=priority_map[priority],
        total_steps=steps,
        tags=list(tags),
        due_date=due_date,
    )

    console.print(f"[green]✓ Task created:[/green] [{task.id}] {name}")
    console.print(f"  Use [cyan]taskbar start {task.id}[/cyan] to begin working on it")


@main.command("list")
@click.option("--status", "-s", type=click.Choice(["pending", "in_progress", "completed", "paused", "cancelled"]), help="Filter by status")
@click.option("--priority", "-p", type=click.Choice(["low", "medium", "high", "urgent"]), help="Filter by priority")
@click.option("--tag", "-t", help="Filter by tag")
@click.option("--search", help="Search in task names and descriptions")
@click.option("--all", "-a", "show_all", is_flag=True, help="Show all tasks including completed")
def list_tasks(status: Optional[str], priority: Optional[str], tag: Optional[str], search: Optional[str], show_all: bool) -> None:
    """List all tasks."""
    manager = get_manager()

    status_filter = None
    if status:
        status_filter = TaskStatus(status)

    priority_filter = None
    if priority:
        priority_map = {
            "low": TaskPriority.LOW,
            "medium": TaskPriority.MEDIUM,
            "high": TaskPriority.HIGH,
            "urgent": TaskPriority.URGENT,
        }
        priority_filter = priority_map[priority]

    tasks = manager.list_tasks(
        status=status_filter,
        priority=priority_filter,
        tag=tag,
        search=search,
    )

    if not tasks:
        console.print("[yellow]No tasks found[/yellow]")
        return

    table = Table(title="📋 Task List", show_header=True, header_style="bold cyan")
    table.add_column("ID", style="dim", width=8)
    table.add_column("Name", width=30)
    table.add_column("Status", width=15)
    table.add_column("Priority", width=10)
    table.add_column("Progress", width=20)
    table.add_column("Tags", width=15)

    for task in tasks:
        progress_bar = f"[green]{'█' * int(task.progress / 5)}[/green][dim]{'░' * (20 - int(task.progress / 5))}[/dim]"
        progress_text = f"{progress_bar} {task.progress:.0f}%"

        table.add_row(
            task.id,
            task.name[:30] + ("..." if len(task.name) > 30 else ""),
            format_status(task.status),
            format_priority(task.priority),
            progress_text,
            ", ".join(task.tags[:3]) or "-",
        )

    console.print(table)

    # Show statistics
    stats = manager.get_statistics()
    console.print()
    console.print(f"[bold]Statistics:[/bold] {stats['total']} total | "
                  f"[blue]{stats['in_progress']} active[/blue] | "
                  f"[green]{stats['completed']} completed[/green] | "
                  f"[yellow]{stats['pending']} pending[/yellow]")


@main.command()
@click.argument("task_id")
def start(task_id: str) -> None:
    """Start working on a task."""
    manager = get_manager()
    task = manager.get_task(task_id)

    if not task:
        console.print(f"[red]Task not found: {task_id}[/red]")
        return

    task.start()
    manager.save()
    console.print(f"[green]✓ Started task:[/green] {task.name}")
    console.print(f"  Use [cyan]taskbar progress {task_id}[/cyan] to update progress")


@main.command()
@click.argument("task_id")
def pause(task_id: str) -> None:
    """Pause a task."""
    manager = get_manager()
    task = manager.get_task(task_id)

    if not task:
        console.print(f"[red]Task not found: {task_id}[/red]")
        return

    task.pause()
    manager.save()
    console.print(f"[yellow]⏸ Paused task:[/yellow] {task.name}")


@main.command()
@click.argument("task_id")
def resume(task_id: str) -> None:
    """Resume a paused task."""
    manager = get_manager()
    task = manager.get_task(task_id)

    if not task:
        console.print(f"[red]Task not found: {task_id}[/red]")
        return

    task.resume()
    manager.save()
    console.print(f"[green]▶ Resumed task:[/green] {task.name}")


@main.command()
@click.argument("task_id")
def complete(task_id: str) -> None:
    """Mark a task as completed."""
    manager = get_manager()
    task = manager.get_task(task_id)

    if not task:
        console.print(f"[red]Task not found: {task_id}[/red]")
        return

    task.complete()
    manager.save()
    console.print(f"[green]✅ Completed task:[/green] {task.name}")

    elapsed = task.get_elapsed_time()
    if elapsed:
        console.print(f"  Time spent: [cyan]{TaskExporter._format_duration(elapsed)}[/cyan]")


@main.command()
@click.argument("task_id")
@click.argument("progress", type=float)
def progress(task_id: str, progress: float) -> None:
    """Update task progress (0-100)."""
    manager = get_manager()
    task = manager.get_task(task_id)

    if not task:
        console.print(f"[red]Task not found: {task_id}[/red]")
        return

    task.set_progress(progress)
    manager.save()

    bar = "█" * int(progress / 5) + "░" * (20 - int(progress / 5))
    console.print(f"[green]Progress updated:[/green] {task.name}")
    console.print(f"  [{bar}] {progress:.0f}%")

    if task.status == TaskStatus.COMPLETED:
        console.print("[green]🎉 Task completed![/green]")


@main.command()
@click.argument("task_id")
@click.argument("steps", type=int, default=1)
def step(task_id: str, steps: int) -> None:
    """Increment task progress by steps."""
    manager = get_manager()
    task = manager.get_task(task_id)

    if not task:
        console.print(f"[red]Task not found: {task_id}[/red]")
        return

    task.update_progress(steps)
    manager.save()

    bar = "█" * int(task.progress / 5) + "░" * (20 - int(task.progress / 5))
    console.print(f"[green]Progress updated:[/green] {task.name}")
    console.print(f"  [{bar}] {task.progress:.0f}% ({task.completed_steps}/{task.total_steps})")

    if task.status == TaskStatus.COMPLETED:
        console.print("[green]🎉 Task completed![/green]")


@main.command()
@click.argument("task_id")
def show(task_id: str) -> None:
    """Show task details."""
    manager = get_manager()
    task = manager.get_task(task_id)

    if not task:
        console.print(f"[red]Task not found: {task_id}[/red]")
        return

    # Create detail panel
    content = []
    content.append(f"[bold]ID:[/bold] {task.id}")
    content.append(f"[bold]Name:[/bold] {task.name}")
    content.append(f"[bold]Status:[/bold] {format_status(task.status)}")
    content.append(f"[bold]Priority:[/bold] {format_priority(task.priority)}")
    content.append(f"[bold]Progress:[/bold] {task.progress:.1f}% ({task.completed_steps}/{task.total_steps})")

    if task.description:
        content.append(f"[bold]Description:[/bold] {task.description}")

    if task.tags:
        content.append(f"[bold]Tags:[/bold] {', '.join(task.tags)}")

    if task.due_date:
        content.append(f"[bold]Due Date:[/bold] {task.due_date.strftime('%Y-%m-%d %H:%M')}")

    elapsed = task.get_elapsed_time()
    if elapsed:
        content.append(f"[bold]Elapsed Time:[/bold] {TaskExporter._format_duration(elapsed)}")

    remaining = task.get_estimated_remaining()
    if remaining:
        content.append(f"[bold]Est. Remaining:[/bold] {TaskExporter._format_duration(remaining)}")

    if task.dependencies:
        content.append(f"[bold]Dependencies:[/bold] {', '.join(task.dependencies)}")

    console.print(Panel("\n".join(content), title=f"📋 Task Details", border_style="cyan"))

    # Show subtasks if any
    if task.subtasks:
        tree = Tree(f"[bold]{task.name}[/bold] (subtasks)")
        for subtask in task.subtasks:
            status_icon = "✅" if subtask.status == TaskStatus.COMPLETED else "🔄"
            tree.add(f"{status_icon} {subtask.name} ({subtask.progress:.0f}%)")
        console.print(tree)


@main.command()
@click.argument("task_id")
@click.confirmation_option(prompt="Are you sure you want to delete this task?")
def delete(task_id: str) -> None:
    """Delete a task."""
    manager = get_manager()
    task = manager.get_task(task_id)

    if not task:
        console.print(f"[red]Task not found: {task_id}[/red]")
        return

    name = task.name
    if manager.delete_task(task_id):
        console.print(f"[red]🗑 Deleted task:[/red] {name}")


@main.command()
@click.argument("task_id")
@click.argument("subtask_name")
@click.option("--description", "-d", default="", help="Subtask description")
def subtask(task_id: str, subtask_name: str, description: str) -> None:
    """Add a subtask to a task."""
    manager = get_manager()
    task = manager.get_task(task_id)

    if not task:
        console.print(f"[red]Task not found: {task_id}[/red]")
        return

    sub = Task(name=subtask_name, description=description)
    task.add_subtask(sub)
    manager.save()

    console.print(f"[green]✓ Added subtask:[/green] {subtask_name} to {task.name}")


@main.command()
@click.argument("task_id")
@click.argument("depends_on_id")
def depend(task_id: str, depends_on_id: str) -> None:
    """Add a dependency between tasks."""
    manager = get_manager()

    if manager.add_dependency(task_id, depends_on_id):
        console.print(f"[green]✓ Added dependency:[/green] {task_id} → {depends_on_id}")
    else:
        console.print("[red]Failed to add dependency (circular dependency or task not found)[/red]")


@main.command()
@click.argument("format", type=click.Choice(["json", "yaml", "csv", "md", "html"]))
@click.option("--output", "-o", help="Output file path")
def export(format: str, output: Optional[str]) -> None:
    """Export tasks to various formats."""
    manager = get_manager()
    tasks = list(manager)

    if not tasks:
        console.print("[yellow]No tasks to export[/yellow]")
        return

    if output:
        TaskExporter.export_to_file(tasks, output, format)
        console.print(f"[green]✓ Exported to:[/green] {output}")
    else:
        # Print to stdout
        format_map = {
            "json": TaskExporter.to_json,
            "yaml": TaskExporter.to_yaml,
            "csv": TaskExporter.to_csv,
            "md": TaskExporter.to_markdown,
            "html": TaskExporter.to_html,
        }
        content = format_map[format](tasks)
        console.print(content)


@main.command()
def stats() -> None:
    """Show task statistics."""
    manager = get_manager()
    stats = manager.get_statistics()

    table = Table(title="📊 Task Statistics", show_header=False)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Total Tasks", str(stats["total"]))
    table.add_row("Pending", str(stats["pending"]))
    table.add_row("In Progress", str(stats["in_progress"]))
    table.add_row("Completed", str(stats["completed"]))
    table.add_row("Paused", str(stats["paused"]))
    table.add_row("Cancelled", str(stats["cancelled"]))
    table.add_row("Overall Progress", f"{stats['overall_progress']:.1f}%")

    console.print(table)


@main.command()
@click.confirmation_option(prompt="Are you sure you want to clear all completed tasks?")
def clear() -> None:
    """Clear all completed tasks."""
    manager = get_manager()
    count = manager.clear_completed()
    console.print(f"[green]✓ Cleared {count} completed tasks[/green]")


@main.command()
def tui() -> None:
    """Launch interactive terminal UI."""
    manager = get_manager()

    def generate_layout() -> Layout:
        layout = Layout()

        layout.split(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3),
        )

        layout["body"].split_row(
            Layout(name="tasks"),
            Layout(name="details"),
        )

        return layout

    def render() -> Panel:
        stats = manager.get_statistics()
        tasks = manager.list_tasks()

        # Header
        header = Panel(
            f"[bold cyan]TaskBar[/bold cyan] | "
            f"Total: {stats['total']} | "
            f"Active: [blue]{stats['in_progress']}[/blue] | "
            f"Progress: {stats['overall_progress']:.1f}%",
            style="bold white on blue",
        )

        # Task list
        task_table = Table(show_header=True, header_style="bold")
        task_table.add_column("ID", width=8)
        task_table.add_column("Name", width=25)
        task_table.add_column("Status", width=12)
        task_table.add_column("Progress", width=10)

        for task in tasks[:10]:
            task_table.add_row(
                task.id,
                task.name[:25],
                task.status.value,
                f"{task.progress:.0f}%",
            )

        return Panel(task_table, title="📋 Tasks", border_style="cyan")

    console.clear()
    console.print("[bold cyan]TaskBar Interactive Mode[/bold cyan]")
    console.print("Press Ctrl+C to exit\n")

    try:
        with Live(render(), console=console, refresh_per_second=1):
            import time
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Exiting interactive mode...[/yellow]")


if __name__ == "__main__":
    main()
