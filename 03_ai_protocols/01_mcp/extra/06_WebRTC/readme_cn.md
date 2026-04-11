# WebRTC：实时点对点通信

WebRTC（Web Real-Time Communication）是面向浏览器与移动应用的实时通信技术标准，支持音频、视频以及任意数据的低延迟点对点传输。视频会议、直播、远程协作、在线游戏等场景大量依赖它。

---

## WebRTC 核心概念

1. **`RTCPeerConnection`**
   WebRTC 的核心对象，负责建立 peer-to-peer 连接、媒体编解码、网络穿透和数据传输。

2. **`getUserMedia()`**
   获取摄像头、麦克风等媒体流。

3. **`RTCDataChannel`**
   在两个 peer 之间传输任意数据，适合文本消息、控制指令、文件片段等。

4. **Signaling（信令）**
   WebRTC 本身不定义“如何找到对方并交换协商信息”。因此通常要用 WebSocket、HTTP、TCP 等外部机制交换：
   - SDP Offer / Answer
   - ICE Candidates

5. **ICE / STUN / TURN**
   - **ICE**：寻找最佳网络路径
   - **STUN**：发现公网地址
   - **TURN**：无法直连时走中继

6. **强制加密**
   媒体通常通过 SRTP 加密，数据通道通过 DTLS 保护。

---

## WebRTC 连接流程

1. 双方创建 `RTCPeerConnection`
2. 发起方创建 offer
3. 另一方设置 remote description 并生成 answer
4. 双方交换 ICE candidate
5. 建立成功后，媒体流或 data channel 开始通信

---

## Python 中的 WebRTC：`aiortc`

虽然 WebRTC 最常见于浏览器，但 Python 可以通过 [`aiortc`](https://aiortc.readthedocs.io/) 参与 WebRTC 会话，适合：

- 服务端媒体处理
- WebRTC bot
- 网关 / 桥接层
- 自动化测试
- 后端 headless peer

### 安装

```bash
uv init hello_webrtc
cd hello_webrtc
uv add aiortc
```

### 原文示例说明

原文实现了一个 **基于 TCP 信令的 WebRTC Data Channel Echo** 示例：

- `webrtc_datachannel_server.py`
  - 监听 TCP 信令连接
  - 为每个 client 创建 `RTCPeerConnection`
  - 接收 data channel 消息并回显

- `webrtc_datachannel_client.py`
  - 通过 TCP 连接到信令 server
  - 主动创建 data channel
  - 发送 offer
  - 收到 answer 后建立连接
  - 发送几条测试消息并接收回显

这套示例重点不是浏览器端，而是帮助你理解：

- 信令与真正数据传输是分开的
- TCP 只负责交换 SDP/协商消息
- 一旦建立成功，data channel 走 WebRTC 直连链路

---

## 优势

- 真正的低延迟 P2P 通信
- 天然适合音视频
- 支持可靠或不可靠数据通道
- 浏览器原生支持广
- 强制加密，安全性较好

## 局限

- 实现复杂，组成部分多
- 需要额外信令机制
- NAT 穿透不总能成功，复杂场景往往要 TURN
- 大规模多人通信通常要 SFU / MCU
- 客户端媒体处理会消耗较多 CPU / 带宽

---

## 常见用途

- 音视频会议
- 实时游戏
- 屏幕共享 / 远程协作
- P2P 文件传输
- 机器人 / IoT / 实时控制

---

## WebRTC 在 DACA / A2A 中的意义

对于需要极低时延和直接点对点交互的 agent 场景，WebRTC 很有吸引力：

- agent 之间直接交换媒体或高速数据
- 浏览器端 agent UI 与 Python agent 直连
- 实时传感器流与控制指令并发传输

但代价也很明确：

- 需要独立信令基础设施
- NAT / TURN 运维复杂
- 对于普通业务消息，WebSocket、MQTT、gRPC 往往更易落地

---

## 协议栈位置

- **层级**：应用层组合技术
- **底层**：UDP 为主，也涉及 DTLS、SRTP、SCTP、ICE 等
- **信令**：通常在 WebSocket / HTTP / TCP 之上自定义

---

## 进一步阅读

- [WebRTC.org](https://webrtc.org/)
- [MDN WebRTC API](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API)
- [`aiortc` Documentation](https://aiortc.readthedocs.io/en/stable/)
