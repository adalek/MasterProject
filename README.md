# Houdini AI Agent

[English](README.md) | [中文](README_CN.md)

## Overview

Houdini AI Agent is an MSc dissertation project exploring the use of Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) for procedural content generation in Houdini.

Users can enter natural-language modelling requests through a PySide6 GUI inside Houdini, select a local or cloud model, and enable or disable RAG.

The generated Houdini Python code is displayed in the GUI for review before being manually executed to create SOP networks.

## Current Features

- Houdini PySide6 GUI
- Natural-language prompt input
- Local Qwen / cloud DeepSeek model selection
- RAG on/off control
- ChromaDB vector retrieval
- Retrieved source and distance display
- Houdini Python code generation
- Generated code preview
- Separate Generate and Execute steps
- Basic unsafe-code keyword filtering
- FastAPI RAG server
- OpenAI-compatible Chat Completions API

---

## Architecture

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

Houdini and the RAG service run in separate Python environments:

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

This avoids installing the RAG dependencies directly into Houdini's Python environment.

---

## Project Structure

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

## Tested Environment

The current version was mainly developed and tested in the university Lab Linux environment.

```text
OS: Linux
Houdini: 21.0.596
Houdini Python: 3.11.7

Local Model:
Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf

Local Inference:
llama.cpp

Cloud Model:
DeepSeek
```

Python dependencies are managed with `uv`.

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd MasterProject
```

### 2. Install Python Dependencies

```bash
uv sync
```

The Python environment is created according to `pyproject.toml` and `uv.lock`.

---

## Configuration

### Project Path

The current Lab Linux development path is:

```text
/home/s5803453/Desktop/MasterProject
```

If the repository is located elsewhere, update `PROJECT_ROOT` in the Houdini Shelf Tool:

```python
PROJECT_ROOT = "/home/user/projects/MasterProject"
```

### Environment Variables

Model configuration is stored in `.env` at the project root.

Create it from:

```bash
cp .env.example .env
```

Example:

```env
MODEL_PROVIDER=local

LOCAL_API_URL=http://127.0.0.1:8080/v1/chat/completions
LOCAL_API_KEY=12345
LOCAL_MODEL=Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf

DEEPSEEK_API_URL=https://api.deepseek.com/chat/completions
DEEPSEEK_API_KEY=
DEEPSEEK_MODEL=deepseek-v4-flash
```

Do not commit `.env` or API keys to Git.

---

## Running the Project

The current system consists of three main components:

```text
1. Local Model Server (optional)
2. RAG Server
3. Houdini GUI
```

### 1. Start the Local Model

When using Local Qwen:

```bash
./scripts/start_qwen.sh
```

Default endpoint:

```text
http://127.0.0.1:8080/v1/chat/completions
```

The local model server is not required when using DeepSeek only.

> The local llama.cpp executable and model paths may depend on the Lab Linux environment. Check `scripts/start_qwen.sh` and update any environment-specific paths when running on another machine.

### 2. Build / Rebuild the RAG Database

After modifying knowledge files:

```bash
./scripts/rebuild_rag.sh
```

A rebuild is normally required after:

- adding knowledge documents
- removing knowledge documents
- editing knowledge content
- changing chunking or embedding configuration

Changes to the GUI or user prompts do not require rebuilding the vector database.

### 3. Start the RAG Server

```bash
./scripts/start_rag.sh
```

Default address:

```text
http://127.0.0.1:8000
```

Health endpoint:

```text
GET /health
```

Generation endpoint:

```text
POST /generate
```

Example request:

```json
{
    "prompt": "Create a spiral staircase",
    "top_k": 1,
    "provider": "deepseek",
    "rag_enabled": true
}
```

Example response:

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

## Houdini Setup

Create a Shelf Tool in Houdini and use the following script:

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

Update `PROJECT_ROOT` if the repository is stored in another location.

Click the Shelf Tool to open the Houdini AI Agent GUI.

---

## Usage

### 1. Enter a Prompt

For example:

```text
Create a spiral staircase
```

or:

```text
Create a parameterized staircase with 15 steps
```

### 2. Select a Model

Currently supported:

```text
Local Qwen
DeepSeek
```

`Local Qwen` uses the local llama.cpp server.

`DeepSeek` uses the configured cloud API.

### 3. Enable or Disable RAG

With RAG enabled:

```text
User Prompt
→ Retrieval
→ Retrieved Knowledge
→ Prompt Builder
→ LLM
```

With RAG disabled:

```text
User Prompt
→ LLM
```

### 4. Generate

Click `Generate`.

The Houdini GUI sends an HTTP request to the FastAPI `/generate` endpoint.

The result is displayed as:

- Retrieved Knowledge
- Generated Code

### 5. Execute

Review the generated Python code and click `Execute`.

The code is then executed inside Houdini's Python environment.

Generation and execution are intentionally separated so generated code is not automatically executed.

---

## Configurable Parameters

| Parameter | Default | Location | Description |
|---|---:|---|---|
| `top_k` | `1` | `src/ui.py` | Number of RAG results |
| `temperature` | `0.1` | `src/ask_model.py` | Model sampling temperature |
| `max_tokens` | `10000` | `src/ask_model.py` | Maximum completion-token budget |
| RAG Server | `127.0.0.1:8000` | `src/ui.py` | FastAPI server address |
| Local API | `127.0.0.1:8080` | `.env` | llama.cpp API endpoint |
| `LOCAL_MODEL` | Qwen2.5-Coder-7B | `.env` | Local model |
| `DEEPSEEK_MODEL` | `deepseek-v4-flash` | `.env` | Cloud model |

A larger `top_k` retrieves more knowledge but increases context size and may introduce less relevant information.

A low temperature is currently used to improve code-generation consistency.

---

## RAG Knowledge Base

Knowledge files are stored under:

```text
knowledge/
```

Current pipeline:

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

Each retrieved document contains:

```text
content
source
distance
```

A smaller distance generally represents higher semantic similarity.

---

## Development Notes

Restart the RAG server after modifying server-side files such as:

```text
src/rag_server.py
src/ask_model.py
src/generate.py
src/generate_with_rag.py
rag/*.py
```

After modifying:

```text
src/ui.py
```

the Shelf Tool uses:

```python
importlib.reload(src.ui)
```

to reload the GUI, so restarting Houdini is normally unnecessary.

After modifying files under `knowledge/`, rebuild the RAG database:

```bash
./scripts/rebuild_rag.sh
```

---

## Safety

Generation and execution are separated:

```text
Generate
→ Preview
→ Execute
```

Basic keyword checks are applied before execution, including terms such as:

```text
subprocess
os.system
shutil
deleteItems
```

This is a prototype safety mechanism and should not be considered a complete Python sandbox.

---

## Current Limitations

- The local 7B model is less reliable for complex Houdini networks.
- RAG performance depends strongly on knowledge quality, chunking, and retrieval queries.
- API keys are currently managed through `.env`.
- Advanced parameters such as `top_k` are not fully exposed in the GUI.
- Generated Python is ultimately executed with `exec()`.
- The current prototype has mainly been tested on Lab Linux with Houdini 21.
- Some local llama.cpp/model paths may be specific to the Lab environment.

---

## Current Status

The current version provides a complete MVP workflow:

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