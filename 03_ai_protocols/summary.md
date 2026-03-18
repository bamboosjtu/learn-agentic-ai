# 03 AI Protocols 总结

本章核心目标是让你理解：一个真正可扩展的 Agentic 系统，不能只靠 prompt 和函数调用堆起来，还需要清晰的协议层、发现机制、身份与安全机制，以及跨框架互操作能力。

## 学习目标

这一章主要解决 4 个问题：

- Agent 怎么连接工具和外部数据
- Agent 怎么和另一个 Agent 通信
- 多协议环境下，Agent 如何被发现、验证和路由
- 网站或系统如何向 LLM / Agent 声明可访问规则

所以它不是单一协议教程，而是一套“从基础网络通信到 AI 原生协议”的分层地图。

## 内容概述

### `01_mcp`

这一部分是 `03_ai_protocols` 里最完整、最核心的内容，主线是 **MCP（Model Context Protocol）**。

它不是一上来就只讲 MCP，而是先把 MCP 背后的通信基础铺出来，再逐步进入 AI 工具调用协议本身。目录结构大致体现了这样的学习顺序：

- `01_http_theory`
  先补 HTTP、请求响应、状态码、流式传输这些网络基础
- `02_rest`
  解释 REST 风格 API，为理解服务接口设计打基础
- `03_json_rpc`
  介绍 JSON-RPC，因为 MCP 的通信形式建立在它之上
- `04_fundamental_primitives`
  讲 MCP 的基础构件，如 tools、resources、prompts 等原语
- `05_capabilities_and_transport`
  讲能力声明、传输方式、协议协商
- `06_openai_agents_sdk_integration`
  讲 MCP 如何和 OpenAI Agents SDK 这类运行时结合
- `07_mcp_specs`
  汇总规格与标准资料
- `08_projects`
  给出 MCP 的项目化应用案例
- `09_oauth`
  专门补 MCP 场景下的认证授权，尤其是 OAuth
- `10_extra_stateful_capabilities`
  延展到更复杂、更有状态的能力设计
- `extra`
  往下继续补 IP、TCP、UDP、HTTP/2、QUIC、gRPC、SSE、WebSockets、MQTT 等更底层或相关传输知识

这一部分最重要的认知是：

- MCP 本质上是 **agent 到 tools / data / context 的标准接口**
- 它解决的是“每接一个工具都要单独适配一次”的问题
- 它让 Agent 的工具接入从“项目私有集成”变成“可复用协议层”

如果你要构建真正可扩展的工具型 Agent，这一部分是必须理解的。

### `02_a2a`

这一部分讲 **A2A（Agent-to-Agent）协议**，重点从“agent 调工具”转向“agent 与 agent 协作”。

它的结构非常工程化，基本就是一条从协议理解到生产化落地的路线：

- `00_protocol_transports_spec`
  先看 A2A 的传输规范
- `01_a2a_fundamentals`
  学 agent card、discovery、skills 等基本概念
- `02_agent_executor`
  学如何封装一个符合 A2A 协议的 Agent 执行器
- `03_client_messaging`
  学客户端如何发现并向其他 Agent 发消息
- `04_streaming_and_tasks`
  学流式响应、任务状态与长任务管理
- `05_multi_agent_systems`
  进入真正的多 Agent 编排示例
- `06_human_in_loop`
  加入人工参与流程
- `07_multiturn_interaction`
  支持多轮会话与上下文持续
- `08_basic_security`
  开始补安全
- `09_mcp_a2a`
  讲 MCP 和 A2A 的衔接
- `10_multimodality`
  支持多模态内容
- `11_push_notifications`
  支持通知和异步回调
- `12_multiple_cards`
  处理更复杂的 agent card 场景
- `13_grpc_transport`
  延展到 gRPC 传输
- `14_authentication_authorization`
  认证与授权
- `15_security_hardening`
  安全加固
- `16_a2a_inspector`
  辅助观察和调试

这一部分最关键的认知是：

- MCP 主要解决 **agent 到 context / tools**
- A2A 主要解决 **agent 到 agent**

也就是说，A2A 不是在替代 MCP，而是在补多 Agent 协作层。

### `03_nanda`

这一部分讲的是 **NANDA（Networked Agents And Decentralized AI）**。它关注的问题不是单次调用，而是更上层的“Agent 网络基础设施”。

从这个目录的材料可以看出，NANDA 更像：

- Agent 世界里的发现与注册层
- 身份、信任、验证和路由层
- 跨协议互操作的基础设施层

可以把它理解为一种面向 Agent 互联网的构想：如果 MCP 是工具协议，A2A 是协作协议，那 NANDA 更像是 Agent 世界里的 DNS + PKI + 路由索引。

这一部分的价值主要在于建立前瞻视角，让你知道未来的 Agent 生态不只需要单点工具调用，还需要：

- agent registry
- cryptographic identity
- verified capability metadata
- cross-protocol discovery and routing

这部分更偏架构视野和生态理解，而不是立刻上手编码。

### `04_llms_txt`

这一部分相对短，但意义很清楚：它讲的是 `llms.txt` 这类面向 LLM / Agent 的网站声明文件。

可以把它类比成：

- `robots.txt` 是给搜索爬虫看的
- `llms.txt` 是给 LLM / Agent 系统看的

它关注的是网站或仓库如何声明：

- 哪些内容允许被模型读取
- 如何读取
- 有哪些面向 LLM 的使用说明

这一部分说明这个仓库不仅关心 Agent “怎么访问内容”，也关心内容提供方“如何向 Agent 暴露规则”。

## 本章主线

**当 Agent 不再是单机单模型，而是要调用工具、协作分工、跨平台通信、跨组织互联时，靠什么协议体系把它们接起来？**

这个模块给出的答案是分层的：

1. 先理解底层网络和 API 通信基础
2. 再理解 MCP 这种 agent-tool 标准
3. 再理解 A2A 这种 agent-agent 标准
4. 再往上理解 NANDA 这类 agent network 基础设施
5. 最后补充 `llms.txt` 这类面向 AI 抓取与访问治理的声明机制

## 检查清单

- 知道 HTTP、REST、JSON-RPC 为什么会成为 AI 协议的基础
- 知道 MCP 在 Agent 架构中的定位，不会把它误解成普通 API 包装
- 知道 A2A 解决的是多 Agent 协作，而不是工具调用
- 知道未来 Agent 系统不仅要“能调工具”，还要“能发现彼此、验证身份、跨协议协作”
- 知道 `llms.txt` 这类机制是在补 AI 时代的内容访问规范

## 
