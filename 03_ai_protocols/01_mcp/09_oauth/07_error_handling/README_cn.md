# 06：OAuth 错误处理

**目标：** 为 OAuth 2.1 流程中的常见失败场景实现健壮的错误处理。

一个能用于生产环境的应用，必须优雅处理错误、过期或权限不足的凭据。本课重点关注：当 MCP server 返回特定 OAuth 错误时，client 如何正确解释这些错误，并采取合适的应对动作。

## 关键 OAuth 概念

- **`WWW-Authenticate` Header：** 这是错误通信的关键。一个安全的 Resource Server（也就是我们的 MCP server）会通过它告诉 client：请求为什么失败。
- **`error` 与 `error_description` 参数：** `WWW-Authenticate` Header 可以包含标准化错误码（例如 `invalid_token`、`insufficient_scope`）以及可读的错误说明。
- **`invalid_token`（RFC 6750）：** 表示 access token 已过期、格式错误或已被撤销。client 的正确做法是丢弃该 token，并尝试重新获取新的 token（例如重新执行 Authorization Code Flow，或使用 refresh token）。
- **`insufficient_scope`（RFC 6750）：** 表示 token 本身合法，但不具备执行当前操作所需的权限。例如用户只授予了“读”权限，而 client 却在尝试“写”。

## 实现计划

- **`authorization_server_mock.py`：**
  - mock AS 会被扩展成可以按需签发 scope 有限、或过期时间很短的 token，以便测试这些错误场景。

- **`mcp_server.py`：**
  - server 的安全中间件会增强为能够识别这些特定条件：
    - 如果 token 已过期，返回 `401 Unauthorized`，并带上 `error="invalid_token"`
    - 我们会模拟一个“带 scope 限制”的工具；如果使用了缺少对应 scope 的 token，则 server 返回 `403 Forbidden`，并带上 `error="insufficient_scope"`

- **`client.py`：**
  - client 的请求逻辑会包裹在 `try...except` 或类似结构中，以处理 HTTP 错误。
  - **场景 1（Invalid Token）：**
    - client 尝试使用一个已经过期的 token
    - 它捕获到 `401` 错误，解析 `WWW-Authenticate` Header，并识别出 `invalid_token`
    - 然后打印类似 “Token is invalid, starting re-authentication...” 的提示，并重新启动完整授权流程
  - **场景 2（Insufficient Scope）：**
    - client 使用一个 scope 不足但本身合法的 token 去调用受保护工具
    - 它捕获到 `403` 错误，识别出 `insufficient_scope`
    - 并向用户打印清晰提示，例如：“你没有授权执行这个操作。”
