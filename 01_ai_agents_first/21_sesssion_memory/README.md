# [Sessions](https://openai.github.io/openai-agents-python/sessions/)：让智能体记住对话

## 什么是会话记忆？

把 **Session Memory（会话记忆）** 想象成 **给你的智能体一本笔记本**，它会把你们聊过的内容都记下来。没有会话记忆，就像你在和一个严重失忆的人说话，他会立刻忘掉你刚才说过的内容；有了会话记忆，智能体就能记住整段对话。

### 简单类比：对话笔记本

想象你在和一个朋友聊天：

- **没有记忆**："你好，你叫什么名字？" -> "我叫 Alice" -> "你叫什么名字？" -> "我叫 Alice"（立刻就忘了！）
- **有记忆**："你好，你叫什么名字？" -> "我叫 Alice" -> "你住在哪个州？" -> "我住在 California"（记得我叫 Alice！）

会话记忆就像给你的智能体一份完美的对话记忆。

## OpenAI Agents SDK 中的 Sessions

Agents SDK 提供了内置的会话记忆功能，可以在多次 agent 运行之间自动维护对话历史，不再需要你在每一轮之间手动处理 `.to_input_list()`。

Sessions 会为某个特定会话保存对话历史，让 agent 在无需显式手动管理记忆的情况下保持上下文。这对于构建聊天应用或多轮对话尤其有用，因为你通常希望 agent 能记住之前的交互内容。

---

## 核心概念

**没有会话记忆（默认）**：

```python
# 每次对话彼此独立，agent 会忘记之前的内容！
result1 = Runner.run_sync(agent, "What city is the Golden Gate Bridge in?")
# Agent: "San Francisco"

result2 = Runner.run_sync(agent, "What state is it in?")
# Agent: "What are you referring to?" (forgot about San Francisco!)
```

**有会话记忆**：

```python
# Agent 会记住对话！
session = SQLiteSession("conversation_123")

result1 = Runner.run_sync(agent, "What city is the Golden Gate Bridge in?", session=session)
# Agent: "San Francisco"

result2 = Runner.run_sync(agent, "What state is it in?", session=session)
# Agent: "California" (remembers we were talking about San Francisco!)
```

---

## 会话记忆如何工作

### 幕后机制

当你使用会话记忆时，agent 会自动完成以下流程：

1. **每次运行前**：取回此前全部对话历史
2. **运行过程中**：带着完整上下文处理你的新消息
3. **运行结束后**：把新消息和响应保存进记忆

```python
# 自动发生的事情：
session = SQLiteSession("user_123")

# 第 1 轮
result1 = Runner.run_sync(agent, "Hello", session=session)
# 当前记忆: [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi!"}]

# 第 2 轮
result2 = Runner.run_sync(agent, "How are you?", session=session)
# 会加载此前历史，并加入新的消息
# 当前记忆: [之前的消息 + 新的用户消息 + 新的 assistant 回复]
```

### 会话存储选项

| 存储类型 | 代码 | 适用场景 |
| --------------------- | ---------------------------------------- | ------------------------------ |
| **无记忆** | `Runner.run_sync(agent, query)` | 快速测试、一次性提问 |
| **临时记忆** | `SQLiteSession("session_id")` | 仅当前会话 |
| **持久记忆** | `SQLiteSession("session_id", "<db...>")` | 永久保存对话 |

---

## 循序渐进示例

### 1. 你的第一个会话记忆

```python
import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, SQLiteSession, OpenAIChatCompletionsModel, AsyncOpenAI

# Load environment variables
load_dotenv(find_dotenv())

# Setup Gemini client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

external_client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)
model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)

# Create agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant. Be friendly and remember our conversation.",
    model=model
)

# Create session memory
session = SQLiteSession("my_first_conversation")

print("=== First Conversation with Memory ===")

# Turn 1
result1 = Runner.run_sync(
    agent,
    "Hi! My name is Alex and I love pizza.",
    session=session
)
print("Agent:", result1.final_output)

# Turn 2 - Agent should remember your name!
result2 = Runner.run_sync(
    agent,
    "What's my name?",
    session=session
)
print("Agent:", result2.final_output)  # Should say "Alex"!

# Turn 3 - Agent should remember you love pizza!
result3 = Runner.run_sync(
    agent,
    "What food do I like?",
    session=session
)
print("Agent:", result3.final_output)  # Should mention pizza!
```

### 2. 持久记忆 vs 临时记忆

```python
import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, SQLiteSession, OpenAIChatCompletionsModel, AsyncOpenAI

# Load environment variables
load_dotenv(find_dotenv())

# Setup Gemini client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

external_client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)
model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)

# 临时记忆（程序结束后丢失）
temp_session = SQLiteSession("temp_conversation")

# 持久记忆（保存到文件）
persistent_session = SQLiteSession("user_123", "conversations.db")

agent = Agent(name="Assistant", instructions="You are helpful.", model=model)

# 使用临时会话
result1 = Runner.run_sync(
    agent,
    "Remember: my favorite color is blue",
    session=temp_session
)

# 使用持久会话
result2 = Runner.run_sync(
    agent,
    "Remember: my favorite color is blue",
    session=persistent_session
)

print("Both sessions now remember your favorite color!")
print("But only the persistent session will remember after restarting the program.")
```

