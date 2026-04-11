# 🏓 MCP Ping Utility

> **类比：** 把 ping 工具想象成潜艇上的声呐。你向黑暗水域中发出一个 “ping”。如果听到了回声，你就知道连接还活着，甚至还能通过延迟判断 server “离你有多远”。如果听不到回声，那连接可能已经沉入深海。MCP Ping 就是数字连接里的这种声呐。

本课演示如何使用简单但至关重要的 `ping` utility，来监控连接的健康状态和响应性。

## 🎯 你将学到什么

- **Server 端：** `FastMCP` 如何自动处理 `ping` 请求，而无需额外代码
- **Client 端：** 如何发送 `ping` 请求，并处理空的 `pong`（即空 `result`）响应
- **协议层面：** 如何用 `ping` 做基础健康检查和延迟测量
- **交互测试：** 如何用 Postman 发送 `ping` 请求，并验证 server 是否符合 MCP 规范

## ✅ 如何使用这个示例

你可以通过两种方式测试 `ping` utility：

### 1. 使用 Python Client（自动测试）

这个脚本会初始化一个 MCP session，并运行一个基础 `ping` 测试。

```bash
# Navigate to the code directory
cd mcp-decoded/02_server_engineering/09_ping/mcp_code

# Terminal 1: Start the server
uv run uvicorn server:mcp_app --reload

# Terminal 2: Run the client test
uv run client.py
```

### 2. 使用 Postman Collection（交互测试）

这是最适合你亲自观察请求 / 响应流程的方式。

1. **启动 Server**：确保上一步的 Python server 正在运行
2. **使用 Collection**：打开 `postman/` 目录，并把 `MCP_Ping_Tests.postman_collection.json` 导入 Postman
3. **按照说明操作**：collection 中的 `README.md` 会逐步指导你完成 `ping` 生命周期测试。你需要先初始化连接，再发送 `ping`

## ⚙️ 代码结构

- `mcp_code/server.py`：一个最小化的 `FastMCP` server。注意，这里没有任何专门处理 `ping` 的代码，框架会自动替你处理，这是本课的重要知识点。
- `mcp_code/client.py`：一个简单 Python client，用来连接 server、发送 `ping` 并打印结果。
- `postman/`：用于交互测试的 Postman collection 及其说明文档。

## 🎯 关键结论

MCP ping 是最简单却最基础的连接健康工具。先掌握这个基础，再继续理解更复杂的 utility，例如 logging 和 progress tracking。🏓
