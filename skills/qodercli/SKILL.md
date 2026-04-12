---
name: qodercli
description: Use Qoder CLI (qodercli) for AI-powered coding tasks, automation, and CI/CD integration. Covers TUI interactive mode, Print non-interactive mode, slash commands, subagents, skills, hooks, MCP, permissions, worktree, memory, ACP protocol, and Qoder Action for GitHub. Trigger this skill whenever the user mentions qodercli, Qoder CLI, qoder print mode, qoder automation, qoder headless mode, qoder hooks, qoder subagents, qoder skills, qoder MCP, qoder ACP, qoder worktree, or asks how to use qodercli for any coding or automation task. Also use when the user wants to integrate AI coding into CI/CD pipelines, automate code reviews, or set up AI-assisted GitHub workflows with Qoder.
---

# Qoder CLI Skill

Qoder CLI (`qodercli`) is an AI-powered command-line coding assistant. It supports two primary modes: **TUI (Interactive)** for hands-on development and **Print (Non-Interactive)** for automation and CI/CD. This skill guides you through all features with emphasis on Print mode for scripting and pipeline integration.

## Quick Reference: Two Modes

| Mode | Command | Use When |
|------|---------|----------|
| **TUI (Interactive)** | `qodercli` | Hands-on development, exploring code, real-time Q&A |
| **Print (Non-Interactive)** | `qodercli -p "prompt"` | Automation, scripting, CI/CD, batch processing |

---

## Installation & Authentication

### Install

```bash
# macOS / Linux (cURL)
curl -fsSL https://qoder.com/install | bash

# macOS / Linux (Homebrew)
brew install qoderai/qoder/qodercli --cask

# All platforms (NPM)
npm install -g @qoder-ai/qodercli
```

Verify: `qodercli --version`

### Authenticate

**Interactive (recommended):**
```bash
qodercli
# then type /login
```

**Environment variable (for automation/CI-CD):**
```bash
export QODER_PERSONAL_ACCESS_TOKEN="your_token_here"
```

Get tokens at: `https://qoder.com/account/integrations`

If both `/login` and env var are set, `/login` token takes precedence.

### Upgrade

```bash
# Any method
curl -fsSL https://qoder.com/install | bash -s -- --force   # cURL
brew update && brew upgrade                                   # Homebrew
npm install -g @qoder-ai/qodercli                            # NPM
qodercli update                                               # Built-in
```

Disable auto-updates in `~/.qoder.json`:
```json
{ "autoUpdates": false }
```

---

## TUI Mode (Interactive)

Run `qodercli` in any project directory to start the interactive TUI.

### Input Modes

| Prefix | Mode | Description |
|--------|------|-------------|
| `>` | Conversation (default) | Chat with the AI |
| `!` | Bash | Run shell commands directly |
| `/` | Slash commands | Built-in and custom commands |
| `#` | Memory | Append to AGENTS.md |
| `\ ⏎` | Multi-line | Enter multi-line text |

### Key Slash Commands

| Command | Description |
|---------|-------------|
| `/login` | Log into Qoder account |
| `/logout` | Log out |
| `/init` | Generate AGENTS.md from project analysis |
| `/memory` | Edit AGENTS.md memory file |
| `/quest` | Spec-based task delegation with subagents |
| `/review` | Review local code changes |
| `/resume` | Resume a previous session |
| `/clear` | Clear session history |
| `/compact` | Compress conversation context |
| `/model` | Switch AI model tier |
| `/agents` | Manage subagents |
| `/skills` | Manage skills |
| `/bashes` | View background bash tasks |
| `/config` | View system configuration |
| `/status` | View session status |
| `/usage` | View credits consumption |
| `/vim` | Open external editor |
| `/quit` | Exit TUI |
| `/help` | Show help |

### TUI Launch Options

