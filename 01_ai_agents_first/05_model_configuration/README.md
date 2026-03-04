# [如何在不同层级（全局、运行和 Agent）配置 LLM 提供方](https://colab.research.google.com/drive/1nWQny-AxpqQB3HGkyFLBCuai3G4igx6X?usp=sharing)?

Agents SDK 默认使用 OpenAI 作为提供方。使用其他提供方时，可以在不同层级进行配置：
1. Agent 层级
2. 运行层级
3. 全局层级

我们通常会优先采用 Agent 层级配置，这样每个 agent 都可以使用最适合它的 LLM。

## 1. AGENT 层级

```python
import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled

gemini_api_key = ""

#Reference: https://ai.google.dev/gemini-api/docs/openai
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

set_tracing_disabled(disabled=True)

async def main():
    # This agent will use the custom LLM provider
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    )

    result = await Runner.run(
        agent,
        "Tell me about recursion in programming.",
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
```

## 2. 运行层级

```python
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

gemini_api_key = ""

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Hello, how are you.", run_config=config)

print(result.final_output)
```

## 3. 全局层级

```python
from agents import Agent, Runner, AsyncOpenAI, set_default_openai_client, set_tracing_disabled, set_default_openai_api

gemini_api_key = ""
set_tracing_disabled(True)
set_default_openai_api("chat_completions")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_default_openai_client(external_client)

agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model="gemini-2.0-flash")

result = Runner.run_sync(agent, "Hello")

print(result.final_output)
```

## 总结

Q：为什么要设置三个层级的model config，全局、agent、runner？

> 设置全局、Agent、Runner 三个层级，本质上是为了同时解决“默认值复用”、“角色差异化”和“单次执行覆盖”这三类不同问题。

- 全局配置适合放项目级默认值。比如默认模型提供商、默认客户端、默认 tracing 行为。这样你不用在每个地方重复写一遍，项目能先有一个统一基线。

- Agent 级配置适合表达“这个智能体是谁、该用什么模型”。因为不同 Agent 的职责不同，代码生成、分类、摘要、规划，未必应该用同一个模型。把模型绑在 Agent 上，语义最清楚，也最符合“Agent 是一份能力配置”的设计。

- Runner 级配置适合处理“这一次运行要临时改规则”。比如压测时换便宜模型、某次请求关闭 tracing、某个环境切到别的 provider，或者同一个 Agent 在不同调用场景下使用不同模型。这个层级不改 Agent 定义，只影响当前这次 run。

可以把它理解成三层覆盖关系：

>  全局默认 < Agent 专属 < Runner 本次执行

这样设计的好处是：

- 全局层减少重复配置。
- Agent 层保留多智能体之间的角色差异。
- Runner 层允许调用时临时覆盖，不污染长期定义。

如果只保留一个层级，会出问题：

- 只有全局：所有 Agent 很难差异化。
- 只有 Agent：每次临时切模型都要改 Agent 对象，不灵活。
- 只有 Runner：每次调用都要传完整配置，重复且容易错。

一句话说，三个层级分别服务于“项目默认”、“角色定义”和“单次执行”。这不是重复设计，而是把配置作用域拆清楚。
