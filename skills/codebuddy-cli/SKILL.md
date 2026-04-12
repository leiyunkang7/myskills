---
name: codebuddy-cli
description: Use Codebuddy CLI (codebuddy/cbc) for AI-powered coding, automation, and CI/CD integration. Covers TUI interactive mode, Print non-interactive mode, slash commands, subagents, skills, hooks, MCP, permissions, worktree, memory, and CI/CD pipelines. Trigger this skill whenever the user mentions codebuddy, Codebuddy CLI, cbc, codebuddy print mode, codebuddy automation, codebuddy headless mode, codebuddy hooks, codebuddy subagents, codebuddy skills, codebuddy MCP, codebuddy worktree, codebuddy memory, or asks how to use codebuddy for any coding or automation task. Also use when the user wants to integrate AI coding into CI/CD pipelines, automate code reviews, set up AI-assisted GitHub/GitLab workflows, or pipe data into an AI coding assistant.
---

# Codebuddy CLI Skill

Codebuddy CLI (`codebuddy` / `cbc`) is an AI-powered command-line coding assistant built on Tencent Cloud AI. It supports two primary modes: **TUI (Interactive)** for hands-on development and **Print (Non-Interactive)** for automation and CI/CD. This skill covers all features with emphasis on Print mode for scripting and pipeline integration.

## Quick Reference: Two Modes

| Mode | Command | Use When |
|------|---------|----------|
| **TUI (Interactive)** | `codebuddy` | Hands-on development, exploring code, real-time Q&A |
| **Print (Non-Interactive)** | `codebuddy -p "prompt"` | Automation, scripting, CI/CD, batch processing |

---

## Installation & Authentication

### Install

```bash
# All platforms (NPM)
npm install -g @tencent-ai/codebuddy-code
```

Requires Node.js 18.0+. Verify: `codebuddy --version`

### Authenticate

**Interactive (recommended):**
```bash
codebuddy
# then type /login
```

**Environment variable (for automation/CI-CD):**
```bash
export CODEBUDDY_PERSONAL_ACCESS_TOKEN="your_token_here"
```

### Upgrade

```bash
npm install -g @tencent-ai/codebuddy-code
codebuddy update          # Built-in updater
```

---

## TUI Mode (Interactive)

Run `codebuddy` in any project directory to start the interactive TUI.

### Input Modes

| Prefix | Mode | Description |
|--------|------|-------------|
| `>` | Conversation (default) | Chat with the AI |
| `!` | Bash | Run shell commands directly |
| `/` | Slash commands | Built-in and custom commands |
| `#` | Memory | Append to CODEBUDDY.md |
| `@` | File reference | Include file content in context |
| `\ ⏎` | Multi-line | Enter multi-line text |

### Key Slash Commands

| Command | Description |
|---------|-------------|
| `/login` `/logout` | Account management |
| `/init` | Generate CODEBUDDY.md from project analysis |
| `/memory` | Manage long-term memory |
| `/agents` | Manage subagents |
| `/skills` | View loaded skills |
| `/review` | Review local code changes |
| `/security-review` | Code security review |
| `/resume` | Resume a previous session |
| `/clear` | Clear session history |
| `/compact` | Compress conversation context |
| `/model` | Switch AI model |
| `/config` | View or modify configuration |
| `/permissions` | Manage tool permissions |
| `/mcp` | Manage MCP connections |
| `/cost` | View session cost and token usage |
| `/export` | Export conversation to file/clipboard |
| `/help` | Show help |

### Permission Modes (Shift+Tab / Alt+M)

| Mode | Description |
|------|-------------|
| **Normal** (default) | Asks for tool use confirmation |
| **Auto-accept Edits** | Auto-approves file edit operations |
| **Bypass Permissions** | Bypasses all permission checks (sandboxed envs only) |
| **Plan Mode** | AI creates a plan and waits for approval |

### Key Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Cancel input/generation |
| `Ctrl+D` | Exit session |
| `Ctrl+L` | Clear terminal |
| `Ctrl+O` | Toggle verbose output |
| `Ctrl+R` | Reverse search history |
| `Ctrl+V` / `Alt+V` | Paste image from clipboard |
| `Shift+Tab` / `Alt+M` | Toggle permission mode |
| `Tab` | Toggle thinking mode |
| `Esc+Esc` | Rewind (when input empty) |
| `Ctrl+B` | Move bash command to background |

