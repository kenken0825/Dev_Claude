#!/usr/bin/env python3
"""カスタムスキーマでClaude Codeマニュアルを構成"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

import sys
sys.path.insert(0, str(Path(__file__).parent / "src"))

from yaml_context_engineering.config import Config
from yaml_context_engineering.tools import FileSystemManager


async def create_custom_schema():
    """カスタムスキーマで構造化されたマニュアルを作成"""
    
    print("""
╔════════════════════════════════════════════════════════════╗
║    カスタムスキーマ マニュアル構成                        ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    config = Config.from_env()
    config.output.output_base_directory = Path("generated_contexts/claude-code-complete")
    file_manager = FileSystemManager(config)
    
    # カスタムスキーマ定義
    schema = {
        "version": "1.0.0",
        "generated_at": datetime.now().isoformat(),
        "schema_type": "claude-code-manual",
        "metadata": {
            "title": "Claude Code Complete Manual",
            "description": "完全なClaude Codeリファレンスマニュアル",
            "language": "ja",
            "authors": ["YAML Context Engineering Agent"],
            "tags": ["claude-code", "ai", "programming", "documentation"]
        },
        "structure": {
            "sections": [
                {
                    "id": "getting-started",
                    "title": "はじめに",
                    "priority": 1,
                    "content_files": ["quickstart_complete.md"],
                    "subsections": [
                        {
                            "id": "installation",
                            "title": "インストール",
                            "commands": [
                                "npm install -g @anthropic-ai/claude-code",
                                "curl -fsSL claude.ai/install.sh | bash"
                            ]
                        },
                        {
                            "id": "first-steps",
                            "title": "最初のステップ",
                            "commands": ["claude", "claude --help"]
                        }
                    ]
                },
                {
                    "id": "commands",
                    "title": "コマンドリファレンス",
                    "priority": 2,
                    "content_files": ["cli-reference_complete.md"],
                    "subsections": [
                        {
                            "id": "basic-commands",
                            "title": "基本コマンド",
                            "commands": [
                                "claude",
                                "claude \"query\"",
                                "claude -p \"query\"",
                                "claude -c",
                                "claude -r"
                            ]
                        },
                        {
                            "id": "advanced-commands",
                            "title": "上級コマンド",
                            "commands": [
                                "claude commit",
                                "claude --resume",
                                "claude -c -p \"query\""
                            ]
                        }
                    ]
                },
                {
                    "id": "slash-commands",
                    "title": "スラッシュコマンド",
                    "priority": 3,
                    "content_files": ["slash-commands_complete.md"],
                    "subsections": [
                        {
                            "id": "session-management",
                            "title": "セッション管理",
                            "commands": ["/clear", "/exit", "/help"]
                        },
                        {
                            "id": "custom-commands",
                            "title": "カスタムコマンド",
                            "commands": ["/setup", "/config", "/debug"]
                        }
                    ]
                },
                {
                    "id": "troubleshooting",
                    "title": "トラブルシューティング",
                    "priority": 4,
                    "content_files": [],
                    "subsections": [
                        {
                            "id": "common-errors",
                            "title": "よくあるエラー",
                            "solutions": {
                                "認証エラー": "APIキーを確認してください",
                                "メモリ不足": "/clearコマンドを使用",
                                "接続エラー": "ネットワーク設定を確認"
                            }
                        }
                    ]
                }
            ]
        },
        "navigation": {
            "quick_links": [
                {"label": "クイックスタート", "href": "#getting-started"},
                {"label": "コマンド一覧", "href": "#commands"},
                {"label": "トラブルシューティング", "href": "#troubleshooting"}
            ],
            "search_keywords": [
                "claude", "code", "ai", "programming", "command",
                "install", "setup", "git", "commit", "debug"
            ]
        },
        "interactive_features": {
            "command_palette": True,
            "search_enabled": True,
            "copy_to_clipboard": True,
            "dark_mode": True,
            "keyboard_shortcuts": {
                "search": "Ctrl+K",
                "toggle_dark": "Ctrl+D",
                "copy": "Ctrl+C"
            }
        },
        "statistics": {
            "total_commands": 20,
            "total_sections": 4,
            "total_pages": 3,
            "last_updated": datetime.now().isoformat()
        }
    }
    
    # スキーマ保存
    schema_path = config.output.output_base_directory / "schema" / "manual_schema.json"
    schema_path.parent.mkdir(parents=True, exist_ok=True)
    schema_path.write_text(json.dumps(schema, indent=2, ensure_ascii=False), encoding='utf-8')
    
    print(f"✅ カスタムスキーマ保存: schema/manual_schema.json")
    
    # スキーマに基づくインデックス生成
    print("\n📚 スキーマベースのインデックス生成中...")
    
    index_content = generate_schema_based_index(schema)
    
    await file_manager.execute(
        action="write_file",
        path="MASTER_INDEX.md",
        content={
            "title": "Claude Code マスターインデックス",
            "schema_version": schema["version"],
            "body": index_content
        }
    )
    
    print("✅ マスターインデックス生成: MASTER_INDEX.md")
    
    # 検索可能なJSONインデックス生成
    search_index = generate_search_index(schema)
    
    search_path = config.output.output_base_directory / "search" / "search_index.json"
    search_path.parent.mkdir(parents=True, exist_ok=True)
    search_path.write_text(json.dumps(search_index, indent=2, ensure_ascii=False), encoding='utf-8')
    
    print("✅ 検索インデックス生成: search/search_index.json")
    
    # 設定ファイルテンプレート生成
    settings_template = generate_settings_template(schema)
    
    await file_manager.execute(
        action="write_file",
        path="templates/claude_settings_template.json",
        content={
            "title": "Claude Code Settings Template",
            "body": json.dumps(settings_template, indent=2, ensure_ascii=False)
        }
    )
    
    print("✅ 設定テンプレート生成: templates/claude_settings_template.json")
    
    return schema


