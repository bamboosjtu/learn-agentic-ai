# Neo4j AuraDB

<https://neo4j.com/docs/aura/>

## 创建账户与实例

<https://neo4j.com/docs/aura/getting-started/create-account/>

<https://neo4j.com/docs/aura/getting-started/create-instance/>

## 连接到实例

<https://neo4j.com/docs/aura/getting-started/connect-instance/>

## 实例操作

<https://neo4j.com/docs/aura/managing-instances/instance-actions/>

## 开发

<https://neo4j.com/docs/aura/managing-instances/develop/>

## Cypher 入门

<https://neo4j.com/docs/getting-started/cypher/>

## Cypher Fundamentals 课程：1 小时学会 Cypher

<https://graphacademy.neo4j.com/courses/cypher-fundamentals/>

## Neo4j Python Driver 手册

其中包含示例代码：

<https://neo4j.com/docs/api/python-driver/current/>

<https://neo4j.com/docs/python-manual/current/>

## Cypher 25 速查表

<https://neo4j.com/docs/cypher-cheat-sheet/25/all/>

## Cypher 25 手册

<https://neo4j.com/docs/cypher-manual/25/introduction/>

本教程将带你使用 **Neo4j AuraDB** 从零开始构建一个知识图谱。AuraDB 是 Neo4j 提供的云端图数据库服务。我们将使用 **Cypher** 查询语言来建模和查询数据，并使用 **Python** 以编程方式连接数据库。

-----

## 1. 什么是知识图谱？

知识图谱是一种把数据表示为“实体网络及其关系”的方式。它不是通过行和列组成的表来组织数据，而是通过 **节点（nodes）** 来表示实体，通过 **关系（relationships）** 来表示连接。这种模型在表达复杂且高度互联的数据时非常灵活且强大，例如社交网络、供应链、生命科学网络等。

**Neo4j** 是领先的图数据库平台，而 **AuraDB** 是它的全托管云服务。AuraDB 会替你完成数据库的部署、维护和扩缩容。

-----

## 2. 搭建你的 Neo4j AuraDB 实例

首先，你需要创建一个免费的 Neo4j AuraDB 账户，并启动一个新的数据库实例。

### 创建账户

