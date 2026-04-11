# [Elicitation](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation) - 交互式工具体验

Model Context Protocol（MCP）提供了一种标准化方式，让 server 在工具执行过程中向用户请求额外信息。这使工具能够根据用户输入动态调整行为，从而构建交互式、动态化的体验。

## 🎯 学习目标
完成本课后，你将能够：
1. **理解** 工具为什么、以及在什么场景下需要向用户提问
2. **实现** 一个支持 elicitation 的基础 MCP server
3. **处理** MCP client 中的 elicitation 请求
4. **设计** 友好的交互式工具体验

## 🤔 为什么需要 Elicitation？

### 问题：静态工具 vs 交互式工具

**传统工具（静态）：**
```python
@mcp.tool()
def order_pizza(size: str, toppings: str) -> str:
    # User must provide ALL parameters upfront
    return f"Order: {size} pizza with {toppings}"
```

**交互式工具（带 Elicitation）：**
```python
@mcp.tool()
async def order_pizza(ctx: Context, size: str) -> str:
    # Ask for toppings only if user wants them
    result = await ctx.elicit(
        message="Would you like toppings?",
        schema=OrderPreferences
    )
    if result.data.want_toppings:
        return f"Order: {size} pizza with {result.data.toppings}"
    return f"Order: plain {size} pizza"
```

### 关键收益
1. **渐进式披露（Progressive Disclosure）：** 只在真正需要时再询问信息
2. **条件逻辑（Conditional Logic）：** 根据前面的回答动态调整后续问题
3. **更好的用户体验（Better UX）：** 引导用户完成复杂决策
4. **输入校验（Validation）：** 保证输入格式正确并满足约束

## 🏗️ 核心概念

### 1. 有状态连接
Elicitation 需要在工具执行中进行来回通信：
```
Client → Tool Request → Server
Client ← "Want toppings?" ← Server
Client → "Yes, mushrooms" → Server
Client ← Final Result ← Server
```

### 2. Elicitation Schema
使用 Pydantic 定义所请求数据的结构：
```python
class OrderPreferences(BaseModel):
    want_toppings: bool = Field(
        description="Would you like to add extra toppings?"
    )
    toppings: str = Field(
        default="mushrooms",
        description="What toppings would you like? (comma-separated)"
    )
```

### 3. 响应动作
Elicitation 请求可能有三种结果：
- **Accept：** 用户提供所请求的数据
- **Decline：** 用户明确拒绝提供数据
- **Cancel：** 用户关闭对话而没有做出选择

## 🛠️ 实现指南

### Server 端设置
1. 创建一个有状态 MCP server：
   ```python
   mcp = FastMCP(
       name="elicitation-server",
       stateless_http=False  # Required for elicitation
   )
   ```

2. 定义数据 schema：
   ```python
   class OrderPreferences(BaseModel):
       want_toppings: bool = Field(...)
       toppings: str = Field(...)
   ```

3. 创建支持 elicitation 的工具：
   ```python
   @mcp.tool()
   async def order_pizza(ctx: Context, size: str) -> str:
       result = await ctx.elicit(
           message=f"Ordering a {size} pizza. Would you like to customize it?",
           schema=OrderPreferences
       )
       # Handle the response...
   ```

### Client 端设置
1. 创建 elicitation 回调处理器：
   ```python
   async def mock_elicitation(
       context: RequestContext["ClientSession", Any], 
       params: types.ElicitRequestParams
   ) -> types.ElicitResult | types.ErrorData:
       print(f"<- Client: Received 'elicitation' request from server.")
       print(f"<- Client Parameters '{params}'.")
       
       # Return mock response (in real app, would get from user)
       return types.ElicitResult(
           action="accept",
           content={"want_toppings": True, "toppings": "fajita"}
       )
   ```

2. 使用回调初始化 session：
   ```python
   async with ClientSession(
       read_stream, 
       write_stream, 
       elicitation_callback=mock_elicitation
   ) as session:
       await session.initialize()
   ```

## 🚀 运行 Demo

### 前置准备
```bash
cd mcp_code
uv sync
```

### 启动 Server
```bash
uvicorn server:mcp_app --port 8000
```

### 运行 Client
```bash
python client.py
```

### 预期输出
```
🚀 Connecting to MCP server...
✅ Connected. Initializing session...

SCENARIO 1: Accepting the elicitation
----------------------------------------
<- Client: Received 'elicitation' request from server.
<- Client Parameters: [Schema and message details]
✅ Result: Order confirmed: large pizza with fajita

SCENARIO 2: Declining the elicitation
----------------------------------------
<- Client: Received 'elicitation' request from server.
<- Client Parameters: [Schema and message details]
✅ Result: Order confirmed: medium pizza with fajita
```

## 🎓 最佳实践

1. **清晰消息：**
   - 在 schema 中提供清晰提示
   - 为每个字段写有帮助的描述
   - 在 schema 中展示校验约束

2. **合理校验：**
   - 使用合适字段类型（bool、str 等）
   - 在合适情况下设置合理默认值
   - 为字段加描述，改善 UX

3. **渐进式披露：**
   - 只在需要时提问
   - 根据之前回答决定后续字段
   - 保持 schema 简洁、聚焦

4. **错误处理：**
   - 处理所有响应动作（accept/decline/cancel）
   - 提供清晰错误提示
   - 准备 fallback 行为

## 🔄 与其他课程的联系

**基于前面内容：**
- **Sampling：** 会思考的工具
- **本课：** 会提问的工具

**引向下一课：**
- **Roots：** 能理解项目上下文的工具

## 🎯 练习题

1. **基础：** 给 pizza toppings 增加校验（例如最多 3 个 toppings）
2. **中级：** 根据聚会人数给出尺寸建议
3. **高级：** 创建一个多步骤点餐向导（尺寸 → 配料 → 饮料）
---

**🎓 准备进入上下文能力了吗？** 接下来前往 [05_roots](../05_roots/)，学习工具如何发现并利用你的项目结构。
