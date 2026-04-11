# 你将学到什么：OpenAI Agents SDK 与 MCP 集成

这一部分搭起了一座桥梁，把 MCP 这种开放、可互操作的协议世界，和一个流行的、生产级的 agent 框架连接起来。它展示的不是 MCP 与 agent 框架之间的竞争关系，而是 MCP 作为一种强大的**补充机制**，如何让 agent 框架变得更模块化、更易测试，也更易扩展。

## **全局视角**

你正在探索如何通过 Model Context Protocol（MCP）把 OpenAI Agents（借助 OpenAI Agents SDK）连接到外部上下文，尤其是通过无状态、可扩展的 `streamable-http` 传输方式。这使 agent 能够动态发现并调用工具和 prompts，从而让你的 agent 系统更模块化、更具互操作性，也更适合生产环境，并与 DACA 设计模式保持一致。

## 为什么这种架构很强大（符合 DACA）

- **解耦（Decoupling）：** agent 的核心逻辑（OpenAI Assistant）与工具实现（MCP Server）彻底分离。
- **互操作性（Interoperability）：** 在本课程里构建并测试过的同一个 MCP server，可以被 OpenAI agent、LangChain agent，或任何其他框架使用，而无需修改一行 server 代码。
- **可扩展与可维护（Scalability & Maintainability）：** 你可以独立开发、测试、扩展工具（MCP server），而不影响 agent。本身也支持不同团队分别维护不同工具服务器。
- **开放核心（Open Core）：** 这与 DACA 的原则一致，即在边缘层用 MCP 这样的开放标准去连接托管服务或闭源框架（例如 OpenAI API）。

---

### **模块拆解**

#### **01_agent_mcp_http**
- **目标：** 通过 `streamable-http` 传输把一个 OpenAI agent 连接到单个 MCP server。
- **你会掌握：**
  - 配置 agent，使其把 MCP server 作为工具来源
  - 理解最基础的 agent 到 MCP 交互循环

#### **02_caching_tool_lists**
- **目标：** 通过缓存 MCP server 的工具列表来优化性能。
- **你会掌握：**
  - 启用 / 禁用工具列表缓存
  - 理解工具最新状态与访问延迟之间的权衡

#### **03_static_tool_filter**
- **目标：** 使用静态 allow/block list 过滤可用工具。
- **你会掌握：**
  - 限制哪些工具对 agent 可见
  - 使用静态配置实现工具访问控制

#### **04_dynamic_tool_filters**
- **目标：** 基于 agent 上下文或运行时条件动态过滤工具。
- **你会掌握：**
  - 实现可调用的工具过滤函数
  - 让工具可用性具备上下文感知能力（例如基于用户、session、环境）

#### **05_prompt_server**
- **目标：** 通过专用的 MCP server 提供 prompts 和工具定义。
- **你会掌握：**
  - 将 prompt / tool 逻辑从 agent 逻辑中分离
  - 使用 MCP 为 agent 提供动态或静态 prompts

#### **06_agent_with_multiple_mcp_servers**
- **目标：** 让一个 agent 同时连接多个 MCP server。
- **你会掌握：**
  - 聚合多个来源的工具
  - 让 agent 能跨多个分布式工具服务器进行编排

#### **shared_mcp_server**
- **目标：** 提供一个可复用的共享 MCP server 实现。
- **你会掌握：**
  - 理解 MCP 的 server 端实现
  - 复用并扩展通用 MCP server，以支持不同工具集

---

### **关键学习收获**
- **解耦：** agent 逻辑与工具实现彼此分离。
- **互操作性：** 任何 agent 框架（OpenAI、LangChain 等）都可以使用同一个 MCP server。
- **可扩展性：** 工具服务器与 agent 可以独立开发、部署和扩容。
- **可扩展能力：** 你可以轻松添加、移除或更新工具，而不需要改动 agent 代码。
- **DACA 一致性：** 遵循 DACA 的开放核心、边缘托管、模块化和云原生设计思想。

---

**总结一下：**

你正在掌握一种构建 agent 系统的方法：让 agent 可以灵活地从一个或多个 MCP server 中发现并使用工具，并结合高级过滤和缓存能力，以一种可扩展、可维护、适合真实生产环境的方式运作。

完成本模块后，你会对如何通过 Model Context Protocol 为 OpenAI Agents 扩展强大的工具与资源能力形成实际理解。
