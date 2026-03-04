# 使用 Render 部署

[Render Docs](https://render.com/docs/your-first-deploy)

## Render 部署指南（一步一步）

### 前置条件

开始之前，请确认你已经具备：

* 一个 **GitHub 账号**
* 已经推送到 **公开 GitHub 仓库** 的项目代码
* 一个像 `main.py` 这样的入口文件
* 一个列出依赖的 `pyproject.toml`
* 一个本地可运行的启动命令，例如：

  ```bash
  uv run chainlit run main.py
  ```

---

## 第 1 步：注册或登录

1. 打开 [Render.com](https://render.com)
2. 点击 **Sign Up**（或 **Log In**）
3. 使用 **GitHub** 登录（推荐）

---

## 第 2 步：创建新的 Web Service

1. 在仪表盘中点击 **New -> Web Service**
2. 选择 **Git Provider** 标签
3. 如果你看不到仓库，点击 **Reconnect GitHub -> Grant full repo access**
4. 选择你要部署的仓库

---

## 第 3 步：填写基础信息

Render 会要求你填写以下设置：

| 字段 | 填写内容 |
| ------------------ | ------------------------------------------------------------------------------------ |
| **Branch** | `main` |
| **Root Directory** | 留空（除非应用在子目录里） |
| **Build Command** | `pip install uv && uv sync` |
| **Start Command** | `uv run chainlit run main.py --host 0.0.0.0 --port $PORT` |
| **Instance Type** | 选择 **Free (512 MB RAM)** |

---

## 第 4 步：设置环境变量（如果需要）

如果应用依赖 API keys 或其他 secrets：

1. 滚动到 **Environment Variables** 区域
2. 添加变量，例如：

   ```
   OPENAI_API_KEY = your_api_key_here
   OPENAI_VECTOR_STORE_ID = your_api_key_here
   ```
3. 后续你也可以随时继续添加或修改

---

## 第 5 步：点击 “Deploy Web Service”

Render 会自动：

* 克隆你的 GitHub 仓库
* 安装依赖（`uv sync` 或 `pip install`）
* 按启动命令运行应用

你可以在部署过程中看到实时日志。

---

## 第 6 步：查看日志

* 等待类似下面的日志：

  ```
  ==> Running 'uv run chainlit run main.py --host 0.0.0.0 --port $PORT'
  ==> Your service is live
  ```
* 如果失败了，Render 会显示完整错误日志，便于排查。

---

## 第 7 步：访问你的应用

当你看到 **Live** 状态后，点击生成出来的 Render URL，例如：

```
https://your-app-name.onrender.com
```

现在你的 Chainlit 或 Python 应用已经在线运行了。

---

## 第 8 步：更新后重新部署

每次你向同一个 GitHub 分支（`main`）推送新代码时，
Render 都会自动检测并重新部署。

---

## 可选第 9 步：排错建议

| 问题 | 解决方法 |
| ------------------------- | -------------------------------------------------------------------- |
| `No pyproject.toml found` | 确认仓库根目录有它，或正确设置 **Root Directory** |
| 仓库不可见 | 重新连接 GitHub 并授予完整访问权限 |
| 应用无法启动 | 确保启动命令包含 `$PORT` 且使用 `--host 0.0.0.0` |
| 启动较慢 | 免费实例空闲 15 分钟后会休眠，访问时会自动唤醒 |
