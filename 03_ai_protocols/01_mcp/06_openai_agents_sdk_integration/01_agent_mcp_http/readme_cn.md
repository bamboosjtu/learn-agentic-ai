# 子模块 01：连接到 MCP 服务器（Streamable HTTP）

**目标：** 演示如何使用 OpenAI Agents SDK 中的 `MCPServerStreamableHttp` 客户端类，把一个 OpenAI Agent 基础配置并连接到使用 `streamable-http` 传输的 MCP 服务器。

## 核心概念

这里的主要目标，是展示如何用一个 `MCPServerStreamableHttp` 实例来初始化 `Agent`。这个实例本身就是一个客户端，它指向一个正在运行的 MCP 服务器。我们希望确认：当 agent 初始化，或者第一次需要和 MCP 工具交互时，它会尝试连接到这个服务器。一个常见的第一次交互，就是 agent（或者 SDK 代表它）调用 MCP 服务器上的 `list_tools()`。

## 关键 SDK 概念

- `MCPServerStreamableHttpParams`：用于配置 `streamable-http` MCP 服务器的连接细节
- `MCPServerStreamableHttp`：SDK 中用于与这类服务器交互的客户端类
- `Agent(mcp_servers=[...])`：让 agent 知道有哪些 MCP 服务器可用
- `mcp_server_client.list_tools()`：显式调用工具列表（Agent 也会隐式触发）
- 对 `MCPServerStreamableHttp` 使用异步上下文管理（`async with`）
- 使用 `Runner.run()` 执行一个带查询的 agent

## 环境准备

### 1. 运行共享 MCP 服务器

在本模块 `06_openai_agents_sdk_integration` 以及后续示例中，我们会使用一个共享的独立 MCP 服务器。这个服务器设计得很简单，目的是为所有 agent 示例提供一个一致的目标服务。

- **位置：** `03_ai_protocols/01_mcp/06_openai_agents_sdk_integration/shared_mcp_server/server.py`
- **运行方式：**
  1. 打开一个新终端。
  2. 进入 `shared_mcp_server` 目录：
  ```bash
  cd 03_ai_protocols/01_mcp/06_openai_agents_sdk_integration/shared_mcp_server/
  ```
  3. 执行服务器脚本（使用 `uv run`）：
      ```bash
      uv run python server.py
      ```
- **服务器信息：**
  - 运行地址为 `http://localhost:8001`
  - MCP 协议端点是 `/mcp`，因此客户端连接地址完整写法是 `http://localhost:8001/mcp`
  - 它暴露了一个名为 `greet_from_shared_server` 的工具
  - 它会把收到的请求打印到控制台日志中

**当你运行本子模块中的 agent 脚本时，请保持这个服务器终端持续运行。**

### 2. “Hello World” Agent SDK 连接

#### 安装

```bash
uv init agent_connect
cd agent_connect

uv add openai-agents
```

创建一个 `.env` 文件，并添加 `GEMINI_API_KEY`

### 代码

在当前目录创建一个名为 `main.py` 的文件，并写入以下内容：

```python
import asyncio
import os
from dotenv import load_dotenv, find_dotenv

from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams


_: bool = load_dotenv(find_dotenv())

# URL of our standalone MCP server (from shared_mcp_server)
MCP_SERVER_URL = "http://localhost:8001/mcp/" # Ensure this matches your running server

gemini_api_key = os.getenv("GEMINI_API_KEY")

#Reference: https://ai.google.dev/gemini-api/docs/openai
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

async def main():
    # 1. Configure parameters for the MCPServerStreamableHttp client
    # These parameters tell the SDK how to reach the MCP server.
    mcp_params = MCPServerStreamableHttpParams(url=MCP_SERVER_URL)
    print(f"MCPServerStreamableHttpParams configured for URL: {mcp_params.get('url')}")

    # 2. Create an instance of the MCPServerStreamableHttp client.
    # This object represents our connection to the specific MCP server.
    # It's an async context manager, so we use `async with` for proper setup and teardown.
    # The `name` parameter is optional but useful for identifying the server in logs or multi-server setups.
    async with MCPServerStreamableHttp(params=mcp_params, name="MySharedMCPServerClient") as mcp_server_client:
        print(f"MCPServerStreamableHttp client '{mcp_server_client.name}' created and entered context.")
        print("The SDK will use this client to interact with the MCP server.")

        # 3. Create an agent and pass the MCP server client to it.
        # When an agent is initialized with mcp_servers, the SDK often attempts
        # to list tools from these servers to make the LLM aware of them.
        # You might see a `list_tools` call logged by your shared_mcp_server.
        try:
            assistant = Agent(
                name="MyMCPConnectedAssistant",
                mcp_servers=[mcp_server_client],
                model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
            )
            
            print(f"Agent '{assistant.name}' initialized with MCP server: '{mcp_server_client.name}'.")
            print("Check the logs of your shared_mcp_server for a 'tools/list' request.")

            # 4. Explicitly list tools to confirm connection and tool discovery.
            print(f"Attempting to explicitly list tools from '{mcp_server_client.name}'...")
            tools = await mcp_server_client.list_tools()
            print(f"Tools: {tools}")

            print("\n\nRunning a simple agent interaction...")
            result = await Runner.run(assistant, "What is Sir Zia mood?")
            print(f"\n\n[AGENT RESPONSE]: {result.final_output}")

        except Exception as e:
            print(f"An error occurred during agent setup or tool listing: {e}")

    print(f"MCPServerStreamableHttp client '{mcp_server_client.name}' context exited.")
    print(f"--- Agent Connection Test End ---")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An unhandled error occurred in the agent script: {e}")
```

