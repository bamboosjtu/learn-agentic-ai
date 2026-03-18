# 第 03 步：[Custom Entity & Edge Types](https://help.getzep.com/graphiti/core-concepts/custom-entity-and-edge-types) - 让知识图谱真正贴合你的领域

Graphiti 支持你定义自定义实体类型（entity types）和边类型（edge types），从而更准确地表达领域知识。这会让知识图谱中的数据抽取更结构化，语义关系也更丰富。

现在你已经理解了 episodes，接下来要让你的知识图谱更精确：通过定义自定义类型，让它真正具备“领域感知能力”。这一节会继续复用你在 Step 01 已经学过的**记忆类型理论**，例如 STM、episodic、semantic、procedural memory，把理论直接映射到实践实现上。

## 你将学到什么

完成这一节后，你将能够：

- 定义基于记忆理论的实体类型，例如 `Student`、`MemoryEvent`
- 创建面向记忆建模的边类型，例如 `MemoryFormation`，并给它添加保持强度、形成时间等属性
- 使用 Pydantic 模型来表达 episodic、semantic、procedural 等记忆结构
- 把这些自定义类型应用到 episodes 上，从而获得更精准的知识抽取
- 看到 Step 01 里的理论是如何直接变成 Graphiti 中的工程实现的

## 为什么自定义类型很重要

### 泛型类型的问题

**如果没有自定义类型：**

```text
Generic entities: "person", "thing", "concept", "event"
Generic relationships: "relates_to", "connected_to", "associated_with"
```

**结果：** 图谱语义模糊、难以查询、很难真正表达领域知识。

### 自定义类型的价值

**如果使用自定义类型：**

```text
Educational entities: Student, Course, Instructor, Assignment, Skill
Educational relationships: ENROLLED_IN, TEACHES, COMPLETED, MASTERED, STRUGGLES_WITH
```

**结果：** 知识变得更精确、可查询、具备领域语义，也更能表达你正在建模的教学上下文。

### 核心收益

- **语义更精确**：能明确知道每个实体到底表示什么
- **属性更丰富**：可以存储领域专属信息，例如 GPA、学分、技能等级
- **查询效果更好**：可以查找更具体类型的信息
- **对 LLM 有引导作用**：帮助模型从 episode 中抽取更正确的实体和关系
- **类型安全**：可以提前校验数据结构，尽早发现错误

## 理解自定义类型的架构

### Entity Types 与 Edge Types 的区别

**Entity Types** 定义的是你领域中的“事物”：

- `Student`：学习者，可能带有 GPA、专业、学习风格等属性
- `Course`：课程，可能带有学分、难度、先修要求等属性
- `Instructor`：教师，可能带有经验、专业方向、所属院系等属性
- `Skill`：技能，可能带有难度等级、分类等属性

**Edge Types** 定义的是这些事物之间的“关系”：

- `Enrollment`：学生 ↔ 课程，可能带有成绩、学期、状态等属性
- `TeachingAssignment`：教师 ↔ 课程，可能带有授课时间、班级等属性
- `SkillDevelopment`：学生 ↔ 技能，可能带有熟练度、证据等属性
- `PrerequisiteRelationship`：课程 ↔ 课程，表示依赖或先修关系

### 使用 Pydantic 定义类型

Graphiti 使用 **Pydantic BaseModel** 来定义自定义类型。这样做的好处包括：

- **类型校验**：保证数据结构正确
- **丰富属性**：可以定义结构化字段和字段说明
- **文档化能力**：天然具备 schema 描述能力
- **IDE 友好**：支持自动补全和类型检查

因此，自定义 entity types 和 edge types 都是通过 Pydantic 模型定义的。每个模型代表一种具体类型，并带有自己的自定义属性。

