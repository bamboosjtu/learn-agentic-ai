# OpenAI Agents SDK 项目

## 项目 0：构建一个专用天气助手

https://www.datacamp.com/tutorial/openai-agents-sdk-tutorial

## 项目 1：邮件自动化 Agent

https://aiablog.medium.com/complete-openai-agents-sdk-course-2025-a4dd68af0855

https://github.com/nnamu-cl/agents-sdk-course-2

## 项目 2：构建研究助手

https://www.datacamp.com/tutorial/openai-agents-sdk-tutorial

## 项目 3：使用 Agents SDK 与 Stripe API 自动化争议管理

https://cookbook.openai.com/examples/agents_sdk/dispute_agent

## 项目 4：“Agento”：模块化 AI 规划系统

“Agento” 项目展示了如何使用 OpenAI Agents SDK，把宽泛目标转化为结构化、可执行的计划，并通过迭代不断打磨。你几乎可以把任何目标或想法交给它，它都会开始帮你分解和规划。你可以从这里查看细节和起始代码，并在此基础上继续改进：

https://github.com/dazzaji/agento6

# 需要提交的项目

下面是一些适合学生使用 OpenAI Agents SDK 构建 AI Agent 的项目建议。这些项目兼具教育性、实用性和趣味性，能够帮助学生在开发问题解决能力和批判性思维的同时，探索 AI Agent 的能力边界。每个项目都包含项目描述、目标和建议的实施步骤。这里刻意不直接给出代码，以鼓励学生结合 OpenAI Agents SDK 文档和自己的创造力独立实现。

---

### 项目 1：个人学习助手

**描述：** 构建一个 AI Agent 系统，帮助学生管理学习计划、查找相关学习资源，并总结学术内容。系统由多个 Agent 协作完成，包括：计划安排 Agent、网页研究 Agent 和摘要 Agent。

**目标：**

- 学习如何创建并编排多个具有不同职责的 Agent
- 使用 Responses API 进行网页搜索和文件处理
- 实现 Agent 之间的 handoff，实现顺畅的任务委派

**给学生的实施步骤：**

1. **定义 Agent：**
   - 创建一个 “Scheduler Agent”，接收用户输入（例如学习主题和截止日期），生成学习计划。
   - 创建一个 “Research Agent”，搜索与学习主题相关的文章、视频或论文。
   - 创建一个 “Summarizer Agent”，把研究结果压缩成简洁笔记。
2. **设计输入方式：**
   - 做一个简单界面，例如命令行或文本界面，让用户输入学习目标和时间限制。
3. **配置工具：**
   - 使用 Responses API 内建的网页搜索工具，让 Research Agent 获取实时信息。
   - 让 Summarizer Agent 可以处理网页结果中的文本或上传文件（如 PDF）。
4. **实现 Handoffs：**
   - 让 Scheduler Agent 把学习主题交给 Research Agent，Research Agent 再把收集到的数据交给 Summarizer Agent。
5. **添加 Guardrails：**
   - 增加检查，确保网页搜索结果相关（例如过滤非学术来源），同时保证摘要足够简洁（例如限制字数）。
6. **测试和调试：**
   - 用类似 “Learn about machine learning by next week” 这样的输入进行测试，并借助 SDK tracing 工具观察 Agent 之间的协作过程。
7. **增强功能：**
   - 添加将学习计划和摘要保存到文件中的功能，方便后续查看。

---

### 项目 2：AI 驱动旅行规划师

**描述：** 开发一个多 Agent 系统，根据用户偏好（预算、目的地、兴趣）规划一次旅行。不同 Agent 分别负责目的地研究、行程安排和预算控制。

**目标：**

- 探索 Agent 协作与任务委派
- 集成实时网页搜索和基础计算工具
- 练习调试和优化 Agent 工作流

**给学生的实施步骤：**

1. **定义 Agent：**
   - 创建 “Destination Agent”，根据用户兴趣（例如海滩、博物馆）研究适合的旅行地点。
   - 创建 “Itinerary Agent”，根据目的地信息生成逐日行程安排。
   - 创建 “Budget Agent”，估算成本并确保计划符合用户预算。
2. **设计输入方式：**
   - 允许用户输入类似 “我想要一个 5 天欧洲行，预算 2000 美元以内，主题偏历史” 的偏好。
3. **配置工具：**
   - 使用网页搜索工具获取目的地、景点和旅行成本信息。
   - 为 Budget Agent 实现一个简单成本计算工具，例如汇总机票、酒店和活动费用。
4. **实现 Handoffs：**
   - 让 Destination Agent 把候选地点交给 Itinerary Agent，Itinerary Agent 再与 Budget Agent 协作，完成最终计划。
5. **添加 Guardrails：**
   - 确保 Destination Agent 只选择安全、适合游客的地点；Budget Agent 在超预算时要明确提示。
6. **测试和调试：**
   - 用不同预算和目的地组合测试，并使用 tracing 找出系统失败点，例如行程安排不完整。
7. **增强功能：**
   - 如果预算不足，自动推荐替代目的地。

---

### 项目 3：客户支持自动化系统

