# 第 04 步：[Communities](https://help.getzep.com/graphiti/core-concepts/communities) - 自动发现隐藏模式

现在你已经能通过自定义类型构建更精确的知识图谱，接下来我们来看 Graphiti 如何自动发现相关信息形成的群组，也就是所谓的 “communities”。

## 你将学到什么

完成这一节后，你将能够：

- 理解 communities 是什么，以及它们如何自动形成
- 使用 `build_communities()` 来发现数据中的隐藏模式
- 看到 communities 如何把相关学生、主题和概念自动分组
- 在添加新 episodes 后动态更新 communities
- 把 community 洞察应用到教育类场景中

## 什么是 Communities？

### 核心概念

**Communities**（在 Graphiti 中表示为 `CommunityNode` 对象）是一些彼此之间连接很强的实体节点群组。Graphiti 会通过分析知识图谱中的连接模式，使用 **Leiden 算法** 自动识别这些群组。

**教育场景里的例子：**

- 在相似主题上遇到困难的学生群体
- 经常被一起教授的概念群组
- 会自然递进和依赖的技能集合
- 围绕共同兴趣形成的学习小组

### Communities 是如何形成的

1. **添加 Episodes** → 在知识图谱中创建实体和关系
2. **建立连接** → 实体通过共享经验和共同属性连接起来
3. **Leiden 算法分析** → 通过社区发现算法，把强连接节点自动分成组
4. **生成摘要** → 每个 community 都会有一个 summary 字段，用于汇总其成员实体的摘要

### Community Detection 的处理过程

**技术细节：**

- **算法**：Leiden 算法，用于把强连接节点自动聚类
- **节点表示**：communities 会以 `CommunityNode` 对象形式保存
- **摘要生成**：每个 community 都有一个 summary，用来综合其成员实体的信息
- **高层洞察**：除了边上原始事实外，还会额外给出更高层次的综合信息

### Communities 的动态更新

**两种更新方式：**

1. **全量重建**（推荐定期执行）：

```python
await graphiti.build_communities()  # 删除现有 communities，重新生成
```

2. **动态更新**（适合持续增量添加）：

```python
await graphiti.add_episode(
    episode_body="New content...",
    update_communities=True  # 更新现有 communities
)
```

**更新算法说明：**

- 当你使用 `update_communities=True` 时，新节点会根据其周围节点中最常见的 community 被自动分配到某个已有 community 中
- 这种方法受到 **label propagation algorithm** 的启发

### 为什么 Communities 很重要

- **发现模式**：找出你之前并不知道存在的隐藏关系
- **自动组织**：内容会通过算法自然聚成有意义的群组
- **更好的搜索**：可以把查询集中到相关 community 中，提高结果针对性
- **学习洞察**：理解你的领域知识是如何自然聚类的
- **高层综合能力**：快速获得图中整体结构的摘要信息

## 简单 Communities 示例

下面我们创建一小批最简数据，让 communities 形成，然后再手动探索它们。

### communities_demo.py

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
    """Build communities and explore them manually in Neo4j"""
    
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
                model="gemini-2.0-flash"
            )
        )
    )
    
    try:
        await graphiti.build_indices_and_constraints()
        print("🏘️ Communities Demo - Building Knowledge Graph...")
        
        # Add just 4 simple episodes to create communities
        episodes = [
            "Alice and Bob are both learning Python programming together.",
            "Alice is helping Charlie connect Python to web backends.", 
            "Bob and Diana are collaborating on a full-stack project."
        ]
        
        print("\n📝 Adding episodes...")
        for i, episode in enumerate(episodes):
            print(f"episode_{i+1}\n")
            await graphiti.add_episode(
                name=f"episode_{i+1}",
                episode_body=episode,
                source=EpisodeType.text,
                source_description="Engineers Collaboration",
                reference_time=datetime.now() - timedelta(days=i)
            )
        
        print("✅ Episodes added!")
        await asyncio.sleep(60)  # Small delay for clarity
        print("\n🔍 Exploring communities...")
        # Build communities to see patterns
        print("\n🔍 Building communities...")
        res = await graphiti.build_communities()
        print("✅ Communities built!")
        
        print(f"Communities found: \n\n {res}\n\n\n")
        print("\n🎓 Communities demo completed!")
        print("\n👀 Now manually explore your Neo4j database...")
                
    finally:
        await graphiti.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## 运行示例

