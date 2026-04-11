# 📮 MCP Ping Utility 的 Postman 测试指南

本目录包含一个 Postman collection，用来依据 [MCP 2025-06-18 Ping 规范](https://modelcontextprotocol.io/specification/2025-06-18/basic/utilities/ping)测试 MCP Ping Utility。

## 🎯 你将测试什么

- **🏓 基础 Ping 请求 / 响应**：标准 ping / pong 流程
- **⏰ 响应时间校验**：确保 server 响应足够及时
- **🔧 规范合规性**：验证请求与响应格式是否严格符合规范
- **⚡ 性能测试**：快速连续发送 ping，观察高负载下的健康状态

## 📋 前置条件

1. **启动 MCP Server**：
    ```bash
    # Navigate to the code directory
    cd mcp-decoded/02_server_engineering/09_ping/mcp_code
    
    # Start the server
    uv run server.py
    ```
    server 会运行在 `http://localhost:8000`。

2. **导入 Collection**：
    - 把 `MCP_Ping_Tests.postman_collection.json` 导入 Postman
    - collection 已预先配置好 `mcp_session_id` 变量

## 🔄 如何测试：完整生命周期

请按顺序执行 Postman collection 中的这些请求。

### 1. Initialize MCP Server
这个请求会启动一个新的 MCP session，并自动保存后续请求所需的 `mcp-session-id`。

- **请求**：`POST http://localhost:8000/mcp/`
- **请求体**：
    ```json
    {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-06-18",
            "clientInfo": {
                "name": "postman-ping-client",
                "version": "1.0.0"
            },
            "capabilities": {}
        },
        "id": 1
    }
    ```
- **预期结果**：测试脚本会确认状态码为 `200 OK`，并提取 session ID

### 2. Send Initialized Notification
这个请求告诉 server：我们已经准备好继续后续流程。

- **请求**：`POST http://localhost:8000/mcp/`
- **Headers**：包含从上一步获取到的 `mcp-session-id`
- **预期结果**：返回 `202 Accepted`

### 3. Basic Ping Test
这个请求发送标准 `ping`，并校验响应。

- **请求**：`POST http://localhost:8000/mcp/`
- **请求体**：
    ```json
    {
        "jsonrpc": "2.0",
        "id": "ping_test_1",
        "method": "ping"
    }
    ```
- **预期结果**：返回 `200 OK`，并带一个空的 `result` 对象：`{"jsonrpc": "2.0", "id": "ping_test_1", "result": {}}`。测试脚本会验证这一结构。

## 📚 规范深入理解

根据 [MCP Ping 规范](https://modelcontextprotocol.io/specification/2025-06-18/basic/utilities/ping)：

- **请求格式**：`ping` 请求 **不能**包含 `params` 对象
- **响应格式**：响应中 **必须**包含一个空的 `result` 对象（`{}`）
- **行为要求**：接收方 **必须**及时响应。我们的 Postman 测试会通过断言合理的响应时间来检查这一点

这个简单握手，是稳定可靠的 MCP 连接的基础。

## 🧪 测试场景

### ✅ **成功场景**
1. **Basic Ping** - 标准规范示例
2. **Rapid Pings** - 并发发送多个 ping 请求
3. **Response Time** - 校验“及时响应”的规范要求
4. **Format Compliance** - 严格校验格式是否符合规范

### ❌ **错误场景**
1. **Invalid Parameters** - 带 `params` 的 ping（应被拒绝）
2. **Missing Session** - 没有 MCP session 的 ping
3. **Malformed JSON** - 非法 JSON-RPC 格式

## 📊 预期结果

| 测试用例 | 预期状态 | 响应时间 | 说明 |
|-----------|----------------|---------------|-------|
| Basic Ping | 200 OK | < 1000ms | 符合规范 |
| Rapid Pings | 200 OK | < 500ms | 性能验证 |
| Invalid Params | 200/400 | 任意 | server 可自行处理 |
| No Session | 200/400/401 | 任意 | 取决于 server 策略 |

## 📚 参考资料

- [MCP Ping Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/utilities/ping)
- [MCP Basic Protocol](https://modelcontextprotocol.io/specification/2025-03-26/basic/overview)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)

---

**🎯 核心学习点：** MCP ping 是连接健康监控的基础。理解这个简单 utility，会让你更容易掌握后续更复杂的 MCP utilities，例如 logging 和 progress tracking。🏓
