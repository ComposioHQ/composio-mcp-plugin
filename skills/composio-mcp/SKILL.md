---
name: composio-mcp
description: Use the Composio Connect MCP server to interact with 1000+ apps — GitHub, Slack, Notion, Gmail, Linear, Jira, and more. Composio manages auth, permissions, and intelligent tool routing. Trigger when the user asks to connect an app, execute an action on an external service, or work with connectors.
---

# Composio Connect MCP

The Composio MCP server at `connect.composio.dev/mcp` gives the agent access to 1000+ apps. Composio manages auth and permissions for all connected apps, intelligently routes to the best tool for the task, helps with long context tasks, and enables programmatic tool calling.

## How it works

You have 7 meta-tools that orchestrate everything:

### 1. `COMPOSIO_SEARCH_TOOLS` — always start here

Discovers the right tools and returns a recommended execution plan. Call this **first** whenever the user mentions or implies an external app or workflow.

- Pass `queries` with a `use_case` describing what the user wants to do
- For complex workflows, split into multiple atomic queries (1 query = 1 tool call)
- Include app names in each query to keep intent scoped (e.g., "fetch Gmail emails", not just "fetch emails")
- Pass `known_fields` for any IDs, names, or settings the user mentioned
- Use `session: { generate_id: true }` for new workflows; reuse the returned `session_id` for follow-up calls
- If the user pivots to a different task, generate a new session

### 2. `COMPOSIO_GET_TOOL_SCHEMAS` — inspect before executing

Retrieves full input schemas for tools by slug. Call this when SEARCH_TOOLS doesn't provide a complete schema — never guess or invent input parameters.

### 3. `COMPOSIO_MULTI_EXECUTE_TOOL` — run tools (up to 50 in parallel)

Executes discovered tools. Supports parallel execution for independent operations.

- Only batch tools that are logically independent (no output-to-input dependencies)
- Always use valid slugs and schema-compliant arguments from SEARCH_TOOLS
- Ensure an ACTIVE connection exists before executing
- Set `sync_response_to_workbench: true` if the response may be large
- Include inline references/links (e.g., Slack thread links, GitHub PR URLs) in results

### 4. `COMPOSIO_MANAGE_CONNECTIONS` — connect apps

Creates, lists, renames, or removes app connections. Actions:

- `add` — initiates OAuth, returns a redirect URL to show the user
- `list` — shows connected accounts with IDs, aliases, statuses
- `rename` — rename an account alias
- `remove` — disconnect an account

After initiating a connection, show the auth link to the user as a formatted markdown link, then immediately call `COMPOSIO_WAIT_FOR_CONNECTIONS`.

### 5. `COMPOSIO_WAIT_FOR_CONNECTIONS` — poll until auth completes

Call after showing the auth link from MANAGE_CONNECTIONS. Waits until the connection reaches ACTIVE or FAILED state.

### 6. `COMPOSIO_REMOTE_BASH_TOOL` — shell commands in a remote sandbox

For processing large tool responses saved to remote files. Use jq, awk, sed, grep, etc.

### 7. `COMPOSIO_REMOTE_WORKBENCH` — Python scripting in a remote sandbox

For bulk operations, data processing, or multi-tool chains. Persistent Jupyter notebook — state is preserved across calls. Has helper functions like `run_composio_tool()` and `invoke_llm()`.

Only use the workbench when data is stored in a remote file or you need bulk/scripted execution. If data is already inline, process it directly.

## Default workflow

1. **Search** — `COMPOSIO_SEARCH_TOOLS` with the user's intent
2. **Connect** — if no active connection, `COMPOSIO_MANAGE_CONNECTIONS` → show auth link → `COMPOSIO_WAIT_FOR_CONNECTIONS`
3. **Schema** — `COMPOSIO_GET_TOOL_SCHEMAS` if needed
4. **Execute** — `COMPOSIO_MULTI_EXECUTE_TOOL` with discovered tools
5. **Process** — use workbench/bash only for large or bulk results

## Tips

- Always start with SEARCH_TOOLS — never say "I don't have access to X" before searching
- The server knows which apps the user has connected and optimizes search results accordingly
- For cross-app workflows, split into atomic queries and execute independent steps in parallel
- Re-run SEARCH_TOOLS when you need additional tools due to missing details, errors, or a changed use case
- OAuth is fully managed — no API keys needed from the user