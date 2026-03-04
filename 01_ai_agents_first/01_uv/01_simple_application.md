# 使用 `uv` 创建简单应用

## 1. 概述

在 `uv` 中，**简单应用（simple application）** 指的是不引入打包开销的 Python 项目。本质上它就是一个脚本目录，由 `uv` 统一管理依赖和环境。

适用场景：

- 快速原型
- 内部工具
- 一次性自动化脚本
- 概念验证（PoC）项目

简单应用可以几乎立即创建和运行，无需定义打包元数据，也不需要发布到 PyPI。

## 2. 前置条件

创建简单应用前，请确认：

1. **已安装 `uv`** - 若未安装，请参考 [`../00_uv_installation/README.md`](../00_uv_installation/readme.md) 中的说明。
   检查安装：

   ```bash
   uv --version
   ```

   **期望输出（示例）：**

   ```
   uv 0.x.x
   ```

   _（具体版本号会有所不同。）_

2. **已安装 Python** - `uv` 也可以帮你管理并固定 Python 版本。
   检查可用性：

   ```bash
   python --version
   ```

   **期望输出（示例）：**

   ```
   Python 3.x.x
   ```

## 3. 创建简单应用的步骤

### 步骤 1 - 创建项目

1. 在你希望创建新项目的目录中打开终端（例如 `Projects`）。
2. 执行：

   ```bash
   uv init my-simple-app
   cd my-simple-app
   ```

这会：

- 创建 `my-simple-app` 目录
- 初始化一个新的 `uv` 项目，包含：

  - `.gitignore`
  - `.python-version`（自动固定）
  - `main.py`（示例脚本）
  - `pyproject.toml`
  - `README.md`

**期望项目结构：**

```text
my-simple-app/
├── .gitignore         # Python 项目的预置忽略规则
├── .python-version    # 自动固定的 Python 版本
├── main.py            # uv 创建的示例 Python 脚本
├── pyproject.toml     # 项目配置文件
└── README.md          # uv 创建的空 readme 文件
```

### 步骤 2 - 创建环境

立即创建虚拟环境和锁文件（对 VS Code 等编辑器配置很有帮助）：

```bash
uv sync
```

这会：

- 创建 `.venv` 目录，便于编辑器识别解释器
- 生成 `uv.lock`，将依赖锁定为从 `pyproject.toml` 解析得到的版本

### 步骤 2.1 -（可选）激活环境

> 你**不需要**激活环境也能使用 `uv`（`uv run ...` 会自动使用项目环境）。
> 只有在你希望不通过 `uv run`、直接运行 `python`/`pip`，或用于编辑器/REPL 工作流时，才需要手动激活。

如果你在 VS Code 中使用内置终端并已设置解释器，通常不需要手动激活环境。

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

4. 确认 VS Code 状态栏显示了已选中的解释器。

### 步骤 4 - 更新默认代码

将 `main.py` 内容替换为：

```python
def main():
    print("Hello from my-simple-app! - Hassan, PIAIC")

if __name__ == "__main__":
    main()
```

应用运行时会打印一条问候语。

### 步骤 5 - 运行应用

无需手动激活环境（推荐）：

```bash
uv run python main.py
```

**期望输出：**

```
Hello from my-simple-app! - Hassan, PIAIC
```

_（如果你在步骤 2.1 已激活环境，直接运行 `python main.py` 也可以。）_

## 4. 可选运行方式（模块与脚本入口）

即使不完全打包，你也可以用“包风格”的方式运行简单应用。

### 4.1 按模块运行

通过模块解析器运行脚本（如果以后重构为包，这种方式更易迁移）：

```bash
uv run -m main
```

该命令会查找 `main.py`（或 `main` 包）并以模块方式执行。若你后续把主文件重命名或移动到包目录，请调整模块路径（例如 `uv run -m mypackage.main`）。

### 4.2 在 `pyproject.toml` 中定义脚本命令

你可以在**简单应用**中暴露一个友好的 CLI 命令（类似打包应用），方法是在 `uv` 中启用打包并定义脚本入口。

打开 `uv` 创建的 `pyproject.toml`，并在文件末尾添加以下内容：

```toml
[project.scripts]
myapp = "main:main"

[tool.uv]
package = true
```

然后刷新环境，让 `uv` 安装该 CLI 入口：

```bash
uv sync
```

现在你可以运行：

```bash
uv run myapp
```

**说明：**

- `myapp` 必须与 `[project.scripts]` 下的键名一致。
- `"main:main"` 的含义是：打开 `main.py` 并执行 `main()` 函数。
- 这在简单应用中可行；但如果你的长期目标是分发项目或进行专业化维护，建议一开始就采用**打包应用**工作流。
  打包应用在脚本管理、版本管理、依赖管理和发布方面更规范。

## 5. 简单应用实用建议

- 任何时候都可以添加依赖：

  ```bash
  uv add <package-name>
  ```

- 为保证可复现，建议提交这些文件：`pyproject.toml`、`uv.lock`、`.gitignore`、`.python-version`。
- 需要分享项目时，其他人可精确复现环境：

  ```bash
  uv sync --frozen
  ```

- 随着项目增长（多模块、测试、分发需求），可考虑迁移到**打包应用**（见 [`../02_packaged_application`](../02_packaged_application/README.md)）。

## 6. 常用命令速查

```bash
uv init my-simple-app        # 创建并初始化新项目
uv sync                      # 立即创建 .venv 和 uv.lock
code .                       # 在 VS Code 中打开
# （可选）激活环境
source .venv/bin/activate    # macOS/Linux
.\.venv\Scripts\activate     # Windows
uv add <package-name>        # 添加依赖
uv run python main.py        # 以文件方式运行
uv run -m main               # 以模块方式运行
uv run myapp                 # 运行脚本入口（在 pyproject 中添加后）
uv sync --frozen             # 精确复现环境
deactivate                   # 退出虚拟环境
```
