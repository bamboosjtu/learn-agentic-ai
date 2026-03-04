# 使用 `uv` 创建打包应用

## 1. 概述

在 `uv` 中，**打包应用（packaged application）** 是按可分发包结构组织的 Python 项目。
它包含元数据、依赖，以及可选的入口点，因此可以：

- 在本地或其他机器上安装
- 通过版本与依赖管理实现更清晰的长期维护
- 通过可导入模块或 CLI 命令运行

适用场景：

- 需要复用或内部共享的应用
- 需要清晰、可导入模块结构的项目
- 追求长期可维护性的项目
- 需要 CLI 入口或为其他项目提供库能力的应用

与简单应用相比，打包应用更好地处理：

- **版本管理**（在 `pyproject.toml` 中）
- **标准化安装**
- **脚本入口点**（无需额外 `tool.uv` 配置）

## 2. 前置条件

创建**打包应用**前，请确认：

1. **已安装 `uv`** - 若未安装，请参考 [`../00_uv_installation/README.md`](../00_uv_installation/readme.md)。
   检查安装：

   ```bash
   uv --version
   ```

   **期望输出（示例）：**

   ```
   uv 0.x.x
   ```

   _（具体版本可能不同。）_

2. **已安装 Python** - `uv` 可帮你管理并固定 Python 版本。
   检查可用性：

   ```bash
   python --version
   ```

   **期望输出（示例）：**

   ```
   Python 3.x.x
   ```

## 3. 创建打包应用的步骤

### 步骤 1 - 创建项目

在你希望创建新项目的目录（如 `Projects`）打开终端并执行：

```bash
uv init --package my-packaged-app
cd my-packaged-app
```

这会：

- 创建 `my-packaged-app` 目录
- 使用 **`src` 布局** 初始化一个 `uv` 打包项目，将源码与配置/元数据分离
- 包含以下内容：

  - `.gitignore`
  - `.python-version`（自动固定）
  - `src/my_packaged_app/`（含 `__init__.py` 的包目录）
  - `pyproject.toml`
  - `README.md`

**期望项目结构：**

```text
my-packaged-app/
├── .gitignore                # Python 项目的预置忽略规则
├── .python-version           # 自动固定的 Python 版本
├── pyproject.toml            # 项目元数据与依赖
├── README.md                 # 项目文档
└── src/
    └── my_packaged_app/      # 你的包目录
        └── __init__.py       # 标记该目录为 Python 包
```

> **为什么使用 `src` 布局？**
> 它可以避免开发时误从本地文件导入，并确保你的代码以与安装后一致的方式被测试。

### 步骤 2 - 创建环境

立即创建虚拟环境与锁文件（对 VS Code 等编辑器配置很有帮助）：

```bash
uv sync
```

这会：

- 创建 `.venv` 目录，便于编辑器识别解释器
- 生成 `uv.lock`，将依赖锁定到由 `pyproject.toml` 解析出的版本

### 步骤 2.1 -（可选）激活环境

> 你**不需要**激活环境也能使用 `uv`（`uv run ...` 会自动使用项目环境）。
> 仅当你希望不经过 `uv run`、直接运行 `python`/`pip`，或用于编辑器/REPL 工作流时才需要激活。

如果你在 VS Code 中使用内置终端并且已设置解释器，通常无需手动激活环境。

**macOS/Linux：**

```bash
source .venv/bin/activate
```

**Windows：**

```bash
.\.venv\Scripts\activate
```

- 激活后，命令行提示符通常会显示 `(.venv)`。
- 退出激活：

  ```bash
  deactivate
  ```

**PowerShell 说明（若激活被阻止）：**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

（或者继续使用 `uv run ...`，无需激活。）

### 步骤 3 - 打开 VS Code 并选择解释器

1. 在 VS Code 中打开项目：

   ```bash
   code .
   ```

2. 打开 **Command Palette（命令面板）**：

   - **Windows/Linux**：`Ctrl+Shift+P`
   - **macOS**：`Cmd+Shift+P`
     然后选择：**Python: Select Interpreter** -> **Enter Interpreter Path** -> **Find**。

3. 在项目 `.venv` 中选择解释器：

   - **macOS/Linux**：`.venv/bin/python`
   - **Windows**：`.venv\Scripts\python.exe`

4. 确认 VS Code 状态栏中显示已选择的解释器。

### 步骤 4 - `__init__.py` 的作用，以及为什么 `uv run my-packaged-app` 可用

当前你的包在 `src/my_packaged_app/__init__.py` 中暴露了入口函数：

```python
# src/my_packaged_app/__init__.py
def main() -> None:
    print("Hello from my-packaged-app!")
```

- **`__init__.py` 的作用（简版）：** 它将目录标记为包，同时也是暴露包公共 API 的合适位置（轻量辅助函数、`__version__`、重导出等）。
- **为什么命令可用：** 你的 `pyproject.toml` 中有：

  ```toml
  [project.scripts]
  my-packaged-app = "my_packaged_app:main"
  ```

  这会把 CLI 命令 `my-packaged-app` 映射到**包模块** `my_packaged_app`（即 `__init__.py`）中的 `main` 可调用对象。路径里不需要写 `__init__`。

