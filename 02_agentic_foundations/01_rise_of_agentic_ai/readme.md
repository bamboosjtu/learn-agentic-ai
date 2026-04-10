# Agentic AI 的兴起

## 材料1概要

[详细课程大纲说明](https://docs.google.com/document/d/15usu1hkrrRLRjcq_3nCTT-0ljEcgiC44iSdvdqrCprk/edit?usp=sharing)

这份文档是 Panaversity 的 `Certified Agentic and Robotic AI Engineer` 项目说明，核心目标不是单纯讲概念，而是给出一条从入门到可落地的 Agentic AI 学习与实践路径，最终培养能够开发云原生智能体系统和机器人系统的工程师。

### 项目愿景

文档提出的愿景是 `Agentia World`：未来从智能家居、自动驾驶汽车、企业系统，到整座城市，都可能由彼此协作的 AI agent 构成。这里的重点不只是数字世界里的软件 agent，也包括能够进入物理世界的机器人和 Physical AI。

### 核心判断

- Agentic AI 的重点不是普通聊天，而是能理解上下文、调用工具、协同执行任务的智能体。
- 未来的系统交互方式会从传统 REST API 转向更动态的 agent-to-agent 对话。
- 要让 agent 真正可用，必须同时考虑智能性、可扩展性、可靠性和成本。
- 面向生产的 agent 系统，必须建立在云原生基础设施之上，而不是只停留在演示级原型。

### 主要挑战

文档明确提出的工程挑战是：如何设计一个能支撑 `1000 万` 并发用户、同时又尽量控制训练和部署成本的 AI agent 系统。

### DACA 架构

文档把 Dapr Agentic Cloud Ascent（DACA）作为核心实现方案。它的定位是一个面向大规模 agent 系统的设计模式，强调：

- `AI-first`：先把 agent 的推理、决策和工具使用能力设计清楚。
- `cloud-first`：再用云原生方式保证弹性、分布式和全球扩展能力。
- `OpenAI Agents SDK`：作为 agent 逻辑的基础框架，强调简单、直接、易上手。
- `MCP`：用于标准化工具接入。
- `A2A`：用于 agent 与 agent 之间的通信和协作。
- `Dapr`：用于分布式状态、消息、工作流等能力。
- `Docker / Rancher / Kubernetes`：用于容器化和部署编排。
- `Serverless / 托管服务`：用于降低运维负担并支持逐步扩展。

### 学习路径

这份文档的教学思路是先易后难，先让新手掌握 OpenAI Responses API 和 Agents SDK，再逐步进入云原生部署、长期运行的有状态 agent、以及更复杂的多智能体系统。它强调先建立清晰概念和动手能力，再进入复杂架构。

### 课程结构与培养目标

课程被分成两个层次：

- `Core level`：完成后就具备进入工作的基础能力。
- `Professional level`：可以在工作的同时继续进阶学习。

整体学习周期大约是 `1 年`，如果一次只学一门课；如果一个季度同时学多门课，可以缩短时长。文档还强调，学生在大约 `9 个月` 后就有机会面向全球认证、创业和自由职业机会。

### 技能方向

文档前期重点放在软件侧的 Vertical LLM Agents，也就是面向垂直场景的智能体开发；后续会扩展到 humanoid robots 和 Physical AI，把数字智能延伸到物理交互。

### 为什么这套项目重要

- 它面向的是未来高需求的 Agentic AI 工程能力，而不是只讲理论。
- 它把入门学习、云原生部署、分布式系统和机器人方向串成了一条连续路线。
- 它强调学生最终要具备构建可扩展、可部署、可运行的智能系统的能力。

### 对新手的直接结论

如果你是刚入门的开发者，这份文档传达的核心意思是：先学会用 OpenAI 的基础 API 和 Agents SDK 做出一个能工作的 agent，再把它迁移到云原生环境中，最后逐步扩展到多 agent 协作和机器人方向。它不是让你一开始就学最复杂的系统，而是按“概念 - 原型 - 部署 - 扩展”的顺序成长。

## 材料2概要

[Agentic AI 兴起幻灯片](https://docs.google.com/presentation/d/1MAtoPc_yjR9UIwktX-rioPiDhm08CIwRX2Gl5kODnqM/edit?usp=sharing)

这份幻灯片展示的是 Panaversity 的 Agentic AI 学习路线总览。它的重点不是单个工具，而是一整条从普通开发者走向 Agentic AI、云原生 AI 和机器人 AI 的进阶路径。

### 总体主线

幻灯片的主线可以概括为：

- 先学现代 Python 和 AI 辅助开发。
- 再学面向 agent 的开发方法和工具。
- 然后进入云原生部署、分布式运行和长期有状态系统。
- 最后扩展到多智能体协作、web-native agent 系统，以及 Physical AI / humanoid robotics。

### 课程分层

幻灯片背后的课程体系大致分为几层：

- `AI-101`：现代 Python 基础，为 AI 编程打底。
- `AI-300`：AI-Driven Development，学习如何和 AI 协作写软件。
- `AI-400`：Cloud-Native AI，学习 Docker、Kubernetes、Dapr 等云原生部署能力。
- `AI-210`：MCP、Agentic Memory、Agentic RAG 等 agent 能力增强主题。
- `AI-220`：A2A 协议和 Agentic Web，关注 agent 之间的协作和 web 场景。
- `AI-301`：Agent Native Cloud Development，面向云优先的 agent 部署。
- `AI-310`：Planet-Scale Distributed AI Agents，面向大规模分布式 agent 网络。
- `AI-451`：Physical and Humanoid Robotics AI，进入机器人和 Physical AI 方向。

### 关键观点

- AI 开发正在从“逐行写代码”转向“先写规格，再让 AI 协作实现”。
- 未来的开发者更像架构师和编排者，而不只是手写代码的人。
- Agentic AI 的学习不应该只停留在 prompt，而要覆盖上下文工程、工具接入、记忆、推理和系统部署。
- 真正可落地的 agent 系统必须考虑可观测性、扩展性、状态管理和云原生运行环境。
- 多智能体和机器人方向不是附加项，而是这条路线的自然延伸。

### 对新手的含义

对新手来说，这份幻灯片传达的最重要信息是：不要把 Agentic AI 理解成“会聊天的模型”，而要把它理解成一整套软件工程栈。你的成长顺序应该是先掌握 Python 和 AI 协作开发，再学 agent 逻辑和工具，再学云原生部署，最后进入多 agent 和机器人系统。

### 一句话总结

这份幻灯片实际是在讲：未来的 AI 开发路线不是单点工具学习，而是 `Python + AI 协作开发 + Agent SDK + MCP/A2A + 云原生 + 机器人` 的连续进阶体系。
