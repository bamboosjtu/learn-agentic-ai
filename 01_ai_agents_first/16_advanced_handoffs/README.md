# Advanced Handoffs MasterClass

你已经学会了如何把对话从一个智能体转交给另一个智能体。现在要做的是把它升级成“VIP 转接”：下一个智能体不只是接手，还会收到完整的背景说明，知道该做什么，并且只看到与任务相关的信息。

> 核心思路：高级 handoff 不只是“路由”，而是一次干净、智能、上下文丰富的专家交接。

### 本节会掌握什么

* **自定义 handoff**：如何修改 handoff 在 LLM 看来对应的工具名和描述？如何在 handoff 触发瞬间执行代码？
* **传递结构化数据**：如何让第一个智能体把一份详细“简报”通过结构化数据传给下一个智能体？
* **控制叙事上下文**：如何在下一个智能体接手前清理对话历史，避免无关的工具调用让它困惑？
* **提升可靠性**：怎样写 prompt，才能让智能体知道什么时候该 handoff、又该如何正确 handoff？
* **管理多轮对话**：发生 handoff 后，如何确保用户下一轮继续跟正确的专家智能体交流？

---

## 第一部分：自定义并传递数据

基础 handoff 像“盲转接”，高级 handoff 则像附带了一份详细转接说明。你可以自定义 handoff 在 LLM 眼中的样子，并同时传递关键数据。

### 自定义工具并添加回调

```python
from agents import Agent, handoff, RunContextWrapper

def log_handoff_event(ctx: RunContextWrapper):
    print(f"HANDOFF INITIATED: Transferring to the Escalation Agent at {ctx.current_timestamp_ms}")

specialist = Agent(name="Escalation Agent")
custom_handoff = handoff(
    agent=specialist,
    tool_name_override="escalate_to_specialist",
    tool_description_override="Use this for complex issues that require a specialist.",
    on_handoff=log_handoff_event,
)
```

### 使用 `input_type` 传递结构化数据

```python
from pydantic import BaseModel

class EscalationData(BaseModel):
    reason: str
    order_id: str

async def on_escalation(ctx: RunContextWrapper, input_data: EscalationData):
    print(f"Escalating order {input_data.order_id} because: {input_data.reason}")

escalation_agent = Agent(name="Escalation agent")
escalation_handoff = handoff(
    agent=escalation_agent,
    on_handoff=on_escalation,
    input_type=EscalationData,
)
```

---

## 第二部分：过滤对话历史

默认情况下，新智能体会看到完整对话历史，包括之前所有工具调用。这可能很吵。你可以通过 `input_filter` 在交接时清理这些信息。

```python
from agents.extensions import handoff_filters

faq_agent = Agent(name="FAQ agent")
faq_handoff = handoff(
    agent=faq_agent,
    input_filter=handoff_filters.remove_all_tools,
)
```

---

## 第三部分：管理整段对话

### 用 prompt 提高成功率

```python
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

triage_agent = Agent(
    name="Triage Agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    Your primary job is to diagnose the user's problem.
    If it is about billing, handoff to the Billing Agent.
    If it is about refunds, handoff to the Refund Agent."""
)
```

### 让专家继续后续对话

```python
# Turn 1: Triage hands off to the Refunds specialist
result1 = await Runner.run(triage_agent, "I need a refund for order #123.")
print(f"Reply from: {result1.last_agent.name}")
print(f"Message: {result1.final_output}")

# The user replies: "Thanks, how long will it take?"
follow_up_message = {"role": "user", "content": "Thanks, how long will it take?"}

# CONTINUE WITH THE SPECIALIST
specialist = result1.last_agent
follow_up_input = result1.to_input_list() + [follow_up_message]

result2 = await Runner.run(specialist, follow_up_input)
print(f"Reply from: {result2.last_agent.name}")
print(f"Message: {result2.final_output}")
```

---

## 什么时候优先用 handoffs，什么时候优先用 agents-as-tools

