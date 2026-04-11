# MCP 规范

[规范简介](https://modelcontextprotocol.io/specification/2025-06-18)

[架构](https://modelcontextprotocol.io/specification/2025-06-18/architecture)

[基础部分](https://modelcontextprotocol.io/specification/2025-06-18/basic)

[生命周期](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle)

[传输层](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)

[授权](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)

[取消](https://modelcontextprotocol.io/specification/2025-06-18/basic/utilities/cancellation)

[Ping](https://modelcontextprotocol.io/specification/2025-06-18/basic/utilities/ping)

[进度](https://modelcontextprotocol.io/specification/2025-06-18/basic/utilities/progress)

客户端特性

[Roots](https://modelcontextprotocol.io/specification/2025-06-18/client/roots)

[Sampling](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling)

[Elicitation](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation)

服务端特性

[概览](https://modelcontextprotocol.io/specification/2025-06-18/server)

[Prompts](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)

[Resources](https://modelcontextprotocol.io/specification/2025-06-18/server/resources)

[Tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)



## **Model Context Protocol（MCP）简介**

Model Context Protocol（MCP）是一个开源协议，目的是标准化外部数据源和工具与大语言模型（LLM）应用之间的集成方式。它为 LLM 应用提供了一种结构化方法，使 AI 驱动的 IDE、聊天界面以及自定义 AI 工作流等应用，都能够连接到所需的上下文信息。MCP 的设计灵感来自 Language Server Protocol（LSP），目标是通过共享上下文信息、向 AI 系统暴露工具、以及构建可组合的集成方式，打造一个更统一、可互操作的 AI 应用生态。该协议由 TypeScript Schema 定义，并使用 JSON-RPC 2.0 进行通信。

### **MCP 架构**

MCP 的架构基于 client-host-server 模型，这种方式有助于建立清晰的安全边界和职责分离。

* **Host：** Host 是主应用程序，用于管理和协调多个 client 实例。它负责创建和管理 clients、控制它们的权限和生命周期、执行安全策略，以及处理用户授权。Host 还会聚合来自不同 clients 的上下文信息，并协调整体 AI/LLM 集成与 sampling 流程。
* **Client：** 每个 client 都由 host 创建，并与一个 server 建立一对一关系。Client 会与 server 建立有状态 session，处理协议协商和能力交换，并在 host 与 server 之间转发消息。它还负责管理订阅、通知，以及 server 之间的安全边界。
* **Server：** Server 是提供上下文、资源、工具和 prompts 的专用服务，它们通过 client 向 host 提供能力。Server 可以是本地进程，也可以是远程服务，并且以独立方式运行，各自承担明确职责。Server 必须遵守 host 施加的安全约束，并且可以通过 client 向 host 请求 sampling。

### **基础概念**

MCP 建立在模块化架构之上，所有实现都必须支持一个核心基础协议。这个基础协议定义了所有交互中最基本的 JSON-RPC 2.0 消息类型。协议的关键组成包括：

* **生命周期管理（Lifecycle Management）：** 负责处理 client 与 server 之间的连接建立、能力协商和 session 控制。
* **授权框架（Authorization Framework）：** 为 client 通过 HTTP 与 server 安全通信提供机制。
* **服务端特性（Server Features）：** 允许 server 暴露 resources 和 tools。
* **客户端特性（Client Features）：** 让 client 能执行 sampling 等任务。

所有 client 和 server 之间的通信都必须遵循 JSON-RPC 2.0 规范，其中包括请求、响应和通知。

### **上下文连接的生命周期**

在 MCP 中，client 与 server 之间的连接生命周期包含三个明确阶段：

1. **Initialization（初始化）：** 生命周期从 client 向 server 发送 `initialize` 请求开始。这个请求会包含 client 支持的协议版本、它的能力，以及自身信息。Server 会返回自己支持的协议版本和能力。如果双方版本不兼容，连接会被终止。一旦协商出兼容版本，client 会发送 `initialized` 通知，表示这一阶段结束。
2. **Operation（运行阶段）：** 初始化成功后，连接进入运行阶段。在这个阶段中，client 与 server 会基于双方协商好的能力交换消息并执行操作。为保证通信顺畅，双方必须严格遵守已经约定的协议版本和能力范围。
3. **Shutdown（关闭阶段）：** 这个阶段通常由 client 发起，用于优雅地终止连接。MCP 依赖底层传输机制来表示连接结束。例如，在标准输入输出传输中，client 会关闭它通往 server 的输入流。

### **传输层**

MCP 使用 JSON-RPC 对消息进行编码，规范中定义了两种标准传输机制：

* **stdio：** 这是推荐给本地 client 的传输方式，通常由 client 以子进程方式启动 MCP server。双方通过 server 的标准输入和标准输出进行通信，消息以换行符分隔。
* **Streamable HTTP：** 这种传输方式允许 server 作为独立进程运行，并通过 HTTP `POST` 和 `GET` 请求处理多个 client 连接。它还可以选择使用 Server-Sent Events（SSE）来流式传输服务端消息。规范中详细说明了该传输方式下的 HTTP Header、状态码，以及安全注意事项，例如校验 `Origin` Header 以防止 DNS rebinding 攻击。

### **授权**

MCP 规范为基于 HTTP 的传输提供了一个可选的授权框架，使 client 能够代表资源拥有者向受限 server 发起请求。这个机制基于 OAuth 2.1 等成熟规范，并定义了受保护的 MCP server、MCP client 和授权服务器三种角色。

整个授权流程大致如下：MCP server 会向 client 公布它所关联的授权服务器；然后 client 去发现该授权服务器的端点和能力。规范还详细说明了资源参数和访问令牌的使用方式，包括 token 的要求和处理方法。同时，它也讨论了 token audience 绑定、token 窃取风险以及通信安全等问题。

### 工具性能力

这些是可选但非常实用的功能，用于管理 client 与 server 之间的连接。

* **Cancellation（取消）：** 允许 client 或 server 取消一个已经在执行中的请求。这对终止不再需要的长时间任务很有帮助。希望取消的一方会发送一条 `notifications/cancelled` 消息，并附带要取消的请求 ID。
* **Ping：** 用于快速检查连接是否仍然存活。无论是 client 还是 server，都可以发送 `ping` 请求，对方必须尽快响应。如果一直收不到响应，就可以认为连接已经失效。
* **Progress（进度）：** 让 server 能够向 client 报告长时间运行操作的进度。这对于向用户提供反馈非常有用，例如展示一个进度条。

### 客户端特性

这些是 client 可以向 server 提供的能力。

* **Roots：** Roots 是一些 URI，用来定义 server 可以工作的目录范围，或者说“安全区域”。通过设置 roots，client 可以限制 server 只能访问特定文件、文件夹，甚至 API 端点，从而增强安全性和控制力。例如，你可以把某个文件系统 server 限制在特定项目目录中工作。
* **Sampling：** 这个能力反转了常见的信息流方向。通常是 client 向 server 发请求，而 sampling 允许 *server* 反过来请求 *client* 用 LLM 执行一次文本生成任务。这是构建更高级、具备 agent 行为系统的重要能力。
* **Elicitation：** 这是一个比较新的特性，它允许 server 通过 client 动态向用户请求额外信息。如果 server 在完成任务时还需要更多上下文（例如用户偏好或缺失的信息），它可以向 client 发送 `elicitation/create` 请求，然后由 client 向用户收集所需输入。

### 服务端特性

这些是 server 可以向 client 暴露的核心能力。

* **Overview（概览）：** MCP server 可以暴露三种主要能力：resources、prompts 和 tools。这使得扩展 LLM 能力的方式变得更加灵活和强大。
* **Prompts：** 这些是 server 提供给 client 的预定义消息模板或工作流。它们为常见任务提供标准化的 LLM 交互方式，可用于引导用户或 AI 模型。
* **Resources：** 允许 server 向 LLM 暴露数据和内容，作为上下文使用。内容可以是文件内容，也可以是数据库记录等各种形式的数据。
* **Tools：** 这些是 server 可以提供给 LLM 调用的可执行函数。正是它让 AI 具备了在现实世界中执行动作的能力，例如发邮件、调用 API、执行计算等。Tools 被设计为“由模型控制”，也就是说 LLM 可以在获得用户许可的前提下自行决定是否调用它们。
