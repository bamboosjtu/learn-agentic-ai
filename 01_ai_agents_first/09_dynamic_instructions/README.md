# Dynamic Instructions：让你的智能体自适应

## 什么是 Dynamic Instructions？

你可以把 **Dynamic Instructions** 理解成一个**会根据对话对象切换风格的智能助手**。你不必每次都给智能体写死同一套指令，而是可以让它根据当前情境动态调整自己的行为。

### 简单类比：像“变色龙”一样的老师

想象一位老师会这样做：
- **热情欢迎新学生**，并主动介绍自己
- 对提出追问的学生，**讲解得更详细**
- 对已经帮助过很多次的学生，**回应更高效**

Dynamic Instructions 就是让你的 AI 智能体也具备这种能力。

---

## 核心思路

如果使用静态指令，通常会像这样：

```python
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant."  # 总是一样
)
```

你也可以改成使用一个**函数**来动态生成指令：

```python
from agents import RunContextWrapper, Agent

def dynamic_instructions(context: RunContextWrapper, agent: Agent) -> str:
    return f"You are {agent.name}. Adapt to the user's needs."

agent = Agent(
    name="Smart Assistant",
    instructions=dynamic_instructions  # 会根据上下文变化
)
```

---

## 函数签名

动态指令函数会接收两个参数：

```python
from agents import RunContextWrapper, Agent

def dynamic_instructions(context: RunContextWrapper, agent: Agent) -> str:
    return f"The user's name is {context.context.name}. Help them with their questions."
```

### 参数说明

| 参数 | 类型 | 含义 |
|-----------|------|------------------|
| **`context`** | `RunContextWrapper` | 对话上下文、用户数据、消息等信息 |
| **`agent`** | `Agent` | 智能体对象，包含名称、工具、设置等 |
| **返回值** | `str` | 最终提供给智能体的指令字符串 |

---

## 从简单开始的示例

### 1. **最基础的动态指令**

```python
from agents import RunContextWrapper, Agent

def basic_dynamic(context: RunContextWrapper, agent: Agent) -> str:
    return f"You are {agent.name}. Be helpful and friendly."

agent = Agent(
    name="Dynamic Agent",
    instructions=basic_dynamic
)
```

### 2. **感知上下文的指令**

```python
def context_aware(context: RunContextWrapper, agent: Agent) -> str:
    # 检查当前对话里有多少条消息
    message_count = len(getattr(context, 'messages', []))
    
    if message_count == 0:
        return "You are a welcoming assistant. Introduce yourself!"
    elif message_count < 3:
        return "You are a helpful assistant. Be encouraging and detailed."
    else:
        return "You are an experienced assistant. Be concise but thorough."

agent = Agent(
    name="Context Aware Agent", 
    instructions=context_aware
)
```

### 3. **基于时间的指令**

```python
import datetime

def time_based(context: RunContextWrapper, agent: Agent) -> str:
    current_hour = datetime.datetime.now().hour
    
    if 6 <= current_hour < 12:
        return f"You are {agent.name}. Good morning! Be energetic and positive."
    elif 12 <= current_hour < 17:
        return f"You are {agent.name}. Good afternoon! Be focused and productive."
    else:
        return f"You are {agent.name}. Good evening! Be calm and helpful."

agent = Agent(
    name="Time Aware Agent",
    instructions=time_based
)
```

---

## 进阶示例

### 4. **有状态的指令（记住交互次数）**

```python
class StatefulInstructions:
    def __init__(self):
        self.interaction_count = 0
    
    def __call__(self, context: RunContextWrapper, agent: Agent) -> str:
        self.interaction_count += 1
        
        if self.interaction_count == 1:
            return "You are a learning assistant. This is our first interaction - be welcoming!"
        elif self.interaction_count <= 3:
            return f"You are a learning assistant. This is interaction #{self.interaction_count} - build on our conversation."
        else:
            return f"You are an experienced assistant. We've had {self.interaction_count} interactions - be efficient."

instruction_gen = StatefulInstructions()

agent = Agent(
    name="Stateful Agent",
    instructions=instruction_gen
)
```

