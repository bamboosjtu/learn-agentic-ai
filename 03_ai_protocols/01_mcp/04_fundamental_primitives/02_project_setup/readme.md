# 项目初始化

让我们先搭好这个基础项目，后续完成 MCP 基础模块时都会基于它来做。这个项目有 3 种不同变体实现，而我们会把 `agents_sdk_cli_project` 作为基线项目。

## MCP Chat - Agents SDK CLI 项目

MCP Chat 是一个命令行界面应用。它支持文档检索、基于命令的提示词调用，以及通过 MCP（Model Control Protocol）架构进行可扩展的工具集成。

## 前置要求

- Python 3.9+
- 任意支持 Chat Completions 的 LLM API Key 和提供商，例如 Gemini

## 环境搭建

### 第 1 步：配置环境变量

1. 在项目根目录创建或编辑 `.env` 文件，并确认以下变量已正确设置：

```env
LLM_API_KEY=""  # 填入你的 GEMINI API 密钥
LLM_CHAT_COMPLETION_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
LLM_MODEL="gemini-2.0-flash"
```

### 第 2 步：安装依赖

[uv](https://github.com/astral-sh/uv) 是一个快速的 Python 包安装与解析工具。

1. 如果还没安装 `uv`，先执行：

```bash
pip install uv
```

2. 创建并激活虚拟环境：

```bash
uv venv
source .venv/bin/activate  # Windows 下使用: .venv\\Scripts\\activate
```

3. 安装依赖：

```bash
uv sync
```

4. 启动 MCP Server：

```bash
uv run uvicorn mcp_server:mcp_app --reload
```

5. 在 CLI 中运行带 ChatAgent 的项目：

```bash
uv run main.py
```

6. 可选：启动 Inspector

```bash
npx @modelcontextprotocol/inspector
```

## 使用方式

### 基础交互

直接输入消息并按回车，即可与模型对话。

### 文档检索

使用 `@` 符号加文档 ID，把文档内容加入你的提问中：

```text
> Tell me about @deposition.md
```

### 命令

使用 `/` 前缀执行在 MCP Server 中定义的命令：

```text
> /summarize deposition.md
```

按 `Tab` 键时，这些命令会自动补全。

## 开发说明

### 添加新文档

编辑 `mcp_server.py` 文件，把新文档加入 `docs` 字典。

### 实现 MCP 功能

要完整实现 MCP 功能，你需要：

1. 完成 `mcp_server.py` 中的 TODO
2. 实现 `mcp_client.py` 中缺失的功能

### Lint 与类型检查

当前项目还没有配置 lint 或类型检查。
