# Advanced Tools MasterClass

欢迎进入工具调用的下一阶段。基础工具解决的是“让智能体具备能力”，高级工具解决的是“让你掌控流程”。这份指南会教你如何管理智能体的工作流、优雅处理错误，并构建更稳健的真实应用。

> **核心思路：** 你是管理者，工具是你的团队。高级特性就是你的管理手册，用来决定它们什么时候工作、能不能工作，以及出错时怎么办。

### 本节会掌握什么

* **控制执行流程**：如何使用 `tool_use_behavior`，让智能体在第一次动作后停止，或者只在某个特定“收尾工具”执行后停止？
* **防止智能体失控**：`max_turns` 是什么？它如何限制 LLM 调用次数，以及到达上限时为什么会抛异常？
* **创建上下文感知工具**：如何让工具只在特定条件下可用，例如通过动态 `is_enabled` 做出“仅管理员可用”的工具？
* **构建具备韧性的智能体**：如何通过 `try/except` 优雅处理工具失败，让智能体恢复而不是崩掉？
* **管理有状态工具**：少数情况下如果工具需要记住信息，该如何用 `FunctionTool` 类来实现？
* **落地到生产模式**：这些功能如何映射到现实中的 API Gateway、数据流水线、交互式助手等架构？

## 为什么需要 Advanced Tools MasterClass？

如果没有这些高级控制，智能体可能会陷入循环、因为一个简单错误而崩溃，或者调用本不该开放的工具。这会浪费时间和成本。高级工具就是用来解决这些关键问题的：
* **控制**：防止智能体无限运行，或无意义调用工具。
* **上下文约束**：根据用户权限或当前情境动态启用/禁用工具。
* **韧性**：即使工具失败，也不至于让整个流程崩掉。
* **精确编排**：构建可预测的多步骤工作流。

---

## 第一部分：掌握 `tool_use_behavior`

`Agent` 上的 `tool_use_behavior` 参数决定了工具执行成功之后，智能体下一步会发生什么。

### 模式 1：`"run_llm_again"`（默认）
工具运行结束后，工具输出会被送回 LLM，LLM 再决定下一步。

### 模式 2：`"stop_on_first_tool"`
在第一次工具调用后立刻停止执行。该工具的原始输出直接成为最终结果，LLM 不会再看到这个工具结果。

### 模式 3：`StopAtTools`
你可以给出一组“收尾工具”的名字。智能体持续执行，但一旦调用这些指定工具中的某一个，就立即停止。

```python
from agents import Agent, StopAtTools

agent = Agent(
    name="DataPipeline",
    tools=[fetch_data, process_data, save_data],
    tool_use_behavior=StopAtTools(stop_at_tool_names=["save_data"]),
)
```

---

## 第二部分：Runner 的安全网 `max_turns`

`Runner.run` 中的 `max_turns` 参数，是防止无限循环的最后一道安全网。

```python
result = await Runner.run(agent, "Find articles about AI agents. You can think and act a maximum of 5 times.", max_turns=6)
```

* **它是什么**：对 LLM 调用次数设定硬上限。
* **达到上限时会怎样**：会抛出 `MaxTurnsExceeded` 异常，你的应用代码必须准备好捕获它。

---

## 第三部分：让工具动态出现和消失

`@function_tool` 上的 `is_enabled` 参数允许你只在条件合适时开放工具。

### 静态开关

```python
@function_tool(is_enabled=False)
def under_maintenance_tool():
    """This tool is temporarily disabled."""
    return "Sorry, this feature is offline for maintenance."
```

### 动态开关

```python
def is_user_admin(context: RunContextWrapper, agent: Agent) -> bool:
    return context.get("user_role") == "admin"

@function_tool(is_enabled=is_user_admin)
def delete_user_database():
    """[ADMIN ONLY] Deletes the entire user database."""
    return "Database has been deleted."
```

---

## 第四部分：优雅的错误处理

