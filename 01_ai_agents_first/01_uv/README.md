# `uv`：统一的 Python 包与项目管理器

- [如何安装 UV - Notion 指南？](https://www.notion.so/UV-Installation-236e9749823180b7ab82d96a3b5997fd?source=copy_link)
- [Python UV：最快 Python 包管理器终极指南](https://www.datacamp.com/tutorial/python-uv)
- [官方文档](https://docs.astral.sh/uv/)
- [运行脚本](https://docs.astral.sh/uv/guides/scripts/)
- [项目开发](https://docs.astral.sh/uv/guides/projects/)
- [CLI 参考](https://docs.astral.sh/uv/reference/cli/)
- [视频：简化 Python 环境配置 - 完整 uv 教程](https://www.youtube.com/watch?v=-J5SnWR4UXw)

## 1. 什么是 `uv`？

`uv` 是一个快速的一体化工具，用于端到端管理 Python 项目。它可以创建虚拟环境、下载并固定特定 Python 版本、添加或更新依赖、维护可复现安装所需的锁文件、无需手动激活环境即可运行代码与工具，并支持构建和发布包。
你主要会与两个文件打交道：

* **`pyproject.toml`** - 声明式依赖需求
* **`uv.lock`** - 解析并安装后的精确版本

## 2. `uv` 中的应用与库

`uv` 同时支持构建 **应用（applications）** 和 **库（libraries）**，两者在 Python 生态中承担不同角色。应用是直接面向最终用户运行的程序，例如命令行工具、Web 服务和自动化脚本。它们通常包含入口点（如 CLI 命令或 `__main__.py`），并在受控运行时环境中执行，以保证一致性。

而库是可复用代码的集合，供其他项目导入使用。它们提供共享能力，通常会发布到 PyPI 等包索引，供其他开发者依赖。应用直接向最终用户交付价值，库则作为构建模块被应用或其他库复用。两者都很重要：应用直接创造用户价值，库则促进代码复用、可维护性和生态发展。

## 3. 在 `uv` 中如何构建应用

创建应用时，`uv` 提供两种主要方式：

* **打包应用（Packaged applications）** - 以可安装 Python 包形式构建，并定义入口点。该结构适合长期项目、分发到其他环境，或对版本管理与可复现性要求较高的场景。打包应用在正确环境下可被方便地安装并运行。
* **简单应用（Simple applications）** - 以非结构化项目目录形式创建，包含可通过 `uv run` 直接运行的脚本。搭建速度快，适合原型、内部工具和一次性小工具，不需要承担打包开销。

两种方式都有价值：打包应用适合精致、可分享的软件；简单应用则在早期开发或内部场景中提供最高速度和灵活性。

## 4. 开发生命周期（分步）

| 步骤 | 标题 | 说明 |
| ---- | ---- | ---- |
| 1 | 初始化项目 | `uv init` 可快速生成干净的项目结构和初始 `pyproject.toml`，替代手动建目录与拷模板。 |
| 2 | 固定 Python 版本 | `uv python pin 3.12` 确保所有人使用同一解释器版本；必要时自动下载，并记录给开发者和 CI。 |
| 3 | 创建环境 | 首次进行依赖操作时，`uv` 会自动创建虚拟环境。使用 `uv run` 可在无需手动激活环境的情况下执行代码。 |
| 4 | 添加运行时依赖 | `uv add pkg` 会在一个原子步骤中更新声明、解析版本、加锁并安装，保持声明与已安装包一致。 |
| 5 | 添加开发工具 | `uv add --dev tool` 可将开发依赖（测试、lint、格式化）与运行时依赖清晰分离，并共用同一个锁文件。 |
| 6 | 可选功能分组 | `uv add --group docs mkdocs` 可定义按需安装的可选功能组。 |
| 7 | 锁定依赖 | 依赖变更后，`uv` 会自动维护 `uv.lock`，以保证可复现安装。 |
| 8 | 同步环境 | `uv sync` 确保环境与锁文件完全一致；`uv sync --frozen` 会在锁文件未更新时阻止变更。 |
| 9 | 运行代码与工具 | `uv run <cmd>` 会在正确环境中执行命令，无需手动激活 venv。 |
| 10 | Lint / 格式化 / 类型检查 | 通过 `uv run` 运行工具，可确保本地与 CI 使用完全一致的锁定版本。 |
| 11 | 测试 | `uv run pytest` 可保证测试基于锁定依赖集运行，避免“我机器上是好的”问题。 |
| 12 | 升级依赖 | `uv upgrade` 在一个受控步骤中重新解析、加锁并安装更新。 |
| 13 | 构建产物 | `uv build` 可在最少配置下快速生成 wheel 与 sdist。 |
| 14 | 发布 | `uv publish` 可在一步中完成构建（如有需要）并上传到 PyPI 或其他索引。 |
| 15 | 使用缓存 | 共享缓存可加速安装，并可进行检查或清理。 |
| 16 | 离线/受限环境 | 配合缓存导出导入与 `uv sync --frozen`，可完整重建离线环境。 |
| 17 | CI 可复现性 | 在 CI 中使用 `uv sync --frozen`，可在安装前确保锁文件与声明文件一致。 |
| 18 | 检查环境 | `uv run pip list` 等命令始终作用于项目环境，而不是全局 Python。 |
| 19 | 清理与裁剪 | `uv cache prune` 或删除环境可释放空间；所有内容都可由声明 + 锁文件重建。 |
| 20 | Monorepo 管理 | Monorepo 中每个项目都可拥有自己的 `pyproject.toml` + `uv.lock`，实现独立同步。 |
| 21 | 迁移（可选） | `uv` 可从旧式 requirements 文件导入规格、解析并加锁，简化到双文件模型。 |

## 5. 新手常见坑（及修复）

* **忘记提交 `uv.lock`** - 一定要提交，这样团队成员才能得到一致版本。
* **手动编辑 `pyproject.toml`** - 优先用 `uv add` 或 `uv remove`，让锁文件自动更新。若确实手改了，请运行会重新加锁的命令（`uv sync` 或 `uv add`）进行刷新。
* **手动激活环境** - 直接使用 `uv run`。
* **混用 `pip install` 与 `uv add`** - 尽量统一使用 `uv add`，保持锁文件正确。

---

### Cursor 系统规则

在 Cursor 中进行 Python 开发时，始终使用 **`uv`** 作为包管理器。

在可行情况下，优先使用 CLI 命令完成常见任务，而不是手写环境初始化代码。比如，当你被要求用 `uv` 创建新项目时：

**打包应用（Packaged Applications）：**
打包应用适用于很多场景，例如构建要发布到 PyPI 的命令行工具，或希望将测试放在独立目录中。

创建打包应用：

```bash
uv init --package example-pkg
```

**添加依赖：**
在项目中安装依赖：

```bash
uv add openai-agents
```

---
