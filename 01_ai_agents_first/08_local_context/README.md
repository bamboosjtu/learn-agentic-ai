# 上下文管理

在 OpenAI Agents SDK 中，上下文管理指的是：在 agent 执行期间，如何处理那些可供你的代码使用的附加数据。这类“上下文”主要分为两种形式：

[学习参考](https://openai.github.io/openai-agents-python/context/)

### 1. 本地上下文（Local Context）

**它是什么：**  
本地上下文是你在运行 agent 时传入的任意数据或依赖，这些内容可供你的代码使用，例如工具、生命周期钩子等。它完全属于内部数据，不会发送给 LLM。

**它如何工作：**  
- **创建上下文：**  
  你可以创建一个 Python 对象，通常使用 dataclass 或 Pydantic 模型，用来封装用户名、用户 ID、logger 或辅助函数等数据。
  
- **传递上下文：**  
  你可以在运行方法中传入这个对象，例如 `Runner.run(..., context=your_context)`。SDK 会把这个对象包装成 `RunContextWrapper`，这样在该次运行中，每个工具函数、生命周期钩子或回调都可以通过 `wrapper.context` 访问它。

- **关键点：**  
  同一次 agent 运行中的所有部分必须共享同一种上下文类型，以保证一致性。

**典型使用场景：**  
- 存储工具可能需要的用户信息，例如用户名或用户 ID。
- 注入 logger、数据获取器等依赖。
- 提供在整个运行流程中都可访问的辅助函数。

*注意：* 这种本地上下文不会暴露给 LLM。它只服务于你的后端逻辑和运行流程。

---

### 2. Agent / LLM 上下文

**它是什么：**  
Agent / LLM 上下文是指 LLM 在生成回答时能看到的信息。它本质上就是对话历史或消息内容，例如 system prompt、instructions 和用户输入，这些内容会共同引导模型输出。

**如何使用：**  
- **写入 Instructions：**  
  你可以把重要上下文（比如用户名、当前日期、特定规则）直接写进 agent 的 instructions 或 system prompt 中。
  
- **写入输入消息：**  
  你也可以在调用 `Runner.run()` 时，把上下文附加到输入消息中，确保这些信息成为 LLM 处理对话的一部分。
  
- **函数工具：**  
  LLM 还可以调用函数工具，按需获取那些最初并不在对话历史中的数据。
  
- **检索 / Web 搜索：**  
  你可以使用专门的工具拉取相关外部数据，从而让 LLM 的回答建立在最新或更详细的信息之上。

**核心区别：**  
本地上下文是内部数据，绝不会发送给 LLM；而 Agent / LLM 上下文则会被明确暴露在对话中，用来影响和引导模型生成回答。

---

### 代码示例解析

下面这个简化示例展示了本地上下文的管理方式：

```python
import asyncio
from dataclasses import dataclass

from agents import Agent, RunContextWrapper, Runner, function_tool

# Define a simple context using a dataclass
@dataclass
class UserInfo:  
    name: str
    uid: int

# A tool function that accesses local context via the wrapper
@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:  
    return f"User {wrapper.context.name} is 47 years old"

async def main():
    # Create your context object
    user_info = UserInfo(name="John", uid=123)  

    # Define an agent that will use the tool above
    agent = Agent[UserInfo](  
        name="Assistant",
        tools=[fetch_user_age],
    )

    # Run the agent, passing in the local context
    result = await Runner.run(
        starting_agent=agent,
        input="What is the age of the user?",
        context=user_info,
    )

    print(result.final_output)  # Expected output: The user John is 47 years old.

if __name__ == "__main__":
    asyncio.run(main())
```

**示例说明：**

1. **创建本地上下文：**  
   定义了一个 `UserInfo` dataclass，用来保存用户相关数据。

2. **传递上下文：**  
   创建 `UserInfo` 实例，并在运行 agent 时把它作为 context 传入。

3. **在工具中访问上下文：**  
   `fetch_user_age` 函数通过 `RunContextWrapper` 访问 `UserInfo` 数据，并基于这些上下文生成结果。

4. **本地上下文 vs. LLM 上下文：**  
   - **本地上下文：** 这里的 `UserInfo` 对象由工具函数使用，它属于内部数据，不会展示给 LLM。  
   - **Agent / LLM 上下文：** 如果你希望 LLM 也考虑额外信息（比如在 instructions 中包含用户名），那就需要把这类信息写入 agent 的 instructions 或对话历史。
