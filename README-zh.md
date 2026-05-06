# TaskBar

> 强大的终端任务进度追踪工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 安装

```bash
pip install taskbar-cli
```

## 快速开始

```bash
# 创建新任务
taskbar add "完成项目报告" --priority high --tags work

# 查看所有任务
taskbar list

# 开始处理任务
taskbar start <task_id>

# 更新进度
taskbar progress <task_id> 50

# 完成任务
taskbar complete <task_id>
```

## 文档

完整文档请参阅 [README.md](README.md)。
