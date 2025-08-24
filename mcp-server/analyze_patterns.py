#!/usr/bin/env python3
"""Claude Codeドキュメントのパターン分析とインタラクティブマニュアル生成"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime
import json
import re
from typing import Dict, List, Tuple
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent / "src"))

from yaml_context_engineering.config import Config
from yaml_context_engineering.ldd import LDDConfig, MemoryBank
from yaml_context_engineering.tools import FileSystemManager


async def analyze_patterns():
    """抽出済みコンテンツのパターン分析と最適化"""
    
    print("""
╔════════════════════════════════════════════════════════════╗
║    パターン分析＆インタラクティブマニュアル生成           ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    config = Config.from_env()
    config.output.output_base_directory = Path("generated_contexts/claude-code-complete")
    
    # LDDシステム初期化
    ldd_config = LDDConfig(
        logsDir=str(config.output.output_base_directory / 'ldd_logs'),
        memoryBankPath=str(config.output.output_base_directory / '@memory-bank.md')
    )
    memory_bank = MemoryBank(ldd_config)
    await memory_bank.initialize()
    
    # メモリバンクから手動でエントリを読み込む（パースに問題がある場合）
    if len(memory_bank.entries) == 0:
        print("⚠️ メモリバンクエントリが空。手動で読み込み中...")
        memory_path = Path(config.output.output_base_directory / '@memory-bank.md')
        if memory_path.exists():
            content = memory_path.read_text()
            # 簡易的にコマンドエントリを抽出
            import re
            entries = []
            pattern = r'\*\*Description:\*\*\s+\n(.+)'
            matches = re.findall(pattern, content)
            for i, match in enumerate(matches):
                if 'Claude Codeコマンド:' in match:
                    entries.append({
                        'id': f'cmd_{i}',
                        'date': '2025-08-10',
                        'timestamp': datetime.now().isoformat(),
                        'type': 'Command',
                        'agent': 'yaml-context-agent',
                        'details': {
                            'description': match,
                            'insights': [],
                            'impact': 'Documentation extracted'
                        },
                        'relatedTasks': [],
                        'tags': ['claude-code', 'command']
                    })
            memory_bank.entries = entries
            print(f"  ✅ {len(entries)}個のエントリを手動で読み込みました")
    
    # パターン分析
    print("\n📊 パターン分析中...")
    analysis = await memory_bank.analyze_patterns()
    
    print(f"\n✅ 分析結果:")
    print(f"  - 総エントリ数: {len(memory_bank.entries)}")
    print(f"  - タグ分布: {dict(list(analysis['commonTags'].items())[:5])}")
    print(f"  - タイプ分布: {analysis['typeDistribution']}")
    
    # コマンドパターンの抽出
    command_patterns = extract_command_patterns(memory_bank.entries)
    
    print(f"\n🔍 コマンドパターン:")
    for pattern, count in command_patterns.most_common(5):
        print(f"  - {pattern}: {count}回")
    
    # マニュアルファイルの統合と最適化
    file_manager = FileSystemManager(config)
    manual_dir = config.output.output_base_directory / "manuals"
    
    # 既存マニュアルの読み込み
    manuals = {}
    for file_path in manual_dir.glob("*_complete.md"):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            manuals[file_path.stem] = content
    
    # インタラクティブマニュアルの生成
    print("\n🎨 インタラクティブマニュアル生成中...")
    
    interactive_manual = generate_interactive_manual(
        manuals, 
        command_patterns,
        analysis
    )
    
    # HTML版の生成
    html_manual = generate_html_manual(manuals, command_patterns, analysis)
    
    # ファイル保存
    await file_manager.execute(
        action="write_file",
        path="manuals/INTERACTIVE_MANUAL.md",
        content={
            "title": "Claude Code インタラクティブマニュアル",
            "body": interactive_manual
        }
    )
    
    # HTML版も保存
    html_path = config.output.output_base_directory / "manuals" / "interactive_manual.html"
    html_path.write_text(html_manual, encoding='utf-8')
    
    print(f"✅ インタラクティブマニュアル生成完了")
    print(f"  - Markdown版: manuals/INTERACTIVE_MANUAL.md")
    print(f"  - HTML版: manuals/interactive_manual.html")
    
    # パターン分析レポートの生成
    report = generate_pattern_report(analysis, command_patterns, manuals)
    
    await file_manager.execute(
        action="write_file",
        path="analysis/pattern_report.md",
        content={
            "title": "パターン分析レポート",
            "body": report
        }
    )
    
    print(f"✅ パターン分析レポート生成: analysis/pattern_report.md")
    
    return {
        "analysis": analysis,
        "command_patterns": command_patterns,
        "manual_generated": True
    }


