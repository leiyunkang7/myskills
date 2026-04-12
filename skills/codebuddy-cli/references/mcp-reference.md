# MCP Complete Reference

This file provides the full detailed reference for MCP (Model Context Protocol) integration in Codebuddy CLI.

---

## Configuration File Format (JSONC supported)

```jsonc
{
  // MCP server configuration
  "mcpServers": {
    "server-name": {
      "type": "stdio|sse|http",    // Optional, auto-inferred
      "command": "command path",    // For stdio
      "args": ["arg1", "arg2"],     // For stdio
      "env": { "ENV_VAR": "value" },// For stdio
      "url": "http://example.com/mcp", // For sse/http
      "headers": { "Authorization": "Bearer token" }, // For sse/http
      "description": "Server description",
      "defer_loading": false,       // Defer tool loading
      "tools": {                    // Tool-level config override
        "tool_name": { "defer_loading": false }
      }
    }
  },
  "disabledMcpServers": ["deprecated-server"],
  "projects": {                     // Local-scope (user file only)
    "/path/to/project": {
      "mcpServers": {
        "local-server": { "type": "stdio", "command": "./local-tool" }
      }
    }
  }
}
```

## Configuration File Locations

| Scope | Path (Recommended) | Priority |
|-------|---------------------|----------|
| **User** | `~/.codebuddy/.mcp.json` | Lowest |
| **Project** | `<project_root>/.mcp.json` | Medium |
| **Local** | In user file under `projects` field | Highest |

Within same scope, only the first existing file is used (no merging).

## Transport Types

### STDIO Type

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Fixed value `"stdio"` |
| `command` | string | Yes | Executable path or command |
| `args` | Array\<string\> | No | Command-line arguments |
| `env` | Object | No | Environment variables |
| `defer_loading` | boolean | No | Defer tool loading (default `false`) |
| `tools` | Object | No | Tool-level config override |

### SSE Type

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Fixed value `"sse"` |
| `url` | string | Yes | SSE endpoint URL |
| `headers` | Object | No | HTTP request headers |
| `defer_loading` | boolean | No | Defer tool loading |
| `tools` | Object | No | Tool-level config override |

### HTTP Type

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Fixed value `"http"` |
| `url` | string | Yes | HTTP endpoint URL |
| `headers` | Object | No | HTTP request headers |
| `defer_loading` | boolean | No | Defer tool loading |
| `tools` | Object | No | Tool-level config override |

## Environment Variable Expansion

| Syntax | Behavior |
|--------|----------|
| `${VAR_NAME}` | Expands to the value of VAR_NAME |
| `${VAR_NAME:-default_value}` | Uses default if VAR_NAME is unset |

**Variable naming rules**: Must start with uppercase letter or underscore `[A-Z_]`, subsequent `[A-Z0-9_]*`.

**Supported fields**:
- STDIO: `command`, `args` (each item), `env` (values only)
- SSE/HTTP: `url`, `headers` (values only)

**Error handling**: Unset variable with default → uses default; unset without default → preserves placeholder, reports WARNING.

## Deferred Loading

Reduces context consumption for servers with many tools (30+).

**Server-level (all tools deferred):**
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

**Tool-level override:**
```json
{
  "mcpServers": {
    "large-server": {
      "type": "stdio",
      "command": "my-server",
      "defer_loading": true,
      "tools": {
        "frequently_used_tool": { "defer_loading": false }
      }
    }
  }
}
```

**Inheritance:**

| Server `defer_loading` | Tool `defer_loading` | Result |
|------------------------|----------------------|--------|
| `true` | Not set | `true` (inherited) |
| `true` | `false` | `false` (overridden) |
| `false`/not set | Not set | `false` |
| `false`/not set | `true` | `true` (overridden) |

## MCP Permission Control

Three rule types by priority: `deny` > `ask` > `allow`. No wildcards supported.

**Permission format:**
- Server-level: `mcp__server_name` (matches any tool from that server)
- Tool-level: `mcp__server_name__tool_name` (matches a specific tool)

```json
{
  "permissions": {
    "allow": ["mcp__github"],
    "deny": ["mcp__dangerous_server__delete_file"]
  }
}
```

## MCP Prompts Integration

MCP servers can provide Prompts (prompt templates) that auto-convert to Codebuddy slash commands:
- Auto-register as `/server_name:prompt_name`
- Supports dynamic parameters via interactive UI
- Real-time config change monitoring and auto-updating

## CLI Commands Reference

```bash
# Add STDIO server
codebuddy mcp add --scope user my-tool -- /path/to/tool arg1 arg2
codebuddy mcp add --scope project python-tool -- python /path/to/script.py

# Add SSE server
codebuddy mcp add --scope user --transport sse sse-server https://example.com/mcp/sse

# Add HTTP server
codebuddy mcp add --scope project --transport http http-server https://example.com/mcp/http

# Add via JSON
codebuddy mcp add-json --scope user my-server '{"type":"stdio","command":"/usr/local/bin/tool","args":["--verbose"]}'
codebuddy mcp add-json --scope user http-server '{"type":"http","url":"https://example.com/mcp","headers":{"Authorization":"Bearer token"}}'

# Manage
codebuddy mcp list
codebuddy mcp get my-server
codebuddy mcp remove my-server
codebuddy mcp remove my-server --scope user
```

## Pre-built Server Examples

```bash
# Chrome DevTools
codebuddy mcp add --scope user chrome-devtools -- npx -y chrome-devtools-mcp@latest

# Filesystem
codebuddy mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem ./src

# Context7
codebuddy mcp add context7 -- npx -y @upstash/context7-mcp@latest

# DeepWiki
codebuddy mcp add deepwiki -- npx -y mcp-deepwiki@latest
```
