# OpenAI Agents SDK 的自定义 Session Memory 后端

这个文件夹包含了一些为 OpenAI Agents SDK 实现自定义 session memory 的示例。它们可以让你把会话历史保存在默认内存或 SQLite 之外的后端中，从而支持更持久、更可扩展的对话存储。对于生产系统而言，如果你需要可靠、可扩展的 Agent 会话存储，这类方案就很有价值。

## 为什么需要自定义 Session？

- **持久化：** 即使进程重启，聊天历史也不会丢失
- **可扩展：** 可以使用更健壮的数据库支持多用户、分布式部署
- **灵活性：** 能接入你现有的基础设施，例如 Supabase、Redis、PostgreSQL

这些示例都实现了 OpenAI Agents SDK 中的 `Session` 协议，因此你几乎不需要改动 Agent 代码，就能替换掉默认 session 存储。

---

## 1. Supabase Session（最小示例）

- **文件：** `supabase_session.py`
- **后端：** [Supabase](https://supabase.com/)（PostgreSQL + REST API）
- **用途：** 演示如何使用云数据库作为 session memory
- **用法：**

  ```python
  from custom_sessions.supabase_session import SupabaseSessionMinimal
  session = SupabaseSessionMinimal(session_id="my-session-id")
  # 在 Agent 中使用时传入 session=session
  ```

- **注意：** 你需要自己实现实际的 Supabase 连接逻辑

---

## 2. Redis Session（生产可用）

- **文件：** `redis_session.py`
- **后端：** [Redis](https://redis.io/)（通过 `aioredis`）
- **用途：** 为生产环境提供快速、可扩展的内存型 session 存储
- **要求：**
  - 正在运行的 Redis 服务（本地或云端）
  - Python 包 `aioredis`（`uv add aioredis`）
- **用法：**

  ```python
  from custom_sessions.redis_session import RedisSession
  session = RedisSession(session_id="my-session-id", redis_url="redis://localhost:6379/0")
  # 在 Agent 中使用时传入 session=session
  ```

- **协议兼容：** 实现了所需全部方法：`get_items`、`add_items`、`pop_item`、`clear_session`

---

## 3. PostgreSQL Session（生产可用）

- **文件：** `postgres_session.py`
- **后端：** [PostgreSQL](https://www.postgresql.org/)（通过 `asyncpg`）
- **用途：** 使用关系型数据库提供持久化、可扩展的 session 存储
- **要求：**
  - 正在运行的 PostgreSQL 服务
  - Python 包 `asyncpg`（`uv add asyncpg`）
  - 一张名为 `agent_sessions` 的表，至少包含以下字段：
    - `id SERIAL PRIMARY KEY`
    - `session_id TEXT`
    - `role TEXT`
    - `content TEXT`
    - `created_at TIMESTAMP`
- **用法：**

  ```python
  from custom_sessions.postgres_session import PostgresSession
  session = PostgresSession(session_id="my-session-id", dsn="postgresql://user:password@localhost:5432/yourdb")
  # 在 Agent 中使用时传入 session=session
  ```

- **协议兼容：** 同样实现了 `get_items`、`add_items`、`pop_item`、`clear_session`

---

## 如何使用

1. 选择适合你部署方式的后端（Supabase、Redis、PostgreSQL，或者你自己实现）
2. 为每个用户 / 对话创建唯一的 `session_id`
3. 初始化 session 实例，并传给 Agent：

   ```python
   agent = MyAgent(..., session=session)
   ```

4. 之后，Agent 就会通过你定义的后端来存取对话历史

---

## 进一步扩展

- 你可以按照相同协议实现自己的 session 后端
- 也可以根据业务需求增加认证、加密或自定义逻辑

---

## 参考资料

- [OpenAI Agents SDK: Sessions Documentation](https://openai.github.io/openai-agents-python/sessions/)