- **Handoffs**：适合长对话、专业性强的场景，让另一个智能体真正拥有这段对话。
- **Agents-as-tools**：适合快速、局部的能力借用，主智能体继续掌控对话。

---

## 常见问题与防护建议

- 在 prompt 里把路由规则写明确。
- 如有必要，在交接前清理历史。
- 如果希望继续由同一个专家处理后续消息，记得保留 `result.last_agent`。

---

## 动手实验：一个小型 Lab

```python
from agents import Agent, Runner, handoff, RunContextWrapper
from agents.extensions import handoff_filters
from pydantic import BaseModel
import asyncio

# --- Define the data for our "briefing note" ---
class HandoffData(BaseModel):
    summary: str

# --- Define our specialist agents ---
billing_agent = Agent(name="Billing Agent", instructions="Handle billing questions.")
technical_agent = Agent(name="Technical Support Agent", instructions="Troubleshoot technical issues.")

# --- Define our on_handoff callback ---
def log_the_handoff(ctx: RunContextWrapper, input_data: HandoffData):
    print(f"\n[SYSTEM: Handoff initiated. Briefing: '{input_data.summary}']\n")

# --- TODO 1: Create the advanced handoffs ---
to_billing_handoff = handoff(
    # Your code here
)

to_technical_handoff = handoff(
    # Your code here
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="First, use the 'diagnose' tool. Then, based on the issue, handoff to the correct specialist with a summary.",
    tools=[
        function_tool(lambda: "The user's payment failed.")("diagnose")
    ],
    handoffs=[to_billing_handoff, to_technical_handoff],
)


async def main():
    print("--- Running Scenario: Billing Issue ---")
    result = await Runner.run(triage_agent, "My payment won't go through.")
    print(f"Final Reply From: {result.last_agent.name}")
    print(f"Final Message: {result.final_output}")

# asyncio.run(main())
```

#### 预期结果

1. 一条系统日志，显示 handoff 已发生，并附带类似 “User's payment failed.” 的摘要。
2. 最终回复来自 `"Billing Agent"`。

---

## 总结

* **它是什么**：一组强大的控制能力，用来管理智能体之间的对话转交。
* **什么时候用**：构建需要明确角色分工、上下文传递和干净对话流的多智能体系统时。
* **怎么做**：使用 `handoff()` 自定义 `tool_name`，在 `on_handoff` 中触发逻辑，用 `input_type` 传结构化数据，用 `input_filter` 清理历史。
---

## 补充： Handoff 的高级用法

说明：下面内容基于当前目录中的 `01_handoff_obj.py`、`02_handsoff_callbacks.py`、`03_handoff_dynamic_permission.py`、`03_input_filters.py`、`04_is_enabled.py` 做补充总结。这里只做追加，不覆盖本 README 现有内容。

### 1. Handoff 不只是“转给别人”，还可以被建模成一个可配置对象

`01_handoff_obj.py` 的重点不是简单把 `NewsAgent` 挂到 `WeatherAgent` 上，而是把 handoff 当成一个显式对象来配置：

* 交给哪个目标 Agent
* 何时触发
* 触发时是否执行额外逻辑

这一层抽象的意义在于，handoff 不再只是“从 A 切到 B”，而是变成一个带策略的路由节点。真实项目里，这让你可以把“是否该转交”“转交给谁”“转交时做什么”拆开管理。

虽然这个示例文件本身还没写完整，但它已经表达了一个关键方向：

* handoff 可以像 tool 一样被显式配置
* handoff 不是硬编码跳转，而是 Agent 能调用的受控能力

### 2. `on_handoff` 让交接点具备可观测性和副作用能力

`02_handsoff_callbacks.py` 展示了 handoff 的第一个高级扩展点：`on_handoff`。

示例里定义了：

* `NewsRequest`
* `on_news_transfer(ctx, input_data)`
* `handoff(agent=news_agent, on_handoff=on_news_transfer, input_type=NewsRequest)`