### 5. **异步动态指令**

```python
import asyncio

async def async_instructions(context: RunContextWrapper, agent: Agent) -> str:
    # 模拟从数据库中拉取数据
    await asyncio.sleep(0.1)
    current_time = datetime.datetime.now()
    
    return f"""You are {agent.name}, an AI assistant with real-time capabilities.
    Current time: {current_time.strftime('%H:%M')}
    Provide helpful and timely responses."""

agent = Agent(
    name="Async Agent",
    instructions=async_instructions
)
```

---

## 理解 Context 和 Agent

### `Context` 参数

`context` 中通常包含：
- **Messages**：对话历史
- **User data**：自定义用户信息
- **Run state**：当前运行状态
- **Metadata**：额外元数据

```python
def explore_context(context: RunContextWrapper, agent: Agent) -> str:
    # 访问对话消息
    messages = getattr(context, 'messages', [])
    message_count = len(messages)
    
    # 访问用户上下文（如果存在）
    user_name = getattr(context.context, 'name', 'User')
    
    return f"You are {agent.name}. Talking to {user_name}. Message #{message_count}."
```

### `Agent` 参数

`agent` 中通常包含：
- **Name**：智能体名称
- **Tools**：可用工具
- **Settings**：模型设置
- **Configuration**：智能体配置

```python
def explore_agent(context: RunContextWrapper, agent: Agent) -> str:
    # 访问智能体属性
    agent_name = agent.name
    tool_count = len(agent.tools)
    
    return f"You are {agent_name} with {tool_count} tools. Be helpful!"
```

---

## 什么时候适合使用 Dynamic Instructions

| 使用场景 | 示例 |
|----------|---------|
| **个性化** | 根据用户偏好调整行为 |
| **上下文感知** | 根据对话历史改变回应方式 |
| **时间敏感** | 不同时间段采用不同风格 |
| **学习进阶** | 随着用户经验增加而调整讲解方式 |
| **多模态场景** | 针对不同输入类型切换指令 |

---

## 自己动手试一试

### 练习 1：简单动态指令

```python
from agents import RunContextWrapper, Agent

def my_dynamic_instructions(context: RunContextWrapper, agent: Agent) -> str:
    return f"You are {agent.name}. You love helping people learn Python!"

agent = Agent(
    name="Python Helper",
    instructions=my_dynamic_instructions
)

result = Runner.run_sync(agent, "What is a function?")
print(result.final_output)
```

### 练习 2：基于消息数量感知

```python
def message_count_aware(context: RunContextWrapper, agent: Agent) -> str:
    message_count = len(getattr(context, 'messages', []))
    
    if message_count == 0:
        return "You are a welcoming assistant. Say hello!"
    else:
        return f"You are an assistant. This is message #{message_count}. Be helpful!"

agent = Agent(
    name="Message Counter",
    instructions=message_count_aware
)
```

---

## 学习路径

1. **从简单开始**：先写基础动态指令
2. **加入上下文**：利用对话历史
3. **加入时间因素**：实现基于时间的适配
4. **加入状态**：记住交互过程
5. **使用异步**：处理异步操作

---

## 实用建议

- **先保持简单**：从基础函数开始
- **充分测试**：动态指令的行为可能更难预测
- **记录行为**：明确写清每个函数的作用
- **处理异常**：始终准备兜底指令
- **关注性能**：异步函数会增加复杂度

---

## 下一步

- 尝试运行 `hello_agent/` 文件夹里的示例
- 自己实验不同的动态指令写法
- 学习 [Context Management](../10_context_management/)
- 探索 [Advanced Agent Patterns](../11_advanced_patterns/)

---

*记住：Dynamic Instructions 能让你的智能体更聪明，也更灵活。*
