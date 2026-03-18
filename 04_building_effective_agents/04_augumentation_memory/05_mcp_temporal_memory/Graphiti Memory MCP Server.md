# [Graphiti Memory MCP Server](https://github.com/getzep/graphiti/tree/main/mcp_server)

> 这是从原始 Graphiti Server 派生出来的版本，目标是基于符合最新 MCP 规范的无状态可流式 HTTP Transport，构建一个可扩展的远程服务端。

Graphiti 是一个用于构建和查询“具备时间感知能力的知识图谱”的框架，特别适合运行在动态环境中的 AI Agent。与传统的检索增强生成（RAG）方式不同，Graphiti 会持续把用户交互、企业中的结构化与非结构化数据，以及外部信息整合进一个连贯、可查询的图结构中。

这个框架支持增量式数据更新、高效检索以及精确的历史查询，而不需要每次都对整张图重新计算，因此非常适合构建交互式、具备上下文感知能力的 AI 应用。

这是 Graphiti 的一个实验性 Model Context Protocol（MCP）Server 实现。它通过 MCP 协议暴露出 Graphiti 的核心能力，使 AI 助手能够直接调用 Graphiti 的知识图谱功能。

## 功能特性

Graphiti MCP Server 暴露了 Graphiti 的以下高层能力：

- **Episode 管理**：添加、读取和删除 episodes（支持文本、消息和 JSON 数据）
- **实体管理**：搜索并管理知识图谱中的实体节点和关系
- **搜索能力**：通过语义搜索和混合搜索查找 facts（边）和节点摘要
- **分组管理**：通过 `group_id` 过滤，组织和管理相关数据分组
- **图维护**：清空图数据并重建索引

## 快速开始

### 克隆 GitHub 仓库

```bash
git clone ...
```

1. 进入 `mcp_server` 目录：

```bash
cd mcp_server
```

## 安装

### 前置要求

1. 确保已安装 Python 3.10 或更高版本
2. 一个正在运行的 Neo4j 数据库（要求版本 5.26 或更高）
3. 用于 LLM 相关操作的 OpenAI API Key

### 安装步骤

1. 克隆仓库并进入 `mcp_server` 目录
2. 使用 `uv` 创建虚拟环境并安装依赖：

```bash
# 如果还没装 uv，先安装
curl -LsSf https://astral.sh/uv/install.sh | sh

# 一步完成虚拟环境创建和依赖安装
uv sync
```

## 配置

服务端会使用以下环境变量：

- `NEO4J_URI`：Neo4j 数据库 URI，默认值：`bolt://localhost:7687`
- `NEO4J_USER`：Neo4j 用户名，默认值：`neo4j`
- `NEO4J_PASSWORD`：Neo4j 密码，默认值：`demodemo`
- `OPENAI_API_KEY`：OpenAI API Key，用于 LLM 操作
- `OPENAI_BASE_URL`：可选，用于指定 OpenAI API 的基础地址
- `MODEL_NAME`：用于主要 LLM 操作的 OpenAI 模型名
- `SMALL_MODEL_NAME`：用于较小型 LLM 操作的 OpenAI 模型名
- `LLM_TEMPERATURE`：LLM 响应温度，范围 `0.0-2.0`
- `SEMAPHORE_LIMIT`：episode 处理的并发上限。详见下文 [并发与 LLM 提供商 429 限流错误](#并发与-llm-提供商-429-限流错误)

你可以把这些变量写到项目目录下的 `.env` 文件中。

## 运行服务端

使用 `uv` 直接启动 Graphiti MCP Server：

```bash
uv run server.py
```

### 并发与 LLM 提供商 429 限流错误

Graphiti 的数据摄取流水线是为高并发设计的，并发量由环境变量 `SEMAPHORE_LIMIT` 控制。

默认情况下，`SEMAPHORE_LIMIT` 设为 `10`，也就是最多并发 10 个操作，以尽量降低从 LLM 提供商处收到 `429` 限流错误的概率。如果你遇到这类错误，可以尝试降低这个值。

如果你的 LLM 提供商允许更高吞吐量，也可以适当提高 `SEMAPHORE_LIMIT`，以提升 episode 摄取性能。

## 与 MCP Client 集成

### 配置

如果要在支持 MCP 的客户端中使用 Graphiti MCP Server，需要在客户端里配置连接到该服务端。

## 可用工具

Graphiti MCP Server 提供以下工具：

- `add_episode`：向知识图谱中添加 episode，支持文本、JSON 和消息格式
- `search_nodes`：在知识图谱中搜索相关节点摘要
- `search_facts`：在知识图谱中搜索相关 facts，也就是实体之间的边
- `delete_entity_edge`：删除知识图谱中的某条实体关系边
- `delete_episode`：删除知识图谱中的某条 episode
- `get_entity_edge`：通过 UUID 获取某条实体关系边
- `get_episodes`：获取某个分组最近的 episodes
- `clear_graph`：清空知识图谱中的所有数据并重建索引
- `get_status`：获取 Graphiti MCP Server 和 Neo4j 连接状态

## 处理 JSON 数据

Graphiti MCP Server 可以通过 `add_episode` 工具处理结构化 JSON 数据，只需传入 `source="json"`。这样系统就能自动从结构化数据中抽取实体和关系。

示例：

```

add_episode(
name="Customer Profile",
episode_body="{\"company\": {\"name\": \"Acme Technologies\"}, \"products\": [{\"id\": \"P001\", \"name\": \"CloudSync\"}, {\"id\": \"P002\", \"name\": \"DataMiner\"}]}",
source="json",
source_description="CRM data"
)

```

## 与 Coding IDE 集成

## 遥测（Telemetry）

Graphiti MCP Server 底层使用的是 Graphiti Core Library，而该核心库默认会进行匿名遥测统计。当你初始化 Graphiti MCP Server 时，系统会收集匿名使用统计，用于帮助改进这个框架。

### 会收集什么

- 匿名标识符和系统信息，例如操作系统、Python 版本
- Graphiti 的版本信息与配置选择，例如使用的 LLM 提供商、数据库后端、embedder 类型
- **不会收集任何个人数据、API Key，也不会收集实际图数据内容**

### 如何关闭

如果你想关闭 MCP Server 中的遥测功能，可以设置以下环境变量：

```bash
export GRAPHITI_TELEMETRY_ENABLED=false
```

或者把它写到 `.env` 文件里：

```env
GRAPHITI_TELEMETRY_ENABLED=false
```

## 许可证

本项目使用与上游 Graphiti 项目相同的许可证。
