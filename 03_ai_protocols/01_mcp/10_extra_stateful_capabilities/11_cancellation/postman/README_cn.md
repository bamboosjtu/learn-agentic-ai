# MCP Cancellation Postman 测试 🧪

这个 Postman collection 提供了一种简单、可动手的方式来测试 MCP 请求取消。

## 🚀 **快速准备**

### **1. 导入 Collection**
1. 打开 Postman
2. 点击 `Import`，选择 `MCP_Cancellation_Tests.postman_collection.json`
3. 该 collection 会出现在你的工作区中

### **2. 启动 MCP Server**
在终端中进入 `mcp_code` 目录并启动 server：
```bash
# From the 11_cancellation directory
cd mcp_code
uv run server.py
```
server 会运行在 `http://localhost:8000`。

### **3. 运行请求**
现在你就可以运行 collection 中的请求了。为了得到最佳体验，请按顺序执行。

## 🧪 **取消测试流程**

这个 collection 演示标准 cancellation 流程。它最适合在**快速地一前一后运行第 3 和第 4 步**时使用。

1. **`1. Initialize MCP Connection`**：与 server 建立 session，并保存 `sessionId`
2. **`2. Send Initialized Notification`**：完成 MCP 握手
3. **`3. Start Long-Running Task`**：向 `process_large_file` 工具发送请求，该任务会运行 10 秒。这个请求在 Postman 中会表现得像“卡住了”，这是预期现象
4. **`4. Cancel Long-Running Task`**：在前一个请求还处于“运行中”时，发送这个请求。它会向 server 发一条 `notifications/cancelled` 消息，告诉它停止任务

## 📊 **预期结果**

如果你及时取消了长任务（也就是在第 3 步开始后的 10 秒内运行第 4 步），server 日志会显示：
```
INFO:     Calling tool: process_large_file
INFO:     Starting to process postman_test_file.csv (Request: 2)
DEBUG:    Processed chunk 1/10
DEBUG:    Processed chunk 2/10
WARNING:  Processing of postman_test_file.csv was cancelled by client.
```

然后，**第 3 步**的原始请求最终会返回一个 JSON 错误对象，表明该任务已被取消（`"code": -32800`）。

## 🔧 **故障排查**

- **Server 没响应**：确认 server 已启动，并检查 Postman collection 中的 `baseUrl` 是否设置正确（默认是 `http://localhost:8000`）
- **Session ID 问题**：如果报错，重新运行 `1. Initialize MCP Connection`，拿一个新的 session ID

---
💡 **小提示**：运行 Postman 请求时，注意同时观察 server 终端输出。它能实时展示 server 如何处理每一步，包括何时收到 cancellation 通知。
