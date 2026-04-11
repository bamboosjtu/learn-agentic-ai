# Shared MCP Server

在模块 `07_openai_agents_sdk_integration` 的示例中，我们会使用一个共享的、独立运行的 MCP server。这个 server 的设计目标是保持简单，并为各个 agent 示例提供一个一致的目标服务。

- **位置：** `05_ai_protocols/01_mcp/07_openai_agents_sdk_integration/shared_mcp_server/server_main.py`
- **运行方式：**
  1. 打开一个新终端。
  2. 进入 `shared_mcp_server` 目录：
  ```bash
  cd 05_ai_protocols/01_mcp/07_openai_agents_sdk_integration/shared_mcp_server/
  ```
  3. 执行服务器脚本（使用 `uv run`）：
      ```bash
      uv run python server.py
      ```
- **服务器信息：**
  - 运行地址是 `http://localhost:8001`
  - 它的 MCP 协议端点是 `/mcp`，因此客户端完整访问地址为 `http://localhost:8001/mcp`
  - 它暴露一个名为 `greet_from_shared_server` 的工具
  - 它会把收到的请求记录到控制台日志中
