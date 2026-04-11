# 教程：在 MCP Streamable HTTP 中使用 GET 与 POST

这份文档解释的是 MCP 规范（2025-03-26 版本）里的 **Streamable HTTP** 传输方式。它使用单个 HTTP 端点承载 JSON-RPC 消息，并通过 `POST` 与 `GET` 两种方法完成双向通信。

---

## 1. 总览

在 MCP 的 Streamable HTTP 中：

- **POST**
  - 客户端向服务端发送 JSON-RPC
  - 可以是 request / notification / response / batch

- **GET**
  - 客户端建立 SSE 流
  - 服务端可主动推送 JSON-RPC request / notification

这套设计把旧版多端点方式合并为一个统一入口，例如 `/mcp`。

---

## 2. POST 的使用方式

### 目的

POST 是客户端把 JSON-RPC 消息送给服务端的主要方式。

### 请求时通常需要带上

- `Accept: application/json, text/event-stream`
- `Mcp-Session-Id`（如果已有会话）
- `Content-Type: application/json`

### 服务端可能如何响应

#### 如果 POST 里只有 notification 或 response

- 成功时返回 `202 Accepted`
- 失败时返回 HTTP 错误

#### 如果 POST 里包含 request

服务端必须返回以下之一：

- `application/json`
- `text/event-stream`

也就是说，**客户端必须同时支持 JSON 与 SSE 两种响应形式**。

### 会话管理

如果初始化阶段服务端发出了 `Mcp-Session-Id`，客户端后续所有请求都必须带上它。

---

## 3. GET 的使用方式

### 目的

GET 用于让客户端打开一条 SSE 通道，接收服务端主动推送的 JSON-RPC 消息。

### 常见请求头

- `Accept: text/event-stream`
- `Mcp-Session-Id`
- `Last-Event-ID`（恢复断线流时）

### 服务端响应

- 如果支持 SSE：返回 `text/event-stream`
- 如果不支持：返回 `405 Method Not Allowed`

### 可恢复性

如果流断开，客户端可以通过 `Last-Event-ID` 重新连接，让服务端从某个事件之后继续推送。

---

## 4. POST 与 GET 的区别

| 维度 | POST | GET |
| :-- | :-- | :-- |
| 主要用途 | 客户端发消息给服务端 | 客户端打开 SSE 流 |
| 典型载荷 | JSON-RPC body | 无 body |
| 服务端响应 | 202 / JSON / SSE | SSE 或 405 |
| 场景 | 主动调用、上报、应答 | 服务端主动通知 |

---

## 5. 实践建议

### 对客户端

- 保存 `Mcp-Session-Id`
- POST 时同时支持 JSON 与 SSE
- GET 时实现断线重连
- 正确处理 `Last-Event-ID`

### 对服务端

- 校验 `Origin`
- 正确区分不同 POST 载荷类型
- 为 SSE 流附上事件 ID
- 在合适时机关闭 SSE 流

---

## 6. 常见误区

- 以为 POST 只会返回 JSON，忽略 SSE
- 以为 SSE 中断就等于取消请求
- 忘记发送 `Mcp-Session-Id`
- 忽略认证与 DNS rebinding 风险

---

## 7. 总结

MCP 的 Streamable HTTP 通过：

- **POST 负责客户端发起**
- **GET + SSE 负责服务端主动推送**

形成了一套兼顾 HTTP 兼容性、流式能力、会话管理与断线恢复的现代协议设计，非常适合 agent、工具和模型之间的持续交互。