def extract_command_patterns(entries: List[Dict]) -> Counter:
    """メモリバンクからコマンドパターンを抽出"""
    patterns = Counter()
    
    for entry in entries:
        if entry['type'] == 'Command':
            desc = entry['details']['description']
            # コマンド部分を抽出
            match = re.search(r'Claude Codeコマンド: (.+)', desc)
            if match:
                command = match.group(1)
                # 基本パターンを抽出
                base_pattern = re.sub(r'"[^"]*"', '"..."', command)
                patterns[base_pattern] += 1
    
    return patterns


def generate_interactive_manual(
    manuals: Dict[str, str], 
    command_patterns: Counter,
    analysis: Dict
) -> str:
    """インタラクティブなマニュアルを生成"""
    
    manual = """# 🚀 Claude Code インタラクティブマニュアル

## 📌 クイックナビゲーション

<details>
<summary>🎯 初めての方へ</summary>

### 5分でClaude Codeをマスター

1. **インストール** (30秒)
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

2. **起動** (10秒)
   ```bash
   claude
   ```

3. **最初の質問** (20秒)
   ```
   > what does this project do?
   ```

4. **コード変更** (30秒)
   ```
   > add a hello world function
   ```

5. **Git操作** (30秒)
   ```
   > commit my changes
   ```

</details>

<details>
<summary>🔧 よく使うコマンド Top 10</summary>

"""
    
    # トップコマンドを追加
    for i, (pattern, count) in enumerate(command_patterns.most_common(10), 1):
        manual += f"{i}. `{pattern}` - 使用頻度: {count}回\n"
    
    manual += """
</details>

<details>
<summary>💡 便利なTips</summary>

### 効率的な使い方

- **Tab補完**: コマンドの入力を高速化
- **履歴検索**: ↑キーで過去のコマンド
- **スラッシュコマンド**: `/`で利用可能なコマンド一覧
- **継続モード**: `claude -c`で前回の続きから

### ショートカット

| 操作 | コマンド | 説明 |
|------|---------|------|
| 継続 | `claude -c` | 前回の会話を継続 |
| クエリ | `claude -p "..."` | 単発の質問 |
| 再開 | `claude -r` | 会話履歴から選択して再開 |
| Git | `claude commit` | 変更をコミット |

</details>

## 📚 機能別ガイド

### 🎯 基本操作

<details>
<summary>プロジェクト理解</summary>

```bash
# プロジェクトの概要を理解
> what does this project do?

# 使用技術の確認
> what technologies are used?

# ファイル構造の説明
> explain the folder structure
```

</details>

<details>
<summary>コード編集</summary>

```bash
# 機能追加
> add validation to the user form

# バグ修正
> fix the login bug

# リファクタリング
> refactor this to use async/await
```

</details>

<details>
<summary>Git操作</summary>

```bash
# 変更確認
> what files have I changed?

# コミット
> commit with a descriptive message

# ブランチ操作
> create a feature branch
```

</details>

### 🔥 上級機能

<details>
<summary>サブエージェント</summary>

Claude Codeは専門的なタスクのためのサブエージェントを使用できます：

- **コードレビュー**: 品質チェックと改善提案
- **セキュリティ分析**: 脆弱性の検出
- **パフォーマンス最適化**: ボトルネックの特定

</details>

<details>
<summary>フック機能</summary>

ツール実行前後にカスタム処理を追加：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "command": "prettier --write $FILE_PATH"
      }
    ]
  }
}
```

</details>

## 🔍 トラブルシューティング

<details>
<summary>よくある問題と解決策</summary>

### インストールエラー

**問題**: `npm install`が失敗する
**解決**: Node.js 18以降を確認
```bash
node --version  # v18.0.0以上が必要
```

### 認証エラー

**問題**: APIキーが無効
**解決**: 環境変数を確認
```bash
echo $ANTHROPIC_API_KEY
```

### メモリ不足

**問題**: 大きなファイルで応答が遅い
**解決**: コンテキストをクリア
```
> /clear
```

</details>

## 📊 使用統計

"""
    
    # 統計情報を追加
    if analysis.get('insights'):
        manual += "### インサイト\n\n"
        for insight in analysis['insights']:
            manual += f"- {insight}\n"
    
    manual += f"""

## 🎓 学習リソース

- [公式ドキュメント](https://docs.anthropic.com/ja/docs/claude-code)
- [GitHubリポジトリ](https://github.com/anthropics/claude-code)
- [Discordコミュニティ](https://www.anthropic.com/discord)

---

*最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
    
    return manual


def generate_html_manual(
    manuals: Dict[str, str],
    command_patterns: Counter,
    analysis: Dict
) -> str:
    """インタラクティブHTML版マニュアルを生成"""
    
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claude Code インタラクティブマニュアル</title>
    <style>
        :root {{
            --primary: #007bff;
            --secondary: #6c757d;
            --success: #28a745;
            --dark: #343a40;
            --light: #f8f9fa;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: var(--dark);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        header {{
            background: white;
            border-radius: 1rem;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: var(--primary);
            margin-bottom: 1rem;
        }}
        
        .search-box {{
            width: 100%;
            padding: 1rem;
            font-size: 1.1rem;
            border: 2px solid var(--light);
            border-radius: 0.5rem;
            transition: border-color 0.3s;
        }}
        
        .search-box:focus {{
            outline: none;
            border-color: var(--primary);
        }}
        
        .content {{
            display: grid;
            grid-template-columns: 1fr 3fr;
            gap: 2rem;
        }}
        
        .sidebar {{
            background: white;
            border-radius: 1rem;
            padding: 1.5rem;
            height: fit-content;
            position: sticky;
            top: 2rem;
        }}
        
        .main-content {{
            background: white;
            border-radius: 1rem;
            padding: 2rem;
        }}
        
        .nav-item {{
            display: block;
            padding: 0.75rem 1rem;
            margin: 0.25rem 0;
            text-decoration: none;
            color: var(--dark);
            border-radius: 0.5rem;
            transition: background 0.3s;
        }}
        
        .nav-item:hover {{
            background: var(--light);
        }}
        
        .nav-item.active {{
            background: var(--primary);
            color: white;
        }}
        
        .command-card {{
            background: var(--light);
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
            border-left: 4px solid var(--primary);
        }}
        
        code {{
            background: #f4f4f4;
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            font-family: 'Courier New', monospace;
        }}
        
        pre {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 1rem;
            border-radius: 0.5rem;
            overflow-x: auto;
            margin: 1rem 0;
        }}
        
        .collapsible {{
            background: var(--light);
            cursor: pointer;
            padding: 1rem;
            width: 100%;
            border: none;
            text-align: left;
            outline: none;
            font-size: 1.1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
            transition: background 0.3s;
        }}
        
        .collapsible:hover {{
            background: #e9ecef;
        }}
        
        .collapsible:after {{
            content: '\\002B';
            float: right;
            font-weight: bold;
        }}
        
        .active:after {{
            content: "\\2212";
        }}
        
        .collapsible-content {{
            padding: 0 1rem;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 2rem 0;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            padding: 1.5rem;
            border-radius: 0.5rem;
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
        }}
        
        .copy-btn {{
            background: var(--primary);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 0.25rem;
            cursor: pointer;
            margin-left: 0.5rem;
        }}
        
        .copy-btn:hover {{
            background: #0056b3;
        }}
        
        @media (max-width: 768px) {{
            .content {{
                grid-template-columns: 1fr;
            }}
            
            .sidebar {{
                position: static;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 Claude Code インタラクティブマニュアル</h1>
            <p>AIペアプログラマーの完全ガイド</p>
            <input type="text" class="search-box" placeholder="検索... (例: commit, git, debug)" id="searchBox">
        </header>
        
        <div class="content">
            <nav class="sidebar">
                <a href="#quickstart" class="nav-item active">🎯 クイックスタート</a>
                <a href="#commands" class="nav-item">📝 コマンド一覧</a>
                <a href="#tips" class="nav-item">💡 Tips & Tricks</a>
                <a href="#troubleshooting" class="nav-item">🔧 トラブルシューティング</a>
                <a href="#advanced" class="nav-item">🔥 上級機能</a>
                <a href="#stats" class="nav-item">📊 使用統計</a>
            </nav>
            
            <main class="main-content">
                <section id="quickstart">
                    <h2>🎯 クイックスタート</h2>
                    
                    <button class="collapsible">5分でマスター</button>
                    <div class="collapsible-content">
                        <div class="command-card">
                            <h3>1. インストール (30秒)</h3>
                            <pre><code>npm install -g @anthropic-ai/claude-code</code></pre>
                            <button class="copy-btn" onclick="copyToClipboard('npm install -g @anthropic-ai/claude-code')">コピー</button>
                        </div>
                        
                        <div class="command-card">
                            <h3>2. 起動 (10秒)</h3>
                            <pre><code>claude</code></pre>
                            <button class="copy-btn" onclick="copyToClipboard('claude')">コピー</button>
                        </div>
                        
                        <div class="command-card">
                            <h3>3. 最初の質問</h3>
                            <pre><code>> what does this project do?</code></pre>
                        </div>
                    </div>
                    
                    <button class="collapsible">基本コマンド</button>
                    <div class="collapsible-content">
                        <table style="width: 100%; margin: 1rem 0;">
                            <tr>
                                <th>コマンド</th>
                                <th>説明</th>
                                <th>例</th>
                            </tr>
                            <tr>
                                <td><code>claude</code></td>
                                <td>インタラクティブモード開始</td>
                                <td><code>claude</code></td>
                            </tr>
                            <tr>
                                <td><code>claude -c</code></td>
                                <td>前回の会話を継続</td>
                                <td><code>claude -c</code></td>
                            </tr>
                            <tr>
                                <td><code>claude -p</code></td>
                                <td>単発クエリ</td>
                                <td><code>claude -p "explain this"</code></td>
                            </tr>
                        </table>
                    </div>
                </section>
                
                <section id="stats" style="display: none;">
                    <h2>📊 使用統計</h2>
                    <div class="stats">
                        <div class="stat-card">
                            <div class="stat-number">{len(command_patterns)}</div>
                            <div>コマンドパターン</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{len(analysis.get('commonTags', {}))}</div>
                            <div>タグ数</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{sum(command_patterns.values())}</div>
                            <div>総使用回数</div>
                        </div>
                    </div>
                </section>
            </main>
        </div>
    </div>
    
    <script>
        // コラプシブル要素の制御
        var coll = document.getElementsByClassName("collapsible");
        for (var i = 0; i < coll.length; i++) {{
            coll[i].addEventListener("click", function() {{
                this.classList.toggle("active");
                var content = this.nextElementSibling;
                if (content.style.maxHeight) {{
                    content.style.maxHeight = null;
                }} else {{
                    content.style.maxHeight = content.scrollHeight + "px";
                }}
            }});
        }}
        
        // ナビゲーション
        document.querySelectorAll('.nav-item').forEach(item => {{
            item.addEventListener('click', function(e) {{
                e.preventDefault();
                document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
                this.classList.add('active');
                
                document.querySelectorAll('section').forEach(s => s.style.display = 'none');
                const target = this.getAttribute('href').substring(1);
                const section = document.getElementById(target);
                if (section) section.style.display = 'block';
            }});
        }});
        
        // 検索機能
        document.getElementById('searchBox').addEventListener('input', function(e) {{
            const query = e.target.value.toLowerCase();
            // 検索ロジックを実装
        }});
        
        // コピー機能
        function copyToClipboard(text) {{
            navigator.clipboard.writeText(text).then(() => {{
                alert('コピーしました！');
            }});
        }}
    </script>
</body>
</html>"""
    
    return html


