# 使用 Postman Collection

这个 Postman Collection 允许你以交互方式测试 MCP 进度通知服务器。

## 如何使用

1. **导入 Collection**：把 `MCP_Progress_Notifications.postman_collection.json` 文件导入到 Postman。
2. **启动服务器**：确保 Python 服务器已经运行（`uv run server.py`）。
3. **运行请求**：按 Collection 中的顺序依次执行请求。

## 观察进度

关键请求是 **"Call 'download_file' with Progress"**。当你发送这个请求时：

1. Postman 会保持连接打开，并等待响应返回。
2. 你会看到 `notifications/progress` 事件实时流入响应体。
3. `tools/call` 的最终 `result` 会出现在流的末尾。

这是理解原始 MCP 消息的好方法，也能帮助你直观看到服务器是如何在长时间运行的操作过程中，持续向客户端推送更新的。