```python
@function_tool
def divide(a: int, b: int) -> str:
    """Divides two numbers."""
    try:
        result = a / b
        return str(result)
    except ZeroDivisionError:
        return "Error: You cannot divide by zero. Please ask for a different number."
```

更复杂场景下，还可以使用 `failure_error_function` 来做自定义日志记录或错误路由。

---

## 第五部分：状态型工具（谨慎使用）

虽然 99% 的场景都更适合 `@function_tool`，但你也可以继承 `FunctionTool` 类来构建一个带内部状态的工具。

```python
from agents import FunctionTool

class CounterTool(FunctionTool):
    def __init__(self):
        self._count = 0
        super().__init__(
            name="incrementing_counter",
            description="Counts up by one each time it is called.",
            params_json_schema={"type": "object", "properties": {}},
            on_invoke_tool=self.on_invoke_tool
        )

    async def on_invoke_tool(self, context, args_json_str) -> str:
        self._count += 1
        return f"The current count is: {self._count}"


agent_tools = [CounterTool()]

print(agent_tools)
```

#### 预期输出：

```python
[CounterTool(name='incrementing_counter', description='Counts up by one each time it is called.', params_json_schema={'type': 'object', 'properties': {}, 'additionalProperties': False, 'required': []}, on_invoke_tool=<bound method CounterTool.on_invoke_tool of ...>, strict_json_schema=True, is_enabled=True)]
```

---

## 第六部分：生产实践模式

* **API Gateway**：快速、直接、单步动作。适合 `tool_use_behavior="stop_on_first_tool"`。
* **Data Pipeline**：有明确结束点的顺序流程。适合 `tool_use_behavior=StopAtTools(...)`。
* **Interactive Assistant**：需要根据工具结果继续思考。适合默认的 `tool_use_behavior="run_llm_again"`。

---

## 动手实验：一个小型 Lab

```python
from agents import (
    Agent,
    OpenAIChatCompletionsModel,
    Runner,
    function_tool,
    StopAtTools,
    AsyncOpenAI,
    set_tracing_disabled,
)
from dotenv import find_dotenv, load_dotenv
import asyncio
import os

_ = load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Reference: https://ai.google.dev/gemini-api/docs/openai
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

set_tracing_disabled(disabled=True)


@function_tool
def get_user_data(user_id: str) -> str:
    """Looks up user data."""
    return f"Data for {user_id}: Name - Alex, Role - user"


# TODO 1: Make this an admin-only tool using `is_enabled`.
@function_tool
def delete_user(user_id: str) -> str:
    """Deletes a user. This is a final action."""
    return f"User {user_id} has been deleted."


admin_agent = Agent(
    name="Admin Agent",
    instructions="Help manage users. First get data, then delete if asked.",
    tools=[get_user_data, delete_user],
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tool_use_behavior=StopAtTools(stop_at_tool_names=["delete_user"]),
)


async def main():
    print("--- Running as a regular user ---")
    result_user = await Runner.run(
        admin_agent, "Please delete user client_456.", context={"role": "user"}
    )
    print(f"Final Output: {result_user.final_output}")

    print("\n--- Running as an admin ---")
    result_admin = await Runner.run(
        admin_agent,
        "Get data for user_123 and then delete them.",
        context={"role": "admin"},
        max_turns=3,
    )
    print(f"Final Output: {result_admin.final_output}")


asyncio.run(main())
```

#### 预期结果
```
--- Running as a regular user ---
Final Output: User client_456 has been deleted.

--- Running as an admin ---
Final Output: User user_123 has been deleted.
---
```

## 总结

* **它是什么**：一组精细控制手段，用于管理智能体何时、如何使用工具。
* **关键控制项**：用 `tool_use_behavior` 管理工作流，用 `Runner.max_turns` 做安全上限，用 `is_enabled` 实现上下文感知的工具开放策略。
* **最佳实践**：在工具内部用 `try/except` 处理错误，并根据实际业务模式配置智能体行为。

