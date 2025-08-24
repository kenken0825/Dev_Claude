# 📁 YAML Context Engineering - フォルダ構成ガイド

## 推奨フォルダ構造

```
mcp-server/
├── 📂 contexts/                    # すべてのコンテキストのルート
│   ├── 📂 slack-api/               # Slack API コンテキスト
│   │   ├── 📄 manifest.yaml        # コンテキストメタデータ
│   │   ├── 📂 raw/                 # 生データ
│   │   │   ├── slack_api_docs.md
│   │   │   └── slack_api_structure.json
│   │   ├── 📂 dsl/                 # DSL形式
│   │   │   ├── slack_api_dsl.txt
│   │   │   └── SLACK_API_DSL_COMPLETE.md
│   │   ├── 📂 manual/              # マニュアル
│   │   │   └── slack_api_manual.md
│   │   └── 📂 cache/               # キャッシュデータ
│   │       └── extracted_urls.json
│   │
│   ├── 📂 aws-docs/                # AWS ドキュメント（例）
│   │   ├── 📄 manifest.yaml
│   │   ├── 📂 raw/
│   │   ├── 📂 dsl/
│   │   ├── 📂 manual/
│   │   └── 📂 cache/
│   │
│   ├── 📂 github-api/              # GitHub API（例）
│   │   ├── 📄 manifest.yaml
│   │   ├── 📂 raw/
│   │   ├── 📂 dsl/
│   │   ├── 📂 manual/
│   │   └── 📂 cache/
│   │
│   └── 📄 INDEX.md                 # 全コンテキストのインデックス
│
├── 📂 templates/                    # 共通テンプレート
│   ├── context_template.yaml
│   ├── dsl_template.txt
│   └── manual_template.md
│
├── 📂 scripts/                      # 抽出スクリプト
│   ├── extract_slack_full.py
│   ├── extract_generic.py
│   └── utils/
│       ├── dsl_generator.py
│       └── hierarchy_parser.py
│
├── 📂 config/                       # 設定ファイル
│   ├── sources.yaml                # ソース定義
│   ├── extraction_rules.yaml       # 抽出ルール
│   └── .env                        # 環境変数
│
└── 📂 logs/                        # ログファイル
    ├── extraction/
    ├── errors/
    └── metrics/
```

## manifest.yaml の例

```yaml
---
context_name: "Slack API Documentation"
version: "1.0.0"
source_url: "https://api.slack.com/docs"
extraction_date: "2025-08-07"
metadata:
  total_urls: 13
  max_depth: 4
  confidence_avg: 0.65
  language: "en"
  category: "API Documentation"
tags:
  - api
  - slack
  - messaging
  - collaboration
files:
  raw:
    - slack_api_docs.md
    - slack_api_structure.json
  dsl:
    - slack_api_dsl.txt
    - SLACK_API_DSL_COMPLETE.md
  manual:
    - slack_api_manual.md
dependencies:
  - events-api
  - web-api
  - rtm-api
---
```

## コンテキスト追加の手順

### 1. 新規コンテキストの作成

```bash
# 新しいコンテキストディレクトリを作成
yaml-context setup-context <context-name>

# 例: OpenAI APIドキュメントを追加
yaml-context setup-context openai-api
```

### 2. 抽出の実行

```bash
# 特定のコンテキストに抽出
yaml-context extract <sources> --context <context-name>

# 例:
yaml-context extract https://platform.openai.com/docs --context openai-api
```

### 3. マニフェストの自動生成

```bash
# コンテキストのマニフェストを生成/更新
yaml-context update-manifest --context <context-name>
```

## 設定ファイル: sources.yaml

```yaml
---
sources:
  slack-api:
    primary_urls:
      - https://api.slack.com/docs
      - https://api.slack.com/methods
      - https://api.slack.com/reference
    extraction_config:
      max_depth: 4
      rate_limit: 1.0
      patterns:
        - "/docs"
        - "/methods"
        - "/reference"
    
  aws-docs:
    primary_urls:
      - https://docs.aws.amazon.com/
    extraction_config:
      max_depth: 3
      rate_limit: 2.0
      patterns:
        - "/lambda/"
        - "/s3/"
        - "/ec2/"
  
  github-api:
    primary_urls:
      - https://docs.github.com/rest
      - https://docs.github.com/graphql
    extraction_config:
      max_depth: 3
      rate_limit: 1.5
---
```

## グローバルインデックス: INDEX.md

```markdown
# 📚 Context Library Index

## Available Contexts

### 1. Slack API
- **Path**: `contexts/slack-api/`
- **Version**: 1.0.0
- **URLs**: 13
- **Depth**: L4
- **Last Updated**: 2025-08-07

### 2. AWS Documentation
- **Path**: `contexts/aws-docs/`
- **Version**: 1.0.0
- **URLs**: TBD
- **Depth**: L3
- **Last Updated**: TBD

### 3. GitHub API
- **Path**: `contexts/github-api/`
- **Version**: 1.0.0
- **URLs**: TBD
- **Depth**: L3
- **Last Updated**: TBD

## Quick Access

- [All DSL Files](./*/dsl/)
- [All Manuals](./*/manual/)
- [All Raw Data](./*/raw/)

## Statistics

- **Total Contexts**: 3
- **Total URLs Processed**: 13+
- **Total Storage**: ~1MB
```

## CLI コマンドの拡張案

```bash
# コンテキスト管理コマンド
yaml-context list                           # すべてのコンテキストをリスト
yaml-context info <context-name>            # 特定のコンテキストの情報
yaml-context delete <context-name>          # コンテキストを削除
yaml-context merge <context1> <context2>    # コンテキストをマージ

# 検索コマンド
yaml-context search <query>                 # 全コンテキストを検索
yaml-context search <query> --context <name> # 特定のコンテキスト内を検索

# エクスポート/インポート
yaml-context export <context-name> --format zip
yaml-context import <archive-file>

# 比較・差分
yaml-context diff <context1> <context2>
yaml-context update <context-name>          # 最新版との差分を取得
```

## 利点

### 1. **スケーラビリティ**
- 新しいコンテキストを簡単に追加
- 各コンテキストは独立して管理

### 2. **整理性**
- 明確な階層構造
- 一貫したファイル配置

### 3. **再利用性**
- 共通テンプレートの活用
- スクリプトの共有

### 4. **検索性**
- グローバルインデックス
- メタデータによる管理

### 5. **バージョン管理**
- 各コンテキストごとのバージョン
- 更新履歴の追跡

## 移行手順

現在のファイルを新構造に移行：

```bash
# 1. 新しいディレクトリ構造を作成
mkdir -p contexts/slack-api/{raw,dsl,manual,cache}

# 2. 既存ファイルを移動
mv my-project/generated_contexts/slack_api_*.md contexts/slack-api/raw/
mv my-project/generated_contexts/slack_api_dsl.txt contexts/slack-api/dsl/
mv my-project/generated_contexts/SLACK_API_DSL_COMPLETE.md contexts/slack-api/dsl/
mv my-project/generated_contexts/slack_api_manual.md contexts/slack-api/manual/
mv my-project/generated_contexts/slack_api_structure.json contexts/slack-api/raw/

# 3. マニフェストを作成
yaml-context update-manifest --context slack-api
```

## 次のステップ

1. **フォルダ構造の実装**
2. **CLIコマンドの拡張**
3. **自動インデックス生成**
4. **検索機能の実装**
5. **GitHub Actionsとの統合**

この構造により、複数のAPIドキュメントやコンテキストを体系的に管理できます。