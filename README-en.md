<div align="center">

# 📋 TaskBar

**A Powerful Terminal-Based Task Progress Tracking Tool**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**[简体中文](README-zh.md) | [繁體中文](README-zh-TW.md) | [English](README-en.md)**

</div>

---

## 🎉 Introduction

TaskBar is a **terminal-based task progress tracking tool** designed specifically for developers. It provides powerful task management features including nested tasks, dependency visualization, time statistics, and multi-format export, helping you efficiently manage project progress right in your terminal.

### 💡 Inspiration

In daily development, we often need to track progress of multiple tasks in the terminal. Existing tools are either too simple or require leaving the terminal for GUI applications. TaskBar was born to bring powerful task management into your most familiar terminal environment.

### ✨ Key Differentiators

- 🔄 **Smart Progress Tracking** - Auto-calculates remaining time with intelligent estimation based on historical progress
- 📊 **Nested Task Support** - Unlimited levels of subtasks with automatic progress aggregation
- 🔗 **Dependency Management** - Visualize task dependencies with automatic circular dependency detection
- 📈 **Real-time Statistics Panel** - Terminal TUI interface with live task status display
- 📦 **Multi-format Export** - Supports JSON, YAML, CSV, Markdown, and HTML formats
- ⚡ **Zero Configuration** - Install and use immediately with automatic data persistence

---

## ✨ Core Features

### 📝 Task Management

- ✅ Create, update, delete tasks
- ✅ Task status workflow (Pending → In Progress → Completed)
- ✅ Priority settings (Low/Medium/High/Urgent)
- ✅ Tag classification system
- ✅ Due date reminders

### 📊 Progress Tracking

- ✅ Percentage progress display
- ✅ Step counter
- ✅ Time statistics (elapsed/estimated remaining)
- ✅ Progress bar visualization

### 🔗 Advanced Features

- ✅ **Nested Tasks** - Unlimited subtask levels
- ✅ **Dependencies** - Inter-task dependency management
- ✅ **Cycle Detection** - Automatic circular dependency prevention
- ✅ **Data Persistence** - Automatic local storage

### 📤 Export Options

| Format | Use Case |
|--------|----------|
| JSON | Data exchange, API integration |
| YAML | Configuration files, version control |
| CSV | Excel import, data analysis |
| Markdown | Documentation, blog publishing |
| HTML | Report display, web publishing |

---

## 🚀 Quick Start

### 📋 Requirements

- Python 3.8 or higher
- pip package manager

### 📥 Installation

```bash
# Install from PyPI
pip install taskbar-cli

# Or install from source
git clone https://github.com/gitstq/taskbar.git
cd taskbar
pip install -e .
```

### 🎮 Basic Usage

```bash
# Create a new task
taskbar add "Complete project report" --priority high --tags work

# List all tasks
taskbar list

# Start working on a task
taskbar start <task_id>

# Update progress (percentage)
taskbar progress <task_id> 50

# Update progress by steps
taskbar step <task_id> 5

# View task details
taskbar show <task_id>

# Complete a task
taskbar complete <task_id>

# Export tasks
taskbar export json -o tasks.json
```

---

## 📖 Detailed Usage Guide

### Creating Tasks

```bash
# Basic creation
taskbar add "Task name"

# With all parameters
taskbar add "Important project" \
  --description "Detailed project description" \
  --priority high \
  --steps 50 \
  --tags work urgent \
  --due "2026-06-30"
```

### Task Status Management

```bash
# Start task
taskbar start <task_id>

# Pause task
taskbar pause <task_id>

# Resume task
taskbar resume <task_id>

# Complete task
taskbar complete <task_id>

# Delete task
taskbar delete <task_id>
```

### Progress Updates

```bash
# Set percentage progress
taskbar progress <task_id> 75

# Increment by steps
taskbar step <task_id>      # +1 step (default)
taskbar step <task_id> 5    # +5 steps
```

### Subtask Management

```bash
# Add subtask
taskbar subtask <parent_id> "Subtask name"

# Subtasks automatically calculate parent task progress
```

### Dependencies

```bash
# Add dependency
taskbar depend <task_id> <depends_on_id>

# System automatically detects circular dependencies
```

### Query and Filter

```bash
# List all tasks
taskbar list

# Filter by status
taskbar list --status in_progress

# Filter by priority
taskbar list --priority high

# Filter by tag
taskbar list --tag work

# Search tasks
taskbar list --search "keyword"
```

### Data Export

```bash
# Export to JSON
taskbar export json -o tasks.json

# Export to Markdown
taskbar export md -o tasks.md

# Export to HTML
taskbar export html -o tasks.html

# Export to CSV
taskbar export csv -o tasks.csv
```

### Statistics

```bash
# View statistics
taskbar stats
```

---

## 💡 Design Philosophy & Roadmap

### 🎯 Design Principles

1. **Simplicity First** - Intuitive command design with low learning curve
2. **Terminal Native** - Leverage terminal features without leaving command line
3. **Data Security** - Local storage ensures privacy
4. **Extensibility** - Modular design for easy feature expansion

### 🛠 Technology Stack

| Component | Technology | Reason |
|-----------|------------|--------|
| CLI Framework | Click | Clean command-line app development |
| Terminal UI | Rich | Beautiful terminal output |
| Data Storage | JSON | Lightweight, readable, easy backup |
| Packaging | setuptools | Python standard packaging tool |

### 📅 Roadmap

**v1.1.0 (Planned)**
- [ ] Interactive TUI interface
- [ ] Task templates
- [ ] Pomodoro timer

**v1.2.0 (Planned)**
- [ ] Team collaboration
- [ ] Cloud sync support
- [ ] Web Dashboard

**v2.0.0 (Future)**
- [ ] Plugin system
- [ ] API service
- [ ] Mobile sync

---

## 📦 Build & Deployment

### Local Development

```bash
# Clone repository
git clone https://github.com/gitstq/taskbar.git
cd taskbar

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or venv\Scripts\activate  # Windows

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/

# Type check
mypy src/
```

### Build for Release

```bash
# Build wheel package
python -m build

# Upload to PyPI
twine upload dist/*
```

---

## 🤝 Contributing

We welcome all forms of contributions!

### Submitting PRs

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add new feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request

### Reporting Issues

- Use a clear title to describe the problem
- Provide reproduction steps
- Attach relevant logs or screenshots

### Code Standards

- Follow PEP 8 coding conventions
- Use Black for code formatting
- Add necessary unit tests

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

You are free to:
- ✅ Commercial use
- ✅ Modify code
- ✅ Distribute copies
- ✅ Private use

The only requirement is to preserve the copyright notice and license copy.

---

<div align="center">

**If this project helps you, please give it a ⭐ Star!**

Made with ❤️ by SOLO Agent

</div>
