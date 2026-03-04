# OpenAI Traces Dashboard

这个文件夹包含一些示例，用来演示如何使用 OpenAI 的 Traces Dashboard 对 LLM 应用进行监控与分析。

## 官方资源
- [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/tracing/)
- [OpenAI Traces Dashboard](https://platform.openai.com/traces)

## 第一部分：理解可观测性（看见你的应用在做什么）

### 什么是 Observability（可观测性）？

简单来说，可观测性指的是你能够看到并理解 AI 应用在运行时到底做了什么。

如果把你的 AI 应用想成一个正在工作的员工，那么可观测性就像一台记录全过程的监控摄像头。你可以回放整个过程，弄清楚发生了什么。

### 为什么我们需要可观测性？

当你向 AI 应用提问时，幕后通常会发生很多事情：

- 应用接收你的问题
- 它可能调用 AI 模型
- 它可能搜索文档
- 它可能使用工具或函数
- 最后才把答案返回给你

如果没有可观测性，你就像在盲飞。你只能看到最终答案，却不知道应用是怎么走到这一步的。

---

## 第一步：理解基础构件

### 什么是 Run？

**run** 是应用执行的单个动作或步骤。

例子：做一个三明治

- 取出面包 = 1 个 run
- 涂黄油 = 1 个 run
- 加奶酪 = 1 个 run
- 把两片面包合起来 = 1 个 run

每一个单独动作都可以理解为一个 run。

在 AI 应用中：

- 调用一次 AI 模型 = 1 个 run
- 搜索一次文档 = 1 个 run
- 格式化一次 prompt = 1 个 run

关键点：run 是应用里最小的工作单元。

---

### 什么是 Trace？

**trace** 是从开始到结束发生的全部过程记录。

继续用三明治类比：

- 整个做三明治流程（4 个步骤加起来）= 1 个 trace
- 每一个步骤 = 这个 trace 中的一个 run

在 AI 应用中：

- 用户提问 -> 应用搜索文档 -> 调用模型 -> 返回答案
- 整个序列 = 1 个 trace
- 每一个箭头之间的动作 = trace 中的一个 run

关键点：trace 是一组 run，描述了从输入到输出的完整旅程。

---

## 第二部分：使用 OpenAI Platform 进行基础 Tracing

## 功能
- 实时监控 LLM 调用
- 性能分析
- 成本跟踪
- 错误分析
- 请求/响应可视化

## 环境要求
- OpenAI API key
- 已安装 OpenAI Agents SDK
- 支持异步的 Python 环境

## 示例结构
这个文件夹会包含如下示例：
1. 基础 tracing 设置
2. 自定义 trace 属性
3. 性能监控
4. 错误追踪
5. 成本分析

## OpenAI Agents SDK 示例
```python
from agents import Agent, Runner, trace
import asyncio

from agents import Agent, Runner, trace

async def main():
    agent = Agent(name="Joke generator", instructions="Tell funny jokes.")

    with trace("Joke workflow"): 
        first_result = await Runner.run(agent, "Tell me a joke")
        second_result = await Runner.run(agent, f"Rate this joke: {first_result.final_output}")
        print(f"Joke: {first_result.final_output}")
        print(f"Rating: {second_result.final_output}")

asyncio.run(main())
```

## 输出

```python
Joke: Why don't scientists trust atoms?

Because they make up everything!
Rating: That's a classic! I'd give it a solid 8 out of 10. It's a clever play on words and has that nerdy charm.

```

## OpenAI Tracing Dashboard
https://platform.openai.com/traces

