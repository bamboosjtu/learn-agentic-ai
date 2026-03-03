# 本章小结



## 1. Chat Completions API 与 Responses API

### 1.1 Chat Completions API
- 经典消息列表输入（`messages`）。
- 典型场景：基础对话、简单工具调用。
- 你需要显式管理对话历史（无状态风格）。

### 1.2 Responses API
- 更统一的输入输出结构（`input` + `output items`）。
- 原生更适合工具编排、推理、文件输入、Web Search、File Search。
- 支持 `previous_response_id` 进行会话延续，减少手动拼接历史。

### 1.3 两者共同点与差异
- 都可做工具调用与结构化输出。
- Responses API 在复杂 Agent 场景中更自然（工具、检索、推理链路更统一）。

---

## 2. Structured Outputs 与 Parse

### 2.1 `create` vs `parse`
- `create`：返回原始内容，需你自己 `json.loads` + 校验。
- `parse`：SDK 帮你按 schema / Pydantic 解析，直接拿到结构化对象（如 `parsed`）。

### 2.2 `response_format` 与格式约束
- `json_schema`：强约束结构化输出（推荐）。
- `json_object`：只保证合法 JSON，不保证业务 schema 完全匹配。

### 2.3 典型错误：`NoneType` on `response.output[0]`
- 根因：`response.output` 第一个元素是特殊，却直接下标访问。
- 常见原因：请求不完整、网关兼容问题、异常状态。
- 实践：先检查 `status/error/incomplete_details/output is None`，再访问 `output`。

---

## 3. Pydantic 的两种角色（重点）

你提出的关键理解非常重要：

### 3.1 在 Structured Output 中
- 约束的是“模型最终回答”的结构。
- 输出目标是给用户/前端/下游系统的最终数据格式。

### 3.2 在 Function Calling 中
- 约束的是“模型发起工具调用时的参数结构”（arguments）。
- 不是最终回答格式。

### 3.3 结论
- 两者不冲突，作用阶段不同。
- 工程上常见是“先 tools（参数）再 structured output（最终答案）”。

---

## 4. Function Calling

### 4.1 标准两步闭环
1. 模型返回 tool call（函数名 + 参数）。
2. 客户端执行函数并回传结果。
3. 模型基于工具结果给最终回答。

### 4.2 多轮/多工具循环
- 一次请求可能触发多个 tool calls。
- 需要循环处理：识别每个 `function_call` -> 执行 -> 逐个回传 `function_call_output`。

### 4.3 Chat 与 Responses 的处理差异
- Chat API：消息拼接方式更传统。
- Responses API：`output` 里包含不同 item（reasoning、function_call 等），需按 `type` 过滤处理。

### 4.4 `previous_response_id`
- Responses API 可用它续接上下文。
- 在多轮工具调用时可减少手动传历史负担。

---

## 5. File Input / Files API / File Search / Retrieval

### 5.1 `openai.files.create(..., purpose="user_data")` 作用
- 上传本地文件，获得可复用的 `file.id`。
- 后续可用于 `input_file` 或加入向量库做检索。

### 5.2 `file.id` 与 API Key 权限
- `file.id` 不是上传 token，而是资源 ID。
- 是否可跨 key 使用，取决于同组织/同项目权限边界。

### 5.3 `files.create` 400 报错
- 报错来自第三方网关（Aihubmix），不是 `rich.print(file)`。
- 本质是请求已失败，`file` 对象未创建。
- 推断重点：第三方对 OpenAI Files API 兼容与权限策略可能不完整。

### 5.4 File Search vs Retrieval
- `file_search`：模型内置检索工具，偏“托管式”。
- `retrieval`：你手动控制检索流程、过滤、排序，偏“可控式”。

---

## 6. Web Search 工具

### 6.1 基本能力
- 通过 tools 让模型联网检索。
- 可返回引用来源（citation/url annotation）。

### 1.2 常见控制项
- 域名限制（`allowed_domains`）。
- 用户地理位置（`user_location`）。
- 实时联网与缓存模式控制（依模型与参数支持而定）。

---

## 7. Reasoning（推理）

### 7.1 推理模型特点
- 更擅长多步问题与复杂决策。
- 常见参数：`reasoning.effort`（低/中/高）。

### 7.2 Token 与不完整响应
- 推理 token 会消耗输出预算。
- 若预算不足可能出现 `incomplete`，需提高 `max_output_tokens` 或调整策略。

---

## 8. 模型认知

### 8.1 `o3-mini` vs `gpt-4o`
- `o3-mini`：偏推理模型。
- `gpt-4o`：通用多模态模型（非纯推理定位）。

### 8.2 `gpt-4o` vs `gpt-4o-search-preview`
- 前者：通用能力更强（含多模态、函数调用等）。
- 后者：面向搜索场景，能力边界更窄（以官方模型页为准）。

### 8.3 `gpt-5` 家族与 `web_search`
- 你确认的关键点：`gpt-5` 家族支持 web_search（按官方工具支持表）。

### 8.4 `file_input` 能力
- 不是所有模型都支持。
- 是否可用取决于具体模型能力（模态支持与工具支持矩阵）。

