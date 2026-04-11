# MCP Completions Server - Postman 测试（有状态）

这个 collection 演示如何通过 HTTP 端点，以有状态生命周期方式测试 MCP completions。

## 🚀 快速开始

### 1. 启动 Server
```bash
cd mcp_completions_server
uv run server.py
```
Server 运行在 `http://localhost:8000`

### 2. 运行 Collection
1. **导入 Collection**：把这个文件导入 Postman。
2. **按顺序执行生命周期请求**：按 `"1. Connection Lifecycle"` 文件夹中的顺序依次运行。
   - `Initialize Connection` 请求会自动捕获并设置 collection 变量 `mcp_session_id`
3. **测试 Completions**：运行 `"Prompt Completions"` 或 `"Resource Completions"` 文件夹中的任意请求。它们会自动使用捕获到的 session ID。

## 🎯 测试流程

这个 collection 是按 MCP session 生命周期组织的：

### 1. Connection Lifecycle
- **Initialize Connection**：与 server 建立 session，并获取 session ID
- **Send Initialized Notification**：通知 server，client 已准备好

### 2. Server Discovery
- **List Prompts / Resources**：询问 server 在当前 session 中有哪些 prompts 和 resources 可用

### 3. Completions
- 分别运行 prompt 与 resource 的 completion 请求。每个请求本质上都是对 `/mcp/` 端点发起的 JSON-RPC 调用。

## 📚 学习点

### 1. 有状态生命周期
- 所有通信都在一个由 `mcp-session-id` 标识的 session 中完成
- 在发起其他调用之前，`initialize` 请求是必需的

### 2. JSON-RPC 格式
- `initialize` 之后的所有请求都是发往 `/mcp/` 的 `POST` 请求，并带 JSON-RPC body
- `method` 字段指定要执行的操作（例如 `complete`、`prompts/list`）
- `params` 字段承载对应方法的参数

### 示例 `complete` 请求：
```json
{
    "jsonrpc": "2.0",
    "id": 10,
    "method": "complete",
    "params": {
        "ref": { "type": "ref/prompt", "name": "review_code" },
        "argument": { "name": "language", "value": "py" }
    }
}
```

### 3. 自动化 Session 处理
- `Initialize Connection` 请求中的测试脚本会自动处理 session ID：
    ```javascript
    const sessionId = pm.response.headers.get('mcp-session-id');
    pm.collectionVariables.set('mcp_session_id', sessionId);
    ```
- 所有后续请求都在 Header 中使用 `{{mcp_session_id}}`

## 🔧 自定义方式

- 要开始新的测试 session，只需重新运行 `Initialize Connection`
- 想增加新的 completion 测试，可以复制一个现有请求，再修改请求体中的 `params`

## 🎓 下一步

- **探索错误场景**：尝试用无效 session ID 发送 `complete` 请求，观察 server 返回什么
- **查看其他示例**：阅读项目中的其他 Postman collection，了解更复杂的生命周期交互方式
