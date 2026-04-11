# 智能体流式输出

本 README 演示了如何使用 Python 的异步能力以及假设中的 `agents` 库，实现并理解智能体的流式输出。

## 示例 1：带工具调用的流式智能体

这个示例展示了一个智能体如何利用异步工具动态完成任务。

- **Agent**：定义了特定的指令和工具。
- **Tool**：`how_many_jokes`，返回一个随机整数，用来决定要讲几个笑话。
- **Runner**：异步执行智能体动作，并流式输出事件。

### 用法
```python
import asyncio
import random
from agents import Runner, ItemHelpers

async def main():
    agent = Agent(
        instructions="You are a helpful assistant. First, determine how many jokes to tell, then provide jokes.",
        tools=[how_many_jokes],
    )

    result = Runner.run_streamed(agent, input="Hello")

    async for event in result.stream_events():
        if event.item.type == "tool_call_output_item":
            print(f"Tool output: {event.item.output}")
        elif event.item.type == "message_output_item":
            print(ItemHelpers.text_message_output(event.item))

asyncio.run(main())
```

### 预期输出示例
```
=== Run starting ===
-- Tool output: 4
-- Message output:
 Sure, here are four jokes for you:

1. **Why don't skeletons fight each other?**
   They don't have the guts!

2. **What do you call fake spaghetti?**
   An impasta!

3. **Why did the scarecrow win an award?**
   Because he was outstanding in his field!

4. **Why can't you give Elsa a balloon?**
   Because she will let it go!

```

- **`tool_call_output_item`**：表示工具返回的数据。
- **`message_output_item`**：表示智能体生成的消息内容。

## 示例 2：处理原始响应事件

```python
from agents import Agent, Runner
import asyncio

async def main():
    agent = Agent(
        name="Joker",
        instructions="You are a helpful assistant.",
    )

    result = Runner.run_streamed(agent, input="Please tell me 5 jokes.")

    async for event in result.stream_events():
        if event.item.type == "message_output_item":
            print(ItemHelpers.text_message_output(event.item))

asyncio.run(main())
```

## 事件类型

### event.type

1. `raw_response_event`
作用：这是 LLM 原始流式事件，直接从模型底层透传上来。
常见用途：拿增量文本、token 级输出、原始 response delta。
你代码里把它 continue 掉，等于“不关心底层细粒度输出”。
2. `agent_updated_stream_event`
作用：表示 当前正在运行的 agent 变了。
常见场景：发生 handoff，或者流程切换到了另一个 agent。
你这里打印 event.new_agent.name，就是在看“现在轮到哪个 agent 了”。
3. `run_item_stream_event`
作用：这是 SDK 已经整理好的高层事件。
它会把消息输出、工具调用、工具结果、handoff 等包装成统一的 RunItem 给你。
你现在主要处理的就是这一类。

### event.item.type

- tool_call_item
作用：工具被调用了
- tool_call_output_item
作用：工具返回结果了
- message_output_item
作用：模型产出可展示消息了

另外，run_item_stream_event 本身还有一个 event.name 字段。在当前版本里可选值有 8 个：

- message_output_created
- handoff_requested
- handoff_occured
- tool_called
- tool_output
- reasoning_item_created
- mcp_approval_requested
- mcp_list_tools

所以可以这样理解：

- event.type：大类，只有 3 种
- event.name：run_item_stream_event 里的更细事件名，有 8 种
- event.item.type：具体 item 类型，你代码里目前只处理了其中 3 种
常见场景：发生 handoff，或者流程切换到了另一个 agent。
你这里打印 event.new_agent.name，就是在看“现在轮到哪个 agent 了”。
3. run_item_stream_event
作用：这是 SDK 已经整理好的高层事件。
它会把消息输出、工具调用、工具结果、handoff 等包装成统一的 RunItem 给你。
你现在主要处理的就是这一类。

你这段代码里真正分支最多的，其实不是 event.type，而是 run_item_stream_event 里面的 event.item.type。
你现在用到的有：

- tool_call_item
作用：工具被调用了
- tool_call_output_item
作用：工具返回结果了
- message_output_item
作用：模型产出可展示消息了

另外，run_item_stream_event 本身还有一个 event.name 字段。在你当前版本里可选值有 8 个：

