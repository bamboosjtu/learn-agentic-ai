# 04：连接多个 MCP Server 的 Agent

**目标：** 学习如何配置一个 OpenAI Agent，使其能够同时连接并使用多个 MCP 服务器上的工具。

### 🧪 这一模块在实践中覆盖什么

本子模块提供：

- 可运行的多 MCP 集成 Python 脚本
- 模拟或 mock 的 MCP server 配置
- 一个能和这些服务器上托管工具交互的 agent
- 关于错误处理、server 隔离和扩展性的说明

[示例 Trace](https://smith.langchain.com/public/1a4bfa57-791d-4b8c-97da-bf0fbdf3b874/r)：这里两个工具分别位于不同服务器上，由使用 OpenAI Agents SDK 创建的一个 Agent 统一调用。

---

### 🧠 使用场景与优势

- **🔌 分布式工具集：** 访问托管在不同 MCP server 上的工具，例如一个做天气，一个做金融。
- **🧱 模块化架构：** 不同团队可以独立托管各自工具，同时统一暴露标准 MCP 接口。
- **📈 可扩展性与弹性：** 负载可以分散到多个 MCP；单台服务器下线也不一定会阻断 agent 能力。
- **🌐 第三方集成：** 任何暴露 MCP 兼容端点的外部服务，都可以平滑接入。

---

### ⚙️ 配置与要求

- agent 的 `mcp_servers` 参数接受的是**已激活的 MCP client 实例列表**。
- 每个 client 都应通过 `MCPServerStreamableHttpParams` 配置，并放在 `AsyncExitStack` 中统一管理。

#### ✅ 推荐的异步模式

```python
import asyncio
from contextlib import AsyncExitStack
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner

# Define all MCP server URLs
MCP_SERVER_URLS = [
    "http://localhost:8001/mcp",
    "http://localhost:8002/mcp",
]

# Setup client (e.g., OpenAI/Gemini-compatible)
client = AsyncOpenAI(
    api_key="your-api-key",
    base_url="https://your-base-url",
)

async def main():
    mcp_servers = []

    async with AsyncExitStack() as stack:
        for url in MCP_SERVER_URLS:
            mcp_params = MCPServerStreamableHttpParams(url=url)
            mcp_server_client = await stack.enter_async_context(
                MCPServerStreamableHttp(params=mcp_params, name=f"MCPClient_{url}")
            )
            mcp_servers.append(mcp_server_client)

        assistant = Agent(
            name="MultiMCPAgent",
            instructions="You are a multi-server agent.",
            mcp_servers=mcp_servers,
            model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
        )

        result = await Runner.run(assistant, "Get today's weather and Tesla stock price.")
        print(f"[AGENT RESPONSE]: {result.final_output}")

asyncio.run(main())
```

---

### 🚀 分步运行示例

如果你想运行这个示例，观察一个 agent 如何连接多个 MCP server，请按以下步骤进行：

1. **启动 MCP Servers：**
   你需要启动两个 MCP server：一个处理 mood，一个处理 weather。它们位于本示例模块（`04_agent_with_multiple_mcp_servers`）中的 `mcp_servers` 子目录下。请打开两个独立终端。

   - **Mood Server（运行在 8001 端口）：**
     在第一个终端中进入 `mcp_servers` 目录：
      ```bash
      cd mcp_servers
      uv run python mood_server.py
      ```
      这个 server 提供 `mood_from_shared_server` 工具。

   - **Weather Server（运行在 8002 端口）：**
     在第二个终端中也进入 `mcp_servers` 目录：
      ```bash
      cd mcp_servers
      uv run python weather_server.py
      ```
      这个 server 提供 `get_forecast` 工具。

   确保这两个 server 都成功启动。它们会在各自终端中打印日志（例如 `"INFO: Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)"`）。这些终端可以保持运行。

2. **配置环境变量：**
   agent 代码位于 `agent_connect/main.py`（在本示例模块内部），它通过 `AsyncOpenAI` 使用 Gemini 模型，因此需要 API key。

   - 进入 `agent_connect` 子目录。
   - 如果还没有，就创建一个 `.env` 文件（例如 `agent_connect/.env`）。
   - 在文件中添加你的 `GEMINI_API_KEY`：
      ```env
      GEMINI_API_KEY="your_actual_api_key_here"
      ```
   - `main.py` 还配置了 LangSmith tracing。如果你想启用 LangSmith，请确保设置好 `LANGCHAIN_API_KEY`、`LANGCHAIN_TRACING_V2="true"` 和 `LANGCHAIN_PROJECT="your-project-name"`（可写在同一个 `.env` 文件中，或系统环境变量中）。

3. **运行 Agent：**
   如果你当前不在 `agent_connect` 目录，请从本示例模块根目录（`04_agent_with_multiple_mcp_servers`）进入：

    ```bash
    cd agent_connect
    ```

   然后执行主 agent 脚本：

    ```bash
    uv run python main.py
    ```

   agent 会尝试连接这两个 MCP server，汇总它们的工具（`mood_from_shared_server` 和 `get_forecast`），然后处理类似 `"What is Junaid's mood and what is the weather in London?"` 这样的查询。你会在终端中看到 agent 的交互输出（包括通过 MCP server client 名称识别出的工具调用）以及最终响应。

4. **观察 Tracing（可选但推荐）：**
   `agent_connect/main.py` 中配置了 `OpenAIAgentsTracingProcessor`（并使用 `typing.cast` 保证 linter 兼容）。如果你的 LangSmith 环境变量配置正确：
   - 你可以进入 LangSmith 项目页面查看 agent 执行的完整 trace。
   - 这个 trace 会清晰展示 agent 的决策过程、调用了哪些工具、由哪个 MCP server 处理了每次调用（可通过类似 `MCPServerClient_http://localhost:8001/mcp` 这样的 client 名字识别），以及数据如何在系统中流动。这对调试、理解多 MCP 交互，以及验证不同 server 上的工具是否被正确使用都非常有价值。

---

### 🧰 聚合后的工具管理

- 当一个 agent 同时连接到**多个 MCP server** 时，它会把这些工具集合聚合成一个**逻辑上的统一注册表**。
- 对 `agent.tools` 的访问，或者 LLM 做出的工具选择，都会自动把**所有 MCP 来源的工具**一并纳入考虑。

---

### 🚨 工具名唯一性与冲突处理

- **重要：** 所有已连接 MCP 中的工具名**必须唯一**。
- 冲突（例如两个都叫 `get_weather` 的工具）可能导致不可预测的行为，具体表现取决于内部解析顺序。
- **最佳实践：** 使用**命名空间或前缀**规范，例如：

  - `finance_get_stock_price`
  - `weather_get_forecast`

SDK **目前不会**自动解决这些冲突，这部分是**开发者自己的责任**。

---

本子模块会通过 Python 示例代码说明这些概念，包括如何搭建 mock MCP server，以及如何构建一个能与它们交互的 agent。