| Option | Description | Example |
|--------|-------------|---------|
| `-w` | Workspace directory | `qodercli -w /path/to/project` |
| `-c` | Continue last session | `qodercli -c` |
| `-r` | Resume specific session | `qodercli -r <session-id>` |
| `--allowed-tools` | Restrict to specific tools | `qodercli --allowed-tools=READ,WRITE` |
| `--disallowed-tools` | Prohibit specific tools | `qodercli --disallowed-tools=BASH` |
| `--max-turns` | Limit conversation turns | `qodercli --max-turns=10` |
| `--yolo` | Skip all permission checks | `qodercli --yolo` |

---

## Print Mode (Non-Interactive) - Key Feature

Print mode runs qodercli without any human interaction. Output is printed in the specified format, making it ideal for scripting, automation, and CI/CD pipelines.

### Basic Usage

```bash
# Simple prompt
qodercli -p "explain this codebase"

# With quiet mode (suppresses TUI elements)
qodercli -q -p "fix the bug in main.py"

# Specify workspace
qodercli -w /path/to/project -p "add unit tests for auth module"

# Continue last session in print mode
qodercli -c -p "now add integration tests"

# Resume specific session
qodercli -r <session-id> -p "continue the refactoring"
```

### Output Formats

Control output format with `--output-format`:

| Format | Description | Use When |
|--------|-------------|----------|
| `text` | Plain text (default) | Human-readable output, simple scripts |
| `json` | Structured JSON | Programmatic parsing, integrations |
| `stream-json` | Streaming JSON lines | Real-time processing, progressive display |

```bash
# JSON output for programmatic consumption
qodercli --output-format=json -p "list all TODO comments in the codebase"

# Streaming JSON for real-time processing
qodercli --output-format=stream-json -p "refactor the auth module"
```

### Print Mode with Tool Control

```bash
# Read-only analysis (safe for CI)
qodercli --allowed-tools=READ,GREP,GLOB -p "analyze code quality"

# No bash execution (security-safe)
qodercli --disallowed-tools=BASH -p "review the changes"

# Limit turns for cost control
qodercli --max-turns=5 -p "write a simple hello world"

# Yolo mode for fully automated pipelines
qodercli --yolo -p "fix all linting errors and commit"
```

### CI/CD Integration Patterns

**GitHub Actions example:**
```yaml
- name: AI Code Review
  env:
    QODER_PERSONAL_ACCESS_TOKEN: ${{ secrets.QODER_TOKEN }}
  run: |
    qodercli -w . --output-format=json \
      --allowed-tools=READ,GREP,GLOB \
      -p "/review 重点检查安全漏洞和性能问题"
```

**Git pre-commit hook:**
```bash
#!/bin/bash
qodercli -q -p "check staged files for obvious bugs" \
  --allowed-tools=READ,GREP,GLOB \
  --max-turns=3
```

**Batch processing script:**
```bash
#!/bin/bash
for dir in ~/projects/*/; do
  qodercli -w "$dir" -q -p "/init" --output-format=text
done
```

### Using Slash Commands in Print Mode

Only **Prompt-type** commands work in Print mode: `/init`, `/review`, `/quest`:

```bash
# Run a review
qodercli -p '/review'

# Review with specific focus
qodercli -p '/review 重点检查注释覆盖情况'

# Initialize project memory
qodercli -p '/init'

# Quest-based development
qodercli -p '/quest 实现用户认证功能'
```

---

## Model Configuration

Switch models with `/model` in TUI or `--model` flag:

```bash
qodercli --model lite        # Free tier, simple tasks
qodercli --model efficient   # Low cost, daily coding
qodercli --model auto        # Default, complex tasks
qodercli --model performance # Hard engineering problems
qodercli --model ultimate    # Maximum performance
```

| Tier | Credits | Best For |
|------|---------|----------|
| Lite | Free | Simple Q&A, lightweight tasks |
| Efficient | Low | Daily coding, completion |
| Auto | Standard | Complex tasks, multi-step reasoning |
| Performance | Higher | Large codebases, hard problems |
| Ultimate | Highest | Best results regardless of cost |

Custom models (via own API keys) are available for paid subscribers via `/model` > Custom tab.

---

## Subagents

