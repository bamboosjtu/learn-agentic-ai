# 第 05 步：PKCE 实现


PKCE（Proof Key for Code Exchange）是 OAuth 2.1 Authorization Code Flow 的一个**安全扩展**，不是单独的一种流程。根据 [MCP Authorization 规范](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization.md)，**PKCE 对 MCP client 是强制要求**。

这一步专门讲 PKCE。我们会：
- 添加 `code_verifier` / `code_challenge` 生成逻辑
- 用 PKCE 安全机制增强第 04 步的流程
- 达到 MCP 合规要求

## 什么是 PKCE？

**PKCE** 用于防止 **authorization code interception attacks（授权码拦截攻击）**，通过确保只有发起授权请求的那个 client，才能用 authorization code 换取 token。

### PKCE 的工作方式

1. **Client 生成随机密钥**（`code_verifier`）
2. **Client 对这个密钥求哈希**（得到 `code_challenge`）
3. **授权请求** 中带上 `code_challenge`
4. **Authorization server** 存储这个 challenge
5. **Token 交换** 时带上原始的 `code_verifier`
6. **Server 校验** `SHA256(code_verifier) == code_challenge`

## MCP 对 PKCE 的要求

摘自 MCP 规范：

### 强制实现
> “MCP clients **MUST** 按照 [OAuth 2.1 Section 7.5.2](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-12#section-7.5.2) 实现 PKCE”

### 安全目的
> “PKCE 通过要求 client 创建 verifier-challenge 配对，帮助防止授权码拦截和注入攻击，从而确保只有原始请求方才能用 authorization code 换取 token。”

## PKCE 与普通 Authorization Code Flow 的区别

| 步骤 | 普通流程 | PKCE 流程 |
|------|-------------|-----------|
| 1. Authorization Request | `response_type=code&client_id=...` | `response_type=code&client_id=...&code_challenge=...&code_challenge_method=S256` |
| 2. Authorization Response | `code=abc123` | `code=abc123`（相同） |
| 3. Token Exchange | `grant_type=authorization_code&code=abc123` | `grant_type=authorization_code&code=abc123&code_verifier=original_secret` |

## 在第 03 步实现中的 PKCE

我们当前的第 03 步主要聚焦在 **Dynamic Client Registration**。下一步则会实现 **OAuth flow**：

```python
# Example PKCE implementation (for future steps)
import secrets
import hashlib
import base64

def generate_pkce_params():
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).decode('utf-8').rstrip('=')
    
    return {
        'code_verifier': code_verifier,
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256'
    }
```

## 为什么 PKCE 对 MCP 至关重要

1. **Public Clients：** MCP client 往往无法安全保存 `client_secret`
2. **移动端 / 桌面应用：** 更容易遭遇授权码拦截
3. **默认安全性：** OAuth 2.1 要求所有 client 都启用 PKCE
4. **MCP 合规性：** 对 HTTP transport 而言，MCP 规范明确要求 PKCE

我们刚刚加上的 `basic` scope 已经支持启用 PKCE 的 client。第 04 步 Basic Authorization Code Flow 会优先聚焦核心 OAuth 概念、用户交互、redirect URI、state 参数，因此不先引入 PKCE 复杂度，以便纯粹学习基础流程。


