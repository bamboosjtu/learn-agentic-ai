# 第 06 步：[Searching the Graph](https://help.getzep.com/graphiti/working-with-data/searching) - 混合搜索与高级检索

现在你已经理解了 namespacing，接下来要真正掌握 Graphiti 强大的搜索能力。最好的方式，是用**同一个查询**去比较不同搜索策略的差异。

## 你将学到什么

完成这一节后，你将能够：

- 观察不同搜索策略在同一个查询上的表现差异
- 理解混合搜索（语义搜索 + BM25）与聚焦型搜索的区别
- 比较不同 search recipes，例如以节点为中心、以边为中心、以及组合搜索
- 理解每一种搜索策略分别适合什么场景
- 在 Neo4j 中手动探索搜索结果

### 两种主要搜索方式

1. **混合搜索（Hybrid Search）**：`await graphiti.search(query)`
   - 同时结合语义相似度和 BM25 检索
   - 使用 Reciprocal Rank Fusion（RRF）进行重排序
   - 适合：宽泛探索、通用发现

2. **基于节点距离的重排序（Node Distance Reranking）**：`await graphiti.search(query, focal_node_uuid)`
   - 本质上仍然是混合搜索，但会优先返回靠近某个指定节点的结果
   - 适合：以实体为中心的查询，例如 “Alice 对 Python 了解什么？”

### 使用 Recipes 做可配置搜索

Graphiti 提供了 `graphiti._search()`，并内置 **15 个现成 recipe**：

| Recipe Focus | 返回内容 | 适用场景 |
|-------------|---------|---------|
| `NODE_HYBRID_SEARCH_RRF` | 实体 / 概念 | 查找人物、主题、概念 |
| `EDGE_HYBRID_SEARCH_RRF` | 关系 / 事实 | 查找连接、交互 |
| `COMBINED_HYBRID_SEARCH_RRF` | 全部内容 | 做综合探索 |

### 文档中的重排序策略

