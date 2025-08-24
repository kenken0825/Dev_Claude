---
title: クイックスタート - Anthropic
source_url: https://docs.anthropic.com/ja/docs/claude-code/quickstart
last_updated: '2025-08-10T09:26:43.458599Z'
content_type: manual
language: ja
extraction_confidence: 0.9
agent_version: 1.0.0
extracted_by: YAML Context Engineering Agent
extraction_timestamp: '2025-08-10T09:26:43.458602Z'
hierarchy_levels: []
related_sources: []
tags: []
---

# クイックスタート - Anthropic

## 📚 概要

**ソースURL**: https://docs.anthropic.com/ja/docs/claude-code/quickstart
**最終更新**: 2025-08-10T18:26:43.458510
**コンテンツサイズ**: 7676 文字

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

はじめに

クイックスタート

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



はじめに

# クイックスタート

Copy page

Claude Codeへようこそ！

このクイックスタートガイドでは、わずか数分でAI搭載のコーディング支援を使用できるようになります。最後には、一般的な開発タスクでClaude Codeを使用する方法を理解できるでしょう。

## 

​

始める前に

以下を準備してください：

  * ターミナルまたはコマンドプロンプトを開く
  * 作業するコードプロジェクト



## 

​

ステップ1：Claude Codeをインストールする

### 

​

NPMインストール

