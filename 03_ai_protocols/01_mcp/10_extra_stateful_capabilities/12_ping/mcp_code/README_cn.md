# MCP Ping Utility - 代码实现

本目录包含完整的 MCP ping utility 实现，包括 server 与 client 代码。

## 🚀 快速开始

### 1. 启动 Server
```bash
uv run server.py
```

### 2. 使用 Client 测试
```bash
# Run all ping tests
uv run client.py
```

## 📁 文件

- `server.py` - 带 ping utility 的 FastMCP server
- `client.py` - 功能完整的 ping 测试 client
- `pyproject.toml` - UV 项目配置

## 🏓 你将学到什么

1. **基础 Ping 实现** - 按照 MCP 规范实现
2. **连接健康监控** - 实用的 ping 模式
3. **超时处理** - 更健壮的错误处理
4. **性能测试** - 验证 server 的响应能力

## 📚 参考资料

- [MCP Ping Specification](https://modelcontextprotocol.io/specification/2025-03-26/basic/utilities/ping)
- 主 README：`../readme.md`
- Postman 测试：`../postman/`
