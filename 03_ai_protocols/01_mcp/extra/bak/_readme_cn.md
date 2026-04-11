# 面向 Agentic 与多模态 AI 系统的基础协议

这个模块提供了一条按学习顺序组织的协议学习路径，帮助你从网络基础一路理解到现代 agent 系统中的应用层协议与未来方向。它既面向当前工程实践，也预留了对新兴协议的扩展空间。

## 前置要求

- 已完成 `01 AI Agents First Module`
- 具备现代 Python 基础，尤其是 `asyncio`

## 为什么这样组织

- **Agentic AI 系统** 依赖稳定、可互操作、可扩展的通信基础
- **多模态 agent** 需要支持文本、音频、视频、传感器等不同数据类型
- **未来可扩展性** 很重要，因此专门保留了 `extra` 区域跟踪新协议

## 学习路径概览

| 顺序 | 目录 | 说明 |
| :-- | :-- | :-- |
| 01 | `01_HTTP_Theory` | HTTP/1.1 基础 |
| 02 | `02_REST` | 面向资源的 API |
| 03 | `03_Streamable_HTTP` | 基于 HTTP 的流式通信 |
| 04 | `04_JSON_RPC` | 基于 JSON 的 RPC |
| 05 | `05_mcp_streamable_http_spec` | MCP 的 Streamable HTTP 传输规范 |

## 如何使用这个目录

- 按顺序学习主线目录，建立协议基础
- `extra` 是补充区域，用于追踪更前沿或更偏未来的通信技术，例如：
  - `00_IP`
  - `01_TCP`
  - `02_UDP`
  - `03_HTTP2`
  - `04_QUIC`
  - `05_HTTP3`
  - `06_WebRTC`
  - `07_WebTransport`
  - `08_WebCodecs`
  - `09_WebSockets`
  - `10_MQTT`
  - `11_SSE`
  - `12_GRPC`
  - `13_Future_AI_Protocols`

## 协议分类总结

### 核心部分

- **HTTP / REST**：通用 Web 与服务通信基础
- **Streamable HTTP / SSE**：流式与事件驱动数据传输
- **JSON-RPC**：结构清晰的远程调用模式

### 扩展部分

- **IP / TCP / UDP / QUIC**：网络传输基础
- **WebRTC / WebTransport / WebCodecs**：实时、多模态和低时延系统的重要组成
- **WebSockets / MQTT**：持久连接与轻量事件通信
- **Future AI Protocols**：面向未来的研究方向和新标准

这个目录的设计目标，是帮助你理解当前 agent 系统的通信现实，也为未来协议演进打下基础。