---

## Print Mode (Non-Interactive) - Key Feature

Print mode runs codebuddy without any human interaction. Output is printed in the specified format, making it ideal for scripting, automation, and CI/CD pipelines.

### Critical Rule for Print Mode

When using `-p/--print`, any operation requiring tool authorization (file operations, network requests, bash commands, etc.) **must include `--dangerously-skip-permissions`**, otherwise it will be blocked by permission checks.

### Basic Usage

```bash
# Simple prompt
codebuddy -p "explain this codebase"

# With quiet mode (suppresses TUI elements)
codebuddy -q -p "fix the bug in main.py"

# Specify workspace
codebuddy -w /path/to/project -p "add unit tests for auth module"

# Continue last session in print mode
codebuddy -c -p "now add integration tests"

# Resume specific session
codebuddy -r <session-id> -p "continue the refactoring"
```

### Output Formats

Control output format with `--output-format`:

| Format | Description | Use When |
|--------|-------------|----------|
| `text` | Plain text (default) | Human-readable output, simple scripts |
| `json` | Structured JSON (single result) | Programmatic parsing, integrations |
| `stream-json` | Streaming JSON lines | Real-time processing, progressive display |

```bash
# JSON output for programmatic consumption
codebuddy --output-format=json -p "list all TODO comments in the codebase"

# Streaming JSON for real-time processing
codebuddy --output-format=stream-json -p "refactor the auth module"

# Pipe output to file or other tools
cat data.txt | codebuddy -p 'summarize this data' --output-format text > summary.txt
cat code.py | codebuddy -p 'analyze for bugs' --output-format json > analysis.json
```

### Input Formats

Control input format with `--input-format`:

| Format | Description |
|--------|-------------|
| `text` | Plain text input (default) |
| `stream-json` | Streaming JSON lines input |

```bash
# Real-time log analysis with streaming input
tail -f app.log | codebuddy -p "monitor and analyze logs" --input-format stream-json
```

### Print Mode with Tool Control

```bash
# Read-only analysis (safe for CI)
codebuddy --allowedTools=Read,Grep,Glob -p "analyze code quality"

# No bash execution (security-safe)
codebuddy --disallowedTools=Bash -p "review the changes"

# Limit turns for cost control
codebuddy --max-turns=5 -p "write a simple hello world"

# Operations requiring tool authorization (MUST add --dangerously-skip-permissions)
codebuddy -p "fix all linting errors" --dangerously-skip-permissions

# Allow only specific tools with authorization
codebuddy --allowedTools "Read Edit" -p "modify files" --dangerously-skip-permissions

# Allow specific Git operations
codebuddy --allowedTools "Bash(git:status,git:diff)" -p "check git status" --dangerously-skip-permissions

# Plan mode headless query (read-only, no --dangerously-skip-permissions needed)
codebuddy --permission-mode plan -p "analyze the auth system and suggest improvements"
```

### CI/CD Integration Patterns

**GitHub Actions example:**
```yaml
- name: AI Code Review
  env:
    CODEBUDDY_PERSONAL_ACCESS_TOKEN: ${{ secrets.CODEBUDDY_TOKEN }}
  run: |
    codebuddy -w . --output-format=json \
      --allowedTools=Read,Grep,Glob \
      -p "review for security vulnerabilities and performance issues"
```

**Git pre-commit hook:**
```bash
#!/bin/bash
codebuddy -q -p "check staged files for obvious bugs" \
  --allowedTools=Read,Grep,Glob \
  --max-turns=3
```

**Batch processing script:**
```bash
#!/bin/bash
for dir in ~/projects/*/; do
  codebuddy -w "$dir" -q -p "/init" --output-format=text
done
```

**Automated fix pipeline:**
```bash
codebuddy --dangerously-skip-permissions --max-turns=10 \
  -p "fix all TypeScript compilation errors in the project"
```

### UNIX Pipe Integration

Codebuddy follows the UNIX philosophy - pipe-friendly, script-integrable, composable:

