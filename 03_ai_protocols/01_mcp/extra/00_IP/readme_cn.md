# [Internet Protocol（IP）](https://www.cloudflare.com/learning/network-layer/internet-protocol/)

IP 协议（Internet Protocol）工作在网络层（OSI 第 3 层），负责数据包的寻址与路由。原始 IP 通信并不常见，因为 IP 通常要和 TCP、UDP 这类传输层协议配合，分别提供可靠通信或无连接通信。

在这一节里，你会构建一个使用原始 IP 的 client 和 server：client 发送 `ClientMessage` 包，server 回复 `ServerResponse`，以此理解最底层的网络通信方式。

## 什么是 IP？

IP 可以看作互联网的“邮政系统”，它负责把**数据包**从一个设备送到另一个设备，依赖的是 IP 地址（例如 `139.135.36.98`）。

IP 主要做三件事：
- **寻址（Addresses）**：给数据包标记源地址和目标地址
- **路由（Routes）**：在网络中找到传输路径
- **投递（Delivers）**：尽力把包送出去，但不保证送达

这里的 **Raw IP** 指的是你跳过 TCP/UDP，直接发送原始 IP 包，并使用 `proto=253` 这样的自定义协议号。它适合帮助你建立“未来 AI 协议从哪里开始”的直觉。

## 什么是数据包？

数据包就是网络上传输的数据单元，像一封封小信件。

在这个项目里：
- **Client Packet**：负载是 `ClientMessage`
- **Server Packet**：负载是 `ServerResponse`

一个 IP 包通常由两部分组成：
- **Header**：像信封，携带版本、长度、TTL、协议号、源 / 目标 IP 等
- **Payload**：真正的数据内容，例如 `ClientMessage`

之所以使用数据包，是因为：
- 小块数据更高效
- 每个数据包可以独立路由
- 很适合实时、多端、分布式 AI 系统

## 为什么没有端口？

端口通常由 TCP / UDP 使用，像楼栋里的“房间号”。而原始 IP 通信只依赖：
- **IP 地址**
- **协议号（Protocol Number）**
- **负载内容**

也就是说，你这里区分消息的方式不是端口，而是 `proto=253` 和 `ClientMessage` / `ServerResponse`。

---

## Scapy

[Scapy](https://scapy.net/) 是一个非常适合学习网络协议的 Python 工具。它可以：
- 构造数据包
- 捕获数据包（sniff）
- 解析数据包

它对初学者很友好，因为能自动帮你生成很多 header 字段，非常适合做 AI 协议原型实验。

### 什么是 Sniffing？

Sniffing 就是“抓包”。你可以把它理解成检查邮箱里是否收到某种类型的信件。

Scapy 的 `sniff()` 可以按过滤规则抓包，例如：
- `ip and proto 253`

这样：
- server 可以只抓 `ClientMessage`
- client 可以只抓 `ServerResponse`

这种定向抓包对于协议调试尤其重要。

### 什么是 Asyncio？

`asyncio` 是 Python 的异步并发工具，用于让程序高效地处理多个任务。

虽然 `asyncio` 不直接支持原始 IP，但它非常适合扩展到 TCP / UDP 场景，也非常契合未来多 agent 系统的并发通信模式。

---

## 环境准备

### 安装
```bash
uv init ip_hands_on
cd ip_hands_on
uv add scapy
```

## 动手实验：Raw IP Client-Server

本节推荐从 Scapy 开始，因为它最容易上手。你会基于：
- **Scapy**：最适合学习与抓包
- **Socket**：更底层，按字节操作
- **Asyncio**：适合理解未来 AI 系统中的并发扩展

### 前置条件

- **Python 3.13+**
- 本机网络接口，例如 `en0`
- 你自己的 IP 地址

使用如下命令查看：
```bash
ifconfig
```

## Scapy Server（`server.py`）

server 的核心逻辑是：
- 监听 `proto=253` 的 IP 包
- 如果收到 `ClientMessage`
- 就回发一个 `ServerResponse`

代码里重点关注：
- `sniff()` 抓包
- `handle_packet()` 处理逻辑
- `send()` 发送响应

## Scapy Client（`client.py`）

client 的核心逻辑是：
- 构造一个带 `ClientMessage` 的 IP 包
- 发送给目标地址
- 然后等待 server 返回的 `ServerResponse`

## 如何运行

1. 启动 server：
   ```bash
   sudo uv run python server.py
   ```
2. 运行 client：
   ```bash
   sudo uv run python client.py
   ```
3. 结束时按 `Ctrl+C`

如果直接使用公网 IP 不稳定，可以退回 loopback：
- `lo0`
- `127.0.0.1`

---

## 概念总结

### 核心理解
IP 的职责是把包送出去。它是无连接、不可靠的，但它是所有上层协议存在的基础。

### 关键特征
- **寻址**
- **路由**
- **无连接**
- **不保证可靠性**
- **支持分片**

### 优势
- 可扩展
- 灵活
- 是互联网的基础

### 缺点
- 不保证送达
- 没有端口语义
- 手工构造和调试更复杂

### AI 协议中的用途
- 自定义协议实验
- 低延迟场景
- 多 agent 实时数据交换

### 在协议栈中的位置
- **所在层级**：网络层（Layer 3）
- **上层协议**：TCP、UDP
- **下层介质**：以太网、Wi-Fi

---

## 故障排查

如果 client 无法正常通信，可以检查：

1. **接口是否正确**
   ```bash
   ifconfig
   ```
2. **防火墙**
3. **tcpdump 抓包**
   ```bash
   sudo tcpdump -i en0 ip and proto 253
   ```
4. **Wireshark**
5. **放宽过滤条件**，确认是不是过滤规则过严

---

**IP 是所有 agentic、多模态、AI 驱动通信的隐形底座。这个目录中的所有协议和数据交换，最终都依赖 IP 才能送达。**

## 延伸阅读

- [Scapy Documentation](https://scapy.readthedocs.io/en/stable/)
- [Python Socket](https://docs.python.org/3/library/socket.html)
- [Python Asyncio](https://docs.python.org/3.15/library/asyncio.html)
- [Cloudflare: IP](https://www.cloudflare.com/learning/network-layer/internet-protocol/)
