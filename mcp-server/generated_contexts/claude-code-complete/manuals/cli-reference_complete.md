---
title: CLIリファレンス - Anthropic
source_url: https://docs.anthropic.com/ja/docs/claude-code/cli-reference
last_updated: '2025-08-10T09:26:43.628761Z'
content_type: manual
language: ja
extraction_confidence: 0.8
agent_version: 1.0.0
extracted_by: YAML Context Engineering Agent
extraction_timestamp: '2025-08-10T09:26:43.628764Z'
hierarchy_levels: []
related_sources: []
tags: []
---

# CLIリファレンス - Anthropic

## 📚 概要

**ソースURL**: https://docs.anthropic.com/ja/docs/claude-code/cli-reference
**最終更新**: 2025-08-10T18:26:43.628643
**コンテンツサイズ**: 5579 文字

---

## 📋 完全なコンテンツ

[Anthropic home page](/)

日本語

Search...

  * [Research](https://www.anthropic.com/research)
  * [Login](https://console.anthropic.com/login)
  * [Support](https://support.anthropic.com/)
  * [Discord](https://www.anthropic.com/discord)
  * [Sign up](https://console.anthropic.com/login)
  * [Sign up](https://console.anthropic.com/login)



Search...

Navigation

リファレンス

CLIリファレンス

[ようこそ](/ja/home)[Developer Platform](/ja/docs/intro)[Claude Code](/ja/docs/claude-code/overview)[Model Context Protocol (MCP)](/en/docs/mcp)[API リファレンス](/en/api/messages)[リソース](/ja/resources/overview)[リリースノート](/ja/release-notes/overview)

##### はじめに

  * [Overview](/ja/docs/claude-code/overview)
  * [クイックスタート](/ja/docs/claude-code/quickstart)
  * [一般的なワークフロー](/ja/docs/claude-code/common-workflows)



##### Claude Code で構築

  * [Claude Code SDK](/ja/docs/claude-code/sdk)
  * [サブエージェント](/ja/docs/claude-code/sub-agents)
  * [Claude Codeフック](/ja/docs/claude-code/hooks-guide)
  * [GitHub Actions](/ja/docs/claude-code/github-actions)
  * [Model Context Protocol (MCP)](/ja/docs/claude-code/mcp)
  * [トラブルシューティング](/ja/docs/claude-code/troubleshooting)



##### デプロイメント

  * [概要](/ja/docs/claude-code/third-party-integrations)
  * [Amazon Bedrock](/ja/docs/claude-code/amazon-bedrock)
  * [Google Vertex AI](/ja/docs/claude-code/google-vertex-ai)
  * [Corporate proxy](/ja/docs/claude-code/corporate-proxy)
  * [LLMゲートウェイ](/ja/docs/claude-code/llm-gateway)
  * [開発コンテナ](/ja/docs/claude-code/devcontainer)



##### 管理

  * [高度なインストール](/ja/docs/claude-code/setup)
  * [アイデンティティとアクセス管理](/ja/docs/claude-code/iam)
  * [セキュリティ](/ja/docs/claude-code/security)
  * [監視](/ja/docs/claude-code/monitoring-usage)
  * [コスト](/ja/docs/claude-code/costs)
  * [アナリティクス](/ja/docs/claude-code/analytics)



##### 設定

  * [設定](/ja/docs/claude-code/settings)
  * [IDEにClaude Codeを追加する](/ja/docs/claude-code/ide-integrations)
  * [ターミナル設定](/ja/docs/claude-code/terminal-config)
  * [メモリ管理](/ja/docs/claude-code/memory)



##### リファレンス

  * [CLIリファレンス](/ja/docs/claude-code/cli-reference)
  * [インタラクティブモード](/ja/docs/claude-code/interactive-mode)
  * [スラッシュコマンド](/ja/docs/claude-code/slash-commands)
  * [フックリファレンス](/ja/docs/claude-code/hooks)



##### リソース

  * [データ使用](/ja/docs/claude-code/data-usage)
  * [法的事項とコンプライアンス](/ja/docs/claude-code/legal-and-compliance)



リファレンス

# CLIリファレンス

Copy page

Claude Codeコマンドラインインターフェースの完全なリファレンス（コマンドとフラグを含む）。

## 

​

CLIコマンド

コマンド| 説明| 例  
---|---|---  
`claude`| インタラクティブREPLを開始| `claude`  
`claude "query"`| 初期プロンプトでREPLを開始| `claude "explain this project"`  
`claude -p "query"`| SDK経由でクエリを実行し、終了| `claude -p "explain this function"`  
`cat file | claude -p "query"`| パイプされたコンテンツを処理| `cat logs.txt | claude -p "explain"`  
`claude -c`| 最新の会話を継続| `claude -c`  
`claude -c -p "query"`| SDK経由で継続| `claude -c -p "Check for type errors"`  
`claude -r "<session-id>" "query"`| セッションIDでセッションを再開| `claude -r "abc123" "Finish this PR"`  
`claude update`| 最新バージョンに更新| `claude update`  
`claude mcp`| Model Context Protocol (MCP)サーバーを設定| [Claude Code MCPドキュメント](/ja/docs/claude-code/mcp)を参照してください。  
  
## 

​

CLIフラグ

これらのコマンドラインフラグでClaude Codeの動作をカスタマイズできます：

フラグ| 説明| 例  
---|---|---  
`--add-dir`| Claudeがアクセスする追加の作業ディレクトリを追加（各パスがディレクトリとして存在することを検証）| `claude --add-dir ../apps ../lib`  
`--allowedTools`| [settings.jsonファイル](/ja/docs/claude-code/settings)に加えて、ユーザーの許可を求めることなく許可すべきツールのリスト| `"Bash(git log:*)" "Bash(git diff:*)" "Read"`  
`--disallowedTools`| [settings.jsonファイル](/ja/docs/claude-code/settings)に加えて、ユーザーの許可を求めることなく禁止すべきツールのリスト| `"Bash(git log:*)" "Bash(git diff:*)" "Edit"`  
`--print`, `-p`| インタラクティブモードなしでレスポンスを印刷（プログラム的な使用の詳細については[SDKドキュメント](/ja/docs/claude-code/sdk)を参照）| `claude -p "query"`  
`--output-format`| 印刷モードの出力フォーマットを指定（オプション：`text`、`json`、`stream-json`）| `claude -p "query" --output-format json`  
`--input-format`| 印刷モードの入力フォーマットを指定（オプション：`text`、`stream-json`）| `claude -p --output-format json --input-format stream-json`  
`--verbose`| 詳細ログを有効化、完全なターンバイターンの出力を表示（印刷モードとインタラクティブモードの両方でデバッグに役立つ）| `claude --verbose`  
`--max-turns`| 非インタラクティブモードでのエージェンティックターンの数を制限| `claude -p --max-turns 3 "query"`  
`--model`| 最新モデルのエイリアス（`sonnet`または`opus`）またはモデルのフルネームで現在のセッションのモデルを設定| `claude --model claude-sonnet-4-20250514`  
`--permission-mode`| 指定された[許可モード](iam#permission-modes)で開始| `claude --permission-mode plan`  
`--permission-prompt-tool`| 非インタラクティブモードで許可プロンプトを処理するMCPツールを指定| `claude -p --permission-prompt-tool mcp_auth_tool "query"`  
`--resume`| IDで特定のセッションを再開、またはインタラクティブモードで選択| `claude --resume abc123 "query"`  
`--continue`| 現在のディレクトリで最新の会話を読み込み| `claude --continue`  
`--dangerously-skip-permissions`| 許可プロンプトをスキップ（注意して使用）| `claude --dangerously-skip-permissions`  
  
`--output-format json`フラグは、スクリプトや自動化に特に有用で、 Claudeのレスポンスをプログラム的に解析できます。

出力フォーマット、ストリーミング、詳細ログ、プログラム的な使用を含む印刷モード（`-p`）の詳細情報については、 [SDKドキュメント](/ja/docs/claude-code/sdk)を参照してください。

## 

​

関連項目

  * [インタラクティブモード](/ja/docs/claude-code/interactive-mode) \- ショートカット、入力モード、インタラクティブ機能
  * [スラッシュコマンド](/ja/docs/claude-code/slash-commands) \- インタラクティブセッションコマンド
  * [クイックスタートガイド](/ja/docs/claude-code/quickstart) \- Claude Codeの開始方法
  * [一般的なワークフロー](/ja/docs/claude-code/common-workflows) \- 高度なワークフローとパターン
  * [設定](/ja/docs/claude-code/settings) \- 設定オプション
  * [SDKドキュメント](/ja/docs/claude-code/sdk) \- プログラム的な使用と統合



Was this page helpful?

YesNo

[メモリ管理](/ja/docs/claude-code/memory)[インタラクティブモード](/ja/docs/claude-code/interactive-mode)

[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)

On this page

  * CLIコマンド
  * CLIフラグ
  * 関連項目




---

## 🏗️ ドキュメント構造

- **CLIリファレンス**
  ```
  Copy page

Claude Codeコマンドラインインターフェースの完全なリファレンス（コマンドとフラグを含む）。

## 

​

CLIコマンド

コマンド| 説明| 例  
---|---|---  
`claude`| インタラクティブREPLを開始| `claude`  
`claude "query"`| 初期プロンプトでREPLを開始| `claude "explain th
  ```

## 🔍 抽出されたエンティティ

### URLs
- https://www.anthropic.com/discord)
- https://x.com/AnthropicAI)
- https://www.anthropic.com/research)
- https://console.anthropic.com/login)
- https://www.linkedin.com/company/anthropicresearch)
- https://support.anthropic.com/)

### キーワード
Google Vertex, Claude Code, Amazon Bedrock, Model Context Protocol, Developer Platform
