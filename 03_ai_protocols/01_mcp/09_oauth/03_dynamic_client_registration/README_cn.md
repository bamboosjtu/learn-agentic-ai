# 03：Dynamic Client Registration

## 本节你将学到什么

这一步演示 [RFC 7591](https://datatracker.ietf.org/doc/rfc7591/) 中定义的 **Dynamic Client Registration**，从而完成 MCP 认证所需的 OAuth 2.1 发现与注册过程。

### 为什么 Dynamic Client Registration 对 MCP 很重要

[MCP Authorization 规范](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization.md) 强调 Dynamic Client Registration，原因在于：

- **无缝的 MCP 发现流程：** AI agent 可能会动态发现新的 MCP server，并需要自动完成注册
- **无需手动预配置：** 用户不应该为每一个可能出现的 MCP client 都手动注册
- **可扩展性：** 这支撑了 **DACA 愿景**，即 1000 万并发 agent 能够自动向 server 注册
- **贴近真实 AI 工作流：** agent 可以在没有人工干预的情况下连接新的 MCP server

### 基于前两步继续推进
1. **第 01 步：** 从 MCP server 发现 Authorization Server URL
2. **第 02 步：** 查询 Authorization Server 以发现它的端点

现在我们实现 **第 03 步**：使用 Keycloak 和 Initial Access Token 进行 Dynamic client registration。

---

## 学习目标

完成本模块后，你将能够：
1. 按 RFC 7591 实现 Dynamic Client Registration
2. 理解完整的三阶段 OAuth 准备过程
3. 使用 Initial Access Token 安全地完成 client 注册
4. 处理 client credentials 并校验注册响应

## 标准合规性

本实现遵循以下规范：
- **[MCP Authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization.md)** - MCP OAuth 主规范
- [RFC 7591 - OAuth 2.0 Dynamic Client Registration Protocol](https://datatracker.ietf.org/doc/rfc7591/)
- [OAuth 2.1](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/)
- [OpenID Connect Dynamic Client Registration 1.0](https://openid.net/specs/openid-connect-registration-1_0.html)

### MCP 规范要求

根据 MCP 规范：
> “MCP clients 和 authorization servers **SHOULD** 支持 OAuth 2.0 Dynamic Client Registration Protocol [RFC7591]，从而让 MCP clients 在无需用户交互的情况下获得 OAuth client ID。”

## 前置条件

- 已完成第 01 步（Protected Resource Metadata Discovery）
- 已完成第 02 步（Authorization Server Metadata Discovery）
- 对 OAuth 2.1 client registration 概念有基础理解

## 核心概念

### 什么是 OAuth Dynamic Client Registration？（面向初学者）

可以把 Dynamic Client Registration 想成**自动办图书馆借书证**：
- **传统方式**：你手工填表，等待审批，拿到卡号
- **动态方式**：你出示证件，机器读取信息，立刻发卡

换到 OAuth 语境下：
- **传统方式**：管理员提前手动创建 `client_id` 和 `client_secret`
- **动态方式**：client 软件自动完成注册，并即时拿到凭据

### 1. Dynamic Client Registration（RFC 7591）
- **目的：** 让 OAuth client 可以通过编程方式在 Authorization Server 上注册
- **为什么重要：** 对于运行时发现新 MCP server 的 AI agent 来说，这是必需能力
- **安全性：** 通过 Initial Access Token 控制谁有权注册 client
- **流程：** Client metadata → Registration endpoint → Client credentials

### 2. Initial Access Token（IAT）
- **它是什么：** 一个专门用于授权 dynamic client registration 的“许可条”
- **现实类比：** 像是一张访客通行证，允许你完成会议注册
- **如何产生：** 由管理员通过 Keycloak admin console 生成
- **如何使用：** 在注册请求时放进 Authorization Header
- **安全性：** 可配置过期时间和使用次数限制

### 3. 注册流程（完整旅程）
1. **发现（Discovery）：** client 从 AS metadata（第 02 步）中发现 `registration_endpoint`
2. **准备（Preparation）：** client 组装自己的 metadata（名称、redirect URI、scope 等）
3. **请求（Request）：** client 带上 Initial Access Token，向注册端点 POST metadata，以证明自己有注册权限
4. **校验（Validation）：** Authorization Server 检查 token 和 metadata
5. **响应（Response）：** AS 校验通过后返回 `client_id` 和 `client_secret`
6. **存储（Storage）：** client 安全保存这些凭据，供后续 OAuth 流程使用

### 4. MCP 特定注意点
- **Resource 参数：** client 必须请求与 MCP server 相关的 scope（如 `mcp:read`、`mcp:write`）
- **Audience Binding：** token 会绑定到特定 MCP server URL（第 06 步会讲）
- **AI Agent 场景：** 注册过程应由程序自动完成，不依赖人工干预

## 实现指南

### 文件结构
```
03_dynamic_client_registration/
└── open_source/keycloak/
    ├── client.py              # Complete registration client
    ├── server.py              # MCP server with OAuth discovery
    ├── docker-compose.yml     # Keycloak configuration
    ├── realm-export.json      # Keycloak realm setup
    └── pyproject.toml         # Python dependencies
```

### 运行 Demo

#### 1. 启动 Keycloak
```bash
cd open_source/keycloak
docker-compose up -d

# Wait for Keycloak to start
docker-compose logs -f keycloak
```

#### 2. 启动 MCP Server
```bash
# In the same directory
uvicorn server:app --reload --port 8000
```

#### 3. 创建 Initial Access Token
1. **访问**：http://localhost:9000/admin
2. **登录**：admin / admin123
3. **选择 realm**：mcp-oauth
4. **进入**：Clients → Client registration → Initial access tokens
5. **点击**：Create
6. **设置**：Expiration: 3600 seconds，Count: 10
7. **立刻复制 token**

#### 4. 运行 Registration Client
```bash
# With environment variable
INITIAL_ACCESS_TOKEN="your-token-here" uv run client.py

# Or interactive mode
uv run client.py
```

### 预期输出

client 会演示 MCP 所需的三阶段 OAuth 准备过程：

#### 🔍 **阶段 1**：MCP Protected Resource Metadata Discovery（[RFC 9728](https://datatracker.ietf.org/doc/rfc9728/)）
```
📡 Making unauthenticated request to MCP server: http://localhost:8000/mcp
❌ HTTP 401 Unauthorized (expected!)
📋 Fetching MCP metadata: http://localhost:8000/.well-known/oauth-protected-resource
✅ Successfully retrieved MCP server metadata
📍 Authorization Server discovered: http://localhost:9000/realms/mcp-oauth
```

#### 🔍 **阶段 2**：Authorization Server Metadata Discovery（[RFC 8414](https://datatracker.ietf.org/doc/rfc8414/)）
```
📋 Fetching Keycloak metadata: http://localhost:9000/.well-known/oauth-authorization-server
✅ Successfully retrieved Keycloak metadata
🔐 Authorization Endpoint: http://localhost:9000/realms/mcp-oauth/protocol/openid-connect/auth
🎫 Token Endpoint: http://localhost:9000/realms/mcp-oauth/protocol/openid-connect/token
📝 Registration Endpoint: http://localhost:9000/realms/mcp-oauth/clients-registrations/openid-connect
```

#### 📝 **阶段 3**：Dynamic Client Registration（[RFC 7591](https://datatracker.ietf.org/doc/rfc7591/)）
```
📤 Sending registration request with Initial Access Token
✅ Registration Status: SUCCESS
🆔 Client ID: cf285ac3-70a8-417d-9ec4-c8b88b4f5bd8
🔐 Client Secret: ******************** (hidden for security)
📍 Redirect URIs: http://localhost:8888/callback, http://127.0.0.1:8888/callback
🎭 Scopes: mcp:write openid offline_access mcp:read
```

**刚刚发生了什么？** 你的 MCP client 已经成功：
1. ✅ **发现** 了去哪里获取授权（第 01-02 步的知识）
2. ✅ **注册** 了自己到 Authorization Server
3. ✅ **获得** 了后续 OAuth 流程所需的凭据（为第 04 步做准备）

### 示例注册请求
```json
{
  "client_name": "MCP OAuth Demo Client - Step 03",
  "client_uri": "http://localhost:8888",
  "redirect_uris": [
    "http://localhost:8888/callback",
    "http://127.0.0.1:8888/callback"
  ],
  "grant_types": ["authorization_code", "client_credentials"],
  "response_types": ["code"],
  "scope": "openid mcp:read mcp:write offline_access",
  "token_endpoint_auth_method": "client_secret_post",
  "application_type": "web"
}
```

### 示例注册响应
```json
{
  "client_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "client_secret": "supersecret123...",
  "client_id_issued_at": 1234567890,
  "redirect_uris": [
    "http://localhost:8888/callback",
    "http://127.0.0.1:8888/callback"
  ],
  "grant_types": ["authorization_code", "client_credentials"],
  "scope": "openid mcp:read mcp:write offline_access"
}
```

## Keycloak 配置

### Admin Console 访问方式
- **URL**：http://localhost:9000/admin
- **用户名**：admin
- **密码**：admin123

### 预配置资源
- **Realm**：mcp-oauth
- **User**：mcpuser / password123
- **Client**：mcp-demo-client（用于测试）
- **Scopes**：openid、mcp:read、mcp:write、offline_access

## 故障排查

### 常见问题

1. **401 Unauthorized**
   - **原因**：Initial Access Token 缺失、过期或无效
   - **解决方法**：在 Keycloak admin console 中重新创建 token

2. **403 Forbidden**
   - **原因**：Client Registration Policies 阻止了请求
   - **解决方法**：使用 Initial Access Token，或检查 Keycloak 策略配置

3. **找不到 MCP Server**
   - **原因**：MCP server 没有启动
   - **解决方法**：执行 `uvicorn server:app --reload --port 8000`

4. **Keycloak 无法访问**
   - **原因**：Keycloak 没有启动，或仍在启动过程中
   - **解决方法**：使用 `docker-compose logs keycloak` 检查

## 安全最佳实践

1. **Initial Access Token 管理**
   - 安全存储 token（如环境变量）
   - 设置合理的过期时间
   - 监控 token 使用情况

2. **Client Credentials 保护**
   - 安全存储 `client_secret`
   - 不要记录或暴露凭据
   - 生产环境中使用 HTTPS

3. **Redirect URI 校验**
   - 明确指定精确的 redirect URI
   - 不要使用通配符
   - 校验所有 URI 是否符合预期模式

## 下一步

完成 client 注册后，**第 04 步**将实现 **Authorization Code Flow**：

1. **Authorization Request**：把用户重定向到 Keycloak 登录
2. **User Authentication**：用户输入凭据完成登录
3. **Authorization Code**：Keycloak 带着 code 重定向回来
4. **Token Exchange**：用 code 换取 access token
5. **API Access**：使用 token 调用受保护的 MCP 端点

这一步得到的 `client_id` 和 `client_secret`，会在第 04 步中直接使用。

## 参考资源

- [RFC 7591 - OAuth 2.0 Dynamic Client Registration](https://datatracker.ietf.org/doc/rfc7591/)
- [OpenID Connect Dynamic Client Registration](https://openid.net/specs/openid-connect-registration-1_0.html)
- [Keycloak Documentation](https://www.keycloak.org/documentation)
- [OAuth 2.1 Security Best Practices](https://datatracker.ietf.org/doc/draft-ietf-oauth-security-topics/)
