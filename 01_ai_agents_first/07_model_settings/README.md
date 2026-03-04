# Model Settings：控制你的 AI Agent“大脑”

## 什么是 Model Settings？

你可以把 **Model Settings** 理解成专业相机上的**旋钮和拨盘**。摄影师会调整对焦、曝光和快门速度来获得理想画面；同样地，你也可以调整 AI agent 的行为方式，从而得到你想要的回答。

### 一个简单类比：精准烹饪

想象你正在做饭：
- **Temperature** = 你的 agent 是更有创意，还是更专注
- **Tool Choice** = 你的 agent 是否可以使用计算器、天气工具等
- **Max Tokens** = 回答可以有多长
- **Parallel Tools** = 你的 agent 是否可以同时使用多个工具

---

## 最重要的几个设置（从最基础开始）

### 1. **Temperature**：创意控制旋钮

```python
# Low temperature (0.1) = Very focused, consistent answers
agent_focused = Agent(
    name="Math Tutor",
    instructions="You are a precise math tutor.",
    model_settings=ModelSettings(temperature=0.1)
)

# High temperature (0.9) = More creative, varied responses
agent_creative = Agent(
    name="Story Writer",
    instructions="You are a creative storyteller.",
    model_settings=ModelSettings(temperature=0.9)
)
```

**适用场景：**
- **低温度（0.1-0.3）**：数学、事实、精确指令
- **中温度（0.4-0.6）**：一般对话、解释说明
- **高温度（0.7-0.9）**：创意写作、头脑风暴

注意：对于 Gemini，temperature 的范围可以扩展到 `2`。

### 2. **Tool Choice**： “能不能使用工具”的开关

```python
# Agent can decide when to use tools (default)
agent_auto = Agent(
    name="Smart Assistant",
    tools=[calculator, weather_tool],
    model_settings=ModelSettings(tool_choice="auto")
)

# Agent MUST use a tool (even if not needed)
agent_required = Agent(
    name="Tool User",
    tools=[calculator, weather_tool],
    model_settings=ModelSettings(tool_choice="required")
)

# Agent CANNOT use tools (chat only)
agent_no_tools = Agent(
    name="Chat Only",
    tools=[calculator, weather_tool],
    model_settings=ModelSettings(tool_choice="none")
)
```

### 3. **Max Tokens**：回答长度上限

```python
# Short, concise responses
agent_brief = Agent(
    name="Brief Assistant",
    model_settings=ModelSettings(max_tokens=100)
)

# Longer, detailed responses
agent_detailed = Agent(
    name="Detailed Assistant", 
    model_settings=ModelSettings(max_tokens=1000)
)
```

---

## 动手示例

### 示例 1：低温度的数学导师

```python
from agents import Agent, ModelSettings, Runner

# Create a precise math tutor
math_tutor = Agent(
    name="Math Tutor",
    instructions="You are a precise math tutor. Always show your work step by step.",
    model_settings=ModelSettings(
        temperature=0.1,  # Very focused
        max_tokens=500    # Enough for detailed steps
    )
)

result = Runner.run_sync(math_tutor, "Solve: 2x + 5 = 13")
print(result.final_output)
```

### 示例 2：高温度的创意写作者

```python
creative_writer = Agent(
    name="Creative Writer",
    instructions="You are a creative storyteller. Write engaging, imaginative stories.",
    model_settings=ModelSettings(
        temperature=0.8,  # Very creative
        max_tokens=300    # Short but creative
    )
)

result = Runner.run_sync(creative_writer, "Write a short story about a robot learning to paint")
print(result.final_output)
```

### 示例 3：使用工具的助手

```python
from agents import function_tool

@function_tool
def calculate_area(length: float, width: float) -> str:
    """Calculate the area of a rectangle."""
    area = length * width
    return f"Area = {length} 脳 {width} = {area} square units"

# Agent that MUST use tools
tool_user = Agent(
    name="Tool User",
    instructions="You are a helpful assistant. Always use tools when available.",
    tools=[calculate_area],
    model_settings=ModelSettings(tool_choice="required")
)

result = Runner.run_sync(tool_user, "What's the area of a 5x3 rectangle?")
print(result.final_output)
```

---

## 高级设置（后面再学）

### 并行工具调用

```python
# Agent can use multiple tools at once
parallel_agent = Agent(
    name="Multi-Tasker",
    tools=[weather_tool, calculator, translator],
    model_settings=ModelSettings(
        tool_choice="auto",
        parallel_tool_calls=True  # Use multiple tools simultaneously
    )
)

# Agent uses tools one at a time
sequential_agent = Agent(
    name="One-at-a-Time",
    tools=[weather_tool, calculator, translator],
    model_settings=ModelSettings(
        tool_choice="auto",
        parallel_tool_calls=False  # Use tools one by one
    )
)
```

### Top-P 和惩罚项

```python
# More focused vocabulary
focused_agent = Agent(
    name="Focused",
    model_settings=ModelSettings(
        top_p=0.3,              # Use only top 30% of vocabulary
        frequency_penalty=0.5,   # Avoid repeating words
        presence_penalty=0.3     # Encourage new topics
    )
)
```

---

## 什么时候使用这些设置

| 设置 | 适用场景 | 示例 |
|---------|----------|---------|
| **低 Temperature** | 需要精确、一致的回答 | 数学题、事实核查 |
| **高 Temperature** | 希望回答更有创意、更多样 | 故事写作、头脑风暴 |
| **Tool Choice: Required** | 希望强制使用工具 | 数据分析、计算 |
| **Tool Choice: None** | 希望只聊天，不调用工具 | 日常对话 |
| **低 Max Tokens** | 需要简短回答 | 快速问答、摘要 |
| **高 Max Tokens** | 需要详细解释 | 教程、文档说明 |

---

## 学习路径

1. **先学简单的**：先用 `temperature` 和 `max_tokens`
2. **再加入工具**：尝试 `tool_choice`
3. **继续进阶**：试试 `parallel_tool_calls` 和各种 penalty
4. **真正掌握**：组合多个设置来得到理想结果

---

## 实用建议

- **先使用默认值**：除非有需要，否则不要急着改设置
- **每次只调一个参数**：这样更容易看出变化
- **记录你的设置**：记下不同任务下哪些配置效果更好
- **结合任务场景思考**：不同任务需要不同设置

---

## 下一步

- 运行 `hello_agent/` 目录中的示例
- 自己尝试不同的设置组合

---

*记住：Model settings 就像做饭时的调味料，用一点点就会有明显变化，搭配得对，结果就完全不同。*
