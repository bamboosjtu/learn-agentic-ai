# 第 3 阶段：Docker 基础

这一阶段会带你学习如何把 Chainlit 应用打包进容器。你可以把容器想象成一个午餐盒：食物是你的代码，餐具是你的依赖库，它们会一起被打包，这样无论放到哪张桌子上都能正常工作。本指南会介绍 Docker 基础，并演示如何把 Chainlit 应用容器化。

## 你将学到什么

- 新术语：**image**、**container** 和 **registry**
- 如何用一条命令构建 image
- 如何在本地运行 image
- 以后如何把它分享给 Render 或 Railway
- Docker 的基础概念与常用命令

## 开始之前

- 从 https://www.docker.com/products/docker-desktop 安装 Docker Desktop
- 打开 Docker Desktop 一次，让它完成初始化
- 确保第 1 阶段已经能在本地跑通，因为这里会复用同一个 `main.py`

## 第 1 步：查看文件

```
03_docker_basics/
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── main.py
├── requirements.txt
└── README.md
```

- `Dockerfile` 告诉 Docker 如何构建这个“午餐盒”
- `docker-compose.yml` 让你在开发时更方便地运行它
- `.dockerignore` 用来避免把大文件或敏感文件打进镜像

## 第 2 步：构建镜像

```bash
cd 03_docker_basics
docker build -t chainlit-agent .
```

发生了什么：

- Docker 下载了基础镜像
- 把你的应用文件复制进去
- 安装 `requirements.txt` 中的依赖

可以通过下面命令查看镜像：

```bash
docker images
```

## 第 3 步：运行容器

```bash
docker run \
  -p 8000:8000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  chainlit-agent
```

- `-p 8000:8000` 把容器端口映射到本机端口
- `-e OPENAI_API_KEY=...` 把密钥传进容器
- 你也可以使用 `--env-file .env`

打开 [http://localhost:8000](http://localhost:8000) 测试应用。

完成后，用 `Ctrl + C` 停止。

## 第 4 步：使用 Docker Compose（可选但很方便）

```bash
docker compose up --build
```

Compose 可以帮助你在开发时更方便地启动、重建和管理容器。退出时用 `Ctrl + C`，清理停止的容器用：

```bash
docker compose down
```

## 第 5 步：分享镜像（进阶）

当你准备好了，可以把镜像打 tag 并推送到 Docker Hub 或内部 registry：

```bash
docker tag chainlit-agent yourname/chainlit-agent:v1
docker push yourname/chainlit-agent:v1
```

之后 Render、Railway 等服务就可以直接拉取这个镜像来部署。

## Dockerfile 示例说明

```dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN useradd -m -u 1000 user
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
USER user
CMD ["chainlit", "run", "main.py"]
```

## Docker Compose 示例说明

```yaml
version: "3.8"
services:
  chatbot:
    build: .
    ports:
      - "7860:7860"
    volumes:
      - .:/app
    environment:
      - OPENAI_API_KEY
```

## 最佳实践

1. **安全性**
   - 使用非 root 用户
   - 尽量减小镜像体积
   - secrets 放在环境变量中

2. **性能**
   - 使用 `.dockerignore`
   - 利用 layer cache
   - 必要时用 multi-stage build

3. **开发体验**
   - 使用 Docker Compose
   - 开启热重载
   - 用 volume 挂载本地代码

## 常用命令

```bash
docker build -t app-name .
docker run app-name
docker ps
docker stop container-id
docker rm container-id
docker logs container-id
docker exec -it container-id bash
```

## 故障排查

1. **容器无法启动**
   - 查看日志：`docker logs container-id`
   - 检查端口映射
   - 检查环境变量

2. **改动没有生效**
   - 重新构建：`docker-compose up --build`
   - 检查 volume 挂载
   - 必要时清理 Docker 缓存

3. **权限问题**
   - 检查用户权限
   - 检查文件所有权
   - 检查 volume mount 配置

## 下一步

掌握这些基础后，你就可以继续：

1. 部署到生产环境
2. 构建多容器应用
3. 在 CI/CD 中使用 Docker
4. 优化容器性能

## 参考资料

- [Official Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
