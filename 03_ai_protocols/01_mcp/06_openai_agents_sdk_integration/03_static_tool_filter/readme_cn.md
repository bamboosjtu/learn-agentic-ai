# 03：使用 `MCPServerStreamableHttp` 做静态工具过滤

## 这一节在学什么？（Why）

这一节你要学的是：**如何控制你的 agent 能看到和使用 MCP 服务器上的哪些工具**。这是构建安全、聚焦、且用户友好的 agent 系统的基础能力。

- **为什么重要？**
  - 有时候，一个 MCP 服务器会提供很多工具，但你只希望 agent 在某个特定任务或特定用户场景里使用其中少数几个。
  - 过滤工具有助于避免误用、减少混乱，并让 agent 的能力边界更清晰、更安全。
  - 这也是迈向更高级 agent 控制方式的“第一步” 先从简单的 allow/block list 开始，再逐步过渡到动态、上下文感知的过滤。

## 核心思路是什么？

- **静态工具过滤** 指的是：你在代码里预先决定哪些工具允许使用、哪些工具禁止使用。
- 你通过给 MCP server client 传入一个 filter 来实现这一点。
- 这个 filter 就像是 agent 的“菜单”：只有你批准的项目才会显示出来。

## 它是怎么工作的？（How）

1. **导入一个辅助函数** 来创建 filter。
2. **告诉 MCP server client** 哪些工具允许、哪些工具禁止。
3. **当 agent 建立连接时**，它只能看到你选定的那些工具。

## 分步示例

```python
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams, create_static_tool_filter

# Only allow the "mood_from_shared_server" tool
tool_filter = create_static_tool_filter(allowed_tool_names=["mood_from_shared_server"])
mcp_params = MCPServerStreamableHttpParams(url="http://localhost:8001/mcp/")

async with MCPServerStreamableHttp(params=mcp_params, tool_filter=tool_filter, name="MyFilteredMCPServer") as mcp_server_client:
    # ... set up your agent and run as before ...
```

- 这样一来，无论你是列出工具，还是运行 agent，它都只能看到并使用 `mood_from_shared_server`。

## 你应该注意什么？

- 如果你尝试使用一个未被允许的工具，agent 根本看不到它。
- 这是一种简单而可靠的方式，可以先把 agent 的工具箱“做安全处理”。

## 为什么这是一个好的学习步骤？

- **安全**：你可以放心实验，因为 agent 无法使用你没批准的工具。
- **清晰**：你能非常明确地看到当前可用工具，调试和学习都会更简单。
- **基础扎实**：这为下一步更高级的过滤方式（例如动态、上下文感知过滤）打下基础。

---

**总结一下：**
你学到的是，如何为 agent 精心挑选一组工具，就像给小孩准备安全的玩具一样。这是构建安全、可扩展、可维护的 agent 系统的重要基础。

---
