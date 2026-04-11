# MCP Completions - 智能自动补全

**学习目标：** 掌握 MCP completions 能力，为参数化 prompts 和 resources 提供智能、上下文感知的自动补全建议，从而提升用户体验。

## 什么是 MCP Completions？

MCP completions 是一种 **utility feature（辅助能力）**，允许 server 向 client 提供智能自动补全建议。你可以把它理解成 IDE 里的自动补全，只不过它补的是 MCP prompt 参数和 resource template 参数。

### 现实类比
想象你在填写一个在线表单：
- 当你开始输入国家时，系统在你输入 `"Un..."` 时提示 `"United States"`
- 当你选中 `"United States"` 后，州字段会自动显示 `"California"`、`"Texas"` 等相关选项
- MCP completions 对 prompt 参数和 resource 参数做的事情，本质上就是这个体验

## 为什么 Completions 很重要？

### 没有 Completions（糟糕体验）
```
User: I want to review some code
System: Please provide the language parameter
User: Uh... what languages do you support?
System: [No help provided]
User: *guesses* "javascript"?
System: Error: Unsupported language. Try: python, rust, typescript, go...
```

### 有了 Completions（优秀体验）
```
User: I want to review some code
System: Please provide the language parameter
User: [starts typing "py"]
System: [suggests: "python", "pytorch"]
User: [selects "python"]
System: ✅ Perfect! Now analyzing Python code...
```

## 核心概念（MCP 2025-06-18）

### 1. Completion Request（`completion/complete`）
client 向 server 发问：“这个参数我应该给用户建议什么值？”

```json
{
  "method": "completion/complete",
  "params": {
    "ref": {
      "type": "ref/prompt",
      "name": "review_code"
    },
    "argument": {
      "name": "language",
      "value": "py"
    }
  }
}
```

### 2. Completion Response
server 返回智能建议：

```json
{
  "result": {
    "completion": {
      "values": [
        {
          "value": "python",
          "description": "Python programming language"
        },
        {
          "value": "pytorch", 
          "description": "PyTorch deep learning framework"
        }
      ],
      "total": 2,
      "hasMore": false
    }
  }
}
```

### 3. 上下文感知的 Completions
补全还可以结合之前已填写的值：

```json
{
  "params": {
    "ref": {
      "type": "ref/prompt", 
      "name": "setup_project"
    },
    "argument": {
      "name": "framework",
      "value": "fast"
    },
    "context": {
      "language": "python"
    }
  }
}
```

**结果：** 因为 `language="python"`，server 会建议 Python 框架，例如 `"fastapi"`、`"flask"`，而不是 JavaScript 框架。

## 学习路径：从简单到高级

### Level 1：静态补全
最基础的补全，不依赖上下文。

**例子：** 编程语言
```python
@mcp.completion()
async def handle_completion(request):
    if request.argument.name == "language":
        return ["python", "javascript", "rust", "go"]
```

### Level 2：过滤补全
根据用户已输入内容做过滤。

**例子：** 过滤出以 `"py"` 开头的语言
```python
@mcp.completion()
async def handle_completion(request):
    if request.argument.name == "language":
        all_languages = ["python", "javascript", "rust", "go"]
        typed = request.argument.value or ""
        return [lang for lang in all_languages if lang.startswith(typed)]
```

### Level 3：上下文感知补全
根据其他参数动态变化。

**例子：** 根据语言建议框架
```python
@mcp.completion()
async def handle_completion(request):
    if request.argument.name == "framework":
        language = request.context.get("language", "")
        if language == "python":
            return ["fastapi", "flask", "django"]
        elif language == "javascript":
            return ["express", "fastify", "koa"]
```

### Level 4：层级式补全
多级补全，前一步结果影响后一步。

**例子：** GitHub owner → repository → branch
```python
@mcp.completion()
async def handle_completion(request):
    if request.argument.name == "owner":
        return ["microsoft", "google", "facebook"]
    elif request.argument.name == "repo":
        owner = request.context.get("owner", "")
        if owner == "microsoft":
            return ["vscode", "typescript", "playwright"]
```

## 实现架构

