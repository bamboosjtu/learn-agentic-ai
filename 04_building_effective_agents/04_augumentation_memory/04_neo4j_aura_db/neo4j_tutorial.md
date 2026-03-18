# 使用 Neo4j AuraDB 构建知识图谱：完整教程

Neo4j AuraDB 是 Neo4j 提供的全托管云图数据库服务。它为构建图应用提供了可靠、安全、自动化的平台，你不需要自己管理数据库运维。在本教程中，我们将完整走一遍使用 Neo4j AuraDB 构建一个简单**知识图谱**的过程，示例场景采用社交网络。我们会覆盖从创建 AuraDB 实例，到使用 Cypher 图查询语言（这里使用 **Cypher 25**，也就是 Neo4j 最新查询语言版本）进行查询，再到通过 Python 代码访问数据库的完整流程。

本指南面向初学者，包含分步骤说明、代码示例以及实践建议，适合作为入门教程。

## 1. 搭建 Neo4j AuraDB

在开始构建知识图谱之前，我们需要先创建一个 Neo4j AuraDB 实例并连接上它。

### 1.1 创建 Neo4j AuraDB 账户和实例

**注册 AuraDB：**  
如果你还没有 AuraDB 账户，可以先打开 Neo4j Aura 控制台 **console.neo4j.io** 并创建账户。你可以使用邮箱注册，也可以直接用 Google 账户登录。Aura 控制台就是你管理 Neo4j 数据库实例的网页界面。

**创建新的 AuraDB 实例：**  
登录之后，在 Aura 控制台里新建一个数据库实例。对于初学项目，直接选免费层就够了。

1. 在 Aura 控制台点击 **“New Instance”**
2. 选择 **“Create Free Instance”**
3. 为实例命名，例如 `MyKnowledgeGraph`，并选择 **Neo4j 版本**。建议使用当前最新可用的版本，也就是 Neo4j 5.x，它支持 Cypher 25
4. Aura 会自动创建实例。在创建过程中会显示自动生成的用户名和密码，请**复制并保存好**，也可以下载 TXT 文件保存凭据。后续连接数据库必须用到这些信息
5. 确认创建提示后点击 **Continue**

**说明：**  
每个账户通常只能拥有一个免费实例。AuraDB Free 有一些限制，例如节点和关系数量上限。免费实例如果连续 72 小时没有活动会自动暂停，暂停超过 30 天后实例会被删除，所有数据都会丢失。如果你要长期保存数据，需要定期使用或升级套餐。

### 1.2 连接到 AuraDB 实例

当你的 AuraDB 实例启动完成后，在控制台里应该能看到状态为 **Active**。这时可以通过多种方式连接数据库：

* **Neo4j AuraDB Workspace（网页界面）**  
  在 Aura 控制台中，点击实例旁边的 **“Open”** 按钮。系统会在浏览器中打开 Neo4j Workspace，它整合了 Neo4j Browser 和其他工具。然后输入你刚才保存的用户名和密码并点击 **Connect**。  
  Workspace 非常适合交互式执行 Cypher 查询和可视化图结构。

* **Connection URI**  
  在 Aura 控制台实例详情页中，你会看到一个 **Connection URI**，通常长这样：

  ```
  neo4j+s://<your-instance-id>.databases.neo4j.io
  ```

  这是一个 **Bolt 协议 URI**。其中 `neo4j+s://` 表示通过安全连接访问 Neo4j。你可以用它搭配用户名和密码，在 Neo4j Desktop、Cypher Shell 或各种编程语言中建立连接。例如：

  * **Neo4j Desktop**：复制这个 URI，在 Neo4j Desktop 中添加 Remote Graph，填入 URI 和用户名密码后连接
  * **Cypher Shell（命令行）**：安装 Neo4j Cypher Shell 工具后，可以执行：

    ```bash
    cypher-shell -a <bolt-uri> -u <username> -p <password>
    ```

    对 Aura 来说，大致就是：

    ```bash
    cypher-shell -a neo4j+s://... -u neo4j -p <yourPassword>
    ```

本教程主要聚焦 **Neo4j Python Driver**，因为我们的目标是把 Cypher 和 Python 集成起来。

### 1.3 实例管理基础：暂停、恢复、删除

Neo4j AuraDB 提供了几个实例管理动作，可以在 Aura 控制台的实例卡片上找到：

