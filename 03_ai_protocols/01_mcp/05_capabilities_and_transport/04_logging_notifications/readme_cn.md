# [Logging - 服务器的声音](https://modelcontextprotocol.io/specification/2025-06-18/server/utilities/logging)

**目标：** 学习 MCP 服务器如何基于 **2025-06-18 规范**，通过结构化日志通知把自己的内部状态传达给客户端。

### 🤔 什么是 MCP Logging？（通俗解释）

你可以把 MCP logging 理解成：**给服务器装上一个声音**，让它能够告诉你自己在做什么。

**现实类比**：想象你在和朋友一起做饭。你不是默默做事，而是边做边说：
- “我在热油。”（info 级别）
- “洋葱正在慢慢变褐。”（debug 级别）
- “小心，锅越来越热了！”（warning 级别）
- “糟了，蒜烧糊了！”（error 级别）

**MCP Logging 也一样**：服务器会把自己的活动“讲出来”，帮助你理解发生了什么、排查问题，并监控性能表现。

### 📊 MCP 与常见技术的对比

| **技术** | **它做什么** | **MCP Logging 的优势** |
|----------------|------------------|---------------------------|
| **Console.log()** | 基础文本输出 | 结构化、标准化格式 |
| **Winston/Bunyan** | Node.js 日志 | 协议原生、面向客户端 |
| **Syslog** | 系统日志 | 更适合 AI、具备上下文 |
| **CloudWatch** | AWS 日志 | 面向 MCP 场景、可与工具集成 |

### 🎯 为什么这对 AI 开发很重要

1. **🔍 调试**：准确看到你的 AI agent 在做什么
2. **📊 监控**：追踪性能与行为模式
3. **🤝 透明性**：让用户看到他们的 AI 正在执行什么
4. **🛠️ 开发效率**：更快排障与优化

## 🎓 学习目标

完成本节后，你将能够：

### ✅ **概念理解**
- 解释什么是 MCP logging，以及它为什么重要
- 描述 8 个日志级别及其使用场景
- 理解 logging 和普通输出的区别

### ✅ **技术能力**
- 使用 `Context` 对象在服务端实现日志
- 创建能监听日志通知的客户端
- 动态设置和调整日志级别
- 处理带有元数据的结构化日志

### ✅ **实践应用**
- 用日志调试 MCP 服务器问题
- 实时监控 AI agent 行为
- 创建用户友好的日志展示界面
- 为性能优化日志策略

## 🌟 8 个沟通级别

基于 [RFC 5424](https://tools.ietf.org/html/rfc5424)，MCP 支持 8 个日志级别：

| 🎯 **级别** | 🎭 **何时使用** | 💡 **示例场景** | 📝 **样例消息** |
|-------------|-------------------|------------------------|----------------------|
| `emergency` | 系统不可用 | 完全故障 | "Database cluster down" |
| `alert` | 需要立即处理 | 关键组件故障 | "Memory usage at 95%" |
| `critical` | 严重条件 | 核心功能损坏 | "Authentication service offline" |
| `error` | 错误条件 | 某事失败了 | "Failed to process user request" |
| `warning` | 警告条件 | 潜在问题 | "API rate limit at 80%" |
| `notice` | 正常但重要 | 关键事件 | "User session started" |
| `info` | 信息性消息 | 一般信息 | "Processing 50 records" |
| `debug` | 调试级消息 | 详细追踪 | "Function entry: validateUser()" |


## 🛠️ 我们将构建什么

### **📡 智能日志服务器**（`server.py`）
- **结构化日志**：使用 MCP `Context` 进行规范日志输出
- **多日志级别**：演示全部 8 个严重级别
- **真实场景**：展示现实应用中的日志写法
- **性能跟踪**：记录耗时和资源使用

### **👂 监听型客户端**（`client.py`）
- **实时展示**：日志一产生就显示
- **级别过滤**：控制展示哪些消息
- **更友好的格式**：用颜色和 emoji 辅助阅读
- **交互控制**：动态切换日志级别

## 🔄 MCP Logging 如何工作

### **步骤 1：服务器声明能力**
```python
# Server tells client: "I can send you log messages"
capabilities = {
    "logging": {}
}
```

### **步骤 2：客户端设置偏好**
```python
# Client tells server: "Send me 'info' level and above"
await session.set_logging_level("info")
```

### **步骤 3：服务器发送结构化消息**
```python
# Server narrates what it's doing
await ctx.info("Processing user request", extra={
    "user_id": "123",
    "request_type": "weather",
    "processing_time": 0.5
})
```

### **步骤 4：客户端接收并展示**
```python
# Client formats and shows the message
def log_handler(params):
    print(f"📰 [INFO] Processing user request")
    print(f"    User: 123, Type: weather, Time: 0.5s")
```

## 🏗️ 实现指南

### **设置环境**
```bash
# Navigate to the lesson directory
cd mcp_code

# Install dependencies
uv sync

# Run the server (Terminal 1)
uv run uvicorn server:app --reload

# Run the client (Terminal 2)
uv run python client.py
```

### **测试不同场景**
```bash
# Test with different log levels
uv run python client.py --log-level debug
uv run python client.py --log-level info
uv run python client.py --log-level warning
```

## 📚 规范参考

- **MCP 2025-06-18 Logging 规范**：[官方文档](https://modelcontextprotocol.io/specification/2025-06-18/server/utilities/logging)
- **RFC 5424 Syslog**：标准日志级别与格式
- **JSON-RPC 2.0**：通知消息格式

## 🎓 评估问题

检验你的理解：

1. **概念题**：`warning` 和 `error` 级别有什么区别？
2. **技术题**：如何由客户端设置日志级别？
3. **实践题**：什么情况下你会使用 `debug` 级日志？
4. **设计题**：如果要记录一个多步骤流程，你会怎么设计日志？

## 🚀 下一步

掌握 logging 之后，你就可以继续学习：
- **07_tool_update_notification**：动态工具管理
- **08_progress**：长任务进度跟踪
- **09_ping**：连接健康状态监控

---

> **🎯 成功标准**：当你能够只通过读日志就解释服务器正在做什么，并且能根据需要控制可见细节级别时，就说明你已经掌握了本节内容。

准备好让你的 MCP 服务器开口说话了吗？开始吧。🎤
