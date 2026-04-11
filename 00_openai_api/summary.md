# 本章小结

当成 **Python 面向对象建模思路** 来理解

- **ChatCompletion** 适合你理解成：
  `一次请求 -> 若干候选答案对象`
- **Response** 更适合你理解成：
  `一次请求 -> 若干执行产物对象`

OpenAI 官方现在仍提供 Chat Completions，但也明确建议**新项目优先考虑 Responses API**。Chat Completions 的返回核心是 `choices`；Responses 的返回核心是 `output`。([OpenAI平台](https://platform.openai.com/docs/api-reference/chat?.docx=&_clear=true&utm_source=chatgpt.com))

------

## 1. ChatCompletion

你可以先脑补成这样：

```python
from dataclasses import dataclass, field
from typing import List, Optional, Literal

FinishReason = Literal["stop", "length", "tool_calls", "content_filter", "function_call"]

@dataclass
class ChatMessage:
    role: Literal["system", "user", "assistant", "tool"]
    content: Optional[str] = None
    # 省略 tool_calls / function_call / audio 等扩展字段


@dataclass
class ChatChoice:
    index: int
    message: ChatMessage
    finish_reason: Optional[FinishReason] = None
    # 还可能有 logprobs


@dataclass
class Usage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class ChatCompletion:
    id: str
    model: str
    created: int
    choices: List[ChatChoice] = field(default_factory=list)
    usage: Optional[Usage] = None
```

这个模型非常重要，因为它直接体现了 **ChatCompletion 的设计哲学**：

> **顶层对象表示“一次生成”**
> **choice 表示“这次生成返回的一个候选结果”**

官方文档里，Chat Completion object 的核心字段就是 `choices[]`，每个 choice 带 `message`、`index`、`finish_reason` 等字段；`finish_reason` 的官方枚举包括 `stop`、`length`、`tool_calls`、`content_filter`，以及已弃用的 `function_call`。([OpenAI平台](https://platform.openai.com/docs/api-reference/chat/object?lang=python）也报错&utm_source=chatgpt.com))

------

### 1.1 为什么 `message` 要放在 `choice` 里面

你用 Python 类看就很直观了。

如果这样设计：

```python
@dataclass
class BadChatCompletion:
    message: ChatMessage
    usage: Usage
```

那它表达的是：

> “一次请求只会产生一个唯一答案”

但 ChatCompletion 不是这么想的。它的真实抽象更像：

```python
@dataclass
class ChatCompletion:
    choices: list[ChatChoice]
```

因为模型本质上是从概率分布里生成文本的，API 要保留“**一个请求可以返回多个候选**”的能力。OpenAI 的 Chat Completions 接口也保留了 `n` 参数，用来生成多个 completion choices。([OpenAI平台](https://platform.openai.com/docs/api-reference/chat?.docx=&_clear=true&utm_source=chatgpt.com))

所以从类设计角度：

- `ChatCompletion` 是**容器**
- `ChatChoice` 是**候选结果对象**
- `ChatMessage` 是**候选里的实际内容**

也就是：

```python
completion.choices[0].message.content
```

而不是：

```python
completion.message.content
```

------

### 1.2 ChatCompletion 更像“文本生成器”的对象模型

如果你把它翻成一句 Python 设计语言，就是：

> `ChatCompletion` 像一个 **ResultSet**
> `ChatChoice` 像一个 **Candidate**
> `ChatMessage` 像一个 **Payload**

所以它最自然的使用方式是：

```python
best = completion.choices[0]
print(best.message.content)
print(best.finish_reason)
```

这说明 ChatCompletion API 的中心思想是：

> **模型首先是在生成“候选回答”**，不是在执行复杂任务流程。

------

## 2. stream ChatCompletion

stream 时，类关系会变成这样：

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class DeltaMessage:
    role: Optional[str] = None
    content: Optional[str] = None
    # 还可能有 tool_calls 的增量字段


@dataclass
class ChatChoiceDelta:
    index: int
    delta: DeltaMessage
    finish_reason: Optional[str] = None


@dataclass
class ChatCompletionChunk:
    id: str
    model: str
    created: int
    choices: list[ChatChoiceDelta]
```

这里设计重点不是 `message`，而是 `delta`。

因为 stream 不是“最终对象”，而是“**最终对象的增量更新**”。

所以你在代码里通常会这么写：

```python
parts = []

for chunk in stream:
    choice = chunk.choices[0]
    if choice.delta.content:
        parts.append(choice.delta.content)

text = "".join(parts)
```

这说明 ChatCompletion stream 的类设计思想是：

> **把最终的 `ChatMessage` 拆成一系列 delta patch**

也就是它更像：

```python
message = reduce(apply_delta, chunks)
```

而不是：

```python
message = chunk.message
```

------

## 3. Response

如果用 Python 重新建模，应该这样想：

```python
from dataclasses import dataclass, field
from typing import List, Optional, Union, Literal, Any

@dataclass
class ResponseUsage:
    input_tokens: int
    output_tokens: int
    total_tokens: Optional[int] = None


@dataclass
class OutputText:
    type: Literal["output_text"]
    text: str


@dataclass
class AssistantMessage:
    type: Literal["message"]
    role: Literal["assistant"]
    content: List[OutputText]


@dataclass
class FunctionToolCall:
    type: Literal["function_call"]
    name: str
    arguments: str
    call_id: str


@dataclass
class ReasoningItem:
    type: Literal["reasoning"]
    summary: Optional[str] = None


ResponseItem = Union[AssistantMessage, FunctionToolCall, ReasoningItem]


@dataclass
class Response:
    id: str
    model: str
    created_at: int
    status: str
    output: List[ResponseItem] = field(default_factory=list)
    usage: Optional[ResponseUsage] = None
```

这套类设计的味道和 ChatCompletion 完全不同。

它表达的不是：

> “这里有几个候选答案”

而是：

> “这里有这次执行过程中产生的若干输出项”

OpenAI 官方对 Responses 的描述是：它是更先进、统一的接口，支持文本和图像输入、文本或 JSON 输出、函数调用，以及内建工具如 web search、file search 等；返回对象的核心字段是 `output`，而不是 `choices`。([OpenAI平台](https://platform.openai.com/docs/api-reference/responses/object?_clear=true&referral_type=blog&utm_source=chatgpt.com))

------

### 3.1 为什么 Response 顶层不是 `choices`，而是 `output`

因为如果还是沿用 `choices`，那类设计会很别扭。

比如你想表达：

- 模型先想了一下
- 然后发起工具调用
- 然后输出最终回答

用 `choice.message` 很难优雅表示。

但用 `output: list[ResponseItem]` 就很自然：

```python
response.output == [
    ReasoningItem(...),
    FunctionToolCall(...),
    AssistantMessage(...),
]
```

这说明 Response 的设计哲学已经从：

> **候选答案集合**

变成了：

> **执行产物集合**

这是给 agent 用的关键变化。

------

### 3.2 用 Python 继承体系理解 Response

如果你是 Python 程序员，可以把它理解成一个基类加若干子类：

```python
class ResponseItem:
    pass


@dataclass
class MessageItem(ResponseItem):
    role: str
    content: list


@dataclass
class ToolCallItem(ResponseItem):
    name: str
    arguments: str
    call_id: str


@dataclass
class ReasoningItem(ResponseItem):
    summary: str | None = None
```

然后：

```python
@dataclass
class Response:
    output: list[ResponseItem]
```

这其实是很典型的 **AST / Event / Command 对象建模**：

- `MessageItem` = 输出给用户看的内容
- `ToolCallItem` = 要求外部系统执行的动作
- `ReasoningItem` = 中间推理产物

所以你遍历时也会很像在处理语法树或事件流：

```python
for item in response.output:
    if isinstance(item, ToolCallItem):
        run_tool(item)
    elif isinstance(item, MessageItem):
        render_message(item)
```

这就是为什么说 Response 比 ChatCompletion 更适合 agent。

------

## 4. 总结

一旦开始写 agent runtime，代码结构会立刻分叉。

### 4.1 ChatCompletion

更像这样：

```python
class ChatCompletion:
    choices: list[ChatChoice]
```

它的中心对象是 **Candidate**。

你的代码通常会长这样：

```python
resp = client.chat.completions.create(...)

msg = resp.choices[0].message

if hasattr(msg, "tool_calls") and msg.tool_calls:
    # 处理工具调用
    ...
else:
    print(msg.content)
```

也就是说：

> 你是从“一个回答对象”里，额外检查它是否藏了工具调用

这是一种“回答优先”的思路。

------

### 4.2 Response

更像这样：

```python
class Response:
    output: list[ResponseItem]
```

它的中心对象是 **Execution Item**。

你的代码更自然会写成：

```python
resp = client.responses.create(...)

for item in resp.output:
    if item.type == "function_call":
        ...
    elif item.type == "message":
        ...
```

也就是：

> 你在处理“多个执行项”

这是一种“流程优先”的思路。

这更像 agent orchestration。

------

### 4.3 stream

Responses 的 streaming 官方是按 **server-sent events** 发一系列 typed events，不再只是 ChatCompletion 那种 `delta.content` 增量。官方文档列出了 `response.created` 等事件，以及一整套 streaming events。([OpenAI平台](https://platform.openai.com/docs/api-reference/responses-streaming/response/output_item?ref=canvas&utm_source=chatgpt.com))

如果你用 Python 建模，更像这样：

```python
class ResponseStreamEvent:
    pass


@dataclass
class ResponseCreated(ResponseStreamEvent):
    response_id: str


@dataclass
class OutputTextDelta(ResponseStreamEvent):
    delta: str
    item_id: str


@dataclass
class OutputItemAdded(ResponseStreamEvent):
    item: ResponseItem


@dataclass
class ResponseCompleted(ResponseStreamEvent):
    response_id: str
```

然后你的主循环是：

```python
for event in stream:
    if isinstance(event, OutputTextDelta):
        print(event.delta, end="")
    elif isinstance(event, OutputItemAdded):
        handle_item(event.item)
    elif isinstance(event, ResponseCompleted):
        break
```

注意这里已经不是“拼 message”了，而是在“处理事件”。

这进一步说明：

- **ChatCompletion stream** 更像 `delta patch`
- **Response stream** 更像 `event bus`

---

## 注意事项

### `o3-mini` vs `gpt-4o`

- `o3-mini`：偏推理模型。
- `gpt-4o`：通用多模态模型（非纯推理定位）。

### `gpt-4o` vs `gpt-4o-search-preview`

- 前者：通用能力更强（含多模态、函数调用等）。
- 后者：面向搜索场景，能力边界更窄（以官方模型页为准）。

###  `gpt-5` 家族与 `web_search`

- 你确认的关键点：`gpt-5` 家族支持 web_search（按官方工具支持表）。

### `files` 和`vector_stores`能力

- 必须要用官方原生的API，与个人的账号绑定，中转站api无法调用
- 是否可用取决于具体模型能力（模态支持与工具支持矩阵）。