```bash
# Analyze git commits
git log --oneline | codebuddy -p "analyze these commits and find potential issues"

# Analyze error logs
cat error.log | codebuddy -p "help me analyze these error logs"

# Generate commit message
git diff --cached | codebuddy -p "generate a commit message" --output-format text --dangerously-skip-permissions

# Code review via pipe
git diff | codebuddy -p "review these code changes"

# Multi-stage processing
find . -name "*.js" | head -5 | xargs cat | codebuddy -p "analyze code patterns"

# Lint validation pipeline (package.json)
# "lint:codebuddy": "codebuddy -p 'You are a linter. Check changes relative to main and report issues with filename and line number.'"
```

### Using Slash Commands in Print Mode

Only **prompt-type** commands work in Print mode: `/init`, `/review`, `/security-review`:

```bash
codebuddy -p '/review'
codebuddy -p '/review focus on security vulnerabilities'
codebuddy -p '/init'
codebuddy -p '/security-review'
```

### Non-Interactive MCP Server Approval

In Print mode, project-scoped MCP servers need explicit approval:

```bash
# Allow all project MCP servers
codebuddy --settings '{"enableAllProjectMcpServers": true}' -p "your prompt"

# Allow specific MCP servers
codebuddy --settings '{"enabledMcpjsonServers": ["server-name"]}' -p "your prompt"
```

---

## Model Configuration

Switch models with `/model` in TUI or `--model` flag:

```bash
codebuddy --model gpt-4 -p "simple task"          # Fast model
codebuddy --model gpt-5 -p "complex analysis"      # Advanced model

# Set fallback model for overload protection
codebuddy --model gpt-5 --fallback-model gpt-4 -p "query"
```

---

## CLI Reference (Complete Flags)

### Global Options

| Flag | Description |
|------|-------------|
| `-V, --version` | Output version number |
| `-h, --help` | Display help |
| `-d, --debug` | Enable debug mode |
| `--verbose` | Verbose output |
| `-p, --print` | Print response and exit (non-interactive) |
| `-q` | Quiet mode (suppress TUI elements) |
| `-w` | Workspace directory |
| `-c, --continue` | Continue most recent conversation |
| `-r, --resume [sessionId]` | Resume specific session |
| `--session-id <uuid>` | Use specific session ID |
| `--model <model>` | Model for current session |
| `--fallback-model <model>` | Fallback model (only with --print) |
| `--output-format <format>` | Output format: text/json/stream-json (only with --print) |
| `--input-format <format>` | Input format: text/stream-json (only with --print) |
| `--permission-mode <mode>` | Permission mode: default/acceptEdits/bypassPermissions/plan |
| `--dangerously-skip-permissions` | Bypass all permission checks (required for -p mode tool usage) |
| `--allowedTools <tools...>` | List of allowed tools |
| `--disallowedTools <tools...>` | List of disallowed tools |
| `--add-dir <directories...>` | Additional directories allowed for tool access |
| `--max-turns <n>` | Limit conversation turns |
| `--mcp-config <fileOrString>` | Load MCP servers from JSON file or string |
| `--strict-mcp-config` | Only use MCP servers from --mcp-config |
| `--ide` | Auto-connect IDE on startup |
| `--settings <json>` | Override settings for this session |

### Subcommands

| Command | Description |
|---------|-------------|
| `codebuddy config list` | List configuration |
| `codebuddy config get <key>` | Get configuration value |
| `codebuddy config set <key> <value>` | Set configuration value |
| `codebuddy mcp list` | List MCP servers |
| `codebuddy mcp add <name> ...` | Add MCP server |
| `codebuddy mcp remove <name>` | Remove MCP server |
| `codebuddy mcp get <name>` | Get MCP server details |
| `codebuddy mcp add-json <name> <json>` | Add MCP via JSON |
| `codebuddy update` | Check for updates |

---

## Subagents

Subagents are specialized AI agents with independent context, system prompts, and tool permissions.

### Using Subagents

```bash
# In TUI - explicit delegation
> 使用 code-reviewer subagent 审查代码

# In TUI - implicit (just describe the task)
> 帮我审查这段代码

# In Print mode
codebuddy -p "使用 code-reviewer subagent 审查 src/ 下的代码" --max-turns 10
```

### Creating Custom Subagents

Create a `.md` file at `~/.codebuddy/agents/<name>.md` (user-level) or `.codebuddy/agents/<name>.md` (project-level):

