# Houdini AI Agent

## 项目简介

本项目为硕士毕业设计，探索利用大语言模型辅助 Houdini 程序化建模（PCG）。

整体思路采用**大模型理解、本地模型执行**的架构：

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

## 当前已完成

- 部署本地 `llama.cpp` 推理环境
- 成功运行 `Qwen2.5-Coder-7B`
- Python 调用 OpenAI Compatible API
- Houdini 成功调用本地模型
- 模型生成 Houdini Python 并自动执行
- 建立 Prompt 文件管理
- 开始建立 Houdini Benchmark（Box、Connection、Parameters、Copy to Points）

---

## 当前项目结构

```
python/
    houdini_run_llm.py
    test_llm_request.py

prompts/

scripts/

docs/
```

---

## 下一步计划

- 测试不同模型（Qwen3、DeepSeek 等）
- 调研传统 PCG 建筑生成流程
- 设计适合 Houdini 的 Skill 架构
- 探索 RAG / LoRA 对 Houdini 代码生成的提升效果

---

## 当前研究重点

目前主要回答以下几个问题：

- Prompt Engineering 对生成质量的影响？
- 大模型负责理解，本地模型负责执行是否可行？
- 如何将 LLM 与传统 PCG 工作流结合？