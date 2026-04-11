# MCP Pagination Postman 测试 🧪

这个 Postman collection 提供了一种简单、可动手操作的方式，用来测试符合规范的、基于游标的分页。

## 🚀 **快速准备**

### 1. 导入 Collection

1. 打开 Postman
2. 点击 `Import`，选择 `MCP_Pagination_Tests.postman_collection.json`
3. 导入后 collection 会出现在你的工作区中

### 2. 启动 MCP Server

在终端中进入 `mcp_pagination_server` 目录并启动 server：

```bash
# From the 12_pagination directory
cd mcp_pagination_server
uv run server.py
```

server 会运行在 `http://localhost:8000`。

## 🧪 **分页测试流程**

这个 collection 演示如何使用 cursor 对大型工具列表进行分页读取。

1. **`1. Initialize Session`**：这是你首先要发送的请求。它会与 server 建立 session，并自动保存 `mcp-session-id`，同时清除上次测试遗留的旧 cursor。

2. **`2. List Tools (First Page)`**：这个请求会获取第一页工具。它的测试脚本会自动从响应中找到 `nextCursor`，并把它保存到 collection 变量中。

3. **`3. List Tools (Next Page)`**：这个请求会使用 `{{nextCursor}}` 变量向 server 请求下一页。你可以**重复运行这个请求**，直到遍历完整个工具列表。每次发送后，测试脚本都会自动更新 `nextCursor` 变量。

当到达列表末尾时，server 将不再返回 `nextCursor`，变量会被清空，后续请求将返回空的工具列表。你可以打开 Postman Console，观察 cursor 是如何被设置与更新的。
