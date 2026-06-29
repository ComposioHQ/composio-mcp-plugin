---
name: composio-activity-summary
description: Generates comprehensive company activity summary across connected apps — Slack, GitHub, Notion, Linear, Gmail, and more. Use when user asks for company updates, daily summary, or what's happening across the org.
---

# Company Activity Summary (MCP)

Generate a comprehensive summary of company activity over the last 24 hours (or specified time period) across all connected apps.

## Arguments

- `$ARGUMENTS` - Time period to analyze (default: "last 24 hours"). Examples: "last 24 hours", "last 7 days", "since Monday"

## Step 1: Discover Connected Apps

First, check which apps the user has connected by trying lightweight read calls. Use AskUserQuestion if you're unsure which apps they use.

Common apps to check (try each, skip silently if not connected):

| App | Test Tool | What to Fetch |
|-----|-----------|---------------|
| Slack | `SLACK_LIST_CHANNELS` | Channel messages, threads, announcements |
| GitHub | `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER` | PRs, merges, issues, code reviews |
| Notion | `NOTION_SEARCH_NOTION_PAGE` (query: "", sort by last_edited_time) | Recently edited pages, meeting notes, docs |
| Linear | `LINEAR_LIST_LINEAR_ISSUES` or `LINEAR_RUN_QUERY_OR_MUTATION` | Issues created/updated/completed, project progress |
| Gmail | `GMAIL_FETCH_EMAILS` | Important emails, threads |
| Google Calendar | `GOOGLECALENDAR_LIST_EVENTS` | Meetings that happened, upcoming schedule |

Note which apps are connected and skip the rest.

## Step 2: Launch Parallel Agents Per Connected App

For each connected app, launch a background Agent to gather and summarize activity. Each agent writes its summary to a markdown file in the current working directory.

### Slack Agent
Prompt: Fetch Slack activity for the time period "$ARGUMENTS" (default: last 24 hours).
1. List channels with `SLACK_LIST_CHANNELS`
2. For active channels, fetch recent messages with `SLACK_GET_CHANNEL_MESSAGES_AND_THREAD_REPLIES`
3. Focus on: key discussions, decisions made, announcements, questions asked
4. Write summary to `slack-activity-summary.md`

### GitHub Agent
Prompt: Fetch GitHub activity for the time period "$ARGUMENTS" (default: last 24 hours).
1. List repos with `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER`
2. For each active repo, fetch PRs with `GITHUB_LIST_PULL_REQUESTS_IN_A_REPOSITORY`
3. For significant PRs, get details and changed files
4. Focus on: PRs opened/merged/reviewed, issues created/closed, code changes
5. Write summary to `github-activity-summary.md`

### Notion Agent
Prompt: Fetch Notion activity for the time period "$ARGUMENTS" (default: last 24 hours).
1. Search recent pages with `NOTION_SEARCH_NOTION_PAGE` (sort by last_edited_time, descending)
2. For important pages, fetch content with `NOTION_FETCH_ALL_BLOCK_CONTENTS`
3. Focus on: documentation updates, meeting notes, project tracking changes
4. Write summary to `notion-activity-summary.md`

### Linear Agent
Prompt: Fetch Linear activity for the time period "$ARGUMENTS" (default: last 24 hours).
1. Fetch updated issues with `LINEAR_LIST_LINEAR_ISSUES` or use `LINEAR_RUN_QUERY_OR_MUTATION` with GraphQL for richer data
2. Group by team and status changes
3. Focus on: issues completed, issues created, blockers, project progress
4. Write summary to `linear-activity-summary.md`

### Gmail Agent (if connected)
Prompt: Fetch Gmail activity for the time period "$ARGUMENTS" (default: last 24 hours).
1. Fetch recent emails with `GMAIL_FETCH_EMAILS`
2. Focus on: important threads, action items, external communications
3. Write summary to `gmail-activity-summary.md`

### Calendar Agent (if connected)
Prompt: Fetch Google Calendar activity for the time period "$ARGUMENTS" (default: last 24 hours).
1. List events with `GOOGLECALENDAR_LIST_EVENTS`
2. Focus on: meetings that happened, key attendees, upcoming schedule
3. Write summary to `calendar-activity-summary.md`

## Step 3: Compile Overview

After all agents complete, read each summary file and present:

```markdown
# Company Activity Summary - [Date Range]

## Connected Apps Analyzed
- [list of apps that were successfully queried]

## Key Highlights
[3-5 bullet points of the most important things across all apps]

## Detailed Summaries
| Platform | File | Highlights |
|----------|------|------------|
| Slack | [slack-activity-summary.md](./slack-activity-summary.md) | [1-line summary] |
| GitHub | [github-activity-summary.md](./github-activity-summary.md) | [1-line summary] |
| ... | ... | ... |
```

Read each file and provide a brief overview of key highlights, then let the user know they can open individual files for full details.

## Guidelines

- Only summarize apps that are actually connected — don't fail or warn about missing apps
- Use AskUserQuestion if the time period is ambiguous
- For large time periods (>7 days), warn the user it may take longer
- If any agent fails, note which summaries are missing but still present the rest
- Focus on actionable insights, not just lists of items
