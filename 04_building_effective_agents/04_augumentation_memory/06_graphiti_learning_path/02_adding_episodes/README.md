# 第 02 步：[Adding Episodes](https://help.getzep.com/graphiti/core-concepts/adding-episodes) - 三种数据类型

现在你已经完成了第一个 Graphiti 程序，接下来要真正掌握 episodes。它是 Graphiti 吞入和处理信息的基础机制。

## 你将学到什么

完成这一节后，你将能够：

- 掌握三种 episode 类型：`text`、`message` 和 `json`
- 理解在不同教学场景下，应该精确地选择哪一种类型
- 处理批量 episode 加载以提升性能
- 理解 episode 如何经过 LLM 处理，最终变成可搜索的知识

## 前置要求

- 已完成 Step 01（Hello World）
- Graphiti client 已经能正常工作，并支持基础搜索
- 理解异步 Python 编程

## 什么是 Episodes？

### 核心概念

**Episode** 是 Graphiti 摄取信息的主要方式。你可以把一个 episode 理解为：在某个特定时间发生的一次“事件”或“一段信息”。

**关键特性：**

- **Episode 本身也是节点**，它们会成为知识图谱的一部分
- **具备时间跟踪能力**，每个 episode 都带有 `reference_time`
- **具备可追溯性（Provenance）**，你可以追踪任何被抽取出来的知识最初来自哪里
- **经过 LLM 处理**，episode 会被分析并抽取出实体和关系

### Episode 是如何工作的

1. **你添加一个 episode** → 原始信息进入 Graphiti
2. **LLM 处理这个 episode** → 抽取实体（人、概念、事物）和关系
3. **知识图谱增长** → 创建新的节点和边
4. **所有内容保持连接** → 被抽取出的实体会通过 `MENTIONS` 边回连到原始 episode

### 三种 Episode 类型

Graphiti 支持三种 episode 类型，它们分别针对不同的数据结构做了优化。

## `Text Episodes` - 用于叙述性内容

**适用场景：** 故事、描述、报告、文章、学习内容、学生反思  
**最适合：** 非结构化叙述内容，需要系统自动做实体抽取

```python
await graphiti.add_episode(
    name="student_background",
    episode_body=(
        "Alice Chen is a 22-year-old biology student who enrolled in Python 101. "
        "She has excellent analytical skills from her science background but has "
        "never programmed before. Alice wants to learn Python to analyze DNA "
        "sequences and biological data for her research."
    ),
    source=EpisodeType.text,
    source_description="Student enrollment system",
    reference_time=datetime.now()
)
```

**Graphiti 会抽取什么：**

- 实体：`Alice Chen`、`Python 101`、`biology`、`DNA sequences`
- 关系：`Alice ENROLLED_IN Python 101`、`Alice STUDIES biology`
- 时间上下文：这些信息是在什么时候被记录的

## `Message Episodes` - 用于对话内容

**适用场景：** 对话、聊天、辅导过程、访谈、问答环节  
当使用 `EpisodeType.message` 时，可以把多轮对话一起塞进 `episode_body`。文本需要按 `{role/name}: {message}` 的格式组织。

**格式要求：** 必须使用 `Speaker: Message` 模式，这一点很关键。

```python
await graphiti.add_episode(
    name="tutoring_session",
    episode_body=(
        "Student: I don't understand Python loops\n"
        "Tutor: Let's start with a simple example. What do you want to repeat?\n"
        "Student: I want to count DNA bases in a sequence\n"
        "Tutor: Perfect! A for loop is ideal for that task\n"
        "Student: Can you show me the syntax?\n"
        "Tutor: Sure! for base in dna_sequence:"
    ),
    source=EpisodeType.message,
    source_description="Online tutoring platform",
    reference_time=datetime.now()
)
```

**Graphiti 会抽取什么：**

- 参与者：`Student`、`Tutor`
- 讨论主题：`Python loops`、`DNA bases`、`for loop syntax`
- 学习进展：学生的困惑 → 导师的引导 → 理解逐步建立
- 对话流以及教学互动关系

## `JSON Episodes` - 用于结构化数据

