# JSON-RPC：轻量级远程过程调用协议

> JSON-RPC 是一种无状态、轻量、与传输无关的 RPC 协议，使用 JSON 作为数据格式。

JSON-RPC 的核心价值在于：它把“远程调用”组织成结构化的消息格式，非常适合服务间调用、工具调用、agent 间命令传递与结果回报。

---

## 为什么 agent 系统喜欢 JSON-RPC

- **结构清晰**：`method / params / id / result / error`
- **易于调试**：JSON 可读性高
- **跨语言容易**：任何语言都能处理 JSON
- **支持通知**：无需响应的 fire-and-forget 消息
- **支持 batch**：减少网络往返

---

## 核心对象

### Request

用于调用远程方法，典型字段：

- `jsonrpc: "2.0"`
- `method`
- `params`
- `id`

### Notification

本质上是**没有 `id` 的 request**，表示不需要响应。

### Response

成功时包含：

- `jsonrpc`
- `result`
- `id`

失败时包含：

- `jsonrpc`
- `error`
- `id`

### Error Object

标准错误码包括：

- `-32700` Parse error
- `-32600` Invalid Request
- `-32601` Method not found
- `-32602` Invalid params
- `-32603` Internal error

---

## JSON-RPC 2.0 的关键特性

1. **显式版本号**
   必须带 `jsonrpc: "2.0"`

2. **支持位置参数和命名参数**
   `params` 可以是数组或对象

3. **通知不返回响应**

4. **支持 batch**
   可将多个 request / notification 放进一个数组中发送

5. **响应顺序不一定等于请求顺序**

---

## 优势

- 简单直接
- 轻量
- 传输无关，可跑在 HTTP、WebSocket、TCP、stdio 等之上
- 很适合定义 agent capability 调用协议

## 局限

- JSON 本身缺少强类型约束
- 协议本身不带认证授权
- 无内建服务发现机制
- 状态与会话要额外设计

---

## 在 DACA / A2A 里的意义

JSON-RPC 很适合作为 agent 之间的**消息格式层**：

- 一个 agent 调另一个 agent 的能力
- 标准化地返回结果或错误
- 搭配 HTTP / SSE / WebSocket / stdio 使用
- 很适合 MCP 这种“方法调用 + 工具参数 + 结果返回”的场景

它的定位不是取代传输协议，而是成为传输协议之上的**统一消息结构**。

---

## 延伸阅读

- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
- [Language Server Protocol](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/)
