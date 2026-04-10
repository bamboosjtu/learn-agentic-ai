# 推理模型的提示工程

本节内容当前主要指向 OpenAI 关于推理模型的官方文档，可参考以下链接进一步学习：

- https://platform.openai.com/docs/guides/reasoning

这页文档主要在讲 **OpenAI 的推理模型（reasoning models）怎么用，以及什么时候该用**。

核心内容：

- **推理模型是什么**
  - 这类模型会在生成最终回答前，先分配内部推理 token。
  - 更适合复杂问题求解、编程、科学推理、多步骤 agent 工作流。
  - 文档建议大多数场景先从 `gpt-5.4` 开始；更强但更慢可用 `gpt-5.4-pro`；更低成本/延迟可考虑 `gpt-5-mini` 或 `gpt-5-nano`。  
  来源：<https://developers.openai.com/api/docs/guides/reasoning>

- **推荐怎么调用**
  - 优先用 **Responses API**，而不是旧的 Chat Completions API。
  - 调用时可设置 `reasoning.effort`，它控制模型在回答前投入多少推理预算。
  - 文档把 `reasoning.effort` 定位为“调优旋钮”，不是提升质量的首选手段。更重要的是把任务、约束和输出格式说清楚。  
  来源：<https://developers.openai.com/api/docs/guides/reasoning>

- **成本和 token 管理**
  - 推理 token 也会计入输出 token 使用量。
  - 可以用 `max_output_tokens` 限制总生成量，但要注意：如果模型在推理阶段就把预算用完，可能会返回 `incomplete`，而你可能已经消耗了输入和推理 token，却还没拿到可见答案。  
  来源：<https://developers.openai.com/api/docs/guides/reasoning>

- **推理内容是否可见**
  - 原始推理 token 默认**不会直接暴露**。
  - 如果模型支持，你可以通过 `reasoning.summary` 请求一个**推理摘要**，例如设为 `auto`，返回的是总结版 reasoning，而不是完整思维链。
  - 文档还提到，某些最新推理模型在使用 summarizer 前可能需要完成组织验证。  
  来源：<https://developers.openai.com/api/docs/guides/reasoning>

- **提示词建议**
  - 对推理模型，最好提供：
    - 明确任务目标
    - 清晰约束
    - 明确输出格式
  - 不要过度规定每一步中间推理过程。
  - 对 agent 或 research-heavy 工作流，要提前定义“完成标准”和“如何验证结果”。  
  来源：<https://developers.openai.com/api/docs/guides/reasoning>

一句话总结：**这页文档的重点不是“教你逼模型多想”，而是教你把推理模型接到 Responses API 上，并通过清晰任务定义、适当的 `reasoning.effort` 和 token 管理，稳定地用在复杂任务里。**

来源链接：
- OpenAI 官方文档：<https://developers.openai.com/api/docs/guides/reasoning>

如果你要，我可以继续把这页文档整理成一版更适合开发者落地的“实操清单”。
