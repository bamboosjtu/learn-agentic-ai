# 🔄 10：MCP Connection Resumption

> **类比：** 想象你在打一通很长的电话，结果信号中断了。当你重新拨回去时，你的朋友不是让你从头再说一遍，而是说：“你刚才断线前讲到……” 然后你们从中断的位置无缝继续。这就是 MCP Resumption。它让 client 在网络中断后，能够继续之前的 session，而不用丢失进度。

本课演示如何构建一个具备容错能力的 client，使它能够在连接中断后，通过 `Last-Event-ID` Header 恢复一个长时间运行的操作。

## 🎯 你将学到什么

- **Server 端：** 如何使用 `EventStore` 缓冲消息，让 server 在 client 重连时重放这些消息
- **Client 端：** 如何持久化 session 状态（session ID 和 last event ID），并在连接中断后用它来恢复
- **协议层面：** client 如何通过 `mcp-session-id` 和 `Last-Event-ID` Header 发起 resumption，以及 server 如何利用这些信息让 client 补齐遗漏内容
- **交互测试：** 如何使用 Postman 模拟连接中断和成功恢复

## ✨ “Cross-Stream Replay” 概念

MCP 规范是严格的：`The server MUST NOT replay messages that would have been delivered on a different stream.`  
但是为了教学，这里的 `InMemoryEventStore` 采用了更强但没那么严格遵循规范的做法：它会回放与当前 session 相关的**所有 stream** 中的消息。

这种 “cross-stream replay” 让 client 即使在最终结果是从另一个逻辑 stream 返回的情况下，也能恢复工具调用。它是构建高韧性系统时非常强大的模式，因此这里特意展示给你看。

## 🚀 如何运行这个示例

你可以使用简化版 Python client，或者配套的 Postman collection 来测试 resumption。

### 1. 启动 Server

首先启动 MCP server。它有一个带故意 6 秒延迟的工具（`get_forecast`），这样更容易模拟超时。

```bash
# In your terminal, from the 10_resumption directory
uv run uvicorn server:mcp_app --reload
```

### 2. 运行 Python Client（两步过程）

Python client 会模拟“崩溃并重启”。你需要运行它两次。

**第一次运行（模拟“崩溃”）：**

```bash
# This run will connect, start the tool call, and then "crash"
# before the server finishes. It saves its state in `.session_cache`.
uv run client.py
```

你会看到它初始化，然后退出。

**第二次运行（模拟“恢复”）：**

```bash
# Run the exact same command again.
# The client will find the .session_cache file, reconnect with the
# old session ID and last event ID, and instantly get the result.
uv run client.py
```

### 3. 使用 Postman Collection

如果你想更直观地操作，可以使用附带的 Postman collection。

1. **导入 Collection**：把 `postman/MCP_Resumption_Tests.postman_collection.json` 导入 Postman
2. **按照 `README.md` 操作**：打开 collection 文档（或者阅读 `postman/POSTMAN_README.md`），按照它给出的步骤顺序执行，以模拟 session 中断并成功恢复
