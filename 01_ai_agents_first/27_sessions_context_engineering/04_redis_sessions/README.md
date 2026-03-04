# Redis Sessions

## 概览

**Redis Sessions** 提供超高速、分布式的 session 管理能力，适用于高性能应用。Redis 把 session 保存在内存中，并可选择持久化，因此非常适合需要毫秒级延迟的实时应用和分布式系统。

## 关键特性

- **超高速**：内存存储，微秒级延迟
- **分布式**：天然适合多服务器部署
- **TTL（生存时间）**：支持自动过期
- **Pub/Sub**：支持实例之间实时更新
- **集群**：通过 Redis Cluster 横向扩展
- **持久化**：可选磁盘持久化（RDB/AOF）
- **多租户**：通过 key 前缀隔离

## 什么时候适合使用

**以下场景适合使用 Redis Sessions：**

- 需要超低延迟（< 1ms）
- 构建实时应用（聊天、游戏等）
- 部署分布式系统
- 需要自动 session 过期（TTL）
- 想把缓存和 session 存储合并在一起
- 处理高吞吐（10k+ req/sec）

**以下场景更适合 PostgreSQL：**

- 需要复杂 SQL 查询
- 需要强 ACID 保证
- 希望保留持久分析历史
- 预算有限（Redis 可能更贵）

实现参考：
https://github.com/openai/openai-agents-python/pull/1785
