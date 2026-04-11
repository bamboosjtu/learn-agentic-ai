# 07：MCP Resources 的当前状态与未来方向

**MCP Resources** 是一个很强大的能力，它允许 MCP server 暴露可被客户端读取的数据和内容，并将其作为 LLM 交互时的上下文使用。不过，这项能力在 OpenAI Agents SDK 中目前仍然处于**进行中**的状态。

---

## 当前状态：Resources 支持仍然有限

### **现在已经有的部分**
- **MCP Resources 规范** 已经存在，而且定义比较完整
- **单个 MCP server** 可以自行实现 resources
- 通过自定义代码，已经可以**手动处理 resources**

### **目前缺少的部分**
- OpenAI Agents SDK 中的**原生集成**
- agent 工作流中的**自动资源处理**
- 从工具输出中**自动解析 resource link**

---

## [GitHub PR: #1042](https://github.com/openai/openai-agents-python/pull/1042)

根据 [GitHub PR #1042](https://github.com/openai/openai-agents-python/pull/1042)，SDK 正在推进对 MCP Resources 的支持：

### **这个 PR 增加了什么**
- 在基础 `MCPServer` 类上新增了三个抽象方法：
  - `list_resources()`
  - `list_resource_templates()`
  - `read_resource()`
- 在 `_MCPServerWithClientSession` 中完成实现（它是所有传输类的父类）
- 提供了一个带可运行演示的 MCP resources server 示例
- 更新了文档，并附带用法示例

### **这个 PR 没包含什么**
- `subscribe_resource` 和 `unsubscribe_resource` 方法
- **自动集成**到 agent 工作流
- 从工具输出中做 **resource link parsing**

---

## PR 中的关键讨论点

### **核心问题：“这东西现在真的能做什么吗？”**

正如 [@artificial-aidan](https://github.com/openai/openai-agents-python/pull/1042#issuecomment-1984561234) 所说：
> “它现在真的能和 agent flow 集成起来做什么吗？还是说实现者仍然得自己去取 resources？看起来不太实用。工具调用可以返回资源链接，感觉更有价值的做法应该是解析工具输出，并把 resource link 对应的资源传给 LLM。”

### **OpenAI 的回应**

[@seratch](https://github.com/openai/openai-agents-python/pull/1042#issuecomment-1984561234) 的说明是：
> “目前，这个 SDK 的 agent 机制还没有计划直接使用 resources。这里提出的 resource support，只是为了在同一套代码库中增加调用 resource 的方法，但这并不意味着你的 agents 在没有你额外写代码的情况下就能直接利用它们。”

---

## 这对你意味着什么

### **现在（当前状态）**
- 你可以**手动**使用 MCP resources
- 你需要**自己写自定义代码**来处理 resource links
- resources **不会自动**进入 agent 工作流

### **未来（如果 PR #1042 被合并）**
- 你将拥有一组**辅助方法**来操作 resources
- 你仍然需要**自定义逻辑**把 resources 接入 agent flow
- SDK 会提供**基础设施**，但不会提供**自动集成**

---

## 学习收获

1. **MCP Resources** 是一种很强的数据暴露机制
2. 目前 OpenAI Agents SDK 对它的支持仍然**有限**
3. 随着开发推进，未来会有更多**可能性**
4. 现阶段依然需要**手动实现**资源集成
