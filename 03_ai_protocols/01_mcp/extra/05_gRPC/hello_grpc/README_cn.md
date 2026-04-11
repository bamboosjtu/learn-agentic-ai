## 在 Python 中使用 gRPC：`grpcio`

- [`grpcio`](https://grpc.io/docs/languages/python/) 是官方 Python gRPC 库。
- [`grpcio-tools`](https://pypi.org/project/grpcio-tools/) 用于从 `.proto` 文件生成 Python 代码。

### 安装

```bash
uv init hello_grpc
cd hello_grpc
uv add grpcio grpcio-tools
```

### 示例：基础 gRPC Server 与 Client

#### 1. 定义协议文件 `helloworld.proto`

原始示例定义了一个最小化的 `Greeter` 服务：

- `SayHello(HelloRequest) -> HelloReply`
- `HelloRequest` 里包含 `name`
- `HelloReply` 里包含 `message`

#### 2. 生成 Python 代码

```bash
uv run python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. helloworld.proto
```

#### 3. 服务端 `server.py`

服务端主要做这些事：

- 继承 `GreeterServicer`
- 实现 `SayHello`
- 返回 `Hello, {name}!`
- 监听 `50051` 端口

#### 4. 客户端 `client.py`

客户端主要做这些事：

- 连接 `localhost:50051`
- 创建 `GreeterStub`
- 调用 `SayHello`
- 打印服务端返回的问候语

---

## 运行方式

```bash
uv run python server.py
uv run python client.py
```

如果运行正常，客户端会输出类似：

```text
Greeter client received: Hello, Agentic AI!
```
