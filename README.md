# Composio for Cursor

Composio lets you connect and act on **[1000+ apps](https://composio.dev/toolkits)** like Google Workspace, Slack,
GitHub, Notion, Linear, Jira, HubSpot, and more
directly from your agent, through the [Composio](https://composio.dev) MCP server.

Composio handles OAuth, permissions, and intelligent tool routing, and provides a remote sandbox for bulk data processing.

Composio is compatible with any agent harness, such as Claude Code, Codex, OpenClaw, and Hermes.

## What you can do

Beyond single-app actions, the agent can:

- **Run cross-app workflows** — e.g. turn the latest GitHub PR into a Linear issue
  and announce it in Slack; draft a doc from a calendar event.
- **Compute in a remote sandbox** — aggregate, parse, and transform large tool
  responses (e.g. sender-domain distributions across hundreds of emails, weekday
  breakdowns, dedupe/joins) without pulling everything into context.
- **Connect apps on demand** — fully managed OAuth; the agent hands you an auth link
  and waits for it to complete.

## What's included

| Component | Purpose |
|---|---|
| `mcp.json` | Registers the Composio MCP server (`connect.composio.dev/mcp`), exposing 7 meta-tools. |
| `skills/composio-mcp` | Teaches the agent the search → connect → execute workflow and best practices. |

## Install

### Add the MCP server to Cursor (one click)

[![Add to Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/en-US/install-mcp?name=composio&config=eyJ1cmwiOiJodHRwczovL2Nvbm5lY3QuY29tcG9zaW8uZGV2L21jcCJ9)

Or add it manually in **Cursor → Settings → MCP**:

```json
{
  "mcpServers": {
    "composio": {
      "url": "https://connect.composio.dev/mcp"
    }
  }
}
```

### Install the full plugin (MCP + skill)

From the Cursor plugin marketplace:

```
/add-plugin composio
```

On first use the agent walks you through connecting an app: it returns an OAuth
link, you authorize, and the connection becomes available to every future request.

### Local testing

Symlink the repo into Cursor's local plugins, then reload the window
(`Developer: Reload Window`):

```bash
ln -sfn "$PWD" ~/.cursor/plugins/local/composio   # remove with: rm ~/.cursor/plugins/local/composio
```

## How it works

The plugin exposes 7 `COMPOSIO_*` meta-tools instead of thousands of individual app
tools. The agent:

1. **Searches** for the right tool with `COMPOSIO_SEARCH_TOOLS`.
2. **Connects** the app via managed OAuth if needed (`COMPOSIO_MANAGE_CONNECTIONS` → `COMPOSIO_WAIT_FOR_CONNECTIONS`).
3. **Executes** one or many tools with `COMPOSIO_MULTI_EXECUTE_TOOL`.
4. **Processes** large/bulk results in a remote sandbox (`COMPOSIO_REMOTE_WORKBENCH` / `COMPOSIO_REMOTE_BASH_TOOL`).

See `skills/composio-mcp/SKILL.md` for the full meta-tool reference.

## Examples

Each query names the apps explicitly, which is what the skill expects — it keeps
tool search scoped and the run reliable.

**Single app:**

```text
What's on my Google Calendar for tomorrow? Add an event for lunch at 12PM.
```

**Cross-app workflow** (triage — reads feed the write):

```text
Do the following:
1. Fetch today's unread Gmail emails and unread Slack mentions/DMs
2. Triage them into action items vs. FYI
3. Post a concise summary to a new Notion page amed "Daily Triage"
```

**Parallel workflow** (independent reads, fanned out in one batch):

```text
In parallel, search and execute: 
- fetch my last 10 Gmail emails
- open Linear issues
- today's Google Calendar events

Then give me a concise summary.
```

**Sandbox compute** (bulk data, kept out of the chat):

```text
Fetch my last 20 most recent Gmail emails,
- find the promotional/newsletter senders
- rank them by how many emails each sent so I can unsubscribe manually

Use the COMPOSIO_REMOTE_WORKBENCH.
```

## License

MIT
