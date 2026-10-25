# agent-reach-web-mcp

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Agent Reach](https://github.com/Panniantong/Agent-Reach) の `web` チャネルを MCP サーバとして公開する、uvx で動かせる Web 検索 MCP サーバ。

- **検索**: Exa の無料ホスト MCP（APIキー不要）
- **ページ読取**: Jina Reader（失敗時は Exa にフォールバック）
- 読み取り専用（投稿・変更なし）
- 返り値は Agent Reach 統一エンベロープ形式（`ok` / `items` / `error.code` / `hint`）

## ツール

| ツール | 説明 |
|---|---|
| `search(query, limit=5)` | Web 検索（Exa セマンティック検索）。結果は title / url / published_at / text ハイトライト |
| `fetch_content(url)` | Web ページを Markdown のクリーンテキストとして取得（Jina Reader → Exa） |

## uvx で実行

```bash
# クローン内で（推奨）
uvx --from . agent-reach-web-mcp

# GitHub のパブリックリポジトリから直接（認証不要）
uvx --from git+https://github.com/denpadokei/agent-reach-web-mcp agent-reach-web-mcp
```

`agent-reach` は PyPI ではなく GitHub からインストールされる依存（`git+https://github.com/Panniantong/Agent-Reach`）として自動で取得されます。PyPI にある同名の `agent-reach` パッケージは別物なので使わないでください。

## MCP クライアント設定例

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

## 開発

```bash
uv venv
uv pip install -e .
uv run agent-reach-web-mcp   # stdio MCP サーバとして起動
```

環境変数 `AGENT_REACH_MCP_TIMEOUT`（秒、既定 30）で上流呼出のタイムアウトを調整できます。

## ライセンス

MIT（[LICENSE](LICENSE)）。上流の Agent Reach も MIT。