- message_output_created
- handoff_requested
- handoff_occured
- tool_called
- tool_output
- reasoning_item_created
- mcp_approval_requested
- mcp_list_tools

## 核心概念

- **Streaming Output**：来自异步智能体执行过程中的实时响应。
- **Event Handling**：对流式事件进行筛选和处理，以提取特定输出。
- **Agent Tools**：智能体在执行任务时调用的模块化函数。

## 最佳实践
- 清晰地区分不同事件类型的处理逻辑。
- 确保正确使用异步方法（`async` / `await`）。
- 忽略无关的事件类型（例如原始增量事件），从而提供更友好的用户输出。

这份指南可以帮助开发者在各种应用场景中，更高效地实现和理解异步、流式 AI 智能体。

# OpenAI Agents SDK流式机制

OpenAI Agents SDK 的流式机制，核心上是：

1. **运行入口**：你不是用 `Runner.run()`，而是用 `Runner.run_streamed()` 启动一次 agent run。
2. **事件通道**：拿到的是一个 `RunResultStreaming`，然后通过 `result.stream_events()` 持续读取事件。
3. **两层事件**：
   - **底层原始事件**：直接来自 Responses API，粒度很细，适合“逐 token 输出”。
   - **高层语义事件**：由 Agents SDK 整理出来，粒度更粗，适合“消息生成了 / 工具调用了 / 工具产出了 / 发生 handoff 了”这类业务进度。 ([OpenAI](https://openai.github.io/openai-agents-python/running_agents/))

------

## 一、整体心智模型

把一次 agent 运行想成一条流水线：

```text
用户输入
  ↓
Runner.run_streamed(...)
  ↓
模型开始生成
  ↓
不断吐出流式事件
  ↓
可能触发工具 / handoff / MCP / approval
  ↓
事件流结束
  ↓
RunResultStreaming 内保留完整运行结果
```

官方文档明确说，`Runner.run_streamed()` 会返回 `RunResultStreaming`；你通过 `.stream_events()` 异步读取事件。并且**一次流式 run 只有在迭代器真正结束时才算完整结束**，因为最后一个可见 token 出来后，还可能有会话持久化、审批记录、历史压缩之类的收尾工作。`result.is_complete` 会在流结束后反映最终状态。 ([OpenAI](https://openai.github.io/openai-agents-python/running_agents/?utm_source=chatgpt.com))

这个点非常重要，因为很多初学者会误以为：

> “最后一个文本 token 出来了，run 就结束了。”

实际上不一定。**“用户看见最后一个字”** 和 **“这次 agent run 在系统内部彻底完成”** 不是同一时刻。官方文档专门强调要把 `stream_events()` 消费到结束。 ([OpenAI](https://openai.github.io/openai-agents-python/streaming/))

------

## 二、事件“流”

Agents SDK 的“流”，并不只是流文本。

它可能流出以下几类变化：

- 模型开始创建响应
- 文本增量输出
- 工具调用开始
- 工具调用结果返回
- reasoning 条目产生
- handoff 请求与切换
- MCP 工具列表 / 审批请求 / 审批响应
- 最终完成或中断

所以要把它理解为：

> **不是单纯的 token streaming，而是“整个 agent 执行过程的事件流”。**

官方文档把这分成两层：

### 1) Raw response events（原始响应事件）

这是直接从底层 LLM / Responses API 传出来的事件。它们是 **Responses API 的事件格式**，每个事件都有 `type` 和 `data`，例如：

- `response.created`
- `response.output_text.delta`
- `response.completed`

如果你要做“打字机效果”、逐 token 往前端推内容，这层最合适。 ([OpenAI](https://openai.github.io/openai-agents-python/streaming/))

### 2) Run item events（运行项事件）

当外层事件是 `run_item_stream_event` 时，这个被包装的运行项本身是什么类型，比如：

- 一条消息完整生成了
- 一次工具调用发生了
- 工具输出生成了
- handoff 发生了

这层更适合做业务 UI，比如状态栏、步骤条、审计日志。 ([OpenAI](https://openai.github.io/openai-agents-python/streaming/))

------

## 三、为什么会有“两层事件”

这是理解 Agents SDK 的关键。

### 底层事件解决的是“快”

你想要：

- 用户一边看一边出字
- 尽快看到模型正在说什么
- 细粒度捕获生成过程

就应该读 **raw events**。

典型场景：

- 聊天 UI
- CLI 实时打印
- 打字机效果
- 边生成边做内容审核

### 高层事件解决的是“稳”

你想要：

- 展示 agent 当前处于哪个阶段
- 告诉用户“正在调用工具”
- 做任务编排、审计和观测
- 不关心每个 token，只关心“一个步骤完成了”

就应该读 **run item events**。

典型场景：

- “正在搜索资料…”
- “已调用天气工具”
- “已获得搜索结果”
- “已切换到财务 agent”

所以经验上：

- **做聊天文本显示**：看 raw events
- **做 agent 执行进度 / 调试面板**：看 run item events
- **生产系统**：通常两层一起用

------

## 四、基本代码模式

### 1) 逐 token 输出文本

官方给出的模式是：调用 `Runner.run_streamed()`，然后在 `stream_events()` 里筛选 `raw_response_event`，再判断是不是 `ResponseTextDeltaEvent`，把 `delta` 打印出来。 ([OpenAI](https://openai.github.io/openai-agents-python/streaming/))

Python 示例：

```python
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner

async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant."
    )

    result = Runner.run_streamed(
        agent,
        input="请用中文解释什么是流式输出。"
    )

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

    print("\n---")
    print("is_complete:", result.is_complete)

asyncio.run(main())
```

这段代码里最值得学的不是语法，而是模式：

- `run_streamed()` 启动流式 run
- `stream_events()` 是唯一事件入口
- 只处理你关心的事件
- **必须把整个流读完**
- 流结束后再看最终状态

------

### 2) 做高层“步骤进度”输出

如果你不想要 token 级别，而想做“步骤级反馈”，就看 `run_item_stream_event`。

```python
import asyncio
from agents import Agent, Runner

async def main():
    agent = Agent(
        name="Assistant",
        instructions="你是一个会解释技术概念的助手。"
    )

    result = Runner.run_streamed(
        agent,
        input="先思考，再回答：解释 agent 流式事件。"
    )

    async for event in result.stream_events():
        if event.type == "run_item_stream_event":
            print(f"[{event.name}] {type(event.item).__name__}")

asyncio.run(main())
```

这个适合：

- 调试 agent orchestration
- 打印工具调用时间线
- 做“任务执行轨迹”面板

------

## 五、事件类型

### A. 顶层 `StreamEvent` 的主要类别

从官方文档可以概括出，至少有这几类你最常见：

#### 1. `raw_response_event`

表示底层 Responses API 的原始流事件。事件对象里带 `data`，其内部 `type` 可能是 `response.created`、`response.output_text.delta` 等。 ([OpenAI](https://openai.github.io/openai-agents-python/ref/stream_events/))

#### 2. `run_item_stream_event`

表示 SDK 已经识别出一个高层运行项。比如消息完成、工具调用、工具输出、handoff 等。 ([OpenAI](https://openai.github.io/openai-agents-python/ref/stream_events/))

#### 3. `agent_updated_stream_event`

表示当前活跃 agent 发生变化，常见于 handoff。文档说明它在当前 agent 改变时发出更新。 ([OpenAI](https://openai.github.io/openai-agents-python/streaming/))

------

### B. `raw_response_event` 里常见的底层事件

官方在 Responses 流式文档中列出，做文本流最常见的是：

- `response.created`
- `response.output_text.delta`
- `response.completed`
- `error` ([OpenAI开发者门户](https://developers.openai.com/api/docs/guides/streaming-responses))

可以把它们理解为：

#### `response.created`

响应对象刚建立。
相当于“这次生成开始了”。

#### `response.output_text.delta`

文本增量。
相当于“又吐出一小段文本”。

#### `response.completed`

响应完成。
相当于“底层响应结束了”。

#### `error`

流过程中发生错误。

------

### C. `run_item_stream_event.name` 的固定语义事件名

Agents SDK 文档给出了固定集合：

- `message_output_created`
- `handoff_requested`
- `handoff_occured`
- `tool_called`
- `tool_search_called`
- `tool_search_output_created`
- `tool_output`
- `reasoning_item_created`
- `mcp_approval_requested`
- `mcp_approval_response`
- `mcp_list_tools` ([OpenAI](https://openai.github.io/openai-agents-python/streaming/))

下面逐个解释。

------

## 六、高层事件名

### 1) `message_output_created`

表示一条消息输出已经形成。
注意，它不是“每个 token 来一次”，而是“**一条消息 item 生成了**”。

适合做什么

- 在消息列表里插入一条 assistant message
- 在步骤日志里记“已生成回复消息”
- 做审计记录

和 `response.output_text.delta` 的区别

- `response.output_text.delta`：字一个个来
- `message_output_created`：这条消息作为一个 item 成型了

可以类比成：

- `delta` = 键盘敲字过程
- `message_output_created` = 一条消息发送出去

------

### 2) `handoff_requested`

表示模型提出要把工作交给另一个 agent。
也就是 handoff 的“请求阶段”。

典型场景

你定义了多个 agent，比如：

- 总控 agent
- 财务 agent
- 搜索 agent
- 代码 agent

总控 agent 判断某个任务该交给搜索 agent，于是先出现 `handoff_requested`。

------

### 3) `handoff_occured`

表示 handoff 已经实际发生。
官方文档特别说明：**`occured` 这个拼写是故意保留的历史拼写错误，为了兼容性不能改。** ([OpenAI](https://openai.github.io/openai-agents-python/streaming/))

这是一个很容易面试式提问的点，也很容易在代码里踩坑：

```python
if event.name == "handoff_occured":
    ...
```

不能写成 `handoff_occurred`。

理解为两个阶段

- `handoff_requested`：我想切换
- `handoff_occured`：已经切换成功

------

### 4) `tool_called`

表示模型调用了一个工具。
这通常意味着 agent 已经不只是“说话”，而是在“行动”。

可能对应哪些工具

- function calling 工具
- OpenAI hosted tools
- 本地运行时工具
- computer 工具
- 甚至嵌套 agent 作为工具

文档还提到：对 computer tool 的原始流事件，不管是 preview 的单 `action` 还是 GA / `gpt-5.4` 的批量 `actions[]`，在更高层 `RunItemStreamEvent` 里都统一表现为 `tool_called`。 ([OpenAI](https://openai.github.io/openai-agents-python/streaming/))

这说明一个设计原则：

> **高层事件追求语义统一，不暴露太多底层差异。**

------

### 5) `tool_search_called`

这是 hosted tool search 相关事件。
当模型发出“工具搜索请求”时，会有这个事件。 ([OpenAI](https://openai.github.io/openai-agents-python/streaming/))

它不是一般意义上“任意工具调用”的同义词，而是更特化地对应“tool search”。

------

### 6) `tool_search_output_created`

表示 hosted tool search 的结果已经返回了“加载后的子集”。官方文档明确说明了这一点。 ([OpenAI](https://openai.github.io/openai-agents-python/streaming/))

所以这两个通常成对看：

- `tool_search_called`
- `tool_search_output_created`

------

### 7) `tool_output`

表示工具产出已经生成。
这往往出现在 `tool_called` 之后。

实际开发里常见模式

你会把它映射成 UI 状态：

- `tool_called` → “正在查询数据库…”
- `tool_output` → “数据库结果已返回”

这比看原始 token 更贴近业务。

------

### 8) `reasoning_item_created`

表示产生了 reasoning item。
这不是“最终给用户看的正文”，而是 agent 执行过程中的 reasoning 相关运行项。 ([OpenAI](https://openai.github.io/openai-agents-python/streaming/))

对学习者来说，理解到这个程度就够了：

- 它是一个**高层执行痕迹**
- 不等于普通消息文本
- 可用于观察 agent 的思考流程结构

------

### 9) `mcp_approval_requested`

表示 MCP 工具调用需要审批。
这通常和 human-in-the-loop 配合。

------

### 10) `mcp_approval_response`

表示对审批请求给出了响应。
比如批准或拒绝。

------

### 11) `mcp_list_tools`

表示与 MCP 工具列表加载相关的事件。
本质上是 agent 在和 MCP 工具体系交互时的高层执行信号。

------

## 七、Agent 切换、Agent 作为工具、普通工具调用

这是学习者最容易混淆的地方。

### 1) Handoff

A agent 把会话主导权交给 B agent。
新 agent 接过上下文继续工作。
对应关注：

- `handoff_requested`
- `handoff_occured`
- `agent_updated_stream_event`

### 2) Agent as tool

A agent 把 B agent 当成一个“工具”来调用。
B agent 完成局部子任务后，控制权回到 A。
文档明确说：这和 handoff 不同，因为 handoff 是接管对话，而 `Agent.as_tool()` 是“被当作工具调用，原 agent 继续对话”。 ([OpenAI](https://openai.github.io/openai-agents-python/ref/agent/))

并且文档有一个 `AgentToolStreamEvent`：表示当 agent 被当工具调用时，会发出来自嵌套 agent run 的流式事件。它包含：

- `event`：嵌套 agent 的流事件
- `agent`：嵌套 agent
- `tool_call`：对应的原始工具调用信息（如果有） ([OpenAI](https://openai.github.io/openai-agents-python/ref/agent/))

这说明：

> 当 agent 被作为工具嵌套调用时，流式事件是可以“透传嵌套层”的。

### 3) 普通工具调用

模型调用的是你注册的函数、hosted tools、computer tool 等。
关注：

- `tool_called`
- `tool_output`

------

## 八、审批中断与流式的关系

官方文档明确说：

- 流式运行和 approval pause 是兼容的
- 如果某个工具需要 approval，那么 `result.stream_events()` 会结束
- 待审批项会出现在 `RunResultStreaming.interruptions`
- 你把结果转成 `RunState`，批准或拒绝后，再次 `Runner.run_streamed(...)` 恢复执行。 ([OpenAI](https://openai.github.io/openai-agents-python/streaming/))

这意味着：

### 一个 run 的“流”不一定一次到头

可能是：

```text
开始流式输出
  ↓
工具请求审批
  ↓
事件流结束（不是失败，是暂停）
  ↓
你处理 approval
  ↓
恢复 run
  ↓
继续新的事件流
```

示意代码：

```python
result = Runner.run_streamed(agent, "Delete temporary files if they are no longer needed.")

async for _event in result.stream_events():
    pass

if result.interruptions:
    state = result.to_state()
    for interruption in result.interruptions:
        state.approve(interruption)

    result = Runner.run_streamed(agent, state)

    async for _event in result.stream_events():
        pass
```

这正是官方文档给出的模式。 ([OpenAI](https://openai.github.io/openai-agents-python/streaming/))

------

## 九、4 层事件理解框架

我建议学习时这样记：

### 第 1 层：生命周期事件

- `response.created`
- `response.completed`
- `error`

作用：知道一次生成开始/结束/失败。 ([OpenAI开发者门户](https://developers.openai.com/api/docs/guides/streaming-responses))

### 第 2 层：文本增量事件

- `response.output_text.delta`

作用：打字机输出。 ([OpenAI](https://openai.github.io/openai-agents-python/streaming/))

### 第 3 层：执行步骤事件

- `message_output_created`
- `tool_called`
- `tool_output`
- `reasoning_item_created`

作用：给用户看“当前执行到了哪一步”。 ([OpenAI](https://openai.github.io/openai-agents-python/streaming/))

### 第 4 层：编排控制事件

- `handoff_requested`
- `handoff_occured`
- `agent_updated_stream_event`
- `mcp_approval_requested`
- `mcp_approval_response`

作用：处理多 agent、审批、MCP 集成。 ([OpenAI](https://openai.github.io/openai-agents-python/streaming/))

------

## 十、实践中应该监听哪一层

### 场景 1：做聊天界面

你最少要监听：

- `raw_response_event` 中的 `response.output_text.delta`
- `response.completed`
- `error`

用途：

- 打字机效果
- 结束态切换
- 错误提示

------

### 场景 2：做 agent 调试控制台

你最少要监听：

- `run_item_stream_event`
- `agent_updated_stream_event`

用途：

- 看工具调用顺序
- 看 handoff
- 看 reasoning item
- 看 MCP 审批

------

### 场景 3：做生产系统的前端

通常是“双轨制”：

**给用户看的主界面**

- 用 raw text delta 实时渲染正文

**给开发者/高级用户看的侧边栏**

- 用 run item events 渲染执行轨迹

这样用户体验和可观测性都兼顾。

------

## 十一、生产代码骨架

```python
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner

async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant."
    )

    result = Runner.run_streamed(agent, input="帮我规划一份学习 Agents SDK 的路线。")

    collected_text = []

    async for event in result.stream_events():
        # 1) 底层文本流
        if event.type == "raw_response_event":
            if isinstance(event.data, ResponseTextDeltaEvent):
                delta = event.data.delta
                collected_text.append(delta)
                print(delta, end="", flush=True)

        # 2) 高层步骤流
        elif event.type == "run_item_stream_event":
            print(f"\n[STEP] {event.name}")

        # 3) agent 更新
        elif event.type == "agent_updated_stream_event":
            print("\n[AGENT UPDATED]")

    print("\n\n=== FINAL ===")
    print("complete:", result.is_complete)
    print("text:", "".join(collected_text))

asyncio.run(main())
```

这个骨架体现了三个原则：

- **文本流和步骤流分开处理**
- **不要只依赖 token 事件**
- **最后一定检查完整状态**

------

## 十二、初学者最容易踩的坑

### 坑 1：只读到最后一个字就停止

不对。
官方明确说，流式 run 要等 async iterator 结束才完整完成，因为还有收尾处理。 ([OpenAI](https://openai.github.io/openai-agents-python/streaming/))

### 坑 2：把 raw event 和 run item event 混为一谈

不对。
raw event 是底层协议流；run item event 是 SDK 聚合后的语义层。用途不同。 ([OpenAI](https://openai.github.io/openai-agents-python/streaming/))

### 坑 3：用高层事件做打字机效果

通常不合适。
高层事件是“item 完整产生后”才发，不能替代 token 增量。 ([OpenAI](https://openai.github.io/openai-agents-python/streaming/))

### 坑 4：写错 `handoff_occured`

要注意官方保留了历史拼写：`occured`。 ([OpenAI](https://openai.github.io/openai-agents-python/streaming/))

### 坑 5：审批中断被当成异常

不一定是异常。
当工具需要 approval 时，流会先结束，等待你从 `interruptions` 恢复。 ([OpenAI](https://openai.github.io/openai-agents-python/streaming/))

### 坑 6：Responses WebSocket ≠ Realtime API 

官方明确区分：Agents SDK 文档这里提到的是 **Responses API over WebSocket transport**，**不是 Realtime API**。 ([OpenAI](https://openai.github.io/openai-agents-python/running_agents/))

------

## 十三、总结

最准确的学习者版本可以记成：

> **OpenAI Agents SDK 的流式机制，不只是把文本一个字一个字吐出来，而是把“整个 agent 运行过程”事件化。底层是 Responses API 的原始流事件，适合 token 级输出；上层是 Agents SDK 的语义事件，适合消息、工具、handoff、审批等执行状态管理。** ([OpenAI](https://openai.github.io/openai-agents-python/streaming/))

| 层级     | 事件                         | 含义                | 常见用途         |
| -------- | ---------------------------- | ------------------- | ---------------- |
| 原始层   | `response.created`           | 响应开始            | 初始化 UI        |
| 原始层   | `response.output_text.delta` | 文本增量            | 打字机输出       |
| 原始层   | `response.completed`         | 响应完成            | 收尾、解锁输入框 |
| 原始层   | `error`                      | 错误                | 错误提示         |
| SDK 高层 | `message_output_created`     | 一条消息已形成      | 消息日志         |
| SDK 高层 | `tool_called`                | 调用了工具          | 进度提示         |
| SDK 高层 | `tool_output`                | 工具结果已出        | 展示工具结果     |
| SDK 高层 | `handoff_requested`          | 请求切换 agent      | 编排追踪         |
| SDK 高层 | `handoff_occured`            | 已切换 agent        | 编排追踪         |
| SDK 高层 | `reasoning_item_created`     | reasoning item 产生 | 调试/观测        |
| SDK 高层 | `mcp_approval_requested`     | 请求审批            | HITL             |
| SDK 高层 | `mcp_approval_response`      | 审批结果            | HITL             |