## 代码说明

1. **`MCP_SERVER_URL`：**
   指向共享 MCP 服务器。

2. **`MCPServerStreamableHttpParams` 与 `MCPServerStreamableHttp`：**
   - 负责配置并创建一个连接 MCP 服务器的客户端，作用和之前版本说明的一样。

3. **`Agent` 初始化：**
   - `Agent` 会使用 `name`、`instructions`、`mcp_servers`（指向我们的 `mcp_server_client`）以及 `model` 进行初始化。
   - `model` 使用的是 `OpenAIChatCompletionsModel`，配置为 `model="gemini-2.0-flash"`，并把 `openai_client` 指向 Gemini 客户端。

4. **显式调用 `list_tools()`：**
   - 脚本显式执行 `await mcp_server_client.list_tools()`，用于验证连接和工具发现是否成功。
   - 它会检查是否存在 `greet_from_shared_server` 和 `mood_from_shared_server` 这两个工具。

5. **`Runner.run(assistant, "What is Junaid's mood?")`：**
   - 这一行会用指定查询执行 agent。
   - `Runner.run` 会处理整个交互流程：把用户查询和 instructions 发给 LLM，处理 LLM 决定调用的工具（通过配置好的 MCP 服务器），最后返回最终结果。
   - 查询 `"What is Junaid's mood?"` 的设计目的是：如果 LLM 觉得合适，它可能会触发 `mood_from_shared_server` 工具。

## 预期输出 / 行为

当你运行 `uv run python main.py` 时（前提是已经启动 `shared_mcp_server/server_main.py`，并且 `.env` 文件中配置了 `GEMINI_API_KEY`）：

1. **Agent 脚本终端（`main.py` 输出）：**

   - 打印连接步骤日志
   - 打印来自 `httpx` 的日志，显示它向 MCP 服务器（`http://localhost:8001/mcp/`）和 Gemini API（`https://generativelanguage.googleapis.com/...`）发起了 HTTP 请求
   - 显示 `MySharedMCPServerClient` 创建成功
   - 显示 agent 初始化日志
   - 成功列出 MCP 服务器工具，包括 `greet_from_shared_server` 和 `mood_from_shared_server`
   - 打印 `"Running a simple agent interaction..."`
   - 在执行 `Runner.run` 期间，继续出现 MCP 与 Gemini 的交互日志
   - 打印最终 agent 响应，例如：`[AGENT RESPONSE]: OK. Junaid is happy.`（具体内容取决于 LLM 和工具执行情况）
   - 最后打印客户端上下文退出和测试结束的日志

2. **共享 MCP 服务器终端（`server_main.py` 输出）：**
   - 你会看到日志表明它收到了 `tools/list` 请求
   - 如果 LLM 决定使用 `mood_from_shared_server` 工具（或其他工具），你会看到对应的 `tool/run` 请求。例如：
      ```
      INFO:SharedStandAloneMCPServer:MCP Request ID '...' received: tools/list
      INFO:SharedStandAloneMCPServer:Responding to 'tools/list' (ID '...') with 2 tool(s).
      ...
      INFO:SharedStandAloneMCPServer:MCP Request ID '...' received: tool/run (tool_name='mood_from_shared_server')
      INFO:SharedStandAloneMCPServer:Running tool 'mood_from_shared_server' with args: {'name': 'Junaid'}
      INFO:SharedStandAloneMCPServer:Tool 'mood_from_shared_server' execution successful.
      ```

这个完整测试不仅验证了连接和工具列表获取，也验证了 agent 在执行流程中能够使用 LLM（Gemini），并在需要时调用 MCP 工具。