### 3. 记忆操作：添加、查看和移除

```python
import asyncio
from agents import SQLiteSession

async def memory_operations_demo():
    session = SQLiteSession("memory_ops", "test.db")

    # 手动添加一些对话项
    conversation_items = [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi there! How can I help you?"},
        {"role": "user", "content": "What's the weather like?"},
        {"role": "assistant", "content": "I don't have access to weather data."}
    ]

    await session.add_items(conversation_items)
    print("Added conversation to memory!")

    # 查看记忆中的所有项
    items = await session.get_items()
    print(f"\nMemory contains {len(items)} items:")
    for item in items:
        print(f"  {item['role']}: {item['content']}")

    # 移除最后一项（撤销）
    last_item = await session.pop_item()
    print(f"\nRemoved last item: {last_item}")

    # 再次查看记忆
    items = await session.get_items()
    print(f"\nMemory now contains {len(items)} items:")
    for item in items:
        print(f"  {item['role']}: {item['content']}")

    # 清空全部记忆
    await session.clear_session()
    print("\nCleared all memory!")

    # 验证记忆已清空
    items = await session.get_items()
    print(f"Memory now contains {len(items)} items")

# Run the async demo
asyncio.run(memory_operations_demo())
```

## 自定义记忆实现

记住，你也可以通过创建一个遵循 Session 协议的类，来实现自己的会话记忆。

## 真实世界应用

### 自我挑战项目：客户支持聊天 Agent

```python
from agents import Agent, Runner, SQLiteSession
import datetime

class CustomerSupportBot:
    def __init__(self):
        self.agent = Agent(
            name="SupportBot",
            instructions="""You are a helpful customer support agent.
            Remember the customer's information and previous issues throughout the conversation.
            Be friendly and professional."""
        )

    def get_customer_session(self, customer_id: str):
        """Get or create a session for a specific customer"""
        return SQLiteSession(f"customer_{customer_id}", "support_conversations.db")

    def chat_with_customer(self, customer_id: str, message: str):
        """Handle a customer message"""
        session = self.get_customer_session(customer_id)

        result = Runner.run_sync(
            self.agent,
            message,
            session=session
        )

        return result.final_output

# Example usage
support_bot = CustomerSupportBot()

# Customer 123's conversation
print("=== Customer 123 Support Session ===")
print("Customer: Hi, I'm having trouble with my order #12345")
response1 = support_bot.chat_with_customer("123", "Hi, I'm having trouble with my order #12345")
print(f"Support: {response1}")

print("\nCustomer: The item was damaged when it arrived")
response2 = support_bot.chat_with_customer("123", "The item was damaged when it arrived")
print(f"Support: {response2}")

print("\nCustomer: What was my order number again?")
response3 = support_bot.chat_with_customer("123", "What was my order number again?")
print(f"Support: {response3}")  # Should remember order #12345!

# Different customer's conversation
print("\n=== Customer 456 Support Session ===")
print("Customer: Hello, I need help with billing")
response4 = support_bot.chat_with_customer("456", "Hello, I need help with billing")
print(f"Support: {response4}")  # Fresh conversation, no memory of customer 123
```

---

## 重要提示与最佳实践

### 会话 ID 命名规范

| 模式 | 示例 | 使用场景 |
| ----------------- | ---------------------------- | ---------------------- |
| **基于用户** | `"user_12345"` | 个人对话 |
| **基于线程** | `"thread_abc123"` | 论坛/聊天线程 |
| **基于上下文** | `"support_ticket_456"` | 特定用途 |
| **带时间戳** | `"session_2024_01_15_14_30"` | 基于时间的追踪 |

### 记忆管理

```python
# Good: 使用有意义的 session ID
session = SQLiteSession("customer_support_user_123", "production.db")

# Good: 不同上下文使用不同 session
work_session = SQLiteSession("work_chat_user_456")
personal_session = SQLiteSession("personal_chat_user_456")

# Good: 重新开始时清空会话
await session.clear_session()  # Start over

# Avoid: 过于泛化的 session ID
session = SQLiteSession("session1")  # 不够清晰

# Avoid: 在同一个 session 里混用不同上下文
# 不要把工作和私人对话放在同一个 session 中
```

### 性能注意事项

```python
# 对于长对话，可限制记忆读取量
session = SQLiteSession("long_conversation")

# 仅获取最近的项目以提升性能
recent_items = await session.get_items(limit=50)  # 只取最近 50 条消息

# 对非常活跃的会话，可考虑定期清理
conversation_length = len(await session.get_items())
if conversation_length > 1000:
    print("Consider archiving old messages for performance")
```

---

## 学习路径

1. **从简单开始**：为单个对话使用基础会话记忆
2. **多个会话**：为不同上下文创建不同对话
3. **记忆操作**：添加、查看、移除项目
4. **纠错**：用 `pop_item()` 修正错误
5. **真实应用**：客户支持、辅导、个人助理
6. **自定义记忆**：构建自己的存储后端
7. **生产模式**：性能优化与最佳实践

---

_记住：会话记忆能让你的智能体从“失忆状态”变成“完整记住你们对话内容”的助手。_
