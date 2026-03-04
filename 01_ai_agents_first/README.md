# 构建 AI Agent

OpenAI Agents SDK 是一个开源、轻量级框架，帮助开发者构建并编排“Agentic”AI 应用。也就是让多个 AI“代理（agents）”协同工作，自主完成复杂的多步骤任务。

**[OpenAI Agents SDK Panaversity 课程视频列表](https://www.youtube.com/playlist?list=PL0vKVrkG4hWovpr0FX6Gs-06hfsPDEUe6)**

**[观看：OpenAI 全新 Agents SDK - 速成课程](https://www.youtube.com/watch?v=e7qvd2bOITc&t=4s)**

**[OpenAI Agents SDK 文档](https://openai.github.io/openai-agents-python/)**

**[OpenAI Agents SDK 概览](https://medium.com/@danushidk507/openai-agents-sdk-ii-15a11d48e718)**

**[OpenAI 的战略布局：Agents SDK 以及它为何会改变企业 AI](https://venturebeat.com/ai/openais-strategic-gambit-the-agent-sdk-and-why-it-changes-everything-for-enterprise-ai/)**

> 这篇 VentureBeat（2025年3月14日）文章的核心观点是：OpenAI 通过 Responses API + 内置工具 + 开源 Agents SDK，在企业 AI赛道做了一次“平台级卡位”。要点总结：
>
>   1. 从“模型能力竞争”转向“Agent 平台竞争”。 OpenAI 不只是发模型，而是提供从工具到编排的整套 Agent 开发栈，目标是成为企业默认基础设施。
>   2. 企业价值：降低碎片化复杂度。以前企业常要拼多个框架、RAG 组件、编排逻辑；现在可在一套标准化接口中完成更多能力（如 web/file search、computer use、多 Agent handoff、tracing）。
>   3. 战略信号：OpenAI 借开源吸收外部创新。文章认为 OpenAI 在“Agent 可靠性”上承认需要社区创新，因此开放 SDK 来加速迭代。
>   4. API 标准化带来网络效应。OpenAI 的 API 形态已成事实标准之一。若企业围绕该标准建设，迁移和生态协同会更容易，但 OpenAI 也更居中。
>   5. 对生态的冲击。对纯 Agent 框架公司（如编排/RAG 中间层）形成直接竞争，可能推动市场整合。
>   6. 企业决策的两难。
>       - 好处：更快落地、可观测性更好、上线路径更清晰。
>       - 风险：供应商锁定、与现有系统兼容、真实生产可靠性仍需验证。
>       
>   文章也指出此前方案（如 Assistants API）未完全满足企业需求，新方案仍要时间验证。
>   【一句话结论】这篇文章把 OpenAI Agents SDK 定位为一次“从模型提供商到企业 Agent 平台”的战略转向：机会很大，但企业应在采用速度与锁定风险之间做权衡。

https://github.com/aurelio-labs/cookbook/blob/main/gen-ai/openai/agents-sdk-intro.ipynb

## OpenAI Agents SDK

### 启发思考的问题

OpenAI Agents SDK 的设计非常值得研究。下面这些问题可以帮助你更深入地理解代码：

1. `Agent` 类为什么被定义为 `dataclass`？

查看 `Agent` 源码： https://openai.github.io/openai-agents-python/ref/agent/

> 从 Agent 源码看，它被定义成 @dataclass 主要是工程取舍，不是语义“必须”：
>
>   1. Agent 本质是“配置对象”
>        - 字段很多（name/instructions/tools/handoffs/model/...），更像一组声明式配置。
>        - 用 dataclass 可以自动生成 __init__ / __repr__ / __eq__，减少大量样板代码。
>
>   2. 需要安全的可变默认值
>        - 源码里大量 field(default_factory=list)（如 tools/handoffs/input_guardrails）。
>        - dataclass 对这种“每实例独立默认容器”非常直接、标准。
>
>   3. 需要低成本克隆配置
>        - clone() 直接用 dataclasses.replace(self, \*\*kwargs)。
>        - 这正是 dataclass 的典型用法：快速“改一点配置，复用其余配置”。
>
>   4. 与体系内其他类型保持一致
>        - AgentBase、Agent、RealtimeAgent 都是 dataclass，结构统一，维护成本更低。
>
>   5. 仍保留运行时校验
>        - 他们在 __post_init__ 做了严格类型检查，说明 dataclass 负责“数据承载与构造便利”，业务约束仍由显式校验控制。
>
>   结论：Agent 用 dataclass 是为了把它当作“可组合、可克隆、字段多的配置载体”，提升可读性和可维护性，而 不是为了不可变或更强封装。



2a. 系统提示词（system prompt）为什么放在 `Agent` 类的 `instructions` 中？为什么它还可以设置为可调用对象（callable）？

> 放在 Agent.instructions 里，是因为在这个框架里它被当成“智能体定义的一部分”，而不是一次请求的临时参 数。
>
>   1. 为什么放在 instructions
>        - Agent 是“角色+能力+约束”的配置对象，instructions 正是角色/行为边界。
>        - 同一个 Agent 在不同入口运行，系统提示不会漂移。
>        - 评测（eval）时更稳定，便于定位是 instructions 问题还是 tools 问题。
>        - 和 tools、handoffs 放在一起，方便复用、测试、克隆和版本管理。
>        - 运行器拿到一个 Agent 就能完整知道它该怎么思考和行动。
>        
>   2. 为什么允许 callable
>        - 静态字符串不够：很多系统提示要随上下文动态变化（用户身份、租户策略、语言、会话状态、环境变量）。
>        - callable 可以在“每次 run 时”生成最新指令，而不是实例化时写死。
>        - 这让你能做：
>            - 按用户/组织注入不同 policy
>            - 根据上下文拼接任务目标
>            - 动态启用/禁用某些行为约束
>            - 保持 Agent 定义不变，但运行时行为可参数化
>
>   一句话：instructions 放在 Agent 是为了“把行为定义集中管理”，支持 callable 是为了“让定义可复用，但执行时可动态适配”。



2b. 但用户提示词（user prompt）是作为参数传给 `Runner` 的 `run` 方法，而且这个方法是类方法（classmethod）。这是为什么？

查看这里： https://openai.github.io/openai-agents-python/ref/run/

>   1. Runner.run(...) 接收“本次输入”
>        - 用户提示词属于一次会话/一次任务的瞬时数据，不应写进 Agent 配置。
>        - 所以作为 run 参数传入，天然支持每次调用不同输入。
>
>   2. run 做成 classmethod 的原因
>        - Runner 更像“执行引擎/调度器”，通常不需要先创建实例再跑。
>        - 用类方法可直接 Runner.run(agent, input, ...)，API 更简洁。
>        - 也避免把可变运行态挂在 Runner 实例上，减少状态污染风险（并发/复用更清晰）。
>
>   一句话：Agent 管“定义”，run 管“执行时数据”；classmethod 是为了让执行器以无状态、易调用的方式工作。



3. `Runner` 类的职责是什么？

> Runner 的职责可以概括为一句话：把一个 Agent 从“定义”执行成“结果”。
>
> 核心职责通常包括：
>   1. 执行循环
>        - 驱动 LLM 多轮推理，直到满足退出条件（最终输出、无工具调用、异常、超限）。
>
>   2. 工具与交接调度
>        - 执行工具调用。
>        - 在多 Agent 场景中处理 handoff，把控制权转给下一个 agent。
>
>   3. 上下文与状态管理
>        - 维护本次 run 的消息、上下文、步骤结果。
>        - 把工具结果/中间输出回填给模型继续推理。
>
>   4. 护栏与策略执行
>        - 在输入、过程、输出阶段触发 guardrails。
>        - 违反策略时中断、报错或升级人工介入。
>
>   5. 结果封装与可观测性
>        - 返回结构化 run result（最终输出、新增消息、轨迹等）。
>        - 提供日志/trace 钩子，便于调试和评测。
>
>   所以：Agent 定义“做什么”，Runner 负责“怎么跑完”。



4. Python 中什么是泛型（generics）？为什么 `TContext` 要用泛型？

> TContext 用泛型是为了在“通用框架”里实现“强类型的上下文传递”。
>
>   1. 表达“上下文类型可变，但同一次 Agent/Runner 是一致的”
>        - 不同项目上下文结构不同：有的用 dict，有的用 UserSession 类。
>        - 泛型让框架不写死上下文类型。
>
>   2. 提升静态类型安全
>        - Agent[TContext]、RunContextWrapper[TContext]、工具函数参数能联动校验。
>        - IDE/类型检查器能发现“把错误上下文类型传进来”的问题。



---

### 核心概念：简洁设计的力量

Agents SDK 真正突出的地方，在于它在“简洁”和“能力”之间取得了很好的平衡。SDK 主要围绕四个核心原语（primitives）构建：

- **Agents：**  
  这是预先配置好的语言模型（LLMs），可包含特定指令、工具访问能力（如 Web 搜索、文件检索），以及安全护栏。Agent 能根据上下文生成回复，并决定调用哪个工具。  


- **Handoffs：**  
  SDK 的强大能力之一是任务委派。一个 Agent 如果遇到超出自己领域的问题，可以把任务“交接（handoff）”给另一个更专业的 Agent。  


- **Guardrails：**  
  这是内置的安全检查机制，用于校验输入与输出，确保 Agent 在设定边界内运行，并降低自动化带来的风险。  
  
- **Tracing & Observability：**  
  SDK 集成了追踪能力，开发者可以可视化并调试 Agent 的执行流程。这对监控复杂工作流、优化性能非常有帮助。

这种极简设计让新手更容易上手，同时也给有经验的开发者保留了足够的灵活性去构建复杂系统。内置追踪能力进一步提升了开发体验，让 Agent 工作流更容易可视化、调试和评估。



---

### 关键特性

- **Python-First 设计：**  
  SDK 与 Python 天然融合。开发者可以快速创建 Agent、定义可用工具（甚至把 Python 函数直接转换为可调用工具），并把多个流程串联起来，而不需要陡峭的学习曲线。

- **内置 Agent 循环：**  
  当你通过 SDK 运行 Agent 时，它会自动进入一个循环：
  1. 向 LLM 发送提示词。
  2. 检查是否需要调用工具。
  3. 处理 Agent 之间的交接（handoff）。
  4. 重复以上步骤，直到产生最终输出。
  
- **互操作性：**  
  虽然它与 OpenAI 自有模型和新版 Responses API 能无缝配合，但 Agents SDK 也足够灵活，可用于任何支持 Chat Completions API 格式的模型提供方。

- **简化多 Agent 工作流：**  
  它可以让你构建复杂系统。例如，一个 Agent 负责调研，另一个 Agent 负责客服，多个 Agent 协同完成共同目标。 


- **真实世界应用：**  
  企业可用该 SDK 构建 AI 助手，例如通过 Web 搜索拉取实时数据、通过文件搜索访问内部文档，甚至与计算机界面进行交互。这让 AI Agent 在客服、法律研究、金融等行业更具实用性。  


---

### 为什么它重要

Agents SDK 把过去需要手工编排或临时拼接的大量编排逻辑抽象掉了，显著简化开发流程，让你能把精力聚焦在应用核心功能上。由于抽象层更少且以 Python 为中心，复杂 Agent 工作流也更容易维护、扩展和调试。

总结来说，OpenAI Agents SDK 提供了构建自主多 Agent 系统的基础模块。它让不同 Agent 的能力可以协同起来处理复杂任务，是 AI 从“只会对话”走向“可执行、可落地”的关键一步。

---

如果你想看更深入的技术细节和示例，可以参考[官方文档](https://openai.github.io/openai-agents-python/)和 [GitHub 仓库](https://github.com/openai/openai-agents-python)

[使用 OpenAI Agents SDK 构建 AI Agent：新手指南](https://medium.com/@agencyai/building-ai-agents-with-openais-agents-sdk-a-beginner-s-guide-66751e5e7e05)

> 这篇文章是一个面向新手的 OpenAI Agents SDK 上手指南，主线很清晰：从“能跑起来”到“能做一个小型多 Agent 系统”。
>
>   核心内容
>
>   1. 先讲 SDK 的 4 个核心概念
>      Agents、Handoffs、Guardrails、Tracing。
>   2. 从最小示例开始
>      演示 Agent + Runner.run() 的 Hello World，解释 Agent loop：模型判断是直接回复、调用工具，还是交接给其他 Agent。
>   3. 逐步增强能力
>      加入函数工具（天气查询示例）、加入 handoff（语言分流/专长代理）、加入输入护栏（拦截不当请求）、加入 tracing（观察执
>      行链路）。
>   4. 给出一个完整综合案例
>      “电商客服系统”：一个总分流 Agent，交接给订单与退款专长 Agent，并调用订单状态/物流预估/退款工具。
>   5. 结论与下一步
>      作者强调：SDK 的优势是低门槛但可扩展；建议下一步连接真实 API、做结构化输入输出、加强 guardrails、加监控用于生产。

### 早期评价

[拆解 OpenAI Agents SDK：面向 AI Agent 未来的技术深潜](https://mtugrull.medium.com/unpacking-openais-agents-sdk-a-technical-deep-dive-into-the-future-of-ai-agents-af32dd56e9d1)

> 这篇文章（2025-03-12）的核心是：OpenAI Agents SDK 把“AI Agent 从实验玩具推进到工程化生产”，关键在于更少抽象、更强可观
>   测性和更规范的工具调用。
>
>   文章要点
>
>   1. 定位
>      Agents SDK 不是单纯聊天封装，而是面向多步骤任务的 Agent 编排框架，和 Responses API、工具能力一起使用。
>   2. 技术核心（六件套）
>      Agent、Tools（函数工具）、Agent Loop、Handoff、Guardrails、Tracing。
>      作者认为这套最小核心兼顾了易用与控制力。
>   3. 为什么比“手搓 Agent”更实用
>      SDK 自动处理循环执行、工具调用、结果回注、结束条件，减少大量样板代码；开发者更聚焦业务逻辑。
>   4. 多 Agent 协作价值
>      通过 handoff 把任务分发给专长 Agent，适合客服、研究、内容生成、销售流程等协同场景。
>   5. 可观测性是生产关键
>      Tracing/Span 级别监控可看清每一步调用与输入输出，便于排错、性能优化和评估。
>   6. 与 LangChain 对比
>      作者观点是：LangChain 生态更大但抽象更重；Agents SDK 抽象更轻、流程更透明，适合追求可控和生产监控的团队。也可能出现
>      混合方案（如 SDK + LangGraph）。
>   7. 与 Auto-GPT/BabyAGI 对比
>      早期自治 Agent 展示了潜力，但常见问题是循环失控、成本高、难调试。Agents SDK 用结构化函数调用 + guardrails + tracing
>      提高可控性和稳定性。
>   8. 生态影响判断
>      作者预测 Agents SDK 可能推动行业标准化，并迫使其他框架与云厂商重新定位（跟进或差异化）。
>
>   一句话结论
>   这篇文把 Agents SDK 视为“从 demo 到生产”的分水岭：不是功能最多，但在工程可控性和落地效率上更接近企业需要。

开发者对 OpenAI Agents SDK 的“简洁且强大”给出了很高评价。以下是社区反馈摘要：

- **易用性与 Python-First 路线：**  
  很多开发者认为这个 SDK 抽象很少，而且专为 Python 设计。这意味着你可以快速搭建 Agent、定义工具、编排流程，而不会被复杂学习成本拖慢。很多教程和入门文章都提到：它让复杂的多 Agent 场景变得“开箱即用”。  


- **更顺畅的多 Agent 工作流：**  
  开发者对内置 handoff 与 tracing 功能非常认可。相比过去更手工的方案，现在任务可以在专业 Agent 间无缝传递，并且可以可视化追踪和调试，体验提升明显。  
  
- **社区与开源采用：**  
  GitHub 仓库已有接近 2,000 个 star 和大量 fork，说明社区兴趣和参与度较高。用户持续分享案例、提交问题、提出改进建议，这说明 SDK 既有实际价值，也在根据真实需求快速演进。  


- **真实业务影响：**  
  不止个人项目，企业层面的反馈（例如 Box 等公司）也显示：当 SDK 与 Web 搜索、文件搜索等能力结合时，更容易把企业内部数据与实时外部信息整合起来。这种整体能力被认为是构建真正自主 AI 系统的关键。  

总体而言，开发者和早期采用者对该 SDK 持非常积极态度：它减少了手工提示词工程工作量，提升了 Agent 自主性，并通过 tracing 提供了清晰、可操作的反馈。社区热度与企业兴趣的持续增长，也表明它有潜力成为下一代 AI 应用的重要基础设施。



## Agent开发指引

本节基于 [a-practical-guide-to-building-agents](./a-practical-guide-to-building-agents.pdf )的核心内容。Agent 不是“会聊天的 LLM”，而是“能在护栏内自主完成多步工作流”的系统；落地成功关键是：**先单体、后多体，先可用、再优化，先安全、再放权**。

**1)  先判断该不该做 Agent（立项门槛）**，只在这 3 类场景优先做：

1. 流程复杂且有大量例外判断（规则引擎难覆盖）。
2. 现有规则系统维护成本高、改动慢。
3. 强依赖非结构化信息（文本、文档、对话）。

如果你的流程是稳定、规则清晰、可穷举，优先用确定性自动化，不要上 Agent。

**2)  最小可行架构（MVP）**， 先只做三件事：

1. Model：先用最强模型打基线。
2. Tools：只接 3-5 个高价值工具（查数据、执行动作、必要时调用其他 agent）。
3. Instructions：把 SOP/知识库改写成编号步骤，且每步都对应明确动作。
   

**3) 指令设计（最容易被忽略）**，写指令时强制包含：

1. 目标和完成条件（何时算完成，何时停止并交还用户）。
2. 标准步骤（按序执行）。
3. 分支处理（信息缺失、用户跑题、工具失败时怎么做）。
4. 输出格式（结构化字段，便于评测和审计）。

**4) 编排策略（避免一上来就过度设计）**， 按这个顺序演进：

1. 单 Agent + 工具循环（默认方案）。
2. 当提示词分支过多或工具高度重叠导致误调用时，再拆多 Agent。
3. 多 Agent 两种模式：
    - Manager 模式：一个总控调度专用 agent（适合统一对外体验）。
    - Decentralized 模式：agent 间直接 handoff（适合客服分诊等场景）。

**5) Guardrails（上线必备）**，至少分层做这几类：

1. 相关性检查（防跑题）。
2. 安全检查（防注入/越狱）。
3. PII 过滤（防泄露）。
4. Moderation（有害内容拦截）。
5. 工具风险分级（高风险动作前加人工确认）。
6. 规则层（正则、黑名单、长度限制）。
7. 输出校验（品牌和合规约束）。

**6) Human-in-the-loop（必须提前设计）**，两类情况直接转人工：

1. 连续失败超过阈值（比如重试 2-3 次仍失败）。
2. 高风险/不可逆动作（退款、支付、取消订单、写入关键系统）。

**7) 你的落地执行清单（可直接用）**

1. 选 1 个高价值但可控的流程（如“订单查询+退款申请”）。
2. 定义成功指标：任务完成率、人工接管率、平均时长、错误率、单次成本。
3. 用最强模型做基线版本并跑评测集。
4. 逐步替换部分环节为小模型，观察指标不退化再保留。
5. 上线前接入最小护栏集（相关性+安全+高风险人工确认）。
6. 小流量灰度，记录失败案例，每周迭代指令和护栏。
7. 指标稳定后再考虑拆分多 Agent。

**8) 常见失败点（提前规避）**

1. 过早多 Agent 化，复杂度暴涨。
2. 工具定义模糊，导致误调用。
3. 没有明确“停止条件”和“交还控制条件”。
4. 护栏只做一层，未做分层防御。
5. 没有失败闭环（日志、评测、复盘、再训练/改提示）。
