#!/usr/bin/env python3
"""Claude Code公式ドキュメントのコンテキスト抽出スクリプト"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from yaml_context_engineering.config import Config
from yaml_context_engineering.tools import (
    WebContentFetcher,
    LLMStructureExtractor,
    URLDiscoveryEngine,
    FileSystemManager
)


async def extract_claude_code_docs():
    """Claude Code公式ドキュメントから階層的コンテキストを抽出"""
    
    print("""
╔════════════════════════════════════════════════════════════╗
║       Claude Code ドキュメント コンテキスト抽出           ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    # Claude Codeドキュメントの主要URL
    claude_docs_urls = [
        "https://docs.anthropic.com/ja/docs/claude-code/overview",
        "https://docs.anthropic.com/ja/docs/claude-code/quickstart",
        "https://docs.anthropic.com/ja/docs/claude-code/common-workflows",
        "https://docs.anthropic.com/ja/docs/claude-code/mcp",
        "https://docs.anthropic.com/ja/docs/claude-code/sdk",
        "https://docs.anthropic.com/ja/docs/claude-code/hooks",
        "https://docs.anthropic.com/ja/docs/claude-code/github-actions",
        "https://docs.anthropic.com/ja/docs/claude-code/troubleshooting",
        "https://docs.anthropic.com/ja/docs/claude-code/cli-reference",
        "https://docs.anthropic.com/ja/docs/claude-code/interactive-mode",
        "https://docs.anthropic.com/ja/docs/claude-code/slash-commands",
        "https://docs.anthropic.com/ja/docs/claude-code/settings"
    ]
    
    # 設定を初期化
    config = Config.from_env()
    config.output.output_base_directory = Path("generated_contexts/claude-code-full")
    
    # ツールを初期化
    fetcher = WebContentFetcher(config)
    extractor = LLMStructureExtractor(config)
    discovery = URLDiscoveryEngine(config)
    file_manager = FileSystemManager(config)
    
    # 出力ディレクトリを作成
    await file_manager.execute(
        action="create_directory",
        path="",
        content={
            "overview": {},
            "getting-started": {},
            "building": {},
            "deployment": {},
            "administration": {},
            "configuration": {},
            "reference": {},
            "resources": {}
        }
    )
    
    all_contexts = []
    
    try:
        for url in claude_docs_urls:
            print(f"\n📄 処理中: {url}")
            print("="*60)
            
            # URLからセクション名を抽出
            url_parts = url.split('/')
            section_name = url_parts[-1] if url_parts else 'unknown'
            
            # カテゴリを決定
            if 'overview' in section_name or 'quickstart' in section_name:
                category = 'getting-started'
            elif any(x in section_name for x in ['mcp', 'sdk', 'hooks', 'github']):
                category = 'building'
            elif any(x in section_name for x in ['cli', 'interactive', 'slash', 'commands']):
                category = 'reference'
            elif 'settings' in section_name:
                category = 'configuration'
            else:
                category = 'overview'
            
            print(f"📁 カテゴリ: {category}")
            
            # Step 1: コンテンツを取得
            print("  1️⃣ コンテンツ取得中...")
            fetch_results = await fetcher.fetch([url], timeout=60)
            
            if not fetch_results or not fetch_results[0].get("success"):
                print(f"  ❌ 取得失敗: {url}")
                continue
            
            content = fetch_results[0].get("content", "")
            title = fetch_results[0].get("title", section_name)
            print(f"  ✅ {len(content)} 文字を取得")
            
            # Step 2: 構造を抽出
            print("  2️⃣ 階層構造を抽出中...")
            structure = await extractor.extract(
                content,
                extraction_config={
                    "granularity": "full_hierarchy",
                    "summarization": "detailed"
                }
            )
            
            headings_count = structure.get("total_headings", 0)
            confidence = structure.get("confidence_score", 0)
            print(f"  ✅ {headings_count} 個の見出しを抽出 (信頼度: {confidence:.2f})")
            
            # Step 3: 関連URLを発見
            print("  3️⃣ 関連URL発見中...")
            discovered_urls = await discovery.discover(content, "docs.anthropic.com")
            internal_urls = [u for u in discovered_urls if u['relation_type'] == 'internal']
            print(f"  ✅ {len(internal_urls)} 個の内部リンクを発見")
            
            # Step 4: コンテキストファイルを生成
            print("  4️⃣ コンテキストファイル生成中...")
            
            # 階層構造を文字列に変換
            def format_headings(headings, indent=0):
                result = []
                for h in headings:
                    prefix = "  " * indent
                    result.append(f"{prefix}- **L{h['level']}**: {h['text']}")
                    if h.get('children'):
                        result.extend(format_headings(h['children'], indent + 1))
                return result
            
            structured_headings = structure.get("structured_headings", [])
            hierarchy_text = "\n".join(format_headings(structured_headings))
            
            # コンテキストドキュメントを作成
            context_body = f"""# {title}

## 📌 概要

**ソースURL**: {url}
**抽出日時**: {datetime.now().isoformat()}
**見出し数**: {headings_count}
**信頼度**: {confidence:.2f}

## 📊 階層構造

{hierarchy_text if hierarchy_text else "階層構造が見つかりませんでした"}

## 📝 コンテンツサマリー

{structure.get('content_summary', 'サマリーなし')}

## 🔗 関連リンク

"""
            # 上位10個の関連URLを追加
            for url_info in internal_urls[:10]:
                context_body += f"- [{url_info['url'].split('/')[-1]}]({url_info['url']})\n"
            
            if not internal_urls:
                context_body += "関連リンクが見つかりませんでした\n"
            
            # 抽出されたエンティティを追加
            entities = structure.get('extracted_entities', {})
            if entities.get('key_terms'):
                context_body += f"\n## 🏷️ キーワード\n\n"
                context_body += ", ".join(entities['key_terms'][:20])
                context_body += "\n"
            
            # ファイルに保存
            file_path = f"{category}/{section_name}.md"
            result = await file_manager.execute(
                action="write_file",
                path=file_path,
                content={
                    "title": title,
                    "source_url": url,
                    "language": "ja",
                    "content_type": "documentation",
                    "extraction_confidence": confidence,
                    "hierarchy_levels": structure.get("hierarchy_levels", []),
                    "tags": ["claude-code", category, section_name],
                    "body": context_body
                }
            )
            
            if result.get("success"):
                print(f"  ✅ 保存完了: {file_path}")
                all_contexts.append({
                    "title": title,
                    "path": file_path,
                    "url": url,
                    "category": category,
                    "headings": headings_count,
                    "confidence": confidence
                })
            else:
                print(f"  ❌ 保存失敗: {result.get('error')}")
        
        # 全体のインデックスを生成
        print("\n" + "="*60)
        print("📚 インデックス生成中...")
        
        index_body = """# Claude Code ドキュメント - 完全コンテキスト

このディレクトリには、Claude Code公式ドキュメントから抽出された階層的コンテキストが含まれています。

## 📁 カテゴリ別インデックス

"""
        
        # カテゴリ別にグループ化
        by_category = {}
        for ctx in all_contexts:
            if ctx['category'] not in by_category:
                by_category[ctx['category']] = []
            by_category[ctx['category']].append(ctx)
        
        category_names = {
            'getting-started': '🚀 はじめに',
            'building': '🛠️ 構築',
            'deployment': '🚢 デプロイメント',
            'administration': '🔧 管理',
            'configuration': '⚙️ 設定',
            'reference': '📖 リファレンス',
            'resources': '📚 リソース',
            'overview': '📋 概要'
        }
        
        for category, contexts in sorted(by_category.items()):
            index_body += f"\n### {category_names.get(category, category)}\n\n"
            for ctx in contexts:
                index_body += f"- [{ctx['title']}]({ctx['path']}) - "
                index_body += f"{ctx['headings']}個の見出し (信頼度: {ctx['confidence']:.2f})\n"
        
        index_body += f"""

## 📊 統計情報

- **総ドキュメント数**: {len(all_contexts)}
- **総見出し数**: {sum(ctx['headings'] for ctx in all_contexts)}
- **平均信頼度**: {sum(ctx['confidence'] for ctx in all_contexts) / len(all_contexts) if all_contexts else 0:.2f}
- **抽出日時**: {datetime.now().isoformat()}

## 🔍 使用方法

各ファイルは以下の構造を持っています：

1. **YAMLフロントマター**: メタデータと階層情報
2. **階層構造**: L1〜L6レベルの見出し構造
3. **コンテンツサマリー**: 主要内容の要約
4. **関連リンク**: 発見された関連ドキュメント
5. **キーワード**: 抽出された重要用語

これらのコンテキストファイルは、Claude Codeのインタラクティブマニュアル作成、
ドキュメント検索システム、ヘルプボットなどの構築に活用できます。
"""
        
        # インデックスを保存
        await file_manager.execute(
            action="write_file",
            path="README.md",
            content={
                "title": "Claude Code Documentation Context Index",
                "generated_at": datetime.now().isoformat(),
                "total_documents": len(all_contexts),
                "body": index_body
            }
        )
        
        print("✅ インデックス生成完了")
        
        # サマリーを表示
        print("\n" + "="*60)
        print("✨ 抽出完了！")
        print("="*60)
        print(f"\n📊 結果サマリー:")
        print(f"  - 処理したURL: {len(all_contexts)}/{len(claude_docs_urls)}")
        print(f"  - 生成したコンテキストファイル: {len(all_contexts)}")
        print(f"  - 出力ディレクトリ: generated_contexts/claude-code-full/")
        print(f"  - インデックスファイル: generated_contexts/claude-code-full/README.md")
        
    finally:
        await fetcher.close()


if __name__ == "__main__":
    asyncio.run(extract_claude_code_docs())