这意味着 handoff 发生时，你可以：

* 记录审计日志
* 上报监控事件
* 写入数据库或消息队列
* 做权限复核
* 在交接瞬间执行同步或异步副作用

这类能力很适合高价值流程，例如：

* 升级到人工客服前记录原因
* 转给高权限专家前保留审计痕迹
* 跨子系统交接时写入事件流

核心点不是“能打印日志”，而是 handoff 本身变成了一个可插入治理逻辑的生命周期节点。

### 3. `input_type` 可以把“交接说明”结构化，而不是只靠自然语言猜

还是在 `02_handsoff_callbacks.py` 里，`NewsRequest(BaseModel)` 是另一个高级点。

它说明 handoff 时不仅能把对话历史交给下一个 Agent，还能额外传一份结构化 briefing，例如：

* `topic`
* `reason`

这样做的价值很直接：

* 上游 Agent 不需要把所有背景都塞进 prompt 文本
* 下游 Agent 接收到的是清晰、可校验的数据结构
* 交接协议更稳定，减少 LLM 在 handoff 参数上的自由发挥

在真实系统里，`input_type` 很适合承载：

* 工单摘要
* 升级原因
* 用户身份标签
* 风险等级
* 待处理对象 ID

所以高级 handoff 的一个核心思想是：不仅要“转过去”，还要“带着结构化交接单转过去”。

### 4. `input_filter` 可以清洗交接上下文，避免下游 Agent 看到一堆噪音

`03_input_filters.py` 展示了 handoff 的另一个关键能力：交接前重写输入。

示例里定义了：

* `summarized_news_transfer(data: HandoffInputData) -> HandoffInputData`

然后在 handoff 中使用：

* `input_filter=summarized_news_transfer`

这个模式非常重要，因为默认情况下，下游 Agent 往往会看到完整对话、之前的工具调用和中间状态。对复杂多 Agent 流程来说，这经常是负担，而不是帮助。

这个示例做了三件很典型的事：

* 把完整历史压缩成一句摘要：`Get latest tech news.`
* 清空 `pre_handoff_items`
* 清空 `new_items`

换句话说，它把“原始上下文”重写成“最适合下游 Agent 接手的上下文”。

这在工程里很有价值，常见用途包括：

* 隐藏上游工具链细节
* 降低 token 消耗
* 避免下游 Agent 被之前的错误尝试污染
* 去掉和目标专家无关的历史
* 做隐私或敏感字段脱敏

如果说 `input_type` 负责补充结构化信息，那么 `input_filter` 负责清理和重塑原始历史。

### 5. `handoff(..., is_enabled=...)` 可以做动态交接权限控制

`03_handoff_dynamic_permission.py` 和 `04_is_enabled.py` 都在演示 handoff 级别的动态开关。

这说明 `is_enabled` 不只是 tools 能用，handoffs 也能用。

**`03_handoff_dynamic_permission.py` 的重点**

这里直接把 handoff 绑定到：

* `ctx.context.has_permission`

也就是说，是否允许用户把问题升级给 `Expert`，取决于运行时上下文，而不是写死在 Agent 定义里。

这适合：

* 某些用户不能访问专家 Agent
* 某些租户不能触发高成本 handoff
* 某些敏感领域必须先通过权限校验

**`04_is_enabled.py` 的重点**

这个文件进一步把动态控制做成“带参数的策略工厂”：

* `news_region(region: str)`
* 内部返回 `is_news_allowed(ctx, agent)`

然后 handoff 只有在：

* `ctx.context.get("is_admin", False)` 为真
* 并且 region 为 `"us-east-1"`

时才可用。

这比单纯检查一个布尔值更接近真实生产逻辑。因为真实系统的 handoff 开放条件通常是多维的：

* 用户角色
* 地域
* 合规区域
* 套餐等级
* 运行环境
* 负载状态

