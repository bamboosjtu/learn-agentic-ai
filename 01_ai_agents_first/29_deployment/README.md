# 第 28 阶段：部署你的第一个 Agent

到这里，你已经构建过 Python agent，并用 Chainlit 运行过它们。本阶段会教你如何把这个 agent 分享给别人使用。课程步骤都比较短，并且会重复使用同一个简单友好的 Chainlit 应用，这样你可以把注意力集中在新的部署概念上。

## 学习路径

```
28_deployment/
├── 01_prepare_app/         # 为分享清理和整理 Chainlit 应用
├── 02_huggingface_spaces/  # 通过免费托管平台点击式部署
├── 03_docker_basics/       # 理解容器，并让应用可在任何地方运行
└── 04_cicd_auto_deploy/    # 每次 push 后让 GitHub 自动重新部署
```

建议按顺序完成，每一步都比较短，并建立在前一步基础上。

### 第 1 阶段：准备应用

- 以更安全的方式配置 `.env` 和 secrets
- 添加简单 health check 和基础日志
- 用 `uv` 锁定 Python 依赖

### 第 2 阶段：Hugging Face Spaces

- 用网页界面创建一个新的 Space
- 上传 Space 所需的三个文件
- 把 API key 保存为 secret，而不是写进代码

### 第 3 阶段：Docker 基础

- 用通俗语言理解 image 和 container
- 在 Docker 里运行同一个 Chainlit 应用
- 准备好后把 image 推送到 Render 或 Railway

### 第 4 阶段：CI/CD 自动部署

- 复制一个简单友好的 GitHub Actions workflow
- 在你 push 到 `main` 后自动构建并部署
- 学会快速识别常见错误及其修复方式

## 如何使用这个模块

- 逐个阅读每个 README
- 把示例代码拷贝到你自己的项目中
- 每次改动后先在本地测试
- 只有本地通过后再部署

## 完成之后

- 尝试把 agent 放进 MCP server 中托管
- 在后续模块里加入 tracing、analytics 或 queue
- 让 agent 服务更多渠道（Slack、语音等）

部署本质上只是把你已经做好的 agent 分享出去的另一种方式。