**适用场景：** 数据库记录、API 响应、测评结果、结构化系统数据  
**最适合：** 你已经拥有结构化数据，并希望系统精确保留其结构时使用

```python
assessment_data = {
    "student_id": "alice_chen_001",
    "student_name": "Alice Chen",
    "course": "Python 101",
    "assessment_type": "loops_quiz",
    "date": "2024-01-15",
    "score": 88,
    "max_score": 100,
    "time_spent_minutes": 35,
    "questions_correct": 7,
    "questions_total": 8,
    "topics_tested": ["for_loops", "while_loops", "nested_loops"],
    "strengths": ["basic_loop_syntax", "iteration_logic"],
    "needs_improvement": ["nested_loop_complexity"],
    "instructor_notes": "Great progress! Ready for functions next."
}

await graphiti.add_episode(
    name="alice_loops_assessment",
    episode_body=assessment_data,
    source=EpisodeType.json,
    source_description="Learning management system",
    reference_time=datetime.now()
)
```

**Graphiti 会抽取什么：**

- 结构化关系：`Alice SCORED 88 ON loops_quiz`
- 表现指标：分数、耗时、主题掌握情况
- 学习洞察：优势点和待改进点
- 时间演化信息：测评发生的时间线

## 完整可运行示例

下面构建一个完整的教学场景示例，演示三种 episode 类型如何共同工作。

### main.py

```python
import asyncio
import os
import json

from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv

from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType

# Gemini setup (same as Step 01)
from graphiti_core.llm_client.gemini_client import GeminiClient, LLMConfig
from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig
from graphiti_core.cross_encoder.gemini_reranker_client import GeminiRerankerClient

load_dotenv(find_dotenv())


async def main():
    """Complete example using all three episode types"""

    # Initialize Graphiti (same setup as Step 01)
    graphiti = Graphiti(
        os.environ.get('NEO4J_URI', 'bolt://localhost:7687'),
        os.environ.get('NEO4J_USER', 'neo4j'),
        os.environ.get('NEO4J_PASSWORD', 'password'),
        llm_client=GeminiClient(
            config=LLMConfig(
                api_key=os.environ.get('GEMINI_API_KEY'),
                model="gemini-2.5-flash"
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
                model="gemini-2.0-flash"
            )
        )
    )

    try:
        await graphiti.build_indices_and_constraints()
        print("🚀 Starting Episode Types Demo...")

        # 3. JSON EPISODE - Assessment results
        print("📊 Adding JSON episode (assessment data)...")
        assessment_result = {
            "student_id": "alice_chen_001",
            "student_name": "Alice Chen",
            "course": "Python 101",
            "assessment_type": "loops_quiz",
            "date": "2024-01-15",
            "score": 88,
            "max_score": 100,
            "time_spent_minutes": 35,
            "questions_correct": 7,
            "questions_total": 8,
            "topics_tested": ["for_loops", "while_loops", "nested_loops"],
            "strengths": ["basic loop syntax", "iteration logic"],
            "needs_improvement": ["nested loop complexity"],
            "instructor_notes": "Great progress! Ready for functions next."
        }

        await graphiti.add_episode(
            name="alice_loops_assessment",
            episode_body=json.dumps(assessment_result),
            source=EpisodeType.json,
            source_description="Assessment system results",
            reference_time=datetime.now() - timedelta(days=1),
        )

        print("✅ All episodes added successfully!")

        # Specific searches by type
        print("\n🎯 Searching for alice tutoring interactions...")
        tutoring_results = await graphiti.search(
            query="What is alice confusion",
            num_results=5,
        )

        print(f"Tutoring insights: {len(tutoring_results)} results")
        for result in tutoring_results[:3]:
            print(f"  • {result.fact}")

        print("\n🎓 Episode types demo completed!")

    finally:
        await graphiti.close()
        print("Connection closed.")

if __name__ == "__main__":
    asyncio.run(main())
```

## 运行示例

1. **把代码保存为** `main.py`
2. **确保第 01 步的环境已经可用**
3. **运行程序**：

```bash
uv run python main.py
```

