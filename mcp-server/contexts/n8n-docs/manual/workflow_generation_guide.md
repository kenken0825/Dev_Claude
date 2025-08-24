# n8n Automatic Workflow Generation Guide

## 概要
このガイドは、自然言語からn8nワークフローを自動生成するための完全なリファレンスです。

## 目次
1. [基本概念](#基本概念)
2. [ワークフロー生成プロセス](#ワークフロー生成プロセス)
3. [ノード選択ロジック](#ノード選択ロジック)
4. [パターンライブラリ](#パターンライブラリ)
5. [実装例](#実装例)

## 基本概念

### ワークフローの構成要素
- **Trigger Node**: ワークフローを開始するイベント
- **Action Node**: 実際の処理を行うノード
- **Core Node**: データ操作や制御フローを管理
- **Credentials**: 外部サービスとの認証情報

### データフロー
```
[Trigger] → [Transform] → [Action] → [Response]
```

## ワークフロー生成プロセス

### 1. 要件分析
```yaml
input_analysis:
  - identify_trigger: "何がワークフローを開始するか"
  - identify_actions: "どのような処理が必要か"
  - identify_targets: "どのサービスと連携するか"
  - identify_conditions: "どのような条件分岐があるか"
```

### 2. ノードマッピング
```yaml
node_mapping:
  triggers:
    "毎日": "Schedule Trigger"
    "Webhookを受信": "Webhook Trigger"
    "メールを受信": "Gmail Trigger"
    
  actions:
    "Slackに送信": "Slack Node"
    "データベースに保存": "Database Node"
    "ファイルを作成": "File Node"
    
  transformations:
    "データを変換": "Code Node"
    "条件で分岐": "IF Node"
    "データをマージ": "Merge Node"
```

### 3. 接続ロジック
```javascript
// ノード間の接続を定義
const connectionRules = {
  dataTypeMatching: true,
  requiredFieldValidation: true,
  errorHandling: 'continue_on_fail'
};
```

## ノード選択ロジック

### 優先順位
1. **Native Integration**: 専用ノードが存在する場合は優先
2. **HTTP Request**: APIが公開されている場合
3. **Code Node**: カスタムロジックが必要な場合

### 選択基準
```yaml
selection_criteria:
  performance:
    - batch_processing_capability
    - rate_limit_handling
    - concurrent_execution
    
  reliability:
    - error_retry_mechanism
    - timeout_configuration
    - fallback_options
    
  maintainability:
    - credential_management
    - version_compatibility
    - documentation_quality
```

## パターンライブラリ

### 1. Webhook to Database
```json
{
  "nodes": [
    {
      "type": "webhook",
      "parameters": {
        "path": "/data-intake",
        "responseMode": "onReceived"
      }
    },
    {
      "type": "function",
      "parameters": {
        "functionCode": "// データ検証と変換"
      }
    },
    {
      "type": "postgres",
      "parameters": {
        "operation": "insert",
        "table": "events"
      }
    }
  ]
}
```

### 2. Scheduled Data Sync
```json
{
  "nodes": [
    {
      "type": "schedule",
      "parameters": {
        "cronExpression": "0 */6 * * *"
      }
    },
    {
      "type": "googleSheets",
      "parameters": {
        "operation": "read"
      }
    },
    {
      "type": "notion",
      "parameters": {
        "operation": "create"
      }
    }
  ]
}
```

### 3. Error Handling Pattern
```json
{
  "nodes": [
    {
      "type": "errorTrigger",
      "parameters": {}
    },
    {
      "type": "slack",
      "parameters": {
        "channel": "#alerts",
        "text": "Workflow error: {{$json.error}}"
      }
    }
  ]
}
```

## 実装例

### Example 1: Slack通知ワークフロー
**入力**: "GitHubにプッシュがあったらSlackに通知"

**生成されるワークフロー**:
```yaml
workflow:
  name: "GitHub to Slack Notification"
  nodes:
    - id: "github_trigger"
      type: "github-trigger"
      parameters:
        events: ["push"]
        
    - id: "format_message"
      type: "function"
      parameters:
        code: |
          return {
            text: `New push to ${$json.repository.name}`,
            author: $json.pusher.name,
            commits: $json.commits.length
          }
          
    - id: "slack_send"
      type: "slack"
      parameters:
        channel: "#dev-updates"
        messageType: "text"
```

### Example 2: データ変換パイプライン
**入力**: "CSVファイルをJSONに変換してAPIに送信"

**生成されるワークフロー**:
```yaml
workflow:
  name: "CSV to API Pipeline"
  nodes:
    - id: "file_trigger"
      type: "file-trigger"
      parameters:
        path: "/data/input/"
        
    - id: "read_csv"
      type: "spreadsheet-file"
      parameters:
        operation: "read"
        
    - id: "transform"
      type: "function"
      parameters:
        code: |
          // CSV to JSON transformation
          return items.map(row => ({
            id: row.id,
            data: row
          }))
          
    - id: "api_send"
      type: "http-request"
      parameters:
        method: "POST"
        url: "https://api.example.com/data"
```

## ベストプラクティス

### 1. エラーハンドリング
- 全てのワークフローにエラーハンドリングノードを追加
- リトライロジックの実装
- エラー通知の設定

### 2. パフォーマンス最適化
- バッチ処理の活用
- 並列処理の実装
- キャッシュの利用

### 3. セキュリティ
- 認証情報の環境変数化
- APIキーの暗号化
- アクセス制限の実装

## 自動生成コードサンプル

```javascript
// ワークフロー自動生成関数
function generateWorkflow(requirements) {
  const workflow = {
    name: requirements.name,
    nodes: [],
    connections: []
  };
  
  // トリガーノードの選択
  const trigger = selectTriggerNode(requirements.trigger);
  workflow.nodes.push(trigger);
  
  // アクションノードの追加
  requirements.actions.forEach(action => {
    const node = selectActionNode(action);
    workflow.nodes.push(node);
  });
  
  // 接続の生成
  workflow.connections = generateConnections(workflow.nodes);
  
  return workflow;
}

// ノード選択関数
function selectTriggerNode(triggerDesc) {
  const triggerMap = {
    'webhook': 'n8n-nodes-base.webhook',
    'schedule': 'n8n-nodes-base.schedule',
    'manual': 'n8n-nodes-base.manualTrigger'
  };
  
  // 自然言語から適切なトリガーを選択
  const triggerType = analyzeTriggerType(triggerDesc);
  return {
    type: triggerMap[triggerType],
    parameters: getDefaultParameters(triggerType)
  };
}
```

## トラブルシューティング

### よくある問題と解決策

1. **認証エラー**
   - Credentialノードの設定確認
   - OAuth2フローの再実行
   - APIキーの有効期限確認

2. **データ型不一致**
   - Transform nodeで型変換
   - JSON/XML変換の実装
   - Schema validationの追加

3. **レート制限**
   - Wait nodeの追加
   - Batch処理の実装
   - Retry with exponential backoff

## まとめ
このガイドを使用することで、自然言語の要求からn8nワークフローを自動的に生成できます。生成されたワークフローは、必要に応じて手動で調整・最適化が可能です。