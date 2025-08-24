# n8n Context Improvement Plan
## 自動化実現のための追加取得計画

### 📊 現状分析サマリー
- **現在の充足度**: 全体で約30%
- **自動化可能レベル**: 単純なワークフローのみ（60%精度）
- **必要な追加取得量**: 約5,000行以上の詳細仕様

### 🎯 優先度1: 必須取得項目（24時間以内）

#### 1. 主要20ノードの完全仕様
```yaml
priority_nodes:
  - Webhook (完全なパラメータスキーマ)
  - HTTP Request (全オプション詳細)
  - Slack (全リソース・操作の仕様)
  - Database (PostgreSQL, MySQL, MongoDB)
  - Google Sheets (全操作の入出力)
  - Email (送信・受信の全パラメータ)
  - FTP/SFTP (接続・転送オプション)
  - Code (実行環境の詳細)
  - IF (条件式の完全仕様)
  - Switch (分岐ロジック詳細)
```

#### 2. パラメータ型システム
```typescript
interface NodeParameter {
  name: string;
  type: 'string' | 'number' | 'boolean' | 'json' | 'dateTime' | 'collection';
  required: boolean;
  default?: any;
  description: string;
  options?: Array<{label: string, value: any}>;
  validation?: {
    min?: number;
    max?: number;
    regex?: string;
    custom?: string;
  };
  displayOptions?: {
    show?: Record<string, any[]>;
    hide?: Record<string, any[]>;
  };
}
```

### 🎯 優先度2: 品質向上項目（1週間以内）

#### 1. 実装例の収集
- GitHubから実際のworkflow.jsonを20個以上収集
- 各パターンごとに3つ以上の実装例
- エラーハンドリングの実装例

#### 2. ノード間依存関係マップ
```yaml
dependency_map:
  webhook:
    compatible_with: ["all"]
    commonly_followed_by: ["function", "http", "slack"]
  
  database_read:
    requires_before: ["database_credential"]
    compatible_with: ["transform", "filter", "aggregate"]
```

### 🎯 優先度3: 完全性確保（2週間以内）

#### 1. 全400+ノードのインデックス作成
- ノード名、カテゴリ、基本用途のマッピング
- 最低限の入出力仕様

#### 2. 認証システムの詳細
- 各認証タイプの設定手順
- 必要なスコープ・権限
- トークンリフレッシュロジック

### 📈 期待される改善効果

| 指標 | 現在 | 改善後 | 効果 |
|------|------|--------|------|
| **単純ワークフロー生成** | 60% | 95% | +35% |
| **複雑ワークフロー生成** | 20% | 80% | +60% |
| **エラーハンドリング** | 15% | 70% | +55% |
| **パラメータ精度** | 30% | 90% | +60% |
| **実行可能性** | 40% | 85% | +45% |

### 🔧 実行方法

#### Phase 1: GitHub Mining（推奨）
```bash
# n8nリポジトリのクローンと解析
git clone https://github.com/n8n-io/n8n.git
cd n8n/packages/nodes-base/nodes
find . -name "*.node.ts" -exec grep -l "INodeTypeDescription" {} \;
```

#### Phase 2: API Documentation Parsing
```python
# n8n API docsの自動パース
import requests
from bs4 import BeautifulSoup

def extract_node_specs(node_name):
    url = f"https://docs.n8n.io/nodes/{node_name}"
    # パラメータテーブルの抽出
    # 入出力スキーマの解析
    return node_specification
```

#### Phase 3: Workflow Analysis
```javascript
// 実際のworkflowからパターン抽出
const workflows = await fetchPublicWorkflows();
const patterns = analyzeWorkflowPatterns(workflows);
const commonParameters = extractCommonParameters(patterns);
```

### ✅ 成功基準

1. **最小実装要件**
   - 20個の主要ノードの完全仕様
   - 各ノード5個以上のパラメータ定義
   - 10個の実装可能なワークフロー例

2. **品質基準**
   - パラメータカバレッジ 80%以上
   - 型定義の完全性 100%
   - バリデーションルール 70%以上

3. **検証方法**
   - 生成したワークフローの実行テスト
   - n8n CLIでの互換性確認
   - エラー率5%未満

### 📅 タイムライン

| 日程 | アクション | 成果物 |
|------|-----------|---------|
| Day 1 | GitHub解析 | 主要20ノードの仕様 |
| Day 2-3 | パラメータ抽出 | 完全な型定義 |
| Day 4-5 | 実装例収集 | 20個のworkflow.json |
| Day 6-7 | 統合テスト | 検証レポート |

---
*このプランに従って追加取得を行えば、n8nワークフローの自動生成が実用レベルに到達します。*