**描述：** 构建一个用于虚构在线商店的 AI Agent 系统，自动处理客服问题。系统可以回答常见咨询、处理退货流程，并把复杂问题升级给“类人工客服”Agent。

**目标：**

- 理解如何为真实业务场景设计 Agent
- 使用文件搜索和外部工具集成
- 实现安全机制，避免不恰当回答

**给学生的实施步骤：**

1. **定义 Agent：**
   - 创建 “Inquiry Agent”，回答基础问题，例如发货时间、商品是否有货。
   - 创建 “Returns Agent”，根据退货政策引导用户完成退货流程。
   - 创建 “Escalation Agent”，识别复杂问题，并生成一份供人工审核的回复草稿。
2. **设计输入方式：**
   - 设计一个文本输入界面，让用户提出问题，例如 “发货需要多久？” 或 “我想退货。”
3. **配置工具：**
   - 使用文件搜索工具，让 Inquiry Agent 访问 FAQ 文档或商品目录。
   - 让 Returns Agent 读取退货政策文件并处理用户请求。
4. **实现 Handoffs：**
   - 让 Inquiry Agent 把无法解决的问题转交给 Escalation Agent；必要时，Returns Agent 也可以向 Inquiry Agent 确认信息。
5. **添加 Guardrails：**
   - 增加校验，防止 Agent 给出错误信息，或在不必要时乱升级问题。
6. **测试和调试：**
   - 测试常见客服问题和边界情况（如模糊问题），并使用 tracing 确认 handoff 是否顺畅。
7. **增强功能：**
   - 增加会话日志记录，便于后续分析或模型训练。

---

### 项目 4：新闻摘要生成器

**描述：** 创建一个 AI Agent 系统，根据用户指定主题（如科技、体育）生成每日新闻摘要。系统中不同 Agent 分别负责搜索网页、过滤内容和总结文章。

**目标：**

- 使用网页搜索获取实时信息
- 练习多步推理和内容过滤
- 探索可观测性工具用于调优性能

**给学生的实施步骤：**

1. **定义 Agent：**
   - 创建 “Search Agent” 搜索指定主题的最新新闻文章。
   - 创建 “Filter Agent” 去除无关或低质量来源。
   - 创建 “Digest Agent” 把过滤后的文章总结成简短摘要。
2. **设计输入方式：**
   - 允许用户输入感兴趣的话题，例如 “Latest AI developments”。
3. **配置工具：**
   - 使用网页搜索工具抓取文章，并保留引用信息。
   - 设计简单过滤机制，例如根据来源可信度或发布时间筛选。
4. **实现 Handoffs：**
   - 让 Search Agent 把结果交给 Filter Agent，再由 Filter Agent 交给 Digest Agent。
5. **添加 Guardrails：**
   - 确保 Filter Agent 排除过时或不可靠来源，Digest Agent 保持摘要简短。
6. **测试和调试：**
   - 用不同主题测试，检查摘要的准确性和相关性，并用 tracing 找出低效环节。
7. **增强功能：**
   - 增加通过邮件发送摘要或导出 PDF 的功能。

---

### 项目 5：代码审查助手

**描述：** 开发一个 AI Agent 系统辅助代码审查，包括分析代码文件、提出改进建议，并自动生成文档。适合有一定编程基础的学生。

**目标：**

- 集成文件处理和外部工具使用
- 学习用 Agent 处理多步骤任务
- 探索复杂工作流调试

**给学生的实施步骤：**

1. **定义 Agent：**
   - 创建 “Analyzer Agent”，读取代码文件并识别潜在问题（如语法、风格问题）。
   - 创建 “Suggestion Agent”，提出修复建议或优化方案。
   - 创建 “Documentation Agent”，根据代码生成注释或 README。
2. **设计输入方式：**
   - 允许用户上传代码文件（如 Python 脚本）或输入 GitHub 仓库链接。
3. **配置工具：**
   - 使用文件搜索工具处理上传的代码文件。
   - 可选：集成网页搜索，用于查找最佳实践或文档模板。
4. **实现 Handoffs：**
   - 让 Analyzer Agent 把发现的问题交给 Suggestion Agent，再与 Documentation Agent 配合形成最终输出。
5. **添加 Guardrails：**
   - 确保 Analyzer Agent 只标记真正相关的问题，Suggestion Agent 不给出不切实际的修改建议。
6. **测试和调试：**
   - 用示例代码（如带 bug 的脚本）测试，并使用 tracing 确保每个 Agent 都真正参与了工作。
7. **增强功能：**
   - 增加多语言支持，或集成 GitHub API 直接为 Pull Request 添加评论。

---

### 给学生的一些通用建议

- **从简单开始：** 先从单 Agent 单任务做起，再逐步扩展到多 Agent 系统。
- **多看文档：** 参考 OpenAI Agents SDK 官方文档，了解环境配置和工具细节。
- **多实验：** 尝试不同的 Agent 指令、工具组合和配置，找到最佳方案。
- **多协作：** 可以组队一起设计 Agent 角色，并互相测试系统。
- **多展示：** 通过演示介绍你的系统，并解释各个 Agent 是如何协同完成任务的。
