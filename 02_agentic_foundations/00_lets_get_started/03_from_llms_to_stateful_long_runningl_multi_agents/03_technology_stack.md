# Dapr Agentic Cloud Ascent（DACA）技术栈：免费、可扩展的智能，更简单

Agentic AI 正在重塑我们解决问题的方式，我们正在利用它的力量提供可扩展、可适应的智能解决方案。我们的重点是为开发者提供工具，让他们能够创建定制化的 AI Agent 工作流，而不需要不必要的复杂性。通过采用一个极简但强大的架构，我们可以支持从简单查询到复杂多 Agent 系统的一切场景。

**[Dapr Agentic Cloud Ascent（DACA）设计模式综合指南](https://github.com/panaversity/learn-agentic-ai/blob/main/comprehensive_guide_daca.md)**

通过将预定义构件减少到最低限度，我们消除了冗余，并赋能开发者打造定制化的 agentic 解决方案，无论是一个简单查询还是一个复杂的多 Agent 工作流，都可以按我们的具体需求来定制。下面是在分层架构中使用的精简工具集：

1. **LLM APIs**：支持稳健的 Agent 开发，也是与 LLM 交互的事实标准。
2. **轻量级 Agents**：内置护栏、工具集成和无缝交接能力。
3. **REST APIs**：让用户、agent 团队以及团队间交互能够流畅通信。
4. **无状态 Serverless Docker 容器**：用于高效、可扩展的计算（Agents、API、MCP Servers）。
5. **异步消息传递**：连接容器化 AI agents 的动态通信方式。
6. **灵活的容器调用**：通过 HTTP 请求或定时 CronJobs 触发。
7. **关系型托管数据库服务**：用于稳健的数据处理。
8. **内存型数据结构存储**：常作为缓存提升应用性能。
9. **[模型上下文协议（MCP）](https://modelcontextprotocol.io/introduction)**：标准化 agentic 工具调用。
10. **[分布式应用运行时（Dapr）](https://dapr.io/)**：通过提供标准化构件简化构建具韧性的分布式系统，适用于 agentic 工作流。

依托这些核心组件，我们可以部署几乎任何 agentic 工作流，在简洁性与无限可能之间取得平衡。

### DACA 的基础

OpenAI Responses API 是构建 agentic AI 系统的关键基础之一，它提供了用于自主任务执行的高级能力。OpenAI Agents SDK 则通过提供强大的框架来编排基于 Responses API 的多 Agent 工作流，与之形成互补。二者共同构成了我们用于构建 agentic AI 的技术栈核心支柱。

![Agent Orchestration Layer](./agent-orchestration-layer.png)

---

## DACA 框架构件的详细说明

1. **LLM APIs**
   - **目的**：作为与大语言模型交互的核心接口，使 agents 能执行从简单查询到复杂多步推理的任务。它们标准化、稳健且被广泛支持。
   - **选择**：我们选择 **[OpenAI Chat Completion](https://platform.openai.com/docs/guides/text?api-mode=responses)** 和 **Responses API** 作为 LLM APIs。OpenAI 的 Chat Completion API 已成为事实上的行业标准，是兼具通用性和 agent 友好特性的成熟选择，例如 function calling；Responses API 则可提供互补能力。
   - **重要性**：这些 API 为 agentic 工作流提供可靠基础，让开发者能够轻松接入前沿 AI 能力。

2. **轻量级 Agents**
   - **目的**：这些是为特定任务设计的模块化 AI 单元，具备护栏（确保安全运行）、工具集成（例如网页搜索、文件解析等）和交接能力（与其他 agents 协作）。
   - **选择**：我们使用 **[OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)** 来构建这些 agents。这个 SDK 提供了一个简洁的方式创建轻量级 agents，并内置记忆管理（[LangMem](https://langchain-ai.github.io/langmem/) 集成）和工具使用能力。**[模型上下文协议（MCP）](https://modelcontextprotocol.io/introduction)** 标准化 agentic 工具调用。
   - **重要性**：轻量级 agents 以更少资源消耗实现灵活、可扩展的工作流，无论是单独部署还是作为团队的一部分都适用。

3. **REST APIs**
   - **目的**：REST API 使用户、agents 和 agent 团队之间能够通过 HTTP 无缝通信，提供无状态、标准化的实时交互接口。
   - **选择**：这里我们使用 **[FastAPI](https://fastapi.tiangolo.com/)**。FastAPI 是一个高性能、基于 Python 的工具，支持异步编程并自动生成 OpenAPI 文档，可加速开发。
   - **重要性**：它确保低延迟、可扩展的通信，这对面向用户的应用和 agent 间协调都至关重要。

4. **无状态 Serverless Docker 容器**
   - **目的**：这些容器以可移植、无状态的形式打包应用逻辑，例如 agents、API、Dapr、[模型上下文协议（MCP）](https://modelcontextprotocol.io/introduction) Servers，从而支持自动扩缩容与便捷部署，而无需保留内部持久状态。
   - **选择**：我们使用 **[Docker 容器](https://www.docker.com/resources/what-container/)**，它提供轻量、一致、可跨平台部署的运行环境。容器托管方面，原型阶段使用 **[Hugging Face Docker Spaces](https://huggingface.co/docs/hub/en/spaces-sdks-docker)**（内置 CI/CD 的免费托管），生产训练则使用运行在 **[永久免费 Oracle VM](https://github.com/nce/oci-free-cloud-k8s)** 上的 [Kubernetes](https://kubernetes.io/)。
   - **重要性**：容器支持快速部署和高效资源利用，与轻量框架强调的简洁性和可扩展性一致。使用 Docker 部署 AI agents 已被广泛认为是最佳实践，也是事实上的行业标准。Docker 容器提供轻量、可移植且一致的环境，确保 AI 应用能在不同平台上稳定运行。此外，Docker 的广泛采用也形成了丰富的工具与服务生态，进一步增强了它在 AI agent 部署中的价值。总之，Docker 容器为 AI agent 部署提供了标准化且高效的方法，因此是行业中的首选。

   另外，无状态容器不会在会话之间保留数据，这使其能够通过快速复制与分发提升扩展性。它们也可以被部署为 serverless 容器。我们不仅可以把这些无状态容器部署在 Hugging Face Container Spaces 和 Kubernetes 上，也可以部署在大多数云服务中：

   **各云服务提供商总结表**

   | 提供商 / 服务 | 事件驱动容器 | 定时容器 |
   |-------------|-------------|---------|
   | **AWS ECS** | 是 | 是 |
   | **AWS EKS** | 是 | 是 |
   | **AWS Fargate** | 是 | 是 |
   | **AWS Lambda** | 是 | 是 |
   | **AWS Batch** | 间接支持 | 是 |
   | **Azure Container Apps** | 是 | 是 |
   | **Azure Container Jobs** | 是 | 是 |
   | **Azure AKS** | 是 | 是 |
   | **Azure Functions** | 是 | 是 |
   | **Azure ACI** | 间接支持 | 间接支持 |
   | **GCP GKE** | 是 | 是 |
   | **GCP Cloud Run** | 是 | 间接支持 |
   | **GCP Cloud Functions** | 是 | 是 |
   | **GCP Cloud Scheduler** | 否 | 是 |
   | **IBM IKS** | 是 | 是 |
   | **IBM Code Engine** | 是 | 是 |
   | **OCI OKE** | 是 | 是 |
   | **OCI Functions** | 是 | 是 |
   | **OCI Container Instances** | 间接支持 | 间接支持 |
   | **DO DOKS** | 是 | 是 |
   | **DO App Platform** | 有限 | 是 |

5. **异步消息传递**
   - **目的**：让容器化 agents 或系统组件之间实现非阻塞、动态通信，非常适合并行或独立的任务处理。
   - **选择**：原型阶段使用 **[RabbitMQ](https://www.cloudamqp.com/plans.html#rmq)**。生产阶段使用 **[Kubernetes 上的 Kafka](https://www.redhat.com/en/topics/integration/why-run-apache-kafka-on-kubernetes)**。Kafka 是分布式流平台，针对高吞吐、容错消息传递进行了优化，可在复杂工作流中连接 agents。
   - **重要性**：异步消息传递可以解耦组件，增强韧性，并支持事件驱动架构。

6. **定时容器调用**
   - **目的**：容器既可以按需触发（通过 HTTP 请求），也可以按计划（通过类似 cron 的作业）触发，提供执行模式上的灵活性。
   - **选择**：我们会使用 [Dapr Scheduler](https://docs.dapr.io/concepts/dapr-services/scheduler/)。开发阶段还可以使用 Linux/Mac 上的 [python-crontab](https://pypi.org/project/python-crontab/)，Windows 上的 [APSchedule](https://pypi.org/project/APScheduler/)，或者适用于任意系统的进程内调度库 [Schedule](https://pypi.org/project/schedule/)。原型阶段我们使用 **[cron-job.org](https://cron-job.org/en/)** 这个免费的在线调度服务。生产阶段则使用与 Kubernetes 原生集成的 **[Kubernetes CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)**。Dapr 的最新更新中也提供了调度服务。
   - **重要性**：灵活的调用方式同时支持实时和批处理，能够高效适配多种场景。

7. **关系型托管数据库服务**
   - **目的**：关系型数据库提供结构化数据存储和 ACID 一致性，可靠地处理用户数据、agent 状态或日志。
   - **选择**：我们选择 **[CockroachDB](https://www.cockroachlabs.com/)**。CockroachDB 是兼容 Postgres 的分布式 SQL 数据库，旨在实现可扩展性和韧性，并提供托管服务以减少运维负担。为了便于切换数据库提供商，我们会实现抽象层，例如数据库 ORM，这里会使用 SQLModel。
   - **重要性**：它保证稳健的数据持久化，这对追踪工作流或维护系统完整性至关重要。

8. **内存型数据结构存储**
   - **目的**：可作为数据库、缓存和消息 broker 使用。由于数据存储在 RAM 中，因此性能极高。
   - **选择**：**[Upstash Redis](https://upstash.com/pricing)**。Upstash 提供无服务器 Redis，并有免费层。
   - **重要性**：因为数据存于内存，所以性能非常高，非常适合存储 LLM 会话数据。

9. **[分布式应用运行时（Dapr）](https://dapr.io/)**
   - **目的**：Dapr（Distributed Application Runtime）通过提供标准化构件，例如服务调用、状态管理、发布/订阅消息，来简化具韧性分布式系统的开发，特别适合 agentic 工作流。它抽象掉分布式计算的复杂性，使开发者能专注于构建智能、可扩展的 AI 方案，而不是与基础设施问题纠缠。
   - **选择**：我们选择 Dapr，是因为它轻量、语言无关，并且能与无状态 serverless Docker 容器和异步消息传递系统无缝集成。它支持多种编程语言和部署环境，同时符合我们减少预设构件、赋能自定义解决方案的极简理念。
   - **重要性**：在 agentic AI 生态中，agent 与服务之间的动态交互至关重要，Dapr 能在不增加过多开销的情况下保证可靠性和可扩展性。通过标准化 agent 的通信和状态管理，它可以加速开发、提升容错能力，并让架构面向未来更稳健，帮助我们在保持简单与性能的同时适应演进需求。你也可以选择使用 [Dapr Agents](https://dapr.github.io/dapr-agents/) 和 [Dapr Workflows](https://docs.dapr.io/developing-applications/building-blocks/workflow/workflow-overview/)。在本地以 self-hosted 模式运行 `dapr init` 时，Dapr 会默认启动一个 Redis 实例，用于某些功能，例如状态管理和 pub/sub 消息。

---

### 支撑 DACA 框架的两个核心构件

整个框架依赖两个关键构件，它们让原型验证和生产部署都成为可能：
- **事件驱动的容器调用**：由事件触发的容器，例如 HTTP 请求触发，实现实时响应。这是用户发起型工作流或 agent 交互的基础。
- **定时的容器调用**：按预定义计划（通过 cron 作业）执行的容器，支持批处理或周期性任务，为系统增加灵活性。它们也会被用于从 RabbitMQ 和 Kafka 中**拉取异步消息**。

这两个构件共同提供了处理几乎任何 agentic 工作流的灵活性，无论是动态触发还是定期执行，都适用于原型环境与生产环境。

---

### DACA 开发栈（本地）：开源

开发、原型和生产三套栈在所用工具和技术上是一样的，唯一差别在于部署方式。这样的统一开发方式确保开发者可以使用同一套技术栈在本地或云环境中构建和测试，并无缝过渡到原型或生产部署。
- **LLM APIs**：OpenAI Chat Completion（Google Gemini - 免费层）、Responses API
- **轻量级 Agents**：OpenAI Agents SDK（开源）
- **[模型上下文协议（MCP）](https://modelcontextprotocol.io/introduction)**：标准化 agentic 工具调用。
- **REST APIs**：FastAPI（开源）
- **无状态 Serverless Docker 容器**：Docker Desktop 和 Docker Compose（免费层且开源）
- **异步消息传递**：RabbitMQ Docker 镜像（开源）
- **定时容器调用**：开发阶段使用 Linux/Mac 上的 python-crontab，Windows 上的 APSchedule，或适用于任何系统的 Schedule。
- **关系型数据库**：Postgres Docker 镜像（开源）。为了便于切换数据库提供商，我们会实现抽象层，例如数据库 ORM，这里会使用 SQLModel（开源）。
- **内存型数据存储**：Redis Docker 镜像（开源）。在 Python 中可使用 redis-py，或更高层的 Redis OM Python（开源）。
- **在容器内开发**：Visual Studio Code Dev Containers 扩展（开源）
- **本地运行 Dapr**：通过 Docker Compose 运行（开源）。可选地，你也可以使用 [Dapr Agents](https://dapr.github.io/dapr-agents/) 和 [Dapr Workflows](https://docs.dapr.io/developing-applications/building-blocks/workflow/workflow-overview/)

**[Dapr 2025 年现状研究报告](https://pages.diagrid.io/download-the-state-of-dapr-2025-report)**

---

### DACA 原型栈：免费部署

原型栈旨在快速迭代，完全免费或使用免费层，利用低成本工具进行测试与验证。
- **LLM APIs**：与 OpenAI Chat Completion 兼容的 Google Gemini API，拥有慷慨的免费层，以及 Responses API
- **轻量级 Agents**：OpenAI Agents SDK
- **[模型上下文协议（MCP）](https://modelcontextprotocol.io/introduction)** Servers
- **REST APIs**：FastAPI
- **无状态 Serverless Docker 容器**：部署在 **[Hugging Face Docker Spaces](https://huggingface.co/docs/hub/en/spaces-sdks-docker)** 上的 Docker 容器（带内置 CI/CD 的免费托管）
- **异步消息传递**：RabbitMQ（免费层）
- **灵活的容器调用**：cron-job.org（完全免费的在线调度服务）
- **关系型托管数据库服务**：CockroachDB Serverless（免费层）。为了便于切换数据库提供商，我们会实现抽象层，例如数据库 ORM，这里会使用 SQLModel（开源）。
- **内存型数据存储**：[Upstash Redis](https://upstash.com/pricing)
- **Dapr**：把 Dapr 看作任意一个容器。`daprio/daprd` 镜像只是与你的应用并行部署的标准容器，也就是 Dapr Sidecar（开源）。可选地，你也可以使用 [Dapr Agents](https://dapr.github.io/dapr-agents/) 和 [Dapr Workflows](https://docs.dapr.io/developing-applications/building-blocks/workflow/workflow-overview/)
- **成本**：原型阶段完全免费，将开发中的财务门槛降到最低。

### DACA 的无服务器替代方案：适用于原型与生产

那些拥有信用卡并能注册 Azure 免费层的开发者，可以选择使用无服务器平台，这类平台本质上就是托管 Kubernetes，既可用于原型也可用于生产，例如 [Azure Container Apps（ACA）](https://azure.microsoft.com/en-us/products/container-apps)（支持 [Dapr](https://learn.microsoft.com/en-us/azure/container-apps/dapr-overview)）以及 [Azure Container Apps Jobs](https://learn.microsoft.com/en-us/azure/container-apps/jobs?tabs=azure-cli)。

他们可以从 [免费层](https://azure.microsoft.com/en-us/pricing/free-services) 开始：每月前 180,000 vCPU 秒、360,000 GiB/秒和 200 万次请求是免费的。

**DACA 真实示例**

想象一个运行在 ACA 上的 FastAPI 服务：

使用 0.5 vCPU 和 1 GB RAM，它通常每分钟可以稳定处理 50-100 个请求，具体取决于工作负载，例如数据库查询还是静态响应。

如果流量激增，ACA 的自动扩缩容可以拉起另一个 0.5 vCPU 副本，而不是超配一个完整 vCPU，从而降低成本。

---

### DACA 生产栈：云原生与开源

生产栈针对可扩展性、可靠性和性能进行了优化，使用企业级工具，同时保持与开发栈一致，差异只在部署方式。
- **LLM APIs**：任何兼容 OpenAI Chat Completion API 的 LLM（大多数都兼容），以及 Responses API
- **轻量级 Agents**：OpenAI Agents SDK
- **[模型上下文协议（MCP）](https://modelcontextprotocol.io/introduction)**：运行在无状态容器中
- **REST APIs**：FastAPI
- **无状态 Serverless Docker 容器**：由 **Kubernetes** 编排的 Docker 容器（用于自动扩缩容与韧性）
- **异步消息传递**：Kubernetes 上的 Kafka（多 broker、高可用）或 Kubernetes 上的 RabbitMQ
- **灵活的容器调用**：Kubernetes CronJob（与 Kubernetes 原生集成）；开发者需要从 cron-job.org 迁移到 Kubernetes CronJob
- **关系型托管数据库服务**：Kubernetes 上的 Postgres。为了便于切换数据库提供商，我们会实现抽象层，例如数据库 ORM，这里会使用 SQLModel（开源）。
- **内存型数据存储**：Kubernetes 上的 Redis
- **Kubernetes 上的 Dapr**：[在 Kubernetes 集群上部署 Dapr](https://docs.dapr.io/operations/hosting/kubernetes/)（开源）。可选地，你也可以使用 [Dapr Agents](https://dapr.github.io/dapr-agents/) 和 [Dapr Workflows](https://docs.dapr.io/developing-applications/building-blocks/workflow/workflow-overview/)

### DACA 的无服务器替代方案：适用于原型与生产

那些拥有信用卡并能注册 Azure 免费层的开发者，可以选择使用无服务器平台，这类平台本质上就是托管 Kubernetes，既可用于原型也可用于生产，例如 [Azure Container Apps（ACA）](https://azure.microsoft.com/en-us/products/container-apps)（支持 [Dapr](https://learn.microsoft.com/en-us/azure/container-apps/dapr-overview)）以及 [Azure Container Apps Jobs](https://learn.microsoft.com/en-us/azure/container-apps/jobs?tabs=azure-cli)。

他们可以从 [免费层](https://azure.microsoft.com/en-us/pricing/free-services) 开始：每月前 180,000 vCPU 秒、360,000 GiB/秒和 200 万次请求是免费的。

**DACA 真实示例**

想象一个运行在 ACA 上的 FastAPI 服务：

使用 0.5 vCPU 和 1 GB RAM，它通常每分钟可以稳定处理 50-100 个请求，具体取决于工作负载，例如数据库查询还是静态响应。

如果流量激增，ACA 的自动扩缩容可以拉起另一个 0.5 vCPU 副本，而不是超配一个完整 vCPU，从而降低成本。

---

### 为 DACA 生产部署培训开发者

为了让开发者具备用于生产部署的 Kubernetes DevOps 技能，我们利用 **Oracle Cloud Infrastructure（OCI）**，它提供“永久免费”层，包含 2 台 AMD VM（每台 1/8 OCPU，1 GB RAM）或最多 4 台 Arm VM（总计 24 GB RAM）。[这些 VM 被用来部署我们自己的 Kubernetes 集群](https://github.com/nce/oci-free-cloud-k8s)，为学习集群管理、扩缩容和部署提供实践环境。一旦开发者掌握这些技能，他们就可以自信地把我们的 agentic 工作流部署到任何云 Kubernetes 平台，例如 AWS、GCP、Azure，从而保证可移植性和灵活性。这种培训弥合了原型与生产之间的鸿沟，帮助开发者处理真实世界的部署。

参考：

https://www.ronilsonalves.com/articles/how-to-deploy-a-free-kubernetes-cluster-with-oracle-cloud-always-free-tier

https://medium.com/@Phoenixforge/a-weekend-project-with-k3s-and-oracle-cloud-free-tier-99eda1aa49a0

---

### 总结

这个 DACA 框架在简洁性与能力之间取得平衡，拥有统一的开发栈，既能适配免费原型（通过 Hugging Face Docker Spaces、cron-job.org），也能适配稳健的生产环境（通过 Kubernetes、OCI 训练过的 DevOps）。两个核心构件——事件驱动的容器调用和定时的容器调用——支撑了其灵活性，使其可以在任何环境中处理短期或长期工作流。

