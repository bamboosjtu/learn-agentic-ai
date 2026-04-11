# 05：Token Audience 与签名校验

**目标：** 让 MCP server 学会校验 client 发来的 access token（JWT），从而真正保护服务端。

这是保护 Resource Server 的最后一步，也是最关键的一步。MCP server **不能**仅仅因为请求里“带了 token”就放行；它**必须**校验 token 的签名、过期时间、issuer，以及最重要的目标 audience。

## 关键 MCP 与 OAuth 概念

- **JSON Web Token（JWT）：** 一种紧凑、URL-safe 的标准格式，用于在双方之间传递声明信息。我们的 Authorization Server 发出的 access token 就是 JWT。
- **Bearer Token：** 一种“谁持有谁可用”的 access token。它通常通过 `Authorization` HTTP Header 发送：`Authorization: Bearer <token>`。
- **JWT 校验：** MCP server 必须执行多步校验流程：
  1. **获取公钥：** 从 AS 的 `jwks_uri`（在第 2 节已发现）拉取公钥
  2. **校验签名：** 使用公钥验证 JWT 的签名，确认它确实由 AS 签发，且中途未被篡改
  3. **校验 Claims：** 检查 JWT payload 中的标准字段：
     - `exp`：token 没有过期
     - `iss`：token 的签发者是预期的 Authorization Server
     - **`aud`（Audience）：** 这是对 MCP 最关键的字段。server **必须**确认 `aud` 中包含它自己的唯一标识。这意味着这个 token 是专门签发给**当前这个** MCP server 使用的，而不是别的服务。

## 实现计划

- **`authorization_server_mock.py`：**
  - mock AS 将开始使用私钥为发出的 JWT 签名
  - 它还会暴露 `/jwks.json` 端点（也就是 `jwks_uri`），提供对应公钥

- **`mcp_server.py`：**
  - 我们会增强 server 的安全中间件
  - 当携带 `Bearer` token 的请求到达时，中间件会：
    1. 从 AS 的 `jwks_uri` 获取公钥（并进行缓存）
    2. 使用标准库（如 `python-jose`）解码并校验 JWT
    3. 重点检查 token 的 `aud` 是否与 MCP server 自己的标识一致
    4. 如果校验成功，则放行请求；否则返回 `401` 或 `403`

- **`client.py`：**
  - client 在上一课拿到 access token 后，这一步就会真正使用它
  - 它会调用一个受保护的 MCP 端点（例如 `tools/list`），并在 Header 中附带 `Authorization: Bearer <token>`
  - 如果 token 合法，client 会收到 MCP server 返回的 `200 OK`
  - 我们还会测试反例，例如发送被篡改的 token 或错误 token，确认 server 能正确拒绝请求
