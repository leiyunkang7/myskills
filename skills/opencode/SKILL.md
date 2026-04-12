---
name: opencode-cli
description: OpenCode CLI 自动化与脚本化用法。适用于非交互式运行、API 服务器模式、远程连接、CI/CD 集成。当用户提到 opencode 非交互、opencode 自动化、opencode 脚本、opencode headless、opencode serve、opencode run、opencode API、opencode CI/CD、opencode 管道、opencode 批量处理，或需要将 AI 编码能力集成到自动化工作流时触发此技能。
---

# OpenCode CLI Skill

OpenCode 是一个 AI 编程 CLI 工具，默认启动 TUI 交互界面。本技能专注于**非交互式用法**，涵盖脚本化、自动化和 CI/CD 集成场景。

## 核心：两种运行模式

| 模式 | 命令 | 适用场景 |
|------|------|----------|
| **TUI (交互式)** | `opencode` | 实时开发、代码探索 |
| **run (非交互式)** | `opencode run "prompt"` | 脚本化、自动化、CI/CD |

---

## 非交互式核心：`opencode run`

### 基本用法

```bash
# 直接执行提示词
opencode run "Explain the use of context in Go"

# 安静模式（抑制 TUI 元素）
opencode run --format json "Explain async/await"

# 指定模型
opencode run -m provider/model "your prompt"

# 指定 Agent
opencode run --agent agent-name "your prompt"

# 附加文件
opencode run -f file1.js -f file2.py "review these files"

# 分享会话
opencode run --share "your prompt"
```

### 继续会话

```bash
# 继续上一个会话
opencode run -c "continue the refactoring"

# 继续指定会话
opencode run -s session-id "continue the task"

# Fork 会话继续
opencode run -c --fork "parallel task"
```

### 输出格式

```bash
# 默认格式（格式化输出）
opencode run "explain this"

# JSON 格式（原始 JSON 事件流）
opencode run --format json "analyze code"
```

JSON 格式输出结构化事件，适合程序解析：
```bash
opencode run --format json "list all TODO comments" > output.json
```

---

## 服务模式：`opencode serve`

启动无头 HTTP API 服务器，支持远程连接。

### 基本用法

```bash
# 启动服务器（默认端口 4096）
opencode serve

# 指定端口
opencode serve --port 8080

# 指定主机名（允许远程连接）
opencode serve --hostname 0.0.0.0 --port 4096

# 启用 CORS
opencode serve --cors

# 启用 mDNS 发现
opencode serve --mdns
```

### 环境变量配置

```bash
# 设置服务器密码
export OPENCODE_SERVER_PASSWORD="your_password"

# 自动分享会话
export OPENCODE_AUTO_SHARE=true

# 禁用自动更新
export OPENCODE_AUTO_SHARE=false
```

### 连接到远程服务器

```bash
# 终端 1: 启动服务器
opencode serve --hostname 0.0.0.0 --port 4096

# 终端 2: 连接并执行
opencode run --attach http://localhost:4096 "Explain async/await"
```

---

## Web 模式：`opencode web`

带浏览器界面的 HTTP 服务器。

```bash
# 启动 Web 服务器
opencode web

# 指定端口和主机
opencode web --port 4096 --hostname 0.0.0.0

# 允许 CORS
opencode web --cors
```

---

## 模型管理

```bash
# 列出可用模型
opencode models

# 列出特定 provider 的模型
opencode models anthropic

# 刷新模型列表
opencode models --refresh
```

---

## 会话管理

```bash
# 列出最近会话
opencode session list -n 10

# 查看 token 使用统计
opencode stats --days 30 --models

# 导出会话数据
opencode export [session-id]

# 导入会话数据
opencode import session.json
```

---

## CI/CD 集成模式

### GitHub Actions

```yaml
- name: AI Code Review
  run: |
    opencode run --format json \
      -m anthropic/claude-sonnet-4-20250514 \
      -c "review for security vulnerabilities"
```

### Git Pre-commit Hook

```bash
#!/bin/bash
opencode run -c "check staged files for obvious bugs" --max-turns 3
```

### 自动化修复流水线

```bash
#!/bin/bash
# 修复所有 linting 错误
opencode run -c "fix all linting errors" --max-turns 10
```

### 批量处理脚本

```bash
#!/bin/bash
for dir in ~/projects/*/; do
  opencode run -w "$dir" "analyze project structure"
done
```

---

## UNIX 管道集成

```bash
# 分析 git 提交
git log --oneline | opencode run "analyze these commits"

# 生成 commit message
git diff --cached | opencode run "generate a commit message"

# 代码审查
git diff | opencode run "review these code changes"

# 日志分析
cat error.log | opencode run "analyze these error logs"
```

---

## MCP 服务器管理

```bash
# 列出 MCP 服务器
opencode mcp list

# 管理 MCP 服务器（子命令）
opencode mcp
```

---

## Agent 管理

```bash
# 列出可用 Agent
opencode agent list

# 创建新 Agent
opencode agent create

# 管理 Agent
opencode agent
```

---

## 全局参数

| 参数 | 描述 |
|------|------|
| `-h, --help` | 显示帮助 |
| `-v, --version` | 显示版本 |
| `--print-logs` | 输出日志到 stderr |
| `--log-level` | 日志级别: DEBUG, INFO, WARN, ERROR |

---

## run 命令参数

| 参数 | 描述 |
|------|------|
| `-c, --continue` | 继续上一个会话 |
| `-s, --session` | 继续指定会话 ID |
| `--fork` | Fork 会话继续 |
| `-m, --model` | 指定模型 (格式: provider/model) |
| `--agent` | 指定使用的 Agent |
| `-f, --file` | 附加文件到消息 |
| `--format` | 输出格式: default 或 json |
| `--share` | 分享会话 |
| `--title` | 会话标题 |
| `--attach` | 连接到运行中的服务器 |

---

## 常见用例速查

| 场景 | 命令 |
|------|------|
| 快速问答 | `opencode run "解释闭包"` |
| 程序化输出 | `opencode run --format json "分析代码"` |
| 远程访问 | `opencode serve --port 4096` + `opencode run --attach http://host:4096` |
| CI/CD 自动化 | `opencode run -c "fix bugs" --max-turns 10` |
| 模型列表 | `opencode models anthropic` |
| 会话历史 | `opencode session list -n 10` |
| 成本统计 | `opencode stats --days 30` |