## 预期输出

```text
🚀 Starting Episode Types Demo...
📊 Adding JSON episode (assessment data)...
✅ All episodes added successfully!

🎯 Searching for alice tutoring interactions...
Tutoring insights: 5 results
  • student_id: alice_chen_001
  • questions_total: 8
  • questions_correct: 7

🎓 Episode types demo completed!
Connection closed.
```

## 自己动手试一试

### 练习 1：增加更多 Episode 类型

为不同的教学场景创建你自己的 episodes。

### 练习 2：理解 Episode 是怎么被处理的

先添加 episodes，然后再搜索，观察系统究竟抽取出了哪些知识。

## 批量加载 Episode

当数据量很大时，应该使用批量加载方式来提高效率。

## 选择指南：什么时候用哪一种 Episode 类型？

| 你的数据 | Episode 类型 | 原因 | 示例 |
|-----------|--------------|------|------|
| 学生作文、反思、叙述性描述 | `text` | 上下文丰富，需要做实体抽取 | `"Alice reflected on her learning journey..."` |
| 辅导对话、课堂讨论、问答 | `message` | 保留说话人关系和对话流程 | `"Student: I'm confused\nTutor: Let me help"` |
| 成绩记录、测评结果、结构化日志 | `json` | 结构精确，不希望引入歧义 | `{"student": "Alice", "score": 95}` |
| 混合内容（叙述 + 数据） | `text` | 把结构化部分转成叙述形式 | `"Alice scored 95% and felt confident about..."` |
| 邮件或论坛帖子 | `text` 或 `message` | 取决于格式；如果天然符合 `Speaker: Message` 就用 `message` | 根据结构来决定 |

## Episode 是如何变成知识的？

### 处理流水线

1. **创建 Episode** → 你把原始信息交给系统
2. **LLM 分析** → Graphiti 的 LLM 抽取实体和关系
3. **更新知识图谱** → 创建新的节点和边
4. **形成可搜索知识** → 信息变得可查询、可发现

#### 例子：Text Episode 的处理过程

**Graphiti 会抽取：**

- **实体**：`Alice Chen`、`Python loops quiz`、`functions`、`92%`
- **关系**：`Alice SCORED 92% ON Python loops quiz`、`Alice READY_FOR functions`
- **时间上下文**：这次成绩发生在什么时候
- **来源信息**：这些知识和原始 episode 是如何关联的

### 搜索能力

处理完成后，你可以搜索：

- `"Alice performance"` → 找到她的测评结果
- `"students ready for functions"` → 找出已经具备该阶段能力的学生
- `"Python loops assessments"` → 找到所有与 loops 有关的评估
- `"92 percent scores"` → 找出高表现学生

## 验证清单

- [ ] 三种 episode 类型都添加成功
- [ ] 搜索能返回来自不同 episode 类型的结果
- [ ] `message` 类型保留了说话人关系
- [ ] `json` 类型准确保留了结构化数据
- [ ] 搜索结果中能看出时间推进

## 常见问题

**Q: 同一件事可以混用不同 episode 类型吗？**  
A: 可以。例如，一次辅导课你既可以用 `text` 保存叙述性总结，也可以用 `json` 保存其中的结构化测评数据。

**Q: 如果我的对话不是 `Speaker: Message` 格式怎么办？**  
A: 你可以先把它转换成这种格式后再用 `message`，或者直接用 `text`，以叙述方式描述这段对话。

**Q: 怎么判断我的 JSON 会不会太复杂？**  
A: 如果你遇到 context window 错误，说明 JSON 太大了。应把大 JSON 拆成多个更聚焦的小 episode。

**Q: 成绩数据应该用 `text` 还是 `json`？**  
A: 如果是纯数据，例如分数、日期、ID，优先用 `json`；如果你还想表达上下文，例如 “Alice 一开始很吃力，但后来提升很大”，那就更适合用 `text`。

## 下一步

继续前往 **[03_custom_types](../03_custom_types/)**，你将学习如何定义自定义实体和关系，例如 `Student`、`Course` 和 `ENROLLED_IN`，而不是只使用通用节点和边。
