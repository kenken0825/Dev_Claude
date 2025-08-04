# YAML Context Engineering MCP Server

階層的なコンテキスト情報を抽出し、YAML形式のドキュメントを自動生成するMCPサーバー実装。

## 機能

- **URLクロール**: 指定されたURLからコンテンツを取得
- **階層構造抽出**: L1、L2、L3レベルの見出し構造を自動識別
- **コンテンツ要約**: 各セクションの内容を要約・抽出
- **YAML生成**: 構造化されたYAML frontmatterを持つMarkdownファイルを生成
- **自律的クロール**: 関連URLを発見し、再帰的に処理

## インストール

```bash
pip install -e .
```

## 使用方法

### MCPサーバーとして起動

```bash
yaml-context-mcp
```

### プログラムから使用

```python
from yaml_context_engineering import YamlContextServer

server = YamlContextServer()
await server.start()
```

## ツール

### web_content_fetcher

指定されたURLからウェブページのコンテンツを取得します。

```json
{
  "tool": "web_content_fetcher",
  "params": {
    "urls": ["https://example.com"],
    "timeout": 30
  }
}
```

### llm_structure_extractor

テキストコンテンツから階層的な見出し構造を抽出します。

```json
{
  "tool": "llm_structure_extractor",
  "params": {
    "content": "...",
    "target_schema": {},
    "extraction_config": {}
  }
}
```

### url_discovery_engine

コンテンツから関連URLを発見し、優先度付きで返します。

```json
{
  "tool": "url_discovery_engine",
  "params": {
    "content": "...",
    "base_domain": "example.com",
    "filters": []
  }
}
```

### file_system_manager

ディレクトリ作成、ファイル書き込み、パス管理を行います。

## 開発

### 依存関係のインストール

```bash
pip install -r requirements.txt
```

### テストの実行

```bash
pytest
```

### コードフォーマット

```bash
black src/ tests/
```

## ライセンス

MIT License