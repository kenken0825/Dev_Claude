#!/usr/bin/env python3
"""Claude Codeドキュメントの完全コンテンツ抽出スクリプト（フルモード）"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime
import json

sys.path.insert(0, str(Path(__file__).parent / "src"))

from yaml_context_engineering.config import Config
from yaml_context_engineering.tools import (
    WebContentFetcher,
    LLMStructureExtractor,
    URLDiscoveryEngine,
    FileSystemManager
)
from yaml_context_engineering.ldd import LDDConfig, MemoryBank


async def extract_full_content():
    """完全なコンテンツを抽出（要約なし、フルテキスト保持）"""
    
    print("""
╔════════════════════════════════════════════════════════════╗
║    Claude Code 完全コンテンツ抽出 (FULL MODE)             ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    # 重要なURLを選択（まずは主要ページから）
    priority_urls = [
        "https://docs.anthropic.com/ja/docs/claude-code/quickstart",  # クイックスタート
        "https://docs.anthropic.com/ja/docs/claude-code/cli-reference",  # CLIリファレンス
        "https://docs.anthropic.com/ja/docs/claude-code/slash-commands",  # スラッシュコマンド
    ]
    
    config = Config.from_env()
    config.output.output_base_directory = Path("generated_contexts/claude-code-complete")
    
    # フル抽出設定
    full_extraction_config = {
        "context_granularity": "full_hierarchy",  # 全階層を保持
        "content_summarization": "full",          # 要約なし、フルコンテンツ
        "language_detection": True,
        "extract_metadata": True,
        "extract_entities": True,                 # エンティティも抽出
        "max_summary_length": 50000               # 長いコンテンツも許可
    }
    
    # ツール初期化
    fetcher = WebContentFetcher(config)
    extractor = LLMStructureExtractor(config)
    discovery = URLDiscoveryEngine(config)
    file_manager = FileSystemManager(config)
    
    # LDDシステム初期化
    ldd_config = LDDConfig(
        logsDir=str(config.output.output_base_directory / 'ldd_logs'),
        memoryBankPath=str(config.output.output_base_directory / '@memory-bank.md'),
        templatePath=str(config.output.output_base_directory / '@template.md')
    )
    memory_bank = MemoryBank(ldd_config)
    await memory_bank.initialize()
    
    extracted_knowledge = []
    
    try:
        for url in priority_urls:
            print(f"\n{'='*60}")
            print(f"📄 完全抽出中: {url}")
            print('='*60)
            
            # Step 1: フルコンテンツ取得
            print("  1️⃣ フルコンテンツ取得中...")
            fetch_results = await fetcher.fetch([url], timeout=60)
            
            if not fetch_results or not fetch_results[0].get("success"):
                print(f"  ❌ 取得失敗")
                continue
            
            # Markdownコンテンツを取得
            content = fetch_results[0].get("content", "")
            title = fetch_results[0].get("title", "")
            
            print(f"  ✅ {len(content)} 文字を取得")
            
            # コンテンツの最初の部分を表示
            preview = content[:500] if len(content) > 500 else content
            print(f"\n  📝 コンテンツプレビュー:")
            print("  " + "-"*50)
            for line in preview.split('\n')[:10]:
                if line.strip():
                    print(f"  | {line[:70]}...")
            print("  " + "-"*50)
            
            # Step 2: 詳細な構造抽出
            print("\n  2️⃣ 詳細構造を抽出中...")
            structure = await extractor.extract(
                content,
                extraction_config=full_extraction_config
            )
            
            # 抽出されたエンティティを表示
            entities = structure.get("extracted_entities", {})
            if entities:
                print(f"  📌 発見されたエンティティ:")
                for entity_type, items in entities.items():
                    if items:
                        print(f"     - {entity_type}: {len(items)}個")
            
            # Step 3: 詳細なコンテンツファイル生成
            print("\n  3️⃣ 完全なマニュアルページ生成中...")
            
            # セクション名を決定
            section_name = url.split('/')[-1]
            
            # 完全なマニュアルコンテンツを構築
            manual_content = f"""# {title}

## 📚 概要

**ソースURL**: {url}
**最終更新**: {datetime.now().isoformat()}
**コンテンツサイズ**: {len(content)} 文字

---

## 📋 完全なコンテンツ

{content}

---

## 🏗️ ドキュメント構造

"""
            # 階層構造を詳細に記述
            def format_structure(headings, level=0):
                lines = []
                for h in headings:
                    indent = "  " * level
                    lines.append(f"{indent}- **{h.get('text', '')}**")
                    if h.get('content'):
                        # 各セクションの内容も含める
                        content_preview = h['content'][:200] if len(h.get('content', '')) > 200 else h.get('content', '')
                        lines.append(f"{indent}  ```")
                        lines.append(f"{indent}  {content_preview}")
                        lines.append(f"{indent}  ```")
                    if h.get('children'):
                        lines.extend(format_structure(h['children'], level + 1))
                return lines
            
            structured_headings = structure.get("structured_headings", [])
            if structured_headings:
                manual_content += "\n".join(format_structure(structured_headings))
            
            # エンティティセクション
            if entities:
                manual_content += "\n\n## 🔍 抽出されたエンティティ\n\n"
                
                if entities.get('urls'):
                    manual_content += "### URLs\n"
                    for url_item in entities['urls'][:20]:
                        manual_content += f"- {url_item}\n"
                
                if entities.get('code_blocks'):
                    manual_content += "\n### コードブロック\n"
                    for i, code in enumerate(entities['code_blocks'][:5]):
                        manual_content += f"\n**コード例 {i+1}:**\n{code}\n"
                
                if entities.get('key_terms'):
                    manual_content += "\n### キーワード\n"
                    manual_content += ", ".join(entities['key_terms'][:30]) + "\n"
            
            # ファイル保存
            file_path = f"manuals/{section_name}_complete.md"
            result = await file_manager.execute(
                action="write_file",
                path=file_path,
                content={
                    "title": title,
                    "source_url": url,
                    "content_type": "manual",
                    "language": "ja",
                    "extraction_confidence": structure.get("confidence_score", 0),
                    "extraction_mode": "full",
                    "body": manual_content
                }
            )
            
            if result.get("success"):
                print(f"  ✅ 完全マニュアル保存: {file_path}")
                
                # 知識をメモリバンクに追加
                knowledge = {
                    "url": url,
                    "title": title,
                    "key_points": [],
                    "commands": [],
                    "tips": []
                }
                
                # コマンドを抽出
                import re
                command_pattern = r'`(claude[^`]*)`|`(npm[^`]*)`|`(curl[^`]*)`'
                commands = re.findall(command_pattern, content)
                for cmd_tuple in commands[:10]:
                    cmd = next((c for c in cmd_tuple if c), '')
                    if cmd:
                        knowledge["commands"].append(cmd)
                
                # キーポイントを抽出（見出しから）
                for heading in structured_headings[:5]:
                    knowledge["key_points"].append(heading.get('text', ''))
                
                extracted_knowledge.append(knowledge)
                print(f"  📝 知識を抽出: {len(knowledge['commands'])}個のコマンド")
            
            else:
                print(f"  ❌ 保存失敗: {result.get('error')}")
        
        # LDDメモリバンクに知識を保存
        print("\n" + "="*60)
        print("🧠 メモリバンクに知識を追加中...")
        
        for knowledge in extracted_knowledge:
            # コマンドをメモリに追加
            for cmd in knowledge["commands"]:
                await memory_bank.append_entry({
                    'type': 'Command',
                    'agent': 'yaml-context-agent',
                    'details': {
                        'description': f"Claude Codeコマンド: {cmd}",
                        'insights': [f"Source: {knowledge['title']}"],
                        'impact': 'Documentation extracted'
                    },
                    'tags': ["claude-code", "command", knowledge["title"].lower().replace(' ', '-')],
                    'relatedTasks': [knowledge["url"]]
                })
            
            # キーポイントを追加
            for point in knowledge["key_points"]:
                await memory_bank.append_entry({
                    'type': 'Insight',
                    'agent': 'yaml-context-agent', 
                    'details': {
                        'description': f"{knowledge['title']}: {point}",
                        'insights': [],
                        'impact': 'Key documentation point'
                    },
                    'tags': ["claude-code", "documentation"],
                    'relatedTasks': [knowledge["url"]]
                })
        
        print(f"✅ {sum(len(k['commands']) for k in extracted_knowledge)}個のコマンドをメモリバンクに追加")
        print(f"✅ {sum(len(k['key_points']) for k in extracted_knowledge)}個のキーポイントを追加")
        
        # インデックスファイル生成
        print("\n📚 完全マニュアルインデックス生成中...")
        index_content = """# Claude Code 完全マニュアル

## 🎯 このマニュアルについて

Claude Code公式ドキュメントから抽出した**完全なコンテンツ**を含むマニュアルです。
要約や省略なしで、すべての情報が保持されています。

## 📖 利用可能なページ

"""
        
        for knowledge in extracted_knowledge:
            index_content += f"### [{knowledge['title']}]({knowledge['url'].split('/')[-1]}_complete.md)\n"
            index_content += f"- **コマンド数**: {len(knowledge['commands'])}\n"
            index_content += f"- **主要トピック**: {', '.join(knowledge['key_points'][:3])}\n\n"
        
        index_content += """
## 🔍 検索のヒント

1. **コマンドを探す**: `claude`、`npm`、`curl`で検索
2. **設定を探す**: `config`、`settings`、`環境変数`で検索
3. **トラブルシューティング**: `エラー`、`問題`、`解決`で検索

## 💡 活用方法

- **初心者**: クイックスタートから始める
- **開発者**: CLIリファレンスとスラッシュコマンドを参照
- **トラブル時**: トラブルシューティングセクションを確認
"""
        
        await file_manager.execute(
            action="write_file",
            path="manuals/INDEX.md",
            content={"title": "Claude Code Complete Manual Index", "body": index_content}
        )
        
        print("✅ 完全マニュアルインデックス生成完了")
        
    finally:
        await fetcher.close()
    
    print("\n" + "="*60)
    print("🎉 完全コンテンツ抽出完了！")
    print(f"📁 出力先: generated_contexts/claude-code-complete/manuals/")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(extract_full_content())