# Streamable HTTP：通用流式 HTTP 与 MCP 传输

**Streamable HTTP** 指的是在 HTTP 连接上持续分块传输数据，而不是等完整响应生成后一次性返回。这种模式对现代 AI 系统很关键，因为它适合：

- LLM token 流输出
- 大数据分块处理
- 实时 agent 通信
- 持续更新的仪表盘与日志流

原文先讲一般 HTTP 流式传输，再介绍 **MCP 2025-03-26 规范中的 Streamable HTTP transport**。

---

## 通用的 HTTP 流式传输概念

### 1. Chunked Transfer Encoding

- HTTP/1.1 的标准能力
- 可以在不知道总长度的情况下逐块返回内容
- 适合日志流、大文件、增量结果

### 2. SSE

- 是一种专门面向服务端推送的流式 HTTP 方案
- 使用 `text/event-stream`
- 非常适合通知、状态更新、LLM 输出流

### 3. HTTP/2 / HTTP/3 的流能力

- **HTTP/2**：多路复用
- **HTTP/3**：基于 QUIC，进一步缓解阻塞问题

### 4. Long Polling

- 通过“请求挂起 + 重新请求”模拟服务端推送
- 比真正流式方案更低效

---

## MCP 中的 Streamable HTTP

MCP 新版规范使用**单一端点**（通常如 `/mcp`）承载 JSON-RPC 消息，并区分：

- **POST**：客户端向服务端发送 JSON-RPC
- **GET**：客户端打开 SSE 流，接收服务端主动推送

### POST 的作用

POST 可发送：

- request
- notification
- response
- batch

客户端通常需要带上：

- `Accept: application/json, text/event-stream`
- `Mcp-Session-Id`（如果已有会话）

服务端可能返回：

- `202 Accepted`：仅通知 / 响应类输入
- `application/json`
- `text/event-stream`

### GET 的作用

GET 用来建立 SSE 通道，以便服务端主动向客户端发：

- JSON-RPC request
- JSON-RPC notification

客户端应带：

- `Accept: text/event-stream`
- `Mcp-Session-Id`
- `Last-Event-ID`（断线恢复时）

---

## 为什么新版 MCP 采用这种方式

相对旧的双端点 `HTTP + SSE` 方案，新版设计的优点包括：

- **统一端点**
- **更清晰的会话管理**
- **支持同步 JSON 响应和异步 SSE 响应**
- **更符合现代 HTTP API 设计习惯**
- **更容易支持 resumability**

---

## 实践要点

### 对客户端

- 保存并复用 `Mcp-Session-Id`
- POST 时同时支持 JSON 与 SSE 响应
- GET 时实现自动重连与 `Last-Event-ID`

### 对服务端

- 校验 `Origin`
- 正确区分只含 notification / response 的 POST
- 为 SSE 事件附带 `id`，便于恢复

---

## 容易踩坑的地方

- 忘记带 `Accept` 或 `Mcp-Session-Id`
- 把 SSE 中断误认为取消
- 客户端只实现 JSON，不支持 SSE POST 响应
- 忽略 `Origin` 校验与认证

---

## 总结

Streamable HTTP 是 MCP 中非常关键的一层。它保留了 HTTP 的兼容性，又通过 JSON-RPC + SSE 支持了现代 agent 系统需要的流式、会话化和可恢复通信模式。