* **Pause / Resume**  
  对付费版（Professional / Enterprise）来说，可以手动暂停实例，暂停后计算会停止，费用也会下降，之后再恢复即可。  
  *AuraDB Free 不能手动暂停*，它会在 72 小时无活动后自动暂停。

* **Clone**  
  你可以克隆一个实例，得到数据库的副本。这个功能适合创建开发环境、副本测试、升级验证等场景。克隆时可以创建新实例，也可以覆盖一个已有实例，但覆盖会替换目标实例中的数据。

* **Delete**  
  如果不再需要某个实例，可以删除它。通常需要手动输入实例名确认，然后点击 **Destroy**。  
  *注意：删除不可恢复，所有数据都会永久丢失。*

## 2. Cypher 与图数据模型简介

在真正开始构建知识图谱之前，先快速了解一下 **Cypher** 以及图数据库底层使用的数据模型。

**Cypher 查询语言：**  
Cypher 是 Neo4j 的声明式图查询语言，很多人会把它理解为“图数据库版 SQL”。如果你熟悉 SQL，会觉得 Cypher 的结构有点像，但它更适合表达图中的路径与模式匹配。Cypher 使用非常直观的 ASCII 图形语法来描述图结构。

例如：

```cypher
(a:Person)-[:KNOWS]->(b:Person)
```

这个模式表示两个 `Person` 节点，以及它们之间的一条 `KNOWS` 关系。Cypher 的设计目标就是让图查询像写自然语言一样直观。

**图数据模型：**  
在 Neo4j 里，数据由 **节点（nodes）** 和 **关系（relationships）** 组成：

* **节点（Nodes）**  
  节点表示实体或对象，例如人、地点、物品、概念等。节点可以有一个或多个 **标签（labels）**，用来表示它属于什么类型。例如表示人的节点可以打上 `Person` 标签，表示公司的节点可以打上 `Company` 标签。标签在 Neo4j 中类似类别或类型，也有助于查询优化。节点还可以有 **属性（properties）**，也就是键值对数据，例如 `name`、`age` 等。

* **关系（Relationships）**  
  关系连接两个节点，用来表示它们之间的关联，例如 `:FRIENDS_WITH`、`:WORKS_FOR`、`:LIKES`。关系总是有一个**类型**，也有方向。你可以把关系类型理解成把两个实体连接起来的“动词”。在 Cypher 里，关系通常写成 `-[]->`。例如：

  ```cypher
  (p:Person)-[:FRIENDS_WITH]->(q:Person)
  ```

  表示 p 和 q 之间存在 `FRIENDS_WITH` 关系。关系也可以带属性，例如一条 `FRIENDS_WITH` 关系可以加上 `since: 2015`，表示从 2015 年起成为朋友。

* **属性（Properties）**  
  节点和关系都可以存属性。比如一个 `Person` 节点可以有 `name="Alice"`、`age=30`，一条 `FRIENDS_WITH` 关系可以有 `since="2015"`。Cypher 中属性写在花括号里，例如：

  ```cypher
  (:Person {name: "Alice", age: 30})
  ```

图数据库非常适合表达自然语言里的事实。例如：

- Sally 喜欢 Graphs
- Sally 和 John 是朋友
- Sally 在 Neo4j 工作

用图建模会非常自然，因为这些事实本来就是“实体 + 关系”的结构。

**Cypher 25：**  
Neo4j 会持续演进 Cypher。Cypher 25 指的是当前 Neo4j 5.x 体系下的最新语言版本。AuraDB 会保持实例自动更新，所以通常默认就能用上最新 Cypher 特性。

### 2.1 本教程的数据模型：社交网络图

本教程使用一个**社交网络**作为示例数据模型：

* 我们会创建带标签 **`Person`** 的节点，用来表示社交网络中的人。每个 `Person` 节点至少包含一个 `name` 属性，后续也可以扩展更多属性，例如年龄
* 我们会用 **`KNOWS`** 关系把 `Person` 节点连起来，表示两个人认识或是朋友关系
* 为了让图更丰富，我们也可以加入更多类型的节点和关系。例如：
  - `Interest` 节点，以及 `(:Person)-[:LIKES]->(:Interest)`
  - `Company` 节点，以及 `(:Person)-[:WORKS_FOR]->(:Company)`

在本教程里，我们会先聚焦最简单的 `Person` 和 `KNOWS`，你后续可以自己扩展出更复杂的知识图谱。

**为什么要用图？**  
社交网络本来就是图结构。人和人之间形成关系网络，而图数据库非常适合处理这种结构。例如“朋友的朋友”这类查询，用图数据库会非常自然。

