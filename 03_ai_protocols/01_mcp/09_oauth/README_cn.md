# MCP 的 OAuth 2.1 与安全

**目标：** 按照 MCP `2025-06-18` 标准，完整实现端到端的 OAuth 2.1 Authorization Code Flow。

这一部分是构建安全、可用于生产环境的 MCP 应用的核心。我们会创建一个安全的 MCP Resource Server，以及一个符合规范的 MCP Client，让它能够获取并使用 access token 来访问受保护资源。

这是一次深入而多阶段的学习路径，覆盖现代 API 安全的完整生命周期。

## 关键 MCP 与 OAuth 概念

- **MCP 作为 OAuth Resource Server：** MCP server 不只是工具提供方，它本身也是受保护资源。我们会把 MCP server 配置成：所有操作都必须携带有效 access token。
- **Authorization Server（AS）：** 一个独立的第三方服务，负责认证用户并签发 access token。为了演示，我们会自己实现一个简单的 OAuth AS。
- **两阶段发现流程（Two-Stage Discovery Process）：**
  1. **Protected Resource Metadata**（MCP server 上的 `/.well-known/oauth-protected-resource`）告诉 client 去哪里找 Authorization Server
  2. **Authorization Server Metadata**（AS 上的 `/.well-known/oauth-authorization-server`）告诉 client 注册、授权和获取 token 的具体端点
- **Dynamic Client Registration：** client 如何以编程方式在 Authorization Server 上完成注册。
- **Authorization Code Flow：** 安全的、基于浏览器的授权流程。用户在其中完成授权，client 得到 authorization code，再用它换取 access token。
- **Resource Indicators（RFC 8707）：** 一个关键安全机制。client 会显式指定所请求 token 的目标受众（也就是 MCP server），从而防止 token 泄露和误用。
- **Token Validation（JWT）：** MCP server 在接收到 access token（通常是 JWT）后，需要校验它的签名、issuer 和 audience，并在允许访问前提取用户声明信息。

## 学习路径

我们会从底层开始，一步一步把完整流程搭建起来。**每一步都会提供两种实现：**

### 📚 **自定义实现（用于教学）**
简洁、聚焦的 Python 代码（约 30 到 100 行），帮助你理解核心概念，不依赖复杂外部框架。

### 🏭 **开源实现（用于生产）**
使用成熟 OAuth 库和 OAuth 服务的真实世界示例，适用于生产部署。

---

1. **`01_protected_resource_metadata`：**
   MCP server 通过 `/.well-known/oauth-protected-resource` 宣告自己的安全要求以及 Authorization Server 的位置，完成 OAuth 发现流程的第一步。

2. **`02_authorization_server_metadata`：**
   创建一个简单的 OAuth Authorization Server，并通过 `/.well-known/oauth-authorization-server` 暴露自己的端点信息，完成两阶段发现流程。
   - **自定义：** 用基础 Python HTTP server 返回静态 metadata
   - **开源：** 配置 Keycloak 或部署 Hydra

3. **`03_dynamic_client_registration`：**
   通过 `/register` 端点，以编程方式把 client 注册到 Authorization Server 上，实现自动化 client onboarding。
   - **自定义：** 简单的注册端点 + 内存存储
   - **开源：** Keycloak Dynamic Client Registration 或 Auth0 Management API

4. **`04_oauth2_authorization_code_flow`：**
   实现完整、面向用户的登录授权流程，从而获得 access token。这是用户认证最常用的 OAuth 流程。
   - **自定义：** 模拟 HTML 登录表单 + code exchange
   - **开源：** GitHub OAuth 或 Google OAuth 配置

5. **`05_token_audience_validation`：**
   在 MCP server 上实现 JWT 校验，确保 token 合法且作用范围正确。
   - **自定义：** 用 PyJWT 和硬编码密钥做校验
   - **开源：** 使用 `python-jose` 并通过 JWKS 端点发现公钥

6. **`06_error_handling`：**
   处理常见 OAuth 错误，例如无效 token 或 scope 不足，构建健壮的错误处理能力。
   - **自定义：** 基础错误响应和 client 重试逻辑
   - **开源：** Authlib 内建错误处理模式

