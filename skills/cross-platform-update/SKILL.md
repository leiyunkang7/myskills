---
name: cross-platform-update
description: 更新指定软件并适配跨平台兼容性。当用户提到"更新软件"、"升级程序"、"install update"、"软件更新"、"跨平台更新"、"适配多平台"时触发。支持 Linux (apt/yum/dnf)、macOS (brew)、Windows (winget/choco) 等主流平台自动识别与适配。
version: 1.0.0
tags: [software-update, cross-platform, package-manager, devops]
---

# Cross-Platform Software Update Skill

跨平台软件更新技能 - 自动识别操作系统并选择合适的包管理工具完成软件更新。

## 核心能力

1. **平台自动识别**：检测当前操作系统类型和版本
2. **包管理器检测**：识别系统中可用的包管理工具
3. **智能更新策略**：根据平台选择最优更新命令
4. **跨平台兼容性检查**：确保更新操作在目标平台上的兼容性
5. **回滚支持**：提供更新失败时的回滚方案

## 支持的平台与包管理器

| 平台 | 包管理器 | 更新命令示例 |
|------|----------|--------------|
| Linux (Debian/Ubuntu) | apt | `apt update && apt upgrade <pkg>` |
| Linux (RHEL/CentOS/Fedora) | dnf/yum | `dnf update <pkg>` |
| Linux (Arch) | pacman | `pacman -Syu <pkg>` |
| macOS | Homebrew | `brew update && brew upgrade <pkg>` |
| macOS | MacPorts | `port selfupdate && port upgrade <pkg>` |
| Windows | winget | `winget upgrade <pkg>` |
| Windows | Chocolatey | `choco upgrade <pkg>` |

## 工作流程

### 步骤 1: 收集信息

执行以下命令收集系统信息：

```bash
# 获取操作系统信息
uname -a                    # Linux/macOS
systeminfo                 # Windows

# 检测包管理器
which apt dnf yum pacman brew port winget choco 2>/dev/null

# 检查权限
id                         # Linux/macOS
whoami                     # Windows
```

### 步骤 2: 分析目标软件

确定需要更新的软件：
- **通过名称指定**：`node`, `python`, `docker`
- **通过包名指定**：`nodejs`, `python3`, `docker-ce`
- **模糊匹配**：提供建议列表供用户确认

### 步骤 3: 验证兼容性

更新前检查：
1. 软件是否在目标平台可用
2. 目标版本是否支持当前平台
3. 是否有破坏性变更需要用户确认

### 步骤 4: 执行更新

根据平台执行相应命令：

**Linux (apt):**
```bash
sudo apt update
sudo apt upgrade <package-name>
```

**Linux (dnf):**
```bash
sudo dnf check-update
sudo dnf update <package-name>
```

**macOS (brew):**
```bash
brew update
brew upgrade <package-name>
```

**Windows (winget):**
```powershell
winget upgrade <package-name>
```

### 步骤 5: 验证结果

```bash
# 检查版本
<package-name> --version

# 验证安装
which <package-name>     # Linux/macOS
where <package-name>     # Windows
```

## 跨平台兼容性检查清单

更新前必须确认以下事项：

- [ ] 软件在目标平台有官方支持
- [ ] 检查软件官网的 platform support 页面
- [ ] 确认架构兼容性 (x86_64, arm64)
- [ ] 检查依赖项是否满足
- [ ] 查看 changelog 中的 breaking changes

## 特殊场景处理

### 1. 系统级软件（需要 sudo/admin）

```bash
# Linux
sudo apt install --only-upgrade <package>

# macOS (Homebrew 需要注意权限)
brew upgrade <package>  # 通常不需要 sudo

# Windows
winget upgrade <package>  # 可能需要管理员权限
```

### 2. 多个软件批量更新

```bash
# Linux
sudo apt update && sudo apt upgrade package1 package2 package3

# macOS
brew upgrade package1 package2 package3

# Windows
winget upgrade package1 package2 package3
```

### 3. 查看可用更新

```bash
# Linux
apt list --upgradable          # apt
dnf check-update              # dnf
brew outdated                 # Homebrew

# Windows
winget upgrade                # 无参数列出所有可用更新
```

### 4. 更新失败处理

```bash
# 保存当前版本信息
dpkg -l | grep <package>      # Linux
brew info <package>           # macOS

# 查看详细错误
apt-cache policy <package>     # Linux
brew install --verbose <pkg> # macOS
```

## 输出格式

每次更新操作后，提供以下信息：

```
📦 软件更新报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
软件名称: <package-name>
目标平台: <os-name>
包管理器: <package-manager>
当前版本: <old-version>
更新版本: <new-version>
更新状态: ✅ 成功 / ❌ 失败
执行时间: <timestamp>
```

## 错误处理

| 错误类型 | 处理方案 |
|----------|----------|
| 包不存在 | 搜索正确的包名，建议替代方案 |
| 权限不足 | 提示使用 sudo 或以管理员身份运行 |
| 网络问题 | 检查网络连接，重试或使用镜像源 |
| 依赖冲突 | 分析依赖树，提供解决方案 |
| 版本不兼容 | 建议兼容版本或替代软件 |

## 示例对话

**用户**: "更新一下 nodejs"

**助手**:
1. 检测平台为 Ubuntu Linux，使用 apt
2. 执行 `apt-cache search nodejs` 确认包名
3. 执行 `sudo apt update && sudo apt install --only-upgrade nodejs`
4. 验证版本并报告结果

**用户**: "brew 的包怎么更新"

**助手**:
1. 检测 macOS + Homebrew
2. 解释 Homebrew 更新流程
3. 提供 `brew update && brew upgrade <pkg>` 命令
4. 说明如何查看可更新包 `brew outdated`

**用户**: "帮我更新 Windows 上的 docker"

**助手**:
1. 检测 Windows，尝试 winget
2. 执行 `winget upgrade Docker.DockerDesktop`
3. 如失败，提供备用方案（手动下载安装）

## 最佳实践

1. **先查询再更新**：不确定包名时先用 search/info 命令查询
2. **小步快跑**：复杂更新分步骤执行，便于定位问题
3. **记录变更**：保存更新前后的状态，便于回溯
4. **用户确认**：涉及系统核心包或大版本更新时先确认
5. **检查依赖**：更新可能影响依赖它的其他软件

## 注意事项

- ⚠️ 系统核心包（如 glibc、kernel）的更新需格外谨慎
- ⚠️ 大版本更新可能包含 breaking changes
- ⚠️ 部分软件需要手动重启或重新登录才能生效
- ⚠️ 企业环境可能使用内部包源，需要额外配置
