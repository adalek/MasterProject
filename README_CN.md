# Houdini AI Agent

[English](README.md) | [中文](README_CN.md)

## 项目简介

Houdini AI Agent 是一个硕士毕业设计项目，探索利用大语言模型（LLM）与 RAG（Retrieval-Augmented Generation）辅助 Houdini 程序化建模。

用户可以直接在 Houdini 内的 PySide6 GUI 中输入自然语言建模需求，选择本地或云端模型，并决定是否启用 RAG。

系统生成 Houdini Python 代码后，会先在 GUI 中显示代码，再由用户确认并手动执行，在 Houdini 中创建对应的 SOP 节点网络。

## 当前功能

- Houdini PySide6 GUI
- 自然语言 Prompt 输入
- 本地 Qwen / 云端 DeepSeek 模型切换
- RAG 开启 / 关闭
- ChromaDB 向量知识库检索
- 显示 Retrieved Knowledge 及 distance
- Houdini Python 代码生成
- Generated Code Preview
- Generate 与 Execute 分离
- 基础危险代码关键词过滤
- FastAPI RAG Server
- OpenAI-compatible Chat Completions API

---

## 系统架构

```text
Houdini PySide GUI
        │
        │ HTTP POST /generate
        ▼
FastAPI RAG Server
        │
        ├── RAG ON
        │      ├── ChromaDB Retrieval
        │      ├── Prompt Builder
        │      └── LLM
        │
        └── RAG OFF
               └── LLM
                    │
             ┌──────┴──────┐
             ▼             ▼
        Local Qwen      DeepSeek API
        llama.cpp          Cloud
             │             │
             └──────┬──────┘
                    ▼
             Houdini Python
                    │
                    ▼
               GUI Preview
                    │
               User Execute
                    │
                    ▼
            Houdini SOP Network
```

Houdini 与 RAG 服务运行在两个独立的 Python 环境中：

```text
Houdini Python 3.11
        │
        │ HTTP
        ▼
Project Python Environment
        ├── FastAPI
        ├── ChromaDB
        ├── Sentence Transformers
        └── Model API
```

这样可以避免直接在 Houdini Python 环境中安装 RAG 相关依赖。

---

## 项目结构

```text
MasterProject/
│
├── src/
│   ├── ui.py
│   ├── rag_server.py
│   ├── ask_model.py
│   ├── generate.py
│   ├── generate_with_rag.py
│   └── clean_code.py
│
├── rag/
│   ├── config.py
│   ├── ingest.py
│   ├── retrieve.py
│   └── prompt_builder.py
│
├── knowledge/
├── prompts/
├── scripts/
│   ├── start_qwen.sh
│   ├── start_rag.sh
│   └── rebuild_rag.sh
│
├── docs/
├── pyproject.toml
├── uv.lock
├── .env.example
├── README.md
└── README_CN.md
```

---

## 测试环境

当前版本主要在学校 Lab Linux 环境中开发与测试。

```text
OS: Linux
Houdini: 21.0.596
Houdini Python: 3.11.7

本地模型:
Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf

本地推理:
llama.cpp

云端模型:
DeepSeek
```

Python 项目依赖由 `uv` 管理。

---

## 安装

### 1. Clone 项目

```bash
git clone <repository-url>
cd MasterProject
```

### 2. 安装 Python 依赖

```bash
uv sync
```

项目会根据 `pyproject.toml` 与 `uv.lock` 创建对应的 Python 环境。

---

## 配置

### 项目路径

当前 Lab Linux 开发路径为：

```text
/home/s5803453/Desktop/MasterProject
```

如果项目位于其他位置，需要修改 Houdini Shelf Tool 中的：

```python
PROJECT_ROOT = "/home/user/projects/MasterProject"
```

### 环境变量

项目根目录使用 `.env` 保存模型相关配置。

建议从模板创建：

```bash
cp .env.example .env
```

示例：

```env
MODEL_PROVIDER=local

LOCAL_API_URL=http://127.0.0.1:8080/v1/chat/completions
LOCAL_API_KEY=12345
LOCAL_MODEL=Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf

DEEPSEEK_API_URL=https://api.deepseek.com/chat/completions
DEEPSEEK_API_KEY=
DEEPSEEK_MODEL=deepseek-v4-flash
```

不要将 `.env` 或真实 API Key 提交到 Git。

---

## 运行项目

当前系统主要包含三个部分：

```text
1. Local Model Server（可选）
2. RAG Server
3. Houdini GUI
```

### 1. 启动本地模型

使用 Local Qwen 时：

```bash
./scripts/start_qwen.sh
```

默认接口：

```text
http://127.0.0.1:8080/v1/chat/completions
```

如果只使用 DeepSeek，则不需要启动本地模型 Server。

> 本地 llama.cpp 可执行文件和模型文件路径可能依赖 Lab Linux 环境。如果在其他机器运行，请检查 `scripts/start_qwen.sh` 中是否存在需要修改的环境相关路径。

### 2. 构建 / 重建 RAG 数据库

修改 `knowledge/` 中的知识文档后：

```bash
./scripts/rebuild_rag.sh
```

以下情况通常需要重新构建：

- 新增知识文档
- 删除知识文档
- 修改知识文档内容
- 修改 chunking 或 embedding 配置

