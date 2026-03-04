## APIs：超新手友好指南

### 1. API 到底是什么？

| **核心概念** | **大白话解释** |
| --- | --- |
| **API** = *Application Programming Interface*（应用程序编程接口） | 一组规则，让一个软件可以和另一个软件通信。 |
| 把它想成“餐厅菜单” | 你不需要走进后厨；你只要点菜单，服务员把菜端来。后厨更换炉具或改菜谱，你也不用操心。 |

### 更多日常类比

| 场景 | “后厨” | “服务员 / API” | “你（客户端）” |
| --- | --- | --- | --- |
| 天气 App | 气象公司的服务器 | 天气 API | 你的手机 |
| 打车 App | Uber/Lyft 后端 | 行程预订 API | 乘客端 App |
| 网店结账 | Stripe / PayPal | 支付 API | 商城网站 |

---

### 2. API 在实际中长什么样？

下面有两个非常小的真实请求示例，你可以在 Postman 中直接试（GET 示例也可在浏览器里试）。

> 给完全新手的小提示：
>
> Postman 是一个免费桌面应用，可让你构造请求并查看原始响应。点击 **Send** 后，Postman 还可以生成现成代码片段（Python、JavaScript、curl 等）。可找界面中的“`</>` Code”按钮。

| # | 真实任务 | 请求类型 | 示例 URL（无需账号） | Postman 快速步骤 |
| --- | --- | --- | --- | --- |
| 1 | 获取伦敦今天的天气 | GET | https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true | 1. 新建请求 -> GET 2. 粘贴 URL -> Send |
| 2 | 获取一条随机猫咪冷知识 | GET | https://catfact.ninja/fact | 1. 新建请求 -> GET 2. 粘贴 URL -> Send |

---

### 3. OpenAI 的 **Chat Completions API**（无状态）

> “你每次调用我，都要提醒我之前谁说了什么。”

- 你需要在每次请求里附上**完整对话历史**。
- 适合你想**完全掌控**记忆、顺序和自定义逻辑的场景。

```python
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"user","content":"What's the capital of France?"}]
)
print(response.choices[0].message.content)   # Paris

```

---

### 4. OpenAI 的 **Responses API**（有状态，原生支持工具）

> “我可以记住对话，需要时还能帮你查信息。”

- 你只需要发送**新的用户输入**；服务端会为你保存历史。
- 每次调用可按需开启内置“超能力（tools）”：
  - Web 搜索
  - 文件检索
  - 代码解释器
  - 图像生成

```python
from openai import OpenAI
client = OpenAI()

# 1) 使用工具提问，并保存记忆
r1 = client.responses.create(
    model="gpt-4o-mini",
    input="Search the latest AI news in healthcare.",
    store=True,
    tools=[{"type":"web_search_preview"}]
)

# 2) 继续追问（无需重传历史）
r2 = client.responses.create(
    previous_response_id=r1.id,
    input="Summarize those findings in bullet points."
)

print(r2.response.text)

```

---

### 5. 快速对比

| 特性 | **Chat Completions** | **Responses** |
| --- | --- | --- |
| 记忆 | 无状态：每次都要附带历史消息 | 有状态：服务端记住上下文 |
| 内置工具 | 手动接函数调用 | 一行配置即可启用 |
| 典型用途 | 简单对话、精细控制 | 智能助理、研究型机器人 |
| 追问方式 | 继续传 `messages=[...]` | 传 `previous_response_id` 即可 |
| 样板代码 | 更多 | 更少 |

---

### 6. “我该先学哪个？”

| 目标 | 推荐 |
| --- | --- |
| 学习 LLM 基础响应机制 | **Chat Completions**（能看到完整“消息夹心”） |
| 快速搭一个带记忆 + 联网搜索的助手 | **Responses** |
| 集成**你自己的**自定义函数工具 | **Chat Completions**（当前更常见） |
| 希望服务端状态管理尽可能简单 | **Responses** |

> 结论：如果你在实验或学习概念，先从 Chat Completions 开始。
>
> 如果你想快速得到“能记忆、能检索”的现成 agent，直接用 **Responses**。

---

## Bonus：给好奇者的下一步

1. 先在 Postman 试上面的天气 API，然后点击 “Code”，复制 *Python requests* 代码片段到 `.py` 文件里运行。
2. 把 URL 换成另一个公开 API（例如 `https://catfact.ninja/fact`）。
3. 熟悉后，用同样流程试 OpenAI Chat Completions 接口：Postman -> `POST` -> `https://api.openai.com/v1/chat/completions`。
