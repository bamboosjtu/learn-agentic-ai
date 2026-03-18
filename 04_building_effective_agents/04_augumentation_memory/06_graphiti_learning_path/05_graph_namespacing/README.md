# 第 05 步：[Graph Namespacing](https://help.getzep.com/graphiti/core-concepts/graph-namespacing) - 多租户教育系统

Graphiti 通过 `group_id` 参数支持图命名空间（graph namespacing）的概念。这个能力允许你在同一个 Graphiti 实例中创建彼此隔离的图环境，从而让多个不同的知识图谱并存，而互不干扰。

既然你已经理解了 communities，接下来就来学习如何使用 `group_id` 为多租户系统创建隔离的教育环境。Graph namespacing 尤其适用于：

- 多租户应用：隔离不同客户或组织之间的数据
- 测试环境：分别维护开发、测试、生产图环境
- 领域专属知识：为不同领域或用例建立独立图谱
- 团队协作：让不同团队在各自图空间里工作

## 核心概念

Graphiti 中的 **graph namespacing** 是通过 `group_id` 参数来实现的。它会在同一个 Graphiti 实例中创建逻辑隔离的图环境，使多个不同的知识图谱可以共存而不互相影响。

**教育场景中的典型用例：**

- **多机构平台**：不同学校共用同一套 TutorsGPT 系统
- **课程隔离**：把 CS101 和 MATH201 的图谱完全分开
- **学期隔离**：例如 2024 秋季 和 2025 春季 两批学生群体分开
- **隐私边界**：为 FERPA 合规提供学生数据隔离
- **测试环境**：分离开发、测试和生产图环境

### Namespacing 的工作方式

在 Graphiti 中，每个节点和边都可以关联一个 `group_id`。当你指定 `group_id` 时，本质上是在为这部分数据指定一个命名空间。拥有相同 `group_id` 的节点和边会组成一个独立且一致的图，可以被单独查询和操作。

### 在 Graphiti 中使用 group_id

**给 Episode 加上 group_id：**

```python
await graphiti.add_episode(
    name="student_progress",
    episode_body="Alice completed her Python assignment...",
    source=EpisodeType.text,
    group_id="university_a_cs101_fall2024"  # 独立命名空间
)
```

**给 Fact Triples 加上 group_id：**

```python
# 确保两个节点和边拥有相同的 group_id
await graphiti.add_triplet(source_node, edge, target_node)
# 其中三个组件都带相同的 group_id
```

**在某个命名空间内查询：**

```python
# 只在特定 namespace 内搜索
search_results = await graphiti.search(
    query="programming concepts",
    group_id="university_a_cs101_fall2024"  # 只搜这个 namespace
)
```

## 简单 Namespacing 示例

下面创建两个独立课程环境，看看 `group_id` 是如何把它们隔离开的。

### namespacing_demo.py

```python
import asyncio
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv

from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType

from graphiti_core.llm_client.gemini_client import GeminiClient, LLMConfig
from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig
from graphiti_core.cross_encoder.gemini_reranker_client import GeminiRerankerClient

load_dotenv(find_dotenv())

async def main():
    """Simple namespace isolation demo"""
    
    # Initialize Graphiti (same setup as previous steps)
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
                model="gemini-2.0-flash-lite"
            )
        )
    )
    
    try:
        await graphiti.build_indices_and_constraints()
        print("🏫 Namespacing Demo - Creating Isolated Course Environments...")
        
        # Course A: CS101 
        print("\n📘 Adding CS101 episodes...")
        await graphiti.add_episode(
            name="cs101_alice",
            episode_body="Alice is learning Python basics in CS101. She understands variables and loops.",
            source=EpisodeType.text,
            source_description="CS101 student background",
            group_id="course_cs101",  # CS101 namespace
            reference_time=datetime.now() - timedelta(days=2)
        )
        
        await graphiti.add_episode(
            name="cs101_bob",
            episode_body="Bob is struggling with Python functions in CS101. He needs help with parameters.",
            source=EpisodeType.text,
            source_description="CS101 student background",
            group_id="course_cs101",  # CS101 namespace
            reference_time=datetime.now() - timedelta(days=1)
        )

        await asyncio.sleep(60)
        
        # Course B: MATH201
        print("📗 Adding MATH201 episodes...")
        await graphiti.add_episode(
            name="math201_carol",
            episode_body="Carol is studying calculus in MATH201. She excels at derivatives and integration.",
                source=EpisodeType.text,
            source_description="MATH201 student background",
            reference_time=datetime.now() - timedelta(days=3),
            group_id="course_math201"  # MATH201 namespace
        )
        
        await graphiti.add_episode(
            name="math201_diana",
            episode_body="Diana finds linear algebra challenging in MATH201. She needs help with matrices.",
            source=EpisodeType.text,
            source_description="MATH201 student background",
            reference_time=datetime.now() - timedelta(days=2),
            group_id="course_math201"  # MATH201 namespace
        )
        
        print("✅ Episodes added to separate namespaces!")
        await asyncio.sleep(60)
        
        # Search within CS101 namespace only
        print("\n🔍 Searching within CS101 namespace...")
        cs101_results = await graphiti.search(
            query="programming Python students learning",
            group_ids=["course_cs101"],  # 只搜 CS101
            num_results=10
        )
        
        print(f"CS101 results: {len(cs101_results)} found")
        for result in cs101_results:
            print(f"  • {result.fact}")
        
        # Search within MATH201 namespace only
        print("\n🔍 Searching within MATH201 namespace...")
        math201_results = await graphiti.search(
            query="mathematics calculus students learning",
            group_ids=["course_math201"],  # 只搜 MATH201
            num_results=10
        )
        
        print(f"MATH201 results: {len(math201_results)} found")
        for result in math201_results:
            print(f"  • {result.fact}")
        
        # Global search (no group_id) - sees everything
        print("\n🌍 Global search (no namespace restriction)...")
        global_results = await graphiti.search(
            query="students learning",
            num_results=10  # 不传 group_id = 搜全部 namespace
        )
        
        print(f"Global results: {len(global_results)} found")
        for result in global_results:
            print(f"  • {result.fact}")
        
        print("\n🎓 Namespacing demo completed!")
        print("\n👀 Now manually explore namespaces in Neo4j...")
        
    finally:
        await graphiti.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## 运行示例

```bash
uv run python namespacing_demo.py
```

## 预期输出

```text
🏫 Namespacing Demo - Creating Isolated Course Environments...

