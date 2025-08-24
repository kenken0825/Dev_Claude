---
title: スラッシュコマンド - Anthropic
source_url: https://docs.anthropic.com/ja/docs/claude-code/slash-commands
last_updated: '2025-08-10T09:26:43.758218Z'
content_type: manual
language: ja
extraction_confidence: 0.8
agent_version: 1.0.0
extracted_by: YAML Context Engineering Agent
extraction_timestamp: '2025-08-10T09:26:43.758222Z'
hierarchy_levels: []
related_sources: []
tags: []
---

# スラッシュコマンド - Anthropic

## 📚 概要

**ソースURL**: https://docs.anthropic.com/ja/docs/claude-code/slash-commands
**最終更新**: 2025-08-10T18:26:43.758113
**コンテンツサイズ**: 8154 文字

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

スラッシュコマンド

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

# スラッシュコマンド

Copy page

インタラクティブセッション中にスラッシュコマンドでClaudeの動作を制御します。

## 

​

組み込みスラッシュコマンド

コマンド| 目的  
---|---  
`/add-dir`| 追加の作業ディレクトリを追加  
`/agents`| 専門タスク用のカスタムAIサブエージェントを管理  
`/bug`| バグを報告（会話をAnthropicに送信）  
`/clear`| 会話履歴をクリア  
`/compact [instructions]`| オプションのフォーカス指示で会話をコンパクト化  
`/config`| 設定を表示/変更  
`/cost`| トークン使用統計を表示  
`/doctor`| Claude Codeインストールの健全性をチェック  
`/help`| 使用方法のヘルプを取得  
`/init`| CLAUDE.mdガイドでプロジェクトを初期化  
`/login`| Anthropicアカウントを切り替え  
`/logout`| Anthropicアカウントからサインアウト  
`/mcp`| MCPサーバー接続とOAuth認証を管理  
`/memory`| CLAUDE.mdメモリファイルを編集  
`/model`| AIモデルを選択または変更  
`/permissions`| [権限](/ja/docs/claude-code/iam#configuring-permissions)を表示または更新  
`/pr_comments`| プルリクエストコメントを表示  
`/review`| コードレビューを要求  
`/status`| アカウントとシステムのステータスを表示  
`/terminal-setup`| 改行用のShift+Enterキーバインドをインストール（iTerm2とVSCodeのみ）  
`/vim`| 挿入モードとコマンドモードを交互に切り替えるvimモードに入る  
  
## 

​

カスタムスラッシュコマンド

カスタムスラッシュコマンドを使用すると、頻繁に使用するプロンプトをMarkdownファイルとして定義し、Claude Codeが実行できるようになります。コマンドはスコープ（プロジェクト固有または個人）で整理され、ディレクトリ構造を通じて名前空間をサポートします。

### 

​

構文
    
    
    /<command-name> [arguments]
    

#### 

​

パラメータ

パラメータ| 説明  
---|---  
`<command-name>`| Markdownファイル名から派生した名前（`.md`拡張子なし）  
`[arguments]`| コマンドに渡されるオプションの引数  
  
### 

​

コマンドタイプ

#### 

​

プロジェクトコマンド

リポジトリに保存され、チームと共有されるコマンド。`/help`でリストされる際、これらのコマンドは説明の後に「(project)」と表示されます。

**場所** : `.claude/commands/`

以下の例では、`/optimize`コマンドを作成します：
    
    
    # プロジェクトコマンドを作成
    mkdir -p .claude/commands
    echo "Analyze this code for performance issues and suggest optimizations:" > .claude/commands/optimize.md
    

#### 

​

個人コマンド

すべてのプロジェクトで利用可能なコマンド。`/help`でリストされる際、これらのコマンドは説明の後に「(user)」と表示されます。

**場所** : `~/.claude/commands/`

以下の例では、`/security-review`コマンドを作成します：
    
    
    # 個人コマンドを作成
    mkdir -p ~/.claude/commands
    echo "Review this code for security vulnerabilities:" > ~/.claude/commands/security-review.md
    

### 

​

機能

#### 

​

名前空間

サブディレクトリでコマンドを整理します。サブディレクトリがコマンドの 完全な名前を決定します。説明には、コマンドがプロジェクト ディレクトリ（`.claude/commands`）またはユーザーレベルディレクトリ（`~/.claude/commands`）のどちらから来るかが表示されます。

ユーザーレベルとプロジェクトレベルのコマンド間の競合はサポートされていません。それ以外では、 同じベースファイル名を持つ複数のコマンドが共存できます。

例えば、`.claude/commands/frontend/component.md`のファイルは、説明に「(project)」と表示される`/frontend:component`コマンドを作成します。 一方、`~/.claude/commands/component.md`のファイルは、説明に「(user)」と表示される`/component`コマンドを作成します。

#### 

​

引数

`$ARGUMENTS`プレースホルダーを使用してコマンドに動的な値を渡します。

例：
    
    
    # コマンド定義
    echo 'Fix issue #$ARGUMENTS following our coding standards' > .claude/commands/fix-issue.md
    
    # 使用方法
    > /fix-issue 123
    

#### 

​

Bashコマンド実行

`!`プレフィックスを使用してスラッシュコマンドが実行される前にbashコマンドを実行します。出力はコマンドコンテキストに含まれます。`Bash`ツールで`allowed-tools`を含める_必要があります_が、許可する特定のbashコマンドを選択できます。

例：
    
    
    ---
    allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
    description: Create a git commit
    ---
    
    ## Context
    
    - Current git status: !`git status`
    - Current git diff (staged and unstaged changes): !`git diff HEAD`
    - Current branch: !`git branch --show-current`
    - Recent commits: !`git log --oneline -10`
    
    ## Your task
    
    Based on the above changes, create a single git commit.
    

#### 

​

ファイル参照

`@`プレフィックスを使用して[ファイルを参照](/ja/docs/claude-code/common-workflows#reference-files-and-directories)し、コマンドにファイル内容を含めます。

例：
    
    
    # 特定のファイルを参照
    
    Review the implementation in @src/utils/helpers.js
    
    # 複数のファイルを参照
    
    Compare @src/old-version.js with @src/new-version.js
    

#### 

​

思考モード

スラッシュコマンドは[拡張思考キーワード](/ja/docs/claude-code/common-workflows#use-extended-thinking)を含めることで拡張思考をトリガーできます。

### 

​

フロントマター

コマンドファイルはフロントマターをサポートし、コマンドに関するメタデータを指定するのに便利です：

| フロントマター | 目的 | デフォルト | | :--- | :--- | :--- | --- | ---- | | `allowed-tools` | コマンドが使用できるツールのリスト | 会話から継承 | | `argument-hint` | スラッシュコマンドに期待される引数。例：`argument-hint: add [tagId] | remove [tagId] | list`。このヒントは、スラッシュコマンドの自動補完時にユーザーに表示されます。 | なし | | `description` | コマンドの簡潔な説明 | プロンプトの最初の行を使用 | | `model` | `opus`、`sonnet`、`haiku`、または特定のモデル文字列 | 会話から継承 |

例：
    
    
    ---
    allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
    argument-hint: [message]
    description: Create a git commit
    model: haiku
    ---
    
    An example command
    

## 

​

MCPスラッシュコマンド

MCPサーバーは、Claude Codeで利用可能になるスラッシュコマンドとしてプロンプトを公開できます。これらのコマンドは接続されたMCPサーバーから動的に発見されます。

### 

​

コマンド形式

MCPコマンドは以下のパターンに従います：
    
    
    /mcp__<server-name>__<prompt-name> [arguments]
    

### 

​

機能

#### 

​

動的発見

MCPコマンドは以下の場合に自動的に利用可能になります：

  * MCPサーバーが接続されアクティブである
  * サーバーがMCPプロトコルを通じてプロンプトを公開している
  * 接続中にプロンプトが正常に取得される



#### 

​

引数

MCPプロンプトはサーバーによって定義された引数を受け取ることができます：
    
    
    # 引数なし
    > /mcp__github__list_prs
    
    # 引数あり
    > /mcp__github__pr_review 456
    > /mcp__jira__create_issue "Bug title" high
    

#### 

​

命名規則

  * サーバーとプロンプト名は正規化される
  * スペースと特殊文字はアンダースコアになる
  * 一貫性のために名前は小文字になる



### 

​

MCP接続の管理

`/mcp`コマンドを使用して：

  * 設定されたすべてのMCPサーバーを表示
  * 接続ステータスを確認
  * OAuth対応サーバーで認証
  * 認証トークンをクリア
  * 各サーバーから利用可能なツールとプロンプトを表示



## 

​

関連項目

  * [インタラクティブモード](/ja/docs/claude-code/interactive-mode) \- ショートカット、入力モード、インタラクティブ機能
  * [CLIリファレンス](/ja/docs/claude-code/cli-reference) \- コマンドラインフラグとオプション
  * [設定](/ja/docs/claude-code/settings) \- 設定オプション
  * [メモリ管理](/ja/docs/claude-code/memory) \- セッション間でのClaudeのメモリ管理



Was this page helpful?

YesNo

[インタラクティブモード](/ja/docs/claude-code/interactive-mode)[フックリファレンス](/ja/docs/claude-code/hooks)

[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)

On this page

  * 組み込みスラッシュコマンド
  * カスタムスラッシュコマンド
  * 構文
  * パラメータ
  * コマンドタイプ
  * プロジェクトコマンド
  * 個人コマンド
  * 機能
  * 名前空間
  * 引数
  * Bashコマンド実行
  * ファイル参照
  * 思考モード
  * フロントマター
  * MCPスラッシュコマンド
  * コマンド形式
  * 機能
  * 動的発見
  * 引数
  * 命名規則
  * MCP接続の管理
  * 関連項目




---

## 🏗️ ドキュメント構造

- **スラッシュコマンド**
  ```
  Copy page

インタラクティブセッション中にスラッシュコマンドでClaudeの動作を制御します。

## 

​

組み込みスラッシュコマンド

コマンド| 目的  
---|---  
`/add-dir`| 追加の作業ディレクトリを追加  
`/agents`| 専門タスク用のカスタムAIサブエージェントを管理  
`/bug`| バグを報告（会話をAnthropicに送信）  
`/
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
