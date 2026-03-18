# Agentic AI 项目

## 项目 1：克隆 “OpenAI Study Mode”

**目标：** 构建一个可运行的 Study Mode 克隆版本，支持结构化学习流程（讲解、测验、复习），帮助学生更高效地学习。

**实现选项（先选一个起步，后续再逐步升级）：**

* **Google AI Studio**：适合还不熟悉 OpenAI Agents SDK 或 n8n 的同学。
* **n8n + Gemini + Lovable**：低代码 / 无代码编排，适合快速迭代。
* **OpenAI Agents SDK + Gemini + Chainlit**：完整控制、面向生产环境的实现路径。

**交付物：**

* 核心流程：“像对新手解释一样讲解”、抽认卡 / 小测验、间隔重复复习。
* 可配置的学习“模式”，例如初学者模式、练习模式、考试模式。
* 包含安装、环境变量和使用说明的 README，以及演示脚本或简短演示说明。

**参考：** [https://openai.com/index/chatgpt-study-mode/](https://openai.com/index/chatgpt-study-mode/)

---

## 项目 2：高级财务账户 Agent（Xero）

**目标：** 扩展 Xero 工具包 Agent，用于会计分析任务。

**技术栈：** OpenAI Agents SDK + Gemini + Chainlit

**增强点：**

* 多工具 Agent：支持认证、数据获取、试算平衡分析、异常标记。
* 自然语言查询转换为结构化分析结果，例如 CSV 摘要，后续还可以扩展成图表。
* 加入护栏能力：限流、重试机制，以及友好的错误提示。

**参考：** [https://github.com/XeroAPI/xero-agent-toolkit/tree/main/python/openai](https://github.com/XeroAPI/xero-agent-toolkit/tree/main/python/openai)

---

## 项目 3：容器化 Study Mode 克隆版

**目标：** 使用 Docker 对应用进行容器化，构建干净、可复现的运行环境，让“只在我机器上能跑”变成“在哪都能跑”。

**产出：**

* `Dockerfile`
* `docker-compose.yml`（用于本地开发）
* `.env.example`
* 健康检查和最基础的日志能力

---

## 项目 4：在 Kubernetes 上部署 Study Mode

**目标：** 用最小且可复现的方式，把 Study Mode 克隆版跑在 Kubernetes 上。

**产出：**

* K8s 清单文件：`Deployment`、`Service`、`Ingress`（或 `Gateway`）、`ConfigMap` / `Secret`
* 基础自动扩缩容（HPA）
* 滚动更新
* 基础可观测性接入点

---

## 项目 5：容器化高级财务账户 Agent

**目标：** 对财务 Agent 做 Docker 化，构建可预测的镜像和安全配置。

**产出：**

* 生产级 `Dockerfile`（例如 distroless / alpine）
* 多阶段构建
* 非 root 用户运行
* 通过环境变量或 Secret 管理密钥
* 在 CI 中加入 lint，提前发现风险

---

## 项目 6：在 Kubernetes 上部署高级财务账户 Agent

**目标：** 以生产环境风格将财务 Agent 部署到 Kubernetes 上，并补齐资源策略，避免服务无节制占用集群资源。

**产出：**

* `Deployment` / `Service` / `Ingress`
* HPA
* `PodDisruptionBudget`
* 资源请求与限制（requests / limits）
* 基础 tracing / logging

---

## 项目 7：Study Mode on Kubernetes + Dapr

**目标：** 引入 **Dapr** 来实现服务发现、发布订阅、bindings 和 secrets 管理，用更低心智负担实现微服务能力。

**产出：**

* 为服务接入 Dapr sidecar
* 基于 pub/sub 处理事件，例如 `quiz-completed`
* 支持可替换组件，例如不改应用代码即可把 Redis 切换为 NATS

---

## 项目 8：Advanced Accounts Agent on Kubernetes + Dapr

**目标：** 使用 Dapr 的构建模块（状态存储、pub/sub、密钥存储）实现更稳健的财务工作流。

**产出：**

* 事件驱动流水线，例如 `fetch → analyze → notify`
* 幂等处理器
* 集中式 secrets 管理
* 可插拔输出方式，例如 webhook、队列、邮件网关

---

## 项目 9：使用 Ray 的分布式 Python（Anyscale 教程）

学习视频：<https://www.youtube.com/watch?v=pX8OG4P9_V0>

**链接：** [https://www.anyscale.com/blog/writing-your-first-distributed-python-application-with-ray](https://www.anyscale.com/blog/writing-your-first-distributed-python-application-with-ray)

**目标：** 通过构建一个小型分布式 Python 应用来学习 Ray 的 task / actor 模型，然后逐步把它升级到更接近生产的实现。

**为什么适合这里：** Ray 提供了简单的基础原语（tasks、actors、datasets），可以在不手写复杂分布式系统的前提下扩展 CPU / GPU 工作负载。

**核心产出（偏实操、上手快）：**

* 在本地运行教程中的最小 Ray 应用，并使用单机多核构成 Ray “集群”
* 实现 tasks 和 actors，加入重试 / 超时机制，并采集基础指标和日志
* 将应用打包成一个简洁模块，并提供清晰的 CLI 入口

**扩展目标（按需选择）：**

* **Ray Serve**：为计算图暴露 HTTP 接口
* **Kubernetes + KubeRay**：在本地 Rancher Desktop 或云上部署 `RayCluster` CRD
* **Pipelines**：与 Study Mode 或财务 Agent 集成，处理重计算任务，例如批量评分、特征计算
* **Dapr**：通过 pub/sub 触发 Ray 任务
* **Agentic AI：** <https://www.anyscale.com/blog/massively-parallel-agentic-simulations-with-ray>

---

## 本地 Kubernetes 开发

**Rancher Desktop：** [https://www.rancher.com/](https://www.rancher.com/)

可在本地通过可视化界面启动 Kubernetes 环境。

---

## 免费、免绑卡的 Kubernetes 练习环境

这是一个无需把本地电脑折腾得太重，也能快速练习 Kubernetes 的方式。

### Killercoda — Kubernetes Playgrounds

* 介绍： [https://killercoda.com/about](https://killercoda.com/about)
* Playground： [https://killercoda.com/playgrounds/scenario/kubernetes](https://killercoda.com/playgrounds/scenario/kubernetes)

提供真实的浏览器内 k8s / k3s 集群（单节点或多节点）。免费会话通常持续约 1 小时，可按需重启。

### Play-with-Kubernetes（Docker）

* Workshop： [https://training.play-with-kubernetes.com/kubernetes-workshop/](https://training.play-with-kubernetes.com/kubernetes-workshop/)

Docker 提供的经典浏览器实验环境，需要用 Docker ID 或 GitHub 登录。会话是临时性的。

---

## 免费云 Kubernetes（需要信用卡）

这些优惠可能变化，使用前应先核实最新条款。

* **Civo Cloud — 最经济**
  **250 美元**额度，通常为注册后约 1 个月；需要绑卡，但额度内通常不会额外收费。  
  注册： [https://www.civo.com/signup](https://www.civo.com/signup)

* **DigitalOcean — 较合理**
  **100 美元**额度，通常为 60 天（通过推荐或官方链接）；需要绑卡。  
  推荐链接： [https://m.do.co/c/8cce85e94a19](https://m.do.co/c/8cce85e94a19)

* **Alibaba Cloud — 12 个月免费额度**
  **300 美元**额度，分 12 个月提供；需要绑卡；Kubernetes 也出现在其 “always free” 资源中。  
  入口： [https://www.alibabacloud.com/](https://www.alibabacloud.com/)

* **Microsoft Azure（AKS）**
  **200 美元**额度，30 天；需要绑卡。AKS 通常对 AI / ML 工作负载也比较经济。  
  免费入口： [https://azure.microsoft.com/en-us/free/](https://azure.microsoft.com/en-us/free/)

---

## 免费 Ray Cloud

<https://console.anyscale.com/register/ha>

### 建议里程碑（每个项目都可以参考）

* **M1：** 功能完整（happy path）
* **M2：** 测试 + 文档 + lint
* **M3：** 容器化 + 本地 compose
* **M4：** K8s 清单 + CI 部署
* **M5：** Dapr 集成（如适用）

---

### 验收清单（适用于项目 1–8）

* 清晰的 README 和 `.env.example`
* 可复现的运行方式：`make dev`、`docker compose up`、`kubectl apply -f k8s/`
* 健康检查、基础日志、优雅关闭
* 一键演示脚本或 Chainlit 应用

如果一个新同事能在 10 分钟内把项目跑起来，这个项目的交付质量基本就过关了。

---
