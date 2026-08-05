# Houdini AI Agent

## 项目简介

本项目为硕士毕业设计，探索利用大语言模型（LLM）辅助 Houdini 程序化建模（PCG）。

项目目标是在 Houdini 中构建一个 AI Agent，使用户能够通过自然语言生成可执行的 Houdini Python 代码，并自动完成节点创建、连接与参数设置。同时探索 RAG（Retrieval-Augmented Generation）在专业领域代码生成中的应用，以及本地模型与云端模型在 Houdini 建模任务中的能力差异。

---


```
用户自然语言
        │
        ▼
大模型（理解设计意图）
        │
        ▼
本地代码模型（生成 Houdini Python）
        │
        ▼
Houdini 执行代码
        │
        ▼
生成程序化模型
```

目标是在保证生成质量的同时，实现本地、可控的 AI 建模工作流。

---


## 当前架构

```
自然语言 Prompt
        │
        ▼
 Prompt Builder
        │
        ▼
   RAG 检索知识库
        │
        ▼
  构建完整 Prompt
        │
        ▼
LLM（本地 / 云端）
        │
        ▼
生成 Houdini Python
        │
        ▼
代码清洗（Clean Code）
        │
        ▼
Houdini 自动执行
        │
        ▼
生成程序化模型
```

---

## 已实现功能

- 部署本地 `llama.cpp` 推理环境
- 成功运行 `Qwen2.5-Coder-7B`
- 支持 OpenAI Compatible API 调用
- Houdini 自动调用本地模型
- 自动生成并执行 Houdini Python
- Prompt 文件管理
- RAG 知识检索（ChromaDB）
- FastAPI RAG Server
- 本地模型与云端模型切换
- 初步建立 Benchmark 测试流程

---

## 项目结构

```
src/
│
├── ask_model.py              # 模型调用
├── generate.py               # 普通生成
├── generate_with_rag.py      # RAG 生成
├── clean_code.py             # 清洗模型输出
├── houdini_run_llm.py        # Houdini 执行入口
└── rag_server.py             # FastAPI 服务

rag/
│
├── ingest.py                 # 构建向量数据库
├── retrieve.py               # 检索知识
├── prompt_builder.py         # 构建 Prompt
└── config.py

knowledge/                    # RAG 知识库
prompts/                      # Benchmark Prompt
scripts/                      # 启动脚本
docs/                         # 开发记录
```

---

## 当前 Benchmark

目前已完成或正在测试：

- Box
- Node Connection
- Parameters
- Copy to Points
- Staircase
- Spiral Staircase（进行中）

每个 Benchmark 包括：

- Prompt
- RAG 检索结果
- 模型输出
- Houdini 执行结果
- 错误分析

---

## 当前研究内容

目前主要围绕以下几个方向开展实验：

- Prompt Engineering 对生成质量的影响
- RAG 对 Houdini Python 生成的提升效果
- Rule、Pattern、Example 三类知识组织方式
- 本地模型与云端模型的能力对比
- Houdini Python 自动执行与错误分析
- AI Agent 在程序化建模工作流中的应用

---

## 技术栈

- Python
- Houdini HOM API
- llama.cpp
- FastAPI
- ChromaDB
- Sentence Transformers
- OpenAI Compatible API
- uv

---

## 下一步计划

- 完善 RAG 知识库
- 增加更多 Benchmark 场景
- 建立量化评测指标
- 研究不同知识类型（Rule / Pattern / Example）对生成质量的影响
- 对比更多本地模型与云端模型
- 设计 Houdini Skill 架构