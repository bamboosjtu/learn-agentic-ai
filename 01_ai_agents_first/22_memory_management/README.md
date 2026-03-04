# Embeddings 与向量搜索入门指南

---

## 1. 为什么我们需要它？

当你在 Google 中输入内容时，它并不只是查找完全匹配的单词，而是会尝试理解你**真正的意思**。
传统搜索 = 关键词匹配。
但如果你想找的是**语义相近的内容**，而不是字面相同的词呢？
这就是 **embeddings + 向量搜索** 发挥作用的地方。

---

## 2. 什么是 Embeddings？

**定义：**
**Embedding（嵌入）** 可以理解为数据的**数学指纹**。它是一串数字（向量），用于表示文本、图像或音频的含义或特征。

### 关键点：

* Embeddings 能捕捉**语义含义**。
* 相似的东西 -> 相似的 embedding（数值空间里距离更近）。
* 不相似的东西 -> embedding 距离更远。

### 示例：

* 单词：**"Dog"** -> `[0.12, -0.45, 0.88, ...]`
* 单词：**"Puppy"** -> `[0.15, -0.44, 0.90, ...]`
* 单词：**"Car"** -> `[0.92, 0.13, -0.77, ...]`

这里，**dog** 和 **puppy** 会彼此接近，而 **car** 会离得很远。

---

## 3. 类比：图书馆与书籍

想象一座图书馆：

* 每本书都有一个独特的**条形码**。
* 条形码浓缩表达了这本书的信息。
* 即使两本书标题不同，如果它们讲的是相似主题，它们的条形码也可能很接近。

在 AI 里，**条形码 = embedding**。

---

## 4. 什么是向量搜索？

**定义：**
向量搜索就是在数据库中**找到最接近的 embeddings** 的过程。
它回答的问题是：

> “哪些项目和这个最相似？”

### 示例：

查询：`"cute puppy pictures"`

步骤：

1. 把查询转换成一个 embedding。
2. 把它与数据库中的所有 embeddings 进行比较。
3. 返回那些**距离最近**的结果（使用距离计算）。

这也叫做 **相似度搜索**。

---

## 5. 我们如何衡量“接近”？

Embeddings 存在于**向量空间**中（可以把它想成坐标）。
我们用**距离**或**相似度指标**来衡量接近程度：

* **余弦相似度（Cosine similarity）** -> 衡量两个向量夹角的相似程度。
* **欧氏距离（Euclidean distance）** -> 直线距离。

示例（二维可视化）：

* `"Dog"` 在 `(1,2)`
* `"Puppy"` 在 `(1.1, 2.1)`
* `"Car"` 在 `(5,7)`

Dog 和 Puppy 更接近，因此它们的相关性更高。

---

## 6. Embeddings + 向量搜索的工作流程

1. **输入**（文本、图像等）
2. **Embedding 模型** 将其转换为向量
3. **存储 embeddings** 到数据库中（如 Pinecone、FAISS、Weaviate 等向量数据库）
4. **查询** 也会被转换为 embedding
5. **搜索引擎** 把查询向量和已存向量进行比较
6. **返回最接近的匹配项**

---

## 7. 它们用在哪些地方？

* **搜索引擎**：Google、YouTube、ChatGPT 记忆
* **推荐系统**：Netflix 推荐相似电影
* **聊天机器人**：回忆过去的对话（记忆）
* **图像搜索**：查找视觉上相似的图片
* **欺诈检测**：匹配异常行为模式

---

## 8. Python 小示例（使用 OpenAI + FAISS）

```python
from openai import OpenAI
import faiss
import numpy as np

# 1. Get embeddings from OpenAI
client = OpenAI()

texts = ["dog", "puppy", "car"]
embeddings = [client.embeddings.create(model="text-embedding-3-small", input=t).data[0].embedding for t in texts]

# 2. Store in FAISS (vector database)
dimension = len(embeddings[0])
index = faiss.IndexFlatL2(dimension)  # L2 = Euclidean distance
index.add(np.array(embeddings))

# 3. Query search
query = "cute puppy"
query_embedding = client.embeddings.create(model="text-embedding-3-small", input=query).data[0].embedding

D, I = index.search(np.array([query_embedding]), k=2)  # find top-2 matches

print("Query:", query)
print("Closest matches:", [texts[i] for i in I[0]])
```

输出通常会是：`["puppy", "dog"]`

---

## 9. 总结

* **Embedding** = 含义的数字表示（指纹）
* **向量搜索** = 在大量指纹中寻找最接近的那些
* 两者结合起来 -> 机器就能理解超越字面词汇的“相似性”

---

## 10. 一个直观的心理画面

把它想成一片**星系**。

* 每颗星星 = 一个数据点（文本、图像、声音）
* 靠得近的星星 = 含义相近
* 向量搜索 = 一台望远镜，用来找到离你的查询“星星”最近的其他星星

---