结论很明确：如果 handoff 本身有权限或环境依赖，优先在 `is_enabled` 层面控制，不要等模型选中了再事后拦截。

### 6. `RECOMMENDED_PROMPT_PREFIX` 用来强化 Agent 对 handoff 规则的遵守

`04_is_enabled.py` 还展示了另一个经常被忽视的点：

* handoff 是否发生，最终依然是模型决策的一部分

文件里通过：

* `RECOMMENDED_PROMPT_PREFIX`

把推荐的 handoff 提示前缀注入到了 `WeatherAgent.instructions` 中。

这说明高级 handoff 不只是 API 配置问题，也包含 prompt 工程问题。你需要明确告诉路由 Agent：

* 什么时候应该自己回答
* 什么时候应该转给别的 Agent
* 转交后由谁继续负责

如果 prompt 写得弱，模型就可能：

* 明明该 handoff 却没 handoff
* 明明该交给 A 却交给 B
* 或者自己胡乱回答，不走路由

所以 handoff 的稳定性通常依赖两部分：

* SDK 层配置：`handoffs=[...]`
* 语义层约束：清晰的 `instructions`

### 7. 一个 Agent 可以同时拥有多个 handoff，形成受控路由网络

`04_is_enabled.py` 里，`weather_agent` 同时挂了两个 handoff：

* 到 `news_agent`
* 到 `planner_agent`

这说明 handoff 的高级用法不是“一对一转交”，而是让一个 Agent 充当路由器或分诊台。

这种模式适合：

* Triage Agent 分诊
* 业务入口 Agent 做专家路由
* 一个通用助手把请求转给不同垂直 Agent

而且由于其中某些 handoff 还可以动态启用/禁用，所以你得到的是一个“按上下文变化的路由图”，而不是静态拓扑。

### 8. `result.last_agent` 是多 Agent 连续对话里最关键的状态

虽然本目录 README 里已经提到过这个概念，但结合这些 `.py` 文件可以更明确地总结：

handoff 成功后，你不能只看 `final_output`，还应该看：

* `result.last_agent`
* `result.new_items`

尤其是：

* `result.last_agent` 告诉你最终由哪个 Agent 接手并完成回复
* `result.new_items` 能帮助你排查 handoff 是否真正发生，以及 handoff 后经历了哪些新事件

对多轮对话系统来说，`result.last_agent` 很重要，因为后续用户消息应该继续发给当前接手的专家 Agent，而不是永远重新回到入口 Agent。

### 9.  Handoff 四个高级控制面

把这些示例放在一起看，handoff 的高级能力大致可以分成四层：

* 路由定义：把 handoff 建模成显式对象，而不是隐式跳转
* 交接治理：`on_handoff` 用于审计、日志和副作用
* 上下文工程：`input_type` 补充结构化 briefing，`input_filter` 清洗历史
* 动态开放策略：`is_enabled` 根据权限、地区、角色或环境控制 handoff 可见性

对应到真实项目，基本就是四个问题：

* 该不该转
* 转给谁
* 转过去时带什么
* 什么人、什么条件下允许转

### 10. 实战建议

基于本目录这些 handoff 示例，落地时建议按这个顺序设计：

1. 先定义入口 Agent 和专家 Agent 的职责边界，避免路由含糊。
2. 用清晰的 instructions 或推荐 prompt 前缀，让模型知道何时必须 handoff。
3. 对关键 handoff 定义 `input_type`，把交接内容结构化。
4. 对复杂链路加 `on_handoff`，做日志、审计或事件上报。
5. 对敏感 handoff 使用 `is_enabled`，不要等 handoff 发生后再拒绝。
6. 对长链路使用 `input_filter` 清洗历史，避免上下文污染。
7. 调试时同时看 `final_output`、`result.last_agent`、`result.new_items`，不要只看回复文本。

这几项一起用，handoff 才会从“能转交”升级为“可控、可审计、可扩展的多 Agent 交接机制”。
