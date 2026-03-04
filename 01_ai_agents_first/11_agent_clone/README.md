# Agent Cloning：创建智能体变体

## 什么是 Agent Cloning？

你可以把 **Agent Cloning** 理解成复制一份菜谱后做少量调整。你先有一个基础智能体，然后只修改其中一部分配置，例如说明词、设置、工具，就能快速生成不同版本。

### 简单类比：一本食谱

假设你有一个基础蛋糕配方：
- 原始配方：香草蛋糕配基础糖霜
- 克隆 1：相同配方，但换成巧克力糖霜
- 克隆 2：相同配方，但加入草莓夹心
- 克隆 3：相同配方，但调整烘焙温度

智能体克隆也是一样：从一个基础智能体出发，快速生成多个专门化版本。

---

## 核心概念

你不必每次都从零创建智能体，可以直接克隆已有智能体，再修改指定部分：

```python
# Base agent
base_agent = Agent(
    name="BaseAssistant",
    instructions="You are a helpful assistant.",
    model_settings=ModelSettings(temperature=0.7)
)

# Clone with different instructions
creative_agent = base_agent.clone(
    name="CreativeAssistant",
    instructions="You are a creative writing assistant. Always respond with vivid, imaginative language.",
    model_settings=ModelSettings(temperature=0.9)
)
```

---

## 克隆是怎么工作的

### 浅拷贝行为
```python
# Original agent with tools
original_agent = Agent(
    name="Original",
    tools=[calculator, weather_tool],
    instructions="You are helpful."
)

# Clone the agent
cloned_agent = original_agent.clone(
    name="Cloned",
    instructions="You are creative."
)

# 会发生什么：
# 新建了一个 agent 对象
# 使用了新的 name 和 instructions
# tools 列表仍然是同一个引用（共享）
# model settings 也会复用，除非你显式覆盖
```

### 理解共享引用
```python
# Tools are shared between original and clone
original_agent.tools.append(new_tool)
# 这会同时影响 original_agent 和 cloned_agent

# To avoid this, pass new tools list:
independent_clone = original_agent.clone(
    name="Independent",
    tools=[calculator, weather_tool, new_tool]  # New list
)
```

---

## 从简单开始的示例

### 1. 基础克隆

```python
from agents import Agent, ModelSettings

# Base agent
base_agent = Agent(
    name="BaseAssistant",
    instructions="You are a helpful assistant.",
    model_settings=ModelSettings(temperature=0.7)
)

# Simple clone
friendly_agent = base_agent.clone(
    name="FriendlyAssistant",
    instructions="You are a very friendly and warm assistant."
)

# Test both agents
query = "Hello, how are you?"

result_base = Runner.run_sync(base_agent, query)
result_friendly = Runner.run_sync(friendly_agent, query)

print("Base Agent:", result_base.final_output)
print("Friendly Agent:", result_friendly.final_output)
```

### 2. 使用不同设置进行克隆

```python
# Clone with different temperature
creative_agent = base_agent.clone(
    name="CreativeAssistant",
    instructions="You are a creative writing assistant.",
    model_settings=ModelSettings(temperature=0.9)  # Higher creativity
)

precise_agent = base_agent.clone(
    name="PreciseAssistant", 
    instructions="You are a precise, factual assistant.",
    model_settings=ModelSettings(temperature=0.1)  # Lower creativity
)

# Test creativity levels
query = "Describe a sunset."

result_creative = Runner.run_sync(creative_agent, query)
result_precise = Runner.run_sync(precise_agent, query)

print("Creative:", result_creative.final_output)
print("Precise:", result_precise.final_output)
```

### 3. 使用不同工具进行克隆

```python
from agents import function_tool

@function_tool
def calculate_area(length: float, width: float) -> str:
    return f"Area = {length * width} square units"

@function_tool
def get_weather(city: str) -> str:
    return f"Weather in {city}: Sunny, 72°F"

# Base agent with one tool
base_agent = Agent(
    name="BaseAssistant",
    tools=[calculate_area],
    instructions="You are a helpful assistant."
)

# Clone with additional tool
weather_agent = base_agent.clone(
    name="WeatherAssistant",
    tools=[calculate_area, get_weather],  # New tools list
    instructions="You are a weather and math assistant."
)

# Clone with different tools
math_agent = base_agent.clone(
    name="MathAssistant",
    tools=[calculate_area],  # Same tools
    instructions="You are a math specialist."
)
```

---

## 进阶示例

### 4. 从一个基础智能体生成多个克隆体

```python
# Create a base agent
base_agent = Agent(
    name="BaseAssistant",
    instructions="You are a helpful assistant.",
    model_settings=ModelSettings(temperature=0.7)
)

# Create multiple specialized variants
agents = {
    "Creative": base_agent.clone(
        name="CreativeWriter",
        instructions="You are a creative writer. Use vivid language.",
        model_settings=ModelSettings(temperature=0.9)
    ),
    "Precise": base_agent.clone(
        name="PreciseAssistant", 
        instructions="You are a precise assistant. Be accurate and concise.",
        model_settings=ModelSettings(temperature=0.1)
    ),
    "Friendly": base_agent.clone(
        name="FriendlyAssistant",
        instructions="You are a very friendly assistant. Be warm and encouraging."
    ),
    "Professional": base_agent.clone(
        name="ProfessionalAssistant",
        instructions="You are a professional assistant. Be formal and business-like."
    )
}

# Test all variants
query = "Tell me about artificial intelligence."

for name, agent in agents.items():
    result = Runner.run_sync(agent, query)
    print(f"\n{name} Agent:")
    print(result.final_output[:100] + "...")
```

