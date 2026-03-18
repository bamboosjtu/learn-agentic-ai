# 面向开发者的 Agentic Payments 与 Agentic Economy 教程

## 引言

人工智能（AI）正在逐步融入经济系统，并推动一个新的变革时代，而其中最前沿的两个概念就是 **Agentic Payments（Agent 支付）** 和 **Agentic Economy（Agent 经济）**。Agentic Payments 让 AI Agent 能够自主处理支付流程，从而简化商业交易并提升用户体验。与此同时，Agentic Economy 描绘的是这样一种未来：AI Agent 将成为经济活动中的活跃参与者，从购买商品到协商合同，都可以由它们完成。

这篇教程面向 Agent 开发者，目标是帮助你理解这些概念，并学会如何借助 Stripe 的工具来实现 Agentic Payments，尤其是 **Stripe Agent Toolkit** 和 **Model Context Protocol（MCP）**。

我们会先从 Agentic Payments 和 Agentic Economy 的理论基础讲起，分析它们的影响与生态；然后再给出使用 Stripe 工具实现 Agentic Payments 的实操指导，并附带代码示例。读完后，你应当能够同时掌握这些概念的背景和构建 Agent 支付系统所需的技术路径。

## 第一部分：理解 Agentic Payments

### 什么是 Agentic Payments？

Agentic Payments 代表了一种支付处理范式的变化：AI Agent 会代表用户自主执行交易。传统支付系统通常要求用户在结账阶段亲自完成操作，而 Agentic Payments 则让购物流程可以实现从头到尾的自动化。这也是 **Agentic Commerce（Agent 驱动商业）** 的关键组成部分，在这种模式下，AI Agent 可以负责如下任务：

- 根据用户偏好搜索商品或服务
- 比较不同商家的价格
- 发起并完成购买
- 管理订阅或周期性付款

例如，一个 AI Agent 可以自动帮用户预订机票：先搜索多个方案，选出最匹配的选项，再完成支付，而整个过程中只需要极少的用户输入。要做到这一点，就需要把支付 API 与 AI Agent 框架集成起来，让 Agent 能够安全地与金融系统交互。

### 行业进展

主要支付厂商都在积极布局 Agentic Payments：

- **Mastercard**：推出了 **Agent Pay**，并与 Microsoft 等 AI 平台集成，以支持 Agentic Commerce。它通过 **Mastercard Agentic Tokens** 来保障交易安全。
- **Visa**：推出了 **Visa Intelligent Commerce**，为 AI Agent 管理购物和支付提供框架。
- **PayPal**：发布了让 AI Agent 自主完成交易的工具，减少用户亲自参与支付流程的需要。
- **Stripe**：提供了 **Stripe Agent Toolkit**，这是一个可将 Stripe 支付 API 接入 AI Agent 框架的库，支持 OpenAI Agent SDK、LangChain、CrewAI 等生态。

这些进展说明，整个行业已经开始围绕 Agentic Payments 建立基础设施，不同公司则从各自角度提供了推动 AI 商业化落地的工具。

### Agentic Payments 的关键特征

| 特性 | 说明 |
|------|------|
| **自主性（Autonomy）** | AI Agent 可以基于用户预先设定的偏好或提示词，在无人干预的情况下执行交易。 |
| **安全性（Security）** | 通过支付令牌，例如虚拟信用卡，保障交易安全，并与用户原始支付方式绑定。 |
| **个性化（Personalization）** | Agent 可以根据预算、品牌偏好等信息定制购买行为，提升购物体验。 |
| **可扩展性（Scalability）** | Agent 系统可以处理大规模交易，适合企业或平台级场景。 |

### 挑战与注意事项

虽然 Agentic Payments 优势明显，但也面临现实挑战：

- **安全与信任**：必须确保 AI Agent 在获得用户授权的前提下安全地处理支付。例如 Stripe 的工具包会使用一次性虚拟借记卡来提高安全性。
- **反欺诈**：Bot 驱动商业的兴起，也会带来更多欺诈风险，因此需要更强的防护机制。
- **用户接受度**：让用户放心把金融交易交给 AI Agent，需要时间，也需要在产品设计上建立足够信任。

## 第二部分：Agentic Economy

**Agentic Economy** 是一种新兴经济系统，在这个系统里，AI Agent 会作为消费者、生产者和中介角色参与经济活动。这不仅仅局限于支付，还包括交易、协商、生成新产品或服务等更广泛的经济行为。

