# NANDA（网络化智能体与去中心化 AI）

[用 AI 构建去中心化互联网：NANDA 正在到来](https://www.forbes.com/sites/johnwerner/2025/05/13/make-a-decentralized-internet-with-ai-nanda-is-coming/)

[他们正在为 AI 打造 TCP/IP，它叫 NANDA](https://www.forbes.com/sites/johnwerner/2025/04/29/theyre-making-tcpip-for-ai-and-its-called-nanda/)

[官方网站](https://nanda.media.mit.edu/)

[超越 DNS：通过 NANDA Index 与 Verified AgentFacts 解锁 AI 智能体互联网](https://arxiv.org/abs/2507.14263)

[AI Agent Registry 方案综述](https://arxiv.org/html/2508.03095v1)

“Project NANDA” 指的是 **Networked Agents And Decentralized AI**，这是 MIT 发起的一项雄心勃勃的计划，本质上是在为 AI 智能体构建“互联网”。

随着我们从单个聊天机器人走向 **AI 智能体生态系统**，我们需要一套通用方法，让智能体能够跨公司、跨云环境彼此 *发现*、*信任* 和 *交流*。否则，每一次集成都像一次尴尬的定制相亲。MIT 的 **Project NANDA** 提出构建“AI 智能体互联网”：一层兼具发现与信任能力的基础设施，使智能体能够像 Web 服务一样被定位、识别、验证和路由。你可以把它理解为“面向智能体的 DNS + PKI + 智能路由”，但服务对象不再是静态网页，而是可以协作、可以交易的智能体。

其中一个关键技术组件是 **NANDA Index**，其背后依赖 **Verified AgentFacts**。后者是关于某个智能体身份、能力、端点和策略的加密签名元数据。NANDA Index 提供 **快速解析**、**密钥轮换**、**隐私保护查询** 和 **基于 schema 校验的能力声明**。它之所以被称为“超越 DNS”，是因为它解析到的不只是 IP 地址，而是可验证、动态变化的事实。

下面对其内涵及重要性进行拆解。

---

## 什么是 Project NANDA？

**NANDA** 是一套开放、去中心化的基础设施，目标是支撑一个庞大的自治 AI 智能体生态，使它们能够跨不同平台和协议进行发现、验证、通信与协作。

- 它建立在 Anthropic 的 MCP（Model Context Protocol）和 Google 的 A2A（Agent-to-Agent）等协议之上，并把它们编排进一个统一、去中心化的网络中。([nanda.media.mit.edu][1], [numorpho.org][2], [LinkedIn][3])
- Project NANDA 为 **“AI 智能体互联网”** 提供底层基础设施，使来自个人、企业或机构的智能体，能够在联邦式网络环境中运行、交易并持续演化。([LinkedIn][3], [Forbes][4], [numorpho.org][2])

---

## 为什么它重要

你可以把 NANDA 看作是在为 AI 智能体建立 **TCP/IP 或 DNS 层**，也就是它们实现安全、无缝、可扩展交互所需的底座。

- 它像一个 **通用适配器**：NANDA 允许来自不同框架的智能体彼此理解和通信，而无需共享完全相同的协议语言。([LinkedIn][5], [Forbes][4])
- 它提供 **去中心化注册系统**，类似于域名解析，让智能体可以在联邦网络中彼此发现。([Forbes][4], [LinkedIn][3], [Medium][6], [Wikipedia][7])
- NANDA 内含 **安全身份、信任与验证层**，确保交互可审计、可信，并能抵御冒充行为。([Medium][6], [arXiv][8], [LinkedIn][3])

---

## 核心组件与创新点

### 1. **智能体发现与注册**

智能体可以通过联邦式注册表定位并与其他智能体通信。可以把它理解为 NANDA 面向智能体身份的 DNS。([nanda.media.mit.edu][1], [numorpho.org][2], [Medium][6], [arXiv][9])

### 2. **身份、信任与问责**

智能体拥有加密身份，并对每次交互进行签名，以确保可追责并建立信任。([Medium][6], [numorpho.org][2], [arXiv][8])

### 3. **协议互操作**

NANDA 并不取代现有协议，而是包裹在它们之外，通过模块化的“quilt”结构实现跨协议互通，例如 MCP、A2A、HTTPS、NLWeb。([nanda.media.mit.edu][1], [numorpho.org][2], [LinkedIn][3], [Medium][6], [Forbes][4], [velocityascent.com][10])

### 4. **经济与激励系统**

该架构还设想了一层经济机制，智能体可以因有价值的行为而获得 token、积分或可追踪贡献奖励。([Medium][6], [numorpho.org][2], [velocityascent.com][10])

### 5. **自适应解析器**

NANDA 正在把注册系统扩展为动态解析：智能体可以根据区域负载、上下文或安全要求来选择通信端点，就像一个智能路由层。([arXiv][11])

### 6. **范围与架构阶段**

Project NANDA 按阶段推进：

- **阶段 1：Agentic Web Foundations**，聚焦智能体发现、通信与安全
- **阶段 2：Agentic Commerce**，加入经济与市场能力
- **阶段 3：Society of Agents**，走向协作网络与涌现行为([LinkedIn][12])

### 7. **企业与研究应用**

一篇近期论文阐述了 NANDA 在企业环境中构建安全、可互操作多智能体系统的框架，支持发现、凭证验证和跨协议安全。([arXiv][8])
其他研究还进一步探讨了注册表模型、如 AgentFacts 这样的元数据标准，以及跨协议信任机制。([arXiv][9])

---

## 总结表

| 特性 | 描述 |
| ----------------------- | ------------------------------------------------------ |
| **Registry** | 联邦式智能体发现系统，类似 DNS |
| **Identity & Trust** | 基于密码学的安全智能体身份 |
| **Protocol Bridge** | 在 MCP、A2A、HTTPS、NLWeb 之间实现互操作 |
| **Economic Incentives** | 支持奖励、代币与工作证明的机制框架 |
| **Dynamic Routing** | 具备上下文感知能力的端点解析 |
| **Roadmap** | 分阶段建设：基础设施 → 经济层 → 协作层 |

---

## 一句话概括

Project NANDA 正在为一个去中心化生态打地基，在这个生态中，AI 智能体可以：

- 自主地 **发现** 和 **验证** 彼此身份
- 无缝地 **跨平台通信**
- 在透明治理机制下进行 **交易与协作**


[1]: https://nanda.media.mit.edu/index.html?utm_source=chatgpt.com "NANDA - The Internet of AI Agents"
[2]: https://numorpho.org/whitepapers/mantra-m5-thesis-brief-71/?utm_source=chatgpt.com "Mantra M5 Thesis Brief 71 – Platform Evolution 1: Tenets – EVERYTHING CONNECTED – Numorpho's Book of Business"
[3]: https://www.linkedin.com/pulse/project-nanda-internet-ai-agents-mason-nguyen-uyy7c?utm_source=chatgpt.com "Project NANDA: The Internet of AI Agents"
[4]: https://www.forbes.com/sites/johnwerner/2025/04/29/theyre-making-tcpip-for-ai-and-its-called-nanda/?utm_source=chatgpt.com "They’re Making TCP/IP For AI, And It’s Called NANDA"
[5]: https://www.linkedin.com/pulse/revolution-you-havent-heard-why-project-nanda-could-change-reganti-tidmc?utm_source=chatgpt.com "The Revolution You Haven't Heard About: Why Project NANDA Could Change Everything"
[6]: https://rahulshah19.medium.com/nanda-the-internet-stack-for-ai-agents-70bc8d706323?utm_source=chatgpt.com "NANDA: The Internet Stack for AI Agents | by Rahulshah | Medium"
[7]: https://en.wikipedia.org/wiki/Santanu_Bhattacharya_%28data_scientist%29?utm_source=chatgpt.com "Santanu Bhattacharya (data scientist)"
[8]: https://arxiv.org/abs/2508.03101?utm_source=chatgpt.com "Using the NANDA Index Architecture in Practice: An Enterprise Perspective"
[9]: https://arxiv.org/abs/2508.03095?utm_source=chatgpt.com "A Survey of AI Agent Registry Solutions"
[10]: https://velocityascent.com/nanda-networked-agents-and-decentralized-ai/?utm_source=chatgpt.com "NANDA: Networked Agents And Decentralized AI"
[11]: https://arxiv.org/abs/2508.03113?utm_source=chatgpt.com "NANDA Adaptive Resolver: Architecture for Dynamic Resolution of AI Agent Names"
[12]: https://www.linkedin.com/posts/projectnanda_projectnanda-agenticweb-ai-activity-7357456121487388672-qzio?utm_source=chatgpt.com "An electrifying gathering of minds in SF! | Project NANDA: Architecting the Internet of AI Agents"


## NANDA 与 MCP / A2A 的关系

这是个关键问题。Project **NANDA** 并不和 **MCP（Model Context Protocol）** 或 **A2A（Google 提出的 Agent-to-Agent 协议）** 竞争。相反，它被设计为把它们“缝合”在一起的 **互操作与发现层**。

三者的关系可以这样理解：

---

## NANDA vs MCP vs A2A

| 层级 | 目的 | NANDA 所处位置 |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **MCP（Model Context Protocol）** | 规范 LLM / Agent 如何与外部工具、数据源和扩展交互，即“agent ↔ tools” | NANDA 把 MCP 智能体视为网络中的 *节点*。它提供注册、身份与信任系统，使 MCP 智能体能够跨域被发现、被验证并安全连接。 |
| **A2A（Agent-to-Agent）** | Google 正在推进的 agent ↔ agent 对话协议，支持结构化消息、协商与编排 | NANDA 通过充当 **桥接层**，让 A2A 智能体与 MCP 智能体以及其他类型智能体实现互通。它不替代 A2A，而是让 A2A 流量可以跨生态安全流动。 |
| **NANDA** | 网络基础设施：发现、身份、信任、跨协议路由，类似智能体世界的 TCP/IP + DNS | 它提供通用寻址系统与注册表，使 MCP 与 A2A 智能体能够 *找到彼此*、完成身份验证并建立通信，而不受协议差异影响。 |

---

## 它们如何协同工作

1. **发现与注册**

   - NANDA 提供类似 DNS 的服务，让 MCP 智能体、A2A 智能体以及其他协议参与者都可以通过元数据被发现，例如能力、信任等级、归属方等。
   - 例子：一个基于 A2A 的日程安排智能体，可以通过 NANDA 发现一个基于 MCP 的日历智能体。

2. **身份与信任**

   - 在 NANDA 中，每个智能体都拥有加密身份。
   - 无论这个智能体说的是 MCP 还是 A2A，NANDA 都能对消息进行签名与验证，防止冒充。

3. **协议互操作**

   - MCP 关注“agent ↔ tool”
   - A2A 关注“agent ↔ agent”
   - NANDA 像一个 **路由器 / 适配器**，让这些协议能够共存并互通，而不是各自形成割裂生态。

4. **动态解析**

   - NANDA 能够智能路由对话。例如，一个来自 A2A 智能体的请求，如果所需能力只存在于某个 MCP 扩展中，就可以通过 NANDA 被路由过去。

---

## 类比理解

- **MCP** = USB 协议，把工具插到智能体上
- **A2A** = 蓝牙协议，让智能体彼此直接通信
- **NANDA** = 互联网协议栈，它保证无论是 USB 设备还是蓝牙设备，都能在网络中被 *发现、识别并连接*

---

一句话概括：**MCP 和 A2A 处理的是通信的内容与结构，NANDA 处理的是基础设施、发现能力与互操作性。**

## NANDA × MCP × A2A 一页速记版

**TL;DR**

- **MCP** = agent ↔ tools，可以理解成“能力层的 USB-C”
- **A2A** = agent ↔ agent，可以理解成“协商层的蓝牙”
- **NANDA** = 发现、身份、信任、路由，可以理解成“DNS / PKI + 网络道路系统”

如果 MCP 和 A2A 是乐队，NANDA 就是舞台、灯光，以及门口拿着名单验票的保安。([Anthropic][1], [modelcontextprotocol.io][2], [NANDA][3])

**NANDA 是什么，为什么值得关注**

- MIT 的 **Project NANDA**，即 “Networked Agents & Decentralized AI”，目标是构建开放的 **AI 智能体互联网**：一个联邦式 **Index**，把 agent ID 解析到 **Verified AgentFacts**，包括身份、能力、端点与策略，并提供密码学保证与快速吊销能力。([NANDA][3], [ar5iv][4])

**NANDA 与 MCP / A2A 的关系**

- **NANDA** 是基础织网层，负责 *find → verify → route*
- **MCP** 规范工具访问，使 agent 能以安全方式调用动作
- **A2A** 规范 agent 间协作与任务生命周期

三者共同避免协议孤岛问题。([modelcontextprotocol.io][2], [Anthropic][5], [Google Developers Blog][6], [Linux Foundation][7])

**核心工件**

- **NANDA Index & Verified AgentFacts**：带签名的元数据，支持发现、最小披露查询、多端点路由和秒级密钥轮换。([ar5iv][4])
- **MCP Tools**：由 server 以 schema 描述并由 client 调用的工具与资源。([Anthropic][1], [modelcontextprotocol.io][2])
- **A2A Agent Cards & Tasks**：能力广告加结构化、多模态交互，通常通过 Web 传输。([Google Developers Blog][6], [Google Codelabs][8])

**参考流程**

1. **Discover**：客户端向 NANDA 查询“谁会 `calendar.schedule`？”
2. **Verify & Resolve**：NANDA 返回 **AgentFacts** 与端点
3. **Negotiate**：智能体通过 **A2A** 协调任务
4. **Execute**：执行方调用 **MCP** 工具完成动作

**安全与治理**

- 加密身份、签名事实、隐私保护发现机制
- A2A 现已进入 **Linux Foundation** 托管，意味着更中立的开放治理。([Linux Foundation][7], [Google Developers Blog][9])

**快速判断该用什么**

- 问“*我该信任谁来做 X？*” → **NANDA**
- 问“*如何在系统里执行 X？*” → **MCP**
- 问“*哪个智能体来做 X，以及怎么协作？*” → **A2A**

**设计建议**

- 使用共享能力名称，例如 `calendar.schedule`
- 保持 **AgentFacts** 小而带签名
- 尽量采用最小披露查询
- 让 NANDA 去做跨协议桥接

**权威资料入口**

- **NANDA**：MIT 官网 + “Beyond DNS” 论文 ([NANDA][3], [ar5iv][4])
- **MCP**：官方文档与现行规范 ([Anthropic][1], [modelcontextprotocol.io][2])
- **A2A**：Google 公告与 Linux Foundation 项目更新 ([Google Developers Blog][6], [Linux Foundation][7])

- [The Verge](https://www.theverge.com/news/669298/microsoft-windows-ai-foundry-mcp-support?utm_source=chatgpt.com)
- [axios.com](https://www.axios.com/2025/04/17/model-context-protocol-anthropic-open-source?utm_source=chatgpt.com)
- [techradar.com](https://www.techradar.com/pro/what-is-model-context-protocol-and-why-does-it-matter-to-software-engineers?utm_source=chatgpt.com)

[1]: https://docs.anthropic.com/en/docs/mcp?utm_source=chatgpt.com "Model Context Protocol (MCP)"
[2]: https://modelcontextprotocol.io/specification/2025-06-18?utm_source=chatgpt.com "Specification"
[3]: https://nanda.mit.edu/ "NANDA - The Internet of AI Agents"
[4]: https://ar5iv.org/pdf/2507.14263 "[2507.14263] Beyond DNS: Unlocking the Internet of AI Agents via the NANDA Index and Verified AgentFacts"
[5]: https://www.anthropic.com/news/model-context-protocol?utm_source=chatgpt.com "Introducing the Model Context Protocol"
[6]: https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/?utm_source=chatgpt.com "Announcing the Agent2Agent Protocol (A2A)"
[7]: https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents?utm_source=chatgpt.com "Linux Foundation Launches the Agent2Agent Protocol ..."
[8]: https://codelabs.developers.google.com/intro-a2a-purchasing-concierge?utm_source=chatgpt.com "Getting Started with Agent-to-Agent (A2A) Protocol - Codelabs"
[9]: https://developers.googleblog.com/en/google-cloud-donates-a2a-to-linux-foundation/?utm_source=chatgpt.com "Google Cloud donates A2A to Linux Foundation"


## NANDA 的概念构件

1. **Index 与 Resolution**
   一个类似 quilt 的联邦式 **Index**，将智能体标识符解析到 **Verified AgentFacts**；支持快速上线、吊销以及多端点路由。你可以把它理解为“会查身份证、还能绕开拥堵路段的 DNS”。([ar5iv][5])
2. **Verified AgentFacts**
   带签名的元数据，包含身份密钥、能力声明、端点和治理信号；通过 **CRDT 风格更新**，在多个副本之间保持一致。([ar5iv][5])
3. **身份与信任**
   基于密码学身份、能力证明以及最小披露查询，与企业场景下的 **Zero-Trust Agentic Access（ZTAA）** 模式相契合。([arXiv][6])
4. **跨协议互操作**
   一个智能体注册体系支持多种协议，包括 **MCP**、**A2A**、传统 **HTTPS**，以及其他新兴 agent 协议。([arXiv][6])

## MCP：工具与数据集成理论

**MCP** 定义了 LLM / agent 如何以统一方式访问 **工具、资源与上下文**。Server 暴露带 schema 的 **tools**，host / client 发起调用，模型本身保持协议无关。它是 agent 生态的 **工具脊柱**，避免大家用几十种方式重复发明“调用这个 API”。([modelcontextprotocol.io][3])

## A2A：智能体之间会话的理论

**A2A** 描述了如何通过 **Agent Cards** 做能力发现、如何围绕任务进行带生命周期和工件的交互，以及如何通过 **HTTP / SSE / JSON-RPC** 进行多模态消息交换。这样，智能体之间就能像团队成员一样协商和协作，而不是像传真机一样传信息。该项目已进入 **Linux Foundation** 治理，意味着它在多厂商环境下更中立、更可持续。([Google Developers Blog][4], [Linux Foundation][7])

## 分层概念模型

- **体验层**：UI、人类参与、工作流
- **智能体层（A2A）**：智能体发现能力、协商任务、交换上下文。([Google Developers Blog][4])
- **工具层（MCP）**：智能体通过稳定 schema 调用结构化工具与数据。([modelcontextprotocol.io][3])
- **织网层（NANDA）**：发现、身份、注册、信任与跨协议路由。([MIT Media Lab][2], [ar5iv][5])

## 端到端参考流程

1. **Discover**
   A2A 客户端需要 `calendar.schedule` 能力，于是查询 **NANDA Index**，查找匹配 **AgentFacts** 的智能体。([ar5iv][5])
2. **Verify & Resolve**
   Index 返回带密码学身份和端点的 **verified facts**，客户端再根据区域、负载和策略选择路线。([ar5iv][5])
3. **Negotiate**
   智能体通过 **A2A** 协商任务范围、模态和工件，也就是明确“做什么、怎么做”。([Google Developers Blog][4])
4. **Execute**
   执行方智能体通过 **MCP tools** 真正完成动作，例如创建日历事件，并借助 schema 与 guardrails 保证安全。([modelcontextprotocol.io][3])
5. **Audit & Govern**
   借助策略、签名和日志，满足企业治理要求，例如 ZTAA / AVC，同时保留自治性与隐私。([arXiv][6])


## 开放问题

- **能力语义**
  不同领域之间，能力命名能在多大程度上统一，而不至于变得含糊？
- **注册表联邦**
  需要多少个 index、如何委派，以及由谁制定吊销规范？
- **策略可移植性**
  隐私与合规策略能否跟随 AgentFacts 跨组织传播，还是每次都要重新造一套 NDA？
- **采用惯性**
  会先是 MCP 的势能占优，还是 A2A 的企业导向更快落地？又或者 NANDA 的发现层会让这场竞争不再是零和？

---

### TL;DR

- **NANDA** = **基础织网层**，负责发现、身份、信任与路由
- **MCP** = **工具 / 数据协议**
- **A2A** = **智能体到智能体协议**

三者结合起来，才能构建一个 **可发现、可信任、可互操作** 的智能体生态系统，让智能体不仅找得到彼此，还能证明身份，并真正把事情做成。
