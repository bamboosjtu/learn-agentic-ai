# 用元提示“读懂”你的 AI 思维

[观看：How to Read Your AI's Mind with Meta Prompting & Chain-of-Thought](https://www.youtube.com/watch?v=ONsQI5npBYo)

通过元提示（meta-prompting）与思维链（chain-of-thought）技巧来增强 AI 交互，可以显著提升 AI 输出结果的质量与透明度。本教程基于 Prompt Advisers 的 Mark 所分享的思路，介绍了一套结构化方法，帮助你设计更有效的提示词，让 AI 能够表达自己的不确定性、担忧点，以及它认为缺失的信息。

## 定义 AI 的角色和专业领域

首先，明确指定 AI 的角色以及它擅长的领域。这一步能够建立上下文，并引导 AI 的回复方向。例如：

> “You are an AI agent specialized in providing detailed step-by-step reasoning and actions to answer questions. You combine chain-of-thought prompting with react prompting to generate both reasoning traces and task-specific actions leading to reliable and factual responses.”

## 指定职责范围

清楚定义 AI 在交互过程中的职责。这些职责可以包括直接回答问题、说明推理过程，以及在必要时主动请求澄清。例如：

- 直接回答：对简单、明确的事实类问题，给出简洁答案。
- 推理说明：对于复杂问题，展开说明思考过程，并指出其中的假设或不确定性。
- 澄清提问：如果用户输入模糊或细节不足，主动请求补充信息。

## 规定回答结构

定义 AI 应该如何组织输出格式，以确保回答清晰且实用。一个结构化的回复可以包含：

- Answer：对用户问题的直接回答。
- My Reasoning：解释得出该答案时所经历的步骤和考虑因素，包括任何假设或疑问。
- Suggestions for Improvement：告诉用户如何提供更好的输入，以便获得更准确的回答。

## 提供模拟示例

通过加入若干示例交互，进一步加强 AI 对目标行为的理解。建议准备 3 到 5 个不同类型的例子，覆盖多种场景。例如：

示例 1：
- 用户：“How can I increase customer retention for my online store?”
- AI：
  - Clarification：“Could you specify your industry and target customer demographics?”
  - Answer：“Implementing a loyalty program can enhance customer retention.”
  - My Reasoning：“Loyalty programs incentivize repeat purchases by rewarding customers, fostering brand loyalty.”
  - Suggestions for Improvement：“Providing details about your current customer engagement strategies would allow for more tailored advice.”

示例 2：
- 用户：“What’s the capital of France?”
- AI：
  - Answer：“Paris.”
  - My Reasoning：“This is a well-established fact requiring no further elaboration.”
  - Suggestions for Improvement：“N/A.”

## 实现这个提示词

把上述组成部分整合成一个完整提示词。下面是一个为“加拿大历史学习搭子”定制的示例：

> “You are an AI study assistant specialized in Canadian history. Your responsibilities include providing direct answers to factual questions, outlining your reasoning for complex inquiries, and requesting clarification when user inputs are vague. Structure your responses with an ‘Answer’ section, followed by a ‘My Reasoning’ section, and conclude with ‘Suggestions for Improvement’ if applicable. Below are example interactions to guide your responses: [Insert 3-5 diverse examples here].”

## 测试与迭代优化

当提示词写好后，使用你的 AI 模型进行测试，观察它的表现。分析返回结果，确认是否符合你的预期；如果有偏差，就继续调整提示词，以修复问题或提升表达清晰度。

通过这种结构化方法，你实际上是在和 AI 建立一个透明的反馈回路，让它能更有效地表达自己的不确定性以及缺失信息。这种方法可以显著提升 AI 交互质量，让输出结果更有信息量，也更可靠。
