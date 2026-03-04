# 第 2 阶段：部署到 Hugging Face Spaces

现在我们要把同一个 Chainlit agent 分享给更多人使用。Hugging Face Spaces 免费、友好，而且直接在浏览器中运行。按步骤操作时，把这个目录保持打开状态会更方便。

## 开始之前

- 先完成第 1 阶段，并确保应用已经能在本地运行
- 在 https://huggingface.co/join 创建一个免费的 Hugging Face 账号
- 如果你想以后从终端推送代码，可以安装 `git`（可选）

---

## 第 1 步：创建一个新的 Space

1. 打开 https://huggingface.co/spaces
2. 点击 **Create New Space**
3. 设置名称，把 **Space SDK** 选为 **Docker**（Chainlit 最适合），然后选择 **Public** 或 **Private**
4. 点击 **Create Space**

页面创建好后，会等待你上传文件。

---

## 第 2 步：上传项目文件

你只需要上传这个目录中的 3 个文件：

- `main.py`
- `requirements.txt`
- `chainlit.md`

把它们拖进文件区域，或者使用 **Upload files** 按钮。上传完成后，Space 会自动开始构建。

---

## 第 3 步：添加 Secret Key

1. 在 Space 页面点击 **Settings**
2. 进入 **Secrets**
3. 添加一个新的 secret：
   - 名称：`OPENAI_API_KEY`
   - 值：你的真实 key（通常以 `sk-` 开头）
4. 点击 **Add secret**

Space 会在加入 secret 后自动重启。

---

## 第 4 步：测试线上应用

- 等构建日志出现 `App running on port 7860`
- 点击 **App** 标签页
- 与 agent 对话，确认回答和本地运行时一致

如果报错，打开 **Logs** 查看。最常见的问题是 secret 缺失或 `requirements.txt` 拼写错误。

---

## 可选：使用 `git` 更新

Spaces 本质上也是普通 git 仓库。你可以克隆 Space 提供的仓库地址，把文件放进去，之后通过以下命令更新：

```bash
git add .
git commit -m "Deploy Chainlit app"
git push
```

每次你 push 后，Hugging Face 都会自动重新构建这个 Space。

---

## 完成之后

现在你已经有一个可以分享的在线 URL 了。记下这个链接，并继续妥善保管你的 API key。接下来可以进入第 3 阶段，学习如何使用 Docker 运行同一个应用。
