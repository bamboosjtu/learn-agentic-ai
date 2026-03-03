# Agentic AI 学习路线图（新手版）

## 如何使用这份路线图

1. 先做“主线必修”，完成后再做“全量选修”。
2. 每个阶段都以“能做出什么”为目标，避免只看不练。
3. 每个阶段必须学完对应文件夹，再提交阶段产物。

---

## 第一部分：主线必修（建议 14 周）

### 阶段 0：先把学习环境和仓库地图搞清楚

- 学习目标：能独立打开仓库、理解模块分布、运行最小示例。
- 学习内容（按文件夹）：
  - `other_material/01_python_syntax/`
  - 根目录文档：`README.md`、`certification.md`
- 阶段验收产物：
  - `artifacts/stage-0-setup.md`（环境安装、命令、问题记录）
  - 一个最小可运行 Python 模板项目

### 阶段 1：先学会直接调用大模型 API

- 学习目标：能完成提问、流式输出、函数调用、结构化输出。
- 学习内容（按文件夹）：
  - `00_openai_api/`
- 阶段验收产物：
  - `projects/api-playground/`
  - 包含：流式输出 + 1 个函数调用 + JSON 结构化输出

### 阶段 2：完整掌握 Agents SDK，从单 Agent 到多 Agent

- 学习目标：完成 Agents SDK 主线，能独立做出多 Agent 协作应用。
- 学习内容（按文件夹）：
  - `01_ai_agents_first/`
- 阶段验收产物：
  - `projects/multi-agent-assistant/`
  - 包含：2 个 Agent 协作 + 工具调用 + 会话记忆 + 基础 guardrails

### 阶段 3：学会用设计模式把 Agent 做得更稳定

- 学习目标：从“能跑”提升到“更稳定、更可评估”。
- 学习内容（按文件夹）：
  - `04_building_effective_agents/`
- 阶段验收产物：
  - `projects/task-oriented-agent/`
  - `evaluation/stage-3-report.md`（至少 10 条测试样例）

### 阶段 4：学会 MCP 和 A2A，让系统可互联

- 学习目标：理解并跑通 Agent 间标准协议通信。
- 学习内容（按文件夹）：
  - `03_ai_protocols/`
- 阶段验收产物：
  - `projects/protocol-demo/`
  - 包含：1 个 MCP 示例 + 1 个 A2A 流式任务示例

### 阶段 5：给 Agent 做一个可演示的前端界面

- 学习目标：让别人可以直接使用你的 Agent。
- 学习内容（按文件夹）：
  - `11_advanced_agentic_ui/`
- 阶段验收产物：
  - `projects/agent-ui/`
  - 包含：聊天界面 + 调用过程展示 + 错误提示

### 阶段 6：学会把 Agent 容器化并部署到云原生环境

- 学习目标：能把本地 Agent 服务部署为可复现环境。
- 学习内容（按文件夹）：
  - `07_daca_agent_native_dev/`
  - `08_daca_deployment_guide/`
- 阶段验收产物：
  - `projects/deployable-agent/`
  - 包含：`Dockerfile`、`k8s/`、部署与回滚说明

### 阶段 7：完成一个可讲解、可部署、可复现的毕业项目

- 学习目标：打通“需求 -> 开发 -> 部署 -> 演示”完整闭环。
- 学习内容（按文件夹）：
  - `AGENTIA_PROJECTS/`
  - `PROJECTS/`
- 阶段验收产物：
  - `projects/capstone-v1/`
  - 包含：架构图、README、演示脚本、部署文档、测试清单

---

## 第二部分：全量选修清单（主线完成后）

### 选修 A：把理论背景补齐

- 学习目标：看懂 Agentic AI 全景和术语体系。
- 学习内容（按文件夹）：
  - `-01_lets_get_started/`
  - `02_agentic_foundations/`
  - `xx_real_agentic_ai/`
- 阶段验收产物：
  - `electives/A/agentic-foundations-notes.md`

### 选修 B：学习 Agentic Web 与浏览器自动化

- 学习目标：理解网页场景下的 Agent 应用。
- 学习内容（按文件夹）：
  - `05a_agentic_web/`
  - `05b_agentic_browsers/`
  - `05c_agentic_org/`
- 阶段验收产物：
  - `electives/B/web-agent-demo/`

### 选修 C：学习规格驱动开发

- 学习目标：从需求文档拆解到实现落地。
- 学习内容（按文件夹）：
  - `06_spec_driven_vibe_coding/`
- 阶段验收产物：
  - `electives/C/spec-to-implementation/`

### 选修 D：强化 Kubernetes 实战能力

- 学习目标：提升部署、排障、运维能力。
- 学习内容（按文件夹）：
  - `09_ckad/`
- 阶段验收产物：
  - `electives/D/k8s-ops-playbook.md`

### 选修 E：补充 Agent 发现与互联能力

- 学习目标：构建可发现、可组合的多 Agent 系统。
- 学习内容（按文件夹）：
  - `10_agent_discovery/`
  - `12_agent_to_agent/`
- 阶段验收产物：
  - `electives/E/agent-registry-demo/`

### 选修 F：学习语音 Agent

- 学习目标：打通语音输入输出链路。
- 学习内容（按文件夹）：
  - `13_voice_agents/`
- 阶段验收产物：
  - `electives/F/voice-agent-prototype/`

### 选修 G：学习开源 LLM 与微调

- 学习目标：建立自托管与成本性能分析能力。
- 学习内容（按文件夹）：
  - `14_open_source_llms/`
- 阶段验收产物：
  - `electives/G/self-hosted-llm-benchmark.md`

### 选修 H：补齐认证与企业安全能力

- 学习目标：补齐鉴权、安全、企业治理基础。
- 学习内容（按文件夹）：
  - `15_authentication/`
  - `17_enterprise_features/`
- 阶段验收产物：
  - `electives/H/security-checklist.md`

### 选修 I：学习图数据库与 Graph RAG

- 学习目标：掌握图数据建模和查询，服务于 Agent 知识能力。
- 学习内容（按文件夹）：
  - `16_graph_query_language/`
- 阶段验收产物：
  - `electives/I/graph-rag-demo/`

### 选修 J：连接技术到创业实践

- 学习目标：将技术能力映射为 MVP 与产品路线。
- 学习内容（按文件夹）：
  - `18_agentia/`
  - `agentic_ai_startup_roadmap/`
  - `STARTUPS/`
- 阶段验收产物：
  - `electives/J/startup-brief.md`

### 选修 K：整理扩展与历史资料

- 学习目标：形成自己的技术雷达与优先级。
- 学习内容（按文件夹）：
  - `other_material/`
  - `backup_recent/`
- 阶段验收产物：
  - `electives/K/tech-radar.md`

---

## 通用验收规则

1. 每个阶段至少有一个可运行项目或可验证文档。
2. 每个产物必须有 `README`（目标、依赖、启动方式、结果示例）。
3. 不满足验收产物要求，不进入下一阶段。