- https://openai.github.io/openai-agents-python/tools/
- https://github.com/openai/openai-agents-python/tree/main/examples/tools
- https://github.com/mjunaidca/agents-sdk-decoded/blob/main/01_agent/09_tool_behavior.py

---

## 补充：Tool 高级用法

说明：下面内容是基于当前目录中的 `part1.py`、`part2.py`、`part3.py`、`part4.py` 和 `tool_dynamic_permissions.py` 做的补充总结，作为对上文的扩展说明。这里只做追加，不替换本 README 现有内容。

### 1. 用 `StopAtTools` 控制“在哪个工具结束流程”

`part1.py` 演示了一个非常实用的高级模式：不是调用完任意工具都结束，而是只有命中某个“终结型工具”才结束。

适合场景：

* 前面若干工具负责查询、推理、组装信息
* 最后某个工具负责提交、保存、删除、下单等“最终动作”
* 一旦执行了最终动作，就不希望 LLM 再继续自由发挥

核心点：

* `tool_use_behavior=StopAtTools(stop_at_tool_names=[...])`
* 让 Agent 在调用指定工具后立即停止
* 能把多步工具链和“最终提交动作”区分开

这比默认的 `run_llm_again` 更适合有明确收尾动作的工作流。

### 2. 用 `max_turns` 防止工具循环或模型反复试探

`part2.py` 演示了 `Runner.run(..., max_turns=2)` 的安全边界控制。

这个参数的意义不是“限制工具次数”，而是限制整个 Agent 运行过程中模型可进行的轮次数。它适合解决以下问题：

* 模型在“是否调用工具”之间来回试探
* 工具执行后，模型又继续发起新一轮推理
* Prompt 或工具描述不清时，Agent 出现不必要的迭代

`part2.py` 里还打印了 `res.new_items`，这也是调试 tool calling 的关键手段。你可以直接看到：

* 是否真的发起了 `ToolCallItem`
* 工具输出是否进入了 `ToolCallOutputItem`
* 最终自然语言回复是否来自工具结果

所以 `max_turns` 和 `res.new_items` 组合起来，本质上就是：

* `max_turns` 负责兜底
* `res.new_items` 负责排查

### 3. 用 `is_enabled` 做上下文感知的动态工具开关

`part3.py` 和 `tool_dynamic_permissions.py` 共同演示了 `@function_tool(is_enabled=...)` 的高级用法。

这不是简单的布尔开关，而是“根据运行上下文动态决定工具能不能暴露给模型”。

**`part3.py` 里定义了：**

* `UserScope`
* `RunContextWrapper[UserScope]`
* `is_weather_allowed(...)`

然后把这个函数传给 `is_enabled`。这意味着：

* 工具是否可用，取决于当前用户上下文
* 同一个 Agent，在不同 context 下，模型看到的工具集可以不同

这比“在工具函数内部拒绝请求”更好，因为：

* 工具在不可用时，根本不会暴露给模型
* 模型不会围绕一个本来就不可用的工具继续规划
* 运行轨迹更干净，行为更可预测

**`tool_dynamic_permissions.py` 的重点**

这个文件把动态权限控制进一步落地到“订阅等级”场景：

* `free` 用户看不到高级工具
* `premium` / `enterprise` 用户可以使用天气工具

这属于产品里非常常见的高级工具模式：

* 按角色开放工具
* 按套餐开放工具
* 按租户能力开放工具
* 按运行态条件临时禁用工具

如果一个工具本质上有权限限制，优先考虑 `is_enabled`，而不是先暴露给模型、再在函数内部报错。

### 4. 用` instructions` 提高工具调用稳定性

`part4.py` 体现了一个非常重要但经常被忽略的点：工具“注册成功”不等于模型“必然会调用”。

当前 `part4.py` 的处理方式是：

* 给 `get_weather` 补充明确描述
* 在 instructions 里显式要求：
  `If the user asks about weather, you must call the get_weather tool. Do not answer from memory.`

