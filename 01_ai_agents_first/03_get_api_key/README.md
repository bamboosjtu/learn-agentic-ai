# 如何获取 OpenAI API Key 和 Gemini API Key

如果你想在项目中使用 OpenAI 或 Google Gemini 的 AI 服务，你需要分别从两个服务商获取 API Key。下面是分步指南。

---

## 1. 获取 OpenAI API Key

**OpenAI 通过 API 提供 GPT-4、GPT-4o-mini 等模型能力。**

### 步骤：

1. **注册或登录：**

   * 打开 [OpenAI Platform](https://platform.openai.com/)。
   * 注册一个免费账号，或直接登录已有账号。

2. **进入 API Keys 页面：**

   * 登录后，进入设置按钮。
   * 选择 “API keys”，或直接访问 [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)。
   
3. **创建新的 API Key：**

   * 点击 **+ Create new secret key** 按钮。
   * 如果有提示，给你的 key 起一个名称（便于自己识别）。
   * 复制生成的 key，并**妥善保存**。你之后将无法再次查看完整 key。

**注意：**

* 若要更高使用额度，你可能需要绑定支付信息。
* 请保持 API Key 私密，不要暴露在公开仓库中。

---

## 2. 获取 Gemini API Key（Google Generative AI）

**Google Gemini（此前也被称作 Bard 或 Generative Language API）是 Google 的大模型家族。**

### 步骤：

1. **进入 Google AI Studio：**

   * 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)。

2. **使用 Google 账号登录：**

   * 用你的 Google 账号登录。

3. **创建 Gemini API Key：**

   * 在 API keys 页面，点击 **Create API key**。
   * 选择默认项目。
   * 点击按钮生成 API key。
   * 复制你的 key，你的应用会用到它。
   
4. **启用计费（如有提示）：**

   * 若要更高配额或用于生产环境，你可能需要启用计费。按 Google Cloud Console 的提示操作即可。

**注意：**

* Gemini API Key 同样需要严格保密。
* 更多细节请参考 Google 官方[文档](https://ai.google.dev/gemini-api/docs/quickstart)。

---

## 安全提醒

* **不要公开分享你的 API Key。**
* 使用环境变量或密钥管理服务来安全管理 key。

---

## 快速参考表

| Provider      | Website                                                                          | API Key Link                                                                     |
| ------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| OpenAI        | [https://platform.openai.com/](https://platform.openai.com/)                     | [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)     |
| Google Gemini | [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) | [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) |

---

如果你遇到问题，可参考 [OpenAI 文档](https://platform.openai.com/docs/) 或 [Google Gemini 文档](https://ai.google.dev/gemini-api/docs/quickstart)。

---
