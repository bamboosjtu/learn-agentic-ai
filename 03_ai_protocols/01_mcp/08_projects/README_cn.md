# 08：MCP 项目实战

**目标：** 把前面章节学到的知识真正应用起来，构建能够解决复杂现实问题的 MCP 项目。

这一部分相当于一个“毕业项目”模块，我们会把 MCP 的多个能力整合进完整应用中，包括 tools、resources、prompts 和 security。这里的项目会更加开放，不再只是演示单个概念，而是更关注架构设计与创造性问题解决。

## 项目想法

这个目录会承载一个或多个较大的项目。潜在方向包括：

### 1. **符合 DACA 的代码库助手**
- **概念：** 一个具备 agent 能力的助手，可以读取、分析并回答关于本地代码库的问题。
- **用到的 MCP 特性：**
  - **Server：** 暴露用于文件系统访问的工具（`read_file`、`list_directory`）、代码解析（AST）和分析能力。
  - **Client：** 使用 `roots` 识别项目目录；实现 `sampling`，让 server 的工具可以借助 client 侧 LLM 来做代码总结和分析。
  - **Auth：** 服务器通过 OAuth 保护，确保只有授权客户端才能访问代码库。

### 2. **交互式数据库查询 Agent**
- **概念：** 一个提供 SQL 查询工具的 MCP server，但在执行高风险操作前会通过 elicitation 请求用户确认。
- **用到的 MCP 特性：**
  - **Server：** 暴露 `query(sql: str)` 工具；解析 SQL 后，如果发现 `DROP`、`DELETE` 或 `UPDATE`，就通过 `elicitation` 向用户请求确认。
  - **Client：** 实现 elicitation 请求处理器，把确认对话框展示给用户。
  - **Resources：** 以只读 resource 的方式暴露数据库 schema（`resources/read`）。

### 3. **基于 A2A 协议的多 Agent 系统**
- **概念：** 一个更进阶的项目，展示多个彼此独立的 MCP server 如何通过 Agent-to-Agent（A2A）协议协作，其中一个 server 同时充当另一个 server 的 client。
- **用到的 MCP 特性：**
  - **Server A（协调器 / Orchestrator）：** 暴露一个高层工具，例如 `plan_trip(destination: str)`。
  - **Server B（航班预订）：** 暴露查找航班的工具。
  - **Server C（酒店预订）：** 暴露查找酒店的工具。
  - **工作流：** 当协调器 server 的 `plan_trip` 工具被调用时，它会作为 MCP *client* 去发现并调用航班和酒店预订 servers 上的工具。

## 实施计划

对于每个项目，我们都会创建一个独立子目录，其中包含：
- 一个详细的 `README.md`，说明项目架构与搭建方式
- 所需的 server 与 client 代码
- 用于依赖管理的 `pyproject.toml` 和 `uv.lock`
- 适用时配套的 Postman Collection，用于测试