```bash
uv run python communities_demo.py
```

## 预期输出

```text
🏘️ Communities Demo - Building Knowledge Graph...

📝 Adding episodes...
episode_1

episode_2

episode_3

✅ Episodes added!

🔍 Exploring communities...

🔍 Building communities...
✅ Communities built!
Communities found: 

 ([CommunityNode(...)])

👀 Now manually explore your Neo4j database...
```

## 在 Neo4j 中手动探索

现在进入最有意思的部分。打开 **Neo4j Browser**，执行下面这些查询：

### 1. 查看所有节点和 Communities

```cypher
MATCH (n)
OPTIONAL MATCH (n)-[r]->(m)
RETURN n, r, m
```

这个查询会展示整张图，包括实体节点和 community 节点。

### 2. 找出 Community 节点

```cypher
MATCH (c:Community) RETURN c.name, c.summary
```

查看当前识别出来的 community 以及它们的摘要。

### 3. 查看哪些实体属于哪些 Community

```cypher
MATCH (c:Community)-[m:HAS_MEMBER]->(e:Entity) RETURN c, m, e
```

这个查询会展示 community 和其成员实体之间的关系。

## 官方文档中的关键概念

参考：  
[Official Documentation](https://help.getzep.com/graphiti/core-concepts/communities)

### Communities 的工作机制

1. **添加 Episode** → 创建实体和关系
2. **Leiden 算法** → 把强连接节点自动聚成组
3. **生成摘要** → 每个 community 都有 summary，用于汇总成员实体信息
4. **高层综合表达** → 不只是事实，还能提供关于图整体结构的综合理解

### 更新 Communities 的两种方式

```python
# 方式 1：全量重建（删除旧的，重新生成）
await graphiti.build_communities()

# 方式 2：动态更新（把新节点加进现有 communities） - 截至 2025 年 8 月 5 日仍报错
await graphiti.add_episode(
    episode_body="New content...",
    update_communities=True  # Uses label propagation algorithm
)
```

### 为什么手动探索很重要

- **看见算法如何工作**：从图的可视化中理解 Leiden 是怎么把节点聚起来的
- **验证结果是否合理**：检查 communities 是否符合教育语义
- **顺便学习 Neo4j**：练习 Cypher 查询和图分析
- **发现意外模式**：看到你原本没有预料到的连接关系

## 常见问题

**Q: 只有 4 条 episode，我大概会看到几个 community？**  
A: 通常可能只有 1 到 2 个 community。想看到更明显的群组结构，需要更多且更有交叉连接的数据。

**Q: 我在 Neo4j Browser 里应该看到什么？**  
A: 应该能看到 EntityNodes，例如 Alice、Bob、Charlie、Diana，也会看到 CommunityNodes，以及把它们连接起来的 `HAS_MEMBER` 关系。

**Q: 我应该优先用全量重建还是动态更新？**  
A: 建议一开始先用 `build_communities()` 做全量重建，先理解社区构建机制。动态更新更适合长期运行中的持续增量数据。

**Q: 如果我没有看到很清晰的 community 怎么办？**  
A: 试着加入更多 episode，并让分组结构更明显。社区发现算法需要足够多的连接关系，才能识别模式。

## 下一步

**做得很好。** 你现在已经理解了知识是如何自然聚类的，也能够开始利用这些聚类模式做教育分析。

**准备好隔离不同教育上下文了吗？** 下一步前往 **[05_graph_namespacing](../05_graph_namespacing/)**，学习如何为不同学校、班级或组织创建独立的图空间。

**接下来会学什么？**  
你将不再只有一张“大而混杂”的图，而是能构建多个彼此隔离的图环境。这样不同教育上下文就不会互相污染，这对于多租户教育系统尤其重要。

---

**关键结论：** 用极少代码构建 communities，然后在 Neo4j 中手动探索它们。这种方式同时能帮你掌握 Graphiti 的核心概念和实用的图数据库操作能力。

_“理解 communities 的最好方式，就是亲眼在图数据库里看到它们长出来。”_
