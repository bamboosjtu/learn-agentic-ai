# 未来的 AI 协议

随着 AI 系统从单模型调用发展为多 agent、跨工具、跨组织、跨模态的协作系统，新的通信协议也在不断出现。这个章节讨论的是一些正在形成中的标准、研究方向和可能影响下一代 agent 基础设施的协议思路。

---

## 概念总览

未来 AI 协议主要关注这些问题：

- agent 如何互相发现、协作、认证
- 工具与上下文如何标准化暴露给模型
- 多模态数据如何高效传输
- 分布式推理如何兼顾隐私与可审计性
- 大规模 agent 网络如何形成可互操作生态

原文提到了若干代表性方向：

- [Agent2Agent (A2A)](https://github.com/AgentOps/agent2agent)
- [Model Context Protocol (MCP)](https://github.com/AgentOps/model-context-protocol)
- [OpenTelemetry](https://opentelemetry.io/)
- [W3C Verifiable Credentials](https://www.w3.org/TR/vc-data-model/)

---

## 关键趋势

### 1. A2A 协议

用于 agent 与 agent 之间的互操作通信，例如：

- agent 身份描述
- 能力卡片（Agent Card）
- 跨厂商安全协作

### 2. MCP

MCP 关注的是模型如何发现和调用工具、资源与提示词，是连接 LLM 与工具生态的标准接口之一。

### 3. 多模态协议

未来 agent 系统不只处理文本，还会处理图像、音频、视频、传感器数据，因此协议需要支持更丰富的数据类型与流式处理。

### 4. 联邦与隐私保护推理

分布式训练、联邦学习、安全聚合、多方协作计算都会推动新协议演进。

### 5. 可解释与可审计

AI 系统需要日志、追踪、因果链记录，这也是 OpenTelemetry 等标准对 agent 系统重要的原因。

### 6. 身份与凭证

未来 agent 可能需要：

- 可验证身份
- 授权凭证
- 可追责的交互记录

---

## REST、WebRTC、WebTransport 的关系

原文还用较直白的方式比较了 REST 与更实时的协议：

- **REST**
  - 适合初始化、普通配置、非实时任务
  - 不适合极低时延和持续流式交互

- **WebRTC / WebTransport / WebSockets**
  - 更适合实时 agent 通信
  - 更适合流式、多模态和交互式推理系统

一个很实用的判断是：

- **非实时接口**：REST 依然有价值
- **实时协作**：优先考虑 WebSocket / WebTransport
- **点对点媒体**：考虑 WebRTC

---

## 更靠后的演进方向

原文还提到了几个值得关注的方向：

1. **WebTransport**
   作为 WebRTC 之外更偏客户端-服务端的低延迟通道

2. **WebCodecs + WebTransport**
   将“媒体编解码”和“传输协议”解耦

3. **MoQ（Media over QUIC）**
   面向大规模低延迟媒体分发的协议方向

4. **云通信平台**
   如 Agora、Twilio、LiveKit、Daily 等封装实时通信基础设施

5. **边缘计算 + AI 增强 RTC**
   包括边缘推理、隐私保护处理、智能压缩等

6. **XR / Spatial / Metaverse 通信**
   未来沉浸式多模态系统需要更强的实时协议栈

---

## 对工程师的启发

未来 AI 协议不是某一个单点标准，而更像一个组合：

- **A2A / MCP**：定义 agent 如何表达能力、上下文和调用关系
- **JSON-RPC / HTTP / gRPC / WebSocket / WebTransport**：承担传输与消息层
- **OpenTelemetry / Credentials / DID**：补足可观测性、身份与信任

也就是说，未来的 agent 基础设施很可能是一套“**标准组合件**”，而不是单一协议统一所有问题。

---

## 进一步阅读

- [Agent2Agent (A2A)](https://github.com/AgentOps/agent2agent)
- [Model Context Protocol (MCP)](https://github.com/AgentOps/model-context-protocol)
- [OpenTelemetry](https://opentelemetry.io/)
- [W3C Verifiable Credentials](https://www.w3.org/TR/vc-data-model/)
- [Decentralized Identifiers (DID)](https://www.w3.org/TR/did-core/)
