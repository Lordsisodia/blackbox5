# MCP Protocol in Moltbot

## Overview

MCP (Model Context Protocol) is the protocol used by Claude Code to communicate with external tools. Moltbot implements MCP servers to bridge Claude Code with the VPS.

## MCP Server Types

### 1. ralf-vps (stdio over SSH)

**Location:** VPS (77.42.66.40) via SSH

**Connection Method:**
```json
{
  "type": "stdio",
  "command": "ssh",
  "args": [
    "-i", "~/.ssh/ralf_hetzner",
    "root@77.42.66.40",
    "python3", "-c",
    "exec(open('/opt/ralf/mcp-server.py').read())"
  ]
}
```

**Tools:**
- `ralf_get_queue` - Get RALF task queue
- `ralf_get_events` - Get RALF events
- `ralf_list_tasks` - List all tasks
- `ralf_get_task_status` - Get specific task status
- `ralf_run_command` - Run command on RALF VPS

### 2. moltbot-vps (stdio local)

**Location:** Local MacBook

**Connection Method:**
```json
{
  "type": "stdio",
  "command": "python3",
  "args": ["/Users/shaansisodia/.blackbox5/mcp-server-moltbot.py"]
}
```

**Tools:**
- `moltbot_get_status` - Check OpenClaw gateway
- `moltbot_send_message` - Send Telegram message
- `moltbot_get_ralf_status` - Get RALF queue via Moltbot
- `moltbot_get_user_context` - Get user profile
- `moltbot_run_command` - Run command on VPS

## MCP Protocol Flow

### 1. Initialization

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {
      "name": "claude-code",
      "version": "1.0.0"
    }
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {}
    },
    "serverInfo": {
      "name": "moltbot-mcp-server",
      "version": "1.0.0"
    }
  }
}
```

### 2. Tools/List

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "moltbot_get_status",
        "description": "Get OpenClaw/Moltbot gateway status",
        "inputSchema": {
          "type": "object",
          "properties": {}
        }
      },
      {
        "name": "moltbot_send_message",
        "description": "Send a message via Telegram",
        "inputSchema": {
          "type": "object",
          "properties": {
            "message": {
              "type": "string",
              "description": "Message to send"
            }
          },
          "required": ["message"]
        }
      }
    ]
  }
}
```

### 3. Tools/Call

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "moltbot_get_status",
    "arguments": {}
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Gateway is running"
      }
    ]
  }
}
```

## Implementation Details

### mcp-server-moltbot.py

```python
def main():
    # Read JSON-RPC requests from stdin
    for line in sys.stdin:
        msg = json.loads(line)
        method = msg.get("method", "")
        msg_id = msg.get("id")

        if method == "initialize":
            # Return server capabilities
            pass
        elif method == "tools/list":
            # Return tool definitions
            pass
        elif method == "tools/call":
            # Execute tool and return result
            tool_name = msg.get("params", {}).get("name", "")
            args = msg.get("params", {}).get("arguments", {})
            result = handle_tool_call(tool_name, args)
```

## Security Considerations

1. **SSH Key:** Uses dedicated SSH key (`~/.ssh/ralf_hetzner`)
2. **Command Injection:** Arguments are passed directly to subprocess
3. **Token Auth:** SSE endpoint uses Bearer token
4. **User Whitelist:** Telegram bot only responds to approved user IDs

## Research Questions

1. Full MCP specification details
2. Error handling patterns
3. Streaming response support
4. Resource vs Tool distinction
5. Prompt support in MCP

## Resources

- [MCP Specification](https://modelcontextprotocol.io)
- Claude Code MCP documentation
- OpenClaw MCP implementation
