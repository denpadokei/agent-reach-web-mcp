"""MCP server exposing Agent Reach's web channel as MCP tools.

The web channel is Agent Reach's fallback channel:
  - search        -> Exa hosted MCP (free, no API key)
  - fetch_content -> Jina Reader, falling back to Exa

Like Agent Reach itself, every tool call returns the unified result
envelope (ok / items / error.code / hint), so clients can branch on it.
"""

from __future__ import annotations

import os
import time
from typing import Any, Mapping

from mcp.server.mcpserver import MCPServer

from agent_reach.channels.web import WebChannel
from agent_reach.runtime.result import FINAL_CODES, classify, envelope

DEFAULT_TIMEOUT = float(os.environ.get("AGENT_REACH_MCP_TIMEOUT", "30"))
MAX_LIMIT = 20

channel = WebChannel()

server = MCPServer(
    "agent-reach-web-mcp",
    instructions=(
        "Web search and page reading through the Agent Reach web channel. "
        "Search uses Exa's free hosted MCP endpoint (no API key); page reading "
        "uses Jina Reader with an Exa fallback. Read-only: nothing is posted "
        "or modified."
    ),
)


def _action(name: str):
    for action in channel.actions:
        if action.name == name:
            return action
    raise ValueError(f"web channel has no action: {name}")


def _run_action(action, params: Mapping[str, Any], timeout: float) -> dict:
    """Try the channel's ordered backends, exactly like `agent-reach web <action>`."""
    started = time.monotonic()
    attempts: list[str] = []
    last_error = None

    for label, method_name in action.backends:
        attempts.append(label)
        try:
            items = getattr(channel, method_name)(timeout=timeout, **params)
            elapsed_ms = int((time.monotonic() - started) * 1000)
            return envelope(
                channel=channel.name,
                action=action.name,
                backend=label,
                items=items,
                elapsed_ms=elapsed_ms,
                attempts=attempts,
            )
        except Exception as exc:
            last_error = classify(exc)
            # Final codes (rate limit, bad input, ...) will not change with
            # another backend, so stop right there.
            if last_error.code in FINAL_CODES:
                break

    elapsed_ms = int((time.monotonic() - started) * 1000)
    return envelope(
        channel=channel.name,
        action=action.name,
        attempts=attempts,
        error=last_error,
        elapsed_ms=elapsed_ms,
    )


@server.tool(name="search")
def search(query: str, limit: int = 5) -> dict:
    """Search the web via Agent Reach (Exa semantic search, no API key required).

    Returns unified envelope items: title, url, published_at, author and text
    highlights for each result.
    """
    if not query.strip():
        return envelope(
            channel=channel.name,
            action="search",
            error=classify(ValueError("query must not be empty")),
        )
    limit = max(1, min(int(limit), MAX_LIMIT))
    return _run_action(_action("search"), {"query": query.strip(), "limit": limit}, DEFAULT_TIMEOUT)


@server.tool(name="fetch_content")
def fetch_content(url: str) -> dict:
    """Read a web page as clean markdown via Agent Reach (Jina Reader, Exa fallback).

    Returns one unified envelope item with title, url, published_at and text.
    """
    return _run_action(_action("read"), {"target": url.strip()}, DEFAULT_TIMEOUT)


def main() -> None:
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
