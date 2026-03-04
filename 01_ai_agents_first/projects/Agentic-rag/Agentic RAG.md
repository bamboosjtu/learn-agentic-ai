# Agentic RAG

[在 Google Colab 中打开 Notebook](https://colab.research.google.com/drive/1QgAapf_z875sEev_O9COE7TPHIKEXx6r?usp=sharing)

# 代码讲解

这个 Notebook 演示了如何使用 Google Gemini 模型、ChromaDB 向量存储以及 OpenAI Agents SDK 来搭建一个检索增强生成（RAG）系统，并由 Agents SDK 协调整个流程。

## 主要内容

- 使用 Gemini 生成 embedding
- 使用 ChromaDB 存储向量
- 用 `@function_tool` 把知识库查询封装成 Agent 工具
- 通过 OpenAI Agents SDK 创建一个问答 Agent
- 让 Agent 从知识库中检索信息并回答问题
- 扩展知识库，让它也能读取 PDF 内容

## 整体流程

1. 配置 Gemini API Key
2. 初始化 ChromaDB 和 Gemini 客户端
3. 准备初始文档并生成 embedding
4. 把文档写入知识库
5. 创建 `answer_from_knowledge_base` 工具
6. 创建 `qa_agent`
7. 运行 Agent 问答
8. 上传 PDF，并把 PDF 内容也加入知识库
9. 再次运行 Agent，回答基于 PDF 的问题

## 这个示例的意义

这个 Notebook 的重点在于演示：

- 如何把“向量检索”包装成 Agent 可调用的工具
- 如何让 OpenAI Agents SDK 与 Gemini 兼容使用
- 如何把一个普通 RAG 系统做成“Agent + Tool”的形式

它是一个很适合入门的桥梁示例：介于“纯 RAG”与“真正的 Agentic RAG”之间。

## 环境配置与认证

- **导入模块：**
  导入了 `userdata`、`os`、`nest_asyncio`、`agents`（OpenAI Agents SDK）、`chromadb`、`google.genai` 以及 `langchain_community.document_loaders` 等必需库。
- **安装依赖：**
  通过 `!pip install` 安装关键依赖库。
- **API Key 设置：**
  使用 `userdata.get('GEMINI_API_KEY')` 安全读取 Gemini API Key，并写入 `os.environ`。同时做了检查，确保 key 存在。
- **Asyncio 补丁：**
  通过 `nest_asyncio.apply()` 让 `asyncio` 能在 Jupyter / Colab 环境下正常工作。
- **Tracing：**
  使用 `set_tracing_disabled(True)` 禁用 Agents SDK tracing，这在开发阶段通常更方便。

## 初始化客户端

- **ChromaDB 客户端：**
  `chromadb.Client()` 初始化了一个内存中的 ChromaDB 实例，用于存储和搜索向量 embedding。
- **Google GenAI 客户端：**
  `genai.Client(api_key=GEMINI_API_KEY)` 初始化 Gemini 客户端，用于生成 embedding 和回答内容。
- **兼容 OpenAI 的客户端：**
  创建了一个 `AsyncOpenAI` 客户端，并将其指向 Gemini 的 OpenAI 兼容端点：
  `https://generativelanguage.googleapis.com/v1beta/openai/`
  这样一来，原本面向 OpenAI API 设计的 Agents SDK 也能与 Gemini 一起工作。
  使用 `set_default_openai_client(external_client)` 后，这个客户端会作为 Agents SDK 的全局默认客户端。

## 创建知识库（初始数据）

- **文档数据：**
  定义了一组示例文档 `documents` 和对应 ID `doc_ids`。
- **Embedding 模型：**
  选择 `gemini-embedding-exp-03-07` 作为 embedding 模型。
- **生成 Embedding：**
  使用 `client.models.embed_content` 为文档生成向量。这里设置了 `RETRIEVAL_DOCUMENT` 任务类型，以优化检索效果。
- **创建 ChromaDB Collection：**
  `chroma_client.get_or_create_collection(name="knowledge_base1")` 用于创建或获取知识库 collection。
- **写入数据：**
  使用 `collection.add()` 把文档、embedding 和 ID 加入 collection。代码里用了 try-except，用于处理数据已经存在的情况。

## 创建 RAG 工具

- **`answer_from_knowledge_base` 函数：**
  这个 Python 函数通过 Agents SDK 的 `@function_tool` 装饰器暴露为 Agent 工具。

  主要流程如下：

  - **输入：**
    接收一个 `query` 字符串。
  - **对查询做 Embedding：**
    使用同一个 Gemini embedding 模型，但设置 `RETRIEVAL_QUERY` 类型，把用户问题转成向量。
  - **搜索 ChromaDB：**
    使用 `collection.query` 在知识库中搜索最相似的文档。这里示例里取 `n_results=1`，即只取最相关的一条。
  - **提取最相关文档：**
    从搜索结果中取出最相关文档的文本内容。
  - **构造 Prompt：**
    把检索到的上下文和用户问题拼成一个 prompt，并要求模型只基于给定上下文回答。
  - **生成回答：**
    使用 `client.models.generate_content` 和 `gemini-1.5-flash` 模型生成回答。
  - **返回答案：**
    返回生成后的文本回答。

## 创建 Agent

- **`qa_agent`：**
  使用 OpenAI Agents SDK 创建了一个 `Agent`。

  配置包括：

  - **名称和指令：**
    说明 Agent 的角色，即利用工具从知识库中查找信息。
  - **工具列表：**
    把 `answer_from_knowledge_base` 放进 `tools`，让 Agent 能调用它。
  - **模型：**
    使用 `OpenAIChatCompletionsModel`，并通过前面设置好的 `external_client` 接到 Gemini，同时指定兼容端点可用的模型名 `gemini-1.5-flash-001`。

## 运行 Agent

- **`main()` 异步函数：**
  - 定义一个测试问题
  - 使用 `Runner.run(qa_agent, agent_question)` 执行 Agent
  - Agents SDK 会决定是否调用 `answer_from_knowledge_base`
  - 最后把 Agent 的输出打印出来

- **`if __name__ == "__main__": asyncio.run(main())`**
  这保证脚本运行时会执行异步 `main()`。

## 往知识库中加入 PDF 数据

- **加载 PDF：**
  - 使用 `!pip install pypdf` 安装处理 PDF 的依赖
  - `load_and_split_pdf(file_path)` 函数使用 `PyPDFLoader` 读取 PDF，并按页拆分
  - `files.upload()` 允许用户从本地上传 PDF 到 Colab
  - 然后拿到文件路径并调用上面的函数

- **处理 PDF 内容：**
  - 从每一页提取文本
  - 为每一页生成唯一 ID
  - 使用同样的 Gemini embedding 模型和 `RETRIEVAL_DOCUMENT` 类型，为每页内容生成 embedding

- **把 PDF 数据加入 ChromaDB：**
  - 再次使用 `chroma_client.get_or_create_collection(name="knowledge_base1")` 获取原 collection
  - 把 PDF 文档、embedding 和 ID 加入同一个 collection
  - 这样一来，最初示例文档和 PDF 内容就合并到同一个知识库里了
  - 同样通过 try-except 避免重复插入问题

- **使用 PDF 内容回答问题：**
  - 由于 PDF 内容已经加入知识库，现有的 RAG 工具 `answer_from_knowledge_base` 和 Agent `qa_agent` 就能回答来自 PDF 的问题
  - **`main_pdf_question()` 异步函数：**
    - 定义一个和 PDF 内容相关的测试问题
    - 再次运行 Agent
    - 打印执行结果和最终答案