Subagents are specialized AI agents with independent context, system prompts, and tool permissions.

### Built-in Subagents

| Name | Purpose |
|------|---------|
| `code-reviewer` | Code review |
| `design-agent` | Software design, design docs |
| `general-purpose` | General tasks |
| `task-executor` | Development from design docs |

### Invoking Subagents

```bash
# Explicit (TUI or Print)
> 使用 code-reviewer subagent 进行代码审查

# Implicit - just describe the task
> 帮我审查这段代码

# Chained - multiple subagents in sequence
> 先使用 design-agent 完成系统设计，再使用 code-reviewer subagent 审查代码

# Print mode
qodercli -p "使用 code-reviewer subagent 审查 src/ 下的代码" --max-turns 10
```

### Creating Custom Subagents

Create a `.md` file at `~/.qoder/agents/<name>.md` (user-level) or `.qoder/agents/<name>.md` (project-level):

```markdown
---
name: api-reviewer
description: Review API designs for RESTful compliance and best practices
tools: Read,Grep,Glob
---

You are an expert API design reviewer specializing in RESTful architecture...

When reviewing APIs, focus on:
1. Resource naming conventions
2. HTTP methods compliance
3. Status codes usage
4. URL structure
5. Response format consistency
```

Or use `/agents` in TUI for AI-assisted generation.

---

## Skills

Skills package professional knowledge into reusable functions. Each skill is a directory with a `SKILL.md`.

### Storage

| Level | Path | Scope |
|-------|------|-------|
| User | `~/.qoder/skills/{name}/SKILL.md` | All projects |
| Project | `.qoder/skills/{name}/SKILL.md` | Current project |

### Using Skills

```bash
# Auto-trigger: just describe your need
> 分析日志中的错误模式    # model picks the right skill

# Manual trigger
> /log-analyzer
```

### Creating a Skill

```bash
mkdir -p ~/.qoder/skills/my-skill
```

Write `SKILL.md`:

```markdown
---
name: my-skill
description: What this skill does and when to use it. Include trigger keywords.
---

# Skill Name

## Instructions
Step-by-step guidance here.
```

Key: `description` determines when the model auto-triggers the skill. Be specific and include relevant keywords.

### Skill Directory Structure

```
my-skill/
├── SKILL.md           # Required
├── REFERENCE.md       # Optional: detailed docs
├── EXAMPLES.md        # Optional: usage examples
├── scripts/           # Optional: helper scripts
└── templates/         # Optional: template files
```

---

## Hooks

Hooks insert custom logic at key execution points. They are **deterministic** — scripts always execute, unlike prompt instructions which are subject to model interpretation.

For detailed hook events, matcher rules, script writing, and examples, read [references/hooks.md](references/hooks.md).

### Quick Hook Setup

Configuration files (increasing priority):
1. `~/.qoder/settings.json`
2. `${project}/.qoder/settings.json`
3. `${project}/.qoder/settings.local.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.qoder/hooks/block-dangerous.sh",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### Key Hook Events

| Event | Trigger | Can Block? |
|-------|---------|------------|
| `PreToolUse` | Before tool execution | Yes |
| `PostToolUse` | After tool succeeds | No |
| `PostToolUseFailure` | After tool fails | No |
| `Stop` | Agent finishes response | Yes |
| `SessionStart` | Session begins | No |
| `UserPromptSubmit` | After prompt submit | No |

---

## MCP (Model Context Protocol) Integration

```bash
# Add an MCP service
qodercli mcp add playwright -- npx -y @playwright/mcp@latest

# Add with type and scope
qodercli mcp add context7 -t stdio -s user -- npx -y @upstash/context7-mcp@latest

# List MCP services
qodercli mcp list

