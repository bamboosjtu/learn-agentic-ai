# 通过 OpenAI 桌面应用与 App 协作

[通过 App 协作：OpenAI 12 天发布活动，第 11 天](https://www.youtube.com/watch?v=g_qxoznfa7E)

## Warp：智能终端

[Warp](https://www.warp.dev/)

第一天就成为命令行高手。Warp 将 AI 与你的开发团队知识整合到一个快速、直观的终端中。

## Notion：共同构建完善文档

[Notion](https://www.notion.com/)

## VS Code：编程 IDE

[VS Code](https://code.visualstudio.com/)

“Work with Apps” 是 OpenAI 面向 macOS 推出的 ChatGPT 桌面应用功能（Windows 即将支持）。它允许 AI 直接与您电脑上的某些应用交互，从而增强其提供具备上下文感知能力的辅助效果。该功能对开发者尤其有价值，因为它使 ChatGPT 能够访问并分析受支持开发环境中的代码，进而提供更准确、更相关的回答。

## 工作原理

1. **支持的应用**

   在当前 Beta 阶段，“Work with Apps” 兼容多种开发工具，包括：

   - Xcode
   - Visual Studio Code（VS Code）
   - JetBrains IDE（例如 IntelliJ IDEA、PyCharm）
   - TextEdit
   - Terminal 和 iTerm2

2. **启用方式**

   若要使用此功能：

   - 确保 ChatGPT 的 macOS 应用已更新到最新版本。
   - 启动任一受支持的应用。
   - 在 ChatGPT 应用中，点击聊天栏中的“Work With Apps”按钮，并选择你希望接入的当前活动应用。

3. **交互方式**

   启用后，ChatGPT 可以访问所选应用中已打开的编辑器窗格或终端窗口内容。当你发送消息时，这些内容会作为上下文一并提供给 ChatGPT，使其能给出更具针对性和准确性的帮助。如果你高亮了特定文本，ChatGPT 会优先聚焦该选中内容，同时仍结合周边上下文进行理解。

4. **隐私与数据处理**

   从应用中访问到的内容会成为聊天记录的一部分，并存储在你的账户中，直到你选择删除。OpenAI 提供了数据控制选项，用于管理你的信息如何被使用和存储。

## 优势

- **增强辅助能力**：通过访问你编码环境中的实时数据，ChatGPT 可以提供更相关的代码建议、调试帮助和解释说明。
- **简化工作流**：这种集成减少了在不同应用之间复制粘贴代码的需要，使开发体验更加顺畅。

## 局限

- **只读访问**：目前，ChatGPT 可以读取受支持应用中的内容，但不能直接把修改写回这些应用。你仍需要手动落实它提供的建议。
- **应用支持有限**：该功能仍处于 Beta 阶段，目前支持的应用数量有限，主要集中在编程工具上。OpenAI 计划未来扩展到更多应用。
