# Agents as a Tool

**“Agents as a tool”** 的意思是：你把一个智能体当成函数一样，让另一个智能体去调用它，但不会移交整段对话的控制权。这非常适合这样的场景：你希望有一个主智能体始终负责整体流程，而一些专家型智能体只负责完成小而专的任务，比如翻译、提取日期、总结内容等。

---

## 为什么需要 “agents as a tool”

你可以把主智能体看成项目经理，把专家智能体看成专业承包商：

- **保持控制权**：主智能体继续掌控对话，只在需要时“使用”专家，而不是把整个对话转交出去。
- **模块化能力**：你可以随时接入翻译器、日期提取器、代码修复器等小型智能体。
- **更可控的编排**：你可以决定何时调用子智能体、如何调用，同时仍然保留 tool-calling 的智能性。
- **Prompt 更干净**：每个专家智能体只专注一件事，例如“只做翻译”，这样更容易写对。

如果任务是开放式的，或者需要长时间、多步骤地持续交互，那么更适合用 *handoff*。但如果只是需要在单一流程里临时借用一个专家能力，那么 “agents as a tool” 往往更合适。

---

## 心智模型（类比）

- **Handoff** = 把来电转接到另一个部门，让对方继续完成整段对话。
- **Agent as a tool** = 你先让用户稍等，向同事快速问一个答案，然后由你自己再回复给用户。

也就是说，主智能体保持上下文和语气，只是临时借用专家能力。

---

## SDK 中的核心思路

- SDK 明确支持 *Agents as tools*：一个智能体可以被包装成工具，供其他智能体调用。
- 有一个便捷方法 `agent.as_tool(...)`，可以快速把智能体包装成工具。
- 如果你需要更高级的控制，可以自己实现一个工具，在工具内部通过 `Runner.run` 手动执行另一个智能体。

---

## 最小示例：编排器调用两个专家智能体

### 1. 定义专家智能体

```python
from agents import Agent

spanish_agent = Agent(
    name="Spanish agent",
    instructions="Translate the user's message to Spanish."
)

french_agent = Agent(
    name="French agent",
    instructions="Translate the user's message to French."
)

```

### 2. 把它们包装成工具并交给一个编排器

```python
orchestrator = Agent(
    name="Translator Orchestrator",
    instructions=(
        "You are a translation helper. If the user asks for Spanish, "
        "call translate_to_spanish. If French, call translate_to_french. "
        "Otherwise, ask which language they want."
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish."
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to French."
        ),
    ],
)

```

### 3. 运行它

```python
from agents import Runner
import asyncio

async def main():
    result = await Runner.run(orchestrator, "Please say 'Good morning' in Spanish.")
    print(result.final_output)

# asyncio.run(main())

```

这种模式正是 SDK 推荐的 “agents as tools” 用法。

---

## 进阶模式

### 1. 在工具内部运行一个智能体，以获得完整控制权

当便捷封装不够用时，比如你想设置 `max_turns`、修改运行配置、或对输出做后处理，可以创建一个函数工具，在工具实现内部调用 `Runner.run(...)` 执行子智能体，并返回字符串结果。

```python
from agents import Agent, Runner, function_tool

# A focused sub-agent
proofreader = Agent(
    name="Proofreader",
    instructions="Fix grammar and punctuation. Keep meaning. Reply only with the corrected text."
)

@function_tool
async def proofread_text(text: str) -> str:
    """Fix grammar and punctuation; return only corrected text."""
    result = await Runner.run(proofreader, text, max_turns=3)
    return str(result.final_output)

# Main agent that uses the proofreader as just another tool
teacher_agent = Agent(
    name="Teacher",
    instructions="Help students write clearly. Use tools when asked to fix text.",
    tools=[proofread_text],
)

```

### 2. 工具里的智能体还可以再使用自己的工具

