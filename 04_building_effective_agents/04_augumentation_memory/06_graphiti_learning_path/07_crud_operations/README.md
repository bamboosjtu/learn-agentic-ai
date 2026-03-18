# 第 07 步：[CRUD Operations](https://help.getzep.com/graphiti/working-with-data/crud-operations) - 直接操作节点与边

现在你已经掌握了搜索，接下来要学习如何以“外科手术式精度”直接创建、读取、更新和删除节点与边。

## 你将学到什么

完成这一节后，你将能够：

- 直接创建、读取、更新和删除节点与边
- 理解什么时候该用 CRUD，什么时候该用 episodes
- 看到直接操作图谱的实际示例
- 学习教育数据管理中的安全实践
- 在 Neo4j 中手动检查 CRUD 操作结果

## 前置要求

- 已完成 Step 01-06
- 已理解搜索和 namespacing
- 已掌握节点和边的基本概念

### 什么是 CRUD？

**CRUD** = **C**reate、**R**ead、**U**pdate、**D**elete，也就是直接对节点和边进行增删改查。

### CRUD 与 Episodes 的区别

| CRUD Operations | Episodes |
|----------------|----------|
| 直接控制 | 自然语言处理 |
| 精准更新 | LLM 自动抽取实体和关系 |
| 适合已知实体 | 适合非结构化内容 |
| 便于系统集成 | 便于发现丰富上下文 |

### 文档中的核心类