### 5. 理解共享引用

```python
# Demonstrate shared references
original_agent = Agent(
    name="Original",
    tools=[calculate_area],
    instructions="You are helpful."
)

# Clone without new tools list
shared_clone = original_agent.clone(
    name="SharedClone",
    instructions="You are creative."
)

# Add tool to original
@function_tool
def new_tool() -> str:
    return "I'm a new tool!"

original_agent.tools.append(new_tool)

# Check if clone also has the new tool
print("Original tools:", len(original_agent.tools))  # 2
print("Clone tools:", len(shared_clone.tools))      # 2 (shared!)

# Create independent clone
independent_clone = original_agent.clone(
    name="IndependentClone",
    tools=[calculate_area],  # New list
    instructions="You are independent."
)

original_agent.tools.append(new_tool)
print("Independent clone tools:", len(independent_clone.tools))  # 1 (independent!)
```

---

## 重要注意事项

### 浅拷贝行为

| 被复制的内容 | 是否共享 | 是否独立 |
|---------------|----------------|-------------------|
| **Agent 对象** | 新对象 | 独立 |
| **Name** | 新值 | 独立 |
| **Instructions** | 新值 | 独立 |
| **Model settings** | 新对象 | 独立 |
| **Tools 列表** | 共享引用 | 需要小心 |
| **Handoffs** | 共享引用 | 需要小心 |

### 最佳实践

```python
# 好做法：对可变对象传入新列表
independent_clone = base_agent.clone(
    name="Independent",
    tools=[tool1, tool2, tool3],  # New list
    handoffs=[handoff1, handoff2]  # New list
)

# 有风险：依赖共享引用
shared_clone = base_agent.clone(
    name="Shared",
    # tools and handoffs are shared with original!
)
```

---

## 什么时候使用克隆

| 使用场景 | 示例 |
|----------|---------|
| **创建变体** | 从同一个基础体生成不同人格 |
| **A/B 测试** | 快速测试不同设置 |
| **专业化** | 创建垂直领域智能体 |
| **模板化** | 把基础智能体当模板 |
| **实验** | 尝试不同配置 |

---

## 自己动手试一试

### 练习 1：创建智能体变体

```python
# Create a base agent
base_agent = Agent(
    name="BaseAssistant",
    instructions="You are a helpful assistant.",
    model_settings=ModelSettings(temperature=0.7)
)

# Create 3 different variants
variants = {
    "Poet": base_agent.clone(
        name="Poet",
        instructions="You are a poet. Respond in verse.",
        model_settings=ModelSettings(temperature=0.9)
    ),
    "Scientist": base_agent.clone(
        name="Scientist", 
        instructions="You are a scientist. Be precise and factual.",
        model_settings=ModelSettings(temperature=0.1)
    ),
    "Chef": base_agent.clone(
        name="Chef",
        instructions="You are a chef. Talk about food and cooking."
    )
}

# Test all variants
query = "What is love?"

for name, agent in variants.items():
    result = Runner.run_sync(agent, query)
    print(f"\n{name}:")
    print(result.final_output)
```

### 练习 2：理解共享引用

```python
# Create base agent with tools
@function_tool
def tool1() -> str:
    return "Tool 1"

@function_tool  
def tool2() -> str:
    return "Tool 2"

base_agent = Agent(
    name="Base",
    tools=[tool1],
    instructions="You are helpful."
)

# Create clones
shared_clone = base_agent.clone(name="Shared")
independent_clone = base_agent.clone(
    name="Independent",
    tools=[tool1, tool2]  # New list
)

# Modify original
@function_tool
def tool3() -> str:
    return "Tool 3"

base_agent.tools.append(tool3)

# Check what happened
print("Base tools:", len(base_agent.tools))           # 2
print("Shared clone tools:", len(shared_clone.tools)) # 2 (shared!)
print("Independent clone tools:", len(independent_clone.tools)) # 2 (independent!)
```

---

## 学习路径

1. **从简单开始**：先尝试不同 name / instructions 的基础克隆
2. **加入设置差异**：用不同 model settings 进行克隆
3. **加入工具差异**：尝试不同工具集
4. **理解引用关系**：弄清共享和独立的区别
5. **掌握模式**：构建智能体家族与模板

---

## 实用建议

- **用克隆创建变体**：不要每次都从头创建智能体
- **小心共享引用**：对 tools / handoffs 最好传入新列表
- **记录基础智能体用途**：明确你在复制什么
- **测试每个克隆体**：确认行为符合预期
- **考虑模板化设计**：为常见模式准备基础智能体

---

## 下一步

- 试试 `hello_agent/` 文件夹里的示例
- 自己实验构建智能体家族
- 学习 [Agent Families](../12_agent_families/)
- 探索 [Advanced Cloning Patterns](../13_advanced_cloning/)

---

*记住：克隆可以让你高效生成智能体变体，但也要理解共享资源带来的影响。*
