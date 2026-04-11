# ✅ 什么是 `curl`？

* `curl` 是一个命令行工具，可以让你发送 **HTTP 请求**，并查看对应的 **响应**。
* 它可运行在 Linux、macOS 和 Windows（搭配 Git Bash 或 WSL）上。

---

## 假设我们正在与一个简单的测试服务器交互：

我们将使用 [https://reqres.in](https://reqres.in)，这是一个专门用于测试 HTTP 请求的 **模拟 REST API**。

---

## 1️⃣ **GET**：获取数据

获取用户列表：

```bash
curl https://reqres.in/api/users?page=2
```

➡️ 你会得到类似下面的响应：

```json
{
  "page": 2,
  "data": [
    {
      "id": 7,
      "email": "michael.lawson@reqres.in",
      ...
    }
  ]
}
```

✅ 这就像是打开一个网页并读取其中的内容。

---

## 2️⃣ **POST**：发送数据（例如注册）

创建一个新用户：

```bash
curl -X POST https://reqres.in/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Wania", "job": "Developer"}'
```

➡️ 你会得到类似下面的响应：

```json
{
  "name": "Wania",
  "job": "Developer",
  "id": "245",
  "createdAt": "2025-06-17T22:00:00.000Z"
}
```

✅ 这模拟了提交表单来创建一个新账号的过程。

---

## 3️⃣ **PUT**：更新（整体替换）数据

完整更新该用户：

```bash
curl -X PUT https://reqres.in/api/users/2 \
  -H "Content-Type: application/json" \
  -d '{"name": "Wania", "job": "Senior Dev"}'
```

➡️ 响应：

```json
{
  "name": "Wania",
  "job": "Senior Dev",
  "updatedAt": "2025-06-17T22:05:00.000Z"
}
```

✅ 这会把原来的职位整体替换成 `"Senior Dev"`。

---

## 4️⃣ **PATCH**：部分更新数据

只更新一个字段（例如仅更新职位）：

```bash
curl -X PATCH https://reqres.in/api/users/2 \
  -H "Content-Type: application/json" \
  -d '{"job": "Engineer"}'
```

➡️ 响应：

```json
{
  "job": "Engineer",
  "updatedAt": "2025-06-17T22:10:00.000Z"
}
```

✅ 这只会修改职位，不会改动名字。

---

## 5️⃣ **DELETE**：删除资源

删除一个用户：

```bash
curl -X DELETE https://reqres.in/api/users/2
```

➡️ 响应：*(没有消息体，只有状态 `204 No Content`)*

✅ 这表示客户端可以确认该用户已被成功删除。

---

## 6️⃣ **HEAD**：只获取头部（不获取内容）

```bash
curl -I https://reqres.in/api/users/2
```

➡️ 你会得到：

```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 123
...
```

✅ 当你只想检查元数据，而不想下载整个页面或数据时，这很有用。

---

## 7️⃣ **OPTIONS**：询问允许使用哪些方法

```bash
curl -X OPTIONS https://reqres.in/api/users/2 -i
```

➡️ 你会得到：

```
Allow: GET, POST, PUT, PATCH, DELETE, OPTIONS
```

✅ 这会告诉浏览器或客户端，这个端点允许哪些操作。

---

## 📝 总结表

| Method  | curl Command             |
| ------- | ------------------------ |
| GET     | `curl URL`               |
| POST    | `curl -X POST -d ...`    |
| PUT     | `curl -X PUT -d ...`     |
| PATCH   | `curl -X PATCH -d ...`   |
| DELETE  | `curl -X DELETE URL`     |
| HEAD    | `curl -I URL`            |
| OPTIONS | `curl -X OPTIONS -i URL` |

