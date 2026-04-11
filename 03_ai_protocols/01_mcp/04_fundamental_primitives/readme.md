# 模块 4：MCP 基础原语

> **通过动手编码掌握 Model Context Protocol 的核心构建模块**  
> 基于 [Anthropic 的 Introduction to Model Context Protocol 课程](https://anthropic.skilljar.com/introduction-to-model-context-protocol)

> **建议先阅读** [Introduction MCP Course Lessons](https://docs.google.com/document/d/1W7Ex0rAK2kMtqTHHHEGwTFu2Wrf-zmQJosifppqF-vQ/)

MCP 不只是让桌面应用拥有 agent 能力。它更重要的意义在于：把可复用的工具和资源暴露出来，用来构建 agentic 微服务。可以先看这两个视频：

- [Model Context Protocol (MCP) Explained for Beginners: AI Flight Booking Demo!](https://www.youtube.com/watch?v=E2DEHOEbzks)
- [Why MCP really is a big deal | Model Context Protocol with Tim Berglund](https://www.youtube.com/watch?v=FLpS7OfD5-s)

Model Context Protocol（MCP）本质上是一层面向 Agent 上下文与工具的通信层，这样你就不必为每个项目都写一大堆繁琐的集成代码。你可以把工具定义和执行的负担，从自己的服务端转移到 MCP Server 上。

- 如果 GitHub 已经有 MCP Server，而我的 agent 需要管理一些 GitHub Actions，为什么还要重新写一遍？
- 就像公司今天会提供 API 一样，未来它们很可能也会提供 MCP 实现。
- 它在传输层面是协议无关的，当然也有一些前提与限制，客户端和服务端可以通过不同协议通信。

## 概览

本模块介绍 MCP 的三个基础原语：**Tools**、**Resources** 和 **Prompts**。你将学习如何使用 Python SDK 构建 MCP Server 和 Client，并通过面向实践、以代码为中心的示例来理解它们在真实场景中的用法。

## 📚 学习目标

完成本模块后，你将能够：

### 核心能力

- ✅ 使用 Python SDK 构建 **MCP Server**，并通过装饰器定义工具
- ✅ 实现 MCP 的三类基础原语：Tools（模型控制）、Resources（应用控制）、Prompts（用户控制）
- ✅ 创建可连接并与 MCP Server 交互的 **MCP Client**
- ✅ 使用 **MCP Server Inspector** 对服务端功能进行测试与调试

### 技术技能

- ✅ 使用装饰器定义工具，而不必手写 JSON Schema
- ✅ 实现文件管理相关功能，例如读取、写入和管理文件
- ✅ 创建用于暴露只读数据的资源，并正确处理 MIME type
- ✅ 构建适用于常见工作流的预制 Prompt
- ✅ 通过合适的异常处理与用户反馈，实现优雅的错误处理

### 理解层面

- ✅ 区分 MCP 的三类基础原语：知道何时使用 tools、resources 或 prompts
- ✅ 理解控制模型：模型控制（tools）、应用控制（resources）、用户控制（prompts）
- ✅ 应用安全、性能和可维护性方面的最佳实践

## 前置要求

- 具备 Python 编程的基本能力
- 对 JSON 和 HTTP 请求-响应模式有基础理解
- 熟悉 Python 中的装饰器与类型注解

## 学习结构

### 1. 项目初始化与第一个 Server

**目标**：搭建开发环境，并创建你的第一个可运行 MCP Server

- [01_hello_mcp_server](./01_hello_mcp_server/read.md) - 使用 `uv` 和 base_project 搭建开发环境
- [02_project_setup](./02_project_setup/readme.md) - 为本学习模块设置基础项目

### 2. 构建 Tools 与 Resources

**目标**：通过实践示例掌握 MCP 的三种基础原语

- [03_defining_tools](./03_defining_tools/readme.md) - 使用装饰器和类型注解创建工具
- [04_implementing_client](./04_implementing_client/readme.md) - 为 MCP tools 创建一个简单客户端
- [05_defining_resources.md](05_defining_resources/readme.md) - 创建只读数据资源
- [06. Working with Prompts](06_working_with_prompts/readme.md) - 为常见工作流构建预制 Prompt

## MCP 核心原语

### 1. Tools（模型控制）

Tools 是 AI 模型可以调用来执行动作的函数。它们具有以下特点：

- **模型控制**：AI 决定何时以及如何使用它们
- **面向动作**：执行具体任务，例如读取文件、调用 API
- **基于装饰器**：通过 Python 装饰器和类型注解定义

### 2. Resources（应用控制）

Resources 提供对数据的只读访问。它们具有以下特点：

- **应用控制**：由应用决定何时暴露这些资源
- **面向数据**：用于访问文档、数据库、API 等内容
- **基于 URI**：通过特定 URI 访问，并可附带可选参数

### 3. Prompts（用户控制）

Prompts 是为常见工作流预先设计好的指令模板。它们具有以下特点：

- **用户控制**：由用户决定何时应用这些 Prompt
- **面向指令**：提供高质量、可复用的提示模板
- **上下文感知**：可包含动态内容与格式化信息

## 快速开始

1. **环境搭建**：按照 [project setup guide](01_project_setup.md) 操作
2. **创建第一个 Server**：实现一个带 tools 的简单 MCP Server
3. **用 Inspector 测试**：使用内置 Server Inspector 调试
4. **添加 Resources**：实现只读数据访问
5. **构建 Client**：创建可连接你 Server 的 MCP Client
6. **创建 Prompts**：构建可复用的 Prompt 模板

### 知识检查

- [ ] 能解释 tools、resources 和 prompts 的区别
- [ ] 理解每种 MCP 原语适合何时使用
- [ ] 能在 MCP Server 中实现合理的错误处理
- [ ] 知道如何有效使用 MCP Server Inspector
- [ ] 能创建静态资源和模板化资源
- [ ] 理解不同内容类型对应的 MIME type 处理方式

## 🛠️ 开发工具

### 必备工具

- **`uv`**：快速 Python 包管理器，用于依赖管理
- **MCP Python SDK**：构建 MCP Server 与 Client 的核心库
- **MCP Server Inspector**：用于测试和调试 Server 的 Web 工具
- **Postman**：用于测试 API

### 推荐工具

- **Cursor 或 VS Code**：带有 Python 和 MCP 扩展的 IDE
- **Git**：用于版本管理

## 🔗 资源与参考

### 官方文档

- [MCP Specification (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)

### 学习资源

- [Anthropic's MCP Course](https://anthropic.skilljar.com/introduction-to-model-context-protocol)
- [MCP Server Inspector](https://github.com/modelcontextprotocol/server-inspector)
- [JSON Schema Documentation](https://json-schema.org/learn/getting-started-step-by-step)

### 社区与支持

- [MCP GitHub Discussions](https://github.com/modelcontextprotocol/python-sdk/discussions)
- [MCP Discord Community](https://discord.gg/modelcontextprotocol)

## 🚀 下一步

完成本模块后，你将准备好继续探索：

### 模块 2：核心能力与传输通信

- Sampling 与 AI 委托
- Logging 与进度通知
- Roots 与上下文发现
- JSON-RPC 消息类型与传输协议

### 高级模块（后续）

- **Server Engineering**：高级服务端模式与优化
- **Client Features**：高级客户端能力与集成
- **OAuth Integration**：安全与认证模式
- **OpenAI Agents SDK**：与 OpenAI 智能体框架集成

## 💡 学习建议

1. **边看边写**：不要只阅读，把每个示例都亲手实现一遍
2. **多做实验**：修改示例，探索不同场景下的行为
3. **善用 Inspector**：用 MCP Server Inspector 充分测试你的 Server
4. **循序渐进**：先从简单场景开始，再逐步增加复杂度
5. **记录心得**：把发现的模式和最佳实践记下来
