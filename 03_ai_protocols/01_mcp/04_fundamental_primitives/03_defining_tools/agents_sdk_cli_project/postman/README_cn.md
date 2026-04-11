# MCP Tools 定义 - Postman Collection

这个 Postman Collection 提供了一套较完整的测试用例，用于验证 MCP tools 的实现，重点测试文档读取工具和文档编辑工具。

## 🚀 快速开始

### 前置要求

1. **Postman**：从 [Postman](https://www.postman.com/downloads/) 下载并安装
2. **MCP Server**：确认 Server 运行在 `http://localhost:8000/mcp/`

### 环境准备

1. **导入 Collection**：将 `MCP_Defining_Tools.postman_collection.json` 导入 Postman
2. **环境变量**：Collection 使用 `{{server_url}}` 变量，默认值为 `http://localhost:8000/mcp/`
3. **启动 Server**：运行 `uv run uvicorn mcp_server:mcp_app --port 8000 --reload`

## 📋 测试请求

### 1. 初始化连接

- **目的**：使用正确的协议版本建立 MCP 连接
- **方法**：`POST`
- **请求体**：带 `2025-06-18` 协议版本的 JSON-RPC 2.0 `initialize` 请求
- **预期结果**：返回 200 状态码，并在结果中包含 Server capabilities

### 2. 列出可用工具

- **目的**：发现 MCP Server 提供了哪些工具
- **方法**：`POST`
- **请求体**：JSON-RPC 2.0 `tools/list` 请求
- **预期结果**：返回 200 状态码，并在结果中包含 `read_doc_contents` 和 `edit_document` 两个工具

### 3. 读取文档内容

- **目的**：测试文档读取工具
- **方法**：`POST`
- **请求体**：针对 `read_doc_contents` 的 JSON-RPC 2.0 `tools/call` 请求
- **参数**：`doc_id: "deposition.md"`
- **预期结果**：返回 200 状态码，结果中包含文档内容

### 4. 编辑文档

- **目的**：测试文档编辑工具
- **方法**：`POST`
- **请求体**：针对 `edit_document` 的 JSON-RPC 2.0 `tools/call` 请求
- **参数**：
  - `doc_id: "plan.md"`
  - `old_str: "implementation"`
  - `new_str: "execution"`
- **预期结果**：返回 200 状态码，并包含成功消息

### 5. 验证文档编辑结果

- **目的**：确认文档确实已被成功修改
- **方法**：`POST`
- **请求体**：针对 `read_doc_contents` 的 JSON-RPC 2.0 `tools/call` 请求
- **参数**：`doc_id: "plan.md"`
- **预期结果**：返回 200 状态码，文档内容中出现更新后的 `"execution"`，而不是 `"implementation"`

### 6. 测试错误处理

- **目的**：验证当文档不存在时的错误处理是否正确
- **方法**：`POST`
- **请求体**：针对 `read_doc_contents` 的 JSON-RPC 2.0 `tools/call` 请求
- **参数**：`doc_id: "nonexistent.md"`
- **预期结果**：返回 200 状态码，并在响应中包含“文档不存在”的错误信息

## 🧪 运行测试

### 方式 1：运行全部测试

1. 在 Postman 中打开这个 Collection
2. 点击 “Run collection” 按钮
3. 选择所有请求，然后点击 “Run MCP Defining Tools”

### 方式 2：逐个运行

1. 打开 Collection 中任意一个请求
2. 点击 “Send” 执行请求
3. 查看响应内容和测试结果

### 方式 3：自动化测试

1. 使用 Postman 的 Newman CLI 运行自动化测试：

```bash
newman run MCP_Defining_Tools.postman_collection.json
```

## 📊 测试结果

每个请求都包含自动化测试，用于验证：

- **状态码**：确保返回 200 OK
- **响应结构**：校验 JSON-RPC 2.0 格式是否正确
- **工具发现**：确认预期工具已暴露出来
- **工具执行**：验证工具调用结果是否正确
- **错误处理**：测试错误响应是否符合预期

## 🔧 故障排查

### 常见问题

1. **连接被拒绝**
   - 确认 MCP Server 已在 8000 端口启动
   - 检查环境变量中的 Server URL 是否正确

2. **找不到工具**
   - 确认 Server 已正确实现目标工具
   - 检查工具名是否完全匹配

3. **无效的 JSON-RPC**
   - 确认请求体符合 JSON-RPC 2.0 规范
   - 确认 `Content-Type` header 设置为 `application/json`

### 调试步骤

1. **查看 Server 日志**：检查服务端输出是否有报错
2. **检查请求格式**：确认 JSON-RPC 结构正确
3. **使用 MCP Inspector**：通过可视化方式辅助调试
4. **检查工具实现**：确认工具已正确使用装饰器注册

## 📚 相关资源

- [MCP Tools Specification](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
- [FastMCP Documentation](https://github.com/modelcontextprotocol/python-sdk)