# Remove MCP service
qodercli mcp remove playwright
```

MCP types: `stdio`, `sse`, `streamable-http`

Configuration files:
| File | Scope |
|------|-------|
| `~/.qoder.json` | User-level |
| `${project}/.mcp.json` | Project-level |

Recommended MCP tools:
```bash
qodercli mcp add context7 -- npx -y @upstash/context7-mcp@latest
qodercli mcp add deepwiki -- npx -y mcp-deepwiki@latest
```

---

## Permissions System

Three strategies: **Allow**, **Deny**, **Ask** (prompt for confirmation).

Configuration files (increasing priority):
1. `~/.qoder/settings.json`
2. `.qoder/settings.json`
3. `.qoder/settings.local.json`

```json
{
  "permissions": {
    "allow": [
      "Read(/Users/me/project/**)",
      "Edit(/Users/me/project/**)",
      "Bash(npm run test:*)"
    ],
    "deny": [
      "Bash(rm -rf:*)"
    ],
    "ask": [
      "Read(!/Users/me/project/**)"
    ]
  }
}
```

Rule types: `Read`, `Edit` (file access), `WebFetch(domain:...)`, `Bash(command:*)`

---

## Worktree (Parallel Tasks)

Worktrees create isolated git worktrees for concurrent task execution without file conflicts.

```bash
# Create and start a worktree task
qodercli --worktree "implement user authentication"

# With print mode (container stops when done)
qodercli --worktree "fix bug #123" -p "fix the login bug"

# Specify branch
qodercli --worktree "add tests" --branch feature/tests

# View all tasks
qodercli jobs --worktree

# Delete a task
qodercli rm <jobId>
```

---

## Memory System (AGENTS.md)

AGENTS.md is automatically loaded into context to guide the AI.

| Location | Scope |
|----------|-------|
| `~/.qoder/AGENTS.md` | User-level (all projects) |
| `${project}/AGENTS.md` | Project-level |

Generate with `/init` in TUI, or edit manually. Type `#` in TUI for quick memory edits.

---

## ACP (Agent Client Protocol)

ACP enables integration with editors like Zed.

```bash
# Start ACP server
qodercli --acp
```

**Zed IDE configuration** (macOS/Linux):
```json
{
  "agent_servers": {
    "Qoder CLI": {
      "type": "custom",
      "command": "qodercli",
      "args": ["--acp"]
    }
  }
}
```

With environment variable authentication:
```json
{
  "agent_servers": {
    "Qoder CLI": {
      "env": {
        "QODER_PERSONAL_ACCESS_TOKEN": "your_token"
      },
      "command": "qodercli",
      "args": ["--acp"]
    }
  }
}
```

---

## Qoder Action (GitHub Integration)

Automated PR review and `@qoder` interactive assistance in GitHub.

**Quick setup:** Run `/setup-github` in qodercli.

**Manual setup:** Install qoderai GitHub App > Add `QODER_PERSONAL_ACCESS_TOKEN` to repo secrets > Add workflow YAML to `.github/workflows/`.

For detailed Qoder Action configuration, see [references/qoder-action.md](references/qoder-action.md).

---

## Custom Commands

Commands extend slash functionality via `.md` files.

| Level | Path |
|-------|------|
| Project | `.qoder/commands/<name>.md` |
| User | `~/.qoder/commands/<name>.md` |

```markdown
---
description: "Run design then code review workflow"
---

先使用 design-agent subagent 完成系统设计，再使用 code-reviewer subagent 完成代码review
```

Use in TUI: `/quest` (or whatever name you gave the file).

Must restart CLI after adding/modifying command files.

---

## Common Patterns

### Automated Code Review Pipeline

```bash
# Print mode review with JSON output
qodercli -q --output-format=json \
  --allowed-tools=READ,GREP,GLOB \
  -p "/review 检查安全漏洞和代码规范"
```

### Project Initialization

```bash
# Generate AGENTS.md from project analysis
qodercli -p "/init"

# In CI: initialize and review
qodercli -w . -p "/init" && qodercli -p "/review"
```

### Safe Read-Only Analysis

```bash
qodercli --allowed-tools=READ,GREP,GLOB \
  -p "analyze the architecture and suggest improvements"
```

### Automated Fix Pipeline

```bash
qodercli --yolo --max-turns=10 \
  -p "fix all TypeScript compilation errors in the project"
```
