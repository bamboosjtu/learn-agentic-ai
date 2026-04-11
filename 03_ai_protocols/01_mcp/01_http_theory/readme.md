# HTTP 基础（理论）

HTTP（Hypertext Transfer Protocol，超文本传输协议）是用于传输超媒体文档（如 HTML）以及在万维网上交换结构化数据的基础应用层协议。它是 **计算机在互联网上彼此通信的方式**。

📌 可以这样理解：

> 你（浏览器）走进一家 **餐厅**（服务器），看着 **菜单**（网页），再告诉 **服务员**（HTTP）你想要什么。服务员去厨房（服务器逻辑）取餐，再把菜品（响应，例如 HTML、JSON、图片等）端给你。


## 为什么 HTTP 很重要？

每当你：

* 打开一个网站
* 提交一个表单
* 登录一个网站
* 观看一个视频

背后都在使用 **HTTP**！HTTP 是互联网数据通信的骨干，让用户能够访问网站和各种在线资源。[[1]](https://www.freecodecamp.org/news/what-is-http/)

HTTP 的发展史也是一个持续演进的过程，由 Web 对速度、效率和新能力的需求所推动。每一个 HTTP 版本都建立在前一代之上，解决旧限制，并为今天复杂的交互形式铺路。

```ascii
+------------------------------------------------------+
|                   Application Layer                  |
| +---------------------+   +------------------------+ |
| | HTTP (1.x, 2)       |   | HTTP/3 (over QUIC)     | |
| | (Web, APIs)         |   | (Modern Web, Low-Latency)| |
| +--------^------------+   +-----------^------------+ |
|          |                            | (QUIC)       |
|          |                            |              |
| +--------|----------------------------|------------+ |
| |        Transport Layer              |            | |
| | +------V-----+        +-----------V----------+ | |
| | | TCP        |        | UDP                  | | |
| | | (Reliable) |        | (Fast, Connectionless)| | |
| | +------^-----+        +-----------^----------+ | |
| +--------|----------------------------|------------+ |
|          |                            |              |
| +--------|----------------------------|------------+ |
| |        Network/Internet Layer       |            | |
| | +------V-------------V--------------+            | |
| | | IP (Addressing & Routing)         |            | |
| | +-----------------------------------+            | |
+------------------------------------------------------+
```

---

## HTTP 核心概念

理解 HTTP，需要掌握几个决定其工作方式的关键概念：

### 1. HTTP 请求-响应循环

HTTP 通信遵循客户端-服务器模型，以及清晰的请求-响应循环：

1. **客户端发起连接**：客户端（例如浏览器）通常会与服务器建立 TCP/IP 连接（HTTP 通常使用 80 端口，HTTPS 通常使用 443 端口）。
2. **客户端发送 HTTP 请求**：客户端发送一个 HTTP 请求消息。该消息会说明：
   - 希望执行的动作（如 `GET`、`POST` 等 HTTP 方法）。
   - 目标资源（URL）。
   - 使用的 HTTP 协议版本。
   - 包含附加信息的头部（例如客户端能力、Cookie）。
   - 可选的消息体（例如 `POST` 请求携带的表单数据或 JSON）。
3. **服务器处理请求**：服务器接收并解析请求，然后执行相应操作，例如获取文件、查询数据库或运行脚本。
4. **服务器发送 HTTP 响应**：服务器向客户端返回一个 HTTP 响应消息，其中包括：
   - HTTP 协议版本。
   - 表示结果的状态码（例如 `200 OK`、`404 Not Found`）。
   - 描述状态的原因短语（reason phrase）。
   - 包含响应元数据的头部（例如内容类型、服务器信息）。
   - 可选的消息体，包含请求的资源或错误信息。
5. **客户端处理响应**：客户端接收并处理响应，例如渲染 HTML 页面或解析 JSON 数据。
6. **连接管理**：根据 HTTP 版本及相关头部（如 `Connection: keep-alive`），底层 TCP 连接可能被关闭，也可能保持打开以复用后续请求。

### 2. HTTP 消息的结构

请求与响应具有相似的结构：

- **起始行（Start-line）**：请求和响应不同。请求包含（Method、URI、HTTP-Version），响应包含（HTTP-Version、Status-Code、Reason-Phrase）。
- **HTTP 头部**：一组键值对，用于提供请求 / 响应或消息体的元数据。例如 `Content-Type`、`User-Agent`、`Cache-Control`。
- **空行（CRLF）**：一行空白行，用于分隔头部和消息体。
- **消息体（可选）**：实际传输的数据（例如 HTML、JSON、图片数据）。其存在与格式通常通过 `Content-Type`、`Content-Length` 等头部说明。

### 3. 常见 HTTP 方法（Verbs）

HTTP 方法定义了对资源执行的动作：

- **`GET`**：获取资源的一个表示。
- **`POST`**：提交待处理的数据，通常会创建新资源。
- **`PUT`**：用请求负载整体替换目标资源的当前表示。
- **`DELETE`**：删除指定资源。
- **`HEAD`**：类似 `GET`，但只返回头部，不返回消息体。
- **`OPTIONS`**：描述目标资源支持的通信选项。
- **`PATCH`**：对资源应用部分修改。

### 4. HTTP 状态码

响应中的状态码用来表明请求结果：

- **1xx（信息性）**：请求已收到，正在继续处理（例如 `100 Continue`）。
- **2xx（成功）**：请求已成功接收、理解并接受（例如 `200 OK`、`201 Created`）。
- **3xx（重定向）**：完成请求还需要进一步操作（例如 `301 Moved Permanently`、`304 Not Modified`）。
- **4xx（客户端错误）**：请求语法错误或无法完成（例如 `400 Bad Request`、`401 Unauthorized`、`404 Not Found`）。
- **5xx（服务器错误）**：服务器未能完成一个看起来有效的请求（例如 `500 Internal Server Error`、`503 Service Unavailable`）。

### 5. 无状态性（Statelessness）

HTTP 天生是无状态的。服务器默认不会保存同一客户端先前请求的上下文，每一次请求都会被独立处理。为了管理用户会话或跨多个请求保持状态（例如登录状态、购物车），应用程序通常会在 HTTP 之上实现有状态机制，例如 Cookie、放在头部中的会话令牌，或 URL 重写。

### 6. HTTP 头部

头部是 HTTP 的关键扩展机制，用来承载重要元数据。常见分类包括：

- **通用头部（General Headers）**：请求和响应都可以使用（例如 `Date`、`Connection`）。
- **请求头（Request Headers）**：仅用于请求（例如 `User-Agent`、`Accept`、`Authorization`）。
- **响应头（Response Headers）**：仅用于响应（例如 `Server`、`Set-Cookie`、`Content-Type`）。
- **实体头（Entity Headers）**：在现代 RFC 中通常称为 **表示头（Representation Headers）**，用于描述负载内容（例如 `Content-Length`、`Content-Encoding`）。

---

## HTTP 为什么会演进：理解它如何一步步支撑现代 Agentic AI 通信

HTTP 的发展史，是 Web 不断追求速度、效率和新能力的历史。对于 Agentic AI 工程师来说，理解这种演进非常关键。这不只是历史知识，更像是一堂关于“协议如何针对真实世界瓶颈进行演化”的实践课，例如如何解决延迟和并发问题。这些经验可以直接迁移到智能体通信骨干的设计中。每一个 HTTP 版本都建立在前一版之上，解决当时的限制，并为后续更复杂的交互打下基础。


### [HTTP/0.9](https://http.dev/0.9)：极简起点（1990 年代早期）

* **需求：** 为刚诞生的万维网提供一种获取超文本文档的基本方式。
* **“协议”是什么：** 极其简单。客户端只发送一行：`GET /path/to/document`。没有版本号、没有头部、没有状态码。服务器只返回 HTML 内容，然后关闭连接。
* **启示：** 它在当时的有限场景下够用，但完全无法支持更丰富的交互。比如，想向服务器提交数据，或者判断请求是否失败，在 HTTP/0.9 里都是做不到的。

### [HTTP/1.0](https://http.dev/1.0)：加入结构化能力（RFC 1995 - 1996）

* **需求：** HTTP/0.9 太原始了，Web 需要在请求和响应中传递更多信息。
* **关键改进：**
  * **版本号：** 请求中明确写出 `HTTP/1.0`。
  * **HTTP 头部：** 允许客户端与服务器传递附加信息（例如用 `Content-Type` 标明数据格式，用 `User-Agent` 标识客户端）。
  * **状态码：** 标准化响应结果，如 `200 OK`（成功）或 `404 Not Found`。
  * **新方法：** 引入了 `POST`（向服务器发送数据）和 `HEAD`（仅获取头部）。
* **持续存在的问题：** HTTP/1.0 通常会为 **每一个请求** 新建一个 TCP 连接。一个包含多张图片的网页，就意味着要建立很多次连接，带来明显延迟。对于需要频繁快速交换信息的智能体系统，这种模式会非常低效。
* **参考：** [RFC 1945 - Hypertext Transfer Protocol -- HTTP/1.0](https://datatracker.ietf.org/doc/html/rfc1945)

### [HTTP/1.1](https://http.dev/1.1)：长期服役的主力版本（RFC 9112 - 2022，取代如 2616 等早期 RFC）

* **需求：** 解决 HTTP/1.0 的低效问题，尤其是“每个请求都新建连接”的高开销。
* **关键改进：**
  * **持久连接（Keep-Alive）**：这是一次关键飞跃。单个 TCP 连接可以复用来承载多次请求与响应，显著降低延迟。这是高效通信中的基础概念。
  * **管线化（Pipelining）**：允许客户端连续发送多个请求，而不必等待前一个响应返回。但服务器必须按顺序返回响应，这会导致 **队头阻塞（Head-of-Line, HOL Blocking）**，即一个慢响应会卡住后面的所有响应。
  * **Host 头**：使得多个网站共享同一个 IP 地址成为可能（虚拟主机）。
  * 更完善的缓存、内容协商等机制，使其更加健壮。
* **当前状态：** HTTP/1.1 **至今仍被广泛使用**。许多 API 和 Web 服务依然依赖它，因为它简单且兼容性极强。它也是理解 Web 通信的基础版本。
* **瓶颈：** 虽然比 HTTP/1.0 好很多，但 HOL 阻塞仍然存在；同时，文本格式的头部也显得冗长且重复。
* **参考：** [RFC 9112 - HTTP/1.1](https://datatracker.ietf.org/doc/html/rfc9112)

### HTTP/2：为现代速度而设计（RFC 9113 - 2022，取代 RFC 7540）

* **需求：** 解决 HTTP/1.1 的性能限制，尤其是 HOL 阻塞和头部开销，以支持更丰富、更强交互性的 Web 应用。
* **关键改进（底层进行了大幅重构）：**
  * **二进制分帧（Binary Framing）**：消息不再是纯文本，而是被拆分成更小的二进制“帧”。这让计算机更容易解析，也为多路复用提供了基础。
  * **多路复用（Multiplexing）**：多个请求和响应可以在同一个 TCP 连接上并发发送和接收，互不阻塞。这实际上消除了 HTTP/1.1 层面的 HOL 阻塞。对于需要大量并行通信的智能体系统，这一点非常关键。
  * **头部压缩（HPACK）**：降低 HTTP 头部大小，节省带宽，尤其适合频繁的 API 调用。
  * **服务器推送（Server Push）**：服务器可以主动发送客户端可能马上需要的资源。
* **当前状态：** 现代浏览器和 Web 服务器已广泛采用 HTTP/2。它显著提升了性能，常用于高并发、低延迟要求的应用场景。
* **仍然存在的 TCP 问题：** HTTP/2 虽然解决了 **HTTP 自身层面** 的 HOL 阻塞，但底层仍然跑在 TCP 上。如果某个 TCP 数据包丢失，整个 TCP 连接（以及该连接上的所有 HTTP/2 流）都必须等待重传完成后才能继续。
* **参考：** [RFC 9113 - HTTP/2](https://datatracker.ietf.org/doc/html/rfc9113)

### HTTP/3：下一代方案，构建在 QUIC 之上（RFC 9114 - 2022）

* **需求：** 消除仍然影响 HTTP/2 的 TCP 层 HOL 阻塞，并进一步降低连接延迟。
* **根本性变化：QUIC**
  * HTTP/3 不再运行在 TCP 之上，而是运行在 **QUIC（Quick UDP Internet Connections）** 之上（[RFC 9000](https://datatracker.ietf.org/doc/html/rfc9000)）。QUIC 是构建在 UDP 之上的新型传输协议。
  * **独立流（Independent Streams）**：QUIC 可以独立复用多条流。如果某一条流丢包，只会影响该流，不会拖住同一 QUIC 连接上的其他流。这终于从根本上解决了深层 HOL 阻塞问题。
  * **更快的连接建立**：QUIC 将 TLS 加密（必须使用 TLS 1.3 或更新版本）整合进握手流程，经常可以做到 0-RTT（零往返时间）或 1-RTT 连接。
  * **连接迁移（Connection Migration）**：即使客户端 IP 地址变化（例如从 Wi-Fi 切换到蜂窝网络），连接也可以继续存活。
* **当前状态：** HTTP/3 的采用率 **正在持续增长，仍处于走向主流的过程中**。主流浏览器、CDN 和大型科技公司都已支持。虽然它还不像 HTTP/1.1 或 HTTP/2 那样无处不在，但它代表了 Web 性能的前沿，尤其适合复杂网络环境。对于追求最低延迟和最高韧性的 Agentic 系统，HTTP/3 是未来方向。
* **参考：** [RFC 9114 - HTTP/3](https://datatracker.ietf.org/doc/html/rfc9114)

演进路线
---

从最初的简单文档获取，到高度优化的多路复用通信，再到运行在新型传输协议上的下一代方案，对于设计和排查复杂 Agentic AI 系统中的通信层非常有价值。每一步，本质上都在解决真实世界的问题，让交互更快、更可靠。

## HTTP 与安全（HTTPS）

HTTP 本身是明文协议，也就是说传输的数据没有加密，可能被拦截或篡改。为了保护 HTTP 通信，会使用 **HTTPS（HTTP Secure）**。

- HTTPS 本质上就是运行在 **TLS（Transport Layer Security）** 之上的 HTTP，它的前身是 SSL（Secure Sockets Layer）。
- TLS 提供：
  - **加密（Encryption）**：防止数据被窃听。
  - **完整性（Integrity）**：确保传输过程中的数据没有被篡改。
  - **身份认证（Authentication）**：通过数字证书验证服务器身份（也可选验证客户端）。

与 HTTP/HTTPS 相关的重要安全点包括：

- 始终优先使用 HTTPS 来保护敏感数据。
- **HTTP Strict Transport Security（HSTS）**：一种策略机制，强制浏览器只使用 HTTPS。
- **Cookie**：需要通过 `HttpOnly`、`Secure`、`SameSite` 等属性进行安全控制。
- **输入校验（Input Validation）**：无论使用哪个 HTTP 版本，应用层都必须做好输入校验，以防止常见 Web 漏洞（如 XSS、SQL 注入）。
- **跨域资源共享（CORS）**：通过一组 HTTP 头部控制不同域之间的资源请求方式。

---

## 实战示例：原始 HTTP 请求与响应消息

下面的示例展示了 `GET` 与 `POST` 方法的原始 HTTP 请求 / 响应文本格式，用来直观说明“HTTP 消息结构”一节中的内容。通过这些原始消息，你可以看到协议中的各个部分，例如起始行、头部和消息体，是如何在真实场景中组合起来的。

## 示例概览

本节包含 4 段原始 HTTP 消息：
- 一个用于获取 HTML 页面（`/resource/example.html`）的 `GET` 请求。
- 服务器返回 HTML 文档的 `GET` 响应。
- 一个向 API 端点（`/api/submit`）提交 JSON 数据的 `POST` 请求。
- 服务器返回 JSON 确认信息的 `POST` 响应。

这些消息模拟的是客户端与 `example.com` 上的假想服务器之间基于 HTTP/1.1 的交互。后续解释会拆解每条消息的组成，并将它们与教程中的理论概念对应起来。

## 如何探索这个示例

你可以直接在本文档中阅读下面嵌入的原始 HTTP 消息。如果你想亲自实验：
1. 复制这些请求文本，并使用 `curl` 或 `telnet` 等工具把它们发送到真实服务器（记得把 `example.com` 替换成真正支持这些端点的服务器）。
2. 或者，你也可以搭建一个本地 HTTP 服务器（例如使用 Python 的 `http.server`、Node.js 或 Apache），来处理这些请求并观察响应。
3. 使用 Wireshark 之类的网络工具抓取真实的 HTTP 流量，并与这些示例对照。
4. 将这些消息的组成部分，与教程中“HTTP 核心概念”部分的描述进行逐项比较。

## 原始 HTTP 消息及其组成部分

下面给出原始 HTTP 消息，每条消息后面都附有组成解释。消息格式与真实网络传输中的形式保持一致，包含正确的换行和空格。

### 1. GET 请求
```
GET /resource/example.html HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
```

**解释**：
- **起始行**：`GET /resource/example.html HTTP/1.1`
  - **方法**：`GET`，请求指定路径上的资源。
  - **URI**：`/resource/example.html`，标识目标资源（一个 HTML 页面）。
  - **HTTP 版本**：`HTTP/1.1`，指定所使用的协议版本。
- **头部**：
  - `Host: example.com`：指定服务器域名，是虚拟主机场景下的必需字段。
  - `User-Agent`：标识客户端（例如浏览器类型、版本、操作系统等）。
  - `Accept`：列出可接受的响应格式（优先 HTML、XHTML、XML 等）。
  - `Accept-Language`：表示偏好语言（这里优先英语，美国英语优先级更高）。
  - `Accept-Encoding`：说明支持的压缩格式（gzip、deflate）。
  - `Connection: keep-alive`：请求服务器保持 TCP 连接，以便后续复用。
- **空行**：空白行（CRLF）用于分隔头部和消息体。
- **消息体**：无。`GET` 请求通常不带消息体，因为它的语义是获取数据。

### 2. GET 响应
```
HTTP/1.1 200 OK
Date: Thu, 12 Jun 2025 08:51:00 GMT
Server: Apache/2.4.41 (Unix)
Content-Type: text/html; charset=UTF-8
Content-Length: 51
Connection: keep-alive

<html>
<head><title>Example</title></head>
<body><h1>Hello, World!</h1></body>
</html>
```

**解释**：
- **起始行**：`HTTP/1.1 200 OK`
  - **HTTP 版本**：`HTTP/1.1`，与请求版本保持兼容。
  - **状态码**：`200`，表示请求成功。
  - **原因短语**：`OK`，是对状态的可读描述。
- **头部**：
  - `Date`：响应生成的时间戳。
  - `Server`：标识服务器软件（此处为 Apache）。
  - `Content-Type: text/html; charset=UTF-8`：说明响应体是 UTF-8 编码的 HTML。
  - `Content-Length: 51`：表示响应体长度为 51 字节。
  - `Connection: keep-alive`：确认 TCP 连接可以保持打开以供后续请求复用。
- **空行**：分隔头部和消息体。
- **消息体**：包含一个简单的 HTML 文档（`<html>...</html>`），客户端（例如浏览器）可以直接渲染它。

### 3. POST 请求
```
POST /api/submit HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Accept: application/json
Content-Type: application/json
Content-Length: 47
Connection: keep-alive

{
  "name": "Alice",
  "message": "Hello, Server!"
}
```

**解释**：
- **起始行**：`POST /api/submit HTTP/1.1`
  - **方法**：`POST`，向服务器提交数据以供处理。
  - **URI**：`/api/submit`，用于接收提交数据的 API 端点。
  - **HTTP 版本**：`HTTP/1.1`。
- **头部**：
  - `Host`、`User-Agent`、`Connection`：与 GET 请求类似，分别提供服务器、客户端和连接信息。
  - `Accept: application/json`：表示客户端希望接收 JSON 格式的响应。
  - `Content-Type: application/json`：说明请求体中的数据格式是 JSON。
  - `Content-Length: 47`：JSON 请求体的字节长度。
- **空行**：分隔头部和消息体。
- **消息体**：一个 JSON 对象（`{"name": "Alice", "message": "Hello, Server!"}`），用于向服务器提交待处理的数据。

### 4. POST 响应
```
HTTP/1.1 201 Created
Date: Thu, 12 Jun 2025 08:51:05 GMT
Server: Apache/2.4.41 (Unix)
Content-Type: application/json
Content-Length: 75
Connection: keep-alive

{
  "received": {"name": "Alice", "message": "Hello, Server!"},
  "status": "success"
}
```

**解释**：
- **起始行**：`HTTP/1.1 201 Created`
  - **HTTP 版本**：`HTTP/1.1`。
  - **状态码**：`201`，表示资源已成功创建或数据已成功处理。
  - **原因短语**：`Created`，描述成功结果。
- **头部**：
  - `Date`、`Server`、`Connection`：与 GET 响应类似，用于提供元数据。
  - `Content-Type: application/json`：说明响应体是 JSON。
  - `Content-Length: 75`：JSON 响应体长度。
- **空行**：分隔头部和消息体。
- **消息体**：一个 JSON 对象，用于确认已收到提交的数据（`"received"`）并返回成功状态（`"status": "success"`）。

## 本示例体现的关键 HTTP 概念

这个示例与教程中的“HTTP 核心概念”部分直接对应，具体展示了：
- **请求-响应循环**：客户端发送请求（`GET` 或 `POST`），服务器返回带有状态码、头部和可选消息体的响应。
- **HTTP 方法**：`GET` 用于获取数据（例如 HTML 页面）；`POST` 用于提交数据（例如 JSON）供服务器处理。
- **状态码**：`200 OK` 表示成功获取，`201 Created` 表示成功提交 / 创建。
- **头部**：用于提供元数据，例如 `Content-Type`（消息体格式）、`Content-Length`（消息体大小）和 `Connection`（连接管理）。
- **消息结构**：每条消息都包含起始行、头部、一行空白分隔（CRLF）以及可选的消息体，这与教程中的结构说明完全一致。
- **无状态性**：每个请求都自包含，所需信息都在头部和消息体中，不依赖服务器在请求之间保存状态。



---

## Agentic AI 系统中的用例（DACA 语境）

HTTP 在分布式 Agentic AI 平台（例如 DACA）中是核心通信基石之一，通常以 HTTPS 形式出现，并覆盖多个场景：

- **API 通信**：智能体与智能体之间（A2A 协议）、与工具、服务以及大语言模型（LLM）之间交互的主要方式。
  - **RESTful API**：因其简单、无状态而被广泛使用，直接利用 HTTP 方法和状态码。MCP 也可以构建在 HTTP 之上。
  - **gRPC**：通常以 HTTP/2 作为传输层，用于高效、强类型的服务间通信。
  - **GraphQL**：为 API 提供灵活查询语言，通常也通过 HTTP 提供服务。
- **Webhook**：用于事件驱动通信。当其他系统发生事件时，智能体通过 HTTP POST 请求接收通知。
- **用户界面与仪表盘**：为 Human-in-the-Loop（HITL）交互、监控与配置提供基于 Web 的 UI（例如 Streamlit、Next.js、FastAPI + HTML）。
- **数据采集**：智能体从网页（Web 抓取）或外部 API 拉取数据。
- **服务发现与健康检查**：DACA 内部服务（例如启用 Dapr 的应用、Kubernetes Pod）会暴露 HTTP 端点，用于发现与健康监控。

在 DACA 中为某类交互选择 HTTP/1.1、HTTP/2 或 HTTP/3，取决于性能要求、客户端 / 服务器能力和网络条件。对于 Agentic 系统中常见的高并发、性能敏感场景，HTTP/2 和 HTTP/3 更值得优先考虑。

---

## 延伸阅读与参考资料

- **Python 文档（概念层面）**：
  - [`http` 模块概览](https://docs.python.org/3/library/http.html)（提供了 `HTTPStatus`、`HTTPMethod` 等枚举，对理解概念很有帮助）
- **RFC（互联网标准，最权威来源）**：
  - [RFC 9110: HTTP Semantics](https://datatracker.ietf.org/doc/html/rfc9110)
  - [RFC 9112: HTTP/1.1](https://datatracker.ietf.org/doc/html/rfc9112)
  - [RFC 9113: HTTP/2](https://datatracker.ietf.org/doc/html/rfc9113)（取代 RFC 7540 中的 HTTP/2 规范）
  - [RFC 9114: HTTP/3](https://datatracker.ietf.org/doc/html/rfc9114)
  - [RFC 9000: QUIC: A UDP-Based Multiplexed and Secure Transport](https://datatracker.ietf.org/doc/html/rfc9000)
- **Web 资料**：
  - [MDN Web Docs: An overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)
  - [MDN Web Docs: Evolution of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Evolution_of_HTTP)
  - [freeCodeCamp: What is HTTP? Protocol Overview for Beginners](https://www.freecodecamp.org/news/what-is-http/) [[1]]
  - [Cloudflare: What is HTTP?](https://www.cloudflare.com/learning/ddos/glossary/hypertext-transfer-protocol-http/)
  - [web.dev by Google: HTTP/2](https://web.dev/articles/performance-http2), [HTTP/3](https://web.dev/articles/http3)
