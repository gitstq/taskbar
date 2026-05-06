<div align="center">

# 📋 TaskBar

**強大的終端任務進度追蹤工具**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**[简体中文](README-zh.md) | [繁體中文](README-zh-TW.md) | [English](README-en.md)**

</div>

---

## 🎉 專案介紹

TaskBar 是一款專為開發者設計的**終端任務進度追蹤工具**。它提供了強大的任務管理功能，支援巢狀任務、依賴關係視覺化、時間統計和多格式匯出，幫助您在終端中高效管理專案進度。

### 💡 設計靈感

在日常開發中，我們經常需要在終端中追蹤多個任務的進度。現有的工具要麼功能過於簡單，要麼需要離開終端使用 GUI 應用程式。TaskBar 應運而生——它將強大的任務管理功能帶入您最熟悉的終端環境。

### ✨ 自研差異化亮點

- 🔄 **智慧進度追蹤** - 自動計算剩餘時間，基於歷史進度進行智慧估算
- 📊 **巢狀任務支援** - 無限層級的子任務，自動彙總進度
- 🔗 **依賴關係管理** - 視覺化任務依賴，自動檢測循環依賴
- 📈 **即時統計面板** - 終端 TUI 介面，即時顯示任務狀態
- 📦 **多格式匯出** - 支援 JSON、YAML、CSV、Markdown、HTML 五種格式
- ⚡ **零配置啟動** - 安裝即用，資料自動持久化

---

## ✨ 核心特性

### 📝 任務管理

- ✅ 建立、更新、刪除任務
- ✅ 任務狀態流轉（待辦 → 進行中 → 已完成）
- ✅ 優先級設定（低/中/高/緊急）
- ✅ 標籤分類系統
- ✅ 截止日期提醒

### 📊 進度追蹤

- ✅ 百分比進度顯示
- ✅ 步驟計數器
- ✅ 時間統計（已用時間/預估剩餘）
- ✅ 進度條視覺化

### 🔗 進階功能

- ✅ **巢狀任務** - 無限層級子任務
- ✅ **依賴關係** - 任務間依賴管理
- ✅ **循環檢測** - 自動防止循環依賴
- ✅ **資料持久化** - 自動儲存到本地

### 📤 匯出功能

| 格式 | 用途 |
|------|------|
| JSON | 資料交換、API整合 |
| YAML | 設定檔、版本控制 |
| CSV | Excel匯入、資料分析 |
| Markdown | 文件生成、部落格發布 |
| HTML | 報告展示、網頁發布 |

---

## 🚀 快速開始

### 📋 環境要求

- Python 3.8 或更高版本
- pip 套件管理器

### 📥 安裝

```bash
# 從 PyPI 安裝
pip install taskbar-cli

# 或從原始碼安裝
git clone https://github.com/gitstq/taskbar.git
cd taskbar
pip install -e .
```

### 🎮 基本使用

```bash
# 建立新任務
taskbar add "完成專案報告" --priority high --tags work

# 查看所有任務
taskbar list

# 開始處理任務
taskbar start <task_id>

# 更新進度（百分比）
taskbar progress <task_id> 50

# 按步驟更新進度
taskbar step <task_id> 5

# 查看任務詳情
taskbar show <task_id>

# 完成任務
taskbar complete <task_id>

# 匯出任務
taskbar export json -o tasks.json
```

---

## 📖 詳細使用指南

### 建立任務

```bash
# 基本建立
taskbar add "任務名稱"

# 完整參數
taskbar add "重要專案" \
  --description "專案詳細描述" \
  --priority high \
  --steps 50 \
  --tags work urgent \
  --due "2026-06-30"
```

### 任務狀態管理

```bash
# 開始任務
taskbar start <task_id>

# 暫停任務
taskbar pause <task_id>

# 恢復任務
taskbar resume <task_id>

# 完成任務
taskbar complete <task_id>

# 刪除任務
taskbar delete <task_id>
```

### 進度更新

```bash
# 設定百分比進度
taskbar progress <task_id> 75

# 按步驟遞增
taskbar step <task_id>      # 預設+1步
taskbar step <task_id> 5    # +5步
```

### 子任務管理

```bash
# 新增子任務
taskbar subtask <parent_id> "子任務名稱"

# 子任務會自動計算父任務進度
```

### 依賴關係

```bash
# 新增依賴
taskbar depend <task_id> <depends_on_id>

# 系統會自動檢測循環依賴
```

### 查詢與篩選

```bash
# 列出所有任務
taskbar list

# 按狀態篩選
taskbar list --status in_progress

# 按優先級篩選
taskbar list --priority high

# 按標籤篩選
taskbar list --tag work

# 搜尋任務
taskbar list --search "關鍵詞"
```

### 資料匯出

```bash
# 匯出為 JSON
taskbar export json -o tasks.json

# 匯出為 Markdown
taskbar export md -o tasks.md

# 匯出為 HTML
taskbar export html -o tasks.html

# 匯出為 CSV
taskbar export csv -o tasks.csv
```

### 統計資訊

```bash
# 查看統計
taskbar stats
```

---

## 💡 設計思路與迭代規劃

### 🎯 設計理念

1. **簡潔優先** - 命令設計直觀，學習成本低
2. **終端原生** - 充分利用終端特性，無需離開命令列
3. **資料安全** - 本地儲存，隱私有保障
4. **擴展性強** - 模組化設計，易於擴展新功能

### 🛠 技術選型

| 元件 | 技術 | 原因 |
|------|------|------|
| CLI框架 | Click | 簡潔的命令列應用開發 |
| 終端UI | Rich | 美觀的終端輸出 |
| 資料儲存 | JSON | 輕量級、易讀、易備份 |
| 打包發布 | setuptools | Python標準打包工具 |

### 📅 迭代規劃

**v1.1.0 (計劃中)**
- [ ] 互動式 TUI 介面
- [ ] 任務範本功能
- [ ] 番茄鐘計時器

**v1.2.0 (計劃中)**
- [ ] 團隊協作功能
- [ ] 雲端同步支援
- [ ] Web Dashboard

**v2.0.0 (遠期)**
- [ ] 外掛系統
- [ ] API 服務
- [ ] 行動端同步

---

## 📦 打包與部署指南

### 本地開發

```bash
# 複製儲存庫
git clone https://github.com/gitstq/taskbar.git
cd taskbar

# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安裝開發依賴
pip install -e ".[dev]"

# 執行測試
pytest

# 程式碼格式化
black src/

# 類型檢查
mypy src/
```

### 建置發布

```bash
# 建置 wheel 套件
python -m build

# 上傳到 PyPI
twine upload dist/*
```

---

## 🤝 貢獻指南

我們歡迎所有形式的貢獻！

### 提交 PR

1. Fork 本儲存庫
2. 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -m 'feat: 新增新功能'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 建立 Pull Request

### 提交 Issue

- 使用清晰的標題描述問題
- 提供重現步驟
- 附上相關日誌或截圖

### 程式碼規範

- 遵循 PEP 8 編碼規範
- 使用 Black 進行程式碼格式化
- 添加必要的單元測試

---

## 📄 開源協議說明

本專案採用 [MIT License](LICENSE) 開源協議。

您可以自由地：
- ✅ 商業使用
- ✅ 修改程式碼
- ✅ 分發副本
- ✅ 私人使用

唯一要求是保留版權聲明和許可證副本。

---

<div align="center">

**如果這個專案對您有幫助，請給一個 ⭐ Star！**

Made with ❤️ by SOLO Agent

</div>