参考：[Documentation](https://help.getzep.com/graphiti/working-with-data/crud-operations)

```python
from graphiti_core.nodes import EntityNode, EntityEdge

# EntityNode: 直接操作节点
# EntityEdge: 直接操作关系
```

### 基础操作

- **Create**：`node.save(driver)` - 添加新节点 / 新边
- **Read**：`EntityNode.get_by_uuid(driver, uuid)` - 按 UUID 读取
- **Update**：修改属性后再执行 `node.save(driver)`
- **Delete**：`node.delete(driver)` - 删除（要谨慎使用）

### 什么时候用 CRUD？

**适合：** 精准更新、系统集成、纠错、批量操作  
**不适合：** 需要 LLM 去理解和抽取的自然语言内容

## 简单 CRUD 示例

下面通过一个简单的学生-课程场景，演示 CRUD 的完整流程。

### crud_demo.py

```python
import asyncio
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

from graphiti_core import Graphiti
from graphiti_core.nodes import EntityNode
from graphiti_core.edges import EntityEdge

from graphiti_core.llm_client.gemini_client import GeminiClient, LLMConfig
from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig
from graphiti_core.cross_encoder.gemini_reranker_client import GeminiRerankerClient

load_dotenv(find_dotenv())

async def main():
    """Simple CRUD operations demonstration"""
    
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
        print("✏️ CRUD Operations Demo...")
        
        # 1. CREATE - Add student and course
        print("\n📝 **CREATE**: Adding student and course...")
        
        student_uuid = str(uuid.uuid4())
        student_name = "Alice Chen"
        
        # Generate embedding for the student name
        student_embedding = await graphiti.embedder.create([student_name])
        
        student_node = EntityNode(
            uuid=student_uuid,
            name=student_name,
            group_id="cs101",
            created_at=datetime.now(),
            summary="Computer Science student",
            attributes={"gpa": 3.5, "year": "Sophomore"},
            name_embedding=student_embedding  # Use generated embedding
        )
        await student_node.save(graphiti.driver)
        print(f"   ✅ Created student: {student_name}")
        
        course_uuid = str(uuid.uuid4())
        course_name = "CS101 Programming"
        
        # Generate embedding for the course name
        course_embedding = await graphiti.embedder.create([course_name])
        
        course_node = EntityNode(
            uuid=course_uuid,
            name=course_name,
            group_id="cs101",
            created_at=datetime.now(),
            summary="Introduction to programming",
            attributes={"credits": 4, "difficulty": "Beginner"},
            name_embedding=course_embedding  # Use generated embedding
        )
        await course_node.save(graphiti.driver)
        print(f"   ✅ Created course: {course_name}")
        
        # Create enrollment relationship
        enrollment_uuid = str(uuid.uuid4())
        enrollment_edge = EntityEdge(
            uuid=enrollment_uuid,
            source_node_uuid=student_uuid,
            target_node_uuid=course_uuid,
            group_id="cs101",
            created_at=datetime.now(),
            name="ENROLLED_IN",
            fact="Alice Chen enrolled in CS101 Programming",
            attributes={"status": "Active", "grade": None},
            fact_embedding=await graphiti.embedder.create(["Alice Chen enrolled in CS101 Programming"])
        )
        await enrollment_edge.save(graphiti.driver)
        print(f"   ✅ Created enrollment relationship")
        
        # 2. READ - Retrieve what we created
        print("\n📖 **READ**: Retrieving entities...")
        
        retrieved_student = await EntityNode.get_by_uuid(graphiti.driver, student_uuid)
        if retrieved_student:
            print(f"   📚 Found student: {retrieved_student}")
            print(f"      GPA: {retrieved_student.attributes.get('gpa')}")
        
        retrieved_course = await EntityNode.get_by_uuid(graphiti.driver, course_uuid)
        if retrieved_course:
            print(f"   📚 Found course: {retrieved_course}")
            print(f"      Credits: {retrieved_course.attributes.get('credits')}")
        
        retrieved_enrollment = await EntityEdge.get_by_uuid(graphiti.driver, enrollment_uuid)
        if retrieved_enrollment:
            print(f"   📚 Found enrollment: {retrieved_enrollment}")
            print(f"      Status: {retrieved_enrollment.attributes.get('status')}")
        
        # 3. UPDATE - Modify existing data
        print("\n✏️ **UPDATE**: Modifying data...")
        
        # Update student GPA
        if retrieved_student:
            retrieved_student.attributes["gpa"] = 3.8
            retrieved_student.summary = "Computer Science student with improved GPA"

            if retrieved_student.name_embedding is None:
                retrieved_student.name_embedding = await graphiti.embedder.create([retrieved_student.name])
                print("   ⚠️  Warning: name_embedding was None. Regenerated embedding before saving.")

            await retrieved_student.save(graphiti.driver)
            print(f"   ✅ Updated student GPA to: {retrieved_student.attributes['gpa']}")
        
        print("\n👀 Now manually explore CRUD results in Neo4j...")
        
    finally:
        await graphiti.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## 运行示例

```bash
uv run python crud_demo.py
```

## 预期输出

```text
✏️ CRUD Operations Demo...

📝 **CREATE**: Adding student and course...
   ✅ Created student: Alice Chen
   ✅ Created course: CS101 Programming
   ✅ Created enrollment relationship

📖 **READ**: Retrieving entities...
   📚 Found student: Alice Chen
      GPA: 3.5
   📚 Found course: CS101 Programming
      Credits: 4
   📚 Found enrollment: ENROLLED_IN
      Status: Active

✏️ **UPDATE**: Modifying data...
   ✅ Updated student GPA to: 3.8

👀 Now manually explore CRUD results in Neo4j...
```

## 在 Neo4j 中手动探索

打开 **Neo4j Browser**，执行下面的查询查看 CRUD 结果：

### 1. 查看所有创建出的实体

```cypher
MATCH (n)
OPTIONAL MATCH (n)-[r]->(m)
RETURN n, r, m
```

这个查询会展示所有通过 CRUD 创建出来的实体和关系。

## 进阶：把 CRUD 和自定义实体类型结合起来

如果你想把 Step 03 中的自定义实体能力和 CRUD 结合，可以继续看 `custom_crud_demo.py`。

**为什么这种组合很强：**

- **类型安全**：Pydantic 模型能保证数据一致性
- **领域建模能力**：教育类实体可以带有明确属性
- **自动校验**：对教育数据做结构校验
- **IDE 支持更好**：自动补全和类型检查更完整

### 运行自定义 CRUD Demo

```bash
# 运行带 custom types 的增强版 demo
uv run python custom_crud_demo.py
```

## 官方文档中的关键概念

参考：  
[Official Documentation](https://help.getzep.com/graphiti/working-with-data/crud-operations)

### Graphiti 中的核心 CRUD 类

根据文档，Graphiti 有 **8 个核心类**：

- `Node`、`EpisodicNode`、`EntityNode`
- `Edge`、`EpisodicEdge`、`EntityEdge`
- `CommunityNode`、`CommunityEdge`

**如果你要做直接操作，最常用的是：**

- `EntityNode`
- `EntityEdge`

### 文档中的关键方法

1. **Save 方法**：`await node.save(driver)`
   - 根据 UUID 做 find-or-create
   - 会把类中的当前数据同步到图数据库中

2. **Delete 方法**：`await node.delete(driver)`
   - 会做硬删除
   - 要谨慎使用，通常更推荐归档

3. **按 UUID 获取**：`await EntityNode.get_by_uuid(driver, uuid)`
   - 类方法
   - 用于按唯一标识获取实体

### 什么时候该用 CRUD，什么时候该用 Episodes？

| 场景 | 用 CRUD | 用 Episodes |
|------|---------|-------------|
| **精确更新** | ✅ 学生 GPA 变化 | ❌ |
| **系统集成** | ✅ LMS 成绩同步 | ❌ |
| **自然语言内容** | ❌ | ✅ 学习故事 |
| **已知关系** | ✅ 选课状态 | ❌ |
| **批量操作** | ✅ 导入成绩 | ❌ |
| **丰富上下文** | ❌ | ✅ 学生互动、讨论 |

## 验证清单

- [ ] CREATE：学生和课程节点已成功创建
- [ ] READ：能够通过 UUID 正确读取实体及属性
- [ ] UPDATE：属性能被修改并成功保存
- [ ] VERIFY：通过搜索或查看图验证 CRUD 确实生效
- [ ] ARCHIVE：优先采用安全数据管理方式，而不是直接删除
- [ ] Neo4j 查询已能清楚展示 CRUD 结果

## 常见问题

**Q: CRUD 和 episodes 的本质区别是什么？**  
A: CRUD 提供的是直接控制权，适合精确更新；episodes 则适合把自然语言交给 LLM 自动处理，从中抽取实体和关系。

**Q: 为什么更推荐归档，而不是删除？**  
A: 教育数据往往具有法律、审计和分析价值。归档既能保留历史，又能把它标记为不再活跃。

**Q: 我怎么确认 CRUD 操作真的成功了？**  
A: 可以通过搜索验证、直接在 Neo4j 中查看，也可以检查 UUID 是否和预期一致。

**Q: 在同一个应用里能同时混用 CRUD 和 episodes 吗？**  
A: 可以，而且通常就该这么做。结构化更新（例如成绩、选课状态）适合用 CRUD；丰富上下文（例如学习互动、辅导过程）更适合用 episodes。

**Q: 我遇到了 “vector must not be null” 错误，这是怎么回事？**  
A: 说明你在直接创建 `EntityNode` 时没有先生成 embedding。应该先执行 `await graphiti.embedder.create([name])` 再创建节点。

**Q: 我是不是每次都要手动生成 embedding？**  
A: 只有做直接 CRUD 时需要。使用 episodes 时，Graphiti 会在 LLM 处理过程中自动完成 embedding。

## 你在这一节里学会了什么

✅ **CRUD 操作**：能够直接创建、读取、更新和归档节点与边  
✅ **教育数据管理**：能精确管理学生和课程之间的结构化关系  
✅ **基于 UUID 的读取**：通过唯一标识精确找到并修改实体  
✅ **自定义实体类型**：把 Pydantic 模型与 CRUD 结合，获得更强类型安全  
✅ **安全数据实践**：优先采用归档，而不是直接删除教育记录  
✅ **验证模式**：会使用搜索和图数据库检查 CRUD 是否生效

## 下一步

**做得很好。** 你现在已经拥有“外科手术级别”的图谱操作能力，可以精确维护教育系统中的知识图结构。

**准备好直接构造结构化知识了吗？** 接下来前往 **[08_fact_triples](../08_fact_triples/)**，学习如何通过 subject-predicate-object 三元组来精确断言事实。

**下一步会学什么？**  
你将不再依赖自然语言抽取，而是开始直接声明结构化知识关系，用于课程建模和测评系统集成。

---

**关键结论：** CRUD 提供的是“精确控制力”，适合你明确知道该改什么的时候；episodes 提供的是“LLM 理解力”，适合你希望系统从内容中自动发现意义的时候。

_“CRUD 负责精度，episodes 负责智能。这两者结合起来，才是真正适合教育知识图谱的工作方式。”_