```python

@function_tool
def get_weather():
  return "It is sunny"

weather_agent:Agent = Agent(
      name="weather checker",
      instructions="Use avaible tools get weather info",
      tools=[get_weather],
      model=model
  )


@function_tool
def weather_agent_fun(query: str) -> str:

  result:Runner = Runner.run_sync(weather_agent, query)
  return result.final_output


agent:Agent = Agent(
    name="General Agent",
    instructions="Answer general purpose query efficently if tool call is require call available tools",
    tools=[weather_agent_fun],
    model=model
)


async def main():
  result = await Runner.run(agent, "What is the weather like today?")
  print(result.final_output)

if _name_ == "_main_":
    asyncio.run(main())

```

---

## 初学者什么时候选 “agents as tools”，什么时候选 “handoffs”？

| 场景 | 更适合 | 原因 |
| --- | --- | --- |
| 一个主声音，只做一个快速子任务（翻译、提取、重格式化） | **Agents as tools** | 主智能体保持控制，只是短暂借用能力。 |
| 长对话、强专业性任务（比如账单客服应接管后续对话） | **Handoffs** | 让专业智能体接管后续一个或多个回合。 |

---

## 重要参数与常见坑

- **Tool choice**：可以通过 `model_settings.tool_choice` 强制或禁止工具调用，例如 `"auto"`、`"required"`、`"none"` 或指定某个工具名。
- **工具调用后的自动重置**：为了避免死循环，SDK 在一次工具调用后会把 `tool_choice` 重置回 `"auto"`。你也可以改这个行为，或者通过 `Agent.tool_use_behavior="stop_on_first_tool"` 在首次工具调用后直接停止。
- **便捷性 vs 控制力**：`agent.as_tool(...)` 很方便，但不暴露所有能力，例如 `max_turns`。需要完全控制时，就在工具内部显式调用 `Runner.run(...)`。
- **Tracing**：用 traces 可以看清主智能体何时调用了子智能体、子智能体返回了什么，这对排查问题很有帮助。

---

## 分步小练习

1. **先从最小版本开始**
   
   创建两个很小的专家智能体，例如 “Lowercaser” 和 “Title-Caser”，用 `as_tool` 包装，让 orchestrator 进行选择。
    
2. **换成一个真实能力**
   
   把其中一个玩具工具替换成真正能力，比如“总结器”或“翻译器”智能体。
    
3. **加入显式控制**
   
   强制 orchestrator 使用工具（`tool_choice="required"`），观察行为变化。
    
4. **切换到高级模式**
   
   用 `@function_tool` 重新实现一个工具，并在里面通过 `Runner.run(...)` 调用子智能体。
    
5. **配合 tracing 检查**
   
   打开 trace viewer，观察每一次工具调用及其结果。

---

## 可直接复用的起步模板

```python
from agents import Agent, Runner, function_tool

# 1) Specialists
summer = Agent(
    name="Summarizer",
    instructions="Summarize in 3 bullet points. No extra text."
)
detect_lang = Agent(
    name="Language Detector",
    instructions="Return the ISO language code for the given text."
)

# 2) Wrap as tools (quick pattern)
summarize_tool = summer.as_tool("summarize", "Summarize in 3 bullets.")
detect_tool = detect_lang.as_tool("detect_language", "Detect language code.")

# 3) Main agent
coach = Agent(
    name="Coach",
    instructions=("Help the user polish writing. If they say 'summarize', call summarize. "
                  "If they ask 'what language', call detect_language. Otherwise, respond normally."),
    tools=[summarize_tool, detect_tool],
)

# 4) Run
# result = await Runner.run(coach, "Summarize: Large language models are...")
# print(result.final_output)

```

如果后续你需要更严格的控制，可以把其中一个工具换成 `@function_tool`，在里面通过 `Runner.run(...)` 调用子智能体。

---

## 总结

- **它是什么**：把其他智能体当作可调用工具，让编排逻辑集中在主智能体里。
- **什么时候用**：适合短小、专注的子任务，例如翻译、提取、格式化，同时保持一个统一的对话拥有者。
- **怎么做**：先用 `agent.as_tool(...)` 起步；需要更高控制力时，再换成在工具中调用 `Runner.run(...)` 的方式。
