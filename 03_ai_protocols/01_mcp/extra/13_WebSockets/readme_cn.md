# WebSockets：全双工实时通信

WebSockets（RFC 6455）提供的是**基于单条长连接的全双工通信**。一旦握手完成，客户端和服务端都可以随时发送消息，因此非常适合聊天、实时协作、推送数据、控制通道等场景。

---

## 核心概念

1. **HTTP Upgrade 握手**
   WebSocket 连接最开始是一个普通 HTTP 请求，通过 `Upgrade: websocket` 升级为 WebSocket 连接。

2. **持久连接**
   握手后连接持续存在，直到一方主动关闭。

3. **全双工**
   双方都可以独立、异步地发送消息。

4. **帧与消息**
   WebSocket 在 TCP 之上定义了自己的 frame 类型：
   - text
   - binary
   - ping / pong
   - close

5. **子协议**
   可通过 `Sec-WebSocket-Protocol` 协商应用层协议，例如 JSON-RPC over WebSocket。

6. **安全模式**
   - `ws://`
   - `wss://`（基于 TLS）

---

## Python 中使用 WebSockets：`websockets`

### 安装

```bash
pip install websockets
```

### 原文中的示例

原文给了两个最基础的 `asyncio` 示例：

1. **`websocket_server.py`**
   - 监听 `ws://localhost:8765`
   - 接收客户端消息
   - 原样回显
   - 维护连接集合

2. **`websocket_client.py`**
   - 连接服务端
   - 发送几条测试消息
   - 打印回显
   - 最后主动关闭连接

这组代码非常适合理解：

- 服务端如何接入连接
- 客户端如何发送 / 接收
- 持久连接与异步消息处理的基本模式

---

## 优势

- 低延迟
- 真正的双向实时通信
- 一次握手后开销较低
- 浏览器支持广，服务端生态成熟
- 适合状态化长连接场景

## 局限

- 服务端维护大量长连接时有资源压力
- 节点故障时连接状态恢复较麻烦
- 如果只需要单向推送，可能比 SSE 更复杂
- 应用层通常要自行处理消息 ID、请求响应匹配等逻辑

---

## 常见用途

- 实时聊天
- 在线游戏
- 协同编辑
- 实时通知
- 控制面板和状态监控

---

## WebSockets 在 DACA / A2A 中的意义

当 agent 之间需要：

- 持续在线对话
- 低延迟双向消息交换
- 双方都可能主动发起消息
- 长时间保持会话上下文

WebSocket 往往是很直接的选择。

对比来看：

- **SSE** 更适合单向推送
- **Streamable HTTP** 更适合 HTTP 风格的请求 / 流式响应
- **gRPC streaming** 更适合强类型服务间调用
- **消息队列** 更适合解耦和离线可靠传递

WebSocket 的定位是：**在线、实时、双向、状态化**。

---

## 协议栈位置

- **层级**：应用层
- **下层**：TCP
- **握手阶段**：HTTP/1.1 Upgrade
- **安全场景**：TLS + `wss://`

---

## 进一步阅读

- [RFC 6455: The WebSocket Protocol](https://datatracker.ietf.org/doc/html/rfc6455)
- [MDN WebSockets API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
- [`websockets` Python Docs](https://websockets.readthedocs.io/en/stable/)
