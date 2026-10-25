# agent-reach-web-mcp

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A web-search MCP server you can run with `uvx`, exposing the [`web` channel of Agent Reach](https://github.com/Panniantong/Agent-Reach) as MCP tools.

- **Search**: Exa's free hosted MCP endpoint (no API key required)
- **Page reading**: Jina Reader, with an Exa fallback
- Read-only: nothing is posted or modified
- Every tool call returns Agent Reach's unified result envelope (`ok` / `items` / `error.code` / `hint`)

## Tools

| Tool | Description |
|---|---|
| `search(query, limit=5)` | Web search (Exa semantic search). Each result carries title / url / published_at / author and text highlights. `limit` is clamped to 1–20. |
| `fetch_content(url)` | Read a web page as clean markdown text (Jina Reader → Exa fallback). |

## Run with uvx

```bash
# From a clone (recommended)
uvx --from . agent-reach-web-mcp

# Straight from the public GitHub repository (no authentication needed)
uvx --from git+https://github.com/denpadokei/agent-reach-web-mcp agent-reach-web-mcp
```

`agent-reach` is pulled in automatically as a dependency installed from GitHub
(`git+https://github.com/Panniantong/Agent-Reach`), not from PyPI. Do not use the
same-named `agent-reach` package on PyPI — it is a different project.

## MCP client configuration example

```json
{
  "mcpServers": {
    "agent-reach-web-mcp": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/denpadokei/agent-reach-web-mcp", "agent-reach-web-mcp"]
    }
  }
}
```

## Development

```bash
uv venv
uv pip install -e .
uv run agent-reach-web-mcp   # starts as a stdio MCP server
```

The upstream call timeout (30 seconds by default) can be adjusted with the
`AGENT_REACH_MCP_TIMEOUT` environment variable, in seconds.

## License

MIT ([LICENSE](LICENSE)). The upstream Agent Reach project is MIT as well.