📘 Adding CS101 episodes...
📗 Adding MATH201 episodes...
✅ Episodes added to separate namespaces!

🔍 Searching within CS101 namespace...
CS101 results: 9 found
  • Alice is learning Python basics in CS101
  • Alice is learning Python basics
  • Python functions in CS101
  • Python functions... parameters
  • Bob is struggling with Python functions
  • Bob is in CS101
  • She understands variables
  • He needs help with parameters
  • She understands loops

🔍 Searching within MATH201 namespace...
MATH201 results: 8 found
  • calculus in MATH201
  • Carol is studying calculus
  • Carol is studying in MATH201
  • linear algebra challenging in MATH201
  • Diana finds linear algebra challenging
  • She needs help with matrices
  • She excels at derivatives
  • She excels at integration

🌍 Global search (no namespace restriction)...
Global results: 10 found
  • Carol is studying in MATH201
  • calculus in MATH201
  • Carol is studying calculus
  • Alice is learning Python basics in CS101
  • Bob is in CS101
  • Alice is learning Python basics
  • linear algebra challenging in MATH201
  • She understands variables
  • Python functions in CS101
  • She needs help with matrices

🎓 Namespacing demo completed!

👀 Now manually explore namespaces in Neo4j...
```

## 在 Neo4j 中手动探索

打开 **Neo4j Browser**，执行下面这些查询来观察 namespace 的隔离效果：

### 1. 查看所有节点及其命名空间

```cypher
MATCH (n:Entity) 
RETURN n.name, n.group_id
ORDER BY n.group_id
```

```cypher
MATCH (n)
OPTIONAL MATCH (n)-[r]->(m)
RETURN n, r, m
```

这会展示每个实体及其所属的命名空间。

### 2. 查看 CS101 命名空间中的所有节点

```cypher
MATCH (n:Entity) 
MATCH (n)-[r]->(m)
WHERE n.group_id = "course_cs101"
RETURN n, r, m
```

这只会显示 CS101 中的实体。

## 常见问题

**Q: 如果我不指定 `group_id` 会怎样？**  
A: 该实体或 episode 会进入默认命名空间，并会出现在全局搜索中，也就是不带 `group_id` 的搜索里。

**Q: CS101 的学生能看到 MATH201 的数据吗？**  
A: 不能。这就是 namespacing 的核心价值：在课程之间提供完整隔离，用于隐私保护和数据组织。

**Q: 怎么跨多个指定 namespace 搜索？**  
A: 你通常需要分别对每个 namespace 做查询，然后在应用层把结果合并。

**Q: 为什么不用多个数据库，而要用 namespace？**  
A: namespace 更轻量，而且在需要时仍然支持做全局分析；同时又能保持隔离。

## 下一步

**做得很好。** 你现在已经理解了如何通过正确的数据隔离，构建可扩展且具备隐私边界的教育系统。

**准备掌握更高级的搜索方式了吗？** 接下来前往 **[06_searching](../06_searching/)**，学习 Graphiti 更强大的混合搜索能力和结果优化技巧。

**接下来会学到什么？**  
你将不再局限于基础搜索，而会开始掌握：

- 语义搜索
- 关键词搜索
- reranking 策略
- 针对教育场景优化的 search recipes

---

**关键结论：** 命名空间就像知识图谱里的“课程教室”。每门课都有自己的独立空间，但在需要时，你仍然可以做全校范围的分析。

_“命名空间解决的是多租户问题：在需要时提供完整隐私隔离，在适当场景下也保留全局洞察能力。”_
