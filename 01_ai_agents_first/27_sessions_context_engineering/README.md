# 第 27 课：高级 Sessions 与上下文工程

## [Evals x Context Engineering](https://cookbook.openai.com/examples/agents_sdk/session_memory#evals)

归根结底，评估（evals）同样是做好上下文工程所需要的关键手段。核心问题是：我们如何确认模型没有“丢失上下文”或者“混淆上下文”？

虽然这一整部分关于 memory 的内容未来完全可以独立成章，但这里先给出一些轻量级评估思路作为起点：

- **Baseline 与 Delta 对比**：持续运行核心评估集，对比实验前后结果，衡量 memory 改进效果。
- **LLM-as-Judge**：使用一个带精心设计评分 prompt 的模型来评估总结质量，重点看它是否以正确格式保留了最重要的信息。
- **Transcript Replay**：重新跑长对话，比较在上下文裁剪前后，下一轮回答的准确性。指标可以包括实体/ID 的 exact match，以及基于 rubric 的推理质量评分。
- **错误回归跟踪**：关注常见失败模式，例如问题未回答、约束丢失、不必要或重复的工具调用。
- **Token 压力检查**：标记那些因为 token 上限而丢掉受保护上下文的情况，记录裁剪前后 token 数，便于发现关键信息是否被误删。

## 概览

本课讲解高级 session 管理与上下文工程技巧，用于构建**生产级、可长时间运行的 agent**。你会学到如何在长时间多轮交互中保持一致性、效率和智能性。

## 为什么这很重要

**上下文是有限资源。** 随着对话不断变长：

- 模型会出现“context rot”（记忆退化、上下文混乱）
- 成本上升（每轮消耗更多 tokens）
- 延迟变高（处理时间更长）
- 注意力预算被不断拉伸

生产级 agent 需要更成熟的上下文管理能力，才能持续运行数小时、处理多个问题，并服务成千上万的用户。

## 你已经掌握的内容

前面的课程里，你已经学会了：

- Agent 基础、tools、handoffs（第 1-20 课）
- 基础 session memory（第 21 课）
- 用于检索的向量记忆（第 22 课）
- 评估与可观测性（第 26 课）

## 本课新增内容

本课教授的是**生产级上下文工程**模式：

1. **Context Trimming**：仅保留最近 N 轮（确定性、低延迟）
2. **Context Summarization**：压缩较早的上下文（长程记忆）
3. **高级 SQLite Sessions**：对话分支、使用分析
4. **PostgreSQL Sessions**：生产级数据库存储
5. **Redis Sessions**：分布式高性能扩展

## 课程结构

每个子课都采用渐进式、动手实践的方式：

| 子课 | 主题 | 重点 |
| ---------------------------- | ---------------------- | -------------------------------- |
| **01_context_trimming** | 保留最近 N 轮 | 确定性的上下文管理 |
| **02_context_summarization** | 压缩旧上下文 | 保留长程记忆 |
| **03_advanced_sqlite** | 带分析能力的 SQLite | 分支与使用跟踪 |
| **04_postgres_sessions** | PostgreSQL 存储 | 生产级数据库后端 |
| **05_redis_sessions** | 分布式 sessions | 高性能扩展 |

## 学习路径

**推荐顺序：**

1. 从 `01_context_trimming` 开始，掌握基础模式
2. 再学习 `02_context_summarization`，增强记忆能力
3. 学习 `03_advanced_sqlite`，便于开发与调试
4. 继续看 `04_postgres_sessions`，理解生产数据库方案
5. 最后掌握 `05_redis_sessions`，学习分布式扩展

**预计时长**：总计约 4-6 小时（每个子课约 1 小时）

## 关键概念

### Context 与 Memory 的区别

- **Context**：模型在一次推理中能关注到的全部 tokens
- **Memory**：跨多轮持久保存的信息（sessions、数据库等）

### Context Rot

随着上下文越来越长，模型会出现：

- 信息检索能力下降
- 在长对话中更容易混淆
- 成本与延迟增加
- 注意力预算被摊薄

### 上下文工程问题的本质

> “找到一组最小但高信号的 tokens，使它们最大化目标结果。”

这意味着你需要：

- **裁剪**已经不再相关的内容
- **压缩**较早的上下文为摘要
- **高效存储** session 状态
- **扩展**到多个用户和多个实例

## 开始学习

先进入第一个子课：

从 [01_context_trimming](./01_context_trimming/) 开始，学习最简单、最常见的上下文管理模式。

## 关键资源

- [OpenAI Cookbook: Session Memory](https://cookbook.openai.com/examples/agents_sdk/session_memory) - 上下文模式
- [Anthropic: Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) - 最佳实践
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) - 官方文档

### 补充阅读

- [Rise of Context Engineering](https://blog.langchain.com/the-rise-of-context-engineering/)
- [How to Fix Your Context](https://www.dbreunig.com/2025/06/26/how-to-fix-your-context.html)

![Context Engineering](./context_eng.jpeg)
