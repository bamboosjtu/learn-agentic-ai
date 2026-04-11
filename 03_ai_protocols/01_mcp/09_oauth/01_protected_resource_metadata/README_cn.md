# 01：Protected Resource Metadata

## 本节你将学到什么

这一步聚焦于 [RFC 9728](https://datatracker.ietf.org/doc/rfc9728/) 中定义的 **Protected Resource Metadata Discovery**。

你正在实现 OAuth 两阶段发现流程中的**前半部分**。目标是理解：当一个 MCP server 作为“Protected Resource（受保护资源）”时，它如何宣告自己的安全要求，并告诉 client 去哪里找到 Authorization Server。

完成本课后，你将理解并实现如下流程：
1. client 在没有 token 的情况下请求一个受保护工具
2. MCP server 用 `401 Unauthorized` 拒绝请求
3. client 检查错误响应中的 `WWW-Authenticate` Header
4. client 拉取 server 的 metadata 文件（`/.well-known/oauth-protected-resource`）
5. client 从该文件中得知 Authorization Server 的 **URL**（`http://localhost:9000`）

**注意：** 这一步只负责发现 Authorization Server 的位置。第 02 步才会去查询这个 server，获知它的具体端点。

---

## 学习目标

完成本模块后，你将能够：
1. 按照 MCP 规范实现 Protected Resource Metadata
2. 理解 OAuth 2.1 发现流程的第一阶段
3. 理解 client 如何发现 Authorization Server 的位置

## 标准合规性

本实现遵循以下规范：
- [MCP Authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)
- [OAuth 2.1](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/)
- [OAuth 2.0 Protected Resource Metadata (RFC 9728)](https://datatracker.ietf.org/doc/rfc9728/)

## 前置知识

- 对 HTTP 和 REST API 有基础理解
- 具备 Python 使用经验

## 核心概念

### 1. Protected Resource Metadata（RFC 9728）
- **目的：** 标准化 client 如何从 Resource Server 发现 OAuth 配置
- **要求：**
  - MCP server **必须**暴露 `/.well-known/oauth-protected-resource`
  - 文档中**必须**包含 `authorization_servers` 字段
  - server 在返回 401 时**必须**使用 `WWW-Authenticate` Header
  - client **必须**能够解析 `WWW-Authenticate` Header

### 2. 发现流程的第一阶段
- **发生的事情：**
  1. client 向 MCP server 发起未认证的 JSON-RPC 请求
  2. server 返回 401 + `WWW-Authenticate` Header
  3. client 从 MCP server 拉取 `/.well-known/oauth-protected-resource`
  4. client 从 metadata 中提取 Authorization Server URL

### 3. Resource 参数实现
- **要求：**
  - client 在后续 token 请求中**必须**携带 `resource` 参数
  - 该参数**必须**标识目标 MCP server
  - 必须使用规范化 URI 格式
  ```
  &resource=https%3A%2F%2Fmcp.example.com
  ```

### 4. Token 要求（后续步骤会实现）
- **Bearer Token 用法：**
  ```http
  POST /mcp HTTP/1.1
  Host: mcp.example.com
  Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
  ```
- token **不能**放在 URI query string 中
- 每个请求都需要授权

## 实现指南

### 运行 Demo
1. **启动 MCP Server：** 在一个终端中进入 `mcp_code` 目录，运行：
   ```bash
   uv run uvicorn serve:mcp_app --reload
   ```
2. **运行 Client：** 在第二个终端中，也进入 `mcp_code` 目录，运行：
   ```bash
   uv run client.py
   ```

client 的输出会展示：
1. 未认证请求返回的 `401 Unauthorized`
2. 从 `/.well-known/oauth-protected-resource` 拉取到的 metadata 文档
3. 发现出的 Authorization Server URL：`http://localhost:9000`

## 下一步

当 Authorization Server URL 发现完成后，第 02 步会继续：
1. **创建一个简单的 Authorization Server**，运行在 `http://localhost:9000`
2. **查询它的 metadata endpoint**（`/.well-known/oauth-authorization-server`）以发现具体端点
3. **完成 MCP 规范要求的两阶段发现流程**

这种两阶段方案允许一个 Authorization Server 服务多个 MCP Server，同时保持职责清晰分离。

## 参考资源

- [MCP Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)
- [OAuth 2.1 Specification](https://oauth.net/2.1/)
- [RFC 9728 - Protected Resource Metadata](https://datatracker.ietf.org/doc/rfc9728/)


