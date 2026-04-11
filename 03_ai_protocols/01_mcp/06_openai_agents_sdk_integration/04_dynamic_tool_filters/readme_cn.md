# 04：使用 `MCPServerStreamableHttp` 做[动态工具过滤](https://openai.github.io/openai-agents-python/mcp/#dynamic-tool-filtering)

## 这一节在学什么？（Why）

这一节你会学到：如何**动态控制你的 agent 能看到和使用哪些工具**。不是只靠一个固定列表，而是通过自定义逻辑，根据 agent、本次连接的服务器，甚至当前运行时场景来决定。

- **为什么重要？**
  - 有时候，你希望根据用户身份、agent 当前任务，或者其他运行时条件，来显示或隐藏某些工具。
  - 动态过滤可以让你对 agent 的工具箱做更细粒度、具备上下文感知能力的控制。
  - 这是继静态过滤之后的“下一步”，也是构建智能、自适应、安全 agent 系统的关键能力。

---

## 核心思路是什么？

- **动态工具过滤** 指的是：你编写一个函数，对每个工具逐一判断它是否应该可用，这个判断会结合 agent、server 和当前上下文信息。
- 这个 filter 可以是同步函数，也可以是异步函数，内部逻辑完全由你决定。

---

## 它是怎么工作的？（How）

1. **编写一个过滤函数**，它接收 `ToolFilterContext` 和某个 tool，并返回 `True`（显示该工具）或 `False`（隐藏该工具）。
2. **在创建 MCP server client 时**，把这个函数作为 `tool_filter` 传进去。
3. **SDK 会在每次需要确定工具可用性时**，对每个工具调用一次你的函数。

---

## 分步示例

### 1. 导入上下文类型
```python
from agents.mcp import ToolFilterContext
```

### 2. 编写过滤函数
```python
def custom_filter(context: ToolFilterContext, tool) -> bool:
    # Only allow tools that start with "mood"
    return tool.name.startswith("mood")
```

或者，做成带上下文判断的逻辑：
```python
def context_aware_filter(context: ToolFilterContext, tool) -> bool:
    # Only allow tools for a specific agent
    return context.agent.name == "MyMCPConnectedAssistant" and tool.name == "mood_from_shared_server"
```

或者，使用异步逻辑：
```python
async def async_filter(context: ToolFilterContext, tool) -> bool:
    # Example: check a database or external API before allowing the tool
    return await some_async_check(context, tool)
```

### 3. 创建 MCP server client 时使用这个 filter
```python
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams

mcp_params = MCPServerStreamableHttpParams(url="http://localhost:8001/mcp/")
async with MCPServerStreamableHttp(params=mcp_params, tool_filter=custom_filter, name="MyDynamicMCPServer") as mcp_server_client:
    # ... set up your agent and run as before ...
```

---

## 你应该注意什么？

- 当前可用的工具可以随着 agent、server 或你写入 filter 的任何逻辑而变化。
- 这比静态过滤灵活得多，也让你能够构建更聪明、更安全的 agent。

---

## 为什么这是一个好的学习步骤？

- **自适应**：agent 的工具箱可以根据情况动态变化。
- **能力强**：你可以写任何逻辑，包括异步检查、外部数据校验等。
- **贴近真实场景**：大多数生产系统都需要这种灵活性。

---

**总结一下：**
你学到的是，如何给 agent 一个“智能菜单”式的工具集合，让它随着上下文变化。这是构建高级、真实世界 agent 系统的关键能力。
