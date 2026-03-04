# UV 安装

# Python 安装（适用于所有操作系统的分步指南）

---

## Windows

### 步骤 1：下载 Python

- 访问：https://www.python.org/downloads/windows/
- 点击 **"Download Python 3.x.x"**（最新版本）

### 步骤 2：运行安装程序

- 双击下载的 `.exe` 文件
- **重要**：勾选 **"Add Python to PATH"**
- 点击 **Install Now**

### 步骤 3：验证安装

打开 **命令提示符（Command Prompt）** 并执行：

```bash
python --version
```

---

## macOS

### 步骤 1：使用 Homebrew（推荐）

先安装 Homebrew（如未安装）：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

然后安装 Python：

```bash
brew install python
```

### 步骤 2：验证安装

```bash
python3 --version
```

---

## Linux（基于 Ubuntu/Debian）

### 步骤 1：更新系统

```bash
sudo apt update
```

### 步骤 2：安装 Python

```bash
sudo apt install python3 python3-pip -y
```

### 步骤 3：验证安装

```bash
python3 --version
pip3 --version
```

---

# UV 包管理器安装（所有操作系统）

---

## Windows

### 步骤 1：以管理员身份打开 PowerShell

### 步骤 2：运行安装脚本

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 步骤 3：验证

```powershell
uv --version
```

---

## macOS

### 方式 1：通过 Homebrew 安装

```bash
brew install uv
```

### 方式 2：通过脚本安装

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 步骤 3：验证

```bash
uv --version

```

---

## Linux

### 步骤 1：通过 Curl 安装

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 可选：如有需要，加入 PATH

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### 步骤 2：验证
```bash
uv --version
```