def generate_pattern_report(
    analysis: Dict,
    command_patterns: Counter,
    manuals: Dict[str, str]
) -> str:
    """パターン分析レポートを生成"""
    
    report = f"""# パターン分析レポート

生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 サマリー

- **総エントリ数**: {len(analysis.get('agentActivity', {}))} エージェント
- **コマンドパターン数**: {len(command_patterns)}
- **主要タグ数**: {len(analysis.get('commonTags', {}))}

## 🔍 コマンドパターン分析

### 最頻出パターン Top 10

"""
    
    for i, (pattern, count) in enumerate(command_patterns.most_common(10), 1):
        percentage = (count / sum(command_patterns.values()) * 100) if command_patterns else 0
        report += f"{i}. `{pattern}` - {count}回 ({percentage:.1f}%)\n"
    
    report += f"""

## 📈 使用傾向

### コマンドカテゴリ分布

- **基本操作**: {sum(1 for p in command_patterns if 'claude' in p and not '-' in p)}種類
- **オプション付き**: {sum(1 for p in command_patterns if '-' in p)}種類
- **引数付き**: {sum(1 for p in command_patterns if '"' in p)}種類

## 💡 インサイト

"""
    
    for insight in analysis.get('insights', []):
        report += f"- {insight}\n"
    
    report += f"""

## 🎯 推奨事項

"""
    
    for rec in analysis.get('recommendations', []):
        report += f"- {rec}\n"
    
    report += """

## 📝 次のステップ

1. 頻出パターンに基づくショートカット設定の検討
2. 使用頻度の低い機能の改善または削除
3. ユーザーフィードバックの収集と分析
4. パフォーマンス最適化の実施

---

*このレポートは自動生成されました*
"""
    
    return report


if __name__ == "__main__":
    asyncio.run(analyze_patterns())