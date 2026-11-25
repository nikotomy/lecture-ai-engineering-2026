# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：glossary_search_glossary
- STEP 2 の [tool call]：[tool call]   glossary_search_glossary({'query': '3レベル'})
- STEP 3 の [tool call]：fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
- STEP 4 の [tool call]：aws_aws___search_documentation({'search_phrase': 'Amazon S3 バージョニング 概要'})
aws_aws___search_documentation({'search_phrase': 'What is S3 Versioning Amazon S3 Developer Guide'})
- 気づき・疑問：ツールを増やすと、使っていなくても入力トークンが増えていく。

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル： 発展
- やったこと：Claude CodeのMCPサーバーの設定方法を調べて、app/mcp_servers.jsonと比べた。
  - 調べた日: 2026/11/25
  - 参照したドキュメント: https://code.claude.com/docs/ja/mcp-quickstart https://code.claude.com/docs/en/mcp
- 結果：

| 調べること | Claude Code | 演習 |
| ---- | ---- | ---- |
| 設定を書く場所 | コマンドで登録するのと、ファイルに書く方法の2種類がある。コマンドは`claude mcp add`、ファイルに書く場合はプロジェクト直下に`.mcp.json`を作る。 | `app/mcp_servers.json`を編集する |
| コマンドで接続する | コマンド<br>`claude mcp add <名前> -- <起動コマンド>`<br>.mcp.json<br>`"<名前>": {"type": "stdio", "command": "uv", "args": [...]"}` | `{"command": "uv", "args": [...]}` |
| URLに接続する |コマンド<br>`claude mcp add --transport http aws https://knowledge-mcp.global.api.aws`<br>.mcp.json<br>`{ "mcpServers": "<名前>": {"type": "http", "url": "https://knowledge-mcp.global.api.aws"}}}` | `"aws": {"url: "https://knowledge-mcp.global.api.aws"}` |
| 有効になる範囲 | コマンドで登録する場合は`--scope`によって変わる。<br>指定なし(`local`): 自分のみ・現在のプロジェクト ~/.claude.jsonに保存される<br>`--scope project`: プロジェクトのメンバーで共有 .mcp.jsonに保存される<br>`--scope user`: 自分のみ・全プロジェクト ~/.claude.json | app.mcp_agentを動かした時のみ |
- 気づき・疑問：
設定ファイルの書き方は使用するソフトウェアによって違う。