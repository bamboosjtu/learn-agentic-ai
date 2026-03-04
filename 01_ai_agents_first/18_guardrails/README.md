# AI Agent Guardrails

## 什么是 Guardrails？

可以把 guardrails 理解成山路边上的防护栏。正如真实的护栏能防止车辆冲下危险悬崖，AI guardrails 可以防止智能体做出不该做的事，或生成有害、不合适、代价高昂的输出。

### 现实类比：餐厅门口的保安

想象你经营一家高档餐厅，里面的主厨很贵，就像你的 AI 智能体。你不希望任何人都能进来随意浪费主厨时间，于是你雇了两个保安：

- **输入保安（Input Guardrail）**：顾客进门前先检查
- **输出保安（Output Guardrail）**：主厨出菜后先检查

如果任何一个保安发现问题，都可以立刻拦下流程并妥善处理。

## 为什么需要 Guardrails？

### 成本问题
- 恶意用户可能会浪费你的资源
- 不合适的请求可能触发高成本操作
- 智能体可能会生成有害内容，或者偏离品牌风格

### 安全问题
AI 智能体有时可能：
- 生成不当内容
- 泄露敏感信息
- 提供有害指导
- 偏离其原本用途

## Guardrails 的类型

### 1. 输入 Guardrails

**作用**：在主智能体处理用户输入之前先检查输入

### 2. 输出 Guardrails

**作用**：在把回复发给用户之前先检查智能体输出

## Guardrails 的工作方式：三步流程

### 输入 Guardrails 流程
1. Receive
2. Analyze
3. Decide

### 输出 Guardrails 流程
1. Receive
2. Analyze
3. Decide

## 实例 1：检测数学作业（输入 Guardrail）

```python
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)

class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

guardrail_agent = Agent( 
    name="Homework Police",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
)

@input_guardrail
async def math_guardrail( 
    ctx: RunContextWrapper[None], 
    agent: Agent, 
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)
    
    return GuardrailFunctionOutput(
        output_info=result.final_output, 
        tripwire_triggered=result.final_output.is_math_homework,
    )
```

## 实例 2：检测敏感信息（输出 Guardrail）

```python
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    output_guardrail,
)
```

## 高级 Guardrail 策略

### 1. 级联 Guardrails
```python
agent = Agent(
    name="Multi-Protected Agent",
    input_guardrails=[
        profanity_filter,
        topic_validator,
        rate_limiter,
    ],
    output_guardrails=[
        privacy_checker,
        quality_validator,
        brand_compliance,
    ]
)
```

### 2. 上下文感知 Guardrails
```python
@input_guardrail
async def context_aware_guardrail(ctx, agent, input):
    user_context = ctx.context.get('user_history', {})
    
    if user_context.get('suspicious_activity', False):
        pass
```

## 实施 Guardrails 的最佳实践

- 保持 Guardrail 快而便宜
- 明确设计 Tripwire 逻辑
- 优雅处理异常
- 持续监控和迭代

## 结论

Guardrails 是 AI 智能体中非常关键的安全与成本控制机制。它们像智能过滤器一样，在问题发生前拦截不当输入或不安全输出。