参考：[Documentation](https://help.getzep.com/graphiti/working-with-data/searching)

- **RRF（Reciprocal Rank Fusion）**：融合 BM25 与语义搜索结果
- **MMR（Maximal Marginal Relevance）**：在相关性和多样性之间平衡
- **Cross-Encoder**：语义评分最准确，但速度更慢

## 简单示例：对比不同搜索策略

下面我们使用**同一个查询**比较所有搜索策略，看看它们分别返回什么。

### main.py

```python
import asyncio
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv

from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from graphiti_core.search.search_config_recipes import (
    NODE_HYBRID_SEARCH_RRF, 
    EDGE_HYBRID_SEARCH_RRF,
    COMBINED_HYBRID_SEARCH_RRF
)

from graphiti_core.llm_client.gemini_client import GeminiClient, LLMConfig
from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig
from graphiti_core.cross_encoder.gemini_reranker_client import GeminiRerankerClient

load_dotenv(find_dotenv())

async def main():
    """Compare search strategies using the same query"""
    
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
                model="gemini-2.5-flash-lite"
            )
        )
    )
    
    try:
        await graphiti.build_indices_and_constraints()
        print("🔍 Search Strategy Comparison Demo...")
        
        # Add simple educational content
        print("\n📚 Adding educational knowledge...")
        
        episodes = [
            "Alice is learning Python programming. She understands variables but struggles with loops.",
            "Bob helps Alice with debugging techniques. He explains step-by-step problem solving.",
            "Carol collaborates with Alice and Bob on programming projects using Python functions.",
            "Variables are fundamental concepts in Python. Loops build on variable understanding."
        ]
        
        for i, episode in enumerate(episodes):
            print(f"episode_{i+1}")
            await graphiti.add_episode(
                name=f"episode_{i+1}",
                episode_body=episode,
                source=EpisodeType.text,
                source_description="Educational content",
                reference_time=datetime.now() - timedelta(days=i),
                group_id="cs101"
            )
            await asyncio.sleep(60)  # Simulate processing time
        
        print("✅ Episodes added!")
        print("\n⏳ Processing for search...")
        await asyncio.sleep(60)
        
        # THE SAME QUERY for all strategies
        QUERY = "Alice learning Python programming"
        print(f"\n🎯 **Comparing all strategies with query: '{QUERY}'**\n")
        
        # Strategy 1: Basic Hybrid Search
        print("📖 **Strategy 1: Basic Hybrid Search**")
        basic_results = await graphiti.search(query=QUERY)
        print(f"   Results: {len(basic_results)} found")
        for i, result in enumerate(basic_results, 1):
            print(f"     {i}. {result.fact}")
        
        # Strategy 2: Node-Focused Search  
        print(f"\n🎯 **Strategy 2: Node-Focused Search (entities/concepts)**")
        node_config = NODE_HYBRID_SEARCH_RRF.model_copy(deep=True)
        node_config.limit = 10
        
        node_results = await graphiti._search(query=QUERY, config=node_config)
        print(f"   Nodes found: {len(node_results.nodes)}")
        for i, node in enumerate(node_results.nodes, 1):
            print(f"     {i}. {node.name}")
        
        # Strategy 3: Edge-Focused Search
        print(f"\n🔗 **Strategy 3: Edge-Focused Search (relationships)**")
        edge_config = EDGE_HYBRID_SEARCH_RRF.model_copy(deep=True)
        edge_config.limit = 10
        
        edge_results = await graphiti._search(query=QUERY, config=edge_config)
        print(f"   Relationships found: {len(edge_results.edges)}")
        for i, edge in enumerate(edge_results.edges, 1):
            print(f"     {i}. {edge.source_node_uuid} → {edge.target_node_uuid}")
            print(f"        Type: {edge.name}")
        
        # Strategy 4: Combined Search
        print(f"\n🌍 **Strategy 4: Combined Search (everything)**")
        combined_config = COMBINED_HYBRID_SEARCH_RRF.model_copy(deep=True)
        combined_config.limit = 10
        
        combined_results = await graphiti._search(query=QUERY, config=combined_config)
        print(f"   Nodes: {len(combined_results.nodes)}")
        print(f"   Edges: {len(combined_results.edges)}")  
        print(f"   Communities: {len(combined_results.communities)}")
        
        print("\n🎓 Search comparison completed!")
        print("\n👀 Now manually explore search results in Neo4j...")
        
    finally:
        await graphiti.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## 运行示例

```bash
uv run python main.py
```

## 预期输出

```text
🔍 Search Strategy Comparison Demo...

📚 Adding educational knowledge...
episode_1
episode_2
episode_3
episode_4
✅ Episodes added!

⏳ Processing for search...

🎯 **Comparing all strategies with query: 'Alice learning Python programming'**

📖 **Strategy 1: Basic Hybrid Search**
   Results: 10 found
     1. Alice is learning Python programming.
     2. Alice ... using Python functions
     3. Bob helps Alice with debugging techniques.
     4. Bob helps Alice with debugging techniques.
     5. Carol ... using Python functions
     6. Alice and Bob collaborate
     7. Bob ... using Python functions
     8. Variables are fundamental concepts in Python.
     9. Carol collaborates with Alice
     10. She understands variables

🎯 **Strategy 2: Node-Focused Search (entities/concepts)**
   Nodes found: 10
     1. Alice
     2. Python programming
     3. Python
     4. Python functions
     5. Carol
     6. step-by-step problem solving
     7. Bob
     8. variables
     9. loops
     10. debugging techniques

🔗 **Strategy 3: Edge-Focused Search (relationships)**
   Relationships found: 10
     1. ce59d916-31a2-44b9-b51a-869da4b9a45b → b46fcb99-bb04-4f25-b9cc-f013c76dd230
        Type: IS_LEARNING
     2. ce59d916-31a2-44b9-b51a-869da4b9a45b → 66291e1e-ae48-4a67-8393-af7f7b74b544
        Type: USES
     3. b8f6c852-c541-4162-b0d3-5ca31f9c7507 → ce59d916-31a2-44b9-b51a-869da4b9a45b
        Type: HELPS
     4. b8f6c852-c541-4162-b0d3-5ca31f9c7507 → 358ae58e-b214-47d3-bf50-d5e0924d5a16
        Type: EXPLAINS
     5. a73f81ed-992d-4f55-ae2e-6f7722131fbd → 66291e1e-ae48-4a67-8393-af7f7b74b544
        Type: USES
     6. ce59d916-31a2-44b9-b51a-869da4b9a45b → b8f6c852-c541-4162-b0d3-5ca31f9c7507
        Type: COLLABORATES_WITH
     7. b8f6c852-c541-4162-b0d3-5ca31f9c7507 → 66291e1e-ae48-4a67-8393-af7f7b74b544
        Type: USES
     8. dfd26e7d-f119-43ea-867f-586a468e683b → ba45355b-f624-4a7a-a455-21745f4e8216
        Type: ARE_FUNDAMENTAL_CONCEPTS_IN
     9. a73f81ed-992d-4f55-ae2e-6f7722131fbd → ce59d916-31a2-44b9-b51a-869da4b9a45b
        Type: COLLABORATES_WITH
     10. ce59d916-31a2-44b9-b51a-869da4b9a45b → dfd26e7d-f119-43ea-867f-586a468e683b
        Type: UNDERSTANDS

🌍 **Strategy 4: Combined Search (everything)**
   Nodes: 10
   Edges: 10
   Communities: 0

🎓 Search comparison completed!

👀 Now manually explore search results in Neo4j...
```

## 在 Neo4j 中手动探索

打开 **Neo4j Browser**，手动查看搜索结果：

### 1. 查看所有与搜索相关的实体

```cypher
MATCH (n:Entity) 
WHERE n.name CONTAINS "Alice" OR n.name CONTAINS "Python"
RETURN n.name, n.group_id
```

这个查询会找出与你搜索问题相关的实体。

### 2. 查看 Alice 周围的关系

```cypher
MATCH (n:Entity) 
WHERE n.name CONTAINS "Alice" OR n.name CONTAINS "Python"
MATCH (n)-[r]->(m)
RETURN n, r, m
```

这个查询能帮助你看到 Alice 和其他概念或实体之间的连接方式。

## 自己动手试一试

### 练习 1：尝试不同查询

用相同的策略测试不同查询，观察差异：

```python
# 试试这些查询，看看结果怎么变化
queries_to_test = [
    "Bob helping debugging",
    "Python variables concepts", 
    "programming collaboration",
    "learning difficulties"
]
```

### 练习 2：增加更多 Episode 再重新搜索

增加更复杂的 episodes，然后重新跑相同查询，看看结果如何变化：

```python
new_episodes = [
    "Alice mastered Python loops after Bob's debugging help.",
    "Carol teaches Alice about Python functions and code organization.",
    "The programming team uses collaborative debugging strategies."
]

# 重新执行同一个搜索查询，观察结果变化
```

### 练习 3：尝试不同 Search Recipes

切换不同 recipe 进行比较：

```python
from graphiti_core.search.search_config_recipes import (
    NODE_HYBRID_SEARCH_MMR,  # 不同 reranking
    EDGE_HYBRID_SEARCH_MMR,
    COMMUNITY_HYBRID_SEARCH_RRF
)

# 比较 RRF 与 MMR 的差异
query = "Alice learning Python"

rrf_config = NODE_HYBRID_SEARCH_RRF.model_copy(deep=True)
mmr_config = NODE_HYBRID_SEARCH_MMR.model_copy(deep=True)

rrf_results = await graphiti._search(query, config=rrf_config)
mmr_results = await graphiti._search(query, config=mmr_config)

print(f"RRF reranking: {len(rrf_results.nodes)} nodes")
print(f"MMR reranking: {len(mmr_results.nodes)} nodes")
```

## 官方文档中的关键概念

参考：  
[Official Documentation](https://help.getzep.com/graphiti/working-with-data/searching)

### 什么时候用哪种搜索策略？

**基础混合搜索（`graphiti.search()`）**

- **适合**：通用探索、宽泛发现
- **返回**：混合结果，通常是以边上的事实为主
- **使用时机**：你希望同时利用语义相似性和 BM25，获得更全面结果

**节点聚焦搜索（`NODE_HYBRID_SEARCH_RRF`）**

- **适合**：查找实体、概念、人物
- **返回**：EntityNodes，例如 Alice、Python、Variables
- **使用时机**：你要找的是关键概念或核心角色

**边聚焦搜索（`EDGE_HYBRID_SEARCH_RRF`）**

- **适合**：查找关系、交互、连接
- **返回**：Relationships，例如 Alice → Python、Bob → Alice
- **使用时机**：你希望理解连接方式、依赖关系或互动路径

**组合搜索（`COMBINED_HYBRID_SEARCH_RRF`）**

- **适合**：做综合分析
- **返回**：Nodes + Edges + Communities
- **使用时机**：你需要对某个主题形成完整图景

### 从本例能看到什么？

对于查询 `"Alice learning Python programming"`：

| 策略 | 聚焦点 | 返回内容 | 最适合 |
|------|--------|----------|--------|
| **基础混合搜索** | 事实 / 语句 | 6 条文本结果 | 通用发现 |
| **节点聚焦搜索** | 实体 | 4 个概念节点 | 找关键角色 / 主题 |
| **边聚焦搜索** | 关系 | 3 条连接关系 | 理解交互 |
| **组合搜索** | 全部内容 | 4 个节点 + 3 条边 + 1 个 community | 完整分析 |

## 验证清单

- [ ] 已用同一个查询测试四种搜索策略
- [ ] 已清楚理解不同结果类型的差异，例如 facts、nodes、edges
- [ ] Search recipe 配置已正确运行
- [ ] Neo4j 查询已能把搜索结果可视化出来
- [ ] 已能清楚比较不同策略的返回差异

## 常见问题

**Q: 为什么不同策略返回的结果数不一样？**  
A: 因为每种策略聚焦的图元素不同。基础搜索更偏 facts，节点搜索返回实体，边搜索返回关系。

**Q: 教育类应用里我应该先用哪种搜索方式？**  
A: 一般先从基础混合搜索开始做探索，再用节点聚焦找关键概念，用边聚焦理解学习关系和交互模式。

**Q: 为什么要用同一个查询去测不同策略？**  
A: 因为这样你能看到同一信息在不同“视角”下会呈现成什么样子：有的是事实，有的是实体，有的是关系。

**Q: 怎么判断搜索效果是不是好？**  
A: 看结果是否合理，试不同查询，并在 Neo4j 里手动查看图结构，验证系统找到的东西是不是你真正想要的。

## 你在这一节里学会了什么

✅ **搜索策略对比**：用同一个查询测试了四种不同搜索方式  
✅ **结果类型理解**：区分了 facts、entities 和 relationships  
✅ **Search Recipe 配置**：会使用预设 recipe 来做聚焦搜索  
✅ **实际应用理解**：看到了不同策略如何揭示不同层次的信息  
✅ **可视化探索**：能在 Neo4j 中手动检查搜索结果

## 下一步

**做得很好。** 你现在已经掌握了如何在复杂教育知识图谱中找到“你真正需要的信息”。

**准备好直接操作知识图谱了吗？** 接下来前往 **[07_crud_operations](../07_crud_operations/)**，学习如何精确地创建、读取、更新、删除节点和边。

**下一步会学什么？**  
你将不再只是搜索图中的信息，而是开始直接修改知识图谱，用于精细维护和与外部系统集成。

---

**关键结论：** 不同搜索策略就像不同镜头。它们看的是同一份信息，但会呈现完全不同的视角。真正有效的做法，是根据问题本身来选择合适的“镜头”。

_“一个查询，四种策略，四种不同洞察。这就是 Graphiti 搜索的威力。”_
