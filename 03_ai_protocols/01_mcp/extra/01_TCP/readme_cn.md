# 02 [Transmission Control Protocol（TCP）](https://www.geeksforgeeks.org/what-is-transmission-control-protocol-tcp/)

TCP 是传输层的核心协议之一，负责在网络中的应用之间提供**可靠、有序、带错误检查**的数据传输。网页浏览、邮件、API 调用等大多数互联网应用都建立在 TCP 之上。

---

## Socket 的历史背景

Socket 最早可以追溯到 1971 年的 ARPANET，并在 1983 年随着 BSD 系统发展为广泛采用的 Berkeley sockets API。虽然网络协议不断演进，但底层 socket 编程模型一直非常稳定。Python 的 `socket` 模块就是对这一经典接口的封装。

## 在 Python 中使用 TCP：`socket`

Python 内置的 [`socket`](https://docs.python.org/3/library/socket.html) 是构建 TCP client / server 的标准方式。

它的基本能力包括：
- 创建 client / server
- 建立连接
- 收发数据
- 管理连接生命周期

### 不需要额外安装

`socket` 属于 Python 标准库，无需额外安装。

### 示例 1：基础 TCP Server

```python
import socket

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received: {data.decode()}")
            conn.sendall(data)
```

### 示例 2：基础 TCP Client

```python
import socket

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, TCP server!')
    data = s.recv(1024)

print(f"Received from server: {data.decode()}")
```

---

## 概念总览

### 什么是 TCP？

TCP（Transmission Control Protocol）是一种**面向连接**的协议，它在传输层（OSI 第 4 层）工作，负责保证数据可靠、有序地送达。HTTP、SMTP、FTP、数据库连接等常见场景都依赖它。

### 关键特征

- **可靠传输**：通过确认、重传等机制确保数据最终送达
- **面向连接**：在传输前要先建立连接（三次握手）
- **有序交付**：保证数据按发送顺序到达
- **流量控制**：避免发送方压垮接收方
- **拥塞控制**：根据网络状况调整发送速率
- **错误检测和恢复**：使用校验和、序列号等机制
- **全双工通信**：一条连接上可同时双向传输

## Socket 生命周期

一个典型 TCP socket 交互包括：

1. **创建 socket**
   `socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
2. **绑定（server）**
   `bind((HOST, PORT))`
3. **监听（server）**
   `listen()`
4. **连接（client）**
   `connect((HOST, PORT))`
5. **接受连接（server）**
   `accept()`
6. **数据交换**
   - `send()`
   - `sendall()`
   - `recv()`
7. **关闭连接**
   - `shutdown()`
   - `close()`

## 阻塞与非阻塞 Socket

- **阻塞 socket（默认）**
  - `connect()`、`accept()`、`recv()` 等调用会一直等到结果出现
  - 简单直观，适合入门和小规模应用

- **非阻塞 socket**
  - 通过 `setblocking(False)` 设置
  - 调用会立即返回
  - 常与 `select` / `selectors` 搭配，用于高并发连接管理

## 二进制数据处理

TCP 传的是字节流。如果传输整数、结构化数据、浮点数等二进制内容，需要注意：

- **字节序（Endianness）**
- **消息边界（Message Framing）**

因为 TCP 是流协议，没有天然消息边界，所以应用层通常要定义：
- 固定长度消息
- 长度前缀
- 特殊分隔符

## 多连接处理

真实系统通常要同时处理多个 client。常见方式：

- **线程 / 多进程**
- **非阻塞 socket + `select` / `selectors`**

事件驱动式的方式更适合高性能服务，也是构建大规模 agent 系统的重要基础。

## 优势

- 可靠
- 广泛支持
- 内建错误恢复、流控、拥塞控制

## 缺点

- 开销比 UDP 更高
- 连接建立与确认机制会增加延迟
- 在超大规模连接下会消耗较多资源

## 在 Agentic / 多模态 AI 系统中的用途

- agent 之间的可靠消息通信
- 传感器或边缘设备数据接入
- HTTP、gRPC 等服务协议的底层承载

## 在协议栈中的位置

- **层级**：传输层（Layer 4）
- **上层**：HTTP、HTTPS、FTP、SMTP、SSH、gRPC 等
- **下层**：IP

## 常见 Socket 问题与排查

- **连接失败**
  - 检查 server 是否启动
  - 检查 host / port 是否正确
  - 检查防火墙

- **端口占用**
  - 可用 `SO_REUSEADDR`

- **数据不完整**
  - 注意 `recv()` 可能一次拿不完全部数据
  - 应明确定义消息边界

- **调试工具**
  - `ping`
  - `netstat` / `ss`
  - Wireshark
  - 程序日志

## 延伸阅读

- [Python `socket` — Official Docs](https://docs.python.org/3/library/socket.html)
- [Python Socket Programming HOWTO](https://docs.python.org/3/howto/sockets.html)
- [Socket Programming in Python (Guide) - Real Python](https://realpython.com/python-sockets/)
- [Beej's Guide to Network Programming](https://beej.us/guide/bgnet/)
- [TCP Explained (Wikipedia)](https://en.wikipedia.org/wiki/Transmission_Control_Protocol)
