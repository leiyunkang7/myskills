# Qoder CLI Hooks - Complete Reference

Hooks insert custom logic at key execution points. Unlike prompt instructions, hooks are **deterministic** — scripts always execute when an event triggers, unaffected by model interpretation variance.

## Configuration Files

Hooks load from three locations (merged, all executed together):

| Location | Scope | Notes |
|---|---|---|
| `~/.qoder/settings.json` | User-level | Applies to all projects |
| `${project}/.qoder/settings.json` | Project-level | Can commit to git for team sharing |
| `${project}/.qoder/settings.local.json` | Project-local | Highest priority; add to `.gitignore` |

## Configuration Format

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "MatchCondition",
        "hooks": [
          {
            "type": "command",
            "command": "script-to-execute",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

| Field | Required | Description |
|---|---|---|
| `type` | Yes | Fixed: `"command"` |
| `command` | Yes | Shell command to execute |
| `timeout` | No | Timeout in seconds (default: 60) |
| `matcher` | No | Match condition; omit to match all |

## Matcher Rules

| Syntax | Meaning | Example |
|---|---|---|
| Omitted or `"*"` | Match all | All tools trigger |
| Exact value | Exact match | `"Bash"` |
| `\|` separator | Match multiple | `"Write\|Edit"` |
| Regex | Pattern match | `"mcp__.*"` |

## Hook Script Writing

Scripts receive JSON input via **stdin** and control behavior via **exit code** and **stdout/stderr**.

### Common Input Fields

| Field | Description |
|---|---|
| `session_id` | Current session ID |
| `cwd` | Current working directory |
| `hook_event_name` | Name of the triggered event |

### Parsing Pattern

```bash
#!/bin/bash
input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name')
```

### Exit Code Behavior

| Exit Code | Behavior |
|---|---|
| `0` | Success; `stdout` is parsed |
| `2` | **Block operation**; `stderr` is injected into conversation as feedback |
| Other | Non-blocking error; `stdout` ignored |

### Environment Variables

| Variable | Description |
|---|---|
| `QODER_PROJECT_DIR` | Current project working directory |

## Complete Hook Events

| Event | Trigger | Can Block | Matcher Target |
|---|---|---|---|
| `SessionStart` | Session begins | No | Session source |
| `SessionEnd` | Session ends | No | End reason |
| `UserPromptSubmit` | After prompt submit, before Agent processes | No | — |
| `PreToolUse` | Before tool execution | **Yes** | Tool name |
| `PostToolUse` | After tool executes successfully | No | Tool name |
| `PostToolUseFailure` | After tool execution fails | No | Tool name |
| `Stop` | Agent finishes, no pending tool calls | **Yes** | — |
| `SubagentStart` | Sub-agent starts | No | Agent type name |
| `SubagentStop` | Sub-agent completes | **Yes** | Agent type name |
| `PreCompact` | Before context compaction | No | Trigger method |
| `Notification` | Notification event | No | Notification type |
| `PermissionRequest` | Tool requires authorization | No | Tool name |

### SessionStart

Matcher matches session source: `startup`, `resume`, `compact`

Extra input:
```json
{ "source": "startup", "model": "Auto" }
```

### SessionEnd

Matcher matches end reason: `prompt_input_exit`, `other`

Extra input:
```json
{ "reason": "prompt_input_exit" }
```

### UserPromptSubmit

Extra input:
```json
{ "prompt": "user's prompt text" }
```

### PreToolUse (Can Block)

Matcher matches tool name (e.g., `Bash`, `Write`, `Edit`, `Read`, `Glob`, `Grep`; MCP tools: `mcp__server__tool`)

Extra input:
```json
{
  "tool_name": "Bash",
  "tool_input": {"command": "rm -rf /tmp/build"},
  "tool_use_id": "toolu_01ABC123"
}
```

Exit code `2` blocks execution; `stderr` returned to Agent as error message.

### PostToolUse

Extra input:
```json
{
  "tool_name": "Write",
  "tool_input": {"file_path": "/path/to/file.ts", "content": "..."},
  "tool_response": "File written successfully",
  "tool_use_id": "toolu_01ABC123"
}
```

### PostToolUseFailure

Extra input:
```json
{
  "tool_name": "Bash",
  "tool_input": {"command": "npm test"},
  "tool_use_id": "toolu_01ABC123",
  "error": "Command exited with non-zero status code 1",
  "is_interrupt": false
}
```

### Stop (Can Block)

Exit code `2` injects `stderr` into conversation, Agent continues.

### SubagentStart / SubagentStop

Matcher matches agent type name.

Extra input:
```json
{ "agent_id": "a1b2c3d4", "agent_type": "task" }
```

### PreCompact

Matcher matches trigger: `manual`, `auto`

Extra input:
```json
{ "trigger": "manual", "custom_instructions": "keep all tool call results" }
```

### Notification

Matcher matches notification type: `permission`, `result`

Extra input:
```json
{
  "message": "Agent is requesting permission to run: rm -rf node_modules",
  "title": "Permission Required",
  "notification_type": "permission"
}
```

### PermissionRequest

Matcher matches tool name.

Extra input:
```json
{
  "tool_name": "Bash",
  "tool_input": {"command": "rm -rf node_modules"}
}
```

## Example: Block Dangerous Commands

Script (`~/.qoder/hooks/block-rm.sh`):
```bash
#!/bin/bash
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command')

if echo "$command" | grep -q 'rm -rf'; then
  echo "Dangerous command blocked: $command" >&2
  exit 2
fi
exit 0
```

Configuration:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "~/.qoder/hooks/block-rm.sh" }]
      }
    ]
  }
}
```

## Example: Auto-Lint After File Write/Edit

Script (`.qoder/hooks/auto-lint.sh`):
```bash
#!/bin/bash
input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path')

case "$file_path" in
  *.js|*.ts|*.jsx|*.tsx)
    npx eslint "$file_path" --fix 2>/dev/null
    ;;
esac
exit 0
```

Configuration:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": ".qoder/hooks/auto-lint.sh" }]
      }
    ]
  }
}
```

## Example: Auto-Continue on Uncommitted Changes

Script (`~/.qoder/hooks/check-continue.sh`):
```bash
#!/bin/bash
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
  echo "Uncommitted changes detected, please complete git commit" >&2
  exit 2
fi
exit 0
```

Configuration:
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [{ "type": "command", "command": "~/.qoder/hooks/check-continue.sh" }]
      }
    ]
  }
}
```

## Example: Desktop Notifications (macOS)

Script (`~/.qoder/hooks/notify.sh`):
```bash
#!/bin/bash
input=$(cat)
message=$(echo "$input" | jq -r '.message')

if echo "$message" | grep -q "^Agent"; then
  osascript -e 'display notification "Task completed" with title "Qoder CLI"'
else
  osascript -e 'display notification "Permission required" with title "Qoder CLI"'
fi
exit 0
```

Configuration:
```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [{ "type": "command", "command": "~/.qoder/hooks/notify.sh" }]
      }
    ]
  }
}
```
