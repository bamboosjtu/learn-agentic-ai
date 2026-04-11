# 用元提示写出完美的 Agent 指令

[How to Craft Perfect Agent Instructions with Meta Prompting](https://www.youtube.com/watch?v=oAxmD0OxsCo)

## 教程：如何用元提示打造完美的 Agent 指令

概览：元提示（Meta Prompting）是一种非常强大的方法，用来为 AI Agent 编写详细、结构化、且高度定制化的提示词。本教程将深入介绍如何创建清晰的指令，确保你的 AI Agent 能产出高质量、相关性强且有吸引力的回答。从设计基础提示词，到部署对话式 AI 应用，这份指南会帮助你掌握更高级的工具，从而提升 AI 交互效果。

## 核心概念与步骤

### 什么是元提示？

元提示，是指通过设计详细、多层次的指令，引导 AI Agent 输出更贴合上下文、更符合需求的回答。它通常包括：

- 提供示例：通过样例对话来展示理想的交互方式。
- 定义角色与职责：为 Agent 指定明确的任务和人设。
- 收集反馈：让 Agent 能根据用户输入动态调整响应方式。

### 构建你的第一个提示词

从一个基础提示词开始，明确以下内容：

1. 目的（Purpose）：清晰说明 Agent 的核心功能（例如：“一个为加拿大旅游服务的 AI 导游”）。
2. 职责（Responsibilities）：为 Agent 分配多个角色（例如旅行导游、旅游顾问、文化专家）。
3. 澄清请求（Clarification Requests）：引导 Agent 主动向用户获取更多细节，避免问题过于模糊。

示例：

```
Role: You are a Canadian Tourism AI Agent.  

Responsibilities:     
   1. Describe top attractions.  
   2. Provide travel recommendations.  
   3. Highlight cultural nuances.
   4. 用角色结构化提示词
```

### 为 Agent 角色设计一个结构化格式

- 主角色（Primary Role）：定义 Agent 的核心专长。
- 子角色（Sub-Roles）：为每个角色分配具体任务或职责。
- 示例（Examples）：为每项职责附上样例对话。

提示：可以使用 ChatGPT 或 GPT-4 这类工具，迭代式地打磨和原型化你的提示词。

### 示例：加拿大旅游 AI Agent

Agent 角色：

1. 旅行导游（Travel Guide）：介绍某个地区的景点。
2. 旅行顾问（Travel Advisor）：根据用户需求提供个性化旅行建议。
3. 文化专家（Cultural Expert）：分享当地习俗与文化亮点。

指令：

- 引导用户明确自己的偏好（例如地点、预算）。
- 用生动而详细的方式给出建议。

### 原型测试与优化

使用 GPT 工具测试并优化你的提示词：

1. 迭代测试（Iterative Testing）：将提示词输入 GPT，分析输出结果，再根据目标效果持续优化。
2. 反馈回路（Feedback Loops）：把用户反馈整合进提示词，实现持续改进。
3. 元指令（Meta Instructions）：把技巧和最佳实践直接嵌入提示词内部，以支持更细腻的交互。

### 高级技巧

- 协作式问题解决（Collaborative Problem-Solving）：让 Agent 根据用户需求在不同角色之间切换。
- 动态适应性（Dynamic Adaptability）：根据实时反馈调整回答方式。
- API 集成（API Integrations）：明确 Agent 应在何时、以何种方式调用 API，以完成更高级的功能。

### 扩展元提示

当你建立起一个足够稳健的提示词结构后，它就可以被复用并适配到多个 Agent 上：
1. 复制基础提示词。
2. 把主角色和职责替换成新的使用场景。
3. 测试新的提示词是否足够有效。

### 示例用例

- 内容生成 Agent：
  角色：内容策略师、文案写手、视觉设计师。
  职责：创作吸引人的社交媒体帖子、撰写文案说明、设计视觉内容。

- 客户支持 AI：
  角色：问题解决者、FAQ 助手、反馈收集者。

### 实用工具与技巧

- ChatGPT 语音控制：可以使用像 “Voice Control for ChatGPT” 这样的 Chrome 扩展，把语音转文字，轻松生成提示词。
- 示例交互：用 GPT 生成样例对话，用来启发和优化 Agent 行为。
- 构建 AI 群体（AI Swarm）：基于共享的结构模板，创建多个专门化 Agent，让它们协作解决问题。

## 结论：构建 AI 群体

元提示让你能够高效扩展 AI 系统。一个结构良好的提示词，可以作为多个不同角色 Agent 的“蓝图”。通过不断融入反馈并持续优化，你可以构建一个由多个协作型 AI Agent 组成的生态系统，也就是真正意义上的 “AI swarm（AI 群体）”。

让你的 AI 在每一次对话中，都成为推动改变的行动者。
