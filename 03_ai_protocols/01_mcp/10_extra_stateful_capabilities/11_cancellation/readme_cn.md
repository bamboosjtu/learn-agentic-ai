# 11：🛑 MCP Request Cancellation

本课演示 client 如何取消 MCP server 上一个长时间运行的操作。这是构建高响应性、高效率 AI agent 的关键能力，它允许用户不必一直等待任务完成，而是直接中止不再需要的任务。

## 关键概念

MCP 通过一种基于通知、协作式的机制优雅地处理 cancellation。这比手动维护任务状态简单得多，也更稳健。

- ✅ **正确方式（MCP 原生）：** server 中的工具实现只需要处理 `asyncio.CancelledError`。`FastMCP` 框架会自动把来自 client 的取消通知传播到正确的 `asyncio.Task`。
- ❌ **错误方式（手动实现）：** 避免用全局字典手动追踪任务，或自己实现一套取消逻辑。框架已经帮你做了这些事。

### 它是怎么工作的

1. **Client 准备一个任务：** client 构造一个针对长任务的 `tools/call` 请求
2. **Client 获取 Request ID：** 在发送请求前，client 检查 `session` 对象，拿到*下一个*请求的 ID（例如 `session._request_id`）。这是不硬编码 ID 的正确做法。
3. **Client 启动任务并发送取消：** client 发出请求；与此同时，它在延迟一段时间后发送一条 `notifications/cancelled` 消息，其中包含前一步拿到的 `requestId`
4. **Server 处理取消：**
   - `FastMCP` 接收到通知后，找到与该 `requestId` 对应的 `asyncio.Task`
   - 它在那个正在运行的任务内部抛出一个 `asyncio.CancelledError`
   - 工具中的 `try...except asyncio.CancelledError` 捕获该异常、记录日志，并重新抛出
   - `FastMCP` 最终向 client 返回 `RequestCancelled` 错误响应（`-32800`）

## 文件

| 文件 | 用途 |
| -------------------------- | ------------------------------------------------------------------------------------------------------- |
| `mcp_code/server.py`       | 一个 `FastMCP` server，包含一个可取消的长任务工具 `process_large_file` |
| `mcp_code/client.py`       | 一个 Python client，它启动长任务，并在几秒后正确取消它 |
| `postman/`                 | 用于交互测试取消流程的 Postman collection |
| `postman/README.md`        | 使用该 Postman collection 的说明文档 |

## 如何运行这个示例

你可以通过 Python client 或 Postman collection 测试 cancellation 流程。

### 终端 1：启动 Server

首先启动 MCP server。它会监听 `http://localhost:8000`。

```bash
# From the 11_cancellation directory
cd mcp_code
uv run server.py
```

### 终端 2（方式 A）：运行 Python Client

Python client 会启动一个任务，等待 3 秒，然后取消它，并确认它已成功被取消。

```bash
# From the mcp_code directory
uv run client.py
```

**预期输出：**

```
🚀 Starting cancellable task demonstration...
✅ Connected to MCP server.
✅ Session initialized.
📁 Starting long-running task 'process_large_file'...
   (Task with request ID 1 will be cancelled in 3 seconds)
⏹️ Waited 3 seconds. Sending cancellation for request 1...
✅ Task 1 was successfully cancelled by the server!

🎉 Demo finished.
```

### 方式 B：使用 Postman Collection

如果你想更手动地操作，可以使用 `postman/` 目录中的 Postman collection。它允许你一步一步触发 cancellation 流程。详细步骤请看 `postman/README.md`。

## 🎯 学习路径

### 🟢 Beginner
- 运行 `simple_demo.py` 直观看到概念
- 理解任务生命周期和取消点
- 了解 asyncio task 管理

### 🟡 Intermediate
- 学习 FastMCP server 实现
- 探索基于工具的 cancellation 方式
- 测试 httpx client 示例

### 🔴 Advanced
- 正确实现 MCP notification 处理
- 为每个 session 增加任务追踪
- 构建面向生产的 cancellation 系统

## 🚀 快速开始

### 运行概念演示
```bash
# See all cancellation concepts in action
uv run simple_demo.py
```

这个完整 demo 会展示：
- ✅ 基础 cancellation 流程
- ✅ Race condition 处理
- ✅ 多个并发任务
- ✅ 资源清理

### 运行 MCP Server（可选）
```bash
# Terminal 1: Start server
uv run server.py

# Terminal 2: Test client
uv run httpx_client.py quick
```

## 📁 文件概览

| 文件 | 用途 |
|------|---------|
| `simple_demo.py` | 🎭 **完整概念演示**（推荐） |
| `server.py` | 🖥️ 带 cancellation 工具的 FastMCP server |
| `httpx_client.py` | 🔌 用于测试的简单 HTTP client |
| `client.py` | 📡 完整 MCP protocol client |
| `postman/` | 🧪 API 测试 collection |

