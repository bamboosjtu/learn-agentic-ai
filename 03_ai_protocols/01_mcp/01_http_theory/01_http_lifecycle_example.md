# 🔧 动手示例

让我们模拟一下 **你访问一个网页** 的过程。
我们会把它拆解成浏览器（客户端）和网站服务器之间的交互。

---

### 场景：你打开 `https://example.com/hello`

---

### 📤 HTTP 请求（从浏览器发往服务器）

```http
GET /hello HTTP/1.1
Host: example.com
User-Agent: Chrome/123.0
Accept: text/html
```

这表示：

* `GET`：你正在请求 **获取** 一个页面
* `/hello`：这是你要访问的网站路径
* `Host`：你正在与 `example.com` 通信
* `User-Agent`：你的浏览器类型
* `Accept`：你希望接收 `text/html`（网页）

---

### 📥 HTTP 响应（服务器返回给浏览器）

```http
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 38

<html><body>Hello, World!</body></html>
```

这表示：

* `200 OK`：成功，页面已找到
* `Content-Type`：返回的是 HTML 内容
* `Content-Length`：页面大小
* 消息体（body）：真正的网页内容

浏览器收到后，就会 **把页面展示出来**，你会看到 `Hello, World!`。

---

## 简单可视化示意图

下面是 **请求-响应循环** 的工作方式：

```
┌────────────┐       HTTP 请求            ┌───────────────┐
│  浏览器    │ ───────────────────────▶ │    服务器      │
│ （客户端） │                          │ (example.com) │
└────────────┘                          └───────────────┘
     ▲                                        │
     │       HTTP 响应（HTML 页面）           ▼
┌────────────┐ ◀────────────────────── ┌───────────────┐
│  你看到     │                          │    返回：      │
│ "Hello 🌍" │                          │   200 OK      │
└────────────┘                          │ HTML 页面     │
                                       └───────────────┘
```

---

## 用 `curl` 自己试试

如果你有终端（例如 Linux、macOS，或 Windows 上的 Git Bash），可以试试这个命令：

```bash
curl -v https://example.com
```

它会显示：

* 完整请求
* 完整响应
* 返回的 HTML 内容

---

## 关键结论

* HTTP 是 **浏览器（客户端）** 与 **网站（服务器）** 之间的一次 **对话**。
* 你发送一个 **请求**（请求页面或数据），服务器返回一个 **响应**（内容或错误）。
* 每次你加载任何网站时，背后都会发生这个过程。

