# 02：Authorization Server Metadata

**目标：** 创建一个简单的 OAuth Authorization Server，并演示 client 如何通过 `/.well-known/oauth-authorization-server` 端点发现它的能力。

在第 01 步中，我们已经发现了 Authorization Server 的 URL（`http://localhost:9000`）。这一步实现的是发现流程的后半部分：直接去查询 Authorization Server 本身，了解它具体有哪些端点和能力。

## 双实现方案

这一步提供 **两套完整实现**：

### 📚 **自定义实现**（教学用）
- **目的：** 从零开始构建一个简单 server，理解 OAuth 基础
- **技术：** 纯 Python HTTP server（约 200 行）
- **优点：** 不依赖外部系统，就能理解 OAuth 核心概念
- **适用场景：** 学习、开发、理解规范

### 🏭 **Keycloak 实现**（生产用）
- **目的：** 在真实场景中使用企业级 OAuth server
- **技术：** 用 Docker 运行 Keycloak，提供完整 OIDC 支持
- **优点：** 生产可用的能力、安全性和可扩展性
- **适用场景：** 生产部署、企业环境

---

## 本节你将学到什么

这一步聚焦于 [RFC 8414](https://datatracker.ietf.org/doc/html/rfc8414) 定义的 **Authorization Server Metadata Discovery**。

完成本课后，你将理解并实现：
1. 一个简单的 OAuth Authorization Server，它在 `/.well-known/oauth-authorization-server` 提供 metadata
2. 一个 client，通过查询该端点发现 server 的能力
3. MCP 规范要求的两阶段发现流程
4. 教学用实现与生产用实现之间的区别

## 关键 OAuth 概念

- **Authorization Server Metadata（RFC 8414）：** 一个标准 JSON 文档，用来告诉 client Authorization Server 有哪些端点、支持哪些能力
- **`/.well-known/oauth-authorization-server`：** 提供这份 metadata 的标准端点
- **端点发现（Endpoint Discovery）：** client 通过它获知这些具体 URL：
  - `authorization_endpoint`：用户登录与授权同意页面的入口
  - `token_endpoint`：用 authorization code 换取 access token 的端点
  - `registration_endpoint`：client 可动态注册自己的端点
  - `jwks_uri`：获取公钥、用于 token 校验的端点

## 双服务器发现流程

这一步完成 OAuth 的两阶段发现流程：

1. **第 01 步（✅ 已完成）：** client 查询 MCP server 上的 `/.well-known/oauth-protected-resource`，得知 Authorization Server 在 `http://localhost:9000`
2. **第 02 步（本节）：** client 查询 Authorization Server 上的 `/.well-known/oauth-authorization-server`，得知注册、授权和 token 交换的具体端点

### 运行代码

```bash
uv run uvicorn server:mcp_app --reload
```

```bash
uv run uvicorn authorization_server:app --port 9000 --reload
```

```bash
uv run client.py
```

### 运行 Keycloak 实现

```bash
# Terminal 1: Start Keycloak
cd open_source/keycloak
docker-compose up -d

# Terminal 2: Start MCP server (from step 01)
uv run uvicorn server:mcp_app --reload

# Terminal 3: Run discovery client
uv run client.py

# Optional: Check Keycloak Logs
docker-compose logs -f keycloak
```

## 实现方式

这一节通过建立在第 01 步 MCP server 代码之上的方式，演示**端到端 OAuth 发现流程**。不是完全拆开的孤立示例，而是一个把两个阶段串起来的集成方案。

### 自定义实现（教学用）

自定义实现提供了清晰的职责分离，由三个组件构成：

- **`server.py`：**
  - 运行在 `http://localhost:8000` 的 **MCP Resource Server**（与第 01 步相同）
  - 提供 Protected Resource metadata endpoint
  - 对未认证请求返回 401，触发发现流程

- **`authorization_server.py`：**
  - 运行在 `http://localhost:9000` 的 **OAuth Authorization Server**
  - 提供 Authorization Server metadata endpoint
  - 提供后续课程会用到的 mock OAuth 端点

- **`client.py`：**
  Discovery client，执行完整流程：
  1. **第 01 步：** 对 MCP server 发起未认证请求 → 收到 401 → 拉取 Protected Resource metadata → 找到 Authorization Server URL
  2. **第 02 步：** 查询 Authorization Server metadata → 发现具体 OAuth 端点
  3. **总结：** 输出完整的端点发现结果
---

## 📚 自定义实现

### 文件结构
```
custom/
├── server.py                 # MCP Resource Server (from step 01)
├── authorization_server.py   # OAuth Authorization Server
├── client.py                 # Discovery client (two-stage flow)
└── pyproject.toml            # Dependencies (MCP, FastAPI, uvicorn)
```

### 运行自定义 Demo

你需要在不同终端中运行 3 个组件：

#### 终端 1：启动 MCP Resource Server
```bash
cd custom
uv run uvicorn server:mcp_app --host localhost --port 8000 --reload
```

#### 终端 2：启动 Authorization Server
```bash
cd custom
uv run uvicorn authorization_server:app --host localhost --port 9000 --reload
```

#### 终端 3：运行 Discovery Client
```bash
cd custom
uv run client.py
```

### 自定义实现特性
- ✅ **清晰分离**：MCP server 与 Authorization Server 是独立组件
- ✅ **端到端 Demo**：完整展示两阶段发现流程
- ✅ 符合 RFC 8414 的 Authorization Server metadata endpoint
- ✅ 符合 RFC 9728 的 Protected Resource metadata（来自第 01 步）
- ✅ 为后续课程准备好的 mock OAuth 端点（authorization、token、registration）
- ✅ 面向教学的日志和清晰错误信息
- ✅ 每个组件都可通过简单的 uvicorn 命令启动

---

## 🏭 Keycloak 实现

### 文件结构
```
open_source/keycloak/
├── docker-compose.yml         # Keycloak setup
├── realm-export.json         # Pre-configured realm
└── client.py                 # Production client
```

### 运行 Keycloak Demo

1. **启动 MCP Server**（来自第 01 步）：
   ```bash
   cd ../01_protected_resource_metadata/mcp_code
   uv run uvicorn server:mcp_app --reload
   ```

2. **启动 Keycloak**：
   ```bash
   cd open_source/keycloak
   docker-compose up -d
   
   # Monitor startup (takes 30-60 seconds)
   docker-compose logs -f keycloak
   ```

3. **运行 Keycloak Discovery Client**：
   ```bash
   python client.py
   ```

4. **访问 Keycloak 管理后台**（可选）：
   - URL: http://localhost:9000/admin
   - 用户名：`admin`
   - 密码：`admin123`

### Keycloak 实现特性
- ✅ 生产可用的 OAuth 2.1 + OIDC server
- ✅ 真实用户认证（`mcpuser/password123`）
- ✅ 正确的 JWT 签名与校验
- ✅ Dynamic client registration
- ✅ 对 public client 的 PKCE 支持
- ✅ Refresh token 与 session 管理
- ✅ 管理控制台
- ✅ 内建安全能力（如暴力破解防护等）
- ✅ 可扩展到生产部署

---

## 对比：自定义实现 vs Keycloak

| 特性 | 自定义实现 | Keycloak 实现 |
|---------|----------------------|------------------------|
| **学习价值** | ⭐⭐⭐⭐⭐ 高，细节都看得见 | ⭐⭐⭐ 中，重点在集成 |
| **生产可用性** | ❌ 仅演示 | ✅ 企业级 |
| **搭建复杂度** | ⭐ 简单，运行 Python 文件即可 | ⭐⭐⭐ 中等，需要 Docker |
| **安全能力** | ⭐ 基础演示级 | ⭐⭐⭐⭐⭐ 完整安全能力 |
| **可定制性** | ⭐⭐⭐⭐⭐ 完全控制 | ⭐⭐⭐ 以配置为主 |
| **依赖** | 无 | Docker + Keycloak |
| **性能** | ⭐⭐ 足够学习 | ⭐⭐⭐⭐⭐ 高性能 |
| **标准合规性** | ⭐⭐⭐ 基础合规 | ⭐⭐⭐⭐⭐ 完整 RFC 合规 |

## 预期输出

两种实现都会演示：

1. **阶段 1**：从 MCP server 发现 Authorization Server URL
2. **阶段 2**：从 Authorization Server 发现具体端点
3. **最终结果**：得到后续步骤要使用的完整端点信息

### 自定义实现输出示例
```
🚀 OAuth 2.0 Two-Stage Discovery Client
============================================================
🔍 Stage 1: Discovering Authorization Server URL from MCP server
✅ Received expected 401 Unauthorized response
✅ Successfully retrieved MCP server metadata
🎯 Found Authorization Server URL: http://localhost:9000

🔍 Stage 2: Discovering Authorization Server metadata
✅ Successfully retrieved Authorization Server metadata

🎉 DISCOVERY COMPLETE - Two-Stage OAuth Discovery Results
============================================================
📋 STAGE 1: MCP Server Protected Resource Metadata
🔐 Authorization Endpoint: http://localhost:9000/authorize
🎫 Token Endpoint: http://localhost:9000/token
📝 Registration Endpoint: http://localhost:9000/register
```

### Keycloak 实现输出示例
```
🚀 OAuth 2.0 Discovery with Keycloak (Production)
================================================================================
✅ Keycloak health check passed: UP
🔍 Stage 1: Discovering MCP Protected Resource Metadata
✅ Successfully retrieved MCP server metadata

🔍 Stage 2: Discovering Keycloak Authorization Server Metadata
✅ Successfully retrieved Keycloak metadata

🎉 KEYCLOAK OAUTH DISCOVERY COMPLETE
================================================================================
🏢 Issuer: http://localhost:9000/realms/mcp-oauth
🔐 Authorization Endpoint: http://localhost:9000/realms/mcp-oauth/protocol/openid-connect/auth
🎫 Token Endpoint: http://localhost:9000/realms/mcp-oauth/protocol/openid-connect/token
🔑 JWKS URI: http://localhost:9000/realms/mcp-oauth/protocol/openid-connect/certs
👤 UserInfo Endpoint: http://localhost:9000/realms/mcp-oauth/protocol/openid-connect/userinfo

🚀 PRODUCTION FEATURES AVAILABLE:
   ✅ Real user authentication (username: mcpuser, password: password123)
   ✅ Proper JWT token signing and validation
   ✅ PKCE support for public clients
   ✅ Admin console at http://localhost:9000/admin
```

## 下一步

当两个发现阶段都完成后，后续课程会继续使用这些发现出来的端点：

### 对于自定义实现
1. 使用 `registration_endpoint` 在简单 Authorization Server 上**注册 client**
2. 用 mock 用户同意流程**实现授权流程**
3. 通过基础 JWT 校验**验证 token**

### 对于 Keycloak 实现
1. 使用 Keycloak 的动态注册或后台管理台**注册 client**
2. 用真实身份认证**实现用户登录**
3. 通过 Keycloak 的 JWKS endpoint **验证 token**
4. 用 HTTPS 和持久化数据库**部署到生产环境**

## DACA 集成说明

这两种实现都支持 **Dapr Agentic Cloud Ascent（DACA）** 架构：

- **自定义实现**：非常适合本地开发和学习（DACA 第 1 阶段）
- **Keycloak 实现**：适合企业级和超大规模生产环境（DACA 第 3-4 阶段）
- **Agent-to-Agent**：两者都支持 client credentials flow，可支撑千万级并发 agent
- **Kubernetes Ready**：Keycloak 可以部署在 Kubernetes 上，并结合 Dapr 使用