## 3. 写入数据：构建知识图谱

当 AuraDB 实例已经准备好，也理解了图模型之后，就可以开始往里面写数据了。我们会展示两种方式：

1. 直接在 Neo4j Browser 中运行 Cypher
2. 用 Python Driver 通过代码写入

在实际项目里，这两种方式往往都会用到。比如你可以在 Browser 中快速调试，在脚本里批量导入数据。

### 3.1 在 Neo4j Browser 中用 Cypher 创建节点和关系

如果你已经打开 AuraDB 的 Neo4j Browser，就可以直接执行 Cypher 来插入数据。下面我们先创建一个很小的社交网络：

```cypher
// 创建两个 Person 节点：Alice 和 David，以及一条 KNOWS 关系
CREATE (alice:Person {name: "Alice", age: 25});
CREATE (david:Person {name: "David", age: 24});
CREATE (alice)-[:KNOWS]->(david);
```

这三条 `CREATE` 语句会创建两个 `Person` 节点，以及一条从 Alice 指向 David 的 `KNOWS` 关系。运行之后，Browser 通常会直接把结果以图形式可视化出来。

你也可以把这段写成一条语句：

```cypher
CREATE (alice:Person {name: "Alice", age: 25})-[:KNOWS]->(david:Person {name: "David", age: 24});
```

这和前面的三条语句效果一样，只是把整个图模式一次性写出来。

**实践建议：**  
在真实项目里，通常应该给节点定义某种唯一标识，而不是只靠名字，避免重复创建。例如你可以给 `Person.name` 加唯一约束：

```cypher
CREATE CONSTRAINT FOR (p:Person) REQUIRE p.name IS UNIQUE
```

这样数据库会拒绝重复的 `Person.name`，同时也会自动建立索引。

### 3.2 用 Neo4j Python Driver 创建数据

接下来用 Python 来做同样的事情。这非常适合从外部数据源导入，或者在应用里动态写图。

先安装驱动：

```bash
pip install neo4j
```

然后编写 Python 代码连接 AuraDB。请把下面的 `<URI>`、`<username>`、`<password>` 替换成你自己的实例信息：

```python
from neo4j import GraphDatabase

# AuraDB 连接信息，请替换成你自己的
URI = "neo4j+s://<your-instance-id>.databases.neo4j.io"
AUTH = ("neo4j", "<your-password>")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

    summary = driver.execute_query(
        """
        CREATE (a:Person {name: $name})
        CREATE (b:Person {name: $friendName})
        CREATE (a)-[:KNOWS]->(b)
        """,
        name="Alice", friendName="David",
        database_="neo4j"
    ).summary()

    print(f"Created {summary.counters.nodes_created} nodes in {summary.result_available_after} ms.")
```

这里做了几件事：

- 使用 AuraDB 的安全连接 URI `neo4j+s://`
- 用用户名密码建立连接
- 通过 `execute_query` 执行一段 Cypher
- 使用参数 `$name` 和 `$friendName` 传值，而不是把数据直接拼进查询字符串

运行后，你会看到类似：

```text
Created 2 nodes in 123 ms.
```

这说明节点写入成功。

**说明：**  
AuraDB 的默认数据库名通常是 **`neo4j`**，所以这里显式传了 `database_="neo4j"`。如果不写，驱动一般也会自动使用默认数据库。

## 4. 用 Cypher 查询知识图谱

图里有了数据之后，就可以开始查询了。Neo4j 中最常用的是 `MATCH`，它类似 SQL 的 `SELECT`，但它不是选表，而是匹配图模式。然后用 `RETURN` 返回结果。

### 4.1 在 Neo4j Browser 中查询

假设我们想查出所有人以及他们认识的人，可以执行：

```cypher
MATCH (p:Person)-[:KNOWS]->(friend:Person)
RETURN p.name AS person, friend.name AS knows_friend;
```

这个查询会找出所有形如 `Person -> KNOWS -> Person` 的模式，并返回两个人的名字。

查询要点：

- `(p:Person)` 表示匹配带 `Person` 标签的节点，并绑定到变量 `p`
- `friend:Person` 同理
- `-[:KNOWS]->` 表示只匹配这个方向的关系
- `AS` 可以给返回列重命名，方便阅读

如果你想让这个社交图更丰富一点，可以再加入更多数据：

