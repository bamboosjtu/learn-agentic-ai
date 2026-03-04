# 用 MCP Servers 把生产力提升 10 倍

Model Context Protocol（MCP）服务器可以把强大的工具接入你喜欢的编码 agent。只要加上几个，agent 就能在不离开聊天界面的情况下浏览网页、控制 Playwright、连接 GitHub、记住团队知识、搜索最新文档。

这份指南会尽量保持简单和实用。你可以配合任何你偏好的 coding agent 使用。

---

## 在 OpenAI Agents SDK 中使用 MCP

OpenAI Agents SDK 从 v0.2.0 开始支持 MCP，让你的 Agent 能够连接外部工具和数据源。

### 基本概念

| 概念 | 说明 |
|------|------|
| **MCP Server** | 提供工具和资源的后端服务 |
| **Stdio** | 本地进程间通信（适合本地工具） |
| **SSE** | Server-Sent Events（适合远程服务） |
| **Tool** | MCP 暴露给 Agent 的功能 |

### 方式 1：连接本地 MCP Server（Stdio）

```python
import asyncio
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

async def main():
    # 启动文件系统 MCP Server
    async with MCPServerStdio(
        name="filesystem-server",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "./docs"]
    ) as mcp_server:
        
        # 获取 MCP Server 提供的所有工具
        tools = await mcp_server.list_tools()
        
        # 创建使用 MCP 工具的 Agent
        agent = Agent(
            name="Document Assistant",
            instructions="You help users manage and query documents.",
            tools=tools,
            model="gpt-5-nano"
        )
        
        # 运行 Agent
        result = await Runner.run(
            agent,
            "Read the README.md file and summarize its content"
        )
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

### 方式 2：连接远程 MCP Server（SSE）

```python
from agents.mcp import MCPServerSse

async with MCPServerSse(
    name="remote-tools",
    url="https://your-mcp-server.com/sse"
) as server:
    
    tools = await server.list_tools()
    agent = Agent(
        name="Remote Assistant",
        tools=tools,
    )
    
    result = await Runner.run(agent, "Do something")
```

### 完整示例：使用文件系统 MCP

```python
import asyncio
import os
from agents import Agent, Runner, set_default_openai_api, set_default_openai_client
from agents.mcp import MCPServerStdio
from openai import AsyncOpenAI

# 配置 OpenAI 客户端
client = AsyncOpenAI(
    api_key=os.getenv("AIHUBMIX_API_KEY"),
    base_url=os.getenv("AIHUBMIX_BASE_URL")
)
set_default_openai_client(client)
set_default_openai_api("chat_completions")

