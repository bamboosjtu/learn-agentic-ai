# 本章小结

`OpenAI SDK` 是“调用 OpenAI API 的通用客户端库”，`OpenAI Agents SDK` 是“在这些模型/API 之上做 agent 编排的更高层框架”。

- `openai` 包是 **底层 API client**。你主要用 `OpenAI` / `AsyncOpenAI` 去直接调 Responses、Chat Completions、Files 这类 OpenAI API，可以理解为一个HTTP/API SDK。
- `openai-agents` 包是 **构建 agent 工作流的上层 SDK**。它底下仍然会用到 `openai`，但在上面补了一整层“代理编排能力”，可以理解为一个“agent orchestration framework”。

## 摘要

### **`openai-agents` 对 `openai` 的主要封装**

- `Agent`：把 `instructions`、`model`、`tools`、`handoffs` 这些配置收敛成一个 agent 对象。
- `Runner`：帮你跑完整 agent loop，不只是发一次请求。它会处理模型回复、工具调用、继续推理、交接给别的 agent，并返回 `RunResult` / 流式结果。
- `Tools` 封装：
  - `function_tool` 把 Python 函数直接包装成工具
  - Hosted tools：`WebSearchTool`、`FileSearchTool`、`CodeInterpreterTool`、`ImageGenerationTool`、`HostedMCPTool`
  - Local/runtime tools：`ShellTool`、`LocalShellTool`、`ComputerTool`、`ApplyPatchTool`
  - MCP 集成：本地或托管 MCP server 接入
- `Handoffs` / agents-as-tools：一个 agent 可以把任务转给另一个 agent，或者把另一个 agent当工具调用。
- `Guardrails`：输入、输出、工具级校验与拦截。
- `Sessions / memory`：对话历史保存、SQLite session、Responses compaction session 等。
- `Tracing`：内建 tracing，把 generation、tool call、handoff、guardrail 都串起来。
- `Model provider` 抽象：除了直接走 OpenAI，还能接 LiteLLM、OpenAI-compatible endpoint、多 provider 路由。
- `Realtime / voice`：对 Realtime API、WebSocket 会话、语音管线做了进一步封装。

- 

### **`openai-agents`的其他依赖**

`openai-agents 0.13.6` 的**基础依赖**除了 `openai` 之外还有：

- `griffe[lib]`（元数据里显示为 `griffelib<3,>=2`，用于解析函数/docstring/schema）
- `mcp<2,>=1.19.0`
- `pydantic<3,>=2.12.2`
- `requests<3,>=2.0`
- `types-requests<3,>=2.0`
- `typing-extensions<5,>=4.12.2`

它还有不少**可选依赖 / extras**，按能力分组大致是：

- `litellm`
- `any-llm-sdk`
- `websockets`（`realtime` / `voice`）
- `numpy`（`voice`）
- `redis`
- `sqlalchemy`
- `asyncpg`
- `graphviz`
- `cryptography`
- `dapr`
- `grpcio`

## `OpenAI SDK`

- 典型包名是 Python 的 `openai` 或 Node 的 `openai`
- 主要职责是直接调接口，比如 `responses.create()`、`files.create()`、`chat.completions.create()`
- 更接近“API client”
- 你自己负责对话状态、工具循环、路由、多 agent 协作、守护逻辑等
  - 你只需要单次调用模型
  - 你想完全自己控制请求、状态和流程
  - 你的应用更像“API 集成”而不是“agent 系统”

```python
from openai import OpenAI
client = OpenAI()

resp = client.responses.create(
    model="gpt-5",
    input="总结这段内容"
)
```



## `OpenAI Agents SDK`

- 典型包名是 Python 的 `openai-agents`
- 主要职责是构建 agent 系统
- 提供更高层原语：`Agent`、`Runner`、`handoffs`、`guardrails`、`sessions`、`tracing`
- 内置 agent loop，会处理“模型调用 -> 工具调用 -> 把结果再喂回模型 -> 直到完成”这类流程
- 更接近“agent runtime / orchestration framework”

**联系**

- Agents SDK 不是替代 OpenAI API，而是建立在模型/API能力之上的编排层。
- 官方文档里，Responses API 被定义为构建 agentic workflow 的核心接口；Agents SDK 则提供 agent、handoff、guardrails、sessions、tracing 等更高层能力。
- Agents SDK 运行时仍然要调用底层模型接口；只是这些调用被框架封装了，你通常不再手写完整的 tool loop。
  - 你要做工具调用、多轮状态、handoff、多 agent 协作
  - 你不想手写 tool loop 和 orchestration
  - 你需要 tracing、sessions、guardrails 这类 agent 基础设施

```python
from agents import Agent, Runner

agent = Agent(
    name="Tutor",
    instructions="你是一个老师",
)

result = Runner.run_sync(agent, "解释牛顿第一定律")
print(result.final_output)
```

### 核心概念

不太像“新模型框架”，更像：

- 一个 **Agent Runtime**
- 一个 **基于 Responses API 的 orchestration layer**
- 一个 **OpenAI 官方版的轻量 agent framework**
- 

#### 1. `Agent`

`Agent` 是最核心的定义单元。官方定义里，一个 agent 本质上是：

- 一个 LLM
- 一组 `instructions`
- 一组 `tools`
- 可选的：
  - `handoffs`
  - `guardrails`
  - `structured outputs`
  - 运行时行为配置

