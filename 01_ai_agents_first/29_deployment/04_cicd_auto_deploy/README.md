# 第 4 阶段：使用 GitHub Actions 自动部署

把重复工作交给 GitHub。这个阶段你会搭建一个简单流水线：构建 Docker 镜像、推送到 Docker Hub，并通知 Render（或其他宿主平台）拉取最新版本重新部署。

## 用最直白的话理解

- 你把代码推送到 `main` 分支
- GitHub 自动帮你构建容器
- GitHub 把镜像推送到 Docker Hub
- GitHub 再通知你的部署平台进行重部署

完成首次设置后，你基本不需要再点任何按钮。

---

## 你需要先准备好

1. 一个已经包含项目代码的 GitHub 仓库
2. 一个 Docker Hub 账号，以及一个空仓库用来接收镜像
3. 一个基于这个镜像创建好的 Render（或 Railway）服务，并拿到 deploy hook URL

---

## 第 1 步：复制 Workflow

把本目录中的 `deploy.yml` 放到你项目里的 `.github/workflows/deploy.yml`。GitHub 只会识别这个固定路径。

```bash
mkdir -p .github/workflows
cp 04_cicd_auto_deploy/deploy.yml .github/workflows/deploy.yml
```

如果你的应用不在默认目录下，记得修改 workflow 中的 `context` 路径。

准备好后，把这个文件提交到仓库。

---

## 第 2 步：添加 GitHub Secrets

打开 GitHub 仓库，进入 **Settings -> Secrets and variables -> Actions**，添加以下 secrets：

| Secret Name | Value |
| -------------------- | --------------------------------------------------------------------------------- |
| `DOCKERHUB_USERNAME` | 你的 Docker Hub 用户名 |
| `DOCKERHUB_TOKEN` | Docker Hub 的个人访问令牌 |
| `RENDER_DEPLOY_HOOK` | Render 提供的完整 deploy hook URL（如果只推 Docker Hub 可留空） |

你的 OpenAI key 应保留在部署平台自身（Render secret、Hugging Face secret 等），不应该放进 GitHub。

---

## 第 3 步：推送到 `main`

当 secrets 设置完成后，向 `main` 分支推送一次 commit。GitHub 会自动启动 workflow。你可以在 **Actions** 标签页查看执行过程。

每次运行会：

1. 使用 `03_docker_basics` 中的文件构建 Docker 镜像
2. 把镜像以 `latest` 标签推送到 Docker Hub
3. 触发 deploy hook

Render 会自动拉取新镜像、重建并重启服务。

---

## 第 4 步：检查结果

- 打开 Render 仪表盘查看新的部署记录
- 打开线上 URL 测试 agent
- 如果失败，查看 GitHub Actions 日志，它会明确告诉你出错步骤

---

## 额外想法

- 在构建前先加一段自动测试 job
- 通过修改分支过滤器，为 staging 环境单独部署
- 把 Render 换成任何支持 webhook 的平台

完成后，你以后只需要一次 `git push`，就能让线上 agent 自动保持最新。