记住这句话：
*Embedding = 表示方式，Vector Search = 比较引擎*

这样你就不容易再把它们混淆了。

# Mem0 + AI Agents 入门指南

使用 [Mem0](https://mem0.ai) + [OpenAI Agents SDK](https://github.com/openai/agents)，让你的 AI 助手拥有**记忆能力**。
有了记忆后，助手可以跨会话**记住你的名字、偏好和过去的对话**。

---

## 为什么记忆很重要

没有记忆时，每次和 AI 聊天都像是在和陌生人第一次见面：

* 你每次都得重复自己的名字
* 它会立刻忘记你的偏好
* 对话体验会显得机械

有了 **Mem0 记忆**：

* AI 能记住你的名字、爱好和喜欢的食物
* 能根据你的历史提供更个性化的回复
* 对话会更自然、更像和真人交流

---

## 前置条件（开始之前）

1. 已安装 **Python 3.10+**
2. 具备**基础 Python 知识**（变量、函数、导入）
3. 准备好 API Key：

   * [Mem0 API Key](https://mem0.ai)（用于记忆存储）
   * [Gemini API Key](https://ai.google.dev/)（作为 LLM 大脑）

---

## 安装

打开终端并运行：

```bash
uv add openai-agents mem0ai python-dotenv
```

---

## 配置 API Keys

1. **获取 Mem0 API Key**

   * 在 [Mem0](https://mem0.ai) 注册
   * 从控制台复制你的 key

2. **获取 Gemini API Key**

   * 打开 [Google AI Studio](https://aistudio.google.com)
   * 创建并复制一个新的 API key

3. **创建 `.env` 文件**
   在项目目录中创建 `.env`：

   ```env
   GEMINI_API_KEY=your_gemini_api_key
   MEM0_API_KEY=your_mem0_api_key
   ```

不要共享你的 API keys，也不要把它们上传到 GitHub。

---

## 代码概览

### 1. 连接 Gemini（AI 大脑）

```python
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
```

### 2. 设置 Mem0（记忆笔记本）

```python
mem0 = MemoryClient()
```

### 3. 创建记忆工具（保存与回忆）

```python
@function_tool
def add_memory(query: str, user_id: str) -> str:
    return mem0.add([{"role": "user", "content": query}], user_id=user_id)

@function_tool
def search_memory(query: str, user_id: str) -> str:
    return mem0.search(query, user_id=user_id, limit=3)
```

### 4. 构建 Agent（助手本体）

```python
agent = Agent(
    name="Memory Assistant",
    instructions="""You are a helpful assistant with memory.
    Always check memory first before answering.
    Save new details about the user whenever possible.""",
    tools=[search_memory, add_memory],
    model=llm_model,
)
```

---

## 运行示例

将代码保存为 `main.py`，然后运行：

```bash
uv run main.py
```

### 示例交互

**第一次聊天：**

```
User: My name is Wania and I like programming and my favourite dish is biryani `wania_123`
Agent: Got it! I’ll remember that.
```

**第二次聊天：**

```
User: What is my name and what I like to do and user_id is `wania_123`?
Agent: Your name is Wania, you like programming, and your favourite dish is biryani.
```

这个 agent 记住你了。

---

## 初学者需要掌握的关键概念

* **LLM（Large Language Model，大语言模型）**：AI 的“大脑”（这里是 Gemini）
* **Mem0**：保存记忆的“笔记本”
* **Agent**：会使用工具和记忆的助手
* **Tools**：像 `add_memory` 和 `search_memory` 这样的函数
* **User ID**：类似一个文件夹名，用来区分不同用户的记忆

---

## 常见问题与解决方法

* **找不到记忆** -> 确保保存和查询时使用的是**同一个 `user_id`**

* **API key 报错** -> 检查 `.env` 文件，并重新加载终端环境

* **找不到模块** -> 运行：

  ```bash
  uv add openai-agents mem0ai python-dotenv
  ```

---

## 练习任务

你可以自己试一下：

1. 添加一条记忆：`"My favorite color is blue."`
2. 稍后再问：`"What’s my favorite color?"`
3. 看看 agent 是否能记住

---

## 最佳实践

* 为每个人始终使用**唯一的 user ID**
* 不要存储**敏感信息**（例如密码）
* 先从**简单信息**开始，再逐步扩展到复杂数据
* 与 agent 交流时，尽量使用**清晰明确的表达**

---

## 下一步

* 创建**多个 agent**（例如旅行规划师、健康教练），共享同一份记忆
* 使用**过滤器和元数据**进行更高级的记忆搜索
* 构建一个**聊天 Web 应用**，让用户和带记忆的 AI 直接交互

---

## 结语

你已经学会如何使用 Mem0 为 AI 助手加入**记忆能力**。
现在你的 agent 可以记住名字、偏好以及更多信息，让对话更智能，也更像人与人之间的交流。

继续实验下去，你很快就能构建出真正像“长期陪伴型助手”的 AI 应用。