async def main():
    async with MCPServerStdio(
        name="filesystem-server",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "./docs"]
    ) as mcp_server:
        
        # 列出可用的 MCP 工具
        print("Available MCP tools:")
        tools = await mcp_server.list_tools()
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        
        # 创建 Agent
        agent = Agent(
            name="Document Assistant",
            instructions="""You help users manage and query documents.
You have access to filesystem tools through MCP.""",
            tools=tools,
            model="gpt-5-nano"
        )
        
        result = await Runner.run(
            agent,
            "List all files in the directory"
        )
        print(f"\nResult: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 常用 MCP Servers

```bash
# 文件系统
npx @modelcontextprotocol/server-filesystem /path/to/files

# GitHub
npx @modelcontextprotocol/server-github

# PostgreSQL
npx @modelcontextprotocol/server-postgres

# SQLite
npx @modelcontextprotocol/server-sqlite
```

---

## 在 Coding Agent 中使用 MCP（Cursor/Qwen/Claude Code 等）

以下配置适用于各种 AI 编程助手：

---

## 推荐的入门服务器

### Playwright MCP：无头浏览器与 UI 测试

- **为什么用它：** 自动执行用户流程、截图、并在修改后验证页面状态
- **如何添加：**
  ```json
  {
    "mcpServers": {
      "playwright": {
        "command": "npx",
        "args": ["@playwright/mcp@latest"]
      }
    }
  }
  ```

- **可以这样试：**
  > now setup a simple page that shows galaxy. Take the screenshot to ensure it's all perfect and review it. Continue iterating after reviewing to get perfect galaxy view.

### Tavily Browser Search：网页搜索与抓取

- **为什么用它：** 快速研究、对比文档、收集引用资料
- **如何添加：**
  ```json
  {
    "mcpServers": {
      "tavily-remote": {
        "command": "npx",
        "args": [
          "-y",
          "mcp-remote",
          "https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>"
        ]
      }
    }
  }
  ```
  先在 shell 中导出 `TAVILY_API_KEY`。重新加载 agent 后，用 `qwen mcp list` 和 `/mcp` 确认是否接入成功。
- **可以这样试：**
  > Check and research if gemini 3.0 and sonnet 4.5 are released.

### Context7 MCP：最新代码文档

- **为什么用它：** 提供带引用的框架、API 和 changelog 摘要
- **如何添加：**
  ```json
  {
    "mcpServers": {
      "context7": {
        "command": "npx",
        "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
      }
    }
  }
  ```
  把 Context7 key 配成环境变量，并用 `qwen mcp list` 和 `/mcp` 验证。

### OpenMemory：保存团队事实

- **为什么用它：** 跨会话保存决策、偏好和提醒事项
- **如何添加：**
  ```json
    "openmemory": {
      "command": "npx",
      "args": ["-y", "openmemory"],
      "env": {
        "OPENMEMORY_API_KEY": "YOUR_API_KEY"
      }
    }
  ```
- **可以这样试：**
  > Use add-memory tool and save that we prefer to use OpenAI Agents SDK, MCP, A2A, Kubernetes for Agentic AI.

---

## 如何选择服务器（像技术型业务经理那样思考）

1. **先看结果：** 这个服务器能解锁什么工作流？比如"每天验证登录流程"或"5 分钟内整理竞品资料"。
2. **快速判断 ROI：** 安装是否能控制在 15 分钟内？每周是否能节省 30 分钟以上？是否能减少频繁切换上下文？
3. **安全性：** 认证信息用环境变量，不要给过宽的 shell 权限，尽量白名单命令，不要把 token 放进仓库。
4. **维护成本：** 优先选择活跃维护、文档清晰、安装卸载简单、依赖少的项目。
5. **集成匹配度：** 选择能补足你当前工具链能力的服务器，而不是和现有能力重复太多。
6. **验证价值：** 做一个 1 天的小试点，并设定可量化目标，例如抓到一次 flaky login、拉取三条高质量引用来源、自动生成一份会议摘要。

---

有了少量 MCP servers，你的 coding agent 就不只是"代码补全工具"，而更像一个完整队友：它可以研究、测试、记忆并更快地对代码做推理。逐步构建你的工具栈，并在每次加入一个新 server 后都认真验证它的价值。

---

## 附录：自定义 MCP Server

你也可以自己编写 MCP Server 来暴露自定义功能：

```python
# my_mcp_server.py
from mcp.server import Server
from mcp.types import TextContent
import mcp.server.stdio

app = Server("my-server")

@app.list_tools()
async def list_tools():
    return [
        {
            "name": "calculate",
            "description": "Perform a calculation",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            }
        }
    ]

@app.call_tool()
async def call_tool(name, arguments):
    if name == "calculate":
        result = eval(arguments["expression"])
        return [TextContent(type="text", text=str(result))]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

在 Agent 中连接自定义 Server：

```python
async with MCPServerStdio(
    name="my-custom-server",
    command="python",
    args=["my_mcp_server.py"]
) as server:
    tools = await server.list_tools()
    agent = Agent(name="Calculator", tools=tools)
    result = await Runner.run(agent, "Calculate 2 + 2")
```