# Server-Sent Events（SSE）：面向实时推送的单向 Web 通信

SSE（Server-Sent Events）是一种标准的 Web 实时通信技术，允许服务端通过一条长连接持续向客户端推送文本事件。它本质上是**服务端到客户端的单向流**，非常适合通知、日志、状态更新、增量输出等场景。

---

## SSE 的基本工作方式

1. 客户端发起一个普通 HTTP `GET` 请求
2. 服务端返回 `Content-Type: text/event-stream`
3. 连接保持打开，服务端不断推送事件
4. 客户端逐条解析事件并处理

浏览器里通常用 `EventSource`，Python 里可以用 `httpx`、`requests` 等流式读取。

---

## 事件流格式

SSE 消息是 UTF-8 文本，常见字段包括：

- `event`：事件类型
- `data`：事件数据
- `id`：事件编号，可用于断线重连
- `retry`：建议重连间隔

以 `:` 开头的行是注释，常用于 keep-alive。

示例：

```text
: keep alive

event: update
data: {"status":"ok"}
id: 1
```

---

## Python 实现：FastAPI + `httpx`

### 服务端

原文给出了一个可运行的 FastAPI SSE 服务：

- `GET /sse_stream`
  - 建立 SSE 连接
  - 发送 `connection_confirmation`
  - 定时发送 mock AI agent 消息
  - 使用注释行做 keep-alive

- `POST /send_message`
  - 客户端通过普通 POST 发送消息
  - 服务端把确认消息放入该会话对应的队列
  - 再通过 SSE 回推 `message_receipt`

这体现了 SSE 的典型用法：

- **服务端推流**
- **客户端回传数据时走另一个 HTTP 通道**

### 客户端

原文中的 `python_sse_client.py` 使用 `httpx.AsyncClient`：

- 打开流式 GET
- 逐行解析 SSE 消息
- 获得 `session_id`
- 再调用 `POST /send_message`
- 持续接收服务端确认与 mock agent 消息

---

## 优势

- 简单，特别适合服务端单向推送
- 基于 HTTP，部署门槛低
- 浏览器原生支持，客户端实现成本低
- 对 LLM / agent 的流式输出很自然

## 局限

- 连接本身是单向的
- 二进制数据不方便，通常要编码
- 某些代理或中间层可能缓冲流
- 在 HTTP/1.1 下浏览器并发连接数有限

---

## SSE 在 A2A / DACA 中的作用

SSE 适合以下模式：

- agent 持续向 UI 推送状态
- 一个 agent 向多个消费者广播通知流
- 实时日志、任务进度、推理 token 流输出

如果需要客户端频繁主动发消息，就应该搭配：

- 普通 HTTP POST
- WebSocket
- 或 Streamable HTTP / gRPC 等其他方案

对于 DACA 而言，SSE 很适合做“**服务端持续推送更新**”的轻量通道。

---

## 进一步阅读

- [MDN: Using server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server_sent_events)
- [FastAPI StreamingResponse](https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse)
- [httpx Streaming Responses](https://www.python-httpx.org/advanced/#streaming-responses)
