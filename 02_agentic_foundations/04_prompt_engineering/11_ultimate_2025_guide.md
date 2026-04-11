# 终极 2025 指南

[观看：The ULTIMATE 2025 Guide to Prompt Engineering - Master the Perfect Prompt Formula!](https://www.youtube.com/watch?v=bIxbpIwYTXI)

理解 AI 如何解读提示词，是从 ChatGPT 这类语言模型、以及 DALL·E、MidJourney 这类图像生成模型中获得准确且富有创意输出的关键。本教程将深入解释 AI 处理提示词的基本机制，并给出实用的提示工程技巧。

## AI 如何处理提示词

AI 模型会把词语转换成数值数据，并基于模式识别来生成回答。例如，当你输入 “a cat sitting on a couch” 时，AI 会先把每个词映射成数字，再结合它在海量训练数据中学到的模式进行分析。这些训练数据通常包括书籍、网站和代码。正是这种模式识别能力，使 AI 能够生成和上下文相关的输出。

## 提示工程

提示工程，指的是通过精心设计输入内容，引导 AI 模型输出你想要的结果。下面这些规则可以显著提升提示词效果：
- 直接明确（Be Direct）：去掉不必要的废话。比如，不要写 “Can you please write me a short story about a robot and a dog who go on an adventure together”，而是简化为 “Write a short story about a robot and a dog going on an adventure.”
- 描述充分（Be Descriptive）：提供关于主题、语气和受众的详细信息。例如：“Write a 1,000-word blog post about the economic situation of Kuwait from 1961 to 1967 aimed at beginners in a conversational tone.”
- 提供上下文和具体要求（Provide Context and Specifics）：明确受众、语气和结构，避免 AI 给出过于泛化的回答。例如：“Write a 1,000-word blog post about digital social media marketing for beginners using a conversational tone, targeting a general audience, and dividing it into five parts, each with a short list.”
- 赋予角色（Assign a Role）：让 AI 扮演某个专业身份，通常可以得到更准确、更贴切的回答。例如：“You are a patent lawyer. Explain the legal process for patenting an invention in simple terms for a non-legal audience.”
- 设置限制（Set Limitations）：提前规定边界，让回答更聚焦、更简洁。例如：“Write a 200-word summary on the benefits of solar energy, avoiding technical jargon and focusing on environmental advantages.”
- 迭代式提示（Iterative Prompting）：先从简单提示开始，再根据 AI 的回答逐步优化。例如先问 “Explain renewable energy”，再细化成 “Focus on the advantages of wind energy compared to fossil fuels”，最后进一步改成 “Rewrite the explanation for a 10-year-old audience using simple language and examples.”
- 指定格式与风格（Specify Format and Style）：明确你想要的格式、风格或语气。例如：“Write a timeline of major events in computer history formatted as a bullet list, including five to seven key milestones with one sentence explaining each.”
- 提供示例（Provide Examples）：用示例来引导 AI 输出更符合你预期的结果。例如：“Write a chord progression in the style of the Beach Boys. Here’s an example: [insert example].”
- 使用思维链（Use Chain of Thought）：把提示词设计成清单或步骤，有助于 AI 更有逻辑地完成复杂任务。例如：“Explain the pros and cons of renewable energy by addressing the following: environmental impact, economic considerations, availability and scalability, long-term sustainability.”
- 拆解复杂任务（Break Down Complex Tasks）：把大任务拆成更小、更易处理的部分，从而减少错误。例如，不要直接问 “Explain the causes, effects, and potential solutions for climate change”，而可以拆成：“List the top three causes of climate change”，“Describe the main effects of climate change on agriculture”，以及 “Suggest two practical solutions to combat climate change.”
- 让 AI 帮你优化提示词（Seek AI Assistance for Prompt Refinement）：你也可以直接让 AI 帮你改写提示词，使其更清晰有效。例如：“Refine this prompt to make it clearer and more effective: Explain the causes, effects, and potential solutions for climate change.”

## 提示工程中的参数

调整模型参数也会影响 AI 的回答风格：

- Temperature：控制随机性。较高值（例如 1.0）会让回答更有创造力；较低值（例如 0.2）则更稳定、更可预测。
- Max Tokens：决定回答长度。
- Top P 和 Top K：通过限制候选输出范围，影响生成结果的多样性。

## 图像生成提示词

在为图像生成模型编写提示词时，可以参考如下结构：

- 主体（Subject）：清楚定义图像的核心对象。例如：“A sleek black cat.”
- 描述（Description）：补充场景背景和细节。例如：“perched on a rain-soaked urban street in a glowing cyberpunk city at night.”
- 风格 / 美学（Style/Aesthetic）：明确希望的艺术风格或视觉审美。例如：“impressionist painting, wide shot.”

把这几个部分组合起来，就能形成一个更完整的提示词：

> “A sleek black cat perched on a rain-soaked urban street in a glowing cyberpunk city at night, impressionist painting, wide shot.”

## 图像生成的附加技巧

- 负向提示（Negative Prompting）：明确告诉模型不要出现哪些元素。例如：“Avoid buildings, pathways, and artificial lighting.”
- 分辨率与质量（Resolution and Quality）：可以指定所需清晰度或质量，例如 “high resolution” 或 “4K”，从而提升画面细节表现。
