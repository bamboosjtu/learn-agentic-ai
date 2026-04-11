# 🔄 MCP Resumption - Postman 测试指南

> 这个 collection 通过模拟 client 断开连接后无缝重连到长时间任务的过程，来演示 MCP resumption。

## 🎯 这个 Collection 测什么

- **MCP 初始化**：建立 session，并获取 `mcp-session-id`
- **模拟超时**：调用一个长时间运行工具，并设置较短超时，以模拟网络中断
- **连接恢复**：使用带 `Last-Event-ID` 和 `mcp-session-id` Header 的 `GET` 请求重新连接，并按 MCP 规范接收错过的消息

## 🚀 如何使用

### 1. 启动 Server

确保示例 server 已运行。它内置了 6 秒延迟。

```bash
# From the 10_resumption directory
uv run server.py
```

### 2. 按顺序运行请求

按 collection 中的文件夹顺序依次执行请求。这个流程设计成顺序运行。

- **STEP 1: Initialize MCP Connection**：这一组建立连接
  1. `Initialize MCP Server`：获取 `mcp-session-id` 和第一个 `last_event_id`
  2. `Send Initialized Notification`：完成握手
- **STEP 2: Tool Call Timeout**：这一组模拟网络中断
  3. `Tool Call with Timeout`：这个请求设置了 **2 秒超时**。server 需要 6 秒才能完成，所以这个请求**必然超时失败**，这正是我们想要的
- **STEP 3: MCP Resumption**：这一组展示成功恢复
  4. `MCP Resumption with GET + Last-Event-ID`：这个请求会立即从 server 取回已经在后台完成的结果

## 🔍 重点观察什么

- 在 **Step 2** 中，工具调用会因超时失败，这是预期行为
- 在 **Step 3** 中，恢复请求会立即成功（响应时间非常短）
- 查看 Postman Console，可以看到 `mcp-session-id` 和 `last_event_id` 如何被测试脚本自动捕获并复用
- 最终响应体中会包含文本 `(Retrieved via resumption)`，证明返回的是缓存结果

## 🔧 **关键特性**

### **自动跟踪 Event ID**
这个 collection 会自动提取并保存 event ID：
```javascript
// Finds "id: 12345" in SSE response
if (line.startsWith('id: ')) {
    eventId = line.substring(4).trim();
    pm.collectionVariables.set('last_event_id', eventId);
}
```

### **Session 管理**
自动捕获 session ID：
```javascript
const sessionId = pm.response.headers.get('mcp-session-id');
pm.collectionVariables.set('mcp_session_id', sessionId);
```

### **MCP Resumption Header**
测试 4 使用了 MCP 规范中的 Header：
```json
{
  "key": "Last-Event-ID",
  "value": "{{last_event_id}}",
  "description": "MCP spec header for cross-stream event replay"
}
```

## 🔬 **技术学习点**

### **Cross-Stream Event Correlation**
这是学生最应该理解的技术点：
- **问题**：事件被存放在不同 stream 中（`stream_id='1'` vs `stream_id='_GET_stream'`）
- **解决方案**：在所有 stream 中查找 last event ID 之后的新事件
- **结果**：MCP resumption 按预期生效

### **MCP Server 日志证据**
```bash
🏪 Stored event abc123 in stream 1          # Initialize response
🏪 Stored event def456 in stream _GET_stream # Tool result (different stream!)
🔄 Checking stream 1 with 1 events          # Same stream - no new events
🔄 Checking stream _GET_stream with 1 events # Different stream - found tool result!
🔄 Found event to replay: def456 in different stream _GET_stream
🔄 Sending event: def456 from stream _GET_stream
```

## 🎓 **学习收获**

跑完这些测试后，学生会理解：

- ✅ MCP 初始化如何建立连接
- ✅ 为什么真实系统里会发生网络超时
- ✅ `Last-Event-ID` 如何实现 MCP resumption
- ✅ **Cross-stream event correlation**（关键技术突破）
- ✅ GET 请求如何获取缓存结果
- ✅ MCP 如何做到“不丢进度”

## 🔧 **故障排查**

### **常见问题**

1. **Server 未启动**
   ```bash
   uv run server.py  # 先启动 server
   ```

2. **Test 3 没有超时**
   - 检查 timeout 是否设置为 2000ms（2 秒）
   - server 延迟是 6 秒，因此按理一定会超时
   - 查看是否出现 `"Connection timed out as expected"` 这类提示

3. **Event ID 没有被跟踪**
   - 查看 Test Results 标签页中的 console logs
   - 检查是否有 `"Event ID captured"` 相关输出

4. **Test 4 失败**
   - 确保 Tests 1-3 已成功执行
   - 检查 Test 4 中是否正确带上了 `Last-Event-ID` Header
   - 确认 Test 1 中已成功捕获 event ID 变量

## 🔍 **如何验证 MCP Resumption**

### **方法 1：分析 Server 日志**
观察这些日志模式：
```bash
🔄 Replaying events after [event-id]
🔄 Found event to replay: [new-event-id] in different stream [stream-name]
🔄 Sending event: [new-event-id] from stream [stream-name]
```

### **方法 2：响应内容中的标记**
工具结果中会包含明确证据：
```json
{
  "result": "The weather in Tokyo will be warm and sunny! ☀️ (Retrieved via resumption)",
  "indicator_date": "2025-06-18T04:42:55.711075"
}
```

其中 **"Retrieved via resumption"** 证明 server 回放了缓存结果。

### **方法 3：时间分析**
- **Fresh call**：6 秒以上（server 实际处理时间）
- **Resumed call**：约 100ms（读取缓存结果）

## 💡 **整体理解**

这个 collection 教给学生的是：
- **网络问题一定会发生**（Test 3 的超时）
- **跨 stream 事件可以被关联起来**（关键技术点）
- **MCP resumption 可以跨 stream 工作**（Test 4 成功）
- **不会丢失工作结果**（同一工具调用，立即取回缓存结果）
- **Last-Event-ID 是关键**（这是 MCP 规范中支持跨流回放的核心 Header）

## 🎯 **测试序列总结**

| 测试 | 目的 | 预期结果 |
|------|---------|----------------|
| 1 | 初始化 | ✅ 获取 session 和 event ID |
| 2 | 完成握手 | ✅ 建立连接 |
| 3 | 工具调用（超时） | ⏰ 超时（模拟网络问题） |
| 4 | MCP 恢复 | ✅ 使用 GET + Last-Event-ID 成功恢复 |

这非常适合学习 **MCP Cross-Stream Resumption** 的基础原理。🚀

---

## 📋 **总结**

**这教会你什么**：MCP 规范中的恢复机制，只需 4 步即可理解  
**为什么重要**：真实 agent 在生产环境中一定会遇到网络问题  
**技术核心**：Cross-stream event correlation 让恢复可靠可行  
**关键学习点**：GET + Last-Event-ID Header 完全遵循 MCP 规范  
**结果**：学生能理解面向生产环境的高韧性 AI agent 通信方式 🌍
