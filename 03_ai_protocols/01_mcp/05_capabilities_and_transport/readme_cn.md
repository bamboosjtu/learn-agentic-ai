# 模块 4：核心能力与传输通信

一段以动手实践和探索驱动的学习旅程，聚焦 MCP 的高级特性与 StreamableHTTP 模式。

> **掌握适用于生产级应用的 MCP 高级能力与通信协议**  
> 基于 [Anthropic 的 Advanced MCP Topics Course](https://anthropic.skilljar.com/model-context-protocol-advanced-topics)

> **建议先阅读** [Advanced MCP Course Lessons](https://docs.google.com/document/d/1mvWO9NzzomRea_uJuKHEoiyswGVJTpkuQqjUBGalptE/)

> 另见 [MCP 2025-06-18 Specification Schema](./mcp_schema_2025-06-18/schema.ts)

## 🎯 模块概览

本模块介绍那些让 MCP 足以支撑生产应用的高级能力，包括 **Sampling**、**Logging & Progress Notifications**、**Roots** 以及 **Transport Protocols**。你将学习如何构建这样的 MCP Server：它既能把推理委托给客户端，也能提供实时反馈、发现上下文，并高效完成通信。

### 教学方法

本模块采用 **以能力为中心** 的学习方式：

- **Feature-First**：每一课聚焦 MCP 的某一项具体能力
- **Production-Ready**：示例都尽量贴近真实使用方式
- **Protocol Deep-Dive**：理解底层通信机制
- **Integration Patterns**：学习不同能力如何协同工作

## 📚 学习目标

完成本模块后，你将能够：

### 核心能力

- ✅ **实现 Sampling**：构建能够把 AI 推理委托给客户端的 Server
- ✅ **使用 Logging 与 Progress**：为长时间运行的任务提供实时反馈
- ✅ **实现 Roots**：发现并访问用户上下文与项目信息
- ✅ **掌握传输协议**：理解 JSON-RPC、STDIO 和 StreamableHTTP

### 高级技能

- ✅ **设计有状态与无状态架构**：为不同场景选择合适的 Server 架构
- ✅ **处理双向通信**：实现从 Server 到 Client 的请求
- ✅ **管理上下文发现**：构建能够理解用户环境的 Server
- ✅ **优化性能**：针对不同使用场景选择合适的传输协议

### 生产准备

- ✅ **错误处理**：为所有能力实现稳健的异常处理
- ✅ **安全性**：应用 MCP 通信中的安全最佳实践
- ✅ **可观测性**：使用日志和进度通知提高可观测能力
- ✅ **可扩展性**：设计能够承载生产负载的 Server

## 🏗️ 课程结构

### 阶段 1：核心能力（第 01 到 03 课）

**目标**：掌握三项能支撑复杂 AI 交互的核心 MCP 能力

#### [01. Sampling - Giving Tools a Brain](01_sampling/README.md)

- **时长**：75 到 90 分钟
- **重点**：AI 委托与推理能力
- **交付结果**：一个支持 Sampling、具备 AI 驱动工具能力的 MCP Server
- **关键概念**：
  - 理解何时 Server 需要把推理委托给 Client
  - 实现 `sampling/create` 请求与响应
  - 有状态与无状态 HTTP 连接
  - 能力协商与模型偏好
  - Sampling 失败时的错误处理

#### [02. Logging & Progress Notifications](02_logging_progress/README.md)

- **时长**：60 到 75 分钟
- **重点**：实时反馈与可观测性
- **交付结果**：一个具备完整日志与进度跟踪能力的 Server
- **关键概念**：
  - 日志通知类型与级别
  - 长时间运行任务的进度跟踪
  - 带元数据的结构化日志
  - 客户端侧通知处理
  - 性能监控与调试

#### [03. Roots - Context Discovery](03_roots/README.md)

- **时长**：60 到 75 分钟
- **重点**：发现用户上下文与项目信息
- **交付结果**：一个能够发现并访问用户环境的 Server
- **关键概念**：
  - Root 的发现与枚举
  - 文件系统上下文与项目结构
  - 环境变量与配置
  - 工作区与编辑器集成
  - 具备上下文感知能力的工具行为

### 阶段 2：传输与通信（第 04 到 06 课）

**目标**：掌握 MCP 的传输协议与通信模式

#### [04. JSON-RPC Message Types](04_jsonrpc_messages/README.md)

- **时长**：45 到 60 分钟
- **重点**：理解 MCP 建立在 JSON-RPC 2.0 之上的基础
- **交付结果**：深入理解 MCP 消息结构
- **关键概念**：
  - JSON-RPC 2.0 规范与 MCP 扩展
  - 请求 / 响应消息格式
  - 错误处理与状态码
  - 消息校验与解析
  - 协议一致性与调试

#### [05. STDIO and StreamableHTTP Transport](05_transport/README.md)

- **时长**：45 到 60 分钟
- **重点**：用于生产部署的 HTTP 传输，以及用于本地开发的标准输入输出传输
- **交付结果**：一个支持 StreamableHTTP 的 Server，包含有状态和无状态两种管理方式，以及一个基于 STDIO 的 MCP Server 与 Client
- **关键概念**：
  - STDIO 传输实现
  - 消息分帧与解析
  - 进程生命周期管理
  - 错误处理与恢复
  - 开发与调试工作流
  - StreamableHTTP 协议规范
  - 有状态与无状态连接
  - 连接管理与持久化
  - 身份认证与安全
  - 生产部署考量
  
## 🔧 前置要求

### 技术要求

- **已完成模块 4**：理解 MCP 基础概念
- **Python 3.8+**，并具备 `async/await` 使用经验
- **HTTP 与 SSE 知识**：对 Web 协议有基本理解
- **JSON-RPC 基础认知**：理解 RPC 模式，课程中也会补充讲解


### 知识检查

- [ ] 能解释什么时候应该用 sampling，而不是直接实现工具逻辑
- [ ] 理解有状态连接和无状态连接的区别
- [ ] 能为长时间运行任务实现合适的进度通知
- [ ] 知道如何通过 roots 发现并访问用户上下文
- [ ] 能为不同场景选择合适的传输协议
- [ ] 理解 JSON-RPC 消息结构与 MCP 扩展
- [ ] 能为 HTTP 传输实现安全认证
- [ ] 知道如何处理各类能力中的错误与失败情况

## 🔗 资源与参考

### 官方文档

- [MCP Specification - Sampling](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling)
- [MCP Specification - Logging](https://modelcontextprotocol.io/specification/2025-06-18/client/logging)
- [MCP Specification - Roots](https://modelcontextprotocol.io/specification/2025-06-18/client/roots)
- [MCP Specification - Transport](https://modelcontextprotocol.io/specification/2025-06-18/transport)

### 学习资源

- [Anthropic's Advanced MCP Course](https://anthropic.skilljar.com/model-context-protocol-advanced-topics)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
- [HTTP/2 Specification](https://tools.ietf.org/html/rfc7540)
- [OAuth 2.1 Security](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1)

### 社区与支持

- [MCP GitHub Discussions](https://github.com/modelcontextprotocol/python-sdk/discussions)
- [MCP Discord Community](https://discord.gg/modelcontextprotocol)
- [Transport Protocol Discussions](https://github.com/modelcontextprotocol/specification/discussions)

## 🚀 下一步

完成本模块后，你将准备好继续探索：

- MCP Specification
- OAuth Integration
- OpenAI Agents SDK Integration

## 🔧 常见挑战与解决思路

### Sampling 相关挑战

- **挑战**：不清楚什么时候该用 sampling，什么时候该直接实现
- **解决思路**：创造性任务使用 sampling；确定性操作使用直接实现

### 传输层相关挑战

- **挑战**：难以在 STDIO 和 HTTP 传输之间做选择
- **解决思路**：开发阶段优先用 STDIO；生产部署优先用 HTTP

### 状态管理相关挑战

- **挑战**：不清楚如何在无状态与有状态连接中管理状态
- **解决思路**：如果需要双向通信，就使用有状态连接

---

**准备开始了吗？** 从 [Lesson 01: Sampling - Giving Tools a Brain](01_sampling/README.md) 开始，学习如何构建具备 AI 驱动能力的 MCP Server。
