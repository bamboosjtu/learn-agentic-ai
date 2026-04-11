# MCP Prompt

MCP 服务器也可以提供 prompts，用来动态生成 agent 的 instructions。这样你就可以创建可复用的 instruction 模板，并通过参数进行定制。

支持 prompts 的 MCP 服务器会提供两个关键方法：
- `list_prompts()`：列出服务器上所有可用的 prompt
- `get_prompt(name, arguments)`：获取某个指定 prompt，并可传入可选参数

这个示例使用的是本地 MCP prompt server，代码位于 [server.py](server.py)。

运行示例：

1. 启动 MCP Server

```bash
uv run python server.py
```

2. 启动 Agent
```bash
uv run python main.py
```

## 细节说明

这一节使用的是 MCP prompt，它能根据用户控制的参数来生成 agent instructions。MCP server 会暴露类似 `generate_code_review_instructions` 这样的 prompt，它接收关注领域和编程语言等参数。Agent 会调用这些 prompt，根据用户提供的参数动态生成自己的 system instructions。

## 工作流程

本示例展示了两个关键函数：

1. **`show_available_prompts`**
   列出 MCP server 上所有可用的 prompts，让用户知道可以选择哪些 prompt。这体现了 MCP prompts 的“发现能力”。

2. **`demo_code_review`**
   展示完整的“用户控制 prompt”工作流：
   - 用指定参数调用 `generate_code_review_instructions`（关注点：`"security vulnerabilities"`，语言：`"python"`）
   - 使用生成的 instructions 创建一个具备特定代码审查能力的 Agent
   - 让 agent 对存在漏洞的示例代码进行分析（通过 `os.system` 触发命令注入）
   - Agent 利用可用工具分析代码，并给出偏向安全角度的反馈

这种模式允许用户通过 MCP prompts 来动态配置 agent 行为，而不是把 instructions 硬编码在程序里。