也就是说，`Agent` 更像“**能力声明**”或“角色定义”，不是执行器本身。  

#### 2. `Runner`
`Runner` 是执行器，负责把一个 agent 真正跑起来。

它负责的事情包括：

- 调模型
- 处理多轮 agent loop
- 执行 tool calls
- 处理 handoff
- 执行 guardrails
- 管理 session / conversation state
- 支持 tracing 和 streaming

官方文档明确说，runner 的 loop 大致是：

1. 调用 agent
2. 如果得到 final output，就结束
3. 如果发生 handoff，就切换到新 agent
4. 否则执行 tool calls，再继续下一轮

#### 3. `Tools`

Tools 是 agent 能调用的外部能力，比如：

- Python 函数
- Web search
- File search
- Computer use
- 你自己封装的业务 API

这部分本质上是对底层 tool-calling 的封装，但 SDK 帮你统一了注册、调用和结果回传流程。

#### 4. `Handoffs`
Handoff 是多 agent 协作的机制。

它不是让一个 agent “手动描述另一个 agent 应该干什么”，而是让当前 agent 能正式把控制权交给另一个 agent。  
这适合：

- 路由型系统
- manager / specialist 架构
- 分角色 agent 协作

#### 5. `Guardrails`
Guardrails 是输入/输出校验层，用来限制 agent 行为。

比如：

- 输入是否合规
- 输出是否满足格式
- 是否触发敏感内容拦截
- 是否中止运行

#### 6. `RunResult`
执行完以后会返回 `RunResult`，里面一般包含：

- `final_output`
- run items / 中间事件
- tracing 相关信息
- 可恢复状态

#### 7. `Session / conversation state`

SDK 支持自动管理历史对话状态，而不是每次都让你手动拼消息列表。  
对于 OpenAI 模型，它还能利用 `previous_response_id` 来减少重复传历史。  
来源：  

可以把它理解成一套“**定义角色 + 执行循环 + 控制边界**”的结构。

### 关系图

```text
User Input
   |
   v
+------------------+
|      Runner      |
|  负责执行整个流程  |
+------------------+
   |
   v
+------------------+
|      Agent       |
| 角色/指令/模型/工具 |
+------------------+
   |        |         |
   |        |         |
   |        |         +----------------------+
   |        |                                |
   |        v                                v
   |   +-----------+                  +---------------+
   |   |   Tool    |                  |   Handoff     |
   |   | 外部能力   |                  | 切换到别的Agent |
   |   +-----------+                  +---------------+
   |                                           |
   |                                           v
   |                                    +---------------+
   |                                    |   Next Agent  |
   |                                    +---------------+
   |
   v
+------------------+
|    Guardrail     |
| 输入/输出校验/限制 |
+------------------+
   |
   v
Final Output
```

### 运行时真实流程

更接近实际执行的是这样：

```text
1. Runner 接收输入
2. Guardrail 先检查输入
3. Runner 调用 Agent
4. Agent 决定：
   - 直接回答
   - 调 Tool
   - Handoff 给别的 Agent
5. 如果调 Tool：
   - Runner 执行 Tool
   - 把结果回传给 Agent
   - 继续循环
6. 如果 Handoff：
   - Runner 切换当前 Agent
   - 继续循环
7. Guardrail 检查最终输出
8. Runner 返回结果
```

### 设计思路

官方自己强调了两个设计方向：

#### 1. “primitives 很少”
它刻意只保留少数几个原语：

- `Agents`
- `Handoffs`
- `Guardrails`

也就是说，它不想做一个很重的工作流平台，而是想给你**最小但够用的 agent runtime 组件**。  


#### 2. “薄封装，不隐藏底层逻辑”
它不是 LangChain 那种大而全抽象层，反而更接近：

- 你仍然理解 tool calling 在做什么
- 你仍然知道 agent loop 是怎么跑的
- 只是不用每次自己写那套 while-loop、tool dispatch、handoff routing、tracing plumbing

换句话说，它封装的是**重复的样板运行时**，不是试图重新定义 LLM 应用编程模型。

如果你直接用 `Responses API` 自己做 agent，通常要自己处理：

- prompt / instructions 组织
- tool schema 注册
- function/tool call dispatch
- 把 tool result 回传模型
- 多轮 loop
- 切换 agent
- conversation state
- tracing / debug
- streaming 事件处理

Agents SDK 把这些收敛成：

```python
agent = Agent(...)
result = Runner.run_sync(agent, "...")
```

所以它本质上是：

**对 Responses API 的“agent loop、tool loop、handoff loop、state loop”做统一封装。**



## **官方依据**

- OpenAI Python SDK README：主入口是 `Responses API`  
  https://github.com/openai/openai-python
- Responses API 官方文档：用于 stateful、tool-using 的 agentic workflows  
  https://platform.openai.com/docs/api-reference/responses
- Agents SDK 官方文档：强调 `Agents`、`Handoffs`、`Guardrails`、`Sessions`、`Tracing`  
  https://openai.github.io/openai-agents-python/
- Agents SDK Quickstart  
  https://openai.github.io/openai-agents-python/quickstart/

OpenAI Agents SDK 的核心思路可以概括成一句话：

**它不是在发明新的模型能力，而是在 `Responses API + tools + orchestration` 之上，提供一层很薄但实用的“Agent 运行时”。**