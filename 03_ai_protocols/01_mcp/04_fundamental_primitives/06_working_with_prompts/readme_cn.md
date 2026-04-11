# 07. 使用 Prompts

> **为常见工作流和 AI 交互构建并使用预制 Prompt**

## 理解 MCP Prompts

MCP 中的 Prompts 是为常见工作流预先设计好的指令模板。它们是 **用户控制的**，也就是说，用户决定何时应用这些 Prompt。与 tools 和 resources 不同，prompts 的职责是为 AI 交互提供引导和结构。

## 为什么要使用 Prompts？

关键点在这里：用户其实本来就可以直接让 Claude 完成大多数任务。比如，用户可以输入：

`reformat the report.pdf in markdown`

模型通常也能给出还不错的结果。但如果你提供的是一个经过充分测试、面向特定任务、考虑过边界情况并遵循最佳实践的 Prompt，结果通常会好得多。

作为 MCP Server 的作者，你可以花时间去设计、测试和评估那些在不同场景下都能稳定工作的 Prompt。用户则能直接受益于这些经验，而不需要自己成为 prompt engineering 专家。

### Prompts 的关键特征

- **用户控制**：用户决定何时应用 prompts
- **面向指令**：提供高质量、可复用的指令
- **上下文感知**：可包含动态内容和格式化信息
- **可复用**：可以在不同场景下使用
- **结构化**：遵循一致模式以提高效果

## Prompts 是如何工作的？

Prompts 定义了一组可供 Client 使用的 user / assistant 消息。它们应当是高质量、经过验证，并且与 MCP Server 目标相关的内容。整体工作流如下：

- 编写并评估一个与你 Server 功能相关的 Prompt
- 使用 `@mcp.prompt` 装饰器在 MCP Server 中定义这个 Prompt
- Client 可以在任何时候请求这个 Prompt
- Client 提供的参数会作为关键字参数传入你的 Prompt 函数
- 函数返回已经格式化好的消息，供 AI 模型直接使用

这个机制让你可以构建可复用、参数化的 Prompt，同时保持一致性，又允许通过变量进行定制。对于复杂工作流来说，这尤其有用，因为你希望每次都能确保 AI 拿到结构良好的指令。

### **MCP Prompts 核心概念**

- **Prompt Discovery**：通过 `prompts/list` 发现可用模板
- **Prompt Generation**：通过 `prompts/get` 生成定制 Prompt
- **Parameter Handling**：基于类型校验的动态参数化 Prompt
- **2025-06-18 新特性**：`title` 字段、增强元数据和 capabilities 声明

*进一步阅读：* [MCP Prompts Documentation](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)

## 协议消息

### 列出 Prompts

要获取可用 Prompt 列表，Client 会发送 `prompts/list` 请求。该操作支持 [pagination](/specification/2025-06-18/server/utilities/pagination)。

**请求：**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "prompts/list",
  "params": {
    "cursor": "optional-cursor-value"
  }
}
```

**响应：**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "prompts": [
      {
        "name": "code_review",
        "title": "Request Code Review",
        "description": "Asks the LLM to analyze code quality and suggest improvements",
        "arguments": [
          {
            "name": "code",
            "description": "The code to review",
            "required": true
          }
        ]
      }
    ],
    "nextCursor": "next-page-cursor"
  }
}
```

### 获取一个 Prompt

要获取某个具体 Prompt，Client 会发送 `prompts/get` 请求。参数还可以通过 [completion API](/specification/2025-06-18/server/utilities/completion) 自动补全。

**请求：**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "prompts/get",
  "params": {
    "name": "code_review",
    "arguments": {
      "code": "def hello():\n    print('world')"
    }
  }
}
```

**响应：**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "description": "Code review prompt",
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Please review this Python code:\ndef hello():\n    print('world')"
        }
      }
    ]
  }
}
```

## ToDo 练习：给 MCP Server 添加 Prompts

### 添加一个格式化 Prompt

定义一个 Prompt，把文档改写成 Markdown。例如：

```python
from mcp.server.fastmcp.prompts import base

@mcp.prompt(
    name="format",
    description="Rewrites the contents of the document in Markdown format.",
)
def format_document(
    doc_id: str = Field(description="Id of the document to format"),
) -> list[base.Message]:
    prompt = f"""
    Your goal is to reformat a document to be written with markdown syntax.

    The id of the document you need to reformat is:
    <document_id>
    {doc_id}
    </document_id>

    Add in headers, bullet points, tables, etc as necessary. Feel free to add in extra text, but don't change the meaning of the report.
    Use the 'edit_document' tool to edit the document. After the document has been edited, respond with the final version of the doc. Don't explain your changes.
    """

    return [base.UserMessage(prompt)]
```

再添加一个用于总结文档的 Prompt：

```python
@mcp.prompt(
    name="summarize",
    description="Summarizes the contents of the document."
)
def summarize_document(doc_id: str = Field(description="Id of the document to summarize")) -> list:
    from mcp.types import PromptMessage, TextContent
    prompt_text = f"""
    Your goal is to summarize the contents of the document.
    Document ID: {doc_id}
    Include a concise summary of the document's main points.
    """
    return [PromptMessage(role="user", content=TextContent(type="text", text=prompt_text))]
```

---

## 在 MCP Client 中实现 Prompt 使用

在你的 MCP Client 中，实现以下方法以支持 prompts：

```python
async def list_prompts(self) -> types.ListPromptsResult:
    result = await self.session().list_prompts()
    return result.prompts

async def get_prompt(self, prompt_name, args: dict[str, str]):
    result = await self.session().get_prompt(prompt_name, args)
    return result.messages
```

这些方法让 Client 能够：

- 通过 `prompts/list` 获取可用 Prompt 列表
- 通过 `prompts/get` 获取一个插值后的具体 Prompt

---

## 测试 Prompts

要测试你的 Prompt 实现，可以这样做：

- 使用 MCP Inspector 查看 Prompt 模板，并验证变量插值结果
- 在 CLI 中输入 `/`，查看可用 prompt 命令。例如输入 `/format plan.md`，就会获取针对 `plan.md` 的格式化 Prompt
- 验证返回的 messages 是否包含结构化的 Markdown 指令

这些补充让 prompts 真正完成了端到端接入：在 Server 中定义、在 Client 中使用、并通过测试加以验证。

## 下一步

既然你已经理解了 prompts，接下来可以进一步尝试：

1. **创建专用 Prompt**：针对你的特定领域或场景设计 Prompt
2. **构建 Prompt 链**：把多个 Prompt 组合起来处理复杂工作流
3. **增加 Prompt 校验**：确保 Prompt 参数合法
4. **实现 Prompt 缓存**：提升性能

下一课中，我们会继续探索如何构建完整的 MCP 应用，把 tools、resources 和 prompts 组合起来使用。

## 练习

1. **创建领域专用 Prompt**：为你的行业或业务场景设计 Prompt
2. **添加 Prompt 模板**：创建带变量的可复用模板
3. **实现 Prompt 参数校验**：为 prompts 增加参数验证
4. **构建 Prompt 工作流**：为复杂任务设计 Prompt 链

## 资源

- [MCP Prompt Specification](https://modelcontextprotocol.io/specification/2025-06-18#prompts)
- [Prompt Engineering Best Practices](https://www.anthropic.com/index/prompting-guide)
- [JSON Schema Validation](https://json-schema.org/learn/getting-started-step-by-step)
