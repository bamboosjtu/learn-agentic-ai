# 第 5 步：用 [Graphiti](https://help.getzep.com/graphiti/getting-started/overview) 把时序知识图谱理论落到实践

## 到目前为止的学习路径

在第 1 到第 3 步中，你已经理解了：

- **第 1 步**：为什么 Agent 需要不同类型的记忆
- **第 2 步**：不同存储系统是如何工作的，例如向量库、关系型数据库、知识图谱
- **第 3 步**：时序知识图谱如何跟踪关系以及这些关系如何随时间变化

**现在的关键问题是：** 这些东西到底怎么真正应用到真实 Agent 上？

## 挑战：理论与实现之间的距离

你已经知道时序知识图谱非常适合用来做 Agent 记忆。但如果从零实现它，你通常需要处理：

- 复杂的图数据库编程
- 实体抽取与关系识别
- 时间逻辑与时间管理
- 搜索与检索系统

**如果这些复杂度都能被隐藏在一组简单工具后面，会怎样？**

## 解决方案：[Graphiti - 为 Agent 世界打造的知识图谱记忆](https://neo4j.com/blog/developer/graphiti-knowledge-graph-memory/)

[Graphiti 是什么](https://help.getzep.com/graphiti/getting-started/overview)？  
它本质上是一个框架，用来把“时序知识图谱”的理论能力，变成可直接使用的实践工具。它提供了一个 MCP（Model Context Protocol）Server，让 Agent 可以通过简单命令操作复杂的时序记忆系统。

Graphiti 已经发布了一个面向 Agent 应用的 MCP Server。

### [Graphiti MCP Server](https://help.getzep.com/graphiti/getting-started/mcp-server) 在做什么

Graphiti 实际上实现了你在前 1-3 步中学到的大部分内容：

- **时序知识图谱**（第 3 步的核心概念）
- **高效的存储和搜索**（第 2 步的系统能力）
- **不同类型的记忆**（第 1 步的记忆基础）

而这些复杂能力，都被封装成了一组 Agent 可直接调用的简单工具。

> 说明：这里使用的 MCP Server 是在原始 Graphiti Server 基础上派生出来的版本，改成了无状态可流式的 HTTP Transport，并使用 Gemini 作为 LLM 和 embedding 提供方。

## 简单工具：把复杂系统压缩成易用接口

Graphiti 的 MCP Server 不要求你自己写复杂图逻辑，而是提供了一组简单工具：

### 核心记忆工具

**`add_episode`** - 存储任意经历或信息

```python
# Agent 存储："Alice works at Google and loves Italian food"
add_episode(
    name="Team Meeting",
    episode_body="Alice works at Google and loves Italian food",
    source="text"
)
# Graphiti 会自动抽取实体和关系
```

**`search_facts`** - 查找实体之间的关系

```python
# Agent 搜索："Alice food preferences"
search_facts(query="Alice food preferences")
# 返回："Alice -LIKES-> Italian food (from Team Meeting episode)"
```

**`search_nodes`** - 查找某个实体相关信息

```python
# Agent 搜索："Alice"
search_nodes(query="Alice")
# 返回：系统目前已知的关于 Alice 的摘要
```

**`get_episodes`** - 取回最近的记忆

```python
# Agent 问："最近发生了什么？"
get_episodes(last_n=5)
# 返回：最近存储的 5 条 episode
```

### 背后自动发生了什么

当你调用：

```python
add_episode("Alice works at Google and loves Italian food")
```

系统其实会自动完成：

1. **实体抽取**：Alice、Google、Italian food
2. **关系识别**：Alice -WORKS_AT-> Google，Alice -LIKES-> Italian food
3. **时间标记**：加上当前时间戳和时态信息
4. **图存储**：把这些信息写入知识图谱

**也就是说，Agent 不需要自己理解这些底层复杂性。**

## 动手实践：亲眼看时序记忆工作起来

接下来我们就来 [搭建 Graphiti MCP Server](https://help.getzep.com/graphiti/getting-started/mcp-server)，并直接观察时序知识图谱如何实时工作。

### 环境要求

- **Neo4j Database**：用来存储时序关系的图数据库
- **Google API Key**：用于 LLM 能力，例如实体抽取和 embedding
- **Python 环境**：用于运行 MCP Server

### 第一步：准备 Neo4j 数据库

1. 打开 **Neo4j AuraDB**：<https://neo4j.com/product/auradb/>
2. 创建免费账户 → 创建新实例 → 选择免费层
3. 保存以下信息：**URI**、**username**、**password**
4. 等待 2-3 分钟，让实例启动完成

### 第二步：配置环境变量

创建 `.env` 文件：

```env
NEO4J_URI=neo4j+s://your_instance_uri_here
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password_here

GOOGLE_API_KEY=your_google_api_key_here
SMALL_LLM_MODEL=gemini-2.5-flash
MODEL_NAME=gemini-2.5-flash
DEFAULT_EMBEDDER_MODEL=embedding-001
```

### 第三步：启动 MCP Server

```bash
# 在 graphiti_mcp_server 目录中运行
uv run python mcp_server.py
```

成功时你会看到类似信息：

```text
Graphiti client initialized successfully
```

### 第四步：测试 MCP Server

你可以用以下两种方式测试 Graphiti MCP Server：

**方案 A：Python Client**  
使用仓库中提供的 `python_client.py`，底层走的是 httpx：

```bash
uv run python python_client.py
```

这个 Python 客户端演示了：

- 添加 episode（文本、JSON）
- 搜索事实和关系
- 查找实体及其摘要
- 读取最近的记忆

**方案 B：Postman Collection**  
也可以使用提供的 `postman.json` 集合手动调用：

1. **Add an episode**：向知识图谱中写入信息
2. **Search for facts**：查询实体之间的关系
3. 再测试其他工具

### 第五步：可视化知识图谱

在 Neo4j AuraDB 实例中，你现在已经可以直接查询并可视化图里的数据：

```cypher
MATCH (n)
OPTIONAL MATCH (n)-[r]->(m)
RETURN n, r, m
```

### 第六步：与 OpenAI Agents SDK 集成

最后，把这个 Memory MCP Server 接入 OpenAI Agents SDK。

1. 保持你的 MCP Server 运行中，同时运行 `python_client.py`
2. 打开新的终端，切换到 `agent_connect` 目录
3. 为这个项目准备 `.env` 文件；如果需要 tracing，可以额外配置 OpenAI Key
4. 查看 `main.py`，你会看到 OpenAI Agents SDK 是如何连接 MCP Server 的
5. 示例中的查询会围绕 Cloud Expert 和招聘更新展开。此时 Agent 就可以通过 MCP Tools 管理关于这些对象的记忆

示例输出：

```bash
mjs@Muhammads-MacBook-Pro-3 agent_connect % uv run main.py

[AGENT RESPONSE - AHMAD PROFILE]: Ahmad Hassan is a Senior Solutions Architect at Google Cloud. His expertise spans AI/ML, BigQuery, and GCP Architecture. He holds the Google Cloud Professional Architect certification, obtained in 2023.


[AGENT RESPONSE - JAY PROFILE]: I've added Jay's profile to the memory, noting his role as Agent Native Cloud Expert, his position as Senior Cloud Architect at Microsoft Azure, and his expertise in Kubernetes, Azure DevOps, cloud security, and large-scale cloud migrations.
```

上述请求的 tracing：

![](./agent_connect/trace_1.png)

![](./agent_connect/trace_2.png)

## 完整工具参考

为了构建更复杂的 Agent，Graphiti MCP Server 还提供了以下工具：

### 记忆管理

- **`add_episode`**：存储文本、JSON 或消息对话
- **`get_episodes`**：按 group 或时间读取最近的 episodes
- **`delete_episode`**：删除指定记忆

### 搜索与发现

- **`search_facts`**：查找具体关系，也就是实体到实体之间的连接
- **`search_nodes`**：查找实体及其摘要
- **`get_entity_edge`**：获取某条具体关系的详细信息

### 维护与状态

- **`clear_graph`**：清空整个知识图谱
- **`delete_entity_edge`**：删除指定关系
- **`get_status`**：检查服务器和数据库连接状态

### 支持的数据格式

- **Text**：自然语言对话与描述
- **JSON**：结构化数据，例如 CRM 记录、用户画像
- **Messages**：带 user / assistant 格式的聊天消息

## 你已经学会了什么：理论与实践结合

完成这一步之后，你已经：

1. **把概念映射到工具上**：看到了时序知识图谱理论如何变成实际可调用的 MCP 工具
2. **体验了自动处理过程**：亲眼看到实体和关系如何自动被抽取
3. **理解了抽象层**：知道复杂系统也可以通过简单接口暴露出来
4. **构建了可运行记忆系统**：你现在已经有了一个本地可运行的时序知识图谱记忆系统

### 完整学习路径

```text
Step 1: Memory Foundations → Step 2: Storage Systems → Step 3: Temporal Theory → Step 4: Practical Tools
```

你现在已经同时掌握了理论基础，也拥有了实际可运行的工具，可以开始实现更复杂的 Agent 记忆系统了。

## 下一步：构建具备记忆能力的 Agent

当 Graphiti MCP Server 跑起来之后，你接下来可以：

1. **接入 OpenAI Agents SDK**：给 Agent 提供持久化、带时间感知的记忆
2. **构建对话式 Agent**：让它能记住每次交互，并从交互中学习
3. **为 IDE 等工具配置统一记忆 MCP Server**：让系统持续跟踪用户偏好，并随着时间自适应

基础已经具备，工具已经到位。**接下来就是把 Graphiti 真正用起来。**

## 参考资源

- <https://www.youtube.com/watch?v=H2Cb5wbcRzo>
- <https://blog.futuresmart.ai/building-ai-knowledge-graph-using-graphiti-and-neo4j>
- <https://help.getzep.com/graphiti/getting-started/overview>
- <https://help.getzep.com/graphiti/getting-started/quick-start>
- <https://help.getzep.com/graphiti/getting-started/mcp-server>
- <https://neo4j.com/blog/developer/graphiti-knowledge-graph-memory/>
