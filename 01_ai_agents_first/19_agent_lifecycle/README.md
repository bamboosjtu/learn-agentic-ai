# Agent Lifecycle Hooks - 完整初学者指南

## 什么是 Agent Lifecycle Hooks？

你可以把 Agent Lifecycle Hooks 理解成某个特定智能体的事件监听器。就像你会给手机设置通知一样，你也可以给智能体设置“监听器”，在关键事件发生时收到通知。

### 房屋类比
把智能体想象成一座智能房屋。Agent lifecycle hooks 就像布置在这栋房子里的摄像头和传感器，专门用来观察这一个智能体内部发生了什么：

- 前门摄像头（开始接管任务时）
- 工具间传感器（使用工具时）
- 书房监控（调用 LLM 思考时）
- 出口传感器（任务结束时）

## AgentHooksBase 类

这是你针对单个智能体的“监控系统”。你把它挂在 `agent.hooks` 上，就能观察这个智能体发生的事情。

### 可用 Hooks

#### 1. `on_start`
```python
async def on_start(context, agent):
    print(f"Agent {agent.name} is now in charge of handling the task")
```

当这个智能体开始接管当前任务时触发。

#### 2. `on_end`
```python
async def on_end(context, agent, output):
    print(f"Agent {agent.name} completed work with result: {output}")
```

当智能体完成工作并产出结果时触发。

#### 3. `on_llm_start`
```python
async def on_llm_start(context, agent, system_prompt, input_items):
    print(f"Agent {agent.name} is asking the AI for help with: {input_items}")
```

当智能体开始调用 LLM 进行推理时触发。

#### 4. `on_llm_end`
```python
async def on_llm_end(context, agent, response):
    print(f"Agent {agent.name} got AI response: {response}")
```

当 LLM 返回结果时触发。

#### 5. `on_tool_start`
```python
async def on_tool_start(context, agent, tool):
    print(f"Agent {agent.name} is using tool: {tool.name}")
```

当智能体开始使用工具时触发。

#### 6. `on_tool_end`
```python
async def on_tool_end(context, agent, tool, result):
    print(f"Agent {agent.name} finished using {tool.name}. Result: {result}")
```

当工具执行完成时触发。

#### 7. `on_handoff`
```python
async def on_handoff(context, agent, source):
    print(f"Agent {agent.name} received handoff from {source.name}")
```

当当前智能体从另一个智能体手里接管任务时触发。

## 一个完整流程示例

```
User: "What's the weather in New York?"

on_start
on_llm_start
on_llm_end
on_tool_start
on_tool_end
on_llm_start
on_llm_end
on_end
```

## 理解 `on_start` 和 `on_llm_start` 的区别

- `on_start`：智能体开始负责当前任务，只会在接管时触发一次。
- `on_llm_start`：智能体开始向 LLM 请求推理帮助，在一次任务里可能发生多次。

## 简单示例

```python
from openai_agents import Agent, AgentHooksBase

class MyAgentHooks(AgentHooksBase):
    async def on_start(self, context, agent):
        print(f"{agent.name} is starting up!")
    
    async def on_llm_start(self, context, agent, system_prompt, input_items):
        print(f"{agent.name} is asking AI for help")
    
    async def on_llm_end(self, context, agent, response):
        print(f"{agent.name} got AI response")
    
    async def on_tool_start(self, context, agent, tool):
        print(f"{agent.name} is using {tool.name}")
    
    async def on_tool_end(self, context, agent, tool, result):
        print(f"{agent.name} finished using {tool.name}")
    
    async def on_end(self, context, agent, output):
        print(f"{agent.name} completed the task!")

my_agent = Agent(
    name="Helper Bot",
)

my_agent.hooks = MyAgentHooks()
```

## 关键点

1. 这些 hooks 只观察一个指定智能体。
2. 每个智能体都可以拥有自己独立的一套 hooks。
3. 通过 `agent.hooks = YourHooksClass()` 挂载。
4. 所有 hook 方法都必须是 `async`。
5. `on_llm_start` 和 `on_tool_start` 可能多次发生。

## 常见错误

### 不要这样做
```python
def on_start(self, context, agent):  # Missing async
    print("Started")
```

### 正确方式
```python
async def on_start(self, context, agent):
    print("Started")
```

可以把 Agent hooks 想成给每个智能体配了一个贴身助理，专门帮你记录它做过的事情。
