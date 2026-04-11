# 04：OAuth 2.1 Authorization Code Flow

**目标：** 实现完整的、带用户交互的 Authorization Code Flow，从 Authorization Server（AS）获取 access token。

这是整个 OAuth 流程的核心。我们会把前面课程里的所有部分拼接起来：client 把用户重定向到 AS 登录，用户同意授权，AS 再把用户带回 client 并附带一个临时 code，随后 client 用这个 code 去换取真正的 access token。

## 关键 MCP 与 OAuth 概念

- **Authorization Code Flow：** 面向 Web 应用和原生应用最安全的 OAuth 流程。它保证最有价值的 access token 不会暴露在用户浏览器中。
- **`authorization_endpoint`：** AS 上用于用户登录和授权同意的 URL。
- **请求参数（`response_type`、`client_id`、`redirect_uri`、`scope`、`state`、`resource`）：**
  - `response_type=code`：表示我们使用的是 Authorization Code Flow。
  - `state`：client 生成的随机字符串，用于防止 CSRF 攻击。
  - `resource`：**Resource Indicator（RFC 8707）**。它是 MCP server 的唯一标识符，并且在 MCP 规范里是**必需参数**。它告诉 AS，这个 token 是签发给哪个资源受众的。
- **本地 Web Server：** client 需要临时启动一个本地 Web server，在自己的 `redirect_uri`（例如 `http://localhost:8888/callback`）上监听 AS 的重定向。
- **Authorization Code：** 用户成功登录后返回给 client 的、短时有效且只能使用一次的 code。
- **`token_endpoint`：** client 把 authorization code 连同 `client_id` 和 `client_secret` 一起提交给 AS，以换取 access token 的 URL。

## 实现计划

- **`authorization_server_mock.py`：**
  - AS 将扩展为处理 `authorization_endpoint` 和 `token_endpoint` 请求。
  - `GET /authorize`：向用户展示一个简单的（模拟的）登录与授权页面。用户“同意”后，重定向回 client 的 `redirect_uri`，并附带 `authorization_code` 和原始 `state`。
  - `POST /token`：接收 authorization code，校验它是否合法；如果合法，就签发一个已签名的 JWT（也就是 access token）。

- **`client.py`：**
  - 在发现 AS 并完成自身注册之后，client 会：
    1. 在后台线程中启动一个本地 Web server，监听自己的 `redirect_uri`
    2. 构造完整的授权 URL，其中包含 `client_id`、`state`、`redirect_uri` 以及指向 MCP server 的 `resource` 参数
    3. 打开用户浏览器访问这个 URL
    4. 用户与 mock AS 交互后被重定向回来。本地 server 捕获该请求，并提取 `authorization_code`
    5. client 向 AS 的 `token_endpoint` 发起 `POST` 请求，用 code 换取 access token
    6. 最后，client 打印收到的 access token，以确认整个流程执行成功
