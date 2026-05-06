<div align="center">

# 📋 TaskBar

**强大的终端任务进度追踪工具**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**[简体中文](README-zh.md) | [繁體中文](README-zh-TW.md) | [English](README-en.md)**

</div>

---

## 🎉 项目介绍

TaskBar 是一款专为开发者设计的**终端任务进度追踪工具**。它提供了强大的任务管理功能，支持嵌套任务、依赖关系可视化、时间统计和多格式导出，帮助您在终端中高效管理项目进度。

### 💡 设计灵感

在日常开发中，我们经常需要在终端中追踪多个任务的进度。现有的工具要么功能过于简单，要么需要离开终端使用 GUI 应用。TaskBar 应运而生——它将强大的任务管理功能带入您最熟悉的终端环境。

### ✨ 自研差异化亮点

- 🔄 **智能进度追踪** - 自动计算剩余时间，基于历史进度进行智能估算
- 📊 **嵌套任务支持** - 无限层级的子任务，自动汇总进度
- 🔗 **依赖关系管理** - 可视化任务依赖，自动检测循环依赖
- 📈 **实时统计面板** - 终端 TUI 界面，实时显示任务状态
- 📦 **多格式导出** - 支持 JSON、YAML、CSV、Markdown、HTML 五种格式
- ⚡ **零配置启动** - 安装即用，数据自动持久化

---

## ✨ 核心特性

### 📝 任务管理

- ✅ 创建、更新、删除任务
- ✅ 任务状态流转（待办 → 进行中 → 已完成）
- ✅ 优先级设置（低/中/高/紧急）
- ✅ 标签分类系统
- ✅ 截止日期提醒

### 📊 进度追踪

- ✅ 百分比进度显示
- ✅ 步骤计数器
- ✅ 时间统计（已用时间/预估剩余）
- ✅ 进度条可视化

### 🔗 高级功能

- ✅ **嵌套任务** - 无限层级子任务
- ✅ **依赖关系** - 任务间依赖管理
- ✅ **循环检测** - 自动防止循环依赖
- ✅ **数据持久化** - 自动保存到本地

### 📤 导出功能

| 格式 | 用途 |
|------|------|
| JSON | 数据交换、API集成 |
| YAML | 配置文件、版本控制 |
| CSV | Excel导入、数据分析 |
| Markdown | 文档生成、博客发布 |
| HTML | 报告展示、网页发布 |

---

## 🚀 快速开始

### 📋 环境要求

- Python 3.8 或更高版本
- pip 包管理器

### 📥 安装

```bash
# 从 PyPI 安装
pip install taskbar-cli

# 或从源码安装
git clone https://github.com/gitstq/taskbar.git
cd taskbar
pip install -e .
```

### 🎮 基本使用

```bash
# 创建新任务
taskbar add "完成项目报告" --priority high --tags work

# 查看所有任务
taskbar list

# 开始处理任务
taskbar start <task_id>

# 更新进度（百分比）
taskbar progress <task_id> 50

# 按步骤更新进度
taskbar step <task_id> 5

# 查看任务详情
taskbar show <task_id>

# 完成任务
taskbar complete <task_id>

# 导出任务
taskbar export json -o tasks.json
```

---

## 📖 详细使用指南

### 创建任务

```bash
# 基本创建
taskbar add "任务名称"

# 完整参数
taskbar add "重要项目" \
  --description "项目详细描述" \
  --priority high \
  --steps 50 \
  --tags work urgent \
  --due "2026-06-30"
```

### 任务状态管理

```bash
# 开始任务
taskbar start <task_id>

# 暂停任务
taskbar pause <task_id>

# 恢复任务
taskbar resume <task_id>

# 完成任务
taskbar complete <task_id>

# 删除任务
taskbar delete <task_id>
```

### 进度更新

```bash
# 设置百分比进度
taskbar progress <task_id> 75

# 按步骤递增
taskbar step <task_id>      # 默认+1步
taskbar step <task_id> 5    # +5步
```

### 子任务管理

```bash
# 添加子任务
taskbar subtask <parent_id> "子任务名称"

# 子任务会自动计算父任务进度
```

### 依赖关系

```bash
# 添加依赖
taskbar depend <task_id> <depends_on_id>

# 系统会自动检测循环依赖
```

### 查询与筛选

```bash
# 列出所有任务
taskbar list

# 按状态筛选
taskbar list --status in_progress

# 按优先级筛选
taskbar list --priority high

# 按标签筛选
taskbar list --tag work

# 搜索任务
taskbar list --search "关键词"
```

### 数据导出

```bash
# 导出为 JSON
taskbar export json -o tasks.json

# 导出为 Markdown
taskbar export md -o tasks.md

# 导出为 HTML
taskbar export html -o tasks.html

# 导出为 CSV
taskbar export csv -o tasks.csv
```

### 统计信息

```bash
# 查看统计
taskbar stats
```

---

## 💡 设计思路与迭代规划

### 🎯 设计理念

1. **简洁优先** - 命令设计直观，学习成本低
2. **终端原生** - 充分利用终端特性，无需离开命令行
3. **数据安全** - 本地存储，隐私有保障
4. **扩展性强** - 模块化设计，易于扩展新功能

### 🛠 技术选型

| 组件 | 技术 | 原因 |
|------|------|------|
| CLI框架 | Click | 简洁的命令行应用开发 |
| 终端UI | Rich | 美观的终端输出 |
| 数据存储 | JSON | 轻量级、易读、易备份 |
| 打包发布 | setuptools | Python标准打包工具 |

### 📅 迭代规划

**v1.1.0 (计划中)**
- [ ] 交互式 TUI 界面
- [ ] 任务模板功能
- [ ] 番茄钟计时器

**v1.2.0 (计划中)**
- [ ] 团队协作功能
- [ ] 云同步支持
- [ ] Web Dashboard

**v2.0.0 (远期)**
- [ ] 插件系统
- [ ] API 服务
- [ ] 移动端同步

---

## 📦 打包与部署指南

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/gitstq/taskbar.git
cd taskbar

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black src/

# 类型检查
mypy src/
```

### 构建发布

```bash
# 构建 wheel 包
python -m build

# 上传到 PyPI
twine upload dist/*
```

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 提交 PR

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: 添加新功能'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 提交 Issue

- 使用清晰的标题描述问题
- 提供复现步骤
- 附上相关日志或截图

### 代码规范

- 遵循 PEP 8 编码规范
- 使用 Black 进行代码格式化
- 添加必要的单元测试

---

## 📄 开源协议说明

本项目采用 [MIT License](LICENSE) 开源协议。

您可以自由地：
- ✅ 商业使用
- ✅ 修改代码
- ✅ 分发副本
- ✅ 私人使用

唯一要求是保留版权声明和许可证副本。

---

<div align="center">

**如果这个项目对您有帮助，请给一个 ⭐ Star！**

Made with ❤️ by SOLO Agent

</div>
