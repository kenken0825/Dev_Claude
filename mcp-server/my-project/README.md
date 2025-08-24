# my-project - YAML Context Engineering Project

## 概要

YAML Context Engineering Agentを使用したコンテキスト抽出プロジェクトです。
URLやドキュメントから階層的な構造を抽出し、YAML形式で整理されたコンテキストファイルを生成します。

## プロジェクト構造

```
my-project/
├── .claude/                 # Claude Code設定
│   ├── settings.json       # プロジェクト設定
│   ├── agents/            # カスタムエージェント
│   ├── commands/          # カスタムコマンド
│   └── hooks/            # フック設定
├── contexts/              # 抽出されたコンテキスト
│   ├── logs/             # 処理ログ
│   └── @memory-bank.md   # LDD知識ベース
├── src/                   # ソースコード
├── tests/                 # テストコード
├── docs/                  # ドキュメント
└── config.json           # プロジェクト設定

```

## セットアップ

### 1. 依存関係のインストール

```bash
cd ../  # mcp-serverディレクトリへ
pip install -r requirements.txt
pip install -e .
```

### 2. LDDシステムの初期化

```bash
yaml-context ldd init
```

### 3. プロジェクトの起動

```bash
# MCPサーバーの起動
python -m yaml_context_engineering.main --output-dir my-project/contexts
```

## 基本的な使用方法

### コンテキスト抽出

```bash
# 単一URLから抽出
yaml-context extract https://example.com/docs

# 複数URLの一括処理
yaml-context extract https://api.example.com/v1 https://api.example.com/v2

# ファイルから抽出
yaml-context extract file://./docs/api.md
```

### Configuration

`config.json`を編集して設定をカスタマイズできます。

## 高度な機能

### LDDシステム（Log-Driven Development）

タスク管理と知識蓄積のためのシステムです。

```bash
# タスクの作成
yaml-context ldd task "APIドキュメント抽出" -p my-project

# メモリバンクへの追加
yaml-context ldd memory "効率的な抽出パターンを発見" -t Pattern
```

### カスタムエージェント

`.claude/agents/`ディレクトリにカスタムエージェントを配置できます。

### フック設定

処理の前後に実行されるスクリプトを設定できます。

## トラブルシューティング

- **ImportError**: Pythonパスを確認 (`export PYTHONPATH="../src:$PYTHONPATH"`)
- **権限エラー**: ディレクトリ権限を確認 (`chmod 755 contexts`)
- **ネットワークエラー**: プロキシ設定を確認

## ライセンス

MIT License
