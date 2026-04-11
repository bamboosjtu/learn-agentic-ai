# MCP ClientSession 学习项目

这个仓库包含我们 **Class-05: Model Context Protocol - Defining Resources and MCP Client** 课程中的代码示例和学习材料。

## 📺 课程录像

**YouTube 直播课程：** [Class-05: Model Context Protocol - Defining Resources and MCP Client](https://www.youtube.com/live/k12RclRbzUA?si=PNiBjI7KdHwTEwC-)

## 🎯 学习目标

这个项目展示了如何理解带 resources 的 Model Context Protocol（MCP）Server 和 Client 实现：

1. **MCP Server 实现**：创建带 resources 的 FastMCP Server
2. **Resource 定义**：理解 URI scheme 和资源模式
3. **Resource Templates**：带动态参数的资源 URI 模板
4. **增强版 MCP Client**：实现资源列出、资源读取和模板处理

## 📁 项目结构

```text
mcp_client/
├── client.py            # 增强版 MCP Client 实现
├── server.py            # 带 resources 的 FastMCP Server
├── rough_work.txt       # URI scheme 和资源模式草稿
├── pyproject.toml       # 项目依赖
└── README.md            # 当前文档
```

## 🚀 学习路径

### 1. MCP Server 实现（`server.py`）

**涵盖内容：**

- 创建 FastMCP Server
- 使用 URI scheme 定义 resources
- 使用动态参数定义 resource templates
- 配置无状态 HTTP Server

**关键概念：**

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="FastMCP", stateless_http=True)

@mcp.resource("docs://documents", mime_type="application/json")
def list_docs():
    """List all available documents."""
    return list(docs.keys())

@mcp.resource("docs://documents/{doc_name}", mime_type="application/json")
def read_doc(doc_name: str):
    """Read a specific document."""
    if doc_name in docs:
        return {"name": doc_name, "content": docs[doc_name]}
    else:
        raise mcp.ResourceNotFound(f"Document '{doc_name}' not found.")
```

### 2. 增强版 MCP Client（`client.py`）

**涵盖内容：**

- 列出并读取 resources
- 处理 resource templates
- 处理 JSON 类型资源
- 更完善的错误处理

**关键概念：**

```python
async def list_resouces(self) -> list[types.Resource]:
    assert self._sess, "Session not available."
    result:types.ListResourcesResult = await self._sess.list_resources()
    return result.resources

async def read_resources(self, uri: str) -> types.ReadResourceResult:
    assert self._sess, "Session not available."
    result = await self._sess.read_resource(AnyUrl(uri))
    resource = result.contents[0]
    if isinstance(resource, types.TextResourceContents):
        if resource.mimeType == "application/json":
            try:
                return json.loads(resource.text)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
    return resource.text
```

### 3. URI Schemes 与 Resource Patterns（`rough_work.txt`）

**涵盖内容：**

- 理解 URI scheme，例如 `docs://`、`binary://`、`db://`
- 资源模式设计
- 不同资源类型及其使用场景

**关键 URI Schemes：**

- `docs://documents` - 文档管理
- `binary://logo` - 二进制文件，例如音频、PDF、图片
- `db://pana` - 数据库资源
- `file://path` - 文件系统资源
- `s3://bucket` - 云存储资源

## 🛠️ 环境搭建与安装

### 前置要求

- Python 3.13 或更高版本
- 一个运行在 `http://localhost:8000/mcp` 的 MCP Server

### 安装

1. **克隆仓库：**

   ```bash
   git clone <repository-url>
   cd /learn-agentic-ai/03_ai_protocols/01_mcp/04_fundamental_ 20primitives/05_defining_resources/class_code
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

   ```bash
   # 在一个终端中启动 MCP Server
   uv run uvicorn server:mcp_server --reload
   
   # 在另一个终端中运行增强版 MCP Client
   uv run client.py
   ```

## 📚 依赖

- `mcp>=1.12.1` - Model Context Protocol 库
- `pydantic>=2.11.7` - 数据校验与配置管理
- `requests>=2.32.4` - 用于流式通信的 HTTP 库

## 🎓 学习收获

完成这个项目后，你将理解：

1. **MCP Server 开发**
   - FastMCP Server 的创建与配置
   - Resource 定义和 URI scheme 设计
   - 带动态参数的 resource templates
   - 错误处理与资源校验

2. **Resource 管理**
   - 理解不同 URI scheme，例如 `docs://`、`binary://`、`db://`
   - 列出和读取 resources 的操作方式
   - JSON 资源的处理和校验
   - Resource template 处理与动态 URI 生成

3. **增强版 Client-Server 通信**
   - 完整的 MCP Client-Server 交互
   - Resource 发现与访问模式
   - 正确的错误处理与校验

## 🔗 额外资源

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [MCP Python Client Library](https://github.com/modelcontextprotocol/python-sdk)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)

## 📝 备注

这个项目用于教学，展示了一种从基础 Python 概念逐步走到完整 MCP Client 实现的学习方式。每个文件都建立在前一个概念之上，这样更容易帮助学习者理解完整图景。

---

**课程：** Model Context Protocol - Defining Resources and MCP Client  
**日期：** 2025-07-30  
**YouTube：** [https://www.youtube.com/live/k12RclRbzUA?si=PNiBjI7KdHwTEwC-](https://www.youtube.com/live/k12RclRbzUA?si=PNiBjI7KdHwTEwC-)
