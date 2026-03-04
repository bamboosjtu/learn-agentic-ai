# PostgreSQL Sessions

## 概览

**PostgreSQL Sessions** 提供基于 PostgreSQL 数据库的生产级 session 管理方案。它非常适合多服务器部署、高并发应用，以及需要 ACID 保证和高级数据库能力的企业环境。

## 关键特性

- **生产可用**：经过长期验证的关系型数据库，具备 ACID 保证
- **高并发**：可处理数千个并发连接
- **高级查询**：完整 SQL 能力，适合复杂分析
- **可扩展性**：支持纵向与横向扩展
- **复制能力**：内置主从复制能力
- **备份能力**：支持时间点恢复、`pg_dump`、持续归档
- **安全性**：支持行级安全、加密、基于角色的访问控制

## 什么时候适合使用

**以下场景适合使用 PostgreSQL Sessions：**

- 部署生产 Web 应用
- 需要高并发（100+ 同时在线用户）
- 需要高级分析和报表
- 需要多服务器共享状态
- 合规要求 ACID 事务
- 需要生产级备份与恢复能力

**以下场景更适合 SQLite：**

- 本地/桌面应用
- 单用户或低并发
- 希望零配置启动
- 不需要分布式部署

## 架构

```
Multiple Agent Instances (Servers)
  Server 1 | Server 2 | Server 3
                |
         PostgreSQL Database
         - conversations table
         - messages table
         - usage_logs table
         - Connection pooling
```

```bash
uv add asyncpg sqlalchemy "psycopg[binary]"
```

## 延伸阅读

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Connection Pooling Best Practices](https://wiki.postgresql.org/wiki/Number_Of_Database_Connections)
- [OpenAI Agents SDK: PostgreSQL Sessions](https://github.com/openai/openai-agents-sdk)