1. 进入 [Neo4j Aura 注册页](https://www.google.com/search?q=https://neo4j.com/cloud/aura-db-registration/)。
2. 使用邮箱和密码注册，或者绑定 Google / GitHub 账户。
3. 按照页面提示完成账户验证。

### 创建实例

创建账户后，系统会引导你创建一个新的 AuraDB 实例。

1. 选择创建新实例，并选择 **Free** 免费层，这对本教程来说已经足够。
2. 选择一个离你地理位置较近的云服务商和区域，以降低延迟。
3. 系统会自动创建实例，并提供一个连接数据库所需的密码。**请妥善保存这个密码**，因为它之后不会再次完整显示。实例的连接 URI 和用户名可以在实例凭证页面中找到。

-----

## 3. 连接到你的实例

你可以用多种方式连接 AuraDB 实例。

### 使用 Neo4j Browser

最简单的方式是使用网页端的 Neo4j Browser。

1. 在 AuraDB 控制台里，点击实例旁边的 **“Open”** 按钮。
2. 系统会在新标签页中打开 Neo4j Browser。
3. 使用用户名（通常是 `neo4j`）和你之前保存的密码登录。

Browser 提供了一个交互式环境，你可以执行 Cypher 查询，并把结果可视化成图。

### 用 Python 连接

如果你要开发应用，一般会通过驱动程序以编程方式连接数据库。这里我们使用官方的 Neo4j Python Driver。

首先，用 pip 安装驱动：

```bash
pip install neo4j
```

然后，使用 AuraDB 实例页面里的凭据建立连接。连接 URI 通常长这样：`neo4j+s://xxxxxx.databases.neo4j.io`

下面是一个用于测试连接的简单 Python 脚本：

```python
from neo4j import GraphDatabase

# 替换为你自己的实例 URI、用户名和密码
URI = "neo4j+s://your-aura-instance-uri.databases.neo4j.io"
AUTH = ("neo4j", "your-password")

def check_connection(driver):
    """检查是否成功连接到数据库。"""
    try:
        driver.verify_connectivity()
        print("Connection successful!")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        check_connection(driver)
```

运行这个脚本。如果输出 “Connection successful!” ，说明连接已经正常，可以开始构建图谱了。

-----

## 4. Cypher 入门：图数据库的语言

**Cypher** 是专门为图设计的声明式查询语言。它使用 ASCII 图形风格的语法来表示节点和关系，因此读写起来都比较直观。

### 基础 Cypher 语法

* **节点** 用圆括号表示：`()`
* **关系** 用箭头表示：`-[]->` 或 `<-[]-`
* **标签（Label）** 用来定义节点类型：`(:Person)`
* **关系类型（Relationship Type）** 用来定义连接的类型：`-[:ACTED_IN]->`
* **属性（Properties）** 是存储在节点或关系上的键值对：`(p:Person {name: 'Tom Hanks'})`

### 常用 Cypher 子句

* **`CREATE`**：创建节点和关系
* **`MATCH`**：在图中匹配模式
* **`MERGE`**：结合 `MATCH` 和 `CREATE`，如果模式存在就匹配，不存在就创建，非常适合避免重复数据
* **`RETURN`**：指定查询返回哪些内容
* **`SET`**：修改节点或关系属性
* **`DELETE`**：删除节点或关系

-----

## 5. 构建一个电影知识图谱

下面我们构建一个简单的电影与演员知识图谱。

### 第一步：创建 `Movie` 节点

先添加电影 *The Matrix*。一个电影有 `title` 和 `released` 年份。

在 Neo4j Browser 或通过 Python 执行下面的语句：

```cypher
CREATE (m:Movie {title: 'The Matrix', released: 1999})
```

### 第二步：创建 `Person` 节点

现在添加演员：

```cypher
CREATE (p1:Person {name: 'Keanu Reeves'})
CREATE (p2:Person {name: 'Carrie-Anne Moss'})
CREATE (p3:Person {name: 'Laurence Fishburne'})
```

### 第三步：创建关系

图数据库真正的力量来自关系。下面把演员和电影通过 `ACTED_IN` 关系连接起来：

```cypher
MATCH (p:Person {name: 'Keanu Reeves'}), (m:Movie {title: 'The Matrix'})
CREATE (p)-[:ACTED_IN]->(m)

MATCH (p:Person {name: 'Carrie-Anne Moss'}), (m:Movie {title: 'The Matrix'})
CREATE (p)-[:ACTED_IN]->(m)

MATCH (p:Person {name: 'Laurence Fishburne'}), (m:Movie {title: 'The Matrix'})
CREATE (p)-[:ACTED_IN]->(m)
```

### 第四步：查询图谱

现在数据已经建好了，我们可以开始提问。

**查询：谁出演了 *The Matrix*？**

```cypher
MATCH (p:Person)-[:ACTED_IN]->(m:Movie {title: 'The Matrix'})
RETURN p.name
```

**查询：Keanu Reeves 演过哪些电影？**

```cypher
MATCH (p:Person {name: 'Keanu Reeves'})-[:ACTED_IN]->(m:Movie)
RETURN m.title
```

-----

## 6. 用 Python 构建知识图谱

接下来，我们用 Python 把向知识图谱中写入数据的过程自动化。下面这个脚本会连接到 AuraDB，清空已有数据，然后加载一小批电影和演员数据。

```python
from neo4j import GraphDatabase

# --- 连接信息 ---
# 替换成你自己的实例 URI、用户名和密码
URI = "neo4j+s://your-aura-instance-uri.databases.neo4j.io"
AUTH = ("neo4j", "your-password")

# --- 示例数据 ---
movie_data = [
    {
        "title": "The Matrix", "released": 1999,
        "actors": ["Keanu Reeves", "Carrie-Anne Moss", "Laurence Fishburne"]
    },
    {
        "title": "The Matrix Reloaded", "released": 2003,
        "actors": ["Keanu Reeves", "Carrie-Anne Moss", "Laurence Fishburne"]
    },
    {
        "title": "John Wick", "released": 2014,
        "actors": ["Keanu Reeves", "Michael Nyqvist", "Alfie Allen"]
    }
]

def add_movies(driver, movies):
    """向图中写入电影和演员数据。"""
    with driver.session() as session:
        # 清空已有数据
        session.run("MATCH (n) DETACH DELETE n")
        print("Cleared existing data.")

        for movie in movies:
            # 使用 MERGE 避免重复创建电影节点
            session.run("""
                MERGE (m:Movie {title: $title})
                SET m.released = $released
            """, title=movie['title'], released=movie['released'])

            for actor_name in movie['actors']:
                # 对演员和关系也使用 MERGE
                session.run("""
                    MATCH (m:Movie {title: $title})
                    MERGE (p:Person {name: $name})
                    MERGE (p)-[:ACTED_IN]->(m)
                """, title=movie['title'], name=actor_name)
        print("Data loaded successfully.")

def find_keanu_movies(driver):
    """查询 Keanu Reeves 出演的所有电影。"""
    with driver.session() as session:
        result = session.run("""
            MATCH (p:Person {name: 'Keanu Reeves'})-[:ACTED_IN]->(m:Movie)
            RETURN m.title AS movie_title
        """)
        print("\nMovies starring Keanu Reeves:")
        for record in result:
            print(f"- {record['movie_title']}")

if __name__ == "__main__":
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        print("Connected to Neo4j AuraDB.")

        add_movies(driver, movie_data)
        find_keanu_movies(driver)
```

**运行方式：**

1. 用你自己的 `URI` 和 `AUTH` 替换占位值
2. 把代码保存为 Python 文件，例如 `build_kg.py`
3. 在终端中运行：`python build_kg.py`

你会看到连接成功、数据清空、数据写入成功，以及最终查询结果的输出。

-----

## 7. 管理你的 AuraDB 实例

AuraDB 控制台提供了一些常见的实例管理操作：

* **Pause**：如果暂时不用实例，可以暂停它来节省资源（付费版可用）。免费实例会在一段时间无活动后自动暂停。
* **Resume**：恢复已暂停的实例。
* **Delete**：永久删除实例及其全部数据。

这些操作都可以在 Neo4j Aura 控制台的实例列表中找到。

-----

## 8. 继续学习

本教程只覆盖了基础，但知识图谱世界非常大。你可以继续深入这些资源：

* **Cypher Fundamentals Course**：Neo4j GraphAcademy 提供的一小时免费课程：<https://graphacademy.neo4j.com/courses/cypher-fundamentals/>
* **Neo4j Python Driver Manual**：Python 驱动的详细文档：<https://neo4j.com/docs/python-manual/current/>
* **Cypher Cheat Sheet**：Cypher 子句与函数的速查表：<https://neo4j.com/docs/cypher-cheat-sheet/25/all/>
* **官方 AuraDB 文档**：AuraDB 全部功能的详细说明：<https://neo4j.com/docs/aura/>

按照本教程操作后，你已经成功完成了这些事情：

- 创建了一个 Neo4j AuraDB 实例
- 用图结构建模了一个知识领域
- 同时使用 Cypher 和 Python 构建并查询了你的第一个知识图谱

接下来就可以继续扩展你的图谱了。
