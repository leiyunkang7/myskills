# Skills Advanced Reference

This file provides detailed guidance for creating, configuring, and managing skills in Codebuddy CLI.

---

## SKILL.md Frontmatter Fields

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `name` | No | Directory name | Skill identifier |
| `description` | No | - | Skill description, determines auto-trigger behavior. Be specific and include trigger keywords. |
| `allowed-tools` | No | All tools | Tool whitelist, comma-separated. Supports patterns. |
| `disable-model-invocation` | No | `false` | When `true`, skill won't appear in Skill tool; only triggered via `/skill-name` |
| `user-invocable` | No | `true` | When `false`, hidden from `/` menu; only for AI internal calls or other skill references |
| `context` | No | - | When set to `fork`, skill executes in an isolated subagent context |
| `agent` | No | - | Specifies subagent type; only effective when `context: fork` |

## Tool Permission Patterns

```yaml
# Simple tool list
allowed-tools: Read, Write, Bash

# Git-only bash commands
allowed-tools: Bash(git:*)

# Specific git subcommands
allowed-tools: Bash(git:status,git:diff)

# Path-restricted editing
allowed-tools: Edit(src/**/*.ts)

# Combined
allowed-tools: Read, Write, Bash(git:*), Grep
```

## Context Fork

`context: fork` makes a skill run in an isolated subagent context without access to conversation history.

```yaml
---
name: deep-research
description: Deep research on a topic
context: fork
agent: Explore
---

Research $ARGUMENTS:
1. Use Glob and Grep to find related files
2. Read and analyze the code
3. Summarize findings with specific file references
```

### Available Agent Types

| Type | Description |
|------|-------------|
| `general-purpose` | General-purpose agent (default) |
| `Explore` | Read-only tools, optimized for codebase exploration |
| `Plan` | Planning and analysis agent |
| Custom | Agents defined in `.codebuddy/agents/` |

### Execution Flow
1. Creates a new isolated context
2. Subagent receives Skill content as a prompt
3. The `agent` field determines the execution environment
4. Results return to the main conversation

Best for: Skills with clear, well-defined tasks. Not suitable for vague guidelines.

## Hidden Skills (user-invocable: false)

Use cases:
- Background knowledge Skills (project specs, coding standards)
- Auxiliary Skills only referenced by other Skills or AI internally

```yaml
---
name: project-guidelines
description: Project coding standards and best practices
user-invocable: false
---

# Project Coding Standards
- Use TypeScript strict mode
- Function naming: camelCase
- Component naming: PascalCase
```

Such Skills are loaded into AI context but cannot be directly invoked via the `/` menu.

## Shell Command Execution in Skills

Use `` !`command` `` syntax. Commands execute and their output replaces the command in the Skill content.

**Supported features:**
- `$ARGUMENTS` parameter replacement (before shell execution)
- `@file` file references (processed after shell commands)
- Error isolation: individual command failures don't affect others

**Processing pipeline**: `$ARGUMENTS` replacement → `!command` execution → `@file` reference processing

**Important**: When using shell commands, you MUST include `Bash` in `allowed-tools` frontmatter.

## How AI Selects Skills

The AI decides whether to invoke a skill based on:
1. **Task match**: Relevance between task description and skill's `description`
2. **Tool requirements**: Whether required tools fall within `allowed-tools`
3. **Context relevance**: Whether current conversation context is appropriate
4. **Skill source**: Project-level skills take priority over user-level skills

## Skill vs Slash Command Comparison

| Feature | Skills | Slash Commands |
|---------|--------|----------------|
| **Trigger method** | AI model auto-identifies and invokes | User manually types command |
| **Use case** | Professional domain task processing | Quick operations and workflows |
| **Permission control** | Supports tool whitelist restrictions | No special permission control |
| **Working directory** | Supports custom base directory | Uses current working directory |
| **Visibility** | Transparent to user, AI decides | User-initiated |

## Best Practices

1. **Clear descriptions** - The `description` field is the primary triggering mechanism. Be specific and include keywords.
2. **Reasonable tool permissions** - Only grant necessary permissions: `allowed-tools: Read, Bash(git:status,git:diff), Grep`
3. **Organize by domain** - Use subdirectories for related skills
4. **Detailed instructions** - Provide core capabilities, standard workflows, available tools, common scenarios, and output formats
5. **Explain the why** - Tell the model why things are important rather than heavy-handed MUSTs

## Skill Directory Examples

```
.codebuddy/skills/
├── document/
│   ├── pdf/SKILL.md
│   └── markdown/SKILL.md
├── data/
│   ├── analysis/SKILL.md
│   └── visualization/SKILL.md
└── code/
    ├── review/SKILL.md
    └── refactor/SKILL.md
```
