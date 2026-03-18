# 第 12 步：[Zep Memory Architecture](https://help.getzep.com/concepts) - 生产级记忆系统

理解 Graphiti 是如何为 Zep 的生产级 AI Agent 记忆架构提供底层能力的。可以把 Zep 理解成 Graphiti 之上的一层封装，它负责把知识图谱能力组织成真正可用的记忆系统。

## 什么是 Zep？

Zep 是一个闭源的“上下文工程（context engineering）”平台，它使用开源的 Graphiti 引擎，把每一次对话、用户交互以及业务数据流持续构造成一个动态的时序知识图谱。Zep 明确支持 agent memory 和 Graph RAG 场景：它能够提供“结构化、适合 LLM 使用的上下文”，包括用户偏好和业务事实，也提供“面向动态数据的 Graph RAG”，能够在毫秒级速度下对时序图进行查询。

getzep.com

- 在基准测试（例如 Deep Memory Retrieval 和 LongMemEval）中，Zep 相比 MemGPT（Letta）有明显优势，例如在多轮对话推理上准确率提升可接近 100%，并且相较于直接加载完整聊天日志，延迟可降低约 90%
- 由于它是专有 SaaS，Zep 本身是闭源的（而 Graphiti 是 Apache-2.0 开源项目），并以托管平台形式交付
- 它可以集成到企业技术栈中，例如 Neo4j 或 FalkorDB 后端、LangGraph 持久化等，并强调业务可用性，例如客户认证、RBAC，以及可能由其云服务提供的 HIPAA 合规能力

## 官方文档

- [Zep Memory Platform](https://help.getzep.com/concepts) - Zep 完整文档
- [Graphiti in Zep](https://help.getzep.com/graph-overview) - Graphiti 如何驱动 Zep
- [Zep vs Graph RAG](https://help.getzep.com/v3/docs/building-searchable-graphs/zep-vs-graph-rag) - Zep 与 GraphRAG 的比较
- [Agent Memory](https://help.getzep.com/v3/walkthrough) - 企业级记忆模式

## 学习目标

- 理解 Zep 基于 Graphiti 构建的记忆架构
- 学习面向 AI Agent 的生产级记忆模式
- 把 Zep 的设计思路迁移到教育 AI 系统中
- 为 TutorsGPT 设计可扩展的记忆系统
- 掌握企业级记忆管理策略

[观看：Building a Memory Agent with the OpenAI Agents SDK and Zep](https://www.youtube.com/watch?v=IkwRG_MgAn4)

## 核心概念

### Zep 的记忆架构

**Zep** 是一个建立在 Graphiti 之上的生产级记忆服务，它提供：

**记忆类型：**

- **User Memory**：个人上下文与偏好
- **Session Memory**：会话级上下文
- **Group Memory**：跨用户共享的知识
- **Fact Memory**：结构化知识与关系

**教育场景中的应用：**

- **Student Memory**：学生个体的学习历史与偏好
- **Class Memory**：班级共享的课程知识与讨论内容
- **Institutional Memory**：课程体系、教学法等机构级知识
- **Assessment Memory**：成绩模式与学习表现洞察

### Zep 中的记忆生命周期

```python
# Zep Memory Lifecycle（教育场景）
1. Memory Ingestion
   - Student interactions → Episodes
   - Assessment results → Facts
   - Course content → Structured knowledge

2. Memory Processing  
   - Entity extraction (students, concepts, skills)
   - Relationship discovery (learning progressions)
   - Community detection (study groups, concept clusters)

3. Memory Retrieval
   - Contextual search for personalized tutoring
   - Historical analysis for learning analytics
   - Predictive insights for intervention

4. Memory Management
   - Privacy boundaries (FERPA compliance)
   - Retention policies (academic records)
   - Performance optimization
```
