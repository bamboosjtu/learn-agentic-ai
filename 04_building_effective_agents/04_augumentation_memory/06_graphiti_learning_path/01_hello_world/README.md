# 第 01 步：Hello World - 你的第一个 Graphiti 程序

欢迎来到 Graphiti！在这一步中，你将创建自己的第一个时序知识图谱，并亲眼看到它是如何工作的。

## 官方文档

- [Graphiti Getting Started](https://help.getzep.com/graphiti/getting-started/welcome) - Graphiti 官方入门介绍
- [Quick Start Guide](https://help.getzep.com/graphiti/getting-started/quick-start) - Graphiti Core 快速配置指南
- [Gemini Config](https://help.getzep.com/graphiti/configuration/llm-configuration)

## 你将学到什么

完成这一节后，你将能够：

- 安装并配置 Graphiti
- 添加第一条 episode，创建知识图谱
- 搜索图谱并取回信息
- 理解 Graphiti 的基础工作流：文本 → 图谱 → 搜索

## 前置要求

- 已安装 Python 3.10+
- 有一个运行中的 Neo4j 数据库（本地或 AuraDB）
- Gemini API Key
- 具备基础 Python 知识

## 环境准备

### 1. 初始化项目并安装 Graphiti

```bash
uv init hello_tkg

uv add "graphiti-core[google-genai]"
```

### 2. 环境变量

创建一个 `.env` 文件，或者导出以下变量：

```bash
GEMINI_API_KEY="your-openai-api-key"
NEO4J_URI="neo4j://localhost:7687"  # 或你的 AuraDB URI
NEO4J_USER="neo4j"
NEO4J_PASSWORD="your-neo4j-password"
SEMAPHORE_LIMIT=5
```

## Hello World 示例

下面我们来创建你的第一个 Graphiti 程序，它会添加一条简单的 episode，并验证系统能正常工作。

### hello_graphiti.py

1. 导入所需库

```python
import asyncio
import json
import logging
import os
from datetime import datetime, timezone
from logging import INFO

from dotenv import load_dotenv, find_dotenv

from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from graphiti_core.search.search_config_recipes import NODE_HYBRID_SEARCH_RRF
```

2. 导入 Gemini 相关集成

```python
from graphiti_core.llm_client.gemini_client import GeminiClient, LLMConfig
from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig
from graphiti_core.cross_encoder.gemini_reranker_client import GeminiRerankerClient
```

3. 配置日志与环境变量，并连接 Neo4j 数据库

```python
# 配置日志
logging.basicConfig(
    level=INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

# Neo4j 连接参数
# 确保 Neo4j Desktop 正在运行，并且本地 DBMS 已启动
neo4j_uri = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
neo4j_user = os.environ.get('NEO4J_USER', 'neo4j')
neo4j_password = os.environ.get('NEO4J_PASSWORD', 'password')
if not neo4j_uri or not neo4j_user or not neo4j_password:
    raise ValueError('NEO4J_URI, NEO4J_USER, and NEO4J_PASSWORD must be set')

gemini_api_key = os.environ.get('GEMINI_API_KEY')
if not gemini_api_key:
    raise ValueError('GEMINI_API_KEY must be set')
```

4. 创建一个异步 `main()` 函数，用来执行所有 Graphiti 操作

```python
async def main():
    # 主函数逻辑写在这里
    pass

if __name__ == '__main__':
    asyncio.run(main())
```

5. 连接 Neo4j，并初始化 Graphiti 所需的索引。这一步是必须的，之后才能使用其他 Graphiti 功能：

```python
    # 使用 Neo4j 连接初始化 Graphiti
    graphiti = Graphiti(neo4j_uri, neo4j_user, neo4j_password,
                            llm_client=GeminiClient(
        config=LLMConfig(
            api_key=gemini_api_key,
            model="gemini-2.0-flash"
        )
    ),
    embedder=GeminiEmbedder(
        config=GeminiEmbedderConfig(
            api_key=gemini_api_key,
            embedding_model="embedding-001"
        )
    ),
    cross_encoder=GeminiRerankerClient(
        config=LLMConfig(
            api_key=gemini_api_key,
            model="gemini-2.0-flash-exp"
        )
    )

                        )

    try:
        # 初始化图数据库中的索引与约束。这通常只需要执行一次。
        await graphiti.build_indices_and_constraints()
        
        # 后续代码写在这里

        
    finally:
        # 关闭连接
        await graphiti.close()
        print('\nConnection closed')

        pass
```

6. 添加 Episode 并执行基础搜索

- 在 Graphiti 中，获取关系（edges）最简单的方式是使用 `search` 方法。它会执行一种混合搜索，把语义相似度和 BM25 文本检索结合起来。

```python
        print("📝 Adding your first episode...")
        await graphiti.add_episode(
            name="hello_world_episode",
            episode_body=(
                "Today I started learning Graphiti, a powerful Python framework for "
                "building temporal knowledge graphs. Graphiti helps AI agents remember "
                "information over time and understand how relationships evolve."
            ),
            source=EpisodeType.text,
            source_description="Learning journal entry",
            reference_time=datetime.now(),
        )

        print("✅ Episode added successfully!")

        # 验证图中已经有数据
        print("🔍 Verifying the knowledge graph...")

        # 搜索与 Graphiti 相关的信息
        search_results: list[EntityEdge] = await graphiti.search(
            query="What is Graphiti?",
            num_results=3
        )


        print(f"🎉 Found {len(search_results)} results")

        # 输出数据节点
        for i, data in enumerate(search_results):
            print(f"  {i}:\nUUID: {data.episodes}")
            print(f"  Fact: {data.fact}")
            print("\n")
```

## 运行你的第一个程序

1. **把代码保存为** `main.py`
2. **配置好环境变量**（见上面的 Setup 部分）
3. **运行程序**：

```bash
uv run python main.py
```

## 预期输出

你应该会看到类似下面的内容：

```text
🚀 Starting Hello World Graphiti Example...
🔧 Building initial graph structure...
📝 Adding your first episode...
✅ Episode added successfully!
🔍 Verifying the knowledge graph...
🎉 Success! Found 3 nodes and 2 edges
📊 Graph Contents:
    ...
🔒 Graphiti client closed.
```

挑战任务：[做一次节点搜索](https://help.getzep.com/graphiti/getting-started/quick-start#node-search-using-search-recipes)

## 刚才到底发生了什么？

下面来拆解一下你的第一个 Graphiti 程序做了哪些事：

### 1. Client 初始化

```python
client = Graphiti(uri=..., user=..., password=...)
```

- 连接到你的 Neo4j 数据库
- 初始化 Graphiti 框架

### 2. 图结构初始化

```python
await client.build_indices_and_constraints()
```

- 创建必要的数据库索引，以提升性能
- 设置约束，保证数据完整性

### 3. 添加 Episode

```python
await client.add_episode(...)
```

- 把一段文本内容加入知识图谱
- Graphiti 自动抽取实体和关系
- 创建像 “Graphiti”、“Python framework” 这样的概念节点
- 创建这些概念之间的关系边

### 4. 知识检索

```python
search_results = await client.search(query="What is Graphiti?")
```

- 对知识图谱执行语义搜索
- 返回相关节点和关系
- 验证信息已经成功存储，并且可以被重新检索出来

**核心点：** 你输入的是文本 → Graphiti 自动处理 → 得到结构化知识 → 你再对其搜索。

## 自己动手试一试

### 实验 1：添加更多内容

你可以修改 `episode_body`，加入不同的信息：

```python
episode_body = (
    "I'm building a TutorsGPT system that needs to remember student interactions. "
    "The system should track learning progress, personalize content, and adapt "
    "to individual student needs over time."
)
```

### 实验 2：尝试不同搜索问题

换一些不同的查询：

```python
# 搜索具体概念
search_results = await client.search(query="student learning progress")

# 搜索关系
search_results = await client.search(query="what adapts to student needs?")
```

### 实验 3：添加多条 Episode

试试加入多条 episode，然后观察它们是如何连接起来的：

```python
# Episode 1
await client.add_episode(
    name="alice_starts",
    episode_body="Alice started learning Python programming",
    reference_time=datetime.now() - timedelta(days=7)
)

# Episode 2
await client.add_episode(
    name="alice_progress",
    episode_body="Alice completed her first Python project successfully",
    reference_time=datetime.now()
)

# 搜索 Alice 的学习历程
results = await client.search("Tell me about Alice's Python learning")
```

## 验证清单

- [ ] Graphiti 已成功安装
- [ ] 环境变量已配置
- [ ] Neo4j 数据库可访问
- [ ] 程序运行无报错
- [ ] 知识图谱中已经有节点和边
- [ ] 搜索返回了相关结果

## 常见问题

**Q: 为什么我没有手动创建节点和边？**  
A: 因为 Graphiti 会使用 LLM 自动从文本中抽取实体和关系。这正是 Graphiti 的核心价值，它能以语义方式理解文本内容。

**Q: Graphiti 怎么知道该抽取哪些实体？**  
A: 它会使用你配置的 LLM（默认是 OpenAI，也可以像这里一样用 Gemini）去分析文本，并识别重要概念以及概念之间的关系。

**Q: 我能直接看到原始的 Neo4j 图吗？**  
A: 可以。打开 Neo4j Browser，执行：

```cypher
MATCH (n) RETURN n LIMIT 25
```

这样就可以查看底层图结构。

## 下一步

恭喜你，你已经成功完成了这些事：

- 已创建你的第一个 Graphiti 知识图谱
- 已添加一条 episode，并完成自动实体抽取
- 已对图谱执行语义搜索
- 已验证整套系统端到端可运行

**准备好进入下一步了吗？** 前往 **[02_episodes_and_entities](../02_episodes_and_entities/)**，更深入理解 Graphiti 是如何抽取并组织信息的。

## 关键结论

1. **Graphiti 是自动化的**：你提供文本，它负责生成知识图谱
2. **Episode 是输入单位**：文本会被处理为结构化知识
3. **Search 是语义搜索**：返回的是相关信息，而不仅仅是关键词匹配
4. **一切都是时间相关的**：知识会随着时间不断积累
5. **LLM 是底层驱动力**：实体和关系的抽取都是自动完成的

## 你实际掌握了什么

- 如何安装和配置 Graphiti
- 如何通过添加 episode 来构建知识图谱
- 如何在图中搜索并取回信息
- Graphiti 的基础工作流：文本 → episode → 知识图谱 → 搜索

---

**恭喜！** 你已经成功创建了自己的第一个时序知识图谱。

**准备进入下一步？** 继续前往 **[02_adding_episodes](../02_adding_episodes/)**，学习不同类型的 episode，以及它们如何生成不同的知识结构。

---

_“学习 Graphiti 的最佳方式，就是先从最简单的例子开始，再一步一步建立理解。”_
