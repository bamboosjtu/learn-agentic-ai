# gRPC

gRPC 是 Google 推出的高性能开源 RPC 框架，底层通常基于 HTTP/2，序列化通常使用 Protocol Buffers。它适合微服务、内部服务调用和高吞吐、低延迟的分布式系统。

> [!IMPORTANT]
> 该章节仍在完善中。

---

## 概念总览

### 关键特性

- **基于 HTTP/2**：支持多路复用、头部压缩、二进制分帧
- **基于 Protocol Buffers**：序列化高效、结构清晰、类型强
- **支持流式通信**：支持客户端流、服务端流、双向流
- **自动代码生成**：从 `.proto` 生成 Python / Go / Java 等客户端与服务端代码

### 优势

- 低延迟、高吞吐
- 接口契约明确，类型安全更强
- 支持实时流式数据处理
- 跨语言互操作性好

### 局限

- 比 REST/JSON 上手更复杂
- 需要理解 `.proto`、stub、service 等概念

---

## 在 Python 中使用 gRPC（配合 `uv`）

### 1. 初始化项目

```bash
uv init grpc-tutorial
cd grpc-tutorial
uv add grpcio grpcio-tools
```

### 2. 定义 `.proto`

原文示例定义了一个 `UserService`，包含：

- `User`
- `GetUserRequest`
- `GetUserResponse`
- `GetUser` RPC 方法

后续还扩展了：

- `ListUsersRequest`
- `ListUsersResponse`
- `ListUsers` RPC 方法

### 3. 生成 Python 代码

```bash
uv run python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/user.proto
```

生成结果通常包括：

- `user_pb2.py`
- `user_pb2_grpc.py`

### 4. 实现服务端

服务端会：

- 继承 `UserServiceServicer`
- 实现 `GetUser`
- 可继续实现 `ListUsers`
- 监听 `localhost:50051`

### 5. 实现客户端

客户端会：

- 建立 `grpc.insecure_channel('localhost:50051')`
- 创建 `UserServiceStub`
- 发送 `GetUser` 或 `ListUsers` 请求
- 处理成功响应或 `RpcError`

---

## gRPC 在 Agentic AI / DACA 中的用途

- **高性能服务间通信**：适合 agent 与 agent、agent 与工具服务之间的内部调用
- **强类型接口约束**：适合大型团队协作和复杂能力编排
- **流式数据通道**：适合日志、推理结果、传感器流、状态更新
- **Dapr 生态兼容**：Dapr 同时支持 HTTP 和 gRPC，可作为内部通信选项

---

## 协议栈位置

- **层级**：应用层（Layer 7）
- **上层**：业务逻辑、agent framework
- **下层**：HTTP/2、TCP

---

## 进一步阅读

- [gRPC Python Docs](https://grpc.io/docs/languages/python/)
- [Protocol Buffers Docs](https://developers.google.com/protocol-buffers)
- [`grpcio-tools`](https://pypi.org/project/grpcio-tools/)
