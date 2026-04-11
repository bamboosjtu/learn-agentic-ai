# HTTP/2：更快、更高效的 Web 通信

HTTP/2 标准化于 RFC 9113，相比 HTTP/1.1 在性能上有显著提升。它引入了多路复用、头部压缩和二进制分帧层。本指南重点讲如何在本地、非浏览器场景中使用 **HTTP/2 Cleartext（h2c）** 进行练习，同时也会提到浏览器兼容所需的基于 TLS 的 HTTP/2。

---

## 它主要解决了什么问题：HTTP/1.1 的局限

HTTP/1.1 的主要问题包括：
- Head-of-Line Blocking（队头阻塞）
- 连接利用效率低
- Header 冗长重复

HTTP/2 通过在一条 TCP 连接上承载多个流，显著缓解了这些问题。

---

## HTTP/2 的关键特性与实际影响

1. **二进制分帧层**
   HTTP/2 消息不再是纯文本，而是二进制帧，更利于解析与扩展。

2. **多路复用与 Stream**
   多个请求 / 响应可以并发复用一条 TCP 连接，每个请求属于独立 stream。

3. **Header Compression（HPACK）**
   压缩重复 header，减少带宽浪费。

4. **Server Push**
   server 可以主动推送资源，不过这一能力更多出现在 HTTPS 场景中。

5. **流优先级**
   client 可以提示哪些资源更重要。

---

## 如何开始练习 HTTP/2（以 h2c 为主）

h2c 不需要 TLS 证书，因此很适合本地学习、程序化 client/server 测试。

### 1. 安装 Python 工具（使用 `uv`）

```bash
uv init http_code
cd http_code
uv add "httpx[http2]" "fastapi[standard]" hypercorn
```

这里的重点是：
- `httpx`：支持 HTTP/2 的 client
- `FastAPI`：构建 Web 服务
- `Hypercorn`：支持 HTTP/2 / h2c 的 ASGI server

---

## HTTP/2 Cleartext（h2c）示例

### 示例 1：FastAPI + h2c Server（`server_h2c.py`）

这个 server 用 FastAPI 提供两个接口：
- `GET /`
- `POST /data`

它会打印请求头、HTTP 版本，以及 client 信息，用来验证是否真的跑在 HTTP/2 上。

### 启动 h2c Server

```bash
uv run hypercorn server_h2c:app --bind "0.0.0.0:8000"
```

### 示例 2：h2c Client（`client_h2c.py`）

client 通过：
- `httpx.AsyncClient(http2=True, http1=False)`

向 server 发起 GET / POST 请求，并输出：
- 状态码
- 协议版本
- 响应 JSON

启动方式：

```bash
uv run python client_h2c.py
```

如果成功，你会看到 `HTTP Version: HTTP/2`。

---

## 如何练习与实验

1. **跑本地 h2c server + client**
2. **使用 `curl --http2-prior-knowledge` 测试 h2c**
3. **比较 HTTP/1.1 与 HTTP/2 的行为差异**

例如：

```bash
curl --http2-prior-knowledge http://localhost:8000/
```

**注意：** 浏览器通常不支持 h2c。h2c 更适合本地、受信任环境、或后端服务之间通信。

---

## HTTP/1.1 vs HTTP/2：核心差异

| 特性 | HTTP/1.1 | HTTP/2 |
| :---------------- | :-------------------------------- | :-------------------------------------------------- |
| **协议类型** | 文本 | 二进制帧 |
| **连接模型** | 每主机多连接 | 每主机单连接 |
| **多路复用** | 几乎没有 | 有 |
| **队头阻塞** | 严重 | 应用层解决，TCP 层仍存在 |
| **Header** | 明文重复 | HPACK 压缩 |
| **浏览器支持** | 直接支持 | 基本要求 TLS |

---

## HTTP/2 的优缺点

### 优势
- 性能更好
- 连接利用更高
- 更适合资源密集型页面和 API

### 缺点
- TCP 层 HOL blocking 仍存在
- Server Push 使用复杂

---

## HTTP/2 在 Agentic AI / DACA 中的意义

- **h2c**：适合受信任的后端服务通信
- **HTTPS/2**：适合浏览器、外部 API、第三方服务
- **gRPC**：建立在 HTTP/2 上，特别适合强类型微服务和 agent 通信

---

## 参考资源

- [RFC 9113: HTTP/2](https://datatracker.ietf.org/doc/html/rfc9113)
- [RFC 7541: HPACK](https://datatracker.ietf.org/doc/html/rfc7541)
- [`httpx` Documentation](https://www.python-httpx.org/)
- [`FastAPI` Documentation](https://fastapi.tiangolo.com/)
- [`Hypercorn` Documentation](https://pgjones.gitlab.io/hypercorn/)
- [MDN Web Docs: HTTP/2](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Evolution_of_HTTP#http2)
- [Cloudflare: What is HTTP/2?](https://www.cloudflare.com/learning/performance/http2-vs-http1.1/)
- [What is HTTP2?](https://www.upwork.com/resources/what-is-http2)
