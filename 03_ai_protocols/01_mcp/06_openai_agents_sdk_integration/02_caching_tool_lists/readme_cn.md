# 模块 2：在 OpenAI Agents SDK 中缓存 MCP 工具列表

## 介绍

当一个 Agent 与 MCP 服务器交互时，通常会调用 `list_tools()` 来发现可用工具。频繁调用，尤其是对远程服务器调用，会引入额外延迟。OpenAI Agents SDK 提供了一种缓存工具列表的方式，以提升性能。

本模块说明如何在 OpenAI Agents SDK 中使用 MCP server client 时启用并验证工具列表缓存，并引用官方 SDK 文档作为依据。

正如 [OpenAI Agents SDK MCP 文档](https://openai.github.io/openai-agents-python/mcp/) 所说：

> 每次 Agent 运行时，都会在 MCP 服务器上调用 `list_tools()`。这可能带来延迟开销，尤其当服务器是远程服务器时。要自动缓存工具列表，可以传入 `cache_tools_list=True`。


## 启用缓存

要启用工具列表缓存，直接在 MCP server client 的构造函数中传入布尔参数 `cache_tools_list=True`（例如 `MCPServerStreamableHttp`、`MCPServerStdio` 或 `MCPServerSse`）。

```python
    async with MCPServerStreamableHttp(params=mcp_params_cached, name="CachedClient", cache_tools_list=True)
```

如果你想让缓存失效，可以在 server 对象上调用 `invalidate_tools_cache()`。


## 如何验证缓存行为

**服务端日志**：验证缓存是否生效，最可靠的方法是查看 MCP 服务器日志。当客户端缓存启用后，对于同一个客户端实例重复调用 `list_tools()`，服务器收到的 `ListToolsRequest` 消息应该会明显减少。

## 示例说明（`agent_connect_cache/agent_tool_caching.py`）

`agent_tool_caching.py` 脚本（位于本模块的 `agent_connect_cache` 子目录下，与你当前工作版本一致）演示了 `MCPServerStreamableHttp` 的缓存行为。

它会初始化一个 `MCPServerStreamableHttp` 客户端，并设置 `cache_tools_list=True`，然后多次调用 `list_tools()`。通过观察服务器日志，你可以确认：虽然客户端调用了多次 `list_tools()`，但服务器真正处理 `ListToolsRequest` 的次数要少得多。

### 运行示例

1. **确保共享 MCP 服务器已经启动：**
   客户端脚本会连接某个 URL（例如 `http://localhost:8001/mcp`）。请先确保你的服务器在对应地址运行。
   例如，在 `07_openai_agents_sdk_integration/` 目录中可以执行：

    ```bash
    uv run python shared_mcp_server/server.py
    ```

2. **运行缓存脚本：**
   进入 `05_ai_protocols/01_mcp/07_openai_agents_sdk_integration/02_caching_tool_lists/agent_connect_cache/` 目录（或者你实际放置 `agent_tool_caching.py` 的目录），执行：

    ```bash
    uv run python agent_tool_caching.py
    ```

3. **观察服务端日志：**
   注意服务器记录 `ListToolsRequest`（或类似日志）的次数。开启 `cache_tools_list=True` 后，对于客户端的重复调用，这个次数应该非常少。

本模块结合官方文档和你的实践结果，澄清了如何启用并验证工具列表缓存。
