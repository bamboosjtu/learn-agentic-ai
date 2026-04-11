# 用于 MCP 学习的 Postman Collections

这个目录包含用于测试 MCP（Model Context Protocol）Server 的 Postman Collections 和说明文档。使用 Postman 是理解 JSON-RPC 协议和 MCP 消息流的一个很好的学习方式。

## 🎯 为什么用 Postman 学 MCP？

### 教学价值

- **可视化界面**：可以直接看到原始 HTTP 请求和响应
- **容易测试**：无需写代码也能测试不同场景
- **更容易理解**：可以清楚看到 header、body 和响应内容
- **交互式学习**：可以修改参数并立即看到结果
- **文档化友好**：内置示例和说明文档
- **易于分享**：很方便导出并分享给其他学习者

### 技术价值

- **JSON-RPC 可视化**：帮助理解协议结构
- **SSE 响应处理**：可以直观看到 Server-Sent Events 的工作方式
- **错误处理**：了解 MCP 如何处理不同错误场景
- **参数校验**：测试输入校验和 schema
- **Header 管理**：理解哪些 HTTP headers 是必需的

## 📋 前置条件

1. **安装 Postman**：从 [postman.com](https://www.postman.com/downloads/) 下载并安装
2. **启动 MCP Server**：确保你的 MCP Server 已经运行
3. **导入 Collection**：加载 `.postman_collection.json` 文件

## 🚀 快速开始

### 1. 启动 Hello MCP Server

```bash
cd hello-mcp
uv run uvicorn server:mcp_app --port 8000 --reload
```

### 2. 导入 Postman Collection

1. 打开 Postman
2. 点击 **Import** 按钮
3. 选择 `Hello_MCP_Server.postman_collection.json`
4. 导入后该 Collection 会出现在你的工作区中

### 3. 按顺序运行请求

按顺序执行请求，以理解一个符合规范的 MCP Client 交互流程：

1. **Initialize Session**：即使是无状态 Server，合规的 Client 也必须先发送这个请求
2. **Send Initialized Notification**：根据 `2025-06-18` 规范，初始化成功后必须发送
3. **List Available Tools**：发现 Server 提供了哪些工具

## 📚 Collection 概览

### 请求结构

每个请求都演示了 MCP 的关键概念：

```json
{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {},
    "id": 2
}
```

### 响应格式（Server-Sent Events）

```text
data: {"jsonrpc":"2.0","result":{"tools":[...]},"id":2}
```

### 必需的 Headers

- `Content-Type: application/json`
- `Accept: application/json, text/event-stream`
- `MCP-Protocol-Version: 2025-06-18`（用于 `initialize` 之后的请求）

## 🔍 理解这些请求

### 1. Initialize Request

**目的**：启动一次 MCP 交互。这是任何合规 Client 的 **强制第一步**。

**关键要素**：

- 方法：`initialize`
- `params` 中带有 `protocolVersion: "2025-06-18"`
- 包含 Client 的能力声明和信息
- Server 会返回协商后的版本和能力

### 2. Initialized Notification

**目的**：完成初始化序列（在 `2025-06-18` 规范中是必须的）。

**关键要素**：

- 方法：`notifications/initialized`
- 在成功收到 `initialize` 响应后发送
- 告诉 Server，Client 已准备好进入正常操作阶段

### 3. Tools List Request

**目的**：发现 Server 提供了哪些工具。

**关键要素**：

- 方法：`tools/list`
- 返回工具 schema，并包含 `title` 字段（这是 `2025-06-18` 规范中的新内容）
- 必须包含 `MCP-Protocol-Version: 2025-06-18` header

## 🧪 测试不同场景

### 试验不同的 Headers

- 删除必需的 headers
- 尝试不同的 Accept headers
- 用错误的 Content-Type 做测试

## 📊 Collection 特性

### 自动化测试

每个请求都带有测试脚本，用于：

- 验证 HTTP 状态码
- 解析 SSE 响应
- 校验 JSON 结构
- 检查预期字段是否存在

### 环境变量

- `baseUrl`：Server 地址，默认值为 `http://localhost:8000`

**测试愉快！**

记住：目标不是机械地跑完这些请求，而是通过动手实验真正理解 MCP 协议。不要只是点击发送，也要认真看响应内容、修改参数，并尝试一些边界情况。
