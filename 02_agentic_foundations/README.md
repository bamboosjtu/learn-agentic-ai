# 02 Agentic Foundations 总结

`02_agentic_foundations` 这一部分是整个仓库的“理论与认知地基”。它不直接进入复杂 Agent 系统实现，而是先回答几个更基础的问题：生成式 AI 是什么、为什么会出现 Agentic AI、背后的产业和技术背景是什么、Prompt Engineering 为什么重要、AI Agent 到底是什么。

如果说仓库后面的内容是在教你“怎么做 Agent”，那这一部分讲的就是“为什么会有 Agent、它建立在什么能力之上、你需要先具备哪些基本概念”。

## 这一部分的整体作用

这一章的目标不是让你马上写代码，而是帮你建立一套足够稳的认知框架，避免后面学习 Agent、Memory、Protocols、Multi-Agent 时只会照着例子跑，却不知道这些设计为什么成立。

它大致承担 5 个作用：

- 建立对 Agentic AI 整体浪潮的认识
- 补齐生成式 AI 和 LLM 的基础概念
- 补齐 Prompt Engineering 的方法论
- 解释 AI Agent 的定义、组成和应用场景
- 把技术、产业、工程和产品视角连接起来

## 各部分在讲什么

### `00_lets_get_started`

这一部分更像导言。它告诉你这套内容的推荐学习材料是什么，并把“从普通 LLM 应用走向 Agentic AI 系统”的学习方向先交代清楚。

这里的作用不是展开知识点，而是先给学习者一个入口，让你知道后面要学的是一条怎样的路线。

### `01_rise_of_agentic_ai`

这一部分讲的是 Agentic AI 为什么正在变成重要方向。内容更偏趋势、课程导航和背景介绍，帮助你理解：

- 为什么行业从“Prompt 一个模型”走向“让模型执行任务”
- Agentic AI 和传统 AI / SaaS / 自动化的区别
- 为什么工程能力、工作流设计、工具调用、状态管理变得越来越重要

这部分适合用来建立全局视角，知道自己学的不是零散技巧，而是一种新的软件形态。

### `02_technology_background`

这是这一章里最“底层”的部分，重点不是模型调用，而是 AI 时代的技术和产业背景。你会看到 GPU、CUDA、芯片制造、云计算、边缘计算、分布式系统、微服务、Ray、推理成本、AI 经济性这些主题。

它的价值在于让你意识到：

- Agentic AI 不是孤立出现的
- 它依赖上游算力、模型训练与推理基础设施
- 也依赖下游软件架构、云原生、服务编排和系统工程能力

对新人来说，这一部分不一定要一开始逐字精读，但至少要知道这些词为什么会在 Agent 时代变得关键。

### `03_generative_ai_for_beginners`

这一部分负责补生成式 AI 基础，是通往 Agent 的前置知识。它会覆盖：

- 生成式 AI 的基本概念
- LLM 是什么、能做什么、不能做什么
- 常见模型和产品形态
- 对话式 AI 的基本使用方式
- 初学者如何开始接触 ChatGPT、Copilot、Gemini 等工具

这一部分的定位很明确：先让你对“模型本身”建立最基础的理解，再进入更复杂的 Prompt 和 Agent。

### `04_prompt_engineering`

这一部分是从“会用模型”走向“能稳定驱动模型”的关键过渡层。内容覆盖得很广，从基础 Prompt 设计，到中高级 prompting 技术，再到面向 Agent 的 Prompt 方法。

它的主线包括：

- Prompt 的基本组成与写法
- 角色设定、指令设计、Few-shot 等基础技巧
- CoT、Self-Consistency、Prompt Chaining、Least-to-Most、RAG 等中级方法
- Self-Refine、Reflexion、Tree of Thoughts、Plan-and-Solve 等高级方法
- 面向 Agent 的 Prompt 思维，如 ReAct、工具使用、函数调用

这一部分的核心意义是：Agent 系统的很多行为质量，最终仍然取决于 Prompt 设计。不会 Prompt Engineering，后面的 Agent 往往只能停留在“能跑”，很难做到“稳定、可控、可复用”。

### `05_ai_agents_intro`

这是这一章最直接面向 Agent 的部分。它会系统介绍：

- 什么是 AI Agent
- AI Agent 与普通聊天机器人、普通工作流的区别
- Agent 的类型、组成部件和应用场景
- Agent 的经济价值与业务意义
- RAG、Tool Use、Multi-Agent 等概念和 Agent 的关系

这部分相当于后续实作章节的概念桥梁。学完之后，你应该能看懂仓库后面为什么会出现：

- tool calling
- memory
- orchestration
- multi-agent collaboration
- protocol / deployment / evaluation

## 检查清单

学完 `02_agentic_foundations`，你不一定已经会构建复杂 Agent 系统，但你应该至少具备下面这些判断能力：

- 能解释生成式 AI、LLM、Prompt Engineering、AI Agent 之间的关系
- 能理解为什么 Agentic AI 会成为一个独立的软件工程方向
- 能区分普通问答、工作流系统和真正的 Agent 系统
- 能看懂后续仓库中关于 tools、memory、multi-agent、protocols 的基本动机
- 能从技术、产品和工程三个角度理解 Agent 的价值与限制

