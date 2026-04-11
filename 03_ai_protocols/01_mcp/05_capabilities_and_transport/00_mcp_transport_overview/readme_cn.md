# 什么是 MCP
MCP 标准化了 AI 应用（宿主，host）如何连接一个或多个“MCP 服务器”。这些服务器会暴露工具、资源和提示词。其线协议格式是 JSON-RPC 2.0。MCP 是有状态的，先通过初始化握手协商能力，然后在长连接式的消息交互中处理请求、响应和通知。

## 两个层次

### 1. 数据层
定义生命周期管理、核心原语（工具、资源、提示词）、服务器可回调的客户端侧原语（sampling、elicitation、logging），以及通知。以上都基于 JSON-RPC 2.0。

### 2. 传输层
定义消息如何传递。当前规范重点强调两种标准传输：用于本地进程的 `stdio`，以及用于远程场景的 `Streamable HTTP`；同时支持可选的 SSE 作为服务端到客户端的流式传输方式。鉴权则通过常规 HTTP 机制完成，例如 bearer token 或自定义请求头。

### 需要重点理解的核心原语
#### 服务器暴露：
• **Tools**。客户端可调用的可执行函数。通过 `tools/list` 发现，通过 `tools/call` 调用。

• **Resources**。只读上下文，例如文件、Schema、API 响应。通过 `resources/list` 发现，通过 `resources/read` 获取。

• **Prompts**。由服务器提供、可参数化的模板，通过 `prompts/list` 和 `prompts/get` 使用。

客户端暴露：

• **Sampling**。服务器可以通过 `sampling/complete` 请求客户端获取一次 LLM 补全结果。

• **Elicitation**。服务器可以请求额外的用户输入。

• **Logging**。服务器向客户端持续发送日志流。

这些能力会在初始化阶段完成协商，从而让双方都明确当前有哪些能力可用。

1. `initialize`。客户端发送 `protocolVersion` 及自身能力，接收服务端返回的 `serverInfo` 和服务端能力。
2. `notifications/initialized`。客户端通知服务端自己已准备就绪。
3. 发现阶段。按需调用 `tools/list`、`resources/list`、`prompts/list`。
4. 执行阶段。调用 `tools/call`、`resources/read`、`prompts/get`，并按支持情况处理进度和通知。
5. 通知阶段。例如当工具清单变化时，发送 `notifications/tools/list_changed`。

### 传输方式：什么时候用哪一种
#### Stdio
• 最适合本地开发、CLI，以及由编辑器拉起子进程的场景。
• 延迟最低，不经过网络。
• 常见于 Claude Desktop 或 VS Code 启动本地服务器的模式。

#### Streamable HTTP
• 最适合远程服务器，或希望使用标准 HTTP 鉴权和路由的场景。
• 客户端到服务端通过 `POST` 发送，请求返回时可选用 SSE 语义进行流式回传；这也是托管服务和云平台中的常见方式。

#### 那么 SSE 和 WebSocket 呢
• 当前规范重点强调的是 `stdio` 和 `Streamable HTTP`，其中 HTTP 可选用 SSE 风格的流式语义。一些社区 SDK 或框架会说明：相比单独把 SSE 视作传输方案，当前更推荐 `Streamable HTTP`。

#### Hosted MCP tool（模型直接调用服务器，不经过 Python 回调往返）
• 使用 `HostedMCPTool`。你只需要传入服务器标签或连接器配置。
• 适合希望降低延迟，并减少自有基础设施负担的场景。([OpenAI GitHub][3])
