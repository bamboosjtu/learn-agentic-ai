# 在 Google Colab 中打开

<https://colab.research.google.com/drive/18owxL5MyPPlmp4IqfveN1JOSCYQ4GFnu?usp=sharing>

OpenAI Agents SDK 提供了一个稳健的框架，用于把各种工具集成到 Agent 中，使它们能够执行数据检索、网页搜索、代码执行等任务。下面是关于工具集成的一些关键点概览。

## 工具类型

1. **托管工具（Hosted Tools）**：这些是运行在 OpenAI 服务器上的预构建工具，可通过 `OpenAIResponsesModel` 访问。示例包括：
   - **WebSearchTool**：让 Agent 执行网页搜索。
     - **在 Colab 中试用：** [File Search Tool Example](https://colab.research.google.com/drive/1oygnLgbo9d49ClrWViVwrfBd2NDlxC9s?usp=sharing#scrollTo=g4JFNl0q1Clw&uniqifier=1)
   - **FileSearchTool**：允许从 OpenAI Vector Stores 中检索信息。
     - **在 Colab 中试用：** [Computer Tool Example](https://colab.research.google.com/drive/1oygnLgbo9d49ClrWViVwrfBd2NDlxC9s?usp=sharing#scrollTo=gXWTut66yXoa&uniqifier=1)
   - **ComputerTool**：用于自动化计算机上的任务。
     - 我们将使用 `model=computer-use-preview-2025-03-11`
     - 注意：模型 `computer-use-preview` 当前不可用。

2. **函数调用（Function Calling）**：这个能力允许 Agent 把任意 Python 函数当作工具使用，从而提升它们的通用性。

3. **Agent 作为工具（Agents as Tools）**：Agent 可以把其他 Agent 当作工具使用，从而支持分层任务管理，而无需直接转移控制权。

## 工具实现

- **函数工具（Function Tools）**：通过给 Python 函数添加 `@function_tool` 装饰器，可以很自然地把它们集成为 Agent 的工具。

## 工具执行流程

- 在 Agent 运行过程中，如果响应中识别到了工具调用，SDK 会处理该工具调用，把工具返回结果追加到消息历史中，然后继续循环，直到产生最终输出。

## 错误处理

- SDK 提供了优雅的错误处理机制，使 Agent 能够从工具相关错误中恢复，并继续完成任务。

如果你想更系统地理解和实现这些能力，可以参考 [tools documentation](https://github.com/openai/openai-agents-python/blob/main/docs/tools.md)。

## 用于下一代 AI Agent 开发的 LLM 新兴能力

在大语言模型中，函数调用，也常被称为 tool calling，是一个很强的特性。它让 AI Agent 可以与外部系统交互、执行任务，并把能力扩展到纯文本生成之外。这项能力已经成为 AI Agent 开发的基础组成部分，使 LLM 能够执行结构化动作，例如查询数据库、调用 API 或控制设备。

不过，AI Agent 开发正在快速演进，许多即将出现或已经显现的能力和趋势，预计会进一步增强这一领域。下面列出一些重要的发展方向，并重点说明它们和 AI Agent 开发的关系。

### 1. 更强的推理与规划能力

AI Agent 开发中最有前景的方向之一，是提升 LLM 自主推理和规划的能力。当前的函数调用机制允许 Agent 执行预定义工具，但未来的增强版可能会让 LLM 在推理过程中动态决定何时、如何使用工具。例如：

- **推理过程中的动态工具调用**：想象一个 LLM 在推理中途暂停，意识到需要外部数据后主动调用工具，比如网页搜索或计算器，然后把结果整合进当前推理，再继续往下思考，而且这一切不需要显式提示。这会让 Agent 更主动、更具适应性，这对复杂任务执行非常关键。
- **多步骤规划**：像 OpenAI `o1` 系列这类模型的发展表明，LLM 未来可能会把复杂目标拆解为详细、可执行的步骤，并按顺序编排多个工具调用。这对处理旅行预订、库存管理之类工作流型任务的 Agent 非常重要。

### 2. 记忆管理与上下文持久化

高效的 AI Agent 需要记住过去的交互，并在长任务中维持上下文。这个方向上的潜在新能力包括：

- **长期记忆**：除了短期上下文窗口之外，LLM 正在逐步结合持久化记忆系统，例如向量数据库或情节记忆模块，让 Agent 可以回忆过去的相关操作、用户偏好或环境状态。这对于持续性任务很重要，比如客服或项目管理。
- **记忆综合**：一些研究方向表明，Agent 可以从过去的交互中提炼高层洞察，比如总结用户行为模式，从而支持更个性化、更高效的决策。

### 3. 多 Agent 编排

AI Agent 的未来很大程度上依赖协作，也就是多个专长不同的 Agent 在一个 LLM 编排者之下共同工作。相关的新趋势包括：

- **Agent 交接与协作**：像 OpenAI Agents SDK、CrewAI 和 LangGraph 这类框架已经在探索多 Agent 系统，而未来的增强能力可能会让 handoff 更标准化，例如一个 Agent 把任务传递给另一个 Agent，同时提升实时协作能力。举例来说，一个 LLM 可能会统筹一个 Agent 团队，其中一个负责调研，一个负责执行，一个负责验证，从而简化复杂流程。
- **基于角色的专长分工**：LLM 可能会根据任务需求动态给子 Agent 分配角色，利用它们广泛的知识面来优化整体工作流。

### 4. 与外部系统的集成进一步扩展，而不止于 API

虽然当前的函数调用主要聚焦 API 交互，但未来可能会进一步扩展：

- **直接与环境交互**：Agent 可能不仅依赖 API，而是直接与物理系统，例如物联网设备，或数字平台，例如 GUI 界面，进行交互。比如，Large Action Models（LAM）正在作为 LLM 的一种演进方向出现，它们能够理解并操作真实世界中的界面来执行任务。
- **自主创建工具**：未来的 LLM 可能不再只依赖预先定义好的工具，而是能够根据具体任务即时生成自定义函数或脚本，从而提升 Agent 开发的灵活性。

### 5. 护栏与安全机制

随着 Agent 的自主性越来越强，确保其行为安全且合乎伦理就变得非常重要。未来可能出现的能力包括：

- **内建护栏**：LLM 可能会自带原生约束机制，用于阻止有害行为，比如拒绝不合规的工具调用，或根据安全标准校验输出。这对企业级 Agent 特别重要。
- **Tracing 与可解释性**：更强的 tracing 能力，比如记录 Agent 的决策过程，将帮助开发者调试和优化 Agent 行为，使其在关键应用场景中更可靠。

### 6. 与强化学习结合

将 LLM 与强化学习（RL）结合，是一个可能显著增强 AI Agent 能力的发展方向：

- **实时适应**：Agent 可以根据环境反馈不断优化自己的策略，逐渐学会更优的工具使用方式或任务执行路径。比如，一个 Agent 可以通过试错不断提升排程效率。
- **目标驱动行为**：强化学习可以让 Agent 追求更抽象的目标，例如“最大化用户满意度”，并据此动态调整行动和工具调用，而不是只执行静态指令。

### 7. 多模态能力

随着 LLM 演进为多模态模型，例如 GPT-4o，Agent 将获得新的能力：

- **视觉与音频集成**：Agent 可以处理图像、视频或语音输入，以辅助工具调用。例如分析一张照片来订购替换零件，或者转录会议内容后自动安排后续事项。
- **跨模态推理**：Agent 可能同时结合文本、图像和结构化数据来执行更具上下文感知能力的任务，例如根据扫描文档和数据库查询结果自动生成报告。

### 8. 低代码 Agent 开发工具

为了让更多人能创建 AI Agent，未来的框架和 SDK，例如 OpenAI 的 Agents SDK，可能会提供：

- **更简化的工具标注方式**：延续当前函数调用的发展方向，未来系统可能允许开发者用更少代码来定义工具，甚至直接使用自然语言描述或基于 UI 的界面来完成。
- **预构建的 Agent 模板**：为常见 Agent 类型，例如客服、研究或自动化，提供标准化模板，从而加速开发，并内置工具使用和工作流设计的最佳实践。

### 为什么这些方向对 AI Agent 开发重要

这些能力旨在解决当前基于 LLM 的 Agent 的一些关键限制，例如自主性不足、上下文感知能力有限，以及对外部预定义流程的依赖。

注：原始 `README.md` 内容在这里结束，而且源文本最后一句本身是不完整的。下面的章节是本地追加的说明。

---

## Appendix: 本目录内容总结

这个目录是一个 **OpenAI Agents SDK + Playwright + ComputerTool** 的实验示例，重点不是讲通用 Web 自动化，而是演示如何让 Agent 通过“computer use”能力直接操作浏览器。

你可以把它理解成一组最小化样例，用来回答下面几个问题：

- OpenAI Agents SDK 里的 `ComputerTool` 是怎么接入的
- Agent 如何通过截图、点击、输入、滚动来完成网页任务
- 本地浏览器如何包装成 SDK 可调用的“电脑”
- computer use 和普通 function calling 有什么区别

### 这个目录里各文件的作用

- `README.md`
  介绍工具集成、computer use、以及 Agent 开发相关的扩展方向。

- `computer.py`
  本目录最核心的代码文件。它把本地 Playwright 浏览器包装成一个 `AsyncComputer`，再交给 `ComputerTool`，让 Agent 具备“操作浏览器”的能力。

- `tools_openai_agents_sdk.ipynb`
  更偏教学和实验的 Notebook 版本，适合边运行边观察。

- `pyproject.toml` / `uv.lock`
  用来管理依赖和运行环境。

- `.env_example`
  环境变量示例。

### 这一节示例的学习重点

这个目录最值得学的不是某个具体 API，而是下面这套结构：

1. 定义一个 Agent
2. 给 Agent 挂上 `ComputerTool`
3. 实现一个本地 `AsyncComputer`
4. 把模型输出的动作翻译为真实浏览器操作
5. 让 Agent 根据截图和环境反馈不断迭代，直到完成任务

也就是说，这个目录展示的是 **模型驱动的浏览器操作**，而不是传统脚本驱动的浏览器自动化。

---

## `computer.py` 代码讲解

`computer.py` 的作用，是把 **OpenAI Agents SDK 的 `ComputerTool`** 接到 **本地 Playwright 浏览器** 上，让模型像“操作电脑”一样点网页、输入文字、滚动页面，再完成用户任务。

### 整体结构

这份代码主要分成三部分：

1. `main()`
   创建 Agent，挂载 `ComputerTool`，然后运行任务。

2. `CUA_KEY_TO_PLAYWRIGHT_KEY`
   把 computer use 使用的按键名字映射成 Playwright 可识别的按键名。

3. `LocalPlaywrightComputer`
   继承 `AsyncComputer`，把本地浏览器实现成 SDK 可调用的“电脑”。

### `main()` 在做什么

`main()` 是程序入口，流程很短，但很关键：

- 启动一个 `LocalPlaywrightComputer`
- 开启一次 tracing
- 创建 Agent
- 给 Agent 配上 `ComputerTool(computer)`
- 指定 computer use 模型 `computer-use-preview-2025-03-11`
- 调用 `Runner.run(...)` 让 Agent 去执行任务

这里的任务是：

```python
"Search for SF sports news and summarize."
```

也就是说，代码不是手写“打开网页 -> 搜索 -> 摘要”的固定流程，而是只给 Agent 一个目标，由模型自己决定下一步如何操作浏览器。

### `ComputerTool` 的作用

`ComputerTool(computer)` 是桥梁：

- `Agent` 负责理解任务和决定动作
- `ComputerTool` 把这些动作转成对“电脑”的调用
- `LocalPlaywrightComputer` 再把这些调用变成真实的浏览器操作

所以，这三者组合起来形成了一个闭环：

**用户目标 -> Agent 决策 -> ComputerTool 调用 -> 浏览器执行 -> 截图反馈 -> Agent 继续决策**

### `LocalPlaywrightComputer` 的核心作用

这个类继承了 `AsyncComputer`，本质是在实现一套“Agent 能调用的电脑接口”。

它定义了：

- 浏览器怎么启动
- 页面初始打开到哪里
- 如何截图
- 如何点击
- 如何输入
- 如何滚动
- 如何按键
- 如何拖拽

也就是说，这个类是 SDK 和本地浏览器之间的适配层。

### 浏览器是怎么启动的

在 `_get_browser_and_page()` 里，代码会：

- 按 `dimensions` 指定的大小启动 Chromium
- 使用 `headless=False` 打开可视浏览器
- 设置视口大小
- 默认打开 `https://www.bing.com`

所以 Agent 一开始看到的界面就是 Bing 首页。

### 模型怎么“看见屏幕”

靠 `screenshot()` 方法。

这个方法会：

- 对当前浏览器视口截图
- 把图片转成 base64 字符串返回

模型并不是直接读取 DOM，而更像是根据当前屏幕截图来判断下一步该做什么。这也是 computer use 和传统 API 驱动工具一个很大的区别。

### 模型怎么“操作电脑”

`LocalPlaywrightComputer` 实现了一组基础动作：

- `click(x, y, button)`
- `double_click(x, y)`
- `scroll(x, y, scroll_x, scroll_y)`
- `type(text)`
- `wait()`
- `move(x, y)`
- `keypress(keys)`
- `drag(path)`

这些动作会被 `ComputerTool` 调用，最终通过 Playwright 的 `mouse` 和 `keyboard` API 真正执行。

### 为什么需要按键映射

`CUA_KEY_TO_PLAYWRIGHT_KEY` 的存在，是因为模型或 computer use 协议里使用的按键名字，和 Playwright 需要的名字不完全一样。

例如：

- `cmd` 要映射成 `Meta`
- `ctrl` 要映射成 `Control`
- `arrowdown` 要映射成 `ArrowDown`

所以 `keypress()` 会先做映射，再调用：

- `keyboard.down(...)`
- `keyboard.up(...)`

如果没有这个映射层，很多快捷键动作会执行失败。

### 为什么要设置 `truncation="auto"`

在 Agent 创建时，代码显式设置了：

```python
model_settings=ModelSettings(truncation="auto")
```

这是因为 computer use 场景会不断产生截图和中间状态，上下文很容易迅速膨胀。设置自动截断可以降低上下文超限的风险。

### 这份代码真正展示了什么

这份代码展示的不是传统 Playwright 自动化，而是 **Agentic browser automation**：

- 传统 Playwright：开发者自己写死每一步怎么做
- 这里的代码：开发者只给目标，模型根据界面和反馈自己探索操作路径

也正因为如此，这种方式更灵活，但也更依赖模型能力、更消耗 token，也更容易受页面布局变化影响。

### 这份示例的局限

这只是一个演示性质的最小示例，真实项目里通常还需要补上这些能力：

- 超时控制
- 重试机制
- 失败恢复
- 更细粒度的日志和 tracing
- 对可访问网站或动作的限制
- 更稳定的页面状态判断
- 更严格的安全边界

### 一句话总结

`computer.py` 的本质，是把本地浏览器包装成一个可被 Agent 调用的“电脑”，从而让模型通过截图理解界面、通过鼠标键盘操作页面，最终完成真实的浏览器任务。
