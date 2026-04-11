# 07：安全最佳实践

**目标：** 回顾并汇总整个 OAuth 部分学到的安全最佳实践，并把它们与官方 MCP 规范交叉对应起来。

这是 OAuth 模块中的最后一课，重点不再是写新代码，而是理解我们之前写下的代码背后的“为什么”。我们会整理出一份安全检查清单，并确认我们的实现是否符合这些要求。

## 关键安全概念（来自 MCP 规范）

本课直接强化 [`authorization.mdx`](https://github.com/modelcontextprotocol/specification/blob/main/specification/2025-06-18/basic/authorization.mdx) 和 [`security_best_practices.mdx`](https://github.com/modelcontextprotocol/specification/blob/main/specification/2025-06-18/basic/security_best_practices.mdx) 中的要求。

- **Confidential Clients：** 能够安全保存 secret 的 client（例如我们的原生 Python client）**应该**被视作 confidential client，并在调用 token endpoint 时使用自己的 `client_secret`。
- **PKCE（Proof Key for Code Exchange）：** 虽然为了简化教程，我们的 mock flow 没有完整内建 PKCE，但我们会解释为什么 PKCE 对 public client（例如基于浏览器的 JS 应用）是**强制要求**的，并且对所有 client 都**推荐启用**，以防止授权码拦截攻击。
- **HTTPS：** 在生产环境中，所有与 Authorization Server 和 MCP Server 的通信都**必须**使用 TLS（HTTPS）。
- **安全的凭据存储：** client **必须**安全存储自己的 `client_secret` 和收到的 refresh token（例如使用系统 keychain，而不是明文文件）。
- **State 参数：** 在授权请求中**必须**使用 `state` 参数，以缓解 CSRF 攻击。
- **Resource Indicators（RFC 8707）：** 如我们已经实现的那样，client **必须**使用 `resource` 参数来指定 token 的 audience，从而防止 token 被错误定向。
- **Token Validation：** MCP server **必须**做完整 token 校验，包括签名、过期时间、issuer 和 audience。

## 实现计划

这一课主要是代码审查和文档整理练习。

- **`checklist.md`：**
  - 我们会创建一个新的 Markdown 文件，用于整理基于以上安全点的检查清单。

- **代码审查：**
  - 我们会逐一检查前几课编写的代码（`client.py`、`mcp_server.py`、`authorization_server_mock.py`）
  - 对于清单中的每一项，我们都会定位到实现该安全措施的具体代码行
  - 对于在教程中被简化的点（例如 PKCE 或安全存储），我们会在代码里加注释，说明真正的生产级实现应如何处理

- **最终测试：**
  - 最后再完整跑一遍端到端流程，确保所有组件在功能和安全上都能协同工作