```markdown
---
name: api-reviewer
description: Review API designs for RESTful compliance
tools: Read,Grep,Glob
---

You are an expert API design reviewer...
```

Or use `/agents` in TUI for AI-assisted generation.

---

## Skills

Skills package professional knowledge into reusable AI capabilities. They are auto-triggered based on task description matching.

### Skill Directory Structure

```
.codebuddy/skills/          # Project-level (shared with team)
~/.codebuddy/skills/        # User-level (all projects)

my-skill/
├── SKILL.md                # Required
├── references/             # Optional: detailed docs
├── scripts/                # Optional: helper scripts
└── templates/              # Optional: template files
```

### SKILL.md Format

```markdown
---
name: my-skill
description: What this skill does and when to trigger it
allowed-tools: Read, Write, Bash
user-invocable: true          # default true; false to hide from / menu
context: fork                 # optional: run in isolated subagent
agent: Explore                # optional: subagent type when context: fork
---

Skill instructions here...
```

### Key Frontmatter Fields

| Field | Description |
|-------|-------------|
| `name` | Skill name (defaults to directory name) |
| `description` | Determines auto-trigger behavior - be specific |
| `allowed-tools` | Tool whitelist with pattern support: `Bash(git:*)`, `Edit(src/**/*.ts)` |
| `user-invocable` | `false` to hide from `/` menu (background knowledge skills) |
| `context` | `fork` to run in isolated subagent context |
| `agent` | Subagent type when `context: fork`: `general-purpose`, `Explore`, `Plan`, or custom |

### Shell Commands in Skills

Use `` !`command` `` syntax for inline shell execution:

```markdown
---
description: Project status analysis
---

### Current directory
!`echo "CWD=$(pwd)"`

### Git status
!`git status --short`

Please analyze the project status based on the above.
```

For detailed skill creation guidance, read [references/skills-advanced.md](references/skills-advanced.md).

---

## Hooks

Hooks insert deterministic custom logic at key execution points. They are shell commands that always execute, unlike prompt instructions.

### Key Hook Events

| Event | Trigger | Can Block? |
|-------|---------|------------|
| `PreToolUse` | Before tool execution | Yes |
| `PostToolUse` | After tool succeeds | No |
| `UserPromptSubmit` | After prompt submit | Yes |
| `Stop` | Agent finishes response | Yes |
| `SubagentStop` | Sub-agent finishes | Yes |
| `Notification` | Permission request / idle | No |
| `PreCompact` | Before context compaction | Yes |
| `SessionStart` | Session created | No |
| `SessionEnd` | Session ends | No |

### Hook Configuration

Configuration files (increasing priority):
1. `~/.codebuddy/settings.json`
2. `${project}/.codebuddy/settings.json`
3. `${project}/.codebuddy/settings.local.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.codebuddy/hooks/block-dangerous.sh",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

Hooks support two types: `command` (shell execution) and `prompt` (LLM-based evaluation). Use `$CODEBUDDY_PROJECT_DIR` to reference project-stored scripts.

For detailed hook events, matcher rules, JSON input/output, and prompt hooks, read [references/hooks-reference.md](references/hooks-reference.md).

---

## MCP (Model Context Protocol) Integration

```bash
# Add an MCP service
codebuddy mcp add playwright -- npx -y @playwright/mcp@latest
codebuddy mcp add --scope user --transport http api-server https://api.example.com/mcp

# List MCP servers
codebuddy mcp list

