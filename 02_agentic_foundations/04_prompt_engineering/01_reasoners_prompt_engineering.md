# 推理模型的提示工程

本节内容当前主要指向 OpenAI 关于推理模型的官方文档，可参考以下链接进一步学习：

- https://platform.openai.com/docs/guides/reasoning

> 这篇文档的核心是在讲：**推理模型适合复杂任务，但用法和普通生成模型不同，重点是给它清晰目标、留够推理空间、控制好成本。**
>
> **核心内容**
> - 推理模型会先消耗一部分内部 `reasoning tokens` 再给出最终回答，适合复杂问题求解、编程、科学推理和多步 Agent 工作流。
> - 官方建议大多数场景先用 `gpt-5.4`；更强但更慢可用 `gpt-5.4-pro`；更便宜更快可考虑 `gpt-5-mini` 或 `gpt-5-nano`。
> - 推理模型更推荐搭配 `Responses API` 使用，而不是旧的 Chat Completions API。
> - `reasoning.effort` 是一个调节“思考深度”的旋钮：
>   - `none` 适合提取、路由、简单转换这类低延迟任务
>   - `low` 适合稍微需要思考但又不想增加太多延迟的任务
>   - `medium/high` 适合规划、编码、综合分析、复杂推理
>   - `xhigh` 只建议在评测证明确实值得时再用
> - 推理 token 不会保留在后续上下文里，但**会占上下文窗口并计费**，所以要关注成本和窗口上限。
> - 可以通过 `usage.output_tokens_details.reasoning_tokens` 看模型到底用了多少推理 token。
> - 成本控制主要靠 `max_output_tokens`。但如果设得太小，模型可能在还没产出可见答案前就因为 token 不够而返回 `incomplete`。
> - 官方建议一开始实验时，至少预留 **25,000 tokens** 给推理和输出，再根据实际使用情况调整。
> - 原始推理过程不会直接暴露，但可以通过 `reasoning.summary` 获取总结版推理摘要；部分场景还支持 `reasoning.encrypted_content`，用于把推理内容加密传给后续轮次。
> - 提示词策略上，官方明确建议：
>   - 给清楚任务、约束和输出格式
>   - 不要过度规定中间推理步骤
>   - 把 `reasoning.effort` 当调参项，而不是补救提示词质量的主要手段
>   - 对 Agent / research 场景，要明确“完成标准”和“如何自我验证”
>
> **结论**
> - 推理模型的价值不在“回答更长”，而在于**更擅长处理复杂、多步、需要计划和验证的任务**。
> - 真正的使用重点不是疯狂提高 `reasoning.effort`，而是：
>   - 选对模型
>   - 用 `Responses API`
>   - 给清晰任务和输出约束
>   - 预留足够 token
>   - 监控 `reasoning_tokens` 和 `incomplete` 状态
> - 如果任务只是简单抽取、分类、改写，推理模型未必划算；但对于编码、规划、复杂分析和 Agent 工作流，它们通常更合适。
>
> 来源：
> - https://developers.openai.com/api/docs/guides/reasoning
> - https://platform.openai.com/docs/guides/reasoning

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