7. **`07_security_best_practices`：**
   回顾并实现规范中的关键安全注意事项，对实现进行加固。
   - **自定义：** 安全检查清单与基础加固
   - **开源：** 生产级 Keycloak + NGINX + TLS 配置

8. **`08_client_credentials_flow`：**
   不需要用户参与的系统到系统认证流程，为 DACA agent 提供机器到机器通信能力。
   - **自定义：** 直接 client credentials 交换
   - **开源：** 在 Auth0 / Keycloak 中配置 service account

## 当前阶段拆解

**步骤 1-3：发现与注册（基础阶段）**
- **01**：找到 Auth Server 在哪里（如 `http://localhost:9000`）
- **02**：查询 Auth Server，获知它的端点（`/authorize`、`/token`、`/register`）
- **03**：注册 client，获取 `client_id` 和 `client_secret`

**步骤 4-7：完整 OAuth 流程（面向用户交互）**
- **04**：完成 authorization code flow（用户登录并拿到 access token）
- **05**：MCP server 校验 token（JWT 签名、audience 等）
- **06**：处理 OAuth 错误（如 token 过期、scope 不足）
- **07**：回顾安全最佳实践

**步骤 8：替代流程（系统到系统）**
- **08**：client credentials flow（无需用户交互）

步骤 6-7 同时适用于这两类场景。

## 逻辑流程

对于**真人用户**（交互式）：
```
步骤 1→2→3→4→5 = 完整的面向用户 OAuth 流程
```

对于**系统到系统**（自动化）：
```
步骤 1→2→3→8→5 = 完整的机器到机器流程
```

步骤 6-7 适用于两种场景。

## 后续会发生什么？

当你完成全部 OAuth 步骤后，通常会进入这些方向：

1. **构建真实 MCP 应用**：用加好安全保护的 MCP server 承载实际工具
2. **部署到生产环境**：把 OAuth 安全方案迁移到云平台
3. **结合 DACA 扩展**：应用我们讨论过的 Dapr Agentic Cloud Ascent 模式
4. **Agent-to-Agent 通信**：用 OAuth 打好基础，支撑安全的 A2A 协议

## 这种递进路径的价值

每一步都在教一个明确能力：
- **01-03**：client 如何发现并注册到认证系统
- **04**：用户如何完成认证与授权
- **05**：server 如何校验安全性
- **06-07**：如何处理真实世界问题
- **08**：系统如何在没有人参与的情况下完成认证

最终你会同时掌握面向用户和自动化系统场景下的 MCP 安全工具箱。

## DACA 对齐：自定义实现 vs 开源实现

这种“双轨实现”方式与 **Dapr Agentic Cloud Ascent（DACA）** 的部署阶段高度一致：

### 🔬 **本地开发与学习**（自定义实现）
- **阶段：** 本地开发（DACA 上升路径第 1 阶段）
- **目标：** 在不被复杂性干扰的情况下理解 OAuth 基础
- **工具：** 纯 Python + 最少依赖
- **成本：** 免费，无需外部服务
- **规模：** 每秒 1 到 10 个请求，适合学习

### 🚀 **生产与企业环境**（开源实现）
- **阶段：** 企业级到超大规模（DACA 第 3-4 阶段）
- **目标：** 使用经过实战验证、功能完整的 OAuth 服务器
- **工具：** Keycloak、Auth0、GitHub OAuth 等
- **成本：** 可从免费层起步，并随业务增长扩展
- **规模：** 支持成千上万到百万级并发 agent

## 实施策略

**为了学习：** 先从自定义实现开始，理解核心概念  
**为了生产：** 再迁移到开源方案，获得可靠性与扩展性  
**为了 DACA：** 在 agent-to-agent 通信中使用 client credentials flow（步骤 8）

## 双服务器架构

步骤 01 和 02 遵循 MCP 规范中的双服务器模型：

- **MCP Server**（`localhost:8000`）：Resource Server，保护 tools / resources
- **Authorization Server**（`localhost:9000`）：OAuth server，负责认证和 token 签发

每个 server 都有自己的 discovery endpoint：
- MCP Server：`GET /.well-known/oauth-protected-resource`
- Authorization Server：`GET /.well-known/oauth-authorization-server`

这种分离方式允许 Authorization Server 同时服务多个 MCP Server，部署上也更灵活。
