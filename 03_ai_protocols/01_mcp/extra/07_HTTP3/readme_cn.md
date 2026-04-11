# HTTP/3 与 QUIC（理论）

HTTP/3 是 HTTP 的最新主版本标准，定义于 [RFC 9114](https://www.rfc-editor.org/rfc/rfc9114.html)。它最根本的变化是：**不再跑在 TCP 上，而是运行在 QUIC 之上，而 QUIC 本身基于 UDP**。这一变化主要是为了解决 HTTP/1.1 与 HTTP/2 在 TCP 基础上仍然存在的性能瓶颈，尤其是队头阻塞。

---

## 为什么需要 HTTP/3

### HTTP/1.1 的问题

- 一个连接里串行请求容易阻塞
- 为了并发，浏览器往往要开多个 TCP 连接
- 头部冗余、握手开销大

### HTTP/2 的进步与遗留问题

HTTP/2 通过多路复用显著改善了 HTTP 层阻塞问题，但**TCP 层队头阻塞仍然存在**。只要一个 TCP 分段丢失，整个连接上的所有 HTTP/2 stream 都得等待重传。

### HTTP/3 的核心目标

HTTP/3 借助 QUIC 让多个 stream 真正独立，从而解决 TCP 层 HOL blocking。

---

## QUIC 带来的关键能力

1. **消除 TCP 层队头阻塞**
   某个 stream 丢包，只影响该 stream，不会拖慢整条连接。

2. **更快的握手**
   QUIC 将 TLS 1.3 握手整合到建连流程中，支持 1-RTT，部分场景还可做到 0-RTT。

3. **连接迁移**
   客户端切换网络时，连接可以依赖 Connection ID 持续存在。

4. **默认加密**
   QUIC 所有流量默认加密，安全是协议内建能力。

5. **更易演进**
   QUIC 多在用户态实现，相比内核态 TCP 更容易快速迭代。

---

## HTTP/3 的关键点

- **建立在 QUIC 之上**
- **Header Compression 使用 QPACK**
- **支持多路复用**
- **保留优先级与推送能力**

QPACK 是为 QUIC 的乱序流交付场景设计的，解决了 HPACK 不适合该场景的问题。

---

## HTTP/1.1 / HTTP/2 / HTTP/3 对比

| 特性 | HTTP/1.1 | HTTP/2 | HTTP/3 |
| :-- | :-- | :-- | :-- |
| 传输层 | TCP | TCP | QUIC over UDP |
| 多路复用 | 基本没有 | 有 | 有 |
| 队头阻塞 | 明显 | HTTP 层解决，TCP 层仍在 | 传输层基本消除 |
| 握手速度 | TCP + TLS | TCP + TLS | QUIC + TLS 1.3 |
| 加密 | HTTPS 可选 | 浏览器场景几乎默认 TLS | 强制 TLS 1.3 |
| Header 压缩 | 无标准 | HPACK | QPACK |
| 连接迁移 | 否 | 否 | 是 |

---

## 优势

- 在高时延、丢包网络中表现更好
- 连接建立更快
- 移动网络与长连接场景更稳
- 默认安全
- 更适合高并发、多 stream 业务

## 局限

- 某些网络环境仍可能限制 UDP
- 实现复杂度与 CPU 开销更高
- 周边调试工具链仍在持续成熟

---

## HTTP/3 在 Agentic AI / DACA 中的意义

- **低时延工具调用**：适合需要快速响应的 agent
- **高并发流处理**：一个 agent 同时处理多个数据流更高效
- **移动与边缘计算**：连接迁移非常适合不稳定网络环境
- **大规模分布式系统**：更适合未来高并发、多模态 AI 基础设施

---

## 进一步阅读

- [RFC 9114: HTTP/3](https://datatracker.ietf.org/doc/html/rfc9114)
- [RFC 9000: QUIC](https://datatracker.ietf.org/doc/html/rfc9000)
- [RFC 9204: QPACK](https://datatracker.ietf.org/doc/html/rfc9204)
- [HTTP/3 Explained](https://http3-explained.haxx.se/)
