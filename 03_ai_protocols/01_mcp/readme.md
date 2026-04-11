# 模型上下文协议（MCP）

> **一种开放协议，使 LLM 应用能够与外部数据源和工具实现无缝集成。**  
> — [MCP 官方规范](https://modelcontextprotocol.io/specification/2025-06-18)

## 什么是 MCP？

模型上下文协议（Model Context Protocol，MCP）是由 Anthropic 推出的开放标准，旨在简化 AI 系统，尤其是大语言模型（LLM），连接并交互外部数据源与工具的方式。它要解决的是 AI 模型的一个关键限制：与实时、动态数据相隔离。MCP 不再让模型只能依赖静态训练数据，也不要求开发者为每一个新数据源都编写一套定制集成，而是提供了一种通用、标准化的方式，使 AI 应用能够安全、高效地访问并使用各种系统中的信息，例如数据库、API、文件系统或企业工具。

你可以把 MCP 理解成“AI 集成领域的 USB-C”。正如 USB-C 接口让不同设备可以通过统一标准连接到电脑，MCP 让 AI 模型能够通过单一协议接入各种不同的数据源和工具。这显著降低了构建和维护多套独立连接的复杂度，使 AI 系统更灵活、更可扩展，也更具上下文感知能力。例如，一个使用 MCP 的 AI 助手可以查看你的日历、从 Google Drive 获取文件，或者查询数据库，而不需要为每一项任务单独编写专门代码。

MCP 采用客户端-服务器架构：

- **MCP Host**：即需要访问外部数据或能力的 AI 应用，例如聊天机器人或 IDE 插件。
- **MCP Client**：位于 Host 内部，负责管理与服务器之间安全的一对一连接。
- **MCP Server**：轻量级程序，用于向 AI 暴露特定工具、数据或资源，例如一个 GitHub Server 可以提供仓库访问能力。

### MCP 架构

MCP 使用 **Host → Client → Server** 的架构：

```text
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MCP Host      │    │   MCP Client    │    │   MCP Server    │
│                 │    │                 │    │                 │
│ • LLM App       │◄──►│ • Manages conn. │◄──►│ • Exposes tools │
│ • Claude        │    │ • Handles auth  │    │ • Provides data │
│ • ChatGPT       │    │ • Security      │    │ • Resources     │
│ • OpenAI Agents │    │                 │    │                 │
│ • Custom AI     │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

该协议使用 JSON-RPC 2.0 进行通信，支持动态、双向交互，例如获取实时数据或执行动作，同时还包含访问控制等安全机制。它也支持动态工具发现，这意味着 AI 无需硬编码知识，也能知道当前有哪些工具或数据可用。

在实践中，MCP 让 AI 不再只是文本生成器，而能够作为真正与外部世界交互的智能体。对开发者而言，它减少了集成开销；而 MCP 的开源特性也推动了一个不断扩展的生态，出现了面向 Slack、GitHub，甚至本地文件系统的可复用服务器。这是 AI 迈向更实用、更具连接能力现实应用的重要一步。

### 背景

这种无服务器能力，再加上 OAuth 2.1 身份认证、可流式传输的 HTTP、JSON-RPC，以及工具注解，使 MCP 的这次更新成为一次整体性的跃升。很明显，规范正在演进，以支持更广泛的部署模式，既包括适合高负载、持续性任务的持久化服务器，也包括适合轻量、按需任务的无服务器模式。这种双重形态强化了 MCP 作为通用标准的地位，使其既能服务资源密集型企业需求，也能适配精简敏捷的项目。

向无服务器方向的转变也进一步体现了 MCP 降低摩擦的理念：正如它试图标准化 AI 与工具的集成方式，现在它也在尽量减少运行这些集成所需的运维负担。可以预期，这会带来一波新的实验与创新，开发者可能会把无服务器 MCP Server 作为开源模板发布，进一步丰富整个生态。

### 更广泛的背景与未来展望

这些更新反映了 MCP 自 2024 年 11 月由 Anthropic 推出以来的快速演进。它们回应了早期采用者，如 Block、Zed 和 Sourcegraph，在实践中遇到的现实挑战，同时也延续了该协议作为“AI 集成领域 USB-C”标准的承诺。向 streamable HTTP 和 batching 的转变，说明 MCP 正在聚焦实时、高吞吐量场景；而 OAuth 2.1 的引入则表明其安全框架正在成熟。这些变化共同推动 MCP 成为更稳健、更通用的协议，以支持能够无缝接入多样工具和数据源的复杂、上下文感知型 AI 智能体。

展望未来，这些进展意味着 MCP 有机会发展为 AI 工具集成的默认标准，减少行业对碎片化、供应商专有方案的依赖。当然，挑战仍然存在，例如如何实现广泛采用、如何进一步完善规范，例如 webhook 或事件驱动特性的最终定稿。但这些更新无疑是让 AI 系统更互联、更高效、更易用的重要一步。

## OpenAI 对 MCP 的采纳

2025 年 3 月 25 日，OpenAI 宣布将在其所有产品中采纳 **模型上下文协议（MCP）**。其中，**Agents SDK** 已率先支持这一能力，其他产品也将很快跟进。这一举措对开发者、企业以及更广泛的 AI 生态都会带来重要影响。下面对其含义及重要性进行拆解。

---

### OpenAI 采纳 MCP 的关键影响

#### 1. **简化 AI 开发**

- **这意味着什么**：借助 MCP，开发者可以将 OpenAI 的 AI 模型，例如 ChatGPT 或基于 Agents SDK 构建的智能体，连接到各种外部系统，而不必为每一种集成单独编写定制代码。
- **为什么重要**：这减少了开发时间和复杂度。开发者可以直接使用面向 GitHub、Slack 等平台的现成 MCP Server，也可以为自己的工具编写自定义 Server，从而大幅简化 AI 应用开发流程。

#### 2. **更强大的 AI 智能体**

- **这意味着什么**：现在配备了 MCP 的 Agents SDK，可以让 AI 智能体轻松与外部工具和数据源交互。例如，一个智能体可以查看你的日历、查询数据库，或者从网络获取实时数据。
- **为什么重要**：这使 AI 智能体具备更强的**上下文感知能力**，也更能处理复杂的多步骤任务。开发者可以构建横跨多个平台自动化工作流的数字助手，从而提升生产力和系统功能性。

#### 3. **增强实时能力**

- **这意味着什么**：对于 ChatGPT 这类产品而言，MCP 集成让 AI 可以访问实时数据，例如股票价格、天气更新或个人文件，从而给出更准确、更相关的回答。
- **为什么重要**：这让 OpenAI 的模型从静态知识库转变为动态系统，能够提供最新信息，在实际场景中的可用性大幅提高。

#### 4. **推动标准化 AI 生态**

- **这意味着什么**：OpenAI 对 MCP 的采纳，可能会鼓励其他主要参与者，例如 Google、Microsoft，采用同样标准，从而推动 AI 生态更具互操作性。
- **为什么重要**：如果 MCP 被广泛采纳，开发者就能在不同厂商的 AI 模型和工具之间自由组合，而无需担心兼容性问题。当然，如果 OpenAI 仍是唯一的重要采用者，MCP 的影响力可能会受限；但凭借 OpenAI 的行业影响力，它仍可能推动更大范围的接受。

#### 5. **安全与隐私考量**

- **这意味着什么**：将 AI 模型连接到外部数据源，也会引入数据泄露或未授权访问等风险。MCP 为应对这些问题引入了基于 **OAuth 2.1** 的授权框架。
- **为什么重要**：尤其对于受监管行业中的企业来说，稳健的安全能力至关重要。虽然 MCP 的安全框架是积极的一步，但组织仍然需要仔细管理权限，确保数据安全。

#### 6. **对 AI 市场的竞争压力**

- **这意味着什么**：OpenAI 的这一动作可能迫使竞争对手采纳 MCP，或者开发自己的竞争标准。它也可能冲击那些提供 RAG 或 agent 编排工具的厂商，因为 OpenAI 内建的 MCP 能力可能降低对第三方方案的依赖。
- **为什么重要**：这可能带来市场整合，企业更倾向于采用 OpenAI 的一体化生态；同时，也会刺激其他参与者围绕 MCP 或与之竞争的方案继续创新。

#### 7. **仍需克服的挑战**

- **这意味着什么**：MCP 必须保持足够灵活，以适配多样数据源；必须可扩展，以支撑广泛使用；也必须足够安全，以抵御潜在漏洞。此外，它的成功还取决于 OpenAI 之外的更广泛采用。
- **为什么重要**：如果这些挑战得不到解决，MCP 可能无法完全释放潜力；但如果实现得当，它有机会彻底改变 AI 与世界交互的方式。

---

### 为什么这件事整体上很重要

OpenAI 采纳 MCP，是朝着更**互联、更通用、对开发者更友好**的 AI 生态迈出的大胆一步。它简化了集成，增强了 AI 智能体以及 ChatGPT 这类产品的能力，并推动整个行业向标准化方向前进。对开发者而言，这意味着可以更快、更轻松地构建强大的 AI 应用。对企业而言，这意味着更智能、更具上下文感知能力的工具成为可能，前提是安全问题能够妥善处理。对整个 AI 生态而言，这可能是一次改变格局的举措，但其长期影响仍取决于其他主要参与者是否也会拥抱 MCP。

简而言之，这一动作让 OpenAI 站在了 AI 互操作性的前沿，也为未来 AI 系统能够无缝接入全球数据与工具奠定了基础，前提是该协议能够获得足够的生态支持，并持续完善。

## 与其他协议的比较

| 特性 | MCP | REST APIs | GraphQL | gRPC |
|---------|-----|-----------|---------|------|
| **用途** | AI-LLM 集成 | 通用 Web API | 数据查询 | 高性能 RPC |
| **传输方式** | JSON-RPC 2.0 | HTTP | HTTP | HTTP/2 |
| **Schema** | JSON Schema | OpenAPI | GraphQL Schema | Protocol Buffers |
| **实时性** | WebSockets/SSE | WebSockets | Subscriptions | Streaming |
| **安全性** | OAuth 2.1 | 多种方式 | 多种方式 | TLS + Auth |
| **AI 导向** | ✅ 原生支持 | ❌ 通用协议 | ❌ 通用协议 | ❌ 通用协议 |

## 生态与采用情况

### **当前实现**

- **Anthropic Claude**：Claude Desktop 原生支持 MCP
- **OpenAI**：Agents SDK 已集成 MCP（2025 年 3 月）
- **VS Code 扩展**：已有面向开发工具的 MCP Server
- **企业工具**：GitHub、Slack、数据库连接器等

**[DeepLearning MCP 课程](https://learn.deeplearning.ai/courses/mcp-build-rich-context-ai-apps-with-anthropic/lesson/fkbhh/introduction)**

**[MCP 如何改变 AI Agent 中的 tool calling 流程？](https://www.linkedin.com/posts/rakeshgohel01_how-did-the-mcp-change-the-process-of-tool-activity-7312816588267614210-LlK8?utm_source=share&utm_medium=member_desktop&rcm=ACoAAAEcz6oB-KbLJt9GRA1bGQ0NvibVq6_0wBY)**

[观看视频：使用 Model Context Protocol 构建 Agents - Anthropic 的 Mahesh Murag 完整工作坊](https://www.youtube.com/watch?v=kQmXtrmQ5Zg)

[Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)

[代码仓库](https://github.com/modelcontextprotocol)

[官方文档](https://modelcontextprotocol.io/introduction)

[深入解析 MCP 与 AI 工具未来](https://a16z.com/a-deep-dive-into-mcp-and-the-future-of-ai-tooling/)

**[MCP OpenAI Agents SDK](https://openai.github.io/openai-agents-python/mcp/)**

**[开源 Model Context Protocol 刚刚更新，这为什么很重要](https://venturebeat.com/ai/the-open-source-model-context-protocol-was-just-updated-heres-why-its-a-big-deal/)]**

[MCP 并没有杀死 RAG，事实上两者是互补的](https://thenewstack.io/no-mcp-hasnt-killed-rag-in-fact-theyre-complementary/)

## 延伸阅读

- [MCP 官方规范（2025-06-18）](https://modelcontextprotocol.io/specification/2025-06-18)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)
- [JSON-RPC 2.0 规范](https://www.jsonrpc.org/specification) - 基础通信协议
- [OAuth 2.1 安全规范](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1) - 认证授权框架
- [Anthropic 的 MCP 公告](https://www.anthropic.com/news/model-context-protocol) - 最初介绍