想更深入理解，可以看这里：  
[Understand How it works?](https://help.getzep.com/graphiti/core-concepts/custom-entity-and-edge-types#how-custom-types-work)

## 完整可运行示例

下面通过一个例子来演示。

### custom_types_demo.py

```python
import asyncio
import os
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from dotenv import load_dotenv, find_dotenv

from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType

from graphiti_core.llm_client.gemini_client import GeminiClient, LLMConfig
from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig
from graphiti_core.cross_encoder.gemini_reranker_client import GeminiRerankerClient

load_dotenv(find_dotenv())

# === CUSTOM ENTITY TYPES (Based on Student Memory Types) ===

class Student(BaseModel):
    """A learner with memory capabilities"""
    learning_style: str | None = Field(None, description="Visual, auditory, kinesthetic, etc.")
    memory_preference: str | None = Field(None, description="Episodic, semantic, procedural")

class MemoryEvent(BaseModel):
    """A specific learning experience or memory"""
    memory_type: str | None = Field(None, description="STM, episodic, semantic, procedural")
    importance_level: str | None = Field(None, description="High, medium, low")

# === CUSTOM EDGE TYPES ===

class MemoryFormation(BaseModel):
    """Student forms memory relationship"""
    formation_date: str | None = Field(None, description="When memory was formed")
    retention_strength: str | None = Field(None, description="Strong, moderate, weak")

async def main():
    """Complete example using custom educational types"""
    
    # Initialize Graphiti (same setup as previous steps)
    graphiti = Graphiti(
        os.environ.get('NEO4J_URI', 'bolt://localhost:7687'),
        os.environ.get('NEO4J_USER', 'neo4j'),
        os.environ.get('NEO4J_PASSWORD', 'password'),
        llm_client=GeminiClient(
            config=LLMConfig(
                api_key=os.environ.get('GEMINI_API_KEY'),
                model="gemini-2.0-flash"
            )
        ),
        embedder=GeminiEmbedder(
            config=GeminiEmbedderConfig(
                api_key=os.environ.get('GEMINI_API_KEY'),
                embedding_model="embedding-001"
            )
        ),
        cross_encoder=GeminiRerankerClient(
            config=LLMConfig(
                api_key=os.environ.get('GEMINI_API_KEY'),
                model="gemini-2.0-flash-exp"
            )
        )
    )
    
    try:
        await graphiti.build_indices_and_constraints()
        print("🎓 Starting Custom Types Demo...")
        
        # Define our custom type mappings (memory-focused!)
        entity_types = {
            "Student": Student,
            "MemoryEvent": MemoryEvent
        }
        
        edge_types = {
            "MemoryFormation": MemoryFormation
        }
        
        # Define which edge types can exist between entity types
        edge_type_map = {
            ("Student", "MemoryEvent"): ["MemoryFormation"],
            ("Entity", "Entity"): ["RELATES_TO"]  # Fallback for unexpected relationships
        }
        
        # 1. SINGLE MEMORY FORMATION EPISODE with custom types
        print("\n🧠 Adding one memory formation episode...")
        await graphiti.add_episode(
            name="alice_memory_formation",
            episode_body=(
                "Alice Chen is a visual learner who prefers episodic memory formation. "
                "She formed a strong procedural memory about Python loops on October 15, 2024. "
                "This was a high-importance memory event that showed strong retention strength."
            ),
            source=EpisodeType.text,
            source_description="Student memory formation example",
            reference_time=datetime.now() - timedelta(days=30),
            entity_types=entity_types,
            edge_types=edge_types,
            edge_type_map=edge_type_map
        )
        
        print("✅ Episode with custom types added!")
        
        # SEARCH WITH CUSTOM TYPES
        print("\n🔍 Searching for custom type results...")
        
        # Simple search to see our memory-based custom types in action
        results = await graphiti.search(
            query="Alice Chen memory formation procedural episodic learning visual",
            num_results=6
        )
        
        print(f"\n🎯 Custom Type Results: {len(results)} found")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result.fact}")
        
        print("\n🎓 Custom types demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   1. Verify Pydantic models are properly defined")
        print("   2. Check that entity_types and edge_types dictionaries are correct")
        print("   3. Ensure edge_type_map covers your expected relationships")
        
    finally:
        await graphiti.close()
        print("Connection closed.")

if __name__ == "__main__":
    asyncio.run(main())
```

## 运行示例

```bash
uv run python main.py
```

## 预期输出

```text
🎓 Starting Custom Types Demo...

🧠 Adding one memory formation episode...
✅ Episode with custom types added!

🔍 Searching for custom type results...

🎯 Custom Type Results: 4 found
  1. Alice Chen is visual learner who prefers episodic memory formation
  2. Alice Chen formed strong procedural memory about Python loops
  3. Memory formation occurred on October 15, 2024 with high importance
  4. Memory event showed strong retention strength

🎓 Custom types demo completed successfully!
```

可以继续参考这里：  
[Best Practices for Defining Custom Entity and Edge Types](https://help.getzep.com/graphiti/core-concepts/custom-entity-and-edge-types#best-practices)

## 自己动手试一试

### 练习 1：加入 Semantic Memory 类型

试着增加一个 `SemanticMemory` 实体：

```python
class SemanticMemory(BaseModel):
    """Factual knowledge and concepts"""
    knowledge_domain: Optional[str] = Field(None, description="Programming, math, history, etc.")
    confidence_level: Optional[str] = Field(None, description="High, medium, low")

# Add to your types
entity_types["SemanticMemory"] = SemanticMemory
```

### 练习 2：增加一次 Memory Recall Episode

写一条关于“记忆提取”的 episode：

```python
await graphiti.add_episode(
    name="alice_memory_recall",
    episode_body="Alice recalled her semantic memory about Python syntax with high confidence. This programming knowledge helped her solve a new coding problem.",
    source=EpisodeType.text,
    entity_types=entity_types,
    edge_types=edge_types,
    edge_type_map=edge_type_map
)
```

## 关键概念解释

### 自定义类型如何引导 LLM 抽取

**如果没有 Custom Types：**

```text
"Alice formed memory about loops" → Generic entities: "person", "thing", "concept"
```

**如果有 Custom Types：**

```text
"Alice formed memory about loops" → Specific entities: Student("Alice"), MemoryEvent("Python loops")
                                 → Specific relationship: MemoryFormation(retention_strength="Strong")
```

### Edge Type Mapping 策略

`edge_type_map` 的作用，是告诉 Graphiti 哪些类型之间允许存在哪些关系：

```python
edge_type_map = {
    ("Student", "MemoryEvent"): ["MemoryFormation"],  # Students can form memories
    ("Entity", "Entity"): ["RELATES_TO"]              # Fallback for unexpected relationships
}
```

### 基于记忆理论的属性优势

这些自定义类型，直接对应你已经学过的记忆理论：

```python
# 不是只知道 "Alice learned something"
# 而是得到更丰富的记忆形成信息：
MemoryFormation(
    formation_date="2024-10-15",
    retention_strength="Strong"
)
```

## 验证清单

- [ ] 已定义两个基于记忆的实体类型：`Student`、`MemoryEvent`
- [ ] 已定义一个记忆关系类型：`MemoryFormation`
- [ ] `edge_type_map` 已覆盖 `Student-MemoryEvent` 之间的关系
- [ ] 已成功处理一条带自定义类型引导的记忆形成 episode
- [ ] 搜索结果能体现出记忆相关的实体和关系

## 常见问题

**Q: Episodes 和 Custom Types 的区别是什么？**  
A: Episode 是你输入的原始数据；Custom Types 决定 Graphiti 如何把这些原始数据抽取并组织成更精确的实体和关系。

**Q: 这和我学过的记忆理论是怎么对应起来的？**  
A: 这个例子直接复用了 Step 01 中的记忆概念，例如 episodic、semantic、procedural。也就是说，你是在把理论直接映射为 Graphiti 中的自定义类型。

**Q: 为什么这里用记忆类型，而不是一般的教学实体类型？**  
A: 因为你已经理解了记忆理论。这样做的好处是：你不需要从零理解新的抽象，而是可以直接把已知理论迁移到实际实现中。

## 你在这一节里学会了什么

✅ **基于记忆理论的自定义类型**：定义了两个记忆相关实体 `Student` 和 `MemoryEvent`，并和你熟悉的理论概念建立联系  
✅ **记忆关系建模**：创建了一个有明确语义的边类型 `MemoryFormation`，并带有记忆形成相关属性  
✅ **理论到实践的桥接**：把 agentic memory 理论真正落到 Graphiti 自定义类型实现中  
✅ **LLM 引导能力**：通过自定义类型帮助 Graphiti 更准确地抽取记忆形成模式  
✅ **熟悉的认知基础**：整个设计都建立在你已经理解的 STM、episodic、semantic、procedural 上

## 下一步

**做得很好。** 现在你已经能够构建“精确、领域化”的知识图谱，而不只是泛型的实体和关系。

**准备好让图谱自动发现模式了吗？** 接下来前往 **[04_communities](../04_communities/)**，你将学习 Graphiti 如何自动识别知识图谱中的群组和簇结构。

**下一步会看到什么？**  
你不再需要手动整理信息。Graphiti 会开始自动发现：

- 哪些学生在相似主题上存在相似困难
- 哪些教学方法经常一起发挥作用
- 哪些知识结构天然会形成群组

---

**关键结论：** 把新知识建立在你已经理解的理论基础上。使用你在 Step 01 学过的记忆类型，会让 Graphiti 的 custom types 立刻变得熟悉且实用。

🔧 **学习挑战：手动插入数据，而不是交给 LLM 抽取**  
有些数据你并不希望交给 LLM 来“猜”或“抽取”，例如 `student_id`、`course_code`、`topic_id`。这些是系统级标识符，更适合由你**手动控制**。

_“最好的学习方式，是让新的技术能力建立在你已经真正理解的理论基础之上。”_