```cypher
CREATE (bob:Person {name: "Bob", age: 28});
CREATE (alice)-[:KNOWS]->(bob);
CREATE (bob)-[:KNOWS]->(david);
```

现在图里有 Alice、Bob、David，Alice 认识 Bob 和 David，Bob 也认识 David。

可以试几个查询：

**查 Alice 直接认识谁：**

```cypher
MATCH (:Person {name:"Alice"})-[:KNOWS]->(friend:Person)
RETURN friend.name AS AliceFriend;
```

**查朋友的朋友：**

```cypher
MATCH (alice:Person {name:"Alice"})-[:KNOWS]->(friend:Person)-[:KNOWS]->(fof:Person)
RETURN friend.name AS AliceFriend, fof.name AS FriendOfFriend;
```

这会找出 Alice 的朋友，以及这些朋友认识的人。

**查共同朋友：**

```cypher
MATCH (a:Person {name:"Alice"})-[:KNOWS]->(x:Person)<-[:KNOWS]-(d:Person {name:"David"})
RETURN x.name AS MutualFriend;
```

这个查询的意思是：找出一个人 `x`，同时被 Alice 和 David 指向，也就是他们共同认识的人。

### 4.2 用 Python Driver 查询

同样的查询，也可以在 Python 里做：

```python
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    records, summary, keys = driver.execute_query(
        """
        MATCH (p:Person)-[:KNOWS]->(:Person)
        RETURN p.name AS name
        """,
        database_="neo4j"
    )

    for record in records:
        print(record.data())

    print(f"The query '{summary.query}' returned {len(records)} records in {summary.result_available_after} ms.")
```

这个例子会找出所有拥有至少一条 `KNOWS` 出边的人。

你也可以像这样传参：

```python
name_to_find = "Alice"
records, _, _ = driver.execute_query(
    "MATCH (p:Person {name: $name})-[:KNOWS]->(friend:Person) RETURN friend.name AS friend",
    name=name_to_find, database_="neo4j"
)

for record in records:
    print(f'{name_to_find} knows {record["friend"]}')
```

这样就能程序化地获取 Alice 的朋友列表。

### 4.3 更新与删除数据

除了查询之外，Cypher 还支持更新和删除：

**更新属性：**

```cypher
MATCH (p:Person {name: "Alice"})
SET p.age = 26;
```

**删除节点：**

```cypher
MATCH (p:Person {name: "Bob"})
DETACH DELETE p;
```

在 Neo4j 中，如果一个节点还有关系，不能直接删掉它，必须先删关系，或者使用 `DETACH DELETE` 一并删除节点及其关系。

## 5. 总结与下一步

到这里，我们已经完成了一个小型知识图谱的构建：它运行在 Neo4j AuraDB 上，用来表示一个社交网络，并且我们已经通过 Cypher 和 Python 两种方式查询了它。

本教程覆盖了：

- AuraDB 实例的创建与连接
- 图数据模型的核心概念：节点、关系、属性
- 用 Cypher 插入和查询图数据
- 用官方 Python Driver 连接 Neo4j，并在程序里执行查询

**关键回顾：**

* Neo4j AuraDB 提供了一个非常方便的云端 Neo4j 环境，而且有免费层，可以几分钟内启动
* 图数据模型非常适合表示知识图谱、社交网络等高度连接的数据
* Cypher 是强大的图查询语言，读写图模式都非常直观
* Python Driver 让你可以把图数据库能力接进应用、分析脚本或 notebook 中

**接下来可以继续做什么？**

在掌握这些基础后，你可以继续扩展知识图谱，例如：

- 加入更多节点和关系类型
- 学习索引和约束，提升查询效率并保证数据一致性
- 学习全文搜索和图算法
- 把 Neo4j 集成到更大的 Agent 或应用系统中

如果你想继续深入，建议看这些资源：

* **Neo4j Cypher Fundamentals 课程**：GraphAcademy 的交互式课程，适合巩固 Cypher 基础
* **Neo4j 官方文档与 Getting Started 指南**
* **Neo4j Python Driver Manual**
* **Neo4j 社区论坛与 Stack Overflow**

希望这份教程能帮你顺利入门 Neo4j AuraDB、Cypher 和 Python 的组合使用，并作为你后续构建知识图谱项目的起点。

**参考说明：** 本文内容和示例主要基于 Neo4j 官方文档与教程整理，包括 AuraDB 文档、Cypher 手册、Getting Started 指南，以及 Neo4j Python Driver 文档中的示例。
