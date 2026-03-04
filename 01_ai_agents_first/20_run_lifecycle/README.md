# Run Lifecycle Hooks - 完整初学者指南

## 什么是 Run Lifecycle Hooks？

你可以把 Run Lifecycle Hooks 理解成整个系统级别的监控，而不只是某一个房间。Agent hooks 监控的是单个智能体，而 Run hooks 监控的是整次执行过程，也就是所有智能体协同工作的全局过程。

### 办公楼类比
想象你有一栋多层办公楼，每一层都有不同部门：

- **Run Hooks** = 整栋楼的安保系统
- **Agent Hooks** = 某个部门内部的专属摄像头

Run hooks 能看到所有楼层、所有智能体的行为；Agent hooks 只能看到它所属那个智能体内部发生的事情。

## RunHooksBase 类

这是你的“总控室”，用来监控整次智能体运行。你可以看到不同智能体如何轮流工作、调用工具、以及彼此 handoff。

### 可用 Hooks

#### 1. `on_agent_start`
```python
async def on_agent_start(context, agent):
    print(f"SYSTEM: Agent {agent.name} is now active")
```

#### 2. `on_agent_end`
```python
async def on_agent_end(context, agent, output):
    print(f"SYSTEM: Agent {agent.name} completed work with output: {output}")
```

#### 3. `on_llm_start`
```python
async def on_llm_start(context, agent, system_prompt, input_items):
    print(f"SYSTEM: {agent.name} is asking AI for help")
```

#### 4. `on_llm_end`
```python
async def on_llm_end(context, agent, response):
    print(f"SYSTEM: {agent.name} got AI response")
```

#### 5. `on_tool_start`
```python
async def on_tool_start(context, agent, tool):
    print(f"SYSTEM: {agent.name} using {tool.name}")
```

#### 6. `on_tool_end`
```python
async def on_tool_end(context, agent, tool, result):
    print(f"SYSTEM: {agent.name} finished using {tool.name}")
```

#### 7. `on_handoff`
```python
async def on_handoff(context, from_agent, to_agent):
    print(f"HANDOFF: {from_agent.name} -> {to_agent.name}")
```

## 完整多智能体流程示例

```
User: "My premium account isn't working and I need a refund"

on_agent_start: CustomerService
on_llm_start
on_llm_end
on_tool_start
on_tool_end
on_handoff: CustomerService -> TechnicalSupport
on_agent_end: CustomerService

on_agent_start: TechnicalSupport
...
```

## 理解 Run hooks 和 Agent hooks 的区别

**Run Hooks**
- 监控所有智能体
- 看到整次执行里发生的全部行为
- 关注多智能体协作的全局图景

**Agent Hooks**
- 只监控一个特定智能体
- 只看到那个智能体自己的行为
- 关注单个智能体内部执行细节

## 简单示例

```python
from openai_agents import Agent, RunHooksBase
from openai_agents.orchestration import run

class SystemMonitor(RunHooksBase):
    def __init__(self):
        self.active_agents = []
        self.tool_usage = {}
        self.handoffs = 0
    
    async def on_agent_start(self, context, agent):
        self.active_agents.append(agent.name)
        print(f"SYSTEM: {agent.name} is now working")
    
    async def on_tool_start(self, context, agent, tool):
        tool_name = tool.name
        if tool_name not in self.tool_usage:
            self.tool_usage[tool_name] = 0
        self.tool_usage[tool_name] += 1
        print(f"SYSTEM: {tool_name} used {self.tool_usage[tool_name]} times")
    
    async def on_handoff(self, context, from_agent, to_agent):
        self.handoffs += 1
        print(f"HANDOFF #{self.handoffs}: {from_agent.name} -> {to_agent.name}")

customer_service = Agent(name="CustomerService")
system_monitor = SystemMonitor()

result = await run(
    agents=customer_service,
    input="I need help with my account",
    run_hooks=system_monitor,
)
```

## 关键点

1. Run hooks 监控的是整次执行中的全部智能体。
2. 它提供的是全局视图。
3. 通过 `run_hooks=YourHooksClass()` 使用。
4. 很适合观察 handoff 与协作过程。
5. 非常适合做系统级性能与使用统计。

## 常见错误

### 不要这样做
```python
agent.hooks = RunHooksBase()  # Wrong
```

### 正确方式
```python
system_monitor = MyRunHooks()
result = await run(
    agents=agent1,
    run_hooks=system_monitor
)

agent1.hooks = MyAgentHooks()
```

## 什么时候用 Run Hooks，什么时候用 Agent Hooks

| 适合用 Run Hooks 的情况 | 适合用 Agent Hooks 的情况 |
|-------------------|---------------------|
| 监控整个系统 | 监控某个具体智能体 |
| 做系统级分析 | 调试某一个智能体 |
| 跟踪智能体协作 | 做单体日志记录 |

可以把 Run hooks 想成空中交通塔台，而 Agent hooks 更像某一架飞机上的机载仪表。