单纯修改 GUI 或用户 Prompt 不需要重新构建向量数据库。

### 3. 启动 RAG Server

```bash
./scripts/start_rag.sh
```

默认地址：

```text
http://127.0.0.1:8000
```

Health Check：

```text
GET /health
```

代码生成接口：

```text
POST /generate
```

请求示例：

```json
{
    "prompt": "Create a spiral staircase",
    "top_k": 1,
    "provider": "deepseek",
    "rag_enabled": true
}
```

返回示例：

```json
{
    "code": "import hou\n...",
    "retrieved_sources": [
        {
            "source": "spiral_core.md",
            "distance": 0.2631
        }
    ]
}
```

---

## Houdini 设置

在 Houdini 中创建一个 Shelf Tool，并使用以下脚本：

```python
import sys
import importlib

PROJECT_ROOT = "/home/s5803453/Desktop/MasterProject"

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import src.ui
importlib.reload(src.ui)

src.ui.show_window()
```

如果项目路径不同，请修改 `PROJECT_ROOT`。

点击 Shelf Tool 即可打开 Houdini AI Agent GUI。

---

## 使用方法

### 1. 输入 Prompt

例如：

```text
Create a spiral staircase
```

或者：

```text
Create a parameterized staircase with 15 steps
```

### 2. 选择模型

当前支持：

```text
Local Qwen
DeepSeek
```

`Local Qwen` 使用本地 llama.cpp Server。

`DeepSeek` 使用 `.env` 中配置的云端 API。

### 3. 开启或关闭 RAG

RAG 开启：

```text
User Prompt
→ Retrieval
→ Retrieved Knowledge
→ Prompt Builder
→ LLM
```

RAG 关闭：

```text
User Prompt
→ LLM
```

### 4. Generate

点击 `Generate` 后，Houdini GUI 会向 FastAPI `/generate` 接口发送 HTTP 请求。

生成完成后 GUI 会显示：

- Retrieved Knowledge
- Generated Code

### 5. Execute

检查生成的 Python 代码后点击 `Execute`。

代码将在 Houdini Python 环境中执行并创建对应的节点网络。

Generate 与 Execute 被刻意拆分为两个步骤，因此模型生成的代码不会自动执行。

---

## 可修改参数

| 参数 | 当前默认值 | 位置 | 作用 |
|---|---:|---|---|
| `top_k` | `1` | `src/ui.py` | RAG 检索结果数量 |
| `temperature` | `0.1` | `src/ask_model.py` | 模型采样温度 |
| `max_tokens` | `10000` | `src/ask_model.py` | 最大 completion token 数 |
| RAG Server | `127.0.0.1:8000` | `src/ui.py` | FastAPI Server 地址 |
| Local API | `127.0.0.1:8080` | `.env` | llama.cpp API 地址 |
| `LOCAL_MODEL` | Qwen2.5-Coder-7B | `.env` | 本地模型 |
| `DEEPSEEK_MODEL` | `deepseek-v4-flash` | `.env` | 云端模型 |

较大的 `top_k` 会检索更多知识，但同时增加 Context，并可能引入相关性较低的内容。

当前使用较低的 temperature，以提高代码生成的稳定性。

---

## RAG 知识库

RAG 知识文件位于：

```text
knowledge/
```

当前流程：

```text
knowledge/*.md
      ↓
rag/ingest.py
      ↓
Embedding Model
      ↓
ChromaDB
      ↓
rag/retrieve.py
```

每个检索结果包含：

```text
content
source
distance
```

较小的 distance 通常表示更高的语义相似度。

---

## 开发说明

修改以下 Server 相关文件后，通常需要重启 RAG Server：

```text
src/rag_server.py
src/ask_model.py
src/generate.py
src/generate_with_rag.py
rag/*.py
```

修改：

```text
src/ui.py
```

后，Shelf Tool 会通过：

```python
importlib.reload(src.ui)
```

重新加载 GUI，因此通常不需要重启 Houdini。

修改 `knowledge/` 后，需要：

```bash
./scripts/rebuild_rag.sh
```

重新构建向量数据库。

---

## 安全设计

生成与执行被拆成两个步骤：

```text
Generate
→ Preview
→ Execute
```

执行前还会进行基础危险关键词检查，例如：

```text
subprocess
os.system
shutil
deleteItems
```

当前机制仅用于研究原型，不应被视为完整的 Python sandbox。

---

## 当前限制

- 本地 7B 模型处理复杂 Houdini 节点网络时稳定性有限。
- RAG 效果高度依赖知识文档质量、chunking 与检索 query。
- API Key 当前通过 `.env` 管理。
- `top_k` 等高级参数暂未完全暴露到 GUI。
- Generated Python 最终仍通过 `exec()` 执行。
- 当前版本主要在 Lab Linux + Houdini 21 环境测试。
- 部分 llama.cpp 与模型路径可能依赖学校 Lab 环境。

---

## 当前状态

当前版本已经完成最小可用闭环：

```text
Natural Language
      ↓
Houdini GUI
      ↓
Local / Cloud LLM
      ↓
Optional RAG
      ↓
Houdini Python
      ↓
Code Preview
      ↓
User Execute
      ↓
SOP Network
```