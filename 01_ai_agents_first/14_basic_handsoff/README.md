# Handoffs

**Handoff** 指的是：当前智能体把控制权转交给另一个更专业的智能体，由对方继续完成当前任务，或者接着处理后续对话。在 SDK 中，handoff 会以工具的形式暴露给 LLM（例如 `transfer_to_refund_agent`）。当你希望某个专家智能体接管并继续和用户对话时，就适合使用 handoff。

---

## 为什么需要 handoffs？

当一个问题的不同部分适合由不同专家处理时，例如计费、退款、常见问题、研究等，handoff 可以让你在合适时机把对话路由到最合适的智能体。典型例子就是客服系统：一个分诊智能体把对话转交给“订单状态”“退款”或“FAQ”智能体。

**心智模型（类比）：**

- *Agents-as-tools* = 你还拿着麦克风，只是暂时问同事一句。
- **Handoff** = 你把电话转接给同事，由他们继续和用户对话。

底层实现上，runner loop 会直接切换“当前智能体”，然后从新智能体继续执行。

---

## SDK 中会用到的核心组件

- **`Agent.handoffs`**：当前智能体可转交到的目标智能体列表（或 `handoff(...)` 对象）。
- **`handoff(...)`**：用来定制 handoff，例如自定义工具名/描述、添加 `on_handoff` 回调、用 `input_type` 接收结构化输入，或通过 `input_filter` 修改历史消息。
- **Handoff 本质上是工具**：LLM 会把它视作一个类似 `transfer_to_<agent_name>` 的工具。

---

## 最小示例：分诊后转交

真实场景：一个 “Triage Agent” 判断要不要转交给 **Billing** 或 **Refunds**。

```python
from agents import Agent, Runner, handoff
import asyncio

billing_agent = Agent(name="Billing agent", instructions="Handle billing questions.")
refund_agent  = Agent(name="Refund agent",  instructions="Handle refunds.")

triage_agent = Agent(
    name="Triage agent",
    instructions=(
        "Help the user with their questions. "
        "If they ask about billing, handoff to the Billing agent. "
        "If they ask about refunds, handoff to the Refund agent."
    ),
    handoffs=[billing_agent, handoff(refund_agent)],  # either direct agent or `handoff(...)`
)

async def main():
    result = await Runner.run(triage_agent, "I need to check refund status.")
    print(result.final_output)

# asyncio.run(main())

```

## 一个快速调试技巧

运行结束后可以检查：

- `result.final_output`：专家智能体最终给出的回复。
- `result.last_agent`：实际最后响应的是谁，方便下一轮继续衔接。
- `result.new_items`：查找 `HandoffCallItem` 和 `HandoffOutputItem`，这是 handoff 发生过的直接证据。

---

## 互动实验 1：做出你的第一次 handoff

目标：亲眼看到路由发生。

1. 把用户输入换成一个账单类问题后重新运行，比如：“My card was charged twice”。
2. 打印或检查 `result.new_items`，确认里面出现 **HandoffCallItem / HandoffOutputItem**。

> 检查点：你应该能看到最终回复来自专家智能体，同时 `new_items` 中包含 handoff 相关项目。
