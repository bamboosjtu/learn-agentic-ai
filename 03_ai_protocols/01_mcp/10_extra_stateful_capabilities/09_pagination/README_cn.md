# 12：MCP Pagination

本示例演示如何为 `tools/list` 和 `resources/list` 请求实现服务端分页。这是任何管理大量条目的 MCP server 都非常关键的能力。分页允许 client 按较小、可管理的块来获取大数据集，从而提升性能和可靠性。

本课使用 `2025-06-18` MCP 规范要求的 **cursor-based（基于游标）** 分页模型。我们使用底层 `mcp.server.lowlevel.Server` 来手动演示分页逻辑的实现，并结合 `StreamableHTTPSessionManager` 将它暴露为 Web 服务。

这个 server 暴露了 150 个虚拟 tools 和 resources，client 每页抓取 20 个。


## 关键概念

- **基于游标的分页（Cursor-Based Pagination）**：server 在响应中提供一个不透明的 `nextCursor`。client 在下一次请求时把这个 cursor 带回来，以获取后续页面。
- **有状态游标（Stateful Cursor）**：cursor 实际上是一个经过 base64 编码的 JSON 字符串，内部包含下一页页码。这样 server 虽然本身保持无状态，但 client 依然能带着这个 cursor 从上次中断处继续。
- **PaginatedRequest**：`mcp.types.ListToolsRequest` 和 `mcp.types.ListResourcesRequest` 都继承自 `PaginatedRequest`，它为 client 提供 `params` 字段，用于发送 cursor。

## 如何运行这个示例

### 1. 启动 Server

进入当前目录并启动 Uvicorn server：

```sh
cd mcp_pagination_server
uvicorn server:app --reload
```

server 会运行在 `http://127.0.0.1:8000`。

### 2. 运行 Client

在另一个终端中运行 Python client：

```sh
cd mcp_pagination_server
uv run python client.py
```

你会看到 client 连接到 server，并用 8 页把 150 个 tools 全部拉取下来（7 页每页 20 个，最后 1 页 10 个）。

### 3. 使用 Postman 测试

你也可以使用配套的 Postman collection 来测试这个 server 的分页端点。

1. 在 Postman 中导入 `postman/` 目录里的 collection
2. 运行 `"Get Tools (Page 1)"` 请求
3. 从响应体中复制 `nextCursor`
4. 把它粘贴到 `"Get Tools (Page 2)"` 请求体中的 `cursor` 字段，再发送请求
5. 重复这个过程，逐页遍历全部 tools
