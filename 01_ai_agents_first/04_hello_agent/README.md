### [什么是 OpenAI Agents SDK？](https://openai.github.io/openai-agents-python/)

想象你要构建一个**智能助手**，比如聊天机器人或 AI agent，它可以：

* 智能回答问题；
* 使用计算器、网页搜索等工具；
* 并且知道何时把任务交给另一个更擅长的 agent。

**OpenAI Agents SDK** 可以帮助你用 Python 更容易地构建这类智能体。

---

### 用大白话解释

可以这样理解：

* **Agent** = 一个有明确职责（instructions）的智能 AI 角色（由 GPT 驱动）。
* **Tool** = 计算器、文件读取器，或 agent 可调用的任意能力。
* **Handoff** = 一个 agent 把任务转交给另一个更专业的 agent。
* **Guardrail** = 输入过滤器或检查点，用于确保输入符合要求。
* **Runner** = 驱动 agent 运行的执行引擎。

---

### 给 5 岁小朋友的类比

想象你在一所大学校里，里面有很多老师。

* 数学老师负责数学题。
* 历史老师负责历史问题。
* 前台老师负责判断学生该找哪位老师。

Agents SDK 的工作方式类似：

1. “学生”（用户）先提出问题。
2. “前台 agent”读取问题，并把它**交接（handoff）**给合适的老师（agent）。
3. 老师可能会使用**工具**，比如计算器。
4. 如果问题不合规，**guardrail** 可能会在问题到达老师前拦截。
5. 整个过程都会被记录，便于你查看发生了什么并调试（这叫 tracing）。

---

### Hello World 示例（Python）

```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)
```

输出：

```
Code within the code,
Functions calling themselves now,
Infinite loop's dance.
```

---

### 为什么要用它？

* 上手快，代码也好写。
* 能构建**真实业务可用的 AI 工作流**。
* 原生支持 **tools、agents、handoffs 和 guardrails**。
* 帮你**可视化与追踪** AI 推理过程中发生了什么。