## 🎭 Demo 输出

`simple_demo.py` 展示了三个场景：

### 1. 基础 Cancellation
```
🚀 Starting long-running task...
📊 Processing dataset.csv... 1/8 seconds
📊 Processing dataset.csv... 2/8 seconds  
⏹️ Cancelling task...
✅ Successfully cancelled task
❌ Processing was cancelled
```

### 2. Race Condition
```
🏁 Testing race condition...
⚠️ Task not found (may have already completed)
⚡ Quick response: This completes immediately
```

### 3. 多任务并发
```
🚀 Starting 3 concurrent tasks...
⏹️ Cancelling middle task...
📊 Final results:
  Task 0: ✅ Successfully processed
  Task 1: ❌ Processing was cancelled  
  Task 2: ✅ Successfully processed
```

## 🌍 真实世界应用

### 📊 数据处理
- 取消昂贵的数据库查询
- 停止大型文件处理任务
- 中断模型训练 / 推理

### 🤖 AI Agents
- 停止耗时过长的推理链
- 取消不再需要的工具执行
- 中断多步骤工作流

### 🌐 Web 服务
- 当用户离开页面时取消请求
- 当 client 断开时取消 API 调用
- 在优先级变化时停止批处理任务

## 🔧 关键实现细节

### 任务追踪
```python
# Global task registry
active_tasks: Dict[str, asyncio.Task] = {}

# Register task for cancellation
current_task = asyncio.current_task()
active_tasks[task_id] = current_task
```

### 取消点
```python
# Check for cancellation during processing
for i in range(processing_time):
    if task_id in active_tasks:
        await asyncio.sleep(1)  # Cancellation point
    else:
        return "Task was cancelled"
```

### 资源清理
```python
try:
    # Do work...
except asyncio.CancelledError:
    # Clean up resources
    if task_id in active_tasks:
        del active_tasks[task_id]
    return "Task cancelled"
```

## 📚 MCP 规范

本实现遵循 [MCP Cancellation Specification](https://spec.modelcontextprotocol.io/specification/server/cancellation/)。

关键点：
- ⚡ 取消应当**足够快**（< 1 秒）
- 🧹 资源必须被**正确清理**
- 🏁 **Race condition** 必须被优雅处理
- 📊 任务**状态追踪**必须准确

## 🎉 成功标准

跑完 demo 后，你应该理解：

✅ **如何追踪长时间运行任务**  
✅ **什么时候以及如何取消操作**  
✅ **如何处理 race condition**  
✅ **如何正确清理资源**  
✅ **如何构建高响应性的 AI agent**

## 🔗 下一步

- 📖 学习 MCP notifications，实现更规范的协议处理
- 🏗️ 构建生产级 cancellation 系统
- 🔧 集成到你的 AI agent 框架
- 📊 为任务生命周期增加 metrics 和 monitoring

---

💡 **关键洞察**：取消不仅仅是“停止任务”，而是在构建一种**响应迅速、节约资源、用户可控**的 AI agent。

# 11：Cancellation

**目标：** 学习 client 如何通过 `$/cancelRequest` notification 请求 server 取消一个长时间运行的操作。

这是提升用户体验的重要能力。它允许用户在不再需要某个操作时直接中止，而不必等到它自然结束。

## 关键 MCP 概念

- **`$/cancelRequest`（Notification）：** 一种从 client 发往 server 的通知，里面包含需要被取消的原始请求 `id`
- **协作式取消（Cooperative Cancellation）：** MCP 中的取消是协作式的。server 不是被强行打断，而是收到通知后在下一个合适时机优雅停止任务
- **`Context` 对象与 `ctx.is_cancelled`：** `FastMCP` 提供了非常简单的机制。当某个请求收到取消通知后，框架会在该请求的 `Context` 上设置一个标记。工具代码只需定期检查 `ctx.is_cancelled`，为 `True` 时就可以优雅退出
- **错误响应：** 成功取消后，通常应返回一个带 `-32800`（RequestCancelled）错误码的 `Error` 对象

## 实现计划

在 `mcp_code/` 子目录中：

- **`server.py`：**
  - 定义一个长任务工具，例如 `process_large_file()`，它在循环中运行
  - 在每轮循环开始时检查 `if ctx.is_cancelled:`
  - 如果为真，则停止处理、完成必要清理，并抛出 `CancelledError`。`FastMCP` 会捕获它并向 client 返回正确错误响应

- **`client.py`：**
  - client 调用 `process_large_file` 工具
  - 它会立刻得到该请求的 `id`
  - 在短暂延迟（例如 2 秒）后，在 server 仍在工作的情况下，client 会发送 `$/cancelRequest` notification，并带上刚才记录的 `id`
  - 然后 client 等待响应，并验证它收到了 `RequestCancelled` 错误，从而确认任务已成功中止