### Server 组件（`server.py`）

```python
# 1. Declare completions capability
mcp = FastMCP(
    capabilities={"completions": {}}
)

# 2. Define prompts with parameters
@mcp.prompt()
async def review_code(language: str, code: str):
    """Review code with language-specific suggestions"""
    pass

# 3. Define resource templates with parameters  
@mcp.resource("github://repos/{owner}/{repo}")
async def github_repo(owner: str, repo: str):
    """Access GitHub repository"""
    pass

# 4. Implement completion handler
@mcp.completion()
async def handle_completion(request):
    """Provide intelligent completions"""
    # Smart completion logic here
    pass
```

### Client 组件（`client.py`）

```python
# 1. Connect to server
client = Client(StdioServerParameters(command="python", args=["server.py"]))

# 2. Request completions
result = await client.complete(
    ref=PromptReference(type="ref/prompt", name="review_code"),
    argument={"name": "language", "value": "py"}
)

# 3. Display suggestions to user
for completion in result.completion.values:
    print(f"- {completion.value}: {completion.description}")
```

## 教学示例

### 示例 1：编程语言补全
**场景：** 用户想审查代码，开始输入 `"py"`
**Server 返回：** `["python", "pytorch"]`
**学习点：** 基础过滤补全

### 示例 2：带上下文的框架补全
**场景：** 用户已选择 `language="python"`，现在在 framework 中输入 `"fast"`
**Server 返回：** `["fastapi"]`（而不会返回 JavaScript 的 `"fastify"`）
**学习点：** 上下文感知补全

### 示例 3：GitHub 仓库导航
**场景：** 用户在浏览 GitHub resources
- Step 1: owner="model" → `["modelcontextprotocol", "microsoft"]`
- Step 2: repo="mcp"（且 owner="modelcontextprotocol"） → `["specification", "servers"]`
**学习点：** 层级式补全

## 常见模式与最佳实践

### ✅ 推荐做法
```python
# Provide helpful descriptions
{
    "value": "python",
    "description": "Python programming language - great for AI/ML"
}

# Filter based on user input
typed = request.argument.value or ""
return [item for item in items if item.startswith(typed.lower())]

# Use context wisely
language = request.context.get("language", "")
if language == "python":
    return python_frameworks
```

### ❌ 避免这样做
```python
# No descriptions
{"value": "python"}

# No filtering - overwhelming user
return all_10000_programming_languages

# Ignoring context
return ["fastapi", "express", "rails"]  # Mixed languages
```

## 检验理解

### 快速问题
1. completion request 和普通 MCP request 的区别是什么？
2. 上下文感知的 completions 如何改善用户体验？
3. 什么场景适合使用层级式 completions？

### 动手练习
试着修改 server，为下面内容增加补全：
1. 数据库类型：`"postgresql"`、`"mysql"`、`"sqlite"`
2. 做成带上下文的补全：如果 `language="python"`，建议 `"sqlalchemy"`、`"django-orm"`

## 与 DACA 框架的集成

在 DACA（Dapr Agentic Cloud Ascent）框架中，completions 会从这些角度提升 agent 体验：

- **降低认知负担：** agent 不需要“猜”参数值
- **提高准确性：** 上下文感知建议减少错误
- **增强可发现性：** 用户能通过补全学会系统支持什么
- **支持扩展性：** 更好的体验意味着更高信心与更广泛采用

## 下一步

掌握 completions 之后，你就可以继续学习：
- **08：Progress Tracking** - 在长任务中告诉用户系统正在做什么
- **09：Ping/Pong** - 保持连接活跃和健康

## 参考资源

- [MCP 2025-06-18 Completion Specification](https://spec.modelcontextprotocol.io/specification/2025-06-18/server/utilities/completion)
- [FastMCP Completion Documentation](https://github.com/modelcontextprotocol/python-sdk)
- [Real-World MCP Servers with Completions](https://github.com/modelcontextprotocol/servers)

---

**记住：** 优秀的 completions 对用户来说就像魔法一样，在他们正需要时，给出恰到好处的建议。这就是智能自动补全的力量。🎯
