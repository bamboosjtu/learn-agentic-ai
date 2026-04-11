# MCP ClientSession 学习项目

这个仓库包含我们 **Class-04: Model Context Protocol - Implementing Core MCP Client** 课程中的代码示例和学习材料。

## 📺 课程录像

**YouTube 直播课程：** [Class-04: Model Context Protocol - Implementing Core MCP Client](https://www.youtube.com/live/0DYPJyfmR1E?si=mRJQsvn0g2B7nZJA)

## 🎯 学习目标

这个项目展示了一种渐进式学习方式，帮助你理解 Model Context Protocol（MCP）Client 的实现：

1. **Python 基础**：理解 `async/await` 和上下文管理器
2. **简单的 Server-Sent Events**：使用 `requests` 处理基础 HTTP 流式通信
3. **规范的 MCP Client**：完整实现一个 MCP Client

## 📁 项目结构

```text
mcp_client/
├── main.py          # Python 基础 - async 上下文管理器
├── dump.py          # 使用 requests 的简单 SSE 示例
├── client.py        # 正式的 MCP Client 实现
├── pyproject.toml   # 项目依赖
├── data.txt         # 示例数据文件
├── out.txt          # 输出文件
└── README.md        # 当前文档
```

## 🚀 学习路径

### 1. Python 基础（`main.py`）

**涵盖内容：**

- `async/await` 语法
- 上下文管理器（`async with`）
- 使用 `AsyncExitStack` 管理多个异步上下文
- 自定义异步上下文管理器类

**关键概念：**

```python
# 基础异步上下文管理器
async def get_connection(name):
    class Ctx():
        async def __aenter__(self):
            print(f"ENTER... {name}")
            return name
        async def __aexit__(self, exc_type, exc, tb):
            print(f"EXIT! {name}")
    return Ctx()

# 使用 AsyncExitStack 管理多个上下文
async with AsyncExitStack() as stack:
    a = await stack.enter_async_context(await get_connection("A"))
    b = await stack.enter_async_context(await get_connection("B"))
```

### 2. Server-Sent Events（`dump.py`）

**涵盖内容：**

- 使用 `requests` 处理 HTTP 流式通信
- JSON-RPC 2.0 协议
- 处理流式响应
- 基础 MCP 通信

**关键概念：**

```python
# 发起流式 HTTP 请求
response = requests.post(URL, json=PAYLOAD, headers=HEADERS, stream=True)

# 处理流式响应
for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))
```

### 3. 正式的 MCP Client（`client.py`）

**涵盖内容：**

- MCP `ClientSession` 的实现
- 工具列出与调用
- 资源管理
- 正确的异步上下文管理

**关键概念：**

```python
class MCPClient:
    async def __aenter__(self):
        read, write, _ = await self.stack.enter_async_context(
            streamablehttp_client(self.url)
        )
        self._sess = await self.stack.enter_async_context(
            ClientSession(read, write)
        )
        await self._sess.initialize()
        return self
    
    async def list_tools(self) -> types.Tool:
        return (await self._sess.list_tools()).tools
```

## 🛠️ 环境搭建与安装

### 前置要求

- Python 3.13 或更高版本
- 一个运行在 `http://localhost:8000/mcp` 的 MCP Server

### 安装

1. **克隆仓库：**

   ```bash
   git clone <repository-url>
   cd /learn-agentic-ai/03_ai_protocols/01_mcp/04_fundamental_ 20primitives/04_implementing_client/class_code
   ```

2. **安装依赖：**

   ```bash
   uv sync
   ```

   **或者**

   ```bash
   pip install -e .
   ```

3. **运行示例：**

   **Python 基础：**

   ```bash
   python main.py
   ```

   **SSE 示例（先在 `dump.py` 里取消注释）：**

   ```bash
   python dump.py
   ```

   **MCP Client：**

   ```bash
   python client.py
   ```

## 📚 依赖

- `mcp>=1.12.1` - Model Context Protocol 库
- `requests>=2.32.4` - 用于流式通信的 HTTP 库

## 🎓 学习收获

完成这个项目后，你将理解：

1. **Python 异步编程**
   - 上下文管理器与异步上下文管理器
   - 如何管理多个异步资源
   - 正确的清理与资源管理方式

2. **HTTP 流式通信**
   - Server-Sent Events（SSE）
   - JSON-RPC 2.0 协议
   - 流式 HTTP 响应处理

3. **MCP Client 实现**
   - MCP `ClientSession` 的用法
   - 工具发现与调用
   - 正确的 Client 生命周期管理

## 🔗 额外资源

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)

## 📝 备注

这个项目用于教学，展示了一种从基础 Python 概念逐步走到完整 MCP Client 实现的学习路径。每个文件都建立在前一个阶段的概念之上，这样更容易让学习者看到完整图景。

---
  
**课程：** Class-04: Model Context Protocol - Implementing Core MCP Client  
**日期：** 2025-07-24  
**YouTube：** [https://www.youtube.com/live/0DYPJyfmR1E?si=mRJQsvn0g2B7nZJA](https://www.youtube.com/live/0DYPJyfmR1E?si=mRJQsvn0g2B7nZJA)