这个示例说明了两个结论：

* 工具调用是模型决策的一部分，不是只要 `tools=[...]` 就一定发生
* 如果你需要高确定性，必须在 prompt / instructions 里清楚写出调用规则

也就是说，影响工具调用稳定性的因素不只一个：

* 工具名是否清晰
* 工具描述是否清晰
* 参数 schema 是否明确
* instructions 是否明确禁止“凭记忆回答”

当你发现“模型没有调用工具”时，先检查的往往不是 SDK，而是这几项语义约束是否足够强。

### 5. 工具函数里可观测性

`part4.py` 和 `tool_dynamic_permissions.py` 都加入了 `print(...)` 调试日志，例如：

* `print(f"[TOOL] get_weather called with city={city}")`
* `print("premium_feature_enabled()")`

这体现了一个工程上很重要的高级实践：调试 tool calling 时，不要只看 `final_output`。

建议同时观察三个层面：

* 工具前：`is_enabled` 是否被执行
* 工具中：工具函数是否真的进入
* 工具后：`res.new_items` 里是否出现 tool call / tool output

否则你很容易把以下几种问题混为一谈：

* 模型没选工具
* 工具被权限逻辑禁用了
* 工具调用了但返回异常
* 工具输出没正确反馈回模型

### 6. 用 `try/except` 做工具级容错

`part4.py` 还演示了工具内部的异常处理结构：

* `ValueError`
* `TimeoutError`
* 通用 `Exception`

虽然示例里的天气逻辑比较简单，但它传达的模式是对的：工具层面的失败应尽量在工具层被识别、包装或转义。

适合的工程实践包括：

* 把第三方 API 超时转成可理解错误
* 把业务参数错误转成稳定的错误消息
* 对临时失败做降级或兜底

这样做的好处是：

* Agent 行为更稳定
* 日志更可读
* 更容易在工具层实现 fallback 策略

### 7. `set_tracing_disabled(...)`

`part4.py` 里额外演示了“到底有没有调用工具”：

```python
from agents import set_tracing_disabled
set_tracing_disabled(True)
```

这在本地调试时很实用。因为 tracing 失败、网络超时、进程退出时的后台 flush，常常会制造很多噪音日志，让你误以为是工具调用失败。

本地排查 tool calling 是否成功时，推荐先：

* 关闭 tracing
* 打印工具日志
* 打印 `res.new_items`

先确认“工具有没有被调用”，再去看 tracing、可观测性平台或链路上报问题。

### 8.  Tool 的四层高级控制面

把本目录这些 `.py` 文件合在一起看，已经形成了一套比较完整的高级工具控制思路：

* 调用流程控制：`StopAtTools`
* 运行轮次保护：`max_turns`
* 工具动态暴露：`is_enabled`
* 工具调用稳定性与容错：清晰 instructions + `try/except` + 可观测日志

如果把它们映射到真实项目里，可以这么理解：

* `StopAtTools` 解决“什么时候应该停”
* `max_turns` 解决“最多允许思考几轮”
* `is_enabled` 解决“当前用户是否看得到这个工具”
* 明确 instructions 和日志/异常处理，解决“为什么工具没被调用，或者调用后为什么结果不稳定”

### 9. 实战建议

基于本目录示例，推荐在真实项目里遵循下面这套顺序：

1. 先把工具描述写清楚，不要给空描述。
2. 在 instructions 中明确写出何时必须调用工具。
3. 给关键工具加 `print` 或结构化日志。
4. 调试阶段打印 `res.new_items`。
5. 对敏感工具使用 `is_enabled`，不要只在函数内部做权限拦截。
6. 对最终动作型工具使用 `StopAtTools`。
7. 用 `max_turns` 给整个流程设上限。
8. 本地排查时先关闭 tracing，避免噪音干扰判断。

这几项一起用，才是 Tool 在工程里真正稳定、可控的高级用法。
