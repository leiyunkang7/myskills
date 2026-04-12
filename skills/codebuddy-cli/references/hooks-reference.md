# Hooks Complete Reference

This file provides the full detailed reference for Codebuddy CLI hooks system. Read this when you need specific hook event details, JSON input/output schemas, matcher patterns, or prompt hooks.

---

## Hook Events - Complete Detail

### PreToolUse

Runs **after** Codebuddy creates tool parameters but **before** processing the tool call.

**Common matchers**: `Task`, `Bash`, `Glob`, `Grep`, `Read`, `Edit`, `Write`, `WebFetch`, `WebSearch`, `mcp__*`

**Input JSON:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  }
}
```

**Output (exit code 2 or JSON `continue: false`)**: Blocks the tool call.

**JSON output for permission decision:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "Reason shown in permission dialog",
    "modifiedInput": {
      "field_to_modify": "new value"
    }
  }
}
```

- `"allow"`: Bypass permission system, execute tool directly
- `"deny"`: Block tool call
- `"ask"`: Require user confirmation in UI
- `modifiedInput`: Partially override tool input parameters before execution

### PostToolUse

Runs immediately after a tool **successfully** completes. Same matchers as PreToolUse.

**Input JSON** includes `tool_response` field in addition to PreToolUse fields:
```json
{
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  }
}
```

**JSON output for context injection:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Extra info for Codebuddy, e.g., code style check results"
  }
}
```

### UserPromptSubmit

Runs after user submits a prompt, **before** Codebuddy processes it. No matcher support.

**Input JSON:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "The user's prompt text"
}
```

**Output to block prompt:**
```json
{
  "continue": false,
  "reason": "Block reason shown to user only",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "Extra context injected to Codebuddy"
  }
}
```

### Stop / SubagentStop

`Stop`: Main agent finishes responding. `SubagentStop`: Sub-agent finishes. Neither runs on user interruption.

**Input JSON:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "permission_mode": "default",
  "hook_event_name": "Stop",
  "stop_hook_active": true
}
```

`stop_hook_active` is `true` when Codebuddy has already continued from a previous stop hook.

**Output to block stopping:**
```json
{
  "continue": false,
  "reason": "Tell Agent why it needs to continue"
}
```

### Notification

Runs when Codebuddy sends a notification. Supports matchers: `permission_prompt`, `idle_prompt`, `auth_success`.

**Input JSON:**
```json
{
  "session_id": "abc123",
  "message": "Codebuddy needs your permission to use Bash",
  "notification_type": "permission_prompt"
}
```

### PreCompact

Runs before context compression. Matchers: `manual` (from `/compact`), `auto` (automatic compression).

**Input JSON:**
```json
{
  "trigger": "manual",
  "custom_instructions": "User input from /compact command"
}
```

### SessionStart

Runs when session starts. Matchers: `startup`, `resume`, `clear`, `compact`.

**Output for context injection:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "My additional context here"
  }
}
```

### SessionEnd

Runs when session ends. Reason values: `clear`, `logout`, `prompt_input_exit`, `other`.

---

## Matcher Patterns

| Pattern | Behavior |
|---------|----------|
| `Write` | Matches any tool name containing "Write" (e.g., `Write`, `NotebookWrite`) |
| `^Write$` | Exact match - only `Write` tool |
| `Edit\|Write` | Multiple tools (pipe-separated regex) |
| `Web.*` | Regex pattern matching |
| `*` or `""` or omitted | Match all tools |

For non-tool events (`UserPromptSubmit`, `Stop`, etc.), omit the `matcher` field.

## Exit Codes

| Exit Code | Meaning | Behavior |
|-----------|---------|----------|
| **0** | Success | stdout shown in transcript mode |
| **2** | Blocking error | Message from stdout JSON `reason`/`stopReason` field or plain text; stderr as fallback |
| **Other** | Non-blocking error | stderr shown to user; execution continues |

## Prompt Hooks (`type: "prompt"`)

Instead of shell commands, prompt hooks query a fast LLM for context-aware decisions. Only for `Stop`, `UserPromptSubmit`, `PreToolUse` events.

**Configuration:**
```json
{
  "type": "prompt",
  "prompt": "Evaluate if Codebuddy should stop: $ARGUMENTS. Check if all tasks are complete.",
  "timeout": 30
}
```

**LLM Response Format:**
```json
{
  "ok": true | false,
  "reason": "Explanation for the decision"
}
```

## Common JSON Output Fields

Available for all hook types:

```json
{
  "continue": true,
  "stopReason": "string",
  "reason": "string",
  "suppressOutput": true,
  "systemMessage": "string"
}
```

- `stopReason`/`reason`: Passed to Codebuddy Agent
- `systemMessage`: Shown only to user, never to Agent

## Security Best Practices

1. Validate and sanitize input - never blindly trust hook input data
2. Always quote shell variables - use `"$VAR"` not `$VAR`
3. Block path traversal - check for `..` in file paths
4. Use absolute paths for scripts
5. Skip sensitive files (.env, .git/, keys)

## Execution Details

- **Default timeout**: 60 seconds (configurable per command)
- **Parallelization**: All matching hooks run in parallel
- **Deduplication**: Identical hook commands are deduplicated
- **Shell**: User's default shell on macOS/Linux; Git Bash on Windows
- **Environment**: `CODEBUDDY_PROJECT_DIR` contains project root path