def generate_schema_based_index(schema: Dict) -> str:
    """スキーマに基づくインデックスを生成"""
    
    index = f"""# 📚 Claude Code マスターインデックス

*Schema Version: {schema['version']}*
*Generated: {schema['generated_at']}*

## 🎯 {schema['metadata']['title']}

{schema['metadata']['description']}

## 🗂️ コンテンツ構造

"""
    
    for section in schema['structure']['sections']:
        index += f"### {section['priority']}. {section['title']}\n\n"
        
        if section.get('content_files'):
            index += "📄 **関連ファイル**: " + ", ".join(f"`{f}`" for f in section['content_files']) + "\n\n"
        
        if section.get('subsections'):
            for subsec in section['subsections']:
                index += f"#### {subsec['title']}\n\n"
                
                if subsec.get('commands'):
                    index += "**コマンド**:\n"
                    for cmd in subsec['commands']:
                        index += f"- `{cmd}`\n"
                    index += "\n"
                
                if subsec.get('solutions'):
                    index += "**解決策**:\n"
                    for problem, solution in subsec['solutions'].items():
                        index += f"- {problem}: {solution}\n"
                    index += "\n"
    
    index += f"""
## 🔍 クイックアクセス

"""
    
    for link in schema['navigation']['quick_links']:
        index += f"- [{link['label']}]({link['href']})\n"
    
    index += f"""

## ⌨️ キーボードショートカット

"""
    
    for action, shortcut in schema['interactive_features']['keyboard_shortcuts'].items():
        index += f"- **{action}**: `{shortcut}`\n"
    
    index += f"""

## 📊 統計情報

- **総コマンド数**: {schema['statistics']['total_commands']}
- **セクション数**: {schema['statistics']['total_sections']}
- **ページ数**: {schema['statistics']['total_pages']}
- **最終更新**: {schema['statistics']['last_updated']}

---

*このインデックスはカスタムスキーマから自動生成されました*
"""
    
    return index


def generate_search_index(schema: Dict) -> Dict:
    """検索可能なインデックスを生成"""
    
    search_index = {
        "version": schema["version"],
        "generated_at": datetime.now().isoformat(),
        "entries": []
    }
    
    # セクションとコマンドをインデックス化
    for section in schema['structure']['sections']:
        entry = {
            "type": "section",
            "id": section['id'],
            "title": section['title'],
            "keywords": [],
            "content_refs": section.get('content_files', [])
        }
        
        # サブセクションのコマンドを収集
        all_commands = []
        for subsec in section.get('subsections', []):
            if subsec.get('commands'):
                all_commands.extend(subsec['commands'])
        
        entry['commands'] = all_commands
        entry['keywords'] = extract_keywords(section['title']) + extract_keywords(' '.join(all_commands))
        
        search_index['entries'].append(entry)
    
    # ナビゲーションキーワードを追加
    search_index['global_keywords'] = schema['navigation']['search_keywords']
    
    return search_index


def extract_keywords(text: str) -> List[str]:
    """テキストからキーワードを抽出"""
    import re
    # 簡易的なキーワード抽出
    words = re.findall(r'\w+', text.lower())
    # ストップワードを除外（簡易版）
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
    return [w for w in words if w not in stopwords and len(w) > 2]


def generate_settings_template(schema: Dict) -> Dict:
    """Claude Code設定テンプレートを生成"""
    
    return {
        "version": "1.0.0",
        "generated_from_schema": schema["version"],
        "claude_code": {
            "api_key": "${ANTHROPIC_API_KEY}",
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 4096,
            "temperature": 0.7
        },
        "hooks": {
            "PreToolUse": [
                {
                    "matcher": "Write",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "prettier --write $FILE_PATH"
                        }
                    ]
                }
            ],
            "PostToolUse": [
                {
                    "matcher": "Edit|Write",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "echo 'File modified: $FILE_PATH' >> ~/.claude/changes.log"
                        }
                    ]
                }
            ]
        },
        "slash_commands": {
            "/help": {
                "description": "Show help information",
                "action": "show_help"
            },
            "/clear": {
                "description": "Clear conversation history",
                "action": "clear_history"
            },
            "/config": {
                "description": "Show configuration",
                "action": "show_config"
            }
        },
        "ui_preferences": {
            "theme": "auto",
            "font_size": "medium",
            "show_line_numbers": True,
            "enable_autocomplete": True
        },
        "performance": {
            "cache_enabled": True,
            "cache_ttl": 3600,
            "max_context_size": 100000
        }
    }


if __name__ == "__main__":
    asyncio.run(create_custom_schema())