[Node.js 18以降がインストールされている](https://nodejs.org/en/download/)場合：
    
    
    npm install -g @anthropic-ai/claude-code
    

### 

​

ネイティブインストール

または、現在ベータ版の新しいネイティブインストールをお試しください。

**macOS、Linux、WSL：**
    
    
    curl -fsSL claude.ai/install.sh | bash
    

**Windows PowerShell：**
    
    
    irm https://claude.ai/install.ps1 | iex
    

## 

​

ステップ2：最初のセッションを開始する

任意のプロジェクトディレクトリでターミナルを開き、Claude Codeを開始します：
    
    
    cd /path/to/your/project
    claude
    

新しいインタラクティブセッション内でClaude Codeプロンプトが表示されます：
    
    
    ✻ Welcome to Claude Code!
    
    ...
    
    > Try "create a util logging.py that..." 
    

認証情報はシステムに安全に保存されます。詳細は[認証情報管理](/ja/docs/claude-code/iam#credential-management)をご覧ください。

## 

​

ステップ3：最初の質問をする

コードベースを理解することから始めましょう。これらのコマンドのいずれかを試してください：
    
    
    > what does this project do?
    

Claudeはファイルを分析して概要を提供します。より具体的な質問もできます：
    
    
    > what technologies does this project use?
    
    
    
    > where is the main entry point?
    
    
    
    > explain the folder structure
    

Claudeの機能について質問することもできます：
    
    
    > what can Claude Code do?
    
    
    
    > how do I use slash commands in Claude Code?
    
    
    
    > can Claude Code work with Docker?
    

Claude Codeは必要に応じてファイルを読み取ります - 手動でコンテキストを追加する必要はありません。Claudeは独自のドキュメントにもアクセスでき、その機能について質問に答えることができます。

## 

​

ステップ4：最初のコード変更を行う

次に、Claude Codeに実際のコーディングをさせてみましょう。簡単なタスクを試してください：
    
    
    > add a hello world function to the main file
    

Claude Codeは以下を行います：

  1. 適切なファイルを見つける
  2. 提案された変更を表示する
  3. 承認を求める
  4. 編集を実行する



Claude Codeはファイルを変更する前に常に許可を求めます。個別の変更を承認するか、セッションで「すべて承認」モードを有効にできます。

## 

​

ステップ5：Claude CodeでGitを使用する

Claude CodeはGit操作を会話形式にします：
    
    
    > what files have I changed?
    
    
    
    > commit my changes with a descriptive message
    

より複雑なGit操作を促すこともできます：
    
    
    > create a new branch called feature/quickstart
    
    
    
    > show me the last 5 commits
    
    
    
    > help me resolve merge conflicts
    

## 

​

ステップ6：バグを修正するか機能を追加する

Claudeはデバッグと機能実装に熟練しています。

自然言語で欲しいものを説明してください：
    
    
    > add input validation to the user registration form
    

または既存の問題を修正してください：
    
    
    > there's a bug where users can submit empty forms - fix it
    

Claude Codeは以下を行います：

  * 関連するコードを特定する
  * コンテキストを理解する
  * ソリューションを実装する
  * 利用可能な場合はテストを実行する



## 

​

ステップ7：その他の一般的なワークフローを試す

Claudeと作業する方法は数多くあります：

**コードをリファクタリングする**
    
    
    > refactor the authentication module to use async/await instead of callbacks
    

**テストを書く**
    
    
    > write unit tests for the calculator functions
    

**ドキュメントを更新する**
    
    
    > update the README with installation instructions
    

**コードレビュー**
    
    
    > review my changes and suggest improvements
    

**覚えておいてください** ：Claude CodeはあなたのAIペアプログラマーです。役に立つ同僚に話しかけるように話しかけてください - 達成したいことを説明すれば、そこに到達するのを手助けしてくれます。

## 

​

必須コマンド

日常使用で最も重要なコマンドは以下の通りです：

コマンド| 機能| 例  
---|---|---  
`claude`| インタラクティブモードを開始| `claude`  
`claude "task"`| 一回限りのタスクを実行| `claude "fix the build error"`  
`claude -p "query"`| 一回限りのクエリを実行して終了| `claude -p "explain this function"`  
`claude -c`| 最新の会話を続行| `claude -c`  
`claude -r`| 以前の会話を再開| `claude -r`  
`claude commit`| Gitコミットを作成| `claude commit`  
`/clear`| 会話履歴をクリア| `> /clear`  
`/help`| 利用可能なコマンドを表示| `> /help`  
`exit` または Ctrl+C| Claude Codeを終了| `> exit`  
  
コマンドの完全なリストについては、[CLIリファレンス](/ja/docs/claude-code/cli-reference)をご覧ください。

## 

​

初心者向けのプロのヒント

リクエストは具体的に

「バグを修正して」ではなく

「間違った認証情報を入力した後にユーザーが空白画面を見るログインバグを修正して」と試してください

ステップバイステップの指示を使用する

複雑なタスクをステップに分割してください：
    
    
    > 1. create a new database table for user profiles
    
    
    
    > 2. create an API endpoint to get and update user profiles
    
    
    
    > 3. build a webpage that allows users to see and edit their information
    

Claudeに最初に探索させる

変更を加える前に、Claudeにコードを理解させてください：
    
    
    > analyze the database schema
    
    
    
    > build a dashboard showing products that are most frequently returned by our UK customers
    

ショートカットで時間を節約する

  * コマンド補完にはTabを使用
  * コマンド履歴には↑を押す
  * すべてのスラッシュコマンドを見るには`/`を入力



## 

​

次のステップ

基本を学んだので、より高度な機能を探索してください：

## [一般的なワークフロー一般的なタスクのステップバイステップガイド](/ja/docs/claude-code/common-workflows)## [CLIリファレンスすべてのコマンドとオプションをマスターする](/ja/docs/claude-code/cli-reference)## [設定ワークフローに合わせてClaude Codeをカスタマイズする](/ja/docs/claude-code/settings)

## 

​

ヘルプを得る

  * **Claude Code内で** ：`/help`と入力するか「how do I…」と質問してください
  * **ドキュメント** ：ここにいます！他のガイドを参照してください
  * **コミュニティ** ：ヒントとサポートのために[Discord](https://www.anthropic.com/discord)に参加してください



Was this page helpful?

YesNo

[Overview](/ja/docs/claude-code/overview)[一般的なワークフロー](/ja/docs/claude-code/common-workflows)

[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)

On this page

  * 始める前に
  * ステップ1：Claude Codeをインストールする
  * NPMインストール
  * ネイティブインストール
  * ステップ2：最初のセッションを開始する
  * ステップ3：最初の質問をする
  * ステップ4：最初のコード変更を行う
  * ステップ5：Claude CodeでGitを使用する
  * ステップ6：バグを修正するか機能を追加する
  * ステップ7：その他の一般的なワークフローを試す
  * 必須コマンド
  * 初心者向けのプロのヒント
  * 次のステップ
  * ヘルプを得る




---

## 🏗️ ドキュメント構造

- **クイックスタート**
  ```
  Copy page

Claude Codeへようこそ！

このクイックスタートガイドでは、わずか数分でAI搭載のコーディング支援を使用できるようになります。最後には、一般的な開発タスクでClaude Codeを使用する方法を理解できるでしょう。

## 

​

始める前に

以下を準備してください：

  * ターミナルまたはコマンドプロンプトを開く
  * 作業するコードプロジェクト




  ```
  - **[一般的なワークフロー一般的なタスクのステップバイステップガイド](/ja/docs/claude-code/common-workflows)## [CLIリファレンスすべてのコマンドとオプションをマスターする](/ja/docs/claude-code/cli-reference)## [設定ワークフローに合わせてClaude Codeをカスタマイズする](/ja/docs/claude-code/settings)**
    ```
    ## 

​

ヘルプを得る

  * **Claude Code内で** ：`/help`と入力するか「how do I…」と質問してください
  * **ドキュメント** ：ここにいます！他のガイドを参照してください
  * **コミュニティ** ：ヒントとサポートのために[Discord](https://www.anthropic.com/discord)に参加してください



Was 
    ```

## 🔍 抽出されたエンティティ

### URLs
- https://www.anthropic.com/discord)
- https://x.com/AnthropicAI)
- https://www.anthropic.com/research)
- https://www.anthropic.com/discord)に参加してください
- https://console.anthropic.com/login)
- https://www.linkedin.com/company/anthropicresearch)
- https://claude.ai/install.ps1
- https://support.anthropic.com/)
- https://nodejs.org/en/download/)場合：

### キーワード
Google Vertex, Claude Code, Amazon Bedrock, Model Context Protocol, Developer Platform