### 核心特征

- **自主交易**：AI Agent 可以独立买卖商品和服务，降低消费者与企业之间的沟通摩擦。
- **市场重组**：通过自动化交互，Agent 系统可能重塑市场结构、重新分配权力并催生新的经济模型。
- **创新能力**：Agent 间的程序化协作，可以推动面向用户需求的新产品和新服务出现。

### 对未来的影响

相关研究表明，Agentic Economy 可能带来深远影响：

- **效率提升**：AI Agent 最多可以自动化完成约 70% 的办公室任务，大幅提高生产率。
- **新商业模式**：企业可以把预算从传统人力和软件采购，逐步转移到 Agent 驱动的新型服务与工作流上。
- **社会与经济挑战**：大量劳动密集型任务被自动化，也会带来岗位替代、隐私风险和市场波动等问题，因此需要更健全的治理框架。

### 理论基础

一些资源对 Agentic Economy 提供了更深入的理论视角：

- **《The Agentic Economy: How Billions of AI Agents Will Transform Our World》**，作者 Kye Gomez：设想了大量智能 Agent 将如何改变商业和日常生活。
- **《A-Commerce Is Coming: Agentic AI And The ‘Do It For Me’ Economy》**，作者 David G.W. Birch：讨论了 AI 驱动商业及其经济影响。
- **《The Agentic Economy》**，作者 David M. Rothschild 等（arXiv 论文）：分析了 AI Agent 如何减少沟通摩擦并重组市场。

### 生态与交叉趋势

Agentic Economy 与多种技术趋势交汇：

- **生成式 AI（Generative AI）**：为基于用户提示生成内容和辅助决策提供基础。
- **Agentic AI**：强调自主决策与任务执行，这也是它区别于纯响应式生成式 AI 的关键。
- **可编程支付（Programmable Payments）**：类似 Stripe 这样的支付系统支持自动化，并可集成进 AI 驱动工作流。

### 从 API Economy 走向 Agentic Economy

从 API 经济转向 Agent 经济，不是渐进式优化，而是范式转移。API Economy 的重点是连接不同系统和服务，而 Agentic Economy 的核心则是让自主、智能的 Agent 自己去完成目标。

下面是两者的区别：

### API Economy：连接器的世界

API Economy 建立在应用程序编程接口（API）之上。API 是一套规则和协议，允许不同软件系统彼此通信和共享数据。它一直是现代数字化转型的重要基础，让企业可以通过接入其他系统能力来快速构建新产品和服务。

API Economy 的关键特点包括：

* **以人为中心的编排**：由开发者或预先定义的系统来控制 API 调用流程。开发者写代码调用一个 API、处理返回值，再调用另一个 API，逻辑和工作流都由人明确定义。
* **被动端点**：API 本质上是被动响应式接口。它们等待请求，再返回结果，不具备自主决策、规划或主动发起动作的能力。
* **定义明确的交互**：应用之间的交互通常是固定且明确的。API 契约规定了可以发送什么数据，以及会返回什么数据。
* **关注连接性**：API Economy 的主要价值在于实现系统之间的无缝集成与互操作。

现实中的 API Economy 例子到处都是：Uber 用 Google Maps API 显示实时位置，Stripe 通过 API 提供支付处理，大量应用使用社交媒体 API 来实现登录和数据共享。

### Agentic Economy：自主行为体的世界

相比之下，Agentic Economy 是一种正在形成中的新模型，在这个模型中，AI Agent，而不是人类预先设计死的系统，成为经济活动的主要驱动力。这些 Agent 不再只是被动接口，而是主动、目标导向并具备独立行动能力的“参与者”。

Agentic Economy 的关键特点包括：

* **自主且主动的行为**：Agent 能感知环境、推理当前情境、规划行动路径，并在不需要每一步都由人类显式指挥的情况下执行任务。它们不会只是等命令，而是会为了达成目标主动采取行动。
* **以目标为驱动的执行**：用户只需要给出高层目标，例如“帮我预订商务出差的机票和酒店”，Agent 就可以把任务拆成多个小步骤，和不同服务交互，并处理过程中出现的意外情况。
* **动态且自适应的交互**：不同于 API 的刚性契约，Agent 可以根据实时数据和新信息不断调整行为。它们可以即时决策，并随时修改原定计划。
* **关注价值创造**：Agentic Economy 的价值，不只是让系统连接起来，而是通过自动化整个工作流来创造新的价值，并产出原本需要大量人工才能完成的结果。

