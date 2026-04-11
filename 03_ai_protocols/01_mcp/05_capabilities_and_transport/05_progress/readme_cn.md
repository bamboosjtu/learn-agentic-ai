# 📊 MCP Progress Notifications

> **类比：** 想象你点了一份披萨。糟糕的服务只会告诉你“订单已接收”，然后你只能焦虑地等着。好的服务会实时告诉你：“正在和面”、“正在加配料”、“已入炉”、“正在配送！” 你会感觉更踏实，也更有掌控感。MCP 的 Progress Notifications 对长时间运行的数字任务也是同样的作用。

本节会展示如何利用 MCP 的进度通知系统，把一个沉默的长任务变成透明、实时的交互体验。

## 🎯 你将学到什么

- **服务端**：如何在工具内部发送 `notifications/progress` 来报告当前状态。
- **客户端**：如何接收这些通知，并将它们展示给用户（例如显示成进度条）。
- **协议层面**：请求 `_meta` 字段中的 `progressToken` 如何把一次工具调用与它对应的进度更新流关联起来。
- **交互式测试**：如何使用 Postman 实时查看原始进度事件流。

---

## ▶️ 如何运行这个示例

你可以通过两种方式探索这个示例：使用简单的 Python 客户端，或者直接通过 Postman Collection 与服务器交互。

### 1. 启动服务器

首先，在 `02_server_engineering/08_progress/mcp_code` 目录中打开终端并运行：

```bash
# Install dependencies
uv sync

# Run the server
uv run uvicorn server:mcp_app --reload
```

服务器会在 `http://localhost:8000` 上启动并监听。

### 2. 选择你的客户端

#### A) 运行 Python 客户端

在**新的终端**中运行 Python 客户端：

```bash
# (In the same mcp_code directory)
uv run client.py
```

**预期效果：**
你会看到客户端完成连接、列出工具，并运行两个场景。对于每个场景，都会出现一个实时更新的进度条，直到任务完成。

```
📁 File Download
----------------------------------------
    📊 [████████████░░░░░░░░] 60.0% - Downloading dataset.zip... 60.0%
    📊 [████████████████░░░░] 80.0% - Downloading dataset.zip... 80.0%
    ...
```

#### B) 使用 Postman Collection

如果你想直接看到原始协议消息，这是一个很好的方式。

1. **导入**：把 `postman/MCP_Progress_Notifications.postman_collection.json` 文件导入到 Postman。
2. **按顺序运行**：
   - `1. Connection Lifecycle` -> `Initialize Connection`：建立 session。
   - `1. Connection Lifecycle` -> `Send Initialized Notification`：通知服务器你已经准备好了。
   - `2. Long-Running Tools` -> `Call 'download_file' with Progress`：这就是关键请求。

**预期效果：**
当你发送 `download_file` 请求后，响应会是 `text/event-stream`。Postman 会逐条显示流式返回的 `notifications/progress` JSON 对象，最后再显示最终的 `result`。

---

## 🧠 核心概念

### 服务器：报告进度（`server.py`）

服务器中的工具可以使用 `FastMCP` 提供的 `ctx`（Context）对象轻松上报进度，而不需要手动处理 token。

```python
@mcp.tool()
async def download_file(filename: str, size_mb: int, ctx: Context) -> str:
    # ... setup ...
    for chunk in range(total_chunks + 1):
        # The magic is here! Just report progress on the context.
        await ctx.report_progress(
            progress=chunk,
            total=total_chunks,
            message=f"Downloading {filename}..."
        )
        await asyncio.sleep(0.1)
    return "Download complete"
```

### 客户端：处理进度（`client.py`）

高层的 `ClientSession` 让进度处理变得非常简单。你只需要传入一个回调函数，库会自动替你处理 token 和通知路由。

```python
async def progress_handler(progress: float, total: float | None, message: str | None):
    # ... logic to draw a progress bar ...
    print(f"📊 [{progress_bar}] {percentage:.1f}% - {message}")

# The magic is here! Just pass the handler to the call.
result = await session.call_tool(
    "download_file",
    {"filename": "dataset.zip", "size_mb": 5},
    progress_callback=progress_handler
)
```

### 协议：`progressToken`

在底层，客户端与服务器之间会传递一个 `progressToken`。客户端把它放在请求的 `_meta` 字段中，相当于告诉服务器：“这项任务的进度更新，请和这次调用关联起来。”

下面是 Postman Collection 发送的内容，这也是 Python 客户端自动完成的事情：

```json
{
    "jsonrpc": "2.0",
    "id": 101,
    "method": "tools/call",
    "params": {
        "name": "download_file",
        "arguments": { "...": "..." },
        "_meta": {
            "progressToken": 101 // Link this call to progress updates
        }
    }
}
```

之后服务器会返回带有相同 token 的通知：

```json
{
    "jsonrpc": "2.0",
    "method": "notifications/progress",
    "params": {
        "progressToken": 101, // This update is for request #101
        "progress": 5,
        "total": 10,
        "message": "Downloading..."
    }
}
```

---

## 💡 自己动手试试

1. **修改速度**：在 `server.py` 里调整工具中的 `asyncio.sleep()` 时间。这样会如何影响用户体验？
2. **未知总量**：修改 `process_data` 工具，在 `ctx.report_progress` 中**不要**传 `total`。观察 Python 客户端里的 `progress_handler` 会如何表现。
3. **新增工具**：在 `server.py` 里创建一个新的工具，用来模拟多步骤安装过程。它只返回不同步骤消息、不提供百分比。然后更新 `client.py` 去调用它。
