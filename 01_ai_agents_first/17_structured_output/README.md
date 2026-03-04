# Structured Output：让智能体返回规范数据

## 什么是 Structured Output？

你可以把 Structured Output 理解成在餐厅按固定表单点餐。不是随口说一句“给我来点吃的”，而是填写一张明确的点单表，确保你能以正确格式拿到真正需要的数据。

### 简单类比：点单表

**没有 Structured Output（混乱）**：
- 你："Tell me about the weather"
- 智能体："It's pretty nice today, maybe around 75 degrees and sunny in New York"
- 你：我该怎么提取温度？城市是什么？是华氏还是摄氏？

**使用 Structured Output（规范）**：
- 你："Tell me about the weather"
- 智能体：`{"location": "New York", "temperature_c": 24, "summary": "sunny"}`
- 你：很好，我可以直接把这份数据接进应用里。

---

## 核心概念

**普通输出（不可预测）**：
```python
# Agent returns free-form text
result = Runner.run_sync(agent, "What's the weather in Karachi?")
print(result.final_output)
# "The weather in Karachi is quite warm today, around 30 degrees Celsius with clear skies."
```

**结构化输出（可预测）**：
```python
class WeatherAnswer(BaseModel):
    location: str
    temperature_c: float
    summary: str

agent = Agent(output_type=WeatherAnswer)
result = Runner.run_sync(agent, "What's the weather in Karachi?")

print(result.final_output.location)
print(result.final_output.temperature_c)
print(result.final_output.summary)
```

---

## Structured Output 是如何工作的

### 背后的机制

当你使用结构化输出时，智能体会：

1. **理解 Schema**：知道必须填哪些字段
2. **校验数据**：确保必填字段都存在
3. **保证格式正确**：按你指定的结构返回
4. **做类型检查**：例如保证 temperature 是数字，而不是文本

### Pydantic 模型：你的数据蓝图

| 组成部分 | 作用 | 示例 |
|-----------|-------------|---------|
| **类定义** | 创建数据结构 | `class WeatherInfo(BaseModel):` |
| **字段类型** | 指定数据类型 | `temperature: float` |
| **必填字段** | 默认必须存在 | 所有字段默认都是必填 |
| **可选字段** | 可以缺失 | `rainfall: Optional[float] = None` |

---

## 从简单开始的示例

### 1. 第一个 Structured Output

```python
from pydantic import BaseModel
from agents import Agent, Runner

class PersonInfo(BaseModel):
    name: str
    age: int
    occupation: str

agent = Agent(
    name="InfoCollector",
    instructions="Extract person information from the user's message.",
    output_type=PersonInfo
)

result = Runner.run_sync(
    agent, 
    "Hi, I'm Alice, I'm 25 years old and I work as a teacher."
)

print("Type:", type(result.final_output))
print("Name:", result.final_output.name)
print("Age:", result.final_output.age)
print("Job:", result.final_output.occupation)
```

### 2. 使用不同数据类型

```python
from typing import Optional, List
from datetime import datetime

class ProductInfo(BaseModel):
    name: str
    price: float
    in_stock: bool
    categories: List[str]
    discount_percent: Optional[int] = 0
    reviews_count: int

agent = Agent(
    name="ProductExtractor",
    instructions="Extract product information from product descriptions.",
    output_type=ProductInfo
)

result = Runner.run_sync(
    agent,
    "The iPhone 15 Pro costs $999.99, it's available in electronics and smartphones categories, currently in stock with 1,247 reviews."
)

print("Product:", result.final_output.name)
print("Price:", result.final_output.price)
print("In Stock:", result.final_output.in_stock)
print("Categories:", result.final_output.categories)
print("Reviews:", result.final_output.reviews_count)
```

## 真实应用场景

### 会议纪要提取器

```python
from datetime import datetime
from typing import List, Optional

class ActionItem(BaseModel):
    task: str
    assignee: str
    due_date: Optional[str] = None
    priority: str = "medium"

class Decision(BaseModel):
    topic: str
    decision: str
    rationale: Optional[str] = None

class MeetingMinutes(BaseModel):
    meeting_title: str
    date: str
    attendees: List[str]
    agenda_items: List[str]
    key_decisions: List[Decision]
    action_items: List[ActionItem]
    next_meeting_date: Optional[str] = None
    meeting_duration_minutes: int
```

---

## 自己动手试一试

### 练习 1：构建一个简历解析器

```python
from typing import List, Optional

class Education(BaseModel):
    degree: str
    institution: str
    graduation_year: int
    gpa: Optional[float] = None

class Experience(BaseModel):
    position: str
    company: str
    start_year: int
    end_year: Optional[int] = None
    responsibilities: List[str]

class Resume(BaseModel):
    full_name: str
    email: str
    phone: str
    summary: str
    education: List[Education]
    experience: List[Experience]
    skills: List[str]
    languages: List[str]
```

### 练习 2：创建一个菜谱分析器

```python
from typing import List, Optional

class Ingredient(BaseModel):
    name: str
    amount: str
    unit: str
    notes: Optional[str] = None

class NutritionInfo(BaseModel):
    calories_per_serving: Optional[int] = None
    prep_time_minutes: int
    cook_time_minutes: int
    difficulty_level: str = Field(..., regex=r'^(easy|medium|hard)$')

class Recipe(BaseModel):
    title: str
    description: str
    servings: int
    ingredients: List[Ingredient]
    instructions: List[str]
    nutrition: NutritionInfo
    cuisine_type: str
    dietary_tags: List[str]
```

---

*记住：结构化输出会让你的智能体从“输出杂乱文本”，升级为“稳定输出可直接使用的数据”。*