在 Agentic Economy 中，AI Agent 不仅会使用 API，它们还可能自己成为服务的消费者，甚至是服务的创造者。你可以想象一个未来：个人 AI 助手会自动帮你寻找最优报价、完成下单、处理支付，而且整个过程都是通过与其他商业 Agent 交互完成的。

### 过渡过程：API 将成为 Agent 的工具

Agentic Economy 并不会消灭 API Economy，而是在其基础上演化。API 依然会很重要，只是它们会变成 AI Agent 与外部世界交互的“工具”或“肢体”。真正改变的，是 API 的使用方式。

未来不再是开发者手写一串 API 调用来完成业务流程，而是 AI Agent 会主动组合多种 API 来实现自己的目标。这就要求出现适合 Agent-to-Agent 通信的新型 API 和协议，包括：

* **标准化协议**：让 Agent 能够无需做大量定制集成，就能发现并调用彼此的能力。
* **更强的安全与信任**：由于 Agent 能够自主决策和交易，因此必须有强健的身份验证机制（例如 Know Your Agent，KYA）以及可审计的行为轨迹。
* **更灵活的接口**：未来的 API 需要支持迭代式交互和更复杂、更具上下文感知的流程，而不是局限于简单的一问一答式请求响应模型。

从本质上看，Agentic Economy 把关注点从“我怎样把这个服务和那个服务连起来？”转向“我怎样让一个智能 Agent 能够利用多种服务去完成复杂目标？”。这代表着从人工编排世界，走向自主且智能的价值创造世界。

## Agentic Economy 总结：下一代数字范式

从 API Economy 走向 Agentic Economy，意味着数字系统交互与价值创造方式的根本变化。可以从以下角度来理解：

## 从 API 到 Agent

**API Economy 的特点：**

- 静态、预定义接口，需要显式编程
- 由人类编写代码连接不同服务
- 功能固定，API 只执行它被设计要做的事
- 集成与编排依赖人工完成
- 价值主要来自人类主导的数据交换

**Agentic Economy 的特点：**

- 自主 Agent 能推理、规划并执行任务
- Agent 之间可以在极少人工干预下协作与协商
- 能动态解决问题并适应新情况
- 可以形成自组织的智能 Agent 网络
- 价值来自 Agent-to-Agent 的互动与决策

## 关键变化

**1. 从 Integration 走向 Collaboration**

过去需要开发者手动串联不同 API；未来则是 Agent 自动发现其他 Agent 并协同工作。比如一个旅行 Agent 可以自己和航司 Agent、酒店 Agent、活动预订 Agent 协商，完成整个出行安排。

**2. 从 Requests 走向 Goals**

过去是精确调用 API，例如“先调用天气 API，再调用日历 API，最后发邮件”；未来则是直接给 Agent 一个高层目标，例如“帮我把这一周安排得更高效”，Agent 自己拆解并执行。

**3. 从 Static 走向 Adaptive**

相比固定功能的 API 端点，Agent 可以不断学习、调整策略，并随着时间获得新的能力。

**4. 新的经济模型**

- Agent 可以使用数字货币或令牌为其他 Agent 支付服务费用
- 可以建立 Agent 的信誉系统，用来衡量可靠性与服务质量
- 形成 Agent 市场，让不同 Agent 在竞争中不断专业化
- 通过 Agent 的创造力和问题解决能力，催生新的价值模式

## 影响

这可能会催生更流动、更高效的市场：大量日常交易、协商和优化工作由 Agent 处理，而人类则更多关注高层策略与创造性工作。但这同样会带来控制权、透明性以及如何确保 Agent 行为符合人类价值等问题。

## 第三部分：用 Stripe 实现 Agentic Payments

<https://docs.stripe.com/mcp>

<https://docs.stripe.com/agents>

### 第四部分：串联起来看，一个示例架构

下面用一个实际的例子来理解基于 Stripe 的 Agentic Payment 架构。假设你正在构建一个 **“AutoBuy Assistant”**，它是一个在家用品快用完时自动下单补货的 AI 服务，也就是一个个人购物 Agent。

整个系统可能是这样运作的：