> **建议：** 保持 `__init__.py` 轻量。把主要应用逻辑放到 `main.py`，并让脚本入口指向它。

### 步骤 5 - 创建 `main.py` 并添加第二个 CLI 入口（保留原入口）

目前，CLI 命令 `my-packaged-app` 绑定的是 `__init__.py` 里的 `main()`。
接下来我们会**新增**一个命令，让它运行新的 `main.py` 文件，同时**不移除**原命令；并说明在文件中放置**顶层代码（top-level code）**会发生什么。

#### 1) 在包内创建 `main.py`

```text
src/
  my_packaged_app/
    __init__.py
    main.py
```

**`src/my_packaged_app/main.py`：**

```python
print("Top-level hello from main.py!")  # 文件被执行或导入时会立即运行

def main() -> None:
    print("Hello from my-packaged-app! - running main.py")
```

#### 2) 在 `pyproject.toml` 中添加新脚本入口

`[project.scripts]` 下命令采用如下格式：

```text
command-name = "module_path:function_name"
```

- **command-name** -> 你在 `uv run` 后输入的命令名
- **module_path** -> Python 模块路径（目录用点号分隔，不写 `.py` 后缀）
- **function_name** -> 模块中的可调用函数

```toml
[project.scripts]
my-packaged-app = "my_packaged_app:main"           # 运行 __init__.py 中的 main()
my-packaged-app-main = "my_packaged_app.main:main" # 运行 main.py 中的 main()
```

> 在打包应用中，`uv` 会在运行时解析脚本入口，因此你保存 `pyproject.toml` 后即可直接运行新命令。

#### 3) 运行任一命令

```bash
# 原入口（__init__.py:main）
uv run my-packaged-app
# 输出：
# Hello from my-packaged-app!

# 新入口（main.py:main）
uv run my-packaged-app-main
# 输出：
# Top-level hello from main.py!
# Hello from my-packaged-app! - running main.py
```

**关于顶层代码：**
任何不在函数/类中的语句（如 `print(...)`）都会在模块被**导入或执行时立即运行**。
因此你会先看到顶层 `print`，再看到 `main()` 的输出。

### 步骤 6 - 运行应用（4 种可靠方式）

现在你有两个 CLI 入口：

- `my-packaged-app` -> 调用 `my_packaged_app:main`（来自 `__init__.py`）
- `my-packaged-app-main` -> 调用 `my_packaged_app.main:main`（来自 `main.py`）

按你的工作流选择运行方式：

#### 6.1 使用 **CLI 脚本** 运行（打包应用体验最佳）

使用 `pyproject.toml` 的 `[project.scripts]`：

```bash
uv run my-packaged-app
uv run my-packaged-app-main
```

#### 6.2 以 **模块** 方式运行（包感知，无需文件路径）

遵循包导入方式：

```bash
uv run -m my_packaged_app.main
```

#### 6.3 以 **文件路径** 运行（快捷，但包感知较弱）

- **Windows**

  ```powershell
  uv run python .\src\my_packaged_app\main.py
  ```

- **macOS/Linux**

  ```bash
  uv run python ./src/my_packaged_app/main.py
  ```

_注意：_ 按路径执行时文件以 `__main__` 运行；类似 `from .utils import foo` 的相对导入会失败。除快速检查外，建议优先 6.1 或 6.2。

#### 6.4 单行命令（快速自检很方便）

```bash
uv run python -c "from my_packaged_app.main import main; main()"
```

**再次提醒顶层代码：** 如果 `main.py`（或任何模块）有顶层语句，例如 `print("Hello")`，由于模块会先被导入，这些语句会在 `main()` 之前执行。

### 步骤 7 - 添加依赖（运行时与开发时）

添加运行时依赖：

```bash
uv add <package-name>
```

添加开发工具（lint/format/type check）：

```bash
uv add --dev ruff black mypy
```

`uv` 会自动解析并更新 `uv.lock`。

### 步骤 8 - 建议与最佳实践

- 保持 `__init__.py` 轻量（元数据、重导出）。核心逻辑放到 `main.py` 等模块。
- 日常使用优先 **CLI 脚本**（步骤 6.1）或 **模块运行**（步骤 6.2）。
- 提交这些文件：`pyproject.toml`、`uv.lock`、`.gitignore`、`.python-version` 以及 `src/` 目录。
- 在 CI 或协作环境中使用 `uv sync --frozen`，确保环境与锁文件完全一致。

### 步骤 9 - 常用命令速查

```bash
# 创建并进入项目
uv init --package my-packaged-app
cd my-packaged-app

# 环境与锁文件
uv sync

# 运行（脚本入口）
uv run my-packaged-app
uv run my-packaged-app-main

# 运行（模块与文件）
uv run -m my_packaged_app.main
uv run python ./src/my_packaged_app/main.py   # (Windows: .\src\my_packaged_app\main.py)

# 依赖与开发工具
uv add <package-name>          # 运行时依赖
uv add --dev ruff black mypy   # 开发工具（示例）

# 精确复现环境
uv sync --frozen
```