# Remove MCP server
codebuddy mcp remove playwright
```

### MCP Configuration Files

| File | Scope |
|------|-------|
| `~/.codebuddy/.mcp.json` | User-level (recommended) |
| `${project}/.mcp.json` | Project-level (recommended) |

### Transport Types

| Type | Use When |
|------|---------|
| `stdio` | Local process communication (default) |
| `sse` | Remote Server-Sent Events |
| `http` | Remote HTTP streaming |

### MCP Permission Control

```json
{
  "permissions": {
    "allow": ["mcp__github"],
    "deny": ["mcp__dangerous_server__delete_file"]
  }
}
```

Format: `mcp__<server>` (all tools) or `mcp__<server>__<tool>` (specific tool). No wildcards.

### Deferred Loading

Reduce context consumption for servers with 30+ tools:

```json
{
  "mcpServers": {
    "large-server": {
      "type": "stdio",
      "command": "my-server",
      "defer_loading": true
    }
  }
}
```

For detailed MCP configuration, environment variable expansion, and advanced options, read [references/mcp-reference.md](references/mcp-reference.md).

---

## Memory System

### Memory Hierarchy

| Memory Type | Location | Scope |
|-------------|----------|-------|
| User Memory | `~/.codebuddy/CODEBUDDY.md` | All projects (personal) |
| User Rules | `~/.codebuddy/rules/*.md` | All projects (personal) |
| Project Memory | `./CODEBUDDY.md` or `./.codebuddy/CODEBUDDY.md` | Team-shared |
| Project Rules | `./.codebuddy/rules/*.md` | Team-shared, topic-specific |
| Local Project Memory | `./CODEBUDDY.local.md` | Personal, project-specific |

### Key Operations

```bash
# Generate project memory
codebuddy -p '/init'

# Or in TUI
/init

# Quick memory edit (TUI)
# Type # at start of input

# Manage memory
/memory
```

### Conditional Rules

Rules can be conditionally triggered based on file paths:

```markdown
---
alwaysApply: false
paths: src/api/**/*.ts
---

# API Development Rules
- All endpoints must include input validation
```

### Auto Memory

Auto Memory lets Codebuddy autonomously save persistent memories across sessions. Toggle via `/memory` or `/config`.

---

## Permissions System

Three strategies: **Allow**, **Deny**, **Ask** (prompt for confirmation).

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
    ]
  }
}
```

Configuration files (increasing priority):
1. `~/.codebuddy/settings.json`
2. `.codebuddy/settings.json`
3. `.codebuddy/settings.local.json`

---

## Git Worktree (Parallel Tasks)

Worktrees create isolated git worktrees for concurrent task execution:

```bash
# In TUI
> 使用 worktree 实现用户认证功能

# Multiple parallel sessions
# Terminal 1:
cd ../project-feature-a && codebuddy

# Terminal 2:
cd ../project-bugfix && codebuddy
```

---

## Custom Slash Commands

### Project-Level Commands

```bash
mkdir -p .codebuddy/commands
```

Create `.codebuddy/commands/<name>.md`:

```markdown
---
description: "Code review with focus areas"
argument-hint: "[file-paths...]"
allowed-tools: Read
---

Please review the following files:

@$ARGUMENTS

Focus on: security, performance, maintainability.
```

Use: `/review src/auth.ts`

### Key Frontmatter Fields

| Field | Description |
|-------|-------------|
| `description` | Short description for autocomplete |
| `argument-hint` | Parameter hint text |
| `model` | Specific AI model to use |
| `allowed-tools` | Tool whitelist (e.g., `Bash(git:*)`) |
| `disable-model-invocation` | `true` to hide from Skill tool |

### Parameter Substitution

- Positional: `$1`, `$2`, `$3`
- Capture-all: `$ARGUMENTS`
- Shell execution: `` !`command` ``
- File references: `@path/to/file`

---

## Common Patterns

### Automated Code Review Pipeline

```bash
codebuddy -q --output-format=json \
  --allowedTools=Read,Grep,Glob \
  -p "review for security vulnerabilities and code standards"
```

### Safe Read-Only Analysis

```bash
codebuddy --allowedTools=Read,Grep,Glob \
  -p "analyze the architecture and suggest improvements"
```

### Automated Fix Pipeline

```bash
codebuddy --dangerously-skip-permissions --max-turns=10 \
  -p "fix all TypeScript compilation errors"
```

### Project Initialization

```bash
codebuddy -p "/init"
```

### Validation Pipeline (package.json)

```json
{
  "scripts": {
    "lint:codebuddy": "codebuddy -p 'You are a linter. Check changes relative to main and report issues.'"
  }
}
```

### Extended Thinking

In TUI, use `Tab` to toggle thinking mode, or use keywords like "思考" or "深入思考" in prompts for deeper analysis.

### Resuming Sessions

```bash
codebuddy -c                    # Continue most recent
codebuddy -c -p "show progress" # Continue with prompt
codebuddy -r                    # Interactive session selector
```
