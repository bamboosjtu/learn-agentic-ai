# 01：Hello, MCP Server!

**目标：** 使用 `FastMCP` 库，以 **无状态（stateless）** 模式运行你的第一个、最基础的 Model Context Protocol（MCP）Server。

### 🌐 MCP 和你熟悉的东西有什么关系？

| **如果你熟悉……** | **那么 MCP 类似于……** | **关键区别** |
|-------------------|-------------------|-------------------|
| **REST APIs** | 一种标准协议，不过是给 AI 和工具通信用的 | 专门为 AI 交互设计 |
| **OpenAI Function Calling** | 能适配任意 AI 模型的函数调用机制 | 通用标准，不绑定单一厂商 |
| **Webhooks** | AI 与外部系统之间的双向通信方式 | 针对 AI 场景做了结构化设计 |
| **Plugin Systems** | AI 模型的插件系统 | 跨平台且标准化 |

这个起步示例只关注最基础的内容：

1. 创建一个独立处理每个请求的 Server
2. 让这个 Server 通过无状态 Streamable HTTP 对外提供服务
3. 使用一个符合规范的 Client 与它交互，并正确执行 `initialize` 握手

它相当于 MCP 开发里的 “Hello, World!”。它提供了最简单可行的 Server 配置，同时也教你掌握正确的客户端交互流程。

## MCP 关键概念

- **`FastMCP` Server：** 一个 Python 库，用于处理 MCP `2025-06-18` 规范中的底层细节。
- **无状态 HTTP 传输（`stateless_http=True`）：** `FastMCP` 中的一种便捷模式，Server 会把每个请求都当作全新、彼此独立的交互来处理。它在处理完请求后会立即“忘记”会话状态，因此非常适合学习最基础的请求-响应模式，而不必管理持久状态。

## 实现计划

在 `hello-mcp/` 子目录中，我们将完成：

- **`server.py`：**
  - 以无状态模式（`stateless_http=True`）实例化一个 `FastMCP` Server
  - 将 Server 暴露为可供 `uvicorn` 运行的 ASGI 应用

- **`client.py`：**
  - 一个简单的 Python 脚本，使用 `httpx` 发起 JSON-RPC 请求
  - 它会先调用 `initialize`，以遵循 MCP 规范

- **Postman Collection：**
  - `postman/` 目录中提供了一个集合，用于可视化演示符合规范的三步交互流程

## 关键概念

- **`FastMCP`：** 一个 Python 库，用来简化符合 MCP 规范的 Server 创建过程。它处理了许多底层协议复杂性，让你能更专注于定义 Server 的能力。
- **Server Instantiation：** 创建 `FastMCP` 应用实例。
- **Server Metadata：** 提供一些基础元数据，例如名称和版本，这些信息会在初始化阶段返回给客户端。

## 步骤

1. **环境准备：**

   - 确保你已经安装 Python（建议 Python 3.12+）以及 `uv`

    ```bash
    uv init hello-mcp
    cd hello-mcp
    ```

2. **安装依赖：**

   - 使用 `uv` 安装所需包：

      ```bash
      uv add mcp uvicorn httpx
      ```

3. 更新 `server.py`：

   - 我们将导入 `FastMCP`，并创建一个使用无状态 HTTP 协议的简单工具服务。

```python
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

# 使用 2025-06-18 规范初始化 FastMCP Server，并附带基础元数据
mcp = FastMCP(
    name="hello-server",
    stateless_http=True
)


mcp_app = mcp.streamable_http_app()
```

4. **运行 Server：**

   - 执行命令：

      ```bash
      uv run uvicorn server:mcp_app --port 8000 --reload
      ```

   - 这会启动：
     - MCP Server 地址：`http://localhost:8000`
      

5. **测试 MCP Server：**

   **方式 1：Postman（可视化、适合教学）- 学习阶段推荐**

   1. 从 [postman.com](https://www.postman.com/downloads/) 安装 Postman
   2. 导入集合：`postman/Hello_MCP_Server.postman_collection.json`
   3. 按顺序运行请求，理解 MCP 协议流程
   4. 详细说明见 `postman/README.md`

   **方式 2：MCP Inspector（交互式）**

    ```bash
    npx @modelcontextprotocol/inspector
    ```

    或

    ```bash
    mcp dev server.py
    ```

   - 运行后打开 MCP Inspector：`http://127.0.0.1:6274`

    
   **方式 3：Python Client（程序化）**

    ```bash
    uv run python client.py
    ```

## 🔗 下一步

- **02_project_setup**：从 MCP 入门课程开始继续学习。
