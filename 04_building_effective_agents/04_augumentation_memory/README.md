# 记忆增强

这一部分的设计目标，是带你从 Agent 记忆的基础概念，逐步走到动手实现，再延伸到更偏研究视角的理解。

## 第一步：Agent 记忆基础

目标：理解 AI 系统中“记忆”的核心概念与术语，例如：

- 短期记忆（Short-Term Memory）
- 长期记忆（Long-Term Memory）
- 长期记忆的不同类型，例如语义记忆（semantic）、程序记忆（procedural）、情景记忆（episodic）

## 第二步：动手实践记忆增强

目标：使用 Graphiti 构建并操作一个真实的、基于图结构的记忆系统。

1. 先了解当前主流实现方式，建立对整体生态的认识。
   - 基于向量（Vector-based）：Mem0、LangMem（开源）
   - 基于图（Graph-based）：Zep、Cognee
   - 本节重点：我们将使用 Graphiti 来实现基于图的 Agent 记忆。这里学到的概念可以迁移到其他系统中。

2. 理解“为什么选 Graphiti？”
   - Graphiti 是驱动 Zep 的一个强大开源框架。
   - 它是一个 Python 框架，用于构建具有时间感知能力（temporally-aware）的知识图谱。
   - 它支持在不做批量重算的情况下进行实时更新，因此非常适合动态的 Agent 系统。

3. 动手体验用于 Agent 记忆的 Graphiti MCP Server
   - <https://help.getzep.com/graphiti/getting-started/mcp-server>

4. 拆解 Graphiti 的工作方式，阅读官方文档
   - <https://help.getzep.com/graphiti/getting-started/welcome>

5. 实现 [OpenAI Agents SDK 内置 session memory](https://openai.github.io/openai-agents-python/sessions/)，并根据任务上下文管理需求进行定制。

6. 将 MCP Server 接入 OpenAI Agents SDK，并实现 [Reflect 设计模式](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-2-reflection/)

## 第三步：建立研究者视角

当前关于记忆的研究还很早期，未来会有大量演化。

- **全局视角**：要认识到长期记忆（LTM）、短期记忆（STM）和检索增强生成（RAG）并不是彼此孤立的概念，它们正在逐步收敛为一个更统一、更完整的智能 AI 架构。作为 AI 工程师，培养研究能力很重要。
- **必读材料：**
  - [Zep: A Temporal Knowledge Graph Architecture for Agent Memory](https://arxiv.org/abs/2501.13956)
  - 阅读 [Section 3 Methodology](https://arxiv.org/html/2502.12110v10)，了解它如何从 Zettelkasten 方法推导而来

## 拓展视野（可选但推荐）

目标：通过了解替代架构以及“原始灵感来源”人类记忆，进一步加深理解。

1. 了解 Mem0  
   为了理解不同方案之间的权衡，可以亲自体验一种原生向量化方案：  
   <https://docs.mem0.ai/openmemory/overview>

2. 研究最初蓝图：人类记忆  
   如果想构建真正更具共情能力、也更有效的 AI，理解人类认知的复杂性非常有价值。可以观看这个播客：  
   [Human Memory, Imagination, Deja Vu, and False Memories | Lex Fridman Podcast](https://www.youtube.com/watch?v=4iuepdI3wCU)



# Graphiti and Neo4j

   ┌────────────────────────────────────────────────────────┐
   │                    Graphiti (Ruby gem)                                                                                                 │
   │  ┌─────────────────────────────────────────────────────┐ │
   │  │  高层 API: ActiveRecord 风格的模型定义                                                                           │ │
   │  │  - 节点类定义 (Node)                                                                                                            │ │
   │  │  - 关系类定义 (Relationship)                                                                                                │ │
   │  │  - 查询构建器                                                                                                                         │ │
   │  └─────────────────────────────────────────────────────┘ │
   │                                                                       │                                                                               │
   │                                                                      ▼                                                                               │
   │  ┌─────────────────────────────────────────────────────┐ │
   │  │  Neo4j Ruby Driver (neo4j-ruby-driver)                                                                            │ │
   │  └─────────────────────────────────────────────────────┘ │
   │                                                                       │                                                                                │
   │                                                                      ▼                                                                               │
   │  ┌─────────────────────────────────────────────────────┐ │
   │  │   Neo4j 数据库 (Bolt 协议)                                                                                                    │ │
   │  └─────────────────────────────────────────────────────┘ │
   └────────────────────────────────────────────────────────┘

  关系: Graphiti 是 Neo4j 的 Ruby 语言 ORM/ODM，类似于 ActiveRecord 对于 SQL 数据库

   ## 使用示例
```
class User
    include Neo4j::ActiveNode
    property :name
    has_many :out, :friends, type: :FRIENDS_WITH
end
```

   ## 查询

```
   User.where(name: 'Alice').friends.to_a
```

