# 第 29 阶段：使用 OpenAI Vector Stores 的托管式（Agentic）RAG

这一课先讲 Retrieval-Augmented Generation（RAG）的基础概念，然后展示如何通过 OpenAI 托管的 vector stores，跳过自建数据库的复杂性。我们使用 Agent SDK 的 `FileSearchTool`，把检索能力变成 agent 可以按需调用的工具。

你可以把它理解成 **Agentic RAG**：agent 自己判断何时需要取回事实，再把这些信息融合进回答中。整个课程都围绕 Python 和 Chainlit 展开。

## 快速概念检查

- **为什么需要 RAG？** 模型会遗忘细节。RAG 把最新资料保存在模型之外，只在需要时取回来，保证回答更及时、更有依据。
- **为什么使用托管式 RAG？** 自己托管向量数据库需要时间和成本，而 OpenAI 的托管式 vector store 帮你处理存储、索引和扩展。
- **为什么叫 Agentic RAG？** 不是把所有上下文都塞进每一个 prompt，而是让 agent 在识别到用户需要事实信息时，主动调用检索工具。工具就是 agent 的动作能力。

## 整条流程如何工作

1. **收集资料**：把学习材料（文本文件、转录稿等）放进一个文件夹
2. **切分文本**：vector store 会把长文件切成较小片段，便于判断相关性
3. **创建 embeddings**：每个片段都会变成一个表示语义的向量
4. **存储向量**：托管式 store 保存这些向量及其来源元数据
5. **按需检索**：agent 调用 `FileSearchTool`，返回最适合当前问题的文本片段
6. **生成答案**：agent 把检索片段与用户问题一起交给模型，生成有依据的回答

## 你将构建什么

- 一个在 OpenAI 控制台中创建的托管 vector store
- 一个可通过 `FileSearchTool` 搜索该 store 的 Chainlit agent
- 一个能够依赖已存资料来回答问题的友好聊天应用

## 文件结构

```
29_managed_rag_service/
├── README.md                  # 当前文件
├── .env.example               # 复制为 .env 并填入密钥
├── pyproject.toml             # uv 在这里管理依赖
├── prepare_vector_store.py    # 可选辅助脚本，用于一次性同步多个文件
├── main.py                    # 使用托管 store 的 Chainlit 应用
└── docs/
    └── panaversity_faq.txt    # 可上传的示例文件
```

## 第 1 步：设置 `uv`

让 `uv` 负责管理依赖。

```bash
cd 29_managed_rag_service
uv init .
uv venv
source .venv/bin/activate
uv add chainlit openai python-dotenv agents
```

最后一条命令会把依赖写入 `pyproject.toml`，并安装到虚拟环境中。

## 第 2 步：填写密钥

复制示例文件，并填入自己的密钥：

```bash
cp .env.example .env
```

打开 `.env` 并设置：

```
OPENAI_API_KEY=sk-...
```

先把 `OPENAI_VECTOR_STORE_ID` 留空，等创建好 vector store 后再填。

## 第 3 步：在控制台中创建托管 Vector Store

1. 打开 [platform.openai.com](https://platform.openai.com/) 并登录
2. 进入 **Data** 区域，选择 **Vector stores**
3. 点击 **Create vector store**
4. 给它取一个名字，例如 `panaversity-notes`
5. 上传当前目录里的示例文件 `docs/panaversity_faq.txt`（或者上传你自己的资料）
6. 上传完成后，复制 **Vector store ID**（以 `vs_...` 开头）

把这个 ID 写入 `.env`：

```
OPENAI_VECTOR_STORE_ID=vs_...
```

保管好这个 ID。以后任何需要访问这些资料的 agent，都可以复用同一个 store。

## 第 4 步：启动 Chainlit 应用

```bash
chainlit run main.py -w
```

在浏览器里打开链接，提一个问题，例如：

> How many hours should I study each week?

agent 会判断是否需要调用资料，随后使用托管的 `FileSearchTool`，读取 FAQ 文件，并根据检索到的片段进行回答。

## 第 5 步：进一步探索

- 想上传自己的资料时，编辑 `docs/` 目录，并在加入新文件后重新运行准备脚本
- 修改 `main.py` 中的 `max_num_results`，调整 agent 一次读取多少片段
- 可以把它与前面的部署步骤结合，发布一个托管式 RAG 助手

你现在已经知道如何把自己的数据和 OpenAI 的托管检索工具结合起来了。这让你可以处理更大的文档，而无需自己维护额外服务器。
