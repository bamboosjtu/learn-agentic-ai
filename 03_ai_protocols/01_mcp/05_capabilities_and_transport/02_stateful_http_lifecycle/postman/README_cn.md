# 📮 MCP 生命周期的 Postman 测试指南

本目录包含用于测试完整 Model Context Protocol（MCP）连接生命周期的 Postman Collection，内容遵循 [MCP 2025-06-18 生命周期规范](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle)。

## 🎯 你将学到什么

- 测试完整的 MCP 连接生命周期阶段
- 使用正确的 JSON / HTTP Header 进行协议版本协商
- 验证能力协商
- 通过 HTTP Header 进行会话管理
- 测试错误场景

## 📋 前置条件

1. **启动 MCP 服务器**：
   ```bash
   cd ../hello-mcp
   uv run server.py
   ```
   服务器运行在 `http://localhost:8000`

2. **导入 Collection**：
   - 导入 `MCP_Lifecycle_Tests.postman_collection.json`

## 🔄 MCP 生命周期测试（2025-06-18 规范）

### **阶段 1：初始化**

**请求**：`POST http://localhost:8000/mcp/`
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-06-18",
        "capabilities": {
            "roots": {
                "listChanged": true
            },
            "sampling": {},
            "elicitation": {}
        },
        "clientInfo": {
            "name": "postman-test-client",
            "title": "Postman Test Client",
            "version": "1.0.0"
        }
    }
}
```

**期望响应**：
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "protocolVersion": "2025-06-18",
        "capabilities": {
            "logging": {},
            "prompts": {"listChanged": true},
            "resources": {"subscribe": true, "listChanged": true},
            "tools": {"listChanged": true},
            "completions": {}
        },
        "serverInfo": {
            "name": "weather",
            "title": "Weather Forecast Server",
            "version": "1.0.0"
        }
    }
}
```

**关键 Header**：
- `Content-Type: text/event-stream`
- `mcp-session-id: <uuid>`

### **阶段 2：initialized 通知**

**请求**：`POST http://localhost:8000/mcp/`
```json
{
    "jsonrpc": "2.0",
    "method": "notifications/initialized"
}
```

**必需 Header（依据 2025-06-18 规范）**：
```http
Content-Type: application/json
Accept: application/json, text/event-stream
MCP-Protocol-Version: 2025-06-18
mcp-session-id: <session-id-from-init>
```

**期望响应**：`202 Accepted`

### **阶段 3：运行阶段**

#### 列出工具
**请求**：
```json
{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {},
    "id": 2
}
```

**必需 Header**：
```http
MCP-Protocol-Version: 2025-06-18
mcp-session-id: <session-id>
```

#### 调用工具
**请求**：
```json
{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
        "name": "get_forecast",
        "arguments": {
            "city": "San Francisco"
        }
    },
    "id": 3
}
```

### **阶段 4：关闭**

**依据 MCP 2025-06-18 规范**：
- **“未定义专门的关闭消息”**
- **“对于 HTTP 传输，关闭通过断开关联的 HTTP 连接来表示”**

因此，当 HTTP 连接关闭时，连接终止会自动发生。

## 🧪 测试场景

### ✅ **成功场景**
1. **完整生命周期**：Initialize → Initialized → List Tools → Call Tool →（关闭连接）
2. **协议版本**：JSON 中使用 `"2025-06-18"`，HTTP Header 中使用 `2025-06-18`
3. **会话持久性**：在多个请求中复用同一个 session ID
4. **Header 合规性**：初始化之后带上 `MCP-Protocol-Version` Header

### ❌ **错误场景**
1. **缺少协议 Header**：省略 `MCP-Protocol-Version` Header
2. **无效协议版本**：使用不支持的版本，例如 `"1.0.0"`
3. **错误的 JSON**：发送非法 JSON-RPC

## 📊 期望结果

| 测试用例 | 期望状态 | 关键 Header | 备注 |
|-----------|----------------|-------------|-------|
| Initialize | 200 OK | `text/event-stream`, `mcp-session-id` | SSE 格式 |
| Initialized | 202 Accepted | 标准 Header | 仅通知 |
| Tools List | 200 OK | `text/event-stream` | 返回工具数组 |
| Tool Call | 200 OK | `text/event-stream` | 返回天气结果 |
| Shutdown | N/A | N/A | 关闭 HTTP 连接 |

## 🔧 关键协议要点

### **协议版本的用法（2025-06-18）**
- **JSON 请求中**：使用 `"protocolVersion": "2025-06-18"`
- **HTTP Header 中**：使用 `MCP-Protocol-Version: 2025-06-18`
- 这与官方规范示例完全一致

### **初始化之后的必需 Header**
`initialize` 之后的所有请求都 **必须** 带上：
```http
MCP-Protocol-Version: 2025-06-18
mcp-session-id: <session-id>
```

### **能力结构**
在 2025-06-18 版本中增强了：
- `clientInfo` / `serverInfo` 中的 `title` 字段
- 用于自动补全的 `completions` 能力
- 更细粒度的选项，例如 `listChanged`、`subscribe`

## 🚀 快速测试流程

1. 导入 `MCP_Lifecycle_Tests.postman_collection.json`
2. 启动 MCP 服务器：`uv run server.py`
3. 按顺序运行请求：
   - **Initialize** → 自动捕获 session ID
   - **Initialized** → 使用前一步捕获的 session ID
   - **List Tools** → 查看可用工具
   - **Call Tool** → 执行天气预报工具

4. 观察完整的 MCP 2025-06-18 生命周期。

## 📚 参考资料

- [MCP 2025-06-18 生命周期](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle)
- [HTTP 传输要求](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#protocol-version-header)
- [JSON-RPC 2.0 规范](https://www.jsonrpc.org/specification)

---

**说明**：2025-06-18 规范在 JSON 示例中使用 `"2025-06-18"`，并将自己称作 2025-06-18 修订版。这就是当前规范对应的官方协议版本。✅