* **Agent 大脑（Agent Brain）**：核心 AI（可以是托管 LLM，也可以是自定义模型）监控库存水平，例如通过 IoT 设备或用户输入。当它判断某个商品需要补货时，就会制定执行计划。
* **MCP 接口（MCP Interface）**：Agent 连接到 Stripe MCP 服务器（可以是 Stripe 的云端端点，也可以是你自己部署的），以访问商业相关工具。它也可能同时连接到其他 MCP 服务器，例如某家超市的 API。
* **发起订单（Initiating Order）**：Agent 使用 Stripe 的 **Order Intent**（如果可用）发起订单，提供商品 ID、数量、收货地址等信息。Stripe 通过用户在 Stripe Customer 中保存的银行卡完成支付，并同步把订单发送给商家履约。如果 Order Intents 还不可用，则 Agent 会改用 Stripe Issuing 虚拟卡在商家网站上支付，并自动填写结账表单中的收货信息和卡号。
* **授权与支付（Authorization & Payment）**：如果使用的是虚拟卡，Stripe Issuing 平台会收到扣款请求。你的后端系统（或 Stripe 规则）会自动批准交易，因为它识别出商家和金额与 Agent 的购买意图一致。然后扣款成功，从你的账户余额或指定资金来源中扣除。如果使用的是 Order Intents，则其中的 Payment Intent 会被确认，并通过 Stripe 向用户银行卡扣款，全程无需人工参与。
* **交易后处理（Post-Transaction）**：Stripe 会发送支付成功的 webhook。你的系统记录这次交易，并触发 Agent 发送通知，例如：“我已经下单了 5 包咖啡，总价 30 美元，预计周五送达。” 如果使用了 Stripe 的 Order API，系统还可以将物流信息或订单状态同步给 Agent，再由它转告用户。
* **学习与反馈（Learning and Feedback）**：例如，Agent 还可以记录订单是否按时到达，并据此更新自己的知识。这部分不属于 Stripe 本身的能力范围，但对 Agent 的持续优化非常关键。

从开发者角度看，这条流程中大量工作都由 Stripe 基础设施承担，例如创建订单或支付、处理资金流、保障税务与收据合规，以及提供控制点（webhook 供你介入、dashboard 供你查看活动）。你真正需要重点设计的，是 Agent 的决策逻辑，以及如何把 Stripe 工具正确接入。Stripe 的文档和 quickstart 示例可以提供很大帮助，可以参考官方的 **Agent Quickstart** 与样例应用。

## 结论与下一步

Agentic Payments 以及更广义的 Agentic Economy，正在快速从概念走向实践。上面已经介绍了：自主 Agent 如何借助 MCP 这类协议来发起并完成交易，以及 Stripe 的 Agent Toolkit 如何成为当前可落地的一套实现路径。

对开发者来说，现在正是试验这些概念的合适时机。你可以从一个很小的场景开始，例如：

- 构建一个聊天机器人，在用户提出请求时自动创建 Stripe Payment Link
- 构建一个 AI 系统，监控 SaaS 使用量，并在超过阈值时通过 Stripe Billing 自动计费

在每一步里，都必须优先考虑安全性和用户信任。

继续深入的最佳入口，仍然是 **Stripe 官方资源**：

- [Stripe Agent Toolkit on GitHub](https://github.com/stripe/agent-toolkit)
- Stripe 文档中的 **Agent Quickstart**
- 关于 **Order Intents** 和其他 Beta API 的官方参考文档

由于很多功能还处在预览阶段，你可能需要申请抢先体验权限，例如测试 Order Intents。

最后，也要持续关注整个生态中 Agentic Payments 的演进。随着越来越多开发者开始构建 Agent 驱动应用，标准会不断成熟，最佳实践也会逐步形成。理解这些基础概念，并建立在 Stripe 这样稳健的平台之上，你就更有能力构建下一代商业应用：在这些应用里，**AI Agent 能够无缝完成交易**，推动一个新的自主、去中心化经济交互时代的到来，让商业真正以*算法速度*运行。

**参考说明：** 本文讨论的概念与实现，主要参考了 Stripe 官方文档以及业内对 Agentic Commerce 的可靠分析，包括 Stripe 关于 agentic retail 的指南、Stripe 开发者文档中关于 Agent Toolkit 与 MCP 的说明，以及围绕 Agentic Economy 的专家解读。它们共同构成了本教程的理论与实践基础。
