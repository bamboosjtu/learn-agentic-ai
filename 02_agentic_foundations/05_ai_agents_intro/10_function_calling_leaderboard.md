# Function Calling 排行榜

**Function-Calling Leaderboards** 是一类用于评估和排名大语言模型（LLM）“调用外部函数 / 工具能力”的平台。这种能力让 LLM 不再局限于文本生成，还可以执行代码、访问数据库、或与 API 交互。对于那些需要接入外部系统的真实应用场景来说，评估模型的 function calling 能力非常重要。

**Berkeley Function-Calling Leaderboard（BFCL）：**

其中一个知名例子是 **[Berkeley Function-Calling Leaderboard (BFCL)](https://gorilla.cs.berkeley.edu/leaderboard.html)**，它由加州大学伯克利分校的研究者开发。BFCL 从多个维度全面评估 LLM 的 function calling 能力，包括：

- **简单函数调用**：评估模型是否能正确执行基础函数调用。
- **多函数调用**：评估模型在连续调用多个函数时的表现。
- **并行函数调用**：测试模型能否处理并发函数执行。
- **函数相关性检测**：评估模型能否为具体任务识别出合适的函数。

该排行榜使用了一个多样化数据集，其中包含 Python、Java、JavaScript、SQL 等多种编程语言的函数，以保证对模型多样性和适应性的充分评估。

**在 Agentic AI 崛起中的意义：**

Function calling 能力是 **Agentic AI** 发展的关键部分。具备良好 function calling 能力的 LLM 可以：

- **获取最新信息**：从外部数据源检索当前信息，使回答建立在最新数据基础上。
- **执行复杂操作**：完成超出模型原生能力范围的计算或流程。
- **接入外部系统**：无缝连接其他软件与服务，扩展应用范围。

因此，像 BFCL 这样的排行榜对于推动 Agentic AI 发展至关重要，因为它们帮助我们验证模型是否能有效且安全地执行这类外部交互任务。

**如何选择合适的排行榜：**

虽然目前可能存在多个 function calling 排行榜，但 **Berkeley Function-Calling Leaderboard** 因其全面的评测框架和丰富的数据集而最广为认可。对于希望 benchmark 或提升模型 function calling 能力的研究者和开发者而言，它是非常有价值的参考资源。

总之，function calling 排行榜在评估和推动 LLM 能力发展方面扮演着关键角色，尤其是在 Agentic AI 语境中。通过结构化评测，这些平台帮助我们构建出能够更自主、更有效地与外部系统交互的模型，从而扩展 AI 可以完成的任务范围。

